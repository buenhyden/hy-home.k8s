# AGENTS.md

Agent instructions for `tests/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Purpose

Independent behavior coverage and synthetic fixtures for the repository validators: mutations, bad input, timeouts, staged-index ambiguity, zero consumers and failure diagnostics. A PASS here is repository-static evidence only.

## Responsibilities and Projections

| Work in `tests/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Add or change regressions | [quality-engineer](../.agents/roles/quality-engineer.md) | `k8s-validate`, `workspace-harness-audit` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |
| Review test changes | [code-reviewer](../.agents/roles/code-reviewer.md) | `risk-report` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

## Rules

1. Every `tests/test_*.py` module belongs to exactly one suite in `scripts/run-contract-tests.py` or has its own registry command.
2. Build fixtures synthetically; do not read pinned historical commits or deleted documents.
3. Delete a test whose only subject is removed behavior; rewrite, do not weaken, a test of a current contract.
4. Tests never reach a live cluster, provider or credential.

## Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `python3 scripts/run-contract-tests.py --root . --suite <suite>`
- `ruff check tests`
