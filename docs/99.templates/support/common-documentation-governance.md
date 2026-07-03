---
title: 'Common Documentation Template Governance'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-03
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

## Common Template Family

| Role | Target Pattern | Template Path |
| --- | --- | --- |
| README or folder index | `README.md`, `**/README.md`, `.claude/README.md`, `.codex/README.md` | `../templates/common/readme.template.md` |
| Durable reference | `docs/90.references/<category>/<topic>.md` | `../templates/common/reference.template.md` |
| Archive Tombstone | `docs/98.archive/**/*.md` | `../templates/common/archive-tombstone.template.md` |
| Governance memory | `docs/00.agent-governance/memory/<topic>.md` | `../templates/common/memory.template.md` |
| Progress ledger entry | `docs/00.agent-governance/memory/progress.md` | `../templates/common/progress.template.md` |

## README Governance

- README files are frontmatter-free entrypoints unless a future renderer
  requires otherwise.
- README files must keep `Overview`, `Audience`, `Scope`, `Structure`,
  `How to Work in This Area`, `Link Basis`, and `Related Documents`.
- README files may summarize contracts, but detailed contract bodies belong in
  support docs, Stage 00 governance, or the owning stage document.
- README files must not keep deprecated related-document headings.

## GitHub-Native Control Markdown Governance

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

## Reference Governance

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

## Archive Governance

- Archive Tombstones are metadata-only.
- Active docs link to archive content through the archive index, not directly
  to individual Tombstones.
- Tombstones preserve original path, archived date, reason, replacement, and
  evidence. They must not preserve the old full body.

## Memory and Progress Governance

- Standalone memory files under `docs/00.agent-governance/memory/` use the
  memory template and require a related progress ledger entry in the same
  change.
- The memory `<topic>` route excludes `progress`; `progress.md` is reserved
  for the canonical append-only progress ledger.
- The canonical progress ledger is
  `docs/00.agent-governance/memory/progress.md`.
- `progress.template.md` defines appendable entries, not a whole-document
  frontmatter schema.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Legacy Cleanup Rules](./legacy-cleanup-rules.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Archive Index](../../98.archive/README.md)
