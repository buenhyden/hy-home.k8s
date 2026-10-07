---
title: "Quality and Evidence Policy"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-07"
---

# Quality and Evidence Policy

## Overview

Report exactly what was checked, over which bytes and scope, and with which
limitations. Passing a local command is not proof of provider or live behavior.

## Authority Boundary

This policy owns lane, result, completion-order, and handoff meanings.
The validation-surface contract selects executable checks; validators own
their rules and bounded execution limits. Aggregates compose those checks.
Do not duplicate limit constants, fixture matrices, mutable digests, or corpus
counts in prose.

## Governance Context

Current infrastructure work uses coverage of applicable validation contracts,
not fictitious application coverage numbers. Where testable application code
and coverage tooling exist, apply the approved application coverage target.
Reviewers assess acceptance and regression coverage, not merely test counts.
Provider projections preserve role and permission semantics while using native
metadata; static parity never proves discovery, model resolution, or execution.

## Current Contract

### Validation lane contract

- **quick / affected**: selected checks cover normalized working-tree changes,
  including applicable new files and deletion/rename paths. Record selection
  and the snapshot actually checked.
- **staged**: validate the exact logical Git index in an isolated snapshot.
  Unstaged repairs cannot hide invalid staged content; commit-message hooks
  remain separate.
- **retired full / ci sweep**: historical local `full` and `ci` all-files
  profiles and blanket unit discovery are retained as past evidence, not
  selected for current completion. Even a shared QA-contract change selects
  its actual affected gates and named behavior, Archive and security unit
  regressions; it does not revive a repository-wide sweep. An explicit audit
  identifies its purpose, inputs and bounded named checks under the active
  registry before execution.
- **message/manual**: record applicable commit-message or explicit manual-stage
  checks individually.
- **hosted**: a former local `ci` alias never established GitHub Actions
  execution. Hosted automation
  runs branch or repository metadata checks and the separately selected shared
  style check on PR inputs. A deployment style route applies only if a real
  deployment workflow exists. Hosted automation does not run local full, unit or
  document-content QA. A hosted result reports only what its jobs actually
  observed; old full-QA `NOT_RUN` records remain historical, never a current
  required gate or a proxy for a successful local run or style job.
- **remote/live**: provider discovery or authenticated operation, remote
  execution, and operator-approved runtime checks need direct authorized
  evidence. Static presence and hosted CI do not imply this lane.

A QA profile selects gate IDs; a lane describes routing or an evidence boundary.
The execution registry owns commands and profile membership. Execute one logical
leaf once for identical input bytes and history, configuration, tool identity,
scope, mode and trust. Distinct index, working-tree, integrated-main and remote
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

### Validation runner envelope

Before implementation, identify the required gates and resolve their tools,
environment, expected cost/time/output envelope and any necessary native
execution approval. This is resource preflight, not secret/live authorization;
[approval and safety](approval-and-safety.md) owns the latter. If a required
budget is unavailable, preserve completed safe work and report the required
check as unexecuted with its next owner. Never change a command or wrapper to
evade a resource guard, disable a required check or report a false result.

Every repository-static child selected by the validation-surface contract runs
through the [validation runner](../../scripts/run-validation-lane.py), which
owns the reviewed limit constants. The envelope bounds execution time and
retained stdout and stderr independently, uses one monotonic cleanup deadline,
and drains both streams concurrently in bounded read chunks.

The runner starts each child in its own session/process group. Timeout, either
pipe overflow, pipe failure, or pipes held by descendants after the direct
leader exits is `FAIL`.

### Result vocabulary

- `PASS`: the named check ran over the stated scope and met its acceptance
  condition.
- `NOT_RUN`: the named check did not execute. A selected required gate with this
  result blocks completion and cannot enter PASS cache or signed proof. A check
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

### Semantic review

Routine repository meaning checks previously repeated by a human use both
applicable automated checks and an independent read-only agent review. This
includes acceptance/implementation alignment, document completion or
supersession, ownership, and consistency with current contracts. When both
parts pass with no unresolved finding, do not request another human semantic
confirmation for the same scope and evidence snapshot.

- Run the applicable checks selected by the validation registry. Automation
  establishes only what those checks cover; the reviewer examines remaining
  meaning against the actual diff, current owners, acceptance criteria and
  command results, rather than endorsing the author's summary.
- Select a reviewer with the relevant registered responsibility who did not
  author or modify the reviewed changes. A separate agent identity and a
  read-only assignment are required; an author cannot certify their own work
  by changing roles. The reviewer reports findings without repairing files.
- Record the checked snapshot, check results, reviewer identity, inspected
  scope, findings and disposition in the existing handoff evidence. The writer
  repairs findings; refresh affected checks and independent review after
  changes. Reuse unchanged evidence under the validation lane contract.
- A failed required check or unresolved finding blocks completion. Missing
  applicable automation or an unavailable independent reviewer is an explicit
  evidence gap, not PASS; route it to the responsible owner. Human judgment is
  needed for unresolved intent, conflicting authority or a decision reserved
  to the request owner, not routine repetition of a completed review.
- This review rule supplies quality evidence, not authorization. Explicit
  human/operator approvals, protected external actions and required hosted
  reviews remain governed by their existing owners. Native and live claims
  still require the corresponding observed evidence.

### Agent evaluation evidence

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

### QA admission and retirement

Admit a recurring check only for a current document contract or actual
repository-purpose surface: document profiles, forms, frontmatter, relations,
links and status; GitOps, Kubernetes, Docker, reference project templates, web
content, Vault configuration and external-service interfaces where present.
Shared selection, commit, release, secret and runner controls that enforce
those contracts also need bounded regression coverage. Keep separate rules
when their input, threat model or failure meaning differs.
An old name, a slow run or a failure alone does not prove a test is obsolete.

For a one-use, legacy or deprecated check, first transfer any ongoing
protection to its durable owner, including normal Archive catalog, lifecycle,
link and content integrity apart from historical cutover completion proof.
Then remove the old caller and registration, remove its dedicated helper,
fixture and test when no consumer remains, and preserve necessary past results
in the existing Task, Archive or Git recovery owner. Do not add a new Spec or
progress ledger solely to retire old QA. Ordinary document changes select
profile, relationship, link and state checks; executable behavior changes get
focused negative and boundary regressions. A one-time Spec or Task migration
test is not a permanent gate after its outcome is retained.

Optimize in this order: remove duplicate leaves, separate content validation
from implementation regression, share parsing and Git reads inside one run,
select by changed impact, then reuse only a narrowly proven result. Measure
before claiming a cost or speed improvement. The selected registry contract,
not a policy sentence, owns the exact gate list and per-check limits.

### Ordinary document selection

An ordinary authored document or README router change that alters only prose
or navigation selects the common diff, style and commit-message checks plus
document content checks for profile, relationships, links and lifecycle state.
Do not select repository-wide quality, agent, infrastructure or unit sweeps
gates solely because the changed path is Markdown. A change to a governance,
provider or native contract, a Stage 99 form, schema or registry, or executable
implementation is a contract or behavior change: select its necessary focused
regressions and affected gates under the owning validation registry. Keep
document authoring or status-sync commands explicit; no validator or hook
automatically invokes a writer. Document link checks remain local as specified
above.

### Delivery ownership

| Route | Required owner and evidence |
| --- | --- |
| Routine editing | Run focused behavior checks and selected affected `quick` checks over changed working-tree bytes. |
| Local commit | Review the logical index, run selected exact-index `staged` QA, required lint and format checks on the final index immediately before commit, and actual commit-message validation, then commit with active hooks. An identical hook leaf already run over the same index must not be invoked a second time manually. |
| Feature push | Preserve checked commit evidence and observed push result; pushing adds no QA leaf for unchanged inputs. |
| Pull request | Observe required hosted branch or repository metadata and selected style checks at the exact PR SHA and run identity. Hosted style does not certify local purpose checks or document content; remote protection remains `DEFER` when unobserved. |
| Deployment | If a deployment workflow exists, observe its selected style check at the actual deployment SHA/run before deployment. Without such a workflow or run, retain `NOT_RUN` or `DEFER` for that lane; repository files alone cannot certify deployment. |
| Main integration | Compare the integrated tree and history with checked inputs. Run only checks invalidated by a changed input; an identical fast-forward needs no repeat. Record the actual merge and any remote required-check result separately. |
| Local handoff | Resolve tool, time, output and native approval preflight for applicable selected gates and named unit regressions, including continuing Archive and security guarantees. Do not select blanket discovery or a retired full/ci sweep merely to close the task. |

The registry selects gates within a profile. Reuse only a successful result for
identical declared input bytes and history, configuration, tool identity, scope,
mode and trust; changed inputs require a fresh result. A static workflow file
cannot establish hosted execution or remote branch protection.

### Canonical completion sequence

1. **targeted**: reproduce changed behavior and run focused checks while implementing.
2. **quick**: during iterations, run selected affected checks when the
   working-tree input differs or independent working-tree evidence is needed.
   Record the selection. If the required staged run demonstrably covers the
   same leaf with equivalent bytes, configuration, tool, scope, mode and trust,
   record `quick` as `NOT_RUN` and unrequired for completion; matching paths
   alone do not establish that equivalence.
3. **each logical commit**: inspect status and the unstaged diff, stage only the
   reviewed logical set, inspect the cached diff, run `git diff --check` and
   `git diff --cached --check`, then selected exact-index staged QA and required
   lint/format checks immediately before the commit. Validate the actual
   message under Git policy and commit through normal active hooks;
   record the leaf actually run and do not duplicate it merely because the
   hook and manual command share a caller boundary.
4. **delivery validation**: review the selected focused units and purpose gates
   against the final branch input. Record hosted branch metadata and selected
   style at their own PR or deployment SHA/run when observed. Retired full/ci
   and blanket unit discovery add no completion gate. Recheck an integrated-main
   input only to the extent changed bytes or history invalidate prior evidence.
5. **repair and refresh**: inspect formatter findings, explicitly fix selected
   files, review/restage changed bytes and refresh affected evidence. QA itself
   never fixes source files. A failed required delivery check keeps the work incomplete.
6. **evidence handoff**: record the checked snapshot and any subsequent Task-only
   changes separately, validating those document changes without a self-SHA or
   elapsed-time rewrite loop. Review final diff scope and remaining acceptance using the semantic review
   contract above.

For a no-commit request preserve the index and record staged/message evidence
as N/A. Input identity includes bytes, base/history, configuration and mode;
a matching filename set alone never justifies evidence reuse.

Use raw NUL-delimited machine paths for changed/staged path transport. Do not
reconstruct them with newline iteration or filtered display output. Preserve
runner boundary failures and optional-tool deferrals rather than treating them
as successful selected coverage.

### Handoff evidence contract

Record in the owning Task or approved evidence record:

- scope, changed paths, and acceptance IDs;
- the snapshot the work sits on: branch, HEAD, and the base it diverged from;
- commands and tool/version, with each ordered completion-step result;
- separate lane results and limitations;
- the approval boundary in force: what was authorized and what was not;
- reviewer identity and disposition;
- rollback commit or bounded rollback procedure;
- residual risk and next owner.

A field may state `none` or `DEFER` with a reason, but must not silently
disappear. Do not copy raw child payload or sensitive diagnostics into evidence.

These fields carry a handoff between providers as well as between people. The
receiver re-observes Git, the owning Task, and the canonical owner before
acting; a recorded snapshot says which state the evidence described, and a
recorded boundary keeps a past authorization from being read as a standing
one. Neither field grants authority, and a stale record never widens it.

### Supply-chain identity

Retain immutable identities where byte identity is the security contract:
pinned external Actions/hooks, resolved dependency artifacts, sealed evidence,
or Git-backed recovery objects. Their owning contract records purpose and
refresh/recovery procedure. Branch HEADs, current docs, local validators, and
inventory counts are not policy pins.

## Validation and Refresh

Refresh this policy when evidence semantics change, not when a corpus count or
implementation constant changes. Preserve the distinction between repository,
provider-runtime, hosted CI, and live checks. Formatters or deferred tools
cannot silently advance a task to completion.

## Related Documents

- [Validation Routing Registry](../../scripts/validation/registry.json)
- [Approval and Safety](approval-and-safety.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)
- [Git Policy](git.md)
- [Formatting and Linting Policy](formatting-and-linting.md)
