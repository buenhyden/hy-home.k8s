# AGENTS.md

Agent instructions for `infrastructure/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Scope

### Allowed Surface

Bootstrap assets for the local platform: the Linux server, Docker Engine and k3d cluster definition, external service contracts, Argo CD install values, MetalLB manifests and the `bootstrap-local.sh` entrypoint. Steady-state changes go through `gitops/`, not here.

| Work in `infrastructure/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change bootstrap assets | [k8s-implementer](../.agents/roles/k8s-implementer.md) | `deployment-strategies`, `k8s-validate`, `external-service-contract-audit` | `.claude/agents/k8s-implementer.md` | `.codex/agents/k8s-implementer.toml` |
| Review network and ingress addressing | [network-reviewer](../.agents/roles/network-reviewer.md) | `risk-report` | `.claude/agents/network-reviewer.md` | `.codex/agents/network-reviewer.toml` |
| Review bootstrap secret handling | [security-auditor](../.agents/roles/security-auditor.md) | `k8s-security-audit` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

### Non-goals

Non-goals are stated in rule 2 under Local Obligations.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Do not run bootstrap scripts, `k3d`, `helm` or `kubectl` against a live host or cluster without explicit operator approval; bootstrap is an operator action.
2. Do not move steady-state platform configuration here; it belongs in `gitops/`.
3. Keep MetalLB pools, ingress addresses and external endpoints consistent with `gitops/platform/external-services/` and REQ-0004.
4. Never commit kubeconfigs, tokens, certificates or secret values.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This file states no separate handoff rule.

## Verification

### Required Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `bash scripts/validate-infrastructure-contracts.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `python3 scripts/run-contract-tests.py --root . --suite cluster-gate`

### Evidence and Limits

This file states no separate evidence or limits rule.

## Safety

### Protected Actions

Protected actions are stated in rules 1 and 4 under Local Obligations.

### Stop and Escalate

Stop and escalation conditions are stated in rule 1 under Local Obligations.
