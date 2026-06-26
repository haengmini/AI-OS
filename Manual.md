# Agent OS Manual

## 0. Purpose

이 문서는 Agent OS를 실제로 생성, 사용, 관리, 확장하기 위한 통합 매뉴얼이다.
7-layer 아키텍처 정의는 `AGENT-OS.md` §1(헌법)을 정본으로 한다.

## 1. Basic Definition

Agent OS는 이형민의 범용 개인 AI 작업 운영체계이다.

지원 범위:

- 연구개발
- FPGA / Embedded / Hardware Systems
- Software Development
- AI Tool Workflow
- 연구 노트
- 개인 커리어
- 포트폴리오
- 일상 관리
- 경제활동
- 사업 운영
- 학습
- 콘텐츠 제작

## 2. Create Base Structure

```bash
mkdir -p ~/agent-os/{01-hardware,02-memory,03-models,04-agents,05-dashboard,06-production,07-loop}
```

## 3. Layer 1. Hardware

Agent OS는 Windows 파일시스템이 아니라 Ubuntu 내부에 둔다.

```bash
~/agent-os
```

필수 패키지:

```bash
sudo apt update
sudo apt install -y \
  git curl wget tree unzip zip \
  build-essential make cmake pkg-config \
  ca-certificates gnupg lsb-release \
  jq ripgrep fd-find fzf \
  htop tmux openssh-client \
  python3 python3-pip python3-venv \
  nodejs npm \
  ncdu sysstat lsof net-tools pass
```

## 4. Layer 2. Memory

```text
02-memory
├── obsidian-vault
├── graphify
├── notebooklm
├── zotero
├── profile
├── decisions
├── debug
├── research
├── commands
├── knowledge
├── skills
├── patterns
├── source-digests
└── archive
```

## 5. Layer 3. Models

Model routing은 `AGENT-OS.md` §4 / `03-models/README.md` 참조.

## 6. Layer 4. Agents

```text
Core Control Agents
├── Operator
├── Admin
└── PM

Core Specialist Agents
├── Designer
├── Social Network
├── SW Coder
├── HW Coder
├── Researcher
├── Analyst
└── Reporter

Future Domain Agents
├── Life Agent
├── Finance Agent
├── Business Agent
├── Career Agent
└── Learning Agent
```

## 7. Layer 5. Dashboard + Slack

```text
Dashboard = Visual Interface
Slack     = Mobile Command Interface
JSON      = Shared State Layer
```

Dashboard는 Figma / Figma Make → open-source dashboard template → Codex implementation → JSON schema integration 흐름으로 만든다.

## 8. Layer 6. Production

```text
06-production
├── _templates
├── active
├── archived
├── research
├── software
├── embedded
├── career
├── portfolio
├── business
├── finance
├── life
├── learning
├── content
├── reports
├── experiments
├── web-pages
└── outputs
```

## 9. Layer 7. Loop

Hermes Agent 기반 feedback loop.

```text
Check Dashboard
→ Read active projects
→ Read related Memory
→ Review current status
→ Identify bottlenecks
→ Update Memory
→ Update Dashboard
→ Send Slack report
→ Suggest next action
```

## 10. Daily Usage

```bash
cd ~/agent-os
tree ~/agent-os -L 2
git status
du -sh ~/agent-os
```

Dashboard MVP 실행:

```bash
cd ~/agent-os/05-dashboard/web
python3 -m http.server 8080
```

## 11. Git

```bash
cd ~/agent-os
git status
git add .
git commit -m "Update Agent OS"
git push
```
