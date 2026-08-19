# Local Runtime Baseline (Claude)

## Purpose

Thin baseline for the tracked Claude-native `.claude/**` surface. Durable
common policy remains in Stage 00.

## Loading Order

Load root `CLAUDE.md`, then follow the JIT sequence in
`docs/00.agent-governance/rules/bootstrap.md` with the Claude provider note and
the relevant scope.

## Provider Metadata

- Native role adapters: `.claude/agents/*.md` with provider-owned model and
  least-privilege tool metadata.
- Native permission and event wiring: `.claude/settings.json`.
- Shared asset views: `.claude/{skills,workflows,output-styles}/` symlinks to
  `.agents/**`.

## Canonical References

- Common execution policy: `docs/00.agent-governance/rules/agentic.md`.
- Provider facts: `docs/00.agent-governance/providers/claude.md`.
- Role inventory and semantics: `docs/00.agent-governance/harness-catalog.md`
  and `docs/00.agent-governance/contracts/harness-contract.json`.
- Validation lanes and handoff: `docs/00.agent-governance/rules/quality-standards.md`.
- Shared lifecycle hooks: `docs/00.agent-governance/hooks`.
- Shell guidance: `RTK.md`.

## Evidence Boundary

Tracked Claude adapters and settings prove repository configuration only. They
do not prove native discovery, hook delivery, authentication, model resolution,
permission enforcement, or execution.
