# Local Adapter Baseline (Antigravity / Gemini-Family)

## Purpose

Thin repository-static baseline for the local/Antigravity `.agents/**` surface.
It routes durable policy to Stage 00 and is not Gemini CLI native configuration.

## Loading Order

Load root `GEMINI.md`, then follow the JIT sequence in
`docs/00.agent-governance/rules/bootstrap.md` with the Gemini provider note and
the relevant scope.

## Provider Metadata

- Local role adapters: `.agents/agents/*.md`.
- Shared assets: `.agents/{skills,workflows,output-styles}/`.
- Behavioral wiring: `.agents/hooks.json`; it is neither Gemini CLI settings
  nor a Claude-style permission gate.

## Canonical References

- Common execution policy: `docs/00.agent-governance/rules/agentic.md`.
- Provider facts: `docs/00.agent-governance/providers/gemini.md`.
- Role inventory and semantics: `docs/00.agent-governance/harness-catalog.md`
  and `docs/00.agent-governance/contracts/harness-contract.json`.
- Validation lanes and handoff: `docs/00.agent-governance/rules/quality-standards.md`.
- Shared lifecycle hooks: `docs/00.agent-governance/hooks`.
- Shell guidance: `RTK.md`.

## Evidence Boundary

Tracked local adapters and hooks prove repository configuration only. They do
not prove Gemini CLI discovery, policy loading, event delivery, authentication,
model resolution, or execution.
