---
title: 'Common Documentation Template Governance'
type: template-support
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
- README files must not keep legacy `Related References` headings.

## Reference Governance

- Reference documents own durable lookup facts, source boundaries, freshness
  rules, and stable external-standard snapshots.
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
