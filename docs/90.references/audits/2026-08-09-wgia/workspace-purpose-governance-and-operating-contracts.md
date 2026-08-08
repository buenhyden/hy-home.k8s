---
title: 'Audit: Workspace Purpose, Governance, and Operating Contracts'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Workspace Purpose, Governance, and Operating Contracts

## Overview

This report owns the audit of workspace purpose, roles, governance hierarchy,
root and provider entrypoints, operating contracts, and canonical-owner
conflicts. WGIA-001 establishes the pinned source inventory and finding form;
WGIA-002 owns the complete comparison and independent review.

## Reference Type

Dated repository-static governance audit. It is descriptive Stage 90 evidence,
not an active policy, permission, provider, or operating-contract owner.

## Authority Boundary

Root gateways route agents into Stage 00; Stage 00 rules and machine contracts
remain authoritative for execution behavior. This report may identify and
route conflicts, but it cannot resolve an ambiguous policy or architecture
choice, redefine a provider's runtime, or promote tracked configuration to
runtime-consumption evidence.

## Scope

Included: repository purpose, human and agent roles, governance loading order,
approval and operating boundaries, provider shims, root overview consistency,
and unique current-owner routing. Excluded: the later full semantic comparison,
canonical remediation, hosted CI, authenticated provider execution, secrets,
and live platform behavior.

## Definitions / Facts

### Workspace Purpose

The root `README.md`, `AGENTS.md`, bootstrap rule, and `.codex/CODEX.md` are
current workspace surfaces at observation commit
`50628b84165479b03efc0a25be075a49c91a9aef`. They identify a WSL2+k3d home-lab
managed through Argo CD GitOps and route active rules to canonical Stage 00 and
SDLC owners. WGIA-002 must compare their claims without copying those rules
into this report.

### Workspace Roles

The machine role inventory is routed through
`docs/00.agent-governance/contracts/harness-contract.json`; the human catalog
is `docs/00.agent-governance/harness-catalog.md`. Four tracked adapter roots
exist under `.agents/`, `.claude/`, `.codex/`, and `.gemini/`. Their presence is
repository-static inventory only and does not prove provider discovery or use.

### Operating Contracts

The bootstrap, agentic execution, approval-boundary, quality-standard,
provider-note, memory, and postflight surfaces are current inputs. The exact
JIT route and result vocabulary remain in Stage 00. This report owns only the
dated comparison and any finding that routes a discrepancy back to its current
owner.

### Canonical-owner Inventory

| Role | Current evidence surface | Foundation use |
| --- | --- | --- |
| Human index | `README.md`; `AGENTS.md` | Workspace entry and route evidence. |
| Policy owner | `docs/00.agent-governance/rules/` | Governance and execution expectations. |
| Machine owner | `docs/00.agent-governance/contracts/harness-contract.json` | Exact agent-system inventory. |
| Provider owner | `docs/00.agent-governance/providers/`; provider-native tracked roots | Provider-specific declared behavior only. |
| Evidence producer | repository validators under `scripts/` and `tests/` | Deterministic repository-static checks. |
| Historical snapshot | prior dated audit packs | Source-commit-bounded comparison only. |

### Finding Convention

Every material finding uses all fields below. Verdicts are closed to `Aligned`,
`Partial`, `Gap`, `Conflict`, `Legacy`, `Deprecated`, `One-shot candidate`, and
`DEFER`; evidence depth is closed to `repository-static`, `hosted`,
`provider-runtime`, and `live`. A missing field, unknown value, or unreviewed
claim fails closed.

#### WGA-GOV-001 — Governance source inventory established

- **Request IDs**: purpose, roles, and operating-contract coverage rows in the pack index.
- **Scope**: pinned canonical-owner and entrypoint inventory.
- **Expected state**: the later audit can compare purpose, roles, hierarchy, and operating contracts against unique current owners.
- **Observed state**: root, Stage 00, provider, catalog, machine-contract, and validator inputs are identified; topic-by-topic comparison is pending.
- **Evidence**: `README.md#overview`; `README.md#canonical-owners`; `AGENTS.md#agentsmd`; `.codex/CODEX.md#workspace-contract`; `docs/00.agent-governance/rules/bootstrap.md#jit-loading-sequence`; `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#surfaces`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: the foundation can route later findings, but cannot yet conclude that current claims are consistent or complete.
- **Disposition**: `Keep`.
- **Canonical owner**: current root and Stage 00 owners named above; execution evidence in the paired Task.
- **Verification**: strict profile/link checks plus WGIA-002 owner and contradiction review.
- **Uncertainty**: semantic duplication and conflict analysis is not yet reviewed.
- **Blocker**: none; pending topical work is not a blocker.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-GOV-001 | human index | `README.md#overview`; `README.md#canonical-owners`; `AGENTS.md#agentsmd` | Workspace purpose and entry routing. |
| SRC-WGA-GOV-002 | policy owner | `docs/00.agent-governance/rules/bootstrap.md#definition-of-done-for-governance-tasks`; `docs/00.agent-governance/rules/agentic.md#execution-contract`; `docs/00.agent-governance/rules/quality-standards.md#canonical-completion-sequence` | Current execution and evidence contracts. |
| SRC-WGA-GOV-003 | machine owner | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/contracts/harness-contract.json#surfaces` | Exact machine-readable harness inventory. |
| SRC-WGA-GOV-004 | historical snapshot | `docs/90.references/audits/2026-07-11-weia/README.md#snapshot-contract` | Prior dated observations only. |

## Review and Freshness

- Review status: `Pending` for WGIA-002 independent topic review.
- Review disposition: `DEFER`; no topical conclusion is approved in WGIA-001.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: the linked root, Stage 00, and machine-contract surfaces.
- Refresh triggers: purpose, gateway, JIT route, role inventory, provider shim,
  operating contract, observation commit, verdict, or source-owner change.
- Deeper evidence: hosted, provider-runtime, credential-bearing, remote, and
  live lanes remain `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
