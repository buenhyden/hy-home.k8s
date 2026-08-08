---
title: 'Reference: Documentation Architecture and Diataxis'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
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

| Quadrant | Reader need and authoring test | Workspace relationship | Current status / gap |
| --- | --- | --- | --- |
| Tutorial | Learning by completing a guided lesson; success is a novice gains capability, not merely reaches a production goal. | A Guide can contain a carefully bounded lesson, but the `sdlc/guide` profile does not distinguish a learning progression. | No dedicated tutorial profile, index, or classification check was found. |
| How-to guide | Accomplishing a specific real-world goal; success is safe, ordered, verifiable steps. | Guides and Runbooks contain how-to-shaped material. Runbooks additionally carry operations/recovery authority. | Partially implemented; the Guide template requires audience, prerequisites, steps, and pitfalls. Do not call every Guide a tutorial. |
| Reference | Looking up accurate, complete, stable facts; success is findability and correctness. | Stage 90 references and schema/profile facts are reference-shaped; LLM-WIKI is a routing reference, not copied reference content. | Partially implemented through typed reference records and owner maps. Accuracy/freshness remains source-owner responsibility. |
| Explanation | Understanding concepts, rationale, context, trade-offs, and why; success is a coherent mental model. | ADR consequences, architecture narratives, and research may contain explanation sections. | No dedicated explanation family or declared classification/check was found; rationale can be lost when it is mixed with procedures. |

The quadrants are orthogonal to document families. An ADR can explain a decision
while remaining an ADR; a Runbook can include a short reference table while
remaining an operational procedure. Forcing a one-to-one mapping would obscure
authority, safety, and reader intent.

### Architecture rules by scope

| Scope | Canonical owner | Authoring rule | Failure boundary |
| --- | --- | --- | --- |
| Work item | The selected profile/template and its stage document. | State reader goal, authority, and traceability; select a Diátaxis mode for the main content. | A profile pass does not prove readers can act safely or understand it. |
| Collection/index | README or collection-index profile. | Link to one canonical owner; do not duplicate procedure, policy, or decision content. | An index is navigation, not a substitute for a lifecycle record. |
| Cross-stage lineage | PRD/ARD/ADR/Spec/Plan/Task traceability. | Preserve upstream/downstream relationship and evidence boundary. | Diátaxis wording must not bypass typed status, approval, or reciprocal-link requirements. |
| Operations/security | Policy, Runbook, Incident, Postmortem. | Keep commands, impact facts, controls, and recovery evidence in their respective owners; label assumptions and approvals. | Helpful prose never authorizes secrets, production access, deployment, or recovery action. |
| Reference/research | Stage 90 owner and source ledger. | Date sources, record claim/support/limitation/refresh trigger, and distinguish inference. | Research cannot promote an external framework into local policy. |

### As-Is, gap, target

| Area | As-Is evidence | Gap or risk | Target application (analysis only) |
| --- | --- | --- | --- |
| Typed taxonomy | Profiles define routes, lifecycle states, H2 contracts, templates, and traceability for established SDLC families. | The taxonomy identifies lifecycle family, not reader need. | Keep these layers separate; document the intended Diátaxis mode in authoring/review guidance before adding types. |
| How-to | Guide and Runbook templates require step-oriented sections; Runbooks require verification/evidence/recovery. | Mixing novice learning with an urgent operational procedure can hide prerequisites or safety context. | Write a focused how-to for one goal; preserve operational authority and recovery rules in a Runbook. |
| Reference | `content/reference` records and LLM-WIKI owner links support stable lookup. | A link map may be stale, and a profile cannot certify source accuracy. | Put facts in the canonical reference, date external observations, and make generated pointers fail on drift. |
| Tutorial | No dedicated route/profile/template or index was found. | Newcomers may receive goal-oriented steps without concepts, safe setup, or a learning outcome. | Begin with a review checklist and a small pilot only if a named audience/use case warrants it; do not create a profile by implication. |
| Explanation | No dedicated route/profile/template or index was found. | Rationale and trade-offs may be embedded in ADRs or guides where readers cannot find them. | Prefer an explicitly labelled explanation section or a canonical reference where routing justifies it; design a typed family only with an owner/consumer/validator need. |

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

## Sources

- [Diátaxis — Start here](https://diataxis.fr/start-here/) and [Diátaxis home](https://diataxis.fr/), checked 2026-08-08. They define tutorials, how-to guides, reference, and explanation as distinct documentation needs; they do not prescribe this repository's schema.
- Workspace observation, 2026-08-08: `document-profiles.json`, selected Guide/Runbook templates, Stage 90 reference profiles, stage-routing and stage-authoring documents. This is static configuration evidence only.

## Review and Freshness

Refresh when documentation taxonomy, public audience, Guide/Runbook/reference
templates, profile schema, collection navigation, or authoring/review standards
change. Re-evaluate a tutorial/explanation proposal only when it names an owner,
reader, consumer, and validation approach. Diátaxis source observation is dated
2026-08-08.

## Related Documents

- [SDLC document contracts](spec-driven-sdlc-and-document-contracts.md)
- [LLM-WIKI routing](llm-wiki-and-knowledge-routing.md)
- [Template routing](../../../99.templates/support/template-routing.md)
- [Document profiles](../../../99.templates/support/document-profiles.json)
- [Source ledger](source-coverage-and-migration-ledger.md)
