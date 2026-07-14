---
title: 'Common Documentation Template Governance'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-13
---

# Common Documentation Template Governance

## Overview

This document defines the governance contract for common documentation
templates. Common templates are not tied to a single SDLC stage. They support
repository navigation, durable reference material, archive Tombstones, and
agent memory or progress records.

## Purpose

Common documentation templates keep repository entrypoints and durable
knowledge consistent without forcing every common document into an SDLC phase.

## Owned Contract

### Common Profile Handoff

The [Document Profile Registry](./document-profiles.json) owns the exact routes,
forms, headings, and metadata contracts for `readme/*`, `content/reference`,
`content/archive-tombstone`, `governance/memory`,
`governance/progress-ledger`, and `governance/progress-entry`. This document
owns the human rationale for navigation, reference, preservation, and durable
agent-learning roles without becoming another profile table.

The [Document Type Format and Evidence
Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
records the external and local evidence behind these role decisions.

## Authoring Rules

### README Governance

- README files are frontmatter-free entrypoints unless a future renderer
  requires otherwise.
- Every README path resolves to one `readme/*` registry profile and must keep
  that profile's required H2 headings without adding unsupported H2 headings.
- README files may summarize active control boundaries through matrices and
  links, but detailed rules belong to support, governance, operations, or
  validator owners.
- README files must not keep deprecated related-document headings.
- README files under `examples/aws/docs/**` and `examples/azure/docs/**`
  remain frontmatter-free indexes even though non-README Markdown siblings are
  routed as example-local SDLC snapshot documents.

### GitHub-Native Control Markdown Governance

`.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
`.github/SECURITY.md` are active repository control surfaces, but they are not
structural stage documents and must not receive YAML frontmatter. GitHub reads
or renders these files directly, so metadata belongs in their body structure
or in canonical owners such as Stage 00 governance, `.github/workflows/**`,
and Stage 05 CI/QA guidance.

These files may summarize current workflow, security, or PR expectations, but
they must link to canonical policy owners instead of defining a parallel
template contract.

Official basis:

- [GitHub pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository) documents `.github` as a supported PR template location.
- [GitHub security policy](https://docs.github.com/code-security/getting-started/adding-a-security-policy-to-your-repository) documents `SECURITY.md` as the repository security reporting surface.

### Reference Governance

- Reference documents own durable lookup facts, source boundaries, freshness
  rules, and stable external-standard snapshots.
- Reference type values may be combined with `/` when a document deliberately
  spans compatible reference roles such as `durable-concept`,
  `external-standard-snapshot`, `data-catalog`, `source-ledger`,
  `learning-roadmap`, `faq`, and `dated-implementation-audit`.
- Reference documents must not duplicate active requirements, decisions,
  specs, plans, tasks, policies, or runbooks.
- `reference.template.md` must not contain archive policy wording. Archive
  policy belongs to archive governance and Tombstone templates.

### Archive Governance

- Archive Tombstones are metadata-only.
- Active docs link to archive content through the archive index, not directly
  to individual Tombstones.
- Tombstones preserve original path, archived date, reason, replacement, and
  evidence. They must not preserve the old full body.
- Tombstones and archive index rows are historical evidence, not current
  operating guidance; the current replacement owns active requirements,
  implementation contracts, and procedures.

### Memory and Progress Governance

- Standalone memory files under `docs/00.agent-governance/memory/` use the
  memory template and require a related progress ledger entry in the same
  change.
- The memory `<topic>` route excludes `progress`; `progress.md` is reserved
  for the canonical append-only progress ledger.
- The canonical progress ledger is
  `docs/00.agent-governance/memory/progress.md`.
- `progress.template.md` defines appendable entries, not a whole-document
  frontmatter schema.

## Validation Contract

Changes to common-documentation routes, headings, or forms must keep the
machine registry, template forms, README handoff inventory, and authored
documents synchronized. Validate both the focused profile contract and the
repository consumers:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
```

The selected registry profile owns each common document's exact relationship
heading. A route or heading change is incomplete until its profile, canonical
form, focused fixtures, and every current consumer agree. Repository-static
PASS does not establish generated-output freshness or live provider state;
record those boundaries separately when they apply.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Document Profile Registry](./document-profiles.json)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Legacy Cleanup Rules](./legacy-cleanup-rules.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Archive Index](../../98.archive/README.md)
