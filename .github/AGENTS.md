# AGENTS.md

Agent instructions for `.github/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Purpose

GitHub automation: the `ci.yml` branch metadata, PR title, commit and changed-file style checks, greetings and labeler workflows, pinned CI requirements, rulesets and repository templates. Repository QA runs locally; hosted checks never certify it.

## Responsibilities and Projections

| Work in `.github/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change workflows, actions or rulesets | [ci-workflow-engineer](../.agents/roles/ci-workflow-engineer.md) | `risk-report` | `.claude/agents/ci-workflow-engineer.md` | `.codex/agents/ci-workflow-engineer.toml` |
| Review workflow permissions and supply chain | [security-auditor](../.agents/roles/security-auditor.md) | `vulnerability-patterns` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

## Rules

1. Keep workflow permissions least-privilege, pin every action to a full commit SHA, and keep `persist-credentials: false`.
2. Do not add hosted full QA, deployment or publication jobs; local QA and `scripts/release.py` own those.
3. Change `requirements/ci-validation.txt` only with hashes and run the CI Python contract.
4. Do not change remote settings, rulesets or secrets; document the intended state for the operator.

## Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `python3 scripts/validate-github-actions-security.py --root .`
- `python3 scripts/validate-ci-python-contract.py --root .`
- `python3 scripts/run-contract-tests.py --root . --suite ci-metadata`
