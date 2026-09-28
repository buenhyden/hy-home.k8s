---
title: "Codex Model Tier Rebinding Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0096"
---

# Codex Model Tier Rebinding Technical Specification (Spec)

## Overview

The registry binds one Codex model to each capability tier. On 2026-09-27 the
`worker` binding `gpt-5.3-codex-spark` failed at spawn: the client rejected it
for a ChatGPT account, and `codex debug models` does not list it. The same day
it was rebound to `gpt-6-sol`. The `top` binding `gpt-5.5` still resolves, but
the catalog calls it a "Legacy coding model", and the
[Codex models page](https://learn.chatgpt.com/docs/models) retires it from
Codex on 2026-10-14. The request owner asked for each tier to be researched and
its Codex model improved, and allowed the latest models. They also asked for
`gpt-6-astra` use to be kept to a minimum: only roles that need thinking and
planning get it, and practical roles get a lower model. This Spec owns the
bindings, the per-role model departure they need, and the rationale.

## Strategic Boundaries & Non-goals

In scope: the Codex `capability_models` entry and a Codex
`native_model_override` in `.agents/roles/registry.json`, its schema and
validator rule, the `model` value of each `.codex/agents/*.toml` projection, the
model-selection policy sentence that names role departures, the Codex provider
note, and this package.

Out of scope: Claude bindings; tier membership of any role; permission classes
and sandbox modes; reasoning effort, which the model-selection policy preserves
without task evidence; any account, usage, or rate-limit setting.

## Contracts

- A bound model is one that the installed client's catalog lists and the
  current account can serve.
- A capability tier binds a model for every role that carries it. A role whose
  Codex model genuinely differs declares `native_model_override`, the same way
  `native_reasoning_override` declares an effort departure. The validator
  resolves each projection's model from the tier and that override, and it
  rejects drift.
- `gpt-6-astra` is bound only to roles whose responsibility is planning,
  orchestration, or structural design. Every other role binds a lower model.
- Reasoning bindings and role overrides stay unchanged, and each value must be
  a level the bound model supports.

## Core Design

| Scope | Roles | Before | After | Reason |
| --- | --- | --- | --- | --- |
| `top` tier | governance-steward, incident-responder, security-auditor | `gpt-5.5` | `gpt-6-sol` | `gpt-5.5` is legacy and retires on 2026-10-14, and the models page names `gpt-6-sol` as its replacement. These roles do bounded maintenance, triage, and audit against the repository's own contracts, so their judgment runs on Sol at `xhigh` or `high`. |
| `top` override | supervisor, architect | `gpt-5.5` | `gpt-6-astra` | Supervisor routes and plans multi-step work, and architect owns structural decisions. The models page recommends Astra for "complex end-to-end workflows requiring sustained reasoning". These are the only two roles that plan. |
| `worker` tier | the twelve other roles | `gpt-5.3-codex-spark` | `gpt-6-sol` | The catalog calls it the "Workhorse model for coding and everyday work". `gpt-6-luna` targets clear, repeatable, high-volume work such as extraction, not these review and implementation roles. |

Effort stays as it was: `xhigh` for `top` (supervisor, architect,
governance-steward), `high` for `worker`, `high` for incident-responder and
security-auditor, and `medium` for doc-writer and wiki-curator. The catalog
lists every one of these values for the model it is bound to. The Claude side
keeps its tier bindings, because the override names only `codex`.

## Data Modeling & Storage Strategy

The registry holds the tier bindings and the two overrides, and each projection
restates the resolved value. The schema admits `native_model_override` with a
`codex` model identifier only.

## Interfaces & Data Structures

- `providers[codex].capability_models.top` changes from `gpt-5.5` to
  `gpt-6-sol`. The `worker` change is already on the branch this package starts
  from.
- `roles[supervisor|architect].native_model_override.codex` is `gpt-6-astra`.
- `scripts/validate-agent-governance.py` gains `_bound_model`, which resolves
  the override before the tier binding for both providers.

## Edge Cases & Error Handling

A bound model that the catalog drops, or that the account cannot serve, fails
at spawn. A projection whose model differs from its resolved binding fails
`AGENT-NATIVE-METADATA`.

## Failure Modes & Fallback / Human Escalation

If Sol proves too weak for a non-planning `top` assignment, escalating that one
assignment to `gpt-6-astra` needs the request owner's decision. The Task
records any such escalation. The binding does not change.

## Verification Commands

```bash
python3 scripts/validate-agent-governance.py --root .
python3 -m unittest tests.test_validate_agent_registry
python3 scripts/qa.py staged
codex debug models
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-CMT-001 | Each bound model is in the installed client's catalog, and each bound effort is a level that model supports | Catalog check in the Task |
| VAL-CMT-002 | The registry, its overrides, and all 17 projections agree, and drift is rejected | Governance validator and unit tests |
| VAL-CMT-003 | Spawned roles on each binding apply the bound model and reasoning effort | Rollout records in the Task |
| VAL-CMT-004 | `gpt-6-astra` is bound only to supervisor and architect | Registry and projections |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[Task](tasks/tsk-0001-rebind-codex-model-tiers.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-001 | Catalog check |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-002 | Governance validator |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-003 | Rollout records |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-004 | Registry and projections |
