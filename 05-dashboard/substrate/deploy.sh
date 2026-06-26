#!/usr/bin/env bash
# Agent OS Coordination Substrate — 배포 (Hermes 서버, Docker)
# 멱등: 다시 돌려도 안전. init.sql은 IF NOT EXISTS/OR REPLACE.
set -euo pipefail
cd "$(dirname "$0")"

[ -f .env ] || { echo "[!] .env 없음 → cp .env.example .env 후 PG_PW 설정"; exit 1; }
set -a; . ./.env; set +a
[ "${PG_PW:-}" = "change-me-to-a-strong-password" ] && { echo "[!] PG_PW 기본값 그대로임 — 바꾸세요"; exit 1; }

docker compose up -d --wait        # healthcheck 통과까지 대기 (수동 루프 불필요, bind dir은 docker가 생성)

echo "[*] 스키마 적용 (init.sql)"
docker exec -i agentos-pg psql -U postgres -d agentos -v ON_ERROR_STOP=1 < init.sql

echo "[ok] substrate 기동 완료. 스모크 테스트: ./smoke.sh"
