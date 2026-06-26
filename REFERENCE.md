# Agent OS References

## 목적 / Purpose

이 문서는 Agent OS를 설계하고 생성하는 데 근간이 된 source, theory, idea, workflow, reference를 정리한다.

Agent OS는 단일 자료를 그대로 복사한 것이 아니라 여러 도구, 워크플로, AI agent 운용 방식, 개인 연구개발 요구사항을 통합해 설계한 범용 개인 AI 작업 운영체계이다.

## 1. Core Concept Sources

7-layer concept(구조 정의는 `AGENT-OS.md` §1 정본) 핵심 아이디어:

- AI 도구들을 하나의 작업 운영체계처럼 구성
- Memory를 중심으로 장기 맥락 유지
- Models와 Agents를 분리
- Dashboard로 상태 관제
- Production에서 실제 산출물 생성
- Loop로 반복 개선

## 2. AI Agent / Claude / Codex References

### Claude Prompting Workshops

반영 내용:

```text
Role / Persona
Task Description
Dynamic Content
Detailed Instructions
Examples
Final Reminder
XML-style structured prompt
Iterative refinement
```

### Claude Code Workflow

반영 내용:

```text
Start complex tasks in plan mode
Use parallel sessions / git worktrees
Maintain repo instructions
Create custom skills and slash commands
Use subagents
Always provide verification method
Use hooks for formatting or checking
```

### Codex

Codex는 implementation, debugging, testing, Git/CLI 작업 중심 모델로 설계되었다.

### Gemini Future Expansion

Gemini는 optional future model로 설계되었다.

```text
Gemini = Google ecosystem / YouTube-Web scan / multimodal / long-context scan / alternate review
```

## 3. Hermes Agent / Loop References

Hermes Agent는 Layer 7 Loop의 핵심 도구로 설계되었다.

반영 개념:

```text
Scheduled skill
Memory file
Repeated task automation
Skill extraction
Loop-based improvement
Agent OS feedback system
```

## 4. Dashboard / Slack / Web Control References

```text
Dashboard = Visual Interface
Slack = Mobile Command Interface
JSON = Shared State Layer
```

Dashboard는 Figma / Figma Make, open-source dashboard template, Codex implementation을 결합한다.

참고 후보:

```text
Figma
AdminLTE
TailAdmin
shadcn/ui
MUI Dashboard
React/Tailwind templates
```

## 5. Memory / Knowledge Management References

```text
Obsidian   → 메인 지식 저장소
Graphify   → 지식 관계 시각화
NotebookLM → 문서/PDF 기반 분석
Zotero     → 논문/특허/레퍼런스 관리
```

## 6. FPGA / Embedded / Hardware Workflow References

FPGA/Embedded workflow에서 얻은 원칙:

```text
GUI 수작업보다 script/CLI 기반 재현성
Tcl / Makefile / build script 기반 자동화
Self-checking testbench 지향
CI / regression test 중요성
resource usage / warning / timing report 기록
vendor tool version 관리
문서와 build flow의 재현성
```

주의:

```text
FPGA/AMD는 사용자 연구 정체성에 포함된다.
단, 특정 개인 프로젝트 자료는 project scope에 따라 별도 관리한다.
Agent OS 자체는 범용성을 유지한다.
```

## 7. Operating Theory

### Separation of Concerns

```text
Hardware = 실행 기반
Memory = 지식 저장
Models = 모델 선택
Agents = 역할 실행
Dashboard = 상태 관제
Production = 산출물 생성
Loop = 반복 개선
```

### Feedback Loop

```text
Execute
→ Verify
→ Report
→ Update Memory
→ Improve Workflow
→ Reuse
```

### Human-in-the-loop

위험 작업은 자동화하지 않고 사용자 승인으로 제어한다.

### Progressive Disclosure

항상 모든 정보를 모델에 넣지 않는다.

```text
먼저 index / summary / metadata만 제공
필요할 때 세부 문서 로드
```

### Reproducible Workflow

```text
spec
→ plan
→ tasks
→ execution
→ verification
→ review
→ report
```

## 8. Design Decisions

1. 7-layer Architecture를 최우선 규칙으로 설정
2. Agent와 Model을 분리
3. Dashboard와 Slack을 Layer 5로 통합
4. Production을 Project Factory로 설계
5. Hermes를 Loop Layer로 배치

## 9. Reference Management Rule

새로운 자료는 다음 형식으로 추가한다.

```md
## Source Name

### URL

### Type
YouTube / Reddit / X / GitHub / Docs / Paper / Blog

### Key Idea

### Agent OS Application

### Related Layer

### Status
candidate / adopted / rejected / archived
```
