---
title: P0 Patches — Wiki Entry Wiring + Codex Hook Fix
created: 2026-06-23
owner: 이형민
status: ready-to-apply
note: Cowork 커넥터는 기존 파일 in-place 수정 불가 → 아래를 Hermes 또는 Windows 데스크톱에서 적용.
---

# P0 패치 (task #10, #11)

기존 파일 직접 수정이 필요해 Claude(Cowork)가 못 붙였다. 아래 그대로 적용하면 된다.

## #10 — 위키·graphify 진입 규칙 배선

목적: Second Brain·graphify를 만들어 놨지만 에이전트가 *입구로 안 들어와서* 안 쓰는 문제 해결.

### A. `CLAUDE.md` — "0. Read First"에 두 줄 추가
```text
02-memory/index.md → 지식·위키 진입점(MOC). 그 다음 02-memory/SCHEMA.md(노트 규칙).
graphify-out/graph.json 있으면 코드·구조 질문은 `graphify query "<질문>"` 먼저(raw grep 전).
```

### B. `AGENT-OS.md` — §0 또는 §2 운영 규칙에 한 줄
```text
지식 작업은 02-memory/index.md → SCHEMA.md를 먼저 읽고, graphify query를 raw 탐색보다 우선한다.
```

### C. `GEMINI.md`, `AGENTS.md` — 같은 한 줄 추가
```text
Session start for knowledge work: read 02-memory/index.md → SCHEMA.md; prefer `graphify query` over raw file search when graphify-out/graph.json exists.
```

(`02-memory/SCHEMA.md` §5에는 query-first가 이미 명시돼 있음 — 위는 *진입 파일들이 거기로 보내도록* 거는 것.)

## #11 — `.codex/hooks.json` Windows 경로 수정

원인: command가 `C:\Users\user\...\graphify.EXE`로 박혀 Linux Hermes에서 무효.

### 방법 1 (권장, 자동): vault 루트에서
```bash
graphify codex install
```

### 방법 2 (수동): `.codex/hooks.json` 전체를 아래로 교체
```json
{ "hooks": { "PreToolUse": [ { "matcher": "Bash",
  "hooks": [ { "type": "command", "command": "graphify hook-check" } ] } ] } }
```
`graphify`는 PATH의 것을 쓰므로 Windows·Linux 공통. (Hermes는 setup-graphify-hermes.sh의 wrapper로 PATH 보장됨.)

## 적용 확인
```bash
# #10: 에이전트가 세션 시작 시 02-memory/index.md를 읽는지(수동 확인) + graphify query 우선
# #11:
graphify hook-check </dev/null; echo $?   # 0이면 정상
```
