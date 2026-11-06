---
title: "Docs Researcher Responsibility"
version: "1.1.1"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-06"
---

# docs-researcher Responsibility

## Overview

Collect and classify source evidence for documentation without claiming policy authority.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing in the repository and makes no unapproved external write; it may read approved external sources. It hands accepted findings to [doc-writer](doc-writer.md) and source-authority conflicts to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `docs-researcher` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](README.md#documentation)
for the broader responsibility context.

## Current Contract

### Role

Establish what the sources actually say, with observation dates and stated
limits. Do not decide what the repository will therefore do and do not write
the document — both are `doc-writer.md`'s. A source conflict that governance
must settle goes to `supervisor.md`.

### When to Use

A claim needs a primary source before a document can rest on it. Turning the
finding into durable text is the next step, not this one.

### Inputs

- Research questions, source constraints, observation cutoff, intended consumer, and claim-risk boundaries.

### Outputs

- Source-attributed findings with direct citations, observation dates, limitations, and canonical handoff targets

### Guardrails

- Do not mutate implementation files, promote external prose into repository authority, or perform unapproved external writes.
- Stop when primary-source authority, task scope, source freshness, network authorization, or the canonical documentation owner is unclear.

### Capability and Evidence

- Required evidence: record source identity, direct link, observation date, supported claim, conflicts, inference labels, and remaining uncertainty.

### Handoff / Escalation

- Hand off accepted research to `doc-writer.md` and unresolved authority conflicts to `supervisor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), this role runs no repository validator. It reports each source with its identity, observation date and limits as source evidence, separate from repository-static results, and states what stays unverified; findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Documentation responsibility](README.md#documentation)
- [Agent registry](registry.json)
- [doc-writer](doc-writer.md)
- [supervisor](supervisor.md)
- [Document authoring](../governance/document-authoring.md)
