---
type: entity
title: Graphify
tags: [tool, knowledge-graph, memory, layer-2]
created: 2026-06-22
source: "[[graphify-setup]] · graphify-out/"
status: stable
---

# Graphify

## 한 줄 정의
폴더를 읽어 **지식 그래프**(graph.json + 커뮤니티 + query/path/explain)를 만드는 CLI/스킬. 패키지 `graphifyy`, 명령 `graphify`.

## 핵심
- 빌드된 그래프(2026-06-22): **82 nodes · 168 edges · 8 communities**, `Agent OS/graphify-out/`.
- 사용: `graphify query "<질문>"`(scoped subgraph), `path`, `explain`. 개요 `GRAPH_REPORT.md`, 내비 `wiki/index.md`.
- 백엔드: GEMINI 키 없으면 **호스트 AI 세션이 semantic 백엔드**(외부 API 비용 0). md는 의미추출이 모델 필요, 코드만이면 `graphify update .`(AST, 무료).
- 검색 우선 규칙은 `[[SCHEMA]]` §5. Q&A 저장은 `queries/` (`graphify save-result`).

## 관련
- [[index]] · [[progressive-disclosure]] · [[hermes]]
