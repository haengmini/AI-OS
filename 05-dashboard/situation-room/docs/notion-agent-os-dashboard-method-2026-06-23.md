---
title: Notion CLI를 활용한 Agent OS Dashboard 운영 방법
created: 2026-06-23
status: proposal
source_video: https://youtu.be/UXM74bsbfIA
scope: Agent OS Situation Room / Notion / ntn CLI
---

# Notion CLI를 활용한 Agent OS Dashboard 운영 방법

## 0. 확인한 내용과 제한

사용자가 공유한 영상: **「노션 CLI 이 영상 하나로 종결합니다. 무려 노션을 직접 만드는 분과 설명해드려요. (Eric Goldman, 노션 제품 리드)」**

실행 확인:

- YouTube 페이지/메타데이터 접근은 성공.
- 영상 길이: 약 58분 17초.
- 페이지상 자막 버튼은 `Subtitles/closed captions unavailable`로 표시됨.
- `youtube-transcript-api`, `yt-dlp`로 transcript 추출을 시도했으나 서버/IP 봇 차단으로 원문 자막 확보는 실패.

따라서 아래 제안은 영상 제목/설명에서 확인되는 핵심 주제인 **Notion Developer Platform, Notion CLI `ntn`, Workers, data sync, tool/webhook 기반 agent integration**과 현재 Agent OS 구조를 결합한 적용안이다.

## 1. 결론: Notion은 “사람이 여는 운영 대시보드”, Drive/Kanban/JSON은 “정본 상태 저장소”로 쓴다

Agent OS의 현재 원칙은 유지한다.

```text
Google Drive / Markdown / JSON / Kanban = canonical source of truth
Notion = human-friendly dashboard, views, filters, quick editing surface
Hermes / cron / scripts = sync and verification layer
```

Notion을 원본 저장소로 바꾸는 것이 아니라, 사람이 매일 열어서 보는 **Agent OS Situation Room UI**로 활용한다.

이유:

- Notion은 뷰, 필터, 관계형 DB, 버튼, 템플릿이 강하다.
- Agent OS는 이미 Drive-first, Markdown/JSON-first로 운영되고 있다.
- LLM/agent가 안정적으로 읽고 쓰기 좋은 형식은 여전히 JSON/Markdown이다.
- Notion API/CLI는 Notion을 Agent OS 상태의 “보기 좋고 편집 가능한 프론트엔드”로 만드는 데 적합하다.

## 2. 권장 Notion 구조

상위 페이지:

```text
Agent OS Situation Room
```

하위 데이터베이스/데이터소스:

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

### 2.1 Agents DB

역할 프로필 상태를 표시한다.

속성:

- Name: operator, pm, researcher, analyst, coder, reviewer, reporter, governor, auditor, curator, sentinel
- State: idle / todo / ready / running / blocked / done
- Current Task
- Next Action
- Handoff To
- Last Updated
- Profile Path
- SOUL.md Link

### 2.2 Projects DB

DFXISP, AI드론 등 프로젝트 포트폴리오.

속성:

- Project
- Status: Active / Exploration / Maintenance / Paused
- Priority: P0 / P1 / P2
- Board
- Drive Folder
- Local Cache
- Next Review
- Human Decision Needed

### 2.3 Tasks / Kanban Mirror DB

Hermes Kanban board의 사람이 보기 좋은 미러.

속성:

- Task
- Board: agent-os / dfxisp / ai-drone
- Lane: triage / todo / ready / running / blocked / done
- Owner Agent
- Priority Number
- Priority Label
- Blocker
- Source Link
- Updated At

중요: Notion에서 직접 수정할 수는 있지만, 최종 task truth는 Hermes Kanban DB와 동기화 정책을 명확히 해야 한다. MVP에서는 **Kanban → Notion 단방향 미러**를 권장한다.

### 2.4 Handoffs DB

Agent OS 표준 handoff contract를 기록한다.

속성:

- Title
- From Agent
- To Agent
- Status
- Summary
- Inputs
- Output
- Decisions
- Verification
- Open Questions
- Artifact Links

### 2.5 Artifacts DB

Drive 산출물/문서/대시보드/상태파일 레지스트리.

속성:

- Name
- Type: doc / json / html / script / report / dataset
- Project
- Drive Link
- Local Cache Path
- Owner
- Status
- Updated At

### 2.6 Health / Cron DB

운영 상태, 크론, 동기화, Graphify health.

속성:

- Component
- Status: PASS / WARN / BLOCKED
- Last Run
- Next Run
- Summary
- Log Link
- Needs Human

### 2.7 Decisions DB

장기 결정 기록.

속성:

- Decision
- Date
- Scope
- Rationale
- Reversible?
- Superseded By
- Links

### 2.8 Second Brain Inbox DB

빠른 메모를 Notion에서 잡아 Drive Second Brain으로 보내는 입구.

속성:

- Capture
- Type: idea / link / paper / task / question
- Target: inbox / project / area / resource / note
- Processed?
- Drive Destination

## 3. Notion CLI `ntn` 적용 방식

Notion CLI의 핵심 가치는 다음이다.

1. 터미널에서 Notion page/database/data source를 읽고 쓸 수 있다.
2. Markdown으로 page를 만들거나 갱신할 수 있다.
3. Notion Workers를 통해 sync/tool/webhook을 만들 수 있다.
4. agent가 Notion을 “작업 표면”으로 쓰기 쉬워진다.

Agent OS 적용 명령 패턴:

```bash
# 인증 환경
export NOTION_API_TOKEN=$NOTION_API_KEY
export NOTION_KEYRING=0

# Notion 검색
ntn api v1/search query="Agent OS Situation Room"

# 페이지를 Markdown으로 읽기
ntn api v1/pages/{page_id}/markdown

# 페이지를 Markdown으로 갱신
ntn api v1/pages/{page_id}/markdown -X PATCH markdown="..."

# data source query
ntn api v1/data_sources/{data_source_id}/query -X POST --json query.json
```

현재 환경 상태:

- `NOTION_API_KEY` 없음.
- `ntn` 미설치.
- 따라서 실제 Notion 생성/동기화 전에는 사용자의 Notion integration token과 대상 페이지 공유가 필요하다.

## 4. MVP 구현 순서

### Phase 1 — Notion 수동 대시보드 만들기

사용자가 Notion에서 빈 페이지를 만든다.

```text
Agent OS Situation Room
```

그리고 Hermes/Notion integration에 해당 페이지를 공유한다.

### Phase 2 — Hermes에서 Notion API 연결

필요 작업:

1. Notion integration 생성: https://notion.so/my-integrations
2. API key를 Hermes 환경에 저장: `NOTION_API_KEY`
3. 대상 Notion page를 integration에 `Connect to`로 공유
4. Linux 환경에 `ntn` 설치 또는 HTTP API fallback 사용

### Phase 3 — 데이터베이스 자동 생성

Hermes가 다음 DB를 생성한다.

- Agents
- Projects
- Tasks
- Handoffs
- Artifacts
- Health
- Decisions
- Second Brain Inbox

### Phase 4 — 단방향 sync

초기에는 안전하게 단방향으로만 동기화한다.

```text
Kanban / Drive manifest / status.json / cron output
  -> sync script
  -> Notion DB rows
```

Notion에서 잘못 편집한 내용이 원본 상태를 망치지 않도록 한다.

### Phase 5 — 선택적 양방향 workflow

충분히 안정화된 뒤 일부 필드만 양방향 허용한다.

허용 후보:

- Task priority
- Human decision status
- Note processed checkbox
- Comment / operator note

금지 후보:

- Drive file ID
- cron config
- API token/secret
- destructive action flag

## 5. Notion Workers 활용안

Notion Workers는 Business/Enterprise 또는 해당 기능 사용 가능 플랜이 필요할 수 있다. 가능하다면 다음 용도로 쓴다.

### 5.1 Sync Worker

외부 상태를 Notion DB로 주기적 반영.

```text
Hermes status.json / artifact-registry.json / project portfolio
  -> Notion Worker sync
  -> Notion databases
```

### 5.2 Tool Worker

Notion Custom Agent 안에서 Agent OS 정보를 조회하는 tool.

예:

- `get_agent_status(agent_name)`
- `get_project_summary(project_slug)`
- `list_blockers()`
- `create_inbox_capture(text, source)`

### 5.3 Webhook Worker

외부 이벤트를 Notion으로 수신.

예:

- GitHub PR merged
- cron failure
- Drive sync warning
- Graphify stale alert

주의: webhook URL은 secret 취급해야 한다.

## 6. Agent OS와의 권장 데이터 흐름

```text
[Google Drive / Markdown / JSON / Kanban]
        ↓ deterministic sync script
[Notion DBs: Agents, Projects, Tasks, Health, Artifacts]
        ↓ human views / filters / comments
[Operator decisions]
        ↓ approved sync fields only
[Hermes Kanban / Drive docs update]
```

## 7. 비용/안전 전략

- Notion은 사람이 보는 dashboard로 사용한다.
- 자동 갱신은 script-only cron으로 수행한다.
- LLM은 요약/판단이 필요할 때만 호출한다.
- secrets, OAuth token, API key는 Notion에 저장하지 않는다.
- 삭제/공유/권한 변경은 계속 사용자 확인이 필요하다.
- Notion Workers는 요금/플랜 확인 후 사용한다.

## 8. 바로 실행 가능한 다음 단계

1. 사용자가 Notion에서 `Agent OS Situation Room` 페이지 생성.
2. Notion integration 생성 후 해당 페이지에 연결.
3. Hermes에 `NOTION_API_KEY` 설정.
4. Hermes가 DB 스키마 자동 생성.
5. `agent_os_to_notion_sync.py` 작성.
6. 하루 2~4회 script-only cron으로 Notion 갱신.
7. Notion view 구성:
   - Today
   - Blocked
   - By Agent
   - By Project
   - Health
   - Recent Artifacts
   - Second Brain Inbox

## 9. 최종 권고

우리 Agent OS에서 Notion은 **대체 저장소**가 아니라 **작업자가 매일 여는 Mission Control UI**로 쓰는 것이 가장 안전하고 실용적이다.

가장 좋은 첫 MVP는 다음 한 문장이다.

> Drive/Kanban/JSON에서 이미 있는 Agent OS 상태를 Notion의 Agents·Projects·Tasks·Health·Artifacts DB로 미러링하고, 사용자는 Notion에서 필터/뷰/코멘트/의사결정만 한다.
