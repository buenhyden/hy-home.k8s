---
title: 'Document Authoring Policy'
type: governance/reference
status: active
owner: platform
updated: 2026-08-13
---

# Document Authoring Policy

## Overview

This is the single agent-facing policy for selecting a document stage,
authoring at the right time, applying the repository language boundary, and
closing document work with deterministic evidence. It replaces the former
stage-routing, documentation-protocol, authoring-matrix, and stage-checklist
owners without becoming a second machine registry.

Agents classify the final repository path through the Document Profile
Registry, read the matching form before authoring, keep shared rationale in
Stage 99, and place topic-specific truth in its owning stage. The numeric Stage
04 slot is deliberately unused; Spec, Plan, and Task are siblings in one Stage
03 work unit.

## Authority Boundary

This policy owns agent execution decisions: stage selection, authoring timing,
language, Template-First procedure, safety, readiness and completion checks,
and validation handoff. It does not own exact routes, profile IDs,
frontmatter keys or values, heading sets, relationship shapes, canonical form
paths, lifecycle domains, or registered exceptions. Those machine values come
only from the [Document Profile Registry](../../99.templates/registry.json)
and its schema.

[Document Contract](../../99.templates/README.md) explains
form, body, metadata, and exact-one-profile rationale. [Document
Lifecycle](../policies/document-lifecycle.md) explains
promotion, supersession, retention, archive, date exceptions, and legacy
disposition. README files are navigation and inventory only.

### Safety and protected boundaries

- Keep repository gateways thin and route durable detail here or to the named
  canonical owner.
- Do not mutate live clusters, providers, remote state, credentials, or secret
  values as part of document authoring.
- Do not infer provider discovery, hosted CI, or runtime enforcement from a
  repository-static file or PASS result.
- Do not edit generated current output by hand; use its generator contract.
- Do not rewrite immutable Stage 98 payloads or completed/accepted evidence to
  manufacture compliance with a newer form.
- Protected-surface changes require the approval and evidence boundary named
  by the owning Task and governance contract.

### Prohibited authored trees

Do not create parallel or legacy document trees such as `docs/superpowers/**`,
`docs/api/**`, `docs/01.prd/**`, `docs/02.ard/**`, `docs/03.adr/**`,
`docs/04.specs/**`, `docs/05.plans/**`, `docs/06.tasks/**`,
`docs/07.guides/**`, `docs/08.operations/**`, `docs/09.runbooks/**`,
`docs/10.incidents/**`, or an ad hoc top-level Plan, Spec, reference,
postmortem, or learning tree. Reroute a tool or skill suggestion to the
canonical stage instead of creating the suggested parallel path.

The retired `examples/{aws,azure}/docs/**` trees likewise have no authored
route. Durable provider snapshot material belongs to the governed Stage 90
collection; executable examples stay at their existing executable boundary.

## Governance Context

### Stage selection and timing

| Stage or collection | Purpose and timing | Primary authoring check |
| --- | --- | --- |
| `00.agent-governance` | Agent policy and execution control, before work or when governance changes | JIT order, English policy, memory coupling, and checklist consistency |
| `01.requirements` | Product, optional system/software, and optional interface requirements, before implementation | Testable problem, scope, acceptance, interfaces, and success measures |
| `02.architecture/descriptions` | Architecture Description after the requirement baseline | Stakeholder concerns, boundaries, views, allocations, data flow, and quality attributes |
| `02.architecture/decisions` | Architecture Decision Record when a durable choice is made | Context, alternatives, rationale, consequences, and supersession |
| `03.specs` | Technical contract before implementation, with sibling Plan and Task when needed | Contracts, verification design, order, risk, rollback, status, and evidence |
| `05.operations/guides` | Stable user or operator guidance after feature stabilization | Audience, prerequisites, reproducible steps, and linked owners |
| `05.operations/policies` | Reusable operational control before release or policy change | Control, retention, promotion, approval, and evidence criteria |
| `05.operations/runbooks` | Ordered operational procedure when execution is standardized | Executable steps, verification, rollback, recovery, and escalation |
| `05.operations/incidents` | Real incident facts and post-incident learning | Timeline, impact, evidence, mitigation, cause, and prevention |
| `90.references` | Slow-moving, reusable, factual or dated observation material | Authority, sources, review/freshness, and no duplicate active contract |
| `98.archive` | Immutable terminal history created through the approved archive mechanism | Exact payload/provenance, index membership, recovery, and current replacement |
| `99.templates` | Forms, support rationale, registry, and schema before authoring changes | Registry/form parity and no copied machine inventory in prose |

Stage numbers express responsibility and navigation, not a one-way waterfall.
Operations and incidents may produce new requirements, decisions, Specs,
Plans, or Tasks when evidence changes an upstream contract.

### Language boundary

- Stage 00 governance, provider adapters, hook contracts, prompt/tool
  contracts, technical Specs, Plans, Tasks, and explicit AI-agent sections are
  English-first.
- Human-facing repository and folder READMEs remain Korean.
- Human-facing requirements, operations, and reference explanation may use
  Korean; machine contracts, authority/source/freshness sections, and
  AI-agent execution instructions remain English-first.
- A mixed-audience document keeps reader context in Korean and execution
  requirements in English. Language choice never changes the selected
  profile or evidence standard.

### Selection rules

- Feature-bound implementation truth belongs to its Stage 03 work unit.
- Long-lived reusable knowledge belongs to Stage 90.
- Agent execution policy belongs to Stage 00.
- A guide explains stable use; a policy defines reusable control; a runbook is
  executable in order. Do not duplicate one operating rule across them.
- Architecture Description records current structure, views, allocation,
  quality attributes, requirement disposition, stakeholder concerns,
  boundaries, and data flow. ADR records a choice, alternatives, rationale,
  consequences, and supersession.
- GitHub-native Markdown remains frontmatter-free and routes durable policy to
  canonical owners rather than becoming a stage document.
- `_workspace/**` is ignored non-secret scratch. Promote durable findings to a
  canonical stage before closure.

### Legacy path interpretation

Legacy product, architecture-requirement, decision, specification, Plan,
Task, guide, policy, runbook, and incident paths are historical input only.
Their current destinations are selected from the registry: requirements in
Stage 01, AD/ADR in Stage 02, Spec/Plan/Task siblings in Stage 03, operations
in Stage 05, durable references in Stage 90, and immutable history in Stage
98. Never infer a live target from the old numeric folder name.

## Current Contract

### Template-First authoring procedure

1. Start from repository evidence and choose the owning stage by intent and
   timing.
2. Normalize the final repository-relative POSIX target path.
3. Classify that path through the registry. Zero or multiple matches is a
   stop condition; declaration order and neighboring files are not fallback.
4. Read the matched canonical form under `docs/99.templates/templates/**`
   before creating or restructuring the document.
5. For a new authored document, use `status: draft`, the required metadata
   order, every required heading, and the profile-owned relationship section.
6. Replace prompts and placeholders with topic-specific content, recalculate
   relative links from the final target, and keep optional missing paths as
   code literals rather than broken links.
7. Review the owning folder README for every add, move, removal, or content
   change; update it in the same logical change when its summary, tree, or
   index is stale.
8. Update the canonical progress ledger for repository-changing work.
9. Run focused, affected, staged, test, all-files, formatter, rerun, and diff
   checks in the order owned by the quality standard.
10. Handoff the selected profile/form, changed paths, result lanes,
    limitations, rollback, residual risk, and next owner.

### Lifecycle pre-edit checks

- Resolve the lifecycle domain and evidence contract from the selected
  profile; prose does not define a second transition table.
- Preserve accepted decisions and done execution evidence. A changed decision
  uses a successor ADR; new execution uses a new or active sibling Plan/Task.
- Do not keep two active documents with the same role, purpose, and feature
  lineage.
- Plan requires its sibling Spec; Task requires sibling Spec and Plan.
- Active documents may reach historical content only through the Stage 98
  collection index. Archive index and migration/control records own direct
  record provenance links.
- A stale current owner moves only after replacement coverage, reviewed
  disposition, exact payload/provenance, index parity, recovery, and secret
  classification pass atomically.

### Stage readiness and completion checklist

- Governance: JIT loading, language, current routes, validation, and memory
  coupling are consistent.
- Requirements: problem, value, interfaces, acceptance, scope, and downstream
  lineage are explicit.
- Architecture: concerns, boundaries, views, quality attributes, decisions,
  consequences, and downstream traceability are explicit.
- Spec work unit: contracts and verification are complete; Plan covers phases,
  risk, gates, rollback; Task records status, protected boundaries, commands,
  evidence classes, and handoff.
- Operations: guides are reproducible, policies state controls, runbooks state
  ordered verification/recovery, and incidents preserve facts and learning.
- Reference: material is factual, durable, sourced, freshness-bounded, and
  does not duplicate an active owner.
- Archive: payload, digest, source commit/blob, stable identity, index,
  replacement, and dual recovery are exact.
- Templates: prose, registry, schema, forms, consumers, and negative fixtures
  agree without parallel authority.

### Named skill routing

- Feature-specific memory design belongs in a Stage 03 `agent-design.md`;
  reusable memory-system knowledge belongs in Stage 90 data references.
- Gateway-refactor skills keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` thin;
  detailed rules remain in Stage 00 or shared skill owners.
- Provider-specific runtime guidance belongs to its provider baseline or note,
  never to a parallel authored docs tree.

### Drift garbage collection

Treat recurring code, document, and structure drift as a harness defect. Fix
the smallest durable rule, prompt/skill, hook, validator, template, README, or
memory surface that would prevent recurrence. Active stale contracts must be
updated, consolidated, or archived; debug, backup, token-cache, auth, shell
history, and secret-bearing residue cannot remain tracked.

## Validation and Refresh

Run these repository-static owners after authoring-policy, route, lifecycle,
or authority changes:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
```

Validation is incomplete until the affected and exact staged lanes, plain
pre-commit, relevant tests, all-files pre-commit, formatter review, rerun
decision, and both diff checks are recorded. Repository-static PASS does not
prove CI, provider-runtime, remote, credential-bearing, or live behavior.

## Related Documents

- [Document Profile Registry](../../99.templates/registry.json)
- [Document Contract](../../99.templates/README.md)
- [Document Lifecycle](../policies/document-lifecycle.md)
- [Agent Quality Standards](quality-standards.md)
- [Preflight Checklist](preflight-checklist.md)
- [Postflight Checklist](postflight-checklist.md)
- [Templates README](../../99.templates/README.md)
