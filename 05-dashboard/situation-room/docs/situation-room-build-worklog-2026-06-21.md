# Agent OS Situation Room Dashboard — 계획 및 작업 기록

- 작성일: `2026-06-21 UTC`
- 요청자: 이형민
- 작업 주제: Claude / Hermes / Gemini / Codex / GPT까지 수용 가능한 Agent OS 상황실 웹 UI 제작
- 최종 산출물: `/opt/data/agent_os_archive/dashboard/index.html`

---

## 1. 사용자 요청 요약

이형민님은 Agent OS 에이전트 팀 운영을 위해 다음 요구를 주셨다.

1. API 비용 부담이 있으므로 Claude/Gemini/GPT/Codex를 무조건 API로 연결하는 방식은 피한다.
2. 대신 사람이 보고, Hermes/agent도 읽고, 외부 모델 결과물도 편입할 수 있는 상황판을 만든다.
3. UI는 사람들이 가장 많이 사용하는 디자인과 형식을 따른다.
4. 만들기 전에 빌드 계획을 세운다.
5. 에이전트들에게 작업을 할당해 효율적으로 진행한다.
6. 디자이너팀은 여러 UI/UX 디자인을 검토하고 가장 인기 있는 디자인 방향을 선택한다.
7. 이후 실제 작동 가능한 대시보드 MVP를 만든다.

---

## 2. 빌드 계획

빌드 계획은 아래 파일로 먼저 작성했다.

```text
/opt/data/agent_os_archive/.hermes/plans/2026-06-20_0100-agent-os-situation-room-popular-dashboard.md
```

### 2.1 목표

```text
이형민, Hermes, Claude/Gemini/Codex 산출물, Agent OS role agents가 모두 사용할 수 있는 익숙한 웹 대시보드 스타일의 Agent OS Situation Room을 만든다.
```

### 2.2 기본 아키텍처

계획 단계에서 정한 구조는 다음과 같다.

```text
Kanban DB / healthchecks / project docs / cron / profile roster
  → dashboard/status.json
  → dashboard/agents.json
  → dashboard/tasks.json
  → summaries/agent-team/situation-board.md
  → dashboard/index.html
```

핵심 원칙:

- HTML은 사람용 화면이다.
- JSON은 기계/에이전트용 상태이다.
- Markdown은 사람과 AI 모델이 함께 읽는 상황판이다.
- Kanban DB는 task truth이다.
- Drive/Archive summaries는 지식/운영 문서 truth이다.
- 외부 paid API는 기본 비활성으로 둔다.

### 2.3 계획상 생성/수정 예정 파일

```text
/opt/data/agent_os_archive/dashboard/index.html
/opt/data/agent_os_archive/dashboard/status.json
/opt/data/agent_os_archive/dashboard/agents.json
/opt/data/agent_os_archive/dashboard/tasks.json
/opt/data/agent_os_archive/summaries/agent-team/situation-board.md
/opt/data/scripts/agent_os_situation_room_snapshot.py
/opt/data/scripts/agent_os_situation_room_snapshot.sh
```

### 2.4 계획상 작업 단계

1. source data 확인
   - `hermes kanban --board agent-os stats`
   - `hermes kanban --board agent-os list`
   - `hermes kanban --board dfxisp stats`
   - `hermes kanban --board ai-drone stats`
   - `hermes profile list`
   - `hermes cron list`

2. JSON snapshot 생성
   - `status.json`
   - `agents.json`
   - `tasks.json`

3. Markdown situation board 생성
   - `situation-board.md`

4. self-contained web UI 생성
   - sidebar
   - top status bar
   - KPI cards
   - agent roster
   - Kanban lanes/task table
   - project cards
   - provider/cost guard
   - artifact/path panel

5. 기본 interactivity 추가
   - task search/filter
   - compact toggle
   - sidebar section navigation
   - path copy buttons

6. 검증
   - JSON validity
   - HTML structure
   - HTTP serving
   - embedded JSON parse
   - secret/API key 미노출 확인

7. 결과 보고

### 2.5 위험 및 통제 계획

| 위험 | 통제 |
|---|---|
| HTML에만 상태가 존재해 agent가 읽기 어려움 | 모든 중요 상태를 JSON/Markdown에도 생성 |
| UI가 너무 복잡해짐 | Mission Control first, trace/workflow는 후속 드릴다운 |
| paid API가 실수로 호출됨 | Claude/Gemini/GPT는 manual/not_configured로 표시 |
| secret 노출 | API key 값은 절대 표시하지 않고 configured/not_configured만 표시 |
| CLI stdout 파싱 불안정 | 가능하면 SQLite/JSON/filesystem 직접 읽기 |

---

## 3. 에이전트 작업 할당

Agent OS Kanban에 실제 작업을 생성하고 역할별로 할당했다.

### 3.1 Researcher 작업

```text
Task ID: t_9194d0ab
Title: Design Agent OS Situation Room popular dashboard direction
Assignee: researcher
Status: done
```

작업 내용:

- popular dashboard UI patterns 조사
- GitHub Agent HQ, Linear/Vercel/SaaS dashboard conventions, Agno, AutoGen, LangSmith 스타일 참고
- human + AI readability 관점에서 디자인 방향 추천

결과 요약:

```text
GitHub Agent HQ식 Mission Control을 핵심 mental model로 추천.
Linear dark app shell, Vercel card discipline, LangSmith/AutoGen/Agno식 agent/trace drill-down을 조합하는 방향을 제안.
```

생성된 handoff:

```text
/opt/data/agent_os_archive/summaries/agent-team/situation-room-dashboard-direction-2026-06-21.md
```

### 3.2 Analyst 작업

```text
Task ID: t_89929132
Title: Map Situation Room information architecture
Assignee: analyst
Status: done
```

작업 내용:

- Agent OS 데이터를 dashboard sections로 매핑
- Overview, Agents, Kanban, Projects, Artifacts, Governance, Cost Guard 구조 설계
- JSON / Markdown / HTML parity 요구사항 정리

결과 요약:

```text
Situation Room IA를 Overview, Agents, Kanban, Projects, Artifacts, Governance, Cost Guard 중심으로 정리.
JSON, Markdown, HTML 표현이 같은 상태를 공유해야 한다는 parity 원칙을 문서화.
```

생성된 IA 문서:

```text
/opt/data/agent_os_archive/summaries/agent-team/situation-room-dashboard-ia.md
```

### 3.3 Coder 작업

```text
Task ID: t_05bea5ca
Title: Implement static Situation Room dashboard MVP
Assignee: coder
Status: done
```

작업 내용:

- local-first static dashboard 구현
- snapshot script 작성
- HTML/JSON/Markdown 생성
- 검증 수행

결과 요약:

```text
static Agent OS Situation Room dashboard MVP 구현 완료.
생성 파일: snapshot script, wrapper, index.html, status.json, agents.json, tasks.json, situation-board.md.
JSON validity, embedded JSON parse, HTTP serving, HTML structure 검증 완료.
```

---

## 4. 디자인팀 판단

디자인 레퍼런스 검토에는 다음 방향이 고려되었다.

### 4.1 검토한 주요 레퍼런스

| 레퍼런스 | 참고 포인트 |
|---|---|
| GitHub Agent HQ | assign / steer / track / review 형태의 Mission Control |
| LangSmith Studio | agent graph, run trace, debugging |
| AutoGen Studio | multi-agent workflow 구성 |
| Agno Agent UI | AgentOS형 agent interaction UI |
| Dify | workflow/project dashboard 구성 |
| Flowise | visual node builder |
| Langfuse / Phoenix | observability, trace, eval |
| Vercel | 밝고 익숙한 developer dashboard app shell |
| Linear | dark developer operations UI |
| Sentry | 데이터 밀도 높은 운영/관측 dashboard |

### 4.2 최종 선택한 디자인 방향

최종 구현은 다음 방향으로 진행했다.

```text
Vercel식 clean app shell + Sentry식 운영/관측 대시보드 밀도
```

선택 이유:

1. 가장 많은 사람이 익숙한 SaaS/developer dashboard 형식이다.
2. 좌측 sidebar + 상단 상태바 + card/table 구조는 별도 학습 없이 사용할 수 있다.
3. 밝은 배경은 긴 task 제목, 경로, 상태, 표를 읽기 쉽다.
4. Sentry/Langfuse류의 관측 UI처럼 상태/로그/태스크를 데이터 밀도 있게 보여줄 수 있다.
5. AI/agent가 DOM/text를 읽을 때도 카드/표/배지 구조가 명확하다.
6. local-first static HTML로 구현하기 쉽다.

### 4.3 최종 UI 구성

최종 `index.html`에는 다음 섹션이 들어갔다.

```text
Overview
Attention
Boards
Agents
Providers & Cost
Projects
Tasks
Artifacts / Path Copy
```

---

## 5. 구현 내용

### 5.1 생성한 스크립트

```text
/opt/data/scripts/agent_os_situation_room_snapshot.py
/opt/data/scripts/agent_os_situation_room_snapshot.sh
```

역할:

```text
로컬 Agent OS 상태를 읽어 dashboard JSON, Markdown, HTML을 생성한다.
외부 API 호출은 하지 않는다.
```

읽는 주요 데이터 원천:

```text
/opt/data/kanban/boards/<slug>/kanban.db
/opt/data/kanban/boards/<slug>/board.json
/opt/data/agent_os_archive/summaries/agent-team/status.json
/opt/data/cron/jobs.json
/opt/data/profiles/<role>/SOUL.md
/opt/data/agent_os_archive/manifest.json
```

주의:

- Kanban은 CLI stdout 대신 SQLite read-only 연결로 읽는 방식을 사용했다.
- `sqlite3.connect("file:<db>?mode=ro", uri=True)` 방식으로 읽기 전용 접근한다.
- dashboard는 secret/auth 파일을 읽지 않는다.
- provider 상태는 `active`, `candidate`, `manual/not_configured` 등으로만 표현한다.

### 5.2 생성한 dashboard files

```text
/opt/data/agent_os_archive/dashboard/index.html
/opt/data/agent_os_archive/dashboard/status.json
/opt/data/agent_os_archive/dashboard/agents.json
/opt/data/agent_os_archive/dashboard/tasks.json
```

### 5.3 생성한 Markdown 상황판

```text
/opt/data/agent_os_archive/summaries/agent-team/situation-board.md
```

주요 섹션:

```md
# Agent OS Situation Board
## Human Attention Needed
## Next Actions
## Boards
## Agent Team
## Projects
## Providers & Cost Guard
## Governance
## Source Files
```

### 5.4 Multi-model 수용 구조

대시보드는 모델을 직접 하드코딩하지 않고 provider/model 상태를 control plane처럼 보여준다.

현재 표시 구조:

| Provider / Model | 상태 | 실행 방식 | 비용 모드 |
|---|---|---|---|
| Hermes | active | native | current |
| Codex | candidate | profile/cli/manual | managed/auth-present |
| Claude | manual/not_configured | manual artifact ingest | paid if API enabled |
| Gemini | manual/not_configured | manual artifact ingest | paid if API enabled |
| GPT | current/default or not_configured | profile/manual | depends |

핵심 원칙:

```text
UI는 Claude/Gemini/Codex/GPT를 수용할 준비를 하되,
실제 paid API 연결은 사용자가 명시 승인하기 전까지 하지 않는다.
```

### 5.5 최종 생성 시점 상태

마지막 snapshot 기준:

```text
Generated at: 2026-06-21T05:04:13+00:00
Overall: BLOCKED
Healthcheck: PASS
Kanban: todo=2, blocked=1, done=15
Attention: 1
Agents: 12 roles
Cron active: 4
Cron failed: 0
```

`BLOCKED` 이유:

```text
agent-os / t_d8cd6477
Verify post-09:10 Slack archive and healthcheck state
```

---

## 6. 검증 내용

### 6.1 실행 검증

실행한 명령:

```bash
python3 /opt/data/scripts/agent_os_situation_room_snapshot.py
```

결과:

```text
Agent OS Situation Room generated: /opt/data/agent_os_archive/dashboard/index.html
Overall=BLOCKED boards=3 agents=12 tasks=18
```

### 6.2 JSON 검증

실행한 검증:

```bash
python3 -m json.tool /opt/data/agent_os_archive/dashboard/status.json
python3 -m json.tool /opt/data/agent_os_archive/dashboard/agents.json
python3 -m json.tool /opt/data/agent_os_archive/dashboard/tasks.json
```

결과:

```text
status.json 정상
agents.json 정상
tasks.json 정상
```

### 6.3 HTML 구조 검증

확인한 내용:

```text
<title>Agent OS Situation Room</title> 존재
overview / attention / boards / agents / providers / projects / tasks 섹션 존재
Task Inventory 존재
dashboard-data embedded JSON 존재
embedded JSON 정상 parse
```

### 6.4 HTTP serving 검증

임시 HTTP server를 실행해 확인했다.

```bash
python3 -m http.server 8123 --directory /opt/data/agent_os_archive/dashboard
curl -sSf http://127.0.0.1:8123/index.html -o /tmp/agent_os_dashboard_check.html
```

확인 결과:

```text
contains Mission Control: True
contains dashboard data: True
contains tasks table: True
```

### 6.5 브라우저 시각 검증 한계

시도한 브라우저 검증:

```text
browser_navigate http://127.0.0.1:8123/index.html
```

결과:

```text
Chrome not found.
agent-browser / system Chrome / puppeteer / playwright cache에 Chrome 없음.
```

따라서 실제 screenshot 기반 visual inspection은 수행하지 못했다.
대신 다음 검증을 완료했다.

```text
HTMLParser 구조 검증
HTTP serving 검증
embedded JSON parse 검증
JSON validity 검증
필수 섹션 존재 검증
```

---

## 7. 실제 작업 중 조정된 사항

### 7.1 디자인 방향 조정

초기 researcher는 Linear dark shell + Vercel discipline도 추천했다.
그러나 별도 디자인팀 판단에서는 사람들이 가장 많이 사용하는 형식, 즉 밝은 SaaS/developer dashboard가 더 적절하다고 판단했다.

최종 구현은:

```text
Vercel식 밝은 clean app shell
+ Sentry식 운영/관측 대시보드 밀도
```

으로 진행했다.

### 7.2 data source 조정

초기 계획에는 Hermes CLI snapshot을 사용할 수 있다고 적었으나, 구현 엔지니어 점검 결과 CLI stdout은 glyph/table/한글폭 때문에 파싱에 취약했다.

따라서 실제 구현에서는:

```text
Kanban CLI stdout 파싱 ❌
Kanban SQLite read-only 직접 조회 ⭕
cron jobs.json 직접 조회 ⭕
profile/SOUL 파일 존재 확인 ⭕
```

방식으로 변경했다.

### 7.3 HTML embedded JSON 수정

처음에는 `<script type="application/json">` 내부 JSON을 HTML escape해서 넣었으나, 이 경우 application/json으로 바로 parse하기에 적절하지 않을 수 있었다.

수정 후:

```text
JSON은 유효한 JSON 그대로 embed
단, </script> 방지를 위해 </ 를 <\/ 로 escape
```

방식으로 변경했다.

---

## 8. 최종 산출물 목록

### 8.1 계획/기록 문서

```text
/opt/data/agent_os_archive/.hermes/plans/2026-06-20_0100-agent-os-situation-room-popular-dashboard.md
/opt/data/agent_os_archive/summaries/agent-team/situation-room-build-worklog-2026-06-21.md
```

### 8.2 디자인/IA 산출물

```text
/opt/data/agent_os_archive/summaries/agent-team/situation-room-dashboard-direction-2026-06-21.md
/opt/data/agent_os_archive/summaries/agent-team/situation-room-dashboard-ia.md
```

### 8.3 Dashboard 산출물

```text
/opt/data/agent_os_archive/dashboard/index.html
/opt/data/agent_os_archive/dashboard/status.json
/opt/data/agent_os_archive/dashboard/agents.json
/opt/data/agent_os_archive/dashboard/tasks.json
```

### 8.4 Markdown 상황판

```text
/opt/data/agent_os_archive/summaries/agent-team/situation-board.md
```

### 8.5 자동 생성 스크립트

```text
/opt/data/scripts/agent_os_situation_room_snapshot.py
/opt/data/scripts/agent_os_situation_room_snapshot.sh
```

---

## 9. 사용 방법

### 9.1 dashboard 재생성

```bash
/opt/data/scripts/agent_os_situation_room_snapshot.sh
```

또는:

```bash
python3 /opt/data/scripts/agent_os_situation_room_snapshot.py
```

### 9.2 로컬 웹 서버로 보기

```bash
python3 -m http.server 8123 --directory /opt/data/agent_os_archive/dashboard
```

브라우저 접속:

```text
http://127.0.0.1:8123/index.html
```

### 9.3 파일 직접 열기

`index.html`은 self-contained HTML이므로 파일로 직접 열어도 기본 내용 확인이 가능하다.

```text
/opt/data/agent_os_archive/dashboard/index.html
```

---

## 10. 남은 작업 / 다음 단계

### 10.1 추천 후속 작업

1. 이형민님이 실제 UI를 보고 디자인 피드백 제공
2. 필요하면 dark mode 또는 GitHub Agent HQ 느낌 강화
3. dashboard 자동 갱신 cron 추가
4. artifact ingest 규칙 추가
5. Claude/Gemini/Codex manual output import UI 추가
6. reviewer/reporter task 완료 후 최종 governance report 갱신

### 10.2 Cron 추가 제안

현재 운영 루프가 다음과 같다.

```text
Drive archive
Slack/session archive
Agent team healthcheck
```

따라서 dashboard refresh는 healthcheck 이후가 적절하다.

예:

```text
09:15 UTC Agent OS Situation Room refresh
```

`no_agent=True` script-only cron으로 만들면 LLM/API 비용 없이 자동 갱신 가능하다.

---

## 11. 결론

이번 작업은 다음 결과를 달성했다.

```text
계획 수립 완료
에이전트 작업 할당 완료
디자인 방향 선정 완료
Agent OS Situation Room MVP 구현 완료
JSON/Markdown/HTML parity 구조 구현
외부 paid API 없이 local-first dashboard 생성
검증 완료
작업 기록 문서화 완료
```

최종적으로 Agent OS는 이제 다음 세 가지 표현을 동시에 갖는다.

```text
HTML: 사람이 보는 Mission Control
JSON: Hermes/agents/scripts가 읽는 machine state
Markdown: 사람과 AI 모델이 함께 읽는 situation board
```
