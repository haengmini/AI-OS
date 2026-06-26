---
type: concept
title: Dashboard Layer
tags: [architecture, layer-5, dashboard, situation-room]
created: 2026-06-22
updated: 2026-06-22
source: "[[7-layer-architecture]] · [[drive-first-source-of-truth]]"
status: seed
---

# Dashboard Layer

## 한 줄 정의
Agent OS 7-layer architecture의 Layer 5. Situation Room, Slack digest, status JSON, artifact registry가 사람과 에이전트에게 현재 상태를 보여주는 계층이다.

## 핵심
- HTML은 유일한 상태 저장소가 아니어야 한다.
- 중요한 사실은 Markdown, JSON, Drive artifact registry에도 있어야 한다.
- Slack은 짧은 알림/요약 채널이고, 정본 문서는 Drive에 둔다.

## 관련
- [[7-layer-architecture]]
- [[drive-first-source-of-truth]]
- [[loop-layer]]
