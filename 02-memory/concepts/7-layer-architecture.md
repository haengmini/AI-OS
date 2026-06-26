---
type: concept
title: 7-Layer Architecture
tags: [architecture, core-rule]
created: 2026-06-22
source: "[[AGENT-OS]] §1"
status: stable
---

# 7-Layer Architecture

## 한 줄 정의
Agent OS의 **최우선 고정 규칙** — 모든 작업은 7개 계층 순서를 따른다.

## 핵심
```
Hardware → Memory → Models → Agents → Dashboard+Slack → Production → Loop
```
- 구조는 고정, **도메인은 module처럼 확장**(`[[AGENT-OS]]` §10).
- 각 계층 정본: [[hardware-layer]]·[[memory-layer]]·[[models-layer]]·[[agents-layer]]·[[dashboard-layer]]·[[production-layer]]·[[loop-layer]] (※ 일부는 아직 노트 미생성 — 점진 추가).

## 근거 / 출처
- `[[AGENT-OS]]` §1 Highest Priority Rule (정본).

## 관련
- [[index]]
- [[model-routing]] — Layer 3
- [[hermes]] — Layer 7 실행 주체
