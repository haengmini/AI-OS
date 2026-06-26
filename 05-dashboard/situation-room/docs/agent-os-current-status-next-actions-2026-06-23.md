---
title: Agent OS Current Status and Next Actions
created: 2026-06-23T04:58:47+00:00
status: draft-v1
owner: 이형민
scope: Agent OS / HQ Dashboard / Reference AI Agent ecosystem / next actions
source_context:
  - /opt/data/cache/documents/doc_df6caf99a362_Reference_AIagent.txt
  - /opt/data/cache/documents/doc_c6925d5068ed_AgentOSHQdashboardvisionreport.txt
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/agent-os-hq-dashboard-vision-report-2026-06-23.md
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/agent-dashboard.md
  - /opt/data/agent_os_archive/summaries/agent-team/situation-board.md
  - /opt/data/agent_os_archive/summaries/project-portfolio.md
---

# Agent OS — 지금까지 된 것과 앞으로 해야 할 일

## 0. 한 줄 결론

Agent OS는 현재 **비전·철학·기본 운영체계·Drive archive·Slack loop·Hermes agent team·Kanban·Situation Room dashboard·DFXISP/AI드론 프로젝트 분리**까지 구축된 상태다. 다음 단계는 이것을 실제 HQ처럼 작동하게 만드는 **실행/관측/검토/보고 자동화**이다.

```text
현재 단계 = Agent OS 운영 헌법 + 상황실 뼈대 + 역할 정의 + 초기 프로젝트 보드 구축 완료
다음 단계 = HQ Dashboard v1 + Agent Registry + Notion/Slack 운영면 + Chorus review gate + Production loop 실전 투입
```

---

## 1. 지금까지 된 것

### 1.1 비전 정리 완료

사용자의 핵심 비전을 문서화했다.

- 이형민은 CEO/Owner 역할을 맡는다.
- AI agents는 직원/팀/TFT 역할을 맡는다.
- 목표는 단일 chatbot 사용이 아니라 **여러 AI 모델과 도구를 조직화한 AI-native headquarters** 구축이다.
- 활용 범위는 연구개발뿐 아니라 학습, 커리어/포트폴리오, 비즈니스/경제활동, 개인 운영까지 확장된다.
- 24/7 운영, 자가 학습, 자가 개선, 자율 운영을 장기 목표로 둔다.

관련 Drive 원본:

- `agent-os-hq-dashboard-vision-report-2026-06-23.md`
- Drive file id: `1FfWkJxkozM_Nmu7BgEE3XgQEu91NgMJz`

### 1.2 Agent OS 7-layer architecture 정리 완료

기존 `AGENT-OS.md`와 사용자의 비전이 다음 7-layer로 정리되었다.

```text
01 Hardware
→ 02 Memory
→ 03 Models
→ 04 Agents
→ 05 Dashboard + Slack
→ 06 Production
→ 07 Loop
```

각 layer의 역할도 정리되었다.

| Layer | 현재 의미 |
|---|---|
| 01 Hardware | Desktop, laptop, iPhone, Linux, Windows, iOS 등 실행/접근 환경 |
| 02 Memory | Second Brain, LLM Wiki, Obsidian, Graphify, Zotero, Drive |
| 03 Models | Claude, Codex/ChatGPT, Gemini, Hermes, future local/API models |
| 04 Agents | 역할 기반 AI 직원 조직 |
| 05 Dashboard + Slack | HQ Mission Control + 소통/승인 채널 |
| 06 Production | DFXISP, AI드론, 포트폴리오, 비즈니스, 학습 등 실제 산출물 |
| 07 Loop | 24/7 반복 운영, 자가 개선, healthcheck, archive, review |

### 1.3 Drive-first 원칙 구축 완료

현재 Agent OS는 다음 storage rule을 따른다.

```text
Google Drive = original / canonical document store
Local /opt/data = staging / cache / executable mirror
```

이미 구축된 것:

- Agent OS Drive root folder id: `1xbqGeDdLerv8jd3eeHsR0IS-CHkI7kgz`
- Local archive: `/opt/data/agent_os_archive`
- Manifest: `/opt/data/agent_os_archive/manifest.json`
- Daily Drive sync job: `agent-os-drive-daily-archive`
- 2026-06-23 Drive sync 확인: new files 2, changed/downloaded files 2

### 1.4 Hermes agent team profile 구축 완료

현재 실행 가능한 Hermes profiles:

```text
operator
pm
admin
researcher
analyst
coder
reviewer
reporter
governor
auditor
curator
sentinel
```

역할 문서:

- `/opt/data/profiles/<profile>/SOUL.md`
- `/opt/data/agent_os_archive/summaries/agent-team/team-roster.md`

현재 상태:

- profile-ready
- role-contract-fixed
- dispatcher/model specialization은 아직 pending

### 1.5 Agent team 운영 문서 구축 완료

다음 운영 문서들이 존재한다.

- `team-roster.md`
- `operating-loop.md`
- `handoff-contract.md`
- `internal-management-team.md`
- `kanban-routing.md`
- `situation-board.md`
- `agent-dashboard.md`

핵심 운영 흐름:

```text
User/CEO
  → Operator
  → PM
  → Specialist agents
  → Reviewer / Chorus
  → Reporter
  → Dashboard + Slack
  → Memory
  → Loop
```

### 1.6 Kanban boards 구축 완료

현재 boards:

| Board | 상태 |
|---|---|
| `agent-os` | Agent OS governance / ops |
| `dfxisp` | DFXISP P0 project execution |
| `ai-drone` | AI드론 P1 exploration |

최근 dashboard 기준 상태:

```text
agent-os: todo=2, blocked=1, done=11
dfxisp: running=5, done=2
ai-drone: done=6
```

### 1.7 Project portfolio 분리 완료

현재 프로젝트 포트폴리오:

| Project | Status | Priority | Board | Operating Mode |
|---|---|---|---|---|
| DFXISP | Active | P0 | `dfxisp` | 깊이 우선, 검증 우선 |
| AI드론 | Exploration | P1 | `ai-drone` | 작은 PoC, go/no-go 우선 |
| Agent OS Ops | Operating | P0 | `agent-os` | 시스템 유지보수/상황실/루프 |

Resource guideline:

```text
DFXISP        60–70%
AI드론        20–30%
Agent OS Ops  10%
```

### 1.8 Situation Room dashboard v0 구축 완료

현재 dashboard 산출물:

```text
/opt/data/agent_os_archive/files/05-dashboard/situation-room/ui/agent-dashboard.html
/opt/data/agent_os_archive/files/05-dashboard/situation-room/state/agent-dashboard.json
/opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/agent-dashboard.md
```

상태 파일들:

```text
agent-dashboard.json
artifact-registry.json
second-brain-health.json
tasks.json
status.json
agents.json
```

현재 dashboard cron:

- `agent-dashboard-refresh`
- every 30m
- last status: ok

### 1.9 Cron / Loop 기반 구축 완료

현재 등록된 주요 jobs:

| Job | 역할 | 상태 |
|---|---|---|
| `agent-os-drive-daily-archive` | Drive archive sync | ok |
| `slack-channel-C0BA8DR4VV1-daily-archive` | Slack/session archive | ok |
| `agent-team-healthcheck` | Agent team healthcheck | ok |
| `project-weekly-review` | DFXISP/AI드론 portfolio review | ok |
| `graphify-staleness-check` | Graphify freshness check | ok |
| `agent-dashboard-refresh` | Dashboard snapshot refresh | ok |

즉 Agent OS의 최소 운영 루프는 이미 작동 중이다.

### 1.10 Second Brain / Obsidian / Graphify 기반 구축 완료

현재 확인된 상태:

- Obsidian vault mirror 존재
- Second Brain wiki root: `/opt/data/agent_os_archive/files/02-memory`
- Broken links: 0
- Orphans: 0
- Graphify status: `STALE`

즉 Second Brain의 Markdown 구조는 비교적 정상이나, Graphify semantic graph rebuild가 필요하다.

### 1.11 Reference AI Agent ecosystem 분석 완료

제공된 reference report 기준으로 다음 외부 생태계 방향성이 정리되었다.

핵심 트렌드:

- Agentic AI / autonomous coding agents
- CLI 기반 개발 자동화
- system prompt reverse engineering
- PKM / knowledge graph
- AI business automation
- model/community monitoring

Agent OS에 흡수할 가치:

- Claude Code / Codex / Hermes Agent → development automation
- Chorus → multi-model review gate
- Obsidian / Graphify / NotebookLM / Zotero → memory/knowledge layer
- Reddit/YouTube/GitHub references → trend radar / weekly tech scout source

---

## 2. 아직 부족한 것

### 2.1 HQ Dashboard v1이 아직 “운영 제품” 수준은 아님

현재는 dashboard snapshot과 문서/JSON/HTML 뼈대가 있다. 그러나 아직 부족한 것:

- human-facing Notion dashboard 미구축
- agent별 current work / output / handoff drill-down 부족
- model usage / quota / cost tracking 부족
- 승인 대기/결정 대기 UI 부족
- Slack command → dashboard state 연결 부족
- production artifact registry 완성도 부족

### 2.2 Agent와 Model specialization 미완료

현재 profiles는 만들어졌지만 대부분 default model/tool config를 공유한다.

필요한 것:

- `researcher`: Claude/Gemini long-context 후보
- `analyst`: Claude-style reasoning 후보
- `coder`: Codex/Claude Code/Hermes tool execution 후보
- `reviewer`: Claude/Chorus multi-model review 후보
- `reporter`: Gemini/Hermes summarization 후보
- `sentinel`: cheap/local/fast watchdog 후보

단, paid API 연결은 사용자 승인 전 manual/not_configured로 유지해야 한다.

### 2.3 Future agents가 아직 실제 profile이 아님

사용자 비전에는 다음 agent들이 있다.

```text
Designer
Social Network
SW Coder
HW Coder
Life Agent
Finance Agent
Business Agent
Career Agent
Learning Agent
```

현재는 concept 또는 future role이다. 해야 할 일은 다음 중 선택이다.

1. 기존 profile의 alias로 운용한다.
2. 별도 Hermes profile로 만든다.
3. domain module 문서로 먼저 두고 필요 시 profile화한다.

### 2.4 Chorus 통합이 아직 실제 workflow에 연결되지 않음

Chorus의 위치는 정리되었다.

```text
Chorus = multi-model peer review / quorum / second opinion layer
```

그러나 아직 해야 할 것:

- Chorus 설치/실행 환경 확정
- Codex/Gemini/OpenCode 등 reviewer model 연결 여부 확인
- DFXISP 문서 1개로 `architect-review` pilot
- code diff 1개로 `review-only` pilot
- 결과를 dashboard artifact로 저장

### 2.5 Notion dashboard가 아직 실제 생성되지 않음

정리된 Notion 구조:

```text
1. Agents
2. Projects
3. Tasks / Kanban Mirror
4. Handoffs
5. Artifacts
6. Health / Cron
7. Decisions
8. Second Brain Inbox
```

아직 필요한 것:

- Notion integration token
- target parent page 공유
- `ntn` CLI 또는 API sync script
- Drive/Kanban/JSON → Notion one-way sync

### 2.6 Production 프로젝트 실행 깊이가 아직 초기 단계

DFXISP는 P0이지만 아직 다음이 필요하다.

- 연구 질문 구체화
- 검증 chain 확정
- 첫 milestone task graph 생성
- AI-ISP architecture / FPGA constraints 분석 심화
- 실험 scaffold와 artifact logging plan 실전화

AI드론은 P1 Exploration으로 유지하되:

- 문제 정의
- 가설 3개 이하 압축
- PoC / go-no-go 기준 확정

---

## 3. 앞으로 해야 할 일 — 우선순위별

## P0 — 지금 바로 해야 할 핵심 작업

### P0-1. HQ Dashboard v1 요구사항을 정본화

목표: 지금의 비전 보고서를 실제 build spec으로 바꾼다.

산출물:

```text
05-dashboard/situation-room/docs/hq-dashboard-v1-requirements.md
05-dashboard/situation-room/state/agent-registry.json
05-dashboard/situation-room/state/model-registry.json
05-dashboard/situation-room/state/artifact-registry.json 업데이트
```

포함해야 할 화면:

- Mission Control overview
- Agents roster
- Projects / portfolio
- Tasks / Kanban mirror
- Artifacts / handoffs
- Memory / Graphify
- Cron / loop health
- Cost / usage guard

### P0-2. Agent Registry 만들기

목표: agent와 model을 분리하여 dashboard가 읽을 수 있게 한다.

예시 schema:

```json
{
  "agent_id": "researcher",
  "role": "researcher",
  "status": "idle|running|blocked|not_configured",
  "execution_mode": "hermes-profile|cli|api|manual|chorus-review",
  "provider_family": "hermes|anthropic|openai|google|manual",
  "model_label": "profile default or external model",
  "capabilities": ["research", "analysis", "review"],
  "cost_mode": "local|manual|paid|unknown",
  "safety": {
    "requires_confirmation": ["drive_write", "external_upload", "credential_change", "git_push"]
  }
}
```

### P0-3. Future roles mapping 문서화

목표: 사용자가 제안한 agent 조직을 현재 Hermes profiles와 연결한다.

산출물:

```text
04-agents/role-map/current-and-future-agents.md
```

내용:

- Designer → future profile 또는 reporter/designer mode
- Social Network → future domain/social role
- SW Coder → current `coder` split 후보
- HW Coder → new embedded/fpga role 후보
- Business/Career/Learning/Life/Finance → future domain modules

### P0-4. Graphify STALE 해결

목표: Second Brain이 살아있는 knowledge graph로 작동하게 한다.

해야 할 일:

1. Drive sync 후 `graphify-out` 상태 확인
2. graphify semantic rebuild 실행
3. `second-brain-health.json/md` 갱신
4. dashboard에서 Graphify 상태를 `FRESH`로 전환

현재 dashboard의 가장 명확한 technical blocker이다.

### P0-5. DFXISP P0 작업을 다시 앞으로 당기기

목표: Agent OS가 실제 production value를 만들게 한다.

현재 active tasks:

- DFXISP-R1 Drive corpus and theory-source inventory
- DFXISP-A1 AI-ISP architecture and FPGA constraint analysis
- DFXISP-C1 Reproducible experiment scaffold and artifact logging plan
- DFXISP-V1 Verification checklist for research-to-FPGA handoff
- DFXISP-REP1 Publish DFXISP Situation Room digest

다음 action:

- 위 5개를 Research TFT + Embedded/HW TFT로 정리
- 각 task의 output artifact를 Drive에 저장
- Reviewer가 verification checklist를 만든 뒤 Reporter가 digest 작성

---

## P1 — 다음으로 해야 할 확장 작업

### P1-1. Notion Mission Control MVP

목표: 사람이 매일 여는 HQ dashboard를 Notion에 만든다.

전제:

- Notion API key 필요
- target Notion page를 integration과 공유 필요

초기에는 one-way sync만 권장한다.

```text
Drive/Kanban/JSON → Notion
```

### P1-2. Chorus Review Gate Pilot

목표: AI들이 서로 검토하는 구조를 실제로 한 번 돌린다.

추천 pilot 2개:

1. DFXISP architecture document → `architect-review`
2. dashboard code/config diff → `review-only`

결과 저장:

```text
05-dashboard/situation-room/docs/chorus-review-pilot-YYYY-MM-DD.md
```

### P1-3. Reference radar 구축

Reference_AIagent 보고서의 YouTube/Reddit/GitHub 자료를 weekly trend radar로 만든다.

목표:

- AI agent ecosystem monitoring
- Hermes/Chorus/Codex/Claude/Gemini 관련 업데이트 추적
- 개발 자동화와 PKM workflow를 Agent OS에 흡수

산출물:

```text
02-memory/references/ai-agent-ecosystem-radar.md
07-loop/routines/weekly-tech-scout.md
```

### P1-4. Cost / Usage Guard

목표: 여러 모델을 쓰되 비용 폭주를 막는다.

초기 정책:

- paid provider는 명시 승인 전 manual/not_configured
- subscription CLI 우선
- local/manual artifact ingest 지원
- dashboard에 cost mode 표시

---

## P2 — 이후 확장 작업

### P2-1. Domain Agents 구체화

대상:

- Life Agent
- Finance Agent
- Business Agent
- Career Agent
- Learning Agent

방법:

1. 바로 profile을 만들지 않는다.
2. domain charter 문서부터 만든다.
3. 실제 recurring workflow가 생기면 profile화한다.

### P2-2. Portfolio / Career Project 시작

목표: DFXISP와 Agent OS 자체를 포트폴리오 자산으로 만든다.

가능 산출물:

- 개인 portfolio site
- GitHub README/profile 정리
- DFXISP project page
- Agent OS case study
- 연구/개발 log digest

### P2-3. Business / Economic Activity module

목표: Agent OS를 실제 수익화/경제활동에도 쓰기 시작한다.

가능 task:

- 시장 조사
- product idea ranking
- landing page draft
- proposal/pitch deck
- automation service candidate

---

## 4. 추천 실행 순서

가장 현실적인 순서는 다음이다.

```text
1. Graphify STALE 해결
2. HQ Dashboard v1 requirements 작성
3. Agent Registry JSON 생성
4. Future roles mapping 문서 작성
5. Dashboard snapshot에 HQ/Agent Registry 반영
6. DFXISP 5개 active task 산출물 정리
7. Chorus pilot 1회 실행
8. Notion MVP 준비
9. Reference radar / weekly tech scout 구축
10. Domain agents는 필요 시 하나씩 추가
```

---

## 5. CEO 관점의 다음 의사결정

이형민이 바로 결정하면 좋은 질문은 5개다.

1. **Dashboard 우선순위:** Notion 먼저인가, local HTML/JSON dashboard 강화가 먼저인가?
2. **Agent 확장:** Designer/HW Coder/SW Coder를 지금 profile로 만들까, alias 문서로 먼저 둘까?
3. **Chorus pilot:** DFXISP 문서 리뷰부터 할까, dashboard code/diff 리뷰부터 할까?
4. **Model 연결:** paid API 없이 CLI/manual ingest 중심으로 갈까, 일부 key를 연결할까?
5. **Production 우선순위:** DFXISP를 계속 P0 60–70%로 유지할까, Agent OS HQ 구축을 임시 P0로 끌어올릴까?

---

## 6. Hermes 추천안

현재 단계에서는 다음을 추천한다.

```text
P0 = HQ Dashboard v1 + Agent Registry + Graphify freshness + DFXISP active task 정리
P1 = Chorus pilot + Notion MVP + Reference radar
P2 = Future domain agents + Career/Business expansion
```

이유:

- HQ Dashboard가 먼저 안정되어야 CEO가 전체 조직을 볼 수 있다.
- Agent Registry가 있어야 모델/역할/비용/상태를 dashboard에 붙일 수 있다.
- Graphify가 fresh해야 Memory layer가 신뢰 가능하다.
- DFXISP는 Agent OS의 실전 production testbed다.
- Chorus/Notion은 바로 붙일 수 있지만, canonical state가 먼저 정리되어야 안정적으로 운영된다.

---

## 7. 가장 가까운 next action 카드

```text
[agent-os/P0] HQ Dashboard v1 requirements 정본화
Owner: PM + Analyst + Designer-future + Reporter
Output: hq-dashboard-v1-requirements.md

[agent-os/P0] Agent Registry JSON 생성
Owner: Admin + Coder + Reporter
Output: agent-registry.json, model-registry.json

[agent-os/P0] Graphify STALE 해소
Owner: Admin + Curator + Sentinel
Output: second-brain-health.json/md updated, dashboard status FRESH

[dfxisp/P0] DFXISP active TFT 산출물 정리
Owner: PM + Researcher + Analyst + Coder + Reviewer + Reporter
Output: source inventory, architecture analysis, verification checklist, digest

[agent-os/P1] Chorus review gate pilot
Owner: Reviewer + Coder + Reporter
Output: chorus-review-pilot report
```

---

## 8. 최종 정리

지금까지는 **회사 설립과 사무실/운영 규칙/팀 구성/상황판/프로젝트 보드**를 만든 단계다.

앞으로는 **직원들이 실제로 일하고, 보고하고, 서로 검토하고, 산출물을 만들고, CEO가 dashboard에서 통제하는 단계**로 넘어가야 한다.

즉 다음 전환이 필요하다.

```text
문서화된 Agent OS
→ 관측 가능한 Agent OS
→ 실행하는 Agent OS
→ 검토/개선하는 Agent OS
→ 24/7 자율 운영 Agent OS
```
