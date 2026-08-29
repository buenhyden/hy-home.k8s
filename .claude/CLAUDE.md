# Local Runtime Baseline (Claude)

## Purpose

Thin baseline for the tracked Claude-native surface. Shared policy and
responsibility remain in Stage 00.

## Loading Order

Load root `CLAUDE.md`, then
`docs/00.agent-governance/skills/work-lifecycle.md`, the Claude provider note,
and the relevant responsibility and active Task.

## Provider Metadata

- Native role projections: `.claude/agents/*.md`, with native model and
  least-privilege tool metadata.
- Native permission and event declarations: `.claude/settings.json`.
- Shared skill view: `.claude/skills` points to `.agents/skills`.

## Canonical References

- Common execution policy: `docs/00.agent-governance/policies/agent-execution.md`.
- Provider facts: `docs/00.agent-governance/providers/claude.md`.
- Role inventory and semantics: `.agents/registry.json` and `.agents/agents/`.
- Validation lanes and handoff: `docs/00.agent-governance/policies/quality.md`.
- Shell guidance: `RTK.md`.

## Evidence Boundary

Tracked projections and settings prove repository configuration only, not
native discovery, hook delivery, authentication, model resolution, permission
enforcement, or execution.
