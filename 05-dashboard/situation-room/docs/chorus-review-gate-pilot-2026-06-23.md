---
title: Chorus Review Gate — Pilot Plan
task: P2 #18
created: 2026-06-23
owner: 이형민
status: ready (Chorus 환경 설정 필요)
---

# Chorus Review Gate — 파일럿 계획

여러 AI 모델이 한 산출물을 교차 검토하는 peer-review 게이트를 Agent OS에 1회 실제 적용.

## 위치(아키텍처)
Artifact 생성 → **Chorus 멀티모델 리뷰** → reviewer가 verdict 정리 → PM 다음 작업 결정 → reporter가 Drive/Slack 기록. (`[[agent-os-canonical-roadmap-2026-06-23]]`의 reviewer 역할 확장; model-registry `chorus` = not_configured.)

## 파일럿 대상 (택1, 추천 1번)
1. **DFXISP A1 아키텍처** ([[dfxisp-A1-architecture-fpga-constraints-2026-06-23]]) → `architect-review`. "DFX vs register-only" 판단을 다모델이 교차 검증 — 연구 판단이라 가치 큼.
2. dashboard/substrate config diff → `review-only`.

## 흐름
```
input artifact → chorus (architect-review) → 모델별 의견 수집 →
reviewer 종합 verdict(pass/blocker/의견) → Drive artifact 저장 → Slack 요약
```

## 전제 (실행 전 필요)
- Chorus 설치/실행 환경 확정(Hermes 또는 로컬).
- reviewer 모델 연결: Claude + (Codex/Gemini 중 1+) — paid이므로 승인 후. model-registry `chorus`/`gemini`를 available로.
- 비용: 다모델 호출 → `[[agent-os-execution-trace-telemetry-2026-06-23]]` runs/가드로 추적.

## 성공 기준
- A1 1건이 Chorus 교차리뷰를 통과/보완 → verdict 문서가 `situation-room/docs/chorus-review-pilot-<date>.md`로 저장.
- 이후 code diff review로 확장.

## 상태
설계 ready. **실제 실행은 Chorus 환경 + 모델 키 승인 후** (Cowork에서 Chorus 직접 구동 불가).
