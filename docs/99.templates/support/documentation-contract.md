---
title: 'Template Documentation Contract'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-15
---

# Template Documentation Contract

## Overview

This document defines ownership boundaries for template forms, template support
contracts, Stage 00 governance, and authored documents. It prevents the same
rule from being duplicated across README files, template files, governance
rules, hooks, and validators.

## Purpose

The template system has separate surfaces:

| Surface | Canonical Owner | Responsibility |
| --- | --- | --- |
| Template forms | `docs/99.templates/templates/**` | Starter forms authors copy from. |
| Template support contracts | `docs/99.templates/support/**` | Template-specific routing, schema, governance, and cleanup rules. |
| Agent governance | `docs/00.agent-governance/**` | Agent-facing execution policy, stage routing policy, hooks, and protected-surface rules. |
| Authored documents | `docs/01.requirements` through `docs/05.operations`, `docs/90.references`, `docs/98.archive` | Repository facts, lifecycle records, and evidence. |
| GitHub-native control Markdown | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md` | GitHub-rendered repository control surfaces that remain frontmatter-free and mirror canonical owners. |
| Active control surfaces | GitHub-native Markdown, `.github/workflows/**`, validators, GitOps desired state, policy-as-code, and route manifests | Repository behavior and protection surfaces that route detail to their canonical governance, operations, workflow, script, or manifest owners. |
| Cloud example snapshot collection | Stage 90 Current reference pack | Durable dated provider snapshots; an approved lifecycle change is required to refresh them. |
| Workspace scratch staging | `_workspace/README.md` plus ignored `_workspace/**` scratch | Temporary non-secret repo-support staging; durable findings promote to canonical docs. |

## Owned Contract

### Contract Rules

- The machine-readable [Document Profile Registry](./document-profiles.json)
  owns exact document routes, frontmatter key sets and states, heading sets, and
  template paths. This support contract owns rationale and examples only; it
  must not become a second machine contract.
- The
  [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
  records the research basis for profile-family decisions without owning their
  machine values.
- README files are entrypoints and inventories. They should summarize where to
  find rules and route to canonical owners, not duplicate full contract bodies.
- README files route readers to lifecycle contract owners instead of carrying
  full governance bodies.
- Template forms must contain only the sections and minimal guidance needed to
  create an authored document of that type.
- Template support docs own reusable rules that apply across multiple template
  forms.
- Stage 00 governance owns agent execution policy and can reference support
  docs instead of copying template-specific details.
- Validators and hooks are enforcement surfaces. They must match the documented
  route and schema contracts.
- Authored documents must contain topic-specific content. They must not retain
  template instructions, placeholders, or copied support-rule prose that is not
  specific to the document.
- Authored SDLC documents with a registry body contract are checked in
  production while their status is `draft` or `active`. Canonical forms retain
  the same body contract for source parity and are always form-validated;
  completed execution evidence and accepted decisions remain immutable history
  outside this current-consumer enforcement window.
- GitHub-native control Markdown must not be promoted into stage documents by
  adding frontmatter. Keep those files frontmatter-free and route durable
  policy to the owning governance, operations, script, or workflow surface.
- Active control surfaces may be summarized in README or GitHub-native
  Markdown, but their detailed rules belong to the owning support,
  governance, operations, workflow, validator, GitOps, policy-as-code, or route
  manifest surface.
- Active-surface duplicate rule: stages 01 through 04 must not keep multiple
  active documents that own the same role, purpose, and feature lineage.

### Lifecycle Route Summary

The [Document Profile Registry](./document-profiles.json) is the canonical
owner for exact lifecycle, README, exception, and snapshot routes and their
template mappings. At the support layer, the durable rationale is that
requirements and specifications use numbered lineage, plans and tasks remain
dated execution evidence, cloud knowledge is preserved as a dated Stage 90
snapshot, and README files remain navigation surfaces rather than governance
bodies.

The registry profiles own exact lifecycle states and archive metadata keys.
[SDLC Governance](./sdlc-governance.md) owns lifecycle rationale, numbering,
handoff semantics, and active-surface rules; [Frontmatter
Schema](./frontmatter-schema.md) explains metadata rationale without copying
the registry values.

### SDLC and Common Documentation Split

SDLC documentation follows the delivery lifecycle from requirement through
operations. Common documentation supports repository navigation, durable
reference, archive, memory, and progress recording.

| Contract Family | Support Owner | Template Family |
| --- | --- | --- |
| SDLC documentation | [SDLC Governance](./sdlc-governance.md) | PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, API/Data/Test/Agent helper forms. |
| Common documentation | [Common Documentation Governance](./common-documentation-governance.md) | README, Reference, Archive Tombstone, Memory, Progress. |
| Frontmatter and profile schema | [Frontmatter Schema](./frontmatter-schema.md) | Applies to Markdown template families and explicitly excludes native machine-readable contracts. |
| Routing and path selection | [Template Routing](./template-routing.md) | Explains how one registry profile selects one template form. |
| Legacy cleanup | [Legacy Cleanup Rules](./legacy-cleanup-rules.md) | Removes old keys, sections, values, and routes from active contracts. |

### Protected Surface Rules

- Template migration may change `docs/99.templates/**`, Stage 00 routing docs,
  `docs/00.agent-governance/hooks/k8s-pre-edit.sh`, and
  `scripts/validate-repo-quality-gates.sh` when the change is documented and
  validated.
- Do not mutate live runtime resources as part of template migration.
- Do not inspect secret values.
- Do not push or publish without explicit approval.

## Authoring Rules

1. Classify the target path with the [Document Profile
   Registry](./document-profiles.json), then use the one canonical form routed
   by [Template Routing](./template-routing.md). Do not infer a form from a
   neighboring filename.
2. Keep every required second-level section and replace author comments,
   prompts, and placeholders with topic-specific content. A required section
   with only blank lines or author-only HTML comments is incomplete in an
   authored document; canonical template forms may retain authoring prompts.
3. Use only the selected profile's allowed headings and frontmatter keys in
   their declared order. The selected profile also owns the exact relationship
   heading for every SDLC, helper-Spec, operations, common, README, reference,
   support, archive, and governance document. Do not infer or override that
   literal from a document-family label.
4. Recalculate relative links from the authored target location, update the
   owning folder index when its inventory or description changes, and route
   shared policy back to its canonical support or Stage 00 owner.
5. Report the selected profile, canonical form, and repository-static
   validation evidence at handoff. Keep native-runtime, remote, and live-state
   evidence explicitly separate from repository-static results.

## Validation Contract

For an enforced authored consumer, the matched registry profile supplies the
exact lifecycle table shape, identifier columns, allowed source and target
profile families, reciprocal-evidence rule, and explicit-exclusion capability.
An exclusion is evidence only when it uses the validator's reviewable `N/A —`
form; it is not permission to omit a required table or leave a cell empty.
Templates must remain contract-equal to their authored source profile without
becoming a second inventory owner.

The minimum validation for support contract changes is:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
```

Route-breaking changes must also run focused legacy and path searches defined
in [Template Routing](./template-routing.md) and
[Legacy Cleanup Rules](./legacy-cleanup-rules.md).

## Related Documents

- [Templates README](../README.md)
- [Template Support README](./README.md)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Template Routing](./template-routing.md)
- [Legacy Cleanup Rules](./legacy-cleanup-rules.md)
- [Document Profile Registry](./document-profiles.json)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
