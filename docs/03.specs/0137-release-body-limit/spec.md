---
title: "Release Body Limit"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0137"
---

# Release Body Limit Technical Specification (Spec)

## Overview

`scripts/release.py publish` passes the whole `CHANGELOG.md` section as the
GitHub Release body. GitHub rejects a body longer than 125,000 characters. The
`0.1.0` section that [SPEC-0136](../0136-first-semver-release/spec.md)
prepared covers the whole repository history and holds 143,352 characters, so
publication would fail with `RELEASE-DRAFT-INCOMPLETE`. On 2026-10-28 the
operator chose to keep the full changelog and handle the limit in the tool.
The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-release-body-limit.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `scripts/release.py`, `tests/test_release.py`, RUN-0012's
  description of the release body, this package, the Stage 03 README index
  and the REQ-0003 trace link.
- Added after approval: `scripts/validation/current_executable_references.py`
  and its test, which classify `CHANGELOG.md` as a historical record. The
  `0.1.0` notes name scripts retired since, and the repository quality gate
  rejected them as current references.
- Non-goals:
  - changing `CHANGELOG.md`, `cliff.toml` or what a section contains;
  - publishing any release.

## Contracts

- A section of at most 125,000 characters is the Release body unchanged.
- A longer section makes the body a summary: the section heading, the number
  of entries under each `###` group, and a link to the full section in
  `CHANGELOG.md` at the release tag. The summary itself stays within the
  limit.
- The publish preview reports the body length and whether the summary is
  used, so the operator sees it before `--execute`.
- Remote verification compares the Release body with the same derived body.
- A script named in `CHANGELOG.md` must be recoverable from Git history, as
  for any other historical record; it need not exist in the current tree.

## Core Design

One pure function derives the body from the section and the tag; `publish`
uses it for the draft, the verification and the preview.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

The preview line gains `body_chars=<n>` and `body=section|summary`.

## Edge Cases & Error Handling

- A section exactly at the limit stays whole.
- A section without `###` groups still yields a summary with the link.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request restores the previous behaviour.

## Verification Commands

- `python3 -m unittest tests.test_release`
- `python3 scripts/release.py --root . publish --version v0.1.0 --initial-version`
  on `main` after merge, as a read-only preview.
- `python3 scripts/qa.py staged` on each commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RB-001 | A test fails before the change and passes after it: a section over 125,000 characters yields a summary within the limit with group counts and the tagged `CHANGELOG.md` link, and a section at or under the limit is unchanged. |
| VAL-RB-002 | The publish draft, its verification and the preview use the derived body, the existing release tests pass, RUN-0012 describes the rule, and the repository quality gate accepts the `0.1.0` changelog. |
| VAL-RB-003 | An independent reviewer confirms the change, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RB-001 | Focused failing-then-passing test |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RB-002 | Release tests and runbook |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RB-003 | Review and hosted checks |
