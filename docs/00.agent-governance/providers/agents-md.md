# AGENTS.md Provider Notes

Guidance for consuming the `AGENTS.md` gateway contract.

## Role

`AGENTS.md` is the thin gateway contract for all agent providers (Claude, Gemini, Codex, etc.).
It defines bootstrap, constraints, and routing pointers; it does not duplicate policy text from `rules/`, `scopes/`, or provider files.

## Loading Model

- Load `AGENTS.md` as the first context anchor.
- Follow §1 Bootstrap to resolve the full JIT sequence.
- Do not cache or skip any step in the JIT sequence between sessions.

## Gateway Integrity Rules

- Never add policy text to `AGENTS.md` directly; add it to the appropriate `rules/` or `scopes/` file and add a pointer in `AGENTS.md`.
- Routing pointers must stay in sync with `docs/00.agent-governance/harness-catalog.md`, `subagent-protocol.md`, and rule documents.
- Runtime roster details belong in `docs/00.agent-governance/harness-catalog.md`, not in `AGENTS.md`.
- `.codex/agents/*.toml` mirror status belongs in `harness-catalog.md` and `subagent-protocol.md`, not in a root catalog table.

## Cross-Provider Consistency

- All providers must produce Korean user responses (§2 Constraints).
- All providers must run preflight and postflight (§1 Bootstrap).
- All providers must honor GitOps-First and no-plaintext-secrets constraints (§2 Constraints).
- Provider-specific tuning belongs in `providers/claude.md`, `providers/gemini.md`, etc.

## Repository Instruction Model

- `AGENTS.md` is the shared gateway contract for agent-capable tools in this repository.
- Root `CLAUDE.md` and `GEMINI.md` are provider-specific shims, not replacements for shared governance policy.
- `.claude/CLAUDE.md` is the runtime baseline for local agent execution.
- Claude runtime behavior and editor/tool hook implementations belong under `.claude/**`; Codex event wiring belongs in `.codex/hooks.json` and must reuse the repo-local hook contract instead of defining a separate policy layer.
- Stop/SubagentStop lifecycle validation belongs to the repo-local hook contract; Codex mirror wiring remains context/validation wiring and is not a permission gate equivalent.
- `.claude/*.local.md` files are ignored local warning files. Hookify local rules may advise a local session, but shared enforcement belongs in tracked hooks, provider settings, Codex hook wiring, and validators.
- Durable policy and governance belong under `docs/00.agent-governance/**`.
- This repository does **not** use GitHub-native instruction files such as `.github/copilot-instructions.md` or `.github/instructions/**/*.instructions.md`.
- If GitHub tooling needs guidance, it must be routed through the existing gateway model instead of adding a parallel instruction hierarchy.
