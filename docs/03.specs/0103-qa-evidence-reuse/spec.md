---
title: "QA Evidence Reuse Across Delivery Boundaries"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103"
---

# QA Evidence Reuse Across Delivery Boundaries Technical Specification

## Overview

This work unit removes repeated equivalent QA and test execution across local
commit, push, pull request, merge, and post-merge main validation. Successful
main updates also publish one immutable commit tag. Each required
gate executes once for a proven-equivalent input; a reused result names its
actual successful source. Changed input, Git history, toolchain, or environment
receives a new check. The request owner approved this design direction for Spec
authoring on 2026-10-01. Plan and implementation review have not occurred.

The current [Requirement Package](../../01.requirements/0003-workspace-agent-governance-platform.md),
[Architecture Description](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
[quality policy](../../../.agents/governance/quality.md), and
[validation registry](../../../scripts/validation/registry.json) are inputs.
The QA entrypoint is scripts/qa.py; ci aliases the full gate set. A single full
run already executes unit discovery and manual pre-commit once each. Current
duplication occurs across local final full, PR hosted full, and main push hosted
full. GitHub reported 16m37s for PR #115 QA in [run 36558654976, attempt 1](https://github.com/buenhyden/hy-home.k8s/actions/runs/36558654976),
whose API head SHA was 6b80bf2886c1c6e0cd27021cad49da28170007b4,
and 13m49s for [main run 36561110350, attempt 1](https://github.com/buenhyden/hy-home.k8s/actions/runs/36561110350)
at 0ed105b832d85c88b1000ad58959531d1ae23cae. The PR checkout SHA was
not recovered from the historical run; these durations are motivation, not
reusable gate evidence or target budgets.

## Strategic Boundaries & Non-goals

- Scope includes QA routing and evidence identity, the hosted QA workflow,
  local completion rules, immutable main tag publication, affected security
  contracts, regression tests, and current usage guidance.
- The validation registry remains the single gate-selection and argv owner.
  Validators retain independent meanings. The bounded runner remains the
  executor; no parallel gate catalog or external cache service is added.
- PR hosted CI owns final full evidence for PR delivery. Local-only handoff
  retains local full. Local evidence cannot satisfy a hosted claim.
- Git commit hooks, actual-message validation, branch protection, and required
  CI summary remain active. No global/private hooks or settings are changed.
- GitHub Actions remains repository QA, not live CD. Provider-native, cluster,
  service, and deployment evidence keep separate lanes.
- This draft does not authorize workflow permission expansion, a remote action,
  or live mutation. The later Plan must review narrow actions: read on a
  hosted evidence lookup job, an independently protected required check, and
  scoped write access for tag publication. Reuse remains disabled until that
  check is enforced and observed. Tagging also requires an independently
  protected main verdict and enforced tag ruleset before activation.

## Contracts

### Delivery execution owner

| Boundary | Required evidence | Reuse boundary |
| --- | --- | --- |
| Editing | Focused behavior check and applicable quick gates | Identical local input and check contract only. |
| Each logical commit | Exact-index staged gates, diff checks, actual message, active hooks | Matching local scope and mode only; changed index or formatter output invalidates evidence. |
| Push | Committed bytes and normal Git transport/hooks | No added full QA solely for transport. |
| PR | Hosted full QA on the actual PR merge checkout and required ci-summary | Authoritative full run for PR delivery. |
| Merge | Required current PR checks and merge relationship | The merge command adds no local full run. |
| Main push | Actual integrated commit, source-proof verification, changed-input gates | Reuse only individually proven equivalent PR results. |
| Main tag | Successful final main verdict for the push event's exact commit | Create one immutable `main-<full SHA>` tag; same-target retry is a no-op. |
| Local main sync | HEAD, origin/main, clean state, ancestry | No full QA solely for fetching an already checked commit. |
| Local-only handoff | Local full on final bytes | Hosted result remains unclaimed. |

Feature branches have no hosted full QA on ordinary push; the current CI
workflow already limits QA events to PRs targeting main, main pushes, and manual
dispatch. Local editing runs focused checks; quick runs at the required
checkpoint when the affected input snapshot changes, including new bytes at
the same path. Editing does not launch full on every save or feature push. Each
logical commit still checks its exact index and installed hooks. PR branch
policy runs on PRs, integrated-history gates run on main, and explicit manual
dispatch keeps full as an operator-selected diagnostic path.

The complete required gate set must be satisfied at the final delivery
boundary by an actual successful run on the required input or a verified
reference to one. Missing, skipped, deferred, cancelled, and failed gates do
not satisfy it. The PR branch-policy job remains PR-specific. The required
ci-summary fails closed and never accepts a skipped required QA job as success.

### Equivalent input and result identity

The registry may declare a gate eligible for reuse and its result dependencies.
The default is not reusable until its entire dependency set is audited. Identity
includes exact file bytes and modes, scope, gate ID, argv, validator and config
bytes, tool/dependency versions, execution mode, and relevant environment.
History-sensitive checks additionally include base, candidate commit, named
refs, ancestry, or other Git state they read. A matching tree alone does not
identify gitops-change-set, Archive, document-lifecycle, or any unclassified
gate. Mutable runner labels and Python minor versions do not prove a matching
hosted toolchain.

Quick, staged, full, and hosted CI retain distinct snapshot/evidence meanings.
Cross-mode reuse requires a separate proven equivalence contract. Eligible
quick-to-staged gates may reuse one result only when exact working-tree and
index bytes, modes, scope, base, configuration, and gate behavior match. An
unstaged working tree cannot replace the exact index. Formatter rewrites, source repair,
new untracked files, configuration or validator changes invalidate affected
results. A filename match or selected-path count does not prove scope equality.

The current unit-tests aggregate includes tests that inspect Git history and
the checkout. It must not be declared tree-pure as a whole. Implementation must
classify or separate independently runnable test groups before reusing them
after merge, preserving complete discovery and coverage of the full/ci suite.
Unclassified groups run normally. Manual pre-commit, YAML, and secret scanners
require their own contract review; similar names are not equivalent rules.

A reused gate reports REUSED with the source gate, exact input identity,
run/attempt/job, and eligibility decision. REUSED is an evidence disposition,
not a new process PASS. Reports distinguish actual runs from verified reuse.
No incomplete or failed subprocess result can become a source of reuse.

### Hosted provenance and trust

A separately protected required check, controlled outside the PR-editable
repository checkout, owns the PR reuse eligibility and publishes an independent
main-push verdict. It checks the complete required gate set and source evidence
on both events, including newly executed history-sensitive gates; the merged
workflow's green ci-summary alone cannot certify post-merge reuse. Before
activation, the operator must install or select that check, verify its source
and permissions through authenticated settings read-back, and prove that PR
edits cannot rename or replace it. The current main protection has no required code-owner approval
for CI or validator paths. A policy sentence, PR-authored ci-summary job, or
pinned verifier merely called by a PR-editable workflow is not an independent
control. Until the separate check is enforced, main push executes full QA and
does not consume PR proof for skipping gates.

The protected verifier runs after a successful PR full QA job in an isolated
execution context. It derives the PR event checkout commit/tree from a trusted
workflow and GitHub/Git identity, records the successful source run, attempt,
job, PR/base/head, complete gate results, and tool/contract identity. A
bounded machine-readable record is tied to that run. The verifier derives
the complete gate verdict from provider-authenticated job/step conclusions and
the unchanged trusted runner/registry contract; QA stdout and its artifact
are diagnostics, never independent authority. PR-controlled unit tests and
validators cannot write the verifier's checkout, executable, or output.
A record emitted later from the QA job's writable worktree is an untrusted
claim, not proof. Missing provenance prevents reuse; it does not turn a failed
QA job into success. The later Plan fixes schema, retention, and the protected
check's concrete host before any activation.

The main push verifier authenticates the successful source run and protected
check through GitHub, then compares the record with the actual integrated
commit/tree, PR relationship, workflow revision, and each gate input. Actions
API run head_sha names the PR branch head; it does not prove the synthetic PR
merge checkout tested by the workflow. A PR merge ref may disappear after
merge. The verifier uses the protected record's actual checkout identity and
durable Git objects, never a guess from head_sha. Missing or ambiguous run,
PR, job, or attempt relationships reject reuse.

The verified protected main tip before the entire integration is the trust
anchor. The push event before SHA and verified PR base must identify that tip;
absence or conflict forces full QA. The final commit's immediate parent is
insufficient for a multi-commit rebase or fast-forward. If any PR commit
changes the proof producer, registry, QA runner, CI workflow, dependency
lock, or evidence verifier, the protected check rejects reuse and requires
main full. A PR-produced artifact or successful job cannot establish its own
trust anchor. A changed control contract becomes a new baseline only after
reviewed main full QA and authenticated read-back of the protected check.

All fetched bytes are untrusted data: parse with finite size and schema
bounds, cross-check against GitHub and Git, and never execute content or
extract untrusted paths. Reused main results cannot recursively serve as
source proof. The lookup has only actions: read plus existing contents: read,
subject to security review and operator approval. A control-plane-change PR
that tries to alter the caller, verifier, or required check must be blocked
or forced through a separately reviewed full-validation transition; it must
not self-certify eligibility.

### Environment-specific checks

Installed local hooks and exact-index QA check a developer's commit boundary.
PR CI checks the immutable hosted merge checkout and locked dependencies.
Main push checks integrated Git history and any properties not proven by the
PR evidence. The same named gate executes at two boundaries only if its input
or trust claim differs. K8s plaintext-pattern scanning, Gitleaks, and
detect-secrets retain separate contracts. Labeling, greetings, stale issue
maintenance, and changelog workflows remain separate non-QA functions.

### Main commit tag

A push that updates `refs/heads/main` is the sole tag-publication trigger; a
PR merge is covered by its resulting main push, not a second merge event. A
feature push, PR check, manual QA dispatch, and tag push never publish a main
tag. After the complete main QA verdict and the independently protected
main verdict succeed for the push event's exact integrated SHA, publish the
lightweight `main-<40-hex SHA>` tag pointing to that commit. The protected
verifier must be active before tagging begins. It can attest a full main run
while PR-proof reuse remains disabled, then attest the full-or-reused gate set
after reuse activates. A PR-editable ci-summary cannot attest the tag by itself.
The tag is a checkpoint of validated main history, not a release tag or a
version-support promise. The repository currently has no tags; the existing
changelog workflow matches only `v*.*.*`. No SemVer, changelog, or release
automation is implied.

The publisher validates the event repository, branch ref, full SHA, successful
main verdict, and tag target through authenticated GitHub/Git data. It creates
a missing tag without force. A retry finding the same tag at the same commit
is a no-op; a name collision or different target fails visibly and is never
rewritten or deleted automatically. If one push contains multiple commits,
only its validated `after` SHA is tagged. A later main push has a different
name and may run independently. A failed QA or tag-write step leaves no
false success; the publication status is separately observable and retryable
without rerunning unrelated QA. Tag creation itself does not launch another
QA run.

Tag creation needs a narrowly scoped writer outside PR-controlled execution.
The Plan must choose a protected host and obtain operator review for any
`contents: write` permission; read-only QA jobs keep their current scope.
The writer never executes PR checkout files or untrusted artifact content.
An enforced `refs/tags/main-*` ruleset must limit creation to the publisher
and block updates and deletions even by that publisher, apart from explicit
operator bypass. Separate creation and immutability rules may be required so
a creation bypass does not also bypass update/delete restrictions. The
operator must read back the effective rules, bypass actors, and writer identity
through authenticated settings before enabling tagging. A normal writer's
attempted update and deletion must be denied. See [GitHub tag ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
GitHub documents that events generated with `GITHUB_TOKEN` do not normally
start another workflow run, so a token-created tag cannot be assumed to
trigger a tag workflow. This `main-*` tag intentionally does not match the
current changelog trigger; any future consumer must be specified and tested
separately. See [GitHub token event behavior](https://docs.github.com/en/actions/concepts/security/github_token)
and [workflow permission syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

## Core Design

scripts/qa.py retains profile and snapshot selection. The bounded runner
continues to produce one verdict per selected gate. A verifier first decides
whether a prior successful result covers that gate's declared input. Otherwise
the runner executes it. This is a decision layer over the current registry,
not a second gate-membership source. The independently protected check
attests to the PR full result before a main push can reuse it. The main
workflow always reaches a complete aggregate verdict. The tag publisher
consumes that verdict once per main push SHA and reports publication status
separately from the QA gate result. The independent
required check blocks a PR before merge when a control-plane change could
bypass main verification.

Three approaches were considered. Guidance-only cleanup leaves the two hosted
full runs. Tree or PR-head-SHA skipping loses history and checkout guarantees.
The selected gate-wise evidence route can eliminate proven repeat work while
retaining a normal full fallback. Test-group classification may take time;
unclassified unit tests keep running until their dependencies are proven.

Quality, Git, and work-lifecycle policy must assign final full to PR hosted CI
for PR delivery and keep local full for local-only handoff. Scripts guidance,
PR template, and hosted workflow notes must use the same sequence. Historical
completed Spec and Task evidence remains as observed.

## Data Modeling & Storage Strategy

The registry owns reuse eligibility and dependency dimensions. Local results
are bound to an exact snapshot and are not a permanent shared cache. Hosted
proof is a bounded record from the separately protected verifier, tied to
one source run and attempt; GitHub's own job conclusion remains the authority
for actual execution. A QA-job artifact is untrusted input to this verifier,
not sufficient proof. Task handoff records
references and limitations, not copied raw logs or cache contents. Expired
proof causes execution. No persistent database or repository credential is
introduced.

## Interfaces & Data Structures

- QA entrypoints remain python3 scripts/qa.py quick|staged|full|ci and retain
  isolated snapshots and bounded subprocess execution.
- Registry rows may declare a validated reuse class and dependency dimensions;
  missing or unknown fields mean execute. Full and ci gate parity remains
  tested from this registry.
- Gate evidence states gate ID, input identity, PASS or verified REUSED source,
  scope/mode, tool/config identity, and bounded diagnostics. Hosted provenance
  adds schema version, run/attempt/job, actual checkout commit/tree, PR/base/
  head, workflow identity, and the complete gate set.
- The post-merge verifier gives each gate an eligibility decision and reason.
  It cannot authorize a failed required gate to be skipped.
- Artifact size, field grammar, item count, and source comparisons are bounded
  and tested before a reuse decision.

## Edge Cases & Error Handling

- PR head, synthetic PR merge, and final merge commit can have different SHAs.
  Check actual tested checkout/tree and gate-specific history. PR head alone
  is insufficient.
- Squash, rebase, concurrent main advancement, and merge conflict can change
  tree or ancestry. They miss the reuse path and run affected gates.
- A rerun has its own attempt. Reject wrong repository/workflow/PR/attempt,
  failed/cancelled source, missing gate, incomplete job, or malformed record.
  A successful summary alone does not prove every source gate.
- A passing PR test may mutate the original checkout's post-QA proof producer.
  The isolated protected verifier rejects or cannot observe that mutated
  producer as its own code. A self-produced artifact cannot authorize reuse.
- Forks and modified PR workflows are lower-trust inputs. The proof producer
  and tool/config identities must match reviewed hosted evidence; otherwise
  main runs full. Artifact content is never executed.
- Formatter mutation, missing required tool, timeout, output overflow, escaped
  child, and cleanup failure retain their FAIL meaning. Optional-tool SKIP
  never becomes reusable PASS.
- Independent security scanners retain their original scopes and failure
  meanings even where they inspect some of the same files.
- Concurrent main pushes, retry, delayed publication, or a pre-existing tag
  must not move an immutable tag. A mismatched target fails for review; a
  matching target is an idempotent success.

## Failure Modes & Fallback / Human Escalation

API failure, expired proof, malformed or ambiguous record, source mismatch,
and ineligible input invoke normal gate execution. If execution then fails,
the required QA job and ci-summary fail. A rejected reuse never becomes a
diagnostic SKIP or synthetic PASS. Report reason without secret-bearing data.
The operator owns permission expansion, the independently required check,
tag-writer activation, and any ruleset change. Without observed activation
of the protected main check and tag ruleset, tag publication stays off and
the main QA path stays full. A reviewed revert restores full-on-PR and full-on-main
behavior without history rewrite.

## Verification Commands

The later Plan binds exact commands to the changed files and snapshots.
Focused checks include registry/schema and selection tests, QA runner call
counts, workflow/security contracts, and adversarial provenance tests.
python3 scripts/qa.py quick checks affected working-tree bytes, and
python3 scripts/qa.py staged checks each exact logical index. Final PR-hosted
python3 scripts/qa.py ci must pass on its actual checkout. Local-only handoff
uses python3 scripts/qa.py full. Main push reports its exact run and per-gate
PASS or verified REUSED dispositions. Tag publication reports the exact
main SHA, final verdict, tag target, and create/no-op/fail disposition. Local
workflow lint is repository-static evidence, not a hosted execution.

## Success Criteria & Verification Plan

| Criterion | Observable acceptance condition | Planned evidence |
| --- | --- | --- |
| VAL-QER-001 | Gate selection, argv, mode, and reuse declarations have one registry owner; full/ci required set stays aligned. | Registry and profile-contract tests. |
| VAL-QER-002 | An unchanged local gate input runs once, including proven quick-to-staged equivalence; same-path byte edits, index, untracked file, formatter, config, code, tool, scope, or mode-dependent change invalidate it. | Runner call-count and negative snapshot tests. |
| VAL-QER-003 | Local commit, PR, and local-only handoff run their assigned checks; local full is no longer mandatory before a PR hosted full. | Lifecycle/policy and fixture-flow tests. |
| VAL-QER-004 | Protected PR proof names the actual hosted checkout and complete successful gate set; QA children cannot modify proof code or output. | Isolated-verifier, passing-test mutation, and malformed-proof tests. |
| VAL-QER-005 | Main push reuses only authenticated matching PR gate results; changed Git base, ancestry, refs, or environment rerun affected gates. | Merge/squash/rebase and identity fixtures, then observed hosted run. |
| VAL-QER-006 | All unit tests remain discovered; only independently proven equivalent groups are reused. | Partition/discovery and invocation-count tests. |
| VAL-QER-007 | Missing, failed, cancelled, expired, forged, or ambiguous evidence and any PR-commit control change fall back to execution; execution failure reaches ci-summary. | Adversarial verifier, multi-commit changed-producer, caller spoofing, and CI-summary tests. |
| VAL-QER-008 | Reuse stays off until an independently protected required check is authenticated; it attests PR eligibility and publishes an independent main-push verdict over the complete gate set. Hooks, scanners, permissions, and native/live evidence stay intact. | Settings read-back, hostile-PR and green-ci-summary spoof tests, security review, Actions validator, and direct lane observations. |
| VAL-QER-009 | Feature pushes, PRs, main pushes, and manual dispatch run only their assigned checks; routine editing does not require full QA. | Event/branch matrix tests and focused/quick/staged/full invocation counts. |
| VAL-QER-010 | Once the protected main verdict and `main-*` rulesets are active, each successful main push publishes only its validated tip as immutable `main-<40-hex SHA>`; merge has no second publication, retries are idempotent, mismatched tags and failed verdicts publish nothing, and tag events cause no repeat QA. | Protected full-QA and protected reuse verdict fixtures, event matrix, exact-SHA/conflict and denied update/delete fixtures, authenticated ruleset/writer read-back, and hosted publication observation. |

## Traceability

These criteria implement the current Requirement Package without adding a
second requirement owner. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
places validation routing in the registry and distinguishes local from hosted
evidence. This draft does not edit an accepted ADR. A later Plan determines
whether a new structural decision is needed.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-001 | Registry identity and independent gate tests. |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-002 | Registry identity and independent gate tests. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-004 | Hosted proof, required summary, permission and security tests. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-005 | Hosted proof, required summary, permission and security tests. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-007 | Hosted proof, required summary, permission and security tests. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-008 | Hosted proof, required summary, permission and security tests. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-009 | Branch/event matrix and protected summary tests. |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-010 | Main push/merge event matrix, tag target and permission tests. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-003 | Lifecycle flow and proportional final validation. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-006 | Lifecycle flow and proportional final validation. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-003 | Local/hosted separation and source-run identity. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-004 | Local/hosted separation and source-run identity. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-005 | Local/hosted separation and source-run identity. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-002 | Malformed/missing-tool/fallback rejection tests. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-007 | Malformed/missing-tool/fallback rejection tests. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-001 | Affected/index/full/CI snapshot and execution-count tests. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-002 | Affected/index/full/CI snapshot and execution-count tests. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-003 | Affected/index/full/CI snapshot and execution-count tests. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-006 | Affected/index/full/CI snapshot and execution-count tests. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-009 | Branch/event matrix and invocation-count tests. |
| [REQ-0003-NFR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-005 | Fail-closed identity and aggregate verdict tests. |
| [REQ-0003-NFR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QER-007 | Fail-closed identity and aggregate verdict tests. |
