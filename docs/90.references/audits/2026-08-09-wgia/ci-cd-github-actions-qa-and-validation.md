---
title: 'Audit: CI/CD, GitHub Actions, QA, and Validation'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: CI/CD, GitHub Actions, QA, and Validation

## Overview

This report owns the audit of CI/CD, GitHub Actions, QA, formatting, linting,
syntax, tests, general checks, Validation, Verification, lane selection,
workflow security, evidence results, and dormant controls at observation commit
`50628b84165479b03efc0a25be075a49c91a9aef`.

## Reference Type

Dated repository-static delivery and quality audit. It neither owns workflow
behavior nor replaces the validation-surface and quality-standard contracts.

## Authority Boundary

Workflow YAML, the validation-surface JSON/schema, Stage 00 quality standards,
test suites, and validation scripts retain their current roles. A local parse
or PASS does not prove a hosted run, branch protection, deployment, provider
configuration, or live reconciliation.

## Scope

Included: tracked workflows, quality lanes, formatter/linter/syntax/test
controls, Validation/Verification semantics, security validation, fixtures,
fallbacks, skips, and evidence handoff. Excluded: remote Actions runs,
credentials, provider settings, live deployment, dormant-control activation,
canonical-owner remediation, and aggregate/full-gate execution.

## Definitions / Facts

### CI/CD

The observation tree contains five workflows and eleven jobs. `ci.yml` owns
branch policy, affected-job selection, four selectable validation jobs, and a
fail-closed summary. `generate-changelog.yml` creates a seven-day preview
artifact for version tags. No workflow deploys or reconciles desired state;
GitHub Actions is repository QA, not live deployment CD.

### GitHub Actions

Five workflows contain fifteen `uses` entries over seven unique Actions, all
pinned to full 40-hex commits. All five set root `contents: read`, every workflow
has bounded concurrency, and only greeting, labeler, and stale jobs receive
their required issue/PR write permissions. The changelog artifact retains for
exactly seven days. Hosted runs, rulesets, environments, and actual artifacts
remain outside this report's evidence.

### QA

`docs/00.agent-governance/rules/quality-standards.md` owns lane/result/handoff
semantics. The affected-surface contract owns 22 surfaces, 22 required
validators, and four selectable CI jobs. Pre-commit owns 29 hooks across one
local and twelve immutable remote repositories; direct tests and validator
self-tests supply negative and production evidence.

### Formatting

`.editorconfig`, `.prettierignore`, and `.prettierrc.json` are tracked.
The two Prettier files are routed inputs but no hook, runner, aggregate, or CI
command invokes Prettier. The quality standard states this exact dormant,
decision-gated boundary. Because no current surface falsely claims coverage,
WGIA-004 records `DEFER` and does not manufacture a failing TDD probe.

### Linting

Pre-commit supplies Markdown, shell, Dockerfile, workflow, manifest, secret,
JSON/TOML/YAML, whitespace, and commit-message checks. The aggregate script
adds strict document, contract, policy, security, syntax, and Python regression
checks. Optional `kube-linter` and `conftest` execution is reported separately
from their mandatory built-in fallbacks.

### General Checks

`scripts/validate-repo-quality-gates.sh` is the aggregate repository quality
entrypoint, while `scripts/run-validation-lane.py` executes contract-selected
affected, staged, or all-files validators. WGIA-004 ran only focused workflow,
supply-chain, selection, document, link, and diff checks; it did not run the
aggregate gate, stage files, or invoke pre-commit.

### Verification

Verification asks whether the implementation satisfies Spec 054 acceptance
criteria. WGIA-004's repository-static audit and review evidence may verify its
bounded acceptance scope, but local PASS cannot establish hosted workflow,
branch-protection, artifact, deployment, or live results.

### Validation

Validation asks whether inputs, syntax, structures, schemas, routes, and
contracts are well formed and admissible. The Stage 00 result vocabulary is
`PASS`, `SKIP`, `FAIL`, and `DEFER`; this is distinct from audit finding
verdicts.

### Observation and Current Drift

The workflow, pre-commit, quality-standard, affected-surface, CI lock, and
focused workflow validator owners are identical between the observation commit
and starting HEAD `f2b9c2b9450431a253b328c48d5ba174cdb3ba86`. Current drift in
the inspected quality area is limited to WGIA-001 document-profile inventory
validator/fixture documentation; it does not change the CI/QA conclusions.

### Workflow Matrix

| Workflow | Trigger and jobs | Actions and pins | Permissions and concurrency | Artifact / evidence boundary |
| --- | --- | --- | --- | --- |
| `.github/workflows/ci.yml` | push to `main`, pull request to `main`, manual dispatch; seven jobs including four affected-surface outputs | checkout and setup-python at full commit SHAs; Gitleaks v8.30.0 tarball plus exact SHA-256 | root `contents: read`; per-ref cancellation | summary emits selected `PASS`/`SKIP`/`FAIL`; no hosted run observed |
| `.github/workflows/generate-changelog.yml` | version-tag push; one changelog job | checkout, git-cliff, upload-artifact at full commit SHAs | root `contents: read`; per-ref, no cancellation | `CHANGELOG.md` preview artifact, integer retention 7; not a tracked release write |
| `.github/workflows/greetings.yml` | opened issue or pull request; one job | first-interaction at full commit SHA | root read; job issues/PRs write; per issue/PR cancellation | remote mutation intent only; execution `DEFER` |
| `.github/workflows/labeler.yml` | opened or synchronized pull request; one job | labeler at full commit SHA | root read; job PR write; per-PR cancellation | remote mutation intent only; execution `DEFER` |
| `.github/workflows/stale.yml` | daily `30 1 * * *`; one job | stale at full commit SHA | root read; job issues/PRs write; single maintenance group | remote mutation intent only; execution `DEFER` |

### Validation Lane Matrix

| Lane | Trigger and exact command/tool | Result and depth | Fallback / SKIP | Artifact | Owner |
| --- | --- | --- | --- | --- | --- |
| targeted | task-selected focused validator or test | closed result vocabulary; `repository-static` | unavailable optional tool is `SKIP`; deeper evidence is `DEFER` | command, scope, output | owning Task and validator |
| affected | `run-validation-lane.py --lane affected --paths-file <nul> --delimiter nul` | closed result vocabulary; `repository-static` | empty/no-applicable input is `SKIP`; required child failure is `FAIL` | selected paths/validators and bounded digests | selection JSON + runner |
| staged | runner `--lane staged`, then plain `pre-commit run` on exact index | closed result vocabulary; `repository-static` | neither command substitutes for the other | exact staged set plus both results | quality standard + pre-commit |
| tests | validator self-tests and named `python3 -m unittest ...` suites | `PASS`/`FAIL`; `repository-static` | inapplicable suite is reasoned `SKIP` | test identity/count/output | test and validator owners |
| all-files | `pre-commit run --all-files`; runner all-files is supplemental | closed result vocabulary; `repository-static` | unavailable optional tool is not full coverage | hook output and diff | quality standard + pre-commit |
| formatter-review / rerun | inspect status/worktree/index diffs; rerun after mutation | closed result vocabulary; `repository-static` | rerun `SKIP` only when no formatter changed files | reviewed mutation set | quality standard |
| diff checks | `git diff --check` and staged equivalent | `PASS`/`FAIL`; `repository-static` | no inference to other lanes | exact worktree/index scope | Git + owning Task |
| CI selection | `select-affected-surfaces.py --lane ci` in `ci.yml#jobs.changes` | tracked intent; hosted result separate | unselected job is summary `SKIP`; invalid state fails | four GitHub outputs | workflow + selection JSON |
| CI validation jobs | pre-commit all-files, aggregate, agent checks, manifest/policy checks | hosted result needs run identity | four jobs may be unselected; summary rejects bad combinations | GitHub check result | `ci.yml` |
| changelog automation | git-cliff on version tag | hosted result only | non-tag run not selected | seven-day `CHANGELOG.md` artifact | changelog workflow |
| message/manual | commitizen commit-msg and eight local manual-capable hooks | closed result vocabulary; `repository-static` | all-files does not prove explicit stages | hook result | pre-commit + quality standard |
| remote/live | hosted rulesets, deployment, provider, reconciliation, cluster | `DEFER` without authorized evidence | no local fallback promotes depth | exact run URL or live record | provider/operator |

### Check-family Matrix

| Check family | Exact active surfaces | Coverage boundary |
| --- | --- | --- |
| Formatting | EditorConfig; EOF, line-ending, trailing-whitespace hooks; `shfmt -i 2` | Active hygiene/shfmt only; Prettier is dormant `DEFER`. |
| Lint | markdownlint-cli2, ShellCheck, shfmt, Hadolint, actionlint, zizmor, kube-linter | Pre-commit execution required for tool coverage; config presence is insufficient. |
| Syntax | check-yaml/check-toml/check-json; aggregate `bash -n`; manifest parsers | Repository-static parse only. |
| Unit/regression | validator self-tests; Python `unittest` modules | Exact named suite/output; not application coverage. |
| Integration/contract | infrastructure static contracts, GitOps, Vault/ESO, document/harness/selection contracts | Static contract integration, not external service success. |
| Security/policy | Gitleaks, detect-secrets, Actions security, secret handling, policy gates, optional kube-linter/conftest | Optional `SKIP` stays separate from mandatory fallback PASS. |

### Canonical-owner Inventory

| Role | Current evidence surface | Foundation use |
| --- | --- | --- |
| Machine owner | `docs/00.agent-governance/contracts/validation-surfaces.json` and schema | Path-to-validator and local/CI selection. |
| Semantic owner | `docs/00.agent-governance/rules/quality-standards.md` | Lane, result, completion, and handoff meaning. |
| Workflow owner | `.github/workflows/*.yml` | Tracked GitHub workflow intent. |
| Evidence producer | `scripts/run-validation-lane.py`; validators; tests | Repository-static results. |
| Local hook owner | `.pre-commit-config.yaml` | Tracked hook definitions, not execution proof. |

### Finding Convention

Every material finding exposes the complete finding field set and uses only the
closed evidence-depth and audit-verdict vocabularies. QA result values remain a
separate closed vocabulary and are never substituted for audit verdicts.

#### WGA-QA-001 — Tracked GitHub Actions controls align repository-statically

- **Request IDs**: `REQ-WGA-003`, `REQ-WGA-004`.
- **Scope**: five workflow triggers, eleven jobs, fifteen Action uses, permissions, concurrency, job selection, summary semantics, and artifact retention.
- **Expected state**: tracked Actions are immutably pinned, least-privileged, concurrency-bounded, fail closed for selected jobs, and explicit about repository-static versus hosted evidence.
- **Observed state**: all fifteen uses are full-SHA pins across seven Actions; five workflow roots are read-only and concurrent; required write permissions are job-scoped; changelog retention is exactly seven; local security and workflow-contract checks pass.
- **Evidence**: `.github/workflows/ci.yml#jobs`; `.github/workflows/ci.yml#permissions`; `.github/workflows/ci.yml#concurrency`; `.github/workflows/generate-changelog.yml#jobs.changelog`; `.github/workflows/greetings.yml#jobs.greeting.permissions`; `.github/workflows/labeler.yml#jobs.label.permissions`; `.github/workflows/stale.yml#jobs.stale.permissions`; `scripts/validate-github-actions-security.py#main`; `scripts/validate-agent-governance-ci.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: current workflow intent has deterministic supply-chain, permission, selection, and artifact-retention controls.
- **Disposition**: `Keep`.
- **Canonical owner**: each workflow for intent; Actions-security and agent-governance-CI validators for repository-static enforcement.
- **Verification**: Actions security self-test/production, agent-governance CI self-test/production, CI Python contract, and 110 relevant workflow tests.
- **Uncertainty**: hosted execution, effective GitHub permissions, rulesets, artifacts, and branch protection were not observed.
- **Blocker**: none at repository-static depth.

#### WGA-QA-002 — Lane selection and active QA tool ownership align

- **Request IDs**: `REQ-WGA-008`, `REQ-WGA-010`, `REQ-WGA-015`, `REQ-WGA-021`.
- **Scope**: affected/staged/all-files/message/manual/CI lanes; formatting, lint, syntax, unit, integration, contract, security, and policy checks.
- **Expected state**: every path resolves without ambiguity to required validators and CI jobs; commands, fallback semantics, result classes, artifacts, and owners remain explicit.
- **Observed state**: production coverage resolves 858 paths across 22/22 surfaces to 22 validators and four CI jobs with zero uncovered/ambiguous; all validator fallbacks fail closed. Pre-commit has 29 hooks across twelve frozen remote repositories and one local repository; optional-tool skips remain separate from mandatory fallbacks.
- **Evidence**: `docs/00.agent-governance/contracts/validation-surfaces.json#lanes`; `docs/00.agent-governance/contracts/validation-surfaces.json#validators`; `docs/00.agent-governance/contracts/validation-surfaces.json#ciJobs`; `docs/00.agent-governance/rules/quality-standards.md#validation-lane-contract`; `docs/00.agent-governance/rules/quality-standards.md#result-vocabulary`; `.pre-commit-config.yaml#repos`; `scripts/run-validation-lane.py#main`; `scripts/validate-affected-surfaces.py#main`; `tests/README.md#evidence-boundaries`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: local and tracked CI selection can distinguish required failures, no-applicable-file skips, optional-tool skips, and deferred deeper evidence.
- **Disposition**: `Keep`.
- **Canonical owner**: validation-surface JSON for selection; quality standard for semantics; pre-commit/scripts/tests for execution evidence.
- **Verification**: affected-surface self-test/production, CI Python self-test/production, workflow regressions, and focused document checks.
- **Uncertainty**: actual pre-commit environments and hosted selected-job execution were not run by WGIA-004.
- **Blocker**: none at repository-static contract depth.

#### WGA-QA-003 — Prettier is dormant exactly as the current owner declares

- **Request IDs**: `REQ-WGA-009`.
- **Scope**: `.prettierrc.json`, `.prettierignore`, affected-surface routing, hooks, runner, aggregate gate, CI, and current coverage claims.
- **Expected state**: configured-but-uninvoked tooling is reported as dormant, never as coverage; activation or retirement requires a separate approved decision.
- **Observed state**: two configuration files and two routed inputs exist, with zero Prettier consumers across pre-commit, runner, aggregate, and five workflows. The quality standard explicitly says dormant and decision-gated, so no false claim or TDD RED exists.
- **Evidence**: `.prettierrc.json#printWidth`; `.prettierignore#*.min.js`; `docs/00.agent-governance/contracts/validation-surfaces.json#surfaces[id=root-config]`; `docs/00.agent-governance/rules/quality-standards.md#canonical-completion-sequence`; `.pre-commit-config.yaml#repos`; `scripts/run-validation-lane.py#main`; `scripts/validate-repo-quality-gates.sh#main`; `.github/workflows/ci.yml#jobs`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `DEFER`.
- **Impact**: active whitespace and shfmt controls remain valid, but no handoff may claim Prettier coverage.
- **Disposition**: `DEFER`; preserve the declared dormant boundary without activation/removal in this audit.
- **Canonical owner**: quality standards for formatter completion semantics; root configuration and validation-surface routing for tracked dormant inputs.
- **Verification**: deterministic probe returned `config=2 routed_inputs=2 consumers=0 owner_claim=1 red_required=0`.
- **Uncertainty**: whether a future content/toolchain requirement justifies activation or tracked-config retirement.
- **Blocker**: separate approved formatter/toolchain decision; none is required for current accurate reporting.

#### WGA-QA-004 — Validation is evidenced while Verification and CD remain bounded

- **Request IDs**: `REQ-WGA-003`, `REQ-WGA-020`, `REQ-WGA-021`.
- **Scope**: focused local results, Spec 054 acceptance verification, hosted CI, branch controls, artifacts, deployment, and live GitOps reconciliation.
- **Expected state**: Validation reports well-formed/admissible inputs independently from Verification of acceptance outcomes, and neither is promoted to hosted or live depth without direct evidence.
- **Observed state**: focused Actions, CI Python, affected-surface, workflow-test, Markdown, link, and diff Validation passes. WGIA-004 content/quality reviews remain pending; no hosted run, ruleset, artifact, environment, deployment job, or live reconciliation was accessed. Changelog generation is preview automation, not deployment CD.
- **Evidence**: `docs/00.agent-governance/rules/quality-standards.md#coverage-applicability`; `docs/00.agent-governance/rules/quality-standards.md#validation-lane-contract`; `docs/00.agent-governance/rules/quality-standards.md#handoff-evidence-contract`; `.github/workflows/ci.yml#jobs.ci-summary`; `.github/workflows/generate-changelog.yml#jobs.changelog`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#success-criteria--verification-plan`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: local contract confidence is strong, but the audit cannot claim hosted CI success, remote governance, deployment CD, or live readiness.
- **Disposition**: `Keep` repository-static results; deeper lanes remain `DEFER`.
- **Canonical owner**: quality standards and Spec 054 for result meaning; GitHub/operator owners for hosted/live evidence.
- **Verification**: independent WGIA-004 specification/content and quality reviews; exact hosted run identity only if separately authorized later.
- **Uncertainty**: effective hosted permissions, selected-job execution, branch protection, artifact availability, and live platform state.
- **Blocker**: hosted/remote/live access is outside WGIA-004 authorization; independent report reviews remain pending.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-QA-001 | machine owner | `docs/00.agent-governance/contracts/validation-surfaces.json#lanes`; `docs/00.agent-governance/contracts/validation-surfaces.json#surfaces`; `docs/00.agent-governance/contracts/validation-surfaces.json#validators`; `docs/00.agent-governance/contracts/validation-surfaces.json#ciJobs`; `docs/00.agent-governance/contracts/validation-surfaces.schema.json#properties` | Deterministic validator and CI selection. |
| SRC-WGA-QA-002 | policy owner | `docs/00.agent-governance/rules/quality-standards.md#validation-lane-contract`; `docs/00.agent-governance/rules/quality-standards.md#result-vocabulary`; `docs/00.agent-governance/rules/quality-standards.md#handoff-evidence-contract` | Lane, result, and handoff meanings. |
| SRC-WGA-QA-003 | evidence producer | `.github/workflows/ci.yml#jobs`; `.github/workflows/generate-changelog.yml#jobs.changelog`; `.pre-commit-config.yaml#repos`; `scripts/run-validation-lane.py#main`; `scripts/validate-github-actions-security.py#main`; `scripts/validate-ci-python-contract.py#main`; `scripts/validate-affected-surfaces.py#main`; `tests/fixtures/validation-surfaces.json#selectionCases` | Tracked checks, negative fixtures, and execution intent. |
| SRC-WGA-QA-004 | historical snapshot | `docs/90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md#actionable-finding-register` | Prior observation only. |

## Review and Freshness

- Review status: `Approved`; independent specification/content and quality
  reviews found no Critical or Important issue.
- Review disposition: `Approved` as a bounded repository-static audit, with no
  remediation candidate because current dormant-tool and Validation/
  Verification ownership is accurate.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: workflow YAML, Stage 00 quality semantics,
  validation-surface contract, tests, hooks, and scripts.
- Refresh triggers: workflow, lane, result, hook, formatter, linter, test,
  fixture, fallback, source, observation commit, or evidence-depth change.
- Next owner: WGIA-009 for cross-report integration; no WGIA-010 canonical
  change is proposed by this report.
- Hosted Actions, provider-runtime, credential-bearing, remote, and live lanes
  remain `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/0055-workspace-governance-audit-and-remediation/spec.md)
- [Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
- [Implementation Task](../../../03.specs/0055-workspace-governance-audit-and-remediation/tasks.md)
- [Prior CI/QA Audit](../2026-07-11-weia/ci-qa-automation-pipeline-workflow.md)
