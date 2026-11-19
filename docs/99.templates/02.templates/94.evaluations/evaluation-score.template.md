---
title: "{{TITLE}}"
version: "0.1.0"
type: "evaluation/score"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

# [Evaluation Score]

## Overview

| Field | Observed value |
| --- | --- |
| Cycle ID and trial ID | {{CYCLE_AND_TRIAL_ID}} |
| Task declaration | `task.md` (link after the instance exists) |
| Grader ID and revision | {{GRADER_ID_AND_REVISION}} |
| Granularity | one paired trial |
| Declared pair count | 1 (from `task.md`) |
| Observed complete pair count | {{OBSERVED_PAIR_COUNT}} |
| Input ID and hash | {{INPUT_ID_AND_HASH}} |
| Partial reason | {{PARTIAL_REASON}} |

<!-- Author prompt: A document and a score do not prove a provider session ran. -->

## Trial Evidence

| Trial ID | Baseline output and hash | With-skill output and hash | Session references | Evidence status |
| --- | --- | --- | --- | --- |
| {{TRIAL_ID}} | `baseline.md` {{BASELINE_SHA256}} | `with-skill.md` {{WITH_SKILL_SHA256}} | {{SESSION_REFERENCES}} | incomplete |

<!-- Author prompt: Record actual output hashes and session references; leave a missing condition incomplete. -->

## Criterion Scores

| Trial ID | Criterion ID | Baseline observed signal and raw locator | With-skill observed signal and raw locator | Baseline score | With-skill score |
| --- | --- | --- | --- | --- | --- |
| {{TRIAL_ID}} | {{CRITERION_ID}} | {{BASELINE_SIGNAL_AND_LOCATOR}} | {{WITH_SKILL_SIGNAL_AND_LOCATOR}} | pending | pending |

<!-- Author prompt: Link an output only after it exists; score actual pairs using task.md criteria. -->

## Human Calibration

<!-- Author prompt: Record the observed calibration decision and any unresolved disagreement. -->

## Related Documents

<!-- Author prompt: Link task.md and the evaluation router. -->
