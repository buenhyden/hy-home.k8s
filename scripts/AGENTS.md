# AGENTS.md

Agent instructions for `scripts/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Scope

### Allowed Surface

Executable repository-static validation for documents, agent governance, GitOps, CI and security boundaries, plus release and QA entrypoints. `validation/registry.json` is the single owner of check selection and command mapping; each validator owns its diagnostics.

| Work in `scripts/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change a registered validator or the QA runner | [quality-engineer](../.agents/roles/quality-engineer.md) | `k8s-validate`, `workspace-harness-audit` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |
| Change tooling that is not a registered gate | [repo-tooling-engineer](../.agents/roles/repo-tooling-engineer.md) | `workspace-harness-audit`, `docs-stage-conformance` | `.claude/agents/repo-tooling-engineer.md` | `.codex/agents/repo-tooling-engineer.toml` |
| Review a change | [code-reviewer](../.agents/roles/code-reviewer.md) | `risk-report` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

### Non-goals

This folder adds no non-goal beyond the parent `AGENTS.md` and the governance policies; if work here must be excluded, state it here.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Register every new gate in `validation/registry.json` with its surface, lanes and fallback, and add its regression module to a suite in `run-contract-tests.py`.
2. Make the smallest change, show a failing case for changed behavior and then the passing result, and never weaken a gate or a test to finish.
3. Keep no compatibility branch for an older format, generation or pinned historical commit, and no check of a finished one-time transition; delete them with their tests.
4. Bound every subprocess, file read and output; keep the existing bounded helpers.
5. Run `graphify update .` after changing code when the knowledge graph is in use.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This folder hands off through the work lifecycle's Completion steps with no extra field; if it needs one, state it here.

## Verification

### Required Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `python3 scripts/validate-affected-surfaces.py --root .`
- `ruff check scripts tests`
- `python3 scripts/run-contract-tests.py --root . --suite <suite>`

### Evidence and Limits

This folder adds no evidence rule beyond the quality policy's handoff contract; if a check here has a limit to report, state it here.

## Safety

### Protected Actions

This folder adds no protected action beyond the approval and safety policy; if work here can start one, name it here.

### Stop and Escalate

Stop and escalation conditions are stated in rule 2 under Local Obligations.
