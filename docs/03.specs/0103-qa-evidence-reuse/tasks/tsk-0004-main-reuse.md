---
title: "Main gate-wise reuse"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0004"
---

# Task: Main gate-wise reuse

## Overview

Execute [Plan WP-0004](../plan.md) against the approved [SPEC-0103](../spec.md).
Local implementation provides an isolated PR gate, its 22-gate complement,
fail-closed main reuse, and an independently authenticated main App verdict.
The local implementation is independently reviewed. Hosted PR and main fallback
trials are recorded below; hosted reuse and Spec completion remain unclaimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-005, VAL-QER-006, VAL-QER-007.
- [Task 3 proof boundary](tsk-0003-protected-proof.md): the existing shared QA
  runtime is `unattested` and cannot authorize hosted gate reuse.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-004 | VAL-QER-005, VAL-QER-006, VAL-QER-007 | Follow Plan Task 4 RED, GREEN, review, and handoff steps | platform | In progress | PR partition and full-main fallback PASS; reuse pending | Commits, focused tests, exact-index checks, and per-gate matrix below. |

## Approval and Safety Boundaries

- **Allowed Paths**: scripts/qa.py; scripts/run-validation-lane.py;
  scripts/validation/registry.json; scripts/validation/registry.schema.json;
  .github/workflows/ci.yml; .github/workflows/qa-verifier.yml;
  scripts/qa_provenance.py; scripts/qa_provenance_records.py;
  scripts/qa_provenance_hosted.py; scripts/validate-ci-python-contract.py;
  tests/test_qa_runner.py; tests/test_run_validation_lane.py;
  tests/test_ci_qa_workflow.py; tests/test_validation_profiles.py;
  tests/test_qa_provenance.py; tests/test_qa_provenance_hosted.py;
  tests/test_validate_ci_python_contract.py; this Task and its ignored report.
  The supervisor explicitly approved the verifier workflow, two focused proof
  helpers, and canonical CI validator/test extensions. Other tasks were preserved.
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault
  mutation, archived Spec bodies, and unrelated repository surfaces.
- **Approval Required**: operator activation only after protected PR/main App
  checks and configuration read-back. `QA_REUSE_ENABLED` defaults off and also
  requires `QA_PROVENANCE_ENABLED`; ordinary main and manual runs execute all gates.
- **Static Validation**: focused seven-module unittest set; quick and staged QA;
  workflow security, canonical CI Python contract, pinned formatting/lint and
  actual-message Commitizen checks.
- **Live Validation**: exact PR/main SHA, run, attempt, isolated job, expected App
  author, complete gate verdict and protection read-back; PR partition and full fallback observed, reuse pending.
- **Secret / Vault Handling**: no secret values, App keys or publisher credentials
  used. The separate lookup job has only contents/actions/pull-requests/checks
  read permissions. Checks:read authenticates the expected App's original check.
- **Rollback Plan**: disable `QA_REUSE_ENABLED` first; main returns to 23 fresh
  gates and full-main verdict v2. Keep required protected checks until a reviewed
  replacement exists. A forward revert must account for all three Task 4 code
  commits recorded below.
- **Evidence Location**: this Task; working notes remain ignored under
  `.superpowers/sdd/plan/task-4-report.md`.

## Verification Summary

### Snapshot and trust contract

- Started at `37ac714a616948277b90a887f44744018e5b5c1f` on
  `codex/qa-evidence-implementation`. Interim commit
  `13e8aadbed479294f46bd7557aa1a5b411fe346c`, tree
  `b21e271bdfa10ebbf2f00c7fab9579817cf22687`, provides the protected full-main
  verdict and rejects source-shaped unauthenticated runner reuse. Independent
  `review_task4_interim` found no concrete correctness/regression issue in that
  full-only slice; it was not Task 4 completion evidence.
- Candidate code commit `1a13ea42f36676038f60eb8a9e436866c1564e82`, tree
  `825694d62637dc09b25ea1936d9c5bc357c43c4d`, implements the actual isolated route.
  The registry retains the sole full/ci list of 23 IDs. Its one explicit hosted
  opt-in is `agent-evaluation-cases`; PR jobs derive disjoint 1+22 partitions.
  Three exact, mutually exclusive QA steps cover full, PR complement and main
  reuse. The canonical validator rejects missing, duplicate, overlapping,
  unconditional or arbitrary environment-selected commands.
- The isolated job has no cache, package installation, secret or other PR test.
  It executes `/usr/local/bin/python3 -I -B` in the single-platform image
  `docker.io/library/python@sha256:c90be507635af19768837aa7eeb2f4ce89a74d62962a335497b9df8edfb7f19d`
  on `linux/amd64`. The helper is bootstrapped from raw Git object bytes before
  importing checkout modules. It checks every raw committed file/symlink and
  mode, the index, absence of extra files, and unchanged checkout before/after
  evaluation. The candidate uses a fixed complete environment and stdlib plus
  the protected bounded-I/O module; it does not consume history, refs or provider
  state. Whole-tree identity conservatively includes all candidate data/imports.
- The protected verifier audits every PR and integrated push commit's control
  closure, including every tracked root or nested `.gitattributes` and transient
  edits later reverted, before interpreting source metadata. It authenticates the exact run/attempt, five job identities,
  checkout/step ordering, isolated success and registry union. Container identity
  follows from the immutable trusted workflow contract and provider job success;
  the jobs API does not independently report an OCI digest. No log, artifact,
  cache or PR-provided JSON can establish a verdict.
- PR proof v3 adds the isolated job/runtime/input record. Shared QA runtime stays
  `unattested`; legacy v1 cannot authorize reuse. Full main proof v2 covers 23
  fresh PASS results. Reuse main proof v4 covers 22 PASS and one REUSED, with
  original PR/run/attempt/job/checkout/input. Main records cannot be PR sources.
  Records remain bounded to 16 KiB and expire after 30 days.
- Lookup authenticates the expected App check and independently rebuilds its
  complete proof. Main reuse requires exact final tree and runtime/argv/env/
  registry/workflow/lock identity, a unique merged PR, and unchanged protected
  history. Provider-evaluated lookup step metadata binds original push `before`
  and source `head_sha`; no `HEAD^` approximation is used for multi-commit pushes.
  The App verifier repeats lookup and compares the source before publication.
  Missing, stale, ambiguous or changed evidence selects full QA at lookup; a
  claim that becomes unverifiable later rejects the main App verdict.
- The evaluator gate stays separate from the aggregate `unit-tests` gate.
  History/ref readers `archive-cutover`, `document-lifecycle`, `gitops-change-set`
  and all aggregate unit tests always execute on main. Existing evaluator unit
  tests exercise bounded fixture roots and expectations; they do not invoke the
  same complete root gate as a second CI owner. Local cache identities still bind
  HEAD, refs and environment and are never used across PR merge/main commits.

### Executed local validation

- RED evidence: main verifier entry absent; unauthenticated provider-shaped
  runner candidates skipped failed children (nine combinations); hosted module
  and isolated workflow job absent; canonical validator rejected the new
  partition; a raw-checkout test exposed a staged extra import outside HEAD.
  GREEN follows implementation and the index/leaf-stability fix. Negative proof
  fixtures cover merge/squash/rebase, multi-commit push, advanced base, changed
  named refs, runtime/lock/control changes, expired or wrong-App proof,
  changed attempt, failed candidate, duplicate execution and forged lookup.
- `python3 -m unittest tests.test_qa_runner tests.test_run_validation_lane
  tests.test_qa_provenance tests.test_qa_provenance_hosted
  tests.test_ci_qa_workflow tests.test_validation_profiles
  tests.test_validate_ci_python_contract`: 266 PASS in 426.198 seconds. After
  final raw-index hardening, proof/hosted modules: 41 PASS in 1.221 seconds.
  The full/ci/complement orchestration fixture substitutes bounded marker
  subprocesses for every gate: counts 23/23/22, with a candidate failure failing
  the full route. It never launches nested full QA.
- `python3 scripts/qa.py quick`: eight affected gates PASS on 15 paths.
  `python3 scripts/qa.py staged`: eight exact-index gates PASS on the candidate
  tree recorded above. No full QA or aggregate unit discovery was repeated.
- `python3 scripts/validate-ci-python-contract.py --root .`: PASS, one dependency
  owner and three direct pins. `python3 scripts/validate-github-actions-security.py
  --root .`: PASS. Pinned ruff-format, ruff-check, both whitespace checks and
  actual-message Commitizen PASS. Existing hooks remained active and unchanged.
- An anonymous public OCI manifest read and disposable local runtime confirmed
  Python 3.12.14 and Git 2.39.5. `/usr/bin/python3` is Python 3.11.2 in the image
  and is explicitly rejected as the candidate interpreter. The exact workflow
  bootstrap ran in a read-only, network-disabled container against disposable
  committed fixture `d920261f77aac05fa48c680047d442069f66239e`: 19/19 evaluation
  cases PASS, exit 0. This is local synthetic wiring evidence, not hosted or
  live agent-quality evidence; no credentials were mounted.
- Python's installed `trace --count --summary --missing` measured focused
  statement coverage: provenance 88%, hosted helper 84%, records 100% across
  46 passing tests after review repairs. This is not whole-repository or branch coverage. The separate
  coverage package was unavailable; no dependency was installed.
- Automatic approval rejected a proposed regex-only `--reuse-source` report.
  That change was never applied. QA only selects the registry complement;
  authenticated lookup and the protected main verdict own REUSED evidence.

- Task-only evidence commit `defae927ef70c64631984d6e0f60f16d0f7ef7b7`, checked
  tree `7804e8df8f038932233f0906b531b9924b5083b8`: documentation quick 6/6
  and exact-index staged 6/6 PASS on this Task path; cached whitespace and
  actual-message pinned Commitizen PASS. The commit succeeded through unchanged
  active hooks. This later evidence snapshot is separate from the code checks;
  no full QA was repeated.

### Independent review and repair

- Independent code review of the candidate requested two availability fixes:
  closed fork PRs were absent from open-only discovery, and a rejected older run
  prevented considering a later valid candidate. Both positive regression tests
  failed before repair. Historical discovery now queries the authenticated fork
  owner/branch for closed PRs and requires exact base/head/merged target, source
  repository, branch, run/attempt and original synthetic checkout parents.
  Distinct-fork and URL-sensitive branch fixtures pass; missing, ambiguous,
  changed-identity and unmerged candidates reject. A candidate-specific semantic
  rejection continues to later runs; zero or multiple authenticated matches
  still fall back. Provider transport errors fail the complete lookup closed.
- Independent static security review found no concrete CRITICAL/HIGH/MEDIUM
  exploit in the candidate. Follow-up identified a conditional checkout-transform
  closure gap and required protecting all `.gitattributes` paths. Three root,
  nested and deep-nested intermediate-add/revert cases produced a proof before
  the fix and reject afterward. No ordinary QA raw scan or wider permission was
  added. Skipped isolated jobs now report SKIP, with a ten-case RED/GREEN check.
- Review-fix commit `c5a9ddac38f4d4425a8325fe4dfc6f2d7bb3843f`, tree
  `367990ea7a98fa47d145975a027376df3b8a480f`, contains only seven code/test files.
  Affected proof/hosted/workflow/CI-contract suites passed 136 tests in 18.624
  seconds; the proof-only coverage run passed 46 in 4.195 seconds. Changed-input
  quick passed 12 gates on eight paths, including the held Task draft. Exact
  staged passed eight gates on the seven-file code index. Pinned lint, workflow
  security, canonical CI contract, whitespace and actual-message Commitizen
  passed. No full suite was repeated. Independent scoped re-review of this fix:
  `review_task4_code` returned Spec PASS / quality Approved with no residual
  finding; `review_task4_security` returned static PASS, confirmed the
  `.gitattributes` gap closed, and found no spoof path. These are local review
  dispositions; hosted enforcement remains DEFER.
- Authenticated read-only provider observation on 2026-10-02: closed
  [PR 115](https://github.com/buenhyden/hy-home.k8s/pull/115) reports base
  `c67d7124b3d727c39270267042d2729060260bcd`, head
  `6b80bf2886c1c6e0cd27021cad49da28170007b4`, merge
  `0ed105b832d85c88b1000ad58959531d1ae23cae`; the merged Git commit's parents are
  exactly that base/head pair. This confirms one same-repository historical
  metadata shape only. It is not a fork, App proof, new CI or hosted reuse trial.

### Per-gate disposition matrix

This table describes the implemented routing contract verified by local fixtures.
It does not claim hosted execution. Every fallback and manual diagnostic executes
all 23 gates. Only one gate may be reused after activation and full authentication.

| Gate | PR owner | Main with valid candidate | Main fallback/manual | Hosted observation |
| --- | --- | --- | --- | --- |
| `affected-surface-contract` | QA complement | EXECUTE | EXECUTE | DEFER |
| `archive-cutover` | QA complement | EXECUTE | EXECUTE | DEFER |
| `agent-governance` | QA complement | EXECUTE | EXECUTE | DEFER |
| `ci-python-contract` | QA complement | EXECUTE | EXECUTE | DEFER |
| `github-actions-security` | QA complement | EXECUTE | EXECUTE | DEFER |
| `document-contract-registry` | QA complement | EXECUTE | EXECUTE | DEFER |
| `document-lifecycle` | QA complement | EXECUTE | EXECUTE | DEFER |
| `gitops-change-set` | QA complement | EXECUTE | EXECUTE | DEFER |
| `gitops-structure` | QA complement | EXECUTE | EXECUTE | DEFER |
| `infrastructure-contracts` | QA complement | EXECUTE | EXECUTE | DEFER |
| `k8s-manifests` | QA complement | EXECUTE | EXECUTE | DEFER |
| `knowledge-surface` | QA complement | EXECUTE | EXECUTE | DEFER |
| `links-and-owners` | QA complement | EXECUTE | EXECUTE | DEFER |
| `markdown-profiles` | QA complement | EXECUTE | EXECUTE | DEFER |
| `policy-gates` | QA complement | EXECUTE | EXECUTE | DEFER |
| `repository-quality` | QA complement | EXECUTE | EXECUTE | DEFER |
| `workspace-boundary` | QA complement | EXECUTE | EXECUTE | DEFER |
| `secret-handling` | QA complement | EXECUTE | EXECUTE | DEFER |
| `vault-eso-contracts` | QA complement | EXECUTE | EXECUTE | DEFER |
| `unit-tests` | QA complement | EXECUTE | EXECUTE | DEFER |
| `pre-commit` | QA complement | EXECUTE | EXECUTE | DEFER |
| `agent-evaluation-cases` | isolated job | REUSED from authenticated PR | EXECUTE | DEFER |
| `external-service-contracts` | QA complement | EXECUTE | EXECUTE | DEFER |

### Initial hosted deferral and handoff

- DEFER: no App/environment/required-check activation, provider PR/main trial,
  or source check from this new workflow has been observed. The five-job and
  skipped-step payload shape, exact checkout, immutable container bootstrap,
  merged-PR relation for each merge strategy and App author need hosted trials.
  Closed fork discovery is covered by strict local fixtures; missing or ambiguous
  provider history still falls back. No new hosted run IDs or reuse savings are claimed.
- Provider contracts consulted: [GitHub container jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/run-jobs-in-a-container),
  [exact-attempt job metadata](https://docs.github.com/en/rest/actions/workflow-jobs?apiVersion=2022-11-28),
  [workflow-run identity](https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28),
  and [official Python image metadata](https://github.com/docker-library/repo-info/blob/master/repos/python/remote/3.12-bookworm.md).
  The current platform digest came from the live public manifest read, not a
  mutable image tag or stale documentation cache.
- Next owner: supervisor for Task 5 handoff and final delivery reconciliation;
  operator for activation and authenticated settings/run observations. Task 5
  can consume the full-main v2 verdict even while reuse remains disabled.
  No push, dispatch, remote setting, secret, App, tag or cluster change occurred.

### Hosted PR and main fallback supplement (2026-10-02)

- Normal [PR #121](https://github.com/buenhyden/hy-home.k8s/pull/121)
  completed disjoint isolated 1-gate and complement 22-gate QA in
  [CI run 36956836213](https://github.com/buenhyden/hy-home.k8s/actions/runs/36956836213).
  The verifier App published `qa-provenance` check `110686923231` on exact PR
  head `a8d63142c2d4b07901132a44e978afc093f6e312`. It merged as main commit
  `3fa2f14d57d7d2cd0886e8eb5c7c8f7ff71f0c2a`.
- `QA_REUSE_ENABLED=true` was set for that main integration, but the main
  source lookup rejected a valid `base...head` compare because of its transport
  guard. [Main CI run 36960567064](https://github.com/buenhyden/hy-home.k8s/actions/runs/36960567064)
  therefore executed all 23 gates and passed; verifier App
  `qa-main-verdict` check `110697612642` passed for the exact main commit.
  This is a successful fail-closed fallback, **not** a reuse observation.
- `QA_REUSE_ENABLED` was reset to `false`. [PR #123](https://github.com/buenhyden/hy-home.k8s/pull/123)
  corrected the compare transport guard and merged as
  `91ecc7757727a966f35cc36aa012a4266eaa9e8f`. This Task remains
  **in-progress** until a subsequent main run proves exactly one `REUSED`
  evaluator gate, 22 freshly executed gates, and a successful protected main
  App verdict on that exact SHA. Rollback remains disabling reuse so main runs
  all 23 gates.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-004](../plan.md#work-breakdown) | PR partition and full-main fallback PASS; hosted reuse pending | PR #121 CI `36956836213` ran 1+22 and App check `110686923231` passed. Main CI `36960567064` safely executed all 23 after source lookup rejection; App verdict `110697612642` passed. The compare guard was fixed by PR #123; no main `REUSED` gate is claimed yet. |
