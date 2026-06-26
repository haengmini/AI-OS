---
title: Agent OS / HQ Dashboard Vision Report
created: 2026-06-23T04:50:00+00:00
status: draft-v1
owner: 이형민
scope: Agent OS, HQ Dashboard, multi-model agents, production loop
source_context:
  - user_slack_message: 2026-06-23 Agent OS / HQ dashboard purpose statement
  - local_agent_os_constitution: /opt/data/agent_os_archive/files/AGENT-OS.md
  - situation_room_docs: /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/
  - agent_team_docs: /opt/data/agent_os_archive/summaries/agent-team/
---

# Agent OS / HQ Dashboard Vision Report

## 0. Executive Summary

Agent OS / HQ Dashboard의 목적은 단순한 작업 관리 웹페이지가 아니다. 이 시스템은 이형민이 **사장/오너**로서 목표와 방향을 제시하고, 여러 AI 모델과 도구를 역할별 agent로 조직하여 24/7 병렬 연구개발·학습·커리어·포트폴리오·경제활동을 수행하게 만드는 **AI-native headquarters**이다.

핵심 정의는 다음과 같다.

```text
Agent OS = 여러 모델/도구/메모리/프로젝트를 하나의 운영 체계로 묶는 AI 조직 운영 시스템
HQ Dashboard = 사장이 전체 조직 상태, 작업, 산출물, 비용, 메모리, 프로젝트 진행을 보는 Mission Control
Agent = 모델이 아니라 역할·책임·workflow·handoff·output 단위
Model = Claude, Codex, Gemini, Hermes 등 agent 역할을 수행하는 실행 엔진
Production = 실제 연구개발·생산·경제활동 산출물이 만들어지는 Project Factory
Loop = 24/7 운영, 피드백, 자가 학습, 자가 개선을 반복하는 성장 엔진
```

Agent OS는 현재 이미 다음 기반을 갖고 있다.

- Google Drive 기반 Agent OS source-of-truth 및 local archive
- Slack thread를 통한 사용자 소통 채널
- Hermes profile 기반 agent team: `operator`, `pm`, `admin`, `researcher`, `analyst`, `coder`, `reviewer`, `reporter`, `governor`, `auditor`, `curator`, `sentinel`
- Kanban board: `agent-os`, `dfxisp`, `ai-drone`
- Situation Room dashboard 산출물: JSON / Markdown / HTML
- Second Brain / Obsidian / Graphify / Zotero 연동 방향
- DFXISP, AI드론 등 실제 production project

이번 사용자의 비전 텍스트는 이 기존 Agent OS를 더 명확히 **AI 회사/본사 운영 모델**로 재정의한다. 사용자는 프로젝트를 구상하고 목표를 설정하며, AI agent들은 조사·탐구·제안·제작·수정·검증·보고를 수행한다.

---

## 1. 왜 Agent OS / HQ Dashboard를 만드는가

### 1.1 문제의식

현재 AI 도구는 강력하지만 각각 분리되어 있다.

- Claude는 reasoning, 설계, 문서화, 리뷰에 강하다.
- Codex/ChatGPT 계열은 구현, 디버깅, 테스트, CLI/Git 작업에 강하다.
- Gemini/NotebookLM/Google ecosystem은 long-context, 문서/자료, multimodal, Google Drive/Workspace와 연결성이 좋다.
- Hermes는 Slack, cron, tools, memory, Drive archive, Kanban, local execution을 묶는 운영 agent가 될 수 있다.
- Chorus는 여러 모델의 peer review와 quorum-based 검토를 가능하게 한다.
- Obsidian, Graphify, Zotero, LLM Wiki, Second Brain은 장기 지식 축적과 연결성 분석에 강하다.

하지만 이 도구들을 사람이 매번 수동으로 열고, 맥락을 복사하고, 결과를 정리하고, 다음 작업을 지정하면 관리 비용이 커진다. 따라서 필요한 것은 개별 도구가 아니라 **여러 AI와 도구를 한 조직처럼 운영하는 control plane**이다.

### 1.2 목표

Agent OS / HQ Dashboard는 다음을 목표로 한다.

1. 여러 AI 모델의 장점을 모아 역할별 agent 군단을 만든다.
2. 사용자는 목표·우선순위·최종 승인에 집중한다.
3. agent들은 조사, 계획, 구현, 리뷰, 보고, 유지보수를 수행한다.
4. 프로젝트를 병렬로 운영한다.
5. 연구개발뿐 아니라 학습, 커리어, 포트폴리오, 경제활동까지 확장한다.
6. Slack과 Dashboard를 통해 항상 현재 상태를 볼 수 있게 한다.
7. 24/7 운영 루프를 통해 자가 학습·자가 개선·자가 운영을 달성한다.

### 1.3 회사 비유

사용자의 역할은 **사장 / CEO / Owner**이다.

```text
이형민 = Owner / CEO
  - 비전 제시
  - 목표 설정
  - 우선순위 결정
  - 승인/거절/방향 수정
  - 성과 평가

AI agents = 직원 / 팀 / TFT
  - 조사
  - 분석
  - 기획
  - 설계
  - 구현
  - 검증
  - 보고
  - 유지보수
  - 개선 제안
```

즉 Agent OS는 “AI chatbot 모음”이 아니라 **AI 직원들이 일하는 회사 운영 체계**이다.

---

## 2. Agent OS 7-Layer Architecture

기존 `AGENT-OS.md`의 최상위 규칙과 사용자가 제공한 구조는 동일한 7-layer architecture로 정리된다.

```text
01 Hardware
→ 02 Memory
→ 03 Models
→ 04 Agents
→ 05 Dashboard + Slack
→ 06 Production
→ 07 Loop
```

### 2.1 01 Hardware

목적: Agent OS가 실행되고 사용자가 접근하는 물리/운영 환경.

대상:

- Desktop
- Laptop
- iPhone
- Linux server / VPS
- Windows machine
- iOS device

역할:

- local-first 실행 환경
- 코드/스크립트/대시보드 실행
- Claude/Codex/Gemini CLI 실행 가능성
- Slack/Notion/Drive 접근
- 장기적으로 edge device, workstation, mobile cockpit까지 확장

### 2.2 02 Memory

목적: Agent OS의 장기 기억, 지식, 문헌, 결정을 축적하는 계층.

구성 요소:

- Second Brain
- LLM Wiki
- Obsidian vault
- Graphify knowledge graph
- Zotero literature library
- Google Drive source material
- Markdown/JSON decision logs

운영 원칙:

```text
Google Drive = original / canonical document store
Local archive = executable cache / mirror
Markdown + JSON = agent-readable memory substrate
Obsidian/Graphify = human+agent navigation and relationship graph
Zotero = paper/source management
```

Memory 계층은 단순 저장소가 아니라, agent들이 계속 참조하고 재사용하는 **조직 지식 자산**이다.

### 2.3 03 Models

목적: 각 agent 역할을 수행하는 실행 엔진.

현재/후보 모델 및 도구:

- Claude / Claude Code
- Codex / ChatGPT / OpenAI coding models
- Gemini / Antigravity / NotebookLM
- Hermes Agent
- OpenRouter 경유 모델
- Local LLM / vLLM / Ollama / LM Studio 후보

원칙:

```text
Agent ≠ Model
Agent = responsibility, workflow, handoff, output
Model = Claude, Codex, Gemini, Hermes, etc.
```

즉 `researcher`라는 agent는 특정 모델 하나가 아니라, 필요에 따라 Claude/Gemini/Hermes/NotebookLM 등을 사용할 수 있는 역할이다.

### 2.4 04 Agents

목적: 실제 조직 구성원처럼 역할과 책임을 나눈다.

Core Control Agents:

```text
Operator
Admin
PM
```

Core Specialist Agents:

```text
Designer
Social Network
SW Coder
HW Coder
Researcher
Analyst
Reporter
```

Current Hermes Profiles:

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

Future Domain Agents:

```text
Life Agent
Finance Agent
Business Agent
Career Agent
Learning Agent
```

설계 원칙:

- 역할 경계가 먼저이고 모델 배정은 나중이다.
- 현재 Hermes profile은 실행 가능한 v1 역할군이다.
- 사용자가 제안한 `Designer`, `Social Network`, `SW Coder`, `HW Coder` 등은 현재 profile 체계의 확장/alias로 설계한다.
- 미래 domain agent는 core workflow를 깨지 않고 module로 추가한다.

### 2.5 05 Dashboard + Slack

목적: 사람이 agent 조직을 통제하고, agent들이 상태를 공유하는 Mission Control.

사용자가 원하는 dashboard 기능:

- AI 모델별 사용량 확인
- 프로젝트 진행상황 확인
- agent별 작업 내용 확인
- memory file 확인
- Notion, Obsidian Graph, Slack 등과 연결
- 모든 작업의 현재 상태, 산출물, blocker, 다음 action 표시

권장 구조:

```text
Drive / Kanban / JSON / Markdown = canonical state
Notion = human-facing dashboard / database view
HTML dashboard = local/web visual Situation Room
Slack = command, alert, digest, approval channel
Obsidian Graph / Graphify = knowledge topology view
```

### 2.6 06 Production

목적: 실제 결과물이 생성되는 project factory.

대상 활동:

- 연구개발 활동
- 생산활동
- 경제활동
- 커리어/포트폴리오 관리
- 학습 프로젝트
- 비즈니스/콘텐츠/자동화 프로젝트

현재 production project:

- DFXISP: 머신 비전을 위한 DFX AI-ISP 설계 / Zynq UltraScale+ ZCU104 FPGA 구현
- AI드론: exploration / PoC / go-no-go 중심
- Agent OS Ops: 운영 체계 자체의 유지보수 및 진화

### 2.7 07 Loop

목적: 반복 수행을 통한 자가 발전, 자가 학습, 자율 수행, 자율 운영.

현재 운영 루프:

```text
08:50 Drive archive sync
09:00 Slack/session archive
09:10 Agent team healthcheck
project review cron every 2 days
```

확장 목표:

- daily planning
- project progress review
- memory hygiene
- weekly portfolio review
- model/tool healthcheck
- cost/usage review
- agent performance review
- skill extraction
- self-improvement proposal

Loop는 Agent OS가 단순 대시보드가 아니라 **살아 있는 운영체계**가 되게 하는 핵심이다.

---

## 3. Agent Team Structure

### 3.1 Core Control Agents

| Agent | 역할 | 주요 산출물 |
|---|---|---|
| Operator | 사용자 요청 접수, 의도 분류, Slack/Drive 맥락 보존, 라우팅 | classified request, routing note |
| Admin | OAuth, Drive, Slack, Cron, VPS, credential hygiene, 안전 운영 | system change report, config status |
| PM | 목표 분해, 완료 기준, 의존성, 담당자, handoff 설계 | task graph, plan, acceptance criteria |

### 3.2 Core Specialist Agents

| Agent | 역할 | 현재 대응 profile / 후보 |
|---|---|---|
| Researcher | 자료 조사, 문헌, 출처, 불확실성 정리 | `researcher` |
| Analyst | 근거 종합, tradeoff, architecture 판단 | `analyst` |
| SW Coder | software implementation, scripts, tests, Git/CLI | `coder` / future `sw-coder` |
| HW Coder | FPGA/RTL/HLS/embedded implementation | future `hw-coder` |
| Designer | UI/UX, diagram, presentation, visual communication | future `designer` |
| Social Network | SNS, 콘텐츠 배포, 네트워킹, 브랜드 관리 | future `social-network` |
| Reporter | Slack/Drive/Notion 보고, digest, 산출물 정리 | `reporter` |
| Reviewer | quality gate, 검증, 완료 기준 확인 | `reviewer` |

### 3.3 Internal Management Agents

| Agent | 역할 | 주요 점검 대상 |
|---|---|---|
| Governor | 팀 토폴로지, 역할 경계, 라우팅 무결성 | role boundary, collaboration topology |
| Auditor | 상태/준수 감사 | cron, profiles, archive freshness, security drift |
| Curator | 지식 위생 | memory, decisions, glossary, duplicate docs, skill candidates |
| Sentinel | 이상 감시 | failed cron, stale sync, blocked work, anomalies |

### 3.4 Future Domain Agents

| Agent | 목적 |
|---|---|
| Life Agent | 생활 관리, 루틴, 건강, 일정, 개인 운영 |
| Finance Agent | 예산, 투자, 지출, 수익화, 재무 계획 |
| Business Agent | 사업 기획, 시장 조사, 제품화, 매출 활동 |
| Career Agent | 커리어 전략, 이력서, 포트폴리오, 네트워킹 |
| Learning Agent | 학습 계획, 커리큘럼, 복습, skill tree 관리 |

---

## 4. TFT 구성 모델

Agent OS는 고정 부서뿐 아니라, 목표별 Task Force Team(TFT)을 만들어 병렬 수행한다.

### 4.1 Research TFT

```text
Research TFT = PM + Researcher + Analyst + Reporter + Designer
```

용도:

- 논문/기술 조사
- DFXISP 이론 정리
- Zotero/Obsidian/Graphify 기반 지식 연결
- 연구 report 작성
- 발표/diagram 생성

### 4.2 Software TFT

```text
Software TFT = PM + SW Coder + Designer + Analyst + Reporter
```

용도:

- dashboard 개발
- scripts/automation 개발
- web UI 구현
- API/DB integration
- 테스트/배포/문서화

### 4.3 Embedded / HW TFT

```text
Embedded / HW TFT = PM + HW Coder + SW Coder + Analyst + Reporter
```

용도:

- FPGA/HLS/RTL 설계
- ZCU104 관련 실험
- embedded software + hardware co-design
- verification plan
- resource/latency analysis

### 4.4 Agent OS Maintenance TFT

```text
Agent OS Maintenance TFT = Admin + Operator + SW Coder + Reporter + Hermes Loop
```

용도:

- Drive archive
- Slack archive
- cron healthcheck
- dashboard snapshot
- profile/role update
- status report

### 4.5 Business TFT

```text
Business TFT = PM + Business Agent + Analyst + Designer + Reporter
```

용도:

- 비즈니스 아이디어 발굴
- 시장 조사
- 제품화 전략
- landing page / pitch deck
- 수익 모델 검토

### 4.6 Career / Portfolio TFT

```text
Career / Portfolio TFT = PM + Career Agent + Designer + Reporter + SW Coder
```

용도:

- 포트폴리오 사이트
- GitHub 정리
- 연구/개발 성과 정리
- 이력서/프로필/LinkedIn 자료
- 프로젝트 showcase 자동화

### 4.7 Life / Learning TFT

```text
Life / Learning TFT = PM + Life Agent or Learning Agent + Analyst + Reporter
```

용도:

- 학습 계획
- 복습 루프
- 개인 목표 관리
- 습관/루틴 관리
- 개인 생산성 개선

---

## 5. Tool Ecosystem Mapping

### 5.1 Tool Categories

| Category | Tools | Agent OS 역할 |
|---|---|---|
| Model / Agent Runtime | Claude, Codex, Gemini, Hermes | agent 실행 엔진 |
| Multi-model Review | Chorus | peer review, quorum, second opinion |
| Google Ecosystem | Google Drive, Docs, Sheets, Calendar, Gmail, NotebookLM | source-of-truth, documents, long-context research |
| Memory / Knowledge | Second Brain, LLM Wiki, Obsidian, Graphify, Zotero | 장기 기억, 문헌, 지식 그래프 |
| Collaboration | Slack, Notion | 사용자 소통, dashboard, 승인, digest |
| Source / Code | GitHub, git repos, Hermes repo, Chorus repo | source code, external tool ingestion |
| Dashboard / Control | HTML, JSON, Markdown, Notion DB | Mission Control |

### 5.2 Chorus의 위치

Chorus는 Agent OS의 핵심 실행자가 아니라 **multi-model review layer**로 두는 것이 적합하다.

```text
Hermes / Agent OS creates task or artifact
  → Claude/Codex/Gemini/other model produces output
  → Chorus runs cross-model peer review
  → Reviewer/Reporter records verdict
  → Dashboard/Slack asks 이형민 for final approval if needed
```

활용 예:

- DFXISP architecture review
- code diff pre-merge review
- bug diagnosis
- TDD red-green validation
- business plan second opinion
- career portfolio critique

Chorus는 “한 모델이 만든 결과를 다른 모델들이 검토하는 회의실”이다.

### 5.3 Notion의 위치

Notion은 canonical database가 아니라, 사람이 보기 좋고 조작하기 쉬운 **HQ Dashboard mirror**로 둔다.

```text
Drive / Kanban / JSON / Markdown = 정본
Notion = human-facing Mission Control mirror
Slack = command/alert/approval layer
```

초기에는 단방향 sync가 안전하다.

```text
Kanban/Drive/JSON → Notion
```

이후 승인된 필드만 제한적으로 Notion → Agent OS 역방향 sync를 허용한다.

---

## 6. Dashboard Requirements

### 6.1 Overview / Mission Control

첫 화면은 다음 질문에 답해야 한다.

1. 전체 상태는 정상인가?
2. 어떤 작업이 사람 결정을 기다리는가?
3. 어떤 agent/model이 사용 가능/미구성/오류 상태인가?
4. DFXISP, AI드론, Agent OS Ops는 어디까지 왔는가?
5. 어떤 산출물이 새로 생성되었는가?
6. 어떤 memory/knowledge graph가 stale 상태인가?
7. 비용이 발생할 수 있는 작업은 무엇인가?

필수 widget:

- Overall status: PASS / WARN / BLOCKED
- Human attention needed
- Active blockers
- Agent roster / availability matrix
- Model usage / cost guard
- Project cards
- Kanban counts
- Recent artifacts
- Handoffs
- Cron/health strip
- Memory/Graphify status

### 6.2 Agents View

표시 항목:

- Agent name
- Role / mission
- Backing model/provider
- Execution mode: Hermes profile / CLI / API / manual artifact ingest
- Current task
- Last output
- Handoff target
- Status: idle / ready / running / blocked / done
- Safety permissions

### 6.3 Projects View

표시 항목:

- Project name
- Status: Active / Exploration / Maintenance / Paused
- Priority: P0 / P1 / P2
- Board
- Drive folder
- Local cache
- Current milestone
- Next action
- Human decision needed
- Recent artifacts

### 6.4 Tasks / Kanban View

표시 항목:

- Board: `agent-os`, `dfxisp`, `ai-drone`, future boards
- Lane: triage / todo / ready / running / blocked / done
- Owner agent
- Priority number and label
- Blocker
- Source link
- Handoff link
- Verification state

### 6.5 Memory View

표시 항목:

- Second Brain status
- Obsidian vault path
- Graphify state: FRESH / STALE / MISSING
- Zotero ingestion status
- Broken links
- Orphans
- Important decisions
- Glossary changes
- Knowledge gaps

### 6.6 Production View

표시 항목:

- Active deliverables
- Research outputs
- Code outputs
- Reports
- Portfolio artifacts
- Economic/business outputs
- Review status
- Publish/deploy readiness

### 6.7 Loop View

표시 항목:

- Scheduled jobs
- Last run
- Next run
- Failures
- Daily digest
- Weekly review
- Self-improvement proposals
- Agent performance notes

---

## 7. Operating Flow

### 7.1 Standard Task Flow

```text
User / CEO
  → Operator: 요청 접수, 맥락 보존, 의도 분류
  → PM: 목표 분해, 완료 기준, TFT 구성
  → Specialist agents: 조사/분석/구현/설계
  → Reviewer or Chorus: 품질 검토, peer review
  → Reporter: Slack/Drive/Notion 보고
  → Dashboard: 상태 업데이트
  → Memory: 결정/지식/재사용 규칙 축적
  → Loop: 다음 action 생성
```

### 7.2 Completion Rule

작업 완료 조건은 기존 Agent OS 헌법과 동일하다.

```text
[ ] Output created
[ ] Verification done or defined
[ ] Risks noted
[ ] Memory update considered
[ ] Dashboard update considered
[ ] Slack report sent if important
[ ] Next action defined
```

### 7.3 Handoff Contract

모든 agent 산출물은 다음 형식을 따른다.

```md
## Summary
## Inputs
## Output
## Decisions
## Verification
## Open Questions
## Next Agent
```

이 형식은 agent 간 협업의 표준 언어다.

---

## 8. Current State Assessment

### 8.1 이미 구축된 것

- Agent OS 7-layer constitution 존재
- Drive-first 운영 원칙 존재
- local archive 및 manifest 존재
- Slack channel/thread 기반 운영 맥락 존재
- Hermes profile team 존재
- agent team docs 존재
- Kanban boards 존재
- DFXISP / AI드론 project portfolio 존재
- Situation Room dashboard JSON/Markdown/HTML 존재
- Second Brain / Obsidian / Graphify 기반 존재
- daily Drive/Slack/archive/healthcheck cron 존재

### 8.2 아직 부족한 것

- Notion HQ Dashboard 실제 DB/page 생성 및 sync
- per-role model/provider specialization
- Designer / Social Network / HW Coder 등 미래 역할의 실제 profile화
- Chorus와 Agent OS task/review flow 통합
- model usage / quota / cost telemetry 통합
- agent execution trace 표준화
- long-running 24/7 autonomous loop의 안전 경계
- user approval workflow의 UI화
- production artifact registry의 완성도 향상
- Second Brain / Graphify freshness 자동화

### 8.3 핵심 리스크

| Risk | 설명 | 대응 |
|---|---|---|
| 과도한 자동화 | agent가 승인 없이 위험 작업 수행 | approval gate, safety rule, Slack confirmation |
| 상태 정본 혼란 | Notion/Drive/local/Kanban이 서로 다른 truth를 가짐 | Drive/Kanban/JSON canonical 원칙 유지 |
| 비용 폭주 | 여러 모델/API를 24/7 실행 | cost guard, manual/offline mode, quota dashboard |
| context drift | agent가 오래된 문서를 참조 | archive sync, Graphify freshness, dashboard state timestamp |
| 역할 혼선 | 모델과 agent를 혼동 | role-first, model-second 원칙 유지 |
| 산출물 미검증 | AI output이 검증 없이 production 반영 | reviewer/Chorus gate, verification field mandatory |

---

## 9. Target Architecture

```text
[이형민 / CEO]
    ↕ Slack / Notion / Dashboard

[HQ Dashboard / Mission Control]
    ├─ Overview
    ├─ Agents
    ├─ Projects
    ├─ Kanban Tasks
    ├─ Artifacts
    ├─ Memory / Graphify
    ├─ Cost / Usage
    └─ Loop / Health

[Agent OS Control Plane]
    ├─ Operator
    ├─ PM
    ├─ Admin
    ├─ Governor / Auditor / Curator / Sentinel
    └─ TFT Router

[Agent Teams]
    ├─ Research TFT
    ├─ Software TFT
    ├─ Embedded / HW TFT
    ├─ Agent OS Maintenance TFT
    ├─ Business TFT
    ├─ Career / Portfolio TFT
    └─ Life / Learning TFT

[Model / Tool Runtime]
    ├─ Hermes
    ├─ Claude / Claude Code
    ├─ Codex / ChatGPT
    ├─ Gemini / NotebookLM
    ├─ Chorus
    ├─ Google Workspace
    ├─ Obsidian / Graphify / Zotero
    └─ future tools

[Production]
    ├─ DFXISP
    ├─ AI드론
    ├─ Portfolio
    ├─ Business outputs
    ├─ Learning outputs
    └─ future projects

[Memory + Loop]
    ├─ Drive source-of-truth
    ├─ Markdown / JSON
    ├─ Second Brain / LLM Wiki
    ├─ Obsidian / Graphify
    ├─ daily/weekly cron
    └─ self-improvement proposals
```

---

## 10. Implementation Roadmap

### Phase 1 — HQ Report & Constitution Alignment

목표: 이번 보고서와 기존 Agent OS 헌법을 정렬한다.

작업:

- 본 보고서를 Drive `05-dashboard/situation-room/docs/`에 저장
- `AGENT-OS.md`의 7-layer와 사용자 비전을 연결
- future agents와 current profiles의 mapping 작성
- dashboard 요구사항을 명확히 정의

완료 기준:

- Drive 원본 보고서 존재
- local cache 존재
- Slack에 보고됨

### Phase 2 — Notion Mission Control MVP

목표: Notion을 사람이 보는 HQ Dashboard로 구성한다.

권장 DB:

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

원칙:

- MVP는 Agent OS → Notion 단방향 sync
- Drive/Kanban/JSON이 canonical truth
- Notion은 dashboard/mirror/editing surface

필요 조건:

- `NOTION_API_KEY` 또는 Notion integration token
- 대상 Notion parent page 공유
- `ntn` CLI 또는 Notion API sync script

### Phase 3 — Agent Registry & Model Usage Layer

목표: agent와 model/provider를 분리하여 dashboard에서 관리한다.

필드:

```json
{
  "agent_id": "researcher",
  "role": "researcher",
  "provider_family": "anthropic|openai|google|hermes|manual",
  "model_label": "Claude/GPT/Gemini/etc",
  "execution_mode": "hermes-profile|cli|api|manual|chorus-review",
  "status": "available|not_configured|running|blocked",
  "cost_mode": "free|paid|local|manual",
  "capabilities": ["research", "analysis", "coding", "review"]
}
```

### Phase 4 — Chorus Review Gate Integration

목표: 여러 AI 모델이 서로를 검토하는 peer-review layer를 Agent OS에 넣는다.

우선 적용:

- DFXISP architecture review
- code diff review
- dashboard code review
- report/document critique

Flow:

```text
Artifact generated
  → Chorus review-only / architect-review
  → Reviewer summarizes verdict
  → PM decides next task
  → Reporter logs to Slack/Drive/Dashboard
```

### Phase 5 — Production Project Factory

목표: Agent OS가 실제 병렬 생산을 수행한다.

대상:

- DFXISP P0
- AI드론 P1
- Career / Portfolio project
- Business exploration
- Learning curriculum

각 프로젝트는 독립 board와 독립 scaffold를 가진다.

```text
spec.md
plan.md
tasks.md
verification-plan.md
experiment-log.md
report.md
```

### Phase 6 — 24/7 Autonomous Loop with Governance

목표: 자율 운영 루프를 강화한다.

구성:

- daily status
- weekly portfolio review
- memory cleanup
- cost review
- stale artifact detection
- blocked task escalation
- self-improvement proposal

안전 원칙:

- 위험 작업은 승인 필요
- 비용 발생 작업은 명시 필요
- Drive delete/share/API key/git push/sudo는 사용자 승인 필요
- 자동화는 먼저 read/report 중심으로 시작

---

## 11. Recommended Immediate Next Actions

### 11.1 Documentation

1. 본 보고서를 Agent OS Drive에 저장한다.
2. `AGENT-OS.md`에 HQ/CEO/company metaphor를 반영할지 검토한다.
3. `04-agents/`에 future roles mapping 문서를 만든다.
4. `05-dashboard/`에 HQ dashboard requirements 문서를 정본화한다.

### 11.2 Dashboard

1. 현재 HTML/JSON/Markdown Situation Room에 “HQ Dashboard v1” 개념을 반영한다.
2. Notion dashboard MVP schema를 확정한다.
3. Notion API token이 준비되면 `Agents`, `Projects`, `Tasks`, `Artifacts`, `Health` DB를 생성한다.
4. Kanban/Drive/JSON → Notion sync script를 만든다.

### 11.3 Agents

1. 현재 Hermes profiles와 사용자가 제안한 agents를 mapping한다.
2. `Designer`, `SW Coder`, `HW Coder`, `Social Network`를 profile로 만들지 alias로 둘지 결정한다.
3. per-role model specialization을 설계한다.
4. 비용이 발생하지 않는 manual/offline ingest mode를 먼저 지원한다.

### 11.4 Chorus

1. Chorus를 Agent OS review gate 후보로 등록한다.
2. DFXISP 문서 1개를 `architect-review` 또는 `review-only`로 테스트한다.
3. 결과를 Agent OS dashboard artifact로 저장한다.
4. 이후 코드 diff review로 확장한다.

### 11.5 Production

1. DFXISP P0 작업을 Research TFT + Embedded/HW TFT로 분리한다.
2. AI드론은 Exploration/P1로 작게 유지한다.
3. Career/Portfolio project를 신규 production candidate로 등록한다.
4. Business/Learning/Life는 future domain module로 roadmap에 둔다.

---

## 12. Final Definition

Agent OS / HQ Dashboard는 다음 한 문장으로 정의할 수 있다.

> **이형민이 CEO로서 목표와 방향을 제시하고, Claude·Codex·Gemini·Hermes·Chorus·Google Workspace·Second Brain 등 여러 AI/도구를 역할별 agent 조직으로 묶어, 연구개발·학습·커리어·포트폴리오·경제활동을 24/7 병렬 수행·검토·보고·자가개선하게 만드는 AI-native headquarters이다.**

이 정의에 따라 앞으로의 Agent OS 발전 방향은 명확하다.

```text
도구를 더 붙이는 것보다 먼저,
역할을 명확히 하고,
상태를 보이게 만들고,
산출물을 검증하고,
결과를 memory에 축적하고,
loop를 통해 다음 행동으로 이어지게 해야 한다.
```

이것이 Agent OS / HQ Dashboard의 핵심 운영 철학이다.
