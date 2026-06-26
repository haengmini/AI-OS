---
type: reference
title: AI Agent Ecosystem Radar
layer: memory
tags: [radar, ai-agents, pkm, automation, reference]
created: 2026-06-23
status: active
source: Reference_AIagent 보고서
---

# AI Agent Ecosystem Radar

> weekly-tech-scout 루프의 입력. 외부 생태계를 추적해 Agent OS에 흡수. 갱신 시 `[[log]]`.

## 1. 자율형 코딩 에이전트 (흡수 대상)
- `anthropics/claude-code`, `openai/codex`, `NousResearch/hermes-agent` — CLI 상주 자율 개발. → Agent OS coder/Hermes 설계 직접 참고.
- `DietrichGebert/ponytail` — YAGNI 룰셋(이미 적용). 코드 최소화.

## 2. 지식관리/그래프 (Memory layer)
- `safishamsi/graphify` — 지식 그래프(이미 사용, graphify-out).
- `obsidianmd/obsidian-releases`, `teng-lin/notebooklm-py` — vault/문서 분석.
- `multica-ai/andrej-karpathy-skills` — LLM wiki 원칙(MY.md 채택).

## 3. 멀티모델 리뷰
- Chorus — peer review/quorum (P2 #18 파일럿 대상).

## 4. 프롬프트/정렬
- `asgeirtj/system_prompts_leaks` — 시스템 프롬프트 설계 학습.

## 5. 커뮤니티/트렌드 (모니터링)
- Reddit: r/ClaudeAI, r/ClaudeCowork, r/hermesagent, r/codex, r/google_antigravity
- YouTube: @liamottley(AI 자동화 비즈), @nateherk/@chase-h-ai(툴 트렌드), @tinahuang1(커리어)

## 적용 우선순위
1. hermes-agent/claude-code 소스 → 에이전트 설계(#19, C1 핸드오프 패턴).
2. graphify/obsidian → Memory 파이프라인 유지.
3. Chorus → 리뷰 게이트(#18).
4. 커뮤니티 → 주간 스캔으로 기술부채/신기능 추적.

> 운영: [[weekly-tech-scout]] 루프가 이 radar를 주기 갱신.
