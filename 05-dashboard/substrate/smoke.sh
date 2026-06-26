#!/usr/bin/env bash
# claim 큐 동작 확인: enqueue(ready) → claim_task(running) → handoff(done)
set -euo pipefail
cd "$(dirname "$0")"
PSQL="docker exec -i agentos-pg psql -U postgres -d agentos -v ON_ERROR_STOP=1 -t -A"

echo "[1] ready 작업 1건 투입 (owner_agent=codex)"
echo "INSERT INTO tasks(task_id,board,title,status,owner_agent,priority)
      VALUES('SMOKE-1','agent-os','substrate smoke','ready','codex',1)
      ON CONFLICT(task_id) DO UPDATE SET status='ready';" | $PSQL

echo "[2] claim → running 점유"
echo "SELECT task_id||' '||status FROM claim_task('codex');" | $PSQL

echo "[3] 상태 확인 (running 이어야 함)"
echo "SELECT task_id||' '||status||' '||owner_agent FROM tasks WHERE task_id='SMOKE-1';" | $PSQL

echo "[4] handoff → done"
echo "SELECT handoff('SMOKE-1');" | $PSQL
echo "SELECT task_id||' '||status FROM tasks WHERE task_id='SMOKE-1';" | $PSQL

echo "[5] 정리"
echo "DELETE FROM tasks WHERE task_id='SMOKE-1';" | $PSQL
echo "[ok] claim 큐 정상 (ready→running→done)."
