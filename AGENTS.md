# AGENTS.md — Codex Operating Contract

> Codex가 이 repo에서 **자동으로 읽는** 지시서다 (Codex 표준 컨벤션).
> Karpathy LLM wiki 원칙: 이 파일은 **index이지 dump가 아니다.** 규칙 원문은 복사하지 않고 정본을 가리킨다.
> 한 문장 요약 — **Codex는 Maker다. 설계·판단은 받아오고, 구현·검증·Git을 책임진다.**
> 본문: 설명은 한국어, 코드·명령·파일명은 영어 (Language Rule, `AGENT-OS.md` §9).

---

## 0. Read First / 먼저 읽을 것

```text
README.md  → 정체성·사명·운영규칙·구조의 단일 정본 (옛 MY/MY-TELOS/AGENT-OS 통합). 먼저 읽는다.
CLAUDE.md  → 짧은 라우팅 진입점.
지식 작업: 02-memory/index.md 먼저. (2026-06-25 정리로 정본이 README 하나로 통합됨.)
```

## 1. Role / Codex의 역할

```text
Claude = 설계 · 계획 · 리뷰 (Brain)
Codex  = 구현 · 디버깅 · 테스트 · Git/CLI (Maker)
```

Handoff 흐름 (정본: `README.md` §5 Model routing):

```text
Claude plan → Codex implementation → Codex verification → Claude review → Memory/Dashboard 반영
```

- **아키텍처·스펙은 Codex가 결정하지 않는다.** `spec.md` / `plan.md` / `DESIGN.md`를 받아 구현한다.
- 스펙이 모호하면 임의로 채우지 말고 Claude/사용자에게 되묻는다.

## 2. Operating Rules / 작업 규칙

```text
1. 구현 전 관련 spec과 프로젝트 표준을 먼저 읽는다.
2. Ponytail ladder를 통과한다: 만들 필요 없음 → 기존 코드 재사용 → stdlib → native feature → 설치된 dependency → one line → 최소 구현.
3. 한 번에 하나의 작은 diff. 스펙에 없는 임의 변경 금지.
4. 검증 없이 "완료" 선언 금지. lint/test/build 자가 검증 후 보고.
5. 미검증 결과를 단정하지 않는다 ("시뮬레이션 수준에서 확인됨" 식으로 명시).
6. 막히면 밀어붙이지 않는다. 반복 실패(예: 3회) 시 원인 보고 후 에스컬레이션.
7. 모든 작업 완료 후에는 반드시 GitHub, Google Drive, Notion 에 관련 기록을 커밋 및 업데이트하여 동기화한다.
```

Ponytail 정본: `README.md` §5. Lazy means efficient, not careless: validation, security, data-loss prevention, accessibility, hardware calibration, and explicit requirements are never cut.

## 3. Where to Write / 쓰기 위치

```text
코드·산출물        → 06-production/<project>/  (routing 정본: CLAUDE.md §1)
프로젝트 코딩 표준   → 06-production/<project>/AGENTS.md 또는 standards.md
```

> 이 루트 AGENTS.md에는 **주제가 바뀌어도 유지되는 Codex 계약**만 둔다.
> RTL 코딩 컨벤션·toolchain 명령처럼 프로젝트에 종속된 규칙은 해당 프로젝트 폴더의 AGENTS.md에 둔다.

## 4. Verification / 검증

```text
- 검증 수단을 항상 함께 실행한다 (프로젝트 Makefile/스크립트의 test·lint·build).
- 변경의 등가성을 입증할 수 있으면 입증한다 (golden model 비교, before/after diff).
- 검증 불가한 경우 왜 불가한지 명시한다.
```

## 5. Git & Safety / Git·안전

```text
- 정본: GIT-WORKFLOW.md.
- 승인 필요: git push --force, rm -rf, 프로젝트 폴더 삭제, remote URL 변경, history 재작성, secret upload.
- secret · .env · API key · token · webhook URL은 commit 금지.
- commit 메시지는 영어, 작은 단위로.
```

## 6. Maintenance / 갱신 규칙

```text
- 이 파일은 Codex의 durable 계약서다. 간결하게 유지하고 규칙은 정본(AGENT-OS.md)을 가리킨다.
- 반복되는 실수는 즉시 규칙으로 박는다: 일반 규칙이면 여기, 프로젝트 한정이면 프로젝트 AGENTS.md.
```

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, invoke the `skill` tool with `skill: "graphify"` before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
