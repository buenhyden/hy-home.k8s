---
title: "Agent Evaluation Evidence"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-07"
---

# Agent Evaluation Evidence

## Overview

This directory routes evidence from actual paired trials of the same task:
one `noSkill` baseline and one `withSkill` run. The [agent evaluator](../roles/agent-evaluator.md)
owns the assessment, [quality policy](../governance/quality.md#agent-evaluation-evidence)
owns evidence meaning, and [Stage 99](../../docs/99.templates/README.md)
owns document forms. A stored response alone does not prove native skill
loading, command execution, permission enforcement or a passing repository QA
gate.

## Scope

Admit a cycle only when its task, two actual outputs, and scoring basis can be
linked to their observed sessions. Each cycle has one paired trial; additional
trials use separate cycle directories. Record signals, scorer and criterion
IDs, one-pair score granularity, partial results and human calibration before
any aggregate is claimed. A missing observation stays `NOT_OBSERVED`; an
unexecuted paired comparison stays `NOT_RUN`. The original Task owns work
authorization and execution status, while provider/native and runtime claims
remain with their original evidence owners.

Earlier synthetic cases and responses are historical Git and Task evidence,
not actual paired trials in this directory. An absent expectation in a
synthetic fixture does not become a no-skill response. Neither a fixture
count nor this router registers a standing grader or QA gate. User-supplied
skill definitions that are not present in the workspace are reference
criteria only; this route does not install or create them.

## Structure

| Path | Purpose |
| --- | --- |
| [harnesses/](harnesses/) | Route task-matched trial inputs and raw observed outputs. |
| [templates/](templates/) | Route the Stage 99 task, score and result forms without copying their authority. |
| [results.md](results.md) | Sole aggregate owner when a complete actual cycle is admitted; its empty state carries no score. |

## Usage

### Configuration Boundary

Declare the same task and baseline for both conditions before execution.
Keep actual prompt, skill version, provider/session identity, the one-pair
trial declaration, scorer and criterion IDs with the cycle. A task or rubric change makes a new
comparison input; it does not silently revise an earlier score.

### Validation

Check the current Stage 99 profile, links, declared pair completeness and
score calculation on actual inputs. Results are entered only after every
included cycle has a complete actual pair; partial pairs remain incomplete.
The aggregate reports its actual cycle count without a fixed quality threshold. Repository
QA, independent semantic review and provider-runtime observation are separate
lanes.

### Operations

Keep raw output and session provenance with the observed trial, record scoring
against the declared rubric, then aggregate once at `results.md`. Report an
unavailable provider/session, missing skill, or missing response to the
original Task owner. Do not synthesize an output to complete a row.

## Related Documents

- [Common agent governance](../README.md)
- [Agent evaluator responsibility](../roles/agent-evaluator.md)
- [Quality policy](../governance/quality.md#agent-evaluation-evidence)
- [Stage 99 profiles and templates](../../docs/99.templates/README.md)
- [Stage 03 Spec navigation](../../docs/03.specs/README.md)
