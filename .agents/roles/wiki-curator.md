---
title: "Wiki Curator Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-09-05"
---

# wiki-curator Responsibility

## Overview

Maintain knowledge navigation and canonical links without creating duplicate policy authority.

## Authority Boundary

Follow [agent execution](../governance/agent-execution.md) and
[approval and safety](../governance/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `wiki-curator` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](documentation.md)
for the broader responsibility context.

## Current Contract

### Role

Curate the repo-local LLM Wiki Markdown entrypoints so agents and humans can find canonical owners without duplicating policy, procedure, or runtime contracts.

### When to Use

Maintain repository-local discovery entrypoints and generated owner maps without duplicating canonical policy.

### Inputs

- Canonical owner paths, current taxonomy, generated-map contract, stale-link evidence, and delegated scope.

### Outputs

- Updated LLM Wiki Markdown entrypoints and generated index files

### Guardrails

- Do not create vector stores, embeddings, retrieval services, runtime caches, package manifests, lockfiles, or static wiki site artifacts.
- Stop curation when ownership is ambiguous, content would duplicate a canonical contract, or the request requires a new runtime or generated artifact.

### Capability and Evidence

- Required evidence: identify each changed entrypoint, canonical owner target, stale-link result, and generated-index validation outcome.

### Handoff / Escalation

- Escalate to `doc-writer.md` when a new operations guide, runbook, incident note, or template-aligned document is needed.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../workflows/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../governance/quality.md)
