---
title: 'Document Taxonomy Consolidation Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-08-07
---

# Document Taxonomy Consolidation Technical Specification (Spec)

## Overview

This specification implements the consolidated document taxonomy, lineage
model, rule-ownership topology, and validator surface defined by
[ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md).
It retires the execution stage as a separate top-level tree, co-locates each
work unit's specification, plan, and task evidence, renumbers the operations
stage to keep the sequence contiguous, removes dates from authored filenames,
moves cross-stage lineage into machine-readable frontmatter, collapses ten
authoring-rule documents into three, and reduces the machine contract, census,
and validator corpus.

The design is grounded in two dated external research results and one measured
repository baseline, all from 2026-08-07. The research is recorded in Stage 90
and is descriptive; this specification is the first document that turns it into
an enforced contract.

Consumers are the governance steward, platform maintainer, quality engineer,
technical writer, and AI agent personas. The verification outcome is a
repository whose declared rules, stating documents, and enforcing validators
are in one-to-one correspondence, and whose governance corpus is measurably
smaller with a recorded per-asset delta.

## Strategic Boundaries & Non-goals

Authorized scope is authored Markdown under `docs/`, the machine contracts that
classify and validate it, the shared progress ledger, the reference data and
research packs, and the scripts and tests that enforce those contracts.

Three protected surfaces bound the work.

**The archive stage is inviolable.** Archive records carry the exact original
Git blob bytes after the `archive-envelope:v1` marker, sealed by
`content_sha256`, and `scripts/archive_validation.py` resolves their payload
links against `source_commit` in the Git tree. The 60 archive files that
reference retired live paths are correct as written and are excluded from every
rewrite. Any change inside an archive payload is a specification violation, not
a migration detail.

**Dated observations are not rewritten.** Reference and audit packs under Stage
90 record point-in-time facts. Only navigational cross-links are rewritten.
Observation text naming a retired path retains that path with an explicit
historical annotation.

**Stage identifiers are stable.** No PRD, ARD, ADR, or specification number is
reassigned. The only path-identity changes authorized are the retirement of the
execution stage and the renumbering of the operations stage.

Explicit non-goals: removing the numbered stage-prefix scheme; adding tutorial
or explanation document routes; creating a release-notes stage; changing agent
role semantics, provider adapters, or the platform's desired state; and any
live, hosted, remote, or credential-bearing action.

## Contracts

### C-1 Work unit locality

A Stage 03 work unit is one directory `docs/03.specs/<NNN>-<slug>/` holding at
most three fixed-name documents: `spec.md`, `plan.md`, `tasks.md`. A work unit
may exist with `spec.md` alone. A `plan.md` without a sibling `spec.md`, or a
`tasks.md` without a sibling `plan.md`, is invalid.

### C-2 Filename date prohibition

No authored document filename under stages 01 through 04 begins with a date.
The authoring and modification dates are carried by frontmatter `updated` only.
Archive records and Stage 90 dated pack directories are exempt, because their
date is part of the record identity rather than a mutable attribute.

### C-3 Stage sequence

The active stage sequence is `00`, `01`, `02`, `03`, `04`, followed by the
reserved tail `90`, `98`, `99`. Stage `04` denotes operations. The execution
stage does not exist as a live path.

### C-4 Lineage declaration

Every Stage 03 `spec.md` declares `lineage` naming its owning PRD and `ard`
naming its owning ARD. Optional `adr` and `predecessor` fields name decision
dependencies and ordered-program antecedents. A declared upstream owner that
does not link back to the declaring specification is a validation failure.

### C-5 Rule uniqueness

Each authoring rule is stated by exactly one live document. A document may name
the owner of an adjacent subject; it may not restate that owner's rule text. A
literal search for a retired rule sentence returns zero live hits.

### C-6 Enforcement closure

The validator set declared in
`docs/00.agent-governance/contracts/validation-surfaces.json` and the executable
validator set under `scripts/` are equal. Every declared validator maps to one
rule family and one evidence lane. No enforced rule has two enforcing
validators.

### C-7 Evidence lane honesty

Repository-static results are never reported as hosted CI, provider-runtime,
remote, or live evidence. Every result this specification produces is
repository-static unless separately labelled.

## Core Design

### Migration groups

The 47 specifications, 63 plans, and 65 tasks observed on 2026-08-07 partition
into four disjoint groups by slug correspondence.

| Group           | Count | Source                                                             | Target                                                             |
| --------------- | ----- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| G-A triad       | 39    | `03.specs/<NNN>-<slug>/spec.md` plus same-slug dated plan and task | `03.specs/<NNN>-<slug>/{spec,plan,tasks}.md`                       |
| G-B spec only   | 8     | `03.specs/<NNN>-<slug>/spec.md` with no live same-slug plan        | Unchanged path; archived plan referenced through the archive index |
| G-C orphan plan | 24    | `04.execution/plans/<date>-<slug>.md` with no specification        | `98.archive/04.execution/plans/<date>-<slug>.md`                   |
| G-D orphan task | 3     | `04.execution/tasks/<date>-<slug>.md` with no live plan            | `98.archive/04.execution/tasks/<date>-<slug>.md`                   |

Every G-C and G-D member was verified on 2026-08-07 to carry `status: done`,
which makes them complete historical records rather than interrupted work. They
are archived through the existing `ArchiveEnvelope.v1` route, which preserves
their exact bytes and resolves their links against their source commit. Their
archive mirror path is derived from their original path, so it retains the
retired execution-stage segment; that is the historically correct mirror and is
not a contract violation.

Every authored plan and task outside the suspended program carries
`status: done`. The ten exceptions are exactly the suspended program's set: the
Spec 047 plan and task are `active`, and the Spec 048 through 051 plans and
tasks are `draft`. The two remaining non-conforming files are the plan and task
stage README indexes, which carry a README profile rather than an execution
status and are retired with their stage rather than migrated. No document
therefore requires individual status disposition before migration.

### Stage renumbering

`docs/05.operations/` becomes `docs/04.operations/`. The move is a rename of
one directory plus a rewrite of every tracked reference to the old segment
outside the archive and dated-observation domains.

### Path rewrite execution

The rewrite is scripted, never manual. Its input is the tracked file set; its
exclusion set is `docs/98.archive/**`, generated output, and the observation
bodies of Stage 90 dated packs. Measured reference counts on 2026-08-07:

| Retired segment | Tracked files | Occurrences | Excluded (archive) |
| --------------- | ------------- | ----------- | ------------------ |
| `04.execution`  | 321           | 8,995       | 40 files           |
| `05.operations` | 203           | 6,937       | 20 files           |

The rewrite runs as one operation per segment, followed immediately by the full
quality gate. A partial rewrite that leaves both segments live is not a valid
intermediate state and is not committed.

### Rule consolidation

| Target document                                   | Absorbs                                                                                                           | Current lines |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------- |
| `00.agent-governance/rules/document-authoring.md` | `stage-authoring-matrix.md`, `document-stage-routing.md`, `stage-checklists.md`, `documentation-protocol.md`      | 637           |
| `99.templates/support/document-contract.md`       | `documentation-contract.md`, `template-routing.md`, `frontmatter-schema.md`, `common-documentation-governance.md` | 546           |
| `99.templates/support/document-lifecycle.md`      | `sdlc-governance.md`, `legacy-cleanup-rules.md`                                                                   | 237           |

The sentence "Stage 04 plans and tasks stay date-based execution records"
appears verbatim in `stage-authoring-matrix.md`, `document-stage-routing.md`,
and `sdlc-governance.md`. It contradicts C-1 and C-2 and is deleted from all
three during consolidation. Because those three files collapse into two
surviving owners, the duplication cannot recur.

### Corpus reduction

| ID  | Asset                                               | Before                        | Action                                                                                             |
| --- | --------------------------------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------- |
| R-1 | `90.references/data/active-corpus-*.json` (3 files) | 14,142 lines                  | Delete with their five exclusive validators                                                        |
| R-2 | `scripts/archive_cutover_manifest.py`               | 108 lines                     | Delete; zero referents observed                                                                    |
| R-3 | `90.references/research/2026-07-04-wer/`            | 6 files                       | Archive; facts already merged into the 2026-07-07 pack                                             |
| R-4 | `00.agent-governance/memory/progress.md`            | 13,920 lines                  | Rotate to a bounded live window; closed periods to archive                                         |
| R-5 | `99.templates/support/document-profiles.json`       | 6,413 lines, 64 profiles      | Remove the 24 `template/*` mirror profiles; validate template forms against their authored profile |
| R-6 | `00.agent-governance/contracts/*.json` (21 files)   | 18,199 lines                  | Consolidate into fewer rule-family owners with colocated schemas                                   |
| R-7 | `scripts/`                                          | 48 executables vs 22 declared | Reconcile to enforcement closure under C-6                                                         |

R-1 through R-4 are deletions and relocations whose contracts are already
complete; they run first and shrink the file population that later steps
traverse. R-5 and R-6 change enforced contracts and run last, R-6 in its own
revertible commit.

### Recorded documentation gap disposition

| Gap     | Disposition                                                                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DOC-G1  | Constrain `Guide Type` to the enumeration `how-to`, `tutorial`, `concept` in the profile registry and template.                                               |
| DOC-G2  | No tutorial route is created. Diátaxis states that empty structures must not be created in advance; the decision and its source are recorded.                 |
| DOC-G3  | No explanation route is created, on the same recorded basis. Explanation remains inside ADR context and reference sub-types.                                  |
| DOC-G4  | The guide-versus-runbook boundary becomes a decidable test in `document-lifecycle.md`, and the active-surface duplicate rule extends to the operations stage. |
| DOC-G5  | No release-notes type is created. Zero references exist and the repository declares no public API; the decision is recorded.                                  |
| DOC-G6  | Postmortem trigger thresholds are defined in an operations policy, satisfying the primary source requirement that triggers be defined in advance.             |
| DOC-G7  | `api-spec`, `data-model`, and `tests` templates are retained; their unused mirror profiles are removed under R-5.                                             |
| DOC-G8  | The ARD row of the format ledger gains an explicit "normative text not observed" boundary for ISO/IEC/IEEE 42010.                                             |
| DOC-G9  | The PRD row is relabelled as inference rather than standard-grounded, for ISO/IEC/IEEE 29148.                                                                 |
| DOC-G10 | The runbook template gains the automation counter-rule stated by its primary source.                                                                          |

### Suspended program handling

Spec 047 returns to `status: draft` with a recorded suspension rationale before
the first structural commit. Its plan and task return to `draft` with it. Specs
048 through 051 remain draft. PRD-007 records the suspension and the resumption
route. No suspended tranche executes during this program. On completion, the
suspended tranches resume in the consolidated structure, where Specs 049 and
050 author their validators against the reconciled surface rather than the
pre-consolidation one.

## Data Modeling & Storage Strategy

### Frontmatter lineage fields

```yaml
lineage: PRD-008 # required on every Stage 03 spec.md
ard: ARD-0011 # required on every Stage 03 spec.md
adr: [ADR-0021] # optional, ordered, may be empty
predecessor: Spec-051 # optional, single antecedent
```

Values are symbolic identifiers, not paths, so that a stage rename does not
invalidate them. Resolution from identifier to path is owned by the profile
registry. The reciprocal check resolves the declared upstream document and
asserts that it links back to the declaring specification.

### Progress ledger retention

The live ledger holds the current period only. A closed period becomes one
archive record whose payload is the exact bytes of the removed section, with
`original_path` naming the ledger and `archive_reason` recording rotation. The
ledger remains the single durable owner of shared progress; only its window
changes. Recovery is through the existing archive index and recovery script.

### Contract consolidation invariants

Consolidation of the agent governance contracts preserves the assertion set,
not the file layout. For each rule enforced before consolidation there must
exist, after consolidation, a validator assertion that fails on the same
negative fixture. Fixtures are the migration's proof obligation: a rule whose
negative fixture cannot be located is not silently dropped but recorded as an
open item.

## Interfaces & Data Structures

### Migration tooling interface

Migration is performed by a single-purpose script that takes an explicit
mapping and an explicit exclusion set, and that refuses to run when the working
tree is dirty. It performs no inference: every source-to-target pair is
enumerated by the plan, never derived at run time from a pattern that could
match an unintended path.

```
migrate --map <mapping.json> --exclude <exclusions.txt> --dry-run
migrate --map <mapping.json> --exclude <exclusions.txt> --apply
```

`--dry-run` prints the full change set and exits non-zero if any target already
exists, if any source is inside the exclusion set, or if any rewrite would
touch a file whose path matches an archive route.

### Validator selection contract

`validation-surfaces.json` remains the sole owner of validator identity, argv,
lane membership, evidence lane, and fallback status. C-6 adds one assertion to
it: the declared set and the executable set under `scripts/` must be equal,
checked by a validator that is itself declared.

## Edge Cases & Error Handling

| Condition                                                                    | Deterministic behavior                                                                                       |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| A rewrite target path already exists                                         | Migration aborts before any write; no partial state is produced.                                             |
| A source path resolves inside `docs/98.archive/**`                           | Migration aborts and names the offending path; archive exclusion is fail-closed, never best-effort.          |
| A Stage 90 dated observation names a retired path                            | The path is retained and annotated; the file is not rewritten. Only navigational link targets are rewritten. |
| A `plan.md` has no sibling `spec.md` after migration                         | C-1 validation fails the commit.                                                                             |
| A specification declares a lineage identifier that does not resolve          | C-4 validation fails with the unresolved identifier named.                                                   |
| A declared upstream owner does not link back                                 | C-4 reciprocal validation fails and names both endpoints.                                                    |
| A retired rule sentence survives in a live document                          | C-5 validation fails and names the file and line.                                                            |
| A validator exists in `scripts/` but not in the selection contract           | C-6 validation fails and names the undeclared executable.                                                    |
| A declared validator names a missing executable                              | C-6 validation fails and names the missing path.                                                             |
| A contract consolidation drops a rule whose negative fixture cannot be found | The rule is recorded as an open item; it is not silently dropped and the commit states it.                   |
| The working tree is dirty when migration starts                              | Migration refuses to run.                                                                                    |

## Failure Modes & Fallback / Human Escalation

Every logical commit must leave the repository quality gate passing. A failing
gate blocks the commit; it is never deferred to a later step.

The reduction steps are ordered so that failure is contained. R-1 through R-4
are independent deletions and relocations: a failure in one does not invalidate
the others. R-6, the agent governance contract consolidation, is the highest
risk step because the majority of declared validators depend on those
contracts; it occupies a single commit that can be reverted without disturbing
any predecessor. If R-6 cannot reach a passing gate within the plan's bounded
attempts, it is reverted and recorded as deferred, and the program completes
without it.

The path rewrite is the highest-blast-radius step. Its fallback is
`git checkout` of the affected paths, which is safe because the rewrite runs
only against a clean working tree and produces exactly one commit.

Human escalation is required before: any change inside the archive stage; any
removal of an enforced rule whose negative fixture cannot be located; any
change that would renumber an existing stage identifier; and any action outside
the local repository.

## Verification Commands

```bash
# Full repository gate. Observed baseline 2026-08-07: PASS in 1m59s.
bash scripts/validate-repo-quality-gates.sh .

# Document classification, links, ownership, and profile conformance.
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root .

# Archive inviolability. Must pass unchanged before and after every step.
python3 scripts/archive_validation.py --root .

# Agent governance contracts, after R-6.
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .
python3 scripts/validate-agent-governance-closure.py --root .

# Validator tests.
python3 -m pytest tests -q
```

Evidence limits: every command above is repository-static. None of them proves
live cluster state, Argo CD reconciliation, Vault or ESO behavior, hosted CI
execution, provider runtime discovery, or remote repository state.

## Success Criteria & Verification Plan

| Criterion ID | Criterion                                                                                                                                         | Evidence                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| VAL-WDTC-001 | Every G-A work unit resolves to one folder holding `spec.md`, `plan.md`, and `tasks.md`, and no live path contains the retired execution segment. | Directory inventory diff plus C-1 validation.                                |
| VAL-WDTC-002 | No authored filename under stages 01 through 04 begins with a date, and every migrated document retains its original `updated` value.             | Filename inventory plus frontmatter diff across the migration commit.        |
| VAL-WDTC-003 | The operations stage resolves at its new number and no tracked non-archive reference to the old segment remains.                                  | Reference count before and after, with the archive exclusion set enumerated. |
| VAL-WDTC-004 | Every Stage 03 specification declares resolvable lineage, and every declared upstream owner links back.                                           | C-4 reciprocal validation over the full corpus.                              |
| VAL-WDTC-005 | Three documents own the authoring rules, and the retired date-based execution sentence returns zero live hits.                                    | Literal search plus rule-ownership inventory.                                |
| VAL-WDTC-006 | Each reduced asset has a recorded before-and-after line count.                                                                                    | Measurement table committed with the work unit's task evidence.              |
| VAL-WDTC-007 | Every gap identifier has an implemented control or a dated recorded decision naming rationale and owner.                                          | Gap disposition table with per-row evidence link.                            |
| VAL-WDTC-008 | The declared and executable validator sets are equal.                                                                                             | C-6 validation.                                                              |
| VAL-WDTC-009 | Archive validation passes with no archive payload, digest, or envelope field modified.                                                            | Archive validation result plus a diff proving zero archive-path changes.     |
| VAL-WDTC-010 | The suspended program is recorded as suspended with rationale and resumption route, and no suspended tranche executed.                            | PRD-007 and Spec 047 status diff plus commit inventory.                      |
| VAL-WDTC-011 | The repository quality gate passes at every logical commit.                                                                                       | Per-commit gate result recorded in the task evidence.                        |

## Traceability

- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Decision**:
  [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Suspended program**:
  [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md)
- **External evidence**:
  [Documentation Architecture and SDLC Document Roles Reference](../../90.references/research/2026-08-07-wer/documentation-architecture-and-diataxis.md)

### Lifecycle Traceability

| PRD requirement                                                                                                | Spec criterion | Verification method                                                                                     |
| -------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------- |
| [REQ-WDTC-001](../../01.requirements/008-workspace-document-taxonomy-consolidation.md#functional-requirements) | VAL-WDTC-001   | Directory inventory and work-unit locality validation prove co-location and execution-stage retirement. |
| N/A — REQ-WDTC-002 shares the PRD-008 source linked above.                                                     | VAL-WDTC-002   | Filename inventory and frontmatter diff prove date removal with preserved dates.                        |
| N/A — REQ-WDTC-003 shares the PRD-008 source linked above.                                                     | VAL-WDTC-003   | Reference counting with an enumerated archive exclusion set proves complete renumbering.                |
| N/A — REQ-WDTC-004 and REQ-WDTC-016 share the PRD-008 source linked above.                                     | VAL-WDTC-004   | Reciprocal lineage validation proves resolvable cross-stage lineage without renumbering.                |
| N/A — REQ-WDTC-005 and REQ-WDTC-006 share the PRD-008 source linked above.                                     | VAL-WDTC-005   | Literal search and ownership inventory prove rule uniqueness and rule retirement.                       |
| N/A — REQ-WDTC-007 through REQ-WDTC-011 share the PRD-008 source linked above.                                 | VAL-WDTC-006   | Recorded per-asset line deltas prove corpus reduction.                                                  |
| N/A — REQ-WDTC-012 shares the PRD-008 source linked above.                                                     | VAL-WDTC-007   | Per-gap evidence links prove implemented control or recorded decision.                                  |
| N/A — REQ-WDTC-013 shares the PRD-008 source linked above.                                                     | VAL-WDTC-008   | Declared-versus-executable equality validation proves enforcement closure.                              |
| N/A — REQ-WDTC-014 shares the PRD-008 source linked above.                                                     | VAL-WDTC-009   | Archive validation and a zero-change archive diff prove inviolability.                                  |
| N/A — REQ-WDTC-015 shares the PRD-008 source linked above.                                                     | VAL-WDTC-010   | Status diff and commit inventory prove suspension without execution.                                    |
| N/A — REQ-WDTC-001 through REQ-WDTC-016 share the PRD-008 source linked above.                                 | VAL-WDTC-011   | Per-commit repository quality gate results prove continuous green state.                                |
