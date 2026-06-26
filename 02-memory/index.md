---
type: moc
title: 02-memory — Wiki Index (MOC)
tags: [moc, entry-point]
created: 2026-06-22
status: stable
---

# 02-memory — LLM Wiki Index

> **에이전트 진입점.** 세션 시작 시: 이 파일 → `[[SCHEMA]]` → 필요한 노트.
> 규칙·구조는 `[[SCHEMA]]`. 변경 이력은 `[[log]]`.

## 검색 먼저 (query-first)
- 그래프: `graphify query "<질문>"` (전제: `graphify-out/graph.json` — 빌드됨 2026-06-22)
- 개요: `graphify-out/GRAPH_REPORT.md` · 내비: `graphify-out/wiki/index.md`
- 저장된 Q&A: `queries/`

## 폴더
- [[README]] — Layer 2 Memory overview
- `concepts/` — 개념·원칙
- `entities/` — 사람·도구·모델·프로젝트
- `comparisons/` — 비교·의사결정
- `queries/` — Q&A
- `raw/` — 미증류 원본
- `templates/` — 노트 템플릿

## 핵심 개념 (seed)
- [[7-layer-architecture]] — Agent OS 최우선 구조
- [[hardware-layer]] · [[memory-layer]] · [[models-layer]] · [[agents-layer]] · [[dashboard-layer]] · [[production-layer]] · [[loop-layer]] — 7-layer 하위 계층 노트
- [[model-routing]] — Claude/Codex/Gemini 역할 분담
- [[drive-first-source-of-truth]] — Drive 정본, 로컬은 캐시
- [[progressive-disclosure]] — index 먼저, 세부는 필요할 때
- [[memory-promotion-filter]] — wiki 승격 5대 필터

## 핵심 엔터티 (seed)
- [[hermes]] — Layer 7 루프 에이전트
- [[graphify]] — 지식 그래프 도구

## 비교 / 결정
- [[postgres-vs-drive-as-agent-bus]] — 에이전트 조율 백엔드 선택

## 저장된 Q&A
- [[how-does-hermes-loop-work]] — Hermes Layer 7 loop 동작 방식

## 정본 포인터
- 운영 규칙 → `[[AGENT-OS]]` · owner 맥락 → `[[MY]]` · 설계 출처 → `[[REFERENCE]]`
