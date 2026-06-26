---
type: concept
title: Model Routing
tags: [models, routing]
created: 2026-06-22
source: "[[AGENT-OS]] §4 · 03-models/README · 04-agents/routing/model-handoff"
status: stable
---

# Model Routing

## 한 줄 정의
Agent(역할)와 Model(실행 엔진)을 분리하고, 작업 유형별로 모델을 라우팅하는 규칙.

## 핵심
```
Claude  = planning, reasoning, research, documentation, review
Codex   = implementation, debugging, testing, Git/CLI
Gemini  = optional/future — multimodal, long-context, alternate review
```
- 기본 복합작업 흐름: Claude plan → Codex 구현 → Codex 검증 → Claude 리뷰 → (선택)Gemini 교차리뷰 → Memory/Dashboard/Slack 반영.
- **Agent ≠ Model**: Agent는 책임·workflow·handoff, Model은 실행 엔진 (`[[7-layer-architecture]]` Layer 3 vs Layer 4).

## 근거 / 출처
- `[[AGENT-OS]]` §3–4, `04-agents/routing/model-handoff.md`.

## 관련
- [[index]]
- [[7-layer-architecture]]
- [[hermes]]
