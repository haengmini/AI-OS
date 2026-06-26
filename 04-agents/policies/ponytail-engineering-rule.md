# Ponytail Engineering Rule

Source: <https://github.com/DietrichGebert/ponytail.git>
Applied: 2026-06-23
Scope: Agent OS coding, automation scripts, dashboard implementation, and future Codex/Claude Code/Gemini/OpenCode workflows.

## Purpose

Ponytail is adopted as Agent OS의 **engineering economy rule**: AI coder agents should behave like a lazy senior developer — efficient, not careless. The best code is the code that never needed to be written.

This does **not** replace Agent OS safety, verification, or Drive-first rules. It adds a pre-implementation gate that prevents over-engineering.

## Ponytail Ladder

Before writing code, the implementing agent must understand the task and real code path, then stop at the first rung that holds:

```text
1. Does this need to be built at all? (YAGNI)
2. Does it already exist in this codebase? Reuse it.
3. Does the standard library already do this? Use it.
4. Does a native platform feature cover it? Use it.
5. Does an already-installed dependency solve it? Use it.
6. Can this be one line? Make it one line.
7. Only then: write the minimum code that works.
```

## Agent OS Application

Use Ponytail especially for:

- dashboard scripts and UI changes
- cron jobs and healthcheck scripts
- Agent Registry / model registry generators
- Drive sync and local archive utilities
- DFXISP experiment scaffolds
- small automation tools
- future Codex/Claude Code implementation tasks

## Non-Negotiables

Ponytail is **not** an excuse to skip:

- understanding the real flow
- trust-boundary input validation
- error handling that prevents data loss
- security and secrets hygiene
- accessibility
- hardware calibration / real-device verification
- explicit user requirements
- at least one runnable check for non-trivial logic

## Review Mode

When reviewing code for over-engineering, use this format:

```text
<file>:L<line>: <tag>: <what to cut>. <replacement>.
```

Tags:

- `delete`: dead code, unused flexibility, speculative feature
- `stdlib`: hand-rolled thing the standard library provides
- `native`: dependency/code doing what the platform already does
- `yagni`: abstraction/config/layer without real second use
- `shrink`: same logic with fewer lines

End with:

```text
net: -<N> lines possible.
```

If there is nothing to cut:

```text
Lean already. Ship.
```

## Review Gate (검수 적용)

ponytail-review는 Agent OS 작업 흐름의 **review 단계 게이트**다 (AGENT-OS.md §5 Completion Rule · task flow의 review).

- **언제:** 코드·스크립트·대시보드·자동화 산출물이 review에 들어올 때마다 diff(또는 파일)에 ponytail-review를 돌린다. 플러그인이 있으면 `/ponytail-review`.
- **무엇을:** reinvented stdlib · 불필요 의존성 · speculative 추상화 · dead flexibility. 위 Review Mode 포맷으로 한 줄씩, 끝에 `net: -<N> lines possible.`
- **통과 기준(gate):**
  - findings 0 → `Lean already. Ship.` → 통과.
  - findings 있음 → **제거**하거나, 남길 경우 **한 줄 근거**(왜 필요한지)를 남긴다. 미해결 over-engineering은 report로 넘기지 않는다.
- **범위 밖:** correctness·security·성능 버그는 ponytail-review가 아니라 일반 리뷰로 따로 본다(둘은 보완 관계).
- **Handoff:** 구현 핸드오프엔 아래 `Ponytail Check` 블록 필수.

## Handoff Contract Addition

Implementation handoffs should include:

```md
## Ponytail Check
- Reused existing code? yes/no
- Avoided new dependency? yes/no
- Smallest safe diff? yes/no
- Runnable check left behind? yes/no/not needed
```

## Tool Integration Notes

Ponytail supports Claude Code, Codex, GitHub Copilot CLI, Pi, OpenCode, Gemini CLI, Antigravity, Cursor, Windsurf, Cline, Copilot editor, Aider/Kiro/Zed-style instruction files via copied rules.

Current local environment check on 2026-06-23:

- `node`: available
- `claude`: available
- `codex`, `gemini`, `copilot`: not currently on PATH

Therefore Agent OS applies Ponytail first as **instruction/policy**, and later can install host-specific plugins when those CLIs are configured.
