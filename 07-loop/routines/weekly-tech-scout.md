---
type: routine
title: Weekly Tech Scout Loop
layer: loop
owner_agent: researcher + curator
cadence: weekly (월요일)
created: 2026-06-23
status: design-ready
---

# Weekly Tech Scout Loop

기술 트렌드·외부 소스를 주기 조사해 Agent OS에 적용 가능한 인사이트로 변환.

## 입력
`[[ai-agent-ecosystem-radar]]`의 GitHub/Reddit/YouTube + arXiv(ISP/LLIE/agent) + Notion "문서 허브".

## 흐름
1. **수집(결정적·무료)**: GitHub release watch(claude-code/codex/hermes-agent/graphify/ponytail), Reddit/arXiv 키워드. cron이 신규만 추림.
2. **선별(모델)**: 새 항목을 5대 승격 필터(`[[memory-promotion-filter]]`)로 평가 — 흡수가치 있는 것만.
3. **승격**: 가치 있으면 `02-memory/30-resources/` 또는 `concepts/`에 atomic 노트 + radar 갱신.
4. **보고**: 주간 digest를 `07-loop/reports/`(또는 situation-room) + Slack 요약.

## 산출
- `30-resources/` 신규 노트 + `[[ai-agent-ecosystem-radar]]` 갱신
- 주간 digest(변경분만)

## cron (제안, Hermes)
```
0 9 * * 1  weekly-tech-scout: release/feed 스캔 → 신규 목록 → (모델 선별은 세션) → digest
```
수집/알림은 무료 cron, 선별·요약만 모델(비용). paid run은 `[[agent-os-execution-trace-telemetry-2026-06-23]]` 가드 적용.

## 연계
- 흡수된 도구·패턴 → #19 에이전트 설계, #18 Chorus, graphify 갱신에 환류.
