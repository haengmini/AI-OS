---
type: concept
title: Loop Layer
tags: [architecture, layer-7, loop, hermes]
created: 2026-06-22
updated: 2026-06-22
source: "[[7-layer-architecture]] · [[hermes]]"
status: seed
---

# Loop Layer

## 한 줄 정의
Agent OS 7-layer architecture의 Layer 7. Hermes가 주기적으로 sync, healthcheck, staleness, report, next action을 수행하는 운영 루프 계층이다.

## 핵심
- Loop는 production output을 검토하고 memory/dashboard/slack을 갱신한다.
- Graphify staleness check는 이 계층의 무료 감지 루프이다.
- Semantic rebuild는 모델 세션이 수행하고 Hermes가 Drive sync와 검증을 담당한다.

## 관련
- [[7-layer-architecture]]
- [[hermes]]
- [[07-loop]]
