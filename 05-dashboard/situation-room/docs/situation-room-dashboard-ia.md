# Agent OS Situation Room Dashboard IA

- 작성시각: `2026-06-21T04:56:54+00:00`
- 역할: UX / Information Architecture
- 범위: `agent-os`, `dfxisp`, `ai-drone` 보드와 12개 Agent OS 역할, Hermes/Claude/Gemini/Codex/GPT를 수용하는 model-agnostic Situation Room
- 원칙: **사람이 10초 안에 판단하고, AI agent가 JSON/Markdown만으로 동일 상태를 재사용할 수 있어야 한다.**

## 1. IA 핵심 결론

Agent OS Situation Room은 “예쁜 HTML 대시보드”가 아니라 **운영 상태의 공통 번역 계층**이어야 한다.

```text
Kanban boards + healthchecks + project docs + artifacts + model registry
  → dashboard/status.json          # machine/agent canonical snapshot
  → summaries/agent-team/situation-board.md  # human + AI prompt-readable board
  → dashboard/index.html           # human visual Mission Control
  → Slack digest                   # alert/update only
```

중요 상태는 HTML에만 두지 않는다. 모든 카드, 뱃지, 경고, 다음 액션은 JSON 필드와 Markdown 문단/표에 1:1로 대응되어야 한다.

## 2. 첫 화면 우선순위

### P0 — Mission Control / Overview

사용자가 열자마자 답해야 할 질문:

1. 지금 전체 상태가 `pass`, `warn`, `blocked` 중 무엇인가?
2. 사람이 지금 결정해야 하는 것은 무엇인가?
3. 어떤 보드/프로젝트/agent가 막혀 있는가?
4. 비용이 발생할 수 있는 외부 모델/API 실행이 대기 중인가?
5. 다음으로 누구에게 어떤 작업을 넘겨야 하는가?

첫 화면 위젯 순서:

| 순서 | 섹션 | 목적 | JSON source | Markdown mirror |
|---:|---|---|---|---|
| 1 | Overall status light | `PASS/WARN/BLOCKED` 즉시 판단 | `status.overall` | `## Overall` |
| 2 | Human attention needed | 사용자 결정/승인/차단 사유 | `attention[]` | `## Human Attention Needed` |
| 3 | Today next actions | 오늘 실행 가능한 3~7개 액션 | `next_actions[]` | `## Next Actions` |
| 4 | Board health strip | `agent-os`, `dfxisp`, `ai-drone` 상태 | `boards[]` | `## Boards` |
| 5 | Agent roster summary | 12개 역할의 현재 상태/다음 handoff | `agents[]` | `## Agent Team` |
| 6 | Project cards | DFXISP/AI드론 우선순위와 단계 | `projects[]` | `## Projects` |
| 7 | Cost/provider guard | API/manual/not_configured 비용 경계 | `providers[]`, `cost_guard` | `## Cost / Provider Guard` |
| 8 | Recent artifacts/handoffs | 최근 산출물과 인수인계 링크 | `artifacts[]`, `handoffs[]` | `## Recent Artifacts`, `## Handoffs` |
| 9 | Governance strip | Drive/Slack/cron/healthcheck freshness | `governance` | `## Governance` |

### P1 — Operational Detail

Overview에서 드릴다운하는 화면이다.

1. `Agents`: 역할/모델/실행모드/권한/현재 작업
2. `Kanban`: 보드별 lane, blocked reason, assignee, artifact count
3. `Projects`: 프로젝트별 상태, priority, board, 검증/PoC 단계
4. `Handoffs`: Summary / Inputs / Output / Decisions / Verification / Open Questions / Next Agent
5. `Artifacts`: 산출물 inventory와 task/agent 연결

### P2 — Debug / Authoring / Observability

초기 화면에 과도하게 올리지 않는다.

1. `Graph`: operator → pm → specialists → reviewer → reporter + governance side-loop
2. `Runs / Traces`: run → step → tool/script call → artifact → review
3. `Workflow Builder`: Dify/Flowise 스타일 authoring canvas는 후속 기능
4. `Evaluation`: reviewer/auditor 결과, confidence, regression notes

## 3. 추천 사이드바 구조

```text
Agent OS Situation Room
├── Overview          # P0: Mission Control
├── Attention         # P0: 사용자 승인/결정/차단만 모음
├── Boards            # P0/P1: agent-os, dfxisp, ai-drone
├── Agents            # P1: 12 role registry + model binding
├── Projects          # P1: DFXISP, AI드론, Agent OS Ops
├── Handoffs          # P1: agent 간 계약 기반 인수인계
├── Artifacts         # P1: 산출물/파일/리뷰 링크
├── Governance        # P1: governor/auditor/curator/sentinel + cron/Drive/Slack
├── Providers & Cost  # P1: Hermes/Claude/Gemini/Codex/GPT 연결/비용 상태
└── Traces            # P2: 실행 로그/디버깅/평가
```

## 4. 화면 섹션 상세 설계

### 4.1 Overview

카드 구성:

- `Overall`: 상태, 마지막 갱신, 상태 산출 근거
- `Attention`: 승인 필요, 차단, 질문, 비용 발생 가능 task
- `Next Actions`: owner, suggested assignee, board, due/priority
- `Board Snapshot`: board별 lane count와 blocked count
- `Agent Snapshot`: 역할별 `state`, `current_task`, `handoff_to`
- `Project Snapshot`: DFXISP P0 Active, AI드론 P1 Exploration, Agent OS Ops
- `Provider/Cost`: Hermes active, Codex available/manual, Claude/Gemini/GPT manual/not_configured 가능성
- `Recent Outputs`: 최근 artifact/handoff/healthcheck

### 4.2 Attention

Overview보다 더 엄격하게 “사용자 개입 필요”만 보여준다.

필드:

- `id`
- `severity`: `info|warn|critical`
- `kind`: `approval|decision|blocker|credential|cost|security|missing-input`
- `summary`
- `requested_by`
- `related_board`
- `related_task_id`
- `safe_default`
- `required_user_action`

### 4.3 Boards / Kanban

보드는 task truth의 위치다.

필수 보드:

| Board | 용도 | 첫 화면 노출 기준 |
|---|---|---|
| `agent-os` | 운영/거버넌스/루프/대시보드 | 항상 표시 |
| `dfxisp` | P0 Active 프로젝트 실행 | 항상 표시, P0 강조 |
| `ai-drone` | P1 Exploration 프로젝트 실행 | 항상 표시, exploration/go-no-go 강조 |

Lane 권장값:

```text
triage / todo / ready / running / blocked / review / done
```

AI agent를 위해 task card는 반드시 `board`, `task_id`, `title`, `lane`, `assignee_role`, `agent_id`, `blocker`, `artifact_paths`, `next_action`을 갖는다.

### 4.4 Agents

Agent는 모델명이 아니라 **책임 단위(role)** 로 먼저 표현한다.

역할 그룹:

- Core operations: `operator`, `pm`, `admin`
- Specialist execution: `researcher`, `analyst`, `coder`
- Quality/reporting: `reviewer`, `reporter`
- Governance: `governor`, `auditor`, `curator`, `sentinel`

각 card 필드:

- role name
- mission one-liner
- state: `idle|todo|ready|running|blocked|done|disabled`
- current task + board
- handoff target
- model binding: `provider_family`, `model_label`, `execution_mode`, `connection_status`
- allowed actions / confirmation boundary
- last artifact

### 4.5 Provider & Model Registry

Hermes/Claude/Gemini/Codex/GPT는 UI에 직접 “agent”로 하드코딩하지 않고 registry에서 role에 연결한다.

권장 추상화:

```text
Provider / Model
  → Execution Adapter: api | cli | hermes-profile | manual | external-adapter
  → Agent Role
  → Kanban Task
  → Artifact / Handoff / Trace
```

비용 때문에 Claude/Gemini/GPT는 `manual` 또는 `not_configured`여도 정상 상태로 취급한다. “연결 안 됨”은 장애가 아니라 운영 모드일 수 있다.

### 4.6 Projects

Project card는 board와 artifact root를 같이 보여준다.

- DFXISP: `Active`, `P0`, board `dfxisp`, path `/opt/data/projects/dfxisp`, mode `verification-first`
- AI드론: `Exploration`, `P1`, board `ai-drone`, path `/opt/data/projects/ai-drone`, mode `small PoC + go/no-go`
- Agent OS Ops: 운영 시스템 자체, board `agent-os`, path `/opt/data/agent_os_archive`

### 4.7 Governance

거버넌스는 별도 페이지와 Overview strip을 모두 가진다.

- `governor`: role boundary, routing integrity, patch agenda
- `auditor`: factual healthcheck, security hygiene, cron/profile/archive checks
- `curator`: knowledge hygiene, decisions/glossary/content-map drift
- `sentinel`: stale sync, failed cron, blocked task, anomaly watch

표시 대상:

- Drive archive freshness
- Slack/session archive freshness
- cron job status
- profile/SOUL contract status
- project scaffold status
- patch agenda

### 4.8 Handoffs / Artifacts

모든 agent output은 동일한 handoff contract로 보여준다.

```md
## Summary
## Inputs
## Output
## Decisions
## Verification
## Open Questions
## Next Agent
```

Artifact는 “파일 목록”이 아니라 `task_id`, `agent_id`, `handoff_id`, `review_status`에 연결된 운영 단위로 표시한다.

## 5. JSON / Markdown parity 요구사항

### 5.1 Parity 원칙

1. HTML에 보이는 운영 상태는 반드시 JSON에 존재해야 한다.
2. JSON의 핵심 상태는 반드시 Markdown에 사람이 읽을 수 있게 렌더링되어야 한다.
3. Markdown은 agent prompt에 붙여도 컨텍스트가 유지되도록 path, board, task_id, next_agent를 포함해야 한다.
4. HTML은 JSON/Markdown의 rendering layer일 뿐, unique source of truth가 아니다.
5. `not_configured`, `manual`, `disabled`, `error`를 구분해 비용/설정 상태를 오해하지 않게 한다.

### 5.2 Canonical JSON shape

```json
{
  "schema_version": "1.0.0",
  "updated_at": "ISO-8601",
  "overall": "pass|warn|blocked",
  "summary": "one-line human summary",
  "attention": [
    {
      "id": "attn_001",
      "severity": "info|warn|critical",
      "kind": "approval|decision|blocker|credential|cost|security|missing-input",
      "summary": "...",
      "related_board": "agent-os|dfxisp|ai-drone",
      "related_task_id": "...",
      "required_user_action": "...",
      "safe_default": "..."
    }
  ],
  "boards": [
    {
      "id": "dfxisp",
      "label": "DFXISP",
      "status": "active|exploration|maintenance|paused",
      "priority": "P0|P1|P2",
      "lanes": {
        "triage": 0,
        "todo": 0,
        "ready": 0,
        "running": 0,
        "blocked": 0,
        "review": 0,
        "done": 0
      },
      "blocked_count": 0,
      "next_action": "..."
    }
  ],
  "agents": [
    {
      "id": "reviewer",
      "role": "reviewer",
      "group": "quality",
      "state": "idle|todo|ready|running|blocked|done|disabled",
      "mission": "...",
      "current_task_id": null,
      "current_board": null,
      "handoff_to": "reporter",
      "next_action": "...",
      "model_binding": {
        "provider_family": "hermes|anthropic|google|openai|manual|unknown",
        "model_label": "gpt-5.5|Claude|Gemini|Codex|GPT|manual",
        "execution_mode": "hermes-profile|api|cli|manual|external-adapter",
        "connection_status": "available|not_configured|disabled|error|manual"
      },
      "safety": {
        "can_write_files": false,
        "can_run_shell": false,
        "requires_confirmation": ["credential-change", "paid-provider-run", "external-upload"]
      },
      "last_artifact_path": null
    }
  ],
  "providers": [
    {
      "id": "claude",
      "family": "anthropic",
      "display_name": "Claude",
      "status": "available|not_configured|manual|disabled|error",
      "execution_modes": ["api", "cli", "manual"],
      "cost_mode": "paid|manual|local|unknown",
      "default_policy": "manual unless explicitly enabled"
    }
  ],
  "projects": [
    {
      "slug": "dfxisp",
      "label": "DFXISP",
      "status": "active",
      "priority": "P0",
      "board": "dfxisp",
      "path": "/opt/data/projects/dfxisp",
      "operating_mode": "verification-first",
      "next_action": "..."
    }
  ],
  "handoffs": [
    {
      "id": "handoff_001",
      "from_agent": "analyst",
      "to_agent": "coder",
      "task_id": "...",
      "summary": "...",
      "artifact_paths": ["..."],
      "verification": "...",
      "open_questions": []
    }
  ],
  "artifacts": [
    {
      "id": "artifact_001",
      "task_id": "...",
      "agent_id": "...",
      "type": "plan|report|code|review|healthcheck|snapshot",
      "path": "...",
      "created_at": "ISO-8601",
      "review_status": "unreviewed|reviewed|needs_changes|accepted"
    }
  ],
  "governance": {
    "drive_archive": {"status": "pass|warn|blocked|unknown", "freshness_hours": null},
    "slack_archive": {"status": "pass|warn|blocked|unknown", "last_run_at": null},
    "cron": {"status": "pass|warn|blocked|unknown", "failed_jobs": []},
    "healthcheck": {"status": "pass|warn|blocked|unknown", "last_run_at": null},
    "patch_agenda": []
  },
  "cost_guard": {
    "api_backed_agents_enabled": false,
    "paid_run_pending": false,
    "manual_mode_available": true,
    "requires_confirmation_for": ["Claude", "Gemini", "GPT paid API", "credential changes"]
  },
  "next_actions": [
    {
      "id": "next_001",
      "priority": "P0|P1|P2",
      "owner": "operator|pm|admin|researcher|analyst|coder|reviewer|reporter|governor|auditor|curator|sentinel|user",
      "board": "agent-os|dfxisp|ai-drone",
      "summary": "...",
      "handoff_to": "..."
    }
  ]
}
```

### 5.3 Markdown mirror structure

```md
# Agent OS Situation Board

## Overall
- Status: PASS/WARN/BLOCKED
- Updated: ISO-8601
- Summary: ...

## Human Attention Needed
| Severity | Kind | Summary | Board | Task | Required Action | Safe Default |

## Next Actions
| Priority | Owner | Board | Action | Handoff To |

## Boards
| Board | Status | Priority | Triage | Todo | Ready | Running | Blocked | Review | Done | Next Action |

## Agent Team
| Role | State | Model/Provider | Execution Mode | Connection | Current Task | Next Action | Handoff To |

## Projects
| Project | Status | Priority | Board | Path | Operating Mode | Next Action |

## Providers & Cost Guard
| Provider | Status | Execution Modes | Cost Mode | Default Policy |

## Handoffs
### handoff_id
- From → To:
- Task:
- Summary:
- Artifacts:
- Verification:
- Open Questions:

## Recent Artifacts
| Type | Task | Agent | Path | Review Status |

## Governance
- Drive archive:
- Slack archive:
- Cron:
- Healthcheck:
- Patch agenda:
```

## 6. 모델별 UI 표기 규칙

| Provider/UI label | 권장 위치 | 초기 상태 해석 | 주의사항 |
|---|---|---|---|
| Hermes | native profiles / default control plane | `available` 또는 profile별 active/stopped | 역할 실행의 기본 경로 |
| Codex | coder 계열, CLI/API adapter | `available`, `manual`, 또는 `not_configured` | 구현/검증용. task/artifact 연결 필수 |
| Claude | analyst/reviewer/researcher 후보 | `manual` 또는 `not_configured`도 정상 | 비용 때문에 explicit run만 |
| Gemini | researcher/long-context 후보 | `manual` 또는 `not_configured`도 정상 | Drive/문서 장문 분석용 |
| GPT | synthesis/general/reviewer 후보 | current/default 또는 `not_configured` | provider key 값 노출 금지 |

## 7. 상태 계산 규칙

`overall` 권장 계산:

- `blocked`: critical attention 존재, P0 board blocked, healthcheck failed, credential/security 위험
- `warn`: blocked는 아니지만 stale archive, not_configured provider가 필요한 task에 배정됨, review 대기 누적
- `pass`: P0 차단 없음, cron/healthcheck 정상, next action 명확

Provider `not_configured`는 단독으로 `warn`이 아니다. 해당 provider가 배정된 실행 task가 있을 때만 `warn` 또는 `blocked`로 승격한다.

## 8. 구현 우선순위

1. `status.json` 단일 스키마 확정 — 모든 화면의 canonical source
2. `situation-board.md` 렌더러 — AI agent가 그대로 읽을 수 있는 Markdown mirror
3. `index.html` Overview — P0 Mission Control만 먼저 구현
4. `agents/providers/projects/boards` 섹션 드릴다운
5. artifact/handoff ingest 규칙 연결
6. runs/traces/evaluation은 후속 드릴다운으로 추가
7. workflow canvas는 실제 운영 데이터가 안정화된 뒤 authoring 기능으로 검토

## 9. 수용 기준

- 사용자는 첫 화면 10초 안에 전체 상태, 사람 개입 필요 항목, 다음 액션을 이해한다.
- AI agent는 JSON과 Markdown만으로 같은 상태를 재구성하고 다음 handoff를 판단한다.
- HTML에만 존재하는 운영 정보가 없다.
- `agent-os`, `dfxisp`, `ai-drone` 보드가 분리되어 표시된다.
- 12개 Agent OS role이 model-agnostic registry로 표현된다.
- Hermes/Claude/Gemini/Codex/GPT는 연결 여부와 비용 정책이 분리되어 표시된다.
- API key/token/secret 값은 어떤 표현에도 포함되지 않는다.
