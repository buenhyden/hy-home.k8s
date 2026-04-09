# AGENTS.md Provider Notes

Guidance for consuming the `AGENTS.md` gateway contract.

## Role

`AGENTS.md` is the thin gateway contract for all agent providers (Claude, Gemini, Codex, etc.).
It defines §1–§8 pointers; it does not duplicate policy text from `rules/` or `scopes/`.

## Loading Model

- Load `AGENTS.md` as the first context anchor.
- Follow §1 Bootstrap to resolve the full JIT sequence.
- Do not cache or skip any step in the JIT sequence between sessions.

## Gateway Integrity Rules

- Never add policy text to `AGENTS.md` directly; add it to the appropriate `rules/` or `scopes/` file and add a pointer in `AGENTS.md`.
- §3 Agent Catalog must stay in sync with `.claude/agents/` directory contents.
- §7 Settings must reflect the current `settings.json` / `settings.local.json` split.

## Cross-Provider Consistency

- All providers must produce Korean user responses (§2 Constraints).
- All providers must run preflight and postflight (§1 Bootstrap).
- All providers must honor GitOps-First and no-plaintext-secrets constraints (§2 Constraints).
- Provider-specific tuning belongs in `providers/claude.md`, `providers/gemini.md`, etc.
