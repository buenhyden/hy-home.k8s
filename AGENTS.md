Read `.agents/workflows/work-lifecycle.md` before acting.
Read `RTK.md` before acting.

# AGENTS.md

## Scope

### Allowed Surface

This file states no separate allowed-surface rule; it is a provider gateway.

### Non-goals

This gateway adds no non-goal beyond the governance policies it loads; if work through it must be excluded, state it here.

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

This gateway is a thin provider gateway and adds no obligation beyond the reads above and below; if it needs one, state it here.

## Workflow

### Inspect and Change

Read each selected role and its required `.agents/skills/<id>/SKILL.md`
procedures explicitly before acting; explicit reads complement native discovery; invocation grants no authority.

### Handoff

This gateway hands off through the work lifecycle's Completion steps with no extra field; if it needs one, state it here.

## Verification

### Required Checks

This gateway runs no check of its own; the checks the invoking task selects under the quality policy apply. If it needs a required check, state it here.

### Evidence and Limits

Tracked projections are repository-static configuration, not native discovery
or runtime enforcement evidence.

## Safety

### Protected Actions

This gateway adds no protected action beyond the approval and safety policy; if work through it can start one, name it here.

### Stop and Escalate

This gateway adds no stop condition beyond the work lifecycle's stop rule and the approval and safety policy; if work through it needs its own, state it here.
