---
title: 'Template Documentation Contract'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-04
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

## Contract Rules

- README files are entrypoints and inventories. They should summarize where to
  find rules and route to canonical owners, not duplicate full contract bodies.
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
- GitHub-native control Markdown must not be promoted into stage documents by
  adding frontmatter. Keep those files frontmatter-free and route durable
  policy to the owning governance, operations, script, or workflow surface.
- Active control surfaces may be summarized in README or GitHub-native
  Markdown, but their detailed rules belong to the owning support,
  governance, operations, workflow, validator, GitOps, policy-as-code, or route
  manifest surface.

## SDLC and Common Documentation Split

SDLC documentation follows the delivery lifecycle from requirement through
operations. Common documentation supports repository navigation, durable
reference, archive, memory, and progress recording.

| Contract Family | Support Owner | Template Family |
| --- | --- | --- |
| SDLC documentation | [SDLC Governance](./sdlc-governance.md) | PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, API/Data/Test/Agent helper forms. |
| Common documentation | [Common Documentation Governance](./common-documentation-governance.md) | README, Reference, Archive Tombstone, Memory, Progress. |
| Frontmatter and profile schema | [Frontmatter Schema](./frontmatter-schema.md) | Applies to Markdown template families and explicitly excludes native machine-readable contracts. |
| Routing and path mapping | [Template Routing](./template-routing.md) | Maps authored target patterns to one template form. |
| Legacy cleanup | [Legacy Cleanup Rules](./legacy-cleanup-rules.md) | Removes old keys, sections, values, and routes from active contracts. |

## Protected Surface Rules

- Template migration may change `docs/99.templates/**`, Stage 00 routing docs,
  `docs/00.agent-governance/hooks/k8s-pre-edit.sh`, and
  `scripts/validate-repo-quality-gates.sh` when the change is documented and
  validated.
- Do not mutate live runtime resources as part of template migration.
- Do not inspect secret values.
- Do not push or publish without explicit approval.

## Validation Contract

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
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
