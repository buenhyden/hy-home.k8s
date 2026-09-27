---
title: "Refresh External Workspace Engineering Research"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0099-TSK-0001"
---

# Task: Refresh External Workspace Engineering Research

## Overview

Single execution evidence owner for external research refresh, document integration, ordered validation and local commits under the direct user request dated 2026-09-27. The initial queued boundary was committed before authoring. The Spec/Plan remain active and this Task remains in progress. Member authoring, integration and the historical-prose English translation review are complete. Corrected quick QA passed all six selected gates; research staged/message checks, final full, commit and handoff remain pending.

## Inputs

- [Spec](../spec.md) and [Plan](../plan.md).
- [Existing research pack](../../../90.references/research/0001-workspace-engineering/README.md); origin/main baseline `fc469fd139e6b92d98cc8aabeb3f3e7141f18a54`.
- User attachment requesting the hy-home.k8s external research refresh and single Research Pack maintenance, including U01–U39, topic detail, source contracts and retained branch/worktree finish selection.
- Current Stage 99 profiles/forms and common authoring, lifecycle, quality, Git and delegation procedures. These are authoring inputs, not targets of a conformance audit.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-WER-001 | Establish canonical execution scope and routing | integration owner | Done | Bootstrap commit 64685d5fda7faf40b2c8ed294ba4e53355baa156 validated and independently reviewed | Spec, Plan, Stage 03 routing |
| WORK-002 | VAL-WER-002, VAL-WER-003 | Research topic details using primary external sources | researchers | Done | Three independent research groups returned primary-source packets; integration remains a later work item | Assigned m0001–m0011 evidence |
| WORK-003 | VAL-WER-001, VAL-WER-003, VAL-WER-005 | Author member bodies after source handoff | doc writers | Done | Eleven topic members authored and independently reviewed; historical-prose English translation rereview PASS | Member source records and dispositions |
| WORK-004 | VAL-WER-002, VAL-WER-004, VAL-WER-005 | Integrate U coverage, scope questions and navigation | integration owner | Done | Central coverage/questions and three navigation files integrated and corrected; historical-prose translation reviewed | README, m0012 and m0013 |
| WORK-005 | VAL-WER-006 | Review and validate each coherent local commit | independent reviewer / integration owner | In progress | Research review and corrected quick passed; exact-index staged/message and final full pending | Exact snapshot command results and Git |
| WORK-006 | VAL-WER-006 | Close acceptance and preserve branch/worktree handoff | integration owner | Queued | Final full and handoff pending | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/90.references/research/0001-workspace-engineering/**`; `docs/90.references/research/README.md` and `docs/90.references/README.md` only when navigation changes; `docs/03.specs/0099-workspace-engineering-research-refresh/spec.md`, `plan.md`, `tasks/tsk-0001-refresh-external-research.md`; `docs/03.specs/README.md` solely for the new package route. Exact additional active link consumers require advance path/reason disclosure.
- **Forbidden Paths**: all policy/provider/agent/skill/hook/CI, infrastructure, application, manifest, script, test, template and validator changes; `docs/98.archive/**`; the separate research pack and any parallel authoring/ledger tree.
- **Approval Required**: direct user request already authorizes bounded research/edit/local commits. Scope expansion, runtime investigation, secret access, external state writes, push, PR, merge, history rewrite, destructive cleanup and branch/worktree removal are outside this authorization.
- **Static Validation**: targeted profile/link/lifecycle and scope review → quick affected working tree → every logical exact-index staged check and actual-message validation → final full. Commands and precise snapshots are recorded below when run; no assumed PASS.
- **Live Validation**: DEFER — workspace/provider-runtime/hosted CI/live investigations are excluded. All workspace research results are `not observed in this cycle`.
- **Secret / Vault Handling**: no private config, logs, memory, authentication or secret collection; no Vault/live contact.
- **Rollback Plan**: preserve branch/worktree; inspect exact branch-owned paths and reverse selected logical commits through reviewed forward commits, preserving unrelated work. No reset, amend, rebase or blanket clean.
- **Evidence Location**: this Task for execution; m0012 for source/claim/U mapping and dispositions; m0013 for follow-up scope questions; Git for committed recovery.

### Authorization and structure rulings

Exact execution-management paths and routing reason were disclosed before writes. Direct user authorization supplies the scoped approval; no new approval stop is inferred. Repository lifecycle overrides external skill suggestions for `docs/superpowers/` or duplicate ledgers. Existing pack and all thirteen member identities are retained. Research source assessment and document authoring remain separate responsibilities; integration owns shared IDs/navigation/coverage and commits. No current workspace verdict is derived from historical pack evidence or document QA. Git policy lookup identified an effective user-global hook directory; no private configuration contents were inspected or changed. The integration owner will validate the actual message with pinned pre-commit Commitizen before normal Git commit, preserving active hooks.

## Verification Summary

| Lane / step | Snapshot and result | Limitation / next owner |
| --- | --- | --- |
| Baseline | Origin/main `fc469fd139e6b92d98cc8aabeb3f3e7141f18a54`; branch `codex/research-refresh` in isolated research worktree | Original checkout/index preserved; integration owner records tool results |
| Targeted baseline | PASS — all 14 unchanged pack Markdown files at base fc469fd139e6b92d98cc8aabeb3f3e7141f18a54; validation runner affected lane with NUL-delimited target list | Six selected gates passed; integration owner holds command log. New package checks remain separate |
| Acceptance baseline | Expected RED — read-only individual-table-row check found all U01–U39 rows absent from m0012 at the base | Diagnostic process exited 0; this is unmet requested coverage, not a failed document-format gate. Final mapping/source/question review must prove GREEN |
| First quick | FAIL — `python3 scripts/qa.py quick --root . --base-ref HEAD` on bootstrap HEAD 64685d5fda7faf40b2c8ed294ba4e53355baa156 plus 19 changed files; manifest SHA-256 ae7907e015924ae26a11d22ca9be56738d7b4a31eb3a943aa297d6050834bef9; five gates PASS, markdown-profiles FAIL LANG-ENGLISH-FIRST | Resolved by English translation, targeted profile PASS, independent translation review PASS and corrected quick PASS |
| Corrected quick | PASS — `python3 scripts/qa.py quick --root . --base-ref HEAD`; HEAD 64685d5fda7faf40b2c8ed294ba4e53355baa156 plus 19 changed paths; manifest SHA-256 05123ef722d7311109fe616e9e4b7d466287061c149a70ec6b7da6291ccd6a65; all six selected gates passed | This subsequent Task-only evidence update changes bytes; research staged/full will validate them |
| Bootstrap staged / message | PASS — exact bootstrap index, six selected gates; Commitizen actual-message validation PASS; commit 64685d5fda7faf40b2c8ed294ba4e53355baa156 | Integrated research index/message checks pending |
| Final full | Pending | Full includes unit discovery and manual all-files pre-commit once |
| Independent bootstrap review | PASS — review_bootstrap on the initial contract commit | Bootstrap result does not replace research review |
| Independent research review | PASS — review_research found no open findings after corrections for VAL-WER-001–005; reviewed diff SHA-256 edd34196a5a6ad06b99f252f27a3a1a0f0f525772ef93b811803930280bb9bd5 | Bounded translation rereview PASS with no open findings; required staged/full/commit evidence for VAL-WER-006 remains pending |
| Hosted CI / provider-runtime / live | DEFER — excluded by user scope | No observed implementation outcome |

### Delegated author focused validation

The seven assigned documents passed focused content/date/ID preservation, eight-H2 order and `git diff --check`. The canonical affected runner over an explicit seven-path NUL list passed agent-governance, document-lifecycle and markdown-profiles. It returned FAIL for document-contract-registry on unstaged reference-pack index drift and for links-and-owners on WORK-054 migration recovery proof, the same dirty-tree class requiring the integrated exact-index snapshot rather than a policy or historical repair. Repository-quality returned FAIL for two current upstream script paths being parsed as local executable history; the author replaced those literals with pinned external links. The subsequent integrated quick run passed repository-quality and the other non-language gates; the earlier ambiguous executable-path failure is resolved. Corrected post-translation quick passed all six selected gates. No failure is promoted to PASS and no validator/history change is made.

### Bootstrap execution and active handoff

The initial direct targeted attempt returned FAIL on dirty README/index drift, historical proof and a forbidden host-path field. Those bootstrap defects were corrected within disclosed documentation scope; the isolated exact-index bootstrap passed all six selected gates. The baseline check passed all 14 unchanged pack files. Bootstrap staged QA, actual-message Commitizen and review_bootstrap passed before commit `64685d5fda7faf40b2c8ed294ba4e53355baa156`. These results do not replace integrated QA: the first quick run failed language validation and corrected quick passed; research exact-index staged/message and final full remain pending. No hook, provider or live behavior is inferred.

Research groups returned external evidence; doc writers own eleven topic members, the integrator owns two indices and the curator owns three README routes. All research members, shared IDs/coverage/questions, navigation and execution evidence form one coherent pending logical commit; topic-only partial commits would leave dangling shared relationships. The integration owner runs and records exact commands/snapshots, review, commits and final Git state. Branch/worktree remain retained; rollback is a reviewed forward reversal of these scoped commit paths. Residual risks include mutable external pages, paid-standard limits, unresolved historical pin disagreement and unobserved runtime/account outcomes. Next owner: integration supervisor and independent reviewer.

### Current integration and review evidence

Tools reported by the integration owner are Python 3.12.3, Git 2.43.0, pre-commit 4.6.1 and RTK 0.49.0. The first quick passed all gates except LANG-ENGLISH-FIRST on historical Korean README prose moved into English-first members. English translation preserved historical meaning, dates, identifiers and anchors. The targeted m0012 Markdown check then passed, and review_research's bounded translation rereview reported PASS with no open findings. Its m0012 SHA-256 was fee0e6235865914372eed4c2a7763aeb4e47a5e731e09196e2120a6e3834c1b2, with historical-section SHA-256 8a7aae489342fbc9d3a4372f424db6654b14625680c53959db71e13ec58b9216. The corrected quick recorded above passed agent-governance, document-contract-registry, document-lifecycle, links-and-owners, markdown-profiles and repository-quality; its execution log is `/tmp/research-refresh-quick2.log`. The nineteen-path scope check and diff whitespace check passed; the original checkout remained clean. These are repository-static results, not product or runtime evidence.

The reviewed integration retains all 36 historical REQ IDs, 154 SRC IDs and 181 CLM IDs. m0012 contains 39 individual U rows, 127 current claims and 186 URL records; m0013 supplies 114 follow-up questions with twelve evidence-contract fields. These are delivered mapping/inventory observations, not workspace assessments or permanent policy counts. The SRC-WERPC-014→CLM-WERPC-017-42 support edge corrected after the first quick is included in the corrected snapshot. This Task-only result update follows corrected quick; exact-index staged and final full must cover its subsequent bytes. Research staged/message/full/commit evidence remains pending, with no required failure promoted to PASS.

### Legal closure and retained execution state

Do not mark this package done before required final full QA passes. Even after execution evidence is complete, `done` is terminal in the registry and the lifecycle requires whole-package Stage 98 disposition with a source object reachable from the default branch. Stage 98 writes and push/merge are outside this request, and this research branch is not yet integrated. Accordingly Spec/Plan remain active and Task remains in progress; terminal disposition is DEFER to the owning lifecycle work after authorized default-branch integration. This state does not imply unfinished external research once its actual acceptance and QA evidence are recorded, and it does not authorize archive changes.

Final handoff must record actual baseline/branch, adopted structure, changed documents and reasons, U coverage, major external corrections and unresolved conflicts, scope question entrypoints, exact command/snapshot outcomes and limitations, reviewer identity/disposition, commit SHA/content list, final Git status, bounded rollback, residual research risks and next owner. Initial authoring is not the final handoff. Do not insert a self-referential final SHA or repeat full QA merely to rewrite timing metadata.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WP-001](../plan.md#work-breakdown) | Bootstrap exact-index QA/message/review PASS; committed 64685d5fda7faf40b2c8ed294ba4e53355baa156 | [VAL-WER-001](../spec.md#success-criteria--verification-plan) |
| [WP-002](../plan.md#work-breakdown) | Primary-source research packets integrated and independently reviewed; translation rereview PASS | [VAL-WER-002](../spec.md#success-criteria--verification-plan), VAL-WER-003 |
| [WP-003](../plan.md#work-breakdown) | Member authoring and independent review complete; historical-prose translation rereview PASS | [VAL-WER-003](../spec.md#success-criteria--verification-plan), VAL-WER-005 |
| [WP-004](../plan.md#work-breakdown) | Coverage, questions and navigation integrated and corrected; translation rereview PASS | [VAL-WER-004](../spec.md#success-criteria--verification-plan), VAL-WER-002, VAL-WER-005 |
| [WP-005](../plan.md#work-breakdown) | Independent research and translation reviews PASS; first quick language FAIL resolved by corrected quick six-gate PASS; staged/message/full/commit pending | [VAL-WER-006](../spec.md#success-criteria--verification-plan) |
| [WP-006](../plan.md#work-breakdown) | Final acceptance/handoff pending | [VAL-WER-006](../spec.md#success-criteria--verification-plan) |
