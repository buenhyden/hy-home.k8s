---
title: "Document Authoring Policy"
version: "3.20.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-13"
---

# Document Authoring Policy

## Purpose

### Objective

Select the document owner by purpose, author from its canonical template, and
close the change with traceable evidence.

### Authority

Stage 99 README (`docs/99.templates/README.md`) is the human authoring guide.
Its registry (`docs/99.templates/registry.json`) alone owns exact paths,
profiles, IDs, sections, metadata, lifecycle, and relationships. This policy
owns agent procedure, not a second machine contract.

- [Document Lifecycle](document-lifecycle.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)

## Scope

### Applies To

Use [SDLC flow](sdlc.md) to distinguish durable requirements, current
architecture, change-specific behavior, and operating knowledge. Stage numbers
express ownership, not a one-way waterfall.

- Stage 99 Author Guide (`docs/99.templates/README.md`)
- Archive Index (`docs/98.archive/README.md`)

### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

## Rules

### Requirements

1. Identify the owning stage and normalize the final repository-relative path.
2. Resolve exactly one registry profile and read its canonical template before
   creating or restructuring a document. No match or multiple matches is a
   stop condition.
3. Use the profile-owned initial status, metadata, sections, and relationships.
   Do not assume every profile starts at "draft". Router READMEs participate in
   the governed envelope with an "active" routing constant, but have neither
   artifact identity nor lifecycle binding. Stable reference pack anchors keep
   their reference identity and publication lifecycle even when named README.md.
4. Take the frontmatter key set from the selected profile (the key order is
   stated below), and each key's value grammar from the
   frontmatter schema (`docs/99.templates/contracts/frontmatter.schema.json`).
   The registry's `frontmatter_keys` owns each key's meaning, author,
   consumers and tests, and its `frontmatter_dialect` owns the YAML and JSON
   Schema dialect, so neither is restated here. Frontmatter is read as YAML 1.2
   through the one loader `scripts/frontmatter_yaml.py`, whose stated refusals
   that record carries.
   Every string, date, version, and identity scalar uses double quotes. A
   "title" never repeats the document's "artifact_id": identity is already a
   key, and a title that restates it carries no information.
5. Treat a key the profile omits as a key the document has no business
   declaring. `layer` names the numbered stage a document lives in, so common governance
   sits above that numbering and a Stage 99 form is not the document it
   produces; neither declares one. A profile that declares no `artifact_id`
   describes something the repository does not give a stable identity. Preserve
   an existing optional governance identity; do not mint one for normalization.
6. Replace prompts with concrete content, use complete stable IDs for
   traceability, and calculate links from the final target path. A file outside
   `docs/` links to current owners and stage or collection README navigation,
   never directly to an individual numbered-stage document, including historical
   records. Renaming a link to a plain path or artifact ID does not remove a
   current authority dependency: promote the needed rule to its current owner.
   The boundary normalizes relative/absolute references, Markdown references,
   HTML/wiki links, repository blob/raw URLs, encoding, case and separators.
   Machine reads are admitted only by the exact consumer, target and access-kind
   tuples in the link validator; they do not authorize rendered links. Route
   grammars stay in the Stage 99 registry. Links inside `docs/` retain their
   historical and current relationship contracts. Write each traceability
   relation once, in the document that cites its parent; never hand-write a
   back-link. Derive the reverse view on demand with
   `scripts/document-backlinks.py`. Supersession pairs (rule 13) stay
   reciprocal.
   Link the current owner instead of `docs/98.archive/`; that directory is
   unvalidated history, and a link into it is not checked.
7. Keep a Requirement Package solution-independent. Put executable interface
   contracts and change-scoped Technical Approach and Acceptance Contract in
   the owning Spec package; put order, risks, verification, and rollback in its
   Plan and execution evidence in its Task records. A fresh Spec and Plan
   describe authorized, current intent when approved; Task execution and
   criterion acceptance remain separate from that approval. Keep one Task
   Table with criterion links, row state, result and evidence. Its frontmatter status is
   the sole document status marker. For one row, author its state only in
   frontmatter and use literal `frontmatter` in the row. For a multi-row Task,
   author only row states and omit frontmatter `status`; the validators derive
   the summary from the Registry-bound rows on each read (see the document
   lifecycle policy), so no writer exists and no second human-maintained state is kept.
   Record each criterion's sole authored `pending`, `accepted`, `rejected`, or
   `not-required` disposition in the Task's Criterion Acceptance table, with
   evidence, disposition rationale and current owner. Neither the execution
   row nor a factual check row repeats that verdict. A row's PASS alone is not
   completion: required work needs a completed execution state, concrete PASS
   evidence and an accepted criterion verdict, with no unresolved required
   adverse result. Keep failed or deferred observations in Task Evidence; a
   later PASS resolves an earlier required result only when it names that
   evidence ID and matches the check, work unit and criterion.
   `not-required` is reserved for a cancelled Task whose same-package Spec is
   also cancelled with actual criterion-specific scope and authorization proof.
   Both cancellation dispositions name the exact criterion, and the Task's
   authorization reference points to that Spec decision.
   A successor-only handoff, active or completed Task, or QA
   `NOT_APPLICABLE` result does not waive a criterion.
   Keep ordered work, dependencies, Task links and verification intent in the
   Plan, without copied execution status. Attach factual checks in Task
   Evidence with exact inputs, results, locations, whether each check is
   required, and any earlier evidence it resolves; these facts do not replace
   execution rows, the sole criterion verdict or authorization.
   An observed `FAIL` needs concrete Check, Input and Location just as `PASS`
   does. Unrun `NOT_RUN` or unavailable `DEFER` may retain `Pending` in a
   location until real evidence exists, with the reason and next owner stated.
8. Promote durable cross-change decisions to an Architecture Decision and
   current system views to an Architecture Description. Do not create parallel
   design, test, release, or progress authority. This repository uses external
   release evidence: Task and Git own local work, while tags, hosted CI, and
   provider/live results remain external evidence.
9. Review the owning README after content or path changes and update stale
   navigation in the same logical change.
   A README is written for human readers: purpose, structure, usage and
   navigation. It names no AI agent audience and carries no agent
   instruction. An `AGENTS.md` is written for AI agents. The root `AGENTS.md`
   and `CLAUDE.md` stay the provider gateways; the root `CLAUDE.md` stays on
   `common/root-provider-shim` while the root `AGENTS.md` uses the AGENTS form
   like every folder file. The rules below govern folder `AGENTS.md` files.
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
10. Do not add a router to a Spec package. `spec.md` owns the change contract,
    `plan.md` owns order and risk, and `tasks/` is the Task inventory; a
    package-level index only restates them and drifts from `tasks/`.
11. Keep a Stage 90 collection complete at all three of its levels. The
    registry routes each level and names its form; the reason they are distinct
    is that a collection outlives any one pack, a pack owns its own observation
    boundary and refresh trigger, and a member carries one dated observation or
    finding with its source. A
    collection with a missing level pushes one of those three jobs onto a
    document that does not own it.
12. Treat a retirement as retiring a document, not a location. A reviewed,
    tracked document may later occupy a retired path; never restore the
    retired bytes there.
13. Preserve accepted decisions and completed evidence. Use successors,
    reciprocal lifecycle relationships and the Archived Lineage summary in the
    owning current document; recover removed bytes from Git history rather than
    rewriting history, leaving redirects, or keeping a second recovery ledger.
    Before a current document leaves its stage, follow the manual consumer,
    preservation, hold and authorization review in
    [document lifecycle](document-lifecycle.md#requirements). If
    Git-history-only disposition is selected, also prove exact Git recovery.
    Keep the decision and applicable recovery evidence in the existing Task
    and current owner;
    unresolved conditions defer only that disposition.
14. Run the checks selected by the affected paths and record evidence in the
    owning Task using [quality policy](quality.md).

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

Governed Markdown uses the ordered common prefix "title", "version",
"type", "status", "owner", and "updated"; later keys appear only when the
selected profile declares them. A new document starts at version "0.1.0" and
the first stable approval raises it to "1.0.0". Patch means a correction
without changed meaning, minor means compatible meaning or section growth, and
major means an incompatible role or contract change. Status and version are
independent. Native Skill packages keep name and description at the top and
place that six-key document envelope inside metadata. Preserve native
invocation, tool and model controls; metadata does not grant execution authority.

Markdown templates use the double-braced UPPER_SNAKE_CASE value grammar,
native templates use double-underscore UPPER_SNAKE_CASE markers, and author
guidance uses the registered HTML comment form. The shared value markers are
TITLE, OWNER, UPDATED, ARTIFACT_ID and PARENT_ID; parent_ids names exactly one
direct structural owner rather than a duplicate spec_id. Authored documents contain none
of those markers. Template history belongs to Registry contract version and
Git, not to the created document's "version".
The Registry's `document_language` owns each document's language. Navigation,
reference-pack, and operations profiles default to Korean. Policies under
`.agents/governance/` use English. New prose in governed Markdown elsewhere
under `.agents/` defaults to Korean, and existing English prose remains valid.
Machine keys and required headings retain their registered grammar.
Non-Markdown files under `.agents/`, and non-README files under `.claude/` and
`.codex/`, use English only. READMEs follow the navigation profile. Other
current documents, especially non-README Stage 01–03 authored documents,
remain English, as do agent requirement sections. Template author prompts
follow the registered language. Do not hand-edit generated current artifacts
or create authored trees outside the taxonomy.

The Stage 99 Registry's optional `shared_contract` identifies the approved
shared edition and this local adapter. Its pinned source revision and digest
identify the reviewed bytes; `approval_ref` records a separate shared
decision. A Registry stage value is a local declaration, not acceptance
evidence by itself. Actual local adoption requires the owning Task's
integration check, the owner's semantic review under the
[quality policy](quality.md#semantic-review), and criterion decision. Shared
adoption also requires application evidence from each repository. Keep this
adapter's status, language, and native extensions explicit. A new shared
edition requires an actual owner decision and adoption evidence; do not create
a separate local WGOV core.

Approval and adoption are separate facts. An approved or adopted edition
records past authority and does not freeze the contract; a later approved
target supersedes it through a recorded change. Approval is never inferred
from a role name, hash, signature or registry value; absent evidence stays
unverified, and no new ledger is created for it. Partial adoption is never
reported as full, and an approved compatible edition coexisting with a newer
one is not a defect by itself. The target contract record names the contract
ID, version, single authoring owner, approval reference with approver and
date, scope, exceptions, effective point, migration, rollback and consumer
edition. The registry carries `contract_id`, `version`, `stage` (`candidate`,
`approved` or `adopted`), `owner`, `approval_ref`, `approved_by`, `approved_at`,
`effective_from`, `extensions` and the optional `scope`, `migration`, `rollback`
and `consumer_version`; an approved or adopted record needs the approval facts,
and a fact no record states is `unverified` and is admitted only beside an
`approval_ref`.

A regional extension may bind paths, commands, environments, native syntax,
quality targets and deployment. Each extension states its condition, owner,
verification, review point and removal criterion. An extension
never weakens or removes a common required condition, and a path or edition
difference alone is no permanent exception. Standardization never forces one language,
folder layout, CLI or quality number on every product.

A derived or generated copy names its source and edition and changes only
through that source; an edit made only in the copy is a defect. The Policy
role, its forms and placement are owned by the
[SDLC contract](sdlc.md#ownership-and-placement).

Guide, Runbook, Incident, Postmortem, Policy, AGENTS, Skill, Root README, Stage README,
Service README, Workspace README and Reference Pack README use their registry forms. Guide keeps its classification, readers and
goal under Purpose and its Lifecycle Traceability table under Verification;
Runbook keeps its Lifecycle Traceability table under Validation; Incident keeps
its Lifecycle Traceability table under Evidence and Postmortem under Corrective
Actions; Root README keeps an optional Directory Index table under Directories;
Stage README, which the stage and collection READMEs use, keeps an optional
Index table under Current Items; Service README, which the implementation,
agent and provider, and runtime-governance READMEs use, keeps an optional
Commands table under Checks; AGENTS, which every `AGENTS.md` uses, keeps an
optional Tool Rules table under Local Obligations; Skill, which the common
workflows and every native `SKILL.md` use, keeps an optional Steps table under
Steps. Workspace README, which the seven `_workspace/` READMEs use, and
Reference Pack README, which the research, audit and data pack READMEs use with
the `Pack Contract` and `Pack Index` sections, are Stage 99 local roles under
W03-D09 and W03-D10, not COMMON-DOC-FORM-1 roles; each uses its own registry
form and keeps no table. Policy uses the selected
role's ordered sections. A
TemplateDefinition names each table's section, ordered columns, minimum rows and
row identity, and the validator checks column order, count and minimum rows. A
template whose role has no form keeps its H2 lists and records its tables under
the template's own headings, each named by its exact heading line.
Classifications, prerequisites, controls, observations and recovery stay native
submodules in their relevant roles. Fill sections with concrete content; a
heading, comment, placeholder or empty fence is no operating instruction.
An inapplicable item states why and who owns the remaining boundary. An empty
required section states its reason and the condition for filling it, never a
bare statement that nothing is stated, and a pointer line names a location that
exists. A format
check cannot authenticate a current operator, live service or approval.

Joint edition decisions belong to the request owner `buenhyden`; current
documentation, QA and operations owners review their scope. Verify an existing
approved source when available; otherwise record that no prior joint approved
edition was established and first establish one candidate with the same
identity across adapters. Missing future commit, digest or approval fields
never block authorized investigation, policy/consumer repair or independent
local work. Record candidate preparation, final approval, local adoption and
joint adoption separately in the current Task, and do not claim an unread
adapter adopted an edition. Bind final approval to the reviewed edition's actual
content, revision and digest only after its real decision, and do not create a
competing normative core.

### Enforcement

Run strict registry, Markdown-profile, link/owner, and lifecycle checks when
their contracts are affected. A deletion or consolidation requires replacement
coverage and consumer disposition in the same logical change.

## Exceptions

### Exception Conditions

Exception and escalation conditions are stated under Requirements.

### Approval and Review

Approval and review conditions are stated under Requirements.

## Ownership

### Responsibilities

Responsibilities are stated under Authority and Requirements.

### Change and Adoption

Change and adoption conditions are stated under Requirements.
