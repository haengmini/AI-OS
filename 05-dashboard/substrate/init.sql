-- Agent OS Coordination Substrate — init.sql  (Work Item P1-#13)
-- 정본 설계: 05-dashboard/situation-room/docs/agent-os-coordination-substrate-2026-06-23.md
-- 멱등(idempotent): 여러 번 실행해도 안전.

CREATE EXTENSION IF NOT EXISTS vector;          -- 메모리 겸용(pgvector)

DO $$ BEGIN
  CREATE TYPE task_status AS ENUM ('todo','ready','running','blocked','review','done');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS tasks (
  task_id      text PRIMARY KEY,                -- Notion↔Hermes↔Drive 공통 키(척추)
  board        text NOT NULL,                   -- agent-os | dfxisp | ai-drone
  project      text,
  title        text NOT NULL,
  status       task_status NOT NULL DEFAULT 'todo',
  owner_agent  text,                            -- Hermes/워커 소유
  priority     int  DEFAULT 2,                  -- 사람(Notion) 소유 (0=P0,1=P1,2=P2)
  approval     text DEFAULT 'none',             -- none|approved|rejected (사람/Notion 소유)
  inputs       jsonb DEFAULT '[]',
  outputs      jsonb DEFAULT '[]',              -- drive_file_id 등
  next_agent   text,
  heartbeat_at timestamptz,                     -- Hermes/워커 소유
  created_at   timestamptz DEFAULT now(),
  updated_at   timestamptz DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_tasks_queue ON tasks (status, priority, created_at);

-- updated_at 자동 갱신
CREATE OR REPLACE FUNCTION touch_updated() RETURNS trigger AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS trg_touch ON tasks;
CREATE TRIGGER trg_touch BEFORE UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION touch_updated();

-- 상태/담당 바뀌면 담당 에이전트 채널로 push (폴링 대신 이벤트 깨우기)
CREATE OR REPLACE FUNCTION notify_task() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('agent_'||COALESCE(NEW.owner_agent,'unassigned'),
    json_build_object('task_id',NEW.task_id,'status',NEW.status)::text);
  RETURN NEW;
END $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS trg_notify ON tasks;
CREATE TRIGGER trg_notify AFTER INSERT OR UPDATE OF status, owner_agent ON tasks
  FOR EACH ROW EXECUTE FUNCTION notify_task();

-- 레이스-프리 claim: 한 번 호출로 ready→running 점유 (동시 워커가 같은 작업 못 집음)
CREATE OR REPLACE FUNCTION claim_task(p_agent text)
RETURNS tasks AS $$
DECLARE t tasks;
BEGIN
  SELECT * INTO t FROM tasks
    WHERE status='ready' AND owner_agent=p_agent
    ORDER BY priority, created_at
    FOR UPDATE SKIP LOCKED LIMIT 1;
  IF NOT FOUND THEN RETURN NULL; END IF;
  UPDATE tasks SET status='running', heartbeat_at=now()
    WHERE task_id=t.task_id RETURNING * INTO t;
  RETURN t;
END $$ LANGUAGE plpgsql;

-- 핸드오프 헬퍼: 현재 작업 done + 다음 작업 ready(=next_agent 깨움)
CREATE OR REPLACE FUNCTION handoff(p_task text, p_next_task text DEFAULT NULL)
RETURNS void AS $$
BEGIN
  UPDATE tasks SET status='done' WHERE task_id=p_task;
  IF p_next_task IS NOT NULL THEN
    UPDATE tasks SET status='ready' WHERE task_id=p_next_task;
  END IF;
END $$ LANGUAGE plpgsql;
