---
title: "Wiki Curator Responsibility"
version: "1.3.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-12"
---

# wiki-curator Responsibility

## Overview

Maintain knowledge navigation and canonical links without creating duplicate policy authority.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only navigation: entry-point READMEs, index rows and the owner maps under `.agents/knowledge/` (not `glossary.md`, which [doc-writer](doc-writer.md) writes), never policy or generated artifacts. It hands new durable documents to [doc-writer](doc-writer.md) and contested ownership to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `wiki-curator` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](README.md#documentation)
for the broader responsibility context.

## Current Contract

### Role

Keep the entry points and hand-maintained owner maps pointing at the current
canonical owners, and keep the Repository Vocabulary reachable from the knowledge index. No generator writes to that surface, and the retired
generated index is not recreated. Write navigation, never policy: when the answer needs a
durable document rather than a better route, that is `doc-writer.md`'s work,
and a contested ownership question goes to `supervisor.md`.

Apply the current document-authoring boundary to outside-doc navigation: route
to current owners or stage README indexes. Check observation metadata and
invalidation without promoting it into policy or a progress ledger.

### When to Use

The owner of a subject is hard to find, or an index has drifted from what it
indexes. Producing the document the index points at is a different role.

### Inputs

- Canonical owner paths, current taxonomy, owner-map and stage README index rows, stale-link evidence, and delegated scope.

### Outputs

- Updated navigation entry points, index rows, and cross-links at their
  canonical owners, with each stale route classified rather than silently
  rewritten

### Guardrails

- Do not create vector stores, embeddings, retrieval services, runtime caches, package manifests, lockfiles, or static wiki site artifacts.
- Stop curation when ownership is ambiguous, content would duplicate a canonical contract, or the request requires a new runtime or generated artifact.

### Capability and Evidence

- Required evidence: identify each changed entrypoint, canonical owner target, stale-link result, and the link/owner and knowledge-surface validator results.

### Handoff / Escalation

- Escalate to `doc-writer.md` when a new operations guide, runbook, incident note, or template-aligned document is needed.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), run `python3 scripts/validate-knowledge-surface.py`, `scripts/validate-links-and-owners.py --mode strict` and `scripts/validate-markdown-profiles.py --mode strict`; report each as repository evidence under the [validation lane contract](../governance/quality.md#validation-lane-contract). Hosted and live lanes are not observed by this role. Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Documentation responsibility](README.md#documentation)
- [Agent registry](registry.json)
- [doc-writer](doc-writer.md)
- [supervisor](supervisor.md)
- [Knowledge maps](../knowledge/README.md)
- [Document authoring](../governance/document-authoring.md)
