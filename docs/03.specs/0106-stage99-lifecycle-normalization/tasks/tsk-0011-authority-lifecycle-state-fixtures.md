---
title: "Authority Lifecycle State Fixtures"
version: "1.0.2"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0011"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Authority Lifecycle State Fixtures

## Overview

Adjust three test prerequisites to the published role vocabularies. The required
body-maintenance and reciprocal-evidence behavior is unchanged.

## Inputs

- [Spec VAL-P02-011](../spec.md#success-criteria--verification-plan) and
  [Plan WORK-011](../plan.md#work-breakdown).
- The accepted [Task0010](tsk-0010-completed-state-and-navigation-fixtures.md)
  endpoint and the next executed PR133 run 37387514174, failed job 112024384725.
  Unit-tests failed; document-lifecycle and pre-commit reported PASS. The displayed
  preview is capped and supplies no exhaustive unittest summary.
- Independent review read all twelve methods in the implicated authority class.
  Three named REDs confirm invalid Spec active prerequisites and a reference
  completed state wrongly expected to exercise noninitial publication.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-011 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | Align authority state fixtures with their published roles | platform | frontmatter | PASS | accepted | Observed focused checks, implementation-index checks and independent audits in EVD-P02-111/112 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-110 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | WORK-011 | Three named REDs and independent diagnosis | Unchanged Task0010 endpoint; bounded individual invocations | FAIL | External `hy-p01-7959d52f-named-red.receipt.json` and causes receipt; `/root/p02_independent_review` | rejected |
| EVD-P02-111 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | WORK-011 | Three final-byte focused methods, pinned hooks and independent raw audit | Fixture SHA256 `63178dfe02fb27cd214e4ed452fea6e5139632002775b283e3b2307d9dc94d97` | PASS | External `hy-p01-task11-focused.receipt.json` and `hy-p01-task11-hooks.receipt.json` | accepted |
| EVD-P02-112 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | WORK-011 | Observed draft, ready and implementation actual-index checks and final independent audits | Accepted three logical indices, changed Task Markdown and exact messages | PASS | External `hy-p01-task11-c1-staged.receipt.json`, `hy-p01-task11-c2-staged.receipt.json`, `hy-p01-task11-c3-staged.receipt.json` and corresponding Markdown/message receipts | accepted |
| EVD-P02-113 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | WORK-011 | Observed prospective scoped completion and independent raw audit | Isolated same-base/config closing proposal only; own actual closing checks pending | PASS | External `hy-p01-task11-c4-proposal-completion.receipt.json` | accepted |
| EVD-P02-114 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | WORK-011 | Registered-form cached and committed source metadata | C010 from unchanged declared regular form; target absent before draft | PASS | Ignored `p01-task11-c1-template-rewrite-preflight.json`, full metadata and `p01-task11-c1-postcommit.json` | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/plan.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0011-authority-lifecycle-state-fixtures.md`,
  `tests/test_document_lifecycle_archive_cutover.py`.
- **Forbidden Paths**: Every production contract, security/trust setting,
  frozen Archive unit, completed document and unrelated file.
- **Approval Required**: The explicit commit/push/merge request and scoped
  four-path delegation cover these fixtures. Existing conditional closing
  permission requires prospective review/completion followed by actual checks
  and separate final review before commit. Hosted protection still governs merges.
- **Static Validation**: Three existing named methods with current-state,
  publication and reciprocal boundaries, each within sixty seconds; scoped
  pinned hooks; fresh staged and exact message checks plus independent review
  for every logical index. Local full/affected execution is excluded.
- **Live Validation**: DEFER; repository evidence does not establish live readiness.
- **Secret / Vault Handling**: Public fixture inputs only; retain raw CI diagnostics
  privately and report safe classifications without credential access.
- **Rollback Plan**: A reviewed forward correction preserves the existing history;
  destructive Git operations and provenance exceptions are outside this Task.
- **Evidence Location**: Execution facts belong here. External raw receipts and
  ignored proposal scratch retain tested identities without embedding this
  document's own future commit identity.

## Verification Summary

The intake establishes three prerequisite failures, not a production defect.
Keep maintenance at draft/in-progress/completed, audit draft admission with
active/completed STATE and published CREATE refusals, and approved supersession
with missing EVIDENCE versus exact reciprocal acceptance.

The first uncommitted draft's actual source metadata was C012 from Task0010 and
did not qualify as registered-form creation. Its bytes and preflight remain in
ignored `p01-task11-c1-ordinary-copy-candidate.md` and
`p01-task11-c1-creation-preflight.json`. The concise canonical replacement's
cached and committed metadata is C010 from the declared Task form. Its regular
source is unchanged before and after creation, and the new target was absent.

The draft index separately passed six fresh canonical gates and its exact
configured message, with complete streams/cleanup and stable source/index/refs.
Independent final raw audit preceded the normal draft commit. Copied message
configs and captured disposable semantic entries matched; raw disposable index
bytes changed with unknown cause and were not an acceptance prerequisite.

Readiness uses the ignored three-method `p01-task11-focused-manifest.json` and
four-path `p01-task11-selection.json`: seven validators, unmatched zero, selection
only. No full/affected execution occurred. The ready index separately passed
six fresh gates and its configured exact message; independent final raw audit
preceded its normal commit, with stable source/index/refs and complete cleanup.

The three fixture prerequisites now use their declared states without changing
the refusal assertions. Pinned Ruff check, Ruff format and detect-secrets passed
on exact-byte disposable copies before focused execution; no formatter delta
occurred. All three named methods then passed within their sixty-second bounds.
Independent raw audits accepted focused receipt SHA256
`8c6822e517a77bf9508421cb2396527373474a1c36b451f05e5fb879d34d7de5`
and hook receipt SHA256
`4ededcf10cb0e425f85df1fb387c96bfde16a432ce58ac35f039bce4aff0d088`.
The implementation index then passed its changed Task Markdown, seven fresh
canonical gates and exact configured message. Independent final raw audit
preceded the normal implementation commit; all streams and cleanup completed
with stable source/index/refs. EVD-P02-112 records those observed checks.

The isolated nonauthoritative same-base/config proposal separately passed
SPEC0106-only completion and independent semantic/raw review. Receipt SHA256
`a0960bef428b11215d3f323570289a7ea5ff34182be850765bf9719739daa97c`
records snapshot
`681cf552f3f17ab2d9a4b790bb29df813e86aaeb69677fb28d147480c6ca0b73`,
complete streams/cleanup and unchanged clone/original identities. No proposal
staged run occurred; EVD-P02-113 accepts that prospective lane only.

This conditional actual closing candidate accepts the observed implementation
and prospective results. Its own actual staged, scoped completion, exact message
and final independent review are NOT_RUN/pending and must all pass before the
normal closing commit. Their eventual raw receipts remain external rather than
being inserted into this same input. Final hosted PR and integrated-main results
remain separate from every local observation.
