# Agent OS Cockpit — 자체 호스팅 통합 GUI

관제(에이전트·태스크·헬스·프로젝트) + 제어(명령창 → substrate 큐)를 한 화면에. 의존성 최소(stdlib http.server, 바닐라 JS).

## 구성
| 파일 | 역할 |
|---|---|
| `server.py` | stdlib HTTP 서버. `/api/state`(dashboard-state.json), `/api/tasks`(substrate), `POST /api/command`(큐 투입) |
| `index.html` | 콕핏 UI (다크). 15초 자동 새로고침 |
| `run.sh` | 실행 래퍼 (substrate `.env`의 PG_PW 재사용) |

## 동작
- **관제:** `dashboard-state.json`을 Drive(신선)에서 읽고, 안 되면 로컬 미러로 fallback. substrate `tasks`도 함께.
- **제어/소통:** 명령창 → `POST /api/command` → `tasks`에 `(owner_agent, status='ready', priority=0)` 투입 → `notify_task` 트리거가 담당 에이전트 깨움 → claim/handoff. **LLM 챗봇이 아니라 명령·핸드오프 채널.** substrate 미배포 시 `commands.jsonl`로 폴백.

## 배포 (Hermes)
```bash
mkdir -p /opt/data/agentos-cockpit
cp /opt/data/agent_os_archive/files/05-dashboard/cockpit/* /opt/data/agentos-cockpit/
cd /opt/data/agentos-cockpit
chmod +x run.sh
./run.sh                      # http://127.0.0.1:8787
```
psycopg2 필요(명령창·tasks): `pip install psycopg2-binary`. 관제만이면 없어도 뜸.

## 접근 (127.0.0.1 바인딩 — 외부 비노출)
로컬 PC에서 SSH 터널:
```bash
ssh -L 8787:127.0.0.1:8787 <hermes>
# 브라우저: http://localhost:8787
```

## 상시 실행 (systemd, 선택)
```ini
# /etc/systemd/system/agentos-cockpit.service
[Unit]
Description=Agent OS Cockpit
After=network.target docker.service
[Service]
WorkingDirectory=/opt/data/agentos-cockpit
EnvironmentFile=/opt/data/agentos-substrate/.env
ExecStart=/usr/bin/python3 server.py
Restart=on-failure
[Install]
WantedBy=multi-user.target
```
`systemctl enable --now agentos-cockpit`

## v2 (다음)
- Notion Approvals 패널(승인 버튼 → `tasks.approval`).
- 실제 LLM 챗 탭(Gemini/Claude 키) — 명령 채널과 분리.
- 데이터 소스를 JSON→substrate `tasks`로 일원화.
