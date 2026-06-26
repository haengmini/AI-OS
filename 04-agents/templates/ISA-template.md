---
title: "ISA — <작업/프로젝트 이름>"
task_id: ""              # 조율 substrate / Notion 공통 키
board: ""                # agent-os | dfxisp | ai-drone
status: draft            # draft | active | done
created: ""
owner: 이형민
---

# ISA — Ideal State Artifact

> PAI에서 차용한 primitive. "무엇이 done인가"를 *먼저* 고정해 표류를 막는다.
> spec.md를 이 형식으로 쓴다. 규칙 정본: `04-agents/policies/lifeos-adoption.md`, 완료조건: `AGENT-OS.md §5`.

## 1. Problem / 현재 상태
무엇이 문제인가. 왜 지금 하는가. (현재 상태를 한 문단.)

## 2. Ideal State / 이상 상태
다 됐을 때 세상이 어떤 모습인가. 한 문단으로, 측정 가능하게.

## 3. Goal / 이번 작업의 목표
이번 사이클에서 실제로 닫을 것. (이상 상태 전부가 아니라 이번 분량.)

## 4. Out of Scope / 안 할 것
명시적으로 제외. 범위 표류 방지.

## 5. Constraints / 제약
예산·하드웨어·시간·의존성·정책. (없으면 "없음".)

## 6. Done Criteria / 완료 기준
체크 가능한 항목으로. 이게 AGENT-OS.md §5 Completion Rule의 입력이 된다.

- [ ] …
- [ ] …

## 7. Verification / 검증 수단
각 기준을 *어떻게* 확인하는가 (테스트·실측·재현·교차검증). 미검증 결과를 단정하지 않는다 — "시뮬레이션 수준 확인" 식으로 명시.

## 8. Decisions & Risks / 결정·리스크
주요 설계 결정과 근거, 남은 리스크·열린 질문.
