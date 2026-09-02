# SPEC-0071: Document Taxonomy and Form Identity Normalization

## Overview

Spec 0071 gives every document profile a `family/kind` identity, removes the
stage sort prefix from `layer`, moves `version` onto the semantic grammar the
machine contracts already use, names each Stage 99 form for the document it
produces, and makes the frontmatter value contract executable instead of merely
declared.

## Scope

This README is a navigation projection only. The Spec owns the taxonomy and
form contract, the Plan owns implementation order and risk, and the Task owns
execution evidence. This router does not duplicate those bodies or define a
lifecycle state.

## Item Index

| Item | Body |
| --- | --- |
| Technical contract | [spec.md](spec.md) |
| Implementation order and risk | [plan.md](plan.md) |
| Execution evidence | [tasks/tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |

## Add and Find

Add a package-local Task under `tasks/` and record execution evidence there.
Profile identities and key grammars belong to the registry and the frontmatter
schema, not to this router or to any prose body.

## Related Documents

- [Current Spec Index](../README.md#current-spec-index)
- [Archive Index](../../98.archive/README.md) routes MIG-0010, which seals the form moves
- [Document Authoring Policy](../../00.agent-governance/policies/document-authoring.md)
