---
title: 'Active Control Surface Governance Hardening Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-13
---

# Active Control Surface Governance Hardening Technical Specification (Spec)

## Overview

This document defines the design for hardening the active repository control
surfaces in `hy-home.k8s`. The target surfaces are GitHub configuration and
workflow files, validation scripts, GitOps desired state, infrastructure
contracts, policy-as-code, test entrypoints, Traefik local route manifests, and
the local sample-app onboarding template.

The work preserves the approved boundary for cloud examples: `examples/aws`
and `examples/azure` remain dated Cloud Example Snapshot material, not live
provider-latest guidance and not active SDLC documents requiring wholesale
frontmatter or section migration.

## Strategic Boundaries & Non-goals

In scope:

- Align active control-surface contracts across `.github`, `scripts`,
  `gitops`, `infrastructure`, `policy`, `tests`, `traefik`, and
  `examples/sample-app`.
- Keep README files as frontmatter-free entrypoints that route to canonical
  support, governance, workflow, and validator owners.
- Strengthen deterministic validation for CI/CD, QA, GitOps, secret handling,
  policy-as-code, protected surfaces, and local route contracts where the repo
  can enforce the rule without a live cluster.
- Clarify the Cloud Example Snapshot boundary in active README and validation
  surfaces without rewriting all cloud example SDLC documents as active
  current-state documents.
- Capture implementation evidence through Stage 04 task records and the
  canonical progress ledger.

Out of scope:

- Live Kubernetes, Argo CD, Vault, cloud, DNS, certificate, or GitHub resource
  mutation.
- Secret value inspection, certificate regeneration, or credential changes.
- Pushing, publishing, merging, or dispatching remote automation without
  separate human approval.
- Promoting `examples/aws/docs` or `examples/azure/docs` into active SDLC
  documents with required frontmatter and template heading enforcement.
- Replacing the existing Stage 00 to Stage 99 documentation taxonomy.

## Contracts

- **Config Contract**:
  - `.github` Markdown control files stay frontmatter-free because GitHub
    renders or consumes them directly.
  - README files stay frontmatter-free and follow the common README profile:
    `Overview`, `Audience`, `Scope`, `Structure`,
    `How to Work in This Area`, `Link Basis`, and `Related Documents`.
  - Active workflow, script, GitOps, policy, and route rules are owned by
    governance/support documents and validators, not by duplicated README
    prose.
- **Data / Interface Contract**:
  - GitOps desired state is declarative, versioned in Git, reconciled by
    Argo CD, and validated repo-statically before merge.
  - Secret material is referenced through ESO/Vault contracts or safe
    placeholders; secret values and generated private keys are not inspected.
  - Policy-as-code is enforced through OPA/Conftest when available and through
    the repository fallback checks when optional tools are missing.
  - Cloud example docs are snapshot references. Active repo behavior must not
    depend on their provider-latest accuracy.
- **Governance Contract**:
  - Canonical rules live in Stage 00, Stage 99 support docs, Stage 05
    operations docs, workflow files, or validator scripts according to the
    owning surface.
  - README files and GitHub-native Markdown summarize and route only.
  - Deterministic drift belongs in `scripts/validate-repo-quality-gates.sh` or
    focused validation scripts; non-deterministic live checks belong in
    operator-run infrastructure test scripts.

## Core Design

- **Component Boundary**:
  - GitHub control: `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
    `.github/SECURITY.md`, workflows, Dependabot, labeler, issue templates,
    `CODEOWNERS`, and zizmor configuration.
  - Validation harness: `scripts/*.sh`, `policy/conftest/kubernetes.rego`,
    `tests/README.md`, and `infrastructure/tests/*.sh`.
  - Desired state: `gitops/**`, `infrastructure/**`, `traefik/**`, and
    `examples/sample-app/**`.
  - Snapshot examples: `examples/aws/**` and `examples/azure/**` remain
    reference snapshots with active-boundary checks in parent README surfaces.
- **Key Dependencies**:
  - GitHub Actions for CI and workflow-trigger evidence.
  - OpenGitOps principles for declarative, versioned, pulled, reconciled
    desired state.
  - Kubernetes, Kustomize, Argo CD, Argo Rollouts, ESO, OPA/Conftest, and
    KubeLinter official documentation for active technical claims.
  - Existing repo quality gates and harness validation.
- **Tech Stack**:
  - Markdown README and governance files.
  - GitHub Actions YAML.
  - Kubernetes, Argo CD, Argo Rollouts, ESO, Istio, Traefik, and MetalLB YAML.
  - Bash and embedded Python validation scripts.
  - Rego policy files and optional CLI tools.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Treat each active surface as a contract entity with `owner`,
    `source_of_truth`, `validation`, `mutation_boundary`, and
    `snapshot_boundary`.
  - Treat each README matrix row as an index entry, not a full policy record.
  - Treat each validator check as an executable projection of one canonical
    contract sentence.
- **Migration / Transition Plan**:
  - Update contract/support/governance wording first when a rule changes.
  - Update active README and GitHub control surfaces second to route to the
    canonical owner.
  - Update validators third when the rule can be checked deterministically.
  - Update Stage 04 task evidence and progress memory last.
  - Keep cloud example SDLC documents untouched unless a narrow active-boundary
    reference in an index or README must change.

## Interfaces & Data Structures

### Core Interfaces

```text
Official source basis
-> Stage 00 / Stage 99 canonical contract
-> README or GitHub control routing surface
-> Validator / CI / harness check
-> Stage 04 task evidence and progress memory
```

```text
Cloud example snapshot
-> examples/README.md role matrix
-> provider example README snapshot boundary
-> repo validators preventing provider-latest claims
```

These interfaces are document and validation contracts, not runtime APIs.

### API Contract

This work exposes no external application API. No feature-local `api-spec.md`,
OpenAPI, GraphQL, or protobuf contract is required.

### Agent Role & IO Contract

- **Agent Role**: Documentation and validation implementer, with subagents
  available for independent audit, implementation, and review tasks after the
  implementation plan is approved.
- **Inputs**: This spec, approved implementation plan, target repository
  files, official external sources, current validation output, and Stage 00/99
  contracts.
- **Outputs**: Contract updates, README/control-surface updates, validator
  improvements, Stage 04 evidence, and progress memory.
- **Success Definition**: Active control surfaces route to one canonical owner,
  deterministic drift is validated, cloud examples remain snapshot-bounded,
  and the repository harness passes.

### Tools & Tool Contract

- **Tool List**:
  - `rg`, `sed`, `git`, `bash`, `jq`, YAML/TOML/JSON parsers, and repository
    validation scripts.
  - Web research against official or primary sources for current tool and
    platform claims.
  - Optional subagents for implementation and review once a written plan
    exists.
- **Permission Boundary**:
  - Repo-static file edits are allowed.
  - Live runtime, third-party, credential, publish, push, merge, and destructive
    cleanup actions require separate explicit approval.
  - `secrets/certs/*.pem` may be counted or scanned by safe secret-handling
    tools, but their values must not be displayed, edited, or regenerated.
- **Failure Handling**:
  - If a README duplicates policy, move durable content to the canonical owner
    and keep the README as a route.
  - If validator enforcement is too brittle for a live-only condition, document
    the live validation boundary instead of forcing a false static gate.
  - If official sources contradict current repo wording, update the canonical
    contract before dependent surfaces.

### Prompt / Policy Contract

- **System / Instruction Contract**: Agents must work repo-first, read the
  canonical owner before changing a target surface, and record evidence for
  contract-affecting edits.
- **Policy Constraints**:
  - Keep README files frontmatter-free.
  - Keep GitHub-native Markdown frontmatter-free.
  - Keep AWS/Azure example docs snapshot-bounded.
  - Do not add policy bodies to README files when support, governance,
    workflow, script, or operations owners already exist.
  - Use logical-unit commits.
- **Versioning Rule**: New external-tool claims must cite an official or
  primary source and avoid provider-latest claims unless the implementation
  actually verifies the current provider state.

### Memory & Context Strategy

- **Short-term Context**: Use this spec, the follow-up implementation plan,
  task record, and focused scan output during execution.
- **Long-term Memory**: Update
  `docs/00.agent-governance/memory/progress.md` for completed logical units,
  validation evidence, and reusable constraints.
- **Retrieval Boundary**: Do not persist secret values, live credentials,
  private key material, or local-only runtime state in documentation memory.

### Guardrails

- **Input Guardrails**:
  - Confirm each file is in the active control-surface scope or the snapshot
    boundary before editing.
  - Treat optional tool skips as skips only when the repository fallback passes.
  - Treat cloud provider docs as dated examples unless a separate currentness
    pass is explicitly approved.
- **Output Guardrails**:
  - Keep one canonical owner per rule.
  - Keep README entries concise and matrix-oriented.
  - Preserve active GitOps desired-state semantics and avoid live mutation.
  - Record all deterministic validator additions in the relevant support or
    governance contract.
- **Blocked Conditions**:
  - A validator failure that indicates active contract drift.
  - A requested edit that requires secret value disclosure.
  - A provider-latest claim that cannot be supported by current official
    evidence.
  - A destructive file or branch action without explicit approval.
- **Escalation Rule**: Ask the human before changing the approved snapshot
  boundary, deleting certificate or secret fixtures, mutating live systems,
  pushing, merging, publishing, or changing credentials.

### Evaluation

- **Eval Types**:
  - Repository structural validation.
  - GitHub workflow and control-surface validation.
  - GitOps, Kubernetes manifest, policy, secret, and infrastructure contract
    validation.
  - Snapshot-boundary scan for AWS/Azure provider-latest claims.
  - Review validation for duplicated policy ownership and stale wording.
- **Metrics**:
  - Required repository validation commands pass.
  - No active README gains frontmatter or duplicate contract bodies.
  - `.github` control Markdown remains frontmatter-free.
  - Active validators reflect documented canonical owners.
  - Cloud examples retain snapshot wording and are not treated as active live
    provider guidance.
- **Datasets / Fixtures**:
  - Tracked target files under `.github`, `scripts`, `gitops`,
    `infrastructure`, `policy`, `tests`, `traefik`, and `examples/sample-app`.
  - Snapshot boundary fixtures under `examples/aws` and `examples/azure`.
  - Existing optional-tool behavior for `kube-linter` and `conftest`.
- **How to Run**:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

Focused checks may include:

```bash
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

## Edge Cases & Error Handling

- **Cloud snapshot drift**: If an AWS or Azure snapshot doc contains language
  that reads as current provider-latest guidance, prefer fixing the nearest
  README or index boundary first. Edit the snapshot document only when the
  claim is active-facing or directly misleading from the parent index.
- **Optional tool absence**: If `conftest` or `kube-linter` is unavailable,
  the repository fallback or YAML syntax path must still pass and the output
  must not be represented as full optional-tool coverage.
- **Secret-like fixtures**: Treat committed certificate fixtures as protected
  paths. Validate through secret-handling scans without exposing values.
- **README pressure**: If a desired rule does not fit the README entrypoint
  profile, create or update the owning support/governance/operations document
  instead of adding an ad hoc README section.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A new validator rejects valid snapshot material.
  - **Fallback**: Narrow the validation to active surfaces or add a documented
    snapshot exception.
  - **Human Escalation**: Required if the exception changes the approved
    snapshot boundary.
- **Failure Mode**: A GitOps or infrastructure edit implies live resource
  mutation.
  - **Fallback**: Keep the change repo-static and document the operator-owned
    live validation command.
  - **Human Escalation**: Required before any live mutation.
- **Failure Mode**: Secret or certificate content must be inspected to decide a
  contract.
  - **Fallback**: Validate path, key name, and ownership metadata only.
  - **Human Escalation**: Required before any secret value handling.

## Verification Commands

Minimum validation:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

Focused validation after implementation touches relevant surfaces:

```bash
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
bash infrastructure/tests/verify-contracts-static.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Active control surfaces have one canonical owner per rule,
  and README/GitHub-native Markdown files route rather than duplicate policy.
- **VAL-SPC-002**: Cloud examples remain dated snapshots and are not promoted
  into active provider-latest SDLC documents.
- **VAL-SPC-003**: CI/CD and QA boundaries match GitHub Actions, GitOps,
  Kubernetes, policy-as-code, and secret-handling official source basis.
- **VAL-SPC-004**: Deterministic drift checks are implemented or explicitly
  documented as live/operator-owned checks.
- **VAL-SPC-005**: Required repository and harness validations pass, with
  optional-tool skips reported separately from failures.

## Traceability

- [Workspace Document Governance Hardening](../013-workspace-document-governance-hardening/spec.md)
- [Workspace Document Contract Normalization](../014-workspace-document-contract-normalization/spec.md)
- [Agent Governance Contract Normalization](../015-agent-governance-contract-normalization/spec.md)
- [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Common Documentation Template Governance](../../99.templates/support/common-documentation-governance.md)
- [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Git Workflow](../../00.agent-governance/rules/git-workflow.md)
- [Quality Standards](../../00.agent-governance/rules/quality-standards.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
- [Harness Validation](../../../scripts/validate-harness.sh)
- [Plan](../../04.execution/plans/2026-07-04-active-control-surface-governance-hardening.md)
- [Task](../../04.execution/tasks/2026-07-04-active-control-surface-governance-hardening.md)
### Related inputs

- **PRD**: No separate PRD exists. The upstream requirement is the approved
  user request to harden the active control surfaces while preserving AWS and
  Azure cloud examples as dated snapshots.
- **ARD**: No separate ARD exists. The architectural baseline is the current
  local GitOps platform contract plus Stage 00 and Stage 99 governance.
- **Related ADRs**:
  - [Current Local GitOps Platform Contract](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Prior Specs**:
  - [Workspace Document Governance Hardening](../013-workspace-document-governance-hardening/spec.md)
  - [Workspace Document Contract Normalization](../014-workspace-document-contract-normalization/spec.md)
  - [Agent Governance Contract Normalization](../015-agent-governance-contract-normalization/spec.md)

Official source basis:

- GitHub Actions workflow syntax and permissions:
  <https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions>
- GitHub Actions secure use:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub pull request templates:
  <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository>
- GitHub security policy:
  <https://docs.github.com/code-security/getting-started/adding-a-security-policy-to-your-repository>
- GitHub Dependabot configuration:
  <https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference>
- OpenGitOps principles:
  <https://opengitops.dev/>
- Kubernetes Secrets:
  <https://kubernetes.io/docs/concepts/configuration/secret/>
- Kubernetes Kustomize:
  <https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/>
- Argo CD:
  <https://argo-cd.readthedocs.io/>
- Argo CD automated sync:
  <https://argo-cd.readthedocs.io/en/latest/user-guide/auto_sync/>
- Argo Rollouts:
  <https://argoproj.github.io/rollouts/>
- Argo Rollouts AnalysisTemplate:
  <https://argo-rollouts.readthedocs.io/en/stable/features/analysis/>
- External Secrets Operator with Vault:
  <https://external-secrets.io/latest/provider/hashicorp-vault/>
- External Secrets Operator with Azure Key Vault:
  <https://external-secrets.io/latest/provider/azure-key-vault/>
- OPA Conftest:
  <https://www.conftest.dev/>
- KubeLinter:
  <https://docs.kubelinter.io/>

Repository inputs:

- `docs/99.templates/support/documentation-contract.md`
- `docs/99.templates/support/template-routing.md`
- `docs/99.templates/support/frontmatter-schema.md`
- `docs/99.templates/support/common-documentation-governance.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/git-workflow.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `scripts/validate-repo-quality-gates.sh`
- `scripts/validate-harness.sh`
