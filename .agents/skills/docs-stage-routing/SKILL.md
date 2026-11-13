---
name: "docs-stage-routing"
description: "Use when selecting the canonical owner and template for an authored document or rejecting parallel document trees."
metadata:
  title: "Docs Stage Routing"
  version: "1.1.3"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# docs-stage-routing

## Purpose and Trigger

### When to Use

Use this skill as its frontmatter description states.

### When Not to Use

- Repairing drift in a document whose owner is already settled; use `docs-stage-conformance`.
- Maintaining the indexes and owner maps that route a reader; use `knowledge-map`.

#### Boundaries

Routing never edits global or user-local skills, authentication, or
configuration. Language policy is owned by
[document authoring](../../governance/document-authoring.md). Selecting a template grants no authority to author or execute
beyond the active task.

## Procedure

### Steps

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

### Failure Handling

This skill's stop condition is stated in Step 3: no matching profile, or more than one, stops the work rather than being a judgment call; any other failing step is reported and the work lifecycle's bounded-attempt stop rule applies. If a step needs its own recovery, add it here.

## Inputs and Outputs

### Inputs

This skill takes no input beyond the user's request and the files its Steps name; if a step comes to need another input, list it here.

### Outputs

The canonical path, the selected profile and template, the owner links and
index changes the change requires, validation evidence, and any authority
boundary left unresolved.

## Verification

### Checks

This skill defines no verification step separate from its Steps; the checks the invoking task selects under the quality policy apply. If it needs a separate one, list it here.

### Completion and Handoff

This skill completes and hands off through the work lifecycle's Completion steps and adds no field beyond what its Steps state; if it needs one, list it here.
