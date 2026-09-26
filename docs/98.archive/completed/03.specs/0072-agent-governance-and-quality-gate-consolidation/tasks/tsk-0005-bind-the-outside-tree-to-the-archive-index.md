---
title: "Bind the Outside Tree to the Archive Index"
version: "1.0.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-10"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0005"
---

# Task: Bind the Outside Tree to the Archive Index

## Overview

Execute `WP-013`. The archive keeps two admitted routes in: its index, and the
retention class under `completed/` which holds the document itself rather than
a record of it. Every other path under `docs/98.archive/` is a record whose
location the archive owns and may re-seal, so a link to one couples the outside
tree to a decision the archive has not promised to keep.

The rule already existed as `LINK-ARCHIVE-BYPASS`. Its reach did not: it asked
only documents whose status was `active` or `accepted`, so fifty-nine documents
in every other state linked archive internals and passed.

## Inputs

- [SPEC-0072](../spec.md) for `VAL-AGQ-020`.
- [SPEC-0072-PLAN-0001](../plan.md) for `WP-013`.
- [Document authoring policy](../../../../.agents/governance/document-authoring.md)
  as the rule owner, and
  [document lifecycle](../../../../.agents/governance/document-lifecycle.md)
  for the supersession relation this change had to leave intact.
- Branch `refactor/governance-qa-convergence`.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-033 | VAL-AGQ-020 | WP-013A bind every document outside the archive to the archive index | platform | Done | PASS for the approved local scope | `b21c4c2d`; 9 boundary tests; 59 records rerouted |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-links-and-owners.py`,
  `.agents/governance/document-authoring.md`,
  `tests/test_documentation_link_boundary.py`, the fifty-nine rerouted records
  under `docs/02.architecture/` and `docs/03.specs/`, and this Spec package.
- **Forbidden Paths**: `docs/98.archive/` itself. No archived byte was read for
  modification, and none was written.
- **Approval Required**: the reference boundary and its single exemption were
  directed by the user; the merge that follows is a separate instruction.
- **Static Validation**: `python3 scripts/qa.py staged` for the logical commit
  and `python3 scripts/qa.py full` before handoff.
- **Live Validation**: DEFER. Nothing in this unit reaches a cluster, a hosted
  run, or an external service.
- **Secret / Vault Handling**: not applicable; no secret-bearing path is in
  scope.
- **Rollback Plan**: revert `b21c4c2d`. Every identifier stays named in prose
  either way, so only the route changes back.
- **Evidence Location**: this record and that commit.

## Verification Summary

The boundary is keyed to the document's profile rather than to its lifecycle
status. Status changes over time and would have let a record drift back out of
scope as it closed; a profile says what a document is. `operation/incident` and
`operation/postmortem` are the exemption, because an account of what happened
often rests on the archived record itself.

Twenty-eight of the fifty-nine rerouted records are terminal. Rewriting a
sealed record is a real hazard, so the change was checked against it rather
than assumed safe: the identifier each record cited stays in its prose, only
the path moves to the index, and supersession was confirmed to live in front
matter as `superseded_by` rather than in the body links that moved. No
lifecycle relation depended on a link this unit touched.

One invariant surfaced during execution and is worth recording: the MIG-0004
recovery proof requires its terminal targets to be identical in the Git index
and the worktree, so a half-staged edit of those records fails the archive
proof as `RECOVERY-MIGRATION-TARGET` rather than passing quietly.

Lane results: repo-static PASS for `qa.py staged` (12 gates, exact index) and
`qa.py full` (22 of 22 gates, exit 0), with no FAIL, SKIP or DEFER. This is a
local repository-static result; it is neither a GitHub-hosted PASS nor evidence
of live cluster state.

Independent review disposition: none. One agent implemented and verified this
unit, which is a limitation of the evidence rather than a passed review.

Residual risk: the boundary reads links. A plain-text mention of an archive
path in prose is not a link and is not caught, so a future record could still
name an internal path without creating a resolvable dependency on it.

Next owner: the user, for the merge that follows.

## Traceability

[SPEC-0072](../spec.md) owns `VAL-AGQ-020` and
[SPEC-0072-PLAN-0001](../plan.md) owns `WP-013`. The
[WP-012 Task](tsk-0004-return-duplicated-authority-to-one-owner.md) is closed
and is not reopened here.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-033](../plan.md#wp-013-bind-the-tree-outside-the-archive-to-the-archive-index) | Done / PASS for the approved local scope. | `VAL-AGQ-020`; `b21c4c2d`; 9 boundary regressions and 59 rerouted records |
