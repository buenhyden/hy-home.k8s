# Local Runtime Baseline (Codex)

## Purpose

Thin baseline for the tracked Codex-native surface. Shared policy and
responsibility remain in Stage 00.

## Loading Order

Load root `AGENTS.md`, then
`docs/00.agent-governance/skills/work-lifecycle.md`, the Codex provider note,
and the relevant responsibility and active Task.

## Provider Metadata

- Native role projections: `.codex/agents/*.toml`, with native model and
  reasoning-effort metadata.
- Native sandbox and approval controls belong to the running client.
- Shared skill view: `.codex/skills` points to `.agents/skills`.
- Run explicit repository validation; custom hook graphs are not a supported
  Codex execution or permission surface.

## Canonical References

- Common execution policy: `docs/00.agent-governance/policies/agent-execution.md`.
- Provider facts: `docs/00.agent-governance/providers/codex.md`.
- Role inventory and semantics: `.agents/registry.json` and `.agents/agents/`.
- Validation lanes and handoff: `docs/00.agent-governance/policies/quality.md`.
- Shell guidance: `RTK.md`.

## Evidence Boundary

Tracked projections prove repository configuration only, not native discovery,
authentication, model resolution, sandbox or approval enforcement, event
delivery, or execution.
