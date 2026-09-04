---
name: "knowledge-map"
description: "Use when auditing governance navigation, role/skill references, stage indexes, or current cross-links."
---

# knowledge-map

## Purpose

Find stale navigation and duplicate authority without turning an index into a
second policy or role roster.

## Workflow Steps

1. Read the relevant gateway, Stage 00 work lifecycle, and document-authoring
   policy; inspect current Git state and the task's authorized write boundary.
2. Resolve exact role and skill paths from `.agents/registry.json`; resolve
   document profiles and indexes from the Stage 99 registry.
3. Compare current indexes and links with their owners. Classify a finding as
   missing, stale, orphaned, generated drift, or historical-only.
4. Verify each finding against current source files and their canonical indexes.
   A generated graph snapshot is not a required input or an authority for
   current ownership.
5. When the user invokes graphify, read the installed skill before the requested
   pipeline; do not hardcode a user-local installation or run an external
   pipeline implicitly. Refresh generated output only through its authorized
   generator and record tool limitations.
6. Run the relevant link/owner, registry, Markdown, or generated-index checks.
7. Report exact source, target, finding, and minimal repair. Make changes only
   when authorized; preserve sealed or completed evidence and route historical
   path disposition to the approved migration owner.

## Outputs

A bounded gap list with current owners, verification results, limitations, and
next owner in the active Task. Do not append a separate progress ledger or
recreate machine roster tables.

## Related Owners

- `docs/00.agent-governance/policies/document-authoring.md`
- `docs/00.agent-governance/policies/context-and-memory.md`
- `docs/00.agent-governance/policies/quality.md`
