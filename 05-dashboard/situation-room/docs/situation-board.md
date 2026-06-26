# Agent OS Situation Board

- Generated at: `2026-06-22T00:33:39+00:00`
- Overall: **BLOCKED**
- Healthcheck: `PASS`
- Cost mode: `외부 paid provider는 명시 승인 전 manual/not_configured로 표시`

## Human Attention Needed
- **warn / blocker** — `agent-os` `t_d8cd6477`: Verify post-09:10 Slack archive and healthcheck state → 검토 또는 차단 해제 조건 확인

## Next Actions
- `agent-os` `t_82f11710` [todo] reviewer: Review Agent OS governance verification and patch proposals
- `agent-os` `t_eb8af557` [todo] reporter: Report final Agent OS governance kickoff outcome
- `agent-os` `t_d8cd6477` [blocked] auditor: Verify post-09:10 Slack archive and healthcheck state
- `dfxisp` `t_b872b08f` [running] researcher: DFXISP-R1 Drive corpus and theory-source inventory
- `dfxisp` `t_0d6d5c47` [running] analyst: DFXISP-A1 AI-ISP architecture and FPGA constraint analysis
- `dfxisp` `t_1bb8a94a` [running] coder: DFXISP-C1 Reproducible experiment scaffold and artifact logging plan
- `dfxisp` `t_e207e825` [running] reviewer: DFXISP-V1 Verification checklist for research-to-FPGA handoff
- `dfxisp` `t_5a1ff156` [running] reporter: DFXISP-REP1 Publish DFXISP Situation Room digest

## Boards
- `agent-os` — Agent OS: todo=2, blocked=1, done=11
- `dfxisp` — DFXISP: running=5, done=2
- `ai-drone` — AI드론: done=6

## Agent Team

| Agent | State | Model | Current Tasks |
|---|---|---|---|
| `operator` | idle | hermes / profile default | - |
| `pm` | idle | hermes / profile default | - |
| `admin` | idle | hermes / profile default | - |
| `researcher` | running | hermes / profile default | dfxisp:t_b872b08f running |
| `analyst` | running | hermes / profile default | dfxisp:t_0d6d5c47 running |
| `coder` | running | hermes / profile default | dfxisp:t_1bb8a94a running |
| `reviewer` | running | hermes / profile default | agent-os:t_82f11710 todo; dfxisp:t_e207e825 running |
| `reporter` | running | hermes / profile default | agent-os:t_eb8af557 todo; dfxisp:t_5a1ff156 running |
| `governor` | idle | hermes / profile default | - |
| `auditor` | blocked | hermes / profile default | agent-os:t_d8cd6477 blocked |
| `curator` | idle | hermes / profile default | - |
| `sentinel` | idle | hermes / profile default | - |

## Projects
- **DFXISP** `P0` `Active` — board `dfxisp`, path `/opt/data/projects/dfxisp` — 머신 비전을 위한 DFX AI-ISP 설계 / ZCU104 FPGA 구현
- **AI드론** `P1` `Exploration` — board `ai-drone`, path `/opt/data/projects/ai-drone` — 문제/가설/PoC/go-no-go 기준 탐색
- **Agent OS Ops** `P0` `Operating` — board `agent-os`, path `/opt/data/agent_os_archive` — 상황실, Drive/Slack archive, team governance

## Providers & Cost Guard
- `Hermes`: active / native / current — orchestration, files, cron, Kanban
- `Codex`: candidate / profile/cli/manual / managed/auth-present — coding, scripts, tests
- `Claude`: manual/not_configured / manual artifact ingest / paid if API enabled — analysis, review, design critique
- `Gemini`: manual/not_configured / manual artifact ingest / paid if API enabled — long context, research, documents
- `GPT`: current/default or not_configured / profile/manual / depends — synthesis, reporting

## Governance
- Cron active=4, failed=0
- Archive manifest exists=True, updated_at=2026-06-22T00:22:40.564550+00:00

## Source Files
- `dashboard`: `/opt/data/agent_os_archive/dashboard`
- `situation_board`: `/opt/data/agent_os_archive/summaries/agent-team/situation-board.md`
- `kanban_root`: `/opt/data/kanban/boards`
