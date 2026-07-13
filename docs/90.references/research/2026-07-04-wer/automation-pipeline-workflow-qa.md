---
title: 'Reference: Automation Pipeline Workflow QA Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---

# Reference: Automation Pipeline Workflow QA Research

## Overview

이 문서는 `hy-home.k8s`의 automation, pipeline, workflow, CI/CD, and QA
evidence loop를 repo-first reference로 정리한다. It connects current
GitHub Actions workflow files, pre-commit configuration, validation scripts,
release-evidence automation, and maintenance automation to official/primary
external sources checked for WER-007 on 2026-07-05.

This is descriptive reference material. It does not redefine active workflow
semantics, branch protection, CI enforcement, release approval, deployment
procedure, credential handling, live runtime readiness, or maintenance-bot
behavior.

### Purpose

- Provide a dated source snapshot for automation, workflow triggers,
  workflow syntax, concurrency, reusable workflow concepts, workflow commands,
  `GITHUB_TOKEN`, secrets, artifacts, dependency caching, CI feedback loops,
  and delivery metrics.
- Compare those source-backed concepts with the current repo implementation in
  `.github/`, `.pre-commit-config.yaml`, scripts, and Stage 05 operations
  guidance.
- Keep QA evidence lanes explicit: repo-static, CI/toolchain, artifact/release
  evidence, maintenance automation, market/context scan, and live runtime.
- Record implementation checklist routes for future workflow, pipeline, QA, or
  automation changes without making this reference an active gate.

## Reference Type

- Type: durable-concept / external-standard-snapshot /
  dated-implementation-audit
- Source checked: 2026-07-05 for GitHub Actions workflow syntax, events,
  concurrency, reusable workflows, workflow commands, `GITHUB_TOKEN`, secrets,
  workflow artifacts, dependency caching, workflow visualization graph,
  Martin Fowler Continuous Integration, DORA metrics, pre-commit, and
  OpenSSF Scorecard context.
- Refresh trigger: workflow, pre-commit, validation-script, release-evidence,
  maintenance automation, dependency-update automation, secret-handling,
  artifact, cache, branch-policy, CI/CD QA guide, or referenced external
  source changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed definitions and dated reference findings checked on
    2026-07-05 for WER-007.
  - Lookup-level mapping from external automation, pipeline, workflow, CI, QA,
    artifact, cache, and metric concepts to current repo-backed surfaces.
  - Descriptive implementation status for the tracked files reviewed in this
    task.
- **Not authoritative for**:
  - Active GitHub Actions semantics, branch protection, CODEOWNERS, workflow
    permissions, `GITHUB_TOKEN` policy, action pinning policy, release
    approval, deployment policy, pre-commit hook policy, validation script
    behavior, dependency-update policy, stale-item policy, or secret handling.
  - Live Kubernetes, Argo CD, Vault, ESO, cloud, provider runtime, deployment,
    endpoint, release, or secret readiness.
  - Market scan conclusions. Market/context material in this document is
    non-authoritative and cannot override official sources, repo-backed
    evidence, or canonical owners.

## Scope

- Covers GitHub Actions workflow structure, triggers, path filtering,
  concurrency, permissions, `GITHUB_TOKEN`, secrets, artifacts, dependency
  caching, reusable workflow concepts, workflow summaries, CI feedback loops,
  DORA-style metrics context, pre-commit automation, repo-local validation
  scripts, release-evidence artifacts, Dependabot, labeler, greeting, stale
  maintenance automation, and implementation routing.
- Excludes changes to `.github/workflows/*.yml`, `.github/*.yml`,
  `.pre-commit-config.yaml`, scripts, branch protection, GitHub remote
  settings, release tags, live clusters, credentials, secret values, or
  third-party systems.
- Excludes live runtime validation. Repo-static and CI/toolchain evidence do
  not prove live Kubernetes, Argo CD, Vault, ESO, cloud, endpoint, deployment,
  or secret readiness.

## Definitions / Facts

### Automation, workflow, and pipeline model

GitHub Actions defines a workflow as a configurable automated process stored as
YAML under `.github/workflows`. Workflow syntax covers events, permissions,
environment, concurrency, jobs, steps, matrices, services, reusable workflows,
and related job/step controls. Events such as `push`, `pull_request`,
`workflow_dispatch`, `schedule`, `workflow_call`, and tag pushes determine when
automation starts.

For this repository, the useful vocabulary is:

- **Automation**: any configured machine action such as CI, changelog artifact
  creation, labeling, greeting, stale-item maintenance, Dependabot updates, or
  local pre-commit hooks.
- **Workflow**: one tracked GitHub Actions YAML file under
  `.github/workflows/`.
- **Pipeline**: the ordered or conditional evidence path from trigger to jobs,
  scripts, summaries, artifacts, and task records.
- **QA gate**: an automation whose result is treated as required evidence for
  a change. In the current repo, `.github/workflows/ci.yml` is the required
  remote QA gate described by `.github/ABOUT.md`.
- **Maintenance automation**: automation that helps repository hygiene or
  triage but is not a QA gate.

### Current repo workflow graph

The current tracked workflow set has clear role separation:

| Surface | Current role | Trigger / scope | Evidence produced | Boundary |
| --- | --- | --- | --- | --- |
| `.github/workflows/ci.yml` | Required QA gate | `push` to `main`, `pull_request` to `main`, and `workflow_dispatch` | Branch policy output, path-filter outputs, pre-commit verdict, repo-quality verdict, manifest-static verdict, and `ci-summary` aggregation | No deploy CD, live Kubernetes mutation, Vault mutation, container publish, commit push, or external mutation. |
| `.github/workflows/generate-changelog.yml` | Release-evidence artifact generator | `push` tag matching `v*.*.*` | Uploaded `CHANGELOG.md` artifact and `$GITHUB_STEP_SUMMARY` notes | Does not commit, push, publish, or mutate release history. |
| `.github/workflows/labeler.yml` | Repository maintenance labeling | Pull request opened or synchronized | Path labels through `actions/labeler` | Not a QA gate and not a CODEOWNERS or human-review replacement. |
| `.github/workflows/greetings.yml` | Repository maintenance greeting | First issue or pull request opened | Intake comment | Not a QA gate, approval, or deployment automation. |
| `.github/workflows/stale.yml` | Repository maintenance cleanup | Scheduled issue/PR maintenance | Stale labels and closure comments according to workflow config | Not release evidence, QA evidence, or deployment automation. |
| `.github/dependabot.yml` | Dependency-update automation | Weekly GitHub Actions ecosystem scan | Dependabot PRs with dependency labels/grouping/cooldown | Proposes changes; does not itself prove runtime safety. |
| `.pre-commit-config.yaml` | Local and CI toolchain hook matrix | Local hook runs and `pre-commit/action` in CI | Formatting, linting, security, workflow, shell, Dockerfile, and manifest hook results | Toolchain evidence only; hook availability can vary by environment. |

The `ci.yml` job graph is:

1. `branch-policy` runs only for pull requests and checks PR base/source branch
   shape.
2. `changes` checks out the repository with `persist-credentials: false` and
   uses `dorny/paths-filter` to select evidence lanes.
3. `pre-commit` runs the configured hook matrix when any path changes.
4. `repo-quality-static` runs `bash scripts/validate-repo-quality-gates.sh .`
   for documentation, governance, template, script, workflow, adapter, archive,
   and repository contract checks.
5. `manifest-static` runs infrastructure static contracts, GitOps structure,
   manifest syntax, secret handling, and policy gates for manifest-related
   paths.
6. `ci-summary` aggregates required job results and fails when any required
   lane fails or is cancelled.

This graph is the current implementation snapshot, not a permanent workflow
contract. Active changes belong in the workflow file, operations guide, and the
owning task evidence.

### Permissions, secrets, and token boundary

GitHub Actions workflow syntax supports workflow-level and job-level
`permissions` for `GITHUB_TOKEN`. GitHub's `GITHUB_TOKEN` documentation treats
the token as workflow-scoped automation authentication, while its secure-use
and secrets docs require careful handling of secret data and untrusted inputs.

Current repo mapping:

- `ci.yml` and `generate-changelog.yml` set workflow-level
  `permissions: contents: read`.
- `labeler.yml`, `greetings.yml`, and `stale.yml` use job-level write
  permissions only for their maintenance role.
- `actions/checkout` in `ci.yml` and `generate-changelog.yml` sets
  `persist-credentials: false`, so checkout credentials are not retained for
  later steps by default.
- `labeler.yml` and the maintenance workflows consume `secrets.GITHUB_TOKEN`
  for GitHub-native maintenance actions, not for deployment or publishing.
- `.github/zizmor.yml` currently disables the `unpinned-uses` rule; therefore
  action pinning policy cannot be inferred from that specific local Zizmor
  configuration. `.github/ABOUT.md` routes version inventory and action tag
  policy to `docs/90.references/data/tech-stack-version-inventory.md`.

These observations do not authorize expanding workflow permissions, printing
secrets, inspecting secret values, or mutating GitHub remote settings.

### QA evidence lanes

The automation surfaces map to separate evidence lanes:

| Evidence lane | Current examples | What the evidence can support | What it cannot prove |
| --- | --- | --- | --- |
| Repo-static | `git diff --check`, `validate-repo-quality-gates`, GitOps structure, manifest syntax, secret handling, policy gates, infrastructure static contracts | Committed-file consistency, documentation routing, static desired-state validity, and local contract alignment | Live cluster readiness, deployed state, secret availability, external service health |
| CI/toolchain | GitHub Actions `ci.yml`, `pre-commit/action`, `markdownlint-cli2`, `shellcheck`, `shfmt`, `actionlint`, `zizmor`, `hadolint`, `kube-linter`, `gitleaks`, `detect-secrets` | Remote QA verdicts and tool-backed lint/security feedback | Production deployment, credential safety beyond scanned content, artifact provenance |
| Artifact/release evidence | `generate-changelog.yml` uploaded changelog artifact and `$GITHUB_STEP_SUMMARY` | Release-review evidence for tag-related changelog preview | Publishing, committing, pushing, or releasing by itself |
| Maintenance automation | Dependabot, labeler, greetings, stale workflow | Triage, dependency-update proposal flow, repository hygiene | QA approval, CODEOWNERS approval, release readiness, runtime readiness |
| Market/context scan | DORA metrics, Fowler CI, Scorecard context | Vocabulary for feedback loops, delivery metrics, and security heuristics | Authoritative repo health or active gate status |
| Live runtime | Operator-approved checks against k3d, Argo CD, Vault, ESO, Kubernetes, cloud, endpoints, or services | Actual runtime readiness when separately approved and recorded | Inferred from repo-static or CI PASS alone |

### CI feedback and delivery metrics context

Martin Fowler's Continuous Integration article is historical context for fast
integration and automated build/test feedback. DORA's current metrics page
frames software delivery performance around deployment frequency, lead time for
changes, failed deployment recovery time, change fail rate, and deployment
rework rate.

Current repo implication:

- The repository has QA gate evidence and local task records, but no tracked
  DORA metrics instrumentation in the current WER-007 source set.
- Future metrics adoption should be scoped as a separate spec/plan/task and
  should distinguish CI duration, gate pass/fail, PR lead time, deployment
  frequency, recovery time, change fail rate, deployment rework rate, and any
  separately defined service-health signals.
- For this pack, DORA and Fowler are non-authoritative market/context inputs;
  they do not redefine this repo's active QA gate or release process.

### Artifacts, cache, and reusable workflows

GitHub Actions artifacts are used to share data from workflow runs, and
dependency caching can speed up repeated dependency installation when configured
with appropriate keys and restore behavior. GitHub also supports reusable
workflows through `workflow_call`.

Current repo mapping:

- `generate-changelog.yml` uses `actions/upload-artifact` to publish the
  generated `CHANGELOG.md` as review evidence for the workflow run.
- `ci.yml` does not currently upload QA artifacts or configure dependency
  caching in the checked workflow.
- No tracked workflow currently exposes `workflow_call` or consumes a reusable
  workflow.
- A future artifact, cache, or reusable-workflow adoption should route through
  `.github/workflows/*.yml`, the CI/CD QA guide, and Stage 04 task evidence.

### Non-authoritative market scan

The following findings are non-authoritative market/context material:

- CI/CD practice commonly values short feedback loops, reproducible gates,
  least-privilege automation, clear job graph visualization, dependency update
  hygiene, and evidence attached close to the change.
- DORA metrics are useful for measuring delivery performance, but they require
  instrumentation and operational definitions before they can become local
  management evidence.
- OpenSSF Scorecard can provide security-risk heuristics for a repository, but
  this reference treats Scorecard as context only unless a future task promotes
  it to an active gate.
- Reusable workflows and dependency caching can reduce duplication and latency,
  but adopting them changes CI/toolchain behavior and must be handled by an
  owner-scoped task.

### Implementation checklist

- Route QA gate, path-filter, branch-policy, workflow-permission,
  `GITHUB_TOKEN`, checkout credential, artifact, cache, reusable workflow, or
  job-graph changes to
  [.github/workflows/ci.yml](../../../../.github/workflows/ci.yml),
  [.github/ABOUT.md](../../../../.github/ABOUT.md), and the
  [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md).
- Route release-evidence artifact changes to
  [.github/workflows/generate-changelog.yml](../../../../.github/workflows/generate-changelog.yml),
  `cliff.toml`, and the owning release task evidence.
- Route maintenance automation changes to the specific workflow or config:
  `labeler.yml`, `greetings.yml`, `stale.yml`, `.github/dependabot.yml`,
  `.github/labeler.yml`, and `.github/zizmor.yml`.
- Route pre-commit hook scope, versions, formatting, linting, or secret-scan
  changes to
  [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml),
  [.editorconfig](../../../../.editorconfig),
  [scripts/README.md](../../../../scripts/README.md), and the CI/CD QA guide.
- Route validation-script behavior changes to `scripts/**`,
  `infrastructure/tests/**`, `policy/**`, and matching Stage 04 task evidence.
- Route DORA, CI duration, lead-time, change-failure, recovery-time,
  deployment-rework, artifact provenance, Scorecard, CodeQL/code scanning,
  Dependency Review, SLSA adoption, or separately defined service-health
  metrics to a new scoped spec/plan/task before changing workflow behavior.
- Keep repo-static, CI/toolchain, artifact/release, maintenance,
  market/context, and live-runtime evidence lanes separate in task records.
- Do not encode active policy or runbook procedure in this Stage 90 reference.

## Sources

Official and primary external sources checked on 2026-07-05:

- GitHub Actions workflow syntax:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub Actions events that trigger workflows:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows>
- GitHub Actions concurrency:
  <https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency>
- GitHub Actions reusable workflows:
  <https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows>
- GitHub Actions workflow commands:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands>
- GitHub Actions `GITHUB_TOKEN`:
  <https://docs.github.com/en/actions/tutorials/authenticate-with-github_token>
- GitHub Actions secrets:
  <https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets>
- GitHub Actions workflow artifacts:
  <https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts>
- GitHub Actions dependency caching:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching>
- GitHub Actions visualization graph:
  <https://docs.github.com/en/actions/how-tos/monitor-workflows/use-the-visualization-graph>
- GitHub Actions secure use:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- Martin Fowler, Continuous Integration:
  <https://martinfowler.com/articles/continuousIntegration.html>
- DORA metrics:
  <https://dora.dev/guides/dora-metrics/>
- pre-commit:
  <https://pre-commit.com/>
- OpenSSF Scorecard:
  <https://scorecard.dev/>

Repo-backed sources:

- [GitHub Configuration Hub](../../../../.github/ABOUT.md)
- [GitHub CI Workflow](../../../../.github/workflows/ci.yml)
- [Generate Changelog Workflow](../../../../.github/workflows/generate-changelog.yml)
- [Labeler Workflow](../../../../.github/workflows/labeler.yml)
- [Greeting Workflow](../../../../.github/workflows/greetings.yml)
- [Stale Workflow](../../../../.github/workflows/stale.yml)
- [Dependabot Config](../../../../.github/dependabot.yml)
- [Zizmor Config](../../../../.github/zizmor.yml)
- [Pre-commit Config](../../../../.pre-commit-config.yaml)
- [Scripts README](../../../../scripts/README.md)
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
- [Spec SDLC CI QA Formatting Research](spec-sdlc-ci-qa-formatting.md)
- [Kubernetes Infrastructure Security Research](kubernetes-infrastructure-security.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-05
- Next review trigger: GitHub Actions workflow, workflow event, concurrency,
  reusable-workflow, workflow-command, `GITHUB_TOKEN`, secret, artifact,
  cache, secure-use, pre-commit, DORA, Scorecard, script, CI/CD QA guide,
  release-evidence, maintenance automation, or validation evidence change.

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **Parent references README**: [90.references README](../../README.md)
- **Workspace baseline**: [Workspace Governance Baseline Research](workspace-governance-baseline.md)
- **Spec/SDLC/CI/QA reference**: [Spec SDLC CI QA Formatting Research](spec-sdlc-ci-qa-formatting.md)
- **Kubernetes/infrastructure/security reference**: [Kubernetes Infrastructure Security Research](kubernetes-infrastructure-security.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Task**: [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **CI/CD QA guide**: [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- **Scripts README**: [Scripts README](../../../../scripts/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
