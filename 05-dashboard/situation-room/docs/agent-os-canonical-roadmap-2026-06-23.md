---
title: Agent OS — Canonical Roadmap
created: 2026-06-23
owner: 이형민
status: canonical-v1
supersedes_for_priority:
  - agent-os-hq-dashboard-vision-report-2026-06-23.md
  - Hermes "Agent OS Current Status and Next Actions"
  - Notion 활용 방안 제안
note: 위 3종은 상세 참고용으로 유지. 우선순위·정본 결정은 이 문서가 단일 정본.
---

# Agent OS — Canonical Roadmap (단일 정본)

세 로드맵이 80% 일치하나 우선순위 가중치와 "정본이 어디냐"에서 어긋났다. 이 문서가 그 둘을 확정한다.

## 0. 한 줄
뼈대(헌법·상황실·역할·보드·Second Brain·graphify)는 구축됨. 다음은 **만든 걸 쓰게 배선 + 실행엔진 + 프로젝트 루프 1회 증명**. 폭이 아니라 검증된 한 바퀴.

## 1. 정본 소유권 (충돌 해소)
| 데이터 | 정본 시스템 | 비고 |
|---|---|---|
| 문서·위키·결정·연구·PDF | Google Drive + Obsidian | 사람·동기화·Git 친화 |
| 지식 관계·검색 인덱스 | Graphify (파생, 재생성) | graph.json은 Drive에 보관 |
| 승인·우선순위·사람 의견 | **Notion** | 사람 관제면. Approvals는 Notion 정본 |
| 실행 상태·heartbeat·retry·claim | **Hermes / DB** | 기계 상태. Notion이 아님 |
| 결과 요약 | Hermes → Notion 미러 | 단일 writer = Hermes |
| 코드·대용량 산출물 | Drive / GitHub | |

## 2. 확정 결정 (3종 충돌 해소)
1. **Notion = 사람 관제면, 기계 큐 아님.** 에이전트가 Notion을 작업 큐로 폴링하지 않는다(rate limit·지연·claim 의미 없음).
2. **정본 분리(mirror vs canonical 충돌 해소):** 시작은 단방향 미러(Drive/DB→Notion). 정본으로 승격하는 건 **Approvals + 사람 소유 필드(priority, operator_note)뿐.** 기계/실행 상태는 끝까지 Drive/DB 정본. → Hermes 문서의 "순수 mirror"와 Notion 제안의 "전면 정본 승격"의 중간이자 안전판.
3. **조율 substrate가 대시보드의 전제.** task_id 척추 + claim-safe 큐(Postgres SKIP LOCKED + LISTEN/NOTIFY)가 대시보드보다 먼저/동시. 대시보드는 자기가 읽는 state만큼만 좋다.
4. **Notion은 3 DB부터** (Work Items / Approvals / Health). Vision의 7~8 DB는 sync 표면 과다 → 나중에 확장.
5. **P0는 작게.** Hermes의 5개 P0는 한 분기치 → 막힌 것 3개로 압축.
6. **승인→Hermes는 webhook push**, 폴링 아님.

## 3. 단일 우선순위 (실행 추적 = task list #9–21)
**P0 — 막힌 것 (작게)**
- Graphify STALE 해소(재빌드→Drive) · 위키/graphify 진입 규칙 배선(CLAUDE/AGENT-OS/SCHEMA) · .codex hook 경로 수정 · **DFXISP 1태스크 풀 루프 증명**

**P1 — 운영면**
- 조율 substrate(task_id+claim 큐) → HQ Dashboard v1 + Agent/Model Registry → Notion 3-DB MVP(Approvals 중심) → execution trace + cost telemetry → Reference radar/weekly-tech-scout

**P2 — 확장(루프 증명 후)**
- Chorus 리뷰 파일럿 · per-role 모델 specialization + future roles · domain agents charter · 기존 문서 frontmatter 소급 변환

원칙: domain agents(P2)는 **DFXISP 루프 1회 증명(P0) 이후**. 대시보드(P1)는 **조율 substrate 이후**.

## 4. CEO 미해결 결정 (압축)
1. 대시보드: Notion 먼저 vs 로컬 HTML/JSON 강화 먼저?
2. paid API 연결 vs CLI/manual ingest 유지?
3. Agent OS HQ 구축을 임시 P0로 끌어올릴까, DFXISP P0 60–70% 유지?

(나머지 세부는 supersede된 3 문서 참조.)
