---
title: 'Reference: Claude Provider Notes'
type: governance/reference
status: active
owner: platform
updated: 2026-07-28
---

# Claude Provider Notes

## Overview

Claude-specific guidance for `hy-home.k8s`.

## Authority Boundary

### Native Boundary

- `.claude/settings.json` owns Claude native permissions and hook wiring.
- `.claude/agents/*.md` owns Claude subagent metadata, including `name`,
  `description`, `model`, and least-privilege `tools:`.
- Claude hooks may block objective repo-state failures when wired through
  settings; they do not prove live runtime readiness.
- Claude native tools and permissions must not weaken the repository's
  GitOps-first, no-live-mutation, and secret-handling boundaries.

## Governance Context

### Official Source Basis

Cutoff-sensitive capability evidence was reconciled against
`2026-07-10 10:00 Asia/Seoul` on 2026-07-28:

- Claude Code changelog: <https://code.claude.com/docs/en/changelog>
- Claude Code settings: <https://code.claude.com/docs/en/settings>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>

The dated changelog supports Claude Code `2.1.206` by the cutoff and records
Opus 4.8 plus `/effort xhigh` in `2.1.154`. Current documentation is
observation-time evidence for current syntax; it does not backdate every
subagent field. A read-only `claude --version` observation on 2026-07-28
returned `2.1.220 (Claude Code)`. Installation and version evidence do not prove project
agent discovery, authentication, account entitlement, configured-model
resolution, hooks, or delegated execution.

### Loading Model

- Keep root `CLAUDE.md` thin; it imports `@docs/00.agent-governance/rules/bootstrap.md` (shared governance), `@docs/00.agent-governance/providers/claude.md`, `@.claude/CLAUDE.md`, and `@RTK.md`. It must not import `@AGENTS.md`, which is the GPT/Codex provider shim.
- Root `CLAUDE.md` must load the existing hierarchy; it must not copy RTK, graphify, catalog, or governance policy blocks inline.
- Use `.claude/CLAUDE.md` as the local runtime baseline for agent roster and model hierarchy.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Use `@RTK.md` for shell-command guidance when Claude needs that context.
- Keep provider-specific details here; do not duplicate global rules.
- Keep Claude-specific runtime wiring under `.claude/**`; do not create a parallel `.github/**` instruction layer for this repository.

### Context Strategy

- Prefer concise CLAUDE context files (target under 200 lines per file).
- For larger projects, split rules into `.claude/rules/` files.
- Use path-scoped rules where applicable to reduce always-loaded context.
- Keep conflicting instructions out of CLAUDE hierarchy.
- Avoid introducing provider-specific guidance outside the existing `CLAUDE.md` + `.claude/**` + `docs/00.agent-governance/**` hierarchy.

### Memory and Context

- Follow CLAUDE hierarchy: managed policy -> project -> user -> path-specific rules.
- Use imports for modular instructions when needed.
- Treat auto memory as `provider-local-auxiliary`: advisory only, never the
  owner of repository facts, decisions, task status, or durable handoff
  evidence. Re-observe a claim from the repository before review-promoting it.
- Use `memory/progress.md` for `durable-long-term` shared progress and the
  owning Spec/Runbook/Incident/Postmortem for `domain-scoped` knowledge.
  Ignored `.agent-work/checkpoint.json` content is `working-short-term` only.
- Repo-static loop and checkpoint validators enforce atomic/redacted synthetic
  checkpoint shape, repository-wins resume,
  promotion/refresh/expiry/archive-GC/conflict, compaction, handoff, and five
  bounded reviewed feedback destinations across all four memory classes. They
  neither read nor write ignored checkpoints and do not prove Claude discovery,
  hooks, permissions, model resolution, authenticated execution, hosted CI,
  remote, credential-bearing, live, or actual checkpoint execution.

## Current Contract

### Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- Keep responses to users in Korean.
- Keep governance control docs in English.
- Use `contracts/harness-contract.json` as the machine roster owner and
  `harness-catalog.md` as its readable runtime view.
- Use `docs/00.agent-governance/hooks/lifecycle-guard.sh` as the shared lifecycle hook contract wired by `.claude/settings.json`: Stop/SubagentStop may block objective repo-state failures; PreCompact is advisory and must not replace validation evidence.
- Keep `.claude/*.local.md`, including Hookify rules, as ignored local warning files only. Shared Claude enforcement stays in `.claude/settings.json`, `docs/00.agent-governance/hooks/*.sh`, and repository validators.

### QA Evidence Resolution

- `contracts/harness-contract.json` version `1.0.0` is the provider-neutral
  machine owner. Its current `12 roles / 4 surfaces / 48 adapters` inventory is
  repository-static adapter evidence.
- Keep `repo-static`, `provider-runtime`, `ci`, and `remote-live` evidence
  separate. A result in one class never proves another.
- The legacy role-semantics contract is readable compatibility input with zero
  semantic consumers until Spec 045 and is not current authority.
- Resolve `affected`, `staged`, `all-files`, `message/manual`, `ci`, and
  `remote/live` semantics plus handoff fields from
  [`rules/quality-standards.md`](../rules/quality-standards.md).
- Tracked `.claude/agents/*.md`, `.claude/settings.json`, and shared hook wiring
  are repo-static evidence. They do not prove native Claude discovery, hook
  delivery, delegated role use, permission enforcement, or remote execution.
- Preserve Claude-native `model` and least-privilege `tools:` validation while
  `contracts/harness-contract.json` owns shared role semantics.

## Validation and Refresh

Run the harness, shared role-semantic, roster, and repository quality checks
after changing Claude settings, hooks, or agent adapters:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-config.py --root .
python3 scripts/validate-agent-provider-canaries.py --root .
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
bash scripts/validate-repo-quality-gates.sh .
```

Refresh this note when Claude's tracked settings, native agent schema, or root
shim changes. Native hook delivery, permission enforcement, and delegated-agent
use require separate Claude runtime evidence.

## Related Documents

- [Bootstrap Governance](../rules/bootstrap.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Subagent Protocol](../subagent-protocol.md)
- [Quality Standards](../rules/quality-standards.md)
