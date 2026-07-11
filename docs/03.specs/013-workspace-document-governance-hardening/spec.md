---
title: 'Workspace Document Governance Hardening Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-11
---

# Workspace Document Governance Hardening Technical Specification (Spec)

## Overview

This document defines the technical design for hardening document type
contracts, frontmatter profiles, template governance, provider entrypoints,
and repository-wide documentation quality gates across `hy-home.k8s`.

The work extends the completed template contract migration and template
governance audit enhancement. It does not start by rewriting every document.
It first inventories current drift, then tightens the canonical contracts, then
applies safe changes to provider entrypoints and workspace documentation.

## Strategic Boundaries & Non-goals

This spec owns repo-static documentation and governance hardening for:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, and `DESIGN.md` when
  present.
- Shared and provider-specific agent surfaces under `.agents`, `.claude`, and
  `.codex`.
- GitHub automation documentation under `.github`.
- Canonical docs under `docs`, including `00.agent-governance`,
  `99.templates`, and authored stages.
- Repository documentation under `examples`, `gitops`, `infrastructure`,
  `policy`, `scripts`, `tests`, and `traefik`.
- Static QA and CI/CD documentation and validator coverage.

This spec does not own:

- Live Kubernetes, Argo CD, Vault, PostgreSQL, Valkey, or cloud resource
  mutation.
- Secret value inspection.
- Container publishing, release publishing, or external account changes.
- A bulk rewrite of historical evidence where an archive Tombstone or current
  overlay is safer.
- Introducing a new top-level `docs/` folder outside the existing taxonomy.

## Related Inputs

- **PRD**: No dedicated PRD exists. The user request and prior approved
  template governance work are the active requirements input.
- **ARD**: No dedicated ARD exists. Current architecture constraints are
  inherited from the Stage 00 canonical adapter model and local GitOps platform
  contract.
- **Related ADRs**:
  - [ADR-0013: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
  - [ADR-0014: Current Local GitOps Platform Contract](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Prior Specs**:
  - [Template Contract Governance Migration](../011-template-contract-governance-migration/spec.md)
  - [Template Governance Audit Enhancement](../012-template-governance-audit-enhancement/spec.md)
- **Research and Audit Inputs**:
  - [Workspace Governance Baseline Research](../../90.references/research/2026-07-04-wer/workspace-governance-baseline.md)
  - [Spec SDLC CI QA Formatting Research](../../90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md)
  - [Workspace Governance Implementation Audit](../../90.references/audits/2026-07-02-whia/workspace-governance-implementation-audit.md)
  - [SDLC Delivery Practices Implementation Audit](../../90.references/audits/2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md)

## Contracts

- **Config Contract**: The authoritative route and metadata configuration
  remains documented in `docs/99.templates/support/**`, Stage 00 governance,
  and `scripts/validate-repo-quality-gates.sh`.
- **Data / Interface Contract**: Audit inventories must be derived from tracked
  files and recorded as Markdown evidence, not as hidden local state.
- **Governance Contract**: README files are entrypoints and inventories.
  Reusable rules belong in template support docs or Stage 00 governance.
  Provider shims must point to common governance instead of duplicating it.

## Core Design

- **Component Boundary**:
  - Audit inventory: scan current files for frontmatter, README sections,
    template routing, provider shims, CI/QA surfaces, and stale or legacy text.
  - Core contract hardening: align `docs/99.templates/support/**`,
    `docs/99.templates/templates/**`, Stage 00 routing rules, and the validator.
  - Provider entry hardening: align `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
    `.agents`, `.claude`, and `.codex` as thin provider overlays on shared
    governance.
  - Workspace application: apply safe, topic-specific section and metadata
    fixes to authored docs and README files.
  - Verification and review: run local gates and use sub-agent reviews for
    template/schema, provider, and workspace-wide quality checks.
- **Key Dependencies**:
  - Existing template routing and frontmatter schema.
  - Existing repo-quality validator.
  - GitHub Actions CI gate definitions.
  - Official external documentation for CI/CD, supply-chain security, document
    formatting, GitOps, API contracts, and agent context files.
- **Tech Stack**:
  - Markdown, YAML, shell, Python embedded in shell validators, GitHub Actions,
    Kubernetes manifest conventions, and provider-specific agent files.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Document type profile: `path pattern`, `template`, `frontmatter keys`,
    `allowed type`, `allowed status`, `owner`, and `required sections`.
  - README profile: `path`, `audience`, `scope`, `structure`, `workflow`,
    `link basis`, and `related documents`, without frontmatter.
  - Provider profile: `provider shim`, `shared asset path`, `provider-specific
    runtime path`, `governance owner`, and `validation surface`.
  - CI/QA profile: `workflow`, `trigger`, `permissions`, `local equivalent`,
    `evidence`, and `boundary`.
- **Migration / Transition Plan**:
  - Do not add a new data store.
  - Record audit findings in Stage 04 task evidence or a Stage 90 audit
    report if the findings need durable lookup value.
  - Convert repeated findings into validator checks where deterministic.
  - Archive rather than rewrite old docs when current implementation and old
    evidence conflict.

## Interfaces & Data Structures

### Core Interfaces

The implementation plan should treat these as the durable interfaces:

```yaml
document_profile:
  path_pattern: string
  template_path: string
  frontmatter_type: string
  frontmatter_required_keys:
    - title
    - type
    - status
    - owner
    - updated
  readme_frontmatter: false
  required_sections: list

provider_surface:
  shim_file: string
  provider_runtime_file: string
  shared_assets:
    - .agents/skills
    - .agents/workflows
    - .agents/output-styles
  governance_owner: docs/00.agent-governance

validation_surface:
  local_commands: list
  ci_jobs: list
  protected_surface: list
  approval_required_for_live_actions: true
```

## API Contract (If Applicable)

This feature exposes no external runtime API.

- **API Spec**: Not applicable.
- **Policy**: Machine-readable API contracts remain feature-local under
  `docs/03.specs/<###-Numbering>-<feature-id>/contracts/` when needed by future work.
- **Machine-readable Contract**: Not applicable.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Agents inspect, edit, and validate repository files only.
- **Inputs**:
  - User-approved scope and constraints.
  - Existing repository governance and template contracts.
  - Official external references for current best practices.
  - Static scans from tracked files.
- **Outputs**:
  - Updated Stage 03/04 design and execution evidence.
  - Hardened template/governance/provider contracts.
  - Topic-specific document fixes.
  - Validator-backed checks where deterministic.
- **Success Definition**: The repository has one documented role for each
  document type, one route for each target pattern, provider shims remain thin,
  README files do not duplicate contracts, and local gates pass.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - `rg` and `git ls-files` for repository scans.
  - `bash scripts/validate-repo-quality-gates.sh .` for repo quality.
  - `git diff --check` for whitespace and patch hygiene.
  - `bash scripts/validate-harness.sh` when the change affects multiple
    harness surfaces.
  - Manifest and policy scripts when GitOps, infrastructure, policy, examples,
    or Traefik YAML changes.
  - Sub-agents for independent audit and review tasks.
- **Permission Boundary**:
  - Networked tools are read-only for research unless the user explicitly
    approves an external action.
  - No live cluster mutation, secret value inspection, publish, push, or merge
    without explicit approval.
- **Failure Handling**:
  - If validators fail, fix the deterministic rule or the document drift before
    proceeding.
  - If external facts are uncertain or time-sensitive, verify with official
    sources and record the source boundary.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
  - Follow repository AGENTS instructions and Stage 00 governance.
  - Use Superpowers brainstorming before implementation and subagent-driven
    development when a written implementation plan exists.
- **Policy Constraints**:
  - Do not create unapproved top-level docs folders.
  - Do not leave template instructions, placeholders, or support-rule prose in
    authored documents.
  - Do not add README sections that belong in contract or governance documents.
- **Versioning Rule**:
  - External source claims must include source links and freshness boundaries.
  - Version inventory changes must update the owning Stage 90 data document.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 plan and task records own implementation
  sequencing, findings, and validation evidence.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  repo-changing progress entries.
- **Retrieval Boundary**: Durable lookup material belongs in
  `docs/90.references/**`; active execution policy belongs in Stage 00 or
  template support contracts.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Treat the current passing gate state as a baseline.
  - Separate examples from canonical runtime contracts.
  - Separate provider-specific runtime behavior from shared governance.
- **Output Guardrails**:
  - Keep authored documents topic-specific.
  - Keep README files frontmatter-free.
  - Keep support contracts current-state, not migration-history prose.
  - Keep operations policy, guide, runbook, incident, and postmortem roles
    separate.
- **Blocked Conditions**:
  - A validator failure that cannot be resolved without changing the approved
    scope.
  - Conflicting user instructions about live mutation, secret handling, or
    destructive cleanup.
  - Need for external account mutation without approval.
- **Escalation Rule**: Stop and ask the user when a destructive change, live
  runtime action, or ambiguous governance conflict cannot be resolved from
  repository evidence.

## Evaluation (If Applicable)

- **Eval Types**:
  - Static validation.
  - Route coverage and exactly-one-template matching.
  - Frontmatter profile conformance.
  - README section conformance.
  - Provider shim and shared asset consistency.
  - CI/QA local-vs-remote contract consistency.
- **Metrics**:
  - Zero `git diff --check` failures.
  - Zero repo-quality gate failures.
  - Zero uncovered active authored stage documents.
  - Zero README frontmatter violations.
  - Zero active legacy template route references outside allowed historical
    evidence.
- **Datasets / Fixtures**:
  - Tracked repository files.
  - Template routing tables.
  - Frontmatter schema table.
  - GitHub workflow definitions.
- **How to Run**:
  - Run the verification commands in this spec and in the owning Stage 04 plan.

## Edge Cases & Error Handling

- **Examples docs mirror canonical stages**: Treat `examples/**/docs` as
  example-local documentation unless the validator explicitly includes it in a
  canonical profile. Do not silently promote example docs to active platform
  contracts.
- **Historical progress text contains old terms**: Preserve historical evidence
  when it is clearly historical. Add active-doc denylist checks only where the
  context is current contract prose.
- **Provider capabilities differ**: Keep provider-specific details in provider
  docs and keep common policy in Stage 00. Do not force Claude hooks, Codex
  sandbox behavior, and Gemini context files into a false common runtime.
- **Template path changes affect generated docs**: Update routing docs,
  README indexes, validator mappings, and safe authored document headings in
  the same logical unit.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A broad scan finds many drift classes that cannot fit in a
  single safe commit.
  - **Fallback**: Convert the scan into an audit inventory and split execution
    into additional Stage 04 tasks.
  - **Human Escalation**: Ask whether to prioritize contract, provider, or
    workspace application work.
- **Failure Mode**: External official guidance conflicts with current repo
  contracts.
  - **Fallback**: Record the difference in research or audit evidence and keep
    current repo behavior until a scoped migration is approved.
  - **Human Escalation**: Ask before changing protected surfaces.
- **Failure Mode**: Validator requires a rule that would create false positives
  in historical evidence.
  - **Fallback**: Scope the validator to active docs or add explicit historical
    allow-lists with comments.
  - **Human Escalation**: Ask only if the active/historical boundary is not
    inferable from path or document status.

## Verification Commands

Required baseline commands:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Use the full harness bundle when provider, template, GitHub, script, or
multi-surface governance changes are complete:

```bash
bash scripts/validate-harness.sh
```

Use manifest and policy checks when YAML, GitOps, infrastructure, policy,
examples, secrets, tests, or Traefik surfaces change:

```bash
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

## Success Criteria & Verification Plan

- **VAL-WDGH-001**: The Stage 04 plan contains separate logical tasks for
  audit inventory, core contract hardening, provider entry hardening,
  workspace application, and final validation.
- **VAL-WDGH-002**: `docs/99.templates/support/**`,
  `docs/99.templates/templates/**`, Stage 00 governance, and
  `scripts/validate-repo-quality-gates.sh` describe the same document type and
  routing rules.
- **VAL-WDGH-003**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents`,
  `.claude`, and `.codex` remain thin provider entrypoints with common rules
  routed through Stage 00.
- **VAL-WDGH-004**: README files stay frontmatter-free and do not duplicate
  contract bodies that belong in support or governance documents.
- **VAL-WDGH-005**: Authored SDLC, reference, archive, and governance Markdown
  files use the frontmatter profile required by their document type.
- **VAL-WDGH-006**: CI/CD and QA documentation matches `.github/workflows`,
  `scripts/README.md`, `tests/README.md`, and the local validation scripts.
- **VAL-WDGH-007**: Deterministic drift classes are enforced by validators or
  recorded as explicit deferred items when automation would be noisy.
- **VAL-WDGH-008**: Final `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .` pass.

## External Reference Basis

The implementation plan should prefer official sources and record dated
freshness when claims depend on external tooling behavior:

- [GitHub Actions documentation](https://docs.github.com/actions) for CI/CD
  workflow structure and permissions.
- [OpenSSF Scorecard](https://scorecard.dev/) for supply-chain security check
  categories.
- [SLSA build provenance](https://slsa.dev/spec/draft/build-provenance) for
  artifact provenance concepts.
- [CommonMark](https://commonmark.org/) and
  [YAML 1.2.2](https://yaml.org/spec/1.2.2/) for text and data format
  consistency.
- [Kubernetes declarative configuration](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
  and [Argo CD documentation](https://argo-cd.readthedocs.io/) for GitOps and
  declarative desired-state boundaries.
- [OpenAPI Specification](https://swagger.io/specification/),
  [GraphQL Schema documentation](https://graphql.org/learn/schema/), and
  [Protocol Buffers proto3 guide](https://protobuf.dev/programming-guides/proto3/)
  for machine-readable contract boundaries.
- [Codex AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md),
  [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide), and
  [Gemini CLI GEMINI.md guidance](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html)
  for provider-specific agent entrypoint behavior.

## Related Documents

- [Docs Hub](../../README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- [Template Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [SDLC Template Governance](../../99.templates/support/sdlc-governance.md)
- [Common Documentation Governance](../../99.templates/support/common-documentation-governance.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../scripts/README.md)
- [GitHub Configuration Hub](../../../.github/ABOUT.md)
- [Plan](../../04.execution/plans/2026-07-03-workspace-document-governance-hardening.md)
- [Task](../../04.execution/tasks/2026-07-03-workspace-document-governance-hardening.md)
- **Completed evolution**: [011](../011-template-contract-governance-migration/spec.md) -> [012](../012-template-governance-audit-enhancement/spec.md) -> [013](./spec.md) -> [014](../014-workspace-document-contract-normalization/spec.md) -> [020](../020-workspace-contract-governance-normalization/spec.md) -> [021](../021-sdlc-lifecycle-contract/spec.md) -> [022](../022-control-cloud-doc-normalization/spec.md) -> [023](../023-stage03-04-repo-static-gap-closure/spec.md).
