---
title: "W03 SemVer Version Tests Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0208-PLAN-0001"
parent_ids: ["SPEC-0208"]
---

# W03 SemVer Version Tests Implementation Plan

## Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds four constraints: no existing version value changes and no check chooses a MAJOR, MINOR or PATCH level; no existing gate or test is weakened and the SPEC-0190 case tests and `tests/test_release.py` keep their behavior; no test reads Git history, a network resource or `_workspace/`; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Survey the version-bearing objects, map each required situation to its surface and to an existing or missing test, move the precedence function to the shared grammar module, add the base-to-proposed version comparison to the lifecycle comparison, add the missing tests and the producer and consumer matrix, and add the policy sentence. [Task 0001](tasks/tsk-0001-w03-semver-tests.md) owns execution and evidence.

## Context

Read at `main` `81096a83`:

- `scripts/semver_grammar.py` holds `SEMVER_PATTERN` and `is_semver`; `scripts/release.py` keeps a private `_precedence` over major, minor, patch and prerelease and refuses a non-increasing tag, a reused initial tag and a changed released changelog section; `tests/test_semver_grammar.py` holds the SPEC-0190 cases.
- No document, registry or contract version is compared anywhere. `scripts/document_lifecycle.py` and `scripts/validate-document-lifecycle.py` read a base and a proposed side and the base registry (`CURRENT_REGISTRY_PATH`), and replay every earlier commit in a cumulative history check.
- Three readers pin the registry `schema_version` by equality at `81096a83`. SPEC-0207 (draft) makes it a SemVer string with MAJOR-only readers and one reader function, and SPEC-0205 (draft) raises its MAJOR number, so the matrix is written against the readers that SPEC-0207 leaves (string `11.0.0`, MAJOR-only) and run against the value SPEC-0205 leaves.
- `shared_contract` carries `stage`, `content_digest` and `source_revision`; `common_forms` carries only `contract_id`, `version` and `forms` until SPEC-0209 adds an adoption record.
- The task file marks the policy as not automating the level choice, so the rules are refusals of a lower version and of a changed released edition only; a missing version is mapped to the existing checks.
- The v14.7 case file lists the increment classes the matrix needs; its precedence and grammar cases are already in SPEC-0190's tests.

## Goals & In-Scope

- The survey rows in the Task; the mapping of each required situation to a check and a test.
- The shared `precedence` function; the comparison rules and their diagnostics; the new test module and the added release tests; the policy sentence; the suite row and exact routes.

## Non-Goals & Out-of-Scope

- Any version value change, level choice, release, tag or `CHANGELOG.md` edit; the adoption record of COMMON-DOC-FORM-1; the representation and value of `schema_version`; Q-07 numbering; hosted CI.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SEMVERTEST-001](spec.md#success-criteria--verification-plan) | The survey and the situation-to-test mapping; the shared `precedence` function; the downgrade, unchanged and tampered-edition comparison with failing-first refusal cases and paired accept cases; the `release._precedence` wrapper; the FR-0027 check cell. | The decisions of W03-D68; SPEC-0190 and SPEC-0207 merged; the phase-3 registry packages merged. | [Task 0001](tasks/tsk-0001-w03-semver-tests.md) | Failing tests first, then passing; release tests unchanged; strict validators equal before and after. |
| WORK-002 | [VAL-SEMVERTEST-002](spec.md#success-criteria--verification-plan) | The producer and consumer matrix, the numbering separation case, the policy sentence, the suite row and routes; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-semver-tests.md) | Strict validators, suites, routing check, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change.
- Read the tree row by row for the survey; record each value from its file, not from the Spec table, and name any row that differs.
- Show each refusal case failing before the code exists and passing after, and each accept case failing through its absent entry point and paired with a refusal; the missing-version, reader and release rows are mapped to existing checks and are not failing-first; all on temporary trees; no test runs a gate over the repository.
- Run the comparison once over the whole current tree against its parent commit and record that it reports nothing as Task evidence, not as a test (no test runs a gate over the repository); if the cumulative replay reports a diagnostic, apply the fallback of the Spec and record the first failing commit.
- Architecture compliance: the work stays within AD-0006 and adds no gate, validator or CLI option.
- Commit order: the package commit appends the decision row W03-D68 to the SPEC-0161 Task (re-read the next free number at commit time). Merge order: SPEC-0191 first, SPEC-0207 right after it, then this package after SPEC-0205 and the other phase-3 registry packages (SPEC-0195 to SPEC-0206) and before SPEC-0209 (the closing records package), because SPEC-0209 records the W05 files this package edits and gives `common_forms` its candidate record; the released-edition rule stays on `shared_contract` only. It merges after SPEC-0190 and SPEC-0191 and rebases on `main` before each commit, re-reading the suite rows and routes it edits.
- Record the risk class (`medium`: a validator, test and policy-sentence change; no permission, secret-handling, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **A new rule refuses a current or historical document.** Possible, Moderate: MEDIUM, mitigate. Owner: W05 code. The comparison runs over the tree and the cumulative replay before commit; the replay fallback is stated in the Spec. Review cue: the first diagnostic. Rollback: revert the implementation commit.
- **The comparison is read as a rule that chooses or demands a version bump.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The rules refuse only lower or changed-released values and the policy sentence says so. Review cue: any test that expects a bump. Signal that raises it: a diagnostic on an unchanged version.
- **The `schema_version` changes of SPEC-0207 and SPEC-0205 invalidate the matrix fixtures.** Possible, Minor: LOW, monitor. Owner: W05 code. The matrix reads the current value from the registry and derives the old edition from it through the reader function. Review cue: the first rebase after either package.
- **Residual: decision W03-D67 keeps `common_forms` at `candidate`.** Likely, Minor: LOW, monitor. Owner: W03 author. The released-edition rule applies to `shared_contract` only, so a released `common_forms` edition is not protected until it leaves `candidate`. Review cue: the SPEC-0209 closing commit and the H20 report.
- **A shared `precedence` function changes release ordering.** Unlikely, Severe: MEDIUM, mitigate. Owner: W06 consumer. The function moves unchanged and `tests/test_release.py` runs before and after. Rollback: restore the private copy.
- **Routes or suite rows collide with concurrent packages.** Possible, Minor: LOW, mitigate. Owner: W03 author. The package rebases and runs `python3 scripts/validate-affected-surfaces.py --root .` expecting `uncovered=0 ambiguous=0`.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` with its approval receipt; the decisions are recorded as W03-D68.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Version comparison rules: refuse a lower version and a changed released edition, accept an unchanged version | [Document authoring](../../../.agents/governance/document-authoring.md) | The version paragraph |
| The lifecycle check also judges version fields (no level choice) | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | The FR-0027 check cell |
