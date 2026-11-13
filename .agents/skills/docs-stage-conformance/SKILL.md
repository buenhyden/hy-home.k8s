---
name: "docs-stage-conformance"
description: "Use when repairing scoped document-profile, README, heading, or cross-link drift without changing historical meaning."
metadata:
  title: "Docs Stage Conformance"
  version: "1.0.2"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# docs-stage-conformance

## Purpose and Trigger

### When to Use

Use this skill as its frontmatter description states.

### When Not to Use

- Choosing the owner and template for a document that has neither yet; use `docs-stage-routing`.
- Auditing navigation and owner maps across the tree rather than one document; use `knowledge-map`.

#### Boundaries

Registry/template prompts are not authored-body errors. Do not use broad custom
scans as proof when a canonical validator already owns the rule. Report an
unclear ownership or required semantic change before expanding the task.

## Procedure

### Steps

1. Read the relevant gateway, document-authoring policy, current Git state,
   selected Stage 99 profile/template, and owning README.
2. Identify concrete profile, heading, link, index, or authority drift before editing. For a broad governance audit use
   `workspace-harness-audit` instead.
3. Apply the smallest authorized fix. Preserve completed evidence;
   report historical disposition to its owning Task rather than rewriting
   facts to satisfy a current profile.
4. Update affected navigation and exact current consumers together.
5. Run the applicable strict document validators, link/owner and knowledge-surface checks,
   then the quality-policy completion sequence.
6. Record scope, commands, results, limitations, and next owner in the active
   Task. Do not create a new package or parallel progress ledger merely for a
   narrow cleanup.

### Failure Handling

None is stated in this document.

## Inputs and Outputs

### Inputs

None is stated in this document.

### Outputs

A scoped conformance diff and reproducible validation evidence without altered
historical or runtime claims.

## Verification

### Checks

None is stated in this document.

### Completion and Handoff

None is stated in this document.
