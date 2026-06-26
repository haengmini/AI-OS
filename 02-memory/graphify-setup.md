---
type: raw
title: Graphify Setup
tags: [graphify, setup, memory]
created: 2026-06-18
updated: 2026-06-22
source: "manual setup notes"
status: stable
---

# Graphify Setup / 지식 그래프 연결

> Agent OS vault(`G:/내 드라이브/Agent OS`)를 graphify로 지식 그래프화하는 절차.
> graphify는 옵시디언 플러그인이 아니라, **폴더를 읽어 그래프를 만드는 CLI/AI-어시스턴트 스킬**이다.
> 공식 패키지명: `graphifyy` (y 두 개). CLI 명령은 `graphify`. Python 3.10+.

## 전제

마크다운·문서 추출은 **AI 코딩 어시스턴트(Claude Code / Codex / Gemini CLI)** 를 백엔드로 쓴다.
어시스턴트의 모델 API(내 키)로 추출하며, 코드 파일만이면 로컬 AST로 처리한다.

## 설정 절차

```text
1. 설치(완료): pip install graphifyy
   - Windows에서 `graphify`가 PATH에 안 잡히면:
     uv tool install graphifyy  (권장)  또는  python -m graphify

2. 스킬 등록:
   graphify install                    # Claude Code (Windows 자동감지)
   graphify install --platform gemini  # Gemini CLI
   graphify install --platform codex   # Codex

3. 빌드(어시스턴트 안에서, 경로 따옴표 필수):
   /graphify "G:/내 드라이브/Agent OS"
   → 출력: graphify-out/  (graph.html · GRAPH_REPORT.md · graph.json)

4. (선택) 옵시디언 그래프 vault도 생성:
   /graphify "G:/내 드라이브/Agent OS" --obsidian

5. (선택) 항상 그래프 먼저 읽게 (토큰 절약 핵심):
   graphify claude install     # CLAUDE.md + PreToolUse 훅
   graphify gemini install     # GEMINI.md + BeforeTool 훅
```

## 주의

```text
- 제외 규칙은 vault 루트의 .graphifyignore에 둔다.
  (지시 파일 CLAUDE/AGENTS/GEMINI.md, .obsidian/, graphify-out/, _archive/ 제외)
- vault가 Google Drive 위라 graphify-out/이 Drive에 동기화된다.
  용량 부담 시 graphify-out/cache/ 도 제외.
- 빌드는 첫 1회만 토큰을 크게 쓰고, 이후 질의는 압축된 그래프를 읽어 절약된다.
- 갱신: 파일 바뀐 뒤 /graphify "..." --update (변경분만 재추출).
```

## 운영 연계

```text
주기 갱신   → 07-loop (weekly-tech-scout / project-review 시 그래프 재빌드 고려)
고립 노드   → /lint 대상 (연결 안 된 wiki 노트 점검)
정본 출처   → REFERENCE.md §5 (Graphify = 지식 관계 시각화)
```
