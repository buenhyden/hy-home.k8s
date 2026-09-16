---
title: "Reconcile Document Currency"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-14"
layer: "specs"
artifact_id: "SPEC-0078-TSK-0001"
---

# Task: Reconcile Document Currency

## Overview

This Task owns execution of the six approved packages, the evidence for each
logical commit, the final full result and the handoff record. It records
observed results only and never promotes a repository-static result to hosted,
provider-runtime or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, boundaries and criteria.
- [Plan](../plan.md) owns package order, ownership and rollback.
- Baseline: `python3 scripts/qa.py full` at `EXIT=0`, 22 of 22 gates `PASS`,
  on the tree of commit `404d422c`.
- Four read-only audits on 2026-09-14 covered Stage 01/02, Stage 05/90, the
  hub, indexes and templates, and the incomplete Stage 03 packages.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-DCU-001 | Correct operations documents | platform | Done | Nine runbooks, the service-mesh policy, the QA guide and three operations indexes corrected against the manifests and scripts | `60b6b604`; staged QA PASS |
| WORK-002 | VAL-DCU-001 | Correct requirement, architecture, hub and template documents | platform | Done | Current owner references, seven dated decision clarifications, AD-0006 traceability, hub, archive prose and template catalog corrected; archive manifest and index rows unchanged | `60b6b604`; staged QA PASS |
| WORK-003 | VAL-DCU-002 | Reconcile the decision log | platform | Done | ADR-0027 superseded by ADR-0028 with reciprocal links; ADR-0009 clarified; ADR-0037 proposed | `26635d84`; staged QA PASS |
| WORK-004 | VAL-DCU-005 | Annotate dated reference observations | platform | Done | Currency notes added to m0007, m0008, m0012 and the research pack README; observation dates unchanged | `60b6b604`; staged QA PASS |
| WORK-005 | VAL-DCU-003, VAL-DCU-004 | Take the next lifecycle edge for implemented Stage 03 work | platform | Done | Eight documents moved one declared edge; the Stage 03 index matches | `4d9cd689`; staged QA PASS |
| WORK-006 | VAL-DCU-006 | Record deferred dispositions | platform | Done | Blocked and second-edge dispositions recorded below with owners | This record |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/01.requirements/`, `docs/02.architecture/`,
  `docs/03.specs/`, `docs/05.operations/`, `docs/90.references/`,
  `docs/README.md`, `docs/99.templates/templates/README.md`, and the prose of
  `docs/98.archive/README.md` outside its manifest comment and index table.
- **Forbidden Paths**: sealed records under `docs/98.archive/`,
  `docs/99.templates/registry.json` and contracts, `gitops/`, `infrastructure/`,
  `policy/`, `secrets/`, `scripts/`, `tests/`, `.github/`, `.agents/`.
- **Approval Required**: The request owner approved reconciliation, lifecycle
  status changes, remediation of separate defects found during the work, and
  commit, merge, push and branch cleanup after completion. Withdrawing
  never-activated drafts through an undeclared edge is not approved.
- **Static Validation**: staged QA per logical commit, one
  `python3 scripts/qa.py full` on the final tree, and `git diff --check`.
- **Live Validation**: DEFER. No live cluster, provider runtime or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential or private configuration
  file is read or printed.
- **Rollback Plan**: Each package is one commit that reverts alone.
- **Evidence Location**: This Task record.

## Verification Summary

Every audited finding was re-verified against the tree before it was edited.
Examples of that evidence: `gitops/apps/root/platform-kiali-app.yaml` installs
`kiali-operator` `2.10.0` under Application name `platform-kiali`; no
`istiod-values.yaml` exists; the NetworkPolicy is
`allow-kiali-egress-to-observability`; `namespace-ingress-nginx.yaml` carries
`istio-injection: enabled`; all ten namespaces carry Pod Security labels; no
`kind: Certificate` manifest exists; `.github/workflows/ci.yml` defines three
jobs and the five workflows seven.

Not reproduced and left unchanged: the audit's claim that every namespace
carries an `enforce` label (seven carry only `audit`/`warn`); m0007 and m0008
findings that live in an external repository; RUN-0001's `infra_net` network
name and RUN-0007's EndpointSlice exclusion claim, which depend on runtime
state.

Each logical commit passed `python3 scripts/qa.py staged` over its exact index:
`6fe824ae` (6 gates), `60b6b604` (6 gates), `26635d84` (6 gates),
`4d9cd689` (6 gates). The final `python3 scripts/qa.py full` runs once on the
tree containing this record, so its verdict is recorded in the merge handoff
rather than here. Hosted CI is recorded only for a named observed commit.

This record, its Spec and its Plan were created in their zero-indegree states
(`queued` and `draft`). The lifecycle gate compares a pull request with its
base, where this package did not yet exist, so a document created in the same
change had to keep that state, and activation and closure were named as the
first reviewed change after merge. **Activation (2026-09-16).** That merge
happened, and this change takes the `draft` to `active` and `queued` to
`in-progress` edges under
[SPEC-0084](../../0084-stage03-backlog-closeout/spec.md); closure follows as its
own reviewed change, because no `draft` to `done` edge exists.

A working-tree run of the registry, lifecycle, link and archive validators
fails while edits are unstaged, because those validators compare the index
with the working tree. That is drift, not a content defect; each exact-index
run passed.

Deferred, with owners:

- SPEC-0048 and SPEC-0051: withdrawal is recommended, but the registry declares
  no `draft` to `withdrawn` edge for Specs and Plans. Next owner: the request
  owner, who decides between adding that edge or activating and withdrawing in
  two reviewed changes.
- SPEC-0071 and SPEC-0062 TSK-0011: moved one edge; the move to `done` is the
  next reviewed change. Next owner: this Task's follow-up.
- ADR-0037: proposed; accepting it and superseding ADR-0009 is a separate
  reviewed change. Next owner: the architecture decision owner.
- SPEC-0072 TSK-0001 WORK-009: native runtime acceptance stays open, as its own
  record requires. Next owner: the operator.
- SPEC-0047: its CSASR-004 is obsolete and its stash reconciliation remains
  pending; cancelling the queued Task needs two edges. Next owner: SPEC-0047.
- SPEC-0054 TSK-0009, TSK-0013 and TSK-0014: dispositions depend on the
  retention policy and remain with SPEC-0054.
- SPEC-0049 and SPEC-0050: genuinely pending work whose contract location
  `.agents/contracts/` must be re-planned before activation.

## Traceability

Each work item below carries its observed result and durable evidence.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done. | Operations corrections in `60b6b604`. |
| [WORK-002](../plan.md#work-breakdown) | Done. | Requirement, architecture, hub and template corrections in `60b6b604`. |
| [WORK-003](../plan.md#work-breakdown) | Done. | Decision log reconciliation in `26635d84`. |
| [WORK-004](../plan.md#work-breakdown) | Done. | Reference currency notes in `60b6b604`. |
| [WORK-005](../plan.md#work-breakdown) | Done. | Single-edge lifecycle moves and index parity in `4d9cd689`. |
| [WORK-006](../plan.md#work-breakdown) | Done. | Deferred dispositions with owners in this record. |
