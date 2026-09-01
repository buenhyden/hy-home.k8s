# SPEC-0067: Artifact Identity and Filename Normalization

## Overview

Spec 0067 makes every governed artifact identity name its own type and its
parent, and makes numbered leaf filenames start with the number they carry. It
changes declaration and naming only; no document, rule meaning, or machine-
loaded path moves as a side effect.

## Scope

This README is a navigation projection only. The Spec owns the identity and
filename contract, the Plan owns implementation order and risk, and the Task
owns execution evidence. This router does not duplicate those bodies or define
a lifecycle state.

## Item Index

| Item | Body |
| --- | --- |
| Technical contract | [spec.md](spec.md) |
| Implementation order and risk | [plan.md](plan.md) |
| Execution evidence | [tasks/tsk-0001-aif-000.md](tasks/tsk-0001-aif-000.md) |

## Add and Find

Add a package-local Task under `tasks/` and record execution evidence there.
Identity patterns belong to the registry profile and frontmatter schema, not to
this router or to any prose body.

## Related Documents

- [Current Spec Index](../README.md#current-spec-index)
- [ADR-0024 — terminal artifact identity and archive layout](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md)
- [Document Authoring Policy](../../00.agent-governance/policies/document-authoring.md)
