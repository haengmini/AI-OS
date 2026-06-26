---
title: Frontmatter Migration Spec (기존 정본 문서)
task: P2 #21
created: 2026-06-23
owner: 이형민
status: ready-to-apply (Hermes/데스크톱에서 실행 — 커넥터 in-place 수정 불가)
---

# Frontmatter 소급 변환 스펙

기존 정본 문서(MY/AGENT-OS 등)는 frontmatter·wikilink가 없어 SCHEMA 표준과 불일치. Cowork 커넥터는 기존 파일 in-place 수정이 안 되므로 **Hermes 배치 또는 Windows 데스크톱**에서 적용.

## 대상 (vault 루트 + 04-agents)
MY.md, AGENT-OS.md, README.md, Manual.md, OPERATION.md, REFERENCE.md, GIT-WORKFLOW.md, prompt-standards.md, 04-agents/*, 01~07 layer README.
(제외: `.graphifyignore` 대상 — 변경 불필요한 것은 건너뜀.)

## 각 파일 상단에 추가할 frontmatter 템플릿
```yaml
---
type: <doc|concept|moc>
title: <문서 제목>
layer: <01-hardware..07-loop|root>
tags: [<kebab>]
created: <원본 생성일>
status: stable
source: ""   # 정본이면 비움
---
```
(SCHEMA.md `[[SCHEMA]]` §3 기준. 본문은 그대로 두고 상단에만 추가.)

## wikilink
본문에서 다른 문서 언급 시 `[[문서명]]`로 전환(예: "AGENT-OS.md §1" → "[[AGENT-OS]] §1"). 고아 노트 0 유지.

## 적용 방법 (택1)
1. **Hermes 배치 스크립트**: vault 미러에서 각 .md 상단에 frontmatter prepend(없을 때만) → Drive upsert. 멱등.
2. **Windows 데스크톱**: Obsidian/에디터로 핵심 파일부터 수동(가장 안전).

## 우선순위
MY.md → AGENT-OS.md → 04-agents/routing/* (에이전트가 가장 자주 읽음) → 나머지.

## 검증
변환 후 `graphify update` 또는 wiki lint로 frontmatter 누락·깨진 링크 0 확인 → Health "Second Brain Wiki" 갱신.
