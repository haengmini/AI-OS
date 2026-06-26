---
type: reference
title: Role–Model Map & Future Roles Decision
task: P2 #19
layer: agents
created: 2026-06-23
status: proposal (형민 sign-off 필요)
---

# Role–Model Map & Future Roles

> agent≠model. 역할이 먼저, 모델은 배정. 정본 데이터 = `situation-room/state/{agent,model}-registry.json`. 이 문서는 *결정/근거*.

## 1. 현재 역할별 모델 배정 (제안)
| Role | 권장 모델 | execution | cost | 근거 |
|---|---|---|---|---|
| operator/pm/governor | Hermes profile | hermes-profile | local | 라우팅·계획, 무료 상시 |
| researcher | Hermes/Claude | hermes-profile | local→paid | 깊은 조사 시 Claude |
| analyst | **Claude** | hermes-profile | paid | reasoning·아키텍처 |
| coder | **Codex** | cli | paid | 구현·디버그 (DFXISP-C1 담당) |
| reviewer | Claude (+Chorus 옵션) | hermes-profile/chorus | local→paid | 검증·교차리뷰 |
| reporter | Hermes/Gemini | hermes-profile | local | 요약·digest |
| admin/auditor/curator/sentinel | Hermes profile | hermes-profile | local | 운영·감사·감시 |

원칙: paid(Claude/Codex/Gemini)는 model-registry `available`일 때만, 비용은 #16 가드.

## 2. Future roles — profile vs alias 결정 (제안)
| 역할 | 권장 | 이유 |
|---|---|---|
| SW Coder | **coder의 alias** | 기존 coder=SW. 분리 불필요(YAGNI) |
| HW Coder | **신규 profile** | FPGA/RTL/HLS는 별도 도구·검증체인(`[[MY]]`) → 분리 가치 |
| Designer | **alias(reporter+) → 필요 시 profile** | UI/diagram 수요 생기면 승격 |
| Social Network | charter만 | 아직 워크플로 없음 |
| Life/Finance/Business/Career/Learning | **charter만** → [[domain-agents-charter]] | recurring 워크플로 생길 때 profile화 |

## 결정 규칙
역할은 **recurring 워크플로가 실제로 생기면** profile, 아니면 alias/charter. (폭보다 검증된 한 바퀴 — 정본 로드맵 원칙.)

## sign-off 필요
- HW Coder를 지금 profile로 만들까? (DFXISP-C1이 HLS라 곧 필요할 수 있음)
- 나머지는 alias/charter 유지 동의?
