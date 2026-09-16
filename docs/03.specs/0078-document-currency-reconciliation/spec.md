---
title: "Document Currency Reconciliation Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-14"
layer: "specs"
artifact_id: "SPEC-0078"
---

# Document Currency Reconciliation Technical Specification (Spec)

## Overview

A read-only audit of `docs/` compared the corpus with the current
implementation under `gitops/`, `infrastructure/`, `scripts/`, `.github/` and
`.agents/`. It found runbook commands that name absent files or resources,
policies that forbid what the manifests do, accepted decisions whose decision no
longer describes the tree, stage indexes whose status and dates disagree with
their documents, dated reference observations presented as current, and Stage
03 packages whose work was implemented or overtaken but whose lifecycle state
never moved.

This Spec owns the reconciliation of those statements with the implementation.
It changes documents only. It implements no pending work: where a package's
work is genuinely unfinished, the work stays open and only its description is
corrected.

## Strategic Boundaries & Non-goals

Authorized scope is `docs/01.requirements/`, `docs/02.architecture/`,
`docs/03.specs/`, `docs/05.operations/`, `docs/90.references/`, the prose of
`docs/98.archive/README.md` outside its manifest and index table,
`docs/99.templates/templates/README.md`, and `docs/README.md`.

Explicit non-goals. No manifest, script, test, workflow or registry changes.
No sealed Stage 98 record, migration ledger or archive index row changes. No
lifecycle edge is added to the registry, and no document takes more than one
declared lifecycle edge in one change. No pending criterion is implemented to
make a package look complete. No live cluster, provider runtime or network
action is authorized.

## Contracts

A current document states only what the implementation does today, or names
the dated observation it is quoting. An accepted decision whose decision no
longer holds is either superseded with reciprocal links or carries a dated
clarification that names the current evidence and its successor. A stage index
row matches its document's status and `updated` value. A lifecycle transition
moves exactly one declared edge and records the evidence that justifies it.

## Core Design

Corrections follow the owner of each statement. Runbooks, policies and guides
are corrected in place against the manifests and scripts they describe.
Accepted decisions keep their Decision section and gain a dated clarification
in Traceability; a decision fully replaced by an existing accepted decision
moves to `superseded` with reciprocal links; a decision whose replacement is not
yet decided gets a proposed successor. Stage 90 observations keep their dates
and gain a dated currency note instead of being rewritten.

Stage 03 dispositions take the next single edge only. Packages whose work is
implemented and whose remaining items are recorded operator-owned DEFERs move
to `done`. Packages whose recommended disposition needs an edge the registry
does not declare, such as withdrawing a never-activated draft, keep their state
and gain a dated disposition note naming the blocker and the owner.

## Data Modeling & Storage Strategy

No data shape changes. Frontmatter changes are limited to `status`, the
`supersedes`/`superseded_by` pair the architecture-decision profile declares,
patch `version` increments and `updated` dates.

## Interfaces & Data Structures

No command-line interface, validator, rule identifier or registry profile
changes. Command examples in operations documents are corrected to the
interfaces that already exist.

## Edge Cases & Error Handling

A statement the audit flagged but the tree does not confirm is left unchanged
and recorded as not reproduced. A dated historical section is never rewritten;
a note is added beside it. An archive index edit that would change its manifest
or rows is out of scope.

## Failure Modes & Fallback / Human Escalation

Each logical commit reverts alone. A disposition that needs a missing lifecycle
edge, a second edge, a sealed record or a runtime observation is recorded with
its owner rather than forced. Withdrawal of never-activated drafts and native
runtime acceptance remain decisions for the request owner.

## Verification Commands

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
python3 scripts/qa.py full
```

`full` owns unit discovery and the pre-commit manual stage. No command here
proves provider runtime or live cluster behavior.

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-DCU-001 | Operations, requirement, architecture, hub and template documents state no command, path, resource name, version or rule that conflicts with the current implementation | Audit finding list with per-finding evidence and the strict document gates |
| VAL-DCU-002 | Every accepted decision whose decision no longer describes the tree is superseded with reciprocal links or carries a dated clarification that names its successor | Decision log review and the lifecycle gate |
| VAL-DCU-003 | Stage 03 packages whose work was implemented or overtaken take the next single declared lifecycle edge with recorded evidence, and no pending criterion is implemented | Per-package disposition table and the lifecycle gate |
| VAL-DCU-004 | Stage indexes match their documents' status and `updated` values | Index-status and repository-quality gates |
| VAL-DCU-005 | Stage 90 observations that no longer hold keep their dates and carry a dated currency note | Reference review and the registry index-parity gate |
| VAL-DCU-006 | Dispositions blocked by a missing edge, a second edge or an operator-owned observation are recorded with their owner | Task handoff record |

## Traceability

[Implementation Plan](plan.md) owns ordered work and the
[reconciliation Task](tasks/tsk-0001-reconcile-document-currency.md) owns
execution evidence, approval boundaries and handoff.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCU-001 | Evidence-backed correction of each audited statement |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCU-002 | Reciprocal supersession or dated clarification review |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCU-003 | Package-local disposition evidence |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCU-004 | Index parity gates |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCU-005 | Dated currency-note review |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DCU-006 | Single-edge lifecycle evidence and the handoff record |
