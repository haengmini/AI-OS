---
project: AI드론
date: 2026-06-21
tags:
  - AI드론
  - ASIC
  - FPGA
  - 온보드AI
---

# AI드론 ASIC/FPGA 연동 보드 작업안

작성일: 2026-06-21  
상위 산출물: `asic-development-plan.md` 작업 3 — 보드  
기존 간략 초안을 board block diagram/checklist 수준으로 확장  
목적: FPGA 기반 검증 환경에서 MPW/ASIC 평가 보드, 이후 드론 탑재 prototype으로 전환하기 위한 board-level 요구사항과 리스크를 분리한다.

## 1. 범위와 판단 기준

이 문서는 ASIC 개발 4개 축 중 보드 작업을 구체화한다. 보드 작업은 단일 PCB 제작이 아니라 다음 세 가지 검증 단계를 연결하는 system integration path다.

1. FPGA board 기반 기능 검증: 센서 입력, AI/ISP pipeline, runtime/driver ABI, host 통신을 빠르게 반복 검증한다.
2. MPW daughter/evaluation board 기반 실리콘 bring-up: MPW 칩의 전원, clock, reset, JTAG/debug, register/DMA path, 기본 성능/전력 측정을 검증한다.
3. Drone-fit prototype: 실제 드론 탑재 가능성을 power/thermal/weight/connector/EMI 관점에서 검증한다.

핵심 결정은 lab bring-up board와 drone-fit prototype을 분리하는 것이다. Lab board는 측정성과 디버그 접근성을 우선하고, drone-fit prototype은 SWaP(size, weight, and power), 진동, EMI, 커넥터 고정성, 열 경로를 우선한다. 하나의 보드로 두 목적을 동시에 만족시키려 하면 초기 bring-up 실패 원인 분석이 어려워지고, 반대로 lab-friendly 구조가 드론 탑재성 평가를 왜곡할 수 있다.

## 2. Board block diagram 수준 요구사항

### 2.1 공통 상위 블록

```text
Battery / Bench DC input
        |
Protection + filtering + power sequencing
        |
PMIC / regulators ---- power monitor / ADC / current sense
        |
FPGA or MPW ASIC module ---- clock tree ---- reset supervisor
        |                         |
        |                         +-- JTAG/SWD/UART/SPI debug
        |
Sensor interfaces ---- level shifting / ESD / connectors
        |
Host interface ---- USB / PCIe / Ethernet / UART / SPI
        |
Memory option ---- on-board DDR/LPDDR or host memory path
        |
Thermal + mechanical stack ---- heatsink / thermal pad / mounting holes
```

이 block diagram은 구체 부품 선정 전 요구사항 프레임이다. 초기에는 FPGA vendor board와 carrier/daughter board 조합을 허용하되, MPW 단계부터는 전원 sequence, clock/reset, debug, 측정 포인트를 schematic checklist로 고정해야 한다.

### 2.2 Power 요구사항/checklist

- 전원 입력
  - Lab bring-up: bench supply 입력, current limit 설정 가능, rail별 test point 필수.
  - Drone-fit: 배터리 전압 범위와 순간 drop, 모터/ESC 노이즈를 고려한 DC/DC filtering 필요.
- 전원 레일
  - Core voltage, SRAM/logic voltage, IO voltage, PLL/analog voltage, sensor/connector voltage를 분리 관리한다.
  - MPW/ASIC rail은 power sequencing 조건을 명시하고, enable/reset dependency를 schematic에 반영한다.
- 전류/전력 측정
  - Rail별 shunt/current monitor를 두어 idle, inference, sensor streaming, stress mode 전력을 분리 측정한다.
  - FPGA prototype 전력과 ASIC/MPW 측정치를 같은 workload 기준으로 비교한다.
- 보호/안전
  - Reverse polarity, over-current, ESD, brown-out reset, latch-up 의심 상황을 bring-up procedure에 포함한다.
- 산출물
  - `power tree`, `rail budget`, `power sequencing table`, `measurement point map`, `power risk table`.

### 2.3 Clock 요구사항/checklist

- Clock source
  - FPGA 단계: vendor board clock을 우선 사용하되 sensor pixel clock, accelerator clock, host clock domain을 문서화한다.
  - MPW/ASIC 단계: external oscillator, PLL reference, jitter budget, clock enable/reset relationship을 정의한다.
- Clock domain
  - Sensor/MIPI, AI accelerator, bus/DMA, host interface, debug domain을 분리하고 CDC 검증 항목과 연결한다.
- 측정성
  - Lab board에는 clock test point 또는 muxed clock-out을 두되, drone-fit board에서는 EMI와 routing risk 때문에 최소화한다.
- 산출물
  - `clock tree`, `clock domain table`, `jitter/tolerance assumption`, `CDC-linked checklist`.

### 2.4 Reset/boot 요구사항/checklist

- Reset source
  - Power-on reset, manual reset, host-triggered reset, watchdog reset, thermal/brown-out reset을 구분한다.
- Reset sequence
  - Rail stable → PLL lock → ASIC/FPGA reset release → register access check → memory/DMA init → sensor stream enable 순서로 정의한다.
- Recovery
  - DMA hang, interrupt storm, thermal throttle, sensor disconnect 상태에서 reset recovery가 가능한지 driver/runtime과 함께 검증한다.
- 산출물
  - `reset sequence diagram`, `boot checklist`, `failure recovery matrix`.

### 2.5 Debug/bring-up 요구사항/checklist

- 필수 debug path
  - JTAG 또는 SWD, UART console/log, SPI/I2C sideband control, GPIO straps, boot mode pins.
- Lab board 추가 항목
  - Rail별 test point, logic analyzer header, debug LED, strap switch, current probe loop, optional fault injection point.
- Drone-fit board 제한
  - Debug header는 작게 유지하고 비행 중 이탈 방지/절연을 고려한다. Bring-up용 큰 header는 lab board에만 둔다.
- 산출물
  - `bring-up checklist`, `debug connector pinout`, `strap table`, `known-good smoke test`.

### 2.6 Sensor interface 요구사항/checklist

- 후보 interface
  - Camera: MIPI CSI-2 또는 parallel camera interface.
  - IMU/altimeter/GNSS: SPI/I2C/UART.
  - Optional: range sensor, optical flow sensor, event camera 등은 PoC 범위 확정 후 추가한다.
- 설계 포인트
  - Sensor connector pinout, voltage level, ESD protection, cable length, ground return, shielding을 정의한다.
  - Timestamp/sync 신호가 필요한 경우 GPIO/trigger line을 별도 관리한다.
- Lab vs drone-fit
  - Lab board는 sensor module 교체성을 우선한다.
  - Drone-fit board는 connector locking, cable strain relief, vibration tolerance를 우선한다.
- 산출물
  - `sensor interface matrix`, `connector table`, `sync/timestamp plan`.

### 2.7 Host interface 요구사항/checklist

- Lab bring-up host
  - USB, Ethernet, PCIe, UART 중 debug와 throughput 요구를 분리해 선택한다.
  - Linux driver/runtime 검증을 위해 register access, DMA buffer transfer, interrupt completion path가 안정적으로 보이는 host interface가 필요하다.
- Drone-fit host
  - Flight controller 또는 companion computer와 연결되는 실제 interface를 가정한다. 무게/전력/connector 안정성이 throughput보다 우선일 수 있다.
- 권장 원칙
  - 초기 MPW bring-up은 가장 디버그하기 쉬운 host path를 우선하고, drone-fit prototype에서 최종 탑재 interface를 압축한다.
- 산출물
  - `host interface decision table`, `throughput/latency budget`, `driver ABI dependency list`.

### 2.8 Thermal/vibration/EMI 요구사항/checklist

- Thermal
  - Lab board: thermal camera/thermocouple 측정 위치, heatsink 교체 가능성, forced-air 조건을 명시한다.
  - Drone-fit: natural/prop wash airflow, enclosed mounting, thermal pad 경로, 주변 센서 열 영향 평가가 필요하다.
- Vibration/mechanical
  - Mounting hole, board thickness, connector locking, cable strain relief, mass distribution을 검토한다.
  - Lab board에서 큰 mezzanine connector를 사용하더라도 drone-fit에서는 낮은 profile과 고정 구조가 필요하다.
- EMI/EMC
  - Motor/ESC switching noise, camera cable EMI, high-speed host link, clock source shielding, ground return path를 확인한다.
  - Drone-fit에서는 debug cable이 없는 상태를 기준으로 EMI를 평가한다.
- 산출물
  - `thermal measurement plan`, `mechanical envelope`, `connector retention checklist`, `EMI risk checklist`.

## 3. Lab bring-up board와 drone-fit prototype 요구사항 분리

| 항목 | Lab bring-up board | Drone-fit prototype |
|---|---|---|
| 우선순위 | 측정성, 디버그, 원인 분석 | 탑재성, 전력/열/무게, 안정성 |
| 전원 | Bench supply, rail별 current monitor, 많은 test point | 배터리 입력 범위, filtering, 보호회로, 최소 test point |
| Clock/reset | 관찰 가능한 clock/reset, strap option | 고정 sequence, EMI 최소화, reset recovery 신뢰성 |
| Debug | JTAG/UART/SPI/I2C/GPIO header 풍부 | 최소 debug port, locking/insulation 고려 |
| Sensor | 모듈 교체 쉬운 connector | 실제 탑재 cable length와 고정 구조 반영 |
| Host | 디버그 쉬운 USB/Ethernet/PCIe 허용 | flight controller/companion computer 연결 현실성 우선 |
| Thermal | Probe/heatsink/forced-air 실험 가능 | 제한된 airflow와 mounting thermal path 평가 |
| Mechanical | 크기/무게 제약 완화 | SWaP envelope, 진동, connector retention 필수 |
| 성공 기준 | 전원 인가, ID read, register access, DMA/interrupt, workload 측정 | 목표 전력/열/무게 내에서 안정 동작, cable/connector 유지, EMI 이슈 없음 |

## 4. FPGA board → MPW evaluation board → drone-fit prototype 전환 경로

### Phase A — FPGA board validation

목표: ASIC 후보 블록과 software ABI를 보드 제작 전에 충분히 검증한다.

- FPGA board 또는 FPGA SoC board에서 sensor ingest, preprocessing, accelerator-like datapath, DMA/register path를 검증한다.
- Linux runtime/driver는 FPGA register map을 기준으로 먼저 작성해 MPW 단계의 bring-up 시간을 줄인다.
- Power는 절대값보다 workload별 상대 비교, peak/idle/inference 상태 구분에 집중한다.
- Exit criteria:
  - Register map 초안과 driver ABI가 freeze 후보 상태다.
  - 대표 workload에서 latency/throughput 측정이 가능하다.
  - ASIC화할 block과 FPGA/software에 남길 block이 구분되어 있다.

### Phase B — MPW daughter/evaluation board

목표: MPW 칩의 전기적/기능적 bring-up과 측정 가능성을 확보한다.

- MPW ASIC은 daughter board 또는 evaluation board 형태로 제작해 FPGA/host carrier와 연결한다.
- 필수 기능은 power sequence, clock/reset, JTAG/debug, register ID read, SRAM/BIST, DMA loopback, interrupt, performance counter다.
- Lab board는 측정 포인트와 fallback path를 넉넉히 둔다. 예: slow SPI control path, UART log, bypass clock option.
- Exit criteria:
  - Rail별 전류가 예상 범위 안에 있고 brown-out/latch-up 징후가 없다.
  - JTAG/register access가 안정적이다.
  - DMA/interrupt path가 Linux runtime과 연결된다.
  - 동일 workload 기준 FPGA 대비 power/latency trend를 비교할 수 있다.

### Phase C — Drone-fit prototype

목표: 실제 드론 탑재 제약에서 시스템 통합 가능성을 평가한다.

- Lab board에서 입증된 회로만 축소하고, debug/measurement 기능은 필요한 최소로 줄인다.
- Battery input, filtering, compact PMIC, locking connector, thermal path, mounting holes, cable routing을 반영한다.
- 드론 탑재 테스트는 반드시 bench/static test → vibration/thermal soak → non-flight powered integration → controlled flight readiness review 순서로 진행한다.
- Exit criteria:
  - 목표 power/thermal envelope 안에서 대표 workload를 반복 실행한다.
  - connector/cable 이탈, EMI-induced reset, thermal throttle, host disconnect가 재현되지 않는다.
  - 무게와 크기가 탑재 envelope 안에 들어온다.

## 5. Power/thermal/weight/connector 리스크

| 리스크 | 영향 | 초기 완화책 | 판단 게이트 |
|---|---|---|---|
| Rail sequencing 오류 | MPW 손상, bring-up 실패 | PMIC enable dependency, reset supervisor, current limit | 첫 전원 인가 전 schematic review + smoke test |
| Peak current 과소 추정 | brown-out, reset, 성능 불안정 | workload별 current monitor, margin 포함 rail budget | inference stress에서 rail droop 허용 범위 내 |
| FPGA 전력 추정치 착시 | ASIC 전환 판단 왜곡 | 동일 workload와 동일 sensor/host 조건으로 비교 | FPGA/MPW 비교표에 측정 조건 명시 |
| 열 경로 부족 | throttle, 오류, 수명 저하 | thermal pad/heatsink 옵션, 온도 센서, airflow 조건 기록 | drone-fit envelope에서 steady-state 온도 기준 통과 |
| 보드/커넥터 무게 초과 | 탑재 불가, 비행 안정성 악화 | lab board와 drone-fit 분리, connector 최소화 | 최종 board+connector+cable mass budget 통과 |
| Connector 이탈/접촉 불량 | 센서/host disconnect, reset | locking connector, strain relief, cable routing | vibration/static stress 후 link error 없음 |
| Motor/ESC EMI | sensor corruption, host link error, reset | input filtering, shielding, ground strategy, cable separation | 모터 노이즈 환경에서 error counter 기준 통과 |
| Debug header 과다 | 무게/EMI/기구 간섭 | lab-only header와 drone-fit minimal port 분리 | drone-fit layout review에서 제거/축소 확인 |
| Host interface mismatch | driver 재작성, 성능 부족 | early ABI freeze, interface decision table | MPW board 전에 host path 확정 |

## 6. Board work checklist

### 6.1 Architecture/checklist

- [ ] Lab bring-up board와 drone-fit prototype 목적을 별도 요구사항으로 분리했다.
- [ ] FPGA board, MPW board, drone-fit board의 block diagram 차이를 문서화했다.
- [ ] ASIC/FPGA 후보 block과 host/runtime/driver dependency가 연결되어 있다.
- [ ] Sensor, host, debug, power, clock, reset interface matrix가 있다.

### 6.2 Schematic/checklist

- [ ] Power tree와 sequencing table이 있다.
- [ ] Clock source, PLL reference, reset supervisor, strap pins가 정의되어 있다.
- [ ] JTAG/UART/SPI/I2C/GPIO debug path가 bring-up에 충분하다.
- [ ] Sensor/host connector pinout, voltage, ESD, cable assumption이 명시되어 있다.
- [ ] Rail별 test point/current monitor가 lab board에 포함되어 있다.

### 6.3 Layout/checklist

- [ ] High-current path, high-speed path, clock path, sensor cable path가 충돌하지 않는다.
- [ ] Ground return, decoupling capacitor placement, PMIC thermal area를 검토했다.
- [ ] MPW/ASIC package escape, differential/high-speed constraints, impedance control이 반영되어 있다.
- [ ] Drone-fit board는 mounting hole, board outline, connector orientation, cable strain relief를 반영한다.

### 6.4 Bring-up/checklist

- [ ] No-chip/no-load 전원 테스트 절차가 있다.
- [ ] Rail-by-rail current limit과 예상 idle current 범위가 있다.
- [ ] JTAG detect, chip ID read, register read/write, BIST, DMA loopback, interrupt test 순서가 있다.
- [ ] Failure log template가 있다: rail, clock, reset, host, sensor, thermal, EMI 증상별로 분류한다.

### 6.5 Drone-fit/checklist

- [ ] Board+connector+cable weight budget이 있다.
- [ ] Thermal steady-state 측정 조건과 pass/fail 기준이 있다.
- [ ] Vibration/connector retention 확인 절차가 있다.
- [ ] Motor/ESC 노이즈 환경에서 sensor/host error counter를 확인한다.
- [ ] Flight readiness 전 bench/static powered integration을 완료한다.

## 7. Decision memo

Decision: ASIC/FPGA 연동 보드는 `lab bring-up board`와 `drone-fit prototype`을 분리해서 정의한다.

Rationale:
- MPW/ASIC 초기 bring-up은 원인 분석이 최우선이므로 측정 포인트, debug header, bench supply, fallback host path가 필요하다.
- 드론 탑재성 평가는 크기/무게/전력/열/EMI/진동 조건이 최우선이므로 lab board의 풍부한 debug 구조를 그대로 가져가면 잘못된 판단을 만들 수 있다.
- FPGA → MPW → drone-fit 전환 경로를 명확히 두면 software ABI, register map, sensor/host interface를 단계적으로 고정할 수 있다.

Tradeoff:
- 보드를 두 계열로 나누면 일정과 제작 비용이 증가한다.
- 대신 MPW 손상, bring-up 지연, 드론 탑재 실패 원인 혼선을 줄인다.
- 현 단계가 exploration/P1이고 ASIC 개발도 아직 계획 구체화 단계이므로, 실제 제작 전에는 lab board requirement부터 freeze하고 drone-fit은 envelope/risk checklist 수준으로 유지하는 것이 적절하다.

## 8. 다음 의사결정 필요 항목

아래 항목은 보드 제작 전 확정이 필요하다.

1. MPW/ASIC package 가정: BGA/QFN/WLCSP 등 package와 pin count.
2. 주 host path: USB/Ethernet/PCIe/UART/SPI 중 lab bring-up 우선 path와 drone-fit 최종 path.
3. 주 sensor set: camera interface와 IMU/altimeter/GNSS 등 최소 sensor matrix.
4. 목표 power/thermal envelope: drone-fit prototype에서 허용할 전력, 온도, 무게, board outline.
5. FPGA carrier 선택: 기존 vendor board 활용 여부와 MPW daughter board 연결 방식.

## 9. 프로젝트 report 반영용 요약

ASIC 보드 작업은 `FPGA board validation → MPW daughter/evaluation board → drone-fit prototype`의 3단계로 추진한다. Lab bring-up board는 전원/클럭/리셋/디버그/host path 측정성을 우선하고, drone-fit prototype은 power/thermal/weight/connector/EMI/vibration 탑재성을 우선한다. 주요 리스크는 rail sequencing, peak current, 열 경로, connector 이탈, motor/ESC EMI, host interface mismatch이며, 각 단계별 exit criteria와 checklist로 관리한다.


---

## 관련 노트

- [[AI드론]]
- [[2026-06-21 AI드론 작업 로그]]
