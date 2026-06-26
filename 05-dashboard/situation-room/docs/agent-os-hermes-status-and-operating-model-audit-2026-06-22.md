# Agent OS / Hermes 구축 상태 점검 및 운영모델 제안

- 작성일: 2026-06-22T00:19:25Z
- 대상: 이형민 Agent OS / Hermes Agent workspace
- 원칙: Google Drive가 원본(source of truth), 로컬 `/opt/data`는 staging/cache/mirror
- Drive 배치 예정 폴더: `Agent OS/05-dashboard/situation-room/docs/`

## 1. 결론 요약

현재 구축은 **기본 골격은 이미 갖춰져 있음**: Google Drive Agent OS 루트, 로컬 archive/manifest, Slack archive cron, Drive archive cron, 12개 Hermes 역할 프로필, 3개 Kanban board, 프로젝트별 scaffold, healthcheck 스크립트가 존재한다.

하지만 실제 운영 관점에서는 아직 다음 갭이 크다.

1. **문서 원본 저장 규칙이 일관되게 강제되지 않음**
   - 보고서/cron output/Slack archive/임시 산출물이 `/opt/data` 아래에 남고, Drive 원본 파일 ID/링크와 연결되는 단계가 빠지는 경우가 있다.
   - 앞으로 durable report는 Drive에 먼저 저장하고, 로컬은 cache로만 취급해야 한다.

2. **역할 프로필은 존재하지만 대부분 같은 모델/상태이며 자동 라우팅이 약함**
   - `operator, pm, admin, researcher, analyst, coder, reviewer, reporter, governor, auditor, curator, sentinel` 프로필은 있다.
   - 그러나 모두 `gpt-5.5 / OpenAI Codex` 중심이고, 각 역할의 실제 작업 큐/권한/입출력 schema/완료조건이 Kanban과 강하게 결합되어 있지는 않다.

3. **Situation Room은 방향이 맞지만 아직 “모든 모델이 공유하는 운영 DB/문서 허브”로 완성되지는 않음**
   - dashboard/state/docs 구조는 있다.
   - 다만 Claude/Gemini/Hermes/기타 모델이 동시에 볼 수 있는 표준 workspace contract, artifact registry, trace/log convention이 더 필요하다.

4. **관측 가능성(observability)이 부족함**
   - cron output과 healthcheck는 있지만, task별 trace ID, agent별 run log, tool call/error/cost/review 결과가 일관된 형식으로 축적되지는 않는다.

5. **프로젝트별 보드는 있으나 작업량이 아직 낮음**
   - `agent-os` board에는 작업이 축적되어 있으나, `dfxisp`, `ai-drone` board는 완료 기록 위주이고 다음 연구/구현 작업 routing이 약하다.

## 2. 공개 사례 조사: 기업/대규모 에이전트 생태계의 운영 패턴

공개 GitHub, 프레임워크 문서, X/Twitter 인접 공개 웹, Reddit 논의에서 반복되는 패턴은 다음과 같다.

### 2.1 공유 workspace는 파일/DB/artifact 중심이어야 한다

여러 AI 모델/에이전트가 협업하려면 대화 히스토리만 공유해서는 부족하다. 실무형 구조는 다음과 같다.

```text
workspace/
  tasks/       # 작업 카드, owner, status, done condition
  specs/       # 요구사항, 설계, 프로젝트 정의
  artifacts/   # 조사노트, 설계안, 패치, 테스트 결과, 최종 보고서
  logs/        # agent별 log/trace JSONL
  memory/      # 장기 문맥, 결정사항, glossary
  registry/    # artifact index, source URL, Drive ID, checksum
```

관련 공개 사례:
- AutoGen: https://github.com/microsoft/autogen
- LangGraph: https://github.com/langchain-ai/langgraph
- CrewAI: https://github.com/crewAIInc/crewAI
- OpenHands: https://github.com/All-Hands-AI/OpenHands
- Agent OS by Builder Methods: https://github.com/buildermethods/agent-os

### 2.2 Supervisor / Router / Handoff 패턴이 swarm보다 안정적이다

대규모 생태계는 “모든 agent가 자유롭게 말하는 구조”보다 중앙 supervisor/router가 작업을 분해하고, specialist가 수행하며, reviewer가 검증하는 구조가 더 안정적이다.

권장 기본 흐름:

```text
operator/human
  -> pm/router
  -> researcher / analyst / coder / admin
  -> reviewer
  -> reporter/curator
  -> Drive archive + situation room
```

참고:
- LangGraph multi-agent supervisor: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
- OpenAI Agents SDK handoffs: https://openai.github.io/openai-agents-python/handoffs/
- CrewAI hierarchical process: https://docs.crewai.com/concepts/processes
- AutoGen GroupChatManager: https://microsoft.github.io/autogen/

### 2.3 Human-in-the-loop는 마지막 승인만이 아니라 위험 지점마다 필요하다

공통 원칙:
- 읽기/read-only 작업은 자동화 가능
- 파일 삭제, Drive share/delete, API key/token 변경, git push, 외부 업로드, 배포는 사람 승인 필요
- agent는 변경 전 diff/근거/영향 범위를 제시해야 한다
- 장기 작업에는 budget, timeout, max iteration, interrupt/resume이 필요하다

참고:
- OpenAI Agents SDK human-in-the-loop: https://openai.github.io/openai-agents-python/human-in-the-loop/
- LangGraph interrupts: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
- Claude Code permissions: https://docs.anthropic.com/en/docs/claude-code

### 2.4 로그/트레이스는 선택이 아니라 운영 필수 계층이다

multi-agent 운영에서는 최종 답변만 보면 실패 원인을 알 수 없다. task/run/step/tool call 단위의 trace가 필요하다.

권장 trace schema:

```json
{
  "trace_id": "run_...",
  "task_id": "T-...",
  "agent": "researcher",
  "started_at": "ISO-8601",
  "inputs": ["Drive file", "Kanban card", "Slack request"],
  "tool_calls": [],
  "artifacts": [],
  "decision": "...",
  "verification": "...",
  "cost_estimate": null,
  "status": "done|blocked|failed"
}
```

참고:
- OpenAI Agents tracing: https://openai.github.io/openai-agents-python/tracing/
- LangSmith: https://docs.smith.langchain.com/
- Arize Phoenix: https://docs.arize.com/phoenix
- AgentOps: https://github.com/AgentOps-AI/agentops
- Helicone: https://docs.helicone.ai/

### 2.5 역할 agent는 이름보다 입출력/권한/완료조건이 중요하다

좋은 role design은 “PM/Researcher/Coder” 이름 자체보다 다음을 명확히 한다.

- mission
- allowed tools
- forbidden actions
- required inputs
- output schema
- verification method
- handoff target
- stop condition

참고:
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- ChatDev: https://github.com/OpenBMB/ChatDev
- CAMEL: https://github.com/camel-ai/camel

## 3. 현재 구축 상태 점검

### 3.1 Hermes 상태

점검 명령 기준:
- `hermes --version`
- `hermes status --all`
- `hermes config path`
- `hermes profile list`

확인 결과:
- Hermes Agent: `v0.16.0 (2026.6.5)`, upstream보다 1 commit behind
- Project: `/opt/hermes`
- Python: `3.13.5`
- Config: `/opt/data/config.yaml`
- Model: `gpt-5.5`
- Provider: `OpenAI Codex`
- Gateway: Slack configured, gateway running, docker foreground manager
- Nous Portal logged in
- OpenAI Codex logged in
- Terminal backend: local, sudo disabled
- Scheduled jobs: 4 active
- Active sessions: 11

주의:
- API-key provider는 대부분 미설정: Anthropic, Gemini, OpenRouter, Firecrawl, Tavily 등은 status상 미설정으로 표시됨.
- Nous subscription managed tools는 사용 가능하나 web tools는 “included, not currently selected” 상태로 표시됨.
- 다수 모델을 병렬로 쓰려면 profile별 provider/model 분리가 필요하다.

### 3.2 역할 프로필

`/opt/data/profiles` 아래 12개 역할 프로필 확인:

- operator
- pm
- admin
- researcher
- analyst
- coder
- reviewer
- reporter
- governor
- auditor
- curator
- sentinel

각 profile에는 대체로 다음이 있다.
- `profile.yaml`
- `SOUL.md`
- `memories/MEMORY.md`
- bundled skills

현재 한계:
- 모든 profile이 거의 같은 모델 `gpt-5.5`로 표시된다.
- 역할별 Claude/Gemini/local 모델 배치가 아직 적용되어 있지 않다.
- 역할별 cron/job ownership은 비어 있거나 약하다.
- profile이 존재하는 것과 실제 작업 routing이 되는 것은 별개다.

### 3.3 Google Drive / archive 상태

Drive root:
- 이름: `Agent OS`
- root folder ID: `1xbqGeDdLerv8jd3eeHsR0IS-CHkI7kgz`

로컬 archive:
- `/opt/data/agent_os_archive`
- manifest: `/opt/data/agent_os_archive/manifest.json`
- manifest file count: 67
- latest sync 관측: `2026-06-21T23:51:11Z` 근처

주요 Drive category folder:
- `04-agents`: `1AOzVqWgz8rYFzscuNENb3tmWm2M28BTb`
- `04-agents/routing`: `1uw0sh_1SOrZtXO4gz4-8JywtcdiDesFf`
- `05-dashboard`: `1eUjXgSTbqdkbx2myeV7APWLkYQgnQGhH`
- `05-dashboard/situation-room`: `1jJAvlROw5CiFbGtCo1_WR3KWWivlGuJA`
- `05-dashboard/situation-room/docs`: `1cA0ljwJCm4Mg76Jrk1uQnxZYtkLQhuhd`
- `05-dashboard/situation-room/state`: `1oVkXFEQ_YxLjnYlmdhLSu-BtwbI_UXO0`
- `05-dashboard/situation-room/ui`: `1T_mD1UIyiLx2bobA_DTtDUDLLPWqqUjD`
- `06-production`: `1OUL1mRG3Re7Ni7eLPLaHhMkHk-kbBPyg`
- `06-production/AI드론`: `11vGMy8C1O6luTWPG8aWoG-lwCq9w_Mfm`
- `07-loop`: `1QUbnqkQyXlbs7zpWzYSmNWA9x8ZGx2Aa`

판정:
- Drive 구조는 Agent OS workspace로 충분히 시작 가능한 수준이다.
- 하지만 “로컬 생성 -> Drive 업로드 -> Drive 링크 기록 -> manifest 반영” 루프가 모든 보고서에 강제되지 않는다.

### 3.4 Cron 상태

`/opt/data/cron/jobs.json` 기준 4개 job 모두 enabled, last status ok.

1. `slack-channel-C0BA8DR4VV1-daily-archive`
   - schedule: `0 0 * * *`
   - delivery: Slack channel

2. `agent-os-drive-daily-archive`
   - script: `agent_os_drive_archive.sh`
   - schedule: `50 23 * * *`
   - delivery: local

3. `agent-team-healthcheck`
   - script: `agent_team_healthcheck.sh`
   - schedule: `10 9 * * *`
   - delivery: local

4. `project-weekly-review`
   - script: `project_weekly_review.sh`
   - schedule: every `2880m`
   - delivery: local

판정:
- Drive archive, Slack archive, healthcheck, project review 루프가 있다.
- 다만 cron output이 local에만 남는 job들이 있어 “Drive 원본” 원칙과 충돌한다.
- 특히 `cron/output/*/*.md`는 운영 증거로 중요하므로 Drive의 `07-loop/routines` 또는 `05-dashboard/situation-room/docs`에 summary/index가 생겨야 한다.

### 3.5 Kanban 상태

보드:
- `agent-os`
- `dfxisp`
- `ai-drone`

관측 상태:
- `agent-os`: todo 2, blocked 1, done 11, total 14
- `dfxisp`: done 2, total 2
- `ai-drone`: done 6, total 6
- root `/opt/data/kanban.db`: 테이블은 있으나 task 0

판정:
- governance/Agent OS 구축 task는 어느 정도 진행됨.
- DFXISP와 AI드론은 프로젝트 board는 있으나 현재 active queue가 거의 없다.
- 다음 단계는 각 프로젝트에 “연구/설계/실험/리뷰” task를 다시 seed하고 역할 agent에 연결하는 것이다.

### 3.6 로컬 root 산출물/문제 지점

최근 `/opt/data` top-level에 다음 성격의 파일/디렉터리가 있다.

- `cron/output/` — cron 결과 보고서
- `slack_channel_archive/` — Slack archive
- `agent_os_archive/` — Drive mirror/cache
- `projects/` — project scaffold/cache
- `tmp/` — 임시 생성물
- `tmp_create_ai_drone_asic_tasks.py` — root에 남은 임시 script
- `dfxisp_md/`, `notebooklm_dfx_isp/` — 별도 작업 repo/data

판정:
- `/opt/data`는 실행 환경이므로 일부 state/db/config는 root에 있을 수 있다.
- 그러나 사람이 읽는 보고서, 기획서, 결정문, 작업 로그는 root에 남기면 안 된다.
- `tmp_create_ai_drone_asic_tasks.py` 같은 임시 파일은 정리 후보이나, 삭제는 별도 확인 후 진행해야 한다.

## 4. 갭 분석

| 영역 | 현재 | 목표 | 갭 |
|---|---|---|---|
| Drive source of truth | Drive root/archive 있음 | 모든 문서 산출물 Drive 원본화 | cron/report/local artifacts가 Drive link 없이 남음 |
| 역할 프로필 | 12개 profile 있음 | 역할별 provider/model/tool/권한 분리 | 대부분 동일 모델, profile-local jobs 약함 |
| Task routing | Kanban 3개 board 있음 | PM/router가 specialist에게 task 배정 | 프로젝트 board active queue 부족 |
| Observability | cron output/healthcheck 있음 | trace ID, run log, tool/cost/error/artifact registry | 구조화 trace 부족 |
| Multi-model collaboration | Hermes 중심 | Claude/Gemini/Hermes/local model이 같은 workspace 사용 | 외부 모델이 읽을 표준 contract 부족 |
| Situation Room | dashboard 구조 있음 | JSON/MD/HTML/Slack digest 일원화 | artifact registry와 agent state schema 강화 필요 |
| Human approval | 일부 메모리 규칙 있음 | 위험 action별 승인 gate 명문화 | 각 profile SOUL/board task에 일관 적용 필요 |

## 5. 권장 운영 아키텍처

### 5.1 공유 workspace 원칙

Google Drive의 `Agent OS`를 모든 모델의 공용 workspace로 둔다.

```text
Google Drive / Agent OS
  01-hardware/
  02-memory/
  03-models/
  04-agents/
    routing/
    roles/
    handoffs/
  05-dashboard/
    situation-room/
      docs/
      state/
      ui/
  06-production/
    DFXISP/
    AI드론/
  07-loop/
    routines/
    reports/
    traces/
```

로컬 `/opt/data`는 다음 용도로 제한한다.

```text
/opt/data/agent_os_archive    # Drive mirror/cache
/opt/data/projects            # executable project cache/scaffold
/opt/data/scripts             # automation scripts
/opt/data/cron/output         # transient cron output cache
/opt/data/tmp                 # temporary staging
```

### 5.2 모든 report 저장 규칙

새 규칙:

1. durable report 작성
2. 로컬 staging copy 생성 가능
3. Drive 적절한 folder에 업로드/생성
4. Drive file ID/link를 report와 Slack에 기록
5. local path는 “cache/staging”으로만 표기

권장 report metadata:

```yaml
title: ...
date: ...
owner_agent: reporter|auditor|curator|...
drive_file_id: ...
drive_link: ...
local_cache: ...
source_tasks: []
related_artifacts: []
status: draft|reviewed|canonical
```

### 5.3 역할별 agent 배치

현재 profile을 유지하되, 작업 routing을 다음처럼 강화한다.

| Agent | 역할 | 주요 입력 | 산출물 | 추천 모델/도구 |
|---|---|---|---|---|
| operator | 사용자 요청 접수, 승인, 우선순위 | Slack, Drive, Kanban | command/decision | stable Hermes |
| pm | 작업 분해/라우팅 | Slack request, portfolio | Kanban tasks, milestones | reasoning model |
| researcher | 자료 조사/논문/웹 | Drive corpus, web, papers | cited research notes | Claude/Gemini long context |
| analyst | 구조화 분석/아키텍처 | research notes, specs | tradeoff/design memo | Claude/Gemini |
| coder | 구현/스크립트/테스트 | task/spec/repo | code patch, test result | coding-specialized model |
| reviewer | 검증/반례/누락 점검 | artifacts, diff, tests | review report | strong reasoning model |
| reporter | Drive/Slack 보고 | verified outputs | final report, digest | stable/current model |
| admin | 계정/도구/cron/config | system state | setup/change proposal | Hermes with terminal |
| governor | 역할 경계/운영체계 | all status | topology/routing patch agenda | reasoning model |
| auditor | 상태 점검/보안/정합성 | status, scripts, logs | audit report | deterministic + LLM summary |
| curator | 문서/메모리/지식 정리 | Drive docs, summaries | index/glossary/decision updates | long-context model |
| sentinel | watchdog | cron, sync, stale board | alert only | cheap/fast model/script |

### 5.4 추천 라우팅 그래프

```text
이형민 / Slack
  -> operator
  -> pm
  -> researcher / analyst / coder / admin
  -> reviewer
  -> reporter
  -> Drive canonical report + Situation Room update

parallel governance:
  governor -> auditor / curator / sentinel -> reporter
```

### 5.5 Project board 운영

- `agent-os`: 운영체계, dashboard, automation, role governance
- `dfxisp`: DFX AI-ISP 연구/설계/실험/FPGA 구현
- `ai-drone`: AI드론 exploration/PoC

각 board task는 다음 필드를 포함해야 한다.

```yaml
task_id: ...
project: agent-os|dfxisp|ai-drone
owner_agent: researcher|analyst|coder|reviewer|...
status: todo|ready|running|blocked|review|done
inputs:
  - drive_file_id: ...
outputs:
  - drive_file_id: ...
verification:
  - command/result or review checklist
handoff_to: ...
requires_human_approval: true|false
```

## 6. 즉시 실행 권장 작업

### P0 — 저장 규칙 고정

1. 모든 새 보고서를 `Agent OS/05-dashboard/situation-room/docs/` 또는 프로젝트별 `06-production/<project>/...`에 저장한다.
2. cron output은 local cache로 두되, 매일 digest/index를 Drive에 남긴다.
3. Slack final response에는 Drive link를 먼저, local cache path를 나중에 제시한다.

### P0 — Situation Room 강화

1. `status.json`에 Drive sync, cron, Kanban, profile, artifact registry를 넣는다.
2. `situation-board.md`를 AI 모델 공용 요약판으로 쓴다.
3. HTML dashboard는 사람이 보는 view일 뿐, 유일한 상태 저장소로 쓰지 않는다.

### P1 — 역할별 task routing 활성화

1. `dfxisp` board에 DFX AI-ISP 연구/설계/검증 task를 seed한다.
2. 각 task를 `researcher -> analyst -> coder -> reviewer -> reporter` chain에 연결한다.
3. role별 output schema를 `04-agents/routing/`에 문서화한다.

### P1 — multi-model profile 분리

1. Claude/Gemini/API key 추가는 사용자 확인 후 진행한다.
2. `researcher`, `analyst`, `reviewer`, `curator`는 long-context/reasoning model 우선.
3. `sentinel`, script-only cron은 저비용/무LLM으로 유지.

### P1 — trace/log registry 도입

1. `07-loop/traces/` 또는 `05-dashboard/situation-room/state/traces.jsonl` 생성.
2. task별 trace ID, artifacts, tool result, verification 결과를 기록.
3. reviewer가 artifact와 trace를 보고 검증하게 한다.

### P2 — root cleanup

1. `/opt/data/tmp*`, root 임시 script, old report cache를 목록화한다.
2. Drive에 보존할 것은 업로드 후 local cache로 표시한다.
3. 삭제/이동은 사용자 확인 후 실행한다.

## 7. Hermes 구축 상태에 대한 판정

### 잘 된 점

- Hermes gateway가 Slack에서 정상 동작한다.
- Drive archive, Slack archive, healthcheck, project review cron이 있다.
- Agent OS Drive folder 구조가 이미 존재한다.
- 역할 profile 12개와 SOUL.md가 있다.
- Kanban board가 프로젝트별로 분리되어 있다.
- DFXISP/AI드론을 별도 project로 관리하려는 방향이 맞다.

### 부족한 점

- Drive-first 저장 규칙이 자동화/검증으로 강제되지 않는다.
- role profiles가 실제 모델/권한/라우팅 차이를 충분히 갖지 못했다.
- report/artifact registry가 없다.
- observability가 cron output 수준에 머물러 있다.
- 외부 Claude/Gemini/기타 모델이 읽고 쓸 표준 workspace contract가 부족하다.

## 8. 다음 액션 제안

내가 다음 턴에서 바로 진행할 수 있는 작업:

1. `Agent OS/05-dashboard/situation-room/docs/`에 이 보고서 Drive 원본 저장 완료 확인
2. `04-agents/routing/agent-routing-contract.md` 작성
3. `05-dashboard/situation-room/state/artifact-registry.json` 초안 생성
4. `dfxisp` board에 researcher/analyst/reviewer용 초기 작업 seed
5. cron output을 Drive digest로 묶는 `cron-output-drive-digest` job 설계

단, Drive 파일 생성/수정은 일반 보고서 저장 목적에서는 사용자의 현재 요청에 따라 진행 가능하되, Drive 삭제/공유/권한 변경/API key 변경/git push는 별도 확인이 필요하다.
