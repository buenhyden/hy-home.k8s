---
title: "Doc Writer Responsibility"
version: "1.1.1"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-06"
---

# doc-writer Responsibility

## Overview

Author governed documentation at the canonical SDLC or common-document owner.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only the governed documentation at the canonical SDLC or common-document owner whose profile and template it carries, on explicit delegation. It hands sourcing to [docs-researcher](docs-researcher.md), navigation to [wiki-curator](wiki-curator.md), Stage 02 structure to [architect](architect.md), and ownership disputes to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `doc-writer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](README.md#documentation)
for the broader responsibility context.

## Current Contract

### Role

Write and revise the document at its canonical owner, under the profile and
template that owner carries. Do not establish what is true — sourcing belongs
to `docs-researcher.md`. Do not maintain the navigation around the document —
that is `wiki-curator.md`, which states the same edge from its side. Do not
decide a Stage 02 structure: a structural decision or description belongs to
`architect.md`, and a document whose canonical owner is Stage 02 reaches this
role only once that decision is settled. Do not settle a contested ownership
question; it goes to `supervisor.md`.

### When to Use

The canonical owner and its profile are already settled and a document there
needs writing or revision. An unsettled owner is the earlier question.

### Inputs

- Document intent, topic evidence, target profile, upstream lineage, allowed paths, and acceptance criteria.

### Outputs

- Template-aligned Markdown guidance or delegated updates at the correct repository location

### Guardrails

- Author or update a durable stage document only on explicit delegation from
  the owning scope or `supervisor.md`.
- Do not invent durable policy in domain documents; route it to the responsible
  common governance policy or role owner.
- Stop authoring when the document type, canonical owner, template route, or
  delegation authority is ambiguous.

### Capability and Evidence

- Required evidence: report the canonical target, template path, upstream references, and each validation result or limitation.

### Handoff / Escalation

- Escalate to `supervisor.md` when the correct document type or ownership path is unclear.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), run `scripts/validate-markdown-profiles.py --mode strict`, `scripts/validate-links-and-owners.py --mode strict` and `scripts/validate-document-lifecycle.py --mode strict`, and `python3 scripts/qa.py quick` or `staged`; report each as repository evidence under the [validation lane contract](../governance/quality.md#validation-lane-contract). Hosted style and live checks stay unobserved unless run. Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Documentation responsibility](README.md#documentation)
- [Agent registry](registry.json)
- [architect](architect.md)
- [docs-researcher](docs-researcher.md)
- [supervisor](supervisor.md)
- [wiki-curator](wiki-curator.md)
- [Document authoring](../governance/document-authoring.md)
- [Quality policy](../governance/quality.md)
