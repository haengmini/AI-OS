# Git Workflow

## Repository

```text
https://github.com/haengmini/AI-OS
```

## Visibility

```text
private
```

Private repository이지만 secret, token, API key, Slack webhook URL은 절대 commit하지 않는다.

## Branch Rule

```text
main       → stable Agent OS
dev        → active development
feature/*  → experimental changes
```

## Before Commit

```bash
git status
git diff --check
```

## Commit

```bash
git add .
git commit -m "Update Agent OS"
```

## Push

```bash
git push
```

## Pull

```bash
git pull --rebase
```

## Secret Rule

Never commit:

```text
.env
API keys
Slack webhook URLs
tokens
private credentials
SSH keys
```

## Safety Rule

Approval required before:

```text
git push --force
rm -rf
deleting project folders
changing remote URL
rewriting git history
uploading secrets
```

## Document Rule

```text
README.md     → 통합 개요 문서
AGENT-OS.md  → Agent OS 헌법 / 운영 규칙
Manual.md     → 전체 사용 매뉴얼
OPERATION.md  → 생성 후 사용·관리법
REFERENCE.md  → 설계 출처와 이론
AGENTS.md     → Codex / Claude Code용 repo instruction
```
