---
title: "Project Map"
version: "0.1.0"
type: "governance/knowledge"
status: "draft"
owner: "platform"
updated: "2026-09-07"
---

# Project Map

## Overview

A reader who does not yet know this repository asks which top-level tree owns
what, and which file to open first inside it. This map answers that question and
nothing else.

## Authority Boundary

Every row points; none decides. The owner named in a row keeps its own scope,
approval boundary and validation contract, and this document restates none of
them. A disagreement between a row and its owner is resolved by the owner.

## Pointer Index

| Area | Owner path | Entry path | Stays valid while |
| --- | --- | --- | --- |
| Common governance | `.agents/` | `.agents/README.md` | Provider-neutral policy, roles, skills and lifecycle procedures stay here and native adapters stay outside |
| Claude adapter | `.claude/` | `.claude/README.md` | Claude remains a tracked provider surface |
| Codex adapter | `.codex/` | `.codex/README.md` | Codex remains a tracked provider surface |
| Documentation | `docs/` | `docs/README.md` | The stage contract keeps one canonical owner per document purpose |
| Desired state | `gitops/` | `gitops/README.md` | ArgoCD reconciliation stays the normal change path |
| Cluster bootstrap | `infrastructure/` | `infrastructure/README.md` | The local k3d platform is created from tracked assets |
| Policy rules | `policy/` | `policy/README.md` | Policy rules stay separate from the lanes that run them |
| Local gateway reference | `traefik/` | `traefik/README.md` | The canonical deployment path stays `gitops/` |
| Reference material | `examples/` | `examples/README.md` | Examples stay reference-only and are not deployed |
| Repository tooling | `scripts/` | `scripts/README.md` | Validation routing stays registry-owned |
| Tooling tests | `tests/` | `tests/README.md` | Each validator keeps an independent top-level test |
| Agent evaluation | `evals/` | `evals/README.md` | The evaluation harness stays outside the common governance tree |
| Local sensitive files | `secrets/` | `secrets/README.md` | No secret value is tracked in this repository |
| Hosted surface | `.github/` | `.github/repository-surface.md` | Hosted execution stays separate from repository-static evidence |

## Validation and Refresh

Every owner and entry path above must exist in the tree; a missing path fails
the knowledge validator. Refresh a row when its tree gains or loses ownership,
not on a schedule. Adding or removing a top-level tree invalidates this map.

## Related Documents

- [Common Knowledge](README.md)
- [Domain Index](domains.md)
- [Governance Hub](../README.md)
