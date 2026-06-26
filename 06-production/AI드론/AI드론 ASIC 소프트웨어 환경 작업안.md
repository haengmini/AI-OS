---
project: AI드론
date: 2026-06-21
tags:
  - AI드론
  - ASIC
  - FPGA
  - 온보드AI
---

# AI드론 ASIC 소프트웨어 환경 작업안

## 목적
ASIC/MPW/FPGA prototype에서 동일한 실행 모델을 사용할 수 있도록 compiler, Linux runtime, kernel driver, sample application 범위를 정의한다.

## 작업 범위

1. **Compiler / mapper**
   - TensorFlow Lite, ONNX, PyTorch export 등에서 제한된 operator set으로 변환하는 offline compiler를 우선한다.
   - 초기 지원 후보: convolution, depthwise convolution, pooling, activation, quantize/dequantize, resize, simple post-processing.
   - unsupported operator는 CPU 또는 FPGA/software fallback으로 처리한다.

2. **Runtime API**
   - model binary loading, command buffer 생성, DMA buffer allocation, cache flush/invalidate, job submission, interrupt wait, timeout, profiling counter 수집을 담당한다.
   - user-space API는 FPGA prototype과 ASIC driver에서 가능한 한 동일하게 유지한다.

3. **Linux kernel driver**
   - character device 또는 accelerator framework 형태로 시작한다.
   - mmap, ioctl, interrupt handler, DMA mapping, reset recovery, power management, watchdog, thermal throttling hook을 포함한다.
   - device tree binding과 register map header를 RTL register map에서 자동/반자동 생성하는 흐름을 검토한다.

4. **Validation path**
   - FPGA prototype에서 driver/runtime ABI를 먼저 검증한다.
   - sample app은 synthetic image/frame fixture를 사용해 inference job 제출, 결과 수신, timeout/recovery를 확인한다.
   - CI fixture는 register read/write mock, command buffer encoding, DMA buffer lifecycle, timeout path를 포함한다.

## 산출물

- `compiler/mapper specification`
- `runtime API document`
- `Linux kernel driver skeleton`
- `device tree binding`
- `register map header`
- `sample application`
- `profiling tool`
- `CI test fixture`

## 완료 기준

- `model → compile/map → command buffer → DMA → interrupt → result` 실행 경로가 정의됨.
- register map과 driver ABI의 동기화 규칙이 문서화됨.
- FPGA-first validation 후 ASIC/MPW 보드로 이전하는 절차가 명시됨.


---

## 관련 노트

- [[AI드론]]
- [[2026-06-21 AI드론 작업 로그]]
