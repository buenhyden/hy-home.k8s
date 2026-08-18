# Local Runtime Baseline (Codex)

## Purpose

Thin baseline for the tracked Codex-native `.codex/**` surface. Durable common
policy remains in Stage 00.

## Loading Order

Load root `AGENTS.md`, then follow the JIT sequence in
`docs/00.agent-governance/rules/bootstrap.md` with the Codex provider note and
the relevant scope.

## Provider Metadata

- Native role adapters: `.codex/agents/*.toml` with provider-owned model and
  reasoning-effort metadata.
- Context and validation wiring: `.codex/hooks.json`; it is not a Claude-style
  permission gate.
- Shared asset views: `.codex/{skills,workflows,output-styles}/` symlinks to
  `.agents/**`.

## Canonical References

- Common execution policy: `docs/00.agent-governance/rules/agentic.md`.
- Provider facts: `docs/00.agent-governance/providers/codex.md`.
- Role inventory and semantics: `docs/00.agent-governance/harness-catalog.md`
  and `docs/00.agent-governance/contracts/harness-contract.json`.
- Validation lanes and handoff: `docs/00.agent-governance/rules/quality-standards.md`.
- Shell guidance: `RTK.md`.

## Evidence Boundary

Tracked Codex adapters and hooks prove repository configuration only. They do
not prove native discovery, context delivery, authentication, model resolution,
sandbox or approval enforcement, or execution.
