---
title: "Common Knowledge"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-07"
---
# Common Knowledge

## Overview

This surface answers orientation questions: which tree owns what, and which
document a reader opens first for a given domain. It holds pointers only. Every
statement of policy, design, procedure or current state stays with the owner a
row names.

## Scope

A knowledge document names an owner path, the entry path a reader opens first,
and the condition under which the row stays valid. It reproduces no span of the
text it points at, it is written by hand, and no generator writes to it. The
retired generated index is not recreated here; the non-duplication rule and its
validator are what keep this surface a map rather than a second authority.

Out of scope: approval boundaries, permissions, role rosters, gate commands,
lifecycle states and evidence classes. Those keep their existing owners, and a
row that would restate one is a defect rather than a convenience.

## Item Index

- [Project Map](project-map.md): which top-level tree owns what, with the entry
  document for each.
- [Domain Index](domains.md): per operating domain, the canonical owner, the
  entry path, and the condition that keeps the row valid.

## Add and Find

1. Read [document authoring](../governance/document-authoring.md) and select
   the knowledge profile from the Stage 99 registry before adding a document.
2. Add a row only when a reader would otherwise have to search for the owner.
   A row that repeats what the owner's own index already states is not added.
3. Name the owner path and the entry path as they exist in the tree. A row
   whose owner or entry path is missing fails validation.
4. Write the validity condition as an observable change, not as a date.
5. Index every new document in the Item Index above.

## Related Documents

- [Governance Hub](../README.md)
- [Context and Memory](../governance/context-and-memory.md)
- [knowledge-map skill](../skills/knowledge-map/SKILL.md)
- [Repository documentation](../../docs/README.md)
