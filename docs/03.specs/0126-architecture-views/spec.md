---
title: "Architecture Views"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0126"
---

# Architecture Views Technical Specification (Spec)

## Overview

SPEC-0125 recorded CR-09.05 and CR-09.07 as gaps: the current platform
architecture description
[AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
has no C4 view, and nothing maps its content to the twelve arc42 sections.
This Spec adds a C4 context view, a container view with an element table and
a deployment mapping to AD-0007, an arc42 coverage table, and one optional
template prompt. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-architecture-views.md) records it.

## Strategic Boundaries & Non-goals

- In scope: AD-0007, the architecture description template, this package
  and the Stage 03 README index.
- Non-goals:
  - component or code views, dynamic diagrams and a glossary;
  - a diagram tool, renderer or validator;
  - views for AD-0004, AD-0005 or AD-0006;
  - any manifest or runtime change.

## Contracts

- Every drawn relationship is backed by a tracked source: an Application, a
  manifest, a namespace label or an ADR.
- A C4 container is a running application or data store; it is not mapped
  one-to-one to a Pod, namespace or Docker container.
- Elements have stable identifiers (`P`, `S`, `E`, `C`), and the container
  table gives each one a responsibility, technology, namespace and source.
- The arc42 table states where each section is covered or why it is
  omitted, and links instead of copying.

## Core Design

Mermaid flowcharts inside AD-0007 are the editable source; GitHub renders
them. Argo CD's relationship to every container is in the table rather than
drawn, so the diagram does not imply it applies only one container.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

- AD-0007 `### System context and container views`, `### Deployment mapping`
  and `### arc42 coverage`.
- One optional author prompt in the architecture description template's
  Traceability section.

## Edge Cases & Error Handling

- Infrastructure that is not a C4 container (control plane, CoreDNS,
  MetalLB) is named as omitted, not drawn.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request removes the views and the prompt.

## Verification Commands

- Mermaid syntax validation of both diagrams.
- `python3 scripts/validate-markdown-profiles.py`.
- `python3 scripts/validate-document-contract-registry.py`.
- `python3 -m unittest tests.test_repository_form_contracts`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AV-001 | AD-0007 has valid context and container diagrams, an element table and a deployment mapping, and an independent reviewer finds every relationship backed by a tracked source and no missing external dependency. |
| VAL-AV-002 | AD-0007 has an arc42 coverage table with a location or reason for all twelve sections, and the template carries the optional prompt with its contract tests passing. |
| VAL-AV-003 | Staged QA passes on every commit and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0004-NFR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-AV-001 | Diagram validation and independent source review |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AV-002 | Coverage review and template contract tests |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AV-003 | Staged QA and hosted checks |
