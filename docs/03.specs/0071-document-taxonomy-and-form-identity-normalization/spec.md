---
title: 'Document Taxonomy and Form Identity Normalization Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: draft
owner: platform
updated: 2026-09-02
artifact_id: "SPEC-0071"
---

# Document Taxonomy and Form Identity Normalization Technical Specification (Spec)

## Overview

A document's `type` was supposed to name what the document is. In practice it
named where the repository happened to put the profile: an operations runbook
declared `sdlc/runbook`, a Stage 90 research note declared
`content/research-reference`, and a sealed tombstone declared `content/archive`.
Three of those four family tokens carried no meaning a reader could use, and
`content` covered references and archives at once.

The same drift ran through the neighbouring keys. `layer` repeated the stage
directory including its sort prefix (`03.specs`), so the ordering hint was
duplicated in every document. `version` used a two-component grammar while every
machine contract in the repository used three. Stage 99 forms were named for
their acronyms (`ad`, `adr`) or repeated their own directory
(`archive/archive-record`), one governance form served six different Stage 00
owners, and the Codex runtime form was Markdown although the Codex runtime reads
TOML.

Underneath all of it, `docs/99.templates/contracts/frontmatter.schema.json`
declared the value grammar for every authored key and **nothing loaded it**. The
schema was a tracked document with no consumer, which is why two of the grammars
it declared had already drifted from the corpus it was supposed to govern.

This Spec gives every profile a `family/kind` identity, removes the stage prefix
from `layer`, moves `version` to the semantic grammar, names each Stage 99 form
for the document it produces, and makes the frontmatter schema an enforced
contract rather than a declared one.

Direct human approval on 2026-09-02 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

Counts in this document are point-in-time audit evidence recorded on
2026-09-02. They are not permanent governance invariants.

## Strategic Boundaries & Non-goals

In scope: the `id` and `class` of every profile in
`docs/99.templates/registry.json`; the `version`, `layer`, `supersedes`, and
`superseded_by` grammars in `frontmatter.schema.json` and the `class` domain in
`document-profile.schema.json`; the `type`, `layer`, `version`, and supersession
values of every tracked authored document; the file name, location, and
frontmatter of every Stage 99 form; the executable owners that name a profile
identity; and the Stage 98 generation contracts that pin sealed bytes.

Out of scope: the path or file name of any authored document outside Stage 99;
any document's stage, owner, lifecycle status, or meaning; artifact identity
patterns, which SPEC-0067
already normalized and this Spec only verifies; rendering agent projections from
the registry, which SPEC-0068 owns; and retired-provider residue, which
SPEC-0070 owns.

Renaming a profile is not a lifecycle event. A document whose `type` changes
from `sdlc/runbook` to `operation/runbook` is the same document under the same
authority; it is not superseded, revised, or re-approved.

## Contracts

- **C1 — Family and kind.** A profile identity is `<family>/<kind>`. The family
  names the document class the repository recognizes — `sdlc`, `operation`,
  `reference`, `archive`, `governance`, `readme`, `exception` — and the kind
  names the document. A profile's `class` equals its family.
- **C2 — Stage-free layer, where a layer exists.** `layer` is the owning
  stage's slug without its numeric sort prefix; the prefix orders directories
  and is not part of a layer's name. Only a document that lives in a numbered
  stage declares one. Stage 00 governance documents and Stage 99 forms do not:
  Stage 00 is the authority above the numbered stages, and a form is not the
  document it produces.
- **C3 — Semantic version.** `version` matches
  `^[0-9]+\.[0-9]+\.[0-9]+$`, the grammar every machine contract in this
  repository already used. Normalization appends a patch component to the
  existing value. It does not renumber, reset, or increment any document.
- **C4 — Shared key set.** Every profile that admits frontmatter declares
  `title`, `version`, `type`, `status`, `owner`, and `updated`, in that order,
  before any other key. `layer` follows `type` and `artifact_id` follows
  `updated` wherever the profile declares them. The exclusions are contractual,
  not accidental: `governance/*` declares no `artifact_id` because Stage 00
  carries no artifact identity, neither `governance/*` nor any form declares a
  `layer` under C2, and an `exception/*` provider binding declares only the
  keys its runtime reads.
- **C5 — Form names its output.** A Stage 99 form is named for the document it
  produces, in the directory of the stage that owns it, and never repeats that
  directory in its own file name. A form's extension is the extension the
  consuming runtime reads.
- **C6 — One form per owner kind.** A profile has exactly one form and a form
  has exactly one owning profile.
- **C7 — Placeholders where the contract allows one.** A form spells every
  author-supplied value as a placeholder. `type`, `layer`, and `status` are
  fixed by the profile and are therefore written as their real values, not as
  placeholders.
- **C8 — Title carries no identity.** A `title` never repeats the document's
  `artifact_id`. The body H1 may.
- **C9 — One value contract, enforced.** `frontmatter.schema.json` owns the
  value grammar of every authored key and is evaluated against every classified
  document on every strict run. A grammar it declares and no run evaluates is a
  contract violation, not a style preference.
- **C10 — Generation-pinned sealed bytes.** A sealed Stage 98 record is parsed
  against the frontmatter generation its own digest names. A later key set or
  profile identity never retroactively invalidates reviewed bytes.
- **C11 — A package proves its own navigation.** A Stage 03 package carries no
  router document. `spec.md` owns the change contract, `plan.md` owns
  implementation order and risk, and the `tasks/` directory is the Task
  inventory. A separate index restated all three and had to be edited whenever
  a Task was added, so the inventory is derived from `tasks/` rather than from
  a second document that could disagree with it.
- **C12 — One reference structure for all three collections.** Every Stage 90
  collection carries the same three levels: a collection router
  `{audits,data,research}/README.md`, a pack router
  `{collection}/####-<slug>/README.md`, and pack members
  `{collection}/####-<slug>/m####-<slug>.md`. Each level has exactly one Stage
  99 form, and a collection is structural: it exists whether or not it
  currently holds a pack.
- **C13 — A retirement retires a document, not a location.** A sealed ledger
  row pins the bytes it retired, so the fact a retirement control protects is
  that those bytes do not return. A different, reviewed, tracked document may
  later occupy the same path; restoring the retired bytes there is still
  refused. Reading a row as a permanent ban on its path proves nothing extra
  and forbids ordinary reuse of a location.

## Core Design

### Profile identity

Thirteen profiles are renamed and one is split. `sdlc` keeps the artifacts the
delivery lifecycle produces — requirement, architecture description,
architecture decision, spec, data model, plan, task — and loses the five
operations documents and the requirement package's `-package` suffix. Guide,
policy, runbook, incident, and postmortem move to `operation`. The three Stage
90 members move from `content` to `reference`. Tombstone and migration move from
`content` to `archive`. `content` disappears, because it never described
anything.

`governance/reference` becomes six profiles. One form served
`docs/00.agent-governance/policies/`, `providers/`, `roles/`, `skills/`, and
`sdlc.md` at once, so `type` could not tell a reader which of five different
things they were holding. The six kinds — `contract`, `control`, `provider`,
`role`, `rule`, `skill` — each bind one Stage 00 directory. `control` and
`contract` also reserve the Markdown owners for `hooks/` and `contracts/`, which
today hold only executable and JSON files.

Every profile's `class` is set to its family, which required widening the class
domain in the profile schema from five values to seven. `class` had been a
second, coarser taxonomy that disagreed with the identity beside it.

### Form layout

Twelve forms change path. Nine are `replaced` — their bytes changed with their
name — and three are `moved` with identical bytes into
`templates/specs/contracts/`, which now mirrors the authored destination
`docs/03.specs/####-<slug>/contracts/`.

The Codex form is the one substantive change. Its predecessor was Markdown while
`.codex/agents/*.toml` is TOML, so no author could copy the form into the
destination without rewriting it. The replacement is TOML, and a new
`exception/codex-agent-binding` profile binds it to the path the Codex runtime
actually reads. `exception/local-agent-asset` — provider-neutral `.agents/**`
— keeps no form, because a neutral asset is not a provider binding.

### Enforcement

`scripts/validate-markdown-profiles.py` loads `frontmatter.schema.json` and
evaluates it against each classified document's frontmatter mapping, emitting
`FM-SCHEMA`. Two exemptions are deliberate: a `template`-mode profile, whose
placeholders spell grammars the authored contract must reject, and an
`exception`-class profile, whose keys are the runtime's rather than the
document contract's.

Without this the rest of the Spec would be declaration only. The two grammars
this change corrects had already drifted precisely because the schema declaring
them was never read.

### Sealed Stage 98

Stage 98 frontmatter changes, so every pinned generation contract becomes
generation-aware rather than absolute. `archive_validation` parses a pinned
migration against the key tuple and profile identity its digest names;
`archive_recovery` does the same for an ArchiveEnvelope's metadata. Each
previously pinned digest moves into the superseded set for its path, and
MIG-0001 is regenerated from its canonical builder rather than patched, so the
document still equals the reviewed mapping byte for byte.

MIG-0010 seals the twelve form moves. It is required, not decorative: MIG-0004 pins its
Stage 99 targets as paths that must still exist, and only a later sealed row
naming a target as its own `legacy_path` releases it.

## Data Modeling & Storage Strategy

`frontmatter.schema.json` makes `version` required alongside `title`, `type`,
`status`, `owner`, and `updated`; `layer` and `artifact_id` stay optional there
because the registry decides per profile which of the two a document carries.

No new contract file is introduced. `registry.json` gains six governance
profiles and one Codex binding profile and loses two — the single governance
reference and its template mirror, plus the template mirror of the neutral
agent asset, which no longer has a Markdown form. `frontmatter.schema.json`
gains `supersedes` and `superseded_by`, whose values were previously
undeclared and inconsistently spelled: a single successor was sometimes quoted
and sometimes bare, and a multiple-successor value was a quoted string that
merely looked like a list. Both are now one identity or an ordered set of them.

## Interfaces & Data Structures

The authored interface is the shared frontmatter block:

```yaml
---
title: 'Reference Maintenance Runbook'
version: "1.0.0"
type: operation/runbook
layer: "operations"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "RUN-0011"
---
```

The form interface spells the same keys as placeholders:

```yaml
---
title: '{Topic Name} Runbook'
version: "#.#.#"
type: operation/runbook
status: draft
owner: '{owner}'
updated: YYYY-MM-DD
artifact_id: "RUN-####"
---
```

The form omits `layer`: the form is not the document, and the author writes the
owning stage's slug when the copy lands in that stage.

`scripts/validate-markdown-profiles.py --root . --mode strict` is the enforcing
interface. A value that violates the schema reports `FM-SCHEMA` naming the
JSON path and the offending value, and the run exits non-zero.

## Edge Cases & Error Handling

A base-commit registry still projects onto the current lifecycle contract: the
comparison alias table gains one entry per retired profile identity, so a
lifecycle run against an older base does not report every profile as unknown.

A sealed record from a prior generation still parses. `is_superseded` selects
the prior key tuple and the prior profile identity; a record that mixes the two
generations matches neither and fails, which is the intended outcome for a
hand-patched sealed file.

A form placeholder that spells a grammar the authored schema rejects is correct,
not a defect — that is what makes it a placeholder. The exemption is bound to
`profile.mode == "template"` so it cannot leak to an authored document.

A document that declares `version: 1.0` after this change is rejected by an
anchored pattern. This is the intended failure for a file authored from a stale
copy rather than from a form.

## Failure Modes & Fallback / Human Escalation

The registry edit, the corpus edit, and the executable-owner edit are one
change. Landing any one alone leaves every document unclassifiable, so
verification runs against the whole change rather than any part of it.

Rollback is a Git revert of that change. MIG-0010 pins its source commit, so a
revert restores the twelve forms from the pinned bytes rather than from memory.

Escalate to the human owner if a sealed Stage 98 record is found whose digest
matches neither the current nor a declared prior generation, because C10
forbids inventing a generation for bytes no review recorded.

## Verification Commands

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 -m unittest discover --start-directory tests --top-level-directory tests
bash scripts/validate-repo-quality-gates.sh .
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-DTF-001 | Every profile identity is `family/kind` and every profile `class` equals its family | Registry projection over all profiles |
| VAL-DTF-002 | Every classified document's `type` equals its profile identity | Strict Markdown profile run over the full corpus |
| VAL-DTF-003 | Every `layer` is a stage slug with no numeric prefix and every `version` is three components | Frontmatter schema evaluation over the full corpus |
| VAL-DTF-004 | Every frontmatter-bearing profile declares the shared key set in one order, with only the two contractual exclusions | Registry key-order projection |
| VAL-DTF-005 | Every Stage 99 form is named for its output, owned by exactly one profile, and spells placeholders where the contract admits one | Registry template parity plus form inspection |
| VAL-DTF-006 | The frontmatter schema is evaluated on every strict run and rejects each retired grammar | Rejected-sample assertions for version, layer, and date |
| VAL-DTF-007 | Every sealed Stage 98 record parses against its own generation and no payload byte changes | Strict lifecycle run plus archive payload diff |
| VAL-DTF-008 | MIG-0010 seals all twelve form moves against pinned Git provenance | Sealed migration parse and recovery verification |
| VAL-DTF-009 | No executable owner, test, or current document names a retired profile identity except as declared history | Retired-identity absence sweep |
| VAL-DTF-010 | No Stage 03 package holds a `README.md`, and no current document links one | Package inventory sweep plus strict link validation |
| VAL-DTF-011 | The package Task inventory is proved from `tasks/` alone, with no router document in the projection | Delegated-execution and program-relation validation |
| VAL-DTF-012 | All three Stage 90 collections carry a router, and each of the three structural levels has exactly one Stage 99 form | Reference-pack topology check plus registry template parity |
| VAL-DTF-013 | A retired path accepts a different tracked document and refuses the retired bytes | Focused MIG-0004 admission and resurrection cases |

## Traceability

### Lifecycle Traceability

This Spec has no Requirement Package or Architecture Description. Its
authority is the direct human approval recorded above under
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md).

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — standalone, direct approval | VAL-DTF-001 | Registry profile projection |
| N/A — standalone, direct approval | VAL-DTF-002 | Strict corpus-wide profile validation |
| N/A — standalone, direct approval | VAL-DTF-003 | Frontmatter schema evaluation |
| N/A — standalone, direct approval | VAL-DTF-004 | Registry key-order projection |
| N/A — standalone, direct approval | VAL-DTF-005 | Template parity check and form inspection |
| N/A — standalone, direct approval | VAL-DTF-006 | Rejected-sample assertions |
| N/A — standalone, direct approval | VAL-DTF-007 | Strict lifecycle run and payload diff |
| N/A — standalone, direct approval | VAL-DTF-008 | Sealed migration parse |
| N/A — standalone, direct approval | VAL-DTF-009 | Retired-identity absence sweep |
| N/A — standalone, direct approval | VAL-DTF-010 | Package inventory sweep and strict link validation |
| N/A — standalone, direct approval | VAL-DTF-011 | Delegated-execution projection check |
| N/A — standalone, direct approval | VAL-DTF-012 | Reference-pack topology check |
| N/A — standalone, direct approval | VAL-DTF-013 | Retirement admission and resurrection cases |

### Related Documents

- [Implementation order and risk](plan.md)
- [Current Spec Index](../README.md#current-spec-index)
- [ADR-0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- [SPEC-0071-TSK-0001](tasks/tsk-0001-dtf-000.md)
- [Archive Index](../../98.archive/README.md) routes MIG-0010, which seals the form moves
- [Template Registry](../../99.templates/README.md)
- [Document Authoring Policy](../../00.agent-governance/policies/document-authoring.md)
- [Quality Policy](../../00.agent-governance/policies/quality.md)
