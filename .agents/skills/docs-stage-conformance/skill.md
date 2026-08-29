---
name: docs-stage-conformance
description: Use when repairing scoped document-profile, README, heading, or cross-link drift without changing historical meaning.
---

# docs-stage-conformance

## Workflow Steps

1. Read the relevant gateway, document-authoring policy, current Git state,
   selected Stage 99 profile/template, and owning README.
2. Identify concrete profile, heading, link, index, generated-output, or
   authority drift before editing. For a broad governance audit use
   workspace-harness-audit instead.
3. Apply the smallest authorized fix. Preserve sealed or completed evidence;
   report historical disposition to its migration owner rather than rewriting
   facts to satisfy a current profile.
4. Update affected navigation and exact current consumers together.
5. Run the applicable strict document validators and generated-index checks,
   then the quality-policy completion sequence.
6. Record scope, commands, results, limitations, and next owner in the active
   Task. Do not create a new package or parallel progress ledger merely for a
   narrow cleanup.

## Boundaries

Registry/template prompts are not authored-body errors. Do not use broad custom
scans as proof when a canonical validator already owns the rule. Report an
unclear ownership or required semantic change before expanding the task.

## Outputs

A scoped conformance diff and reproducible validation evidence without altered
historical or runtime claims.
