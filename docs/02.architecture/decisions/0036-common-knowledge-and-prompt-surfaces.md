---
title: "Common Knowledge and Prompt Surfaces"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-09"
layer: "architecture"
artifact_id: "ADR-0036"
supersedes: "ADR-0035"
---

# ADR-0036: Common Knowledge and Prompt Surfaces

## Overview

This decision supersedes ADR-0035. It replaces that decision's
unadopted-directory clause and carries forward its authority-location,
skill-routing, gateway, preservation and validation clauses unchanged,
restating them here so this decision stands alone rather than by reference.
Acceptance records the durable choice; it does not establish native discovery,
permission enforcement, model resolution or hook delivery, which remain
separately observable evidence.

**Current ownership clarification (2026-09-09).** The accepted decision below
remains the historical record of what was decided. Root `evals/` now holds
evaluation case and response data, `scripts/run-agent-evaluations.py` owns
runner behavior, and `scripts/validation/registry.json` owns gate selection.
This clarification records current execution ownership; it does not amend the
decision.

## Context

ADR-0035 decided that optional memory, rules, prompts, evaluations and scripts
folders are not created. That clause was written when no material in the
repository needed those owners, so a blanket prohibition cost nothing and
prevented speculative structure.

Two owners are now needed. Repeatable authoring requests reach an agent as
prose retyped per session, so their inputs and refusal conditions have no
contract and cannot be validated. Cross-cutting orientation material -- which
directory owns what, which document answers which question -- is either absent
or duplicated inside policy documents that own a different subject. The
prohibition now blocks work rather than preventing drift, and a decision that
forbids a directory the repository requires is the kind of stale clause the
document contract exists to catch.

The retired memory structure is a separate matter. It was retired under Spec
0054 and Spec 0065 because a generated progress ledger competed with the owning
Spec Task for the same authority. Nothing in this decision reopens it, and the
governance validator continues to fail closed if that surface reappears.

## Decision

1. `.agents/governance/` owns common policies and normative SDLC;
   `.agents/roles/` owns stable role metadata and neutral responsibilities.
2. `.agents/skills/<id>/SKILL.md` owns existing callable procedures. Codex uses
   its project skill discovery path; Claude uses per-skill relative links in
   `.claude/skills/`. The packages require explicit invocation, and their
   procedures preserve all role, user approval and secret boundaries.
3. `.agents/workflows/` owns the two ordinary lifecycle/delegation procedures.
   Provider-only support notes live beside their native adapters. Two optional
   directories are adopted. `.agents/knowledge/` owns hand-maintained pointer
   material that names owners and answers navigation questions, bound by a
   non-duplication rule so it states no policy of its own. `.agents/prompts/`
   owns input and output contracts for repeatable authoring requests, each
   naming its inputs, its outputs and the conditions under which it refuses.
   Memory, rule, evaluation and script directories stay unadopted, each for its
   own reason: the memory structure is retired and stays retired; a rule
   directory would duplicate policy `.agents/governance/` already owns; `evals/`
   already owns the evaluation runner, its cases and its validation surface;
   and `scripts/` already owns executable tooling at the repository root.
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

This decision grants no Git or runtime action authority; the owning Task records
the current user-authorized scope. Deployment, cluster or Vault operation,
credentials, paid model calls, global configuration, trust grants, new hooks
and model upgrades remain outside the decision.

The adopted knowledge surface is not the retired generated index. That index
was produced from the tree and competed with the documents it described. This
surface is hand-maintained pointer material whose non-duplication rule is
enforced by a validator, so it cannot become a second policy store. No renderer
and no generation step is added for either adopted directory.

## Consequences

The prompt surface gives repeatable requests a contract that can be validated
and refused against, instead of prose that varies per session. The knowledge
surface gives orientation material one owner instead of scattering it through
policy documents that own other subjects.

Both directories add validation obligations before they add value: each needs a
Stage 99 profile, a template, coverage in the affected-surface contract, and at
least one named consumer. A directory with no consumer is drift with a nicer
path, so the adopting work is not complete when the directory exists.

Keeping the evaluation and script directories unadopted preserves one owner per
concern. Two of the five directories ADR-0035 refused are adopted here; the
other three keep that decision's answer and its reasoning.

## Alternatives

- Absorb the material into existing documents: fewer paths and no new profile,
  but the prompt input and output contracts are left without an owner, and
  orientation material continues to accumulate inside policy documents that own
  a different subject. Rejected.
- Adopt every optional directory ADR-0035 refused: internally consistent and
  removes the need for a future successor, but it duplicates an evaluation
  harness that already owns its runner, cases and validation surface, and
  creates directories with no consumer. Rejected.
- Amend ADR-0035 in place: the smallest diff, but an accepted decision's body
  is historical evidence of what was decided and when. Rejected in favour of
  the successor pattern ADR-0035 itself used on ADR-0034.

## Traceability

This decision supersedes [ADR-0035](0035-common-agents-authority-and-native-skill-routing.md),
whose body stays intact as evidence of the decision taken at that time.
[SPEC-0075](../../03.specs/0075-common-knowledge-and-prompt-surfaces/spec.md)
owns the acceptance criteria, the ordered work and the execution evidence for
the two adopted surfaces.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0035](0035-common-agents-authority-and-native-skill-routing.md) | Revises the unadopted-directory clause to adopt a knowledge and a prompt surface; preserves the authority-location, skill-routing, gateway, preservation and validation clauses | [SPEC-0075](../../03.specs/0075-common-knowledge-and-prompt-surfaces/spec.md) |
