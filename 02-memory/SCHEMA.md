---
type: schema
title: LLM Wiki SCHEMA — 02-memory
tags: [meta, wiki, karpathy]
created: 2026-06-22
status: stable
---

# SCHEMA — Agent OS LLM Wiki (02-memory)

> 이 파일은 02-memory wiki의 **규칙 정본**이다. 에이전트는 매 세션 `02-memory/index.md` → 이 SCHEMA → 필요한 노트 순으로 orientation한다.
> 원칙(Karpathy LLM wiki): **"index이지 dump가 아니다."** 원문을 통째로 쌓지 않고, atomic 노트 + 링크 + frontmatter로 *찾을 수 있게* 둔다.

## 1. 왜 (설계 근거 / 레퍼런스)
- **Zettelkasten**: 한 노트 = 한 개념(atomic), 빽빽한 링크 → 구조는 링크에서 창발.
- **PARA / CODE** (Forte): 수집→정리→증류→표현. 저장이 아니라 *증류*가 목적.
- **MOC (Maps of Content)**: 링크를 모으는 인덱스 노트 = `index.md`.
- **Karpathy LLM Wiki**: 사람이 아니라 LLM 에이전트가 navigate하도록 frontmatter + wikilink + SCHEMA/index/log 백본.
- 정본 출처는 `[[REFERENCE]]`, owner 맥락은 `[[MY]]`, 운영 규칙은 `[[AGENT-OS]]`.

## 2. 노트 타입 (folder = type)
```
concepts/     개념·원칙·메커니즘 (atomic 1개념 1노트)
entities/     사람·도구·모델·프로젝트·에이전트
comparisons/  A vs B 비교·의사결정
queries/      자주 묻는 질문 + 답(근거 링크). graphify Q&A 저장소
raw/          미증류 원본(웹클립·논문발췌·레퍼런스 목록). 증류 전 임시
templates/    노트 템플릿
```

## 3. Frontmatter (모든 노트 필수)
```yaml
---
type: concept|entity|comparison|query|raw|moc
title: <사람이 읽는 제목>
tags: [<소문자-kebab>, ...]
created: YYYY-MM-DD
updated: YYYY-MM-DD        # 선택
source: "[[원본노트]]" 또는 경로/URL   # 근거
status: seed|draft|stable
---
```

## 4. 링크 규칙
- 본문에서 다른 노트는 항상 `[[note-title]]` 위키링크로 건다(고아 노트 금지).
- 모든 노트는 최소 1개 상위 MOC(`index.md` 또는 상위 개념)로 역링크되어야 한다.
- 주장에는 `source:` 또는 본문 인용으로 근거를 단다(미검증은 "시뮬레이션 수준" 명시 — `[[MY]]` §6).

## 5. 검색 우선 (query-first)
- 코드/구조 질문은 **graphify 먼저**: `graphify-out/graph.json`이 있으면 `graphify query "<질문>"`. 넓은 개요는 `graphify-out/GRAPH_REPORT.md`, 내비게이션은 `graphify-out/wiki/index.md`.
- 좋은 Q&A는 `queries/`에 저장(`graphify save-result` 연동 가능)해 재사용한다.

## 6. 승격 필터 (`[[MY]]` 5대 필터 통과분만 wiki로)
① 반복 재사용 ② 다른 에이전트/미래의 내가 읽어야 함 ③ 의사결정 근거 추적 ④ 재시도 금지 리스크 ⑤ 공통 규칙. 하나도 아니면 `raw/` 또는 일지에만.

## 7. 유지보수 (Hermes 루프 연계)
- 끊긴 wikilink·고아 노트·frontmatter 누락·노후 노트 점검 → `[[07-loop]]` routines.
- 변경은 `log.md`에 append.
