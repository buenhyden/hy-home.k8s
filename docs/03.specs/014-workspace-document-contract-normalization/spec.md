---
title: 'Workspace Document Contract Normalization Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-13
---

# Workspace Document Contract Normalization Technical Specification (Spec)

## Overview

This document defines the technical design and implementation contract for a
second workspace-wide document governance pass. It normalizes active documents,
historical evidence, template forms, support contracts, README profiles,
CI/QA documentation, and repository validation around one coherent
frontmatter, section, and template-routing model.

The approved strategy is full normalization with evidence preservation:
historical documents are actively brought into the current contract shape, but
past facts remain preserved in explicit historical or superseded sections
instead of being deleted.

## Strategic Boundaries & Non-goals

This spec owns repo-static documentation, template, governance, and validator
normalization for these surfaces:

- `_workspace`
- `.github` GitHub-native control Markdown and workflows
- `docs/01.requirements`
- `docs/02.architecture`
- `docs/03.specs`
- `docs/04.execution/plans`
- `docs/04.execution/tasks`
- `docs/05.operations`
- `docs/90.references`
- `docs/98.archive`
- `docs/99.templates`

This spec does not own live Kubernetes, Argo CD, Vault, cloud, paid service,
publishing, push, or merge actions. It also does not introduce a new document
taxonomy outside the existing Stage 00 to Stage 99 model.

## Contracts

- **Config Contract**:
  - Markdown document metadata follows
    [Template Frontmatter Schema](../../99.templates/support/frontmatter-schema.md).
  - Route selection follows
    [Template Routing Contract](../../99.templates/support/template-routing.md).
  - README files remain frontmatter-free unless a future support contract
    explicitly changes that rule.
  - GitHub-native control Markdown under `.github/ABOUT.md`,
    `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/SECURITY.md` remains
    frontmatter-free and mirrors canonical owners instead of becoming authored
    stage documentation.
  - Native machine contracts remain native: OpenAPI as YAML, GraphQL as SDL,
    and protobuf as `.proto`.
- **Data / Interface Contract**:
  - Each routed Markdown path maps to one template family.
  - Each Markdown document type has a canonical frontmatter key set and order.
  - Each document family has canonical required sections.
  - Historical evidence must be distinguishable from current instructions.
- **Governance Contract**:
  - Support contracts own reusable template rules.
  - Stage 00 owns agent-facing execution policy and protected-surface rules.
  - README files summarize and link; they do not duplicate long governance
    bodies.
  - Validators enforce deterministic drift only, with path-scoped exclusions
    when necessary and documented.

## Core Design

- **Component Boundary**:
  - `docs/99.templates/support/**` defines contract sources.
  - `docs/99.templates/templates/**` defines authoring forms.
  - Active SDLC documents hold current repository facts and delivery evidence.
  - Historical documents hold preserved past evidence in normalized sections.
  - `scripts/validate-repo-quality-gates.sh` enforces deterministic rules.
  - `.github` and CI/QA docs describe actual automation behavior without
    duplicating template contracts.
- **Key Dependencies**:
  - Existing repository quality gates and harness validation.
  - Existing Stage 00 governance routing.
  - Existing Stage 03/04 spec-plan-task traceability.
  - Official external specifications for CI/CD, supply-chain evidence,
    Markdown/YAML formatting, and machine-readable API contracts.
- **Tech Stack**:
  - Markdown with YAML frontmatter for authored documents.
  - Bash and embedded Python for repository validation.
  - GitHub Actions YAML for CI workflows.
  - OpenAPI, GraphQL SDL, and proto3 for feature-local machine contracts.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Treat each document as an entity with `path`, `route`, `template`,
    `profile`, `frontmatter`, `required_sections`, and `evidence_class`.
  - `evidence_class` is one of `current`, `historical`, `superseded`,
    `generated`, or `native-machine-contract`.
  - Historical evidence is normalized by adding explicit sections such as
    `Historical Context`, `Evidence`, or `Superseded Contract` where the old
    text might otherwise read as current instruction.
- **Migration / Transition Plan**:
  - Audit first, then normalize contracts, then apply active docs, then apply
    historical evidence, then reconcile references and CI/QA, then finalize
    validator gates.
  - Each phase creates one logical commit and receives independent spec and
    quality review.
  - Existing evidence is preserved unless it is duplicate, misleading as
    current guidance, or invalid under the target template contract.

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface DocumentContractProfile {
  pathPattern: string;
  templatePath: string;
  frontmatterType: string | null;
  requiredKeys: string[];
  requiredSections: string[];
  evidenceClass: 'current' | 'historical' | 'superseded' | 'generated' | 'native-machine-contract' | 'repository-control';
  validatorScope: 'active' | 'historical' | 'generated' | 'native' | 'control';
}

interface NormalizationFinding {
  path: string;
  category: 'frontmatter' | 'section' | 'route' | 'template-residue' | 'ci-qa' | 'formatting';
  severity: 'blocking' | 'important' | 'advisory';
  currentState: string;
  targetContract: string;
  remediation: string;
}
```

### API Contract

No external API is introduced. Existing API contract templates remain in
`docs/99.templates/templates/sdlc/specs/` and must stay aligned with official
OpenAPI, GraphQL, and Protocol Buffers specifications.

- **API Spec**: Not applicable for this governance normalization.
- **Policy**: Native API contracts remain under their owning feature directory.
- **Machine-readable Contract**:
  - `docs/99.templates/templates/sdlc/specs/openapi.template.yaml`
  - `docs/99.templates/templates/sdlc/specs/schema.template.graphql`
  - `docs/99.templates/templates/sdlc/specs/service.template.proto`

### Agent Role & IO Contract

- **Agent Role**:
  - The controller uses subagent-driven development for implementation tasks.
  - Each implementation subagent owns one logical task and commit.
  - Each task receives a spec compliance review before quality review.
- **Inputs**:
  - This spec.
  - The implementation plan and task record created from this spec.
  - Current repository contracts and focused scan outputs.
  - Official external sources listed in this spec.
- **Outputs**:
  - Audit evidence.
  - Contract and template updates.
  - Authored document normalization.
  - Validator updates.
  - Plan, task, and progress evidence.
- **Success Definition**:
  - All six logical tasks complete with passing validation and independent
    review.

### Tools & Tool Contract

- **Tool List**:
  - `rg`, `rg --files`, `find`, `sed`, `git`, `bash`, `jq`, and repository
    validation scripts.
  - Web research only for current external official sources or standards.
  - Multi-agent tools for implementation and review tasks.
- **Permission Boundary**:
  - Repo-static file changes are allowed.
  - Live runtime mutation, secret value inspection, external publishing,
    remote push, and merge are excluded unless separately approved.
- **Failure Handling**:
  - If a validator change rejects valid historical evidence, first normalize
    the document into current/historical sections. If false positives remain,
    add a path-scoped allow-list with documented rationale.
  - If a task is too large, split it by document family before proceeding.

### Prompt / Policy Contract

- **System / Instruction Contract**:
  - Follow Stage 00 governance and Stage 99 template support contracts.
  - Do not treat README files as contract bodies.
  - Do not let historical evidence read as current operating guidance.
- **Policy Constraints**:
  - Use official or primary sources for external claims.
  - Keep SDLC documents under `docs`.
  - Use logical-unit commits.
  - Keep GitHub-native control Markdown frontmatter-free and route durable
    policy to canonical owners.
  - Preserve user or prior-agent changes unless this spec explicitly requires
    normalization of the same surface.
- **Versioning Rule**:
  - External-source claims include links and should be refreshed when official
    specifications or workflow behavior changes.

### Memory & Context Strategy

- **Short-term Context**:
  - Each subagent receives the specific task text, relevant path list,
    expected validations, and current base commit.
- **Long-term Memory**:
  - Repo-changing work appends progress to
    `docs/00.agent-governance/memory/progress.md`.
- **Retrieval Boundary**:
  - Historical progress and audit entries are evidence, not current rule
    sources, unless linked from active governance or support contracts.

### Guardrails

- **Input Guardrails**:
  - Inspect current repository state before each task.
  - Use route and frontmatter support contracts as source of truth.
  - Treat archive, progress, and audit records as normalizable but evidentiary.
- **Output Guardrails**:
  - No template placeholders remain in authored documents.
  - No duplicate current-rule bodies are added to README files.
  - No unsupported frontmatter keys remain in normalized documents.
  - No current active document points to legacy routes as the current contract.
- **Blocked Conditions**:
  - Repeated validator false positives that cannot be scoped safely.
  - Conflicting support contracts where no canonical owner can be determined.
  - Missing official source for a time-sensitive external claim.
- **Escalation Rule**:
  - Stop and ask if a document must be deleted rather than normalized and the
    deletion would remove unique historical evidence.

### Evaluation

- **Eval Types**:
  - Contract parity checks.
  - Frontmatter profile checks.
  - Section coverage checks.
  - Template residue scans.
  - README profile checks.
  - CI/QA workflow-documentation consistency checks.
- **Metrics**:
  - Zero active route/profile contradictions.
  - Zero authored template residue outside template files.
  - Zero README frontmatter instances.
  - Zero unreviewed validator false positives.
  - All required local gates pass.
- **Datasets / Fixtures**:
  - Current repository documents under the target scope.
  - Existing `docs/99.templates/templates/**` forms.
  - Existing `.github/workflows/**` workflows.
- **How to Run**:
  - Run focused scans per task.
  - Run repository gates before every commit.
  - Run final subagent review over the branch.

## Edge Cases & Error Handling

- **Old task or plan records contain obsolete commands**:
  - Keep the command as evidence, but move it under historical evidence or
    clearly label it as superseded when the current command differs.
- **Archive Tombstone lacks a modern section**:
  - Normalize the Tombstone shape without changing the fact that the document
    is archived.
- **Progress ledger contains legacy strings**:
  - Preserve chronological evidence, but ensure current progress entries and
    validator rules distinguish old evidence from current instructions.
- **GitHub-native control Markdown looks like a document**:
  - Keep it frontmatter-free, validate it as a control surface, and route
    durable policy to Stage 00, Stage 05, scripts, or workflow owners.
- **Template support and validator disagree**:
  - Fix the support contract first, then template forms, then authored docs,
    then validator mappings.
- **External standard has a newer version than the repo baseline**:
  - Record the current official source and decide whether to update the repo
    contract or keep the old version with a stated compatibility boundary.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A broad normalization task creates excessive diff noise.
  - **Fallback**: Split by document family and commit smaller units.
  - **Human Escalation**: Ask only if a preserved historical record must be
    deleted or rewritten beyond section normalization.
- **Failure Mode**: Validator rejects generated or native contract files.
  - **Fallback**: Restrict the validator path scope and document the native
    contract exception.
  - **Human Escalation**: Ask if the native contract itself must be redesigned.
- **Failure Mode**: CI/QA documentation and workflow behavior disagree.
  - **Fallback**: Treat `.github/workflows/ci.yml` and repository scripts as
    repo-local truth, then update docs and validator language.
  - **Human Escalation**: Ask before changing actual CI triggers or remote
    branch policy.

## Verification Commands

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
```

If GitOps, infrastructure, policy, examples YAML, tests, or Traefik files are
changed, also run:

```bash
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Contract sources agree.
  - `docs/99.templates/support/**`, template forms, Stage 00 routing docs, and
    validator route/profile maps describe the same document families.
- **VAL-SPC-002**: Active SDLC documents are normalized.
  - `docs/01.requirements` through `docs/05.operations` match their route,
    frontmatter, and section contracts.
- **VAL-SPC-003**: Historical evidence is normalized and preserved.
  - `docs/98.archive`, old Stage 04 records, audits, and progress entries keep
    evidence while separating historical or superseded content from current
    instructions.
- **VAL-SPC-004**: References and generated knowledge surfaces are aligned.
  - `docs/90.references/{research,audits,data,llm-wiki,learning}` expose clear
    roles, source boundaries, review freshness, and generated-index contracts.
- **VAL-SPC-005**: CI/QA and formatting claims match source truth.
  - `.github`, CI/QA guide, scripts README, and tests README agree with
    workflows and local validation scripts.
- **VAL-SPC-006**: Validator enforces deterministic drift.
  - New checks are path-scoped, explain failures by drift class, and avoid
    false positives on valid evidence or native machine contracts.
- **VAL-SPC-007**: Review gates pass.
  - Every task receives spec compliance and code quality review, and the final
    branch review returns ready or all findings are remediated.

## Traceability

- **PRD**: No separate PRD; upstream requirement is the approved user request in
  this thread.
- **ARD**: No separate ARD; Stage 00 and Stage 99 contracts are the architecture
  baseline.
- **Related ADRs**:
  - [Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
  - [Current Local GitOps Platform Contract](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Prior Specs**:
  - [Template Contract Governance Migration](../011-template-contract-governance-migration/spec.md)
  - [Template Governance Audit Enhancement](../012-template-governance-audit-enhancement/spec.md)
  - [Workspace Document Governance Hardening](../013-workspace-document-governance-hardening/spec.md)
- **Plan**: planned path
  `docs/04.execution/plans/2026-07-04-workspace-document-contract-normalization.md`.
- **Tasks**: planned path
  `docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md`.
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- **Completed evolution**: [011](../011-template-contract-governance-migration/spec.md) -> [012](../012-template-governance-audit-enhancement/spec.md) -> [013](../013-workspace-document-governance-hardening/spec.md) -> [014](./spec.md) -> [020](../020-workspace-contract-governance-normalization/spec.md) -> [021](../021-sdlc-lifecycle-contract/spec.md) -> [022](../022-control-cloud-doc-normalization/spec.md) -> [023](../023-stage03-04-repo-static-gap-closure/spec.md).
### Related inputs

- **PRD**: No separate PRD exists. The user request in this Codex thread is the
  upstream requirement and explicitly authorizes destructive document
  normalization, contract and governance changes, external-source-backed
  improvements, subagents, and logical-unit commits.
- **ARD**: No separate ARD exists. The current architecture baseline is the
  Stage 00 governance model and the Stage 99 template support contract set.
- **Related ADRs**:
  - [Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
  - [Current Local GitOps Platform Contract](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Prior Specs**:
  - [Template Contract Governance Migration](../011-template-contract-governance-migration/spec.md)
  - [Template Governance Audit Enhancement](../012-template-governance-audit-enhancement/spec.md)
  - [Workspace Document Governance Hardening](../013-workspace-document-governance-hardening/spec.md)

### External reference basis

- [GitHub Actions documentation](https://docs.github.com/actions)
- [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [SLSA provenance](https://slsa.dev/provenance)
- [SLSA build provenance](https://slsa.dev/spec/draft/build-provenance)
- [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- [CommonMark](https://commonmark.org/)
- [YAML 1.2.2 Specification](https://yaml.org/spec/1.2.2/)
- [OpenAPI Specification](https://spec.openapis.org/oas/)
- [GraphQL Specification](https://spec.graphql.org/)
- [Protocol Buffers proto3 Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [GitHub Spec Kit Documentation](https://github.github.com/spec-kit/)
- [OWASP SAMM](https://owasp.org/www-project-samm/)
- [Atlassian SDLC overview](https://www.atlassian.com/agile/software-development/sdlc)
