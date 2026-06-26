---
title: Second Brain 시작하기
layer: memory
status: active
owner: 이형민
created: 2026-06-22
tags: [second-brain, agent-os, obsidian, graphify]
---

# Second Brain 시작하기

이 폴더는 Google Drive 원본 기준의 Second Brain / LLM Wiki입니다. 로컬 `/opt/data/agent_os_archive/files/02-memory`는 작업 캐시이며, 최종 원본은 Google Drive입니다.

## 매일 쓰는 입구

1. 빠른 메모는 `00-inbox/`에 넣습니다.
2. 진행 중인 결과물은 `10-projects/`에 둡니다.
3. 지속 관리 주제는 `20-areas/`에 둡니다.
4. 논문, 링크, 원자료 정리는 `30-resources/`에 둡니다.
5. 쪼개진 영구 노트/개념 노트는 `40-notes/`에 둡니다.
6. 더 이상 active가 아닌 것은 `90-archive/`로 이동 후보를 표시합니다. 삭제는 별도 확인 후에만 합니다.

## 기존 LLM Wiki 백본

이미 존재하는 백본은 유지합니다.

- `SCHEMA.md` — 노트 스키마/프론트매터 규칙
- `index.md` — 메모리 계층 인덱스
- `log.md` — 변경 로그
- `concepts/`, `entities/`, `comparisons/`, `queries/`, `raw/`, `templates/` — Graphify/LLM Wiki용 구조

## 운영 규칙

- 모든 주요 노트는 YAML frontmatter를 둡니다: `title`, `layer`, `status`, `tags`, `source`.
- 관련 노트는 Obsidian wikilink `[[노트명]]`로 연결합니다.
- AI가 생성한 요약은 원자료 링크/Drive 파일 ID를 함께 남깁니다.
- DFXISP/AI드론/Agent OS 산출물은 각 프로젝트 폴더와 cross-link합니다.
- 주기적으로 Graphify를 재생성하고 `second-brain-health.md/json`을 확인합니다.

## 현재 핵심 경로

- Drive 폴더: `02-memory`
- 로컬 캐시: `/opt/data/agent_os_archive/files/02-memory`
- Obsidian vault root: `/opt/data/agent_os_archive/files`
- Wiki path: `/opt/data/agent_os_archive/files/02-memory`
