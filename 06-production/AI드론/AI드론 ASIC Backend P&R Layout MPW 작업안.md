---
project: AI드론
date: 2026-06-21
tags:
  - AI드론
  - ASIC
  - FPGA
  - 온보드AI
---

# AI드론 ASIC Backend P&R/Layout/Tape-out/MPW 작업 구체화

작성일: 2026-06-21  
역할: Analyst decision/tradeoff memo  
대상 범위: `AI/ISP accelerator tile + DMA/register interface + test wrapper` 중심의 MPW-ready backend flow

## 1. Executive Decision

현재 AI드론 ASIC backend의 권고 방향은 full drone SoC tape-out이 아니라, 축소된 MPW 후보인 `AI/ISP accelerator tile + DMA/register interface + test wrapper`를 대상으로 P&R feasibility와 sign-off gate를 정의하는 것이다.

이유는 다음과 같다.

1. AI드론은 아직 conditional GO 단계이며, 하드웨어 구매·실비행·대규모 외부 협업은 보류 조건에 가깝다.
2. Backend 작업은 EDA/PDK/MPW 비용과 일정 리스크가 크므로, 전체 SoC보다 작은 tile로 실리콘 리스크를 먼저 낮추는 편이 합리적이다.
3. AI/ISP tile, DMA, register interface, test wrapper는 front-end·software·board 산출물과 직접 연결되어 bring-up evidence를 만들기 쉽다.
4. Full SoC에 필요한 CPU subsystem, complex IO, package, memory subsystem까지 포함하면 MPW 일정과 검증 범위가 급격히 커진다.

결론: MPW는 “제품 칩”이 아니라 “ASIC 전환 가능성 검증용 실리콘 실험”으로 정의한다.

## 2. Backend Flow 정의

### 2.1 입력 산출물

Backend를 시작하기 전에 다음 front-end 입력이 freeze되어야 한다.

| 입력 | 최소 조건 | 미충족 시 리스크 |
|---|---|---|
| RTL/netlist | 합성 가능한 top, lint/CDC major issue 정리 | P&R 반복 중 기능 변경 발생 |
| SDC constraints | primary clock, generated clock, IO delay, false/multicycle path 정의 | STA 결과 신뢰 불가 |
| SRAM/macro list | macro size, port, timing model, LEF/GDS/Lib availability | floorplan 재작업 |
| register map | driver ABI와 동기화 | bring-up 시 software mismatch |
| DFT/test requirement | scan/JTAG/BIST/test mode 정의 | MPW 칩 관측성 부족 |
| pad/IO assumption | shuttle pad frame 또는 top-level IO 정책 | tape-out package mismatch |
| target PVT corners | process/voltage/temp corner 범위 | sign-off gap |

### 2.2 Floorplan

목표는 timing, congestion, IR drop, bring-up 관측성을 동시에 만족하는 물리 구조를 만드는 것이다.

주요 작업:

- Die/core area estimate: synthesized area, macro area, utilization target 기반 산정
- Aspect ratio 결정: macro 배치와 bus direction 기준으로 초기 shape 선택
- Macro placement: SRAM/ROM/register file macro를 data path 근처에 배치
- Block partition: AI MAC/compute array, ISP pipeline, DMA/interconnect, CSR/control, test wrapper를 구역화
- IO/pad planning: clock/reset/test/JTAG/UART/SPI/control IO와 data IO 분리
- Keepout/halo/channel: macro 주변 routing channel 확보
- Congestion estimate: wide bus, DMA burst path, high-fanout control signal 검토

권고 배치 원칙:

- AI/ISP datapath와 SRAM macro는 가까이 배치해 local routing을 줄인다.
- DMA/interconnect는 external bus 또는 host/test wrapper와 연결되므로 중앙 또는 IO 인접 위치를 검토한다.
- CSR/control block은 timing criticality가 낮지만 bring-up 접근성이 중요하므로 test wrapper/JTAG 제어 경로와 가깝게 둔다.
- Clock source/PLL이 있다면 CTS와 noise isolation을 고려해 별도 구역으로 둔다. MPW 초기에는 PLL을 제외하고 외부 clock 입력을 우선 고려한다.

### 2.3 Power Grid / Power Planning

드론용 ASIC은 peak throughput보다 전력 예측성과 열 안정성이 중요하다. MPW에서도 power grid는 단순히 DRC 통과가 아니라 IR/EM 분석 가능성을 확보해야 한다.

주요 작업:

- Power domain 정의: core, SRAM/macro, IO, test/debug, optional always-on domain
- Power intent: UPF/CPF 필요 여부 판단. 초기 MPW는 단일 core domain + clock gating부터 시작하는 것이 현실적
- Ring/stripe/mesh 계획: utilization, routing layer, current density 기준으로 설정
- Decap insertion: high-toggle AI compute region 주변 우선 배치
- IR drop analysis: vectorless + switching activity 기반 vector-aware 분석 병행
- EM analysis: power rail과 high-current path 검토
- Power switch/retention: 초기 MPW에서는 복잡도를 낮추기 위해 보류 가능

Tradeoff:

| 선택 | 장점 | 단점 | 권고 |
|---|---|---|---|
| 단일 power domain | MPW 구현 단순, bring-up 쉬움 | 실제 저전력 제품성과 거리 있음 | 초기 MPW 권고 |
| 다중 power domain | 드론 저전력 시나리오 검증 가능 | UPF/검증/bring-up 복잡도 증가 | 차기 MPW/full ASIC 후보 |
| clock gating 중심 | RTL/STA 영향 제한적 | leakage 절감 한계 | 초기 low-power baseline |
| power gating 포함 | standby power 절감 | DFT/STA/verification 부담 | 초기 MPW에서는 보류 |

### 2.4 Placement

Placement 목표는 timing, congestion, power density를 동시에 맞추는 것이다.

주요 작업:

- Standard cell placement with target utilization
- Timing-driven placement
- Congestion-driven placement
- Macro pin access 확인
- High-toggle block 분산 또는 local decap 보강
- Scan chain reordering
- Tie/high-fanout cell insertion

Gate:

- Global route congestion이 critical overflow 없이 수렴해야 한다.
- Top timing path가 구조적으로 불가능한 수준이면 RTL/architecture feedback으로 되돌린다.
- SRAM macro pin access 문제가 반복되면 macro placement를 재검토한다.

### 2.5 CTS: Clock Tree Synthesis

주요 작업:

- Clock domain inventory: AI core, ISP pipeline, DMA/bus, CSR/test
- Clock gating cell integration
- Skew/latency target 설정
- Generated clock / test clock / scan clock constraint 검증
- Hold fixing strategy 정의
- Clock tree power estimate

권고:

- 초기 MPW는 clock domain 수를 최소화한다.
- CDC가 필요한 경우 async FIFO 또는 명시적 synchronizer를 사용하고 CDC report를 sign-off input으로 둔다.
- Clock gating은 functional enable과 scan/test mode compatibility를 검증해야 한다.

### 2.6 Routing

주요 작업:

- Global route congestion 분석
- Detailed route DRC cleanup
- Shielding/spacing for clocks and high-speed/control signals
- Antenna check/fix diode insertion
- Crosstalk/SI-aware routing if required
- ECO route flow 정의

드론 AI/ISP tile 특이 리스크:

- Wide datapath와 SRAM macro 사이 channel congestion
- DMA burst path와 register/control path 혼잡
- High-toggle compute block 주변 local power noise
- Test wrapper/JTAG/UART/SPI debug path의 route 후 timing 소홀

### 2.7 Timing Closure

Timing closure는 각 단계마다 반복한다.

필수 항목:

- Pre-CTS STA
- Post-CTS STA
- Post-route STA
- Multi-corner multi-mode STA
- Setup/hold closure
- OCV/AOCV/POCV 적용 여부
- Cross-domain path exception 검증
- ECO loop 관리

Sign-off gate:

| Gate | Pass 조건 |
|---|---|
| Setup timing | 모든 sign-off mode/corner에서 WNS/TNS non-negative 또는 승인된 waiver |
| Hold timing | 모든 sign-off mode/corner에서 hold clean |
| Constraint sanity | unconstrained path, disabled arc, false path waiver 검토 완료 |
| FEC/LEC | RTL-to-netlist, netlist-to-ECO equivalence clean |
| CDC/RDC | known-safe waiver 외 critical issue 없음 |

### 2.8 Physical Verification / Sign-off

Tape-out 전 sign-off는 최소 다음 항목을 포함한다.

| 항목 | 목적 | Pass 기준 |
|---|---|---|
| DRC | foundry design rule 위반 제거 | clean 또는 shuttle-approved waiver |
| LVS | layout과 schematic/netlist 일치 | clean |
| ERC | 전기적 rule 검증 | critical issue 없음 |
| Antenna | 제조 중 gate damage 위험 제거 | clean/waived |
| Density/fill | metal density/fill rule 만족 | foundry deck clean |
| STA | timing closure | all sign-off corners clean |
| IR drop | 전원 무결성 | limit 이내 또는 waiver |
| EM | current density 안정성 | limit 이내 |
| SI/crosstalk | timing/noise margin 확인 | critical violation 없음 |
| LEC/FEC | 논리 equivalence | clean |
| DFT coverage | scan/BIST/JTAG 관측성 | MPW 목표 coverage 충족 |

## 3. MPW 대상 범위

### 3.1 권고 MPW Candidate

1차 MPW 후보는 다음 블록으로 제한한다.

```text
AI/ISP accelerator tile
  + local SRAM or SRAM interface stubs
  + DMA/register interface
  + command/status CSR map
  + interrupt/event line
  + test wrapper
  + scan/JTAG or shuttle-supported debug access
  + UART/SPI/I2C simple control path if useful
  + performance counters
  + pattern loader/checker
```

포함할 기능:

- 제한된 operator set: convolution/depthwise/pooling/activation/resize 또는 프로젝트 모델에 필요한 subset
- ISP pre-processing subset: crop/resize/color conversion/filter 등 고정 pipeline 후보
- DMA descriptor 또는 command buffer minimal path
- Register read/write path
- Interrupt completion path
- Built-in deterministic test vectors
- Performance/power counter hooks

제외 또는 보류할 기능:

- Full CPU subsystem
- Full Linux-capable SoC integration
- Complex external DRAM controller
- Mission/flight control logic
- 자주 바뀌는 model-specific operator
- Multi-power-domain aggressive low-power scheme
- Production package/thermal optimization

### 3.2 MPW Bring-up 관점

Bring-up 성공 기준은 “칩이 전 기능 제품처럼 동작”이 아니라 “핵심 ASIC 전환 가설을 측정 가능하게 검증”하는 것이다.

Bring-up 시나리오:

1. Power rail sequence 확인
2. Clock/reset 정상 확인
3. JTAG/scan/test mode 접근 확인
4. Register read/write smoke test
5. Built-in pattern loader로 ISP/AI tile deterministic vector 실행
6. DMA 또는 pseudo-DMA path로 input/output buffer 이동 확인
7. Interrupt/event completion 확인
8. Performance counter latency/throughput 측정
9. Power measurement: idle, active, peak toggle 비교
10. Thermal/voltage margin 기초 sweep

Bring-up 산출물:

- Board power-on checklist
- Register access log
- Test vector pass/fail matrix
- Latency/throughput measurement
- Power measurement table
- Failure signature catalog
- Errata list
- Next MPW/full ASIC recommendation

## 4. Backend Deliverable Checklist

### 4.1 Planning / Setup

- [ ] Process node, foundry/MPW shuttle, PDK version 확인
- [ ] EDA tool chain and version lock
- [ ] Standard cell library, SRAM compiler/macro, IO library 확보
- [ ] Sign-off deck availability 확인: DRC/LVS/PEX/EMIR/STA
- [ ] Top-level scope: MPW tile vs full chip 명시
- [ ] Backend owner, front-end owner, software/board contact 정의

### 4.2 Design Inputs

- [ ] RTL freeze tag
- [ ] Netlist freeze tag
- [ ] SDC constraints
- [ ] UPF/low-power intent, if applicable
- [ ] LEF/DEF/Lib/GDS for macros
- [ ] SRAM macro placement assumption
- [ ] Register map and driver header alignment
- [ ] DFT insertion plan
- [ ] Test mode and scan/JTAG plan

### 4.3 P&R Deliverables

- [ ] Floorplan DEF
- [ ] Power grid plan
- [ ] Placement database/report
- [ ] CTS database/report
- [ ] Routing database/report
- [ ] ECO log
- [ ] Congestion report
- [ ] Utilization report
- [ ] Clock skew/latency report
- [ ] Timing reports by mode/corner

### 4.4 Sign-off Deliverables

- [ ] STA clean report
- [ ] DRC clean report
- [ ] LVS clean report
- [ ] Antenna clean report
- [ ] EM/IR report
- [ ] SI/crosstalk report if required
- [ ] LEC/FEC report
- [ ] DFT coverage report
- [ ] Power report with activity assumption
- [ ] Waiver list with owner/reason/expiry

### 4.5 Tape-out Package

- [ ] Final GDSII/OASIS
- [ ] Final netlist
- [ ] Final SDC
- [ ] Final SPEF/RC extraction
- [ ] Final DEF
- [ ] Final timing/power/physical verification reports
- [ ] Layer map / stream-out map
- [ ] LVS source netlist
- [ ] Fill insertion confirmation
- [ ] Tape-out README and manifest
- [ ] Checksums for submitted files
- [ ] Shuttle submission form/package metadata

### 4.6 MPW Bring-up Package

- [ ] Bring-up board requirement
- [ ] Pinout and package information
- [ ] Power rail/current budget
- [ ] Clock/reset requirements
- [ ] Debug access procedure
- [ ] Register test script
- [ ] Pattern generator/checker
- [ ] Firmware/runtime smoke test
- [ ] Measurement plan
- [ ] Pass/fail criteria

## 5. Sign-off Gates

### Gate B0 — Backend Readiness

Pass 조건:

- RTL/netlist/SDC/register map이 freeze됨
- PDK/library/macro availability가 확인됨
- MPW scope가 full SoC가 아닌 tile 수준으로 명시됨
- DFT/test wrapper requirement가 문서화됨

Fail 시 조치:

- Front-end로 되돌려 architecture/register/constraints 보완
- MPW 일정을 확정하지 않음

### Gate B1 — Floorplan Feasibility

Pass 조건:

- Area/utilization target이 현실적
- Macro placement와 routing channel이 확보됨
- Power grid 초안이 IR/EM 분석 가능한 수준
- Major congestion hotspot이 구조적으로 해결 가능

Fail 시 조치:

- Macro 수/크기 축소, bus width 조정, tile partition 재검토

### Gate B2 — Post-CTS Timing/Power Feasibility

Pass 조건:

- Setup/hold violation이 ECO로 수렴 가능한 수준
- Clock skew/latency target이 합리적
- Clock gating/test mode conflict 없음
- Power estimate가 보드/드론 budget과 비교 가능

Fail 시 조치:

- Clock domain 축소, pipeline 추가, target clock 완화, architecture feedback

### Gate B3 — Post-route Sign-off Candidate

Pass 조건:

- DRC/LVS major issue 없음
- STA가 all-mode/all-corner에서 clean 또는 제한적 waiver
- IR/EM이 limit 이내
- Antenna/density/fill issue 해결
- LEC/FEC clean

Fail 시 조치:

- ECO 반복. 반복 횟수 초과 시 MPW shuttle skip 판단

### Gate B4 — Tape-out Approval

Pass 조건:

- Final GDS/OASIS, netlist, reports, manifest, checksums 준비
- Waiver가 owner/reason/risk와 함께 승인됨
- Bring-up board/software readiness가 shuttle 일정과 정렬됨
- “무엇을 검증할 칩인가”가 pass/fail metric으로 정의됨

Fail 시 조치:

- Tape-out hold. 다음 shuttle로 연기하거나 scope 축소

### Gate B5 — Silicon Bring-up Decision

Pass 조건:

- Power-on, clock/reset, register access, test vector, performance/power 측정 완료
- 측정값이 front-end/P&R estimate와 비교됨
- Errata와 next-step decision이 정리됨

가능한 결정:

- GO: full ASIC 또는 차기 MPW로 확장
- ITERATE: tile 수정 후 다음 MPW
- HOLD: ASIC 전환 근거 부족, FPGA/software path 유지

## 6. MPW 리스크 / 비용 / 일정 고려사항

### 6.1 주요 리스크

| 리스크 | 영향 | 완화 |
|---|---|---|
| PDK/EDA 접근 지연 | 일정 지연, sign-off 불가 | shuttle/partner/MPW provider availability 선확인 |
| RTL 변경 지속 | P&R 반복 비용 증가 | RTL/netlist freeze gate 운영 |
| SRAM macro mismatch | floorplan 재작업 | macro availability를 B0에서 확인 |
| Timing closure 실패 | shuttle miss | target clock 완화, pipeline, scope 축소 |
| IR/EM violation | silicon reliability 저하 | early power grid + switching activity 기반 분석 |
| DRC/LVS late violation | tape-out 지연 | nightly physical verification checkpoint |
| Bring-up 관측성 부족 | 실패 원인 분석 불가 | test wrapper, counters, JTAG/scan, pattern loader 포함 |
| Software/board 미준비 | 칩 수령 후 idle | register test/runtime/board plan을 tape-out 전 병행 |
| 비용 불확실성 | 의사결정 지연 | shuttle fee, EDA, packaging, board, bring-up labor 분리 산정 |

### 6.2 비용 항목

정량 비용은 PDK/MPW provider/공정 node에 따라 달라 현재 문서에서는 범주만 명시한다.

- MPW shuttle slot 또는 die area 비용
- PDK/library/SRAM/IO access 비용
- EDA tool license 또는 partner engineering 비용
- DFT/sign-off/physical verification 지원 비용
- Packaging/assembly 비용
- Evaluation board 제작 비용
- Lab bring-up 장비/소모품 비용
- Firmware/runtime/driver bring-up 인력 비용
- 재시도 shuttle 비용

### 6.3 일정 항목

일정은 provider별 shuttle calendar에 종속된다. 내부 planning은 아래 milestone으로 관리한다.

1. Backend readiness: RTL/netlist/SDC/register map freeze
2. Floorplan/power plan feasibility
3. Placement/CTS feasibility
4. Route closure
5. Sign-off closure
6. Tape-out package submission
7. Fab/shuttle wait
8. Package/assembly
9. Board bring-up
10. Silicon measurement report
11. Next decision gate

일정 리스크를 낮추려면 MPW shuttle date를 먼저 고정하지 말고, B0~B3 gate 통과 가능성을 본 뒤 shuttle 후보를 선택한다.

## 7. Decision / Tradeoff Summary

| Decision | Recommendation | Rationale |
|---|---|---|
| MPW scope | Full SoC가 아닌 AI/ISP tile + DMA/register + test wrapper | 비용·일정·bring-up 리스크 최소화 |
| Low power | 초기 MPW는 단일 domain + clock gating | 다중 power domain은 검증 복잡도 큼 |
| External memory | full DRAM controller 제외, DMA/register 또는 simplified memory interface | MPW 목적은 accelerator feasibility 검증 |
| Debug | test wrapper/perf counter/pattern loader 필수 | silicon failure 분석 가능성 확보 |
| Tape-out gate | DRC/LVS/STA/IR/EM/LEC clean 없이는 hold | MPW라도 제조 후 수정 불가 |
| Bring-up success | 제품 동작이 아니라 측정 가능한 가설 검증 | conditional GO 프로젝트 상태와 정렬 |

## 8. Open Questions

1. 실제 target process node와 MPW provider가 정해졌는가?
2. PDK, SRAM macro, IO library, sign-off deck 접근 권한이 있는가?
3. AI/ISP operator set과 target clock/power budget이 front-end에서 freeze 가능한가?
4. MPW bring-up board를 자체 제작할 것인가, provider/evaluation board를 활용할 것인가?
5. Linux driver/runtime까지 MPW bring-up 전에 준비할 것인가, bare-metal/register script 중심으로 시작할 것인가?
6. Conditional GO 상태에서 MPW 비용을 승인할 판단 기준은 무엇인가?

## 9. Handoff Contract

## Summary
AI드론 ASIC backend의 P&R, floorplan, power grid, CTS, routing, timing closure, DRC/LVS, sign-off, tape-out, MPW bring-up 흐름을 구체화했다. 권고는 full SoC가 아니라 `AI/ISP accelerator tile + DMA/register interface + test wrapper` MPW를 통해 ASIC 전환 리스크를 제한적으로 검증하는 것이다.

## Inputs
- `/opt/data/projects/ai-drone/asic-development-plan.md`
- `/opt/data/projects/ai-drone/asic-front-end-work.md`
- `/opt/data/projects/ai-drone/go-no-go.md`
- Kanban task `t_7b37672b`

## Output
- `/opt/data/projects/ai-drone/asic-backend-pr-layout-mpw.md`

## Decisions
- MPW 범위는 full drone SoC가 아니라 AI/ISP accelerator tile + DMA/register interface + test wrapper로 제한한다.
- 초기 MPW는 단일 power domain + clock gating 중심으로 두고, power gating/multi-domain은 차기 단계로 미룬다.
- Tape-out approval은 DRC/LVS/STA/IR/EM/LEC/FEC 및 bring-up readiness gate를 통과해야 한다.

## Verification
- 프로젝트 기존 문서와 현재 go/no-go 조건을 기준으로 scope consistency를 점검했다.
- 산출물 파일을 프로젝트 workspace에 생성했다.
- 실제 PDK/EDA/MPW provider 정보는 아직 없어 정량 비용·일정·node-specific rule은 검증하지 못했다.

## Open Questions
- PDK/공정 node/MPW provider/EDA tool 접근 권한 미정.
- 실제 operator set, target clock, power budget, SRAM macro 정보 미정.
- 원본 `.docx`에 직접 반영하려면 Drive 원본 위치 확인 또는 쓰기 승인이 필요하다.

## Next Agent
- `reviewer`: backend checklist와 MPW gate가 과도하거나 누락된 항목이 없는지 검토.
- `pm`: MPW provider/PDK/EDA 접근 여부와 비용 승인 gate를 별도 task로 분해.
- `reporter`: 승인 후 프로젝트 보고서 또는 원본 문서에 2페이지 수준으로 축약 반영.


---

## 관련 노트

- [[AI드론]]
- [[2026-06-21 AI드론 작업 로그]]
