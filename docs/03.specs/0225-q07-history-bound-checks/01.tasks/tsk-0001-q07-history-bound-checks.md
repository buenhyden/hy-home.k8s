---
title: "Q07 History-Bound Check Conversion"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0225-TSK-0001"
parent_ids: ["SPEC-0225-PLAN-0001"]
---

# Task: Q07 History-Bound Check Conversion

## Scope

### Objective and Parent

This Task runs the [Plan](../plan.md) for the [Spec](../spec.md): it converts
the checks residue Q07-H01 names and records what stays as cutover data,
serving VAL-HISTORY-001 to VAL-HISTORY-004.

### Inputs and Authority

On 2026-11-19 (Asia/Seoul) the user asked to convert or remove the Q07-H01
checks so they no longer depend on history or numbering, then commit, push,
open a pull request, merge and update `main`. Asked about items 2 to 5, the
user chose an explicit form marker for the retained ADR form, a declared
baseline for the reserved policy codes, and the lineage reservations and
`git show` citations handled as data at the cutover. Input revision:
`cabab987`.

- **Allowed Paths**: `scripts/`, `tests/`, `docs/99.templates/`, `docs/00.workspace/03.process/`, `docs/02.architecture/AGENTS.md`, the frontmatter of the 36 retained ADRs, `docs/03.specs/`
- **Forbidden Paths**: accepted ADR bodies, published reference members, completed Task evidence, `docs/98.archive/`
- **Approval Required**: the user's approval of this Spec and Plan; protected operations stay with the user
- **Static Validation**: `python3 scripts/qa.py staged` on the pinned `hyhome-validation` venv
- **Live Validation**: not applicable; no runtime change
- **Secret / Vault Handling**: no secret is read
- **Rollback Plan**: revert the conversion commit
- **Evidence Location**: this Task

## Execution Log

### Work Performed

| Item | Work Unit | Owner | Status | Blocker |
| --- | --- | --- | --- | --- |
| WORK-001 | WORK-001 | platform | draft | none |
| WORK-002 | WORK-002 | platform | draft | none |
| WORK-003 | WORK-003 | platform | draft | none |
| WORK-004 | WORK-004 | platform | draft | none |

WORK-001 set `READABLE_REGISTRY_MAJORS` to the current MAJOR and removed the
code whose own removal condition that meets: `historical_major`, the
`listed_headings` field, `TASK_EVIDENCE_HEADER_MAP` with
`carry_evidence_rows`, and the old-list Plan branch of the lifecycle check.
Tests whose only subject was an older-generation read were deleted or now
assert the fallback to the current registry.

WORK-002 made the tests that read requirement files 0001 to 0004 find a current
requirement document by route and derive its IDs, or use a synthetic path.

WORK-003 added `policy_rule_ids.baseline` (1; absent reads as 1): the
never-shrink, code-change, rule-delete and reissue refusals apply only within
one baseline, and DOCLIFE-R022 names it.

WORK-004 added the `retained_form` frontmatter key (value
`adr-accepted-retained-form`) to the ADR profile, its template twin, the
frontmatter schema and the key table, marked the 36 accepted ADRs the former
bound selected, and selected the ADR retained form by the marker. The registry
refuses an ADR retained form without the marker or with a bound, and
`FM-RETAINED-FORM` refuses the marker on a document that is not accepted.
`FIRST_ADR_OUTSIDE_RETAINED_RANGE` is gone. The Q07-H01 row of the SPEC-0223
Task now names the data left for the cutover.

### Blockers and Decisions

On 2026-11-19 the user approved the Spec and Plan over commit `7f211684` (EVD-007).

### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [VAL-HISTORY-001](../spec.md#criteria) | NOT_RUN | Draft until the Spec and Plan are approved; observed checks are in Results |
| WORK-002 | [VAL-HISTORY-001](../spec.md#criteria) | NOT_RUN | Draft until the Spec and Plan are approved; observed checks are in Results |
| WORK-003 | [VAL-HISTORY-002](../spec.md#criteria) | NOT_RUN | Draft until the Spec and Plan are approved; observed checks are in Results |
| WORK-004 | [VAL-HISTORY-003](../spec.md#criteria), [VAL-HISTORY-004](../spec.md#criteria) | NOT_RUN | Draft until the Spec and Plan are approved; observed checks are in Results |

## Verification Evidence

### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-HISTORY-002](../spec.md#criteria) | WORK-003 | automated | `test_a_declared_new_baseline_is_the_only_reset` against the `cabab987` lifecycle code | pinned `hyhome-validation` venv | `python -m unittest tests.test_policy_rule_history -k baseline` | 1 | FAIL | a raised baseline was still refused | false | none |
| EVD-002 | [VAL-HISTORY-001](../spec.md#criteria) | WORK-001 | automated | Working tree on `cabab987` plus WORK-001 and WORK-002 | pinned `hyhome-validation` venv | every module of the document, document-lifecycle and tooling suites | 0 | PASS | this Task | true | none |
| EVD-003 | [VAL-HISTORY-002](../spec.md#criteria) | WORK-003 | automated | Same test after WORK-003 | pinned `hyhome-validation` venv | `python -m unittest tests.test_policy_rule_history` | 0 | PASS | this Task | true | none |
| EVD-004 | [VAL-HISTORY-003](../spec.md#criteria) | WORK-004 | automated | Working tree with the marker | pinned `hyhome-validation` venv | `python -m unittest tests.test_common_form_tree tests.test_frontmatter_key_contract` and strict registry and Markdown profile checks | 0 | PASS | this Task; 433 form tree tests | true | none |
| EVD-005 | [VAL-HISTORY-004](../spec.md#criteria) | WORK-004 | automated | Staged conversion index against `cabab987` | pinned `hyhome-validation` venv | `python3 scripts/qa.py staged` | none | NOT_RUN | pending the committed staged run | true | none |
| EVD-006 | [VAL-HISTORY-004](../spec.md#criteria) | WORK-004 | automated | Exact index of commit `7f211684` on `9082116c` | pinned `hyhome-validation` venv; the `staged-qa` pre-commit hook | `python3 scripts/qa.py staged` | 0 | PASS | commit `7f211684`; every selected gate passed in the hook | true | EVD-005 |
| EVD-007 | [VAL-HISTORY-001](../spec.md#criteria) | WORK-001 | observation | {"actor": "user", "approval_ref": "user answer 'Approve' of 2026-11-19 in this session, after commit 7f211684", "scope": ["SPEC-0225", "SPEC-0225-PLAN-0001"], "reviewed_commit": "7f211684", "validity": "confirmed", "revocation": "none"} | none | Spec/Plan approval | none | PASS | this Task | true | none |

### Resolution Links

EVD-001 is a non-required observation followed by EVD-003; EVD-006 resolves EVD-005.

## Acceptance Decision

### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [VAL-HISTORY-001](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [VAL-HISTORY-002](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [VAL-HISTORY-003](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [VAL-HISTORY-004](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |

### Remaining Conditions

The user's acceptance of the criteria.
Q07-H01 stays open for the cutover data it names.

## Handoff

### Promotion Receipt

Rule ID baseline: DOCLIFE-R022 names the registry baseline in the
[document lifecycle policy](../../../00.workspace/03.process/document-lifecycle.md#rules).

### Next Owner

platform, after the user's approval; Q07-CUTOVER removes the data Q07-H01 names.
