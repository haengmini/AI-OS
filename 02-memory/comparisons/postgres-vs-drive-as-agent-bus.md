---
type: comparison
title: Postgres vs Drive as Agent Bus
tags: [architecture, queue, decision]
created: 2026-06-22
source: "[[agent-os-backend-references]]"
status: draft
---

# Postgres vs Drive — 에이전트 조율 백엔드

## 결정 질문
멀티모델이 "근실시간"으로 일을 주고받게 하려면, 조율 상태/큐를 **Drive 파일**로 둘까 **DB**로 둘까?

## 비교
| 항목 | Drive (현재) | Postgres (권장 추가) |
|---|---|---|
| 문서 정본 | ✅ 최적(사람·Obsidian·동기화) | ✗ 부적합 |
| 작업 큐/클레임 | ✗ 레이스, in-place 수정 불가 | ✅ `FOR UPDATE SKIP LOCKED` 레이스-프리 |
| 즉시 깨우기 | ✗ 폴링(분 단위 지연) | ✅ `LISTEN/NOTIFY` 이벤트 |
| 메모리/의미검색 | graphify 그래프 | ✅ pgvector(같은 DB) |
| 운영 부담 | 0(이미 있음) | Docker 1개(Hermes) |

## 결론 (현 시점)
- **문서 = Drive 유지**, **조율 상태/큐 = Postgres로 분리**가 정석.
- 핵심 조합: **SKIP LOCKED 테이블(큐) + NOTIFY(깨우기)** → 폴링 없이 근실시간 + 충돌 없음.
- 주의: NOTIFY 단독은 큐가 못 됨(연결된 클라이언트에만 전달) — 반드시 테이블 큐와 병행.
- 1인 규모면 Redis/Kafka 불필요. "Hermes에 Postgres(+pgvector) 1개"가 80/20.

## 근거 / 출처
→ [[agent-os-backend-references]] (Postgres SKIP LOCKED, LISTEN/NOTIFY, pgvector 등 원문 링크).

## 관련
- [[index]] · [[drive-first-source-of-truth]] · [[hermes]]
