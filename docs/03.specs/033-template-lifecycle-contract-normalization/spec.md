---
title: 'Template Lifecycle Contract Normalization Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-14
---

# Template Lifecycle Contract Normalization Technical Specification (Spec)

## Overview

This Spec defines the approved follow-up normalization of the Stage 99 template
system. It separates reusable forms from human governance and machine
contracts, keeps the five-key Markdown frontmatter baseline, adds
registry-owned body traceability contracts, and migrates only current or active
consumers whose content conflicts with the resulting contract.

At baseline commit `ac3ba71959ab2672803450588f193749f92a996e`, the document
registry, Markdown profile, link/owner, and repository quality gates pass. The
remaining work is therefore contract consolidation and semantic assurance, not
recovery from a currently failing route or profile migration.

## Strategic Boundaries & Non-goals

- **In scope**: `docs/99.templates/**`; the registry and schema; current
  Stage 00 routing mirrors; document validators and fixtures; current or active
  Stage 01 through 05 consumers; affected indexes; and execution evidence.
- **Historical boundary**: Existing `done` PRDs, Specs, Plans, and Tasks and
  accepted ADR bodies remain historical evidence. An accepted ADR is replaced
  by a new decision rather than rewritten.
- **Runtime boundary**: Repository-static validation does not prove live
  Kubernetes, GitOps, Vault, ESO, provider, or remote CI state.
- **External-action boundary**: This tranche does not push, publish, mutate
  remote rules, inspect secret values, or apply resources.
- **Non-goals**: Universal `id`, `created`, relationship, schema-version, or
  reviewer frontmatter; a Release document family; renumbering historical
  documents; deleting dormant canonical forms solely because they have no
  current consumer; or treating `01 -> 05` as a mandatory waterfall.

## Contracts

- **Authority Contract**: `document-profiles.json` is the sole machine owner of
  routes, document types, five-key frontmatter, profile status domains, H2
  structure, template mapping, explicit exceptions, and body traceability
  contracts. Support Markdown explains rationale and procedure without copying
  exact machine inventories.
- **Form Contract**: `docs/99.templates/templates/**` contains copyable document
  shapes only: a valid starting frontmatter example where applicable, an H1,
  profile-required H2 headings, type-specific tables, and short removable
  prompts. It does not own routes, lifecycle enums, migration policy, archive
  policy, or validator procedure.
- **Governance Contract**: `docs/99.templates/support/**` owns role boundaries,
  lifecycle rationale, authoring procedure, migration rules, and validation
  interpretation. README files remain navigation and inventory surfaces.
- **Metadata Contract**: General Markdown uses exactly `title`, `type`,
  `status`, `owner`, and `updated` in repository order. Archive Tombstones keep
  their approved extension. README, progress-entry, and native contract forms
  remain frontmatter-free.
- **History Contract**: Current and active consumers receive the new semantic
  body contract. Completed execution evidence and accepted ADR bodies are not
  rewritten to simulate evidence that did not exist at the time.
- **Validation Contract**: Validators derive exact facts from the registry,
  reject authored placeholder residue and incomplete semantic tables, and keep
  behavior fixtures independent from exhaustive registry snapshots.

## Core Design

### Baseline findings and dispositions

| Finding | Baseline evidence | Approved disposition |
| --- | --- | --- |
| Stage 99 route facts are repeated | The templates README and `template-routing.md` mirror the same route table and the shell gate enforces both copies. | Keep one machine inventory in the registry; reduce README and support views to procedure, examples, and canonical links. |
| Retired cloud routes are described as active | `documentation-contract.md` and `frontmatter-schema.md` retain example-local language that conflicts with the retired-tree guard. | Make the Stage 90 snapshot location the only steady-state documentation route and remove unreachable legacy validation branches. |
| Native template mapping is outside the registry | The native-contract exception has no template mapping while the quality gate hardcodes OpenAPI, GraphQL, and protobuf targets. | Model the three native mappings in the registry and derive checks from them. |
| Template forms repeat governance prompts | Markdown forms repeat target-path, replacement, and generic section guidance. | Remove contract prose; retain only minimal type-specific author prompts and structures. |
| Registry facts are copied into validators and fixtures | Template inventories, routes, heading/type pairs, profile IDs, and semantic digests have parallel owners. | Retain independent mutation and negative cases but derive exhaustive inventory checks from the registry. |
| Structural checks do not prove semantic handoff | Required H2 headings pass even when PRD requirements, Spec criteria, Task results, or lifecycle evidence are not mapped. | Add a registry-owned body traceability contract for draft and active authored documents. |
| Non-empty frontmatter placeholders can pass | A non-empty starter title is not rejected by the current title check. | Reject placeholder tokens and title/H1 starter residue in authored documents while allowing them in templates. |
| PRD 003 links an inconsistent current Spec | PRD 003 identifies Spec 006 as canonical while that completed Spec records a different lineage. | Correct the current PRD pointer without rewriting the completed Spec. |

### Responsibility model

```text
document-profiles.json
  -> support contracts explain why and how
  -> template forms provide copyable shape
  -> authored documents provide topic facts and evidence
  -> validators and fixtures enforce the registry contract
  -> README files route readers to the canonical owners
```

The support layer has one owner for each rationale:

- `documentation-contract.md`: responsibility boundaries and protected
  surfaces.
- `sdlc-governance.md`: document roles, numbering, lifecycle handoff, state
  evidence, and forward/reverse feedback.
- `common-documentation-governance.md`: README, reference, archive, memory, and
  progress roles.
- `frontmatter-schema.md`: five-key meaning, ordering convention, allowed value
  ownership, and exception rationale.
- `template-routing.md`: exact-one-profile selection procedure and examples,
  without a second complete route inventory.
- `legacy-cleanup-rules.md`: retirement, preservation, and forbidden residue.

### Document role separation

| Family | Unique responsibility | Must not duplicate |
| --- | --- | --- |
| PRD | Problem, users, requirement IDs, scope, and acceptance criteria | Architecture and execution procedure |
| ARD (Architecture Reference Document) | Architecture boundary, views, quality attributes, data, and deployment constraints | Individual decision rationale and implementation plan |
| ADR | One decision, alternatives, consequences, and replacement lineage | System-wide description and work breakdown |
| Spec and helper Specs | Implementable behavior, interfaces, invariants, failures, and verification criteria | Product motivation and execution schedule |
| Plan | Ordered work, dependencies, gates, risks, rollback, and completion criteria | Requirement or technical-contract redefinition |
| Task | Bounded action, safety boundary, result, and evidence | Long-running plan and reusable operation procedure |
| Guide | Reader-oriented how-to, tutorial, or concept content | Policy authority and protected operational procedure |
| Policy | Scope, controls, responsibilities, exceptions, and review cadence | Command-by-command implementation procedure |
| Runbook | Preconditions, steps, expected results, stop/escalation, verification, and recovery | Policy rationale and control ownership |
| Incident | Real-time facts, impact, roles, timeline, response state, and evidence | Root-cause analysis and retrospective conclusions |
| Postmortem | Blameless cause analysis, learning, and owned prevention actions | Live incident-state tracking |

Incident and Postmortem, Plan and Task, and Spec and helper Spec remain separate
because their evidence responsibilities differ. Dormant API Spec, Data Model,
Tests, Incident, Postmortem, OpenAPI, GraphQL, and protobuf forms remain
canonical until a separate consumer or retirement decision changes them.

### Lifecycle and feedback model

The numbered directories express responsibility and navigation, not a universal
standard or one-way gate:

```text
01 Requirement -> 02 Architecture/Decision -> 03 Spec
    -> 04 Plan/Task evidence -> 05 Guide/Policy/Runbook
    -> Incident/Postmortem -> new Requirement/ADR/Spec/Task as needed
```

New single-feature PRD and Spec lineages share the three-digit feature number.
Architecture requirements and decisions and steady-state operations collections
retain four-digit collection numbering. Plans and Tasks remain dated execution
records. Incidents retain year and `INC-###` identity. Historical identifiers
are never changed for cosmetic alignment, and program-to-tranche exceptions
remain explicit registry facts backed by the accepted lineage ADR.

The existing profile-specific state domains remain unchanged. Draft and active
documents must carry the semantic evidence required to promote them. Completed
execution records and accepted ADRs remain immutable evidence; future changes
create a successor or a new execution record.

### External basis and local adoption

| Source | Local adoption | Boundary |
| --- | --- | --- |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Keep verifiable requirements and acceptance criteria in the PRD family. | The public abstract is evidence for role separation, not a claim of full ISO conformance. |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Keep architecture description semantics separate from the Markdown recording format. | The local ARD name and path remain a repository convention. |
| [Nygard ADR practice](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) | Preserve accepted ADRs and replace decisions with a new numbered ADR. | ADR practice does not prescribe the repository's full SDLC directory scheme. |
| [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) and [JSON Schema 2020-12](https://json-schema.org/specification) | Validate metadata centrally with exact required keys and enums. | Frontmatter itself is a repository convention rather than CommonMark semantics. |
| [Kubernetes page content types](https://kubernetes.io/docs/contribute/style/page-content-types/) | Distinguish how-to, tutorial, concept, and reference intent in Guide body content. | No new Guide frontmatter key is introduced. |
| [NIST SP 800-53 AC-1 OSCAL example](https://pages.nist.gov/OSCAL/learn/concepts/layer/control/catalog/sp800-53rev5-example/) | Separate policy/control ownership from implementation procedure. | This tranche does not claim NIST authorization or compliance. |
| [Google SRE incident management](https://sre.google/sre-book/managing-incidents/) and [postmortem culture](https://sre.google/sre-book/postmortem-culture/) | Separate live Incident facts from Postmortem cause analysis and track actions into Tasks. | No fabricated or live incident is created to prove the template. |

## Data Modeling & Storage Strategy

The registry advances from schema v4 to v5 to add the body-contract shape. The
existing profile identity, route, frontmatter, state, heading, exception,
current-owner, reference-pack, and program-lineage data remain compatible.

Each applicable authored profile gains one declarative traceability contract
that can express:

- the H2 section that contains the contract;
- required table headers or labeled fields;
- identifier patterns;
- allowed upstream and downstream profile families;
- statuses to which semantic enforcement applies; and
- whether reciprocal evidence is required.

Exact names and JSON structure are settled in the implementation Plan through
red fixtures before registry migration. The schema uses closed objects and
finite enums rather than permitting arbitrary per-profile validator options.
No relationship data is moved into frontmatter.

Compatibility rules:

- `done` execution evidence and accepted ADR bodies stay readable under their
  current structural profiles.
- New and migrated draft/active consumers use the body contract.
- Template profiles derive their source type and body shape from the authored
  source profile while retaining template-only placeholders.
- Native contracts use registry-declared target-to-template mappings and their
  native syntax, with no Markdown metadata.

## Interfaces & Data Structures

### Semantic handoff tables

The exact table lives under the existing `Traceability` H2 and varies by role:

| Profile | Required semantic mapping |
| --- | --- |
| PRD | Requirement ID -> acceptance criterion -> downstream owner |
| ARD | Upstream requirement -> quality attribute or boundary -> ADR/Spec |
| ADR | Decision lineage -> replacement relation -> affected Spec |
| Spec | PRD requirement ID -> Spec criterion -> verification method |
| Plan | Spec criterion -> work package -> expected Task |
| Task | Criterion/work item -> result -> evidence |
| Guide/Policy/Runbook | Promoted Spec, Task, or policy owner -> operating surface |
| Incident | Timeline/action -> evidence -> follow-up Task |
| Postmortem | Root cause/action -> owner and due state -> Task/Spec/ADR/PRD feedback |

### Template-to-authored interface

A Markdown form may contain removable HTML comments and starter tokens. The
authored-document interface rejects those tokens, comments, empty required
sections, and a starter title or H1. Route instructions, status domains, and
migration rules are resolved before copying the form and are never copied into
the authored body.

### Validation interface

Validators load the registry once and return deterministic rule IDs with the
path, profile, field or section, expected contract, and observed value. Tests
contain minimal positive and negative trees and mutation cases. They do not
redeclare the complete production profile set merely to prove inventory
equality.

## Edge Cases & Error Handling

- If a current document cannot identify an upstream requirement, it records an
  explicit, reviewable exclusion rather than inventing a relationship.
- If one path matches zero or multiple profiles, authoring stops before a form
  is selected.
- If a status transition lacks semantic evidence, validation fails without
  modifying historical evidence to manufacture a pass.
- Accepted ADR changes require a new ADR. Link-only current-owner corrections
  are made on the mutable current surface whenever possible.
- A dormant form is not legacy merely because the current corpus has no
  consumer. Retirement requires a separate role and route decision.
- The former `examples/aws/docs/**` and `examples/azure/docs/**` routes remain
  absent; provider documentation refreshes extend the Stage 90 snapshot pack.
- YAML, GraphQL, and protobuf forms remain native and must not acquire Markdown
  comments or frontmatter.
- Guide subtype is body content under `Guide Type`, not a new metadata enum.
- A validator-generated projection may be checked for consistency, but it must
  not become a hand-maintained second owner.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Registry, forms, support prose, and current consumers cannot
  migrate in independently green commits.
  **Fallback**: Use a bounded compatibility field or a single atomic contract
  commit; do not weaken strict validation globally.
- **Failure Mode**: A proposed semantic rule would force rewriting completed
  evidence or accepted ADRs.
  **Fallback**: Scope enforcement to draft/active consumers and preserve the
  historical profile.
- **Failure Mode**: Removing a hardcoded fixture eliminates independent drift
  detection.
  **Fallback**: Replace the snapshot with targeted mutation and negative cases
  before deleting it.
- **Failure Mode**: A template section contains rules needed by authors.
  **Fallback**: Move reusable rules to the owning support document and keep a
  short form prompt with a canonical link from the support entrypoint.
- **Human Escalation**: A new frontmatter key, status value, document family,
  accepted-ADR rewrite, historical-body migration, remote action, secret read,
  or live-system mutation requires a new explicit decision or approval.

## Verification Commands

```bash
git diff --check
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

Focused validation also proves that existing completed document bodies and
accepted ADR bodies outside newly created execution evidence are absent from
the implementation diff.

## Success Criteria & Verification Plan

- **VAL-TLCN-001**: Every tracked document and template path matches exactly one
  registry profile or explicit native/control exception; uncovered and
  ambiguous paths are zero.
- **VAL-TLCN-002**: The registry is the only exhaustive route, template,
  frontmatter, status, H2, exception, and traceability-contract inventory.
- **VAL-TLCN-003**: Stage 99 README and support documents contain no conflicting
  complete route mirror, active example-local cloud claim, or duplicate
  lifecycle/status table.
- **VAL-TLCN-004**: All 27 Markdown forms and three native forms have one unique
  role, contain no reusable governance body, and provide the profile-specific
  structure needed by their authored consumer.
- **VAL-TLCN-005**: General Markdown profiles retain exactly the five-key
  frontmatter baseline; legacy, duplicate-purpose, and consumer-free keys are
  zero.
- **VAL-TLCN-006**: Authored placeholder titles, generic template prompts,
  incomplete required sections, invalid semantic tables, and invalid
  source/target relationships fail independent negative fixtures.
- **VAL-TLCN-007**: Current draft/active Stage 01 through 05 consumers satisfy
  their profile body contract, including PRD requirement -> Spec criterion ->
  Task result/evidence handoff where applicable.
- **VAL-TLCN-008**: Existing completed PRD/Spec/Plan/Task and accepted ADR
  bodies are unchanged, except that a separately approved successor document
  may link to them.
- **VAL-TLCN-009**: PRD 003 no longer claims the inconsistent completed Spec 006
  as its canonical current Spec, and all resulting cross-links resolve.
- **VAL-TLCN-010**: Self-tests, strict validators, repository quality gates,
  `pre-commit run --all-files`, and `git diff --check` pass with repo-static
  evidence clearly separated from remote/live state.

## Traceability

### Upstream authority

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Registry ADR**: [Declarative Document Contract Registry](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)

### Prior implementation and evidence

- **Registry Spec**: [Document Contract Registry](../026-document-contract-registry/spec.md)
- **Template Spec**: [Template Contract Consolidation](../027-template-contract-consolidation/spec.md)
- **Semantic Validation Spec**: [Semantic Document Validation](../029-semantic-document-validation/spec.md)
- **Authored Migration Spec**: [Authored Document Migration](../030-authored-document-migration/spec.md)
- **Current Audit Finding**: [SDLC, Document Lifecycle, and Frontmatter](../../90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md)
- **Current Remediation Roadmap**: [Integrated Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)

### TLCN-002 registry evidence

- **RED**: The v5 minimal registry and eleven new body/native mutations were
  added before implementation. `validate-document-contract-registry.py
  --root . --self-test` exited `1` because the v4 implementation returned
  `REGISTRY_SCHEMA` for the valid v5 fixture.
- **GREEN**: The registry self-test passes `59` mutation cases with `64`
  profiles and `30` registry-derived forms. Strict registry validation reports
  zero uncovered or ambiguous routes, and the repository quality gate passes.
- **Compatibility boundary**: All production body contracts retain
  `enforcedStatuses: []`. This commit defines and validates the contract shape
  without enforcing semantic tables on active consumers before their planned
  migration.

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-FUN-01, REQ-PRD-FUN-02](../../01.requirements/005-workspace-document-assurance-modernization.md#functional-requirements) | VAL-TLCN-001 through VAL-TLCN-004 | Registry mutation tests, registry-derived form inventory, and focused support-owner scans |
| [REQ-PRD-FUN-05, REQ-PRD-FUN-12](../../01.requirements/005-workspace-document-assurance-modernization.md#functional-requirements) | VAL-TLCN-005 through VAL-TLCN-009 | Five-key metadata validation, lifecycle-table fixtures, reciprocal-link validation, and historical-body diff guard |
| [REQ-PRD-FUN-10, REQ-PRD-MET-08](../../01.requirements/005-workspace-document-assurance-modernization.md#success--acceptance-criteria) | VAL-TLCN-010 | Logical commits, independent reviews, strict repository gates, and all-files pre-commit |

### Execution

- [Implementation Plan](../../04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md)
- [Execution Task](../../04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md)
