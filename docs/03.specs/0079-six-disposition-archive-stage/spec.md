---
title: "Six-Disposition Archive Stage Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0079"
---

# Six-Disposition Archive Stage Technical Specification (Spec)

## Overview

[ADR-0038](../../02.architecture/decisions/0038-six-disposition-archive-stage.md)
proposes a Stage 98 of six dispositions in two kinds: the retention classes
`completed/`, `superseded/`, `retired/`, and `resolved/` hold a whole
once-current body, and the route dispositions `tombstones/` and `migrations/`
hold no body. Citability is derived from what each family names, one catalog
Retention Envelope names the source Git object, and frozen content keeps its
generation.

This Spec owns applying that model. It proceeds in two steps that cannot share a
change. The first states the contract in common governance, the documentation
hub, and the stage indexes, with the transition boundary explicit. The second
moves the registry routes, archive forms, validators, and tests together, after
ADR-0038 is accepted.

## Strategic Boundaries & Non-goals

Authorized scope for the governance step is `.agents/governance/`
(`document-lifecycle.md`, `document-authoring.md`, `sdlc.md`), `docs/README.md`,
the prose of `docs/98.archive/README.md` outside its manifest comment and record
table, the Stage 01, 02, and 03 indexes, the decision index, ADR-0032's
Traceability, AD-0006, REQ-0003-FR-0020, the new ADR-0038, and this package.

Authorized scope for the machine step is `docs/99.templates/registry.json`,
`docs/99.templates/templates/archive/`, `docs/99.templates/README.md`,
`.markdownlint-cli2.yaml`, and the archive, lifecycle, link, and profile
validators under `scripts/` with their tests.

Explicit non-goals. No frozen Stage 98 record, migration ledger, retained
package, manifest comment, or record table row changes. No lifecycle state or
edge is added. No existing superseded decision moves out of Stage 02 and no
existing citation is rewritten in this Spec. No live cluster, provider runtime,
or network action is authorized.

## Contracts

- A governed document that is no longer current leaves Stages 01, 02, 03, 05,
  90, and 99 for the one disposition that matches what happened to it. Superseded
  architecture decisions are not exempt.
- A retention class keeps the body under its original profile, identity, and
  terminal state at `docs/98.archive/<class>/<its own stage path>`, and the body
  names what its class requires.
- A route disposition holds no body and names only its route and current owner.
- An active-stage document may cite `completed/` and, as historical evidence,
  `resolved/`; it cites the successor or the current route for every other
  family.
- No Stage 98 record carries a redirect, path ledger, self-designed body digest,
  branch SHA, or recovery commit. The catalog's Retention Envelope names one
  `<commit>:<original path>`.
- Frozen content is classified by generation and never rewritten.
- Until the machine step lands, the validators admit only ADR-0032's routes, and
  governance prose says so wherever it states the new contract.

## Core Design

The governance step changes owners, not machines. The lifecycle policy owns the
disposition obligations, the authoring policy owns the link rule, the Stage 98
index owns the catalog and its generation boundary, and each stage index points
at them instead of restating ADR-0032's four directories.

The machine step makes the registry the only place a route is spelled and
removes the three hardcoded retention-class lists. Frozen records and retained
bodies may share a directory, so classification cannot rest on a path pattern
alone. The registry distinguishes the frozen record generation from original
profiles, and the validators select the generation before any other rule runs.

## Data Modeling & Storage Strategy

A retained body carries its original frontmatter unchanged. The catalog row for
a disposition carries the record path, the original path, and one Retention
Envelope `<commit>:<original path>`. A route disposition carries the route, its
successor or absence, the reason, and for a migration the moved scope, current
owner, and `MIG-####`. Frozen records keep their ArchiveEnvelope, `source_blob`,
and `content_sha256`, and frozen ledgers keep their pinned rows.

## Interfaces & Data Structures

The governance step changes no interface. The machine step changes the registry
profiles for the archive family and the retention path alternatives of the
origin profiles, the catalog row parser, and the retention-class and link
boundary logic. Rule identifiers that name a removed obligation are retired, and
a new rule identifier is added only for a new obligation.

## Edge Cases & Error Handling

A document that could match two classes is decided by what happened to it: a
replacement makes it `superseded`, and withdrawal with no successor makes it
`retired`. A closed Incident whose Postmortem is not yet published is not
`resolved`. A citation that predates ADR-0038 acceptance is recorded as a
consumer and left in place. A frozen record that would need a metadata repair
stays unchanged, and the repair needs its own decision.

## Failure Modes & Fallback / Human Escalation

If ADR-0038 is rejected, the governance step is reverted by its commit and
ADR-0032 remains the only contract. If the machine step cannot keep frozen
records passing without rewriting them, it stops and returns to the request
owner rather than weakening a gate. Each step reverts alone.

## Verification Commands

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
python3 scripts/qa.py full
```

`full` owns unit discovery and the pre-commit manual stage. No command here
proves provider runtime or live cluster behavior.

## Success Criteria & Verification Plan

| ID          | Criterion                                                                                                                                                                                                                             | Evidence                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| VAL-SDA-001 | ADR-0038 records the two kinds, the six dispositions, derived citability, the single Retention Envelope, the withdrawn decision-log exception, and the frozen generation boundary in its initial state                                | Decision review and the lifecycle gate      |
| VAL-SDA-002 | Common governance and the documentation hub state the six-disposition contract, the derived citation rule, the absence of a second recovery ledger, and the transition boundary without contradicting the routes the validators admit | Policy review and the strict document gates |
| VAL-SDA-003 | The Stage 98 index states both kinds, the catalog Retention Envelope, and the frozen generation, with its manifest comment and record table unchanged                                                                                 | Archive gate and diff review                |
| VAL-SDA-004 | The Stage 01, 02, and 03 indexes, the decision index, AD-0006, and REQ-0003-FR-0020 no longer restate ADR-0032's four directories or the decision-log exception, and ADR-0032 names its proposed successor                            | Index review and the strict document gates  |
| VAL-SDA-005 | Registry routes and profiles, archive forms, validators, and tests implement the model in one change, with frozen records passing unmodified                                                                                          | Staged and full QA on the cutover commit    |
| VAL-SDA-006 | Pending dispositions and pre-acceptance consumers are enumerated with their owner and are not executed                                                                                                                                | Task handoff record                         |

## Traceability

[Implementation Plan](plan.md) owns order and risk. The
[governance Task](tasks/tsk-0001-state-the-six-disposition-contract.md) owns
the first step and the
[machine cutover Task](tasks/tsk-0002-move-registry-and-validators.md) owns the
second.

### Lifecycle Traceability

| Requirement ID                                                                        | Spec criterion | Verification method                                   |
| ------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDA-001    | Decision review against the disposition requirement   |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDA-002    | Owner-by-owner policy review                          |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDA-003    | Archive gate over the unchanged frozen generation     |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDA-004    | Index and description review                          |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDA-005    | Registry, form, and validator agreement under full QA |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDA-006    | Enumerated consumer and disposition record            |
