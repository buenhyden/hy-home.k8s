---
title: "Architecture Views"
version: "0.4.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0126-TSK-0001"
parent_ids: ["SPEC-0126-PLAN-0001"]
---

# Task: Architecture Views

## Overview

Add C4 views and an arc42 coverage table to AD-0007. It executes
[SPEC-0126](../spec.md) through [WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: the operator said on 2026-10-27 to proceed as recommended; slice
  B of the SPEC-0125 status table covers CR-09.05 and CR-09.07.
- Sources: SPEC-0124 rows `SRC-WERPC-116`, 273, 274 (C4) and 117 (arc42).
- Start: main `5347f851`, branch `docs/c4-arc42-views`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AV-001](../spec.md#success-criteria--verification-plan) | Add the C4 views, element table and deployment mapping | platform | completed | PASS | EVD-005 closes EVD-001 |
| WORK-002 | [VAL-AV-002](../spec.md#success-criteria--verification-plan) | Add the arc42 coverage table and template prompt | platform | completed | PASS | EVD-004 closes EVD-002 |
| WORK-003 | [VAL-AV-003](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | completed | PASS | EVD-006 closes EVD-003 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Diagram validation and source review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Coverage review and template tests | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AV-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Coverage review and template tests | Branch `docs/c4-arc42-views`: `python3 scripts/validate-document-contract-registry.py`, `python3 -m unittest tests.test_repository_form_contracts`, `python3 scripts/validate-markdown-profiles.py`, `python3 scripts/validate-links-and-owners.py` | PASS | AD-0007 gains `### arc42 coverage` with a location or reason for all twelve sections; five rows name a gap or omission (component view, dynamic diagram, crosscutting concepts kept in ADRs, risk register, glossary). The template gains one optional Traceability prompt. The registry passes 969 paths, the form contract tests pass, and the profile and cross-document checks pass with every in-page anchor resolving | yes | EVD-002 |
| EVD-005 | [VAL-AV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Diagram validation and source review | PR #181: Mermaid Chart validation of both diagrams at `2e68ebd2` with source identical to the file; independent GitOps review of `dbbef82e`, then of `2e68ebd2` | PASS | Both flowcharts are valid. The first review requested changes: cert-manager does not issue Argo CD's certificate, and image registries, Grafana, Loki, Tempo, the Alloy gateway, Rollouts analysis, sidecar trace export, the CoreDNS host mapping and the bootstrap-loaded CA were missing; the arc42 runtime row overstated AD-0004. Commit `2e68ebd2` scoped the cert-manager arrow, added those dependencies and paths and corrected the row. The second review traced every new claim to its source and approved; its remaining note (Kubernetes API calls and C1 chart pulls are not drawn) matches the stated omissions | yes | EVD-001 |
| EVD-006 | [VAL-AV-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Staged QA and hosted checks | PR #181 heads `dbbef82e` (CI run `40497308810`) and `2e68ebd2` (CI run `40498430860`); pre-commit staged QA on commits `48b3ea53`, `bb7222c1`, `dbbef82e` and `2e68ebd2` | PASS | `ci-summary` and `style-pr` passed on both heads, and the PR checks list `label` and GitGuardian as passed. Staged QA passed on all four commits | yes | EVD-003 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AV-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-005 | Accepted by the operator on 2026-10-27: valid context and container views, element table and deployment mapping, with every relationship traced to a source | platform |
| [VAL-AV-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the operator on 2026-10-27: all twelve arc42 sections have a location or reason, and the template prompt passes its contract tests | platform |
| [VAL-AV-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Accepted by the operator on 2026-10-27: staged QA and the hosted checks passed | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/01.requirements/0004-current-local-gitops-platform.md`,
  `docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`
  and `docs/99.templates/templates/architecture/description.template.md`.
- **Forbidden Paths**: manifests, infrastructure, provider settings and
  credentials.
- **Approval Required**: the operator said on 2026-10-27 to proceed as
  recommended. Push, pull request and merge follow RUN-0013.
- **Acceptance**: on 2026-10-27 the operator accepted VAL-AV-001 to
  VAL-AV-003.
- **Static Validation**: Mermaid validation, focused tests and `qa.py staged`.
- **Live Validation**: none; the views describe tracked desired state.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

WORK-001 passed (EVD-005): AD-0007 has valid C4 context and container views,
an element table and a deployment mapping, revised after the first review
and approved by the second. WORK-002 passed (EVD-004): the arc42 coverage
table and the optional template prompt are in place. WORK-003 passed
(EVD-006): staged QA and the hosted checks passed. The operator accepted all
three criteria. The ADR form comparison (CR-09.06) and the branch-strategy
ADR (CR-13.07) remain for the next Spec.
