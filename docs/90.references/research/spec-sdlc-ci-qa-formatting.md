---
title: 'Reference: Spec SDLC CI QA Formatting Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-02
---

# Reference: Spec SDLC CI QA Formatting Research

## Overview

이 문서는 spec-driven development, SDLC/secure SDLC, CI/CD, QA evidence,
formatting, and pre-commit practice를 durable reference로 정리한다. It maps
official and repo-backed sources checked on 2026-07-02 back to the local
`hy-home.k8s` Stage 03/04 lifecycle, CI jobs, validation scripts, and
formatting gates.

This is descriptive reference material. It does not redefine active governance,
CI semantics, release approval, live runtime procedure, or provider behavior.

## Purpose

- Provide a dated source snapshot for spec, SDLC, CI, QA, and formatting terms.
- Compare GitHub Spec Kit's SDD artifact flow with this repository's existing
  Stage 03/04 lifecycle without recommending installation.
- Connect NIST secure SDLC and software supply-chain guidance to this repo's
  existing evidence lanes and boundary checks.
- Preserve a repo-local validation matrix that future specs, plans, tasks, and
  references can cite without turning this document into policy.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-02
- Refresh trigger: spec lifecycle, CI workflow, QA gate, formatting,
  pre-commit, template, or validation-script changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed definitions and dated reference findings checked on
    2026-07-02.
  - Lookup-level mapping from external SDD, SDLC, CI, QA, and formatting
    concepts to current repo-backed evidence surfaces.
  - Checklist-level follow-up routing to canonical repository owners.
- **Not authoritative for**:
  - Active governance rules, CI workflow semantics, branch policy, release
    approval, pre-commit hook policy, template requirements, or validation
    script behavior.
  - GitHub Spec Kit installation, adoption, migration, or workflow replacement.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, or secret readiness.
  - Market scan conclusions. Market findings in this document are
    non-authoritative and cannot override official sources or repo-backed
    contracts.

## Scope

- Covers spec-driven development, SDLC and secure SDLC, CI/CD, QA evidence
  lanes, formatting and pre-commit, repo-local validation commands,
  non-authoritative market scan findings, and implementation checklist routes.
- Excludes changes to Stage 00 governance, Stage 03/04 templates, GitHub
  Actions workflow jobs, pre-commit configuration, scripts, manifests, secrets,
  provider adapters, or live operations.
- Excludes live runtime validation. Repo-static validation does not prove live
  k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, or secret readiness.

## Definitions / Facts

### Spec-driven development

GitHub Spec Kit frames spec-driven development as putting specifications at the
center of AI-assisted delivery. Its public docs describe a default flow of
`Spec -> Plan -> Tasks -> Implement`, with each Markdown artifact feeding the
next phase. The Spec Kit repository exposes related commands such as
`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and
`/speckit.implement`.

This repository already has a similar artifact ladder, but it is implemented
through the canonical docs taxonomy rather than through Spec Kit installation:

| Concept | GitHub Spec Kit flow | `hy-home.k8s` repo lifecycle |
| --- | --- | --- |
| Define intent | Spec artifact describes what to build and why. | Stage 03 `docs/03.specs/<feature-id>/spec.md` owns implementation contract after upstream requirements and architecture inputs. |
| Plan implementation | Plan artifact captures technical approach and constraints. | Stage 04 `docs/04.execution/plans/*.md` owns execution order, risks, gates, rollback, and verification. |
| Break down work | Tasks artifact generates actionable units. | Stage 04 `docs/04.execution/tasks/*.md` owns task table, phase view, status, validation evidence, and handoff. |
| Implement | Agent executes tasks against spec/plan/task context. | Agents edit only approved write scope, follow repo templates and governance, run validation, and record evidence before commit/handoff. |

The useful reference pattern is artifact traceability: intent, plan, tasks,
implementation, and validation should stay linked. This document does not
recommend installing Spec Kit, replacing current templates, or changing the
Stage 03/04 lifecycle.

### SDLC and secure SDLC

NIST SP 800-218 defines the Secure Software Development Framework (SSDF) as a
core set of high-level secure software development practices that can be
integrated into each SDLC implementation. Its stated goal is to reduce released
software vulnerabilities, limit exploitation impact, and provide a common
secure-development vocabulary.

NIST SP 800-204D applies software supply-chain security to cloud-native
DevSecOps CI/CD pipelines. The NIST news page describes CI/CD pipeline
strategies that integrate software supply-chain assurance and map those
strategies to SSDF high-level practices.

Local repo implications:

- **Evidence lanes**: secure SDLC claims should name whether evidence is
  repo-static, CI/toolchain, or live runtime. These lanes are separate in the
  quality standards and CI/CD QA guide.
- **Validation**: repo-static gates such as repository quality, GitOps
  structure, manifest syntax, policy gates, secret handling, and infrastructure
  static contracts are evidence of committed desired-state consistency, not live
  deployment readiness.
- **Secrets**: SSDF and supply-chain boundaries map locally to no plaintext
  secrets in manifests, no secret values in docs, least-privilege Vault policy
  checks, GitHub Actions secret handling, and human approval for credential
  changes.
- **Supply chain**: action pinning/review, read-only `GITHUB_TOKEN` defaults,
  dependency update review, pre-commit hook provenance, and script inventory
  review are supply-chain concerns. Actual policy changes belong to canonical
  owners, not this reference.

### CI/CD

Martin Fowler's CI article describes continuous integration as frequent
integration into a shared codebase, verified by automated build and test so
integration errors surface quickly. GitHub Actions provides workflow, job,
runner, secret, deployment, concurrency, and monitoring primitives for CI/CD
automation. GitHub's secure-use reference emphasizes least privilege, careful
secret handling, dependency upkeep, and action-source review.

Current repo mapping:

- `.github/workflows/ci.yml` owns the active GitHub Actions job graph.
- `branch-policy` runs only for pull requests and checks PR base branch plus
  source branch prefix.
- `changes` uses path filtering to decide which validation lanes need to run.
- `pre-commit` runs the configured hook matrix across changed surfaces.
- `repo-quality-static` runs `bash scripts/validate-repo-quality-gates.sh .`
  for docs, governance, scripts, adapters, workflow, and related surfaces.
- `manifest-static` runs infrastructure static contracts, GitOps structure,
  manifest syntax, secret handling, and policy gates for manifest/infrastructure
  surfaces.
- `ci-summary` aggregates required job results and fails the workflow when a
  required lane fails or is cancelled.

These jobs are the current CI implementation. This reference only describes
them; workflow semantics change in `.github/workflows/ci.yml` and the CI/CD QA
guide.

### QA and validation evidence

QA evidence is not one bucket. This repository separates it into three lanes:

- **Repo-static evidence**: deterministic checks against committed files,
  documentation structure, templates, scripts, manifests, generated indexes,
  and static infrastructure contracts. Examples include `git diff --check`,
  `validate-repo-quality-gates`, GitOps structure checks, manifest syntax,
  policy gates, and secret handling scans.
- **CI/toolchain evidence**: GitHub Actions jobs and local tools such as
  `pre-commit`, `markdownlint-cli2`, `shellcheck`, `shfmt`, `actionlint`,
  `kube-linter`, `gitleaks`, `detect-secrets`, and optional tool-backed
  validators.
- **Live runtime evidence**: separately approved and recorded checks against
  k3d, ArgoCD, Vault, ESO, Kubernetes, deployments, cloud resources, external
  services, or real secret readiness.

Repo-static and CI/toolchain PASS results are necessary documentation and
desired-state evidence. They do not prove live k3d, ArgoCD, Vault, ESO,
Kubernetes, deployment, or secret readiness. Live runtime evidence must come
from an approved live check or operator-owned runbook result.

### Formatting and pre-commit

pre-commit is a framework for managing and maintaining multi-language
pre-commit hooks. The local `.pre-commit-config.yaml` uses it for commit-message
checks, file hygiene, secret scanning, Markdown linting, dependency-file
validation, shell formatting, GitHub Actions linting, Dockerfile linting, and
Kubernetes manifest linting.

Current local mapping:

- **Docs formatting**: `markdownlint-cli2`, `trailing-whitespace`,
  `end-of-file-fixer`, `mixed-line-ending`, and `git diff --check` catch common
  Markdown and whitespace drift.
- **Scripts formatting**: `shellcheck` and `shfmt` apply to shell scripts under
  `scripts/`, `infrastructure/`, and Stage 00 hook scripts.
- **Workflow formatting/security**: `actionlint` and `zizmor` inspect GitHub
  Actions workflow structure and security patterns.
- **Manifest formatting/validation**: `check-yaml` excludes Kubernetes-like
  manifest paths where the repo's manifest validators and optional
  `kube-linter` lane are better suited.
- **Secret hygiene**: `gitleaks`, `detect-secrets`, and
  `check-secret-handling.sh` are complementary. They do not authorize reading,
  writing, or publishing secret values.

The active hook list and versions live in `.pre-commit-config.yaml`. Changing
hook scope, versions, or enforcement belongs there plus the CI/CD QA guide and
task evidence.

### Repo-local validation matrix

| Evidence lane | Command or gate | Current purpose | Boundary |
| --- | --- | --- | --- |
| Whitespace/diff hygiene | `git diff --check` | Detect whitespace errors in the pending diff. | Repo-static only. |
| Generated reference index | `bash scripts/generate-llm-wiki-index.sh --check` | Verify the generated LLM Wiki index matches generator output. | Repo-static generated-artifact freshness only. |
| Repository quality | `bash scripts/validate-repo-quality-gates.sh .` | Validate docs taxonomy, README contracts, template coverage, workflow/script references, archive currentness, and repository governance checks. | Repo-static only; does not prove CI or live runtime health. |
| GitOps structure | `bash scripts/validate-gitops-structure.sh` | Validate ArgoCD root app, kustomization structure, and resource reference completeness. | Desired-state structure only. |
| Kubernetes manifests | `bash scripts/validate-k8s-manifests.sh .` | Validate YAML syntax and optional kube-linter checks for manifest paths. | Manifest syntax/tooling only. |
| Secret handling | `bash scripts/check-secret-handling.sh .` | Scan GitOps, infrastructure, and example manifests for plaintext secret patterns. | Static scan only; does not prove Vault/ESO readiness. |
| Policy gates | `bash scripts/validate-policy-gates.sh .` | Run Conftest/Rego when available and built-in fallback checks for plaintext Secret, `CreateNamespace=true`, AppProject wildcard, and `latest` image patterns. | Static policy evidence only. |
| Infrastructure static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | Check static contract expectations for root app, external services, ingress, Vault policy, AppProject allow-lists, notifications, network policy, and sample ExternalSecret surfaces. | Static contract evidence only. |
| pre-commit hook matrix | `pre-commit run --all-files` | Run configured file hygiene, lint, security, workflow, script, Dockerfile, and manifest hooks. | Local/CI toolchain evidence; hook availability may vary by environment. |

### Non-authoritative market scan

The following findings are non-authoritative market scan material. They provide
context only and must not override official documentation, repo-backed
contracts, or canonical repository owners.

- Spec Kit ecosystem material signals a broader AI-coding pattern: turn vague
  prompts into explicit spec, plan, task, and implementation artifacts with
  validation checkpoints. The local repository already has equivalent Stage
  03/04 artifacts, so any adoption question should be a separate proposal.
- The Spec Kit repository exposes community extensions, presets, bundles, and
  integrations. Those are ecosystem signals, not trusted local dependencies.
  Review source, scope, and install behavior before any future experiment.
- CI/QA industry practice continues to emphasize fast feedback, small
  integrations, least-privilege automation, dependency upkeep, secret hygiene,
  and evidence captured close to the change. In this repo, the canonical
  evidence locations remain Stage 04 task records, CI jobs, scripts, and
  relevant operations guides.

### Implementation checklist

- Route spec lifecycle changes to
  [Stage 03 specs](../../03.specs/009-workspace-harness-research-pack/spec.md),
  [Stage 04 plans](../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md),
  and [Stage 04 tasks](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md).
- Route template or document-structure changes to
  [Templates README](../../99.templates/README.md),
  [reference.template.md](../../99.templates/templates/common/reference.template.md),
  [document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md),
  and `scripts/validate-repo-quality-gates.sh`.
- Route CI job or branch-policy changes to
  [.github/workflows/ci.yml](../../../.github/workflows/ci.yml) and the
  [CI/CD QA guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md).
- Route pre-commit hook, formatting, or lint-scope changes to
  [.pre-commit-config.yaml](../../../.pre-commit-config.yaml),
  [scripts/README.md](../../../scripts/README.md), and the CI/CD QA guide.
- Route validation-script changes to `scripts/**`, `scripts/README.md`, CI
  workflow path filters, and the relevant Stage 04 task evidence.
- Route manifest, policy, secret-handling, or infrastructure static-contract
  changes to the matching `gitops/`, `infrastructure/`, `policy/`, and script
  owners, with explicit static-vs-live evidence language.
- Route secure SDLC or approval-boundary changes to Stage 00 governance and
  operations policy/runbook owners; do not encode active policy in this
  reference.
- Update [Research README](./README.md) and task evidence when this reference
  changes status, scope, sources, or validation results.
- Record durable progress/memory only when the active task write scope includes
  `docs/00.agent-governance/memory/progress.md`.
- Before handoff for this reference, run `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .`; record PASS/FAIL and
  limitations in the task record.

## Sources

Official and primary external sources, checked 2026-07-02:

- NIST SSDF SP 800-218:
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- NIST SP 800-204D news/page:
  <https://csrc.nist.gov/News/2024/nist-publishes-sp-800204d>
- GitHub Actions docs:
  <https://docs.github.com/actions>
- GitHub Actions secure use:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- pre-commit docs:
  <https://pre-commit.com/>
- GitHub Spec Kit docs:
  <https://github.github.com/spec-kit/>
- GitHub Spec Kit repository:
  <https://github.com/github/spec-kit>
- Martin Fowler, Continuous Integration:
  <https://martinfowler.com/articles/continuousIntegration.html>

Repo-backed sources:

- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Agent Quality Standards](../../00.agent-governance/rules/quality-standards.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Templates README](../../99.templates/README.md)
- [Scripts README](../../../scripts/README.md)
- [GitHub CI Workflow](../../../.github/workflows/ci.yml)
- [Pre-commit Config](../../../.pre-commit-config.yaml)
- [Workspace Governance Baseline Research](./workspace-governance-baseline.md)
- [Infrastructure Static Contract Verification](../../../infrastructure/tests/verify-contracts-static.sh)

Non-authoritative market scan source, checked 2026-07-02:

- GitHub Blog, Spec-driven development with AI:
  <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-02
- Next review trigger: spec lifecycle, CI workflow, QA gate, formatting,
  pre-commit, template, validation-script, NIST SSDF/SP 800-204D,
  GitHub Actions, GitHub Spec Kit, or pre-commit source changes.

## Related Documents

- **Parent research README**: [README.md](./README.md)
- **Parent references README**: [90.references README](../README.md)
- **Workspace baseline**: [Workspace Governance Baseline Research](./workspace-governance-baseline.md)
- **Harness/loop reference**: [Harness and Loop Engineering Research](./harness-and-loop-engineering.md)
- **Provider status**: [Provider Harness Implementation Status Research](./provider-implementation-status.md)
- **Spec**: [Workspace Harness Research Pack Spec](../../03.specs/009-workspace-harness-research-pack/spec.md)
- **Plan**: [Workspace Harness Research Pack Plan](../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md)
- **Task**: [Workspace Harness Research Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md)
- **CI/CD QA guide**: [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- **Scripts README**: [Scripts README](../../../scripts/README.md)
- **Templates README**: [Templates README](../../99.templates/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
