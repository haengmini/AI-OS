# 05-dashboard — 공유 상황판 README

> 이 폴더는 Claude, Gemini, GPT, Hermes가 **공동으로 읽고 쓰는** 단일 상태 공간이다.
> 단일 정본: `dashboard-state.json`

---

## 1. 핵심 파일

| 파일 | 역할 | R/W |
|---|---|---|
| `dashboard-state.json` | **공유 상황판 정본** — 에이전트 상태·태스크·핸드오프 | READ + WRITE |
| `DASHBOARD-README.md` | 이 가이드 | READ |

---

## 2. dashboard-state.json 구조

```text
_meta              → 스키마 버전, 규칙, 읽기/쓰기 에이전트 목록
system_status      → 전체 시스템 상태 및 현재 Phase
owner              → 형민의 오늘 포커스·우선순위·블로커
agent_status       → Claude / Gemini / GPT / Hermes 각자의 상태 블록
active_tasks       → 진행 중인 태스크 목록 (id, title, owner_agent, status, ...)
handoff_queue      → 에이전트 간 인계 대기 항목
active_projects    → 활성 프로젝트 요약
memory_log         → 이 파일에 기록된 주요 변경 이력
weekly_focus       → 이번 주 목표·핵심 프로젝트
system_health      → WSL 디스크·Git 동기화·Memory 품질 상태
```

---

## 3. 에이전트별 수정 규칙

### 공통 규칙
```text
1. last_updated_by, last_updated_at 반드시 갱신
2. 자기 agent_status 블록만 수정 (타 에이전트 블록 금지)
3. active_tasks 추가만 허용. 삭제는 형민 승인 후
4. secret / token / API key 절대 기록 금지
5. 수정 후 memory_log에 한 줄 추가
```

### Claude
```text
- 작업 완료 시 agent_status.Claude 갱신
- 설계·계획 산출물은 active_tasks에 기록
- Hermes로 인계 시 handoff_queue에 추가
```

### Gemini
```text
- 정제·scan 완료 시 agent_status.Gemini 갱신
- last_output에 산출물 Drive 경로 기록
```

### GPT
```text
- 작업 완료 시 agent_status.GPT 갱신
- 특이사항은 notes에 기록
```

### Hermes (Loop Agent)
```text
- 매일 1회 전체 상황판 점검 및 갱신
- system_health 블록 업데이트
- weekly_focus 주간 목표 갱신 (월요일)
- Slack으로 형민에게 일일 요약 보고
```

---

## 4. active_tasks 항목 형식

```json
{
  "id": "TASK-001",
  "title": "작업 제목",
  "owner_agent": "Claude",
  "collaborators": ["Hermes"],
  "project": "프로젝트명",
  "layer": "05-dashboard",
  "status": "in_progress",
  "priority": "high",
  "created_at": "2026-06-19T00:00:00Z",
  "due": null,
  "last_updated": "2026-06-19T00:00:00Z",
  "output_path": null,
  "notes": ""
}
```

`status` 값: `pending` / `in_progress` / `blocked` / `review` / `done`

---

## 5. handoff_queue 항목 형식

```json
{
  "id": "HO-001",
  "from": "Claude",
  "to": "Hermes",
  "task_ref": "TASK-001",
  "message": "설계 완료. 메모리 반영 및 Slack 보고 요청",
  "status": "pending",
  "created_at": "2026-06-19T00:00:00Z"
}
```

`status` 값: `pending` / `acknowledged` / `done`

---

## 6. 갱신 주기

| 에이전트 | 갱신 주기 |
|---|---|
| Hermes | 매일 (daily-status-loop) |
| Claude | 작업 시작·완료 시 |
| Gemini | 정제·scan 완료 시 |
| GPT | 작업 완료 시 |
| 형민 | owner 블록: 매일 아침 / weekly_focus: 월요일 |

---

## 7. Routing 정본

Dashboard·Slack·공유 상태 전반 → `CLAUDE.md` §1 Routing Table
운영 규칙 → `AGENT-OS.md` §5 Completion Rule
