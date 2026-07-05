---
title: 'Reference: Implementation Roadmap and Automation Opportunities Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---

# Reference: Implementation Roadmap and Automation Opportunities Audit

## Overview

This dated audit converts the 2026-07-05 workspace engineering implementation
audit findings into a cross-report roadmap, automation opportunity matrix, and
owner-routed implementation checklist.

This audit is descriptive reference material. It does not change active
governance, provider adapter behavior, CI/CD workflows, validation scripts,
GitOps manifests, policy bundles, secrets, runtime operations, or deployment
procedure.

## Purpose

- Summarize the implementation status patterns across governance, harness,
  loop, provider, SDLC, CI/CD, QA, formatting, Kubernetes, Infrastructure, and
  security reports.
- Convert recurring findings into safe future automation candidates.
- Separate repo-static automation opportunities from protected surfaces that
  require explicit approval, live-runtime context, or external-system access.
- Give future specs, plans, tasks, and owners a stable routing map without
  changing behavior during this audit.

## Reference Type

- Type: dated-implementation-roadmap / automation-opportunity-snapshot
- Source checked: 2026-07-05
- Refresh trigger: audit report, research benchmark, Stage 00 governance,
  provider adapter, template, script, workflow, GitOps, policy, infrastructure,
  security, QA, DORA/CI metrics, live-runtime evidence, or owner-routing
  change.

## Authority Boundary

- **Authoritative for**:
  - Cross-report implementation status summary as checked on 2026-07-05.
  - Candidate roadmap priorities and automation opportunity routes.
  - Repo-static versus live-runtime and external-action approval boundaries.
  - Owner routing for future implementation specs, plans, tasks, validators,
    scripts, workflows, or operations documents.
- **Not authoritative for**:
  - Active governance, CI/CD, QA, formatting, linting, workflow, script,
    template, GitOps, Kubernetes, Vault, ESO, policy, provider, or security
    enforcement semantics.
  - Live k3d, Argo CD, Vault, ESO, Kubernetes, cloud, GitHub remote,
    deployment, endpoint, network, ingress, TLS, provider-runtime, paid-job,
    secret, or external-service readiness.
  - Approval to mutate credentials, secrets, remote services, workflows,
    manifests, policy bundles, provider runtime configuration, or protected
    infrastructure.

## Scope

- Covers cross-report status patterns, roadmap priorities, automation
  opportunities, protected surface constraints, owner routing, implementation
  checklist, and residual risks.
- Uses the three completed part reports and the 2026-07-04 research pack as
  benchmark context.
- Uses only repo-backed evidence for current implementation status.
- Excludes implementation of new validators, workflow changes, policy changes,
  manifest changes, provider config changes, live runtime checks, secret reads,
  credential changes, GitHub remote mutation, push, merge, publishing, paid
  jobs, or third-party mutation.

## Definitions / Facts

### Cross-report Status Summary

| Domain | Current pattern | Status | Evidence | Roadmap implication |
| --- | --- | --- | --- | --- |
| Governance, rules, and operating model | Stage 00, provider shims, memory, templates, scripts, and audit references give the workspace a clear documented operating model. | Implemented | [Governance harness provider audit](governance-harness-loop-providers.md), [Harness catalog](../../../00.agent-governance/harness-catalog.md), [Bootstrap rule](../../../00.agent-governance/rules/bootstrap.md) | Keep routing and ownership current when provider adapters or templates change. |
| Harness and loop engineering | Observe/plan/act/verify/learn and review loops are implemented as documented procedure and evidence practice, not as a single automated runtime engine. | Partial | [Governance harness provider audit](governance-harness-loop-providers.md), [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) | Automate evidence checks where deterministic; keep judgment-heavy review as human/model review. |
| Claude, Codex, and Gemini provider parity | Common `.agents/**` assets and provider docs exist, but native capabilities and enforcement differ by provider. | Partial | [Governance harness provider audit](governance-harness-loop-providers.md), [Claude provider](../../../00.agent-governance/providers/claude.md), [Codex provider](../../../00.agent-governance/providers/codex.md), [Gemini provider](../../../00.agent-governance/providers/gemini.md) | Add parity evidence checks that flag overclaims without forcing false equivalence. |
| Spec-driven SDLC | Stage 03 specs, Stage 04 plans/tasks, Stage 90 references, and validation evidence implement local spec-driven traceability. | Implemented | [SDLC CI QA audit](sdlc-ci-qa-formatting-automation.md), [Spec index](../../../03.specs/README.md), [Plan index](../../../04.execution/plans/README.md), [Task index](../../../04.execution/tasks/README.md) | Preserve the artifact ladder and automate stale links/status vocabulary checks. |
| CI/CD and QA | CI validates repository quality, docs, policies, manifests, and static contracts; it does not deploy or publish runtime artifacts. | Implemented | [SDLC CI QA audit](sdlc-ci-qa-formatting-automation.md), [CI workflow](../../../../.github/workflows/ci.yml), [CI/CD QA reference guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md) | Summarize workflow and QA evidence automatically before adding heavier gates. |
| Formatting and linting | `.editorconfig`, markdownlint/CommonMark, pre-commit, shellcheck, shfmt, actionlint, zizmor, hadolint, kube-linter path, and diff checks are documented. | Partial | [SDLC CI QA audit](sdlc-ci-qa-formatting-automation.md), [.editorconfig](../../../../.editorconfig), [pre-commit config](../../../../.pre-commit-config.yaml), [Scripts README](../../../../scripts/README.md) | Optional-tool coverage should be reported explicitly as run, skipped, or fallback. |
| Kubernetes and GitOps | Desired-state surfaces, root Application boundaries, AppProjects, namespaces, Kustomize, and static contracts are repo-backed. | Implemented | [Kubernetes infrastructure security audit](kubernetes-infrastructure-security.md), [GitOps README](../../../../gitops/README.md), [Infrastructure README](../../../../infrastructure/README.md) | Build repo-static evidence aggregation before any live readiness automation. |
| Secrets and security | No-plaintext-secret, ESO/Vault interfaces, OPA/Conftest policy, and static secret handling are represented; live secret readiness is not proven. | Partial | [Kubernetes infrastructure security audit](kubernetes-infrastructure-security.md), [secret handling validator](../../../../scripts/check-secret-handling.sh), [policy bundle](../../../../policy/conftest/kubernetes.rego) | Keep secret evidence non-value-bearing and route live readiness to approved operations work. |
| Supply-chain, provenance, and DORA/CI metrics | Explicit image tags and context research exist; signatures, SBOMs, SLSA provenance, Scorecard gates, and DORA metrics are not active gates. | Gap | [SDLC CI QA audit](sdlc-ci-qa-formatting-automation.md), [Kubernetes infrastructure security audit](kubernetes-infrastructure-security.md) | Treat as future proposal routes, not current implementation. |
| Live-runtime readiness | Static documentation and tests separate live evidence from repo-static evidence. Live checks were not run for this audit. | Not in scope | [Kubernetes infrastructure security audit](kubernetes-infrastructure-security.md), [Infrastructure README](../../../../infrastructure/README.md), [Tests README](../../../../tests/README.md) | Require explicit operator approval, runbooks, and evidence capture before live checks. |

### Priority Matrix

| Priority | Roadmap item | Current status | Why it matters | Owner route | Approval boundary | Evidence lane |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Audit matrix validator | Gap | All part reports depend on exact columns, required rows, allowed status values, and evidence links. | Stage 04 task plus `scripts/` owner | Repo-static script change approval | repo-static |
| P1 | README/index stale-link checker for audit folderization | Gap | Folderized audit packs can drift when planned code literals become current report links or moved paths remain. | Stage 04 task plus Stage 90 reference owner | Repo-static validator/index change approval | repo-static |
| P1 | Provider parity evidence checker | Gap | Claude, Codex, and Gemini differ; overclaiming native parity can weaken governance. | Stage 00 agent-governance owner | Provider-doc and adapter-surface approval | repo-static |
| P1 | Workflow/QA evidence summarizer | Partial | Current QA spans CI, scripts, optional tools, and local gates; summaries reduce stale evidence and skipped-tool ambiguity. | `.github`, `scripts`, and Stage 05 guide owners | CI/script behavior approval if enforcement changes | CI/toolchain |
| P1 | GitOps manifest and policy evidence aggregator | Partial | GitOps, AppProject, namespace, policy, image, and static-contract evidence is spread across several files and scripts. | GitOps, policy, infrastructure, and scripts owners | Manifest/policy/script approval if behavior changes | repo-static |
| P2 | Secret-handling evidence summarizer | Partial | Secret evidence must prove scanner/policy coverage without exposing values or implying live secret readiness. | Security, scripts, Stage 05 operations owners | Secret-handling and credential-boundary approval | repo-static |
| P2 | Live-runtime readiness evidence route | Not in scope | Live checks need operator context, cluster access, runbooks, and no secret leakage. | Stage 05 runbook and infrastructure owners | Explicit live-runtime and credential approval | live-runtime |
| P3 | DORA/CI metrics proposal route | Gap | Metrics need precise definitions and should not be inferred from static files alone. | Stage 03/04 measurement task owner | GitHub remote/API or telemetry approval if queried | market/context |
| P3 | Supply-chain hardening proposal route | Gap | SBOM, signatures, provenance, vulnerability gates, and Scorecard can add value only with scoped build/release ownership. | CI/security/release owners | CI, artifact, registry, or remote-service approval | CI/toolchain |

### Automation Opportunity Matrix

| Opportunity | Owner route | Required approval boundary | Evidence lane | Safe for future repo-static automation | Initial implementation shape |
| --- | --- | --- | --- | --- | --- |
| audit matrix validator | Stage 04 task, Stage 90 reference owner, `scripts/` owner | Approval to add or change repo-static validation script and quality gate wiring | repo-static | Yes | Check required headings, exact matrix columns, allowed status vocabulary, required rows, and evidence links for audit reports. |
| README/index stale-link checker for audit folderization | Stage 90 reference owner, Stage 04 task owner | Approval to add stale-link validator or extend existing link checks | repo-static | Yes | Detect root-level moved audit path links, planned code literals for existing reports, and missing folder README links. |
| provider parity evidence checker | Stage 00 agent-governance owner | Approval to codify provider-specific parity rules and non-parity warnings | repo-static | Yes | Check Claude/Codex/Gemini docs for shared `.agents/**` references, provider-specific boundaries, and hook/permission overclaims. |
| workflow/QA evidence summarizer | `.github`, `scripts`, Stage 05 guide owners | Approval before changing CI behavior; read-only summarizer can stay repo-static | CI/toolchain | Yes | Generate a deterministic summary of workflows, validation commands, optional tool paths, skip semantics, and artifacts. |
| GitOps manifest and policy evidence aggregator | GitOps, policy, infrastructure, scripts owners | Approval before changing manifests, policies, or enforcement; read-only aggregation is repo-static | repo-static | Yes | Summarize AppProjects, namespaces, Kustomize completeness, image policy, policy bundle rules, and static contract coverage. |
| secret-handling evidence summarizer | Security, scripts, operations owners | Approval before adding secret scanners or touching credential flows; output must not reveal secret values | repo-static | Yes | Combine gitleaks/detect-secrets/static secret checks and policy-gate status into a non-value-bearing evidence report. |
| DORA/CI metrics proposal route | Stage 03/04 measurement task owner, CI owner | Approval for GitHub remote/API access, telemetry queries, or metrics storage | market/context | No | Start as a measurement spec defining lead time, deployment frequency, recovery time, change fail rate, and source-of-truth limits. |
| live-runtime readiness evidence route | Stage 05 runbook owner, infrastructure owner, operator | Explicit approval for live Kubernetes, Argo CD, Vault, ESO, network, endpoint, or secret checks | live-runtime | No | Create a runbook-first checklist that names cluster context, commands, redaction rules, rollback boundaries, and evidence capture. |

### Protected Surface Constraints

- Repo-static automation may inspect tracked files, Markdown, YAML, scripts,
  policy bundles, templates, task records, and local validation output.
- Repo-static automation must not mutate provider settings, GitHub remotes,
  CI secrets, cluster state, Vault state, ESO state, Kubernetes objects,
  external gateway state, package registries, artifact stores, paid jobs, or
  third-party resources.
- Workflow or script enforcement changes need a Stage 03/04 route because they
  can change CI pass/fail behavior.
- GitOps, policy, infrastructure, and secret handling changes need explicit
  owner review because they affect deployment or security boundaries.
- Live-runtime readiness evidence must start from Stage 05 runbooks or
  policies, name the operator context, redact sensitive output, and record
  evidence separately from Stage 90 repo-static references.
- DORA/CI metrics, GitHub remote checks, and external provider evidence require
  source-of-truth definitions and approval before querying or storing data.

### Owner Routing

| Change class | Canonical owner route | Start artifact | Validation lane |
| --- | --- | --- | --- |
| Audit/report structural validation | Stage 90 references plus Stage 04 task | Spec or task for validator | `git diff --check`, repository quality gate, targeted `rg` |
| README/index link freshness | Stage 90 references plus docs quality scripts | Task or script proposal | Markdown link check and stale-path scan |
| Provider parity and non-parity wording | Stage 00 agent-governance | Spec plus provider docs | Provider-doc scan and repo quality gate |
| CI/CD or QA summarization | `.github`, `scripts`, Stage 05 guide | Spec or plan before workflow/script changes | CI/toolchain evidence and local quality gate |
| GitOps manifest evidence | `gitops`, `infrastructure`, `scripts` | Spec/plan before manifest or test changes | GitOps structure, manifest, policy, static contract checks |
| Policy-as-code changes | `policy/conftest`, `scripts`, CI owners | Spec/plan before enforcement changes | Policy gate and CI evidence |
| Secret handling evidence | Security/operations plus scripts | Spec/plan with no-secret-output contract | Secret scanners, static checks, redacted evidence |
| Live runtime readiness | Stage 05 runbooks/policies plus operator | Runbook/task with explicit approval | Live command output, redacted separately |
| DORA/CI metrics | Stage 03/04 measurement owner plus CI owner | Measurement spec | Defined metrics, source boundaries, approval log |
| Supply-chain hardening | CI/security/release owners | Spec/plan before gate adoption | Scanner/provenance/SBOM evidence when implemented |

### Implementation Checklist

- [x] Used the local reference template section model.
- [x] Included the required frontmatter exactly.
- [x] Included the required reference sections.
- [x] Included Cross-report Status Summary, Priority Matrix, Automation
  Opportunity Matrix, Protected Surface Constraints, Owner Routing,
  Implementation Checklist, and Residual Risks.
- [x] Included automation opportunity rows for audit matrix validator,
  README/index stale-link checker, provider parity evidence checker,
  workflow/QA evidence summarizer, GitOps manifest and policy evidence
  aggregator, secret-handling evidence summarizer, DORA/CI metrics proposal
  route, and live-runtime readiness evidence route.
- [x] Included owner route, required approval boundary, evidence lane, and
  future repo-static automation safety for each automation opportunity.
- [x] Used only `Implemented`, `Partial`, `Gap`, and `Not in scope` as audit
  status values.
- [x] Used repo-backed evidence only for implementation status claims.
- [x] Kept repo-static, CI/toolchain, market/context, and live-runtime
  evidence lanes separate.
- [ ] Future work: implement selected automation through scoped specs, plans,
  tasks, and validation scripts.

### Residual Risks

- This roadmap is a 2026-07-05 snapshot and can become stale when reports,
  templates, governance, provider adapters, CI workflows, scripts, GitOps
  manifests, policies, infrastructure tests, operations documents, or research
  benchmarks change.
- Priority labels are advisory and based on current repository evidence, not a
  committed delivery schedule.
- Automation candidates can create CI burden or false confidence if implemented
  without explicit skip/fallback semantics and owner review.
- Repo-static automation cannot prove live provider runtime, Kubernetes,
  Argo CD, Vault, ESO, NetworkPolicy, ingress/TLS, endpoint, cloud, secret,
  paid-job, GitHub remote, or third-party readiness.
- DORA/CI and supply-chain work require careful source-of-truth definitions
  before metrics or gates become operational.

## Sources

- [Governance Harness Loop Provider Audit](governance-harness-loop-providers.md)
- [SDLC CI QA Formatting Automation Audit](sdlc-ci-qa-formatting-automation.md)
- [Kubernetes Infrastructure Security Audit](kubernetes-infrastructure-security.md)
- [Workspace Engineering Research Pack README](../../research/2026-07-04-wer/README.md)
- [Workspace Governance Baseline Research](../../research/2026-07-04-wer/workspace-governance-baseline.md)
- [Harness and Loop Engineering Research](../../research/2026-07-04-wer/harness-and-loop-engineering.md)
- [Provider Harness Implementation Status Research](../../research/2026-07-04-wer/provider-implementation-status.md)
- [Spec, SDLC, CI, QA, and Formatting Research](../../research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md)
- [Kubernetes Infrastructure Security Research](../../research/2026-07-04-wer/kubernetes-infrastructure-security.md)
- [Automation Pipeline Workflow QA Research](../../research/2026-07-04-wer/automation-pipeline-workflow-qa.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [CI Workflow](../../../../.github/workflows/ci.yml)
- [GitOps README](../../../../gitops/README.md)
- [Infrastructure README](../../../../infrastructure/README.md)
- [Scripts README](../../../../scripts/README.md)
- [Tests README](../../../../tests/README.md)
- [Policy Bundle](../../../../policy/conftest/kubernetes.rego)
- [Task Record](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-05
- Next review trigger: audit report, roadmap priority, automation
  opportunity, protected-surface boundary, owner route, Stage 00 governance,
  Stage 03/04 SDLC, `.github`, `scripts`, `gitops`, `policy`,
  `infrastructure`, secret-handling, DORA, live-runtime, repo-static,
  CI/toolchain, market/context, or research benchmark change.
- Refresh this report before converting any opportunity into active
  automation, CI enforcement, manifest change, policy change, live check, or
  external-system integration.

## Related Documents

- **Audit pack README**: [README.md](./README.md)
- **Audits README**: [Parent audits index](../README.md)
- **Parent Plan**: [Workspace Engineering Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- **Task record**: [Workspace Engineering Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
