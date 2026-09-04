---
title: "Common Document Contract v9 and Governed Router Envelopes"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-09-04"
layer: "architecture"
artifact_id: "ADR-0033"
---

# ADR-0033: Common Document Contract v9 and Governed Router Envelopes

## Overview

Adopt one public Stage 99 document-contract model with snake_case fields,
governed identity-free README envelopes, profile-bound templates, and
generation-aware Archive validation. This decision is a scoped amendment to
the README and Registry-shape clauses of ADR-0015 and ADR-0031; their
single-authority, current-corpus, and package-local execution principles remain
in force.

## Context

The repository already treats Stage 00 as semantic policy authority and the
Stage 99 Registry as the sole machine owner of document classification.
However, the published Registry used repository-specific camelCase fields,
README profiles were frontmatter-free while authored leaves had a common
envelope, and several validators projected the public object through a second
private shape. Template examples also used more than one placeholder grammar.

Those differences made the same facts appear in Registry prose, templates,
validators, and README conventions. They also prevented the repository from
sharing one clear contract vocabulary without weakening its Git-backed
Archive proof and immutable payload rules.

The current Requirement Package already integrates PRD, SRS, and interface
requirement perspectives. ADR-0030 also deliberately excludes a local Release
Record because Task, Git, tag, CI, and external provider evidence are the
current release owners. Neither decision needs to be reversed to normalize the
document contract.

## Decision

### Authority and public model

Stage 00 owns meaning, approval, SDLC, lifecycle obligations, and authoring
procedure. Stage 99 Registry version 9 owns exact paths, profile IDs,
frontmatter policy, sections, lifecycle binding, relationships, and template
binding. JSON Schema validates Registry structure and frontmatter value
grammar; templates project the Registry contract and do not define it.

The public Registry has only "$schema", "$id", "schema_version", "profiles",
and "lifecycle_domains". Public profile families are "common", "governance",
"sdlc", "operation", "reference", and "archive"; public modes are "authored",
"router", "template", "evidence", "native", and "non-target". Fields use
snake_case. Authored classification uses only "type", whose value is the
profile's lowercase kebab-case "family/kind" ID.

Current readers accept only version 9. A lifecycle or Archive comparison may
interpret a version 7 or 8 Git snapshot only inside a commit-bounded historical
proof path; that does not authorize legacy fields in a current proposal.

### Governed Markdown envelope

Governed Markdown, including governed README routers, starts with the ordered
common prefix "title", "version", "type", "status", "owner", and "updated".
All string, date, version, and identity scalars use double quotes.

A numbered stage document declares its Registry-fixed "layer". A profile with
stable identity declares "artifact_id". Router READMEs declare neither
"artifact_id" nor lifecycle binding; their "status: active" is a routing
constant, not an artifact lifecycle state. Governance documents without stable
identity likewise omit "artifact_id".

Document version starts at "0.1.0". First stable approval raises it to
"1.0.0"; patch, minor, and major changes describe correction, compatible
meaning growth, and incompatible role or meaning changes respectively. Status
and version remain independent.

### Schema and template grammar

Retain "contracts/frontmatter.schema.json" as the sole authored frontmatter
scalar and array grammar in this repository. Its responsibility is documented
rather than duplicated in the Registry schema. The Registry owns per-profile
required, optional, forbidden, ordered, constant, and enumerated facts.

Markdown value placeholders use "&#123;&#123;UPPER_SNAKE_CASE&#125;&#125;"; author guidance uses
"<!-- Author prompt: ... -->"; native templates use
"__UPPER_SNAKE_CASE__". A template's "version: 0.1.0" is the initial version
of the document it creates, not a template revision. Registry contract version
and Git history own template evolution.

"docs/99.templates/templates/README.md" is the only human template catalog.
The Registry's "template_source" and relationship fields own the machine
binding. A required form has one source; an orphan, duplicate, missing, or
unregistered form is invalid.

### Lifecycle, Release, and Archive boundaries

Lifecycle domains remain profile-specific. Requirement Packages continue to
integrate PRD/SRS/interface requirement viewpoints, and Spec, Plan, and Task
retain separate behavior, ordering, and execution-evidence ownership.

No "operation/release" profile or local Release Record is added. The repository
continues to use the external-release-evidence mode established by ADR-0030:
Tasks and Git record repository work, while tags, hosted CI, and provider or
live evidence remain external and must not be inferred from local validation.

Stage 98's root router owns current Archive governance. Frozen legacy payloads
are not rewritten to the v9 envelope. Current archive records use their
registered evidence profiles, while historical readers are generation-aware
and bounded by source commit, blob, digest, and exact migration evidence.

### Reference-framework application

GitHub Spec Kit is applied to the Stage 03 clarify, Spec, Plan, Task,
implement, and verify flow without replacing individual Task records.
Diátaxis shapes reader intent in Operations documents without replacing stage
taxonomy. C4 and arc42 guide proportional Architecture Description views.
ADR practice preserves one decision and successor history. Google SRE
principles shape factual incidents and blameless, tracked postmortems. No
external template is copied wholesale.

## Explicit Non-goals

- This decision does not change Kubernetes, GitOps, Helm, Vault, ESO, cloud,
  provider, secret, certificate, or live-cluster state.
- It does not add a Release Record, CHANGELOG owner, deployment procedure, or
  hosted evidence claim.
- It does not rewrite frozen Archive payloads or historical links.
- It does not move provider role or permission authority from
  ".agents/registry.json" into the document Registry.
- It does not turn README prose or templates into a second machine authority.

## Consequences

Authors see one envelope and one placeholder grammar across governed Markdown.
README routers become machine-classified without receiving fake identities.
Validators can report path, metadata, value, lifecycle, relationship, and
template failures from one public model.

The v9 migration touches many active documents because representation is part
of the contract. This is controlled churn: Archive payload bytes remain
unchanged, and semantic document content is not reformatted.

Historical comparison code must retain an explicit v7/v8 branch until all
bounded migration proofs no longer need those snapshots. That branch is more
complex than a current-only reader, but it is isolated from authoring and
current proposal validation.

Keeping external release evidence avoids a redundant document family, but it
also means a future audit need for a repository-local release record requires a
new decision, profile, lifecycle, template, and consumer analysis.

## Alternatives

__Keep README frontmatter-free.__ Rejected because governed routers would remain
the only Markdown class outside the common metadata contract, forcing separate
classification and validation conventions.

__Publish v9 but retain a permanent dual reader.__ Rejected because accepting
both field vocabularies in current proposals would make migration drift
invisible and preserve a second contract indefinitely.

__Rename "frontmatter.schema.json" immediately.__ Rejected for this slice.
The current name has one documented responsibility and no competing same-name
schema in this repository; a rename would add path churn without changing
semantics.

__Add "operation/release" while normalizing Operations forms.__ Rejected because
the repository has no demonstrated consumer that outweighs the existing
external evidence owners, and ADR-0030 already made the opposite decision.

__Rewrite frozen Archive payloads to v9.__ Rejected because it would destroy
the byte-level historical evidence the Archive contract exists to preserve.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0015](./0015-declarative-document-contract-registry.md), [ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md), and [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Scoped amendment of README envelope and public Registry-shape clauses; no full supersession | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |

### Implementation Traceability

| Decision element | Implementation owner | Verification |
| --- | --- | --- |
| Public v9 model and lifecycle binding | "docs/99.templates/registry.json" and "contracts/document-profile.schema.json" | strict Registry and authority validation |
| Frontmatter value grammar and canonical quoting | "contracts/frontmatter.schema.json" and Markdown validator | positive corpus plus "FM-QUOTE" negative test |
| Template binding and placeholder grammar | Registry and "templates/" | parity, orphan, duplicate, and residue tests |
| Router envelopes and active-document migration | Registry-selected current Markdown corpus | strict Markdown and link/owner validation |
| Frozen historical generation | Stage 98 and Archive validators | zero Archive payload diff and bounded recovery tests |
| Execution evidence | [Task SPEC-0054-TSK-0013](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md) | gap matrix, commands, results, and limitations |
