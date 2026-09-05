---
title: "Common Agents Authority and Native Skill Routing"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-09-06"
layer: "architecture"
artifact_id: "ADR-0035"
---

# ADR-0035: Common Agents Authority and Native Skill Routing

## Overview

The latest user request authorizes moving the common authority to `.agents/`
and retiring the former documentation governance root. That direct instruction
authorizes this bounded local implementation. The new ADR remains `proposed`: the
repository requires an initial proposed record before a later accepted-state
transition, and this task does not authorize commits. No lifecycle transition,
review signature or runtime result is invented. The proposed durable decision
narrows ADR-0034's authority-location and skill-routing clauses; its QA, security,
preservation and GitOps CD boundaries remain in force.

## Context

Main at `eb4fcfe3283115388d6eb1f31d56780b3e578f77` already consolidated the
role registry, native references and QA. Its location decision requires Codex
to read skills explicitly outside the documented project skill discovery root.
A second copy or provider generator would add avoidable drift. The old hub
contains policies, roles, callable skills, two ordinary workflow documents and
provider-only notes; these are distinct responsibilities.

## Decision

1. `.agents/governance/` owns common policies and normative SDLC;
   `.agents/roles/` owns stable role metadata and neutral responsibilities.
2. `.agents/skills/<id>/SKILL.md` owns existing callable procedures. Codex uses
   its project skill discovery path; Claude uses per-skill relative links in
   `.claude/skills/`. The packages require explicit invocation, and their
   procedures preserve all role, user approval and secret boundaries.
3. `.agents/workflows/` owns the two ordinary lifecycle/delegation procedures.
   Provider-only support notes live beside their native adapters. Optional
   memory, rules, prompts, evaluations and scripts folders are not created.
4. The old documentation governance root is removed after file-by-file review
   and consumer migration. No redirect, fallback or duplicate authority stays.
   Historical provenance remains recoverable by its real baseline commit and
   original path; source hashes and past execution results are not rewritten.
5. Root AGENTS explicitly requires reading selected common files. Root CLAUDE
   may import shared and Claude instructions, never the Codex entrypoint.
   Native model/tool mappings stay unchanged and static parity does not prove
   runtime permissions, discovery, invocation or hook delivery.
6. The existing QA registry, bounded runner, Stage 99 profiles and narrow
   provider write hook validate the new hidden paths. Old-root reintroduction,
   broken links, invalid metadata and widened permissions fail closed.

## Explicit Non-goals

No commits, push, merge, PR, deployment, cluster or Vault operation, credentials,
paid model call, global configuration, trust grant, new hook or model upgrade.
The retired common memory structure remains retired. No renderer is added.

## Consequences

One ownership graph now matches Codex's documented skill discovery path.
Native invocation metadata limits unintended activation, but is not an approval
system. Actual native loading remains separately verifiable in a fresh session.
The transition affects links, document routing and historical replacement
endpoints as well as files; moving the folder alone is insufficient.

## Alternatives

- Retain the old location and explicit reads: fewer changed paths, but fails
  the requested common authority and native discovery design.
- Copy or generate a second skill tree: introduces drift and an additional
  maintenance/validation owner without a runtime need.
- Move the reviewed common files and rehome provider/workflow documents:
  selected for one authority, native path compatibility and minimal adapters.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0034](0034-stage-00-governance-and-unified-quality-gates.md) | Narrows authority location and skill routing; preserves QA, security and CD decisions | [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) |
