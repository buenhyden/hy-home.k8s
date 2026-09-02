---
title: 'Reference: Documentation Architecture and Diataxis'
version: "1.0"
type: content/research-reference
layer: "90.references"
status: active
owner: platform
updated: 2026-08-31
artifact_id: "RES-0001-m0005"
---

# Reference: Documentation Architecture and Diataxis

## Overview

This reference applies the official Diátaxis framework to the workspace without
mistaking its four user needs for the workspace's SDLC document types. The
stage taxonomy answers who owns a document and its lifecycle; Diátaxis answers
what kind of help a reader needs from a passage or document.

## Reference Type

Source-backed documentation-architecture analysis, not a profile/schema change
or a declaration that a document is complete, usable, or accessible.

## Authority Boundary

The Stage 99 profile/schema, selected templates, stage-routing rule, and
canonical stage owners remain authoritative. This document neither adds a
Tutorial/Explanation profile nor classifies every existing document. Static
profile validity proves structural compliance only; usability requires review
against an intended reader and task.

## Scope

It covers REQ-WERPC-020: the four Diátaxis quadrants, their partial current
application, the tutorial/explanation gaps, and safe target-state guidance.

## Definitions / Facts

### Diátaxis baseline

Diátaxis separates documentation by reader need and writing mode:

| Quadrant     | Reader need and authoring test                                                                                      | Workspace relationship                                                                                                            | Current status / gap                                                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Tutorial     | Learning by completing a guided lesson; success is a novice gains capability, not merely reaches a production goal. | A Guide can contain a carefully bounded lesson, but the `sdlc/guide` profile does not distinguish a learning progression.         | No dedicated tutorial profile, index, or classification check was found.                                                             |
| How-to guide | Accomplishing a specific real-world goal; success is safe, ordered, verifiable steps.                               | Guides and Runbooks contain how-to-shaped material. Runbooks additionally carry operations/recovery authority.                    | Partially implemented; the Guide template requires audience, prerequisites, steps, and pitfalls. Do not call every Guide a tutorial. |
| Reference    | Looking up accurate, complete, stable facts; success is findability and correctness.                                | Stage 90 references and schema/profile facts are reference-shaped; LLM-WIKI is a routing reference, not copied reference content. | Partially implemented through typed reference records and owner maps. Accuracy/freshness remains source-owner responsibility.        |
| Explanation  | Understanding concepts, rationale, context, trade-offs, and why; success is a coherent mental model.                | ADR consequences, architecture narratives, and research may contain explanation sections.                                         | No dedicated explanation family or declared classification/check was found; rationale can be lost when it is mixed with procedures.  |

The quadrants are orthogonal to document families. An ADR can explain a decision
while remaining an ADR; a Runbook can include a short reference table while
remaining an operational procedure. Forcing a one-to-one mapping would obscure
authority, safety, and reader intent.

### Architecture rules by scope

| Scope               | Canonical owner                                       | Authoring rule                                                                                                            | Failure boundary                                                                           |
| ------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Work item           | The selected profile/template and its stage document. | State reader goal, authority, and traceability; select a Diátaxis mode for the main content.                              | A profile pass does not prove readers can act safely or understand it.                     |
| Collection/index    | README or collection-index profile.                   | Link to one canonical owner; do not duplicate procedure, policy, or decision content.                                     | An index is navigation, not a substitute for a lifecycle record.                           |
| Cross-stage lineage | PRD/ARD/ADR/Spec/Plan/Task traceability.              | Preserve upstream/downstream relationship and evidence boundary.                                                          | Diátaxis wording must not bypass typed status, approval, or reciprocal-link requirements.  |
| Operations/security | Policy, Runbook, Incident, Postmortem.                | Keep commands, impact facts, controls, and recovery evidence in their respective owners; label assumptions and approvals. | Helpful prose never authorizes secrets, production access, deployment, or recovery action. |
| Reference/research  | Stage 90 owner and source ledger.                     | Date sources, record claim/support/limitation/refresh trigger, and distinguish inference.                                 | Research cannot promote an external framework into local policy.                           |

### As-Is, gap, target

| Area           | As-Is evidence                                                                                                     | Gap or risk                                                                                           | Target application (analysis only)                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Typed taxonomy | Profiles define routes, lifecycle states, H2 contracts, templates, and traceability for established SDLC families. | The taxonomy identifies lifecycle family, not reader need.                                            | Keep these layers separate; document the intended Diátaxis mode in authoring/review guidance before adding types.                                                        |
| How-to         | Guide and Runbook templates require step-oriented sections; Runbooks require verification/evidence/recovery.       | Mixing novice learning with an urgent operational procedure can hide prerequisites or safety context. | Write a focused how-to for one goal; preserve operational authority and recovery rules in a Runbook.                                                                     |
| Reference      | `content/reference` records and LLM-WIKI owner links support stable lookup.                                        | A link map may be stale, and a profile cannot certify source accuracy.                                | Put facts in the canonical reference, date external observations, and make generated pointers fail on drift.                                                             |
| Tutorial       | No dedicated route/profile/template or index was found.                                                            | Newcomers may receive goal-oriented steps without concepts, safe setup, or a learning outcome.        | Begin with a review checklist and a small pilot only if a named audience/use case warrants it; do not create a profile by implication.                                   |
| Explanation    | No dedicated route/profile/template or index was found.                                                            | Rationale and trade-offs may be embedded in ADRs or guides where readers cannot find them.            | Prefer an explicitly labelled explanation section or a canonical reference where routing justifies it; design a typed family only with an owner/consumer/validator need. |

### Authoring and review checklist

1. Identify whether the primary reader needs to learn, accomplish, look up, or
   understand. Record one primary mode; a supporting section may have another.
2. Select the existing SDLC family by authority and lifecycle, then its required
   template. Do not select a family because its Diátaxis label sounds similar.
3. For how-to/Runbook content, include preconditions, outcome verification,
   failure/recovery boundary, and any required approval. For tutorials, use a
   safe learning environment and a learning outcome. For reference, avoid
   procedural narrative. For explanation, make trade-offs explicit.
4. Keep executable production procedures, incident facts, policy controls, and
   release approval in their canonical families. Link rather than copy them.
5. Run the profile/link/owner checks and use a human reader review for clarity,
   accessibility, and safety; no static validator can infer those properties.

### 2026-08-11 upstream-source verification and decision reconciliation

The published pages remain unreachable, but the claims are now verified against
the upstream source that generates them, and the local "gap" framing is
reconciled against an approved decision.

| Question                                                    | 2026-08-11 result                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Evidence class                          |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Are `diataxis.fr/start-here/` and `diataxis.fr/` reachable? | No. A third attempt from a different client also returned HTTP 429. Three failed attempts across two days and two egresses make the block persistent.                                                                                                                                                                                                                                                                                                                                   | Direct observation                      |
| Do the four modes and their authoring tests still hold?     | Yes. `source/start-here.rst` at `evildmp/diataxis-documentation-framework@main` states the four kinds are tutorials, how-to guides, reference, and explanation, and defines a tutorial as a lesson serving study, a how-to guide as addressing a real-world goal for an already-competent user at work, reference as neutral technical description, and explanation as context and background serving study ([SRC-WERPC-067](m0012-source-coverage.md#source-register)). | Upstream source, not the published page |
| Does the framework mandate creating the four sections?      | No, and it says the opposite. `source/how-to-use-diataxis.rst` states verbatim: "It certainly does not mean that you should create empty structures for tutorials/howto guides/reference/explanation with nothing in them. Don't do that. It's horrible." It adds that "Diátaxis changes the structure of your documentation from the inside."                                                                                                                                          | Upstream source, not the published page |

The upstream repository is the source that builds the site, so it is stronger
evidence than an inference about commit dates, but it is still not the published
page. A published page can lag or diverge from `main`. Treat these as
source-verified, not page-verified.

#### The tutorial and explanation absence is a decision, not an unmade choice

This report's `As-Is, gap, target` table records that no tutorial or explanation
route exists, and `REQ-WERPC-020` carries `Partial` on that basis. Both remain
factually correct as observations, but read alone they suggest an open question.
They are reconciled here.

Spec 052 is `active` and already decided the question. `DOC-G2` states no
tutorial route is created because Diátaxis says empty structures must not be
created in advance, and `DOC-G3` declines an explanation route on the same
recorded basis, keeping explanation inside ADR context and reference sub-types.
The verbatim upstream sentence quoted above is that recorded basis, now checked
at source rather than accepted secondhand.

The consequence is that creating these two profiles would contradict both the
approved local decision and the framework's own instruction. The open item is
not a missing route. It is `DOC-G1`: constraining `Guide Type` to the
enumeration `how-to`, `tutorial`, `concept` in the profile registry and template,
which a 2026-08-11 registry check confirms is still unenforced, together with
validating that the eight current guides declare their type and recording the
`DOC-G2` and `DOC-G3` absences deliberately. That work is the queued `WORK-013`
package and belongs to its owning Plan, not to this reference.

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-020 re-observation

**External result:** `unchanged`, and for the first time in four cycles the
published page was directly reachable (`SRC-WERPC-089`). Prior cycles recorded
`diataxis.fr` behind HTTP 429 on three separate attempts and verified the claims
against the upstream source that builds the site, registered as
`SRC-WERPC-067`. On 2026-08-17 the published page responded directly, so that
fallback was not needed. The framework still defines tutorials, how-to guides,
reference, and explanation as four distinct needs separated by the action-versus-
cognition and study-versus-work axes, consistent with every prior observation.

**Workspace result:** `confirmed`. No tutorial or explanation profile identifier
exists in `document-profiles.json`.
`docs/03.specs/052-document-taxonomy-consolidation/spec.md:200-201` still records
`DOC-G2` and `DOC-G3`, which establish that the absence is a decision resting on
the framework's own instruction not to create empty structures, rather than an
open question. `DOC-G1` at `spec.md:199` remains unenforced, and `sdlc/guide`'s
`Guide Type` heading at `document-profiles.json:733` still carries no value
constraint. The eight tracked guides all still declare `how-to`.

**Status effect:** `no-change` (`CLM-WERPC-011-20`). `REQ-WERPC-020` keeps
`Partial`, and that `Partial` continues to reflect unenforced `DOC-G1` enum work
rather than an undecided route. The direct reachability of the source removes a
standing evidence caveat without changing any status.

**Blocking class:** `human-judgement`. The remaining work is an approved
enforcement decision and, for the usability half, a named reader-validation
activity. Neither is obtainable by reading files. Reopens when `WORK-013`
executes, when Spec 052 is superseded, when a current Guide stops satisfying the
static contract, or when a reader-validation activity is approved.

## Sources

- [Diátaxis — Start here](https://diataxis.fr/start-here/) and [Diátaxis home](https://diataxis.fr/), checked 2026-08-08. They define tutorials, how-to guides, reference, and explanation as distinct documentation needs; they do not prescribe this repository's schema.
- [Diátaxis upstream source](https://github.com/evildmp/diataxis-documentation-framework) `source/start-here.rst` and `source/how-to-use-diataxis.rst` at `main`, checked 2026-08-11 (`SRC-WERPC-067`). This is the source that builds the site, not the published page.
- Workspace observation, 2026-08-08: `document-profiles.json`, selected Guide/Runbook templates, Stage 90 reference profiles, stage-routing and stage-authoring documents. This is static configuration evidence only.

## Review and Freshness

Refresh when documentation taxonomy, public audience, Guide/Runbook/reference
templates, profile schema, collection navigation, or authoring/review standards
change. Re-evaluate a tutorial/explanation proposal only when it names an owner,
reader, consumer, and validation approach. Diátaxis source observation is dated
2026-08-08.

A re-check attempted on 2026-08-10 did not succeed. Both `diataxis.fr/start-here/`
and `diataxis.fr/` returned HTTP 429 across repeated attempts and path variants,
so the pages were unreachable from that egress. This is `unreachable`, not
`unchanged`: the four-mode model, the quadrant names, and the load-bearing
boundary that Diátaxis describes documentation needs rather than mandating a
document type system were not re-verified and retain their 2026-08-08
observation date. As a labelled inference only, the upstream source repository
`evildmp/diataxis-documentation-framework` shows no commit between 2026-08-08
and 2026-08-10, and the last change to the `start-here` source was a 2026-08-01
typo fix; an upstream repository state cannot establish what the published pages
currently say. A second independent attempt later on 2026-08-10 also failed: ten requests across `/start-here/`, `/`, `www.diataxis.fr`, and an unrelated `/map/` probe all returned HTTP 429, so the block is host-wide for this egress rather than specific to the cited pages. Two failed re-checks on the same day make this a persistent condition, not a transient one. A third attempt on 2026-08-11 from a different client also returned HTTP 429, so the published pages stay unverified. The four-mode claims and the no-mandated-structure boundary are now verified against the upstream source instead, which is a different and slightly weaker evidence class than the published page. Re-run the page check from a different egress if page-level verification is required.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and checked on **2026-08-12**; the heading
retains the approved package date. It addresses only REQ-WERPC-020 and uses
official Diátaxis evidence plus the existing registered source and claim rows.
No secondary source, taxonomy change, empty route, or Guide instance was added.

#### Published-page provenance and retained decision

| Official primary page                                                                   | 2026-08-12 observation                                                                                                                                                              | Claim boundary                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Diátaxis home](https://diataxis.fr/) and [Start here](https://diataxis.fr/start-here/) | Both published pages were reachable. They directly retain the four forms—tutorials, how-to guides, technical reference, and explanation—and distinguish them by user need.          | This re-verifies the framework claims recorded by `SRC-WERPC-020`, `SRC-WERPC-067`, and `CLM-WERPC-003-08`; it does not prescribe a workspace profile or prove local reader outcomes.                                                                                                         |
| [Diátaxis as a guide to work](https://diataxis.fr/how-to-use-diataxis/)                 | The published page was reachable and directly retains the instruction not to create empty four-part structures, with documentation structure developing from internal improvements. | This is the successful published-page re-check named by `SRC-WERPC-067`'s refresh trigger. It upgrades current provenance from upstream-source-only to page-verified without changing the claim. The page exposes no publisher revision date, so it does not establish when the text changed. |

No fallback was needed on this check. The exact upstream `main` files already
registered as `SRC-WERPC-067` remain provenance for the failed 2026-08-10 and
2026-08-11 page observations; the successful 2026-08-12 published-page result
does not rewrite those dated facts. One source proposal records the materially
new page-level provenance. No claim proposal is created because the supported
claims are unchanged.

Spec 052 remains `active`: `DOC-G2` declines a tutorial route, `DOC-G3`
declines an explanation route on the same recorded basis, and `DOC-G1` assigns
Guide Type enumeration to the existing implementation path. `WORK-013` is
still `Queued` / `Not executed`. The current profile still has no separate
tutorial or explanation route, all eight numbered Guides declare `how-to`, and
`CLM-WERPC-003-09` remains `Partial` because static classification does not
establish reader usefulness.

**Final disposition:** REQ-WERPC-020 remains `Partial` and
`exclude-duplicate`. Do not create empty tutorial or explanation structures or
reopen `DOC-G2`/`DOC-G3`. Reconsider only if Spec 052 is superseded or a
concrete owner, reader, consumer, instance, and validation need is approved.
Guide classification correctness, usability, accessibility, safe execution,
and effectiveness remain `DEFER` without actual reader evidence.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-020` only, checked on **2026-08-14**. It did not
invoke a provider, query the GitHub remote, or inspect a cluster.

#### REQ-WERPC-020 Diátaxis workspace and source consistency check

**Workspace delta:** `no-change`. `docs/05.operations/guides/` still holds
exactly eight numbered Guide instances (`0001`, `0002`, `0003`, `0006`,
`0007`, `0008`, `0009`, `0010`), each still declaring `` `how-to` `` under
its `## Guide Type` heading. `git diff --stat a5d2dfbb HEAD --
docs/05.operations/guides/ docs/99.templates/registry.json`
shows no change under `docs/05.operations/guides/`; the profiles file itself
appears in the diff, but a parsed-JSON key-level comparison against the
`a5d2dfbb` baseline shows only the `standaloneExecutions` key differs (this
cycle's own Spec 057/Plan/Task admission) — the `profiles` array, including
the `sdlc/guide` entry and its `Guide Type` heading requirement, is
byte-for-byte identical; the surrounding whitespace-only reflow is the
formatter noted in this pack's evidence boundary. Spec 052 remains `active`;
`DOC-G1` still has no enum constraint in the `sdlc/guide` profile object,
`DOC-G2`/`DOC-G3` remain decided and unreopened, and `WORK-013` remains
`Queued` / `Not executed` (confirmed by re-grep; no other file assigns it a
different state).

**External result:** `SRC-WERPC-067` was re-checked first, per the pack's
recorded evidence order. `source/start-here.rst` and
`source/how-to-use-diataxis.rst` at
`evildmp/diataxis-documentation-framework@main` still hold the exact
verbatim text already adopted: the tutorial/how-to/reference/explanation
definitions, and "It certainly does not mean that you should create empty
structures for tutorials/howto guides/reference/explanation with nothing in
them." The published site was then attempted once, as instructed:
`https://diataxis.fr/start-here/` was reachable this time (unlike the three
429 responses recorded 2026-08-10/2026-08-11) and directly confirmed the
same four-kind definitions already recorded by `SRC-WERPC-071`'s 2026-08-12
published-page check. This is the pack's second successful published-page
observation of this page; no page-content or publisher-date claim beyond
"reachable and matching" is made.

**As-Is:** Unchanged from the 2026-08-12 section: the tutorial/explanation
absence remains a decided outcome of Spec 052 `DOC-G2`/`DOC-G3`, not an open
gap. The open item remains `DOC-G1` registry-enum enforcement, queued under
`WORK-013`.

**Gap and bounded target:** Unchanged. No tutorial or explanation route is
proposed or reopened. `DOC-G1` enum enforcement and eight-guide
re-validation remain the only open Diátaxis-adjacent item, and both belong
to `WORK-013`'s owning Plan, not this reference.

**Missing evidence:** a named reader, task, environment, method, acceptance
threshold, and evidence owner for Guide classification usefulness; `DOC-G1`
enum-enforcement and eight-guide re-validation evidence. **Owning
authority:** Spec 052 for the `DOC-G1`–`DOC-G3` decisions; `WORK-013`'s
owning Plan for enum-enforcement execution. **Safe boundary:** a separately
approved, non-secret reader-validation activity, or the already-approved
`WORK-013` registry/template change executed by its own Plan; neither is
authorized in this increment. **Refresh trigger:** Spec 052 is superseded,
`WORK-013` executes, a current Guide stops satisfying the static contract,
or a named reader-validation activity is approved.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New source registered: `SRC-WERPC-076`. New claim registered:
`CLM-WERPC-010-09`.

### 2026-08-20 full-corpus reverification

This increment consumes the reviewed `REQ-WERPC-020` row and its empty
source/claim allocation slice. The current official pages remain unchanged and
the workspace selector is normalized to
`m0005-documentation-architecture-and-diataxis.md#ditaxis-baseline`. No provider,
published site generator, or reader study was executed.

#### REQ-WERPC-020 Diataxis architecture and reader evidence

- **Sources and result:** `unchanged` / `confirmed`, using existing
  `SRC-WERPC-020`, `SRC-WERPC-071`, and `SRC-WERPC-089` boundaries. The
  official pages still separate tutorial, how-to, reference, and explanation
  by reader need and still advise against creating empty four-part structures.
- **As-Is:** `DOC-G2` and `DOC-G3` retain the deliberate absence of tutorial
  and explanation routes. Guide and Runbook can remain how-to-shaped, Stage 90
  remains reference-shaped, and ADR/research can explain while each keeps its
  own authority and lifecycle. `DOC-G1` enum enforcement remains the open
  repository decision path rather than a reason to add empty families.
- **Gap / Target:** no named reader evidence establishes whether current
  classification is useful, accessible, findable, understandable, or safe for
  a real task. Retain the four purposes as authoring/review tests, preserve the
  decided absences, and route `DOC-G1` through its existing WORK-013 owner.
- **Evidence / rejected inference:** repository-static plus official public
  documentation. The framework neither mandates local profiles nor proves
  reader outcomes; a profile pass and a declared `how-to` value are not
  usability or accessibility evidence.
- **Disposition / retained boundary:** `Partial`; blocking class
  `human-judgement`. Named reader validation and DOC-G1 execution evidence
  remain `DEFER`.
- **Owner / safe follow-up / trigger:** Spec 052 owns `DOC-G1..G3` and the
  WORK-013 Plan owns enum implementation. Reopen if those decisions change, a
  current Guide violates its contract, Diataxis materially changes, or a
  separately approved activity names reader, task, environment, method,
  threshold, and evidence owner.

## Related Documents

- [SDLC document contracts](m0004-spec-driven-sdlc-and-document-contracts.md)
- [LLM-WIKI routing](m0006-llm-wiki-and-knowledge-routing.md)
- [Template routing](../../../99.templates/README.md)
- [Document profiles](../../../99.templates/registry.json)
- [Source ledger](m0012-source-coverage.md)
