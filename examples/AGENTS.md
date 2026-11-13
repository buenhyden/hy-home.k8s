# AGENTS.md

Agent instructions for `examples/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Scope

### Allowed Surface

Reference-only examples for designing a new app or cloud target: `sample-app/` is the minimal local GitOps onboarding template, and `aws/` and `azure/` are cloud reference implementations. `gitops/` is the active desired state; nothing here is reconciled or deployed.

| Work in `examples/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change an example | [k8s-implementer](../.agents/roles/k8s-implementer.md) | `deployment-strategies`, `gitops-workflow`, `k8s-validate` | `.claude/agents/k8s-implementer.md` | `.codex/agents/k8s-implementer.toml` |
| Review an example | [gitops-reviewer](../.agents/roles/gitops-reviewer.md) | `gitops-workflow`, `k8s-validate` | `.claude/agents/gitops-reviewer.md` | `.codex/agents/gitops-reviewer.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

### Non-goals

Non-goals are stated in the opening text of Allowed Surface: nothing here is reconciled or deployed.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Never change an account or a live cluster from an example.
2. Promote an example into `gitops/` only through an owned change with its own Spec.
3. Never commit credentials, kubeconfigs or deployment outputs.
4. Read a deeper `AGENTS.md` (for example `azure/AGENTS.md`) before working there.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This folder hands off through the work lifecycle's Completion steps with no extra field; if it needs one, state it here.

## Verification

### Required Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/validate-policy-gates.sh .`

### Evidence and Limits

This folder adds no evidence rule beyond the quality policy's handoff contract; if a check here has a limit to report, state it here.

## Safety

### Protected Actions

Protected actions are stated in rules 1 and 3 under Local Obligations.

### Stop and Escalate

This folder adds no stop condition beyond the work lifecycle's stop rule and the approval and safety policy; if work here needs its own, state it here.
