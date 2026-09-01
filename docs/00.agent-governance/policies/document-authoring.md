---
title: 'Document Authoring Policy'
version: "1.0"
type: governance/reference
layer: "00.agent-governance"
status: active
owner: platform
updated: 2026-08-28
---

# Document Authoring Policy

## Overview

Select the document owner by purpose, author from its canonical template, and
close the change with traceable evidence.

## Authority Boundary

[Stage 99 README](../../99.templates/README.md) is the human authoring guide.
Its [registry](../../99.templates/registry.json) alone owns exact paths,
profiles, IDs, sections, metadata, lifecycle, and relationships. This policy
owns agent procedure, not a second machine contract.

## Governance Context

Use [SDLC flow](../sdlc.md) to distinguish durable requirements, current
architecture, change-specific behavior, and operating knowledge. Stage numbers
express ownership, not a one-way waterfall. Root `DESIGN.md` owns UI and
design-system rules only.

## Current Contract

1. Identify the owning stage and normalize the final repository-relative path.
2. Resolve exactly one registry profile and read its canonical template before
   creating or restructuring a document. No match or multiple matches is a
   stop condition.
3. Use the profile-owned initial status, metadata, sections, and relationships.
   Do not assume every profile starts at `draft`; router READMEs have no
   lifecycle or artifact ID.
4. Replace prompts with concrete content, use complete stable IDs for
   traceability, and calculate links from the final target path.
5. Keep a Requirement Package solution-independent. Put executable interface
   contracts and change-scoped Technical Approach and Acceptance Contract in
   the owning Spec package; put order, risks, verification, and rollback in its
   Plan and execution evidence in its Task records.
6. Promote durable cross-change decisions to an ADR and current system views
   to an Architecture Description. Do not create parallel design, test,
   release, or progress authority.
7. Review the owning README after content or path changes and update stale
   navigation in the same logical change.
8. Preserve accepted decisions and completed evidence. Use successors,
   reciprocal lifecycle relationships, and minimal Git-backed recovery
   mappings rather than rewriting history or leaving redirects.
9. Run the checks selected by the affected paths and record evidence in the
   owning Task using [quality policy](quality.md).

Governance and agent execution sections remain English. Human-facing root,
folder, requirement, operations, and reference explanation may use Korean;
source, authority, and machine-contract sections remain English-first. Never
hand-edit generated current output or create an off-taxonomy authored tree.

## Validation and Refresh

Run strict registry, Markdown-profile, link/owner, and lifecycle checks when
their contracts are affected. A deletion or consolidation requires replacement
coverage, consumer disposition, and applicable Archive recovery evidence in
the same logical change.

## Related Documents

- [Document Lifecycle](document-lifecycle.md)
- [Stage 99 Author Guide](../../99.templates/README.md)
- [Work Lifecycle](../skills/work-lifecycle.md)
- [Archive Index](../../98.archive/README.md)
