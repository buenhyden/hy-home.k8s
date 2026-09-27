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

Single execution evidence owner for external research refresh, document integration, ordered validation and local commits under the direct user request dated 2026-09-27. The initial queued boundary was committed before authoring. The Spec/Plan remain active and this Task remains in progress. Member authoring, integration and the historical-prose English translation review are complete. Corrected quick, research exact-index staged QA and actual-message validation passed, and the research was committed. Final full QA failed three required gates, so overall acceptance remains incomplete. This Task records the bounded failure handoff; its evidence commit remains pending.

## Inputs

- [Spec](../spec.md) and [Plan](../plan.md).
- [Existing research pack](../../../90.references/research/0001-workspace-engineering/README.md); origin/main baseline `fc469fd139e6b92d98cc8aabeb3f3e7141f18a54`.
- User attachment requesting the hy-home.k8s external research refresh and single Research Pack maintenance, including U01–U39, topic detail, source contracts and retained branch/worktree finish selection.
- Current Stage 99 profiles/forms and common authoring, lifecycle, quality, Git and delegation procedures. These are authoring inputs, not targets of a conformance audit.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-WER-001 | Establish canonical execution scope and routing | integration owner | Done | Bootstrap commit 64685d5fda7faf40b2c8ed294ba4e53355baa156 validated and independently reviewed | Spec, Plan, Stage 03 routing |
| WORK-002 | VAL-WER-002, VAL-WER-003 | Research topic details using primary external sources | researchers | Done | Three independent research groups returned primary-source packets integrated into the pack | Assigned m0001–m0011 evidence |
| WORK-003 | VAL-WER-001, VAL-WER-003, VAL-WER-005 | Author member bodies after source handoff | doc writers | Done | Eleven topic members authored and independently reviewed; historical-prose English translation rereview PASS | Member source records and dispositions |
| WORK-004 | VAL-WER-002, VAL-WER-004, VAL-WER-005 | Integrate U coverage, scope questions and navigation | integration owner | Done | Central coverage/questions and three navigation files integrated and corrected; historical-prose translation reviewed | README, m0012 and m0013 |
| WORK-005 | VAL-WER-006 | Review and validate each coherent local commit | independent reviewer / integration owner | In progress | Research review, corrected quick and research staged/message passed; final full FAIL keeps VAL-WER-006 incomplete | Exact snapshot command results and Git |
| WORK-006 | VAL-WER-006 | Close acceptance and preserve branch/worktree handoff | integration owner | In progress | Failure handoff documented; final acceptance remains incomplete and Task-only evidence validation/commit pending | This Task |

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

Tool identities reported by integration: Python 3.12.3, Git 2.43.0, pre-commit 4.6.1 and RTK 0.49.0. All following results are repository-static; hosted CI, provider-runtime and live evidence are DEFER because those investigations were excluded.

| Lane / step | Exact command or checked scope and result | Limitation / disposition |
| --- | --- | --- |
| Baseline | Origin/main fc469fd139e6b92d98cc8aabeb3f3e7141f18a54; branch codex/research-refresh | Original checkout/index preserved; no baseline full replay was performed |
| Targeted baseline | PASS — bounded affected validation over a NUL list of all 14 unchanged pack Markdown files at the baseline; six selected gates | Static authoring baseline only |
| Acceptance baseline | Expected RED — all U01–U39 individual rows absent from baseline m0012; diagnostic exited 0 | Requested coverage deficit, not document gate failure |
| First quick | FAIL — `python3 scripts/qa.py quick --root . --base-ref HEAD`; bootstrap HEAD plus 19 changed files; manifest SHA-256 ae7907e015924ae26a11d22ca9be56738d7b4a31eb3a943aa297d6050834bef9; five PASS, LANG-ENGLISH-FIRST FAIL | Moved historical Korean README prose translated without changing meaning/IDs/dates/anchors |
| Corrected quick | PASS — same quick command; bootstrap HEAD plus 19 changed paths; manifest SHA-256 05123ef722d7311109fe616e9e4b7d466287061c149a70ec6b7da6291ccd6a65; all six selected gates | Subsequent Task evidence bytes were included in research staged/full checks |
| Bootstrap staged / message | PASS — six exact-index gates and actual-message Commitizen; commit 64685d5fda7faf40b2c8ed294ba4e53355baa156 | Initial scoped contract, not final research acceptance |
| Research staged / message | PASS — `python3 scripts/qa.py staged --root . --base-ref HEAD` over 19 staged paths; exact tree 3ce250eaf428db504f3ef07051571e466fae6e02; all six selected gates; Commitizen actual-message PASS | Research commit 915c9a95a603cab6789ab641d922c8ce7c16ed3f |
| Final full | FAIL — `python3 scripts/qa.py full --root . --base-ref HEAD` on clean research commit 915c9a95a603cab6789ab641d922c8ce7c16ed3f; 22 gates / 1,224 all-files paths; 19 PASS and three FAIL | Required archive-cutover, unit-tests and pre-commit failures below keep VAL-WER-006 and overall acceptance incomplete |
| Independent reviews | PASS — review_bootstrap; review_research found no open VAL-WER-001–005 findings; bounded English-translation rereview PASS | Reviews do not override failed required full QA |
| Final Task focused evidence | FAIL — `python3 scripts/run-validation-lane.py --root . --lane affected --paths-file /tmp/research-refresh-handoff-target.nul --delimiter nul` over the single Task path; five gates PASS, links-and-owners FAIL with WORK-054 WP-004B migration recovery proof differs | Direct worktree proof class previously passed in isolated QA; this failure is not declared resolved. Subsequent precision edits require exact-index staged validation; actual-message/commit pending, no self-SHA |

### Resolved authoring failures and reviewed coverage

Initial direct targeted checks failed on dirty reference-pack/index drift, historical recovery proof and a forbidden host-path field. Scoped documentation corrections and isolated bootstrap/index checks resolved those findings without rewriting history or weakening validators. The delegated seven-file affected run later passed governance, lifecycle and Markdown profiles but failed dirty reference index/proof checks and two upstream script names parsed as local executable history. Pinned external links resolved the author-owned ambiguity; corrected integrated quick and research staged checks passed all six selected gates. The first quick language failure was resolved by translation, targeted m0012 Markdown PASS and independent translation rereview PASS.

The research review checked diff SHA-256 edd34196a5a6ad06b99f252f27a3a1a0f0f525772ef93b811803930280bb9bd5. Translation rereview checked m0012 SHA-256 fee0e6235865914372eed4c2a7763aeb4e47a5e731e09196e2120a6e3834c1b2 and historical-section SHA-256 8a7aae489342fbc9d3a4372f424db6654b14625680c53959db71e13ec58b9216. The SRC-WERPC-014→CLM-WERPC-017-42 support edge missing after first quick was corrected and reviewed before corrected quick. Nineteen-path scope and whitespace checks passed; the original checkout remained clean.

All 36 historical REQ IDs, 154 SRC IDs and 181 CLM IDs remain. m0012 maps 39 individual U aliases, 127 current claims and 186 URL records; m0013 supplies 114 follow-up questions with twelve evidence-contract fields. These describe this delivered research snapshot, not permanent policy inventories or workspace assessments. VAL-WER-001–005 have authored/reviewed evidence; VAL-WER-006 is incomplete because final full failed.

### Final full failures and bounded diagnostics

The final full raw-log SHA-256 is d8f396bcef00a96b7f021a1dadabe63a37f995014f94efefbaf1dc9d7082cb75. The command, snapshot, required gate failures and bounded diagnostics are retained here so the task-owned temporary log can be removed without treating raw output as a second evidence owner.

- **Archive-cutover FAIL:** ARCHIVE-CUTOVER-INCOMPLETE and ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE at the Archive README. No archive body/index repair or classifier bypass was attempted.
- **Unit-tests FAIL:** four assertions failed and four tests were skipped. The Gitleaks assertion failures were `test_public_document_terms_do_not_exempt_other_secret_matches` and `test_snapshot_secret_scan_covers_clean_history_and_hidden_files`; both failed before fixtures/scans. The four skipped tests’ identities and reasons were not exposed in the aggregate log, so they are not invented here. `test_escaped_descendant_is_failed_without_post_reap_group_signal` did not raise the expected ProcessLookupError; `test_file_reader_rejects_changes_during_read` did not raise the expected BoundedInputError. Independent review found the escaped-descendant case uses a 0.2-second cleanup deadline and cannot distinguish a live PID from a zombie through its existence check. Timing/load/platform or implementation cause remains unknown. The bounded-read case overwrites equal-length eight-byte content and relies on device/inode/mode/size/mtime/ctime detection; unchanged/coarse timestamps are a possible explanation, not a proven cause, and no filesystem probe was performed.
- **Pre-commit FAIL:** required executable unavailable to the full lane's trusted resolver, so the all-files hook was not executed. Shell discovery of pre-commit was true while trusted resolution was none; Gitleaks was not found by shell discovery and was not accepted by the trusted resolver; this proves neither physical absence nor a specific resolver rejection reason. An installed/discoverable shell command therefore did not satisfy this lane's trusted-tool contract.

Independent read-only comparison confirmed the three failed-test files, QA/runner implementation, bounded_io.py, Gitleaks configuration and pre-commit configuration have identical Git blobs at baseline fc469fd139e6b92d98cc8aabeb3f3e7141f18a54 and research 915c9a95a603cab6789ab641d922c8ce7c16ed3f. The two Gitleaks tests fail at required-tool assertions before fixtures/scans, leaving scan behavior untested. The synthetic timing fixtures do not read research documents; no causal evidence links their failures to these documentation changes. This does not prove a pre-existing baseline full failure: baseline full was not replayed, and timing-dependent failures are unresolved. No tools were installed, no global/private configuration changed, no gates weakened, and no identical full/unit/pre-commit rerun was performed. Required failures remain FAIL, not SKIP/PASS. Next owners are repo-tooling-engineer and quality-engineer for separately authorized tool-environment preparation and failed-test triage, using the independent reviewer’s bounded classification above. Fresh full evidence requires a relevant environment or reviewed change and separate authorized scope; the research request does not authorize implementation repair.

### Retained branch and failure handoff

The single existing pack keeps all member identities and current external synthesis first, with preserved historical observations. Eleven topic reports were substantively refreshed; README ledgers were consolidated into m0012, scope questions into m0013, and three existing README routes updated. No new pack/member, implementation change, source-truth policy, runtime experiment or external state write was introduced. m0012's current source/claim/coverage/disposition sections and m0013's follow-up ledger are the investigation entrypoints; every current workspace result is `not observed in this cycle`.

Important external corrections distinguish Spec Kit implementation from an SDLC standard, AD from legacy ARD history, C4 containers from Docker, native agent configuration from permission enforcement, and external maintained-wiki proposals from the retired local generated map. Agency Agents uses a fresh inspected pin while preserving earlier pin disagreement; product limits and costs stay dated and product-specific. Residual limits include paid standards abstracts rather than normative clauses, mutable pages without exact revision/publication metadata, unresolved immutable gist revision/license, RAG abstract-only evidence, anecdotal wiki scale, account-specific prices/entitlements and unobserved adoption/runtime outcomes. Document QA does not certify these claims or deployment safety.

Committed recovery points are bootstrap 64685d5fda7faf40b2c8ed294ba4e53355baa156 and research 915c9a95a603cab6789ab641d922c8ce7c16ed3f. The research worktree was clean before this Task-only evidence update. The evidence commit and its final Git status will be reported by integration after the recorded focused result and pending staged/message checks; this document does not embed its own future SHA. Keep branch codex/research-refresh and the research worktree. No push, PR, merge, branch/worktree removal, secret collection or provider/live action occurred. Bounded rollback is a reviewed forward reversal of only these task-owned logical commits/paths, preserving unrelated work; never reset, amend, rebase or blanket clean.

Execution evidence is preserved here before deletion of explicitly enumerated task-owned scratch. Scratch logs are not durable authority. The user/operator owns later investigation scope and default-branch integration; repo-tooling-engineer/quality-engineer own the separately scoped QA follow-up. Overall acceptance remains incomplete and is not reported as done.

### Legal closure and retained execution state

Spec/Plan remain active and Task remains in progress. Required full QA failed, so completion is not legal. Additionally `done` is terminal in the registry and requires whole-package Stage 98 disposition whose source object is reachable from the default branch. Stage 98 writes and push/merge are outside this request; terminal disposition remains DEFER to authorized post-integration lifecycle work. Preserved failure handoff neither closes acceptance nor grants archive authority.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WP-001](../plan.md#work-breakdown) | Bootstrap exact-index QA/message/review PASS; committed 64685d5fda7faf40b2c8ed294ba4e53355baa156 | [VAL-WER-001](../spec.md#success-criteria--verification-plan) |
| [WP-002](../plan.md#work-breakdown) | Primary-source research packets integrated and independently reviewed; translation rereview PASS | [VAL-WER-002](../spec.md#success-criteria--verification-plan), VAL-WER-003 |
| [WP-003](../plan.md#work-breakdown) | Member authoring and independent review complete; historical-prose translation rereview PASS | [VAL-WER-003](../spec.md#success-criteria--verification-plan), VAL-WER-005 |
| [WP-004](../plan.md#work-breakdown) | Coverage, questions and navigation integrated and corrected; translation rereview PASS | [VAL-WER-004](../spec.md#success-criteria--verification-plan), VAL-WER-002, VAL-WER-005 |
| [WP-005](../plan.md#work-breakdown) | Research/translation review, corrected quick and research staged/message PASS; research committed; final full FAIL, VAL-WER-006 incomplete | [VAL-WER-006](../spec.md#success-criteria--verification-plan) |
| [WP-006](../plan.md#work-breakdown) | Failure handoff recorded; Task evidence checks/commit pending; overall acceptance incomplete | [VAL-WER-006](../spec.md#success-criteria--verification-plan) |
