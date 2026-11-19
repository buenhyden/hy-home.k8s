---
title: "Workspace Path Cutover"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0224-TSK-0001"
parent_ids: ["SPEC-0224-PLAN-0001"]
---

# Task: Workspace Path Cutover

## Scope

### Objective and Parent

This Task runs the [Plan](../plan.md) for the [Spec](../spec.md): it moves the
W documents to `docs/00.workspace/`, splits SAFE and GIT along their W and A
rule lists, numbers the category folders of `docs/` and updates every
consumer, serving VAL-CUTOVER-001 to VAL-CUTOVER-003.

### Inputs and Authority

On 2026-11-19 (Asia/Seoul) the user asked to apply the governance redesign
package `_workspace/governance-redesign-2026-11-19-v2/` (local, untracked) to
this checkout, to finish the allowed local implementation and verification,
and not to push, merge, deploy, rewrite history or reset IDs. The local Q07
residue rows SDLC-H01 and DOC-H01 hold the user's earlier adoptions of the
target. Input revision: `4b2b670d` on branch `claude/q07-workspace-cutover`.

- **Allowed Paths**: `docs/` except `docs/98.archive/`, `.agents/governance/`, `.agents/knowledge/`, `scripts/`, `tests/`, tracked files that link a moved path
- **Forbidden Paths**: `docs/98.archive/`, `_workspace/` contents, `.workspace-memory/`, `sessions/`, historical bodies beyond link destinations
- **Approval Required**: the user's approval of this Spec and Plan; push, pull request and merge stay with the user
- **Static Validation**: `python3 scripts/qa.py staged` on the pinned `hyhome-validation` venv
- **Live Validation**: not applicable; no runtime, cluster or provider change
- **Secret / Vault Handling**: no secret is read; `.secrets.baseline` keeps its entries
- **Rollback Plan**: revert the cutover commit
- **Evidence Location**: this Task

## Execution Log

### Work Performed

| Item | Work Unit | Owner | Status | Blocker |
| --- | --- | --- | --- | --- |
| WORK-001 | WORK-001 | platform | completed | none |
| WORK-002 | WORK-002 | platform | completed | none |
| WORK-003 | WORK-003 | platform | completed | none |

A one-time script outside the tree ran `git mv` for 152 tracked files and
recomputed relative links and repository-root path strings, protecting
`commit:path` references and URLs. Published reference members, accepted ADR
bodies, the REQ-0003 Archived Lineage and the SPEC-0223 Task were then
restored from `4b2b670d` with link destinations recomputed only.

WORK-001 split approval and safety and Git: the W halves moved to
`docs/00.workspace/04.quality/approval-and-safety.md` and
`docs/00.workspace/03.process/git.md`, and the A halves stay at their
`.agents/governance/` paths. The registry `policy_rule_ids` lists the rule IDs
of each half, and the registry check refuses a rule ID with two owners, a
split record without its list and a foreign rule ID.

WORK-002 numbered the folders and updated profiles, schemas, readers and
tests. The lifecycle comparison first refused every move (LIFECYCLE-RENAME and
LIFECYCLE-CREATE). It now follows a Git-paired move whose profile and artifact
ID are unchanged, recomputes base link destinations for the move, and lets the
new half of a registered split continue the original policy (DOCLIFE-R023). A
regression first passed a rename that changed ADR-0998 to ADR-0999; the
artifact ID guard made it fail again as required. The stage-path grammar
check stopped treating a heading anchor as part of a path.

On the user's follow-up request of 2026-11-19, WORK-001 also separated the
two architecture areas. Each ADR was assigned by the AD that traces it and by
its decision scope: sixteen work-system ADRs (0030, 0031, 0033, 0036, 0047,
0048, 0052, 0053, 0055 to 0057 and 0059 to 0063) moved beside ADR-0058 with
link destinations recomputed only, and the platform ADRs and AD-0004, AD-0005
and AD-0007 stayed. The stage gained `AGENTS.md`, `CLAUDE.md` and a README for
each category; `docs/AGENTS.md`, the product architecture README and
`AGENTS.md` and both decision indexes state the split. The repository quality
check now scans `docs/00.workspace/` for unmarked commands, which made SAFE-R013
name its operator approval route, and `.secrets.baseline` follows the moved
files with the same 17 findings.

WORK-003 points the knowledge check at the workspace glossary; its regression
failed (21 failures) before the change and passes after.

A read-only code-reviewer sub-agent in a separate context reviewed the
validator changes (EVD-006). It reported three FIX findings, all applied: an
ID-less pair that Git matched by similarity could pass as a move, so a move
now also keeps its file name; a split half could inherit any policy, so the
base registry must have held the code once at the original path and the half's
rule IDs must be Rules rows of the original; and one moved file could redirect
links to unmoved siblings, so a folder maps only when every base file under it
moved with it. Regressions for the three guards fail against the `4b2b670d`
validator and pass after (EVD-007, EVD-008). Its NOTE findings stay as stated
limits: a bare path token's anchor is not validated by the stage-path grammar
check, and link rewriting in the base comparison also applies inside code
fences.

### Blockers and Decisions

On 2026-11-19 the user approved the Spec and Plan (EVD-011) and accepted
ADR-0064 (EVD-012), each over the reviewed bytes of commit `8557aa8e`.
Criterion acceptance stays a separate decision.

### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [VAL-CUTOVER-001](../spec.md#criteria) | PASS | EVD-002, EVD-011, EVD-012 |
| WORK-002 | [VAL-CUTOVER-002](../spec.md#criteria) | PASS | EVD-003, EVD-008 |
| WORK-003 | [VAL-CUTOVER-003](../spec.md#criteria) | PASS | EVD-004, EVD-010 |

## Verification Evidence

### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CUTOVER-003](../spec.md#criteria) | WORK-003 | automated | `tests/test_validate_knowledge_surface.py` with the glossary at its new path and the old validator | pinned `hyhome-validation` venv | `python -m unittest tests.test_validate_knowledge_surface` | 1 | FAIL | 21 failures: the validator read no glossary | false | none |
| EVD-002 | [VAL-CUTOVER-001](../spec.md#criteria) | WORK-001 | automated | Working tree on `4b2b670d` plus the cutover | pinned `hyhome-validation` venv | `python -m unittest tests.test_policy_rule_ids` and `python3 scripts/validate-document-contract-registry.py --root . --mode strict` | 0 | PASS | this Task | true | none |
| EVD-003 | [VAL-CUTOVER-002](../spec.md#criteria) | WORK-002 | automated | Staged cutover index against `4b2b670d` | pinned `hyhome-validation` venv | `python3 scripts/validate-document-lifecycle.py --root . --mode strict`, `validate-links-and-owners.py` and `validate-markdown-profiles.py` in strict mode, and every module of the document, document-lifecycle and tooling suites | 0 | PASS | this Task | true | none |
| EVD-004 | [VAL-CUTOVER-003](../spec.md#criteria) | WORK-003 | automated | Same input as EVD-001 after the change | pinned `hyhome-validation` venv | `python -m unittest tests.test_validate_knowledge_surface` | 0 | PASS | this Task | true | none |
| EVD-005 | [VAL-CUTOVER-003](../spec.md#criteria) | WORK-003 | automated | Staged cutover index against `4b2b670d` | pinned `hyhome-validation` venv | `python3 scripts/qa.py staged` | none | NOT_RUN | pending the final staged run | true | none |
| EVD-006 | [VAL-CUTOVER-002](../spec.md#criteria) | WORK-002 | review | `git diff HEAD` of the lifecycle, contract, profile and link validators on the cutover branch | read-only code-reviewer sub-agent, separate context | Independent semantic review | none | FAIL | this Task; three FIX findings (ID-less similarity pair, unverified split origin, broad folder map), five NOTE findings | false | none |
| EVD-007 | [VAL-CUTOVER-002](../spec.md#criteria) | WORK-002 | automated | `RelocationGuardTest` and the relocation case of `CumulativeLifecycleHistoryTest` against the `4b2b670d` validator | pinned `hyhome-validation` venv | `python -m unittest tests.test_document_lifecycle_cumulative_history -k relocation -k Relocation` | 1 | FAIL | one failure and three errors: moves refused, guard helpers absent | false | none |
| EVD-008 | [VAL-CUTOVER-002](../spec.md#criteria) | WORK-002 | automated | Same tests after the three fixes, and the whole module | pinned `hyhome-validation` venv | `python -m unittest tests.test_document_lifecycle_cumulative_history` | 0 | PASS | this Task | true | none |
| EVD-009 | [VAL-CUTOVER-003](../spec.md#criteria) | WORK-003 | automated | Staged cutover index against `4b2b670d`, including the workspace architecture split | pinned `hyhome-validation` venv | `python3 scripts/qa.py staged` | 1 | FAIL | 23 of 24 gates PASS; `selected-nonstyle` fails because detect-secrets reads the trusted HEAD `.secrets.baseline`, which names the pre-move paths of 17 unchanged findings. Stage 99 rule 6 needs the baseline commit first | true | none |
| EVD-010 | [VAL-CUTOVER-003](../spec.md#criteria) | WORK-003 | automated | Exact index of commit `8557aa8e` on `0806c3b0`, whose `.secrets.baseline` names the moved paths | pinned `hyhome-validation` venv; the `staged-qa` pre-commit hook | `python3 scripts/qa.py staged` | 0 | PASS | commit `8557aa8e`; every selected gate, `selected-nonstyle` included, passed in the hook | true | EVD-005, EVD-009 |
| EVD-011 | [VAL-CUTOVER-001](../spec.md#criteria) | WORK-001 | observation | {"actor": "user", "approval_ref": "user message of 2026-11-19 in this session, after reviewing the committed package, asking to proceed with the Task evidence, the approval, the post-approval residue cleanup and the worktree cleanup", "review_ref": "the user's own review of commit 8557aa8e", "scope": ["SPEC-0224", "SPEC-0224-PLAN-0001"], "reviewed_spec_sha256": "4ae07f633c01a4013e513f7e941d7c72e4e6d064250e80eaab6ed36ecc931155", "reviewed_plan_sha256": "4e6f6a45ace0569d510a983b88574fde0b475f036ca9449b0c556db07eaa996f", "validity": "confirmed", "revocation": "none"} | none | Spec/Plan approval | none | PASS | this Task | true | none |
| EVD-012 | [VAL-CUTOVER-001](../spec.md#criteria) | WORK-001 | observation | {"actor": "user", "approval_ref": "user message of 2026-11-19 in this session, after reviewing the committed package, asking to proceed with the Task evidence, the approval, the post-approval residue cleanup and the worktree cleanup", "scope": ["ADR-0064"], "reviewed_adr_sha256": "9a6012f505b7eb40fde85a452fd40aa94e3d3161ee84cd6eb052d88ec4cf12c5", "validity": "confirmed", "revocation": "none"} | none | ADR acceptance | none | PASS | this Task | true | none |
| EVD-013 | [VAL-CUTOVER-003](../spec.md#criteria) | WORK-003 | observation | PR #327 head `46cd0039` against `main` `4b2b670d` | GitHub Actions `ci.yml` on `pull_request` | `ci-summary` and `style-pr` jobs of run 44519130779 | 0 | PASS | https://github.com/buenhyden/hy-home.k8s/actions/runs/44519130779; both required checks passed and PR #327 merged as `0336e77c` without administrator bypass | false | none |

### Resolution Links

EVD-010 resolves EVD-005 and EVD-009. EVD-001, EVD-006 and EVD-007 are non-required observations followed by EVD-004 and EVD-008.

### Residue Handoff

| ID | Residue | State | Owner | Resume condition | Closure |
| --- | --- | --- | --- | --- | --- |
| DOC-H01 | No legacy row: the DOC-PATH-PLAN path plan, adopted by the user on 2026-11-19 (SDD-PATHS), with its hand-edit consumers and preconditions (SPEC-0161 EVD-212, moved from the SPEC-0223 Task). The category moves and the W owner moves ran in this package (EVD-010); the document ID renumbering and the Stage 98 disposal remain for the cutover, after a full validator run on a copy | open | Q07 | In the Q07-CUTOVER task, after every package is closed and Q07-H01 is converted | none |
| SDLC-H01 | No legacy row: the user adopted `docs/00.workspace/` as the physical owner of the W layer on 2026-11-18 and chose to move it once with the final path cutover (SPEC-0161 EVD-209, moved from the SPEC-0223 Task). This package moved the W rows of the SDLC-R036 table and split approval and safety and Git along their rule lists, with routers, validators, registry routes and links in one change | terminal | Q07 | In the Q07-CUTOVER task, together with the SDD-PATHS renumbering | EVD-010 |

## Acceptance Decision

### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [VAL-CUTOVER-001](../spec.md#criteria) | accept | accepted | EVD-002, EVD-011, EVD-012 | User message of 2026-11-19 in this session accepting VAL-CUTOVER-001 to VAL-CUTOVER-003 | user | platform | none |
| [VAL-CUTOVER-002](../spec.md#criteria) | accept | accepted | EVD-003, EVD-008 | User message of 2026-11-19 in this session accepting VAL-CUTOVER-001 to VAL-CUTOVER-003 | user | platform | none |
| [VAL-CUTOVER-003](../spec.md#criteria) | accept | accepted | EVD-004, EVD-010 | User message of 2026-11-19 in this session accepting VAL-CUTOVER-001 to VAL-CUTOVER-003 | user | platform | none |

### Remaining Conditions

The user accepted VAL-CUTOVER-001 to VAL-CUTOVER-003 on 2026-11-19.
SDLC-H01 is terminal here (EVD-010); DOC-H01 stays open here for ID
renumbering and Stage 98 disposal under Q07-CUTOVER, so this package remains
the host of that residue. Push and pull request stay with the user.

## Handoff

### Promotion Receipt

Document move rule: DOCLIFE-R023 is in force in the
[document lifecycle policy](../../../00.workspace/03.process/document-lifecycle.md#rules).

### Next Owner

Every item is completed with PASS evidence and an accepted criterion; the
local staged QA of each commit passed, and no hosted, provider or cluster check ran (not in scope). The user
owns criterion acceptance, push and pull request. Q07-CUTOVER keeps DOC-H01
(document ID renumbering and Stage 98 disposal) after Q07-H01.
