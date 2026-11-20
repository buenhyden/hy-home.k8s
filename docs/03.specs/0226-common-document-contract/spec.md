---
title: "Common Document Contract"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0226"
---

# Common Document Contract Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This change gives document authors and validators one common template meaning
while keeping each document role's own content and native output syntax.
Authors, Stage 99 maintainers and CI consumers use this contract.

### 책임과 적용 범위

This Spec owns the P04 change contract for this workspace. The current
[requirement package](../../01.requirements/0003-workspace-agent-governance-platform.md)
owns lasting document governance; [Stage 99](../../99.templates/README.md)
owns the machine profiles and forms. This draft does not approve an edition,
accept a criterion or change the completed residue-transfer criteria of
[SPEC-0223](../0223-work-residue-handoff/spec.md).

## 내용 계약

### 입력과 전제

The user selected P04-TEMPLATES from package 1.1.0 on 2026-11-20. Its D04
design and bundled common contract are candidate inputs, not an already
adopted repository edition. P00–P03 and the eleven completed streams provide
predecessor evidence. The existing 20-field TemplateDefinition, role-specific
tables, numeric-version grammar and valid links remain required behavior.

### 본문과 규칙

#### Overview

##### Goal

Bind the bundled common metadata, 32 payload kinds and four-H2/eight-H3
Markdown envelope to this repository's actual profiles, templates, producer,
parser, validator, generator and affected-check selector. Preserve the meaning
of existing approval and execution records.

###### Owning Requirements

[REQ-0003-FR-0006, FR-0012, FR-0013 and FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md)
require one form owner, exact routes and role boundaries. FR-0009 requires
native provider metadata to remain separate. FR-0015 and FR-0020 govern
preservation and succession; IF-0001 governs a single owner switch. NFR-0002
governs selected validation. The [workspace architecture](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
places the machine document contract in Stage 99.

##### Consumers

Stage 99 registry and template definitions, document generator, frontmatter and
Markdown readers, lifecycle and link checkers, affected CI selection, authors
and native provider asset consumers.

#### Scope

##### In Scope

The common contract's kind, metadata, lifecycle, scope, payload and relation
meanings; the common authored Markdown envelope and template guidance;
compatibility of native asset generation; current consumers, targeted
regressions and one relevant corpus check.

##### Out of Scope

Completed evidence rewriting, earlier user acceptance, wholesale renumbering
or history removal, live cluster/provider operation, another workspace, later
P prompts and general external HTTP availability checks. Existing accepted
retained forms keep their recorded meaning until their authorized disposition.

#### Behavior Contract

##### Inputs and Outputs

Each current profile maps explicitly to one common kind and scope; absent
profile kinds remain declared capabilities, not fabricated forms. The ordered
common envelope carries role content under `본문과 규칙` and meaningful guidance
under each other section. Existing status, type and layer fields are interpreted
through one adapter, without parallel authorities. Native Markdown and
JSON/YAML/TOML/Proto outputs preserve their consumer syntax; the definition
document may carry the common envelope without leaking it into those outputs.

Requirement interface meaning stays linked to functional or quality
requirements. Acceptance IDs are scoped to this Spec and begin at AC-0001. Existing
`VAL-*` identifiers and their readers remain valid until the coordinated
display conversion under P17. Evidence
identifies the actual candidate and dependencies without a universal full-SHA
or whole-corpus pin for every PASS. Document numeric `X.Y.Z` is distinct from
registry edition, lifecycle and criterion acceptance; incompatible changes
raise MAJOR and reset lower components, compatible additions raise MINOR and
reset PATCH, and compatible corrections raise PATCH.

The relationship graph distinguishes `requires`, `designs`, `implements`,
`verifies`, `operates`, `defines` and `cites`. Relative Markdown links and
renderer fragments resolve against their actual source; moved/deleted targets
select their inbound references. External URLs and example placeholders do
not become local file dependencies.

##### Failure Behavior

Unknown kinds or statuses, duplicate semantic owners, invalid version text,
broken local links and incompatible template/generated output fail their
owning check. A missing native provider observation is reported separately
from static compatibility. No failed check or missing approval becomes PASS
through default mappings, skipped CI selection or status promotion.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Every current Stage 99 profile and template definition has an explicit common-kind, metadata and payload disposition; the existing 20-field definition and valid role tables remain usable. |
| AC-0002 | Governed Markdown templates and generated documents use the common four-H2/eight-H3 envelope, with role payload and useful K8s traceability preserved; native outputs retain their syntax. |
| AC-0003 | The local common contract has a recorded identity, edition and digest; actual consumers read it through one metadata adapter, and partial adoption does not invent approval. |
| AC-0004 | Requirement interfaces, Spec criterion display, Task evidence identity and lifecycle map without losing prior meaning or turning validation into acceptance. |
| AC-0005 | Document versions accept only complete ASCII numeric triplets, and edition changes follow MAJOR/MINOR/PATCH compatibility and lower-component reset. |
| AC-0006 | Relationships have distinct meaning; local links, fragments and moved/deleted inbound references validate without universal backlinks or commit-time HTTP availability. |
| AC-0007 | Representative documents from actual templates pass their consuming readers, and one relevant corpus check plus selected local and hosted checks validate the final candidate. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| document-contract-registry | Profile, form and common-contract binding are coherent | Candidate registry, schemas and templates | Repository static | Stage 99 contract changes | Task Results |
| document-contract-tests | Parser, generator, metadata and native negative cases behave as specified | Candidate source and fixtures | Synthetic and repository static | Changed producer or reader | Task Results |
| document-lifecycle | Current statuses, IDs and retained records remain valid | Candidate and previous tree | Repository static | Document or contract changes | Task Results |
| links-and-owners | Local paths, fragments and inbound references resolve | Changed documents and deletion closure | Repository static | Changed links or moves | Task Results |
| pull-request | Hosted affected checks run on the reviewed candidate | PR base-to-merge input | Hosted, separate from local | Delivery | PR run and Task Results |

###### Normative and Evidence

[Document authoring](../../00.workspace/03.process/document-authoring.md),
[document lifecycle](../../00.workspace/03.process/document-lifecycle.md) and
[quality](../../00.workspace/04.quality/quality.md) own execution rules.
Actual implementation and results belong to the [Task](01.tasks/tsk-0001-common-document-contract.md).

###### Historical and Navigation

[SPEC-0223](../0223-work-residue-handoff/spec.md) keeps the completed residue
transfer and later P00–P03 handoff evidence. The original 11 accepted work
streams are historical inputs, not P04 work units.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Registry and profile checks |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Template and generator checks |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Adapter contract tests |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Lifecycle and identity tests |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0005 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Version tests |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0006 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Link and inbound check |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0007 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Corpus and selected CI checks |

## 적용과 확인

### 적용 방법

The [Plan](plan.md) orders one bounded P04 implementation across the canonical
owners. Consumers change with the contract; existing evidence keeps its
recorded shape. P17 owns the coordinated display renumbering.

### 확인 기준

Acceptance requires each criterion's observed evidence and a separate user
decision. Draft authoring and a passing static form check establish neither
approval nor native execution.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| requires | [Stage 99 common contract](../../99.templates/01.contracts/common-document-contract.json) |

Navigate to the [Plan](plan.md), [Task](01.tasks/tsk-0001-common-document-contract.md)
and [Stage 99](../../99.templates/README.md). These relation rows classify
dependencies; they do not assert contract approval or criterion acceptance.

### 외부 근거

The supplied D04 design summarizes SemVer, CommonMark, URI and Diátaxis for
this change. Those sources inform the local contract; the current repository
owners decide its adopted behavior.
