---
title: 'Template Contract and Governance Migration Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-11
---

# Template Contract and Governance Migration Technical Specification (Spec)

## Overview

This document defines the technical design and migration contract for
restructuring `docs/99.templates/` into separated template forms, support
contracts, and governance rules. The migration is intentionally destructive:
legacy flat template paths, duplicated README governance content, legacy
frontmatter roles, legacy template references, and copied boilerplate sections
are removed or rewritten when they conflict with the canonical template
contract.

The approved migration shape is a four-phase repository migration:

1. Define the template system, support contracts, and validation schema.
2. Move template files and update validator, hook, routing, and index paths.
3. Normalize frontmatter and remove legacy keys, values, sections, and routes.
4. Apply the new contracts to authored documents and verify repository gates.

The design uses repository evidence first and official external sources as
supporting references. External sources establish these principles:

- YAML frontmatter is metadata that can be schema-validated and used by docs
  tooling.
- Documentation types should follow the reader need and the lifecycle role,
  not only the file extension.
- Markdown, links, dates, and terminology should be consistent enough to be
  linted and reviewed.
- API contract templates should remain machine-readable and avoid mixing
  unrelated prose into OpenAPI, GraphQL, or protobuf roots.

## Strategic Boundaries & Non-goals

This spec owns the migration contract for `docs/99.templates/**`, the related
Stage 00 governance rules, repository validation, pre-edit routing hints, and
authored documentation cleanup required by the new template schema.

This spec does not own live cluster validation, GitHub branch protection,
external publishing, secret value inspection, paid remote jobs, or runtime
mutation. Those actions require separate operator approval and are out of scope
for this documentation migration.

The first implementation unit after this spec should create support documents
before moving templates. That keeps reviewers able to compare the new contract
against the old flat inventory before the path migration begins.

## Related Inputs

- **PRD**: No separate PRD exists. The user-approved request in this Codex
  thread is the product requirement input.
- **ARD**: No separate ARD exists. Existing Stage 00 documentation governance
  defines the architectural boundary.
- **Related ADRs**: No new ADR is required unless the implementation changes
  non-documentation runtime behavior.
- **Current template inventory**:
  [`../../99.templates/README.md`](../../99.templates/README.md)
- **Documentation protocol**:
  [`../../00.agent-governance/rules/documentation-protocol.md`](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage routing rules**:
  [`../../00.agent-governance/rules/document-stage-routing.md`](../../00.agent-governance/rules/document-stage-routing.md)
- **Stage authoring matrix**:
  [`../../00.agent-governance/rules/stage-authoring-matrix.md`](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Repository quality gate**:
  [`../../../scripts/validate-repo-quality-gates.sh`](../../../scripts/validate-repo-quality-gates.sh)

## Contracts

- **Config Contract**:
  - The canonical template root remains `docs/99.templates/`.
  - Template forms move under `docs/99.templates/templates/`.
  - Support contracts, schema, routing, and governance rules move under
    `docs/99.templates/support/`.
  - Stage 00 remains the canonical owner for agent governance and repository
    policy. `docs/99.templates/support/**` owns template-specific contract
    details that Stage 00 references instead of duplicating.

- **Data / Interface Contract**:
  - Template routing must be represented as data that validators and hook hints
    can consume or mirror consistently.
  - Frontmatter must be defined per document profile. Each profile must list
    allowed keys, required keys, allowed values, lifecycle values, and exception
    handling.
  - Markdown templates and non-Markdown machine-readable templates must be
    classified separately.

- **Governance Contract**:
  - README files stay entrypoints and inventories. They must not accumulate
    sections that belong in `support/*contract*.md` or `support/*governance*.md`.
  - SDLC documentation contracts and common documentation contracts must be
    separate.
  - Deprecated template routes, owner values, related-document headings, and
    obsolete copied template boilerplate must be removed from active policy and
    authored documents.
  - Repo-changing work must update the progress ledger and validation evidence.

## Core Design

### Component Boundary

| Component | Target | Responsibility |
| --- | --- | --- |
| Template inventory README | `docs/99.templates/README.md` | Human entrypoint, current inventory, and links to support contracts. |
| SDLC template forms | `docs/99.templates/templates/sdlc/**` | PRD, ARD, ADR, Spec, Plan, Task, operations, incident, and feature-helper forms. |
| Common template forms | `docs/99.templates/templates/common/**` | README, Reference, Archive Tombstone, Memory, Progress, and shared utility forms. |
| Template support contracts | `docs/99.templates/support/**` | Frontmatter schema, SDLC governance, common documentation governance, routing map, legacy cleanup rules. |
| Stage 00 governance | `docs/00.agent-governance/**` | Agent-facing governance, routing policy, language rules, hooks, and protected-surface behavior. |
| Quality gate | `scripts/validate-repo-quality-gates.sh` | Deterministic enforcement for routing, frontmatter profiles, required headings, and legacy rejection. |
| Pre-edit hook hint | `docs/00.agent-governance/hooks/k8s-pre-edit.sh` | Template-first path hints for authored document changes. |

### Target Folder Model

```text
docs/99.templates/
├── README.md
├── support/
│   ├── README.md
│   ├── documentation-contract.md
│   ├── frontmatter-schema.md
│   ├── legacy-cleanup-rules.md
│   ├── sdlc-governance.md
│   └── template-routing.md
└── templates/
    ├── README.md
    ├── common/
    │   ├── archive-tombstone.template.md
    │   ├── memory.template.md
    │   ├── progress.template.md
    │   ├── readme.template.md
    │   └── reference.template.md
    └── sdlc/
        ├── architecture/
        │   ├── adr.template.md
        │   └── ard.template.md
        ├── execution/
        │   ├── plan.template.md
        │   └── task.template.md
        ├── operations/
        │   ├── guide.template.md
        │   ├── incident.template.md
        │   ├── policy.template.md
        │   ├── postmortem.template.md
        │   └── runbook.template.md
        ├── requirements/
        │   └── prd.template.md
        └── specs/
            ├── agent-design.template.md
            ├── api-spec.template.md
            ├── data-model.template.md
            ├── retired duplicate harness Task starter (removed by Spec 027)
            ├── openapi.template.yaml
            ├── schema.template.graphql
            ├── service.template.proto
            ├── spec.template.md
            └── tests.template.md
```

### Migration Phases

| Phase | Name | Required Output | Commit Boundary |
| --- | --- | --- | --- |
| 1 | Support contract baseline | `support/**` docs and README inventory contract. | Commit support docs and README references only. |
| 2 | Template path migration | Move templates into `templates/**`; update routing, hooks, validators, and README links. | Commit moves and deterministic path enforcement together. |
| 3 | Frontmatter and legacy cleanup | Standardize profile schema and remove legacy values from templates and active docs. | Commit schema enforcement and migrated docs together by stage or profile. |
| 4 | Authored docs application and final gate | Update generated/authored docs that reference old templates; run validation gates. | Commit final docs sync and evidence. |

## Data Modeling & Storage Strategy

The migration should introduce a central routing table in
`support/template-routing.md`. The repository quality gate may keep an internal
Python representation, but it must match this documented source exactly.

The frontmatter schema should use profile-based records:

| Profile Family | Example Profile | Document Type Value | Required Keys | Notes |
| --- | --- | --- | --- | --- |
| `sdlc` | `sdlc.spec` | `sdlc/spec` | `title`, `type`, `status`, `owner`, `updated` | Technical specs and helper contracts. |
| `sdlc` | `sdlc.task` | `sdlc/task` | `title`, `type`, `status`, `owner`, `updated` | Execution evidence and validation records. |
| `sdlc` | `sdlc.policy` | `sdlc/policy` | `title`, `type`, `status`, `owner`, `updated` | Replaces legacy `operation` wording. |
| `content` | `content.reference` | `content/reference` | `title`, `type`, `status`, `owner`, `updated` | Durable reference material. |
| `content` | `content.archive-tombstone` | `content/archive-tombstone` | `title`, `type`, `status`, `owner`, `updated` | Tombstones use `status: archived`. |
| `content` | `content.readme` | none | none | README files remain frontmatter-free unless a future renderer requires it. |
| `governance` | `governance.memory` | `governance/memory` | `title`, `type`, `status`, `owner`, `updated` | Standalone governance memory. |
| `governance` | `governance.progress` | none | none | Canonical progress ledger remains entry-based, not document-frontmatter based. |
| `machine-contract` | `machine.openapi` | n/a | n/a | YAML root must follow OpenAPI, not Markdown frontmatter. |
| `machine-contract` | `machine.graphql` | n/a | n/a | GraphQL schema root must remain parseable schema text. |
| `machine-contract` | `machine.protobuf` | n/a | n/a | Protobuf root must remain parseable `.proto` text. |

The current implementation uses simple values such as `spec`, `task`, and
`reference`. Phase 3 owns the migration from simple values to namespaced values.
Validators must allow only the target schema after the migration phase closes.

## Interfaces & Data Structures

### Template Route Record

```typescript
interface TemplateRoute {
  profile: string;
  targetPattern: string;
  templatePath: string;
  requiredHeadings: string[];
  frontmatterRequired: boolean;
  languagePolicy: "english-first" | "korean-human-facing" | "mixed-by-section";
  owner: "platform";
}
```

### Frontmatter Profile Record

```typescript
interface FrontmatterProfile {
  profile: string;
  typeValue?: string;
  requiredKeys: string[];
  allowedKeys: string[];
  allowedStatusValues: string[];
  defaultOwner: "platform";
  frontmatterRequired: boolean;
}
```

These TypeScript interfaces are illustrative contracts for the migration. The
actual repository gate can remain Bash plus embedded Python if it is simpler to
integrate with the existing validator.

## API Contract (If Applicable)

No external API is introduced by this migration.

Machine-readable template files must keep their native contract roots:

- OpenAPI templates must follow the OpenAPI Description structure and keep the
  root fields required by the selected OpenAPI version.
- GraphQL schema templates must remain valid schema text.
- Protobuf service templates must remain valid `.proto` text.

Do not wrap machine-readable contracts in Markdown frontmatter.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation migration agent.
- **Inputs**:
  - User-approved A design and four-phase migration boundary.
  - Existing `docs/99.templates/**` flat inventory.
  - Stage 00 governance rules and validation scripts.
  - Official external documentation style and schema sources.
- **Outputs**:
  - Support contract docs.
  - Moved template files.
  - Updated governance/routing/validator/hook surfaces.
  - Cleaned authored docs and README references.
  - Validation evidence and commit-separated logical units.
- **Success Definition**:
  - The template system has one canonical owner per role and function.
  - Every authored stage document maps to exactly one template route.
  - Legacy routes and legacy frontmatter values are rejected by validation.
  - Repository quality gates pass after each logical implementation unit where
    possible, and at minimum after each migration phase.

## Tools & Tool Contract (If Applicable)

- Use `rg` and `find` for repository inventory.
- Use `git mv` for template path migration where files are moved.
- Use `apply_patch` for manual edits.
- Use `bash scripts/validate-repo-quality-gates.sh .` as the primary static
  validation gate.
- Use `git diff --check` before commits.
- Do not use live cluster, Vault, cloud, paid jobs, external publishing, or
  remote mutation for this migration.

## Prompt / Policy Contract (If Applicable)

The implementation must honor these prompt-level constraints:

- Keep SDLC content under `docs/`.
- Keep README entrypoints lean; route contract/guidance sections to support or
  governance docs.
- Remove legacy templates, sections, keys, values, and references.
- Apply template changes to authored documents, not only to template files.
- Separate SDLC documentation contracts from common documentation contracts.
- Keep logical-unit commits.

## Memory & Context Strategy (If Applicable)

Reusable lessons from this migration belong in
`../../00.agent-governance/memory/progress.md`. Long-lived policy belongs in
Stage 00 or `docs/99.templates/support/**`, not in a transient task summary.

The final migration should record:

- The new canonical template folder model.
- The frontmatter profile model and namespaced `type` values.
- The validator surfaces that reject legacy paths and values.
- Any intentionally deferred live or remote validation boundaries.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Read the current template README and matching template before authoring or
    moving documents.
  - Inventory existing template links before changing path contracts.
  - Treat generated files and protected surfaces according to repository
    governance.

- **Output Guardrails**:
  - No final authored document may retain copied template instruction blocks
    when topic-specific content is required.
  - No active route may point to a deleted flat template path after Phase 2.
  - No active frontmatter may keep deprecated owner values, old operations
    policy type values, or duplicate role keys after Phase 3.
  - README changes must not become a dumping ground for support-contract
    content.

- **Blocked Conditions**:
  - Validation cannot identify a unique template for an authored stage path.
  - A machine-readable template becomes invalid because Markdown frontmatter was
    introduced.
  - A legacy route remains in an active hook, validator, Stage 00 rule, or stage
    README after the corresponding migration phase.

- **Escalation Rule**:
  - Ask for explicit user approval before pushing, publishing, changing remote
    resources, running paid jobs, or inspecting secrets. Local documentation
    edits and static validation are in scope.

## Evaluation (If Applicable)

- **Eval Types**:
  - Static repository validation.
  - Manual contract review.
  - Link and legacy-reference search.
  - Frontmatter schema review.

- **Metrics**:
  - Zero active references to removed flat template paths after Phase 2.
  - Zero active references to deprecated template route, owner value, and
    README related-document heading literals after Phase 3.
  - Every non-README authored Markdown document under active stages has exactly
    one route and the expected frontmatter profile.
  - Every template file is listed in the template inventory and categorized as
    SDLC, common, governance, or machine-readable.

- **Datasets / Fixtures**:
  - Current `docs/99.templates/**` inventory.
  - Current authored documents under `docs/01.requirements` through
    `docs/05.operations`, `docs/90.references`, and `docs/98.archive`.
  - Current Stage 00 governance and hook scripts.

- **How to Run**:
  - Use `rg` searches listed in the verification commands.
  - Run the repository quality gate.
  - Review the staged diff before each logical commit.

## Edge Cases & Error Handling

- **README files without frontmatter**:
  README files remain valid without frontmatter. Their profile is inferred from
  path and filename.

- **Progress ledger without document frontmatter**:
  `docs/00.agent-governance/memory/progress.md` remains an entry ledger. The
  progress template defines appendable entries, not a whole-document
  frontmatter schema.

- **Machine-readable templates**:
  YAML, GraphQL, and protobuf templates must not receive Markdown frontmatter.
  They are classified by path and file extension.

- **Historical progress entries**:
  Historical entries may mention old paths as evidence. Phase 3 should remove
  active policy references and active route references first. Historical
  mentions can remain only when validation deliberately allows dated evidence
  contexts.

- **Archived docs**:
  Archive Tombstones use the common/content archive profile and remain
  metadata-only. They must not inherit SDLC frontmatter values.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Validator updates fail because route data and README
  inventory diverge.
  **Fallback**: Stop the phase, repair the route table and README inventory,
  then rerun static validation.
  **Human Escalation**: Request review only if a document path could reasonably
  belong to more than one profile.

- **Failure Mode**: A stage README link update creates broken relative links.
  **Fallback**: Recalculate links from the final authored document location and
  rerun the repository quality gate.
  **Human Escalation**: Not required unless the linked target was intentionally
  removed without a replacement.

- **Failure Mode**: Legacy cleanup touches too many authored docs for one safe
  review.
  **Fallback**: Split Phase 3 into profile-based commits such as SDLC specs,
  execution docs, operations docs, and references.
  **Human Escalation**: Report the split and continue with the approved
  migration strategy.

## Verification Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md
find docs/99.templates -maxdepth 4 -type f -print | sort
```

The flat-path `rg` command is expected to return matches before Phase 2 and no
active-route matches after Phase 2. Historical progress evidence may require a
specific validator allow-list rather than a blanket repository-wide zero-match
rule.

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `docs/99.templates/support/**` exists and separates SDLC
  governance, common documentation governance, routing, legacy cleanup, and
  frontmatter schema.
- **VAL-SPC-002**: `docs/99.templates/templates/**` contains all template forms
  and no contract-only support documents.
- **VAL-SPC-003**: `docs/99.templates/README.md` is an inventory and entrypoint,
  not the owner of detailed contracts that belong in support docs.
- **VAL-SPC-004**: Stage 00 routing and documentation protocol point to the new
  template paths and support contract owners.
- **VAL-SPC-005**: `scripts/validate-repo-quality-gates.sh` enforces the new
  route table, frontmatter profiles, and legacy rejection rules.
- **VAL-SPC-006**: `docs/00.agent-governance/hooks/k8s-pre-edit.sh` surfaces the
  new template paths for authored document edits.
- **VAL-SPC-007**: Authored documents using affected templates have updated
  links, profile-appropriate frontmatter, and topic-specific section content.
- **VAL-SPC-008**: No active template route, governance rule, or authored
  document depends on a removed legacy template path after the migration closes.
- **VAL-SPC-009**: `git diff --check` and `bash
  scripts/validate-repo-quality-gates.sh .` pass before final handoff.

## Related Documents

- [Templates README](../../99.templates/README.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Stage 03 Specs README](../README.md)
- [Progress Ledger](../../00.agent-governance/memory/progress.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
- [Plan](../../04.execution/plans/2026-07-03-template-contract-governance-migration.md)
- [Task](../../04.execution/tasks/2026-07-03-template-contract-governance-migration.md)
- **Completed evolution**: [011](./spec.md) -> [012](../012-template-governance-audit-enhancement/spec.md) -> [013](../013-workspace-document-governance-hardening/spec.md) -> [014](../014-workspace-document-contract-normalization/spec.md) -> [020](../020-workspace-contract-governance-normalization/spec.md) -> [021](../021-sdlc-lifecycle-contract/spec.md) -> [022](../022-control-cloud-doc-normalization/spec.md) -> [023](../023-stage03-04-repo-static-gap-closure/spec.md).
- [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
- [Diátaxis documentation framework](https://diataxis.fr/)
- [Google developer documentation style guide](https://developers.google.com/style)
- [Vale front matter documentation](https://vale.sh/docs/formats/front-matter)
- [OpenAPI Description structure](https://learn.openapis.org/specification/structure.html)
