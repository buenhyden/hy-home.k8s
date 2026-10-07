---
title: "{{TITLE}}"
version: "0.1.0"
type: "evaluation/task"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

# [Evaluation Task]

## Overview

| Field | Declared value |
| --- | --- |
| Cycle ID | {{CYCLE_ID}} |
| Exact task/prompt or immutable source | {{TASK_PROMPT_SOURCE}} |
| Input ID and hash | {{INPUT_ID_AND_HASH}} |
| Baseline input, mode, tool, config and trust source | {{BASELINE_CONDITION_SOURCE}} |
| With-skill input, mode, tool, config and trust source | {{WITH_SKILL_CONDITION_SOURCE}} |
| Skill revision | {{SKILL_REVISION}} |
| Provider and baseline session | {{BASELINE_PROVIDER_SESSION}} |
| Provider and with-skill session | {{WITH_SKILL_PROVIDER_SESSION}} |
| Declared pair count | 1 |

<!-- Author prompt: One harness directory is one paired trial. A reevaluation uses a new cycle ID. -->

## Declared Trials

| Trial ID | Baseline output | With-skill output | Pair status | Partial reason |
| --- | --- | --- | --- | --- |
| {{TRIAL_ID}} | `baseline.md` (NOT_OBSERVED until captured) | `with-skill.md` (NOT_OBSERVED until captured) | pending | {{PARTIAL_REASON}} |

<!-- Author prompt: Declare the count before scoring. Link each output only after its file exists. -->

## Signals and Criteria

| Criterion ID | Observable signal | Scoring rule | Scorer ID |
| --- | --- | --- | --- |
| {{CRITERION_ID}} | {{SIGNAL}} | {{SCORING_RULE}} | {{SCORER_ID}} |

<!-- Author prompt: Define each criterion and its observable signal before collecting either condition. -->

## Human Calibration

<!-- Author prompt: Name the reviewer, calibration input and decision boundary before scoring. -->

## Related Documents

<!-- Author prompt: Link the evaluation router and the owner of the evaluated skill. -->
