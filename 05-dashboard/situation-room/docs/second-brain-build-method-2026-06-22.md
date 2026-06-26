# Second Brain 만드는 방법 — Agent OS / Obsidian / Graphify / Multi-Model Workspace

- 작성일: 2026-06-22
- 대상: 이형민 Agent OS workspace
- 원칙: Google Drive가 원본/source of truth, Hermes local은 cache/mirror/execution layer
- 목표: Claude, Gemini, Hermes, Codex, Obsidian, 여러 디바이스가 같은 지식/로그/산출물을 보고 함께 일하는 Second Brain 구축

## 0. 한 문장 정의

Second Brain은 단순한 노트 앱이 아니라 다음 네 가지가 합쳐진 운영체계다.

```text
공유 저장소 + 지식 구조 + 자동 동기화/감지 + 에이전트 작업 루프
```

우리 환경에서는 다음으로 구현한다.

```text
Google Drive = 원본 문서 저장소
Obsidian vault = 사람이 읽고 편집하는 지식 UI
LLM Wiki = AI가 읽고 갱신하는 구조화된 Markdown 지식베이스
Graphify = vault 전체의 지식 그래프/질의 계층
Hermes Agent OS = 작업 실행, cron, 감지, 요약, Drive upsert, Slack 보고
Claude/Gemini/Codex = 설계/분석/구현/재빌드 전문 모델 세션
Situation Room = 현재 상태/작업/산출물/리스크 대시보드
```

## 1. 핵심 아키텍처

```text
[Human / Devices]
  ├─ Obsidian desktop/mobile
  ├─ Claude
  ├─ Gemini
  ├─ Codex
  └─ Slack
        │
        ▼
[Google Drive: Agent OS]  ← canonical source of truth
        │
        ▼ sync/archive
[Hermes local mirror: /opt/data/agent_os_archive/files]
        │
        ├─ LLM Wiki: SCHEMA.md / index.md / log.md / entities / concepts / raw
        ├─ Graphify: graphify-out/graph.json / GRAPH_REPORT.md / wiki
        ├─ Situation Room: status.json / artifact-registry.json / docs
        └─ Cron/agents: sync, healthcheck, staleness, reports
```

## 2. 폴더 구조

Vault root는 현재 다음 경로를 사용한다.

```text
/opt/data/agent_os_archive/files
```

Drive에서는 Agent OS 폴더가 원본이다.

권장 구조:

```text
Agent OS/
├── AGENT-OS.md
├── CLAUDE.md
├── GEMINI.md
├── AGENTS.md
├── SCHEMA.md
├── index.md
├── log.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   └── assets/
├── entities/
├── concepts/
├── comparisons/
├── queries/
├── graphify-out/
│   ├── graph.json
│   ├── GRAPH_REPORT.md
│   ├── STATUS.md
│   └── wiki/
├── 04-agents/
├── 05-dashboard/
│   └── situation-room/
│       ├── docs/
│       ├── state/
│       └── ui/
├── 06-production/
│   ├── dfxisp/
│   └── ai-drone/
└── 07-loop/
```

## 3. 만드는 순서

### Phase 1 — Drive-first vault 확정

목표:

```text
모든 모델과 디바이스가 같은 원본을 보게 만든다.
```

작업:

1. Google Drive `Agent OS`를 원본으로 확정한다.
2. Hermes local mirror는 `/opt/data/agent_os_archive/files`로 고정한다.
3. 모든 보고서/로그/산출물은 Drive에 먼저 upsert하고, local은 cache로 둔다.
4. Obsidian은 Drive-backed vault를 연다.
5. Claude/Gemini/Codex/Hermes 모두 root 지시 파일을 읽게 한다.

필수 규칙:

```text
완료 보고 = Drive link/file ID + local cache path + 검증 결과
```

### Phase 2 — LLM Wiki backbone 생성

목표:

```text
노트 더미가 아니라 AI가 누적 관리할 수 있는 지식베이스로 만든다.
```

필수 파일:

```text
SCHEMA.md  # 규칙/택소노미/페이지 기준
index.md   # 전체 지식 카탈로그
log.md     # append-only 작업 기록
```

필수 폴더:

```text
raw/
entities/
concepts/
comparisons/
queries/
```

운영 규칙:

1. 모든 wiki page는 YAML frontmatter를 가진다.
2. 모든 page는 최소 2개 이상 wikilink를 가진다.
3. 모든 page는 `index.md`에 등록된다.
4. 모든 ingest/update/query/lint는 `log.md`에 기록된다.
5. raw source는 원본 보존용이므로 수정하지 않는다.

### Phase 3 — Graphify graph 생성

목표:

```text
vault 전체를 그래프로 만들어 AI가 빠르게 질의하고 관계를 추적하게 한다.
```

현재 Hermes에서는 wrapper가 설정되어 있다.

```bash
cd /opt/data/agent_os_archive/files
graphify query "How does the Hermes loop work?"
graphify explain "7-Layer Architecture"
```

핵심 산출물:

```text
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/STATUS.md
graphify-out/wiki/index.md
```

운영 분리:

```text
Hermes/free/script-only = staleness 감지
Claude/Codex/Gemini/model session = semantic rebuild
Drive = rebuilt graphify-out 원본 저장
```

### Phase 4 — Multi-model operating contract

목표:

```text
모델마다 다른 일을 맡기되 같은 상태와 문서를 보게 한다.
```

역할 예시:

```text
Claude = Brain / 설계 / 계획 / 리뷰 / 문서 구조화
Gemini = 긴 문맥 / multimodal / 대량 자료 요약
Codex = 구현 / 디버깅 / 테스트 / Git/CLI
Hermes = 실행 / Drive sync / cron / Slack / Agent OS governance
Obsidian = 사람이 읽고 편집하는 UI
Graphify = 지식 그래프 질의/관계 탐색
```

모든 모델이 읽어야 할 파일:

```text
AGENT-OS.md
CLAUDE.md
GEMINI.md
AGENTS.md
SCHEMA.md
index.md
log.md
graphify-out/wiki/index.md
graphify-out/GRAPH_REPORT.md
05-dashboard/situation-room/state/artifact-registry.json
05-dashboard/situation-room/state/status.json
```

### Phase 5 — Situation Room 구축

목표:

```text
Second Brain을 사람이 보고, AI가 읽고, cron이 갱신하는 상황판으로 만든다.
```

필수 산출물:

```text
05-dashboard/situation-room/state/status.json
05-dashboard/situation-room/state/artifact-registry.json
05-dashboard/situation-room/docs/situation-board.md
05-dashboard/situation-room/docs/second-brain-health.md
05-dashboard/situation-room/ui/index.html
```

상황판에 들어갈 정보:

- 현재 프로젝트
- active agents
- Kanban board 상태
- 최근 Drive artifacts
- graphify staleness
- broken wikilinks
- pending rebuild
- human attention needed
- 다음 작업자/다음 액션

### Phase 6 — 자동 루프

목표:

```text
사람이 매번 기억하지 않아도 시스템이 stale 상태를 감지하고 보고한다.
```

현재/권장 루프:

```text
08:50 Drive archive sync
09:00 Slack/session archive
09:05 graphify staleness check
09:10 agent-team healthcheck
주기적 project review
주기적 second-brain healthcheck
```

Graphify staleness 흐름:

```text
markdown 변경 발생
→ graphify-staleness-check.sh가 STALE 감지
→ graphify-out/needs_update 생성
→ Slack/상황판에 재빌드 필요 표시
→ Claude/Codex/Gemini가 semantic rebuild 수행
→ graphify-out을 Drive에 upsert
→ Hermes archive sync
→ FRESH 확인
```

## 4. 일상 사용법

### 새 자료 넣기

```text
1. raw/articles 또는 raw/papers에 원본 저장
2. 관련 entities/concepts 업데이트
3. index.md 업데이트
4. log.md 기록
5. graphify staleness는 STALE이 됨
6. 필요할 때 semantic rebuild
```

### 질문하기

1. 먼저 Graphify query를 실행한다.

```bash
graphify query "질문"
```

2. 부족하면 관련 wiki page를 읽는다.
3. 답변이 가치 있으면 `queries/`에 저장한다.
4. log.md에 기록한다.

### 프로젝트 작업하기

```text
06-production/<project>/spec.md
06-production/<project>/plan.md
06-production/<project>/tasks.md
06-production/<project>/experiment-log.md
06-production/<project>/verification-plan.md
```

프로젝트 작업 결과는 Situation Room과 artifact registry에 등록한다.

## 5. 품질 기준

좋은 Second Brain:

```text
- 같은 질문을 반복할수록 더 똑똑해진다.
- 모든 산출물이 Drive에서 찾을 수 있다.
- 어떤 모델이 들어와도 SCHEMA/index/log/graph를 보고 맥락을 복구한다.
- 사람이 보기 좋은 Obsidian graph와 AI가 쓰기 좋은 graphify graph가 같이 있다.
- stale 상태와 미완료 작업이 자동으로 드러난다.
```

나쁜 Second Brain:

```text
- 보고서가 local root나 tmp에 흩어진다.
- index/log가 없어 무엇이 있는지 모른다.
- Graphify가 오래되어 틀린 graph를 본다.
- Claude/Gemini/Codex/Hermes가 서로 다른 파일을 본다.
- Slack에는 말이 많은데 Drive에는 canonical artifact가 없다.
```

## 6. 우리 시스템의 현재 상태

현재 이미 된 것:

```text
Drive-backed Agent OS folder
Obsidian vault config
Claude/Gemini/Codex/Hermes root instruction files
Graphify graphify-out sync
Graphify wrapper/PATH setup
Graphify staleness checker
Hermes cron for staleness detection
Situation Room docs/state/artifact registry 시작
Drive-first report workflow
Agent OS role profiles and Kanban boards
```

아직 강화할 것:

```text
SCHEMA.md / index.md / log.md 완성
raw/entities/concepts/comparisons/queries 체계화
Second Brain healthcheck 자동화
Graphify rebuild handoff protocol
Slack STALE-only 알림
Obsidian/Drive/headless sync 정책 확정
모델별 역할/프로필 specialization 강화
```

## 7. 다음 실행 작업 리스트

즉시 실행 권장 순서:

1. `SCHEMA.md`, `index.md`, `log.md`를 Drive root에 생성/정비한다.
2. 기존 Markdown 100개를 분류해서 index에 1차 등록한다.
3. `raw/`, `entities/`, `concepts/`, `comparisons/`, `queries/` 폴더를 확정한다.
4. `second-brain-health.json/md`를 생성한다.
5. Graphify staleness가 STALE이면 Claude/Codex/Gemini에게 semantic rebuild를 맡긴다.
6. Situation Room에 Second Brain status card를 추가한다.
7. Slack에는 FRESH는 조용히, STALE만 알림 보내도록 한다.

## 8. 최종 운영 원칙

```text
Drive에 없으면 완료가 아니다.
index/log에 없으면 기억된 것이 아니다.
graphify에 없으면 모델이 빠르게 찾을 수 없다.
Situation Room에 없으면 운영 상태가 아니다.
검증 없이는 완료가 아니다.
```
