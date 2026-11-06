---
title: "SDLC Cross-Artifact Conformance"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0146"
---

# SDLC Cross-Artifact Conformance Technical Specification (Spec)

## Overview

On 2026-11-06 the operator asked for an audit and remediation of the
engineering governance that ties Requirement, Architecture, Spec, Plan and
Task together. The [audit](../../90.references/audits/0001-sdlc-governance/m0001-sdlc-governance-audit.md)
found the chain enforced machine-side from Requirement to Task, with four
prose gaps on the Architecture side and on conflict handling. A governance and
Stage 99 form change needs this package. The [Plan](plan.md) orders the work
and [Task 0001](tasks/tsk-0001-sdlc-cross-artifact-conformance.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - one `Cross-artifact conformance` subsection in `.agents/governance/sdlc.md`;
  - author prompts in the Spec, Plan and ADR templates under
    `docs/99.templates/templates/`;
  - the audit pack `docs/90.references/audits/0001-sdlc-governance/`.
- Non-goals:
  - any registry, schema or validator change: required sections and
    relationship columns stay as they are;
  - rewriting current Requirement, Architecture or ADR documents;
  - adding files for tools the repository does not use (Spec Kit, OpenSpec,
    Cursor, Copilot).
- Open questions: none that change a criterion. Whether to make the Spec's
  Architecture link machine-checked is recorded as a decision for the
  operator in the audit.

## Contracts

- `sdlc.md` states, for Stage 03 change kinds only: a Spec links its
  constraining Architecture Descriptions and ADRs or says none apply; an open
  question that changes a criterion blocks approval; a departure from current
  architecture waits for an accepted ADR; a divergence between implementation
  and an approved document is recorded and resolved at its owner, never by
  editing a downstream document alone.
- The Spec template prompts for constraining architecture and for open
  questions; the Plan template prompts for an architecture compliance check;
  the ADR template prompts for the requirement IDs and views served.
- Every current document still passes the strict document checks.

## Core Design

Prose-only change. The rule lives once in `sdlc.md`, which owns the flow;
templates carry prompts that point authors at it. The registry's existing
`Lifecycle Traceability` contracts already enforce Requirement → Spec → Plan →
Task and Architecture → Spec links, so no machine field is added. Constraining
architecture: [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
assigns document form to Stage 99 and flow to `.agents/governance/`; this
change stays inside that split.

## Data Modeling & Storage Strategy

No data or schema changes.

## Interfaces & Data Structures

Template prompts are HTML comments; required headings are unchanged, so
existing documents and the validators are unaffected.

## Edge Cases & Error Handling

- Normal: a new Spec from the template shows the architecture and
  open-question prompts.
- Error: a small correction or README edit is not drawn into the new rules;
  the subsection scopes itself to the Stage 03 change kinds.
- Boundary: a Spec with no constraining architecture states that none apply.

## Failure Modes & Fallback / Human Escalation

A failing strict check means a prompt broke a template contract; revert the
template edit. A rule the operator rejects is reverted with its commit.

## Verification Commands

- `python3 scripts/validate-markdown-profiles.py --root . --mode strict`
- `python3 scripts/validate-links-and-owners.py --root .`
- `python3 scripts/validate-document-lifecycle.py --root . --mode staged`
- `python3 -m unittest discover -s tests -p 'test_document*.py'`

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SDLC-001 | `sdlc.md` carries the Cross-artifact conformance subsection; strict document and link checks PASS |
| VAL-SDLC-002 | The Spec, Plan and ADR templates carry the new prompts; strict profile checks and the document unit tests PASS |
| VAL-SDLC-003 | The audit pack records inventory, findings, remediation and validation state; strict checks PASS and an independent review finds no blocking issue |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDLC-001 | Strict document and link checks |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDLC-002 | Strict profile checks and document unit tests |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDLC-003 | Strict checks and independent review |
