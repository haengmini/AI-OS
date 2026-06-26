---
type: entity
title: Hermes
tags: [agent, loop, layer-7]
created: 2026-06-22
source: "[[07-loop]] · [[loop-flow]] · [[agent-routing-contract]]"
status: stable
---

# Hermes

## 한 줄 정의
Agent OS **Layer 7 Loop 에이전트** — Linux 서버에서 24/7 cron으로 도는 점검·기록·보고·디스패치 주체.

## 핵심
- 역할: Dashboard 읽기 → blocked/지연/검증누락/stale 점검 → Memory·Dashboard 갱신 → Slack 보고 → 다음 액션 제안 (`[[loop-flow]]`).
- 환경: `/opt/data` (HOME=HERMES_HOME=/opt/data), vault 미러 `/opt/data/agent_os_archive/files`. graphifyy 설치됨(2026-06-22).
- 멀티에이전트에서 **유일한 상시 가동 노드** → 30분 폴링보다 "Hermes가 감지하고 다른 모델을 깨우는" 디스패처 패턴이 맞음. → [[postgres-vs-drive-as-agent-bus]].
- 이름 충돌 주의: 내부 Layer 7 loop agent vs 외부 NousResearch Hermes (별개).

## 관련
- [[index]] · [[7-layer-architecture]] · [[model-routing]] · [[graphify]]
