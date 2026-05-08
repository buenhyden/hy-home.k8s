# Agentic Execution Rules

Rules for AI Agent-first Engineering quality and safety.

## Execution Contract

- Complete `rules/preflight-checklist.md` before substantial work.
- Plan from repository evidence first: docs, manifests, scripts, validators, and current diffs.
- Identify target layer, stage, persona, and scope before editing.
- Load the matching scope rules before taking action.
- Prefer the local harness roster in `harness-catalog.md` for agent and skill selection.
- Use the smallest set of rules and runtime files required for the task.
- Define validation evidence before editing and complete `rules/postflight-checklist.md` before completion.

## Agent-first Engineering Defaults

- Convert user intent into explicit success criteria, affected paths, validation commands, and known limitations.
- Keep implementation GitOps-first: repository change -> review -> ArgoCD reconciliation.
- Keep generated documents in the canonical docs taxonomy and route through `document-stage-routing.md`.
- Keep `.claude/agents/*.md` and `.codex/agents/*.toml` aligned whenever runtime contracts change.
- Report unavailable tools, skipped live checks, and CI-only validation honestly.

## Readiness Review Defaults

- Check `harness-catalog.md` before changing agent, skill, hook, or mirror contracts.
- Treat readiness as a matrix across gateways, runtime baseline, agents, mirrors, skills, hooks, validation scripts, memory, and escalation boundaries.
- Do not add new runtime surfaces until the existing readiness matrix shows a concrete gap.
- Keep direct `kubectl apply`, `kubectl patch`, external secret writes, and other live-cluster mutations outside the default Agent-first path.
- If a runbook requires live mutation for bootstrap or emergency recovery, mark it as human-approved bootstrap or break-glass work and record the expected evidence.

## Gateway and Runtime Audit Checklist

Before changing gateway, runtime, hook, mirror, or governance-memory files:

- Confirm root shims stay thin: `AGENTS.md`, root `CLAUDE.md`, and root `GEMINI.md` route to canonical governance/runtime files instead of embedding duplicate policy.
- Confirm tracked governance/runtime files under `docs/00.agent-governance/**`, `.claude/**`, and `.codex/**` remain English-only.
- Confirm no legacy source labels from prior external harness examples remain.
- Confirm `.claude/agents/*.md` and `.codex/agents/*.toml` mirror parity stays intact.
- Confirm provider-specific hook boundaries are described accurately: `.claude/settings.json` owns Claude permissions/hooks; `.codex/hooks.json` is a Codex context hook, not an equivalent permission gate.
- Confirm historical memory entries point to the current source of truth instead of presenting initial implementation snapshots as current inventory.

## Persona and Rule Enforcement

- Every non-trivial task must align to one persona in `rules/persona.md`.
- If work spans layers, process one layer at a time and declare transitions.
- If delegation is needed, use `subagent-protocol.md` and the local agent files instead of inline role definitions.

## Escalation and Safety

- Stop and ask for clarification when requirements conflict.
- Do not silently override explicit user constraints.
- Never perform direct cluster mutation, destructive Git actions, or external secret changes without explicit human approval.
- Record non-obvious lessons in `memory/` when recurrence risk exists.
