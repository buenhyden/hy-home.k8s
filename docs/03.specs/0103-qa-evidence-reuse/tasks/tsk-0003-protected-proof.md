---
title: "Protected App PR proof"
version: "0.1.5"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0003"
---

# Task: Protected App PR proof

## Overview

Execute [Plan WP-0003](../plan.md) against the approved [SPEC-0103](../spec.md). The local verifier is implemented and independently reviewed. The first hosted App check exposed a PR-head versus synthetic-merge check-target mismatch; a scoped local repair is independently reviewed. Protected required-check activation and reuse remain outstanding.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-004, VAL-QER-007, VAL-QER-008.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-003 | VAL-QER-004, VAL-QER-007, VAL-QER-008 | Follow Plan Task 3 RED, GREEN, review, and handoff steps | platform | In progress | First hosted App check observed; protected activation and repair trial DEFER | Hosted run/check and scoped repair evidence below. |

## Approval and Safety Boundaries

- **Allowed Paths**: .github/workflows/qa-verifier.yml; .github/workflows/ci.yml; scripts/qa_provenance.py; tests/test_qa_provenance.py; tests/test_ci_qa_workflow.py; one required Workflow Responsibility Matrix row in .github/repository-surface.md
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Operator review before verifier App creation/install, main-only environment secret, required-check settings, or control-code bootstrap
- **Static Validation**: python3 -m unittest tests.test_qa_provenance tests.test_ci_qa_workflow; python3 scripts/qa.py quick
- **Live Validation**: Authenticated verifier App ID and permission ceiling, environment policy, required-check source, hostile PR and control-change trials; DEFER until configured
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Disable App-sourced reuse, retain full main QA; never remove a required check without protected replacement.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

- Snapshot: branch `codex/qa-evidence-implementation`, starting HEAD
  `a30c021a324c337986536308e0e353d31140b480`, diverging from origin/main
  `0ed105b832d85c88b1000ad58959531d1ae23cae`. Implementation commit
  `21bfec9dee70f64a52044190c7d548657141a0ed` has tree
  `eeede8b5fdcd242ec5298c0a4398ff5572b4dd00`. The five approved
  implementation/test files, this Task, and the one required
  GitHub workflow-navigation row are changed. The supervisor authorized that
  row after the quality validator exposed the direct new-workflow dependency.
- RED: `python3 -m unittest tests.test_qa_provenance tests.test_ci_qa_workflow`
  failed because `scripts.qa_provenance` did not exist; 14 existing CI cases
  passed. GREEN: the same command passed 31 cases after implementation.
- The unchanged registry/runner and successful provider-authenticated aggregate
  QA step establish the complete required gate disposition. The verifier does
  not claim that the jobs API independently reports individual gate processes.
  Any optional or non-static gate in the full profile rejects proof.
- The trusted checkout step exposes the synthetic merge SHA as provider step
  metadata. Only after every PR commit's protected control tree matches main
  does the verifier interpret it; the durable Git commit must have exactly the
  authenticated base/head parents. The Actions `head_sha` remains the PR head.
  Missing Git objects, incomplete pagination, changed attempt and stale PR state
  fail closed. Repository scripts and skill-owned script directories are
  conservatively protected to cover transitive imports, including additions and
  temporary edits later reverted.
- A first read-only step authenticates the source; the publication step repeats
  authentication and compares the bounded proof before reading the App key.
  The App installation must have exactly metadata/read, actions/read,
  contents/read, pull-requests/read and checks/write. The minted token is
  repository-restricted and revoked after the check request. No publisher key
  is referenced. The proof is at most 16 KiB, version 1, and expires after
  30 days for consumers. API bytes, pages, calls and network waits are bounded.
- At the initial implementation checkpoint, the App check targeted the tested
  merge commit. Its complete proof records
  dependency-lock identity but explicitly leaves runtime identity `unattested`;
  Task 4 must establish actual tool/environment equality before gate reuse.
  Local evidence and same-name checks from a different App are rejected.
- Static workflow security: `python3 scripts/validate-github-actions-security.py
  --root .` PASS. The initial invocation omitted the mandatory root argument;
  corrected immediately. `python3 -m black --check ...` was unavailable;
  the existing pinned `ruff-format` hook formatted the three changed Python
  files instead. The pinned zizmor check now passes with the reviewed inline
  trigger exception. The first retained quick run passed 11 gates and failed
  `repository-quality` because the new workflow lacked its required matrix row
  in the GitHub hub. The supervisor authorized that one-row correction; no
  validator contract was weakened.
- Validation after that repair: `python3 scripts/qa.py quick` PASS, 12 affected
  gates on seven changed paths. That checkpoint preceded the final explicit
  JSON Content-Type header. `python3 scripts/qa.py staged` PASS, eight gates on
  the six-file implementation index whose tree is recorded above; it includes
  the final header. Both unstaged/cached whitespace checks passed. The exact
  message `ci: add isolated protected PR provenance verifier` passed pinned
  Commitizen before the commit. Git used the existing executable
  `scripts/githooks` wrappers; no hook configuration or bypass flag changed.
- Tools: Python 3.12.3, pre-commit 4.6.1, pinned ruff v0.16.5 and zizmor v1.24.1.
  Repository-static checks only; no full QA or unit discovery was repeated for
  this editing/commit boundary. PR hosted CI or final local-only delivery still
  owns final full evidence. An initial exploratory quick process completed
  without retained output and supplies no PASS claim; the retained runs above
  supersede it over changed inputs.
- Review: independent `task3_zizmor_review` security-auditor accepted the single
  inline `dangerous-triggers` exception after finding no concrete route from PR
  code, cache or artifacts to verifier execution or credentials. The initial
  pinned zizmor run reported that trigger as HIGH; the exception applies only
  at this workflow's `on` key, with its isolation rationale beside it. This is
  a scoped trigger disposition, separate from the subsequent independent
  code and static security reviews recorded below.
- At the initial local checkpoint, hosted/live DEFER: no verifier App ID,
  installation permission read-back,
  environment branch policy, required-check source setting, hosted run/attempt,
  hostile-PR or control-change trial is available. `QA_PROVENANCE_ENABLED`
  defaults off; `QA_REUSE_ENABLED` remains disabled and main keeps ordinary full
  QA. Static YAML cannot enforce or prove a main-only environment policy.
- Original operator sequence, partly observed below: merge inert code through
  ordinary full QA; install the
  verifier-only App and configure `qa-control` for main only; set the CI workflow
  ID and App ID; observe an App-authored check; pin that App ID using branch
  protection; run hostile-PR/control-change trials; only then consider reuse.
  The ruleset alternative needs separate permission review and is not implied.
- Authorization: scoped local code/tests/Task and logical commits only. No
  remote settings, secrets, Apps, environments, rulesets, variables, pushes or
  tags were created or changed. Rollback disables proof/reuse activation and
  preserves full main QA. A reviewed forward revert must cover the final
  combined implementation: fix `606de370ab844434fd58cb86f77cb5a3b9adcfb6`
  and original `21bfec9dee70f64a52044190c7d548657141a0ed`. Preserve evidence
  history; do not rewrite branch history.
- Review fix round 1 resumes from `5a8401639349e32308b5083c57545e0c7196131a`.
  Independent `review_task3_code` found that a fork PR can have an empty
  workflow-run PR relation, leaving a required App check pending. RED: the
  new valid-fork provider fixture failed in a 34-case focused run. GREEN:
  all 34 focused cases passed after bounded authenticated PR discovery.
  Fix commit `606de370ab844434fd58cb86f77cb5a3b9adcfb6`, tree
  `8f165c615dd88f8db27e374fd760f669e1154642`, passed all 34 focused cases,
  12 changed quick gates and 12 exact-index staged gates. Pinned ruff, both
  whitespace checks and the actual-message Commitizen check also passed.
- The fallback queries open PRs against main using the URL-encoded provider
  head repository owner and exact branch. It requires exactly one candidate,
  then re-reads that PR and binds repository IDs, branch, head/base SHAs and
  the current synthetic merge SHA to the already authenticated run/attempt.
  The durable merge-parent and control-closure checks remain mandatory.
  Missing, ambiguous, stale, changed-repository and changed-branch candidates
  reject proof before App-key access. No head-SHA-only inference is used.
  No workflow-path relaxation, permission or activation change is included.
- Independent scoped re-review of fix commit
  `606de370ab844434fd58cb86f77cb5a3b9adcfb6`:
  `review_task3_code` returned Spec PASS / quality Approved with no residual
  finding; `review_task3_security` returned static security PASS with no
  actionable spoofing finding. These dispositions approve the local
  implementation; they do not establish hosted enforcement or Spec completion.
- Review evidence commit `ab2747fdd5ddf4ce7b4d70ab5a77c5924c37e66c`
  changed only this Task document. On its checked and committed tree
  `b23d5bc00b6b84a8aa2da18a49d0414d34e0172c`,
  `python3 scripts/qa.py quick` PASS (six affected gates) and
  `python3 scripts/qa.py staged` PASS (six exact-index gates).
  `git diff --check`, `git diff --cached --check` and the committed-diff
  whitespace check passed; the actual commit message passed pinned Commitizen.
  The final quick ran on stable input after an earlier run overlapped the
  message hook's temporary stash; that earlier run is not final evidence.
- Next owner: operator for App/environment/required-check configuration and
  hosted trials, with supervisor reconciliation of the final delivery package.
  Task status remains in progress; hosted activation remains DEFER.

### Hosted supplement — 2026-10-02

- PR [#118](https://github.com/buenhyden/hy-home.k8s/pull/118) passed the
  disjoint 1+22 QA partition and `ci-summary` in [CI run
  36945619228](https://github.com/buenhyden/hy-home.k8s/actions/runs/36945619228).
  The isolated [verifier run 36947289910](https://github.com/buenhyden/hy-home.k8s/actions/runs/36947289910)
  succeeded and App 5156553 authored successful `qa-provenance` check
  110652259257 on tested synthetic merge `25f2ec19`. The triggering
  workflow run's `pull_requests` array was empty, confirming the authenticated fallback was
  used. The App's public permission map is Actions/read, Checks/write,
  Contents/read, Metadata/read and Pull requests/read. Secret values were not
  read.
- Pinning `qa-provenance` to that App as a required check left the PR
  **UNSTABLE**: GitHub required the check on the PR head, while this check was
  attached to the tested merge commit. Strict branch protection was restored
  to its prior `ci-summary`-only requirement before PR #118 merged as
  `c2987739`. An App-authored success on the merge SHA is therefore not proof
  of effective protected PR enforcement.
- The scoped repair moves the check envelope to the authenticated PR head;
  proof still binds the v3 synthetic merge checkout. Focused tests: 94 PASS
  on the repair working tree. PR [#119](https://github.com/buenhyden/hy-home.k8s/pull/119)
  passed disjoint hosted QA and `ci-summary` on run 36951722638, then merged
  as `98a6b00e`. Its protected-control change was rejected by verifier run
  36953277086 before App key access, as designed. Main full QA run
  36953307326 and App 5156553 `qa-main-verdict` check 110675592214 passed on
  that merge commit. PR [#120](https://github.com/buenhyden/hy-home.k8s/pull/120)
  passed hosted QA on run 36954162376 and merged as `cdd1a0b8`; its CI lock
  change is also protected control input. Hosted ordinary-PR head-check trial,
  App-pinned required-check read-back and hostile/control-change enforcement
  trials remain DEFER; the pre-pinning control-change rejection is observed. Keep
  `QA_REUSE_ENABLED` off and full main QA active. Next owners: operator and
  supervisor for a protected trial and
  exact source/SHA/check read-back. Rollback: retain `ci-summary` protection
  and full main QA; disable provenance/reuse if the trial fails.

### Protected control transition — 2026-10-02

- The App-pinned positive PR #121 used CI run 36956836213 and verifier run
  36958534800; `qa-provenance` check 110686923231 passed on head
  `a8d63142c2d4b07901132a44e978afc093f6e312`. Strict branch protection
  read-back required `ci-summary` from App 15368 and `qa-provenance` from App
  5156553. The control-change negative PR #122 passed CI run 36958945183
  and `ci-summary`, but verifier run 36960429886 rejected it before App-key
  access. It remained `BLOCKED` and was closed without merging.
- Main merge `3fa2f14d57d7d2cd0886e8eb5c7c8f7ff71f0c2a` exposed a narrow
  control-code defect: the transport route guard rejects GitHub's authenticated
  `compare/<40-hex>...<40-hex>` endpoint. `qa-source` therefore selected full
  fallback in CI run 36960567064. `QA_REUSE_ENABLED` was set back to `false`;
  `QA_TAG_ENABLED` remains off. A RED route test reproduced the rejection;
  the corrected guard accepts only the exact repository and two SHA segments,
  retains traversal rejection, and 54 focused tests pass. A read-only hosted
  replay using the original main control bytes and corrected route matched PR
  source run 36956836213. This replay is diagnostic, not hosted activation.
- Pending transition owner: repository operator acting under the user's
  delivery authorization. Target: one reviewed control-fix PR at an exact
  recorded head SHA. Before merge, require its successful hosted full QA and
  `ci-summary`, independent code/security review, no other open merge activity,
  reuse and tag flags off, and protected settings read-back. The verifier
  intentionally rejects changed control code. Independent security review
  found that dropping `qa-provenance` and relying on PR-authored `ci-summary`
  alone would conflict with the no-bypass policy and Plan rollback. Keep both
  App-pinned checks required while an independently enforced replacement or
  an explicit operator-approved policy exception is resolved; do not merge a
  blocked PR. After an authorized transition, observe full main QA, a fresh
  protected main verdict, an ordinary PR App check and a control-change denial
  before re-enabling reuse. Rollback retains the two-check protection, full
  main QA and disabled tags. This records a pending transition, not a completed
  hosted reuse result.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-003](../plan.md#work-breakdown) | First hosted App check observed; protected activation DEFER | Scoped fix `606de370ab844434fd58cb86f77cb5a3b9adcfb6`, tree `8f165c615dd88f8db27e374fd760f669e1154642`; initial focused 34, quick 12 and staged 12 PASS; PR #118 and verifier run 36947289910 exposed the PR-head target mismatch; repair focused 94 PASS, hosted trial pending. |
