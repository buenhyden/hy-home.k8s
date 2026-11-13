---
title: "W03 Policy Form"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0175-TSK-0001"
parent_ids: ["SPEC-0175-PLAN-0001"]
---

# Task: W03 Policy Form

## Overview

This Task records the seventh phase-2 package of W03, the Policy form, for [SPEC-0175](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-policy-form` from `3d9428b9` (SPEC-0174 closure; PR #239 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D04, W03-D06, W03-D08 and W03-D11; W03-H10 (Policy part); SPEC-0168 (one policy role); EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Policy (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[8]); conditional content from `TEMPLATE-DEFINITION-CONTRACT.md`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | Registry form, extension, TemplateDefinitions, tables, lists and body contract; `REGISTRY_TABLE_TWIN`; tests. | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | 14 documents and two templates moved with the map; anchor edits; policy texts; regression and exact-index QA. | platform | completed | PASS | EVD-005, EVD-006, EVD-007; implementation commit `7c6a35f0` passed exact-index QA and the hooks |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds 1 to 3 | Read-only code-reviewer that wrote none of the package, over spec.md `1b28926f…`, `b3bb7df5…`, `cad60e62…` and plan.md `dec757e4…`, `d31280b5…`, `ebbac4aa…`; 2026-11-13 | FAIL | REJECT three times. Round 1: BLOCK four of nine links into removed H2 anchors unnamed (the link validator checks no cross-file fragment); FIXes on test pins and the per-form loop, the twin body contract, the Stage 99 README bullets, Related Documents link typing, none lines that would deny existing text, and the risk rating. Round 2: BLOCK link kinds without one destination; FIXes to list the fragment search as a command and as the evidence for the anchor edits. Round 3: BLOCK a contradiction on `sdlc.md`; FIX for the document-profile registry link. The author applied each. | no | none |
| EVD-002 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"6168372e9a5b2e613eda16bbe4f1ecc3d065e52f371f1c53aebadb59a4af52f4","plan_sha256":"ebbac4aa9474b067b69423ecdf51cf502ffa2ce89f7fb2402eb5810787e2bfaa"} | PASS | Same reviewer, round 4, 2026-11-13: only the round-3 line changed, every Related Documents link of the 14 documents has one destination, every earlier finding is closed; verdict APPROVE. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0175 approval question naming spec.md 6168372e and plan.md ebbac4aa dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0175","SPEC-0175-PLAN-0001"],"reviewed_spec_sha256":"6168372e9a5b2e613eda16bbe4f1ecc3d065e52f371f1c53aebadb59a4af52f4","reviewed_plan_sha256":"ebbac4aa9474b067b69423ecdf51cf502ffa2ce89f7fb2402eb5810787e2bfaa","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, extension, tables, body contract, `REGISTRY_TABLE_TWIN` and tests, red then green | Working tree over `43658eaa`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_common_form_tree` with the new tests and no registry or code change, 22 failures and 2 errors; the `REGISTRY_TABLE_TWIN` case, rebuilt on a clone of the guide twin, failed only for the missing rule. Green: 154 tests OK (one skipped base); with `test_common_agents_document_routes` (its pinned `## Overview` case now translates `## Purpose`) and `test_validation_tooling_ownership`, 176 OK. The registry Policy form is built from COMMON-DOC-FORM-1 1.0.0 roles[8] by the mapping that reproduces the seven existing forms, `link_only` false; extension `policy-lifecycle-traceability` under `policy-ownership`; the four profiles carry empty lists without `substantive_body` and `ordered`; the body contract of `operation/policy` and its twin reads `Ownership`; both twins carry `Rules`, the operations twin also `Lifecycle Traceability`; consumer paths are regular files. | yes | none |
| EVD-005 | [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | 14 documents and two templates meaning map | Implementer maps (two doc-writer subagents) and a line comparison of every document against `HEAD`, read by the author | PASS | Every source line is kept; old H2 headings are removed and old H3 headings become H4 under the W03-D06 destinations; the `Responsibilities` H3 of POL-0001 and POL-0005 merges into Ownership > Responsibilities; `Lifecycle Traceability` is the local H3 under Ownership; the POL-0001 HTML anchor and its comments are removed; Related Documents links moved inline by the Spec defaults with list text unchanged. Added lines are none-with-reason or pointer lines (English in governance rules, Korean in operations policies) and two Korean lead-in lines before link-only Authority lists in POL-0001 and POL-0005, which the empty-section check refused without prose; the author checked each pointer against its document and corrected two (`approval-and-safety` Exception Conditions, POL-0007 Authority). Placement calls for owner review: governance Responsibilities lines point to Authority and Requirements; mixed exceptions paragraphs stay whole in Exception Conditions; POL-0003 and POL-0004 runbook links appended to the existing Enforcement list; POL-0003 and POL-0004 retired-package items before the Lifecycle Traceability table; link-only Authority sections given a lead-in line. | yes | none |
| EVD-006 | [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, fragments, suites and lint | Author run over the working tree after `0d1d0041`, 2026-11-13 | PASS | The four strict document validators exit 0 with output equal to the before run at `43658eaa`. Fragment search outside `docs/98.archive/`: 69 lines before, 71 after; the difference is exactly the nine repointed links (`#requirements` three times, `#exceptions` six times) plus two lines of this package's own Spec and Plan text; all 47 parsed fragment links resolve to an existing heading or anchor. `quality.py` PASS; markdownlint over the edited Markdown 0 issues; `ruff check scripts tests` and `ruff format --check scripts tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 490, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` not re-run in this package (known default-branch error, SPEC-0161 W03-H11). `.secrets.baseline` registry `source_revision` line 6753 moved to 6924 in `0d1d0041`. | yes | none |
| EVD-007 | [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 30 files over `0d1d0041` | PASS | Risk class `medium` (registry, one registry rule, tests, nine governance policies agents load and five operations policies). Checklist: scope matches the Spec; one writer per file; the form equals the external contract; W03-D06 map applied; `REGISTRY_POLICY_ROLE` unchanged and strict; the body contract reads its table under Ownership; old H3 anchors keep their slugs and the nine H2 anchors are repointed; provider gateways read these files whole, not by heading; policy text `document-authoring.md` forms sentence and `docs/99.templates/README.md` 0.25.0; templates keep their frontmatter placeholder; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |
| EVD-008 | [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 exit authority; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-POLICY-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0175 criterion question, which listed the five placement calls of EVD-005) | platform |
| [VAL-POLICY-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0175 criterion question, which listed the five placement calls of EVD-005) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document authoring policy, the registry and `scripts/document_contracts.py` (Plan Promotion row). No new handoff arises; the Plan part of W03-H10 stays with phase 3 in the SPEC-0161 Task. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. Registry text, code comments and test docstrings name SPEC-0175 as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's explicit 2026-11-13 answer "Exit, push and PR" is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); implementation commit `7c6a35f0`. The user accepted both criteria and the package exit on 2026-11-13 (EVD-008). Risk class `medium`. Next owner: W03 for the AGENTS package.
