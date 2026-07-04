---
title: 'Reference: Spec SDLC CI QA Formatting Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---

# Reference: Spec SDLC CI QA Formatting Research

## Overview

이 문서는 spec-driven development, SDLC/secure SDLC, CI/CD, QA evidence,
formatting, and pre-commit practice를 durable reference로 정리한다. It maps
official and repo-backed sources to the local `hy-home.k8s` Stage 03/04
lifecycle, GitHub Actions jobs, validation scripts, formatting gates, and
security/supply-chain evidence routes. WER-005 refreshed the official and
primary sources on 2026-07-05. Older 2026-07-04 CI/formatting and 2026-07-02
SDLC/supply-chain history is preserved where it explains why this reference
exists.

This is descriptive reference material. It does not redefine active governance,
CI semantics, release approval, live runtime procedure, or provider behavior.

## Purpose

- Provide a dated source snapshot for spec, SDLC, CI, QA, formatting,
  security, and supply-chain terms.
- Compare GitHub Spec Kit's SDD artifact flow with this repository's existing
  Stage 03/04 lifecycle without recommending installation.
- Connect NIST SSDF, NIST SP 800-204D, GitHub Actions security, GitHub CodeQL
  code scanning, Dependency Review, SLSA, and OpenSSF Scorecard concepts to
  this repo's existing evidence lanes and boundary checks.
- Preserve a repo-local validation matrix that future specs, plans, tasks, and
  references can cite without turning this document into policy.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-05 for WER-005 refreshed sources: GitHub Actions
  workflow syntax, GitHub Actions secure use, GitHub Code scanning/CodeQL
  concepts, GitHub Dependency Review, GitHub Spec Kit, NIST SSDF SP 800-218,
  NIST SP 800-204D, SLSA spec v1.1, OpenSSF Scorecard, Prettier, EditorConfig,
  CommonMark 0.31.2, YAML 1.2.2, markdownlint, and pre-commit.
- Historical source notes: 2026-07-04 CI/formatting refresh and 2026-07-02
  broader SDLC/supply-chain research remain part of this reference history.
- Refresh trigger: spec lifecycle, CI workflow, QA gate, formatting,
  pre-commit, template, validation-script, security-gate, dependency-review,
  code-scanning, provenance/attestation, or supply-chain source changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed definitions and dated reference findings checked on
    2026-07-05 for WER-005 refreshed official/primary sources.
  - Lookup-level mapping from external SDD, SDLC, CI, QA, formatting,
    security, and supply-chain concepts to current repo-backed evidence
    surfaces.
  - Checklist-level follow-up routing to canonical repository owners.
- **Not authoritative for**:
  - Active governance rules, CI workflow semantics, branch policy, release
    approval, pre-commit hook policy, template requirements, validation script
    behavior, code-scanning policy, dependency-review policy, SLSA
    attestation/provenance policy, or OpenSSF Scorecard enforcement.
  - GitHub Spec Kit installation, adoption, migration, or workflow replacement.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, or secret readiness.
  - Market scan conclusions. Market findings in this document are
    non-authoritative and cannot override official sources or repo-backed
    contracts.

## Scope

- Covers spec-driven development, SDLC and secure SDLC, CI/CD, GitHub Actions
  secure-use concepts, QA evidence lanes, CodeQL/code scanning, Dependency
  Review, SLSA provenance/attestation, OpenSSF Scorecard context, formatting
  and pre-commit, repo-local validation commands, non-authoritative market scan
  findings, and implementation checklist routes.
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
integrated into each SDLC implementation. The SSDF practice groups provide a
common vocabulary for preparing the organization, protecting software,
producing well-secured software, and responding to vulnerabilities.

NIST SP 800-204D applies software supply-chain security to cloud-native
DevSecOps CI/CD pipelines. The final NIST publication frames CI/CD pipelines as
part of the software supply chain and outlines strategies for integrating
software supply-chain security measures into those pipelines.

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
  dependency update review, code scanning, SLSA provenance/attestation,
  OpenSSF Scorecard context, pre-commit hook provenance, and script inventory
  review are supply-chain concerns. Actual policy changes belong to canonical
  owners, not this reference.

### CI/CD

Martin Fowler's CI article remains historical context for frequent integration
and automated build/test feedback. GitHub Actions is the active local CI
platform. Its workflow syntax defines workflow, job, runner, permission,
secret, deployment, concurrency, and monitoring primitives for automation.
GitHub's secure-use reference emphasizes least privilege, careful secret
handling, dependency upkeep, untrusted-code boundaries, and action-source
review.

Current repo mapping:

- `.github/workflows/ci.yml` owns the active GitHub Actions job graph.
- The workflow-level `permissions: contents: read` setting is repo-static
  evidence of a least-privilege `GITHUB_TOKEN` baseline for the current CI
  workflow. Future jobs that need broader permissions must request them in the
  workflow and record evidence in the owning task.
- `actions/checkout` uses `persist-credentials: false` in the current CI jobs,
  keeping checkout credentials out of later steps unless a future owner changes
  that behavior explicitly.
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

### Security and supply-chain findings

The WER-005 source refresh adds these source-backed findings. They are
descriptive reference material, not active policy changes.

- **Least privilege workflow permissions**: GitHub Actions workflow syntax
  supports workflow-level and job-level `permissions` for `GITHUB_TOKEN`.
  GitHub secure-use guidance recommends granting minimum required permissions.
  The current `ci.yml` workflow sets `contents: read` at the workflow level;
  this document does not change workflow permissions.
- **Secrets boundary**: GitHub secure-use guidance treats automatic redaction as
  useful but not a complete guarantee. Locally, secret handling remains split
  across no plaintext secret values in docs/manifests, static secret scans,
  GitHub Actions secret handling, and separately approved live/operator secret
  checks. This reference does not authorize reading or printing secret values.
- **Code scanning and CodeQL**: GitHub code scanning can use CodeQL or
  third-party SARIF-producing tools to surface alerts. CodeQL is GitHub's code
  analysis engine for automated security checks. The current CI workflow does
  not configure CodeQL, code scanning, or SARIF upload; adding it would be a
  CI/toolchain change owned by `.github/workflows/ci.yml`, security review, and
  task evidence.
- **Dependency Review**: GitHub Dependency Review provides pull-request
  visibility into dependency changes and known vulnerabilities, and the
  dependency-review action can enforce checks in GitHub Actions. The current CI
  workflow does not run dependency-review-action; the current pre-commit matrix
  validates Dependabot config but is not a Dependency Review replacement.
- **SLSA provenance/attestation**: SLSA spec v1.1 describes levels for
  improving supply-chain security and includes recommended attestation formats,
  including provenance. The current CI workflow does not build or publish
  artifacts and does not emit SLSA provenance/attestation. Future build,
  container, chart, or release pipelines should route provenance decisions to
  the owning spec/plan/workflow and keep repo-static evidence separate from
  artifact attestation evidence.
- **OpenSSF Scorecard context**: Scorecard assesses open source projects for
  security risks through automated checks. It can inform a market/context scan
  or future CI proposal, but this reference treats Scorecard findings as
  non-authoritative context unless a separate task makes it an active gate.

### QA and validation evidence

QA evidence is not one bucket. This repository separates it into three lanes:

- **Repo-static evidence**: deterministic checks against committed files,
  documentation structure, templates, scripts, manifests, generated indexes,
  and static infrastructure contracts. Examples include `git diff --check`,
  `validate-repo-quality-gates`, GitOps structure checks, manifest syntax,
  policy gates, and secret handling scans.
- **CI/toolchain evidence**: GitHub Actions jobs and local tools such as
  `pre-commit`, `markdownlint-cli2`, `shellcheck`, `shfmt`, `actionlint`,
  `kube-linter`, `gitleaks`, `detect-secrets`, CodeQL/code scanning,
  Dependency Review, SLSA attestation/provenance tooling, OpenSSF Scorecard,
  and optional tool-backed validators.
- **Live runtime evidence**: separately approved and recorded checks against
  k3d, ArgoCD, Vault, ESO, Kubernetes, deployments, cloud resources, external
  services, or real secret readiness.

Repo-static and CI/toolchain PASS results are necessary documentation and
desired-state evidence. They do not prove live k3d, ArgoCD, Vault, ESO,
Kubernetes, deployment, or secret readiness. Live runtime evidence must come
from an approved live check or operator-owned runbook result.

### Formatting, linting, and pre-commit

Prettier describes itself as an opinionated code formatter with broad language
support and few options. EditorConfig defines a file format and editor plugin
ecosystem for consistent editor-level coding styles. CommonMark 0.31.2 is the
checked Markdown syntax specification, YAML 1.2.2 is the checked YAML
specification, markdownlint is a Markdown/CommonMark style checker, and
pre-commit is a multi-language hook manager.

The current local configuration uses EditorConfig and pre-commit, not Prettier:

- `.editorconfig` sets UTF-8, LF line endings, final newline insertion, spaces,
  two-space default indentation, four-space Python indentation, and Markdown
  trailing-whitespace tolerance.
- `.pre-commit-config.yaml` manages commit-message checks, file hygiene,
  secret scanning, Markdown linting, dependency-file validation, shell
  formatting, GitHub Actions linting, Dockerfile linting, and Kubernetes
  manifest linting.
- No tracked Prettier config or Prettier hook is active in the checked local
  files. A future Prettier adoption would be a formatting/toolchain proposal,
  not an implication of this reference.

Current local mapping:

- **Docs formatting**: `markdownlint-cli2`, `trailing-whitespace`,
  `end-of-file-fixer`, `mixed-line-ending`, and `git diff --check` catch common
  Markdown/CommonMark and whitespace drift.
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

The active hook list and versions live in `.pre-commit-config.yaml`. Active
formatting/editor defaults live in `.editorconfig`. Changing hook scope,
versions, Prettier adoption, EditorConfig defaults, or enforcement belongs
there plus the CI/CD QA guide and task evidence.

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
| GitHub Actions secure-use review | Workflow/source review plus security linters such as `zizmor` and `actionlint` | Review least privilege permissions, untrusted input boundaries, action source, and secret handling. | CI/toolchain evidence; not live runtime or credential readiness. |
| CodeQL/code scanning | Future `github/codeql-action` or SARIF upload workflow if adopted | Surface code scanning alerts for supported languages or third-party SARIF tools. | Not currently active in `ci.yml`; future CI/toolchain evidence only. |
| Dependency Review | Future `actions/dependency-review-action` workflow if adopted | Review dependency manifest or lockfile changes and known vulnerabilities in PRs. | Not currently active in `ci.yml`; future CI/toolchain evidence only. |
| SLSA provenance/attestation | Future build/release attestation tooling if adopted | Record verifiable build provenance for published artifacts. | Not currently active; artifact/build evidence, not repo-static evidence. |
| OpenSSF Scorecard | Future scorecard scan if adopted | Produce automated security-risk heuristic results for repository context. | Non-authoritative context unless a future task promotes it to an active gate. |

### Non-authoritative market scan

The following findings are non-authoritative market scan material. They provide
context only and must not override official documentation, repo-backed
contracts, or canonical repository owners.

- Spec Kit ecosystem material signals a broader AI-coding pattern: turn vague
  prompts into explicit spec, plan, task, and implementation artifacts with
  validation checkpoints. The local repository already has equivalent Stage
  03/04 artifacts, so any adoption question should be a separate proposal.
- GitHub Actions security practice, Dependency Review, CodeQL/code scanning,
  SLSA provenance/attestation, and OpenSSF Scorecard reflect common
  supply-chain topics in current CI/QA discussions. In this repo, they remain
  reference findings until an owning task changes `.github/workflows/ci.yml`,
  scripts, templates, or operations guidance.
- OpenSSF Scorecard is useful as a market/context scan because it summarizes
  automated security heuristics. Its score is not an authoritative repo health
  verdict here unless future governance makes it a required gate.
- CI/QA industry practice continues to emphasize fast feedback, small
  integrations, least-privilege automation, dependency upkeep, secret hygiene,
  provenance where artifacts are published, and evidence captured close to the
  change. In this repo, the canonical evidence locations remain Stage 04 task
  records, CI jobs, scripts, and relevant operations guides.

### Implementation checklist

- Route spec lifecycle changes to
  [Stage 03 specs](../../../03.specs/017-workspace-engineering-research-pack/spec.md),
  [Stage 04 plans](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md),
  and [Stage 04 tasks](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md).
- Route template or document-structure changes to
  [Templates README](../../../99.templates/README.md),
  [reference.template.md](../../../99.templates/templates/common/reference.template.md),
  [document-stage-routing.md](../../../00.agent-governance/rules/document-stage-routing.md),
  and `scripts/validate-repo-quality-gates.sh`.
- Route GitHub Actions CI job, branch-policy, workflow-permission, checkout
  credential, or secret-handling changes to
  [.github/workflows/ci.yml](../../../../.github/workflows/ci.yml) and the
  [CI/CD QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md).
- Route CodeQL/code scanning, Dependency Review, SLSA provenance/attestation,
  OpenSSF Scorecard, release, or artifact-publishing proposals to a new
  scoped spec/plan/task plus `.github/workflows/ci.yml`, security review, and
  operations evidence as applicable.
- Route pre-commit hook, Prettier, EditorConfig, formatting, markdownlint,
  CommonMark, YAML 1.2.2, or lint-scope changes to
  [.editorconfig](../../../../.editorconfig),
  [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml),
  [scripts/README.md](../../../../scripts/README.md), and the CI/CD QA guide.
- Route validation-script changes to `scripts/**`, `scripts/README.md`, CI
  workflow path filters, and the relevant Stage 04 task evidence.
- Route manifest, policy, secret-handling, or infrastructure static-contract
  changes to the matching `gitops/`, `infrastructure/`, `policy/`, and script
  owners, with explicit static-vs-live evidence language.
- Route secure SDLC, SSDF, NIST SP 800-204D, supply-chain, or
  approval-boundary changes to Stage 00 governance and operations
  policy/runbook owners; do not encode active policy in this reference.
- Update [Research README](../README.md) and task evidence when this reference
  changes status, scope, sources, or validation results.
- Record durable progress/memory only when the active task write scope includes
  `docs/00.agent-governance/memory/progress.md`.
- Before handoff for this reference, run `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .`; record PASS/FAIL and
  limitations in the task record.

## Sources

Official and primary external sources. WER-005 refreshed the following sources
on 2026-07-05. Earlier 2026-07-04 CI/formatting and 2026-07-02
SDLC/supply-chain source history is preserved above for continuity:

- GitHub Actions workflow syntax:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub Actions secure use/security hardening:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub Code scanning / CodeQL concepts:
  <https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning>
- GitHub Dependency Review:
  <https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review>
- GitHub Spec Kit:
  <https://github.com/github/spec-kit>
- NIST SSDF SP 800-218:
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- NIST SP 800-204D:
  <https://csrc.nist.gov/pubs/sp/800/204/d/final>
- SLSA spec v1.1:
  <https://slsa.dev/spec/v1.1/>
- OpenSSF Scorecard:
  <https://scorecard.dev/>
- Prettier docs:
  <https://prettier.io/docs/>
- EditorConfig:
  <https://editorconfig.org/>
- CommonMark 0.31.2:
  <https://spec.commonmark.org/0.31.2/>
- YAML 1.2.2:
  <https://yaml.org/spec/1.2.2/>
- markdownlint:
  <https://github.com/DavidAnson/markdownlint>
- pre-commit:
  <https://pre-commit.com/>

Historical context retained from earlier versions:

- Martin Fowler, Continuous Integration:
  <https://martinfowler.com/articles/continuousIntegration.html>

Repo-backed sources:

- [Documentation Protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Templates README](../../../99.templates/README.md)
- [Scripts README](../../../../scripts/README.md)
- [GitHub CI Workflow](../../../../.github/workflows/ci.yml)
- [EditorConfig](../../../../.editorconfig)
- [Pre-commit Config](../../../../.pre-commit-config.yaml)
- [Workspace Governance Baseline Research](workspace-governance-baseline.md)
- [Infrastructure Static Contract Verification](../../../../infrastructure/tests/verify-contracts-static.sh)

Non-authoritative market/context scan sources:

- GitHub Blog, Spec-driven development with AI:
  <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>
- OpenSSF Scorecard context, checked 2026-07-05:
  <https://scorecard.dev/>

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-05
- Next review trigger: spec lifecycle, CI workflow, QA gate, formatting,
  pre-commit, template, validation-script, NIST SSDF/SP 800-204D,
  GitHub Actions, GitHub Spec Kit, CodeQL/code scanning, Dependency Review,
  SLSA provenance/attestation, OpenSSF Scorecard, Prettier, EditorConfig,
  CommonMark, YAML 1.2.2, markdownlint, or pre-commit source changes.

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **Parent references README**: [90.references README](../../README.md)
- **Workspace baseline**: [Workspace Governance Baseline Research](workspace-governance-baseline.md)
- **Harness/loop reference**: [Harness and Loop Engineering Research](harness-and-loop-engineering.md)
- **Provider status**: [Provider Harness Implementation Status Research](provider-implementation-status.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Task**: [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **CI/CD QA guide**: [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- **Scripts README**: [Scripts README](../../../../scripts/README.md)
- **Templates README**: [Templates README](../../../99.templates/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
