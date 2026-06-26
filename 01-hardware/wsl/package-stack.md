# WSL Package Stack

## 목적 / Purpose

이 문서는 Agent OS 7-layer 전체를 실행하기 위한 WSL Ubuntu base package stack을 정의한다.

## 1. Base CLI Tools

```bash
sudo apt update
sudo apt install -y \
  git curl wget tree unzip zip \
  build-essential make cmake pkg-config \
  ca-certificates gnupg lsb-release \
  jq ripgrep fd-find fzf \
  htop tmux openssh-client \
  python3 python3-pip python3-venv
```

## 2. Dev Runtime

```bash
sudo apt install -y nodejs npm
```

## 3. Python Dashboard Runtime

```bash
python3 -m pip install --user flask python-dotenv requests
```

## 4. Agent CLI Tools

```bash
curl -fsSL https://claude.ai/install.sh | bash
npm install -g @openai/codex
npm install -g @google/gemini-cli
```

## 5. Monitoring Tools

```bash
sudo apt install -y htop ncdu sysstat lsof net-tools
```
