---
title: "Document Authoring Policy"
version: "4.1.3"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-17"
---

# Document Authoring Policy

## Purpose and Scope

### Objective

Select the document owner by purpose, author from its canonical template, and
close the change with traceable evidence.

### Applies To

Use [SDLC flow](sdlc.md) to distinguish durable requirements, current
architecture, change-specific behavior, and operating knowledge. Stage numbers
express ownership, not a one-way waterfall.

- Stage 99 Author Guide (`docs/99.templates/README.md`)
- Archive Index (`docs/98.archive/README.md`)

#### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| AUTHOR-R001 | Always | Identify the owning stage and normalize the final repository-relative path. | `markdown-profiles` | none |
| AUTHOR-R002 | Before creating or restructuring a document | Resolve exactly one registry profile and read its canonical template before creating or restructuring a document. No match or multiple matches is a stop condition. Start a new document with `python3 scripts/document-generator.py`, which copies the template, fills the shared value markers from the inputs and the target path, and refuses a request the registry or the identity rules do not admit; the caller writes the number in the path. A hand copy of the form stays valid, and the validators stay the gate for either. | `markdown-profiles` | none |
| AUTHOR-R003 | Always | Use the profile-owned initial status, metadata, sections, and relationships. Do not assume every profile starts at "draft". Router READMEs participate in the governed envelope with an "active" routing constant, but have neither artifact identity nor lifecycle binding. Stable reference pack anchors keep their reference identity and publication lifecycle even when named README.md. | `document-lifecycle` | none |
| AUTHOR-R004 | Always | Take the frontmatter key set from the selected profile (the key order is stated below), and each key's value grammar from the frontmatter schema (`docs/99.templates/01.contracts/frontmatter.schema.json`). The registry's `frontmatter_keys` owns each key's meaning, author, consumers and tests, and its `frontmatter_dialect` owns the YAML and JSON Schema dialect, so neither is restated here. Frontmatter is read as YAML 1.2 through the one loader `scripts/frontmatter_yaml.py`, whose stated refusals that record carries. Every string, date, version, and identity scalar uses double quotes. A "title" never repeats the document's "artifact_id": identity is already a key, and a title that restates it carries no information. | `markdown-profiles` | none |
| AUTHOR-R005 | Always | Treat a key the profile omits as a key the document has no business declaring. `layer` names the numbered stage a document lives in. It is kept only on an accepted architecture decision from ADR-0001 to ADR-0061, which is never edited in place, until a successor replaces it, and never on an ADR after ADR-0061; every other document, common governance and a Stage 99 form declare none. A profile that declares no `artifact_id` describes something the repository does not give a stable identity. Preserve an existing optional governance identity; do not mint one for normalization. | `markdown-profiles` | none |
| AUTHOR-R006 | Always | Replace prompts with concrete content, use complete stable IDs for traceability, and calculate links from the final target path. A file outside `docs/` links to current owners and stage or collection README navigation, never directly to an individual numbered-stage document, including historical records. Renaming a link to a plain path or artifact ID does not remove a current authority dependency: promote the needed rule to its current owner. The boundary normalizes relative/absolute references, Markdown references, HTML/wiki links, repository blob/raw URLs, encoding, case and separators. Machine reads are admitted only by the exact consumer, target and access-kind tuples in the link validator; they do not authorize rendered links. Route grammars stay in the Stage 99 registry. Links inside `docs/` retain their historical and current relationship contracts. Write each traceability relation once, in the document that cites its parent; never hand-write a back-link. Derive the reverse view on demand with `scripts/document-backlinks.py`. Operating supersession is written by its successor and the lifecycle checker derives the reverse relation. Other supersession evidence follows the applicable domain in rule 13. The Stage 99 registry `relationship_contract` owns the meaning of each relation (kind, direction, cardinality, canonical owner, consumers, checks) and of the four link types (normative, evidence, historical, navigation). A link fragment names a heading slug or an explicit anchor of its Markdown target, and no document is reachable from itself over `supersedes` and `superseded_by`. Link the current owner instead of `docs/98.archive/`; that directory is unvalidated history, and a link into it is not checked. | `links-and-owners` | none |
| AUTHOR-R007 | Always | Keep a Requirement Package solution-independent. Put executable interface contracts and change-scoped Technical Approach and Acceptance Contract in the owning Spec package; put order, risks, verification, and rollback in its Plan and execution evidence in its Task records. A fresh Spec and Plan describe authorized, current intent when approved; Task execution and criterion acceptance remain separate from that approval. Keep each Task work item's state in the core Work Items table and its criterion links, result and evidence in the Lifecycle Traceability table, joined by Item. Its frontmatter status is the sole document status marker. A one-item Task has no Work Items table and authors its state only in frontmatter; a Task recorded under the earlier header keeps literal `frontmatter` in its row. A multi-row Task follows the row-derived status of [DOCLIFE-R009](document-lifecycle.md#requirements). Record each criterion's sole authored `pending`, `accepted`, `rejected`, or `not-required` disposition in the Task's Criterion Decisions table, with evidence, disposition rationale and current owner. Neither the execution row nor a factual check row repeats that verdict. A row's PASS alone is not completion: required work needs a completed execution state, concrete PASS evidence and an accepted criterion verdict, with no unresolved required adverse result. Keep failed or deferred observations in the Task's Results table; a later PASS resolves an earlier required result only when it names that evidence ID and matches the check, work unit and criterion. When `not-required` applies, and what does not waive a criterion, follows [DOCLIFE-R003](document-lifecycle.md#requirements). Keep ordered work, dependencies, Task links and verification intent in the Plan, without copied execution status. Attach factual checks in Task Evidence with exact inputs, results, locations, whether each check is required, and any earlier evidence it resolves; these facts do not replace execution rows, the sole criterion verdict or authorization. An observed `FAIL` needs concrete Command, Input and Location just as `PASS` does. Unrun `NOT_RUN` or unavailable `DEFER` may retain `Pending` in a location until real evidence exists, with the reason and next owner stated. | `document-lifecycle` | none |
| AUTHOR-R008 | Always | Promote durable cross-change decisions to an Architecture Decision and current system views to an Architecture Description. Do not create parallel design, test, release, or progress authority. This repository uses external release evidence: Task and Git own local work, while tags, hosted CI, and provider/live results remain external evidence. | Semantic review | none |
| AUTHOR-R009 | After content or path changes | Review the owning README after content or path changes and update stale navigation in the same logical change. A README is written for human readers: purpose, structure, usage and navigation. It names no AI agent audience and carries no agent instruction. An `AGENTS.md` is written for AI agents. The root `AGENTS.md` and `CLAUDE.md` stay the provider gateways; the root `CLAUDE.md` stays on `common/root-provider-shim` while the root `AGENTS.md` uses the AGENTS form like every folder file. The rules below govern folder `AGENTS.md` files. | `links-and-owners` | none |
| AUTHOR-R010 | Always | Do not add a router to a Spec package. `spec.md` owns the change contract, `plan.md` owns order and risk, and `01.tasks/` is the Task inventory; a package-level index only restates them and drifts from `01.tasks/`. | Semantic review | none |
| AUTHOR-R011 | Always | Keep a Stage 90 collection complete at all three of its levels. The registry routes each level and names its form; the reason they are distinct is that a collection outlives any one pack, a pack owns its own observation boundary and refresh trigger, and a member carries one dated observation or finding with its source. A collection with a missing level pushes one of those three jobs onto a document that does not own it. | `document-contract-registry` | none |
| AUTHOR-R012 | Always | Treat a retirement as retiring a document, not a location. A reviewed, tracked document may later occupy a retired path; never restore the retired bytes there. | `document-lifecycle` | none |
| AUTHOR-R013 | Always | Preserve accepted decisions and completed evidence. Use successors, the applicable lifecycle relationship and the Archived Lineage summary in the owning current document; recover removed bytes from Git history rather than rewriting history, leaving redirects, or keeping a second recovery ledger; a closed work residue ledger entry is recovered from Git history. Before a current document leaves its stage, follow the manual consumer, preservation, hold and authorization review in [document lifecycle](document-lifecycle.md#requirements). If Git-history-only disposition is selected, also prove exact Git recovery. Keep the decision and applicable recovery evidence in the existing Task and current owner; unresolved conditions defer only that disposition. | `document-lifecycle` | none |
| AUTHOR-R014 | Always | Run the checks selected by the affected paths and record evidence in the owning Task using [quality policy](../04.quality/quality.md). | `scripts/qa.py` | none |
| AUTHOR-R015 | Always | Governed Markdown uses the ordered common prefix "title", "version", "type", "status", "owner", and "updated"; later keys appear only when the selected profile declares them. A new document starts at version "0.1.0" and its first stable approval raises it to "1.0.0" when the document is still at major zero. Document Revision, Contract Version and Registry Schema Version each use the ASCII numeric triplet `X.Y.Z` from `scripts/semver_grammar.py`. Each component is zero or begins with an ASCII digit from 1 through 9. Prefixes, whitespace, prerelease identifiers and build metadata are invalid. Compare components numerically in order. Product tags follow [Git release ownership](git.md#release-ownership). External deployment labels, database migration numbers and artifact identities retain their own types. Historical Registry integers are read as `N.0.0` only in the history reader. Current readers accept the Registry schema MAJOR they implement. | `markdown-profiles` | none |
| AUTHOR-R016 | Always | Markdown templates use the double-braced UPPER_SNAKE_CASE value grammar, native templates use double-underscore UPPER_SNAKE_CASE markers, and author guidance uses the registered HTML comment form. The shared value markers are TITLE, OWNER, UPDATED, ARTIFACT_ID and PARENT_ID; parent_ids names exactly one direct structural owner rather than a duplicate spec_id. Authored documents contain none of those markers. The Registry's TemplateDefinition records `contract_id` and the numeric `contract_version` separately. Git and that contract identity and version record template history. The created document has its own "version". The Registry's `document_language` owns each document's language. Navigation, reference-pack, and operations profiles default to Korean. Policies under `.agents/governance/` use English. New prose in governed Markdown elsewhere under `.agents/` defaults to Korean, and existing English prose remains valid. Machine keys and required headings retain their registered grammar. Non-Markdown files under `.agents/`, and non-README files under `.claude/` and `.codex/`, use English only. READMEs follow the navigation profile. Other current documents, especially non-README Stage 01–03 authored documents, remain English, as do agent requirement sections. Template author prompts follow the registered language. Do not hand-edit generated current artifacts or create authored trees outside the taxonomy. | `markdown-profiles` | none |
| AUTHOR-R017 | Always | The Stage 99 Registry's optional `shared_contract` identifies the approved shared edition and this local adapter. Its pinned source revision and digest identify the reviewed bytes; `approval_ref` records a separate shared decision. A Registry stage value is a local declaration, not acceptance evidence by itself. Actual local adoption requires the owning Task's integration check, the owner's semantic review under the [quality policy](../04.quality/quality.md#semantic-review), and criterion decision. Shared adoption also requires application evidence from each repository. Keep this adapter's status, language, and native extensions explicit. A new shared edition requires an actual owner decision and adoption evidence; do not create a separate local WGOV core. | `document-contract-registry` | none |
| AUTHOR-R018 | Always | Approval and adoption are separate facts. An approved or adopted edition records past authority and does not freeze the contract; a later approved target supersedes it through a recorded change. Approval is never inferred from a role name, hash, signature or registry value; absent evidence stays unverified, and no new ledger is created for it; an unverified approval fact is not a work residue ledger entry. Partial adoption is never reported as full, and an approved compatible edition coexisting with a newer one is not a defect by itself. The target contract record names the contract ID, version, single authoring owner, approval reference with approver and date, scope, exceptions, effective point, migration, rollback and consumer edition. The registry carries `contract_id`, `version`, `stage` (`candidate`, `approved` or `adopted`), `owner`, `approval_ref`, `approved_by`, `approved_at`, `effective_from`, `extensions` and the optional `scope`, `migration`, `rollback` and `consumer_version`; an approved or adopted record needs the approval facts, and a fact no record states is `unverified` and is admitted only beside an `approval_ref`. | `document-contract-registry` | none |
| AUTHOR-R019 | Always | A regional extension may bind paths, commands, environments, native syntax, quality targets and deployment. Each extension states its condition, owner, verification, review point and removal criterion. An extension never weakens or removes a common required condition, and a path or edition difference alone is no permanent exception. Standardization never forces one language, folder layout, CLI or quality number on every product. | `document-contract-registry` | none |
| AUTHOR-R020 | Always | A derived or generated copy names its source and edition and changes only through that source; an edit made only in the copy is a defect. The Policy role, its forms and placement are owned by the [SDLC contract](sdlc.md#ownership-and-placement). | `agent-governance` (provider agent projections, provider baselines, skill links and the Codex rules digest changed alone); Semantic review for other copies | none |
| AUTHOR-R021 | Always | Use the Registry described in [Stage 99](../../99.templates/README.md) to resolve the document role, canonical template, section IDs and titles, table contracts, applicability, relationships, and language. Apply a local extension only under its registered condition and follow its owner, validation, review, and removal criteria. Use the registered retained form where its scope applies. Follow the [Stage 99 authoring guidance](../../99.templates/README.md#entry-points) when creating a document. | `markdown-profiles` | none |
| AUTHOR-R022 | Always | Joint edition decisions belong to the request owner `buenhyden`; current documentation, QA and operations owners review their scope. Verify an existing approved source when available; otherwise record that no prior joint approved edition was established and first establish one candidate with the same identity across adapters. Missing future commit, digest or approval fields never block authorized investigation, policy/consumer repair or independent local work. Record candidate preparation, final approval, local adoption and joint adoption separately in the current Task, and do not claim an unread adapter adopted an edition. Bind final approval to the reviewed edition's actual content, revision and digest only after its real decision, and do not create a competing normative core. | Semantic review | none |
| AUTHOR-R023 | Always | A rule ID and a policy code are permanent until a user-approved new baseline under the Q-07 contract. An ID is issued once, never renumbered and never reused. A retired rule keeps its row and never becomes `active` again; a restored rule takes a new ID, which the retired row may name as its successor. A registered code never changes and is never given to another policy, and the document lifecycle check refuses a missing ID, a retired row made active, a changed code and a shrunken `reserved_codes` list. | `document-lifecycle` | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| AUTHOR-R001 | required | active |
| AUTHOR-R002 | required | active |
| AUTHOR-R003 | required | active |
| AUTHOR-R004 | required | active |
| AUTHOR-R005 | required | active |
| AUTHOR-R006 | required | active |
| AUTHOR-R007 | required | active |
| AUTHOR-R008 | required | active |
| AUTHOR-R009 | required | active |
| AUTHOR-R010 | required | active |
| AUTHOR-R011 | required | active |
| AUTHOR-R012 | required | active |
| AUTHOR-R013 | required | active |
| AUTHOR-R014 | required | active |
| AUTHOR-R015 | required | active |
| AUTHOR-R016 | required | active |
| AUTHOR-R017 | required | active |
| AUTHOR-R018 | required | active |
| AUTHOR-R019 | required | active |
| AUTHOR-R020 | required | active |
| AUTHOR-R021 | required | active |
| AUTHOR-R022 | required | active |
| AUTHOR-R023 | required | active |

1. `AUTHOR-R009`
   - **README.md and AGENTS.md together** when a folder is the root of a work
     area that has its own agent responsibilities (a registry role works
     there) and rules an agent must follow that common policy and the parent
     `AGENTS.md` do not already state: forbidden live actions, ownership
     boundaries, required checks. The registry profile
     `common/folder-agents-guide` governs every such file and the root `AGENTS.md`; list the current
     set with `git ls-files '*/AGENTS.md'` rather than keeping a copy here. A
     folder `AGENTS.md` also carries the rules of subfolders that have none
     of their own, as `examples/azure/` does.
   - **README.md only** when the folder is navigation or a collection inside
     an area whose parent `AGENTS.md` already covers it (the collections
     inside a `docs/` stage, the unvalidated `docs/98.archive/`,
     `gitops/platform/`, `examples/aws/`, the `examples/azure/` subfolders), when it is a governance or provider
     surface whose gateway and provider notes are the agent instructions
     (`.agents/`, `.claude/`, `.codex/`), when its tracked files are fixed by
     a validator (`_workspace/`, `secrets/`), or when its agent rules would
     only repeat common policy.
   - An `AGENTS.md` always sits beside its folder's human router: `README.md`,
     or `repository-surface.md` in `.github/`, where GitHub renders
     `README.md` as the profile page. A README never points agents to rules;
     the folder's README may list `AGENTS.md` in its structure.
   - A folder `AGENTS.md` is English, has no frontmatter, and applies to its
     subtree. It states the folder's purpose for agents; names the
     responsibilities that work there with their common role and skills under
     `.agents/` and the matching `.claude/agents/`, `.claude/skills/`,
     `.claude/commands/` and `.codex/agents/` projections and provider notes;
     and lists only the rules and checks specific to that folder. It links
     common policy instead of copying it, and a child refers to its parent
     instead of repeating it.
   - Add or remove a folder `AGENTS.md` in the same change that creates or
     retires the responsibility, and update this list.

An Architecture Description explains requirement-linked quality scenarios,
including stimulus, environment, response, and measure; structural choices
and ADRs; and a context/container view that makes responsibilities and
relationships readable. In Stage 90, an Audit owns criteria, check scope,
observations, evidenced findings with severity, corrective owners, and
verification state. Research owns questions, methods, claims by source,
limitations, and recommendations. Data owns scope and provenance, production
method, field meanings and units, observed facts, and staleness bounds. The
Registry owns local headings and form, and templates provide a starting point;
each document's actual evidence and owner determine its facts, decisions, and
current authority.

#### Frontmatter order and versions

`AUTHOR-R015`

Assess compatibility against previously valid producers and consumers across
keys, sections, table columns, relationships, states, meaning, diagnostics and
outputs. Use MAJOR for an incompatible change, MINOR for a compatible addition
and PATCH for a correction that preserves the contract. Reset both lower
components after a MAJOR increase and reset PATCH after a MINOR increase.
Judge compatibility against the prior interface even when all consumers
change at once. The owning Task records the highest applicable level and its
reason. An unchanged contract retains its version. A stable shared edition
retains its approved source identity under the same contract ID and version.
Status changes, content changes and new observations carry separate evidence
under the [document lifecycle policy](document-lifecycle.md). The lifecycle
check detects downgrades and same-version changes to a released shared edition.
The staged check also verifies the lower-component reset for a single change.

Native Skill packages keep name and description at the top and
place that six-key document envelope inside metadata. Preserve native
invocation, tool and model controls; metadata does not grant execution authority.

#### Template markers and language

`AUTHOR-R016`

#### Shared contract edition

`AUTHOR-R017`

#### Approval and adoption

`AUTHOR-R018`

#### Regional extensions

`AUTHOR-R019`

#### Derived and generated copies

`AUTHOR-R020`

#### Registry forms

`AUTHOR-R021`

Fill applicable sections with concrete content for the role's reader. Omit an
optional section when its condition is absent. Where a required section permits
a justified omission, state the reason, the responsible owner, and the
condition for supplying the content. Resolve evidence pointers to an existing
location. A format check establishes structural conformance. Record operator
authority, live observations, and acceptance with their own evidence.

#### Joint edition decisions

`AUTHOR-R022`

#### Rule ID permanence

`AUTHOR-R023`

### Exceptions

Exception and escalation conditions are stated under Requirements.

#### Approval and Review

Approval and review conditions are stated under Requirements.

## Enforcement

### Mechanisms

Run strict registry, Markdown-profile, link/owner, and lifecycle checks when
their contracts are affected. A deletion or consolidation requires replacement
coverage and consumer disposition in the same logical change.

### Limits

The strict registry, Markdown-profile, link/owner and lifecycle checks run only when their contracts are affected. Native skill metadata does not grant execution authority, and a deletion or consolidation still requires replacement coverage and consumer disposition in the same logical change.

## Ownership

### Owner

Stage 99 README (`docs/99.templates/README.md`) is the human authoring guide.
Its registry (`docs/99.templates/registry.json`) alone owns exact paths,
profiles, IDs, sections, metadata, lifecycle, and relationships. This policy
owns agent procedure, not a second machine contract.

- [Document Lifecycle](document-lifecycle.md)
- [Work Lifecycle](../../../.agents/workflows/work-lifecycle.md)

#### Responsibilities

Responsibilities are stated under Owner and Requirements.

### Review Triggers

Change and adoption conditions are stated under Requirements.
