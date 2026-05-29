# Codex Provider Notes

Guidance for Codex (GPT) execution in the `hy-home.k8s` repository.

## Role

Codex sessions act as a peer provider to Claude and Gemini. This document defines how Codex interacts with the shared governance model while maintaining its own runtime baseline.

## Loading Model

- Start with the shared gateway: `AGENTS.md`
- Follow the JIT loading sequence defined in `docs/00.agent-governance/rules/bootstrap.md`
- Load the local Codex runtime baseline: `.codex/CODEX.md`

## Context Strategy

- Codex uses `.codex/agents/*.toml` as mirrors for the primary agent definitions.
- Hook wiring is defined in `.codex/hooks.json`, which points to the repository's shared lifecycle hook implementations.
- `.codex/hooks.json` is strictly for event wiring (context and validation) and is **not** a permission gate.

## Execution Expectations

- **Symmetry**: Codex is expected to follow the same 3-provider parity rules as Claude and Gemini.
- **GitOps-First**: Adhere strictly to the workspace constraints; never write plaintext secrets.
- **Language**: Produce human-facing responses in Korean, but keep governance and policy documents in English.

## Permission & Hook Boundary

Unlike Claude's `settings.json` which governs tool permissions natively, Codex relies on the shared `.codex/hooks.json` to bridge validation logic. The hooks orchestrate validation (e.g., `pre-validate`, `post-validate`) but the agent must autonomously honor the constraints defined in the governance docs.
