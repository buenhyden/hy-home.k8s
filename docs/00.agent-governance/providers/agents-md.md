---
title: 'Reference: AGENTS.md Provider Notes'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# AGENTS.md Provider Notes

## Overview

Guidance for consuming the `AGENTS.md` Codex/GPT gateway contract.

### Role

`AGENTS.md` is the thin gateway contract for Codex/GPT sessions in this repository.
Claude and Gemini use their root provider shims (`CLAUDE.md`, `GEMINI.md`) and must not import `AGENTS.md`.
`AGENTS.md` defines bootstrap and routing pointers for Codex/GPT; it does not duplicate policy text from `rules/`, `scopes/`, or provider files.

## Authority Boundary

### Gateway Integrity Rules

- Never add policy text to `AGENTS.md` directly; add it to the appropriate `rules/` or `scopes/` file and add a pointer in `AGENTS.md`.
- Routing pointers must stay in sync with `docs/00.agent-governance/harness-catalog.md`, `subagent-protocol.md`, and rule documents.
- Runtime roster details belong in `docs/00.agent-governance/harness-catalog.md`, not in `AGENTS.md`.
- `.codex/agents/*.toml` role-adapter status belongs in `harness-catalog.md` and `subagent-protocol.md`, not in a root catalog table.

### Cross-Provider Consistency

- Codex/GPT sessions must produce Korean user responses through the Codex gateway contract.
- Codex/GPT sessions must run preflight and postflight through the shared JIT sequence.
- Codex/GPT sessions must honor GitOps-First and no-plaintext-secrets constraints.
- Provider-specific tuning belongs in `providers/claude.md`, `providers/gemini.md`, etc.

## Governance Context

### Loading Model

- Codex/GPT sessions load `AGENTS.md` as the first context anchor.
- Follow §1 Bootstrap to resolve the full JIT sequence.
- Do not cache or skip any step in the JIT sequence between sessions.

## Current Contract

### Codex Provider Resolution

Codex provider policies have been separated into `docs/00.agent-governance/providers/codex.md` to maintain 3-provider symmetry.
Codex sessions consume the `AGENTS.md` gateway and the local `.codex/CODEX.md` baseline.

### Repository Instruction Model

- `AGENTS.md` is the Codex/GPT gateway contract for this repository.
- Root `CLAUDE.md` and `GEMINI.md` are provider-specific shims, not replacements for shared governance policy.
- `.claude/CLAUDE.md` is the runtime baseline for local agent execution.
- Claude runtime behavior and editor/tool hook implementations belong under `.claude/**`; Codex event wiring belongs in `.codex/hooks.json` and Gemini event wiring belongs in `.agents/hooks.json`. Both hook JSON files must reuse the repo-local hook contract instead of defining separate policy layers.
- Stop/SubagentStop lifecycle validation belongs to the repo-local hook contract; Codex and Gemini hook JSON wiring remains context/validation wiring and is not a permission gate equivalent.
- `.claude/*.local.md` files are ignored local warning files. Hookify local rules may advise a local session, but shared enforcement belongs in tracked Claude settings, shared hook scripts, repository validators, and provider hook JSON only as context/validation wiring.
- Durable policy and governance belong under `docs/00.agent-governance/**`.
- This repository does **not** use GitHub-native instruction files such as `.github/copilot-instructions.md` or `.github/instructions/**/*.instructions.md`.
- If GitHub tooling needs guidance, it must be routed through the existing gateway model instead of adding a parallel instruction hierarchy.

### QA Evidence Resolution

- `AGENTS.md` points to, but does not restate, the validation lane, result, and
  handoff contract in [`rules/quality-standards.md`](../rules/quality-standards.md).
- A tracked `AGENTS.md`, `.codex/agents/*.toml`, or `.codex/hooks.json` proves
  repository configuration only. Codex discovery, context loading, delegated
  role use, and event delivery require separate native-runtime evidence.
- The affected-surface and agent-role semantic validators provide repo-static
  selection and content evidence; provider-native model, effort, sandbox, and
  approval semantics remain with Codex-owned surfaces.

## Validation and Refresh

Run the role-semantic validator, roster-currentness validator, and repository
quality gate after changing the gateway or a Codex adapter:

```bash
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
bash scripts/validate-repo-quality-gates.sh .
```

Review this note when `AGENTS.md`, `.codex/CODEX.md`, Codex role adapters, or
the shared JIT sequence changes. These commands prove repository configuration,
not native Codex discovery or instruction loading.

## Related Documents

- [Bootstrap Governance](../rules/bootstrap.md)
- [Codex Provider Notes](codex.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Subagent Protocol](../subagent-protocol.md)
