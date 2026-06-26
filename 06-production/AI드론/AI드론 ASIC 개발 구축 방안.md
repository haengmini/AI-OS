---
project: AI드론
date: 2026-06-21
tags:
  - AI드론
  - ASIC
  - FPGA
  - 온보드AI
---

# AI드론 ASIC 개발 구축 방안

작성일: 2026-06-21  
대상 문서: `AI드론 프로젝트 / 드론 탑재형 FPGA 기반 온보드 AI 실행 플랫폼 구축 방안.docx` 추가 섹션 초안  
요청 컨펌: “ASIC 개발에 대해서도 2페이지 정도로 부탁해요.”  
범위: (1) Front-end 아키텍처 설계, RTL, 논리합성 (2) Backend P&R, layout, tape-out, MPW (3) 보드 (4) 소프트웨어 환경

## 1. ASIC 개발 목표와 추진 방향

AI드론의 온보드 AI 실행 플랫폼은 초기에는 FPGA 기반으로 알고리즘, 데이터 경로, 메모리 대역폭, 전력 예산, 센서 인터페이스를 빠르게 검증하고, 이후 반복적으로 안정화된 기능 블록을 ASIC으로 전환하는 단계적 전략이 적합하다. FPGA는 기능 검증과 현장 실험, 모델 변경 대응에 유리하지만, 드론 탑재 환경에서는 전력·무게·열·부피 제약이 강하므로 장기적으로는 고정 기능 가속기, ISP 전처리, 신경망 추론, 센서 동기화, DMA/메모리 서브시스템 등을 저전력 ASIC 또는 ASIC-ready IP 형태로 정리할 필요가 있다.

ASIC 전환의 핵심은 “바로 칩을 만든다”가 아니라 FPGA/SoC에서 검증된 온보드 AI 파이프라인을 재사용 가능한 하드웨어 IP, 검증 가능한 RTL, 합성 가능한 제약 조건, 소프트웨어 런타임과 드라이버까지 포함한 플랫폼 패키지로 고정하는 것이다. 따라서 본 과제에서는 Front-end, Backend, 보드, 소프트웨어 환경을 병렬로 정의하되, 각 단계의 산출물이 다음 단계의 입력이 되도록 관리한다.

## 2. 작업 1 — Front-end: 아키텍처 설계, RTL, 논리합성

Front-end 단계의 목표는 AI드론 온보드 플랫폼의 기능 요구사항을 하드웨어 아키텍처로 분해하고, FPGA 검증 결과를 기반으로 ASIC 구현 가능한 RTL과 합성 제약으로 정리하는 것이다. 우선 전체 시스템을 센서 입력부, ISP/전처리부, AI 추론 가속부, 후처리 및 의사결정부, 메모리/DMA, 제어 레지스터, 호스트 인터페이스로 나눈다. 드론 환경에서는 영상 입력의 프레임 지연, 센서 타임스탬프, 배터리 전력 상태, 비상 모드 전환이 중요하므로 단순한 AI accelerator만이 아니라 실시간 데이터 경로와 안전 상태 머신을 함께 설계해야 한다.

아키텍처 설계에서는 다음 항목을 먼저 고정한다. 첫째, 입력 해상도·프레임율·센서 수에 따른 처리량 목표를 정의한다. 둘째, 온칩 SRAM, 외부 DRAM, AXI interconnect, DMA burst 길이 등 메모리 구조를 결정한다. 셋째, CNN/NPU류 MAC array, depthwise convolution, activation, pooling, quantization/dequantization, image pre-processing pipeline 중 ASIC화할 블록과 소프트웨어로 남길 블록을 분리한다. 넷째, register map과 interrupt/event 구조를 정해 Linux driver와 런타임이 동일한 ABI를 사용하도록 한다.

RTL 구현은 SystemVerilog/Verilog 기준으로 합성 가능 코딩 스타일을 사용하고, clock/reset domain, CDC, low-power clock gating 가능성, scan/DFT 삽입 가능성을 초기부터 고려한다. 검증은 unit testbench, block-level simulation, FPGA prototype 비교, golden model 비교를 포함한다. AI 연산 블록은 Python/C++ reference model과 bit-exact 비교가 필요하며, 고정소수점 quantization 오차와 latency budget을 별도 표로 관리한다.

논리합성 단계에서는 target process node를 가정한 standard cell library, timing constraint, clock definition, IO constraint, false/multicycle path, area/power target을 준비한다. 초기 합성 산출물은 gate-level netlist 자체보다 “이 아키텍처가 주어진 clock에서 timing closure 가능하고, 면적·전력 범위가 드론 탑재 목표에 들어오는가”를 판단하는 근거로 사용한다. 산출물은 `architecture specification`, `RTL source`, `verification report`, `synthesis script`, `timing/area/power report`, `register map`으로 묶는다.

## 3. 작업 2 — Backend: P&R, Layout, Tape-out, MPW

Backend 단계는 합성된 netlist를 실제 실리콘 레이아웃으로 구현하는 과정이다. 주요 작업은 floorplanning, power planning, placement, clock tree synthesis, routing, timing closure, signal integrity, IR drop/EM 분석, DRC/LVS 검증, sign-off, tape-out package 생성으로 구성된다. AI드론용 ASIC은 고성능 서버용 NPU와 달리 절대 성능보다 전력 효율, 안정성, 작은 면적, predictable latency가 중요하므로 floorplan 단계에서 메모리 매크로, MAC array, DMA/interconnect, 제어부의 배치를 신중히 정해야 한다.

P&R 단계에서는 먼저 die size, pad ring 또는 flip-chip 여부, SRAM macro 배치, 주요 clock domain을 정의한다. 이후 placement와 CTS를 진행하면서 timing violation, congestion, clock skew를 반복적으로 줄인다. 영상/AI 데이터 경로는 버스 폭이 크고 burst traffic이 집중되므로 routing congestion과 전력망 강건성이 문제가 되기 쉽다. 따라서 power grid planning, decap insertion, high-toggle region 분산, thermal hotspot 검토를 초기부터 포함해야 한다.

Sign-off 단계에서는 static timing analysis, DRC, LVS, antenna check, IR drop, electromigration, formal equivalence check를 수행한다. tape-out 전에는 RTL freeze, netlist freeze, GDS freeze 기준을 명확히 두고, ECO 발생 시 영향 범위를 추적한다. MPW는 초기 ASIC 검증 비용을 낮추기 위한 현실적 접근이다. full custom tape-out 이전에 MPW shuttle을 통해 핵심 IP 블록 또는 축소된 AI/ISP subsystem을 실리콘으로 확인하면, 기능·전력·타이밍 리스크를 낮출 수 있다.

MPW 대상은 전체 드론 SoC가 아니라 `AI/ISP accelerator tile + DMA/register interface + test wrapper` 수준으로 시작하는 것이 적절하다. MPW 검증용 칩에는 scan/JTAG, BIST, UART/SPI 제어, test pattern loader, performance counter를 넣어 bring-up을 쉽게 해야 한다. Backend 산출물은 `floorplan`, `P&R scripts`, `STA report`, `power/IR report`, `DRC/LVS clean report`, `GDSII/OASIS`, `tape-out checklist`, `MPW bring-up plan`이다.

## 4. 작업 3 — 보드: ASIC/FPGA 연동 및 드론 탑재 평가 보드

보드 단계의 목표는 ASIC 또는 MPW 칩을 실제 드론 탑재 환경과 유사한 조건에서 검증할 수 있는 평가 플랫폼을 만드는 것이다. 초기에는 FPGA 보드와 센서 모듈을 사용해 기능을 검증하고, MPW 칩이 확보되면 ASIC daughter board 또는 evaluation board를 제작해 기존 FPGA/host 보드와 연동한다. 보드는 단순한 전기적 연결물이 아니라 전원, 클럭, 리셋, 센서 입력, 디버그, 열 설계, 무게/크기 제약을 함께 검증하는 시스템이다.

보드 설계 항목은 전원 레일, 전류 예산, PMIC 또는 regulator 선택, power sequencing, clock source, reset supervisor, JTAG/SWD/UART/SPI/I2C debug, MIPI CSI 또는 parallel sensor interface, DDR/LPDDR 또는 host memory interface, PCIe/USB/Ethernet 등 host 연결 옵션을 포함한다. 드론 탑재 환경에서는 배터리 전압 변동, 모터 노이즈, 진동, 열 방출 부족이 문제가 될 수 있으므로 전원 무결성, EMI/EMC, 커넥터 고정성, thermal pad/heatsink 가능성을 검토해야 한다.

평가 보드는 두 단계로 나누는 것이 현실적이다. 1단계는 lab bring-up board로, 측정 포인트와 디버그 포트를 충분히 확보해 기능 검증을 우선한다. 2단계는 drone-fit prototype으로, 크기·무게·전력·열 제약을 반영해 실제 탑재 가능성을 검토한다. 보드 산출물은 `block diagram`, `schematic`, `PCB layout`, `BOM`, `power budget`, `signal integrity checklist`, `bring-up procedure`, `measurement report`이다.

## 5. 작업 4 — 소프트웨어 환경: 컴파일러, Linux run-time, device driver

소프트웨어 환경은 ASIC 플랫폼의 사용성을 결정하는 핵심 요소다. 동일한 하드웨어라도 컴파일러, 런타임, 드라이버, profiling tool이 없으면 실제 AI드론 애플리케이션에서 재사용하기 어렵다. 따라서 하드웨어 설계와 동시에 `model → graph/layer lowering → accelerator command → DMA buffer → interrupt completion → result post-processing`으로 이어지는 실행 경로를 정의해야 한다.

컴파일러 또는 변환기는 TensorFlow Lite, ONNX, PyTorch export 등 상위 모델 형식에서 ASIC이 지원하는 연산 집합으로 모델을 변환하는 역할을 한다. 초기에는 완전한 범용 컴파일러보다 제한된 operator set을 대상으로 offline compiler를 구성하는 것이 현실적이다. 예를 들어 convolution, depthwise convolution, pooling, activation, quantize/dequantize, resize 등 드론 비전 파이프라인에 필요한 연산만 우선 지원하고, unsupported operator는 CPU 또는 FPGA/소프트웨어 fallback으로 처리한다.

Linux runtime은 user-space library와 kernel driver 사이의 ABI를 안정화한다. Runtime은 model binary loading, command buffer 생성, DMA buffer allocation, cache flush/invalidate, job submission, timeout 처리, profiling counter 수집을 담당한다. Device driver는 character device 또는 DRM/accelerator framework 형태로 구현할 수 있으며, mmap, ioctl, interrupt handler, DMA mapping, power management, reset recovery를 포함해야 한다. 드론 환경에서는 long-running job보다 짧고 예측 가능한 inference job이 중요하므로 timeout, watchdog, graceful degradation, thermal throttling 정책을 포함해야 한다.

소프트웨어 산출물은 `compiler/mapper specification`, `runtime API`, `Linux kernel driver`, `device tree binding`, `register map header`, `sample application`, `profiling tool`, `CI test fixture`이다. 특히 register map과 driver ABI는 Front-end 단계의 RTL register 설계와 동기화되어야 하며, FPGA prototype에서 먼저 검증한 뒤 ASIC/MPW 보드로 이전하는 흐름이 바람직하다.

## 6. 통합 일정과 리스크 관리

ASIC 개발은 Front-end와 Backend만의 문제가 아니라 보드와 소프트웨어까지 동시에 준비해야 성공 가능성이 높다. 추천 추진 순서는 다음과 같다.

1. FPGA 기반 기능 검증 결과를 기준으로 ASIC 후보 블록과 제외 블록을 선정한다.
2. ASIC-ready architecture spec, RTL, register map, verification plan을 작성한다.
3. FPGA prototype에서 runtime/driver ABI를 먼저 검증한다.
4. 합성 및 P&R feasibility를 통해 면적·전력·타이밍 리스크를 평가한다.
5. MPW용 축소 칩 또는 accelerator tile을 정의한다.
6. MPW bring-up board와 Linux software stack을 함께 준비한다.
7. 측정 결과를 기반으로 full ASIC 또는 차기 MPW 여부를 결정한다.

주요 리스크는 세 가지다. 첫째, AI 모델이 자주 바뀌면 ASIC 고정 기능과 충돌할 수 있으므로 operator set과 quantization 정책을 제한해야 한다. 둘째, 드론 탑재 환경의 전력·열 제약은 실리콘뿐 아니라 보드와 케이스에서 결정되므로 early power budget이 필요하다. 셋째, driver/runtime이 늦게 준비되면 칩 bring-up이 지연되므로 register map, command queue, interrupt, DMA ABI를 Front-end 초기에 고정해야 한다.

## 7. 4개 작업 실행 체크리스트

- [ ] Front-end: architecture spec, RTL partition, verification plan, synthesis baseline 생성
- [ ] Backend: P&R feasibility, sign-off checklist, MPW candidate definition 생성
- [ ] Board: lab bring-up board와 drone-fit prototype 요구사항 분리
- [ ] Software: compiler/runtime/driver ABI와 FPGA-first validation path 정의

## 8. Front-end 상세 산출물

Front-end 작업은 별도 상세 문서 `/opt/data/projects/ai-drone/asic-front-end-work.md`로 구체화했다. 해당 문서는 다음 항목을 포함한다.

- Sensor Input, Timestamp/Sync, ISP, Quantized AI Accelerator, DMA/Memory, CSR, Safety/Watchdog, Debug/DFT wrapper 단위의 architecture partition
- 합성 가능한 RTL block list: sensor adapter, pre-processing pipe, command queue, DMA read/write, AI conv/depthwise engine, CSR/IRQ/performance counter, safety watchdog FSM 등
- Linux runtime/driver와 공유할 register map 초안: version/capability, global control/status, IRQ, command queue, DMA, sensor/ISP/accelerator, watchdog, performance, error register
- Reference model, block simulation, integration simulation, FPGA prototype, synthesis feasibility, CDC/RDC로 이어지는 verification plan
- synthesis baseline input package와 timing/area/power/constraint/CDC/DFT report checklist
- FPGA-first 검증 경로와 ASIC-ready 전환 기준: requirements freeze, ABI freeze, functional/performance/safety confidence, RTL quality, synthesis feasibility, backend handoff readiness

## 9. Backend P&R/Layout/Tape-out/MPW 상세 산출물

Backend 작업은 별도 상세 문서 `/opt/data/projects/ai-drone/asic-backend-work.md`로 구체화했다. 해당 문서는 다음 항목을 포함한다.

- Backend readiness input: RTL/netlist/SDC/SRAM macro/register map/DFT/pad IO/target PVT freeze 조건
- Floorplan, power grid, placement, CTS, routing, timing closure, physical verification 단계별 작업 흐름
- DRC/LVS/STA/IR/EM/antenna/density/LEC/FEC/DFT coverage sign-off checklist
- Final GDSII/OASIS, netlist, SDC, SPEF, DEF, reports, manifest, checksum 중심 tape-out package checklist
- MPW 후보 범위: `AI/ISP accelerator tile + DMA/register interface + test wrapper`
- MPW bring-up: power-on, clock/reset, register access, test vector, DMA/pseudo-DMA, interrupt, performance/power measurement
- B0 Backend Readiness부터 B5 Silicon Bring-up Decision까지 gate별 pass/fail 기준
- MPW 비용 항목, 일정 milestone, 주요 리스크와 완화 방안

## 10. 보드 상세 산출물

보드 작업은 별도 상세 문서 `/opt/data/projects/ai-drone/asic-board-work.md`로 구체화했다. 해당 문서는 다음 항목을 포함한다.

- Lab bring-up board와 drone-fit prototype 요구사항 분리: 측정성/디버그 우선 vs SWaP·진동·EMI·커넥터 안정성 우선
- 공통 board block diagram: power protection/filtering/sequencing, PMIC/regulator, FPGA/MPW ASIC module, clock/reset, debug, sensor, host, memory, thermal/mechanical stack
- 전원, 클럭, 리셋, 디버그, 센서 인터페이스, host interface, thermal/vibration/EMI 요구사항/checklist
- FPGA board validation → MPW daughter/evaluation board → drone-fit prototype 전환 경로와 phase별 exit criteria
- power/thermal/weight/connector/EMI/host interface mismatch 리스크와 판단 게이트
- schematic/layout/bring-up/drone-fit checklist와 보드 제작 전 확정이 필요한 package, host path, sensor set, power/thermal envelope, FPGA carrier decision

## 11. 소프트웨어 환경 상세 산출물

소프트웨어 환경 작업은 별도 상세 문서 `/opt/data/projects/ai-drone/asic-software-stack.md`로 구체화했다. 해당 문서는 다음 항목을 포함한다.

- model export/compile → command buffer → DMA → interrupt completion → post-processing end-to-end 실행 경로
- 제한된 operator set 기반 offline compiler/mapper 1차 범위와 fallback/제외 항목
- Linux runtime C API 초안, kernel driver ioctl ABI, job state machine
- device tree binding 예시와 FPGA/MPW board 공통 property
- register map/driver ABI 동기화 규칙: ABI versioning, source-of-truth, generated header, 변경 절차
- FPGA prototype에서 먼저 검증할 register/DMA/interrupt/runtime smoke test
- compiler, runtime, driver, device-tree, sample app, profiling tool deliverable checklist

## 12. 문서 반영 메모

이 초안은 원본 `.docx`가 로컬 archive에서 발견되지 않아 프로젝트 로컬 산출물로 먼저 작성했다. Drive 원본 문서에 반영하려면 원본 `.docx` 위치 확인 또는 Drive 쓰기 승인이 필요하다.


---

## 관련 노트

- [[AI드론]]
- [[2026-06-21 AI드론 작업 로그]]
