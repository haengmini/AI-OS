# Layer 1. Hardware

## 목적 / Purpose

Hardware Layer는 Agent OS 전체가 실행되는 기반 계층이다.

```text
Local PC
├── Windows Host
└── WSL Ubuntu 22.04 LTS
    └── ~/agent-os
```

## Core Rule

Agent OS는 Windows 파일시스템(`/mnt/c`)이 아니라 Ubuntu 파일시스템 내부에 위치한다.

## Base Package Stack

```text
1. Base CLI Tools
2. Dev Runtime
3. Web / Dashboard Runtime
4. Agent CLI Tools
5. Monitoring / Resource Tools
6. Security / Secret Management
```
