---
type: concept
title: Hardware Layer
tags: [architecture, layer-1, hardware]
created: 2026-06-22
updated: 2026-06-22
source: "[[7-layer-architecture]] · [[AGENT-OS]]"
status: seed
---

# Hardware Layer

## 한 줄 정의
Agent OS 7-layer architecture의 Layer 1. 실제 실행 환경, 장치, 서버, FPGA/ASIC/드론 보드 같은 물리·컴퓨팅 기반을 의미한다.

## 핵심
- Agent OS는 추상 문서 시스템이 아니라 실제 hardware/project execution 위에서 돈다.
- DFXISP에서는 Zynq UltraScale+ ZCU104, FPGA/ISP pipeline, verification hardware가 이 계층에 속한다.
- AI드론에서는 ASIC/board/sensor/edge compute가 이 계층에 속한다.

## 관련
- [[7-layer-architecture]]
- [[production-layer]]
