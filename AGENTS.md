Read `.agents/workflows/work-lifecycle.md` before acting.
Read `RTK.md` before acting.

# AGENTS.md

## Scope

### Allowed Surface

This file states no separate allowed-surface rule; it is a provider gateway.

### Non-goals

This file states no separate non-goals rule.

## Required Policies

### Canonical Sources

Thin GPT/Codex provider gateway for `hy-home.k8s`. The common core comes
first; the Codex-only reads follow in their own block.

- Shared execution policy: `.agents/governance/agent-execution.md`
- Role and skill authority: `.agents/roles/registry.json`
- Responsibilities: `.agents/roles/README.md`
- Validation and handoff: `.agents/governance/quality.md`
- Document authoring: `docs/99.templates/README.md`

Codex-only provider reads:

Read `.codex/provider.md` before acting.
Read `.codex/CODEX.md` before acting.

### Local Obligations

This file states no separate local obligations beyond the reads above and below.

## Workflow

### Inspect and Change

Read each selected role and its required `.agents/skills/<id>/SKILL.md`
procedures explicitly before acting; explicit reads complement native discovery; invocation grants no authority.

### Handoff

This file states no separate handoff rule.

## Verification

### Required Checks

This file states no separate required checks.

### Evidence and Limits

Tracked projections are repository-static configuration, not native discovery
or runtime enforcement evidence.

## Safety

### Protected Actions

This file states no separate protected-action rule.

### Stop and Escalate

This file states no separate stop or escalation rule.
