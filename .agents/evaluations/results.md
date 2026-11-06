---
title: "Agent Evaluation Results"
version: "0.1.1"
type: "evaluation/results"
status: "draft"
owner: "platform"
updated: "2026-11-06"
---

# Evaluation Results

## Overview

This is the sole aggregate owner for actual, same-task `noSkill` and
`withSkill` paired evaluations. As of 2026-10-07, no observed cycle has been
admitted. This draft establishes capacity under the current
[evaluation router](README.md), without claiming a provider session or a
repository QA result.

## Pair Coverage

| Cycle ID | Trial ID | Declared pairs | Complete pairs | Task | Score | Partial reason |
| --- | --- | --- | --- | --- | --- | --- |

No actual pair is recorded. Enter one row per admitted cycle only after its
task, baseline output, with-skill output and score identify the same declared
one-pair trial. Additional trials use distinct cycle IDs; incomplete attempts
remain with their own evidence owners and are not counted as complete pairs.

## Aggregate

| Scope | Actual pairs | Criterion ID | Baseline summary | With-skill summary | Calibration reference |
| --- | --- | --- | --- | --- | --- |

No denominator or score is reported. Aggregate only complete, declared cycles
with an identified scorer, criterion IDs, score granularity and human
calibration disposition. Report the actual count and measured scope; no fixed
performance threshold is inferred from an empty form.

## Limitations

Historical synthetic fixtures and missing expectations are not observed
paired outputs. The two user-provided Skill definitions are absent from this
workspace. No paired session, skill loading, command execution, permission
enforcement, score truth or human calibration was observed for this draft.

## Related Documents

- [Evaluation router](README.md)
- [Quality policy](../governance/quality.md#agent-evaluation-evidence)
- [Stage 99 template navigation](../../docs/99.templates/templates/README.md)
- [Agent evaluator responsibility](../roles/agent-evaluator.md)
