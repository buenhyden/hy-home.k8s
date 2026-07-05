---
title: 'Workspace Harness Research Pack Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-02
---

# Workspace Harness Research Pack Technical Specification (Spec)

---

## Overview

This document defines the design contract for a durable research pack under
`docs/90.references/research/`. The pack will summarize the current
`hy-home.k8s` workspace purpose, governance, CI/CD, QA, automation, formatting,
templates, scripts, SDLC, and operating contract, then compare those repo-backed
findings with official external sources, market scan material, and practical
implementation checklist guidance.

The requested output is documentation-only. It does not change GitOps desired
state, live cluster state, credentials, CI enforcement semantics, or provider
runtime policy.

## Strategic Boundaries & Non-goals

This spec owns the research-pack structure, source-selection rules, analysis
boundaries, and verification contract for the requested reference documents.

In scope:

- Create a compact integrated research pack: one README plus four reference
  documents.
- Preserve repo-first analysis from current governance, CI/QA, template, script,
  and runtime evidence.
- Use official external sources first for Claude, Codex/OpenAI, Gemini/Google,
  spec-driven development, SDLC, CI/CD, QA, and formatting references.
- Include a bounded market scan for current agent-harness, agent-loop, and AI
  software-delivery patterns.
- Include implementation checklist sections that translate research into
  workspace-applicable controls and next-step checks.
- Keep `docs/90.references/**` as durable lookup material, not as a new policy
  or runtime enforcement source.

Out of scope:

- Live k3d, ArgoCD, Vault, ESO, or Kubernetes mutation.
- Publishing, pushing, opening PRs, or changing third-party resources without
  explicit human approval.
- Replacing canonical Stage 00 governance, CI workflow, scripts, templates, or
  provider adapters.
- Creating parallel documentation trees such as `docs/superpowers/**`.
- Treating market-scan material as authoritative when it conflicts with
  official vendor or repo-backed sources.

## Related Inputs

- **Workspace gateway**: `../../AGENTS.md`
- **Bootstrap governance**: `../../00.agent-governance/rules/bootstrap.md`
- **Documentation routing**: `../../00.agent-governance/rules/document-stage-routing.md`
- **Documentation protocol**: `../../00.agent-governance/rules/documentation-protocol.md`
- **Harness catalog**: `../../00.agent-governance/harness-catalog.md`
- **Harness implementation map**: `../../00.agent-governance/harness-implementation-map.md`
- **CI/CD and QA guide**: `../../05.operations/guides/0010-ci-cd-qa-reference-guide.md`
- **Prior harness audit reference**: `../../90.references/audits/2026-05-24-whga/workspace-harness-gap-analysis.md`

## Contracts

- **Config Contract**: No repository configuration or runtime settings change is
  required. The research pack must route to `docs/90.references/research/` and
  use `docs/99.templates/templates/common/reference.template.md` for non-README documents.
- **Data / Interface Contract**: The pack consists of Markdown reference
  documents with frontmatter, source/freshness metadata, authority boundaries,
  definitions/facts, and related-document links.
- **Governance Contract**: The pack must not redefine active governance. Any
  implementation recommendations must be framed as checklist items or candidate
  follow-up work, with canonical owners named for actual policy changes.

## Core Design

- **Component Boundary**:
  - `docs/90.references/research/README.md`: folder entrypoint, index, and
    reading order.
  - `workspace-governance-baseline.md`: repo-first baseline covering purpose,
    roles, governance, operating contract, templates, scripts, automation, and
    current evidence lanes.
  - `harness-and-loop-engineering.md`: definitions, external-source analysis,
    market scan, and applicability checklist for harness engineering and loop
    engineering.
  - `provider-implementation-status.md`: Claude, Codex/OpenAI, and
    Gemini/Google implementation status for harness and loop capabilities,
    including shared-environment construction patterns and known differences.
  - `spec-sdlc-ci-qa-formatting.md`: spec-driven development, SDLC, CI/CD, QA,
    formatting, and verification patterns, mapped back to this repository.
- **Key Dependencies**:
  - Repo-backed Stage 00 governance, CI workflow, scripts, templates, and
    existing reference docs.
  - Official vendor documentation and standards sources for provider and
    delivery-practice claims.
  - Bounded market scan sources for non-authoritative trends and implementation
    examples.
- **Tech Stack**: Markdown, existing docs templates, repository validation
  scripts, Git commit history, and web-sourced citations.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each reference document follows the existing
  reference template fields: `Overview`, `Purpose`, `Reference Type`,
  `Authority Boundary`, `Scope`, `Definitions / Facts`, `Sources`,
  `Review and Freshness`, and `Related Documents`.
- **Migration / Transition Plan**: No migration is required. The new `research/`
  folder extends the existing `90.references` taxonomy and requires updates to
  the parent `docs/90.references/README.md`.

## Interfaces & Data Structures

### Research Pack Document Contract

```typescript
interface ResearchReferenceDocument {
  frontmatter: {
    title: string;
    type: "reference";
    status: "draft";
    owner: "platform";
    updated: "2026-07-02";
  };
  requiredSections: [
    "Overview",
    "Purpose",
    "Reference Type",
    "Authority Boundary",
    "Scope",
    "Definitions / Facts",
    "Sources",
    "Review and Freshness",
    "Related Documents",
  ];
  analysisBlocks: {
    repoFirstFindings: string[];
    officialSourceFindings: string[];
    marketScanFindings: string[];
    implementationChecklist: string[];
  };
}
```

## API Contract (If Applicable)

No external API is introduced.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation and governance researcher operating under the
  repo-local docs, meta, and QA scopes.
- **Inputs**: Repository governance/docs/scripts/CI evidence, user-approved
  integrated pack structure, official external sources, bounded market scan
  sources.
- **Outputs**: Five Markdown files under `docs/90.references/research/`, parent
  README updates, progress ledger updates, validation evidence, and logical
  commits.
- **Success Definition**: The pack gives future agents and maintainers a
  source-attributed, repo-aligned research baseline without creating conflicting
  policy.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `sed`, `git`, `apply_patch`, web search/browsing, and
  repository validation scripts.
- **Permission Boundary**: External sources are read-only. No posting,
  publishing, pushing, paid jobs, credentials changes, or third-party resource
  mutation may occur without explicit approval.
- **Failure Handling**: If official sources conflict with market-scan sources,
  prefer official sources and record market findings as non-authoritative. If a
  repo validation gate fails, fix the smallest affected document or report the
  scoped blocker.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Follow repo JIT governance, template-first
  authoring, and the `docs-stage-routing` contract.
- **Policy Constraints**: Human-facing explanatory prose may use Korean;
  authority, source, freshness, and AI-agent routing fields stay English-first.
- **Versioning Rule**: All external claims must include the source-checked date
  and a refresh trigger because provider capabilities and product names change.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Use the current task plan and fetched sources while
  writing the research pack.
- **Long-term Memory**: Append concise reusable lessons and evidence to
  `../../00.agent-governance/memory/progress.md`.
- **Retrieval Boundary**: `docs/90.references/research/` stores durable
  lookup material; active policy remains in `docs/00.agent-governance/**`.

## Guardrails (If Applicable)

- **Input Guardrails**: Verify current provider claims through browsing before
  writing implementation-status sections.
- **Output Guardrails**: Avoid long verbatim quotations, secret exposure,
  invented citations, and policy duplication.
- **Blocked Conditions**: Missing template coverage, unresolved source
  conflicts on material claims, or failed repository validation with no scoped
  remediation.
- **Escalation Rule**: Ask the human before changing canonical governance,
  live-runtime behavior, CI enforcement semantics, or external resources.

## Evaluation (If Applicable)

- **Eval Types**: Repository-static validation, link/template conformance,
  source attribution review, and checklist coverage review.
- **Metrics**:
  - Every requested topic appears in at least one reference document.
  - Every reference document contains official sources and a source-checked
    date.
  - Market-scan findings are clearly labeled non-authoritative.
  - Implementation checklist items name the canonical repo owner or follow-up
    route.
- **Datasets / Fixtures**: Existing governance docs, CI workflow, scripts,
  templates, prior audit reference, and fetched external sources.
- **How to Run**: Use the verification commands below.

## Edge Cases & Error Handling

- **External source drift**: Provider docs may change after authoring. Record
  `Source checked: 2026-07-02` and refresh triggers tied to provider release
  notes or major governance changes.
- **Conflicting terminology**: Normalize local meanings around the repo's
  four-element harness model while acknowledging vendor-specific terms.
- **Reference-vs-policy ambiguity**: Keep recommendations as checklists and
  route policy changes to Stage 00 or operations policy in future work.
- **README sync drift**: Update both `docs/90.references/README.md` and the new
  `research/README.md` when the folder is created.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Web research cannot verify a provider implementation claim.
  **Fallback**: Mark the claim unknown or omit it; do not infer current status.
  **Human Escalation**: Ask for an approved source if the claim is required.
- **Failure Mode**: Repo validation fails due to new reference structure.
  **Fallback**: Adjust documents to the existing template/readme contract.
  **Human Escalation**: Ask before changing validators or template mappings.
- **Failure Mode**: Market scan suggests a tool or framework outside the repo
  boundary.
  **Fallback**: Record it as optional comparative context only.
  **Human Escalation**: Ask before installing, configuring, or integrating it.

## Verification Commands

```bash
git diff --check
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-repo-quality-gates.sh .
```

Additional checks when relevant:

```bash
bash -n scripts/validate-repo-quality-gates.sh
rg --files | rg '(^|/)progress\.md$'
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `docs/90.references/research/README.md` exists and indexes
  the four reference documents with reading order and authority boundaries.
- **VAL-SPC-002**: The four reference documents exist, use the reference
  template structure, include source/freshness metadata, and contain no
  placeholder text.
- **VAL-SPC-003**: The pack covers workspace purpose, roles, CI/CD, QA,
  automation, overview, formatting, operating contract, templates, scripts,
  integration guides, SDLC, governance, system, and rules.
- **VAL-SPC-004**: Harness engineering, loop engineering, repo application
  requirements, Claude/Codex/Gemini implementation status, shared environment
  construction, spec-driven development, SDLC, CI/CD, QA, and formatting are
  all covered with official-source and market-scan context.
- **VAL-SPC-005**: The implementation checklist sections avoid redefining
  active policy and instead name canonical owners or follow-up routes.
- **VAL-SPC-006**: Repository-static validation passes or any limitation is
  documented with scoped remediation.

## Related Documents

- **Workspace governance platform PRD**: `../../01.requirements/003-workspace-agent-governance-platform.md`
- **Workspace governance ARD**: `../../02.architecture/requirements/0006-workspace-agent-governance-platform.md`
- **Canonical adapter ADR**: `../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md`
- **Existing harness gap-analysis spec**: `../006-workspace-harness-gap-analysis/spec.md`
- **Execution plan**: `../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md`
- **Task record**: `../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md`
- **Reference maintenance runbook**: `../../05.operations/runbooks/0011-reference-maintenance-runbook.md`
