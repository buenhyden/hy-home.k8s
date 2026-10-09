---
title: "Purpose-Based QA and CI Follow-up"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107-TSK-0003"
parent_ids: ["SPEC-0107-PLAN-0001"]
---

# Task: Purpose-Based QA and CI Follow-up

## Overview

This Task owns P05 execution for [WORK-003](../plan.md#work-breakdown) and
[VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan). It records
the current leaf/caller/input audit, implementation and selected local
validation before the single criterion acceptance decision. Completed
[Task 0001](tsk-0001-local-qa-and-release.md) and
[Task 0002](tsk-0002-archive-and-qa-retirement.md) retain their original
results. Their earlier local and hosted observations are inputs for comparison,
not P05 execution evidence.

## Inputs

- The current [Spec](../spec.md), [Plan](../plan.md),
  [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
  [ADR-0048](../../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md),
  [quality policy](../../../../.agents/governance/quality.md),
  [validation registry](../../../../scripts/validation/registry.json), and
  [GitHub surface](../../../../.github/repository-surface.md).
- The user's current P05 request: purpose- and input-based redesign of QA,
  CI/CD gates, lint and format, with local purpose QA for this public K8s
  repository and narrow trusted-base server PR style. Investigate actual
  leaves and consumers, retain distinct continuing protection, select affected
  checks, measure duplicate execution, and report results by actual input.
  Local investigation, plan, source/consumer repair, selected checks, normal
  commits, local main integration and cleanup of owned development refs are
  authorized. Remote writes or dispatch, server settings, deployment, tag,
  secrets and live operation have their separate target and authority.
- The coordinator's 2026-10-09 read-only GitHub branch and check lookup found
  remote main `5cfd420b…`, strict required `ci-summary` and `style-pr` checks
  from App 15368, no required `qa-provenance`, no main branch ruleset and two
  active tag-only rulesets. Earlier PR 136 head `a639…` and CI run
  `37785109216` are historical inputs, not execution for this P05 candidate.
- Intake source: clean `codex/p05-purpose-qa` worktree at
  `11a1c26210c26962b9899df0f046513b7e57056f` on 2026-10-09, based on
  local `main`. Stage 99 `sdlc/spec`, `sdlc/plan` and `sdlc/task` profiles
  select the three existing forms. Before this edit, this Spec package had
  completed WORK-001/002 and Tasks 0001/0002, with no
  `VAL-LOCAL-QA-006`, `WORK-003` or `SPEC-0107-TSK-0003` in the package.
- The one common review candidate remains `WGOV-CORE / 3.0.0-draft.3`,
  proposed owner `buenhyden`, proposed source
  `Project-Template/.agents/governance/shared-standard.md`, and reviewed
  content digest
  `sha256:3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`.
  Stage 99 registry source revision and approval reference are null. C01,
  C06, C07 and C12 are comparison input, not a final approved edition,
  local adoption or four-repository adoption. Existing local contracts own
  this implementation while the common decision remains pending.
- Initial P05 investigation has not measured the current leaf/caller map or
  completed implementation. The coordinator's remote read of branch metadata
  and prior PR 136 CI is a dated historical input; the P05 Task must bind any
  hosted claim to its own observed SHA, run, App and protection input.
  `SEC-P01-001` HIGH remains open with the security/CI operator.
- The intake source and document contract were admitted by six selected
  exact-index checks on tree `915a28a7ac972255f7d146f9f65a8785aa5dd6bf`
  and committed normally as `ea9f4d7920005df7d6112668b7a691685e497c34`.
  `_workspace/p05-intake-index-qa.log` has SHA-256
  `0702e583f7c62b9bdae0f82915477fb49edf1989798101c105e897f5a7a4091f`;
  the actual message passed pinned Commitizen and has SHA-256
  `eee6f0c6aa2c24d4440ef1f62b5fc376201dabd5a4cc8008b3674e14d5e4c5b9`.
  This admits the intake documents, not the later source implementation.
- Coordinator tool preflight used Python 3.12.3 and a task-owned environment
  created with `uv --no-config`; the existing hash-locked
  `.github/requirements/ci-validation.txt` packages installed with
  `--require-hashes --only-binary=:all:`. Ignored
  `_workspace/p05-tools-install.log` SHA-256
  `11e60bd5ffcf71d3caa5df59d2c57d7ae65e6cbc8b150a3dc1eba7dcf8490c2d`
  records the actual setup. Local `core.hooksPath` points to `scripts/githooks`;
  the common `.git/hooks/pre-commit` and `commit-msg` files are absent. The
  normal hook chain remains active; check each actual candidate message with
  pinned Commitizen rather than claiming an absent hook ran it.
- A first source proposal exists as an unstaged nine-path QA/code/test/fixture
  diff from intake commit `ea9f4d7920005df7d6112668b7a691685e497c34`.
  That earlier nine-path source-only diff had SHA-256
  `0efdaeffce3dd7658beaa6a92cad4b83fcd5d970628417f5d83998640fcb0f93`.
  It reuses the captured private tree for per-gate QA identity, holds the
  current Registry/inventory in the link context, routes QA entrypoint changes
  to the selector contract, and removes the completed-only cloud-absence
  guard and its dedicated test. Subsequent repairs to stale test expectations
  change that source-only diff; the earlier hash remains its historical input,
  not the final source identity. The source changes await selected exact-index
  admission and a normal source commit. The separate ordinary
  document impact-closure design remains pending.
  The revised nine-path source-only diff has SHA-256
  `2c850c8c3d598c630d9c30cb2680e5312cdd00b243871133ef67bf0254d538db`;
  this identifies the first unit after those test repairs, still before
  exact-index admission. The original first source index then failed three
  selected gates as EVD-P05-016. Subsequent source and style repairs changed
  the combined staged-plus-working-tree source-only diff from HEAD to ten
  paths, SHA-256
  `749edd868cc9fb722828262a910836759f3d0d1fd12cd89f34fb90bb9258298a`.
  The earlier nine-path hashes identify proposal and failed-input history,
  not the current source. The CI writer's three `.github/` paths are a
  separate concurrent diff and do not share these source-only digests.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-003 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | Map purpose QA and hosted consumers; repair proven duplicate selection and evidence boundaries; measure and validate the actual P05 input | platform | frontmatter | NOT_RUN | The aggregate WORK-003 result is not yet admitted. EVD-P05-002, EVD-P05-007, EVD-P05-012, EVD-P05-015 and EVD-P05-018 cover intake, repaired probes, inventory and current proposed source; EVD-P05-016 records an unresolved first source-index FAIL |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P05-001 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical owner, Stage 99 route and unused in-package ID audit | Local `main` source `11a1c26210c26962b9899df0f046513b7e57056f`; `git status --short --branch`, `git rev-parse HEAD`, `rg --files` and `rg -n` over this Spec package and Stage 99 registry; source files read on 2026-10-09 | PASS | This Task Inputs; Spec criterion and Plan WORK-003 link; current forms `docs/99.templates/templates/specs/{spec,plan,task}.template.md` | yes | none |
| EVD-P05-002 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Initial document exact-index and actual-message admission | Intake three-document tree `915a28a7ac972255f7d146f9f65a8785aa5dd6bf`, `python scripts/qa.py staged` through task-owned interpreter, pinned Commitizen on actual message, normal commit `ea9f4d7920005df7d6112668b7a691685e497c34` | PASS | `_workspace/p05-intake-index-qa.log` SHA-256 `0702e583f7c62b9bdae0f82915477fb49edf1989798101c105e897f5a7a4091f`; actual message SHA-256 `eee6f0c6aa2c24d4440ef1f62b5fc376201dabd5a4cc8008b3674e14d5e4c5b9`; six selected gates passed, with no source admission implied | yes | none |
| EVD-P05-003 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Task-owned validation tool and hook preflight | Python 3.12.3, `uv --no-config` environment and `--require-hashes --only-binary=:all:` against existing `.github/requirements/ci-validation.txt`; `git config --local core.hooksPath` and common hook presence check on intake commit | PASS | `_workspace/p05-tools-install.log` SHA-256 `11e60bd5ffcf71d3caa5df59d2c57d7ae65e6cbc8b150a3dc1eba7dcf8490c2d`; installed dependencies and observed hook topology; no actual later gate implied | yes | none |
| EVD-P05-004 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | First source proposal and consumer identity | Earlier nine-path unstaged QA/code/test/fixture source-only diff from `ea9f4d7920005df7d6112668b7a691685e497c34`, SHA-256 `0efdaeffce3dd7658beaa6a92cad4b83fcd5d970628417f5d83998640fcb0f93`; `git diff` over those paths only before later test-expectation repair | PASS | This Task Inputs and earlier first-slice worktree diff; concurrent CI three-path source diff is separate. A changed test input needs its own source identity; this proposal has no exact-index QA or normal source commit | yes | none |
| EVD-P05-005 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Actual 927-document link result and duplicate work comparison | First changed links reader in an unstaged worktree with a different Git index, base `ea9f4d7920005df7d6112668b7a691685e497c34` | FAIL | Checkout-root ignored `_workspace/p05-qa-design/links-after-actual.json` SHA-256 `3c2e144a223c4414e62e6124fc29054f68a3d294771da3340f555c38ce45b99e`; rc2 `configuration error: generic migration recovery proof differs`, underlying `ARCHIVE-MIGRATION-STAGED-DRIFT`. The guard legitimately rejects mismatched index/worktree input; use a synchronized staged clone | yes | none |
| EVD-P05-006 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Actual 927-document link result and duplicate work comparison | Changed links reader staged in a disposable clone at detached HEAD, base `ea9f4d7920005df7d6112668b7a691685e497c34` | FAIL | Checkout-root ignored `_workspace/p05-qa-design/links-after-detached-failed.json` SHA-256 `1a494213c68881c76718b1f1898fb50c4863450097d8227ed89b59a89869489a` summarizes observed rc2 and underlying `RECOVERY-DURABLE-REF`; the original JSON path was overwritten by later PASS, so this is an observed-output summary, not a raw failure log. Use a named durable ref in that clone | yes | none |
| EVD-P05-007 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Actual 927-document link result and duplicate work comparison | Old link source at intake `ea9f4d7920005df7d6112668b7a691685e497c34`; changed links reader staged in a named-ref disposable clone at the same base; actual diagnostics enabled on both inputs | PASS | Checkout-root ignored `_workspace/p05-qa-design/links-before-actual.json` SHA-256 `cae2de15530804aec7ba7f35cae69367b5401a799c5682ec3cd65315590546a3` and `links-after-staged-actual.json` SHA-256 `8ee7d020ac68de993e55dc92050a9761e2f8453b942037015cf6d7717bc4eeb9`; both rc0, zero diagnostics, stdout SHA-256 `0170043de0ba24f50cebd64c52cc181a9e46d0e9312baa9e283cf7eab4978cc2`, Registry loads 78→2, inventory 2→1, Git `ls-files` 3→2; one timing pair does not establish speed | yes | EVD-P05-005, EVD-P05-006 |
| EVD-P05-008 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Synthetic local runner result propagation and work-count comparison | Disposable Git fixture with a synthetic PASS/FAIL leaf; old `11a1c26210c26962b9899df0f046513b7e57056f` and proposed first-slice source at `ea9f4d7920005df7d6112668b7a691685e497c34` | PASS | Checkout-root ignored `_workspace/p05-qa-design/prechange-measurement.json` SHA-256 `45b3102b7460bba624e9e89a12a4ddd4a73b4a92c9d52bd222853c21a5990c77` and `postchange-measurement.json` SHA-256 `95e8dcf1aa0385f04c55af6f8c6af3bd30a203e06fc5828de67a0f641442dad2`; both PASS rc0/FAIL rc1 propagate, private tree scans 4→3, Git calls 33→32. Disposable histories differ, so these are work-count observations, not an exact-same-input speed claim or document/hosted result | yes | none |
| EVD-P05-009 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Read-only execution resource and failure-boundary audit | Current hosted job and style helper source, `scripts/run-validation-lane.py`, current branch/PR metadata as reported by CI owner on 2026-10-09 | PASS | Current CI source and coordinator handoff: job cancellation and finite execution, style helper input/output bounds, runner monotonic cleanup and process-group termination; no business deadline or reserve reapproval; historical PR 136 success does not measure a cold worst-case or certify this changed input | yes | none |
| EVD-P05-010 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Three asserted boundaries in scoped QA regression | First source worktree at `ea9f4d7920005df7d6112668b7a691685e497c34`, task-owned Python, `python -B -m unittest tests.test_qa_runner tests.test_documentation_link_boundary tests.test_document_scope_selection tests.test_validate_affected_surfaces tests.test_document_strict_cutover` | FAIL | Checkout-root ignored `_workspace/p05-qa-design/related-tests-adverse.json` SHA-256 `4da6c85f0aa56cc99a0d5b60df28828c4b25a7eadbd524da6a78722ea5bc7719` summarizes 132 tests in 474.951 seconds, 129 passed and three assertions failed: two stale private snapshot guard text expectations and one fixed template-link count. The summary is not a complete raw log; later named repairs need their own result | yes | none |
| EVD-P05-011 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Historical baseline assertion comparison | Untouched `ea9f4d7920005df7d6112668b7a691685e497c34` disposable clone, same task-owned Python, same three named tests as EVD-P05-010 | FAIL | Same `related-tests-adverse.json` receipt records 3/3 identical assertion failures in 26.499 seconds. This diagnostic comparison shows the assertions predate the P05 source diff; it is not a current required validation gate | no | none |
| EVD-P05-012 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Three asserted boundaries in scoped QA regression | Repaired first-slice tests: two named private snapshot guard cases on the current worktree and one named form-placeholder case in a synchronized staged named-ref clone; task-owned Python | PASS | QA owner observed two named QA cases PASS and the form case PASS in 279.291 seconds on its valid clone. Assertions now distinguish actual guard failures and require valid template links without pinning occurrence count. This resolves the three failed assertions, not a rerun of all 132 tests or final exact-index QA | yes | EVD-P05-010 |
| EVD-P05-013 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Finite first-slice caller, gate and fixture map | Intake source `ea9f4d7920005df7d6112668b7a691685e497c34`, four changed runtime/registry paths and in-repository direct references | PASS | Checkout-root ignored `_workspace/p05-qa-design/p05-current-consumer-map.json` SHA-256 `3890c00956fc439f89b3d447ae70fa287ef360cbf7432cc1db39c090b90cd914`; seven dynamic edges, three registered gates, eight direct test modules and one fixture identified. It covers finite in-repository references, not external or native discovery | yes | none |
| EVD-P05-014 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | First source proposal and consumer identity | Revised nine-path unstaged QA/code/test/fixture source-only diff from `ea9f4d7920005df7d6112668b7a691685e497c34`, SHA-256 `2c850c8c3d598c630d9c30cb2680e5312cdd00b243871133ef67bf0254d538db`; `git diff` over the same nine paths after repaired assertions and before EVD-P05-016 | PASS | Earlier first-slice worktree diff and this Task Inputs; it replaced EVD-P05-004 proposal bytes but is no longer the current input after later failure repairs. No successful exact-index QA or normal source commit is inferred | yes | none |
| EVD-P05-015 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Current static validation inventory | Dirty worktree at HEAD `ea9f4d7920005df7d6112668b7a691685e497c34`; tracked scripts, tests, `.github/`, `.agents/`, pre-commit config and current validation registry | PASS | Checkout-root ignored `_workspace/p05-qa-design/p05-current-validation-inventory.json` SHA-256 `6d9f547ef91775291bd76583104f46e4b981af3c3c8448f26caf42f7587eeb93`: 260 hashed tracked paths, 121 Python AST records, 206 static dynamic-call sites, 10 fixture records, 24 validators and 30 surfaces. It is a static snapshot; runtime imports, computed subprocess argv, native hook enforcement and external callers are unproven | yes | none |
| EVD-P05-016 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | First source exact-index selected QA admission | Fourteen-path staged tree `5d723055047e1642dc5ec4fb78fb8f504b61f57a`; task-owned Python `scripts/qa.py staged`; before and after `git write-tree` equal | FAIL | `_workspace/p05-source-index-qa.log` SHA-256 `7e8458fa6dc86b8e3f668cac2e7c36f1c35a83beb4f9fcb38e096e7eac1c2fd3`: 12 gates, nine PASS and three FAIL. Checkout-root ignored `_workspace/p05-qa-design/failed-leaves-diagnostics.json` SHA-256 `f6943263d6462472410b60f146737cebf79512d63d5234dec168a6086ab0abe0` preserves exact leaf output: links-and-owners rejects a `.github/rulesets/main-protection.md` direct Task link, repository-quality rejects three missing PR-template phrases, and selected-style reports `STYLE-FORMAT-MUTATION`. No resolution or source commit claimed | yes | none |
| EVD-P05-017 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Required-check producer and protection read-back | Coordinator's actual read-only GitHub branch, protection/ruleset and PR check lookup on 2026-10-09; remote main `5cfd420b…`, prior PR 136 head `a639…` and CI run `37785109216` | PASS | GitHub branch/ruleset/check API observations reported to this Task: strict main required `ci-summary` and `style-pr`, App 15368, no required `qa-provenance`, no main branch ruleset, two active tag-only rulesets. Historical PR checks were on a different input; no P05 hosted run or protection mutation occurred | yes | none |
| EVD-P05-018 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | First source proposal and consumer identity | Current ten-path QA/code/test source-only `git diff HEAD -- <ten paths>` combining staged and working-tree bytes from `ea9f4d7920005df7d6112668b7a691685e497c34`, SHA-256 `749edd868cc9fb722828262a910836759f3d0d1fd12cd89f34fb90bb9258298a` after three first-index failure repairs | PASS | Current source proposal across index and worktree: the QA owner removed only obsolete PR-template literal demands in repository quality and explicitly formatted two test files; the CI writer's separate three-path diff repairs the direct Task link. Restaging, changed-input selected index QA and normal source commit are still pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | pending | EVD-P05-002, EVD-P05-003, EVD-P05-007, EVD-P05-008, EVD-P05-012, EVD-P05-013, EVD-P05-015, EVD-P05-016, EVD-P05-017, EVD-P05-018 | Intake, local tool preflight, proposed source, finite static census, failed probe resolution, bounded measurements and remote read-back are recorded. The first source index failed three required gates; a later same-check PASS must explicitly resolve EVD-P05-016. Still require final source index and actual-message admission, remaining ordinary DOC impact closure, final independent review and local acceptance decision on their exact input | platform for local QA and documents; CI/security operator for hosted protection and `SEC-P01-001` |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package, current local QA/validation scripts,
  tests, hooks, quality and formatting guidance, relevant Operations guidance,
  and bounded `.github/` workflow and repository-surface consumers assigned
  to a single writer. File ownership is coordinated before each edit.
- **Forbidden Paths**: frozen Archive payloads, unrelated provider or personal
  configuration, actual secrets, live Kubernetes/Vault resources and another
  writer's in-progress files.
- **Approval Required**: the current P05 request authorizes local audit,
  implementation, checks, normal logical commits, local main integration and
  owned worktree/ref cleanup. It does not authorize remote push/PR write,
  workflow dispatch, protection/ruleset mutation, Release/tag publication,
  deployment, credential use or live operation. Any such action needs its
  actual operation, target, reviewed revision and operator approval record.
- **Static Validation**: derive named regressions and selected affected/staged
  gates from the current registry and changed input. Before each normal commit,
  inspect the final index, run its read-only lint/format and applicable
  document/purpose checks, and validate the actual message. Record commands,
  tool/config/input identity, failures and explicit resolutions here.
- **Live Validation**: DEFER to the operating owner until an authorized live
  target and execution evidence exist. Prior PR checks cannot become P05
  hosted or live PASS.
- **Secret / Vault Handling**: inspect only non-secret source and metadata;
  do not read, print or transmit credentials or Vault data.
- **Rollback Plan**: use a forward correction on the isolated branch for
  source and consumer changes; preserve failed-check and completed-Task facts.
  A protected remote or live action requires its own operator rollback plan.
- **Evidence Location**: this Task, actual reviewed commits and narrowly
  scoped ignored command receipts where an exact post-commit OID cannot be
  written into its own commit. No parallel progress ledger.

## Verification Summary

The intake owner audit and its six selected exact-index gates passed on their
specified inputs. A bounded first source proposal, local tool setup, finite
caller map and before/after measurements are now observed, but the revised
source unit still awaits its selected exact-index admission and normal commit.
The first full link probes failed on mismatched index/worktree and detached-ref
inputs; a staged named-ref clone then passed. The actual 927-document link
runs returned the same stdout digest and zero diagnostics while Registry
loads fell from 78 to 2, inventory enumerations from 2 to 1 and Git
`ls-files` calls from 3 to 2. One observed elapsed-time pair is not a speed
claim. A disposable synthetic runner fixture retained PASS and FAIL
propagation while its private tree scans fell from 4 to 3 and Git calls from
33 to 32; its Git histories differ and it does not certify document-content
or hosted style behavior. The five-module run observed 132 tests with three
failed assertions, reproduced on the clean baseline. The three repaired named
cases passed on their stated valid inputs; the complete 132 were not rerun
after that correction. The first source exact-index run on tree `5d723055…`
selected 12 gates: nine passed and links-and-owners, repository-quality and
selected-style failed. The actual original-tree leaf diagnostics and aggregate
log are EVD-P05-016; no changed-input PASS has resolved that row yet.
The coordinator has a historical remote branch/PR observation, but this Task
has no P05 hosted run, settings write, dispatch, deployment, native
enforcement or live PASS. The common candidate is unapproved, and
`SEC-P01-001` HIGH remains open.
