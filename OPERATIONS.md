# OPERATIONS.md — Agent OS 운영 런북 (v0.1)

> README는 "무엇/왜"의 정본, 이 파일은 "어떻게 돌리는가"의 런북. **짧게 유지.**
> 새 헌법이 아니다 — 매일 돌아가는 최소 루프만 적는다. (2026-06-25, ponytail MVP 고정)

## 한 줄 방향
"AI 회사 전체 운영체계를 설계하자" → **"매일 볼 수 있는 HQ 상황판 하나를 확실히 작동시키자."**
DFXISP 같은 진짜 작업은 Agent OS를 계속 만드는 데 쓰지 말고, 이 간단한 HQ 위에서 굴린다.

## Backend = 상태를 모으는 스크립트
```text
1. Drive mirror        (/opt/data/agent_os_archive)        — Drive-first 정본 미러
2. Kanban / project state                                  — 작업 상태
3. healthcheck         agent_team_healthcheck.sh           — PASS/FAIL
4. dashboard generator build_dashboard.py                  — 상태 → JSON+HTML (정본 generator 1개)
```

## Frontend = 그 상태를 보여주는 화면 (정본 3개, 이것만)
```text
HTML : 05-dashboard/hq-dashboard.html        ← 매일 더블클릭으로 여는 화면
JSON : 05-dashboard/agent-dashboard.json     ← 단일 상태 계약
GEN  : 05-dashboard/build_dashboard.py        ← 위 둘을 생성/갱신
```
`hq-dashboard.html`은 데이터를 인라인 임베드한다 → **파일 더블클릭만으로 열린다(서버 불필요).**
서빙 환경이면 `agent-dashboard.json`을 fetch해 자동으로 최신화한다.

생성/갱신:
```bash
cd .../05-dashboard
python3 build_dashboard.py --src situation-room/state \
  --out agent-dashboard.json --html hq-dashboard.html [--cron live_cron.json]
```

## Command Center — 에이전트 지휘 (`hq-dashboard.html`)
탭 4개 단일 페이지: **Overview**(상태) · **Console**(채팅+작업 디스패치) · **Agents** · **Kanban**.
두 가지 모드:
```text
① local mode (기본)  : 서버 없이 더블클릭만으로 동작.
                       - 채팅: 대시보드 데이터에 즉답(상태/cron/dfxisp/막힌/에이전트…)
                       - 디스패치: 작업을 브라우저 localStorage에 staged (Kanban 'staged(나)' 열)
② live mode          : Hermes 브리지 연결 → 채팅·작업이 실제 Hermes로.
```
live 연결:
```bash
# WSL에서 브리지 실행 (의존성 0, 로컬 전용). /chat 과 /task 라우팅.
cd .../05-dashboard
python3 agent_bridge.py --state agent-dashboard.json --outbox tasks_outbox.jsonl --port 8765
# → 대시보드 ⚙ 클릭 → base URL 입력:  http://localhost:8765
```
작업 디스패치 흐름(부작용 없는 기본): Console에서 board·owner·model·priority·title 입력 → ▸디스패치
→ 브리지가 `tasks_outbox.jsonl`에 append → **Hermes/Codex가 outbox를 소비**해 실제 Kanban 카드 생성.
실제 즉시 생성을 원하면 `agent_bridge.py`의 `route_to_hermes_task()` 훅에 kanban CLI 한 줄만 넣으면 된다
(자유 대화는 `route_to_hermes_chat()` 훅). 그 전엔 안전하게 outbox/status로 폴백.
채팅 히스토리·엔드포인트 설정은 브라우저 localStorage에 저장된다.

## Frozen (삭제 아님, 보류) — 나머지 dashboard 파일
```text
situation-room/ui/index.html, agent-dashboard.html      → legacy, frozen
situation-room/state/{status,tasks,agents,...}.json     → generator의 source로만 사용
agent_os_situation_room_snapshot.py (424줄)             → build_dashboard.py로 대체, frozen
agent_dashboard_snapshot.py (338줄)                     → 통합됨, frozen
05-dashboard/dashboard-state.json                        → frozen
```

## Deferred (지금 필요 없음 — YAGNI)
```text
Postgres substrate · Cockpit server · Notion bridge · 자동 멀티모델 라우팅
Slack daily LLM archive (429 동안 저빈도/비활성)
```

## v0.1 완료 조건 (이거 5개면 충분)
```text
1. Drive sync가 매일 성공한다.            [현재 FAIL — drive-archive 권한오류]
2. healthcheck가 PASS 나온다.             [PASS]
3. 대시보드 HTML 하나로 상태가 보인다.     [DONE — hq-dashboard.html]
4. DFXISP 다음 행동 1~3개가 명확하다.      [DONE — next_actions]
5. Slack 명령 → Hermes가 상태를 갱신한다.  [미검증 — Slack daily-archive(429)와 별개 경로로 평가]
```
> ⚠️ #5 주의: Slack **명령 입력**(가벼움)과 Slack **daily archive**(채널 전체 LLM 요약 = 429 원인)는
> 다른 경로다. archive를 보류해도 #5는 살아있을 수 있다. 둘을 분리해 판단한다.

## 지금 막힌 것 = 운영 배관 (AI 설계 아님)
```text
[P0] agent-os-drive-daily-archive   — Permission denied  → 먼저 수정 (완료조건 #1)
[P0] graphify-staleness-check       — Permission denied  → 먼저 수정
[P1] slack-channel-daily-archive    — HTTP 429            → 임시 저빈도/비활성
```
진단·수정 커맨드: `05-dashboard/cron-fix-guide-2026-06-25.md` 참조.

## 유지 / 멈춤 요약
```text
유지 : Drive-first, local mirror, Hermes profiles(직접 실행 최소화), Kanban,
       build_dashboard.py, hq-dashboard.{html,json}, healthcheck
멈춤 : Postgres, Cockpit, Notion bridge, 자동 멀티모델, Slack LLM archive, 중복 generator
```
