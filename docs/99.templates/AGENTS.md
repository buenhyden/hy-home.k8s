# AGENTS.md

Agent instructions for `docs/99.templates/`: the Document Profile Registry,
its contracts and the form catalog. The parent
[`docs/AGENTS.md`](../AGENTS.md) still applies.

## Scope

### Allowed Surface

Stage 99 is the machine contract every governed document is validated
against. `registry.json` declares each profile's path pattern, frontmatter,
sections, lifecycle and relationships; `contracts/` holds the JSON Schemas;
`templates/` holds the forms that authors copy.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change the registry, schemas or validators that read them | [repo-tooling-engineer](../../.agents/roles/repo-tooling-engineer.md) | `workspace-harness-audit`, `docs-stage-conformance` | `.claude/agents/repo-tooling-engineer.md` | `.codex/agents/repo-tooling-engineer.toml` |
| Governance and provider forms | [governance-steward](../../.agents/roles/governance-steward.md) | `workspace-harness-audit`, `knowledge-map` | `.claude/agents/governance-steward.md` | `.codex/agents/governance-steward.toml` |
| Document form text | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing`, `requirements-to-design` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Validate the contract change | [quality-engineer](../../.agents/roles/quality-engineer.md) | `k8s-validate`, `workspace-harness-audit` | `.claude/agents/quality-engineer.md` | `.codex/agents/quality-engineer.toml` |

### Non-goals

This file states no separate non-goals rule.

## Required Policies

### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

### Local Obligations

1. A change to `registry.json`, a schema or a form is a contract change, not
   an ordinary document edit. Scope it in a Spec, add the focused regression
   in `tests/`, and update the validators that consume it in the same change.
2. Every `template_source` must exist and every form must be referenced by a
   profile. Add or remove a form together with its profile.
3. Keep forms free of real values: placeholders stay placeholders and
   templates keep the `{{ARTIFACT_ID}}` placeholder.
4. A state or field removed from a profile must also leave the templates,
   schemas and the policy that described it.
5. `docs/98.archive/**` has no profile; do not add one.
6. Moving lines in `registry.json` can shift a baselined secret-scan finding.
   When it does, move the `.secrets.baseline` line number in its own commit
   first; the non-style gate scans against the HEAD baseline.

## Workflow

### Inspect and Change

Inspecting and changing files follows the rules under Local Obligations.

### Handoff

This file states no separate handoff rule.

## Verification

### Required Checks

`python3 scripts/validate-document-contract-registry.py --root . --mode strict`,
the strict Markdown-profile and lifecycle checks from the parent `AGENTS.md`,
and `python3 scripts/run-contract-tests.py --root . --suite document`.

### Evidence and Limits

This file states no separate evidence or limits rule.

## Safety

### Protected Actions

This file states no separate protected-action rule.

### Stop and Escalate

This file states no separate stop or escalation rule.
