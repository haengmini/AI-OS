---
type: query
title: "Q: How does the Hermes loop work?"
tags: [qa, loop]
created: 2026-06-22
source: "graphify query (2026-06-22) · [[loop-flow]]"
status: stable
---

# Q: Hermes 루프는 어떻게 동작하나?

## A (요약)
Production 산출 → Dashboard JSON 갱신 → **Hermes 리뷰** → Memory 갱신 → Slack 보고 → 다음 액션. Hermes는 Dashboard를 읽고 blocked/지연/검증누락/stale memory/반복 수작업/리소스 과다/미보고/미종료 태스크를 점검한 뒤, Memory·Dashboard·리포트를 갱신하고 다음 작업·담당·우선순위·리스크·검증을 제안한다.

## 근거
- `graphify query "How does the Hermes loop work?"` (2026-06-22) → 시작노드 [[hermes]], [[loop-flow]], 커뮤니티 "Hermes Loop & Routines".
- 정본: `[[loop-flow]]`, `07-loop/README.md`.

## 관련
- [[index]] · [[hermes]]
