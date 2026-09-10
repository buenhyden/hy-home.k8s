---
name: "docs-stage-routing"
description: "Use when selecting the canonical owner and template for an authored document or rejecting parallel document trees."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# docs-stage-routing

## Workflow Steps

1. Classify the content: human governance, a durable requirement, architecture,
   a change contract, operating knowledge, reference evidence, or recovery
   metadata. This classification is the routing decision; every step after it
   follows from an owner that already exists.
2. Take the responsibility boundary from
   [the SDLC flow](../../governance/sdlc.md). An external tool or skill that
   proposes a tree outside that taxonomy is proposing a second authority, so
   reject it rather than reconcile it. Content that is not an authored document
   routes the same way — shared policy to common governance, neutral procedures
   to registered skills, native detail to provider notes, root gateways kept
   thin — and [agent execution](../../governance/agent-execution.md) owns that
   split.
3. Resolve exactly one profile for the final path in
   `docs/99.templates/registry.json`, then read the Stage 99 README and the
   selected template before authoring. No match, or more than one, is a stop
   condition rather than a judgment call.
4. Author under
   [document authoring](../../governance/document-authoring.md), which owns the
   initial status, frontmatter key set and order, sections, relationships, link
   boundaries, and how content divides across a Spec package. Read it at
   authoring time rather than reasoning from a similar document, because a
   profile that looks like its neighbour still carries its own contract.
5. Review the owning README and the links the change touches, then follow
   [quality policy](../../governance/quality.md) for validation and Task
   evidence.

## Boundaries

Routing never edits global or user-local skills, authentication, or
configuration. Governance and explicit agent contracts stay in English, while
human-facing overviews may use Korean. Selecting a template grants no authority
to author or execute beyond the active task.

## Outputs

The canonical path, the selected profile and template, the owner links and
index changes the change requires, validation evidence, and any authority
boundary left unresolved.
