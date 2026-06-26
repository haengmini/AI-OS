---
type: concept
title: Production Layer
tags: [architecture, layer-6, production, projects]
created: 2026-06-22
updated: 2026-06-22
source: "[[7-layer-architecture]] · [[drive-first-source-of-truth]]"
status: seed
---

# Production Layer

## 한 줄 정의
Agent OS 7-layer architecture의 Layer 6. DFXISP, AI드론 같은 실제 프로젝트 산출물·실험·검증이 생성되는 계층이다.

## 핵심
- 프로젝트별 spec, plan, tasks, experiment log, verification plan을 분리한다.
- 결과물은 Drive에 canonical artifact로 저장하고 artifact registry에 등록한다.
- Production output은 [[dashboard-layer]]와 [[loop-layer]]가 검토한다.

## 관련
- [[7-layer-architecture]]
- [[hardware-layer]]
- [[loop-layer]]
