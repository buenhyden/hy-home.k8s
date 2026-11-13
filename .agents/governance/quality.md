---
title: "Quality and Evidence Policy"
version: "2.6.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-13"
---

# Quality and Evidence Policy

## Purpose

### Objective

Report exactly what was checked, over which bytes and scope, and with which
limitations. Passing a local command is not proof of provider or live behavior.

### Authority

This policy owns lane, result, completion-order, and handoff meanings.
The validation-surface contract selects executable checks; validators own
their rules and bounded execution limits. Aggregates compose those checks.
Do not duplicate limit constants, fixture matrices, mutable digests, or corpus
counts in prose.

- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)
- [Git Policy](git.md)
- [Formatting and Linting Policy](formatting-and-linting.md)

## Scope

### Applies To

Current infrastructure work uses coverage of applicable validation contracts,
not fictitious application coverage numbers. Where testable application code
and coverage tooling exist, apply the target the owning Requirement defines; no
such target is defined today.
Reviewers assess acceptance and regression coverage, not merely test counts.
Provider projections preserve role and permission semantics while using native
metadata; static parity never proves discovery, model resolution, or execution.

### Exclusions

This policy marks no subject as excluded from its scope.

## Rules

### Requirements

#### Validation lane contract

- **quick / affected**: selected checks cover normalized working-tree changes,
  including applicable new files and deletion/rename paths. Record selection
  and the snapshot actually checked.
- **staged**: validate the exact logical Git index in an isolated snapshot.
  Unstaged repairs cannot hide invalid staged content; commit-message hooks
  remain separate.
- **retired full / ci sweep**: historical local `full` and `ci` all-files
  profiles and blanket unit discovery are retained as past evidence, not
  selected for current completion. Even a shared QA-contract change selects
  its actual affected gates and named behavior and security unit
  regressions; it does not revive a repository-wide sweep. An explicit audit
  identifies its purpose, inputs and bounded named checks under the active
  registry before execution.
- **message/manual**: record applicable commit-message or explicit manual-stage
  checks individually.
- **hosted**: a former local `ci` alias never established GitHub Actions
  execution. Hosted automation
  runs branch or repository metadata checks and the separately selected shared
  style check on PR inputs. When a PR changes `.github/requirements/`, the
  style job also runs the reviewed base's CI Python contract check against the
  PR files, because a bot-authored lock update never passes local staged QA
  (SPEC-0123; Git history: package `0123-hosted-lock-check` under
  `docs/03.specs/` at commit `69445fca`). A
  deployment style route applies only if a real
  deployment workflow exists. Hosted automation does not run local unit or
  document-content QA. A hosted result reports only what its jobs actually
  observed and is never a proxy for a successful local run or style job.
  The user adopted on 2026-11-12 a target in which PR-time hosted CI runs the
  affected implementation and product checks with a read-only token and no
  secrets. It is a target, not current behavior: until one change set accepts
  a successor to ADR-0048 and amends REQ-0003 FR-0017 with the workflow,
  FR-0017 and ADR-0048 govern, and the hosted jobs are `ci-summary` and
  `style-pr`.
- **remote/live**: provider discovery or authenticated operation, remote
  execution, and operator-approved runtime checks need direct authorized
  evidence. Static presence and hosted CI do not imply this lane.

A QA profile selects gate IDs; a lane describes routing or an evidence boundary.
The execution registry owns commands and profile membership. Execute one logical
leaf once for identical input bytes and history, configuration, tool identity,
environment, scope, mode, trust, guarantee and consumer; a matching filename
set alone never justifies reuse, and reuse never drops a required security,
regression or artifact check. A check that runs after an action observes it;
it never claims to have blocked it.
Distinct index, working-tree, integrated-main and remote
observations require their own evidence where those inputs differ. A phase name
or a second caller does not justify replaying an already proven leaf.
Treat local candidate-code QA as validation in the authorized workspace, not
as an isolation boundary for adversarial PR code. The hosted PR style route
has a separate trusted-base source, merge input and run identity; neither
route certifies the other's trust conditions.

Document link and owner checks execute only through selected local QA. Hosted
metadata jobs neither run nor certify them. A local repository link-target
result does not establish external URL availability; record that as a separate
unobserved external condition unless directly authorized and checked.

#### Validation runner envelope

Before implementation, identify the required gates and resolve their tools,
environment, actual cost/output needs, technical command limits and necessary
native execution approval. This is resource preflight, not secret/live authorization;
[approval and safety](approval-and-safety.md) owns the latter. If an actual
required resource or native permission is unavailable, preserve safe work and report the required
check as unexecuted with its next owner. Never change a command or wrapper to
evade a resource guard, disable a required check or report a false result.

Business deadlines, session timeboxes and final-validation reserve approvals
are not prerequisites to scoped work or local validation. Do not invent them,
rename them as resource gates, or restore obsolete requirements from historical
Task/Plan wording. Explicit cancellation, lack of progress, real cost/token or
platform limits, and protected-action authority govern their own steps.
Per-command timeout, output bounds and descendant cleanup protect execution;
they do not expire the user's authoring authorization or stop independent work.

Every repository-static child selected by the validation-surface contract runs
through the [validation runner](../../scripts/run-validation-lane.py), which
owns the reviewed limit constants and treats timeout, pipe overflow or failure,
or pipes held by descendants after the leader exits as `FAIL`.

#### Result vocabulary

- `PASS`: the named check ran over the stated scope and met its acceptance
  condition.
- `NOT_RUN`: the named check did not execute. A selected required gate with this
  result blocks completion and cannot enter the PASS cache, which is the local evidence index kept by
  `scripts/qa.py`. A check
  outside the selected scope stays factual `NOT_RUN` without becoming a new
  requirement merely because a previous workflow once ran it.
- `NOT_APPLICABLE`: the named check has no applicable target for the stated
  scope. It is not evidence that a selected required check ran.
- `FAIL`: execution or input validation did not meet the acceptance condition.
  Missing required tools/modules, invalid registry, cancellation, timeout,
  output overflow, and cleanup failure cannot become NOT_APPLICABLE or PASS.
- `DEFER`: required authority, environment, provider, or external evidence is
  unavailable. An applicable optional tool's absence needs a reason and next
  owner, with its fallback classified separately. This is a visible limitation,
  never a pass.

A modern Task Evidence `FAIL` records concrete Check, Input and Location as a
`PASS` does. `NOT_RUN` and `DEFER` may use `Pending` where no result artifact
exists, while naming the reason and next owner. QA `NOT_APPLICABLE` judges a
check's target; it is never the Task criterion verdict `not-required`, which
requires a cancelled Task and same-package cancelled Spec with the actual
criterion-specific scope and authorization evidence.

When a Task records a required `FAIL`, `DEFER`, or `NOT_RUN`, keep the original
observation. A later `PASS` closes it only when the new evidence explicitly
names the earlier evidence ID and concerns the same check, work unit and
criterion. An unrelated PASS cannot hide a required unresolved result. The
Task's Criterion Acceptance table owns the single criterion verdict; check
results, approval, integration and publication are distinct facts.

#### Semantic review

A single-maintainer review combines a recorded risk class, the applicable
static and contract checks, a core-diff checklist over the exact snapshot, the
owner's explicit acceptance and a recovery path, with the evidence and any
release approval recorded. An extra agent or model API call is never a required
reviewer: no rule, gate or completion condition may depend on one, and adding
one under another name (proxy, summary or gate helper) is the same violation.
When the operator asks for one, a separate read-only agent review is optional
supporting evidence. No review step, agent or human, is recorded as a second
human approval.

- Record the risk class in the existing handoff evidence: `low` for a
  document-only change outside policy, registry, validator, hook, workflow and
  permission files; `medium` for a policy, registry, template, validator or test
  change; `high` for a permission, secret-handling, hook, workflow,
  protected-action or data-loss path. A disputed class takes the higher one.
- Run the applicable checks selected by the validation registry. Automation
  establishes only what those checks cover.
- Complete the core-diff checklist against the actual diff, current owners,
  acceptance criteria and command results, not the author's summary:
  acceptance and implementation alignment, document completion or
  supersession, one writer per file, consistency with current contracts and
  policies, removed or weakened checks, secret exposure and the recovery path
  (rollback commit or bounded procedure). A `high`
  change also lists each changed permission, trigger and protected action.
- Grade every finding `BLOCK`, `FIX` or `NOTE`. `BLOCK` is a correctness,
  security or data-loss defect or a violation of a current contract or policy;
  it must be fixed before merge. `FIX` should be fixed, in the same change or
  in a tracked follow-up with a named owner. `NOTE` is informational. A `BLOCK`
  from an optional review blocks in the same way until fixed or dispositioned
  by the owner.
- Record the checked snapshot, check results, risk class, checklist outcome,
  findings, any optional reviewer identity and the disposition in the existing
  handoff evidence. The writer repairs findings and refreshes the affected
  checks and checklist after changes. Reuse unchanged evidence under the
  validation lane contract.
- For a pull request, complete the checklist over the final diff of the exact
  head.
- A failed required check or unresolved `BLOCK` finding blocks completion.
  Missing applicable automation is an explicit evidence gap, not PASS; route it
  to the responsible owner. The owner's explicit acceptance is the decision; it
  is never inferred from a check PASS, a merge or an optional review. Human
  judgment beyond that acceptance is needed for unresolved intent, conflicting
  authority or a decision reserved to the request owner.
- This review rule supplies quality evidence, not authorization. Explicit
  human/operator approvals, protected external actions and required hosted
  reviews remain governed by their existing owners. Native and live claims
  still require the corresponding observed evidence.

#### Agent evaluation evidence

The [agent evaluator](../roles/agent-evaluator.md) may compare actual
`noSkill` and `withSkill` trials of the same task as bounded measurement
evidence. The evaluation router holds raw observations, task context,
criteria, scores and one aggregate results owner; Stage 99 owns their form.
Declare trial count, signals, criterion IDs and human calibration before
scoring. Preserve partial trials as incomplete and enter an aggregate only
after every declared pair has actual evidence. A synthetic example or an
unobserved condition is not an actual cycle.

Evaluation scores and calibration are distinct from repository QA
`PASS`/`FAIL`/`NOT_RUN`/`DEFER`, approval, and provider-runtime evidence. A
recorded response does not prove that a native skill loaded, a command ran,
its result succeeded, or a permission boundary enforced; those claims need
direct session evidence. Keeping evaluation evidence does not register a
grader as a recurring QA gate. Admission requires a durable consumer, an
owned failure rule and the validation registry's separate review.

#### QA admission and retirement

Admit a recurring check only for a current document contract or actual
repository-purpose surface: document profiles, forms, frontmatter, relations,
links and status; GitOps, Kubernetes, Docker, reference project templates, web
content, Vault configuration and external-service interfaces where present.
Shared selection, commit, release, secret and runner controls that enforce
those contracts also need bounded regression coverage. Keep separate rules
when their input, threat model or failure meaning differs.
An old name, a slow run or a failure alone does not prove a test is obsolete.

For a one-use, legacy or deprecated check, first transfer any ongoing
protection to its durable owner, including lifecycle, link and content
integrity apart from historical cutover completion proof.
Then remove the old caller and registration, remove its dedicated helper,
fixture and test when no consumer remains, and preserve necessary past results
in the existing Task or Git history. Do not add a new Spec or
progress ledger solely to retire old QA. Ordinary document changes select
profile, relationship, link and state checks; executable behavior changes get
focused negative and boundary regressions. A one-time Spec or Task migration
test is not a permanent gate after its outcome is retained.

Optimize in this order: remove duplicate leaves, separate content validation
from implementation regression, share parsing and Git reads inside one run,
select by changed impact, then reuse only a narrowly proven result. Measure
before claiming a cost or speed improvement. The selected registry contract,
not a policy sentence, owns the exact gate list and per-check limits.

#### Ordinary document selection

An ordinary authored document or README router change that alters only prose
or navigation selects the common diff, style and commit-message checks plus
document content checks for profile, relationships, links and lifecycle state.
Do not select repository-wide quality, agent or infrastructure gates, or
unit sweeps, solely because the changed path is Markdown. A change to a governance,
provider or native contract, a Stage 99 form, schema or registry, or executable
implementation is a contract or behavior change: select its necessary focused
regressions and affected gates under the owning validation registry. No
validator or hook rewrites a governed document. Document link checks remain local as specified
above.

#### Delivery ownership

| Route | Required owner and evidence |
| --- | --- |
| Routine editing | Run focused behavior checks and selected affected `quick` checks over changed working-tree bytes. |
| Local commit | Review the logical index, then commit with active hooks as one run: the `staged-qa` hook runs exact-index `staged` QA, which includes the selected lint and format gate (`selected-style`), and the commit-msg hooks validate the actual message. Record that run once. |
| Feature push | Preserve checked commit evidence and observed push result; pushing adds no QA leaf for unchanged inputs. |
| Pull request | Observe required hosted branch or repository metadata and selected style checks at the exact PR SHA and run identity. Hosted style does not certify local purpose checks or document content; remote protection remains `DEFER` when unobserved. A pull request completes only when the required checks pass, the review requirement is met (no approving review is required, count 0) and the core-diff checklist of the final diff records no unresolved `BLOCK` finding. The repository owner merges it, or explicitly directs its merge, with a merge commit; automated checks, Apps and signatures never stand in for the owner's approval. |
| Deployment | Observe the selected style check at the actual deployment SHA/run before deployment, as the hosted lane requires; otherwise retain `NOT_RUN` or `DEFER`. Repository files alone cannot certify deployment. |
| Main integration | Compare the integrated tree and history with checked inputs. Run only checks invalidated by a changed input; an unchanged merge candidate needs no repeat. Record the actual merge and any remote required-check result separately. |
| Local handoff | Resolve tools, actual resources, output, technical command limits and necessary native approval for applicable selected gates and named unit regressions, including continuing security guarantees. No session timebox or reserve approval is required. |

The registry selects gates within a profile; changed inputs require a fresh
result. A static workflow file
cannot establish hosted execution or remote branch protection.

#### Canonical completion sequence

1. **targeted**: reproduce changed behavior and run focused checks while implementing.
2. **quick**: during iterations, run selected affected checks when the
   working-tree input differs or independent working-tree evidence is needed.
   Record the selection. If the required staged run demonstrably covers the
   same leaf with equivalent bytes, configuration, tool, scope, mode and trust,
   record `quick` as `NOT_RUN` and unrequired for completion; matching paths
   alone do not establish that equivalence.
3. **each logical commit**: inspect status and the unstaged diff, stage only the
   reviewed logical set, inspect the cached diff, run `git diff --check` and
   `git diff --cached --check`, then commit through the active hooks, whose
   `staged-qa` hook runs `qa.py staged` (exact-index QA including the selected
   lint/format gate) as one run. Validate the actual message under Git policy
   and record the leaf actually run.
4. **delivery validation**: review the selected focused units and purpose gates
   against the final branch input. Record hosted branch metadata and selected
   style at their own PR or deployment SHA/run when observed. Recheck an integrated-main
   input only to the extent changed bytes or history invalidate prior evidence.
5. **repair and refresh**: inspect formatter findings, explicitly fix selected
   files, review/restage changed bytes and refresh affected evidence. QA itself
   never fixes source files. A failed required delivery check keeps the work incomplete.
6. **evidence handoff**: record the checked snapshot and any subsequent Task-only
   changes separately, validating those document changes without a self-SHA or
   elapsed-time rewrite loop. Review final diff scope and remaining acceptance using the semantic review
   contract above.

For a no-commit request preserve the index and record staged/message evidence
as N/A.

Use raw NUL-delimited machine paths for changed/staged path transport. Do not
reconstruct them with newline iteration or filtered display output. Preserve
runner boundary failures and optional-tool deferrals rather than treating them
as successful selected coverage.

#### Handoff evidence contract

Record in the owning Task or approved evidence record:

- scope, changed paths, and acceptance IDs;
- the snapshot the work sits on: branch, HEAD, and the base it diverged from;
  when they differ, name the candidate the checks ran on, the verified commit
  and the delivered commit. A result recorded over a commit that later changed
  is stale for the new commit until it is run again;
- commands and tool/version, with each ordered completion-step result;
- separate lane results and limitations;
- the approval boundary in force: what was authorized and what was not;
- risk class, checklist outcome, any optional reviewer identity and disposition;
- rollback commit or bounded rollback procedure;
- residual risk and next owner.

A field may state `none` or `DEFER` with a reason, but must not silently
disappear. Do not copy raw child payload or sensitive diagnostics into evidence.

These fields carry a handoff between providers as well as between people. The
receiver re-observes Git, the owning Task, and the canonical owner before
acting; a recorded snapshot says which state the evidence described, and a
recorded boundary keeps a past authorization from being read as a standing
one. Neither field grants authority, and a stale record never widens it.

#### Supply-chain identity

Retain immutable identities where byte identity is the security contract:
pinned external Actions/hooks, resolved dependency artifacts, or Git-backed
recovery objects. Their owning contract records purpose and
refresh/recovery procedure. Branch HEADs, current docs, local validators, and
inventory counts are not policy pins.

### Enforcement

Refresh this policy when evidence semantics change, not when a corpus count or
implementation constant changes. Preserve the distinction between repository,
provider-runtime, hosted CI, and live checks. Formatters or deferred tools
cannot silently advance a task to completion.

- [Validation Routing Registry](../../scripts/validation/registry.json)

## Exceptions

### Exception Conditions

This policy states no exception condition of its own.

### Approval and Review

Approval and review conditions are stated under Requirements.

## Ownership

### Responsibilities

Responsibilities are stated under Authority and Requirements.

### Change and Adoption

Change and adoption conditions are stated under Enforcement.
