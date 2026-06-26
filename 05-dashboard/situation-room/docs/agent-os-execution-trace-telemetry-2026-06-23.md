---
title: Agent OS — Execution Trace + Cost/Usage Telemetry
task: P1 #16
created: 2026-06-23
owner: 이형민
status: design-ready
note: substrate(#13) Postgres 위에 얹음. 24/7 안전 전제(추적+비용 가드). 배포는 Hermes.
---

# Execution Trace + Cost/Usage Telemetry

## 왜
24/7 자율 루프의 두 안전장치: ① 모든 에이전트 실행을 **추적**(누가·어떤 모델·얼마·성공?), ② paid 모델 **비용 가드**(승인 없는 폭주 차단). registry의 `cost_mode` + substrate `tasks`와 연결.

## 1. 실행 추적 표준 (runs 테이블, substrate에 추가)
모든 에이전트 행동 = 시작 시 row insert(status=started) → 종료 시 update(ok/error, tokens, cost). Hermes-local 작업도 추적(cost=0), paid(claude/codex)는 tokens·cost 기록.
```sql
CREATE TYPE run_status AS ENUM ('started','ok','error','timeout','cancelled');
CREATE TABLE runs (
  run_id     bigserial PRIMARY KEY,
  task_id    text REFERENCES tasks(task_id),   -- spine 연결
  agent      text NOT NULL,                     -- agent-registry agent_id
  model      text,                              -- model-registry model_id
  provider   text,                              -- anthropic|openai|google|hermes|...
  cost_mode  text,                              -- local|manual|paid|unknown
  tool       text,
  started_at timestamptz DEFAULT now(),
  ended_at   timestamptz,
  tokens_in  int DEFAULT 0,
  tokens_out int DEFAULT 0,
  cost_usd   numeric(10,4) DEFAULT 0,           -- paid만 계상, local=0
  status     run_status DEFAULT 'started',
  error      text
);
CREATE INDEX ON runs (task_id);
CREATE INDEX ON runs (model, started_at);
```

## 2. 비용/사용량 롤업
```sql
CREATE VIEW cost_daily AS
SELECT date_trunc('day',started_at) AS day, model, provider,
       count(*) AS runs, sum(tokens_in) AS tin, sum(tokens_out) AS tout,
       round(sum(cost_usd),4) AS cost
FROM runs GROUP BY 1,2,3 ORDER BY 1 DESC, cost DESC;
```

## 3. 비용 가드 정책
```sql
CREATE TABLE cost_budget (
  scope         text PRIMARY KEY,   -- 'global' 또는 model_id
  daily_usd_cap numeric(10,2),
  action        text                -- 'alert' | 'pause_paid'
);
-- 예: ('global',5.00,'pause_paid'), ('codex',3.00,'alert')
```
규칙:
- `cost_mode='paid'` 모델은 model-registry `status='available'`일 때만 실행. gemini/chorus = not_configured → 실행 차단(승인 시 available).
- `cost_daily.cost > cap` → sentinel가 Slack 경보 + action='pause_paid'면 신규 paid run을 승인 게이트(Approvals)로 보냄.
- local/Hermes run은 cost=0, cap 없음.

## 4. 정체/오류 감지 (heartbeat)
`tasks.heartbeat_at`(substrate) + `runs.status='started' AND ended_at IS NULL AND started_at < now()-interval '15 min'` → 좀비 run → sentinel 알림.

## 5. Hermes 롤업 cron (무료)
```
0 9 * * *  cost_daily 조회 → Health DB "Cost/Usage <date>" 행 upsert + cap 초과 시 Slack.
```
runs 기록은 각 에이전트/워커가 substrate에 직접 insert(추적은 상시), 집계만 cron.

## 6. Notion 노출
- Health DB에 **Cost Guard** 행(현재 정책 상태). 일일 비용은 cron이 Health "Cost/Usage <date>"로 갱신.
- 폭주 시 Approvals에 "paid run 승인 요청" 행 생성(사람 결정).

## 배포
substrate init.sql에 위 runs/view/cost_budget 추가 → `docker compose` 재적용. 에이전트 wrapper가 run insert/update 호출(작은 헬퍼).

## 연결
- registry: `situation-room/state/{agent,model}-registry.json` (cost_mode)
- substrate: `[[agent-os-coordination-substrate-2026-06-23]]` (tasks/task_id)
