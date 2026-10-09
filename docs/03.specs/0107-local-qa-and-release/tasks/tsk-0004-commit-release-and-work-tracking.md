---
title: "Commit, Release and Work Tracking Follow-up"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107-TSK-0004"
parent_ids: ["SPEC-0107-PLAN-0001"]
---

# Task: Commit, Release and Work Tracking Follow-up

## Overview

This Task owns P06 execution for [WORK-004](../plan.md#work-breakdown) and
[VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan). Completed
[Tasks 0001–0003](../spec.md#overview) retain their original results. This
new Task will record actual commit grammar, hook, release and Issue/Project
consumer repairs and one bounded local criterion decision.

## Inputs

- Intake on 2026-10-09: clean local `main` at
  `45c2d800e6a89509bd7a4473c3382ca7ef44aa63`, with isolated branch
  `codex/p06-git-release` and worktree `.worktrees/p06-git-release` created
  from that commit. No audit SHA reset or previous Task reopening occurred.
- The three-document intake was admitted on staged tree
  `acee0deac09dcc9beb378b5e836c3f14de1c5b54` by six selected local
  gates, then normally committed as
  `8e15711bf85e55e59b680185ea723715d261fef2`. Ignored checkout-root
  `_workspace/p06-git-release/intake-index-qa.log` has SHA-256
  `db3a8886b827b8801fb5a3ba0fe81e33a5a8e6f2aac7b6ce3d73260914ab96dc`.
  The actual candidate message SHA-256
  `612cc5fd8a25eac41eb7cb682704832d8435fffa47da9096bc03c6f7c2c0bd3e`
  passed pinned Commitizen as recorded in
  `_workspace/p06-git-release/intake-message-check.log`, SHA-256
  `a5b63bcd3a30352d4fdcf55092a6cec1dfed4d6141ef853ed7bfbd064f4a1a6f`.
  This admits the intake documents, not P06 implementation or the planned
  Task evidence checks below.
- The draft-to-ready transition passed six selected exact-index gates on tree
  `9ced91e39b59ede07d707bf13357b6687e838863` and was normally committed
  as `cd6de604488c7d6da3d34284921047670c32b0b3`.
  `_workspace/p06-git-release/ready-index-qa.log` has SHA-256
  `90bdf831ee70e9c868f8e1189adb2d8795cbcacfa610ec5cbf79bcc6f330c136`;
  actual message SHA-256
  `b5b1879ff0108bc88f6e865a02a0126b2a590efdf4a63476e829f9bc68b9d4f3`
  passed pinned Commitizen. This proves the state transition input, not the
  P06 implementation checks.
- The current [Spec](../spec.md), [Plan](../plan.md),
  [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [ADR-0048](../../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md),
  [Git policy](../../../../.agents/governance/git.md),
  [commit-message prompt](../../../../.agents/prompts/commit-message.md),
  [release Runbook](../../../05.operations/runbooks/0012-main-release-preparation-runbook.md),
  and [hosted surface](../../../../.github/repository-surface.md) are the
  current owners to compare with their code and direct consumers.
- The user's P06 instruction authorizes local investigation, bounded policy
  and consumer repair, selected local validation, normal logical commits,
  local main integration and owned branch/worktree cleanup. It does not
  authorize tag or Release publication, remote Issue/Project mutation,
  workflow dispatch, server settings, credentials, deployment or live action.
- The same `WGOV-CORE / 3.0.0-draft.3` common review candidate has proposed
  owner `buenhyden`, proposed source
  `Project-Template/.agents/governance/shared-standard.md` and inspected
  content digest
  `sha256:3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`.
  C02/C05/C07/C10 are comparison inputs. Source revision and approval
  reference remain absent; no final common edition, local adoption or joint
  adoption is claimed.
- Read-only remote input at this intake is recorded in ignored checkout-root
  `_workspace/p06-git-release/server-readback.json`, SHA-256
  `fa0fc6e1aa87d9c34e6b67f2066bac7d3d3488b4e10e6b1f1a38fd91f54bd0b2`.
  The current main branch requires `ci-summary` and `style-pr` from App 15368;
  applied branch rulesets are empty and two inherited rulesets cover only
  historical `main-*` tags. Release and Issue API lists were empty, while
  nine local historical tags exist. A main-push check run on a different input
  had `ci-summary` success and `style-pr` skipped. Classic Project returned
  404 and Project v2 read failed with `INSUFFICIENT_SCOPES` (`read:project`);
  these results do not establish that no Project exists. The immutable-Release
  setting and any P06 PR-style or publication outcome remain unobserved.
- Ignored checkout-root `_workspace/p06-git-release/common-adapter-comparison.json`,
  SHA-256
  `8374cf30d10aea971b1213f52e0c70e80dfd60f9243e74f84785bc89df34b75a`,
  compares current Commitizen configuration in Project-Template at
  `52f06b238c75082adc4b0d123881c5d14c025239`, hy-home.docker at
  `38b8fe47587e509750f81707eadec315cbfe53db` and this repository at
  `45c2d800e6a89509bd7a4473c3382ca7ef44aa63`. The static syntax results
  differ for Unicode, scope/case and breaking markers. This was a three-repository
  comparison; it did not execute any native hook or establish adoption.
- A subsequent four-repository read-only comparison is preserved in
  `_workspace/p06-git-release/common-adapter-comparison-four.json`, SHA-256
  `e026917388f855a1d6942b607669a622f590faa0e9022e312bb7686e4744ecd3`.
  It adds blog-data remote `dev` at
  `8c4d62a4d896ec522070e376040cb1e7e9e8ee30`; its
  `site/web/commitlint.config.ts` delegates to
  `scripts/lib/git/commit-message-contract.mjs`. The raw access receipt is
  `_workspace/p06-git-release/common-source-access.json`, SHA-256
  `d7ea42ceff566b9f8e55d10c119260bf57c1157f465f964923648c0d46291368`.
  This static comparison also found the proposed common-standard path absent
  in the inspected Project-Template checkouts and remote refs. The historical
  draft digest above is not a verified current source revision or approval;
  syntax differences remain, and four-repository native or joint adoption is
  unproven.
- Effective local hook topology needs actual-file and tool confirmation:
  local `core.hooksPath` points to `scripts/githooks`, user-global configuration
  names an external hooks directory, common workspace hook files were absent,
  and `commit.template` was unset on the observed input. A source file alone
  cannot prove an installed or executed hook.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | Map and repair only proven commit grammar, hook, release and work-tracking consumer differences; validate the local input and hand off external lanes | platform | frontmatter | NOT_RUN | EVD-P06-001 through EVD-P06-004 remain planned checks; source and document repair is in progress, without final WORK admission |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P06-001 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Commit grammar, prompt and actual hook boundary | Current `.cz.toml`, `.gitmessage`, prompt builder, hook path and generated-message consumers at P06 source revision; named authored/generated positive, refusal and Unicode/breaking/footer cases | NOT_RUN | Pending exact source, command and result in this Task | yes | none |
| EVD-P06-002 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Release preview, write and publication boundary | Current release CLI, Runbook, changelog, historical tags and synthetic local preview/write/refusal inputs; actual tag or Release needs separate authorization | NOT_RUN | Pending exact source, command and result in this Task | yes | none |
| EVD-P06-003 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Current Issue forms, hosted surface, Spec/Task IDs and read-only remote observations; direct link and short-summary consumers | NOT_RUN | Pending source/consumer review and result in this Task; Project v2 scope remains unavailable to the remote owner | yes | none |
| EVD-P06-004 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Final local exact-index, message and independent review | The final changed index, selected named regressions, actual UTF-8 candidate message and reviewers once implementation bytes exist | NOT_RUN | Pending exact input, command, results, commit and later local integration in this Task and Git | yes | none |
| EVD-P06-005 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Commit grammar, prompt and actual hook boundary | Before repair, selected commit-contract tests: 5 tests, 7 failures, including false prose breaking classification and carriage-return acceptance. The historical-punctuation test failed its new bang-marker assertion; its existing punctuation assertion passed | FAIL | `_workspace/p06-git-release/tracked-commit-red.log`, SHA-256 `0d88b94de49774e51ec2a4d7f5ad78406ac188559a1c64a8e8b4adc86d3d0eb2` | yes | none |
| EVD-P06-006 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Release preview, write and publication boundary | Before repair, `validation-venv/bin/python -B -m unittest tests.test_release.ReleaseCliTest.test_release_view_requires_exact_notes_and_prerelease_in_both_phases tests.test_release.ReleaseCliTest.test_publish_preview_reads_exact_main_commit_after_worktree_race tests.test_release.ReleaseCliTest.test_draft_asset_digest_mismatch_blocks_publication -q`: three named local tests, one changelog-source failure and three subtest errors for absent `notes` argument | FAIL | `_workspace/p06-git-release/tracked-release-red.log`, SHA-256 `402966984f6e18babce760bf16e3a7c0dcac03469755b13c70c8fc8f50c8031a` | yes | none |
| EVD-P06-007 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Before consumer repair, `validation-venv/bin/python -B -m unittest tests.test_validate_affected_surfaces.AffectedSurfaceFixtureTests.test_release_tooling_keeps_its_direct_contract_checks tests.test_validate_affected_surfaces.AffectedSurfaceFixtureTests.test_surface_cases -q`: two named tests, six failures from missing direct release-tooling validation ownership | FAIL | `_workspace/p06-git-release/tracked-route-red.log`, SHA-256 `3efb56fc6dd2cfc6b7633e80d3e9f0c7741adc1b1ffb364e78d99e110d2da727` | yes | none |
| EVD-P06-008 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Commit grammar, prompt and actual hook boundary | Tracked candidate `.cz.toml` SHA-256 `80d7ab0e23a33574de84606e33af137f38ebc208c43bc37fcbb5b619fa147137`: `python -B -m unittest tests.test_commit_contracts -q`, 5 tests and shell rc 0; native Commitizen 4.15.1 generated and accepted six Unicode/bang/footer cases on that source. This is local parser/generator proof, not installed-hook delivery | PASS | `_workspace/p06-git-release/qe-validation-final.json`, SHA-256 `428250bd007e1cecb36b2b8fb3162aff3aa1d81ba0f5cac46c5bae553a89bf81`; test log SHA-256 `cb92f3312c9679b1c124f581c247a2d49a69a7d614b271c19005afd814c7494f`; `_workspace/p06-git-release/native-commit-generator-final.json`, SHA-256 `d8da9e0ac254ff00fc3d331f44306d29d15949ef7f8bf9e56bb5bab8385a53bb` | yes | EVD-P06-005 |
| EVD-P06-009 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Earlier tracked candidate registry and fixture: `python -B -m unittest tests.test_validate_affected_surfaces -q`, 19 tests and shell rc 0; only static local release-tooling routes on that input, not later selector refinements, remote Project access or Issue sync | PASS | `_workspace/p06-git-release/qe-validation-final.json`; test log SHA-256 `1922fba7c5ddc9fdf7ee643064bb7dfaead4754ee07f47eaae9485d1a0b52416` | yes | EVD-P06-007 |
| EVD-P06-010 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Release preview, write and publication boundary | Candidate `python -B -m unittest tests.test_release -q` logged 19 tests OK, but its outer shell return code was not captured; no complete process PASS or final-index claim. The separate native cliff named test ran 1 test with rc 0 | DEFER | `_workspace/p06-git-release/qe-validation-final.json`; release log SHA-256 `0b8a5d89fe072edd457350862f81c7ada6c68727dd71efd73fd9a59f7a15e163`; cliff log SHA-256 `79bc95b6e39666b665524d5edadc06b19a8364e51cddc99e95573512b6246d0d` | yes | none |
| EVD-P06-011 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Release preview, write and publication boundary | Same final source hashes as EVD-P06-010; `python -B -m unittest tests.test_release -q` explicitly captured process exit 0 and 19 tests OK. This covers synthetic local CLI/refusal inputs; actual tag or Release publication was not run | PASS | `_workspace/p06-git-release/release-command-admission.json`, SHA-256 `fff25063b9a179a73f1b7aed2ab82c6a05b8020a21f20b3eea004b0ddff5525d`; `_workspace/p06-git-release/release-command-admission.log`, SHA-256 `959b1e53a4d8658c1634c782f15cc005d7a8149152ba91a02338d8ecb60bd476` | yes | EVD-P06-002, EVD-P06-006, EVD-P06-010 |
| EVD-P06-012 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Read-only consumer audit: current `.github/ISSUE_TEMPLATE/bug_report.yml` has an optional direct Spec link; it and `feature_request.yml` distinguish request/priority triage from Spec acceptance and Task execution. `.github/repository-surface.md` and `.agents/governance/sdlc.md` give Project only a display role. No full-copy or two-way status consumer was identified in this scoped read. Project v2 remote access returned `INSUFFICIENT_SCOPES`, so its actual state is unverified | PASS | Current source paths named in Input, `cd6de604488c7d6da3d34284921047670c32b0b3`; `_workspace/p06-git-release/server-readback.json`, SHA-256 `fa0fc6e1aa87d9c34e6b67f2066bac7d3d3488b4e10e6b1f1a38fd91f54bd0b2` | yes | EVD-P06-003 |
| EVD-P06-013 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Commit grammar, prompt and actual hook boundary | Read-only hook and tool audit: effective local `core.hooksPath` is `scripts/githooks`; its commit-msg/pre-commit/pre-push files and chain helper are executable; user-global pre-commit/pre-push exist, common Git hooks absent and `commit.template` unset. Intake and ready normal commits used active hooks, while no installed global commit-msg or P06 source-commit result is claimed | PASS | `_workspace/p06-git-release/hook-and-tool-state.json`, SHA-256 `885e4c26eefcc15a06af3b51408befd560610f0aa7763684d9cc910a3ad74741`; intake and ready commit IDs above | yes | none |
| EVD-P06-014 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Final local exact-index, message and independent review | Two independent read-only reviews passed the earlier frozen 12-file source/consumer diff SHA-256 `f78ea693b714f148db880aa20b58ead5a15865daa3e2e0bdfbe692dc5801fb48`. Code review found no material regression; security review confirmed two initial MEDIUM fixes. Later selector refinements require their own review; neither reviewer ran final index QA. `SEC-P01-001` and future `v*` protection `SEC-P06-001` HIGH remain with their external owners | PASS | `_workspace/p06-git-release/source-review-results.json`, SHA-256 `c63643b5eaa7f8470d4a53d7857098bc992ec3a1dc61ec47a9c27c5e82e855c4` | yes | none |
| EVD-P06-015 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Late exact-route selection check on the two metadata files before repair: two named methods, four expected failures because release-only consumers selected generic Archive/K8S leaves | FAIL | `_workspace/p06-git-release/route-owner-red.log`, SHA-256 `13b4b657d555ef07376d649105cdbe71514218ee75c38d774482cc1c865fec94` | yes | none |
| EVD-P06-016 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Corrected Registry, fixture and selector tests: three named methods, process rc 0 and 3 PASS. `.agents` and Release owners retain their direct leaves while the generic Archive fallback remains for actual Archive inputs; the two release-only metadata files no longer select unrelated Archive/K8S work | PASS | `_workspace/p06-git-release/route-owner-green.log`, SHA-256 `ee0b6e5981189c0827c3cc32d823c826eac54cf9dc46efabe92b6ced8b448d3e`; `_workspace/p06-git-release/route-owner-final.json`, SHA-256 `f556bc5f68041bb71411b6c522209e22af99e0a70e70f7417a3ce26f9c605595` | yes | EVD-P06-015 |
| EVD-P06-017 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Read-only affected-surface contract on revised local source returned rc 0 over 1,301 tracked paths with no uncovered or ambiguous path; the selection prediction is 11 gates for the 13 changed paths, before actual final-index execution | PASS | `_workspace/p06-git-release/route-owner-static.log`, SHA-256 `17b4c067a00ac8ecc03df7c8108d3054095c1fe69a5cca960f0ff64303af0e5e`; `_workspace/p06-git-release/route-owner-final.json` | yes | none |
| EVD-P06-018 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Final local exact-index, message and independent review | Independent code and security rereviews passed the three-file routing correction diff SHA-256 `f149db937f828edce4fb1d9f9cb232e1f8f5cc91d0ffad62f20e2fd089668c6a`; the other nine reviewed source files were unchanged. Exact routes retain relevant contract checks and the generic fallback. These reviews did not run final staged QA or authorize remote publication; both HIGH findings remain external | PASS | `_workspace/p06-git-release/source-review-results-v2.json`, SHA-256 `62628770ad415951064dc9000c1cfe7d6cf65684803d83bce035df5569a64bd6` | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | pending | EVD-P06-001, EVD-P06-002, EVD-P06-003, EVD-P06-004 | Investigate current consumers; implement only confirmed differences; run selected local checks and independent review before one local acceptance decision. Preserve separate remote publication, Project, native and common-edition owners | platform for local source and documents; remote repository/release operator for external settings and publication; common standard owner for final edition |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package, current Git and release governance,
  direct commit/release scripts and tests, relevant Runbook and bounded
  `.github/` consumer files assigned to one writer at a time.
- **Forbidden Paths**: frozen Archive payloads, unrelated user/provider
  configuration, actual secrets, live Kubernetes/Vault resources and another
  writer's in-progress files.
- **Approval Required**: local work, normal commits, main integration and
  owned development cleanup are in the current instruction. Tag/Release
  publication, remote Issue/Project/server mutation, dispatch, deployment,
  credential use and live operation need their actual target and operator
  authority; no standing approval follows from this Task.
- **Static Validation**: derive focused tests and selected affected/staged
  gates from actual changed paths and current Registry. Record exact inputs,
  tool/config, outputs, adverse results and same-check resolution. Validate
  the final index and actual message immediately before each normal commit.
- **Live Validation**: DEFER to the operating owner until an authorized target
  and execution evidence exist. No prior PR or main-push check is P06 PASS.
- **Secret / Vault Handling**: inspect only non-secret source and metadata;
  do not read, print or transmit credentials or Vault data.
- **Rollback Plan**: use forward correction on the isolated branch, keeping
  completed Tasks and earlier failure records. External publication requires
  its own operator rollback or compensating-release decision.
- **Evidence Location**: this Task, exact reviewed Git commits and bounded
  ignored command receipts. No parallel progress ledger.

## Verification Summary

The intake and ready-transition documents each passed six selected exact-index
gates, actual message checks and normal commits. Source and document repair
is in progress; no final P06 implementation or selected-index result is claimed
by those intake receipts. Remote read-back is dated context, not hosted PR, Project or
publication success. Current hook configuration is an observation, not proof
of delivery. The first version, actual release, immutable setting, Project
state and common core adoption need their separate owners and evidence.
