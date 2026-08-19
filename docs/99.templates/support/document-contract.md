---
title: 'Document Contract Support'
type: governance/template-support
status: active
owner: platform
updated: 2026-08-13
---

# Document Contract Support

## Overview

This support contract explains how one repository path selects one document
profile and form, how body and frontmatter shape remain aligned, and where
template, governance, authored-content, and enforcement authority stops. It
consolidates the former documentation-contract, routing, and frontmatter
rationale without copying the machine registry.

## Purpose

Authors need one repeatable selection procedure, while validators need one
machine source of routes, values, headings, forms, relationships, and
exceptions. Separating those concerns prevents a README, template comment,
Stage 00 policy, hook, or validator from becoming a second profile inventory.

The contract also keeps GitHub-native control Markdown, native OpenAPI,
GraphQL and protobuf forms, generated output, scratch space, and immutable
archive payloads within their declared format boundaries.

## Owned Contract

### Authority surfaces

| Surface | Unique responsibility |
| --- | --- |
| `document-profiles.json` and schema | Sole machine owner of exact routes, profile identities, metadata keys and states, heading sets, body/relationship contracts, lifecycle values, forms, and exceptions |
| `docs/99.templates/templates/**` | Minimal starter forms copied or rendered for an authored target |
| This support contract | Exact-One-Profile selection, form/body/frontmatter rationale, and protected change boundary |
| [Document Lifecycle](./document-lifecycle.md) | Promotion, supersession, retention, archive, date exception, and legacy-disposition rationale |
| [Document Authoring](../../00.agent-governance/rules/document-authoring.md) | Agent timing, stage choice, language, safety, checklist, and validation procedure |
| Authored documents | Topic-specific requirements, architecture, decisions, contracts, execution evidence, operations, and references |
| Validators and hooks | Enforcement that must agree with the registry and canonical forms |

README files are frontmatter-free navigation and inventory views. They may
summarize control boundaries and link owners but do not own detailed rules.
GitHub-native Markdown is an active control surface rendered by GitHub, not a
structural stage document; durable policy routes to its Stage 00, Stage 05,
workflow, or script owner.

### Exact-One-Profile selection

1. Normalize the final repository-relative POSIX path without traversing
   ignored scratch or resolving a provider view into another tracked path.
2. Evaluate every exact and anchored-regex route in the registry.
3. Stop on zero or multiple matches. Declaration order, a neighboring file,
   filename resemblance, or a README summary is never precedence.
4. Use the selected profile's form, frontmatter, headings, lifecycle, body,
   relationship, and admission contract.
5. Recalculate links from the authored target and validate the authored
   output, not merely the copied form.

An authored, native, or append-entry profile owns its canonical form. A
template-mode profile classifies the physical starter and inherits the source
contract; it is not a second document-family owner.

### Form and body contract

- A form contains the required sections and minimal author prompts needed to
  create that document type.
- Authored content replaces prompts, placeholders, and copied instructions
  with topic-specific evidence.
- Literal required H2 headings and the profile-owned relationship section are
  contract surface. Placeholder or explicitly optional headings remain
  guidance.
- A required section containing only blanks or author-only comments is
  incomplete in authored content; the canonical form may retain prompts.
- Production body enforcement applies to current authored consumers selected
  by the registry. Completed execution and accepted decisions preserve their
  historical evidence rather than receiving retroactive content.
- Templates and current authored sources remain semantically aligned without
  turning examples into another inventory.

### Frontmatter rationale

Frontmatter carries document identity and lifecycle metadata; it does not
duplicate headings, summaries, route tables, or governance prose. Exact key
sets, order, values, and requiredness come from the registry.

- `title` is human-readable identity; `type` is the namespaced profile role.
- `status` is selected from the profile lifecycle domain and promoted only
  with the owning evidence.
- Repository-authored documents use canonical owner `platform`.
- `updated` is an ISO calendar date and is not path identity.
- Path-derived `artifact_id`, stable group keys, and archive provenance appear
  only where the selected profile admits them.
- README and GitHub-native control Markdown remain frontmatter-free.
- `_workspace/README.md` remains a frontmatter-free scratch entrypoint; ignored
  scratch is not authored documentation.
- The progress form is an appendable ledger entry, not whole-file
  frontmatter.
- OpenAPI, GraphQL, and protobuf remain native machine-readable formats.
- Archive records use their registry-owned traceability extension; embedded
  payload metadata is historical content, not another current outer identity.

### Protected change boundary

A route or shape change updates the registry and schema, owning form, focused
fixtures, affected consumers, Stage 00 procedure, support rationale, README
navigation, and validators in one reviewable unit. It does not authorize live
resource mutation, secret inspection, remote publication, accepted-evidence
rewrite, or immutable archive payload change.

Generated output remains generator-owned. Cloud snapshots remain lifecycle-
approved Stage 90 evidence. Workspace scratch remains ignored and non-secret.
Native contracts must not gain Markdown frontmatter through a broad template
rewrite.

## Authoring Rules

1. Select the final target through the registry before reading or copying a
   form.
2. Read the selected form and keep every required heading, relationship
   section, and metadata field in its declared order.
3. Start new authored content at the profile's permitted draft state and do
   not self-promote it.
4. Replace prompts and placeholders; keep optional missing paths as code
   literals and calculate real relative links from the final target.
5. Keep shared policy in this support layer or Stage 00, and topic-specific
   content in its owning authored document.
6. Review the folder README after any add, move, removal, or content change;
   update it only where its summary, tree, or index became stale.
7. Preserve generated, native, GitHub-rendered, historical, and scratch
   surfaces according to their selected exception rather than forcing a
   Markdown profile onto them.
8. Record the selected profile, form, repository-static evidence, limitations,
   and next owner in the handoff.

### Link and relationship rules

- A real Markdown link inside a template resolves from the template location.
- Target-relative or optional examples are code literals or fenced snippets
  until an authored target exists.
- Authored relationships use the literal selected by the profile and the
  permitted source/target classes. A reasoned `N/A —` is valid only where the
  profile explicitly allows exclusions.
- Current documents reach archive history through the Stage 98 collection
  index; direct record links are limited to archive index, migration, and
  provenance owners.

## Validation Contract

The registry and form set must prove:

- every governed physical path matches exactly one profile;
- every form-owning profile has one existing form and every physical form has
  one owner;
- source/template metadata, headings, relationships, body contract, and
  native-format boundaries agree;
- current authored content contains no unsupported keys, states, headings,
  copied prompts, or unowned routes;
- README and GitHub-native controls remain frontmatter-free;
- generated and archive payload boundaries are not silently normalized; and
- registry, schema, support prose, Stage 00 policy, fixtures, hooks, and
  validators change atomically when their contract changes.

Run:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
```

Passing repository-static validation does not establish provider discovery,
hosted CI, remote execution, secret access, or live-cluster correctness.

## Related Documents

- [Document Profile Registry](./document-profiles.json)
- [Document Registry Form Schema](../contracts/registry-form.schema.json)
- [Document Lifecycle](./document-lifecycle.md)
- [Document Authoring](../../00.agent-governance/rules/document-authoring.md)
- [Templates README](../README.md)
- [Template Support Index](./README.md)
- [Spec-Driven SDLC and Document Contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
