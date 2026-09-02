# SPEC-0070: Retired Provider Residue Disposition

## Overview

Spec 0070 disposes of the tracked residue left by ADR-0030's removal of Gemini
and Antigravity as supported providers. It separates live surfaces and current
documents, which are corrected, from historical records and absence proofs,
which are preserved unchanged.

## Scope

This README is a navigation projection only. The Spec owns the classification
rule and the disposition contracts. The Plan and its Tasks are added when
implementation is authorized. This router does not duplicate those bodies or
define a lifecycle state.

## Item Index

| Item | Body |
| --- | --- |
| Technical contract | [spec.md](spec.md) |

## Add and Find

Add a package-local Task under `tasks/` and record execution evidence there. The
supported provider set belongs to ADR-0030 and the agent registry, not to this
router or to any prose body.

## Related Documents

- [Current Spec Index](../README.md#current-spec-index)
- [ADR-0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- [SPEC-0065 — transition residue retirement](../0065-transition-residue-retirement/spec.md)
