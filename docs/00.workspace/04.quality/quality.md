---
title: "Quality and Evidence Policy"
version: "4.1.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Quality and Evidence Policy

## 문서 개요

### 목적과 독자

Workers and reviewers use Quality and Evidence Policy for the rules in its stated scope.

### 책임과 적용 범위

The policy's coverage is defined in [Purpose and Scope](#purpose-and-scope) and [Applies To](#applies-to).

## 내용 계약

### 입력과 전제

Read the current request, owner and rule conditions before applying this policy.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Report exactly what was checked, over which bytes and scope, and with which
limitations. Passing a local command is not proof of provider or live behavior.

##### Applies To

Current infrastructure work uses coverage of applicable validation contracts,
not fictitious application coverage numbers. Where testable application code
and coverage tooling exist, apply the target the owning Requirement defines; no
such target is defined today.
Reviewers assess acceptance and regression coverage, not merely test counts.
Provider projections preserve role and permission semantics while using native
metadata; static parity never proves discovery, model resolution, or execution.

###### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| QUAL-R001 | Always | A QA profile selects gate IDs; a lane describes routing or an evidence boundary. The execution registry owns commands and profile membership. Execute one logical leaf once for identical input bytes and history, configuration, tool identity, environment, scope, mode, trust, guarantee and consumer; a matching filename set alone never justifies reuse, and reuse never drops a required security, regression or artifact check. A check that runs after an action observes it; it never claims to have blocked it. Distinct index, working-tree, integrated-main and remote observations require their own evidence where those inputs differ. A phase name or a second caller does not justify replaying an already proven leaf. Treat local candidate-code QA as validation in the authorized workspace, not as an isolation boundary for adversarial PR code. The hosted PR style route has a separate trusted-base source, merge input and run identity; neither route certifies the other's trust conditions. | `qa-runner-tests` | none |
| QUAL-R002 | In the quick or affected lane | **quick / affected**: selected checks cover normalized working-tree changes, including applicable new files and deletion/rename paths. Record selection and the snapshot actually checked. | `validation-routing-tests` | none |
| QUAL-R003 | In the staged lane | **staged**: validate the exact logical Git index in an isolated snapshot, including the first commit. Unrelated working-tree bytes are outside this input; unstaged repairs cannot hide invalid staged content. Keep selected syntax, style, secret and content contracts, while implementation regression suites run in affected quick and PR checks. Empty staged input selects no checks. Commit-message hooks remain separate. | `qa-runner-tests` | none |
| QUAL-R004 | Always | **retired full / ci sweep**: historical local `full` and `ci` all-files profiles and blanket unit discovery are retained as past evidence, not selected for current completion. Even a shared QA-contract change selects its actual affected gates and named behavior and security unit regressions; it does not revive a repository-wide sweep. An explicit audit identifies its purpose, inputs and bounded named checks under the active registry before execution. | `validation-routing-tests` | none |
| QUAL-R005 | When a commit-message or manual-stage check applies | **message/manual**: record applicable commit-message or explicit manual-stage checks individually. | Semantic review | none |
| QUAL-R006 | Always | **hosted**: `ci-summary` validates PR metadata and `style-pr` aggregates selected style and purpose checks on the exact cumulative base-to-merge candidate. The `pull-request` profile in the validation registry selects affected implementation regressions, document content and static manifest/render/schema/policy consumers; it excludes the local repository-quality aggregate. Purpose checks execute candidate code with a read-only token, no secrets and no persisted checkout credentials. Style configuration and the hashed Python dependency lock come from the reviewed base. One saved invocation plan binds paths, base, candidate and registry; invalid input is not an empty diff. A selected leaf that is missing, skipped, cancelled or failed blocks the aggregate; only an explicit valid nonselection is NOT_APPLICABLE. No blanket full QA or post-merge replay is added. Hosted results require their exact run and candidate; static or local PASS proves no hosted execution. | `ci-python-contract`, `validation-routing-tests` | none |
| QUAL-R007 | For provider discovery, authenticated operation, remote execution or runtime checks | **remote/live**: provider discovery or authenticated operation, remote execution, and operator-approved runtime checks need direct authorized evidence. Static presence and hosted CI do not imply this lane. | Semantic review | none |
| QUAL-R008 | Always | Before implementation, identify the required gates and resolve their tools, environment, actual cost/output needs, technical command limits and necessary native execution approval. This is resource preflight, not secret/live authorization; [approval and safety](approval-and-safety.md) owns the latter. If an actual required resource or native permission is unavailable, preserve safe work and report the required check as unexecuted with its next owner. Never change a command or wrapper to evade a resource guard, disable a required check or report a false result. | `scripts/run-validation-lane.py` | none |
| QUAL-R009 | When a Task records a FAIL, DEFER or NOT_RUN result | A modern Task evidence `FAIL` records concrete Command, Input and Location as a `PASS` does. `NOT_RUN` and `DEFER` may use `Pending` where no result artifact exists, while naming the reason and next owner. QA `NOT_APPLICABLE` judges a check's target; it is never the Task criterion verdict `not-required`, which requires a cancelled Task and same-package cancelled Spec with the actual criterion-specific scope and authorization evidence. | `document-lifecycle` | none |
| QUAL-R010 | Always | `PASS`: the named check ran over the stated scope and met its acceptance condition. | `qa-runner-tests` | none |
| QUAL-R011 | Always | `NOT_RUN`: the named check did not execute. A selected required gate with this result blocks completion and cannot enter the PASS cache, which is the local evidence index kept by `scripts/qa.py`. A check outside the selected scope stays factual `NOT_RUN` without becoming a new requirement merely because a previous workflow once ran it. | `qa-runner-tests` | none |
| QUAL-R012 | Always | `NOT_APPLICABLE`: the named check has no applicable target for the stated scope. It is not evidence that a selected required check ran. | `qa-runner-tests` | none |
| QUAL-R013 | Always | `FAIL`: execution or input validation did not meet the acceptance condition. Missing required tools/modules, invalid registry, cancellation, timeout, output overflow, and cleanup failure cannot become NOT_APPLICABLE or PASS. | `validation-routing-tests` | none |
| QUAL-R014 | When required authority, environment, provider or external evidence is unavailable | `DEFER`: required authority, environment, provider, or external evidence is unavailable. An applicable optional tool's absence needs a reason and next owner, with its fallback classified separately. This is a visible limitation, never a pass. | Semantic review | none |
| QUAL-R015 | Always | Record the risk class, applicable checks, a core-diff checklist over the exact snapshot, and the owner's acceptance and applicable recovery evidence. Low-risk changes use focused checks and the author's review. Medium-risk changes require a focused review in a fresh context by someone who did not implement the change. High-risk changes require an independent reviewer with the needed domain expertise on a verified read-only execution surface. An independent review uses a different reviewer and a fresh context grounded in the original requirements, design, actual candidate and consumers; high-risk review also requires an enforced source-write boundary. A role label or repeated author review proves none of these. Record the actual surface, scope, inputs, outcome, unresolved findings, enforcement as `enforced`, `failed`, `unobserved` or `unsupported`, and source-write result separately as `denied`, `allowed` or `unobserved`. The independent review grants no execution permission or user acceptance. Choose one suitable reviewer within the approved budget; no paid model call or standing two-provider review is required for every change. For an approved irreversible transition, record applicable pre-transition and forward-correction checks in place of a recovery route for its authorized removal targets. | Semantic review | none |
| QUAL-R016 | Always | Classify risk by the impact of an incorrect change and the authority it affects, then record the reason in existing handoff evidence. `low` covers non-normative text or factual evidence that changes no behavior, authority or acceptance condition. `medium` covers bounded, reversible behavior or contract changes that do not cross a high-risk boundary, including ordinary parser, template, validator or test changes. `high` covers secret/public or source-write boundaries, sandbox or permission changes, protected actions, deletion or migration, a path to false CI PASS, and changes to approval, requirement or contract authority even when the changed file is a document. A filename or line count alone does not lower risk; a disputed class takes the higher one. | Semantic review | none |
| QUAL-R017 | Always | Run the applicable checks selected by the validation registry. Automation establishes only what those checks cover. | `scripts/qa.py` | none |
| QUAL-R018 | Always | For a `low` change, the core-diff checklist is the author's check of the actual diff for acceptance alignment, scope, consistency with current contracts and policies, one writer per file, secret exposure and removed or weakened checks, and reverting its commit is the recovery path. For a `medium` or `high` change, complete the full core-diff checklist against the actual diff, current owners, acceptance criteria and command results, not the author's summary: acceptance and implementation alignment, document completion or supersession, one writer per file, consistency with current contracts and policies, removed or weakened checks, secret exposure and the applicable recovery path (rollback commit or bounded procedure). For approved final removal targets, record candidate validation, exact scope and the stop or forward-correction procedure from Rule 15. A `high` change also lists each changed permission, trigger and protected action. | Semantic review | none |
| QUAL-R019 | Always | Grade every finding `BLOCK`, `FIX` or `NOTE`. `BLOCK` is a correctness, security or data-loss defect or a violation of a current contract or policy; it must be fixed before merge. `FIX` should be fixed, in the same change or in a tracked follow-up with a named owner. `NOTE` is informational. A `BLOCK` from an optional review blocks in the same way until fixed or dispositioned by the owner. | Semantic review | none |
| QUAL-R020 | Always | Record the checked snapshot, check results, risk class, checklist outcome, findings, the reviewing role and identity when independent review is required, and the disposition in the existing handoff evidence. The writer repairs findings and refreshes the affected checks and checklist after changes. Reuse unchanged evidence under the validation lane contract. | Semantic review | none |
| QUAL-R021 | For a pull request | For a pull request, complete the checklist over the final diff of the exact head. | Semantic review | none |
| QUAL-R022 | Always | A failed required check or unresolved `BLOCK` finding blocks completion. Missing applicable automation is an explicit evidence gap, not PASS; route it to the responsible owner. The owner's explicit acceptance is the decision; it is never inferred from a check PASS, a merge or an optional review. Human judgment beyond that acceptance is needed for unresolved intent, conflicting authority or a decision reserved to the request owner. | Semantic review | none |
| QUAL-R023 | Always | This review rule supplies quality evidence, not authorization. Explicit human/operator approvals, protected external actions and required hosted reviews remain governed by their existing owners. Native and live claims still require the corresponding observed evidence. | Semantic review | none |
| QUAL-R024 | Always | The [agent evaluator](../../../.agents/roles/agent-evaluator.md) may compare actual `noSkill` and `withSkill` trials of the same task as bounded measurement evidence. The evaluation router holds raw observations, task context, criteria, scores and one aggregate results owner; Stage 99 owns their form. Declare trial count, signals, criterion IDs and human calibration before scoring. Preserve partial trials as incomplete and enter an aggregate only after every declared pair has actual evidence. A synthetic example or an unobserved condition is not an actual cycle. | `document-contract-tests` | none |
| QUAL-R025 | Always | Admit a recurring check only for a current document contract or actual repository-purpose surface: document profiles, forms, frontmatter, relations, links and status; GitOps, Kubernetes, Docker, reference project templates, web content, Vault configuration and external-service interfaces where present. Shared selection, commit, release, secret and runner controls that enforce those contracts also need bounded regression coverage. Keep separate rules when their input, threat model or failure meaning differs. An old name, a slow run or a failure alone does not prove a test is obsolete. | `validation-routing-tests` | none |
| QUAL-R026 | For an ordinary authored document or README router change | An ordinary authored document or README router change that alters only prose or navigation selects the common diff, style and commit-message checks plus document content checks for profile, relationships, links and lifecycle state. Do not select repository-wide quality, agent or infrastructure gates, or unit sweeps, solely because the changed path is Markdown. A change to a governance, provider or native contract, a Stage 99 form, schema or registry, or executable implementation is a contract or behavior change: select its necessary focused regressions and affected gates under the owning validation registry. No validator or hook rewrites a governed document. Local link results remain local evidence; selected PR document-content checks may run separately on the hosted candidate under QUAL-R006. | `document-contract-tests` | none |
| QUAL-R027 | Always | The registry selects gates within a profile; changed inputs require a fresh result. A static workflow file cannot establish hosted execution or remote branch protection. | Semantic review | none |
| QUAL-R028 | During routine editing | Routine editing | `scripts/qa.py` | none |
| QUAL-R029 | At a local commit | Local commit | `staged-qa` hook of `.pre-commit-config.yaml` | none |
| QUAL-R030 | At a feature push | Feature push | Semantic review | none |
| QUAL-R031 | At a pull request | Pull request | `ci-python-contract` | none |
| QUAL-R032 | At a deployment | Deployment | Semantic review | none |
| QUAL-R033 | At main integration | Main integration | Semantic review | none |
| QUAL-R034 | At a local handoff | Local handoff | Semantic review | none |
| QUAL-R035 | Always | For a no-commit request preserve the index and record staged/message evidence as N/A. | `qa-runner-tests` | none |
| QUAL-R036 | While implementing | **targeted**: reproduce changed behavior and run focused checks while implementing. | Semantic review | none |
| QUAL-R037 | During iterations, when the working-tree input differs | **quick**: during iterations, run selected affected checks when the working-tree input differs or independent working-tree evidence is needed. Record the selection. If the required staged run demonstrably covers the same leaf with equivalent bytes, configuration, tool, scope, mode and trust, record `quick` as `NOT_RUN` and unrequired for completion; matching paths alone do not establish that equivalence. | `scripts/qa.py` | none |
| QUAL-R038 | At each logical commit | **each logical commit**: inspect status and the unstaged diff, stage only the reviewed logical set, inspect the cached diff, run `git diff --check` and `git diff --cached --check`, then commit through the active hooks, whose `staged-qa` hook runs `qa.py staged` (exact-index QA including the selected lint/format gate) as one run. Validate the actual message under Git policy and record the leaf actually run. | `staged-qa` hook of `.pre-commit-config.yaml` | none |
| QUAL-R039 | At delivery | **delivery validation**: review the selected focused units and purpose gates against the final branch input. Record hosted branch metadata and selected style and purpose results at their own PR SHA/run when observed; a deployment style result needs its actual deployment SHA/run. Recheck an integrated-main input only to the extent changed bytes or history invalidate prior evidence. | Semantic review | none |
| QUAL-R040 | When formatter findings or a failed delivery check occur | **repair and refresh**: inspect formatter findings, explicitly fix selected files, review/restage changed bytes and refresh affected evidence. QA itself never fixes source files. A failed required delivery check keeps the work incomplete. | `selected-style` | none |
| QUAL-R041 | At evidence handoff | **evidence handoff**: record the checked snapshot and any subsequent Task-only changes separately, validating those document changes without a self-SHA or elapsed-time rewrite loop. Review final diff scope and remaining acceptance using the semantic review contract above. | Semantic review | none |
| QUAL-R042 | Always | Record in the owning Task or approved evidence record: | `document-lifecycle` | none |
| QUAL-R043 | Always | scope, changed paths, and acceptance IDs; | Semantic review | none |
| QUAL-R044 | Always | the snapshot the work sits on: branch, HEAD, and the base it diverged from; when they differ, name the candidate the checks ran on, the verified commit and the delivered commit. A result recorded over a commit that later changed is stale for the new commit until it is run again; | Semantic review | none |
| QUAL-R045 | Always | commands and tool/version, with each ordered completion-step result; | Semantic review | none |
| QUAL-R046 | Always | separate lane results and limitations; | Semantic review | none |
| QUAL-R047 | Always | the approval boundary in force: what was authorized and what was not; | Semantic review | none |
| QUAL-R048 | Always | risk class, checklist outcome, any optional reviewer identity and disposition; | Semantic review | none |
| QUAL-R049 | Always | rollback commit or bounded rollback procedure; | Semantic review | none |
| QUAL-R050 | Always | residual risk and next owner. | Semantic review | none |
| QUAL-R051 | Where byte identity is the security contract | Retain immutable identities where byte identity is the security contract: pinned external Actions/hooks, resolved dependency artifacts, or Git-backed recovery objects. Their owning contract records purpose and refresh/recovery procedure. Branch HEADs, current docs, local validators, and inventory counts are not policy pins. | `github-actions-security` | none |
| QUAL-R052 | When one run serves both verification and validation | One observed run may give both verification and validation only when its input and guarantee cover both. The Task cites that one evidence row for both and states what each purpose checked and why the run's input suffices. Replaying the same check only to fill the second name is the replay [QUAL-R001](#requirements) forbids, and a run that covers only one purpose leaves the other open. | Semantic review | none |
| QUAL-R053 | When a finding is graded | Grade a finding by its location, the current contract it breaks, a counterexample and its impact. A defect reproduced on an input that the current contract, configuration or deployment accepts is `BLOCK` or `FIX` by that impact; needing a specific or crafted input never lowers it to `NOTE`. A missing required item is graded by the contract it breaks and is never omitted. A suspicion with neither a reproduction nor a reachable input is recorded with its uncertainty, not as `BLOCK`; a security suspicion is escalated to its owner, not dropped. A preference with no failure condition is `NOTE` and blocks nothing. Report one finding per root cause; a number of findings or comments is never a review target. | Semantic review | none |
| QUAL-R054 | When a reviewed change changes again | Review again only what changed after the reviewed commit and the findings that change touches; widen to the whole change when a permission or security boundary, the base or the history changes. A later commit that adds only factual execution evidence, without changing source, obligations, criteria, authority or acceptance, keeps the review once `scripts/review_delta.py --reviewed <commit>` reports `EVIDENCE_ONLY`; record that result instead of replaying review. A new Task, a ledger mutation, a meaning-changing Task addition, or an edit to an existing Task row requires review. The tool conservatively classifies paths and recognized factual rows, not every possible natural-language claim; uncertainty requires semantic review. Widening to transitive impact or a whole boundary is the reviewer's judgment. A changed SHA alone never orders a new review pass. The same reviewer under another label, or the author rerunning their own role, is not an independent review. | `scripts/review_delta.py` | none |
| QUAL-R055 | When a review runs | Give the reviewer one packet, as the [change-review prompt contract](../../../.agents/prompts/change-review.md) lists: original current request and applicable design, actual candidate and base, changed paths and diff, affected consumers and permissions, acceptance IDs, risk class and reason, observed checks, known failures, unobserved scope and cost limits. Omit the author's expected verdict so the reviewer tests real failure conditions, complexity and contract conflicts in a fresh context. The reviewer reruns a check only to test a finding, never to repeat a recorded PASS. Record the actual review surface, reviewed scope, boundary and source-write observations separately from the verdict; static role settings do not prove enforcement ([SAFE-R018](../../../.agents/governance/approval-and-safety.md#execution-controls)). Record, when observed, wait, context loading, active review and rerun time separately, and findings by grade with confirmed, false or duplicate counts. | Semantic review | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| QUAL-R001 | required | active |
| QUAL-R002 | required | active |
| QUAL-R003 | required | active |
| QUAL-R004 | required | active |
| QUAL-R005 | required | active |
| QUAL-R006 | required | active |
| QUAL-R007 | required | active |
| QUAL-R008 | required | active |
| QUAL-R009 | required | active |
| QUAL-R010 | required | active |
| QUAL-R011 | required | active |
| QUAL-R012 | required | active |
| QUAL-R013 | required | active |
| QUAL-R014 | required | active |
| QUAL-R015 | required | active |
| QUAL-R016 | required | active |
| QUAL-R017 | required | active |
| QUAL-R018 | required | active |
| QUAL-R019 | required | active |
| QUAL-R020 | required | active |
| QUAL-R021 | required | active |
| QUAL-R022 | required | active |
| QUAL-R023 | required | active |
| QUAL-R024 | required | active |
| QUAL-R025 | required | active |
| QUAL-R026 | required | active |
| QUAL-R027 | required | active |
| QUAL-R028 | required | active |
| QUAL-R029 | required | active |
| QUAL-R030 | required | active |
| QUAL-R031 | required | active |
| QUAL-R032 | required | active |
| QUAL-R033 | required | active |
| QUAL-R034 | required | active |
| QUAL-R035 | required | active |
| QUAL-R036 | required | active |
| QUAL-R037 | required | active |
| QUAL-R038 | required | active |
| QUAL-R039 | required | active |
| QUAL-R040 | required | active |
| QUAL-R041 | required | active |
| QUAL-R042 | required | active |
| QUAL-R043 | required | active |
| QUAL-R044 | required | active |
| QUAL-R045 | required | active |
| QUAL-R046 | required | active |
| QUAL-R047 | required | active |
| QUAL-R048 | required | active |
| QUAL-R049 | required | active |
| QUAL-R050 | required | active |
| QUAL-R051 | required | active |
| QUAL-R052 | required | active |
| QUAL-R053 | required | active |
| QUAL-R054 | required | active |
| QUAL-R055 | required | active |

###### Validation lane contract

`QUAL-R001`

Document link and owner checks execute through selected local QA or the
selected hosted PR purpose path. Metadata and style alone certify no document
content. Each invocation reports its own input and trust boundary. A repository
link-target result does not establish external URL availability; record that
as unobserved unless directly authorized and checked.

###### Validation runner envelope

`QUAL-R008`

Business deadlines, session timeboxes and final-validation reserve approvals
are not prerequisites to scoped work or local validation. Do not invent them,
rename them as resource gates, or restore obsolete requirements from historical
Task/Plan wording. Explicit cancellation, lack of progress, real cost/token or
platform limits, and protected-action authority govern their own steps.
Per-command timeout, output bounds and descendant cleanup protect execution;
they do not expire the user's authoring authorization or stop independent work.

Every repository-static child selected by the validation-surface contract runs
through the [validation runner](../../../scripts/run-validation-lane.py), which
owns the reviewed limit constants and treats timeout, pipe overflow or failure,
or pipes held by descendants after the leader exits as `FAIL`.

###### Result vocabulary

`QUAL-R009`

When a Task records a required `FAIL`, `DEFER`, or `NOT_RUN`, keep the original
observation. A later `PASS` closes it only when the new evidence explicitly
names the earlier evidence ID and concerns the same check, work unit and
criterion. An unrelated PASS cannot hide a required unresolved result. The
Task's Criterion Decisions table owns the single criterion verdict; check
results, approval, integration and publication are distinct facts.

###### Semantic review

`QUAL-R015`

###### Agent evaluation evidence

`QUAL-R024`

Evaluation scores and calibration are distinct from repository QA
`PASS`/`FAIL`/`NOT_RUN`/`DEFER`, approval, and provider-runtime evidence. A
recorded response does not prove that a native skill loaded, a command ran,
its result succeeded, or a permission boundary enforced; those claims need
direct session evidence. Keeping evaluation evidence does not register a
grader as a recurring QA gate. Admission requires a durable consumer, an
owned failure rule and the validation registry's separate review.

###### QA admission and retirement

`QUAL-R025`

For a one-use, legacy or deprecated check, first transfer any ongoing
protection to its durable owner, including lifecycle, link and content
integrity apart from historical cutover completion proof.
Then remove the old caller and registration, remove its dedicated helper,
fixture and test when no consumer remains, and preserve necessary past results
in the existing Task or Git history. Do not add a new Spec or
progress ledger solely to retire old QA; the work residue ledger is not one. Ordinary document changes select
profile, relationship, link and state checks; executable behavior changes get
focused negative and boundary regressions. A one-time Spec or Task migration
test is not a permanent gate after its outcome is retained.

Optimize in this order: remove duplicate leaves, separate content validation
from implementation regression, share parsing and Git reads inside one run,
select by changed impact, then reuse only a narrowly proven result. Measure
before claiming a cost or speed improvement. The selected registry contract,
not a policy sentence, owns the exact gate list and per-check limits.

###### Ordinary document selection

`QUAL-R026`

###### Delivery ownership

`QUAL-R027`

| Rule ID | Required owner and evidence |
| --- | --- |
| QUAL-R028 | Run focused behavior checks and selected affected `quick` checks over changed working-tree bytes. |
| QUAL-R029 | Review the logical index, then commit with active hooks as one run: the `staged-qa` hook runs exact-index `staged` QA, which includes the selected lint and format gate (`selected-style`), and the commit-msg hooks validate the actual message. Record that run once. |
| QUAL-R030 | Preserve checked commit evidence and observed push result; pushing adds no QA leaf for unchanged inputs. |
| QUAL-R031 | Observe required hosted branch or repository metadata and the selected `style-pr` style and purpose leaves at the exact PR SHA and run identity. Hosted `style-pr` certifies only its selected hosted purpose and document-content checks; it does not certify a separate local execution. Remote protection remains `DEFER` when unobserved. A pull request completes only when the required checks pass, the review requirement is met (no approving review is required, count 0) and the core-diff checklist of the final diff records no unresolved `BLOCK` finding. The repository owner merges it, or explicitly directs its merge, with a merge commit; automated checks, Apps and signatures never stand in for the owner's approval. |
| QUAL-R032 | Observe the selected style check at the actual deployment SHA/run before deployment, as the hosted lane requires; otherwise retain `NOT_RUN` or `DEFER`. Repository files alone cannot certify deployment. |
| QUAL-R033 | Compare the integrated tree and history with checked inputs. Run only checks invalidated by a changed input; an unchanged merge candidate needs no repeat. Record the actual merge and any remote required-check result separately. |
| QUAL-R034 | Resolve tools, actual resources, output, technical command limits and necessary native approval for applicable selected gates and named unit regressions, including continuing security guarantees. No session timebox or reserve approval is required. |

###### Canonical completion sequence

`QUAL-R035`

Use raw NUL-delimited machine paths for changed/staged path transport. Do not
reconstruct them with newline iteration or filtered display output. Preserve
runner boundary failures and optional-tool deferrals rather than treating them
as successful selected coverage.

###### Handoff evidence contract

`QUAL-R042`

A field may state `none` or `DEFER` with a reason, but must not silently
disappear. Do not copy raw child payload or sensitive diagnostics into evidence.

These fields carry a handoff between providers as well as between people. The
receiver re-observes Git, the owning Task, and the canonical owner before
acting; a recorded snapshot says which state the evidence described, and a
recorded boundary keeps a past authorization from being read as a standing
one. Neither field grants authority, and a stale record never widens it.

###### Supply-chain identity

`QUAL-R051`

##### Exceptions

This policy defines no exception condition of its own; exceptions follow the approval and safety policy's operator approval route. If this policy needs its own, state it here.

###### Approval and Review

Approval and review conditions are stated under Requirements.

#### Enforcement

##### Mechanisms

Refresh this policy when evidence semantics change, not when a corpus count or
implementation constant changes. Preserve the distinction between repository,
provider-runtime, hosted CI, and live checks. Formatters or deferred tools
cannot silently advance a task to completion.

- [Validation Routing Registry](../../../scripts/validation/registry.json)

##### Limits

Passing a local command is not proof of provider or live behavior, and a static workflow file cannot establish hosted execution or remote branch protection. A recorded response does not prove that a native skill loaded or a command ran, and formatters or deferred tools cannot silently advance a task to completion; repository, provider-runtime, hosted CI and live checks stay distinct.

#### Ownership

##### Owner

This policy owns lane, result, completion-order, and handoff meanings.
The validation-surface contract selects executable checks; validators own
their rules and bounded execution limits. Aggregates compose those checks.
Do not duplicate limit constants, fixture matrices, mutable digests, or corpus
counts in prose.

- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../../../.agents/workflows/work-lifecycle.md)
- [Git Policy](../03.process/git.md)
- [Formatting and Linting Policy](formatting-and-linting.md)

###### Responsibilities

Responsibilities are stated under Owner and Requirements.

##### Review Triggers

Change and adoption conditions are stated under Enforcement.

## 적용과 확인

### 적용 방법

Apply the rule, enforcement and exception clauses in the payload together.

### 확인 기준

Check named enforcement on actual input and report its evidence level accurately.

## 관계와 출처

### 관련 문서

The ownership and related documents in the payload link adjacent owners.

### 외부 근거

Repository decisions and cited sources support these rules; external sources alone grant no authority.
