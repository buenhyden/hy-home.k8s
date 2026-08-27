---
title: 'Audit: Spec-driven SDLC, Documentation, and Templates'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Spec-driven SDLC, Documentation, and Templates

## Overview

This report audits spec-driven development, Stage 01-05 lifecycle, document
families, templates, profile and README contracts, authoring routes,
integration guides, Diátaxis classification, generated-document boundaries,
and documentation drift at observation commit
`50628b84165479b03efc0a25be075a49c91a9aef`.

## Reference Type

Dated repository-static documentation and SDLC audit. It does not own document
routes, frontmatter, lifecycle transitions, templates, or active SDLC policy.

## Authority Boundary

The Stage 99 registry owns exact routes, profiles, metadata, headings,
templates, lifecycle projections, and relationship roles. Stage 00 owns
authoring procedure, and Stage 01-05 documents own product, architecture,
implementation, execution, and operations truth. This dated report describes
the owners; it does not implement queued Spec 052 documentation-gap work,
reopen its approved negative release-notes decision, or broaden that decision
silently to every possible Release record.

## Scope

Included: PRD, ARD, ADR, Spec, Plan, Task, Guide, Incident, Postmortem, Policy,
Release, and Runbook families; lifecycle, templates, source-template parity,
README profiles, integration guides, Diátaxis mapping, generated-document
boundaries, and evidence producers. Excluded: route/profile/template changes,
historical-pack rewrites, canonical remediation, hosted execution, provider
runtime, credentials, secrets, remote state, and live operations.

## Definitions / Facts

### Spec-driven Development

Stage 01 product intent routes through architecture and Stage 03
specifications to reciprocal Stage 04 Plan/Task evidence, then to stable Stage
05 operations knowledge. Registry body contracts and lifecycle predicates
make those typed relationships enforceable. They do not prove that every
document's topic-specific semantics or runtime procedure is correct.

### Templates

`docs/99.templates/registry.json` contains 64 profiles and is
the exact machine owner. Each of the eleven existing requested families has a
source profile, physical template, corresponding template profile, lifecycle
projection, relationship role, and registry/profile/lifecycle validators.
Registry self-test owns eleven negative template/source-parity mutations.

### Integration Guides

`docs/05.operations/guides/README.md#item-index` and its detailed document
index contain eight numbered guides. The guide profile, physical template,
operations lifecycle, index status/date projection, headings, and links are
repository-static contracts. Usability, command success, and live safety are
not inferred from those checks.

### Documents and Documentation

README files are frontmatter-free and resolve through six explicit README
profiles rather than borrowing adjacent authored-document forms. Generated
`docs/90.references/llm-wiki/wiki-index.md` uses the generated-record exception
and its generator; it is not hand-authored. Diátaxis remains descriptive Stage
90 guidance, while approved Spec 052 DOC-G1 already owns an active Guide Type
decision: `how-to`, `tutorial`, or `concept`. The guide profile requires the
heading, the template names the three values, and all eight guides declare
`how-to`; deterministic registry enum enforcement remains queued in WORK-013.

### SDLC

The requested PRD/ARD/ADR/Spec/Plan/Task/Guide/Policy/Runbook/Incident/
Postmortem families are present and contract-aligned. Release is absent as a
document family: there is no `sdlc/release` profile, target route, physical or
template profile, lifecycle projection, relationship role, stage/index path,
or registry-driven validator admission. Approved Spec 052 DOC-G5 separately
decides that no narrower release-notes type will be created; its Plan and
queued WORK-013 own deliberate-absence text and a conditional future route.
The broader requested `Release` record is not explicitly mapped to that narrow
decision or to another existing evidence owner.

### Document-family Contract Matrix

Validator key: `registry` is
`scripts/validate-document-contract-registry.py#main`; `profile` is
`scripts/validate-markdown-profiles.py#main`; `lifecycle` is
`scripts/validate-document-lifecycle.py#main`; `links` is
`scripts/validate-links-and-owners.py#main`.

| Family | Canonical stage and human index | Machine profile | Physical template | Lifecycle contract | Validator |
| --- | --- | --- | --- | --- | --- |
| PRD | `docs/01.requirements/`; `docs/01.requirements/README.md#document-index` | `sdlc/prd` | `docs/99.templates/templates/requirements/requirement-package.template.md` | product: `draft -> active -> done`; archived preservation allowed | registry/profile/lifecycle/links |
| ARD | `docs/02.architecture/requirements/`; `docs/02.architecture/requirements/README.md#item-index` | `sdlc/ard` | `docs/99.templates/templates/sdlc/architecture/ard.template.md` | architecture-requirement: `draft -> active -> accepted` | registry/profile/lifecycle/links |
| ADR | `docs/02.architecture/decisions/`; `docs/02.architecture/decisions/README.md#item-index` | `sdlc/adr` | `docs/99.templates/templates/architecture/adr.template.md` | architecture-decision: `draft -> active -> accepted` | registry/profile/lifecycle/links |
| Spec | `docs/03.specs/<NNN-topic>/spec.md`; `docs/03.specs/README.md#current-spec-index` | `sdlc/spec` | `docs/99.templates/templates/specs/spec.template.md` | specification: `draft -> active -> done` | registry/profile/lifecycle/links |
| Plan | `docs/04.execution/plans/`; `docs/04.execution/plans/README.md#item-index` | `sdlc/plan` | `docs/99.templates/templates/specs/plan.template.md` | execution pair: `draft -> active -> done` | registry/profile/lifecycle/links |
| Task | `docs/04.execution/tasks/`; `docs/04.execution/tasks/README.md#item-index` | `sdlc/task` | `docs/99.templates/templates/specs/task.template.md` | execution pair: `draft -> active -> done` | registry/profile/lifecycle/links |
| Guide | `docs/05.operations/guides/`; `docs/05.operations/guides/README.md#item-index` | `sdlc/guide` | `docs/99.templates/templates/operations/guide.template.md` | operations: `draft -> active -> accepted` | registry/profile/lifecycle/links |
| Incident | `docs/05.operations/incidents/YYYY/INC-NNN-topic/`; `docs/05.operations/incidents/README.md#item-index` | `sdlc/incident` | `docs/99.templates/templates/operations/incident.template.md` | operations: `draft -> active -> accepted` | registry/profile/lifecycle/links |
| Postmortem | colocated `postmortem.md`; `docs/05.operations/incidents/README.md#item-index` | `sdlc/postmortem` | `docs/99.templates/templates/operations/postmortem.template.md` | operations: `draft -> active -> accepted` | registry/profile/lifecycle/links |
| Policy | `docs/05.operations/policies/`; `docs/05.operations/policies/README.md#item-index` | `sdlc/policy` | `docs/99.templates/templates/operations/policy.template.md` | operations: `draft -> active -> accepted` | registry/profile/lifecycle/links |
| Release | none; Spec 052 DOC-G5 separately rejects a first-class release-notes route | none | none | none; queued WORK-013 will record deliberate absence for release notes | none; no profile means no registry-driven admission |
| Runbook | `docs/05.operations/runbooks/`; `docs/05.operations/runbooks/README.md#item-index` | `sdlc/runbook` | `docs/99.templates/templates/operations/runbook.template.md` | operations: `draft -> active -> accepted` | registry/profile/lifecycle/links |

Spec helpers have separate `sdlc/api-spec`, `sdlc/agent-design`,
`sdlc/data-model`, and `sdlc/tests` profiles under the Spec owner. They are not
additional requested top-level families.

### Supporting-contract Matrix

| Surface | As-Is owner | Enforcement boundary |
| --- | --- | --- |
| README families | `docs/99.templates/registry.json#profiles` owns six `readme/*` profiles and their forms. | Frontmatter-free route/headings and exact active inventory are registry/profile checked. |
| Integration guides | `docs/05.operations/guides/README.md#item-index` plus `sdlc/guide`. | Eight tracked guides are profile/link/index checked; live usability remains `DEFER`. |
| Guide Type / Diátaxis | Spec 052 `#recorded-documentation-gap-disposition` owns DOC-G1 through DOC-G3; the WDTC Plan `#task-14-wdtc-013--disposition-the-documentation-gaps` owns execution. | `Guide Type` heading, three-value template prompt, and eight `how-to` guides exist; registry enum enforcement and recorded deliberate absences remain queued in WORK-013. |
| Generated documents | `docs/90.references/llm-wiki/wiki-index.md` plus `scripts/generate-llm-wiki-index.sh#main`. | `exception/generated-record`; update canonical sources and regenerate, never hand-edit. |

### As-Is / Gap / Target Analysis

| Area | As-Is | Gap | Target |
| --- | --- | --- | --- |
| Existing requested families | Eleven families have source/template/lifecycle/role/validator ownership. | No repository-static contract gap found. | Preserve exact source-template parity and lifecycle ownership. |
| Release | No broad Release profile, path, form, lifecycle, role, or validator admission exists; approved DOC-G5 already rejects a narrower release-notes type. | The broader request is not explicitly mapped to DOC-G5 or another evidence owner, and WORK-013 has not yet recorded the planned deliberate-absence text. | WGIA-009 deduplicates against DOC-G5/WORK-013, preserves the negative release-notes decision, and records the broader semantic mapping without inventing a route. |
| Guide Type / Diátaxis | Approved DOC-G1 decides `how-to`, `tutorial`, `concept`; the profile requires `Guide Type`, the template names the values, and all eight guides declare `how-to`. | The registry does not yet enforce the enum, and queued WORK-013 has not migrated/validated all eight guides or recorded DOC-G2/DOC-G3 absences. | Route the finding to existing WORK-013 and require deterministic enum and migration evidence; do not create a fresh taxonomy decision. |
| Integration guides | Eight guides pass static route/form/index/link contracts. | Static conformance does not prove a reader can safely complete live procedures. | Preserve static conformance and keep usability/live execution `DEFER` until authorized evidence exists. |

### Finding Convention

Material findings require ID, request IDs, scope, expected state, observed
state, exact evidence, evidence depth, verdict, impact, disposition, canonical
owner, verification, uncertainty, and blocker state. Verdict and depth use only
the closed pack vocabularies.

#### WGA-DOC-001 — Eleven requested document families are contract-aligned

- **Request IDs**: `REQ-WGA-005`, `REQ-WGA-016`, `REQ-WGA-019`, `REQ-WGA-023`.
- **Scope**: PRD, ARD, ADR, Spec, Plan, Task, Guide, Incident, Postmortem, Policy, and Runbook route/form/lifecycle/validator ownership.
- **Expected state**: every existing requested family has one source profile, route, physical template, source-linked template profile, lifecycle projection, relationship role, stage index, and deterministic validator route.
- **Observed state**: all eleven families satisfy that shape; the deterministic proof returned `families=11/11 templates=11/11 lifecycles=11/11`, and the registry owns six separate README profiles.
- **Evidence**: `docs/99.templates/registry.json#profiles`; `docs/99.templates/registry.json#documentContracts.lifecycleContracts`; `docs/99.templates/registry.json#documentContracts.roleDecisions`; `docs/99.templates/support/sdlc-governance.md#sdlc-profile-handoff`; `docs/00.agent-governance/rules/stage-authoring-matrix.md#current-contract`; `scripts/validate-document-contract-registry.py#_assert_template_source_parity`; `scripts/validate-document-lifecycle.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: authors and validators resolve the same route, form, lifecycle, and relationship owners for the eleven implemented families.
- **Disposition**: `Keep`.
- **Canonical owner**: `docs/99.templates/registry.json`; Stage 01-05 documents retain topic truth and READMEs remain human indexes.
- **Verification**: existing-family proof plus registry self-test/strict, Markdown self-test/strict, lifecycle self-test/snapshot, template/source parity, and strict links.
- **Uncertainty**: structural alignment does not prove every document's topic semantics, reader usefulness, hosted result, or live procedure.
- **Blocker**: none at repository-static contract depth.

#### WGA-DOC-002 — Broader Release request is not mapped to the approved release-notes absence

- **Request IDs**: `REQ-WGA-016`, `REQ-WGA-019`, `REQ-WGA-023`.
- **Scope**: broader requested Release record versus the narrower release-notes type, including route, profile, template, lifecycle, relationship role, index, validator admission, and deliberate-absence ownership.
- **Expected state**: the broad request is mapped explicitly to an existing evidence family or distinguished from the approved DOC-G5 decision not to create release notes; queued implementation records the negative decision without reopening it.
- **Observed state**: the absence probe remains valid at zero profile/route, template, lifecycle, and relationship-role entries. Approved Spec 052 DOC-G5 already decides not to create a release-notes type, and its Plan gives WORK-013 the deliberate-absence text plus conditional future-instance route; WORK-013 is still queued. Neither owner explicitly maps the broader `Release` request to that narrower decision or another existing record.
- **Evidence**: `docs/03.specs/052-document-taxonomy-consolidation/spec.md#recorded-documentation-gap-disposition`; `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-14-wdtc-013--disposition-the-documentation-gaps`; `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md#task-table`; `docs/99.templates/registry.json#profiles`; `docs/99.templates/registry.json#documentContracts.lifecycleContracts`; `docs/99.templates/registry.json#documentContracts.roleDecisions`; `docs/99.templates/README.md#form-family-inventory`; `docs/99.templates/templates/README.md#item-index`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Gap`.
- **Impact**: release notes are correctly blocked from ad hoc creation, but the broader audit request cannot yet resolve deterministically to that negative decision or an existing release-evidence owner.
- **Disposition**: `Integrate`; WGIA-010 records no duplicate canonical delta and preserves approved DOC-G5/queued WORK-013 as the sole execution route.
- **Canonical owner**: approved Spec 052 DOC-G5 for the release-notes decision; its Plan and WORK-013 for deliberate-absence execution; existing Stage 99/Stage 05 owners remain unchanged.
- **Verification**: the probe returned `WGIA-DOC-RELEASE FAIL profile_route=0 template=0 lifecycle=0 role_validator=0`; WORK-013 must record the DOC-G5 absence, and review must confirm the broad `Release` mapping without adding a route.
- **Uncertainty**: which existing Task, workflow, policy, or reference artifact should satisfy the broader Release evidence request, if any; this does not unsettle DOC-G5.
- **Blocker**: WORK-013 is queued and the broad-versus-narrow semantic mapping is not recorded; WGIA-010 made no registry/template/Spec delta.

#### WGA-DOC-003 — Approved Guide Type enum is not yet enforced

- **Request IDs**: `REQ-WGA-018`, `REQ-WGA-019`.
- **Scope**: approved Guide Type classification for the eight current guides and the related no-tutorial/no-explanation route decisions.
- **Expected state**: DOC-G1's `how-to`, `tutorial`, `concept` enum is enforced in the `sdlc/guide` registry contract and template, all eight guides validate after migration, and DOC-G2/DOC-G3 deliberate absences are recorded without new routes.
- **Observed state**: Spec 052 is active and approved; DOC-G1 already decides the enum. The registry requires a `Guide Type` heading, the template names all three values, and all eight guides declare `how-to`, but the registry lacks deterministic enum enforcement. The WDTC Plan assigns that enforcement, all-eight-guide validation, and deliberate-absence text to WORK-013, which remains queued.
- **Evidence**: `docs/03.specs/052-document-taxonomy-consolidation/spec.md#recorded-documentation-gap-disposition`; `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-14-wdtc-013--disposition-the-documentation-gaps`; `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md#task-table`; `docs/99.templates/registry.json#profiles[id=sdlc/guide]`; `docs/99.templates/templates/operations/guide.template.md#guide-type`; `docs/05.operations/guides/README.md#item-index`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: guide authors have the intended values and current documents are consistent, but an invalid future Guide Type value is not deterministically rejected.
- **Disposition**: `Integrate` execution with existing WORK-013; WGIA-010 records no duplicate canonical delta and does not create a new taxonomy decision.
- **Canonical owner**: approved Spec 052 DOC-G1 through DOC-G3; the WDTC Plan and Task WORK-013 own implementation evidence; Stage 99 remains the registry/template owner.
- **Verification**: add an invalid Guide Type negative fixture, enforce the three-value enum, validate all eight current guides, and confirm no tutorial or explanation route was created.
- **Uncertainty**: implementation timing and exact validator fixture placement, not the approved enum or deliberate-absence decisions.
- **Blocker**: WORK-013 is queued and its deterministic enum/migration evidence is not yet recorded; WGIA-010 made no registry/template/guide delta.

#### WGA-DOC-004 — Integration guides conform statically; live usability is deferred

- **Request IDs**: `REQ-WGA-018`.
- **Scope**: eight numbered Stage 05 guides, their collection index, route, form, lifecycle, headings, status/date projection, and links.
- **Expected state**: guides conform to the repository-static contract, while command success, reader completion, and live safety require separately authorized evidence.
- **Observed state**: the collection indexes eight guides; the deterministic proof returned `guides=8`, and registry/profile/link checks cover their structural contracts. WGIA-003 performed no live guide execution or usability rehearsal.
- **Evidence**: `docs/05.operations/guides/README.md#item-index`; `docs/05.operations/guides/README.md#documentation-standards`; `docs/05.operations/guides/README.md#문서-인덱스`; `docs/99.templates/registry.json#profiles[id=sdlc/guide]`; `docs/99.templates/templates/operations/guide.template.md#topic-name-guide`; `scripts/validate-markdown-profiles.py#main`; `scripts/validate-links-and-owners.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: guides are admissible and discoverable, but static PASS must not be reported as successful operator execution or safe live behavior.
- **Disposition**: `Keep` the static contract and retain live usability as `DEFER`.
- **Canonical owner**: each Guide for its instructions, the guides README for human indexing, and Stage 99 for route/form/lifecycle.
- **Verification**: registry/profile/link/lifecycle checks for static conformance; an approved operator rehearsal with redacted result identity for any later live-usability claim.
- **Uncertainty**: reader comprehension, environment prerequisites, command outcomes, and current live-platform behavior.
- **Blocker**: live/operator authorization and an approved rehearsal environment are absent.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-DOC-001 | machine owner | `docs/99.templates/registry.json#profiles`; `docs/99.templates/registry.json#documentContracts.lifecycleContracts`; `docs/99.templates/registry.json#documentContracts.roleDecisions`; `docs/99.templates/support/document-profiles.schema.json#properties.profiles` | Exact route, form, lifecycle, and relationship contract. |
| SRC-WGA-DOC-002 | policy owner | `docs/03.specs/052-document-taxonomy-consolidation/spec.md#recorded-documentation-gap-disposition`; `docs/99.templates/README.md#exact-one-profile-procedure`; `docs/99.templates/support/sdlc-governance.md#sdlc-profile-handoff`; `docs/00.agent-governance/rules/stage-authoring-matrix.md#current-contract` | Approved documentation-gap decisions plus selection, stage, and lifecycle procedure. |
| SRC-WGA-DOC-003 | human index | `docs/README.md#document-index`; `docs/03.specs/README.md#current-spec-index`; `docs/05.operations/guides/README.md#item-index`; `docs/99.templates/templates/README.md#item-index` | Reader routing and inventory entrypoints. |
| SRC-WGA-DOC-004 | evidence producer | `scripts/validate-document-contract-registry.py#main`; `scripts/validate-markdown-profiles.py#main`; `scripts/validate-document-lifecycle.py#main`; `scripts/validate-links-and-owners.py#main`; `tests/fixtures/document-contracts/template-source-parity.json#cases` | Deterministic local conformance and negative template/source-parity fixtures. |
| SRC-WGA-DOC-005 | historical snapshot | `docs/90.references/research/2026-08-08-wer/documentation-architecture-and-diataxis.md#diátaxis-baseline`; `docs/90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix` | Dated descriptive comparison only; not an active schema owner. |
| SRC-WGA-DOC-006 | human index | `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-14-wdtc-013--disposition-the-documentation-gaps`; `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md#task-table` | Existing DOC-G1 through DOC-G5 implementation route and queued WORK-013 state. |

## Review and Freshness

- Review status: fresh WGIA-010 specification/content and quality reviews of
  the integration/no-delta evidence are `Approved`. The original WGIA-003
  reviews remain Approved.
- Review disposition: `Approved`; WGIA-010 records no duplicate canonical
  change for WGA-DOC-002/003, and queued WORK-013 remains their sole execution
  owner.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: Stage 99 machine contracts and the owning Stage 01-05 documents.
- Refresh triggers: route, profile, schema, template, lifecycle, README, guide,
  observation commit, finding, or canonical-owner change.
- Next owner: the existing WDTC program and queued WORK-013 own implementation;
  WGIA-010 made no registry, template, guide, or Spec change.
- Deeper evidence: guide usability plus hosted, provider-runtime, remote,
  credential-bearing, and live lanes remain `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/0055-workspace-governance-audit-and-remediation/spec.md)
- [Document Profile Registry](../../../99.templates/registry.json)
- [Template Routing Contract](../../../99.templates/README.md)
- [Implementation Task](../../../03.specs/0055-workspace-governance-audit-and-remediation/README.md)
