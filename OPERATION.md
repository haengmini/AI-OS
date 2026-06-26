# Agent OS Operation Guide

## 목적 / Purpose

이 문서는 Agent OS 생성 후 실제 사용법, 관리법, 점검법, 확장법을 정의한다.

## 1. 기본 사용 원칙

Core Flow는 `AGENT-OS.md` §2(헌법)를 단일 정본으로 따른다.

## 2. 매일 사용하는 기본 명령

```bash
cd ~/agent-os
tree ~/agent-os -L 2
git status
du -sh ~/agent-os
df -h
free -h
htop
```

## 3. 작업 시작 Flow

1. 요청 분류
2. 담당 Agent 결정
3. 관련 Layer 확인
4. spec / plan / tasks 작성
5. 실행
6. 검증
7. 보고
8. Memory / Dashboard / Slack 반영

## 4. 프로젝트 생성법

프로젝트는 Layer 6 Production에 생성한다.

```text
project-name
├── README.md
├── spec.md
├── plan.md
├── tasks.md
├── agents.md
├── data
├── logs
├── outputs
├── references
├── review.md
└── report.md
```

## 5. Memory 관리법

```text
중요한 결정       → decisions/decision-log.md
에러와 해결법     → debug/error-log.md
연구 내용         → research/research-notes.md
자주 쓰는 명령어   → commands/useful-commands.md
반복 작업         → skills/skill-index.md
성공한 workflow   → patterns/workflow-patterns.md
외부 자료 요약     → source-digests/external-sources.md
```

## 6. Model 사용법

Model routing은 `AGENT-OS.md` §4 / `03-models/README.md`를 참조한다.

## 7. Dashboard 사용법

```bash
cd ~/agent-os/05-dashboard/web
python3 -m http.server 8080
```

브라우저:

```text
http://localhost:8080
```

## 8. Slack 사용법

예시 명령:

```text
/agent status
/agent projects
/agent agents
/agent resource
/agent report today
/agent run hermes
```

## 9. Hermes Loop 사용법

핵심 루틴:

```text
daily-status-loop
project-review-loop
memory-cleanup-loop
skill-extraction-loop
weekly-tech-scout-loop
```

## 10. 주간 관리 루틴

Daily:

```text
[ ] Dashboard 확인
[ ] Active project 확인
[ ] Blocked task 확인
[ ] Error log 업데이트
[ ] Next Action 정리
```

Weekly:

```text
[ ] Memory cleanup
[ ] Project review
[ ] Skill extraction
[ ] Source digest 업데이트
[ ] Dashboard schema 점검
[ ] Slack command 점검
```

Monthly:

```text
[ ] Archive 정리
[ ] Agent role 재검토
[ ] Model routing 평가
[ ] Production project 정리
[ ] Portfolio/Career/Business 확장 검토
```

## 11. 유지보수 규칙

```bash
cd ~/agent-os
git status
git diff --check
git add .
git commit -m "Update Agent OS"
git push
```

## 12. 금지 사항

```text
7-layer 구조 무시 금지
Memory에 원문 대량 저장 금지
검증 없는 구현 완료 처리 금지
Dashboard 상태 미반영 금지
중요 에러 미기록 금지
API key 노출 금지
승인 없는 위험 명령 금지
반복 작업 수동 방치 금지
```
