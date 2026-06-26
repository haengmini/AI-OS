---
title: Agent OS — Coordination Substrate (task_id + claim queue)
task: P1 #13
created: 2026-06-23
owner: 이형민
status: design-ready
note: 배포는 Hermes 서버(Docker). 이 문서 = 설계 + DDL + compose. ponytail 기준 최소 구성.
---

# Coordination Substrate — task_id 척추 + claim 큐

## 왜
Drive 폴링 + 단일 JSON 덮어쓰기로는 근실시간 핸드오프가 안 되고 레이스가 난다. **Postgres 1개**로 task_id 척추 + 레이스-프리 claim 큐 + 이벤트 깨우기. Notion(사람)·대시보드는 이 위에 얹히고, Drive는 문서 정본 유지.

## 위치
Hermes 서버 Docker. `[[agent-os-canonical-roadmap-2026-06-23]]`의 plane: **Notion(사람) ─ Postgres/Hermes(기계) ─ Drive(문서)**.

## task_id 척추
단일 `task_id`가 Notion↔Hermes↔Drive 공통 조인키. 모든 레코드·아티팩트가 이 키로 묶인다.

## DDL (Postgres + pgvector)
```sql
CREATE EXTENSION IF NOT EXISTS vector;   -- 메모리 겸용(pgvector)
CREATE TYPE task_status AS ENUM ('todo','ready','running','blocked','review','done');

CREATE TABLE tasks (
  task_id      text PRIMARY KEY,          -- 공통 키
  board        text NOT NULL,             -- agent-os|dfxisp|ai-drone
  project      text,
  title        text NOT NULL,
  status       task_status NOT NULL DEFAULT 'todo',
  owner_agent  text,                      -- Hermes 소유
  priority     int  DEFAULT 2,            -- 사람(Notion) 소유
  approval     text DEFAULT 'none',       -- none|approved|rejected (사람/Notion 소유)
  inputs       jsonb DEFAULT '[]',
  outputs      jsonb DEFAULT '[]',        -- drive_file_id 등
  next_agent   text,
  heartbeat_at timestamptz,               -- Hermes 소유
  created_at   timestamptz DEFAULT now(),
  updated_at   timestamptz DEFAULT now()
);
CREATE INDEX ON tasks (status, priority, created_at);

-- 상태/담당 바뀌면 담당 에이전트 채널로 push (폴링 대신)
CREATE FUNCTION notify_task() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('agent_'||COALESCE(NEW.owner_agent,'unassigned'),
                    json_build_object('task_id',NEW.task_id,'status',NEW.status)::text);
  RETURN NEW;
END $$ LANGUAGE plpgsql;
CREATE TRIGGER trg_notify AFTER INSERT OR UPDATE OF status, owner_agent ON tasks
  FOR EACH ROW EXECUTE FUNCTION notify_task();
```

## 레이스-프리 claim
```sql
BEGIN;
SELECT * FROM tasks
 WHERE status='ready' AND owner_agent=$1
 ORDER BY priority, created_at
 FOR UPDATE SKIP LOCKED LIMIT 1;          -- 동시 워커가 같은 작업 못 집음
-- → 잡았으면: UPDATE status='running', heartbeat_at=now()
COMMIT;
```

## 핸드오프
작업 끝 = `status='done'` + 다음 작업 `INSERT/UPDATE (owner_agent=next_agent, status='ready')` → 트리거가 그 에이전트를 깨움.

## 필드 소유권 (단일 writer)
| 필드 | writer |
|---|---|
| title, priority, approval | 사람 / Notion |
| status, owner_agent, heartbeat_at, outputs | Hermes/워커 |
| 문서 본문 | Drive |

## docker-compose (최소)
```yaml
services:
  pg:
    image: pgvector/pgvector:pg16
    environment: { POSTGRES_PASSWORD: ${PG_PW}, POSTGRES_DB: agentos }
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["/opt/data/pg:/var/lib/postgresql/data"]
```

## 에이전트 사용 흐름
1. `LISTEN agent_<name>` (상시) — push 받으면 즉시 claim. 폴링 없음.
2. NOTIFY는 *연결된* 리스너에만 가므로, Hermes가 5분 sweep로 놓친 ready 작업 재공지(안전망).
3. claim → 작업 → outputs에 drive_file_id 기록 → done + next 작업 ready.

## 배포 (Hermes, 사람 손)
```bash
cd /opt/data/agentos-substrate   # compose + init.sql 배치
docker compose up -d
psql "postgresql://postgres:$PG_PW@127.0.0.1/agentos" -f init.sql
```

## 다음
이 위에 #14 대시보드/registry(읽기), #15 Notion 3-DB(사람 필드 동기화, 승인 webhook→이 큐)를 얹는다.
