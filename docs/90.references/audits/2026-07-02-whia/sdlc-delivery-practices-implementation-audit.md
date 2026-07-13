---
title: 'Reference: SDLC Delivery Practices Implementation Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-02
---

# Reference: SDLC Delivery Practices Implementation Audit

## Overview

This dated audit compares the SDLC delivery practices benchmark model to
current repo-backed implementation evidence in `hy-home.k8s` as checked on
2026-07-02. It covers spec-driven development, Stage 03/04 lifecycle routing,
CI/CD, QA validation, formatting, pre-commit, and static-vs-live evidence
boundaries.

This audit is descriptive reference material. It does not change active
governance policy, CI workflow semantics, scripts, pre-commit configuration,
templates, release or operations procedure, provider runtime behavior,
credentials, manifests, approval boundaries, or live runtime behavior.

Static repository evidence does not prove GitHub CI has run on this branch
unless that run is separately checked. Static repository evidence also does
not prove live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, or
secret readiness.

### Purpose

- Record whether the researched SDLC delivery practices model is implemented
  in current repository surfaces.
- Separate external benchmark material, repo-backed implementation evidence,
  validation lanes, gaps, automation opportunities, and residual risks.
- Preserve a bounded follow-up checklist without redefining active policy,
  CI/CD behavior, formatting rules, release procedure, or live readiness.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-02
- Refresh trigger: spec lifecycle, Stage 04 plan/task lifecycle, CI workflow,
  QA gate, formatting, pre-commit, template, validation-script, audit
  benchmark, or audit-index changes.

## Authority Boundary

- **Authoritative for**:
  - SDLC delivery practices implementation audit findings as checked on
    2026-07-02.
  - Repo-backed evidence paths used for this dated comparison.
  - Candidate follow-up routes for future specs, plans, tasks, validators,
    workflow reviews, pre-commit reviews, or operations documents.
- **Not authoritative for**:
  - Active governance policy, CI workflow semantics, branch policy, release
    approval, pre-commit hook policy, template requirements, validation script
    behavior, or operations runbooks.
  - GitHub CI execution status for this branch unless a separate GitHub check
    is inspected.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret,
    paid-job, or external-service readiness.
  - New CI jobs, pre-commit hooks, scripts, templates, provider adapters,
    release procedures, credentials, or automation changes.

## Scope

- Covers spec-driven development, Stage 03 Spec lifecycle, Stage 04 Plan
  lifecycle, Stage 04 Task/evidence lifecycle, secure SDLC evidence lanes,
  CI/CD jobs, QA validation commands, formatting and pre-commit, static-vs-live
  readiness boundaries, and automation opportunities.
- Uses `docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md` as the
  benchmark model and current repository files as local implementation
  evidence.
- Treats repo-backed evidence as stronger than external benchmark material for
  local implementation status. External sources may inform the benchmark, but
  they do not prove local implementation unless a repository surface
  implements or routes the capability.
- Excludes live environment checks, GitHub Actions run inspection, secret
  reads, release approval changes, policy changes, script changes, workflow
  changes, pre-commit changes, template changes, runtime adapter changes, and
  operations procedure changes.

## Definitions / Facts

### Benchmark Model

The benchmark model expects delivery work to move through explicit artifacts:
implementation intent, technical contract, execution plan, task/evidence
record, validation, and handoff. GitHub Spec Kit informed the benchmark with a
`Spec -> Plan -> Tasks -> Implement` flow, while NIST secure SDLC and
supply-chain guidance informed the secure evidence-lane expectations.

For this repository, local implementation status depends on tracked repository
surfaces: Stage 03 specs, Stage 04 plans and tasks, Stage 00 quality and
documentation rules, the CI/CD QA guide, `.github/workflows/ci.yml`,
`.pre-commit-config.yaml`, `scripts/**`, and task evidence. External standards
and upstream tools provide comparison context only; they do not prove local
implementation by themselves.

The benchmark also separates evidence into three lanes:

- **Repo-static evidence**: checks against committed files, docs structure,
  templates, scripts, manifests, generated indexes, and static contracts.
- **CI/toolchain evidence**: GitHub Actions jobs and tool-backed checks such
  as pre-commit, markdownlint, shellcheck, shfmt, actionlint, zizmor,
  gitleaks, detect-secrets, kube-linter, and related validators.
- **Live runtime evidence**: separately approved checks against k3d, ArgoCD,
  Vault, ESO, Kubernetes, deployments, cloud resources, external services, or
  secret readiness.

### Implementation Matrix

| Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route |
| --- | --- | --- | --- | --- | --- | --- |
| Spec-driven development | Delivery should preserve traceability from specification through plan, task, implementation, validation, and handoff. | The repository implements an equivalent Stage 03/04 artifact ladder without adopting GitHub Spec Kit: specs define implementation contracts, plans define execution order and gates, and tasks own status plus evidence. | Implemented | [SDLC research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md), [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md), [Stage 03 README](../../../03.specs/README.md), [Stage 04 plans README](../../../04.execution/plans/README.md), [Stage 04 tasks README](../../../04.execution/tasks/README.md) | Artifact existence does not prove every future task follows the lifecycle or that subjective spec quality is complete. | Keep lifecycle changes in Stage 03/04 templates, README indexes, Stage 00 routing rules, and task evidence. |
| Stage 03 Spec lifecycle | Specs should own implementation contracts, verification criteria, related inputs, and links to downstream execution. | Stage 03 README defines specs as implementation contracts, requires verification and traceability, and indexes current specs including this audit-pack spec. The template map routes `docs/03.specs/<feature-id>/spec.md` to `spec.template.md`. | Implemented | [Stage 03 README](../../../03.specs/README.md), [Audit pack spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md), [Templates README](../../../99.templates/README.md), [Documentation Protocol](../../../00.agent-governance/rules/documentation-protocol.md), [Document Stage Routing Rules](../../../00.agent-governance/rules/document-stage-routing.md) | Static index and template evidence do not prove the current branch has passed remote CI or every spec has perfect design coverage. | Route spec lifecycle changes to Stage 03 owners and validate with repo-quality gates plus review evidence. |
| Stage 04 Plan lifecycle | Plans should define execution order, risks, validation gates, rollout/rollback, approval boundaries, and links to tasks. | Stage 04 plans README defines Plan ownership, and the audit-pack plan breaks work into logical tasks with validation criteria, non-goals, risks, approval gates, and commit boundaries. | Implemented | [Stage 04 plans README](../../../04.execution/plans/README.md), [Audit pack plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md), [Plan Template](../../../99.templates/templates/sdlc/execution/plan.template.md), [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) | Plan status and checklist alignment are not finalized until Task 6; this audit does not update the plan file. | Keep final plan completion and status alignment in PLN-006/T-006. |
| Stage 04 Task/evidence lifecycle | Tasks should own executable work units, status, validation commands, evidence rows, and handoff notes. | Stage 04 tasks README defines task evidence ownership, and the audit-pack task record tracks T-001 through T-006 with status rows, phase checkboxes, validation commands, and task evidence. | Implemented | [Stage 04 tasks README](../../../04.execution/tasks/README.md), [Audit pack task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [Task Template](../../../99.templates/templates/sdlc/execution/task.template.md), [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md) | Task evidence proves recorded local checks and manual review, not remote CI execution or live runtime readiness. | Continue recording validation evidence in Stage 04 and reserve final pack integration for T-006. |
| SDLC and secure SDLC evidence lanes | Secure SDLC claims should distinguish repo-static, CI/toolchain, and live runtime evidence, with secret and supply-chain boundaries explicit. | Research, quality standards, and the CI/CD QA guide define separate evidence lanes and state that repo-static/CI checks do not prove live readiness. Secret handling, workflow security, and supply-chain checks are routed through scripts, pre-commit, and CI surfaces. | Partial | [SDLC research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md), [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md), [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md), [Scripts README](../../../../scripts/README.md), [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) | The repository maps secure SDLC lanes, but this audit does not prove full NIST SSDF coverage, dependency freshness, action-source review completion, or live secret readiness. | Add any deeper SSDF or supply-chain assessment through a future security/governance Spec, Plan, Task, and validator evidence. |
| CI/CD jobs | CI should provide fast feedback, path-scoped validation, least-privilege defaults, static manifest checks, and an aggregate result. | `.github/workflows/ci.yml` defines `branch-policy`, `changes`, `pre-commit`, `repo-quality-static`, `manifest-static`, and `ci-summary`, with read-only contents permission and checkout credential persistence disabled. | Partial | [GitHub CI Workflow](../../../../.github/workflows/ci.yml), [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md), [SDLC research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md) | Static workflow review does not prove GitHub CI has run on this branch, that the latest remote run passed, or that GitHub branch/ruleset settings match the file. | Use separate GitHub check evidence for branch CI status; route workflow semantic changes to a future CI task. |
| QA validation commands | Delivery should have reproducible local commands for repo quality, generated indexes, GitOps structure, manifests, secret handling, policy, and static contracts. | The CI/CD QA guide and scripts README list local reproduction commands. Required Task 5 validation is `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .`; broader manifest/live lanes remain separate. | Partial | [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md), [Scripts README](../../../../scripts/README.md), [Audit pack task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [GitHub CI Workflow](../../../../.github/workflows/ci.yml) | This task validates the scoped docs change, not the full manifest-static bundle, live runtime, or every optional local tool. | Run broader static or live validation only when the changed scope or an approved task requires it. |
| Formatting and pre-commit | Formatting should catch whitespace, file hygiene, Markdown, shell, workflow, secret, Dockerfile, and manifest drift before commit. | `.pre-commit-config.yaml` defines commitizen, pre-commit-hooks, gitleaks, detect-secrets, markdownlint-cli2, check-jsonschema, shellcheck, shfmt, zizmor, hadolint, actionlint, and kube-linter hooks; CI runs `pre-commit/action`. | Partial | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml), [GitHub CI Workflow](../../../../.github/workflows/ci.yml), [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md), [Scripts README](../../../../scripts/README.md) | Static config evidence does not prove hooks are installed locally, that `pre-commit run --all-files` was run for this task, or that remote CI executed on this branch. | Use pre-commit evidence when the task contract requires it or before PR handoff; route hook changes to a future scoped task. |
| Static-vs-live readiness boundary | Reports and validation records must not present repo-static or CI/toolchain evidence as live runtime readiness. | Stage 00 quality standards, the CI/CD QA guide, research reference, audits README, and this report all state that static evidence does not prove live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, or secret readiness. | Implemented | [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md), [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md), [SDLC research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md), [Audits README](../README.md) | Future summaries could still overstate readiness if they collapse evidence lanes. | Keep static-vs-live caveats in task evidence, reports, guides, and final handoff. |
| Automation opportunities | Repeated SDLC, evidence-lane, CI, and audit checks should become deterministic where feasible. | Existing quality gates, generated-index checks, CI jobs, and pre-commit hooks automate broad delivery checks; audit-specific matrix coverage and external-standard mapping remain manual. | Partial | [Scripts README](../../../../scripts/README.md), [GitHub CI Workflow](../../../../.github/workflows/ci.yml), [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml), [Audit pack task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md) | No validator currently proves every SDLC audit row exists, every status value is allowed, every `Partial` rationale is present, or every external benchmark item has a local route. | Add audit/SDLC validators only through a future Spec, Plan, Task, script update, and validation record. |

### Comparison Analysis

- The repository implements a clear spec-driven delivery ladder through Stage
  03 specs, Stage 04 plans, Stage 04 task records, templates, README indexes,
  and Stage 00 routing rules.
- Repo-backed evidence is strongest for artifact routing, validation command
  inventory, local/CI lane definitions, and static-vs-live boundary language.
- CI implementation evidence is present as workflow source, but this audit did
  not inspect GitHub Actions run history. Therefore CI job rows stay bounded to
  static workflow evidence and do not claim this branch has passed remote CI.
- Secure SDLC is partially implemented as evidence lanes, secret-handling
  checks, workflow security checks, least-privilege CI defaults, and routing
  guidance. This audit does not prove full NIST SSDF coverage or live secret
  readiness.
- Formatting and pre-commit coverage is broad in configuration, but local hook
  installation, full-hook execution, and remote CI execution are separate
  evidence.
- Static repository validation remains necessary and useful, but it does not
  prove live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, or secret
  readiness.

### Automation Opportunities

- Add a future audit-matrix validator that checks required SDLC row labels,
  allowed audit status values, and evidence links for every `Implemented` and
  `Partial` row.
- Add a future README-index check that flags planned audit filenames once the
  corresponding report exists.
- Add a future Stage 03/04 traceability check that confirms each active
  implementation task links its parent spec and plan and records validation
  evidence.
- Add a future secure SDLC mapping checklist that records which NIST SSDF or
  supply-chain practices are locally implemented, partially implemented, or out
  of scope.
- Add a future CI evidence helper that records the latest GitHub run URL and
  result when a task is explicitly approved to inspect remote CI.
- Keep any automation behind a separate Spec, Plan, Task, script or workflow
  update, and validation record; this audit does not implement automation.

### Implementation Checklist

- [x] Used `docs/99.templates/templates/common/reference.template.md` as the authoring base.
- [x] Included the required reference-template sections.
- [x] Included the required audit subsections under `Definitions / Facts`.
- [x] Covered spec-driven development in the implementation matrix.
- [x] Covered Stage 03 Spec lifecycle in the implementation matrix.
- [x] Covered Stage 04 Plan lifecycle in the implementation matrix.
- [x] Covered Stage 04 Task/evidence lifecycle in the implementation matrix.
- [x] Covered SDLC and secure SDLC evidence lanes in the implementation
  matrix.
- [x] Covered CI/CD jobs in the implementation matrix.
- [x] Covered QA validation commands in the implementation matrix.
- [x] Covered formatting and pre-commit in the implementation matrix.
- [x] Covered static-vs-live readiness boundary in the implementation matrix.
- [x] Covered automation opportunities in the implementation matrix.
- [x] Used only `Implemented`, `Partial`, `Gap`, and `Not in scope` as audit
  status values.
- [x] Cited repo-backed evidence paths for every `Implemented` and `Partial`
  matrix claim.
- [x] Stated that static repository evidence does not prove GitHub CI has run
  on this branch unless separately checked.
- [x] Stated that static repository evidence does not prove live k3d, ArgoCD,
  Vault, ESO, Kubernetes, cloud, deployment, or secret readiness.
- [x] Kept the audit descriptive and bounded to repository evidence.
- [ ] Future work: automate SDLC audit row coverage, status-vocabulary review,
  and evidence-lane checks if recurring audit packs need stronger mechanical
  assurance.

### Residual Risks

- This audit is a 2026-07-02 repository snapshot. It can become stale when
  Stage 03/04 lifecycle docs, Stage 00 governance, templates, CI workflows,
  scripts, pre-commit configuration, operations guides, or research benchmarks
  change.
- Static workflow review does not prove GitHub Actions has run on this branch
  or that the latest remote run passed.
- Static repo gates and local validation evidence do not prove live k3d,
  ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret, paid-job, or
  external-service readiness.
- Secure SDLC evidence is lane-based and bounded. Full NIST SSDF mapping,
  supply-chain risk acceptance, dependency freshness, action-source review, and
  live secret readiness require separate scoped evidence.
- Audit-specific automation remains future work; current assurance combines
  manual matrix review with broad repository quality gates.

## Sources

Official and external benchmark sources, checked through the research snapshot
on 2026-07-02:

- [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- [NIST SP 800-204D news/page](https://csrc.nist.gov/News/2024/nist-publishes-sp-800204d)
- [GitHub Actions docs](https://docs.github.com/actions)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [pre-commit docs](https://pre-commit.com/)
- [GitHub Spec Kit docs](https://github.github.com/spec-kit/)
- [GitHub Spec Kit repository](https://github.com/github/spec-kit)
- [Martin Fowler, Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)

Repo-backed sources:

- [Spec SDLC CI QA Formatting Research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md)
- [Workspace Harness Implementation Audit Pack Spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- [Workspace Harness Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- [Workspace Harness Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
- [Stage 03 Specs README](../../../03.specs/README.md)
- [Stage 04 Plans README](../../../04.execution/plans/README.md)
- [Stage 04 Tasks README](../../../04.execution/tasks/README.md)
- [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation Protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../../00.agent-governance/rules/document-stage-routing.md)
- [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../../scripts/README.md)
- [GitHub CI Workflow](../../../../.github/workflows/ci.yml)
- [Pre-commit Config](../../../../.pre-commit-config.yaml)
- [Templates README](../../../99.templates/README.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-02
- Next review trigger: spec lifecycle, Stage 04 plan/task lifecycle, CI
  workflow, QA gate, formatting, pre-commit, template, validation-script, NIST
  SSDF/SP 800-204D, GitHub Actions, GitHub Spec Kit, pre-commit source,
  audit-index, or evidence-lane change.
- Refresh this report when a GitHub CI run is separately inspected for this
  branch, when live runtime evidence is approved and recorded, or when
  validation automation gains SDLC audit coverage.

## Related Documents

- **Audits README**: [README.md](../README.md)
- **Research benchmark**: [Spec SDLC CI QA Formatting Research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md)
- **Parent Spec**: [Workspace Harness Implementation Audit Pack Spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- **Parent Plan**: [Workspace Harness Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **Task record**: [Workspace Harness Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **CI/CD QA guide**: [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- **Scripts README**: [Scripts README](../../../../scripts/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
