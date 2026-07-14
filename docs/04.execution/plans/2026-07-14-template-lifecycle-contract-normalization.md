---
title: 'Template Lifecycle Contract Normalization Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-14
---

# Template Lifecycle Contract Normalization Implementation Plan

## Overview

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Stage 99 registry the single machine authority for document
forms and lifecycle traceability, separate form content from governance, and
migrate only current active consumers while preserving completed evidence.

**Architecture:** Schema v5 adds a closed `bodyContract` to each profile and
gives each native contract format its own registry profile and template. Body
validation is implemented and fixture-tested while production
`enforcedStatuses` is empty; after the 37 active consumers are migrated, the
final cutover enables enforcement for `draft` and `active` only.

**Tech Stack:** Markdown, YAML frontmatter, JSON Schema 2020-12, Python 3,
CommonMark-aware repository parsers, Bash, pre-commit, and Git.

### Global Constraints

- General authored Markdown keeps exactly `title`, `type`, `status`, `owner`,
  and `updated` in that order; no universal metadata key is added.
- Existing `done` PRD, Spec, Plan, and Task bodies and accepted ADR bodies are
  immutable evidence for this tranche.
- Accepted ADR 0015 already owns the declarative-registry architecture; schema
  v5 extends that decision and does not create a duplicate ADR.
- README files remain frontmatter-free navigation and inventory surfaces.
- Template forms contain shape, type-specific structures, and removable
  `Author prompt:` comments only; support documents own reusable rules.
- The former `examples/aws/docs/**` and `examples/azure/docs/**` trees remain
  absent. Stage 90 cloud snapshots are the only durable provider-doc route.
- Dormant API Spec, Data Model, Tests, Incident, Postmortem, OpenAPI, GraphQL,
  and protobuf forms remain canonical.
- Use repository-static evidence only. Do not read secrets, mutate live
  systems, push, publish, or change remote repository rules.
- Use `apply_patch` for manual file changes and one logical commit per Task.
- Run independent requirements and quality review after every implementation
  Task before moving to the next Task.

---

## Context

Spec 033 records a clean baseline: route, Markdown, cross-document, and full
repository gates pass. The Current 2026-07-11 WEIA audit still identifies
semantic lineage and lifecycle evidence as gaps. Inspection found five concrete
contract leaks:

1. Stage 99 README and `template-routing.md` repeat a complete route table.
2. Support prose still describes retired example-local cloud routes as active.
3. Native OpenAPI, GraphQL, and protobuf template mapping is hardcoded in the
   shell quality gate rather than the registry.
4. Forms repeat target paths and generic authoring rules in every section.
5. Validators prove structural headings but not PRD requirement to Spec
   criterion to Task result/evidence handoff.

### File and interface map

| Unit | Exact owners | Responsibility |
| --- | --- | --- |
| Registry schema and data | `docs/99.templates/support/document-profiles.schema.json`, `docs/99.templates/support/document-profiles.json` | Own schema v5 profiles, form mapping, and body contracts. |
| Typed registry loader | `scripts/document_contracts.py` | Parse and validate closed registry objects. |
| Registry self-test | `scripts/validate-document-contract-registry.py`, `tests/fixtures/document-contracts/registry-cases.json` | Prove routes, profile/source parity, native mappings, and mutation rejection. |
| Local document semantics | `scripts/validate-markdown-profiles.py`, `tests/fixtures/markdown-profiles.json` | Validate five-key metadata, placeholders, table shape, and identifiers. |
| Cross-document semantics | `scripts/validate-links-and-owners.py`, `tests/fixtures/links-and-owners.json` | Validate linked source/target profiles and reciprocal evidence. |
| Aggregate gate | `scripts/validate-repo-quality-gates.sh`, `tests/fixtures/document-contracts/template-compatibility.json` | Derive template projections from the registry and retain independent negative tests. |
| Human contracts | `docs/99.templates/support/*.md` | Explain ownership, roles, flow, authoring, validation, and retirement without machine mirrors. |
| Form layer | `docs/99.templates/templates/**` | Provide 27 Markdown and three native copyable forms. |
| Current consumers | The exact 37 active Stage 01, 02, 03, and 05 files listed in Tasks 6 and 7 | Provide topic-specific lifecycle traceability without rewriting topic prose. |
| Evidence | Spec 033, this Plan, the same-topic Task, current audit overlay, migration ledger, indexes, and progress ledger | Preserve approval, implementation, verification, and handoff evidence. |

### Schema v5 body-contract interface

Every profile gains `bodyContract`, which is `null` or this closed object:

```json
{
  "section": "Traceability",
  "tableHeading": "Lifecycle Traceability",
  "enforcedStatuses": [],
  "requiredColumns": ["Requirement ID", "Acceptance criterion", "Downstream owner"],
  "identifierColumns": [
    {"column": "Requirement ID", "kind": "requirement"}
  ],
  "sourceLinkColumn": null,
  "targetLinkColumn": "Downstream owner",
  "allowedSourceProfileIds": [],
  "allowedTargetProfileIds": ["sdlc/ard", "sdlc/spec"],
  "reciprocalEvidence": true,
  "allowExplicitExclusion": true
}
```

`identifierColumns[].kind` is one of `requirement`, `criterion`, or
`work-item`. Identifier syntax is owned by the validator:

```text
requirement = ^REQ-[A-Z0-9-]+-[0-9]{2,3}$
criterion   = ^VAL-[A-Z0-9-]+-[0-9]{3}$
work-item   = ^[A-Z][A-Z0-9-]+-[0-9]{3}$
exclusion   = ^N/A — .+$
```

`sourceLinkColumn` and `targetLinkColumn` name columns whose Markdown links
must resolve to the corresponding allowed profile set. A non-link value is
valid only when `allowExplicitExclusion` is true and the cell matches the
exclusion form. `reciprocalEvidence` requires the linked authored document to
link back to the source path. Template profiles copy the source profile's
contract, but form validation always runs regardless of source status.

### Canonical lifecycle tables

| Profile family | `Lifecycle Traceability` columns |
| --- | --- |
| PRD | `Requirement ID`, `Acceptance criterion`, `Downstream owner` |
| ARD | `Upstream requirement`, `Quality attribute or boundary`, `ADR / Spec` |
| ADR | `Decision lineage`, `Replacement relation`, `Affected Spec` |
| Spec and helper Specs | `PRD requirement`, `Spec criterion`, `Verification method` |
| Plan | `Spec criterion`, `Work package`, `Expected Task` |
| Task | `Criterion / work item`, `Result`, `Evidence` |
| Guide | `Promoted owner`, `Audience outcome`, `Operating surface` |
| Policy | `Promoted owner`, `Control owner`, `Enforcement surface` |
| Runbook | `Promoted owner`, `Trigger or control`, `Evidence or recovery owner` |
| Incident | `Timeline or action`, `Evidence`, `Follow-up Task` |
| Postmortem | `Root cause or action`, `Owner and due state`, `Follow-up Task`, `Feedback target` |

Common Reference, Archive, Governance Reference, Memory, Progress, and README
profiles keep their current relationship H2 contract and use `bodyContract:
null`; their role-specific form structure remains enforced by headings and
frontmatter profiles.

## Goals & In-Scope

- Upgrade the registry and schema from v4 to v5 without adding frontmatter.
- Replace the combined native exception with three format-specific profiles
  whose existing `template` field owns the mapping.
- Remove duplicated route/status/profile inventories from README, support,
  validators, and compatibility fixtures.
- Normalize every Stage 99 form and reject authored prompt/placeholder residue.
- Validate lifecycle table shape, identifier syntax, linked profile families,
  and reciprocal evidence.
- Migrate the 37 active consumers and correct PRD 003's false Spec 006 current
  pointer from the mutable PRD surface.
- Enable production enforcement only after all current consumers pass.
- Record Current audit disposition without altering the original observation
  boundary or score.

## Non-Goals & Out-of-Scope

- Rewriting completed or accepted historical bodies.
- Adding document IDs, created dates, reviewer fields, relationship arrays, or
  schema-version frontmatter.
- Renumbering PRD, ARD, ADR, Spec, Plan, Task, operations, or incident records.
- Creating a fabricated operational incident or claiming a live tabletop.
- Removing consumer-free canonical forms.
- Moving SDLC material outside `docs/**`.
- Changing Kubernetes manifests, GitOps desired state, infrastructure, secrets,
  provider adapters, or remote CI settings.

## Work Breakdown

| ID | Work item | Dependency | Primary proof | Commit |
| --- | --- | --- | --- | --- |
| TLCN-001 | Establish reciprocal Spec/Plan/Task execution lineage | Spec 033 approval | Strict link/index validation | `docs(execution): plan template lifecycle normalization` |
| TLCN-002 | Add schema v5, typed body contract, native profiles, and historical diff proof | TLCN-001 | Registry RED/GREEN self-tests | `refactor(contracts): add registry v5 body contracts` |
| TLCN-003 | Consolidate Stage 99 support and README authority | TLCN-002 | Zero complete route mirrors or stale cloud claims | `docs(governance): separate template support authority` |
| TLCN-004 | Normalize 27 Markdown and three native forms and reject authored starter residue | TLCN-003 | Template and placeholder fixtures | `refactor(templates): normalize canonical document forms` |
| TLCN-005 | Validate lifecycle table shape and cross-document relations | TLCN-004 | Local and cross-document RED/GREEN fixtures | `test(docs): validate lifecycle traceability contracts` |
| TLCN-006 | Migrate 13 active Stage 01-03 consumers and correct PRD 003 | TLCN-005 | Core lifecycle tables and reciprocal links | `docs(sdlc): migrate current core lifecycle documents` |
| TLCN-007 | Migrate 24 active Stage 05 consumers | TLCN-006 | Operations lifecycle tables and role boundaries | `docs(operations): migrate current operating documents` |
| TLCN-008 | Enable strict body enforcement and close audit/execution evidence | TLCN-007 | Full gates, history diff, independent whole-branch review | `docs(execution): close template lifecycle normalization` |

### Task 1: Establish Reciprocal Execution Lineage

**Files:**

- Modify: `docs/03.specs/033-template-lifecycle-contract-normalization/spec.md`
- Create: `docs/04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`

**Interfaces:**

- Consumes: approved Spec 033 and the five approved design sections.
- Produces: active Task rows `TLCN-001` through `TLCN-008`, reciprocal links,
  and v5-ready Plan/Task traceability tables.

- [x] **Step 1: Prove the execution files are initially absent**

```bash
test ! -e docs/04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md
test ! -e docs/04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md
```

Expected: both commands exit 0 before this planning commit.

- [x] **Step 2: Create the Plan, Task, reciprocal links, indexes, and ledger rows**

The Plan contains the exact eight work items above. The Task uses columns
`ID`, `Upstream criterion`, `Work item`, `Owner`, `Status`, `Result`, and
`Evidence`; `TLCN-001` is `Done` and all later rows are `Queued`. Spec, Plan,
and Task contain relative reciprocal links. The migration ledger inventory
count increases by two and records one reviewed row for each new execution
document.

- [x] **Step 3: Validate and commit the planning unit**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
git diff --check
git add docs/03.specs/033-template-lifecycle-contract-normalization/spec.md \
  docs/04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md \
  docs/04.execution/tasks/README.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
git commit -m "docs(execution): plan template lifecycle normalization"
```

Expected: all validators pass and one planning commit is created.

### Task 2: Add Registry v5 Body Contracts and Native Mappings

**Files:**

- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/document_contracts.py`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `tests/fixtures/markdown-profiles.json`
- Modify: `docs/03.specs/033-template-lifecycle-contract-normalization/spec.md`

**Interfaces:**

- Consumes: the schema and table interfaces in this Plan.
- Produces: `BodyContract`, `IdentifierColumn`, three native profiles, 64 total
  profiles, and registry-derived form inventory.

- [ ] **Step 1: Add failing registry mutation cases**

Add exact mutations for missing `bodyContract`, unknown body field, section not
in required H2, status outside `statusDomain`, empty/duplicate columns, unknown
source/target profile, template/source drift, missing native template, and
overlapping native route. Replace exhaustive `profileCoverage` and
`templateCoverage` snapshots with independent `routingCases` for PRD, Spec
template, OpenAPI, GraphQL, protobuf, and a retired cloud path.

Run:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
```

Expected: FAIL with the new v5 mutation cases unimplemented.

- [ ] **Step 2: Implement the typed contract**

Add these immutable types to `scripts/document_contracts.py`:

```python
@dataclass(frozen=True)
class IdentifierColumn:
    column: str
    kind: Literal["requirement", "criterion", "work-item"]


@dataclass(frozen=True)
class BodyContract:
    section: str
    table_heading: str
    enforced_statuses: tuple[str, ...]
    required_columns: tuple[str, ...]
    identifier_columns: tuple[IdentifierColumn, ...]
    source_link_column: str | None
    target_link_column: str | None
    allowed_source_profile_ids: tuple[str, ...]
    allowed_target_profile_ids: tuple[str, ...]
    reciprocal_evidence: bool
    allow_explicit_exclusion: bool
```

Add `body_contract: BodyContract | None` to `DocumentProfile`, parse the camel
case JSON fields in `_profile_from_mapping()`, and validate all cross-field
invariants in `validate_registry()` with stable `REGISTRY_BODY_*` diagnostics.

- [ ] **Step 3: Upgrade the JSON schema and registry**

Set schema `$id` to
`https://hy-home.k8s/schemas/document-profiles-5.schema.json` and
`schemaVersion` to `5`. Require `bodyContract` on every profile. Add the
profile-specific column contracts in the table above with production
`enforcedStatuses: []` for the compatibility window.

Replace `exception/native-contract` with:

```json
[
  {"id": "exception/native-contract-openapi", "template": "docs/99.templates/templates/sdlc/specs/openapi.template.yaml"},
  {"id": "exception/native-contract-graphql", "template": "docs/99.templates/templates/sdlc/specs/schema.template.graphql"},
  {"id": "exception/native-contract-protobuf", "template": "docs/99.templates/templates/sdlc/specs/service.template.proto"}
]
```

Each profile receives one anchored route for its exact native basename. Add
Spec `033` to `programLineage.specs`.

- [ ] **Step 4: Remove frozen exhaustive owners and derive form inventory**

Delete `DOCUMENT_PROFILE_CONTRACT_V3`,
`DOCUMENT_PROFILE_CONTRACT_V3_FIELDS`, semantic digest functions, the frozen
profile-ID tuple, and the native bridge tuple. Derive source/template parity and
all 27 Markdown plus three native template paths from the registry. Keep
targeted mutation cases and fail if any physical form is absent or unowned.

- [ ] **Step 5: Re-run registry and aggregate gates**

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
```

Expected: PASS with schema v5, 64 profiles, 27 Markdown templates, and three
native templates.

- [ ] **Step 6: Commit**

```bash
git add docs/99.templates/support/document-profiles.schema.json \
  docs/99.templates/support/document-profiles.json \
  scripts/document_contracts.py \
  scripts/validate-document-contract-registry.py \
  scripts/validate-repo-quality-gates.sh \
  tests/fixtures/document-contracts/registry-cases.json \
  tests/fixtures/document-contracts/template-compatibility.json \
  tests/fixtures/markdown-profiles.json \
  docs/03.specs/033-template-lifecycle-contract-normalization/spec.md
git commit -m "refactor(contracts): add registry v5 body contracts"
```

### Task 3: Separate Stage 99 Support and README Authority

**Files:**

- Modify: `docs/99.templates/README.md`
- Modify: `docs/99.templates/support/README.md`
- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/99.templates/support/common-documentation-governance.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `scripts/validate-repo-quality-gates.sh`

**Interfaces:**

- Consumes: registry v5 as the only exhaustive machine owner.
- Produces: human rationale and procedure with no complete route or status
  mirror.

- [ ] **Step 1: Record current duplicate and stale-contract RED evidence**

```bash
rg -n 'Current Route Map|Template-Folder Mapping|examples/<provider>/docs|routed example-local' \
  docs/99.templates
```

Expected: matches in the two route mirrors and stale cloud support prose.

- [ ] **Step 2: Consolidate support ownership**

Remove the complete route map from `template-routing.md`, exact route/status
copies from the other support documents, and the retired example-local claim.
Keep exact-one-profile procedure, role rationale, numbering and feedback-loop
rationale, five-key meanings, README/common roles, and legacy cleanup in their
single owners. Update support version references from v4 to v5.

- [ ] **Step 3: Reduce Stage 99 README to navigation**

Preserve its registry-required H2 profile. Delete the H3 complete mapping and
duplicated archive/reference/lifecycle policy bodies. Keep concise form-family
inventory, canonical support links, and the four-step workflow: classify,
copy, replace prompts with topic evidence, validate.

- [ ] **Step 4: Replace mirror assertions with registry-owner assertions**

Remove `template_route_pairs()` calls that require identical README and
support tables. Retain a mutation proof that every registry-owned template path
exists and that every physical form is owned by exactly one profile.

- [ ] **Step 5: Prove the conflict is gone and commit**

```bash
if rg -n 'examples/<provider>/docs|routed example-local' docs/99.templates/support; then exit 1; fi
test "$(rg -n '^### Current Route Map$|^### Template-Folder Mapping$' docs/99.templates | wc -l)" -eq 0
python3 scripts/validate-markdown-profiles.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
git add docs/99.templates scripts/validate-repo-quality-gates.sh
git commit -m "docs(governance): separate template support authority"
```

Expected: no stale route claim or full route-map heading and all gates pass.

### Task 4: Normalize Canonical Forms and Starter-Residue Validation

**Files:**

- Modify: `docs/99.templates/templates/common/archive-tombstone.template.md`
- Modify: `docs/99.templates/templates/common/governance-reference.template.md`
- Modify: `docs/99.templates/templates/common/memory.template.md`
- Modify: `docs/99.templates/templates/common/progress.template.md`
- Modify: `docs/99.templates/templates/common/readme-collection-index.template.md`
- Modify: `docs/99.templates/templates/common/readme-implementation.template.md`
- Modify: `docs/99.templates/templates/common/readme-repository.template.md`
- Modify: `docs/99.templates/templates/common/readme-snapshot-pack.template.md`
- Modify: `docs/99.templates/templates/common/readme-stage-index.template.md`
- Modify: `docs/99.templates/templates/common/readme-workspace-staging.template.md`
- Modify: `docs/99.templates/templates/common/reference.template.md`
- Modify: `docs/99.templates/templates/common/template-support.template.md`
- Modify: `docs/99.templates/templates/sdlc/architecture/adr.template.md`
- Modify: `docs/99.templates/templates/sdlc/architecture/ard.template.md`
- Modify: `docs/99.templates/templates/sdlc/execution/plan.template.md`
- Modify: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/guide.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/incident.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/policy.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/postmortem.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/runbook.template.md`
- Modify: `docs/99.templates/templates/sdlc/requirements/prd.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/agent-design.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/api-spec.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/data-model.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/spec.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/tests.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/openapi.template.yaml`
- Modify: `docs/99.templates/templates/sdlc/specs/schema.template.graphql`
- Modify: `docs/99.templates/templates/sdlc/specs/service.template.proto`
- Modify: `scripts/validate-markdown-profiles.py`
- Modify: `tests/fixtures/markdown-profiles.json`
- Modify: `scripts/validate-repo-quality-gates.sh`

**Interfaces:**

- Consumes: registry v5 headings, template mappings, and body contracts.
- Produces: 27 Markdown forms, three native forms, and deterministic authored
  residue diagnostics.

- [ ] **Step 1: Add failing starter-residue cases**

Add cases for `title: '[Document Title]'`, H1 `# [Document Title]`,
`<!-- Author prompt: replace this text -->`, the old target-path HTML marker,
and the old shared replacement paragraph. Keep template-mode positive cases.

Run:

```bash
python3 scripts/validate-markdown-profiles.py --root . --self-test
```

Expected: FAIL because authored placeholder title/H1/comment cases are accepted.

- [ ] **Step 2: Implement scoped placeholder checks**

Add `FM-TITLE-PLACEHOLDER`, `BODY-H1-PLACEHOLDER`, and
`BODY-AUTHOR-PROMPT` diagnostics. Check frontmatter title and H1 for exact
starter delimiters; reject `Author prompt:`, the legacy target-path marker, and
the retired shared paragraph only for authored profiles. Do not reject example
syntax in fenced code.

- [ ] **Step 3: Normalize every Markdown form**

Remove target comments and generic repeated prose. Use only short
`<!-- Author prompt: ... -->` comments, profile H2 headings, type-specific
tables, and the exact `Lifecycle Traceability` table. Keep the five-key order.
Plan gains dependency/gate fields; Task gains upstream/result/evidence fields;
Guide declares how-to/tutorial/concept in body; Policy keeps controls and
responsibilities separate from procedure; Runbook gains expected result and
stop/escalation fields; Incident and Postmortem retain separate evidence roles.

- [ ] **Step 4: Normalize native forms**

Remove route and owner-document comments from OpenAPI, GraphQL, and protobuf
forms. Retain syntactically valid native starter content and no Markdown
frontmatter.

- [ ] **Step 5: Prove forms and residue validation and commit**

```bash
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
if rg -n 'Target:[[:space:]]+docs/|Replace every placeholder|Describe the topic-specific' \
  docs/99.templates/templates; then exit 1; fi
bash scripts/validate-repo-quality-gates.sh .
git add docs/99.templates/templates scripts/validate-markdown-profiles.py \
  tests/fixtures/markdown-profiles.json scripts/validate-repo-quality-gates.sh
git commit -m "refactor(templates): normalize canonical document forms"
```

### Task 5: Validate Lifecycle Tables and Cross-Document Relations

**Files:**

- Modify: `scripts/validate-markdown-profiles.py`
- Modify: `tests/fixtures/markdown-profiles.json`
- Modify: `scripts/validate-links-and-owners.py`
- Modify: `tests/fixtures/links-and-owners.json`
- Modify: `scripts/validate-repo-quality-gates.sh`

**Interfaces:**

- Consumes: typed `BodyContract` and normalized forms.
- Produces: `_body_contract_diagnostics()` for local semantics and
  `_body_contract_link_diagnostics()` for linked profile and reciprocal
  semantics. Both validators accept `--body-contracts audit`; this forces
  non-null body contracts over `draft|active` consumers during migration while
  the registry's production `enforcedStatuses` remains empty. The default
  `registry` behavior always respects the registry value.

- [ ] **Step 1: Add failing local table cases**

Add positive and negative sources for missing table, wrong H3, header order,
duplicate header, blank required cell, invalid requirement/criterion/work-item
ID, explicit exclusion, and status scope. Fixture registries set
`enforcedStatuses: ["draft", "active"]`; production remains empty.
Add parser cases proving `--body-contracts audit` forces `draft|active` only
and the default mode continues to honor production `enforcedStatuses`.

Expected command and result:

```bash
python3 scripts/validate-markdown-profiles.py --root . --self-test
```

Expected: FAIL with unimplemented `BODY-CONTRACT-*` rule IDs.

- [ ] **Step 2: Implement local body-contract validation**

Reuse fenced-code and HTML-comment aware section scanning. Find the exact H3
inside the configured H2, parse the first GFM table, require exact columns and
non-empty cells, and validate configured identifier columns. Templates always
validate table shape; authored documents validate only when their status is in
`enforced_statuses`, unless `--body-contracts audit` forces `draft|active`.

- [ ] **Step 3: Add failing cross-document cases**

Add a positive PRD -> Spec -> Plan -> Task tree and Incident/Postmortem -> Task
feedback tree. Add disallowed source profile, disallowed target profile,
missing reciprocal link, broken link, and exclusion-without-reason cases.

```bash
python3 scripts/validate-links-and-owners.py --root . --self-test
```

Expected: FAIL with unimplemented `BODY-LINK-*` diagnostics.

- [ ] **Step 4: Implement cross-document contract validation**

Reuse `_exact_heading_section()`, `_gfm_table_cells()`, `_extract_links()`, and
the selected profile map. Validate configured source and target link columns,
allowed profile IDs, explicit exclusions, and reciprocal evidence. Keep
ordinary link existence and duplicate-current-owner diagnostics independent.
Apply the same `--body-contracts {registry,audit}` contract to this validator.

- [ ] **Step 5: Run focused and aggregate tests and commit**

```bash
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts audit
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts audit
bash scripts/validate-repo-quality-gates.sh .
git add scripts/validate-markdown-profiles.py \
  tests/fixtures/markdown-profiles.json \
  scripts/validate-links-and-owners.py \
  tests/fixtures/links-and-owners.json \
  scripts/validate-repo-quality-gates.sh
git commit -m "test(docs): validate lifecycle traceability contracts"
```

### Task 6: Migrate Active Stage 01-03 Consumers

**Files:**

- Modify: `docs/01.requirements/001-argo-rollouts-progressive-delivery.md`
- Modify: `docs/01.requirements/002-argo-notifications-slack.md`
- Modify: `docs/01.requirements/003-workspace-agent-governance-platform.md`
- Modify: `docs/01.requirements/004-current-local-gitops-platform.md`
- Modify: `docs/02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md`
- Modify: `docs/02.architecture/requirements/0005-argo-notifications-slack.md`
- Modify: `docs/02.architecture/requirements/0006-workspace-agent-governance-platform.md`
- Modify: `docs/02.architecture/requirements/0007-current-local-gitops-platform.md`
- Modify: `docs/03.specs/004-argo-rollouts-progressive-delivery/spec.md`
- Modify: `docs/03.specs/005-argo-notifications-slack/spec.md`
- Modify: `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
- Modify: `docs/03.specs/008-current-local-gitops-platform/spec.md`
- Modify: `docs/03.specs/033-template-lifecycle-contract-normalization/spec.md`
- Modify only if inventory/currentness changes: Stage 01, 02, and 03 README indexes

**Interfaces:**

- Consumes: lifecycle table forms and validators with production enforcement
  still disabled.
- Produces: 13 topic-specific tables and a corrected PRD 003 current pointer.

- [ ] **Step 1: Capture the exact migration set**

```bash
find docs/01.requirements docs/02.architecture docs/03.specs -type f -name '*.md' -print0 |
while IFS= read -r -d '' file; do
  status=$(sed -n '1,8p' "$file" | sed -n 's/^status: //p')
  case "$status" in draft|active) printf '%s\n' "$file";; esac
done | sort
```

Expected: exactly the 13 paths listed above.

- [ ] **Step 2: Add PRD and ARD lifecycle tables**

Map every existing `REQ-PRD-FUN-*` and `REQ-PRD-MET-*` ID to its existing
acceptance text and verified downstream owner. PRD 001 maps to ARD 0004 and
Spec 004; PRD 002 to ARD 0005 and Spec 005; PRD 004 to ARD 0007 and Spec 008.
PRD 003 maps architecture to ARD 0006 and ADR 0013 but replaces the false
Spec 006 canonical claim with `N/A — no single current Spec owns the Stage 00
platform; completed tranches remain historical evidence`. Do not edit Spec 006
to manufacture reciprocity.

- [ ] **Step 3: Add active Spec lifecycle tables**

Spec 004 references PRD 001, Spec 005 references PRD 002, Spec 008 references
PRD 004, and Spec 033 references PRD 005. Spec 006 records the explicit
repository-governance exclusion already stated in its Related inputs. Use only
existing `VAL-*` criteria and real verification methods.

- [ ] **Step 4: Validate topic fidelity**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts audit
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts audit
rg -n '006-workspace-harness-gap-analysis/spec.md' \
  docs/01.requirements/003-workspace-agent-governance-platform.md
```

Expected: strict validators pass and the final command returns no PRD 003
canonical Spec link.

- [ ] **Step 5: Commit**

```bash
git add docs/01.requirements docs/02.architecture/requirements docs/03.specs
git commit -m "docs(sdlc): migrate current core lifecycle documents"
```

### Task 7: Migrate Active Stage 05 Consumers

**Files:**

- Modify: `docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md`
- Modify: `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`
- Modify: `docs/05.operations/guides/0003-platform-expansion-bootstrap-guide.md`
- Modify: `docs/05.operations/guides/0006-argocd-prometheus-grafana-guide.md`
- Modify: `docs/05.operations/guides/0007-k8s-observability-bootstrap-guide.md`
- Modify: `docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md`
- Modify: `docs/05.operations/guides/0009-llm-wiki-curation-guide.md`
- Modify: `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
- Modify: `docs/05.operations/policies/0001-k8s-gitops-operations-policy.md`
- Modify: `docs/05.operations/policies/0002-wsl2-k3d-gitops-ha-operations-policy.md`
- Modify: `docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md`
- Modify: `docs/05.operations/policies/0004-rollouts-notifications-headlamp-policy.md`
- Modify: `docs/05.operations/policies/0005-observability-platform-operations-policy.md`
- Modify: `docs/05.operations/policies/0006-k8s-observability-operations-policy.md`
- Modify: `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`
- Modify: `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`
- Modify: `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`
- Modify: `docs/05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`
- Modify: `docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`
- Modify: `docs/05.operations/runbooks/0007-kiali-observability-connectivity-runbook.md`
- Modify: `docs/05.operations/runbooks/0008-argocd-metrics-prometheus-runbook.md`
- Modify: `docs/05.operations/runbooks/0009-k8s-observability-runbook.md`
- Modify: `docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md`
- Modify: `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md`
- Modify only if inventory/currentness changes: Stage 05 README indexes

**Interfaces:**

- Consumes: role-specific Guide, Policy, and Runbook body contracts.
- Produces: 24 topic-specific operating handoff tables with no policy/procedure
  duplication.

- [ ] **Step 1: Confirm the active operations set**

Run the top-frontmatter inventory command from Task 6 against
`docs/05.operations`. Expected: eight Guides, seven Policies, nine Runbooks,
and no active Incident or Postmortem record.

- [ ] **Step 2: Migrate Guides and Policies**

For each Guide, classify `Guide Type` as how-to, tutorial, or concept from its
actual audience and steps, then map the existing promoted owner and operating
surface. For each Policy, map the existing promoted owner, control owner, and
enforcement surface. Do not copy Runbook command sequences into Policy.

- [ ] **Step 3: Migrate Runbooks**

Map promoted owner, actual trigger/control, and evidence or recovery owner.
Retain existing commands and safety boundaries. Where a procedure table is
introduced, use `Step`, `Action`, `Expected result`, and `Stop / escalation`.
Do not claim live verification from repository-static evidence.

- [ ] **Step 4: Validate and commit**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts audit
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts audit
bash scripts/validate-repo-quality-gates.sh .
git add docs/05.operations
git commit -m "docs(operations): migrate current operating documents"
```

### Task 8: Enable Strict Enforcement and Close Evidence

**Files:**

- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/03.specs/033-template-lifecycle-contract-normalization/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: all migrated current consumers and green fixture validation.
- Produces: production `draft|active` enforcement, immutable-history proof,
  audit disposition, completed execution evidence, and final handoff.

- [ ] **Step 1: Enable production status enforcement**

Set every applicable authored SDLC `bodyContract.enforcedStatuses` to
`["draft", "active"]`. Keep common and frontmatter-free profiles null. Ensure
template profiles retain source-contract parity.

- [ ] **Step 2: Run the historical-body diff guard**

```bash
python3 - <<'PY'
import subprocess
baseline = 'ac3ba71959ab'
changed = subprocess.check_output(
    ['git', 'diff', '--name-only', baseline, '--',
     'docs/01.requirements', 'docs/02.architecture/decisions',
     'docs/03.specs', 'docs/04.execution'], text=True
).splitlines()
violations = []
for path in changed:
    old = subprocess.run(
        ['git', 'show', f'{baseline}:{path}'], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    if old.returncode:
        continue
    head = '\n'.join(old.stdout.splitlines()[:8])
    if 'status: done' in head or (
        path.startswith('docs/02.architecture/decisions/') and
        'status: accepted' in head
    ):
        violations.append(path)
assert not violations, violations
PY
```

Expected: PASS with zero completed-body or accepted-ADR changes.

- [ ] **Step 3: Record audit and execution disposition**

Append a dated disposition overlay to the Current remediation roadmap without
editing its original finding rows or observation SHA. Mark structural profile,
placeholder, route-owner, and current-consumer body-contract gaps closed;
record real incident/live tabletop evidence as retained because no incident was
fabricated. Set all Task rows Done with concrete commit/evidence links, set
Plan and Spec status Done, update indexes and ledger dispositions, and append a
progress entry.

- [ ] **Step 4: Run the full validation suite**

```bash
git diff --check
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts audit
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts audit
bash scripts/validate-repo-quality-gates.sh .
env TMPDIR=/tmp pre-commit run --all-files
```

Expected: all required gates PASS. Optional tool SKIP remains distinct from
PASS; remote and live verification remain DEFER.

- [ ] **Step 5: Obtain independent whole-branch review and commit closure**

After requirements and quality reviewers report no unresolved findings:

```bash
git add docs/99.templates/support/document-profiles.json \
  docs/99.templates/support/documentation-contract.md \
  docs/99.templates/support/sdlc-governance.md \
  docs/03.specs docs/04.execution \
  docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/00.agent-governance/memory/progress.md
git commit -m "docs(execution): close template lifecycle normalization"
```

## Verification Plan

| ID | Level | Command or evidence | Pass criteria |
| --- | --- | --- | --- |
| VAL-PLN-001 | Registry | Registry self-test and strict mode | Schema v5, 64 profiles, 27 Markdown and three native forms; zero route ambiguity. |
| VAL-PLN-002 | Metadata | Markdown self-test and strict mode | Five-key order; placeholder and prompt residue rejected. |
| VAL-PLN-003 | Body semantics | Local body-contract fixtures | Exact H3/table/header/cell/identifier behavior by status. |
| VAL-PLN-004 | Cross-document | Links/owners self-test and strict mode | Allowed profiles, reciprocal evidence, explicit exclusions, and current owners are valid. |
| VAL-PLN-005 | Support ownership | Focused `rg` scans | No complete route mirror or stale example-local route claim. |
| VAL-PLN-006 | Template forms | Registry-derived inventory and residue scan | Every physical form has one owner; generic repeated guidance is zero. |
| VAL-PLN-007 | Consumer migration | Exact active inventory plus strict mode | All 37 active consumers satisfy body contracts; accepted/done history is excluded. |
| VAL-PLN-008 | History | Baseline diff guard | Zero modified completed PRD/Spec/Plan/Task and accepted ADR bodies. |
| VAL-PLN-009 | Repository | Quality gate and all-files pre-commit | Required gates PASS with SKIP/DEFER accurately labeled. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Enabling semantic checks before migration makes intermediate commits red | High | Keep production `enforcedStatuses` empty until Task 8; fixture registries exercise strict behavior first. |
| Registry DSL becomes a general-purpose validator language | High | Closed v5 fields, three identifier kinds, one table per profile, no arbitrary expressions. |
| Removing frozen fixtures removes independent drift detection | High | Add behavior and mutation cases before deleting exhaustive snapshots. |
| Generic placeholder scans reject valid technical examples | High | Check title/H1 and exact author markers outside fenced code only. |
| Current links are mistaken for historical ownership | High | Migrate only top-frontmatter `draft|active` documents and allow reasoned exclusions. |
| Completed evidence is rewritten to satisfy new semantics | Critical | Run the baseline history guard before final commit and review its changed-path list. |
| Policy and Runbook content converges again | Medium | Enforce separate role tables and review only traceability/role-bearing sections. |
| Incident readiness is overstated | High | Test form semantics with fixtures and keep real/live tabletop disposition retained. |
| Worktree filesystem cannot create FIFO during pre-commit | Medium | Set `TMPDIR=/tmp`; do not weaken the self-test. |

## Completion Criteria

- Registry/schema v5 is the only exhaustive machine contract and strict routing
  reports zero uncovered or ambiguous paths.
- All three native formats select a distinct registry profile and canonical
  native template.
- Stage 99 README and support documents contain no duplicate complete route or
  status inventory and no active retired-cloud claim.
- All 27 Markdown and three native forms contain only their form responsibility.
- Authored starter titles, H1 placeholders, author prompts, invalid lifecycle
  tables, disallowed linked profiles, and missing reciprocal evidence fail
  deterministic fixtures.
- The exact 37 active consumers pass with topic-specific content; PRD 003 no
  longer claims Spec 006 as its canonical current Spec.
- Completed PRD/Spec/Plan/Task and accepted ADR bodies are unchanged.
- Current audit disposition, migration ledger, Spec, Plan, Task, indexes, and
  progress evidence agree on the completed state.
- Full repository-static validation passes and remote/live state remains
  explicitly unverified.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-TLCN-001 through VAL-TLCN-005](../../03.specs/033-template-lifecycle-contract-normalization/spec.md#success-criteria--verification-plan) | TLCN-002 through TLCN-004 registry, support, and form ownership | [Template Lifecycle Contract Normalization Task](../tasks/2026-07-14-template-lifecycle-contract-normalization.md) |
| [VAL-TLCN-006 and VAL-TLCN-007](../../03.specs/033-template-lifecycle-contract-normalization/spec.md#success-criteria--verification-plan) | TLCN-005 through TLCN-007 semantic validation and active migration | [Template Lifecycle Contract Normalization Task](../tasks/2026-07-14-template-lifecycle-contract-normalization.md) |
| [VAL-TLCN-008 through VAL-TLCN-010](../../03.specs/033-template-lifecycle-contract-normalization/spec.md#success-criteria--verification-plan) | TLCN-008 history protection, audit disposition, and closure | [Template Lifecycle Contract Normalization Task](../tasks/2026-07-14-template-lifecycle-contract-normalization.md) |

### Authorities and evidence

- **Spec**: [Template Lifecycle Contract Normalization](../../03.specs/033-template-lifecycle-contract-normalization/spec.md)
- **Task**: [Template Lifecycle Contract Normalization Task](../tasks/2026-07-14-template-lifecycle-contract-normalization.md)
- **Registry ADR**: [Declarative Document Contract Registry](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- **Current audit**: [SDLC, Document Lifecycle, and Frontmatter](../../90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md)
- **Research basis**: [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
