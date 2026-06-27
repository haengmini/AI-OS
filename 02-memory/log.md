---
type: log
title: 02-memory — Wiki Change Log
tags: [log]
created: 2026-06-22
status: stable
---

# Wiki Change Log (append-only)

## 2026-06-27 — Research 폴더 재배치 지원 및 불필요한 로그 파일 정리 (by Gemini)
- 구글 드라이브 가상 드라이브(G:) 환경의 심볼릭 링크 및 Junction 미지원 제약을 파악하고 대안으로 `Research` 내 파일군을 성격별로 `01-hardware`, `03-models`, `06-production` 폴더로의 수동 재배치를 조율함.
- 대량의 연구용 문서 및 데이터셋이 Git 추적에 잡혀 리포지토리가 무거워지는 현상을 방지하기 위해 `.gitignore`에 `Research/`를 등록하고 커밋을 완료함.
- `Agent OS` 폴더 루트에 누적되어 있던 로테이션 백업 및 미사용 과거 MCP 서버 로그 15개 파일(약 37.8 MB)을 삭제 정리하여 클라우드 드라이브 공간 최적화 수행.

## 2026-06-26 — AI OS 및 DFXISP 연구 프로젝트 GitHub 연동 및 1차 동기화 완료 (by Gemini)
- AI OS (`g:\내 드라이브\Agent OS` -> `https://github.com/haengmini/AI-OS.git`) 로컬 리포지토리를 초기화하고 원격에 푸시 완료 (구글 드라이브 포인터 파일 `.gdoc`, `.gsheet`, `.gslides` 필터링 조치 포함).
- DFXISP (`g:\내 드라이브\Agent OS\06-production\DFXISP` -> `https://github.com/haengmini/dfxisp.git`) 로컬 리포지토리를 원격 main 브랜치와 안전하게 연결하여 로컬 최신 연구 파일군 및 HLS csim 코드를 반영한 상태로 동기화 푸시 완료.

## 2026-06-26 — 에이전트 계약 규칙 및 CLAUDE.md 갱신 (by Gemini)
- `AGENTS.md` (§2), `GEMINI.md` (§3) 및 `CLAUDE.md` (§ 핵심 규칙)를 수정하여 "작업 완료 후 항상 GitHub, Google Drive, Notion 에 기록을 갱신/커밋하여 동기화"하는 전역 동기화 규칙을 공식 추가.

## 2026-06-26 — DFXISP 학위논문 기여점 4대 갱신 및 4종 Variant 실험 설계 (by Gemini)
- `00-thesis-outline.md`, `01-thesis-draft.md`, `02-references.md`, `03-figures-tables.md` 문서군을 전면 업데이트.
- 핵심 기여점을 4가지(하이브리드 적응, 인식 특화 저조도 RM, 리소스 인지형 스케줄러, ZCU104 검증 패키지)로 확장.
- 스케줄러 목적함수 수식을 공식화하여 본문 골격에 추가.
- 실험 Variant를 4종(`Static`, `Reg-only`, `DFX-Bin`, `DFX-FP`)으로 통일 및 그림/표 구조 갱신.
- 최근 서베이된 8개 핵심 AI-ISP 논문의 서지 정보 추가 및 관련연구 비교 매트릭스(`Tab2`) 직접 작성 완료.

## 2026-06-22 — Hermes P0 정리 / wiki root 계약 + 링크 보수
- 공식 wiki root 계약을 `02-memory/`로 확정하는 root redirect 파일 생성: `/SCHEMA.md`, `/index.md`, `/log.md`.
- `02-memory/index.md`에 7-layer 하위 노트와 `[[how-does-hermes-loop-work]]` 직접 링크 추가.
- broken wikilink 감소를 위해 seed layer notes 생성: `hardware-layer`, `memory-layer`, `models-layer`, `agents-layer`, `dashboard-layer`, `production-layer`, `loop-layer`, `07-loop`.
- `second-brain-health.json/md` 생성 대상 상태를 재측정하고 Graphify STALE 상태를 유지보수 항목으로 승격.

## 2026-06-22 — 백본 스캐폴딩 (by Claude/Cowork)
- `SCHEMA.md`, `index.md`, `log.md` 생성 — Karpathy LLM-wiki 백본.
- 폴더 생성: `concepts/ entities/ comparisons/ queries/ raw/ templates/`.
- seed atomic 노트 작성: 7-layer-architecture, model-routing, drive-first-source-of-truth, progressive-disclosure, memory-promotion-filter (concepts); hermes, graphify (entities); postgres-vs-drive-as-agent-bus (comparisons); how-does-hermes-loop-work (queries).
- `templates/note-template.md`, `raw/agent-os-backend-references.md` 추가.
- 검색 레이어: `graphify-out/`(graph.json·GRAPH_REPORT·wiki) 연결, query-first 규칙 SCHEMA §5에 명시.
- **미완(커넥터 한계)**: 기존 노트(MY/AGENT-OS/04-agents 등)의 frontmatter·wikilink 소급 변환은 in-place 수정 불가 → `templates/note-template.md` 표준 따라 점진 변환 필요.

<!-- 새 변경은 위에 날짜별로 append -->
