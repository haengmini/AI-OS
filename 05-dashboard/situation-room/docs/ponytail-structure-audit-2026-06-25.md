---
type: audit
title: Agent OS 구조 과잉설계 점검 (ponytail)
date: 2026-06-25
scope: backend(엔진층) / frontend(표면층)
status: draft — 실행은 사용자 승인 후
---

# Agent OS — ponytail 구조 점검

## 한 줄 진단

**1인 FPGA 연구용 OS인데, 다국적 팀 플랫폼처럼 지어졌다.**
그래서 시스템의 주 활동이 "연구"가 아니라 "자기 자신을 설명·라우팅·감사하는 것"이 됐고,
끝나지 않는 이유가 여기 있다 — 끝낼 대상(연구)보다 끝낼 도구(OS)가 더 빨리 자란다.

ponytail 제1질문: **이 작업이 존재할 필요가 있는가?**
지금 폴더의 절반 이상은 "실제 연구 산출"이 아니라 "OS를 관리하기 위한 OS"다.

---

## Backend (엔진 = 에이전트가 읽는 규칙·지식층)

대상: `AGENT-OS.md`, `CLAUDE.md`, `AGENTS.md`, `MY.md`, `MY-TELOS.md`,
`01-hardware`, `02-memory`, `03-models`, `04-agents`, `07-loop`

발견된 과잉:

1. **7-layer 아키텍처가 최소 4번 중복 서술됨**
   - `README.md §4` (Layer Summary)
   - `AGENT-OS.md` (헌법)
   - 각 layer 폴더의 `README.md` (7개)
   - `02-memory/concepts/*-layer.md` (hardware/memory/models/agents/dashboard/production/loop-layer + 7-layer-architecture = **8개 stub 노트**)
   → 같은 그림을 4겹으로 그려놓고, 하나 고치면 4곳을 고쳐야 함. 대부분 "seed" 상태로 방치.

2. **agent/model 라우팅이 4~5개 파일로 분산**
   - `04-agents/routing/agent-routing.md`
   - `04-agents/routing/agent-routing-contract.md`
   - `04-agents/routing/tft-routing.md`
   - `04-agents/routing/model-handoff.md`
   - + `CLAUDE.md`의 Routing Table + `AGENTS.md`의 Role 표
   → 1인 사용자가 사실상 Claude 하나를 쓰는데, 10개 에이전트 역할(Operator/Admin/PM/Designer/Social/SW·HW Coder/Researcher/Analyst/Reporter…)을 계약서까지 만들어 관리.

3. **디렉터리 맵 3중복**: `README §3`, `CLAUDE.md §1`, `AGENTS.md §0` 이 같은 폴더 구조를 각자 다시 적음.

4. **dangling pointer (가리키는데 없는 파일)**
   - `AGENTS.md` → `04-agents/policies/ponytail-engineering-rule.md` … **policies 폴더 자체가 없음**
   - `CLAUDE.md`/`AGENTS.md` → `graphify-out/graph.json` … root에 없음
   - `02-memory/index.md`는 graph를 `/opt/data/agent_os_archive/files`에서 찾으라 하고, `CLAUDE.md`는 `graphify-out/`에서 찾으라 함 → **graph 위치가 문서마다 다름**

5. **root vs 02-memory 이중 정본**
   - `index.md`(root) = **리다이렉트 전용 파일** (내용 없음, "02-memory/index.md로 가라"만 적힘)
   - `log.md`, `SCHEMA.md`도 root와 `02-memory/`에 각각 존재 → 어느 게 정본인지 매번 헷갈림

## Frontend (표면 = 사람이 보고 쓰는 층)

대상: `05-dashboard`, `Manual.md`, `OPERATION.md`, `06-production`

발견된 과잉:

1. **`05-dashboard/situation-room/docs/`에 세션 로그성 문서 ~25개**
   (worklog, audit, handoff, vision, direction, digest, status, roadmap …)
   → 이건 "구조"가 아니라 "작업하면서 나온 배기가스(process exhaust)". 시스템 폴더에 쌓여 구조처럼 보이지만 대부분 일회성.
   날짜별 vision/roadmap/status/next-actions 문서가 서로 겹침 — 어느 게 현재 정본인지 불명.

2. **Dashboard가 3중 표면**: situation-room UI(html) + Slack manifest + JSON state + Notion 대시보드 방법 문서.
   1인 사용자가 동시에 볼 표면이 너무 많다. 실제로 매일 여는 건 1개면 충분.

3. **Manual.md / OPERATION.md / DASHBOARD-README.md / README.md** — 사용법 설명이 4곳에 흩어짐.

---

## 가장 큰 ponytail 위반

> **문서가 문서를 관리한다.**
> 노트를 쓰는 규칙(SCHEMA)을 쓰는 템플릿을 쓰는 인덱스를 가리키는 리다이렉트 파일…
> 실제 연구 산출물(`06-production`: AI드론, DFXISP)은 이 메타 인프라 더미 **아래에 2개 폴더**로 묻혀 있다.

비율로 보면: 연구 산출 폴더 2개 vs 그걸 관리하려는 메타 문서 80+개.

---

## 두 가지 정리안 (택1)

### 안 A — 보수적: 7-layer 유지, 중복만 제거 (저위험, 빠름)
- 7개 layer 폴더 구조는 그대로 둔다(사용자 신념 존중).
- 삭제/병합:
  - `02-memory/concepts/*-layer.md` 8개 stub → 삭제 (README가 정본). 7-layer-architecture 1개만 유지.
  - `index.md`(root) 리다이렉트 파일 → 삭제. `log.md`/`SCHEMA.md` root 중복 → 삭제, 02-memory판만 정본.
  - 라우팅 4파일 → `agent-routing.md` 1개로 통합, 나머지 3개 삭제.
  - `situation-room/docs/` 날짜 로그 → `_archive/`로 이동(삭제 아님).
  - dangling pointer 정리: 없는 파일 참조를 CLAUDE/AGENTS에서 제거하거나 파일 생성.
- 결과: 살아있는 규칙 문서 ~6개, 나머지는 정본 1곳 원칙.

### 안 B — 공격적: 구조를 실제 규모에 맞춤 (고효과, 사용자 신념과 충돌)
```
Agent OS/
├── README.md      ← MY + AGENT-OS + README 병합 (정체성 + 규칙 + 구조, 한 파일)
├── CLAUDE.md      ← 짧은 라우팅 진입점만
├── memory/        ← 02-memory의 실제 노트만 (layer stub 제거)
├── projects/      ← 06-production (실제 산출물 — 시스템의 본체)
└── _archive/      ← 01·03·05·07 + 옛 문서 전부
```
- 7-layer는 폴더가 아니라 README 안의 한 섹션 개념으로 강등.
- hardware/models/dashboard/loop는 "폴더로 운영"할 만큼 내용이 없다 → 노트로 흡수.
- 결과: 살아있는 폴더 3개 + 진입 파일 2개. 매번 "어디 쓰지?"가 사라짐.

---

## 솔직한 권고

당신 철학엔 "7-layer는 고정한다"가 박혀 있다. 그게 **안 끝나는 진짜 원인**이다 —
구조를 신성불가침으로 두면, 구조를 채우는 일이 영원히 남는다.
ponytail 관점에선 **안 B**가 맞다. 하지만 신념과 충돌하므로,
먼저 **안 A로 중복·dangling만 걷어내고** 한 달 써본 뒤,
"layer 폴더를 정말 매주 여는가?"를 데이터로 보고 안 B를 결정하길 권한다.
