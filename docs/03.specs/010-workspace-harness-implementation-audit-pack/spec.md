---
title: 'Workspace Harness Implementation Audit Pack Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-02
---

# Workspace Harness Implementation Audit Pack Technical Specification (Spec)

---

## Overview

This document defines the design contract for a four-report implementation
audit pack under `docs/90.references/audits/`. The audit pack will use the
current `docs/90.references/research/` research pack as the source model, then
compare each researched category against repository evidence to show how much
of the model is currently implemented in `hy-home.k8s`.

The requested output is documentation-only. It does not change active
governance policy, provider runtime behavior, CI enforcement semantics, GitOps
desired state, credentials, or live cluster state.

## Strategic Boundaries & Non-goals

This spec owns the audit-pack structure, maturity/status vocabulary, evidence
model, and verification contract for the requested audit reports.

In scope:

- Create `docs/90.references/audits/README.md`.
- Create four category-aligned audit reports:
  - workspace governance implementation audit
  - harness and loop engineering implementation audit
  - provider harness and loop implementation audit
  - SDLC and delivery practices implementation audit
- Use the existing research pack under `docs/90.references/research/` as the
  benchmark model.
- Compare benchmark items to repo-backed evidence from Stage 00 governance,
  provider adapters, templates, scripts, CI workflows, operations guides,
  execution records, and progress memory.
- Include automation opportunities such as candidate pipeline, workflow, hook,
  validation, or checklist follow-up items.
- Commit by logical unit.

Out of scope:

- Writing active policy into `docs/90.references/audits/`.
- Changing Claude, Codex, Gemini, or `.agents` runtime configuration.
- Creating new provider roles for user-approved labels such as
  `vault-organizer`, `research-orchestrator`, `data-pipeline`, or
  `fullstack-website`; those labels are treated as permission context unless a
  later task explicitly adds provider adapters.
- Installing tools, plugins, or MCP servers.
- Running live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime,
  paid-job, or secret checks.
- Publishing, pushing, opening PRs, or changing external resources without
  explicit human approval.

## Related Inputs

- **PRD**: No standalone PRD exists for this documentation-only audit pack; the
  direct user request is the requirement source.
- **ARD**:
  `[../../02.architecture/requirements/0006-workspace-agent-governance-platform.md]`
- **Related ADRs**:
  `[../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md]`
- **Research Pack Spec**:
  `[../009-workspace-harness-research-pack/spec.md]`
- **Research Pack README**:
  `[../../90.references/research/README.md]`

## Contracts

- **Config Contract**: No runtime configuration changes are required. The work
  adds reference/audit Markdown documents and stage indexes only.
- **Data / Interface Contract**: Each audit report is a Markdown reference
  document with frontmatter, required reference-template sections, a maturity
  matrix, evidence links, gap notes, automation opportunities, and an
  implementation checklist.
- **Governance Contract**: Audit documents may identify gaps and candidate
  follow-up routes, but they must not redefine active policy. Actual policy,
  provider, CI, workflow, or script changes must be routed to canonical owners
  through a future Spec, Plan, Task, or operations document.

## Core Design

- **Component Boundary**:
  - `docs/90.references/audits/README.md`: audit folder entry point, report
    index, maturity vocabulary, evidence rules, and static-vs-live boundary.
  - `2026-07-02-workspace-governance-implementation-audit.md`: workspace
    rules, systems, environment, operating contracts, templates, scripts,
    shared provider structure, and automation opportunities.
  - `2026-07-02-harness-loop-implementation-audit.md`: harness engineering
    and loop engineering implementation status against the research model.
  - `2026-07-02-provider-harness-loop-implementation-audit.md`: Claude,
    Codex, and Gemini implementation status for harness/loop features and
    common environment/rule/system parity.
  - `2026-07-02-sdlc-delivery-practices-implementation-audit.md`:
    spec-driven development, SDLC, CI/CD, QA, and formatting implementation
    status.
- **Key Dependencies**:
  - Research benchmark documents in `docs/90.references/research/`.
  - Repo-backed evidence in `AGENTS.md`, `.codex/CODEX.md`, `CLAUDE.md`,
    `GEMINI.md`, `.agents/**`, `.codex/**`, `.claude/**`,
    `docs/00.agent-governance/**`, `docs/04.execution/**`,
    `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`,
    `docs/99.templates/**`, `scripts/**`, and `.github/workflows/**`.
  - Existing audit precedent:
    `../../90.references/audits/2026-05-24-workspace-harness-gap-analysis.md`.
- **Tech Stack**: Markdown, `docs/99.templates/templates/common/reference.template.md`,
  `docs/99.templates/templates/common/readme.template.md`, repository validation scripts, Git
  history, and read-only web/repo evidence as needed.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each audit report uses a shared audit matrix
  shape:

```typescript
type AuditStatus = "Implemented" | "Partial" | "Gap" | "Not in scope";

interface ImplementationAuditItem {
  category: string;
  expectedCapability: string;
  currentImplementation: string;
  status: AuditStatus;
  evidence: string[];
  gapOrRisk: string;
  recommendedFollowUp: string;
}
```

- **Migration / Transition Plan**: No migration is required. The work extends
  the existing `docs/90.references/audits/` folder with an index README and
  current dated audit reports. The parent `docs/90.references/README.md` must
  be updated so the `audits/` folder is visible in the reference hub.

## Interfaces & Data Structures

### Audit Status Vocabulary

| Status | Meaning |
| --- | --- |
| `Implemented` | Repo-backed evidence shows the capability exists and is documented in the canonical owner. |
| `Partial` | Some evidence exists, but parity, automation, coverage, enforcement, or documentation is incomplete. |
| `Gap` | The expected capability is relevant but no sufficient repo-backed implementation evidence was found. |
| `Not in scope` | The capability is intentionally outside the workspace boundary or requires human-approved future work. |

### Audit Report Required Sections

Each authored audit report must include:

- `Overview`
- `Purpose`
- `Reference Type`
- `Authority Boundary`
- `Scope`
- `Definitions / Facts`
- `Sources`
- `Review and Freshness`
- `Related Documents`

Within `Definitions / Facts`, each report must include:

- `Benchmark Model`
- `Implementation Matrix`
- `Comparison Analysis`
- `Automation Opportunities`
- `Implementation Checklist`
- `Residual Risks`

## API Contract (If Applicable)

No external API is introduced.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation auditor and governance researcher operating in
  the `docs`, `meta`, and `qa` scopes.
- **Inputs**: Existing research pack, repo-backed governance/runtime/CI/QA
  evidence, existing templates, existing audit precedent, and user-approved
  four-report structure.
- **Outputs**: One audits README, four audit reports, parent reference index
  updates, execution Plan/Task records, progress memory, validation evidence,
  and logical commits.
- **Success Definition**: A future maintainer can see which researched
  harness/loop/provider/delivery capabilities are implemented, partially
  implemented, missing, or out of scope, with evidence and follow-up routing.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `sed`, `git`, `apply_patch`, repository validation
  scripts, read-only web browsing when current provider facts need checking,
  and Codex subagents for bounded implementation/review tasks.
- **Permission Boundary**: External and live resources are read-only unless the
  human explicitly approves mutation. Do not inspect secret values.
- **Failure Handling**: If evidence is ambiguous, mark the status `Partial` or
  `Gap` and cite the missing evidence instead of inferring implementation.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Follow the repo JIT governance sequence,
  template-first authoring, documentation stage routing, and source-priority
  rules from the research pack.
- **Policy Constraints**: Human-facing explanatory prose may use Korean;
  authority, source, freshness, status vocabulary, and AI-agent routing fields
  stay English-first.
- **Versioning Rule**: Audit reports are dated snapshots. They must record
  source/evidence checked on `2026-07-02` and refresh when research references,
  Stage 00 governance, provider adapters, CI/QA scripts, templates, or runtime
  evidence changes.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Use the four research references and current repo
  evidence while drafting each audit report.
- **Long-term Memory**: Update
  `../../00.agent-governance/memory/progress.md` with concise audit-pack
  progress, validation evidence, and static-vs-live limitations.
- **Retrieval Boundary**: Audit reports summarize implementation status. Active
  policy remains in `docs/00.agent-governance/**`; execution evidence remains
  in `docs/04.execution/**`; operations procedure remains in
  `docs/05.operations/**`.

## Guardrails (If Applicable)

- **Input Guardrails**: Prefer repo-backed canonical owners over inferred
  behavior. Use external sources only to refresh provider fact claims, not to
  override local implementation evidence.
- **Output Guardrails**: Avoid policy duplication, invented evidence,
  unverifiable provider claims, secret exposure, and live-readiness claims.
- **Blocked Conditions**: Missing research input, failed validation with no
  scoped remediation, or unresolved ambiguity that changes an audit status from
  `Partial` to `Implemented`.
- **Escalation Rule**: Ask the human before changing canonical governance,
  runtime adapters, provider roles, CI enforcement, GitOps manifests, scripts,
  credentials, or external services.

## Evaluation (If Applicable)

- **Eval Types**: Repo-static validation, template conformance, source/evidence
  review, status-vocabulary review, and checklist coverage review.
- **Metrics**:
  - Four audit reports plus `audits/README.md` exist.
  - Every requested category is covered by at least one audit report.
  - Every `Implemented` or `Partial` claim links repo-backed evidence.
  - Every `Gap` has a follow-up route or explicit reason.
  - Static-vs-live limitations are stated in the README and each report.
- **Datasets / Fixtures**: Existing research pack, Stage 00 governance,
  provider adapter files, scripts, CI workflows, templates, operations guide,
  task records, and progress memory.
- **How to Run**: Use the verification commands below.

## Edge Cases & Error Handling

- **Research and repo evidence disagree**: Treat the research document as the
  benchmark and the repo as implementation evidence; record the discrepancy as
  `Partial` or `Gap`.
- **Provider feature exists upstream but not locally**: Mark the local
  implementation `Gap` or `Not in scope`; do not count upstream capability as
  implemented.
- **Automation candidate requires mutation**: Record it as a follow-up item
  only; do not implement it in this audit pack.
- **Existing audit folder lacks README**: Create one from the README template
  and update the parent reference README.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A category lacks enough evidence for a confident status.
  **Fallback**: Use `Partial` or `Gap`, list the missing evidence, and route to
  a future task.
  **Human Escalation**: Ask only if the status would change implementation
  priority or require live checks.
- **Failure Mode**: Validation fails because the new audit folder index exposes
  missing links.
  **Fallback**: Fix the smallest affected index/link.
  **Human Escalation**: Ask before changing validators or template contracts.
- **Failure Mode**: The audit uncovers a policy gap that should be fixed.
  **Fallback**: Document the gap and follow-up route.
  **Human Escalation**: Create implementation work only after approval.

## Verification Commands

```bash
git diff --check
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-repo-quality-gates.sh .
rg --files | rg '(^|/)progress\.md$'
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `docs/90.references/audits/README.md` exists and indexes the
  existing 2026-05-24 audit plus the four new 2026-07-02 reports.
- **VAL-SPC-002**: The parent `docs/90.references/README.md` structure, folder
  role table, and reference index include `audits/`.
- **VAL-SPC-003**: Four audit reports exist and follow the reference-template
  section contract plus the required audit subsections.
- **VAL-SPC-004**: Audit matrices cover harness engineering, loop engineering,
  Claude/Codex/Gemini provider status, common environment/rules/system status,
  workspace rules/system/environment, automation opportunities, spec-driven
  development, SDLC, CI/CD, QA, and formatting.
- **VAL-SPC-005**: Every report separates benchmark model, repo-backed
  implementation evidence, gaps, automation opportunities, and follow-up
  checklist items.
- **VAL-SPC-006**: Final repo-static validation commands pass, with explicit
  static-vs-live limitations recorded in the task and progress memory.

## Related Documents

- **ARD**:
  `[../../02.architecture/requirements/0006-workspace-agent-governance-platform.md]`
- **ADR**:
  `[../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md]`
- **Research Pack Spec**:
  `[../009-workspace-harness-research-pack/spec.md]`
- **Research Pack README**:
  `[../../90.references/research/README.md]`
- **Audits Folder**:
  `[../../90.references/audits/README.md]`
- **Plan**:
  `../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md`
- **Tasks**:
  `../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md`
- **Reference Maintenance Runbook**:
  `[../../05.operations/runbooks/0011-reference-maintenance-runbook.md]`
