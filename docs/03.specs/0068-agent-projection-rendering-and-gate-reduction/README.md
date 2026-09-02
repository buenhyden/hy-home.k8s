# SPEC-0068: Agent Projection Rendering and Gate Reduction

## Overview

Spec 0068 makes the Claude and Codex agent projections a rendered artifact of
`.agents/registry.json`, moves the tier-to-model binding into the registry that
already owns the tier, and retires the validators and fixtures whose question
disappears once the hand-maintained duplication does. It repairs conformance
with the accepted decision in ADR-0030 rather than establishing a new one.

## Scope

This README is a navigation projection only. The Spec owns the binding,
derivation, and gate-inventory contracts. The Plan and its Tasks are added when
implementation is authorized. This router does not duplicate those bodies or
define a lifecycle state.

## Item Index

| Item | Body |
| --- | --- |
| Technical contract | [spec.md](spec.md) |

## Add and Find

Add a package-local Task under `tasks/` and record execution evidence there.
Model bindings and permission baselines belong to the registry and its schema,
not to this router, to a provider projection, or to any prose body.

## Related Documents

- [Current Spec Index](../README.md#current-spec-index)
- [ADR-0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- [Agent Registry](../../../.agents/registry.json)
- [Model Selection Policy](../../00.agent-governance/policies/model-selection.md)
