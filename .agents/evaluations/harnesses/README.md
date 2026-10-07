---
title: "Agent Evaluation Trial Evidence"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-07"
---

# Agent Evaluation Trial Evidence

## Overview

This router is the entry for observed `noSkill` and `withSkill` outputs from
the same task and baseline. The [evaluation root](../README.md) owns routing;
the original Task owns authorization and actual execution status.

## Scope

For each actual cycle, keep its task and baseline identity, both condition
inputs and raw outputs, provider/session provenance, its one paired trial, signals,
criterion IDs and incomplete attempts. A generated example, unrun condition
or historical synthetic response is not an observed trial. Native skill
loading, command execution and permission observations require their own
direct session evidence.

## Structure

### Item Index

Index each admitted direct cycle directory here once. A cycle holds
`task.md`, `baseline.md`, `with-skill.md` and `score.md` for exactly one
paired trial; the two raw output
files keep their original observed content rather than a governed frontmatter
wrapper. A reevaluation uses a new cycle directory and preserves earlier
evidence. Additional trials use separate cycle directories.
[The parent router](../README.md) identifies the sole aggregate
result owner; [forms](../templates/README.md) point to Stage 99 instead of
copying their schema. No placeholder row represents an unrun trial.

## Usage

### Add and Find

Fix the task and baseline before collecting the two conditions. Preserve the
skill/version and provider/session input that make the comparison reproducible.
Compare each claimed score to its raw observation and declared criterion ID.
Record absent output as `NOT_OBSERVED` and unrun trial as `NOT_RUN` in the
owning Task, retaining partial attempts without entering them as completed
pairs or aggregate results. When a complete cycle is admitted, add its direct
directory link to the Item Index and route its score to the sole aggregate
owner with human calibration where the rubric requires it.

## Related Documents

- [Evaluation root](../README.md)
- [Evaluation forms router](../templates/README.md)
- [Agent evaluator responsibility](../../roles/agent-evaluator.md)
- [Quality policy](../../governance/quality.md#agent-evaluation-evidence)
