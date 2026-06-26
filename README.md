# Agent OS — 단일 정본 (Single Source of Truth)

> 이형민의 1인 R&D 작업 운영체계. **이 파일 하나가 정체성·사명·운영규칙·구조의 정본이다.**
> 예전엔 MY / MY-TELOS / AGENT-OS / README 4곳에 흩어져 있었다 → 여기로 합쳤다 (2026-06-25, ponytail 정리).
> 원칙: 이 파일은 index이자 헌법이다. 늘어나면 다시 줄인다.

---

## 1. 나는 누구인가 (Owner)

```text
이형민 (Hyeongmin Lee) · ihyeongmin00@gmail.com
제주대 전자공학과 임베디드시스템 연구실 · 석사 3학기 · Jeju
```

연구 분야(지속): **FPGA 기반 재구성형 하드웨어 + 적응형 ISP(Adaptive ISP) + Edge AI 가속.**
회로를 정적 설계가 아니라 런타임에 바꾸는 것(DPR)에 관심.
구체적 현재 주제·수치는 여기 적지 않는다 → `06-production/<project>/`.

도구는 **고정**(호환성): Vivado/Vitis 2024.1, WSL Ubuntu 22.04, ZCU104, STM32, Python(cocotb).
검증 체인: Verilator(lint) → Icarus+cocotb(golden bit-exact) → Vivado batch(synth/timing). **임의 업그레이드 제안 금지.**

## 2. 사명·목표 (Telos)

- **사명:** 강점이 다른 AI 모델을 하나로 통합해 시너지를 내고, 그 통합 시스템을 연구·학습·경제·생산에 적용해 생산성을 극대화한다. (통합 AI = 수단, 다방면 생산성 = 목적.)
- **단기(~3개월):** DFXISP 논문 작성 · Agent OS 자율 운영.
- **중기(2026.10):** 석사 졸업 논문. **장기:** 통합 AI R&D 체계 완성·발전.

## 3. 핵심 신념 (이 정리의 근거)

- 근거 기반 행동 / 복리 엔지니어링(실수는 재료) / 좋은 기술은 빠르게 흡수·선택 적용 / **사고보다 실행**.
- 사고 모델: 제1원리, **단순화(ponytail) — "더 쉽고 간단하게 할 수 없나?"**, 자동화·task 최소화.
- **Anti-Goals(하지 않을 것):** 파편화, 과설계, 검증 없는 과신·할루시네이션, 졸업을 늦추는 곁가지, 도메인 깊이를 잠식하는 도구.

> 이 README가 짧게 유지되는 것 자체가 위 신념의 실천이다.

## 4. 협업 규칙 (How to work with me)

```text
언어   : 설명·판단·보고는 한국어. 코드·명령어·파일명·role·config는 영어.
어조   : 간결·직접. 군더더기·과한 사과·반복 칭찬 배제.
검증   : 검증 수단을 함께 설계한다. 미검증 결과를 단정하지 않는다("시뮬 수준 확인됨"식 명시).
계획   : 복잡한 작업은 plan 합의 후 실행 (spec → plan → tasks → execution → verification → review → report).
스타일 : 변경의 *이유*까지 설명. 낯선 코드는 ASCII/HTML로 구조부터.
```

## 5. 운영 규칙 (Constitution — 옛 AGENT-OS.md)

```text
1. 작업 전 이 README 관련 섹션을 읽는다.
2. 미검증을 "완료"로 처리하지 않는다. 완료 = [산출물 / 검증(또는 정의) / 리스크 / 다음 액션].
3. 구현은 Ponytail ladder: 만들 필요 없음 → 재사용 → stdlib → native → 설치된 dep → one-line → 최소 구현.
   단 validation·security·data-loss·검증은 절대 줄이지 않는다 (lazy = efficient, not careless).
4. Memory에 원문 대량 저장 금지. 재사용 지식만(요약·규칙·근거·다음액션) → memory(02-memory).
5. 위험 작업(파일 삭제·대량 이동·git push·external upload·API key·sudo)은 사용자 승인 후.
6. 모델 역할: Claude=계획·연구·문서·리뷰 / Codex=구현·디버그·테스트·Git / Gemini=선택(멀티모달·롱컨텍스트).
```

## 6. 구조 (Minimal Map)

```text
Agent OS/
├── README.md      ← 이 파일. 정본(정체성·사명·규칙·구조).
├── OPERATIONS.md  ← 운영 런북(매일 돌리는 최소 루프·MVP v0.1 완료기준).
├── CLAUDE.md      ← 에이전트 진입점(짧은 라우팅).
├── AGENTS.md      ← Codex 계약(짧게, 이 README를 가리킴).
├── 02-memory/     ← 재사용 지식 위키. 실제 노트만. 진입점: 02-memory/index.md.
├── 06-production/ ← 실제 프로젝트·산출물 = 시스템의 본체. (AI드론, DFXISP)
├── 05-dashboard/  ← 라이브 상태·UI. 매일 여는 화면: hq-dashboard.html (정본 3: html·json·build_dashboard.py).
└── _archive/      ← 옛 메타 문서·중복·세션 로그. 구조에서 제외.
```

> 7-layer(Hardware→Memory→Models→Agents→Dashboard→Production→Loop)는 **이제 폴더가 아니라 개념**이다.
> 사고 모델로는 유효하나, "폴더로 운영"할 만큼 내용이 없던 층(hardware/models/agents/loop 문서)은 _archive로 강등한다.
> 살아있는 폴더는 셋: **memory(아는 것) · production(만드는 것) · dashboard(보는 것).**

## 7. 프로젝트 형식 (Production)

각 프로젝트는 필요한 것만: `README.md`(= spec, "무엇이 done인가" 먼저 고정) + `outputs/` + 필요 시 `data/ logs/ references/`.
과한 스캐폴딩(spec/plan/tasks/agents/review/report 7파일 강제)은 만들지 않는다 — 필요할 때만 추가.

## 8. 갱신 규칙

이 파일은 wiki다, dump가 아니다. 추가 정보는 다음 중 하나 이상이어야 한다:
① 반복 재사용 ② 다른 에이전트/미래의 내가 꼭 읽음 ③ 결정 근거 추적 ④ 재시도 금지 리스크 ⑤ 전체 공통 규칙.
하나도 아니면 일지나 `_archive/`로. 늘어나면 줄인다.
