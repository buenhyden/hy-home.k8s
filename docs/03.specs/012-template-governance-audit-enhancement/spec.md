---
title: 'Template Governance Audit Enhancement Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-03
---

# Template Governance Audit Enhancement Technical Specification (Spec)

## Overview

This document defines the design for a follow-up audit and selective
enhancement pass over `docs/99.templates/**`, its support contracts, Stage 00
governance references, and repository validation. The preceding template
contract migration is already implemented on `main`; this spec does not repeat
that migration. It adds a verification-first improvement layer that checks the
current implementation against the approved template model, official external
documentation principles, and repository-specific routing rules.

The follow-up uses an audit-first workflow:

1. Inspect the current template forms, support contracts, frontmatter schema,
   route map, validator, and authored document usage.
2. Record gaps as bounded findings with source, evidence, impact, and proposed
   action.
3. Apply only targeted improvements that reduce drift risk or make future
   authoring safer.
4. Extend deterministic validation where a gap can be checked reliably.

External sources provide supporting principles, not repository authority:

- Diataxis separates documentation by user need and supports keeping reference,
  explanation, how-to, and tutorial-style content distinct.
- GitHub Docs treats YAML frontmatter as structured metadata at the top of
  Markdown pages.
- Google's developer documentation guidance emphasizes clear, consistent
  technical documentation for software practitioners.
- Microsoft's writing guidance emphasizes concise, scannable content and
  practical next steps.

## Strategic Boundaries & Non-goals

This spec owns the follow-up audit and improvement design for the template
system. It may modify `docs/99.templates/**`, Stage 00 documentation routing,
template-related shared skills, `scripts/validate-repo-quality-gates.sh`, and
authored document references when they are directly tied to template governance
or frontmatter consistency.

This spec does not own a second template migration, a new documentation
taxonomy, live cluster validation, external publishing, remote branch
protection, CI configuration changes unrelated to template validation, or broad
rewriting of current content. It also does not create placeholder authored
documents merely to prove a template route.

## Related Inputs

- **PRD**: No separate PRD exists. The user-approved continuation request in
  this Codex thread is the product requirement input.
- **ARD**: No separate ARD exists. Existing Stage 00 documentation governance
  defines the architecture boundary.
- **Related ADRs**: No new ADR is required unless implementation changes
  non-documentation runtime behavior.
- **Parent Template Migration Spec**:
  [../011-template-contract-governance-migration/spec.md](../011-template-contract-governance-migration/spec.md)
- **Template README**:
  [../../99.templates/README.md](../../99.templates/README.md)
- **Template Routing Contract**:
  [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**:
  [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Documentation Protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Repository Quality Gate**:
  [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
- **External Reference: Diataxis**:
  [https://diataxis.fr/](https://diataxis.fr/)
- **External Reference: GitHub Docs YAML frontmatter**:
  [https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
- **External Reference: Google developer documentation style guide**:
  [https://developers.google.com/style](https://developers.google.com/style)
- **External Reference: Microsoft Writing Style Guide**:
  [https://learn.microsoft.com/en-us/style-guide/welcome/](https://learn.microsoft.com/en-us/style-guide/welcome/)

## Contracts

- **Config Contract**:
  - The canonical template root remains `docs/99.templates/`.
  - Template forms remain under `docs/99.templates/templates/**`.
  - Template support contracts remain under `docs/99.templates/support/**`.
  - The follow-up work must not recreate flat template paths or
    `docs/superpowers/**`.

- **Data / Interface Contract**:
  - Audit findings use a stable record shape: scope, evidence, expected
    contract, observed state, risk, action, validation, and status.
  - Any validator enhancement must mirror a documented support contract or
    Stage 00 routing rule.
  - Frontmatter checks must remain profile-based and must not require
    frontmatter on README files or native machine-readable templates.

- **Governance Contract**:
  - README files remain entrypoints and inventories, not long-form contract
    owners.
  - Support documents own template-specific contracts and governance details.
  - Stage 00 owns agent-facing governance, path routing policy, and hook
    behavior.
  - Every repository-changing phase records progress and static validation
    evidence.

## Core Design

### Component Boundary

| Component | Responsibility | Enhancement Boundary |
| --- | --- | --- |
| Audit inventory | Inspect current template, support, governance, and validator state. | Produces findings and a remediation checklist without changing contracts by itself. |
| Template forms | Provide starting forms for authored documents. | Remove contradiction, stale paths, unsafe placeholders, or profile drift only. |
| Support contracts | Define frontmatter, routing, legacy cleanup, and template governance. | Clarify rules that are ambiguous or duplicated across support docs. |
| Stage 00 governance | Define agent-facing routing and protocol rules. | Sync only the portions that reference template behavior or incident/reference routing. |
| Quality gate | Enforce deterministic repository rules. | Add checks only when the expected behavior is stable and repo-local. |
| Authored document usage | Demonstrate that existing documents follow current templates. | Apply safe structural fixes only; avoid topic-level rewrites. |

### Audit Dimensions

| Dimension | Question | Expected Outcome |
| --- | --- | --- |
| Route coverage | Does every active authored Markdown path map to exactly one template? | No uncovered or multiply-covered path. |
| Frontmatter profile | Do templates and authored docs use only profile-appropriate keys and values? | `title`, `type`, `status`, `owner`, `updated` where required; no legacy key drift. |
| Contract separation | Are template forms, support contracts, README inventories, and Stage 00 policy separated? | README summaries link to support docs instead of duplicating full governance. |
| Legacy cleanup | Do active docs contain stale flat template paths, old postmortem paths, old `versions` or `agents` reference routes, or copied template residue? | No active legacy references except dated historical evidence when intentionally preserved. |
| Authoring safety | Do templates contain usable target-relative examples without broken Markdown links? | Placeholder target paths remain code literals; real links resolve. |
| Validator alignment | Does the quality gate enforce the current documented contract? | Deterministic checks cover stable route, frontmatter, and legacy rejection rules. |

## Data Modeling & Storage Strategy

The implementation should use the existing Stage 04 task record for execution
evidence rather than creating a new documentation tree. If an audit report is
needed, it should be an authored task or reference/audit document under an
existing canonical stage, selected by its role:

| Output | Canonical Location | Purpose |
| --- | --- | --- |
| Execution plan | [`docs/04.execution/plans/2026-07-03-template-governance-audit-enhancement.md`](../../04.execution/plans/2026-07-03-template-governance-audit-enhancement.md) | Work order, risks, and verification gates. |
| Task evidence | [`docs/04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md`](../../04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md) | Audit findings, changes, validation evidence, and handoff. |
| Durable reference finding set | `docs/90.references/audits/<date>-template-governance-audit-enhancement.md` | Optional dated snapshot if findings should persist as reference material. |

The default output should be Stage 04 plan/task. A Stage 90 audit should be
created only if the findings are useful as a durable reference beyond the
implementation task.

## Interfaces & Data Structures

### Audit Finding Record

```typescript
interface TemplateGovernanceFinding {
  id: string;
  scope: "template" | "support" | "governance" | "validator" | "authored-doc";
  evidencePath: string;
  expectedContract: string;
  observedState: string;
  risk: "low" | "medium" | "high";
  action: "no-change" | "doc-sync" | "template-fix" | "validator-fix";
  validation: string[];
  status: "open" | "resolved" | "accepted";
}
```

### Validator Rule Candidate

```typescript
interface ValidatorRuleCandidate {
  sourceContractPath: string;
  ruleName: string;
  stablePattern: string;
  failureMessage: string;
  falsePositiveRisk: "low" | "medium" | "high";
}
```

## API Contract (If Applicable)

This feature exposes no external API. No `api-spec.md`, OpenAPI, GraphQL, or
protobuf contract is required.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation governance auditor and selective remediator.
- **Inputs**:
  - Current `docs/99.templates/**` tree.
  - Stage 00 routing and documentation protocol.
  - Repository quality gate.
  - Existing authored docs that use templates.
  - External documentation principles listed in `Related Inputs`.
- **Outputs**:
  - Canonical Stage 04 plan/task records.
  - Targeted support/template/governance/validator updates.
  - Validation evidence.
- **Success Definition**:
  - Current template governance remains internally consistent.
  - Added validator checks are deterministic and tied to documented contracts.
  - Repository quality gates pass.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - `rg`, `find`, `git diff`, `git status`, `git log`.
  - `bash scripts/validate-repo-quality-gates.sh .`.
  - `git diff --check`.
  - Web search for official external source confirmation when source metadata is
    materially relevant.
- **Permission Boundary**:
  - Local repository edits and commits are allowed after plan approval.
  - Pushing, publishing, remote PR creation, live cluster mutation, secret
    inspection, or external service changes require explicit approval.
- **Failure Handling**:
  - If validator changes create unstable false positives, revert or narrow the
    rule in the same logical unit.
  - If audit findings are ambiguous, record them as accepted risk instead of
    forcing speculative changes.

## Prompt / Policy Contract (If Applicable)

- Keep human-facing final responses in Korean.
- Keep Stage 03/04 artifacts English-first.
- Follow Template-First authoring from `docs/99.templates/README.md`.
- Preserve logical commit boundaries.
- Do not implement on `main`; use a development branch.

## Memory & Context Strategy (If Applicable)

- Record durable lessons in
  `docs/00.agent-governance/memory/progress.md`.
- Do not create duplicate progress ledgers.
- Keep audit evidence in the Stage 04 task unless it is intentionally promoted
  to a Stage 90 dated audit snapshot.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Confirm worktree cleanliness before starting.
  - Read current support contracts and validator before proposing changes.
  - Treat `graphify-out/**` as historical generated output unless explicitly
    regenerating graphs.
- **Output Guardrails**:
  - No stale flat template routes in active docs.
  - No frontmatter on README files or native machine-readable templates.
  - No template-only target comments or usage instructions in authored docs
    outside `docs/99.templates/**`.
- **Blocked Conditions**:
  - Repository quality gate fails repeatedly after a validator change.
  - A proposed change conflicts with Stage 00 governance or current template
    support contracts.
  - Required external confirmation cannot be obtained for a source-sensitive
    claim.
- **Escalation Rule**:
  - Ask the user before changing scope from audit enhancement to broad
    documentation migration.

## Evaluation (If Applicable)

- **Eval Types**:
  - Static contract audit.
  - Targeted legacy path/key scan.
  - Validator regression.
- **Metrics**:
  - Number of uncovered template routes: zero.
  - Number of active legacy route references: zero, excluding explicitly dated
    historical evidence.
  - Repository quality gate status: PASS.
- **Datasets / Fixtures**:
  - Existing `docs/**`, `README.md`, `.agents/**`, `.codex/**`, `scripts/**`.
  - No synthetic incident, PRD, or template placeholder document should be
    committed.
- **How to Run**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `git diff --check`
  - Targeted `rg` scans selected by the implementation plan.

## Edge Cases & Error Handling

- **Historical evidence contains old paths**:
  - Keep dated history only when the text is clearly historical and does not
    define current routing. Otherwise update it to the current contract.
- **External style guidance conflicts with repo governance**:
  - Repo governance wins. External sources support reasoning but do not override
    Stage 00 or `docs/99.templates/support/**`.
- **Validator rule is too broad**:
  - Narrow the scope to active docs or add a documented exception for generated
    and historical artifacts.
- **Template example path does not exist yet**:
  - Keep it as code literal, not a Markdown link.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Audit reveals a broad second migration is required.
  - **Fallback**: Stop after documenting findings and ask for scope approval.
  - **Human Escalation**: Required before rewriting the template taxonomy again.
- **Failure Mode**: Validator cannot encode a rule without high false positives.
  - **Fallback**: Document the rule in support governance and keep it as review
    guidance.
  - **Human Escalation**: Required only if the user wants strict enforcement
    despite risk.
- **Failure Mode**: A support contract and authored template disagree.
  - **Fallback**: Treat the support contract as expected behavior and update the
    template or routing docs in the smallest safe change.
  - **Human Escalation**: Required if both contracts appear equally current.

## Verification Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md
find docs/99.templates -maxdepth 5 -type f -print | sort
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `docs/99.templates/**` has no active duplicate template role
  or flat legacy template route.
- **VAL-SPC-002**: Support contracts and README inventories agree on current
  template families and target patterns.
- **VAL-SPC-003**: Frontmatter profile rules are internally consistent and
  enforced where deterministic.
- **VAL-SPC-004**: Authored docs have no current template residue, stale
  template links, or unsupported legacy frontmatter values.
- **VAL-SPC-005**: Repository quality gate and `git diff --check` pass after
  every logical implementation unit.
- **VAL-SPC-006**: Any external-source-derived statement is linked to an
  official or primary source and remains clearly non-authoritative compared to
  repo governance.

## Related Documents

- **Parent Template Migration Spec**:
  [../011-template-contract-governance-migration/spec.md](../011-template-contract-governance-migration/spec.md)
- **Plan**:
  [../../04.execution/plans/2026-07-03-template-governance-audit-enhancement.md](../../04.execution/plans/2026-07-03-template-governance-audit-enhancement.md)
- **Task**:
  [../../04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md](../../04.execution/tasks/2026-07-03-template-governance-audit-enhancement.md)
- **Templates README**:
  [../../99.templates/README.md](../../99.templates/README.md)
- **Template Routing Contract**:
  [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**:
  [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Documentation Protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Quality Gate**:
  [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
