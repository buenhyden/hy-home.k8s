---
title: "QA Evidence Reuse Implementation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-PLAN-0001"
---

# QA Evidence Reuse Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute each required QA gate once per proven-equivalent input, keep every distinct local/hosted/history check, and publish an immutable `main-<40-hex SHA>` tag after a protected successful main verdict.

**Architecture:** The existing registry remains the sole gate/argv selector and the bounded runner remains the executor. A private local evidence file can reuse exact matching local results. Hosted reuse and tag publication use a default-branch `workflow_run` verifier plus a verifier-only GitHub App whose key is available only in a `main`-restricted `qa-control` environment; a separate publisher App key is confined to `qa-tag-publish`; the protected verifier, once activated, rejects changes to every privileged workflow and its execution dependencies before merge. Full main QA and no tag remain the default until authenticated activation.

**Tech Stack:** Python 3.12 stdlib, existing JSON Schema and PyYAML, Git, GitHub Actions/API, repository validation registry, unittest.

**Spec:** [SPEC-0103](./spec.md). Requirement owner: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md).

## Global Constraints

- `scripts/validation/registry.json` alone selects gate IDs, argv, profiles, and reuse declarations; full and ci retain one required gate set.
- `scripts/qa.py` retains `quick|staged|full|ci`, isolated snapshots, and the bounded runner; failed, missing, deferred, or skipped evidence never satisfies a required gate.
- Local results never authorize hosted reuse. PR full runs on the actual hosted merge checkout; history/environment-sensitive main inputs run again unless individually proven equal.
- No global/private Git hooks, provider credentials, Kubernetes, Vault, deployment CD, or release-version workflow are changed.
- Read-only QA jobs retain `contents: read`; any `actions: read`, check-write, or `contents: write` grant belongs to a separately reviewed protected identity.
- Existing independent secret, policy, GitOps, archive, and history failure meanings stay intact. An old name or large file is not a deletion criterion.
- No `main-*` tag is created until the protected main check, publisher identity and scope, and effective creation/update/deletion rulesets are read back. The first protected tag supplies the existing ref needed for live denied-write trials before steady-state activation.

### Review Focus

- A file edited at the same path between quick and staged must rerun its gate; Task 1 adds a same-path byte-change assertion.
- A PR's tested synthetic merge commit must not be inferred from `head_sha`; Task 3 tests a mismatched merge checkout.
- A multi-commit rebase whose immediate parent looks valid must not reuse history-sensitive gates; Task 4 tests the push `before`/base anchor.
- A PR changing the proof producer or workflow must not certify its own new contract; Task 3 tests a changed control path in any PR commit.
- An existing `main-<SHA>` name pointing elsewhere must not move; Task 5 tests conflict, retry, and denied update/delete.

---

## Overview

The request owner approved the Plan on 2026-10-01. The later test-disposition
request added Task 7. Tasks 1–7 have reviewed implementation or audit evidence
in their Task records. PR #124 passed App-pinned protection; main CI run
36966489221 reused one gate and executed 22, with an independent App verdict.
Protected publisher run 36967966896 created the exact main tag, denied-write
trials left it unchanged, and its same-target retry was a no-op. Live fork
labeling and reporter UI navigation remain explicit provider DEFER in Task 2;
they are not required QA gates or blockers for the named criteria.

## Context

The baseline was `0ed105b8` on `main`/`origin/main`; this plan followed the
approved SPEC-0103 commits on `codex/qa-evidence-dedup-spec`. At that baseline,
`.github/workflows/ci.yml` ran the same `qa.py ci` gate set on PR and main,
while `.github/PULL_REQUEST_TEMPLATE.md` asked for local full. The static audit
found no active-path script safe to delete without transferring a unique
contract. GitHub settings read on 2026-10-01 had no separately protected
required check or tags and had four dead `.github` destinations/labels named
in the Spec. Tasks 2–5 record the later authenticated read-back and activation.

| Owner | Existing or proposed files | Responsibility |
| --- | --- | --- |
| Local QA | `scripts/qa.py`, `scripts/run-validation-lane.py`, `scripts/validate-affected-surfaces.py`, `scripts/validation/registry{,.schema}.json`, `tests/test_{qa_runner,run_validation_lane,validation_profiles}.py` | Exact input identity, gate disposition, single registry owner. |
| Delivery guidance and repository surface | `.agents/governance/{quality,git}.md`, `.agents/workflows/work-lifecycle.md`, `scripts/README.md`, `.github/{PULL_REQUEST_TEMPLATE.md,repository-surface.md,ISSUE_TEMPLATE/config.yml,dependabot.yml,labeler.yml,SECURITY.md}`, relevant `tests/test_ci_qa_workflow.py` and governance tests | Delivery owners, proved script disposition, valid GitHub routes. |
| Protected control plane | This repository's `.github/workflows/qa-verifier.yml`, `scripts/qa_provenance.py`, `tests/test_qa_provenance.py`; `.github/workflows/ci.yml` supplies ordinary QA only | Separate App-sourced PR/main verdict, bounded provider lookup, no execution of PR code. After activation, default-branch control code is protected by its App check over the entire privileged execution closure; an external control repository is a fallback only if authenticated tests cannot prove that chain of trust. |
| Hosted decision and tag | `scripts/qa.py`, `scripts/run-validation-lane.py`, registry/schema, `.github/workflows/ci.yml`, `scripts/qa_provenance.py` and `scripts/publish_main_tag.py` | Per-gate full-or-reused verdict and post-verdict tag publication. |
| Task evidence | `docs/03.specs/0103-qa-evidence-reuse/tasks/tsk-0001-*.md` through `tsk-0007-*.md` | Actual commands, reviewer, remote settings, run/attempt, decisions, rollback. |

Do not add a permanent duplicate script inventory. Task 2's caller table is the evidence of the one-time disposition audit. Separate verifier/publisher App installations, their `main`-only environments and secrets, App-sourced required check, trusted control-code baseline, and tag rulesets are separate operator actions requiring review; Plan approval alone does not claim they happened.

## Goals & In-Scope

Deliver exact-input local reuse, a single gate registry, corrected delivery guidance and GitHub routes, protected hosted proof, safe per-gate main reuse, and immutable validated main tags. Preserve every distinct validation meaning and record the one-time active-script disposition in Task 0002.

## Non-Goals & Out-of-Scope

No deployment CD, live cluster or Vault mutation, version-release tagging, global hook change, replacement QA registry, or speculative script deletion. App installation, repository protection, environment secrets, and tag rulesets are operator-owned activation steps; static code does not prove them.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Local exact-input reuse and registry contract | Approved Plan | VAL-QER-001–002 | Focused RED/GREEN and one-run/same-path-change counts; full/ci parity. |
| WP-002 | Delivery policy, script disposition, `.github` route repair | Approved Plan | VAL-QER-003/009/011 | Caller/unique-contract table, template/route negatives, independent semantic review. |
| WP-007 | Active invoked/discovered test disposition | WP-002; later user scope addition | VAL-QER-012 | Test caller/assertion table, reviewed retirements, discovery and failure-meaning parity. |
| WP-003 | Protected PR verifier and App check | WP-001; operator verifier App/environment | Reviewed inert control code; App/environment bootstrap | Protected source read-back, hostile PR/control-change tests, bounded proof record. |
| WP-004 | Main per-gate reuse and test-group classification | WP-003 | Protected App check observed; VAL-QER-005–008 | Merge/rebase/changed-ref fixtures, full fallback, observed PR/main verdict. |
| WP-005 | Protected immutable main tag publisher | WP-004; protected main verdict; operator rulesets | App-pinned PR control, publisher identity/scope, and ruleset read-back | Bounded first publication, denied update/delete on its unchanged ref, same-target retry, and hosted exact-SHA observation before steady-state activation. |
| WP-006 | Integration, security review, and handoff | WP-001–005 and WP-007 or explicit inactive DEFER for hosted criteria | Changed-file and criterion matrix | Criterion matrix, final QA, independent review, activated vs inactive states recorded. |

### Task 1: Local evidence identity and single registry owner

**Files:** Modify `scripts/validation/registry.schema.json`, `scripts/validation/registry.json`, `scripts/validate-affected-surfaces.py`, `scripts/qa.py`, `scripts/run-validation-lane.py`; test `tests/test_validation_profiles.py`, `tests/test_qa_runner.py`, `tests/test_run_validation_lane.py`.

**Interfaces:** `gate_input_identity(snapshot: Path, gate: Mapping[str, Any], *, lane: str, paths: Sequence[str], base_ref: str, environment: Mapping[str, str]) -> str` returns a SHA-256 identity over versioned, length-bounded canonical fields. `LocalEvidenceStore` in `scripts/qa.py` reads/writes one mode-0600 atomic file under the Git common directory; its `matching_pass(gate_id, identity) -> bool` and `record_pass(gate_id, identity) -> None` never store credentials or stdout. `run_selected(..., reuse_candidates: Mapping[str, dict[str, str]] | None = None)` accepts gate ID → {identity, source} after local or hosted field validation and emits `REUSED` with source identity; `validator_argv` remains the sole argv construction path. Missing/unknown reuse metadata means execute. Exact cross-mode reuse is opt-in per audited gate, never inferred from name alone.

- [x] Add RED fixtures for unchanged quick repeat and one proven quick→staged case, same-path byte/mode edit, untracked/new path, formatter rewrite, changed base/config/tool/argv, and a forged or unreadable local record. Assert one execution only for exact matches and ordinary execution otherwise.
- [x] Run `python3 -m unittest tests.test_qa_runner tests.test_run_validation_lane tests.test_validation_profiles`; the new reuse assertions must fail before implementation.
- [x] Implement the identity and private evidence store using existing snapshot/Git/bounded-file helpers. Extend registry schema with a conservative optional reuse declaration and validate it in `validate_contract`; do not add a second gate array. Store only successful completed subprocess results after snapshot integrity passes.
- [x] Run the focused command again and `python3 scripts/qa.py quick`; new cases and full/ci parity must pass. Inspect `git diff --check`; get independent code/security review of the input boundary.
- [x] Commit the reviewed unit with `git commit -m "feat: reuse exact local QA evidence"`; record actual snapshot and result in Task 0001.

### Task 2: Assign delivery owners and repair active surfaces

**Files:** Modify `.agents/governance/quality.md`, `.agents/governance/git.md`, `.agents/workflows/work-lifecycle.md`, `scripts/README.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/repository-surface.md`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/dependabot.yml`, `.github/labeler.yml`, `.github/SECURITY.md`; test `tests/test_ci_qa_workflow.py` and existing policy/projection tests. Touch a script or workflow only if this task's test proves a contract transfer.

**Interfaces:** No new runtime API. The quality policy owns editing/commit/push/PR/main/local-only lanes; PR template and repository hub link to it. Task 0002 owns a table of every active CI/QA script with caller, unique failure meaning, tests, and keep/consolidate/retire decision.

- [x] Add RED route/contract cases: PR template does not demand local full before PR; issue contact does not point to disabled Discussions; Dependabot targets existing `github_actions`; cluster label maps to existing `area/gitops`; SECURITY.md links the enabled private reporting UI. Include a negative manifest missing-directory/nonempty case before considering the `k8s-manifests` overlap.
- [x] Run `python3 -m unittest tests.test_ci_qa_workflow tests.test_validation_profiles tests.test_validation_tooling_ownership`; record new RED cases. Trace `.github` events, hooks, QA profiles, registry argv, direct imports, and docs consumers in Task 0002.
- [x] Make the smallest guidance/config fixes. Keep all currently unique script checks and pre-push hook chaining. Do not add `pull_request_target`, label-creation permission, or a second full QA trigger. Delete/consolidate a script only if Task 0002 proves consumer transfer and the negative fixture passes.
- [x] Run the focused command, relevant policy tests, `python3 scripts/qa.py quick`, and independent read-only semantic/security review. Record authenticated destinations/settings separately from static YAML evidence.
- [x] Commit the reviewed unit with `git commit -m "ci: align QA guidance and GitHub routes"` and update Task 0002.

### Task 7: Audit and retire obsolete or redundant active tests

**Files:** Inspect every `tests/test_*.py` module discovered by the registry's `unit-tests` argv and tests invoked by other CI/QA/validation gates. Modify only proved obsolete, redundant, or conflicting test modules, their direct callers, and `.agents/governance/quality.md` if its test-retirement rule needs clarification; record decisions in `tasks/tsk-0007-test-disposition.md`. Do not add a permanent inventory script.

**Interfaces:** Task 0007 owns a one-time table of active test module/caller, distinct assertion or failure meaning, one-off/legacy/deprecated/duplicate/conflict/size candidate, and keep/consolidate/retire disposition. Discovery and failure meaning of retained tests remain complete. A candidate without a proved equivalent retained assertion is kept; file age, name, or size alone is not grounds for deletion. The `unit-tests` aggregate stays intact unless Task 4 separately proves a disjoint partition.

- [x] Record the registry's exact test argv and baseline discovered module/case counts. Trace direct standalone test invocations, imports, fixtures, and each discovered module's unique assertion families; identify exact and semantic duplicates, stale targets, contradictory expectations, and excessive helper/test repetition.
- [x] For each proposed deletion or consolidation, identify a retained negative check for still-required behavior or prove the caller and requirement have no current contract; record before/after discovery and failure evidence. Preserve security, GitOps, archive, history, and provider-boundary checks. Remove proven obsolete or redundant tests and their dead fixtures/callers; if none qualify, record the concrete keep decisions rather than deleting a test to meet a quota.
- [x] Run focused tests for each changed contract, registry/discovery tests, `python3 scripts/qa.py quick`, and exact-index staged QA when required. Run the full unit-test aggregate once on final changed inputs, not once per candidate. Get an independent read-only semantic review of the disposition table and diff.
- [x] Commit with `git commit -m "test: retire proven redundant QA tests"` if tests change, or `git commit -m "docs: record active QA test disposition"` if the audit proves no safe retirement; update Task 0007 with exact commands, counts, reviewer, and deferred hosted observations.

### Task 3: Separate protected PR proof from PR-controlled QA

**Files:** Create `.github/workflows/qa-verifier.yml`, `scripts/qa_provenance.py`, `tests/test_qa_provenance.py`; modify `.github/workflows/ci.yml` only to expose required read-only run metadata if needed; add `tests/test_ci_qa_workflow.py` cases. No PR checkout or QA artifact supplies verifier code or credentials.

**Interfaces:** A default-branch `workflow_run` job mints a narrowed installation token for the verifier-only App and emits a required `qa-provenance` check from that App ID. Its bounded version-1 record has repository, PR/base/head, actual QA checkout commit/tree, workflow revision, run/attempt/job IDs, registry/tool identity, and complete gate dispositions. `verify_pr(event: Mapping[str, Any], github: GitHubReader) -> Proof | Reject` accepts provider-authenticated run/job/step data plus durable Git objects; it never executes fetched content. The version-1 record is a bounded (16 KiB maximum) JSON object in the App-authored `qa-provenance` check output, retained for at most 30 days as a reuse source; missing, older, or inaccessible checks mean full execution. At PR time the verifier binds the tested merge checkout to the trusted workflow's exact checkout ref and durable Git object, not the Actions API `head_sha`. The verifier workflow runs only on `workflow_run` completion of `CI` and never executes PR code or uses its cache. Its `qa-control` environment permits only `refs/heads/main`; PR merge refs, feature branches and tags are denied. The verifier App installation has metadata/read, actions/read, contents/read, pull-requests/read, checks/write and no contents/write permission at all, so this job cannot mint a tag-writing token. The publisher key is held in the separate `qa-tag-publish` environment and unavailable to this job.

- [x] Add RED cases for missing/failed/cancelled source, mismatched run attempt/job, PR head vs synthetic merge checkout, malformed/oversized record, passing test that mutates the QA checkout, duplicate check name from PR, and any addition, change, or deletion in `.github/workflows/**`, verifier/publisher scripts, QA runner/registry/lock, or transitive verifier dependencies in any PR commit. Assert a direct PR-ref job cannot access the verifier App environment and the verifier App installation cannot request contents/write. A PR-triggered default-branch verifier may access it only after authenticating source repository, event, workflow ID, run/attempt, and head/base/checkout before token use; on mismatch it emits no App PASS or reusable proof.
- [x] Run `python3 -m unittest tests.test_qa_provenance tests.test_ci_qa_workflow`; record RED failures.
- [x] Implement the smallest App-backed reader/proof writer and isolated `workflow_run` workflow. Pin dependencies/actions, bound API pages/bytes/time, allowlist and authenticate source repository/event/workflow/run/attempt before using the App key, and compare the privileged execution closure against the reviewed default-branch baseline before issuing PASS. Protect the App key in `qa-control`, allow only main, and use expected App ID in branch protection; a PR-authored check of the same name cannot satisfy it. A control-code change requires a separate operator-reviewed bootstrap/transition and full main QA.
- [x] Run focused tests and security review. Operator installs the verifier App, configures its main-only environment and exact required check, and reads back verifier App ID, installation permission ceiling, environment branch policy, effective branch settings, and a hostile-PR/control-change trial. Bootstrap in order: merge the inert control code through ordinary full QA, install the verifier App and main-only environment, observe one App-authored PR check, pin that App ID as a required source, run hostile-PR/control-change trials, then enable reuse through an operator-owned `QA_REUSE_ENABLED` repository variable. Until all pass, keep hosted reuse disabled and main full.
- [x] Commit the reviewed local unit; record commit, App/settings and run/attempt in Task 0003. Do not call static tests an activated check.

### Task 4: Reuse individually proven PR gates on main

**Files:** Modify `scripts/qa.py`, `scripts/run-validation-lane.py`, registry/schema, `.github/workflows/ci.yml`; test `tests/test_qa_runner.py`, `tests/test_run_validation_lane.py`, `tests/test_ci_qa_workflow.py`, `tests/test_validation_profiles.py`, and a focused history fixture. `scripts/qa_provenance.py` checks the main verdict in the isolated verifier workflow.

**Interfaces:** `reuse_candidates` passed to `run_selected` contains candidate gate ID → exact identity and source run/attempt/job from a read-only authenticated lookup; `run_selected` executes every other required gate. After the QA job, the isolated App verifier independently authenticates every reuse claim and emits `qa-main-verdict` over the complete set. A candidate skip with no verifiable source makes the App verdict fail; before activation the main job executes full QA. `unit-tests` remains one aggregate gate until a complete, independently runnable and equivalent partition is proved; no partial test-group skip is silently called full coverage.

- [x] Add RED merge, squash, rebase, multi-commit push, advanced main, changed named ref, tool/lock change, expired proof, and modified control-path fixtures. Assert each affected gate executes, the unaffected proven gate may be `REUSED`, and any execution failure makes `ci-summary` fail.
- [x] Run the focused test modules; record RED. Audit unit discovery for history/checkout readers and either prove a disjoint partition with exact discovery parity or keep the aggregate running on main.
- [x] Add the fail-closed lookup and gate-wise execution route. Main `ci.yml` remains a full QA fallback until the protected check is observed; `workflow_dispatch` always executes the selected full diagnostic path. Never reuse a REUSED main result recursively.
- [x] Run focused GREEN, `python3 scripts/qa.py quick`, then observed PR and main runs with exact SHA/run/attempt. Verify final required gate count and independent App verdict; record separately if operator activation is pending.
- [x] Commit with `git commit -m "ci: verify and reuse matching main QA gates"`; record the per-gate matrix and rollback in Task 0004.

### Task 5: Publish only protected successful main tips

**Files:** Create `scripts/publish_main_tag.py` and `tests/test_publish_main_tag.py`; modify `.github/workflows/qa-verifier.yml`, `.github/repository-surface.md`, and `tests/test_ci_qa_workflow.py` for the protected writer route.

**Interfaces:** `publish_main_tag(repository: str, ref: str, after_sha: str, verdict: MainVerdict, github: GitHubWriter) -> Publication` in `scripts/publish_main_tag.py` accepts only `refs/heads/main`, a 40-hex SHA equal to the authenticated push `after`, and the protected verdict for that SHA. It creates lightweight `refs/tags/main-<sha>` without force. Existing same-target tag returns `noop`; different target returns failure. The publisher job uses a distinct publisher-only App installed with contents/read-write and metadata/read, never the verifier App. Its key lives only in the main-only `qa-tag-publish` environment. The job-level condition requires GitHub's `workflow_run.event == 'push'` and `workflow_run.head_branch == 'main'` before environment access; the script independently authenticates repository, workflow, event, run/attempt and exact protected main verdict before using the key. PR-originated verifier jobs and PR QA cannot enter this job or mint a publisher token.

- [x] Add RED tests for PR/feature/tag/manual events attempting to enter the publisher environment, failed or wrong-SHA verdict, multi-commit push, same-target retry, collision, concurrent creation, and failed API write. Assert no tag creation except one successful main tip.
- [x] Run `python3 -m unittest tests.test_publish_main_tag`; record RED.
- [x] Implement publisher and post-verdict job in `.github/workflows/qa-verifier.yml`. Operator installs the separate publisher App, verifies its key is unavailable to PR-originated verifier jobs, and enforces two `main-*` tag rulesets: creation restricted to publisher App, and update/delete blocked for that App. A negative test must show the verifier App cannot mint contents/write even when requested. Keep the writer off behind an operator-owned `QA_TAG_ENABLED` variable in `qa-tag-publish` until the App-pinned PR control, protected main verdict, publisher identity/scope, and both effective rulesets have been read back.
- [x] Run GREEN and security review. With main updates held, allow one bounded first publication for a successful protected main push; record the exact tag, target, publisher identity, and independent verdict ID. Turn the writer off pending a normal writer's denied update and deletion against that tag; read the ref back unchanged after each attempt, then allow one bounded same-target publisher retry and prove it is a no-op. An unexpected successful write is `FAIL`: disable publication and investigate. If deletion succeeded, restore the exact original ref through the protected publisher while main remains held; if an update succeeded, preserve evidence for operator recovery. Do not relax rules or force-update. Enable steady-state publication only after both denials and retry pass. Confirm `main-*` does not match `v*.*.*`, and tag push starts no QA.
- [x] Commit with `git commit -m "ci: publish immutable validated main tags"`; record remote activation and rollback in Task 0005. Rollback disables publication without deleting or moving tags.

### Task 6: Integrate, verify, and hand off

**Files:** Package-local Task records, Spec/Plan lifecycle metadata, affected current policy links and navigation only; implementation files return to their task owner if review finds a defect.

**Interfaces:** Task 0006 maps VAL-QER-001–012 to actual local, hosted, settings, and denied-operation evidence or explicit `DEFER` with owner/retry trigger. No mock is presented as remote enforcement.

- [x] Review the full diff against SPEC-0103, registry gate count, all active script and test dispositions (including tests added by Tasks 3–5 after Task 7), `.github` workflow matrix, permissions, security paths, and a fresh independent read-only semantic and security review.
- [x] Run affected focused suites on final bytes, `python3 scripts/qa.py quick`, exact-index `python3 scripts/qa.py staged` for each logical commit, `git diff --check`, and one `python3 scripts/qa.py full` only for a local-only handoff or a changed full-input snapshot requiring it. Do not repeat already proven same-input full/pre-commit/unit work.
- [x] Record PR hosted `ci-summary`, protected App PR/main checks, tag/ruleset read-back and publication result if activated. If the protected Apps/environments or operator settings are absent, record VAL-QER-004/005/008/010 as `DEFER`, retain full main QA/no tag, and do not mark the Spec completed.

The Plan completion boundary is the reviewed implementation and acceptance
evidence above. Deliver this document change with
`docs: record QA evidence reuse verification`, then use the already authorized
Git finish route for push, PR, merge, `main`/`origin/main` synchronization, and
development-branch cleanup. Report those post-Plan actions in the final handoff;
they cannot be checked as completed inside the pre-merge Plan commit.

## Verification Plan

Focused commands are named in the owning tasks; RED precedes GREEN for changed logic. `python3 scripts/qa.py quick` and `staged` prove different snapshots. `python3 scripts/qa.py full` is not a substitute for PR hosted CI, and a local workflow parser does not prove GitHub enforcement. The hosted trial must identify repository, SHA, event, workflow revision, run, attempt, job, actual checkout, gate result, protected App ID, and final tag disposition. Existing security scanners, manifest presence, hooks, and independent semantic review remain separate evidence.

## Risks & Mitigations

The principal risk is a PR-controlled workflow forging green evidence. verifier-App-ID-pinned required checks, separate main-only App-key environments, and control-closure change rejection must be proved with a hostile PR before reuse. Missing settings, source proof, or ruleset read-back leaves main full and tags off. A delayed or failed `workflow_run` leaves the required App check pending/failing, never green.

Rollback order: disable protected reuse and tag publication first; main continues full QA. Revert main reuse routing, then local cache/schema if needed; revert policy/routes only with their consumer tests. Do not rewrite Git history or move/delete published `main-*` tags. Removing a required App check requires an operator-reviewed replacement or restored full-path protection, never a PR-authored summary alone.

## Completion Criteria

A work package is complete only with its Task's named evidence. SPEC-0103 reaches `completed` only when all criteria, including protected-host activation and tag observation, pass; otherwise record the actual partial state without claiming remote success.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-QER-001](spec.md#success-criteria--verification-plan) | WP-001 | [TSK-0001](tasks/tsk-0001-local-evidence.md) |
| [VAL-QER-002](spec.md#success-criteria--verification-plan) | WP-001 | [TSK-0001](tasks/tsk-0001-local-evidence.md) |
| [VAL-QER-003](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0002](tasks/tsk-0002-delivery-and-github.md) |
| [VAL-QER-004](spec.md#success-criteria--verification-plan) | WP-003 | [TSK-0003](tasks/tsk-0003-protected-proof.md) |
| [VAL-QER-005](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0004](tasks/tsk-0004-main-reuse.md) |
| [VAL-QER-006](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0004](tasks/tsk-0004-main-reuse.md) |
| [VAL-QER-007](spec.md#success-criteria--verification-plan) | WP-003, WP-004 | [TSK-0003](tasks/tsk-0003-protected-proof.md), [TSK-0004](tasks/tsk-0004-main-reuse.md) |
| [VAL-QER-008](spec.md#success-criteria--verification-plan) | WP-003 | [TSK-0003](tasks/tsk-0003-protected-proof.md) |
| [VAL-QER-009](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0002](tasks/tsk-0002-delivery-and-github.md) |
| [VAL-QER-010](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0005](tasks/tsk-0005-main-tags.md) |
| [VAL-QER-011](spec.md#success-criteria--verification-plan) | WP-002, WP-006 | [TSK-0002](tasks/tsk-0002-delivery-and-github.md), [TSK-0006](tasks/tsk-0006-integration.md) |
| [VAL-QER-012](spec.md#success-criteria--verification-plan) | WP-007, WP-006 | [TSK-0007](tasks/tsk-0007-test-disposition.md), [TSK-0006](tasks/tsk-0006-integration.md) |
