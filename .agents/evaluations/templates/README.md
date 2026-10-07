---
title: "Agent Evaluation Form Router"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-07"
---

# Agent Evaluation Form Router

## Overview

The canonical evaluation task, score and aggregate forms belong to
[Stage 99](../../../docs/99.templates/README.md). This directory routes
authors to those forms; it does not duplicate their schema or supply
example outcomes as actual evidence.

## Scope

Select the current Stage 99 profile before authoring an evaluation member.
Task context and two actual outputs precede a scored one-trial cycle; declared rubric,
criterion IDs, signal granularity, scorer ID and human calibration precede
aggregation. The [evaluation root](../README.md) retains the sole aggregate
owner. A form cannot grant execution, publication or native runtime authority.

## Structure

### Item Index

This router holds no local form copies. Consult the [Stage 99 template
router](../../../docs/99.templates/templates/README.md) for current task,
score and results forms and the [trial router](../harnesses/README.md) for
actual evidence placement. Stage 99 names these canonical files
`evaluation-task.template.md`, `evaluation-score.template.md` and
`evaluation-results.template.md`; this router does not link across stages to
individual form files.

## Usage

### Add and Find

Use Stage 99's exact profile and version for the target path. Preserve
criterion and scorer identity with the scored input; a rubric revision
requires a new versioned comparison, not a silent score rewrite. Validate
profile, links and source evidence before aggregation. An empty result form
is capacity only, with no measured score, paired run or repository QA outcome.
Follow [quality policy](../../governance/quality.md#agent-evaluation-evidence)
and the original Task for execution and review; route unavailable sessions
and missing responses as evidence gaps rather than a comparison.

## Related Documents

- [Evaluation root](../README.md)
- [Trial evidence router](../harnesses/README.md)
- [Stage 99 profiles](../../../docs/99.templates/README.md)
- [Stage 99 template navigation](../../../docs/99.templates/templates/README.md)
- [Stage 03 Spec navigation](../../../docs/03.specs/README.md)
