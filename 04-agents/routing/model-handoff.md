# Model Handoff Rule

Agent decides role. Model performs cognition or implementation.

```text
Claude = planning, reasoning, research, documentation, review
Codex  = code editing, debugging, test generation, CLI execution, Git workflow
Gemini = optional/future model for Google ecosystem, multimodal, long-context, alternate review
```

Default complex task flow:

```text
Claude plan
→ Ponytail implementation gate (YAGNI/reuse/stdlib/native/installed dependency/one-line/minimum safe diff)
→ Codex implementation
→ Codex verification
→ Claude review
→ optional Chorus multi-model review for important diffs
→ optional Gemini alternate review
→ Memory/Dashboard/Slack update
```

Implementation agents must include a Ponytail Check in handoff when code/scripts/UI are changed. See `04-agents/policies/ponytail-engineering-rule.md`.
