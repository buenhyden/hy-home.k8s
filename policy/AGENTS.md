# AGENTS.md

Agent instructions for `policy/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Purpose

Declarative Rego policy rules that Conftest evaluates against Kubernetes manifests. This folder owns the rules; `scripts/validation/registry.json` owns when they run. Conftest is required: without it `policy-gates` fails.

## Responsibilities and Projections

| Work in `policy/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Write or change a rule | [security-auditor](../.agents/roles/security-auditor.md) | `k8s-security-audit`, `vulnerability-patterns` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |
| Wire or test the gate | [quality-engineer](../.agents/roles/quality-engineer.md) | `k8s-validate` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

## Rules

1. Keep one implementation per rule; do not add a second engine or duplicate check in `scripts/`.
2. A new or tightened rule must pass on the current `gitops/` and `examples/` trees, or the same change fixes the manifests it rejects.
3. Do not weaken or skip a rule to make a change pass; record an exception through the owning policy document instead.

## Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `bash scripts/validate-policy-gates.sh .`
