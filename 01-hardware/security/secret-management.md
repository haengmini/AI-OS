# Secret Management

## 목적 / Purpose

Agent OS에서 사용하는 API key, Slack webhook, token, credential을 안전하게 관리한다.

## Rules

1. Never commit secrets to Git.
2. Never write secrets in README.md.
3. Never expose secrets on Dashboard.
4. Use `.env` only locally.
5. Add `.env` to `.gitignore`.
6. High-risk commands require user approval.
7. Do not run unknown install scripts without checking source.
