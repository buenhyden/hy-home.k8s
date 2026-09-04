---
title: "GitHub Routing and CI Evidence Implementation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0048-PLAN-0001"
---

# GitHub Routing and CI Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development`; assign each GRCE package to a
> fresh worker, run specification review before quality/security review, and
> preserve read-only remote boundaries.

## Overview

### Current Execution Disposition (2026-09-05)

This Plan remains `draft`; all package Tasks remain `queued`. Resume only
after Spec 0047's evidenced package closure through the legal package-local
`draft → active` route described in the
[Spec disposition](spec.md#current-execution-disposition-2026-09-05).
Accepted ADR-0031/0033 replace ADR-0021 and the public program-instance roster
as current execution authority. The older work breakdown is proposal input;
re-observe its paths, commands, providers, and current owners before activating
implementation. Do not restore retired progress, package routers, instance
rows, or old decision states. New execution evidence belongs in package Tasks.

**Goal:** Add one surface-ID-based GitHub projection contract and deterministic
parity validator, align native labeler/CODEOWNERS/hub claims, and preserve
intentional CI lanes without claiming hosted evidence for local work.

**Architecture:** `scripts/validation/registry.json` remains the sole path router.
`github-surface-routing.json` maps existing surface IDs to label and owner
classes, while the focused validator resolves tracked paths and compares the
machine projection with native `.github` files and workflow claims.

**Tech Stack:** Python 3, JSON Schema Draft 2020-12, YAML, CODEOWNERS parsing,
GitHub Actions static validation, unittest, Bash aggregate gates, and GitHub
CLI metadata-only reads.

## Context

[Spec 048](spec.md)
consumes the committed Spec 047 target matrix. Current drift includes missing
`.agents/**` and `.gemini/**` `area/agent` projections, incomplete explicit
CODEOWNERS coverage for shared/provider surfaces, and a GitHub hub statement
that describes the tag-only changelog workflow as manually dispatchable.

The current `ci.yml` keeps `pre-commit`, `repo-quality-static`,
`agent-governance-static`, and `manifest-static` as distinct evidence jobs and
aggregates them through `ci-summary`. This Plan does not merge those jobs
without exact semantic identity proof. A dated remote observation may record
workflow and branch metadata, but a historical run is valid only for its exact
SHA and current unpushed hosted evidence remains `DEFER`.

### Global Constraints

- Every shell command begins with `rtk`.
- No copied path/regex values are allowed in the new contract; every mapping
  references an existing `scripts/validation/registry.json` surface ID.
- Do not read workflow logs, ignored/private state, secrets, credentials,
  auth caches, shell history, provider payloads, or RTK logs.
- No push, PR, workflow dispatch/rerun, remote merge, branch-rule/ruleset
  mutation, release, or live-system action is authorized.
- Preserve full-SHA Actions, least permissions, explicit timeouts,
  concurrency, seven-day artifact retention, required `ci-summary`, and the
  always-start workflow boundary.
- Repository-quality is the pre-commit aggregate owner; do not add a second
  dedicated pre-commit owner for the same validator.

### Legacy Task ledger inputs

This Task is the durable execution ledger for Spec 048. It will record the
GitHub routing contract package, native labeler/CODEOWNERS/hub projection,
affected and aggregate routing, read-only remote metadata, logical commits,
QA, reviews, closure, and Spec 049 handoff. Every row is queued; this draft
claims no implementation, hosted-current result, remote mutation, or live
evidence.

- Parent [Spec 048](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md),
  and [superseded ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Spec 047 target disposition and successor matrix
- Current `scripts/validation/registry.json`, `.github/labeler.yml`,
  `.github/CODEOWNERS`, `.github/repository-surface.md`, workflow YAML, repository
  aggregate, GitHub security validator, and read-only remote metadata
## Goals & In-Scope

- Create `github-surface-routing.json`, adjacent closed schema, mutation
  fixture, focused validator, and focused unittest.
- Implement source-version, unknown/duplicate surface, copied-route,
  exception-owner, labeler, CODEOWNERS last-match, README/workflow claim, and
  remote-observation validation.
- Align `.github/labeler.yml`, `.github/CODEOWNERS`, and `.github/repository-surface.md`
  only where current evidence proves drift.
- Register the validator in affected-surface routing and the existing
  repository aggregate without creating another CI job.
- Preserve the current workflow/job topology unless exact comparison proves a
  true duplicate.
- Refresh read-only GitHub metadata with exact repository, SHA, timestamp,
  command class, result, limitation, owner, and retry trigger.
- Complete focused, affected, CI-security, strict-document, aggregate,
  all-files, diff, and independent review gates.

## Non-Goals & Out-of-Scope

- Remote GitHub setting changes, CODEOWNER review enforcement, rulesets,
  required approvals, merge methods, branch deletion policy, or admin policy.
- Workflow dispatch, push, PR, remote merge, release, publication, or hosted
  current-commit success claim.
- Workflow log/body reads, secret-bearing diagnostics, provider runtime, cloud,
  Kubernetes, Vault, ESO, Argo CD, or other live evidence.
- A copied path registry, duplicated workflow bodies, or a second primary
  command graph for the focused validator.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| GRCE-000 | Activate reciprocal Spec 048 execution path | Spec 047 closure | Spec 048 is first unfinished relation | Spec/Plan activate, activation Task starts, and Stage 03 index agrees under ADR-0031/0033 |
| GRCE-001 | Define RED contract and native-projection tests | GRCE-000 | Current drift captured | Focused tests reject every named schema, route, labeler, CODEOWNERS, README, and remote boundary defect |
| GRCE-002 | Implement contract, schema, validator, and self-test | GRCE-001 | Expected RED failures observed | Closed contract references surface IDs only and focused self-test/production pass |
| GRCE-003 | Align labeler, CODEOWNERS, and GitHub hub | GRCE-002 | Validator reports exact native drift | All mapped agent/provider surfaces have intended label and explicit owner; hub claims match YAML |
| GRCE-004 | Wire affected and aggregate validation once | GRCE-003 | Focused production validation passes | Surface routing, aggregate, script/test inventories, CI security, and current jobs agree |
| GRCE-005 | Record remote metadata, review, close, and hand off | GRCE-004 | All required local gates pass | SHA-bound remote record, zero review findings, reciprocal closure, and Spec 049 handoff |

### File map and interfaces

**Create:**

- `docs/00.agent-governance/contracts/github-surface-routing.json`
- `docs/00.agent-governance/contracts/github-surface-routing.schema.json`
- `tests/fixtures/github-surface-routing.json`
- `scripts/validate-github-surface-routing.py`
- `tests/test_validate_github_surface_routing.py`

**Modify when evidence requires:**

- `.github/labeler.yml`
- `.github/CODEOWNERS`
- `.github/repository-surface.md`
- `scripts/validation/registry.json`
- `tests/fixtures/validation-surfaces.json`
- `scripts/validate-repo-quality-gates.sh`
- `scripts/README.md`
- `tests/README.md`
- reciprocal package-local Spec/Plan/Task and current index surfaces

**Implement these exact interfaces:**

| Symbol | Input | Output / contract |
| --- | --- | --- |
| `ContractError` | `rule_id: str`, `detail: str` | Value-free validation exception exposing stable rule ID and detail |
| `CodeownersRule` | `pattern: str`, `owners: tuple[str, ...]`, `line_number: int` | Immutable parsed rule |
| `OwnerMatch` | `effective_owners: tuple[str, ...]`, `explicit: bool`, `rule_line: int` | Last-match result separated from explicit-class coverage |
| `load_json_document` | `path: Path`, `rule_id: str` | `Any`; rejects duplicate keys and invalid JSON |
| `validate_contract_data` | `root: Path`, `contract: dict[str, Any]`, optional keyword-only `schema` and `surfaces` dictionaries | `dict[str, Any]` normalized summary or `ContractError` |
| `classify_surface_path` | `surfaces: dict[str, Any]`, `raw_path: str` | Exactly one surface ID or `ContractError` |
| `evaluate_labeler` | `labeler: dict[str, Any]`, `path: str` | `set[str]` matched label classes |
| `parse_codeowners` | `text: str` | `list[CodeownersRule]` preserving order and line numbers |
| `evaluate_codeowners` | `rules: list[CodeownersRule]`, `path: str` | `OwnerMatch` using last-match semantics |
| `validate_workflow_claims` | `root: Path` | `None` on parity or `ContractError` |
| `validate_repository` | `root: Path` | `dict[str, int]` count summary |
| `run_self_test` | `root: Path` | `dict[str, int]` mutation summary |
| `main` | CLI `--root` and `--self-test` | exit `0` pass, `1` finding, `2` input/config error |

The implementation may reuse `normalize_path`, `match_route`, and path
classification semantics from `validate-affected-surfaces.py`, but must not
import CLI side effects or duplicate route data.

### Task 1: GRCE-000 — activate the package-local execution path

- [ ] Verify Spec 0047 and its package-local Plan/Tasks are terminal with
  required validation, review, and handoff evidence; re-observe the clean
  approved checkout and current canonical owners.
- [ ] Move only this Spec and Plan `draft → active`, and its activation Task
  `queued → in-progress`, atomically with the Stage 03 index.
- [ ] Run strict Registry, Markdown, links/owners, staged lifecycle, affected
  and staged lanes, plain pre-commit, and diff checks over the exact activation.
- [ ] Record evidence in the activation Task and commit the bounded change.
  No ADR transition, public execution roster, or implementation is part of
  activation. This Task remains queued until its predecessor condition holds.

### Task 2: GRCE-001 — define focused RED behavior

- [ ] Create `tests/test_validate_github_surface_routing.py` and the mutation
  fixture. Cover missing artifacts, unknown surface, duplicate mapping, copied
  route value, source-version mismatch, unowned exception, unsupported labeler
  shape, CODEOWNERS last-match masking, missing explicit class, tag/manual
  workflow-claim drift, and SHA-less remote observation.

- [ ] Use a concrete unknown-surface mutation and require its stable rule ID.

  ```python
  def test_unknown_surface_is_rejected(self):
      contract = copy.deepcopy(self.valid_contract)
      contract["mappings"][0]["surfaceId"] = "missing-surface"
      with self.assertRaisesRegex(self.module.ContractError, "GRCE-SURFACE-001"):
          self.module.validate_contract_data(
              self.root, contract, surfaces=self.validation_surfaces
          )
  ```

- [ ] Run the focused test and confirm RED is caused by missing production
  artifacts or behavior.

  ```bash
  rtk python3 -m unittest tests/test_validate_github_surface_routing.py
  ```

- [ ] Commit passing test and implementation together after GRCE-002 GREEN;
  retain the observed RED result in the Task rather than committing a broken
  branch.

### Task 3: GRCE-002 — implement the contract package

- [ ] Add Draft 2020-12 schema objects with `additionalProperties: false` and
  the exact top-level fields `schemaVersion`, `contractVersion`, `contractId`,
  `sourceContract`, `labelClasses`, `ownerClasses`, `mappings`, `exceptions`,
  and `remoteObservations`.

- [ ] Add contract data that points `sourceContract.path` to
  `scripts/validation/registry.json`, records source
  schema version `2`, and uses only surface IDs in `mappings`.

- [ ] Implement duplicate-key JSON loading, source compatibility, tracked path
  resolution, copied-route rejection, labeler parsing for current
  `changed-files/any-glob-to-any-file`, CODEOWNERS last-match behavior,
  README/YAML workflow claim comparison, and value-free diagnostics.

- [ ] Run focused self-test, production, and unittest.

  ```bash
  rtk python3 scripts/validate-github-surface-routing.py --root . --self-test
  rtk python3 scripts/validate-github-surface-routing.py --root .
  rtk python3 -m unittest tests/test_validate_github_surface_routing.py
  rtk git diff --check
  ```

- [ ] Commit the contract package.

  ```bash
  rtk git add docs/00.agent-governance/contracts/github-surface-routing.json docs/00.agent-governance/contracts/github-surface-routing.schema.json scripts/validate-github-surface-routing.py tests/fixtures/github-surface-routing.json tests/test_validate_github_surface_routing.py
  rtk git commit -m "feat: add github surface routing validator"
  ```

### Task 4: GRCE-003 and GRCE-004 — align native projections and routing

- [ ] Add `.agents/**` and `.gemini/**` to `area/agent`; preserve the existing
  `.claude/**`, `.codex/**`, gateways, and Stage 00 rules.

- [ ] Add explicit CODEOWNERS entries for shared/provider surfaces and root
  gateway files when required by the contract. Test global fallback and
  last-match effective ownership separately from explicit owner class.

- [ ] Correct `.github/repository-surface.md` so `generate-changelog.yml` is tag-only and
  CI lanes remain intentionally distinct; do not copy machine inventories.

- [ ] Register `github-surface-routing` with direct argv
  `python3 scripts/validate-github-surface-routing.py --root .`, attach it to
  affected agent/GitHub/governance/script/test surfaces, add mutation fixtures,
  and invoke self-test/production once through repository quality. Do not add a
  dedicated pre-commit hook.

- [ ] Run routing, AGQC, security, aggregate, and documentation checks.

  ```bash
  rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
  rtk python3 scripts/validate-affected-surfaces.py --root .
  rtk python3 scripts/validate-agent-governance-ci.py --root . --self-test
  rtk python3 scripts/validate-agent-governance-ci.py --root .
  rtk python3 scripts/validate-github-actions-security.py --root .
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk git diff --check
  ```

- [ ] Commit native projection and integration together so expectations never
  point at stale native state.

  ```bash
  rtk git add .github/CODEOWNERS .github/repository-surface.md .github/labeler.yml docs/00.agent-governance/contracts/github-surface-routing.json scripts/validation/registry.json tests/fixtures/validation-surfaces.json scripts/validate-repo-quality-gates.sh scripts/README.md tests/README.md
  rtk git commit -m "ci: align github projection evidence"
  ```

### Task 5: GRCE-005 — record remote evidence and close

- [ ] Refresh metadata only; bind every observation to time and exact SHA.

  ```bash
  rtk gh repo view buenhyden/hy-home.k8s --json nameWithOwner,defaultBranchRef,isPrivate
  rtk gh workflow list --repo buenhyden/hy-home.k8s --all
  rtk gh run list --repo buenhyden/hy-home.k8s --branch main --limit 10 --json databaseId,workflowName,headSha,status,conclusion,createdAt,event
  rtk gh api repos/buenhyden/hy-home.k8s/branches/main/protection/required_status_checks
  rtk gh api repos/buenhyden/hy-home.k8s/branches/main/protection/required_pull_request_reviews
  ```

- [ ] Record historical results only for their SHA; keep local-current hosted
  evidence and enforcement changes `DEFER`. Do not open logs.

- [ ] Run focused, affected, strict document, aggregate, all-files, formatter,
  and both diff checks; obtain independent requirements and quality/security
  reviews with zero open finding.

  ```bash
  rtk python3 scripts/validate-github-surface-routing.py --root . --self-test
  rtk python3 scripts/validate-github-surface-routing.py --root .
  rtk python3 -m unittest tests/test_validate_github_surface_routing.py
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk pre-commit run --all-files
  rtk git status --short
  rtk git diff --check
  rtk git diff --cached --check
  ```

- [ ] Close Spec 048, Plan, and Tasks through their legal lifecycle edges; update indexes and
  progress so Spec 049 becomes first unfinished, then commit closure.

  ```bash
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/0048-github-routing-and-ci-evidence/spec.md docs/03.specs/README.md docs/03.specs/0048-github-routing-and-ci-evidence/plan.md docs/03.specs/0048-github-routing-and-ci-evidence/plan.md docs/03.specs/0048-github-routing-and-ci-evidence/README.md#task-records docs/03.specs/0048-github-routing-and-ci-evidence/README.md#task-records docs/99.templates/registry.json
  rtk git commit -m "docs: record github routing closure"
  ```

## Verification Plan

```bash
rtk python3 scripts/validate-github-surface-routing.py --root . --self-test
rtk python3 scripts/validate-github-surface-routing.py --root .
rtk python3 -m unittest tests/test_validate_github_surface_routing.py
rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
rtk python3 scripts/validate-affected-surfaces.py --root .
rtk python3 scripts/validate-agent-governance-ci.py --root . --self-test
rtk python3 scripts/validate-agent-governance-ci.py --root .
rtk python3 scripts/validate-github-actions-security.py --root .
rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
rtk bash scripts/validate-repo-quality-gates.sh .
rtk pre-commit run --all-files
rtk git diff --check
rtk git diff --cached --check
```

### Legacy Task verification evidence

Not executed. Implementation will record exact artifact versions, contract
counts, mapped surface classes, native projection differences, focused and
aggregate results, formatter effects, remote repository/SHA/time/result/
limitation rows, reviews, logical commits, and successor handoff. Planned
commands and dated historical metadata are not current PASS evidence.
## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Contract duplicates route patterns | Closed schema and mutation tests reject copied exact/regex route values; mappings contain surface IDs only. |
| Global CODEOWNERS fallback hides missing explicit ownership | Validate effective owner and explicit class separately with last-match fixtures. |
| Labeler/CODEOWNERS parsers over-approximate semantics | Support only observed native shapes and fail closed on unsupported syntax. |
| CI jobs are merged as apparent duplicates | Require exact trigger, permissions, command graph, output, artifact, consumer, and required-check identity before removal. |
| Historical remote failure is promoted to current | Bind result to observed SHA and keep unpushed local HEAD hosted evidence `DEFER`. |
| Validator executes as two primary pre-commit owners | Use repository-quality as the only pre-commit owner and verify command inventory parity. |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: new GitHub routing contract/schema/fixture/validator/test;
  `.github/labeler.yml`, `.github/CODEOWNERS`, `.github/repository-surface.md`; current
  validation routing/fixtures, repository aggregate, inventories, reciprocal
  SDLC documents/indexes, and progress.
- **Forbidden Paths**: ignored/private state, secrets, auth caches, provider
  payloads, shell history, RTK logs, workflow logs, and live-system data.
- **Approval Required**: push, PR, remote merge, workflow dispatch/rerun,
  branch-rule/ruleset or review-enforcement change, credential use, release,
  deployment, or live mutation. None is authorized here.
- **Static Validation**: focused self-test/production/unittest, affected
  surfaces, AGQC, GitHub Actions security, strict documents, repository
  aggregate, all-files pre-commit, formatter inspection, both diff checks, and
  independent requirements plus quality/security reviews.
- **Live Validation**: `DEFER`; historical remote observations bind only their
  exact SHA and local-current hosted evidence remains `DEFER`.
- **Secret / Vault Handling**: no log or secret-value reads; diagnostics and
  durable evidence are metadata-only and value-free.
- **Rollback Plan**: revert GRCE commits in reverse order; native projection
  and its matching contract expectation revert together, and validator
  registration plus aggregate invocation revert together.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.
## Completion Criteria

- The new contract/schema references surface IDs only and rejects unknown,
  duplicate, copied-route, unowned, and incompatible data.
- Native labeler, CODEOWNERS, and GitHub hub claims match the reviewed contract
  and tracked workflow YAML.
- Current CI jobs remain distinct unless exact semantic identity is proven,
  and `ci-summary` remains the required aggregate.
- Focused, affected, AGQC, GitHub security, strict documents, aggregate,
  all-files, diff, and independent reviews pass.
- Remote observations are metadata-only, timestamped, SHA-bound, and no
  hosted-current, enforcement, provider, remote, or live result is fabricated.
- Spec 049 becomes the next eligible package only after Spec 048 closure.

## Traceability

- **Spec**: [GitHub Routing and CI Evidence](spec.md)
- **Task**: [GitHub Routing and CI Evidence Task](plan.md)
- **Program**: [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**: [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**: [superseded ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Predecessor**: Spec 047 Current Surface and Stash Reconciliation in the
  PRD-0007 program lineage
- **Successor**: Spec 049 Platform Validation and Security Evidence in the
  PRD-0007 program lineage

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-GRCE-001](spec.md#success-criteria--verification-plan) | GRCE-001, GRCE-002 | [Contract and validator evidence](tasks/tsk-0002-grce-001.md) |
| N/A — VAL-GRCE-002 and VAL-GRCE-003 share the Spec source above | GRCE-003 | N/A — reciprocal Task is linked in VAL-GRCE-001 |
| N/A — VAL-GRCE-004 and VAL-GRCE-005 share the Spec source above | GRCE-004 | N/A — reciprocal Task is linked in VAL-GRCE-001 |
| N/A — VAL-GRCE-006 and VAL-GRCE-007 share the Spec source above | GRCE-005 | N/A — reciprocal Task is linked in VAL-GRCE-001 |
| N/A — VAL-GRCE-008 shares the Spec source above | GRCE-000, GRCE-005 | N/A — reciprocal Task is linked in VAL-GRCE-001 |

### Legacy Task traceability

- **Spec**: GitHub Routing and CI Evidence
- **Plan**: GitHub Routing and CI Evidence Implementation Plan
- **Predecessor**: Spec 047 Current Surface and Stash Reconciliation
- **Successor**: Spec 049 Platform Validation and Security Evidence

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [GRCE-000](plan.md#work-breakdown) | Not executed | Queued activation evidence. |
| N/A — GRCE-001 shares the Plan and Spec sources above | Not executed | Queued focused RED evidence. |
| N/A — GRCE-002 shares the Plan and Spec sources above | Not executed | Queued contract package evidence. |
| N/A — GRCE-003 shares the Plan and Spec sources above | Not executed | Queued native projection evidence. |
| N/A — GRCE-004 shares the Plan and Spec sources above | Not executed | Queued affected/aggregate integration evidence. |
| N/A — GRCE-005 shares the Plan and Spec sources above | Not executed | Queued remote metadata, QA, review, and closure evidence. |
