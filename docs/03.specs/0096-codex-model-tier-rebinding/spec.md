---
title: "Codex Model Tier Rebinding Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
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
its Codex model improved. This Spec owns both bindings and their rationale.

## Strategic Boundaries & Non-goals

In scope: the Codex `capability_models` entry in `.agents/roles/registry.json`,
the `model` value of each `.codex/agents/*.toml` projection, the Codex provider
note, and this package.

Out of scope: Claude bindings; tier membership of any role; permission classes
and sandbox modes; reasoning effort, which the model-selection policy preserves
without task evidence; any account, usage, or rate-limit setting.

## Contracts

- A tier binds a model that the installed client's catalog lists and the
  current account can serve.
- `top` binds the strongest permitted capability, and `worker` binds a
  bounded capable model, as [model selection](../../../.agents/governance/model-selection.md)
  defines them.
- The reasoning bindings and the role overrides stay unchanged, and each value
  must be a level the bound model supports.

## Core Design

| Tier | Roles | Before | After | Reason |
| --- | --- | --- | --- | --- |
| `top` | supervisor, architect, governance-steward, incident-responder, security-auditor | `gpt-5.5` | `gpt-6-astra` | The catalog calls it "Frontier intelligence for the most demanding work", and the models page recommends it for complex end-to-end workflows. It is also the client's default model. `gpt-5.5` retires on 2026-10-14. |
| `worker` | the twelve other roles | `gpt-5.3-codex-spark` | `gpt-6-sol` | The catalog calls it the "Workhorse model for coding and everyday work", and it is the documented successor for complex coding. `gpt-6-luna` targets clear, repeatable, high-volume work such as extraction, not these review and implementation roles. |

The effort values stay as they are: `xhigh` for `top`, `high` for `worker`,
`high` for incident-responder and security-auditor, and `medium` for doc-writer
and wiki-curator. The catalog lists every one of them for the bound model.

## Data Modeling & Storage Strategy

The registry holds the binding and each projection restates it. The governance
validator rejects any projection that drifts from the registry.

## Interfaces & Data Structures

`providers[codex].capability_models.top` changes, and so does `model` in the
five `top` projections. The `worker` change is already on the branch this
package starts from.

## Edge Cases & Error Handling

A bound model that the catalog drops, or that the account cannot serve, fails
at spawn. The Task records the catalog observation and a spawn per tier.

## Failure Modes & Fallback / Human Escalation

If `gpt-6-astra` usage limits constrain the `top` roles, the fallback is
`gpt-6-sol`, which is the documented migration target for `gpt-5.5`. That
fallback needs the request owner's decision, and the Task records it.

## Verification Commands

```bash
python3 scripts/validate-agent-governance.py --root .
python3 scripts/qa.py staged
codex debug models
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-CMT-001 | Each tier's model is in the installed client's catalog, and each bound effort is a level that model supports | Catalog check in the Task |
| VAL-CMT-002 | The registry and all 17 projections agree | Governance validator |
| VAL-CMT-003 | One spawned role per tier reports the bound model | Dated Codex session record in the Task |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[Task](tasks/tsk-0001-rebind-codex-model-tiers.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-001 | Catalog check |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-002 | Governance validator |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMT-003 | Codex session record |
