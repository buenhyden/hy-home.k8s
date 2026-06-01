# Codex Provider Notes

Guidance for Codex (GPT) execution in the `hy-home.k8s` repository.

## Role

Codex sessions act as a peer provider to Claude and Gemini. This document defines how Codex interacts with the shared governance model while maintaining its own runtime baseline.

## Loading Model

- Start with the Codex/GPT gateway: `AGENTS.md`
- Follow the JIT loading sequence defined in `docs/00.agent-governance/rules/bootstrap.md`
- Load the local Codex runtime baseline: `.codex/CODEX.md`

## Context Strategy

- Codex uses `.codex/agents/*.toml` as provider-native mirrors for the local agent roster.
- Hook wiring is defined in `.codex/hooks.json`, which points to the repository's shared lifecycle hook implementations.
- `.codex/hooks.json` is strictly for event wiring (context and validation) and is **not** a permission gate.
- Shared skills, workflows, and output styles resolve through `.codex/{skills,workflows,output-styles}` symlinks to the `.agents/` SSoT. Codex-specific rules stay in this provider note and Stage 00 rules; `.codex/rules/` is only a placeholder/mirror surface unless populated by a future approved adapter change.

## Execution Expectations

- **Symmetry**: Codex is expected to follow the same 3-provider parity rules as Claude and Gemini.
- **GitOps-First**: Adhere strictly to the workspace constraints; never write plaintext secrets.
- **Language**: Produce human-facing responses in Korean, but keep governance and policy documents in English.

## Permission & Hook Boundary

Unlike Claude's `settings.json` which governs tool permissions natively, Codex relies on the shared `.codex/hooks.json` to bridge validation logic. The hooks orchestrate validation (e.g., `pre-validate`, `post-validate`) but the agent must autonomously honor the constraints defined in the governance docs.

## Runtime Tooling Boundary

Codex should follow `RTK.md` for shell command guidance. If `rtk` is not on
PATH but `/home/hy/.local/bin/rtk --version` works, record the PATH limitation.
If `rtk gain` cannot initialize its tracking database, do not inspect private
databases or credential files; run the underlying command directly and record
the limitation in the active task evidence.
