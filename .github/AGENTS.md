# AGENTS.md

Agent instructions for `.github/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Scope

### Allowed Surface

GitHub automation: the `ci.yml` branch metadata, PR title, commit and changed-file style checks, greetings and labeler workflows, pinned CI requirements, rulesets and repository templates. Repository QA runs locally; hosted checks never certify it.

| Work in `.github/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change workflows, actions or rulesets | [ci-workflow-engineer](../.agents/roles/ci-workflow-engineer.md) | `risk-report` | `.claude/agents/ci-workflow-engineer.md` | `.codex/agents/ci-workflow-engineer.toml` |
| Review workflow permissions and supply chain | [security-auditor](../.agents/roles/security-auditor.md) | `vulnerability-patterns` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

### Non-goals

Non-goals are stated in rule 7 under Local Obligations.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. Give `GITHUB_TOKEN` least privilege: `contents: read` at workflow level, and only the job-level permission a step needs.
2. Pin every Action to a full commit SHA, and use only Actions registered in the allowlist recorded in `.github/rulesets/main-protection.md`. To add one, ask the operator to register its pattern in the remote setting before the pull request runs, and list it in `main-protection.md` in the same change.
3. Leave no credential behind: keep `persist-credentials: false` and never write a token to disk or to an artifact.
4. Never print a secret or token to the log, and mask any derived sensitive value.
5. Treat PR titles, bodies, branch names and commit messages as untrusted input: pass them through `env:` and quote them; never interpolate `${{ }}` expressions into `run:` scripts.
6. A `pull_request_target` or other privileged workflow must never check out, build or run the candidate's code; it may read the diff only as data.
7. Do not add hosted full QA, deployment or publication jobs; local QA and `scripts/release.py` own those.
8. Change `requirements/ci-validation.txt` only with hashes and run the CI Python contract.
9. Do not change remote settings, rulesets or secrets; document the intended state for the operator.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This file states no separate handoff rule.

## Verification

### Required Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `python3 scripts/validate-github-actions-security.py --root .`
- `python3 scripts/validate-ci-python-contract.py --root .`
- `python3 scripts/run-contract-tests.py --root . --suite ci-metadata`

### Evidence and Limits

Evidence limits are stated at the end of the Allowed Surface text: hosted checks never certify repository QA.

## Safety

### Protected Actions

Protected actions are stated in rules 3, 4, 6 and 9 under Local Obligations.

### Stop and Escalate

Stop and escalation conditions are stated in rules 2 and 9 under Local Obligations.
