# Coordination Substrate — 배포 키트

task_id 척추 + 레이스-프리 claim 큐 + 이벤트 깨우기(Postgres). 30분 Drive 폴링을 대체하는 근실시간 버스.
정본 설계: `../situation-room/docs/agent-os-coordination-substrate-2026-06-23.md` · Work Item `P1-#13`.

## 구성
| 파일 | 역할 |
|---|---|
| `docker-compose.yml` | pgvector/pgvector:pg16, 로컬(127.0.0.1:5432) 바인딩 |
| `init.sql` | tasks 테이블 + claim_task() + notify 트리거 + handoff() (멱등) |
| `.env.example` | `PG_PW` (복사해서 `.env`로, secret은 비공개) |
| `deploy.sh` | compose up + init.sql 적용 |
| `smoke.sh` | ready→running→done 동작 확인 |
| `claim_worker.py` | LISTEN/NOTIFY 레퍼런스 워커 (폴링 없음) |

## 배포 (Hermes 서버)
```bash
# 정본을 Hermes 실행 위치로
mkdir -p /opt/data/agentos-substrate
cp /opt/data/agent_os_archive/files/05-dashboard/substrate/* /opt/data/agentos-substrate/
cd /opt/data/agentos-substrate

cp .env.example .env && nano .env       # PG_PW 강력하게 설정
chmod +x deploy.sh smoke.sh
./deploy.sh                              # 기동 + 스키마
./smoke.sh                              # 검증
```

## 사용 흐름
1. 에이전트는 `LISTEN agent_<name>` 상시 대기 → push 오면 즉시 `claim_task('<name>')`.
2. 작업 끝 = `SELECT handoff('<task>', '<next_task>')` → next_agent 깨움.
3. 사람 필드(priority/approval)는 Notion, 기계 필드(status/owner/outputs)는 워커, 문서는 Drive.

## 다음
- `#14` 대시보드/registry가 이 테이블을 읽음 (HQ 대시보드 데이터 소스를 JSON→Postgres로 승격 가능).
- `#15` Notion 승인(webhook) → `tasks.approval='approved'` → 큐 ready.
