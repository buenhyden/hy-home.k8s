---
title: "Delivery policy, scripts, and GitHub routes"
version: "0.2.2"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0002"
---

# Task: Delivery policy, scripts, and GitHub routes

## Overview

Execute [Plan WP-0002](../plan.md) against the approved [SPEC-0103](../spec.md). Implementation landed in `b105708fcc545566aa89a97daadd409b8b1aa4ef` on `codex/qa-evidence-implementation`. Hosted execution is separate evidence.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-003, VAL-QER-009, VAL-QER-011.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-002 | VAL-QER-003, VAL-QER-009, VAL-QER-011 | Assign delivery owners, repair routes, audit script consumers | platform | In progress | Implementation committed; local focused, quick, and exact-index staged evidence PASS; independent handoff review PASS; hosted DEFER | `b105708fcc545566aa89a97daadd409b8b1aa4ef` and verification below. |

## Approval and Safety Boundaries

- **Allowed Paths**: .agents/governance/quality.md; .agents/governance/git.md; .agents/workflows/work-lifecycle.md; scripts/README.md; .github/ISSUE_TEMPLATE/config.yml; .github/PULL_REQUEST_TEMPLATE.md; .github/dependabot.yml; .github/labeler.yml; .github/SECURITY.md; .github/repository-surface.md; tests/test_ci_qa_workflow.py; conditional transfer of scripts/validation/repository/quality.py proved by a RED test
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Authenticated GitHub settings are read-only evidence; no repository setting mutation in this task
- **Static Validation**: python3 -m unittest tests.test_ci_qa_workflow tests.test_validation_profiles tests.test_validation_tooling_ownership; python3 scripts/qa.py quick
- **Live Validation**: Read back destination/label/private-reporting settings; labeler fork behavior remains a separate hosted observation
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Revert policy and consumer routes together; retain independent script checks unless transfer was proved.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

Local evidence is recorded below. Static fixtures are not hosted or provider observations.

### Implementation snapshot and validation

- Branch: `codex/qa-evidence-implementation`; base: `a18d1ed92a9d76eda07e71cc90a4689a24427b8e`; implementation commit: `b105708fcc545566aa89a97daadd409b8b1aa4ef`. That commit changed 13 Task-owned files; its post-commit worktree was clean.
- RED: `python3 -m unittest tests.test_ci_qa_workflow tests.test_validation_profiles tests.test_validation_tooling_ownership` ran 53 tests with five expected route failures (PR local-full demand, Discussions contact, Dependabot label, cluster label, private reporting). The manifest missing-directory/nonempty negative passed. A separate projection-transfer test failed against the old PR-template validator assertion, as expected.
- GREEN: `python3 -m unittest tests.test_ci_qa_workflow tests.test_validation_profiles tests.test_validation_tooling_ownership tests.test_repository_quality_rules` ran 57 tests, all passed. `python3 scripts/validate-github-actions-security.py --root .` returned `PASS: GitHub Actions security`.
- `python3 scripts/qa.py quick` passed all 13 selected gates on 13 working-tree paths. After a Task-only evidence wording correction, `python3 scripts/qa.py staged` passed all 13 gates against the corrected exact index committed as `b105708f`. `git diff --check` and `git diff --cached --check` passed; the normal commit used `scripts/githooks` without bypass. An earlier quick run failed on invalid Task status/headings and an obsolete PR-template assertion; those were repaired before the passing runs.
- Delivery lane: local full QA was not required for this PR-bound unit. The hosted `ci-summary` SHA/run is `DEFER` until a PR exists. No push, PR, merge, or live mutation was performed.
- Independent read-only review round 1 found the code/config changes aligned with the brief but found this tracked handoff incomplete. This Task-only correction records the missing evidence; Task-only repair `b4e854c0` passed quick/staged 6/6 and independent `review_task2` scoped re-review was clean, with one finding addressed and zero open. The controller recorded the local unit complete over `a18d1ed9..b4e854c0`. Rollback is a forward revert of the implementation and Task-only follow-up commits together. The later format-only repair `4f06cf92` passed focused 14/14, quick/staged 3/3 and full 23/23; independent `review_task2_formatter` returned Spec PASS / quality Approved, no findings. The operator owns outstanding hosted and remote evidence; Task 6 records the final integration snapshot.

### Active CI/QA script disposition

`ci.yml` calls `qa.py ci` once. `qa.py` resolves registry profiles, and
`run-validation-lane.py` executes their argv. Quick/staged/full routing and
`coveredBy` are in `scripts/validation/registry.json`; the table records current
consumers, not a second machine registry. `tests/test_validation_profiles.py`
checks profile selection; `tests/test_validation_tooling_ownership.py` checks
single aggregate ownership. Existing non-CLI library modules remain imported by
these owners and have no independent QA invocation to retire.

| Active script / gate | Caller | Unique failure meaning | Direct test / check | Decision |
| --- | --- | --- | --- | --- |
| `qa.py`; `run-validation-lane.py` | CI, local quality procedure, hooks via selected lanes | Profile/snapshot selection; bounded child failure | `test_validation_profiles.py`, `test_run_validation_lane.py` | Keep |
| `select-affected-surfaces.py`; `validate-affected-surfaces.py` | QA/runner, provider write guard; registry full | Path-to-surface routing; tracked coverage | `test_validation_profiles.py`, validation-surface fixtures | Keep |
| `validate-agent-governance.py` | registry quick/staged/full | Role/projection permission and skill integrity | `test_agent_governance.py` and registered QA | Keep |
| `.agents/evaluations/run-agent-evaluations.py` | registry quick/staged/full | Agent evaluation case contract | evaluation tests and registered QA | Keep |
| `run-archive-contract-tests.py` | registry quick/staged; full unit discovery covers it | Archive regression cases on changed scope | `test_archive_registry_contract.py`, registry `coveredBy` tests | Keep |
| `archive_cutover.py` | registry full | Archive cutover and history integrity | archive tests and registered QA | Keep |
| `validate-ci-python-contract.py` | registry full | Locked Python dependency identity | `test_validate_ci_python_contract.py` | Keep |
| `validate-document-contract-registry.py` | registry quick/staged/full | Document route/schema integrity | document contract tests and registered QA | Keep |
| `validate-document-lifecycle.py` | registry quick/staged/full | Lifecycle and staged transition integrity | document lifecycle tests and registered QA | Keep |
| `validate-github-actions-security.py` | registry full | Workflow triggers, permissions and pinned Actions | `test_validate_github_actions_security.py` | Keep |
| `validate-gitops-change-set.py` | registry quick/staged/full | GitOps changed-set identity | `test_validate_gitops_change_set.py` | Keep |
| `validate-gitops-structure.sh` | registry quick/staged/full | Argo CD roots, hierarchy and kustomization completeness | registry QA and structure fixtures | Keep |
| `validate-infrastructure-contracts.sh` | registry quick/staged/full | Repository infrastructure references | registry QA | Keep |
| `validate-k8s-manifests.sh` | registry quick/staged/full | YAML parse plus required directories/nonempty manifest set | `test_ci_qa_workflow.py` missing/empty fixture; registered QA | Keep; full syntax overlaps pinned `check-yaml`, but presence failures do not transfer |
| `validate-knowledge-surface.py` | registry quick/staged/full | Knowledge navigation/owner route | registered QA | Keep |
| `validate-links-and-owners.py` | registry quick/staged/full | Current document link and owner integrity | document link tests and registered QA | Keep |
| `validate-markdown-profiles.py` | registry quick/staged/full | Authored Markdown profile conformance | profile tests and registered QA | Keep |
| `validate-policy-gates.sh` | registry quick/staged/full | Conftest verify and deployment policy denial | policy fixtures and registered QA | Keep |
| `scripts/validation/repository/quality.py` | registry quick/staged/full | Repository-wide structural contract | `test_repository_quality_rules.py` | Keep |
| `check-secret-handling.sh` | registry quick/staged/full | Redacted plaintext-secret pattern denial | `test_check_secret_handling.py` | Keep |
| `validate-vault-eso-contracts.py` | registry quick/staged/full | Vault/ESO reference and isolation contract | `test_validate_vault_eso_contracts.py` | Keep |
| `validate-workspace-boundary.py` | registry full | Staged/ignored workspace boundary | `test_workspace_boundary.py` | Keep |
| `.agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py` | registry quick/staged/full | Selectorless Service/EndpointSlice contract | `test_external_service_contracts.py` and registered QA | Keep |
| pre-commit manual hooks; unit discovery | registry full/ci | Formatting/lint/secret scan; independent unit behavior | `test_validation_tooling_ownership.py`, full/ci contract tests | Keep once per exact input |
| `githooks/chained-hook.sh` and `pre-commit`, `commit-msg`, `pre-push` entries | local Git hooks | Global-before-workspace hook status; pre-push stdin retained for both | hook chain tests and Git policy | Keep; pre-push is active without a QA stage |

Direct consumer search covered `.github/workflows`, `.pre-commit-config.yaml`,
`githooks/`, QA profiles and argv, imports, `scripts/README.md`, tests, and
current document links. No active script had both zero consumers and zero
unique diagnostics. No workflow or validator was removed. The PR-template assertion in `scripts/validation/repository/quality.py` changed after a RED projection test proved the old local-full requirement conflicted with the delivery route. The manifest negative
fixture failed for missing `infrastructure/` and for an empty manifest set, so
removing that gate would lose a check. The archive quick/staged runner and
pre-push chain likewise retain distinct consumers.

### GitHub route and event review

`ci.yml` still runs one QA job on main push, PR, or manual dispatch and has the
same read-only default permission and pinned Actions. `labeler.yml` still uses
`pull_request` with job-local `pull-requests: write`; fork PR token behavior is
not established by a static file. Greetings, stale maintenance, and tag-triggered
changelog generation are separate from required QA. No trigger, permission,
Action identity, required `ci-summary` name, or full QA invocation changed.

Authenticated read-only `gh api` on 2026-10-01 reported `has_discussions=false`,
labels `github_actions` and `area/gitops` present while `github-actions` and
`area/cluster` were absent, and private vulnerability reporting `enabled=true`.
The corresponding tracked routes now point to those existing destinations.
The private reporting URL itself and labeler behavior on a fork PR have no
hosted test here; exact hosted run ID and effective branch/tag ruleset evidence
remain `DEFER` for the operator/PR owner. The ruleset-list read returned no
entries; the tracked ruleset note is not remote enforcement evidence.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-002](../plan.md#work-breakdown) | In progress | Implementation `b105708f`; local evidence in Verification Summary; independent local reviews PASS; hosted evidence DEFER. The workflow topology described above is the Task 2 snapshot; Task 6 reconciles the later isolated/verifier/publisher routes. |
