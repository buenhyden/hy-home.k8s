---
title: "Repository Vocabulary Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0163-PLAN-0001"
parent_ids: ["SPEC-0163"]
---

# Repository Vocabulary Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one constraint: only the files the Spec names by writer change; ADR-0036 itself is not edited.

## Overview

Create the Repository Vocabulary, amend the pointer-only rule through ADR-0058, route the glossary through its own registry profile, teach the knowledge validator to check it, and point the SDLC table and the knowledge owners at it. [Task 0001](tasks/tsk-0001-repository-vocabulary.md) owns execution and evidence.

## Context

The user asked on 2026-11-12 to continue every open item, with current v14.7 requirements prevailing over conflicting rules (SPEC-0161 EVD-018). The glossary path is fixed by the package and conflicts with the pointer-only rule of ADR-0036 and its consumers; the requirement prevails, and ADR-0058 records the narrow exception. This branch continues `claude/w00-v14-7-intake` after `4956440a`. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md) constrain the design.

## Goals & In-Scope

- ADR-0058 (proposed, then accepted by the user) and the decision index.
- REQ-0003 FR-0032 with its Traceability row.
- Registry profiles, template, lifecycle-domain entries; pointer profile excludes the glossary.
- Validator change and tests, including Hangul word matching.
- Glossary; SDLC table; context-and-memory sentence; knowledge README; wiki-curator and knowledge-map; Stage 99 and scripts READMEs.

## Non-Goals & Out-of-Scope

- Other roles' common forms, DOC-09, CI-SCOPE and DOC-12.
- Rewording any policy rule; editing ADR-0036's body.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-VOCAB-002](spec.md#success-criteria--verification-plan) | Add failing vocabulary and Hangul tests, then the validator change. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-repository-vocabulary.md) | Contract suite before and after. |
| WORK-002 | [VAL-VOCAB-001](spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](spec.md#success-criteria--verification-plan) | ADR-0058, FR-0032, registry and template, glossary, SDLC table and the knowledge owners. | WORK-001; ADR-0058 accepted before the glossary is committed. | [Task 0001](tasks/tsk-0001-repository-vocabulary.md) | Knowledge validator, inline ID check, strict document checks, commit hooks. |

## Verification Plan

- Show the new tests failing on the current validator, then passing; run the existing knowledge tests.
- Run the knowledge validator on the tree and fix any copied span the Hangul change surfaces.
- Check the 33 common IDs against the contract inline.
- Map each old SDLC row to its kept rule and moved meaning in the Task.
- Record the risk class (`medium`: registry, validator, test and ADR change) and the core-diff checklist.
- Architecture compliance: ADR-0036 unchanged; ADR-0058 is the only new decision.

## Risks & Mitigations

- **A definition copies policy text.** Mitigation: the duplicate-span rule fails it; reword the definition.
- **Hangul matching flags existing pointer documents.** Mitigation: fix the copied span in that document; never relax the rule.
- **A registry change breaks another consumer.** Mitigation: run the registry, profile and lifecycle validators and the document contract suite.
- **ADR-0058 is not accepted.** Mitigation: stop before committing the glossary.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure, ADR-0058 accepted and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Repository Vocabulary owner | [SDLC contract](../../../.agents/governance/sdlc.md) | Ownership and placement |
