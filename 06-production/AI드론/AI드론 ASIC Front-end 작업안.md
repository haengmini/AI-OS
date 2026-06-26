---
project: AI드론
date: 2026-06-21
tags:
  - AI드론
  - ASIC
  - FPGA
  - 온보드AI
---

# AI드론 ASIC Front-end 작업 구체화

## Summary

FPGA 기반 온보드 AI 실행 플랫폼에서 검증된 기능을 ASIC-ready RTL/IP로 고정하기 위한 front-end 작업 범위, architecture partition, RTL block list, register map, verification plan, synthesis baseline, FPGA-first 검증 경로와 ASIC-ready 전환 기준을 정의한다.

## Inputs

- `/opt/data/projects/ai-drone/asic-development-plan.md`
- 요청 범위: AI드론 온보드 AI 플랫폼의 ASIC 개발 2페이지 추가 중 Front-end 아키텍처 설계, RTL, 논리합성 구체화

## 1. Front-end 목표와 범위

Front-end의 목표는 “드론 탑재 AI 기능을 곧바로 tape-out한다”가 아니라 FPGA에서 기능·성능·전력·소프트웨어 ABI를 먼저 검증한 뒤, 변경 가능성이 낮고 반복 사용 가치가 높은 데이터 경로를 ASIC-ready RTL/IP 패키지로 고정하는 것이다.

### In scope

- 센서 입력, ISP/전처리, AI inference accelerator, post-processing, DMA/memory, register/control, host interface의 architecture partition
- 합성 가능한 SystemVerilog/Verilog RTL block 정의
- Linux runtime/driver와 공유할 control/status register map 초안
- Python/C++ golden model 기반 bit-exact verification plan
- FPGA prototype과 ASIC synthesis baseline을 연결하는 검증 경로
- target clock, reset, CDC, timing constraint, area/power estimate 기준의 논리합성 baseline

### Out of scope 또는 ASIC 고정 보류

- 자주 바뀌는 모델별 operator 전체를 범용 NPU로 포괄하는 설계
- mission-level flight decision policy, 고수준 자율비행 정책
- 모델 학습/재학습 파이프라인
- backend P&R sign-off, board detailed schematic, Linux driver 구현 자체

## 2. Architecture partition

| Partition | 역할 | FPGA-first 검증 항목 | ASIC-ready 판단 포인트 |
|---|---|---|---|
| Sensor Input Adapter | MIPI CSI/parallel stream 또는 FPGA sensor bridge 입력 정규화, frame/line valid 처리 | frame drop, timestamp alignment, resolution/fps별 stress | 센서 수·해상도·fps 요구가 안정적이고 CDC/overflow가 검증됨 |
| Timestamp & Sync | frame timestamp, sensor sync, host clock correlation | multi-sensor skew, wraparound, reset 후 sync 복구 | 드론 제어 루프에서 요구하는 timestamp 정확도 충족 |
| ISP / Pre-processing | resize, crop, color conversion, normalization, optional denoise | golden image 비교, latency per frame, fixed-point 오차 | operator set이 고정되고 품질 저하가 허용 범위 내 |
| Quantized AI Accelerator Tile | INT8/INT16 conv/depthwise/activation/pooling 등 제한 operator 실행 | layer별 bit-exact 비교, saturation/overflow, throughput | 지원 operator와 quantization policy가 PoC 모델 2개 이상에서 안정적 |
| Post-processing Assist | threshold, NMS 후보 필터링, bounding box transform 일부 | CPU 대비 latency 개선, corner case | algorithm churn이 낮은 단순 반복 연산만 고정 |
| DMA & Buffer Manager | input/output tensor, frame buffer, command buffer 이동 | burst length, alignment, cache coherency, backpressure | bandwidth headroom과 timeout recovery가 확인됨 |
| AXI/Memory Interconnect | accelerator, DMA, register, external memory 연결 | contention, QoS, arbitration fairness | peak bandwidth와 worst-case latency가 budget 안에 있음 |
| Control/Register Block | CSR, interrupt, status, performance counter, error reporting | driver ABI smoke test, interrupt storm, error clear | register ABI freeze 후보로 관리 가능 |
| Safety/Watchdog FSM | timeout, thermal/power degrade, emergency bypass/reset | forced hang, brownout simulation, graceful degradation | fail-safe state와 reset recovery가 반복 재현됨 |
| Debug/DFT Wrapper | scan/JTAG hook, trace counter, BIST hook, FPGA debug probe | observability, trace counter consistency | bring-up에 필요한 최소 observability 확보 |

## 3. Top-level data/control flow

```text
Sensor/FPGA bridge
  -> Sensor Input Adapter
  -> Timestamp & Sync
  -> ISP / Pre-processing pipeline
  -> DMA write to frame/tensor buffer
  -> Command Queue + AI Accelerator Tile
  -> DMA read/write for intermediate/output tensors
  -> Post-processing Assist
  -> Interrupt/Event + Performance Counter
  -> Linux runtime / flight application
```

설계 원칙:

1. Streaming path와 memory-mapped path를 분리한다. 센서/ISP는 deterministic latency를 우선하고, AI accelerator는 DMA/command queue 기반으로 운용한다.
2. Register ABI는 FPGA와 ASIC에서 동일하게 유지한다. FPGA prototype의 driver/runtime이 ASIC bring-up의 출발점이 되어야 한다.
3. Safety path는 AI result와 독립적으로 동작해야 한다. accelerator hang 또는 timeout 시에도 bypass/reset/degrade 상태 전이가 가능해야 한다.
4. 모델 변화가 큰 부분은 software fallback 또는 FPGA-resident 영역으로 남기고, ASIC은 반복적·고정적·전력 이득이 큰 블록부터 고정한다.

## 4. RTL block list 초안

| RTL block | 주요 interface | 핵심 parameter | Verification owner/check |
|---|---|---|---|
| `sensor_rx_adapter` | stream in/out, cfg CSR, timestamp in | pixel format, lanes, width/height | malformed frame, fps stress, reset mid-frame |
| `frame_timestamp_unit` | sensor clock, system clock, CSR | counter width, sync mode | wraparound, drift, multi-sensor skew |
| `isp_preproc_pipe` | stream in/out, coefficient CSR | color mode, resize ratio, normalization | image golden diff, fixed-point error |
| `tensor_dma_rd` | AXI master, command queue | burst length, data width, alignment | bandwidth, backpressure, timeout |
| `tensor_dma_wr` | AXI master, completion event | burst length, data width, alignment | output integrity, cache coherency hooks |
| `cmd_queue` | AXI-lite CSR, SRAM/FIFO, irq | queue depth, descriptor format | invalid descriptor, overflow, ordering |
| `ai_conv_engine` | tensor stream, local SRAM | MAC array size, INT8/INT16 mode | layer bit-exact, saturation, utilization |
| `ai_dwconv_engine` | tensor stream, local SRAM | channel parallelism | depthwise-specific golden compare |
| `activation_pool_unit` | tensor stream | relu/relu6/pool mode | boundary, rounding, saturation |
| `local_sram_ctrl` | SRAM macro wrapper | banks, port mode, ECC/parity option | arbitration, read/write hazard |
| `postproc_filter` | tensor/result stream | threshold, top-k/NMS-lite option | corner cases, CPU reference compare |
| `csr_regfile` | AXI-lite/APB, block CSR bus | address map, access policy | reset value, write mask, RO/W1C behavior |
| `irq_event_unit` | block events, host irq | mask/status policy | interrupt coalescing, clear race |
| `perf_counter_unit` | event bus, CSR | counter width, event select | counter overflow, profiling consistency |
| `safety_watchdog_fsm` | timers, error signals, reset req | timeout threshold, mode policy | hang injection, recovery sequence |
| `clock_reset_ctrl` | clocks/resets, scan/test mode | reset order, clock gating enables | CDC/RDC, reset release ordering |
| `dfx_test_wrapper` | scan/JTAG/BIST hooks | test mode, isolation | synthesis/DFT compatibility checklist |

## 5. Register map 초안

Base address는 SoC/FPGA memory map 확정 전까지 `AIACCEL_BASE + offset` 형식으로 관리한다. Register ABI는 driver header와 RTL package에서 단일 소스로 생성하는 방식을 권장한다.

| Offset | Name | Access | Description | ASIC-ready freeze 기준 |
|---:|---|---|---|---|
| `0x0000` | `IP_VERSION` | RO | major/minor/patch, build id | FPGA/ASIC 공통 versioning 확정 |
| `0x0004` | `CAPABILITY` | RO | supported ops, data width, DMA width | operator set freeze와 연동 |
| `0x0008` | `GLOBAL_CTRL` | RW | enable, soft reset, clock gate hint | reset side effect 문서화 |
| `0x000C` | `GLOBAL_STATUS` | RO | idle, busy, error, degraded state | status transition 검증 완료 |
| `0x0010` | `IRQ_STATUS` | W1C | completion/error/timeout/perf event | W1C race 검증 |
| `0x0014` | `IRQ_MASK` | RW | interrupt mask | driver smoke test 완료 |
| `0x0020` | `CMDQ_BASE_LO` | RW | command queue base low | DMA address width 확정 |
| `0x0024` | `CMDQ_BASE_HI` | RW | command queue base high | 32/64-bit 정책 확정 |
| `0x0028` | `CMDQ_SIZE` | RW | descriptor count/bytes | queue overflow test 완료 |
| `0x002C` | `CMDQ_DOORBELL` | WO | submit new jobs | ordering/barrier 규칙 확정 |
| `0x0030` | `DMA_CFG` | RW | burst length, outstanding, QoS | bandwidth headroom 검증 |
| `0x0034` | `DMA_STATUS` | RO | dma busy/error code | timeout recovery 검증 |
| `0x0040` | `SENSOR_CFG` | RW | format, width, height, stride | 대상 센서 조합 확정 |
| `0x0044` | `FRAME_COUNTER` | RO | accepted frame count | drop detection 검증 |
| `0x0048` | `TIMESTAMP_LO` | RO | latest frame timestamp low | timestamp accuracy 검증 |
| `0x004C` | `TIMESTAMP_HI` | RO | latest frame timestamp high | wraparound test 완료 |
| `0x0060` | `ISP_CFG` | RW | resize/color/normalize mode | image quality 기준 충족 |
| `0x0080` | `ACCEL_CFG` | RW | op mode, precision, tiling mode | operator policy 확정 |
| `0x0084` | `ACCEL_STATUS` | RO | layer/job state | bit-exact regression 통과 |
| `0x00A0` | `POSTPROC_CFG` | RW | threshold/top-k mode | algorithm churn 낮음 확인 |
| `0x00C0` | `WATCHDOG_TIMEOUT` | RW | job timeout threshold | fail-safe policy 확정 |
| `0x00C4` | `WATCHDOG_STATUS` | W1C/RO | timeout/degrade/reset reason | recovery scenario 검증 |
| `0x0100` | `PERF_CYCLE` | RO | cycle counter | profiling correlation 검증 |
| `0x0104` | `PERF_DMA_STALL` | RO | DMA stall cycles | bottleneck analysis 사용 가능 |
| `0x0108` | `PERF_MAC_UTIL` | RO | MAC utilization estimate | synthesis/power estimate 입력 |
| `0x01F0` | `ERROR_CODE` | RO | last fatal/nonfatal error | error taxonomy 확정 |
| `0x01F4` | `ERROR_INJECT` | WO | verification-only fault injection | ASIC production disable 정책 확정 |

## 6. Verification plan

### 6.1 검증 레벨

| Level | 목적 | 주요 산출물 | Pass 기준 |
|---|---|---|---|
| Reference model | Python/C++ golden model로 expected output 고정 | model vectors, expected tensor/image | 입력 vector와 expected output이 versioned artifact로 저장됨 |
| Block simulation | RTL block별 기능 검증 | SV/UVM-lite 또는 cocotb test, waveform, coverage | reset/error/corner case 포함 smoke+regression 통과 |
| Integration simulation | DMA/command/register/interrupt 포함 subsystem 검증 | subsystem testbench, driver-like sequence | job submit부터 completion interrupt까지 반복 재현 |
| FPGA prototype | 실제 clock, memory, driver ABI 검증 | bitstream, runtime smoke test, perf log | 목표 fps/latency의 최소 기준 충족, hang recovery 검증 |
| Synthesis feasibility | ASIC target에서 timing/area/power 가능성 확인 | synthesis script/report, constraints | target clock WNS/TNS 수용 가능 또는 개선 경로 명확 |
| Formal/CDC/RDC | clock/reset crossing과 register access 안정성 확인 | CDC/RDC report, waiver list | critical crossing 미해결 0개, waiver 근거 문서화 |

### 6.2 필수 test vector

- 정상 frame: 목표 해상도/fps별 최소 3개 scene
- 경계 frame: width/height/stride alignment 경계값
- 비정상 입력: truncated frame, invalid descriptor, DMA misalignment, unsupported operator
- Fixed-point: rounding, saturation, overflow, negative/zero tensor
- Runtime: submit/cancel/timeout/reset/re-submit sequence
- Safety: accelerator hang injection, watchdog timeout, thermal/power degrade signal, emergency bypass
- Performance: sustained stream, burst traffic, memory contention, interrupt coalescing

### 6.3 Coverage/check metric

- 기능 coverage: register access policy, command descriptor field, operator mode, error code
- 데이터 coverage: image format, tensor shape, quantization scale/zero point, stride/alignment
- 시나리오 coverage: cold boot, warm reset, sensor reset mid-frame, DMA backpressure, timeout recovery
- 성능 metric: frame latency, inference latency, fps, DMA bandwidth, MAC utilization, stall cycles
- 품질 metric: golden model mismatch count, quantization error, post-processing precision/recall 영향

## 7. Synthesis baseline

논리합성 baseline은 tape-out sign-off가 아니라 architecture feasibility 판단 자료다. 따라서 “합성되었다”보다 “어떤 가정에서 timing/area/power risk가 보이는가”를 기록해야 한다.

### 7.1 Baseline input package

- RTL source tree와 file list
- top module, clock/reset definition
- target process/library placeholder 또는 PDK NDA 전 generic library
- SDC: clock, generated clock, input/output delay, false path, multicycle path
- SRAM macro assumption: bank count, width/depth, port, latency, area/power placeholder
- mode constraints: functional, scan/test, low-power clock gating mode
- synthesis script: tool version, compile options, report generation command

### 7.2 Baseline report checklist

| Report | 확인할 질문 | 의사결정 활용 |
|---|---|---|
| Timing | target clock에서 WNS/TNS가 감당 가능한가? critical path가 MAC/SRAM/DMA/control 중 어디인가? | pipeline 추가, clock target 조정, block partition 재검토 |
| Area | MAC array/local SRAM/control 비중이 예상과 맞는가? | ASIC 후보 블록 축소/확대 판단 |
| Power | switching power가 드론 전력 예산에 들어오는가? high-toggle block은 어디인가? | clock gating, duty cycle, operator set 조정 |
| Constraint quality | unconstrained path, ignored constraint가 없는가? | 합성 결과 신뢰도 판단 |
| CDC/RDC | crossing이 의도된 synchronizer를 통과하는가? | architecture sign-off gate |
| Lint | latch, combinational loop, width mismatch가 없는가? | RTL quality gate |
| DFT readiness | scan/test mode에서 blocking construct가 없는가? | backend/DFT 팀 handoff 가능성 |

### 7.3 초기 target 가정

구체 PDK가 확정되지 않았으므로 초기 baseline은 상대 비교용으로 사용한다.

- Target clock 후보: control/CSR 50~100 MHz, DMA/interconnect 100~250 MHz, AI tile 200~500 MHz 범위에서 sweep
- Data precision: INT8 우선, INT16/accumulator width는 model error 결과에 따라 제한
- Memory: local SRAM banked architecture 우선, external DRAM bandwidth 의존도를 perf counter로 측정
- Power: sustained peak보다 mission duty-cycle 기반 average power도 함께 추정
- Reset: async assert/sync deassert 원칙, safety watchdog reset domain 분리

## 8. FPGA-first 검증 경로

```text
FPGA PoC 기능 확인
  -> register ABI 초안 고정
  -> golden model/test vector 고정
  -> block RTL simulation
  -> FPGA bitstream + Linux/runtime smoke test
  -> performance counter 기반 병목 측정
  -> synthesis baseline으로 timing/area/power feasibility 확인
  -> ASIC-ready 전환 gate 통과 시 RTL/IP freeze 후보 지정
```

FPGA에서 먼저 확인해야 할 항목:

1. 동일 register map/header로 runtime이 job submit, interrupt wait, timeout reset을 수행한다.
2. 대표 AI 모델 1개 이상에서 layer output이 golden model과 bit-exact 또는 허용 오차 내 일치한다.
3. target frame latency와 inference latency가 budget 대비 headroom을 가진다.
4. DMA/memory contention 시에도 frame drop, timeout, recovery 동작이 관측 가능하다.
5. watchdog/degrade/bypass 경로가 AI accelerator 정상 동작과 독립적으로 검증된다.
6. performance counter가 bottleneck 분석에 충분한 resolution을 제공한다.

## 9. ASIC-ready 전환 기준

| Gate | 기준 | Evidence |
|---|---|---|
| Requirements freeze | 해상도, fps, sensor count, operator set, quantization policy가 변경 관리 상태 | architecture spec revision, decision log |
| ABI freeze | register map, command descriptor, interrupt/error taxonomy가 driver와 동기화 | generated header, FPGA runtime smoke result |
| Functional confidence | golden model 대비 mismatch가 없거나 허용 오차 근거가 명확 | regression report, vector archive |
| Performance confidence | latency/fps/bandwidth가 목표 대비 headroom 확보 | FPGA perf log, counter report |
| Safety confidence | timeout, reset recovery, degraded mode가 반복 재현 | safety test log |
| RTL quality | lint/CDC/RDC critical issue 0개 또는 waiver 승인 | lint/CDC report, waiver list |
| Synthesis feasibility | target clock에서 critical path 개선 가능, area/power가 예산 범위 후보 | synthesis timing/area/power report |
| Backend handoff readiness | SRAM macro, clock/reset, DFT hook, constraints가 backend 입력으로 사용 가능 | front-end release package |

전환 결론은 세 단계로 기록한다.

- `ASIC-ready`: 해당 block을 MPW/full ASIC 후보로 freeze 가능
- `FPGA-only for now`: 기능은 유효하나 model churn, RTL quality, synthesis risk로 ASIC 고정 보류
- `Software fallback`: 하드웨어 고정보다 CPU/GPU/FPGA software path 유지가 경제적

## 10. Deliverable checklist

### Architecture deliverables

- [ ] `architecture-spec.md`: system context, block diagram, data/control flow, clock/reset domains
- [ ] `asic-partition-matrix.md`: ASIC/FPGA/software 분담표와 rationale
- [ ] `interface-spec.md`: stream, AXI/AXI-lite/APB, interrupt, DMA descriptor 정의
- [ ] `memory-bandwidth-budget.md`: frame/tensor buffer size, DRAM/SRAM bandwidth, burst policy
- [ ] `safety-state-machine.md`: watchdog, timeout, degraded mode, emergency bypass 상태 정의

### RTL deliverables

- [ ] RTL source tree skeleton: `rtl/top`, `rtl/isp`, `rtl/ai_tile`, `rtl/dma`, `rtl/csr`, `rtl/safety`
- [ ] `rtl_block_list.md`: module, interface, parameters, owner, verification status
- [ ] `register-map.yaml` 또는 equivalent single source of truth
- [ ] generated `register_map.sv` and `register_map.h` 후보
- [ ] lint rule set 및 waiver policy
- [ ] CDC/RDC crossing inventory
- [ ] DFT/test mode 요구사항 초안

### Verification deliverables

- [ ] Python/C++ golden model과 versioned test vector
- [ ] block-level testbench list
- [ ] integration simulation scenario list
- [ ] FPGA runtime smoke test procedure
- [ ] performance benchmark script/log format
- [ ] mismatch triage template: input, expected, actual, root cause, disposition
- [ ] safety/fault injection test plan

### Synthesis deliverables

- [ ] synthesis file list
- [ ] baseline SDC constraints
- [ ] SRAM macro assumption sheet
- [ ] synthesis run script
- [ ] timing/area/power report template
- [ ] critical path triage log
- [ ] front-end release checklist for backend handoff

## Decisions

### Decision 1: FPGA-first 후 ASIC freeze

- 결정: ASIC front-end는 FPGA prototype에서 register ABI, driver/runtime path, golden model 비교, performance counter를 먼저 검증한 후 ASIC-ready freeze로 이동한다.
- 이유: 드론 탑재 AI는 모델·센서·전력 조건이 바뀔 가능성이 크므로 초기부터 고정 실리콘으로 잠그면 재작업 비용이 크다.
- Tradeoff: 일정은 길어지지만 잘못된 RTL freeze와 MPW 실패 리스크를 줄인다.

### Decision 2: 범용 NPU보다 제한 operator accelerator 우선

- 결정: 초기 ASIC 후보는 conv/depthwise/activation/pooling/ISP/DMA 등 드론 비전 파이프라인의 반복적 핵심 연산으로 제한한다.
- 이유: 범용 NPU는 compiler/runtime/verification 범위가 급증한다. 2페이지 추가 섹션의 현실적 개발 방안으로는 제한 operator set이 더 검증 가능하다.
- Tradeoff: 모델 유연성은 낮지만 전력·면적·검증 가능성이 좋아진다.

### Decision 3: register ABI를 front-end 초기 산출물로 승격

- 결정: register map과 command descriptor를 RTL 부속 문서가 아니라 driver/runtime과 공유하는 핵심 산출물로 관리한다.
- 이유: MPW/ASIC bring-up 지연의 주요 원인은 software path 준비 부족일 수 있다. FPGA 단계에서 ABI를 먼저 검증해야 한다.
- Tradeoff: 초기에 소프트웨어 팀과 조율 비용이 생기지만 backend 이후 bring-up 리스크를 낮춘다.

## Output

이 문서는 `/opt/data/projects/ai-drone/asic-development-plan.md`의 Front-end 섹션을 실행 가능한 산출물/checklist 수준으로 확장한 별도 산출물이다. 원본 `.docx` 반영은 Drive 원본 위치 확인 또는 Drive 쓰기 승인 후 별도 작업이 필요하다.

## Verification

- 문서 레벨 검증: architecture/RTL/verification/synthesis deliverable checklist가 모두 포함되었는지 확인한다.
- Traceability 검증: `asic-development-plan.md`의 Front-end 항목인 architecture partition, RTL, register map, verification, synthesis baseline이 본 문서의 섹션으로 연결되는지 확인한다.
- 실행 검증 한계: 실제 RTL, synthesis tool, FPGA bitstream은 아직 없으므로 timing/area/power 수치는 산출하지 않았다.

## Open Questions

- target FPGA board, sensor interface, target process node/PDK, target model/operator set은 아직 확정되지 않았다.
- register base address와 SoC host interface(AXI-lite/APB/PCIe/USB 등)는 보드/소프트웨어 작업과 함께 확정해야 한다.
- 원본 `.docx`에 직접 반영하려면 문서 위치와 Drive 쓰기 승인이 필요하다.

## Next Agent

- `reviewer`: 본 front-end checklist가 2페이지 보고서 목적에 비해 과도하거나 누락된 항목이 없는지 검토
- `reporter`: 사용자에게 전달할 문서에는 본 상세안의 핵심을 2페이지 분량으로 압축
- `coder` 또는 `hardware-specialist`(향후): 실제 RTL skeleton, register-map generator, FPGA smoke test fixture가 필요할 때 투입


---

## 관련 노트

- [[AI드론]]
- [[2026-06-21 AI드론 작업 로그]]
