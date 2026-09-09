---
title: "Agent Governance and Quality Gate Consolidation Implementation Plan"
version: "2.6.1"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0072-PLAN-0001"
---

# Agent Governance and Quality Gate Consolidation Implementation Plan

## Overview

Execute the approved [Spec](spec.md) with Superpowers writing-plans and
executing-plans. The Task owns state and results; the ordered work below owns
implementation and verification. The 2026-09-09 user instruction approves local
follow-up and main integration followed by task branch/worktree cleanup only
after the existing completion conditions are satisfied. The subsequent answer
limited that continuation to local review without external transmission. A
distinct 2026-09-09 approval adds `WP-010` and
[SPEC-0072-TSK-0002](tasks/tsk-0002-repair-governance-and-validation-contracts.md)
for local governance and validation contract repairs.

## Context

The authority migration is complete. Its source disposition, former baseline,
reviews and one-off merge approval remain historical evidence in the Task and
Git; they are not work to repeat. ADR-0036 is the current structural decision.
The approved follow-up extends SPEC-0072 to native lint/commit configuration,
formatting coverage, full-tree secrets, diagnostic privacy and duplicate gates.
Re-observe Git before writes and preserve the original checkout and its index.

## Goals & In-Scope

Correct the observed defects through existing owners: common governance,
provider adapters, validation registry/runner, pre-commit/native tool config,
independent tests, current docs and the hosted QA adapter. Preserve the shared
full/ci gate set, required checks and domain verification boundaries.

For `WP-010`, repair evaluation reads, exact QA/prompt inputs, artifact identity,
live-script temporary files and current owner prose through existing owners.
Keep each contract, implementation and focused regression in one logical unit.

## Non-Goals & Out-of-Scope

No new registry, QA wrapper, fixture framework, policy engine, provider model
change or live manifest behavior. No push, PR, dispatch, release/tag, credential
inspection, global settings or live infrastructure actions. After automatic
approval review rejected the proposed Claude call, the user selected local
review without external transmission. Only local native discovery/trust
metadata inspection is in scope; no Provider model call is authorized. Do not
bypass trust or permissions or retry an unchanged failure. The earlier main
integration and external actions remain dated evidence, not reusable authority.
`WP-010` adds no file deletion, gate, registry, profile, form, ledger, README
router, native projection or behavior change to pinned tools. It does not reopen
`WORK-001` through `WORK-009` or authorize native/provider/live execution.

## Global Constraints

`scripts/qa.py` remains the single supported QA entrypoint. Required-tool,
cancellation, timeout, output and cleanup failures remain FAIL. External
permissions/environment remain DEFER. No history rewrite, arbitrary stash,
blanket restore or hook bypass. Preserve frozen recovery identities and NUL
machine paths. Native configuration does not prove runtime delivery.

## Work Breakdown

`WP-005` through `WP-009` below are the dated 2026-09-08/09 follow-up scope
owned by `SPEC-0072-TSK-0001`; their completed local/hosted evidence is not
re-executed by this approval. That Task's `WORK-009` native observation remains
`In progress`/`DEFER` with the operator as next owner and is independent of
`WP-010`.

### WP-005: Correct bounded process diagnostics

Files: `scripts/run-validation-lane.py`, `tests/test_run_validation_lane.py`.
Keep the escaped tuple's fourth field as a state observation; remove argv reads.

1. Add a failing test that refuses `/proc/*/cmdline` access and observes running,
   zombie, disappeared and malformed states using temporary/mock process data.
2. Use bounded status reads and an allowlisted state letter; retain `comm`, PID,
   group and cleanup limits. Preserve updated main's exclusion of confirmed
   terminated states; unknown states still fail closed. Read state once for
   both classification and diagnostics. Remove synthetic token-only tests.
3. Run `python3 -B -m unittest tests.test_run_validation_lane` and inspect the
   diagnostic diff. Preserve timeout, cancellation and descendant regressions.

### WP-006: Repair formatting and full-snapshot secret coverage

Files: `.pre-commit-config.yaml`, `.gitleaks.toml`, validation registry,
`tests/test_validation_profiles.py`, `tests/test_validation_tooling_ownership.py`,
`tests/test_qa_runner.py`, and formatting/quality guidance.

1. Reproduce Codex selector omission, shfmt's success-without-check behavior,
   frozen mutation selection and clean-index Gitleaks scan omission.
2. Include both provider shell paths and set shfmt args to `--write -i 2`.
   Preserve Python-only Ruff selection. Resolve frozen exclusion through the
   existing lifecycle owner, retaining current/draft archive coverage.
3. Give full/ci pre-commit explicit `--hook-stage manual`; keep staged native
   Gitleaks and a manual directory-scan hook on the same pin. Skip `.git`
   traversal narrowly; retain all other manual-stage hook coverage.
4. Run targeted selector, stage and snapshot tests, including unchanged tracked
   canary and non-ignored hidden input. Explicit fixes target reviewed paths.

### WP-007: Align commit validation and current guidance

Files: Git/quality policy, commit prompt/provider command, `.cz.toml`,
`.gitmessage`, `cliff.toml`, PR/commit documentation and independent tests.

1. Test valid/invalid candidate messages and stage selection in a temporary Git
   repository using the pinned Commitizen hook. Create no invalid real commit.
2. Remove full-QA/native-hook equivalence claims and workstation policy prose.
   Use infrastructure examples, distinguish enforced syntax from advice, retain
   BREAKING CHANGE footer and document unsupported bang syntax.
3. Put release-chore skip before generic chore; account for supported build,
   deps and release groups. Preserve historical parser compatibility.
4. Test synthetic changelog behavior with the pinned tool when available;
   record missing tool/environment as a visible limitation.

### WP-008: Remove demonstrated duplication

Files: `scripts/validate-harness.sh`, its current README/PR/fixture consumers,
`scripts/validation/repository/quality.py`, independent test modules,
`.pre-commit-config.yaml`, `.hadolint.yaml`, formatting guidance.

1. Inventory current wrapper consumers and its seven domain gate contracts.
   Point consumers at full QA; remove repeated infrastructure validation.
2. Move embedded heading/table and generic-residue synthetic probes into tests.
   Keep actual production rule functions and independent negative diagnostics.
3. Confirm no Dockerfile target, remove unused hadolint hook/config and repair
   current references. Preserve historical references and Git recovery.
4. Run ownership/profile and transferred-probe tests. Record removed call
   counts; do not claim measured wall-time savings without measurements.

### WP-009: Validate environment, workflows and final handoff

Files: `.github/workflows/ci.yml`, workflow tests, scripts/QA documentation and
this package's Task. Other workflows change only for observed defects.

1. Check local OS/Python/tools, interpreter fallback and trusted caches. Reuse
   hash-locked CI dependencies in an isolated environment when feasible;
   preserve closed HOME/PATH and avoid cold-cache pressure on this workstation.
2. Correct resolver documentation and cache identity where evidence requires.
   Preserve named checkout/history, single QA job and fail-closed ci-summary.
3. Run focused workflow tests for PR, push, dispatch and failure/cancel/skip;
   contract-test full/ci equality instead of rerunning equivalent profiles.
4. Complete independent read-only review and the sequence below. Record actual
   results, limits, rollback and next owner in the Task. Keep its inherited
   native follow-up under WORK-009 separate from Spec hosted acceptance.
5. Re-observe the existing task-branch hosted run read-only and record its exact
   input and verdict. Preserve prior native observations without replaying
   consumed approvals or treating process completion as native acceptance.
6. Resume from the committed local evidence and inspect native prerequisites
   through local metadata APIs. Record discovery separately from unexecuted
   model/tool/hook/probe checks. No external Provider call follows from this
   continuation; preserve the inherited native completion condition.
7. Review the evidence change, run focused document checks, quick and exact
   staged QA, validate the actual message and commit through active hooks.
   Run final full QA over the resulting tree and record subsequent Task-only
   evidence separately without a self-referential validation loop.
8. If every inherited completion condition is met, integrate into local main,
   verify the resulting tree and remove only this task's clean worktree and
   merged branch. Otherwise preserve both and name the remaining prerequisite.

### WP-010: Repair governance and validation contracts

Implement `VAL-AGQ-015` through `VAL-AGQ-019` as five disjoint ownership units.
Each behavior-changing unit starts with a focused failing case and ends with
focused passing checks and diagnostic review. The prose-only unit uses focused
contract checks without manufacturing a failing test. Related contract, implementation and tests remain one
logical boundary without a fixed commit count. A correction returns to its
owning unit; the package-document owner coordinates Task state separately.

| Unit | Cause and owned files | Focused tests and diagnostics | Commit boundary and rollback |
| --- | --- | --- | --- |
| WP-010A | Unsafe direct registry/case/response/citation reads in `scripts/run-agent-evaluations.py`; tests in `tests/test_agent_evaluations.py`; exactly one new pair `evals/cases/code-reviewer-unauthorized-write.json` and `evals/responses/code-reviewer-unauthorized-write.synthetic.md`; optional `evals/README.md` only for minimal safe-input contract prose. Reuse `scripts/validation/repository/bounded_io.py` read-only. | Registry and evaluation path escape, parent/leaf symlink, non-regular, oversize and strict-UTF-8 cases; tracked authority-negative expectation; diagnostics omit response/citation payloads. Move this module's `unittest.main` guard to EOF. | Keep runner, tests and the one case/response pair atomic; include the README only if its bounded input contract needs the minimal clarification, without a new ownership framework. Revert this logical unit; bounded I/O and registry contents remain unchanged. |
| WP-010B | `scripts/qa.py` compares only source bytes, so a child can modify and stage the snapshot index; `.agents/prompts/change-review.md` treats only the unstaged diff as the subject. Own `scripts/qa.py`, `tests/test_qa_runner.py`, `.agents/prompts/change-review.md`, `scripts/prompt-input.py`, `tests/test_prompt_input.py`, `tests/test_agent_governance.py`, `tests/test_k8s_pre_edit_hook.py`, `tests/test_validate_agent_registry.py` and `tests/README.md`; update `scripts/validate-knowledge-surface.py` only if the existing prompt consumer requires the atomic contract change. | Reproduce modify-and-stage mutation; compare pre/post index content. Staged-only succeeds; unstaged-only succeeds; staged and unstaged changes that cancel in the net HEAD diff still review both; empty and untracked-only refuse. A plural subject may name existing input rows with any-nonempty semantics while singular contracts and unknown-name rejection remain unchanged. Preserve deleted-path routing fixtures. Move three test guards to EOF, remove only the duplicate hook guard, and correct deleted-module guidance. | Commit QA/prompt/test-entry changes together. Revert that commit; no registry, hook registration, deleted-path fixture, predicate DSL or prompt-ID exception is introduced. |
| WP-010C | Current validation checks profile-shaped IDs but does not consistently bind every numbered family to its path, current corpus uniqueness or retired-number provenance. Own `scripts/validate-markdown-profiles.py`, `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py` and new `tests/test_document_artifact_identity.py`; use `scripts/document_contracts.py` only if the existing shared contract helper is required. | Coverage of registered numbered authored profiles with representative wrong-but-pattern-valid ID probes, duplicate IDs including partial selected inputs, retired reuse through existing base/sealed-migration/tombstone evidence, and allowed same-document lineage. Tombstone payloads and frozen bytes remain unchanged; diagnostics distinguish stage, package and Task numbering. | Keep identity implementation and its new focused tests atomic. Revert this logical unit; do not edit Stage 99 registry/forms, Archive records or issued IDs. |
| WP-010D | Three live scripts write predictable shared `/tmp` files. Own `infrastructure/verify/verify-gitops.sh`, `infrastructure/verify/verify-external-services.sh`, `infrastructure/verify/verify-ingress-tls.sh` and new `tests/test_infrastructure_tempfiles.py`. | Stub `kubectl`, `curl` and `rg`; run no live command. Verify private per-run mode, cleanup on success/failure, original exit status and existing diagnostics. | Commit three scripts and stubbed tests together. Revert that commit; no retention framework or live state is involved. |
| WP-010E | Current prose blurs evaluation ownership, editor/hook defaults and PR category versus commit syntax. Own `.agents/README.md`, `docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`, `.agents/governance/formatting-and-linting.md`, `.editorconfig`, `.ruff.toml`, `RTK.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `scripts/validation/repository/quality.py`, `docs/99.templates/README.md` and `docs/99.templates/templates/README.md`; update an existing focused test owner only if implementation evidence identifies it. | Focused checks confirm evaluation routes to runner/registry/data owners, ADR clarification is dated, formatting text reflects Git/editor/hooks/pinned defaults, PR categories point to `.cz.toml`, and `quality.py` copies no 13-type list. Check Stage 99 family-versus-physical-group wording with no route/form migration. | Keep current prose and its corresponding existing assertion atomic. Revert prose without changing historical decisions, tool pins, pre-commit configuration or forms. Package Spec/Plan/Task remain with the coordinated document owner. |

#### WP-010 dependency and ownership

| Unit | Depends on | Exclusive write owner | Handoff evidence |
| --- | --- | --- | --- |
| WP-010A | Approved Spec/Plan/Task | Evaluation runner, evaluation tests and one new case/response pair | `VAL-AGQ-015` focused RED/GREEN |
| WP-010B | Approved Spec/Plan/Task | QA runner, prompt contract/builder and named guard/README tests | `VAL-AGQ-016` focused RED/GREEN |
| WP-010C | Approved Spec/Plan/Task | Existing Markdown-profile/lifecycle implementations and new focused identity tests | `VAL-AGQ-017` focused RED/GREEN |
| WP-010D | Approved Spec/Plan/Task | Three live scripts and their stubbed test module | `VAL-AGQ-018` focused RED/GREEN |
| WP-010E | WP-010A through WP-010D final behavior | Current prose/config comments and corresponding existing assertion | `VAL-AGQ-019` focused checks; package owner records final handoff |

### WP-011: Close the documentation entry point and the gaps it exposed

Implement `VAL-AGQ-020` and the defects the boundary sweep surfaced. Each unit
starts from a focused failing case and ends with its passing result.

| Unit | Cause and owned files | Focused tests and diagnostics | Commit boundary and rollback |
| --- | --- | --- | --- |
| WP-011A | Files outside `docs/` reached numbered stage documents through direct links, so every implementation README depended on stage paths. Own `scripts/validate-links-and-owners.py`, the 24 consumer documents, `.agents/governance/document-authoring.md` as rule owner, and new `tests/test_documentation_link_boundary.py`. | `LINK-STAGE-BOUNDARY` fires for every numbered stage target written outside `docs/`, stays silent for the hub, for sources inside `docs/`, and for targets outside the stage tree. | Keep the diagnostic, its consumers and the rule owner atomic. Revert the unit; no stage path, machine reference or docs-internal link changes. |
| WP-011B | The pre-action guard bounded its selector above the hook registration that kills it, and required a `--provider` value it then discarded. Own `scripts/provider_write_guard.py` and `tests/test_k8s_pre_edit_hook.py`. | The bound is compared against both providers' registered timeouts; the Claude payload, path and project variables are read only under the Claude provider. | Keep guard and regressions atomic. Revert the unit; adapters, registrations and the accept/trust boundary are unchanged. |
| WP-011C | Every Archive-stage path with a non-archive profile was reduced to an identity-only check, so the stage index answered to no frontmatter contract. Own `scripts/validate-markdown-profiles.py`, `docs/98.archive/README.md` and `tests/test_common_agents_document_routes.py`. | The index without frontmatter reports `FM-DELIMITER`; a retained payload keeps its identity-only contract. | Keep the narrowed exemption, the conforming index and the route regressions atomic. Revert the unit; retained payloads and sealed bytes are untouched. |
| WP-011D | Four current statements described absent behavior: projection-owned tools, a path-filtered labeler, an undocumented second CI binary, and two review items naming filters and a lane with no owner. Own `.claude/README.md`, `.github/repository-surface.md`, `.github/PULL_REQUEST_TEMPLATE.md` and `scripts/validation/repository/quality.py`. | The corrected template phrase remains the phrase the quality gate asserts. | Keep prose and its assertion atomic. Revert the unit; no workflow, trigger or gate behavior changes. |
| WP-011E | One Git object fixture had two definitions and three further suites imported one of them from a test module. Own `tests/git_fixture.py`, both archive suites, the three importers and `tests/README.md`. | The five affected modules pass unchanged. | Keep the helper and every consumer atomic. Revert the unit; no test behavior or fixture data changes. |

## Verification Plan

For each changed behavior, targeted RED then GREEN. During work run quick;
before each logical commit inspect status/diffs, stage explicit paths, inspect
cached diff, run both diff checks and exact staged QA, then validate the actual
message and use normal active hooks. Related contract/implementation/tests
travel together; no arbitrary commit count target.

Run full QA over the final working tree before handoff. Its discovery and
pre-commit gate are not repeated on identical bytes. If fixes alter bytes,
review/restage and refresh affected evidence. Record subsequent Task-only
changes with scoped document checks; do not create a self-SHA/full-run loop.
Measure targeted invocation/setup/snapshot/gate timing and cache identity.
Cold installation, hosted/native/live results require their own environment;
no absent measurement is a performance claim or PASS.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| User work is mixed into commits | Stay on the dedicated `codex/governance-contract-repairs` branch in the observed clean root checkout; inspect and preserve the existing index before each logical commit |
| Security scan or formatter input shrinks | Synthetic stage/lifecycle/path tests and explicit owner review |
| Removal loses a diagnostic | Move tests before removal; map consumers and unique domain gates |
| Tool installation or active hooks fail | Keep changes; report exact blocker without bypass/global changes |
| Rollback reopens a defect | Forward revert reviewed logical commits with paired config/tests/consumers |

## Completion Criteria

All applicable local acceptance passes with independent review disposition and
logical local commits. Required failures remain incomplete. Hosted, native and
live evidence stay separate with next owners. The inherited Task completion
condition keeps native follow-up open even when Spec static/hosted acceptance
and local implementation are complete; that older native scope introduces no
criterion beyond the criteria it already owned.
The dated TSK-0001 request authorized local integration and task-owned cleanup
only when its own conditions were met; that authority is historical evidence,
not permission for `WP-010`. Remote writes remained outside that continuation.
The original Task preserves the completed migration and current limits.

For `WP-010`, completion means behavior changes have targeted RED/GREEN evidence,
the prose-only unit has focused contract checks, and all units have exact-index
staged evidence per logical commit, normal-hook and actual
pinned-message evidence, independent review, and one final full result. The
initial queued Task contract is committed before its first legal status
transition. Branch/worktree finish, remote actions and the older native
`WORK-009` remain outside this approval.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGQ-001](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-002](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-003](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-004](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-005](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-006](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-007](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-008](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-009](spec.md#success-criteria--verification-plan) | WP-007 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-010](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-011](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-012](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-013](spec.md#success-criteria--verification-plan) | WP-005 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-014](spec.md#success-criteria--verification-plan) | WP-008 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-015](spec.md#success-criteria--verification-plan) | WP-010A | [SPEC-0072-TSK-0002](tasks/tsk-0002-repair-governance-and-validation-contracts.md) |
| [VAL-AGQ-016](spec.md#success-criteria--verification-plan) | WP-010B | [SPEC-0072-TSK-0002](tasks/tsk-0002-repair-governance-and-validation-contracts.md) |
| [VAL-AGQ-017](spec.md#success-criteria--verification-plan) | WP-010C | [SPEC-0072-TSK-0002](tasks/tsk-0002-repair-governance-and-validation-contracts.md) |
| [VAL-AGQ-018](spec.md#success-criteria--verification-plan) | WP-010D | [SPEC-0072-TSK-0002](tasks/tsk-0002-repair-governance-and-validation-contracts.md) |
| [VAL-AGQ-019](spec.md#success-criteria--verification-plan) | WP-010E | [SPEC-0072-TSK-0002](tasks/tsk-0002-repair-governance-and-validation-contracts.md) |
| [VAL-AGQ-020](spec.md#success-criteria--verification-plan) | WP-011A | [SPEC-0072-TSK-0003](tasks/tsk-0003-documentation-entry-point-and-gate-repairs.md) |
| [VAL-AGQ-020](spec.md#success-criteria--verification-plan) | WP-011B | [SPEC-0072-TSK-0003](tasks/tsk-0003-documentation-entry-point-and-gate-repairs.md) |
| [VAL-AGQ-020](spec.md#success-criteria--verification-plan) | WP-011C | [SPEC-0072-TSK-0003](tasks/tsk-0003-documentation-entry-point-and-gate-repairs.md) |
| [VAL-AGQ-019](spec.md#success-criteria--verification-plan) | WP-011D | [SPEC-0072-TSK-0003](tasks/tsk-0003-documentation-entry-point-and-gate-repairs.md) |
| [VAL-AGQ-014](spec.md#success-criteria--verification-plan) | WP-011E | [SPEC-0072-TSK-0003](tasks/tsk-0003-documentation-entry-point-and-gate-repairs.md) |
