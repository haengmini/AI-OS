---
type: concept
title: Progressive Disclosure
tags: [principle, token-economy, retrieval]
created: 2026-06-22
source: "[[REFERENCE]] §7 · [[CLAUDE]] §2"
status: stable
---

# Progressive Disclosure

## 한 줄 정의
항상 모든 정보를 모델에 넣지 않고, **index/summary 먼저 → 필요할 때 세부 로드**.

## 핵심
- 폴더는 README/index부터 읽고 필요한 파일만 연다(토큰 절약).
- LLM-wiki의 존재 이유: `[[index]]` → `[[SCHEMA]]` → 개별 노트의 계단식 접근.
- graphify `query`도 같은 사상 — 전체 GRAPH_REPORT 대신 **scoped subgraph**만 반환.
- 같은 뿌리: [[memory-promotion-filter]](저장 단계의 절제), Zettelkasten(atomic).

## 근거 / 출처
- `[[REFERENCE]]` §7 Operating Theory, `[[CLAUDE]]` §2 규칙 7.

## 관련
- [[index]]
- [[memory-promotion-filter]]
- [[graphify]]
