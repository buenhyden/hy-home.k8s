# AI Agent Governance Hub

## Overview

Stage 00 owns human governance for agent work in this GitOps workspace.
Codex and Claude are the supported providers; `.agents/` is provider-neutral.

## Stage Contract

- `policies/`: approval, safety, quality, data, Git, and SDLC norms.
- `roles/`: responsibility boundaries and handoff meaning.
- `providers/`: native loading and capability differences only.
- `skills/`: reusable governance procedures and their approval boundary.
- `sdlc.md`: Requirements → Architecture → Spec → Implementation → Operations.

The [agent registry](../../.agents/registry.json) owns exact role IDs,
permissions, handoffs, skill references, and projection paths. The
[Stage 99 registry](../99.templates/registry.json) owns document contracts.
Scripts own executable checks; neither registry is duplicated in this router.

Shared hooks and the remaining contracts still have explicit migration owners
in Spec 0054. They are transitional executable consumers, not additional human
policy owners. [Context and memory](policies/context-and-memory.md) owns the
progress and memory boundary; the `memory/` directory retired under
[MIG-0009](../98.archive/migrations/0009-governance-memory-retirement.md).

## Document Index

### Current Governance Authority Index

| Document | Lifecycle |
| --- | --- |
| [`agent-execution.md`](policies/agent-execution.md) | `active` |
| [`approval-and-safety.md`](policies/approval-and-safety.md) | `active` |
| [`document-authoring.md`](policies/document-authoring.md) | `active` |
| [`document-lifecycle.md`](policies/document-lifecycle.md) | `active` |
| [`git.md`](policies/git.md) | `active` |
| [`model-selection.md`](policies/model-selection.md) | `active` |
| [`quality.md`](policies/quality.md) | `active` |
| [`claude.md`](providers/claude.md) | `active` |
| [`codex.md`](providers/codex.md) | `active` |
| [`architecture.md`](roles/architecture.md) | `active` |
| [`documentation.md`](roles/documentation.md) | `active` |
| [`infrastructure.md`](roles/infrastructure.md) | `active` |
| [`operations.md`](roles/operations.md) | `active` |
| [`quality.md`](roles/quality.md) | `active` |
| [`security.md`](roles/security.md) | `active` |
| [`supervision.md`](roles/supervision.md) | `active` |
| [`sdlc.md`](sdlc.md) | `active` |
| [`delegated-development.md`](skills/delegated-development.md) | `active` |
| [`work-lifecycle.md`](skills/work-lifecycle.md) | `active` |

## Authoring Workflow

1. Start from root `AGENTS.md` or `CLAUDE.md`.
2. Follow [work lifecycle](skills/work-lifecycle.md) and load only relevant
   policies, responsibilities, provider notes, and task evidence.
3. Use [document authoring](policies/document-authoring.md) and the Stage 99
   selected template for document work.
4. Change the single responsible owner, migrate current links, and record
   applicable Git-backed recovery in the same logical cutover.
5. Validate the affected registry, projections, semantics, and document
   contracts; keep repository-static and runtime evidence separate.

## Related Documents

- [SDLC Flow](sdlc.md)
- [Agent Registry](../../.agents/registry.json)
- [Roles router](roles/README.md) selects responsibilities without copying the
  machine roster.
- [Templates](../99.templates/README.md)
- [Archive](../98.archive/README.md)
- [Scripts](../../scripts/README.md)
