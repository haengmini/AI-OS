#!/usr/bin/env bash
# Agent OS Cockpit 실행 (Hermes). substrate의 PG_PW 재사용.
set -euo pipefail
cd "$(dirname "$0")"
if [ -f /opt/data/agentos-substrate/.env ]; then
  set -a; . /opt/data/agentos-substrate/.env; set +a   # PG_PW
fi
export COCKPIT_PORT="${COCKPIT_PORT:-8787}"
# psycopg2 없으면 명령창은 commands.jsonl 폴백으로 동작 (관제는 정상)
exec python3 server.py
