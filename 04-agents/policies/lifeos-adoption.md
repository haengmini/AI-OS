# LifeOS / PAI Adoption

Source: <https://github.com/danielmiessler/LifeOS> (Personal AI Infrastructure, MIT)
Applied: 2026-06-24
Scope: Agent OS 개념 차용. **통째 설치하지 않는다** — PAI는 Claude Code-native라 `~/.claude`를 덮고 자체 데몬을 띄워 기존 Agent OS와 충돌. 개념만 이식한다.

## Purpose

PAI의 검증된 primitive를 Agent OS에 흡수해 약점(특히 "무엇이 done인가" 정의)을 보강한다. 기존 7-layer·Drive-first·safety·ponytail 규칙은 그대로 둔다.

## 채택 (adopt)

| PAI 개념 | 무엇 | Agent OS 이식 위치 |
|---|---|---|
| **ISA** (Ideal State Artifact) | "done이 어떤 모습인지"를 한 문서로 고정 | 프로젝트 `spec.md`를 ISA 형식으로 작성. 템플릿: `04-agents/templates/ISA-template.md`. Completion Rule(AGENT-OS.md §5)의 Done Criteria가 여기서 나옴 |
| **TELOS** | mission·goals·beliefs·mental models — AI가 무엇을 향해 최적화하는지 | `MY-TELOS.md` (Owner Profile 심화, `MY.md` 보조) |
| **The Algorithm** (OBSERVE→THINK→PLAN→BUILD→EXECUTE→VERIFY→LEARN) | 작업 루프 프레임 | 기존 task flow(spec→plan→tasks→execution→verification→review→report)와 동형 — 명칭만 참고, 흐름 유지 |
| **Containment zones** | 디렉터리별 privacy zone + 누출 차단 | secrets 위생(AGENT-OS.md §8) 보강 아이디어로 보류·참고 |
| **Text over opaque storage** | 정본은 평문/Markdown, `rg`로 탐색 | 이미 Drive-first + graphify로 충족 |

## 채택 안 함 (deliberately skip)

- **통째 설치 / Pulse 데몬 / one-line installer** — Agent OS와 중복·충돌. 우리 HQ 대시보드(`agent-os-hq`)가 같은 역할.
- **PAI의 anti-DB 순수주의** — PAI는 Postgres/SQLite를 피하지만, 우리는 *멀티에이전트 근실시간 조율*을 위해 조율 substrate(Postgres + SKIP LOCKED)를 쓴다. 1인 개인 OS(PAI)와 멀티에이전트 OS(우리)의 정당한 차이. 문서 정본은 여전히 Drive 평문.

## 규칙 연결

- 새 작업의 `spec.md`는 ISA 형식으로 쓴다 (정본 템플릿 위).
- 완료 판정은 ISA의 Done Criteria + Verification으로 한다 (AGENT-OS.md §5).
