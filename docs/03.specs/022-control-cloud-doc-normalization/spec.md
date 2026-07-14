---
title: 'Control Surface and Cloud Example Documentation Normalization Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-14
---

# Control Surface and Cloud Example Documentation Normalization Technical Specification

## Overview

This specification defines the documentation and validation contract for the
active control surfaces under `.github`, `examples`, `gitops`, `infrastructure`,
`policy`, `scripts`, `secrets`, `tests`, and `traefik`.

The work has two linked outcomes. First, active control-surface README and
GitHub-native Markdown files keep their current frontmatter-free entrypoint
role while routing policy details to canonical owners. Second, AWS and Azure
example documents under `examples/aws/docs/**` and `examples/azure/docs/**`
are promoted from unmanaged Cloud Example Snapshot material to an
example-local SDLC snapshot profile with explicit frontmatter, section, and
template expectations.

> **2026-07-14 steady-state correction:** The example-local route described by
> this completed normalization tranche was superseded by Spec 030. The
> `examples/{aws,azure}/docs/**` trees are retired and absent; their durable
> knowledge lives under `docs/90.references/cloud-examples/**`.
> `DocumentProfileContract.v3` removes every authored/README route for the
> retired trees and rejects tracked reintroduction. The remaining sections
> preserve the point-in-time implementation contract and evidence rather than
> a current authoring path.

## Strategic Boundaries & Non-goals

In scope:

- Keep README files frontmatter-free and aligned with the common README
  structure.
- Keep `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` frontmatter-free because GitHub renders or consumes
  those files directly.
- Update Stage 99 support contracts, Stage 00 routing rules, and the
  repository quality gate so AWS/Azure example docs have an explicit
  example-local SDLC snapshot route.
- Normalize AWS/Azure example PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy,
  and Runbook documents with type-appropriate frontmatter and topic-specific
  content.
- Remove duplicate headings, stale provider-latest wording, template residue,
  and unsupported legacy frontmatter keys from the targeted example docs.
- Preserve the snapshot boundary: example docs are dated reference examples,
  not live provider-latest or active production operations guidance.
- Update cross-links and README indexes for files that are renamed, archived,
  or consolidated.
- Add deterministic validation for the route and frontmatter rules where local
  repository checks can enforce them.

Out of scope:

- Live Kubernetes, Argo CD, Vault, cloud provider, GitHub remote, credential,
  branch protection, or ruleset mutation.
- Secret value inspection or credential generation.
- Provider-latest refresh of AWS or Azure service recommendations beyond
  noting that examples are dated snapshots.
- Renaming every dated AWS/Azure example file only for aesthetics. Renames
  happen only when needed to remove duplicate active purpose, close broken
  cross-links, or satisfy the approved route contract.
- Moving example-local docs into the main `docs/01` through `docs/05` stages.

## Contracts

- **Control-Surface Config Contract**:
  - README files remain frontmatter-free entrypoints.
  - GitHub-native Markdown remains frontmatter-free and routes to Stage 00,
    Stage 05, workflow YAML, support contracts, and validator owners.
  - Control-surface README files may summarize ownership and validation
    matrices, but detailed policy remains in canonical owners.
- **Example-Local SDLC Snapshot Contract**:
  - `examples/aws/docs/**` and `examples/azure/docs/**` are routed as
    example-local SDLC snapshot documents.
  - Non-README Markdown under those paths uses the matching namespaced SDLC
    `type` value from the existing Stage 99 schema.
  - Required frontmatter keys are `title`, `type`, `status`, `owner`, and
    `updated`.
  - `owner` is `platform`; `updated` uses an ISO date.
  - Status values follow the same lifecycle family as active SDLC documents,
    but the body must state the snapshot boundary when provider freshness
    matters.
  - README files under the example docs tree remain frontmatter-free.
- **Governance Contract**:
  - Stage 99 support documents own route and frontmatter rules.
  - Stage 00 rules expose those rules to agents.
  - `scripts/validate-repo-quality-gates.sh` enforces deterministic route,
    frontmatter, README, and stale-currentness checks.
  - `examples/README.md` owns the high-level role matrix for sample app and
    cloud examples.
- **Mutation Boundary**:
  - This work is repository-static. It must not deploy, sync, publish, push,
    write credentials, or mutate external systems.

## Core Design

The implementation proceeds in four parts.

First, update support and governance contracts. The existing Cloud Example
Snapshot exception becomes a routed example-local SDLC snapshot profile instead
of an unmanaged exception. README and GitHub-native Markdown exceptions remain
frontmatter-free.

Second, normalize active control-surface routing text. `.github`, `scripts`,
`tests`, `gitops`, `infrastructure`, `policy`, `secrets`, `traefik`, and
`examples` README files should keep their entrypoint role and route readers to
the canonical owners. They should not duplicate long governance bodies.

Third, normalize AWS/Azure example docs by document type. The goal is not to
copy template boilerplate. Each document must keep topic-specific content while
adding the correct metadata, removing duplicate headings, and aligning section
names with the closest SDLC template.

Fourth, update validation and evidence. The quality gate should ban
frontmatter on README and GitHub-native Markdown, require frontmatter on
example-local SDLC snapshot documents, reject unsupported keys, and prevent
provider-latest claims unless an approved provider refresh spec exists.

## Data Modeling & Storage Strategy

No runtime storage or external system is introduced.

The durable state is stored in Git through:

- Stage 00 governance rules;
- Stage 03 specification and Stage 04 execution evidence;
- Stage 99 support contracts and templates;
- control-surface README and GitHub-native Markdown route summaries;
- AWS/Azure example-local SDLC snapshot Markdown;
- repository validation scripts.

The minimum example-local SDLC frontmatter shape is:

```yaml
---
title: '<Document Title>'
type: sdlc/<role>
status: draft
owner: platform
updated: 2026-07-06
---
```

README files and GitHub-native Markdown files must not use this frontmatter.

## Interfaces & Data Structures

### Core Interfaces

```text
Official source basis
-> Stage 99 support contract
-> Stage 00 routing rule
-> README / GitHub-native routing surface
-> Validator gate
-> Stage 04 task evidence
```

```text
AWS/Azure example doc
-> example-local SDLC snapshot route
-> type-specific frontmatter
-> type-specific section normalization
-> cross-link and README index update
-> repository quality gate
```

#### API Contract

This work exposes no external application API. No `api-spec.md`, OpenAPI,
GraphQL, or protobuf contract is required.

#### Agent Role & IO Contract

- **Agent Role**: Documentation and validation implementer.
- **Inputs**: This spec, the approved plan, current repository files, official
  external sources, Stage 00 governance, Stage 99 support contracts, and
  validation output.
- **Outputs**: Updated contracts, normalized example docs, updated indexes,
  validator changes, task evidence, and progress memory.
- **Success Definition**: The targeted docs match the route/frontmatter
  contract, no README or GitHub-native Markdown receives frontmatter, stale
  provider-latest claims are removed, and repository-static validation passes.

#### Tools & Tool Contract

- **Tool List**:
  - `rg` for repository search.
  - `sed` for narrow file reads.
  - `apply_patch` for manual edits.
  - `git mv` only when a rename is required by the approved route.
  - `bash scripts/validate-repo-quality-gates.sh .` for repository quality.
  - `bash scripts/validate-k8s-manifests.sh .`, `bash scripts/check-secret-handling.sh .`, and `bash scripts/validate-policy-gates.sh .` when manifest/policy surfaces change.
- **Permission Boundary**:
  - Repo-static edits only.
  - No live cluster, provider, credential, publish, merge, or push action.
- **Failure Handling**:
  - If validation exposes a broad route conflict, fix the route owner first.
  - If a cloud example document cannot be safely classified, leave it as a
    dated snapshot and record the unresolved classification in the task record.

#### Prompt / Policy Contract

- Do not add policy bodies to README files when a Stage 00, Stage 05, Stage
  99, workflow, script, or validator owner exists.
- Do not treat AWS/Azure example snapshot docs as live provider-latest
  guidance.
- Do not add frontmatter to GitHub-native Markdown.
- Do not preserve template placeholder text in authored documents.

#### Memory & Context Strategy

- Record durable lessons in
  `../../00.agent-governance/memory/progress.md`.
- Use Stage 04 task evidence for command output and completion status.
- Do not store secrets, tokens, kubeconfigs, local auth material, or private
  diagnostics in progress memory or example docs.

#### Guardrails

- **Input Guardrails**:
  - Treat untracked pre-existing files as user-owned unless explicitly
    brought into scope.
  - Use official external sources for CI/CD, Kubernetes, GitOps, policy, and
    secret-management claims.
- **Output Guardrails**:
  - Keep Markdown links relative and recalculated from the final file
    location.
  - Keep example docs topic-specific; do not leave template instructions.
  - Keep GitHub-native Markdown compatible with GitHub rendering.
- **Blocked Conditions**:
  - A validation rule cannot distinguish README/GitHub-native files from
    example-local SDLC documents.
  - A doc has duplicate active purpose and no safe replacement owner.
- **Escalation Rule**:
  - Ask for human approval before any live runtime, remote GitHub, cloud, or
    credential action.

#### Evaluation

- **Eval Types**:
  - Contract consistency review.
  - Frontmatter schema validation.
  - README and GitHub-native frontmatter-ban validation.
  - Cross-link and stale-currentness scan.
- **Metrics**:
  - Zero validator failures for routed docs.
  - Zero unsupported frontmatter keys in target non-README docs.
  - Zero frontmatter blocks in README and GitHub-native Markdown files.
  - Zero provider-latest claims in snapshot docs unless backed by a refresh
    spec.
- **Datasets / Fixtures**:
  - Current AWS/Azure example docs.
  - Current control-surface README and GitHub-native Markdown files.
  - `scripts/validate-repo-quality-gates.sh` fixture-like repository scans.
- **How to Run**:
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`

## Edge Cases & Error Handling

- **Duplicate cloud docs**: consolidate or archive only when two files own the
  same role and purpose. Otherwise normalize both and clarify scope.
- **README under example docs**: keep frontmatter-free and use README
  structure.
- **Machine-readable example manifests**: do not add Markdown metadata.
- **Optional tool missing**: report optional skips accurately; do not call an
  optional skip a full tool-specific pass.
- **Historical provider claims**: rewrite as dated snapshot claims unless
  current external-source refresh evidence is added.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Validator fails because the route model is ambiguous.
  **Fallback**: Update Stage 99 route and validator classification before
  normalizing more documents.
  **Human Escalation**: Required only if the route would change approved
  document taxonomy.
- **Failure Mode**: Cross-links break after a rename or consolidation.
  **Fallback**: Re-run targeted `rg` searches and update links in the same
  logical commit.
  **Human Escalation**: Required if a document must be deleted with no
  replacement.
- **Failure Mode**: External-source currentness conflicts with existing cloud
  example content.
  **Fallback**: Keep the example as a dated snapshot and document that it is
  not provider-latest guidance.
  **Human Escalation**: Required for a provider refresh scope expansion.

## Verification Commands

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

## Success Criteria & Verification Plan

- **VAL-CCDN-001**: Stage 99 support contracts and Stage 00 routing rules
  distinguish README, GitHub-native Markdown, active control surfaces, and
  example-local SDLC snapshot docs.
- **VAL-CCDN-002**: `.github` Markdown and all README files in target scope
  remain frontmatter-free.
- **VAL-CCDN-003**: AWS/Azure example-local non-README Markdown docs have
  type-appropriate frontmatter, no duplicate H1/near-H1 headings, and no
  template placeholder residue.
- **VAL-CCDN-004**: Cross-links and README indexes reflect any renames,
  consolidations, or route changes.
- **VAL-CCDN-005**: Repository quality gates pass, and optional manifest,
  secret, and policy checks are run when their surfaces change.

## Traceability

- **Spec**: [Active Control Surface Governance Hardening](../016-active-control-surface-governance-hardening/spec.md)
- **Spec**: [Template Path Numbering Contract](../019-template-path-numbering-contract/spec.md)
- **Spec**: [SDLC Lifecycle Contract](../021-sdlc-lifecycle-contract/spec.md)
- **Plan**: [../../04.execution/plans/2026-07-06-control-cloud-doc-normalization.md](../../04.execution/plans/2026-07-06-control-cloud-doc-normalization.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-control-cloud-doc-normalization.md](../../04.execution/tasks/2026-07-06-control-cloud-doc-normalization.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Common Documentation Governance**: [../../99.templates/support/common-documentation-governance.md](../../99.templates/support/common-documentation-governance.md)
- **Completed evolution**: [011](../011-template-contract-governance-migration/spec.md) -> [012](../012-template-governance-audit-enhancement/spec.md) -> [013](../013-workspace-document-governance-hardening/spec.md) -> [014](../014-workspace-document-contract-normalization/spec.md) -> [020](../020-workspace-contract-governance-normalization/spec.md) -> [021](../021-sdlc-lifecycle-contract/spec.md) -> [022](./spec.md) -> [023](../023-stage03-04-repo-static-gap-closure/spec.md).
### Related inputs

- **PRD**: No dedicated PRD exists. The controlling input is the approved user
  request to combine active control-surface normalization with AWS/Azure
  example-local SDLC snapshot normalization.
- **ARD**: No new architecture requirement is required because this change is
  a repository documentation and validation contract.
- **Related ADRs**:
  - [Current Local GitOps Platform Contract](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Prior Specs**:
  - [Active Control Surface Governance Hardening](../016-active-control-surface-governance-hardening/spec.md)
  - [Template Path Numbering Contract](../019-template-path-numbering-contract/spec.md)
  - [Workspace Contract Governance Normalization](../020-workspace-contract-governance-normalization/spec.md)
  - [SDLC Lifecycle Contract](../021-sdlc-lifecycle-contract/spec.md)

Official source basis:

- GitHub Actions workflow files are YAML workflow definitions stored under
  `.github/workflows`, so workflow contracts belong to workflow YAML and
  GitHub control documentation:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub Actions secure-use guidance is the external basis for permissions,
  untrusted code, third-party action, and secret-handling review prompts:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- Kubernetes Kustomize is the official basis for declarative manifest
  composition and local manifest validation expectations:
  <https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/>
- Argo CD declarative setup is the official basis for GitOps Application and
  AppProject configuration as Kubernetes manifests:
  <https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/>
- Conftest and OPA are the official basis for policy-as-code checks over
  structured configuration:
  <https://www.conftest.dev/>
  <https://www.openpolicyagent.org/docs>
- External Secrets Operator is the official basis for synchronizing external
  secret providers into Kubernetes Secret resources without committing secret
  values:
  <https://external-secrets.io/latest/introduction/overview/>
