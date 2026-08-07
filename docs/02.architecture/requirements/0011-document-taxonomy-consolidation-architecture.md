---
title: 'Document Taxonomy Consolidation Architecture Reference Document'
type: sdlc/ard
status: active
owner: platform
updated: 2026-08-07
---

# Document Taxonomy Consolidation Architecture Reference Document (ARD)

## Overview

This document defines the target architecture for the repository's authored
document taxonomy, its identifier and lineage model, its rule-ownership
topology, and the validator surface that enforces them. It serves the
governance steward, platform maintainer, quality engineer, technical writer,
and AI agent personas defined in
[PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md).

The architecture keeps the existing numbered stage taxonomy and the existing
per-stage identifier sequences. It changes the unit of physical organization
from artifact type to work unit, moves cross-stage lineage from filename
convention into machine-readable metadata, and collapses rule ownership so that
each enforced rule has exactly one stating document and one enforcing
validator.

## Boundaries & Non-goals

The architecture governs authored Markdown under `docs/`, the machine contracts
that classify and validate it, and the scripts that execute those validations.
It does not govern platform desired state, provider adapters, agent role
semantics, or any live, hosted, remote, or credential-bearing surface.

Three boundaries are load-bearing and must not be crossed.

**Archive inviolability.** Archive records use the `ArchiveEnvelope.v1` form:
frontmatter metadata followed by the exact original Git blob bytes, sealed by
`content_sha256`. `scripts/archive_validation.py` resolves links inside the
payload against the record's `source_commit` in the Git tree rather than the
working tree, so historical paths stay valid permanently. No migration may
read, rewrite, reformat, or renumber anything under the archive stage. The
archive is therefore excluded from every path rewrite in this architecture, and
its 60 references to retired live paths are correct as written.

**Dated observation integrity.** Reference and audit packs record point-in-time
observations. Rewriting a path inside a dated observation falsifies the record.
Path rewrites in these packs are limited to navigational cross-links, and any
observation text that names a retired path keeps that path with an explicit
historical annotation.

**Stage identifier stability.** No PRD, ARD, ADR, or specification number is
reassigned. Decision-record practice treats a record number as identity that is
never reused; renumbering would invalidate every existing cross-reference of
the form `Spec 047` or `ADR-0021`.

Explicit non-goals: removing the numbered stage-prefix scheme; introducing
tutorial or explanation document routes; creating a release-notes stage;
changing the agent role roster; and adding a fourth machine contract family.

## Quality Attributes

| Attribute               | Measure                                                                                                                                                      | Linked requirement                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------- |
| Rule uniqueness         | Each enforced authoring rule is stated in exactly one live document; a text search for a retired rule returns zero live hits.                                | REQ-WDTC-005, REQ-WDTC-006        |
| Address stability       | Zero existing stage identifiers change; every retired path has a deterministic successor path.                                                               | REQ-WDTC-004, REQ-WDTC-016        |
| Lineage resolvability   | Every specification declares its upstream requirement and architecture owners in frontmatter, and a validator proves the reciprocal link exists.             | REQ-WDTC-004                      |
| Corpus proportionality  | Governance corpus size is recorded before and after each reduction, with a stated line delta per asset.                                                      | REQ-WDTC-007 through REQ-WDTC-011 |
| Enforcement closure     | The declared validator set and the executable validator set are equal; no rule is enforced by two validators and no declared lane names a missing validator. | REQ-WDTC-013                      |
| Migration reversibility | Each logical commit passes the full repository quality gate and can be reverted independently of its successors.                                             | RISK-WDTC-004, DEP-WDTC-001       |
| Evidence honesty        | Repository-static results are never reported as hosted, provider-runtime, remote, or live evidence.                                                          | REQ-WDTC-012                      |

## System Overview & Context

### Target stage taxonomy

```
docs/
  00.agent-governance/   governance rules, contracts, hooks, memory, providers, scopes
  01.requirements/       PRD          ###-<slug>.md
  02.architecture/
    requirements/        ARD          ####-<slug>.md
    decisions/           ADR          ####-<slug>.md
  03.specs/              work unit    ###-<slug>/{spec,plan,tasks}.md
  04.operations/         guides, incidents, policies, runbooks
  90.references/         durable reference, research, audit, data
  98.archive/            immutable ArchiveEnvelope.v1 records
  99.templates/          template forms and support contracts
```

The former execution stage is retired. Its numeric slot is reclaimed by the
operations stage so that the active sequence stays contiguous.

### Work unit as the organizing axis

A work unit is the atomic subject of Stage 03. Its folder carries a stable
three-digit identifier and a slug, and holds up to three fixed-name documents:
`spec.md` states what and why, `plan.md` states how the work is sequenced, and
`tasks.md` records execution evidence. A work unit may have a specification
without a plan; it may not have a plan without a specification.

This mirrors the convergent practice observed across five spec-driven
development toolchains on 2026-08-07, all of which co-locate a work unit's
specification, design, and task list and none of which partitions them by
artifact type. Fixed filenames inside a variably named folder is likewise the
observed convention: identity is carried by the folder, not the file.

### Lineage model

Cross-stage lineage moves from prose links into frontmatter fields that a
validator can resolve:

```yaml
lineage: PRD-008 # owning product requirement
ard: ARD-0011 # owning architecture reference
adr: [ADR-0022] # decisions this work unit depends on
predecessor: Spec-051 # optional ordered-program antecedent
```

Prose relationship sections remain for human readers, but the frontmatter
fields are the machine owner. A specification whose declared upstream owner
does not link back to it fails validation. This keeps per-stage sequences
independent, which decision-record practice requires, while making the
three-counter lineage resolvable without reading prose.

### Rule ownership topology

Ten documents currently state authoring rules. The target is three, each with a
disjoint subject:

| Owning document                                   | Subject                                                                                               |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `00.agent-governance/rules/document-authoring.md` | Which stage owns a document, when it is authored, which persona authors it, and what completes it.    |
| `99.templates/support/document-contract.md`       | Which template form a target selects, what frontmatter it carries, and what headings it must contain. |
| `99.templates/support/document-lifecycle.md`      | Status transitions, promotion evidence, supersession, retirement, and archive routing.                |

No document may restate a rule owned by another. An authority-boundary section
is permitted only to name the owner of an adjacent subject, not to restate its
content.

### Validator topology

The canonical selection contract declares 22 validators; 48 executables exist
in `scripts/`. The target makes these sets equal by three moves: delete
validators whose contract is retired, merge validators that enforce one rule
family, and declare validators that are executed but undeclared. Every
remaining validator maps to exactly one rule family and one evidence lane.

## Data Architecture

### Machine contract ownership

| Contract family                     | Current                                                                 | Target ownership rule                                                                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Document classification and routing | `99.templates/support/document-profiles.json`, 6,413 lines, 64 profiles | One profile per authored document type. Template forms validate against their corresponding authored profile rather than a mirrored `template/*` profile. |
| Agent governance                    | 21 files under `00.agent-governance/contracts/`, 18,199 lines           | Fewer owners, each covering one rule family, with schemas colocated. No rule loses its enforcing assertion.                                               |
| Validator selection                 | `00.agent-governance/contracts/validation-surfaces.json`                | Sole owner of lane, argv, evidence lane, and fallback for every validator. Equality with the script surface is itself validated.                          |
| Reference information architecture  | `90.references/data/reference-information-architecture.json`            | Retained.                                                                                                                                                 |
| Migration census                    | `90.references/data/active-corpus-*.json`, 14,142 lines                 | Deleted with its exclusive validators. The migration it recorded is complete; its outcome is the current tree.                                            |

### Progress ledger retention

The shared progress ledger is append-only and read by every agent session. Its
architecture changes from one unbounded file to a bounded live window plus
archived periods. The live ledger holds the current period; closed periods
become archive records under the archive stage and remain recoverable through
the archive index. The ledger stays the single durable owner of shared
progress; only its retention window changes.

### Path rewrite domain

| Domain                                               | Files referencing retired paths | Treatment                                                                      |
| ---------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------ |
| Live authored documents, stages 00 through 04 and 99 | ~130                            | Rewritten to successor paths.                                                  |
| Reference and audit packs, stage 90                  | ~98                             | Navigational links rewritten; dated observation text annotated, not rewritten. |
| Archive records, stage 98                            | 60                              | Excluded entirely.                                                             |
| Scripts, tests, fixtures, and agent adapters         | ~20 plus validator internals    | Rewritten with the contract they encode.                                       |
| Generated output                                     | 3                               | Regenerated, not edited.                                                       |

## Infrastructure & Deployment

This architecture deploys through Git commits to the local repository only. It
introduces no runtime component, no cluster object, and no hosted or remote
action.

The migration executes as ordered logical commits, each of which must pass
`bash scripts/validate-repo-quality-gates.sh .` before it lands. The observed
baseline for that gate on 2026-08-07 is PASS in 1 minute 59 seconds, which is
short enough to gate every commit rather than only the final one.

Failure boundaries follow the risk ordering in PRD-008. Low-risk deletions of
retired one-shot artifacts run first, reducing the file population that later
high-risk steps must traverse. The agent governance contract consolidation runs
last among the reduction steps and occupies its own commit, so that a
fail-closed gate reverts only that step.

The suspended delivery assurance program is a deployment dependency: its active
tranche returns to draft before this program's first structural commit, and no
suspended tranche executes until this program completes.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-WDTC-001](../../01.requirements/008-workspace-document-taxonomy-consolidation.md#functional-requirements) | Work unit is the organizing axis; fixed filenames inside a variably named folder | [ADR-0021](../decisions/0021-canonical-surface-routing-and-evidence-depth.md) and [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md) |
| N/A — REQ-WDTC-002 through REQ-WDTC-004 share the PRD-008 source linked in REQ-WDTC-001. | Address stability, contiguous stage sequence, and reciprocal lineage resolvability | N/A — Spec 052 shares the owner linked in REQ-WDTC-001. |
| N/A — REQ-WDTC-005 and REQ-WDTC-006 share the PRD-008 source linked in REQ-WDTC-001. | Rule uniqueness across three disjoint owning documents | N/A — Spec 052 shares the owner linked in REQ-WDTC-001. |
| N/A — REQ-WDTC-007 through REQ-WDTC-011 share the PRD-008 source linked in REQ-WDTC-001. | Corpus proportionality with dated observation integrity preserved | N/A — Spec 052 shares the owner linked in REQ-WDTC-001. |
| N/A — REQ-WDTC-012 and REQ-WDTC-013 share the PRD-008 source linked in REQ-WDTC-001. | Evidence honesty and enforcement closure between declared and executable validators | N/A — Spec 052 shares the owner linked in REQ-WDTC-001. |
| N/A — REQ-WDTC-014 through REQ-WDTC-016 share the PRD-008 source linked in REQ-WDTC-001. | Archive inviolability, migration reversibility, and retained stage-prefix taxonomy | N/A — this ARD owns the boundaries stated in Boundaries & Non-goals. |
