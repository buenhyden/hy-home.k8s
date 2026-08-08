---
title: 'Audit: Workspace Purpose, Governance, and Operating Contracts'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Workspace Purpose, Governance, and Operating Contracts

## Overview

This report audits workspace purpose, roles, governance hierarchy, root and
provider entrypoints, operating contracts, and canonical-owner conflicts at
observation commit `50628b84165479b03efc0a25be075a49c91a9aef`. WGIA-002
found consistent repository-static purpose, JIT, approval, completion, and
role-owner contracts; two root README summaries conflict with those owners.

## Reference Type

Dated repository-static governance audit. It is descriptive Stage 90 evidence,
not an active policy, permission, provider, or operating-contract owner.

## Authority Boundary

Root gateways route agents into Stage 00. Stage 00 rules and machine contracts
remain authoritative for execution behavior, while the root README is the
human onboarding owner. This report identifies conflicts and provisional
remediation routes; it does not modify an active owner, redefine provider
runtime, or promote tracked configuration to runtime-consumption evidence.

## Scope

Included: repository purpose, agent roles, governance loading order, approval
and operating boundaries, provider shims, root overview consistency, and
unique current-owner routing. Excluded: canonical remediation, hosted CI,
authenticated provider execution, secrets, remote state, and live platform
behavior.

## Definitions / Facts

### Workspace Purpose

The root `README.md#overview` and
`docs/00.agent-governance/rules/bootstrap.md#core-rules` consistently define a
WSL2+k3d home-lab platform managed through Argo CD GitOps. The root README adds
the human-facing documentation-collaboration purpose and keeps external
runtime provisioning outside the repository boundary. No purpose conflict was
found in the reviewed repository-static surfaces.

### Workspace Roles

`docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles` is
the machine semantic owner and `#currentInventory` records 12 current roles,
four surfaces, and 48 unique current projections. The readable view is
`docs/00.agent-governance/harness-catalog.md#machine-contract-and-inventory-boundary`.
The split between `.agents/` local/Antigravity, `.claude/` Claude, `.codex/`
Codex, and `.gemini/` Gemini project surfaces is explicit in the machine owner
and Stage 00, although the root README summary does not preserve it.

### Operating Contracts

`docs/00.agent-governance/rules/bootstrap.md#jit-loading-sequence` owns
`bootstrap -> preflight -> persona -> scope -> provider -> progress ->
postflight`. Provider notes and the three tracked baselines either repeat that
order or delegate to bootstrap. Approval decisions route to
`rules/approval-boundaries.md#approval-matrix`; validation lanes, result terms,
completion order, and handoff fields route to
`rules/quality-standards.md#current-contract`; postflight consumes rather than
redefines those contracts.

### Canonical-owner Inventory

| Responsibility | Canonical owner | Reviewed relationship |
| --- | --- | --- |
| Human workspace purpose and onboarding | `README.md#overview` | Human index; not an agent-policy owner. |
| Agent entry and JIT order | `docs/00.agent-governance/rules/bootstrap.md#jit-loading-sequence` | Root shims route here and remain thin. |
| Execution and escalation | `docs/00.agent-governance/rules/agentic.md#current-contract` | Shared execution behavior. |
| Protected-action decisions | `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix` | Single surface-specific approval matrix. |
| Validation and handoff semantics | `docs/00.agent-governance/rules/quality-standards.md#current-contract` | Postflight and providers consume this vocabulary. |
| Role semantics and exact inventory | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory` | Machine owner for 12 roles, four surfaces, and 48 projections. |
| Readable role and capability view | `docs/00.agent-governance/harness-catalog.md#machine-contract-and-inventory-boundary` | Human projection of the machine owner. |
| Provider-specific declared behavior | `docs/00.agent-governance/providers/claude.md#current-contract`; `docs/00.agent-governance/providers/codex.md#current-contract`; `docs/00.agent-governance/providers/gemini.md#current-contract` | Repository-static behavior declarations only. |
| Provider-runtime evidence state | `docs/00.agent-governance/contracts/provider-runtime-evidence.json#providers` | Separate discovery/authenticated-run lane; no cross-lane promotion. |

### As-Is / Gap / Target Analysis

| Area | As-Is | Gap | Target |
| --- | --- | --- | --- |
| Purpose and shared operating hierarchy | Root purpose, Stage 00 JIT order, approval owner, completion owner, machine role owner, and readable catalog are consistent. | None found at repository-static depth. | Preserve the owner split and its deterministic validators. |
| Root canonical-owner summary | `README.md#canonical-owners` lists the thin `AGENTS.md` gateway as a canonical owner and omits the Stage 00 policy SSoT. | Human navigation misclassifies a route as authority. | Point the canonical-owner list to `docs/00.agent-governance/README.md`; retain root shims as entrypoints. |
| Root adapter-area summary | `README.md#top-level-areas` groups `.agents/`, `.claude/`, and `.codex/` as shared/provider runtime overlays and omits `.gemini/`. | The summary loses the local/Antigravity versus native-project split and omits a tracked current surface. | Describe `.agents/` as shared/local, `.claude/` and `.codex/` as native tracked adapters, and `.gemini/` as repo-static Gemini project-surface evidence. |
| Provider execution | Tracked adapters and repo-static validators exist; the evidence contract keeps native discovery and authenticated run unpromoted. | No authorized current provider-runtime evidence was collected by WGIA-002. | Retain `DEFER`; promote only through a separately authorized provider-runtime canary. |

### Finding Convention

Every material finding uses all fields below. Verdicts are closed to `Aligned`,
`Partial`, `Gap`, `Conflict`, `Legacy`, `Deprecated`, `One-shot candidate`, and
`DEFER`; evidence depth is closed to `repository-static`, `hosted`,
`provider-runtime`, and `live`. A missing field, unknown value, or unreviewed
claim fails closed.

#### WGA-GOV-001 — Purpose, JIT, approvals, and role-owner separation align

- **Request IDs**: `REQ-WGA-001`, `REQ-WGA-002`, `REQ-WGA-012`.
- **Scope**: workspace purpose, Stage 00 authority, JIT order, approval and completion ownership, and machine/readable role-owner separation.
- **Expected state**: human onboarding, agent policy, machine semantics, readable projections, approvals, and completion evidence have explicit non-conflicting owners.
- **Observed state**: the root and bootstrap purpose agree; seven explicit JIT consumers preserve the canonical order and Codex delegates to bootstrap; the harness contract records 12 roles, four surfaces, and 48 unique current projections; approval, quality, and postflight responsibilities are separated.
- **Evidence**: `README.md#overview`; `docs/00.agent-governance/README.md#overview`; `docs/00.agent-governance/rules/bootstrap.md#jit-loading-sequence`; `docs/00.agent-governance/rules/agentic.md#context-hierarchy-defaults`; `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/rules/quality-standards.md#current-contract`; `docs/00.agent-governance/rules/postflight-checklist.md#validation-and-refresh`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/harness-catalog.md#machine-contract-and-inventory-boundary`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: agents and reviewers can resolve shared policy and role semantics without treating a readable projection or provider shim as the machine owner.
- **Disposition**: `Keep`.
- **Canonical owner**: purpose in `README.md`; JIT in bootstrap; approvals in `approval-boundaries.md`; completion semantics in `quality-standards.md`; roles in `harness-contract.json` with `harness-catalog.md` as readable view.
- **Verification**: the corrected deterministic no-conflict probe returned `PASS explicit_jit=7/7 delegated_jit=1/1 roles=12 surfaces=4 adapters=48`; focused governance, harness, profile, and link checks remain required.
- **Uncertainty**: this verdict is limited to tracked content and deterministic local semantics; it does not cover provider consumption or live behavior.
- **Blocker**: none at repository-static depth.

#### WGA-GOV-002 — Root canonical-owner list misclassifies the Codex gateway

- **Request IDs**: `REQ-WGA-001`, `REQ-WGA-012`.
- **Scope**: root human navigation to the active agent-governance authority.
- **Expected state**: `README.md#canonical-owners` links the Stage 00 policy SSoT as authority and treats `AGENTS.md` only as a thin Codex/GPT entrypoint.
- **Observed state**: the canonical-owner list names `AGENTS.md` but omits `docs/00.agent-governance/README.md`; the gateway and its provider note explicitly say policy and role semantics live in Stage 00 and the machine contract.
- **Evidence**: `README.md#canonical-owners`; `AGENTS.md#agentsmd`; `docs/00.agent-governance/README.md#overview`; `docs/00.agent-governance/providers/agents-md.md#gateway-integrity-rules`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Conflict`.
- **Impact**: a human following the canonical-owner list can mistake a routing shim for the policy authority and miss the exhaustive Stage 00 governance index.
- **Disposition**: `Correct` provisionally; WGIA-009 must admit the roadmap row before WGIA-010 changes the owner.
- **Canonical owner**: `README.md#canonical-owners` for the stale summary; `docs/00.agent-governance/README.md#overview` for agent-policy authority.
- **Verification**: the pre-edit contradiction probe returned `THIN_GATEWAY_AS_CANONICAL_OWNER`; target validation must require the Stage 00 link while keeping all three root gateways thin and reachable.
- **Uncertainty**: none for the tracked text conflict; the exact wording of the later human-facing correction remains a content-review choice.
- **Blocker**: WGIA-009 admission and independent review precede canonical remediation.

#### WGA-GOV-003 — Root adapter-area summary omits and misclassifies current surfaces

- **Request IDs**: `REQ-WGA-002`, `REQ-WGA-012`.
- **Scope**: root overview of current tracked agent adapter roots.
- **Expected state**: root navigation distinguishes `.agents/` shared/local Antigravity ownership from provider-native tracked roots and includes the current `.gemini/` project surface without claiming runtime use.
- **Observed state**: `README.md#top-level-areas` groups `.agents/`, `.claude/`, and `.codex/` as shared assets and provider runtime overlays, omits `.gemini/`, and therefore disagrees with the four-surface machine inventory and the explicit Gemini boundary.
- **Evidence**: `README.md#top-level-areas`; `GEMINI.md#geminimd`; `docs/00.agent-governance/README.md#current-adapter-surface-matrix`; `.agents/GEMINI.md#purpose`; `docs/00.agent-governance/providers/gemini.md#gemini-cli-native-surface`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Conflict`.
- **Impact**: the primary human overview can conceal a tracked current adapter surface and blur the evidence boundary between local/shared assets and provider-native project configuration.
- **Disposition**: `Correct` provisionally in the same root-owner remediation unit as WGA-GOV-002.
- **Canonical owner**: `README.md#top-level-areas` for the stale summary; the harness contract and Stage 00 adapter matrix for current classification.
- **Verification**: the pre-edit contradiction probe returned `GEMINI_NATIVE_SURFACE_OMITTED`; target checks must see all four surface classes and retain the repo-static-only qualification for `.gemini/`.
- **Uncertainty**: native Gemini discovery, event delivery, authentication, and model resolution remain outside this tracked-summary correction.
- **Blocker**: WGIA-009 admission and independent review precede canonical remediation.

#### WGA-GOV-004 — Provider discovery and authenticated consumption remain unverified

- **Request IDs**: `REQ-WGA-002`, `REQ-WGA-012`.
- **Scope**: native provider discovery, authentication, instruction loading, hook delivery, role consumption, and model resolution.
- **Expected state**: repository-static adapter presence never promotes a provider-runtime claim without an authorized observation or canary.
- **Observed state**: the provider evidence contract records repository-static surfaces separately; native discovery and authenticated execution remain `DEFER`, with the dated Gemini installation/discovery observation recorded as `ABSENT` rather than inferred from `.gemini/` files.
- **Evidence**: `docs/00.agent-governance/contracts/provider-runtime-evidence.json#providers`; `docs/00.agent-governance/contracts/harness-contract.json#evidenceClasses`; `docs/00.agent-governance/providers/claude.md#qa-evidence-resolution`; `docs/00.agent-governance/providers/codex.md#qa-evidence-resolution`; `docs/00.agent-governance/providers/gemini.md#qa-evidence-resolution`; `docs/00.agent-governance/rules/quality-standards.md#handoff-evidence-contract`.
- **Evidence depth**: `provider-runtime`.
- **Verdict**: `DEFER`.
- **Impact**: no audit or remediation may claim effective provider instruction, permission, hook, role, authentication, or model behavior from the tracked adapters alone.
- **Disposition**: `Keep` the evidence separation; no runtime action is authorized by WGIA-002.
- **Canonical owner**: `docs/00.agent-governance/contracts/provider-runtime-evidence.json#providers` for provider evidence state; provider-native runtime for any future observed behavior.
- **Verification**: require one separately authorized, provider-specific canary identity and result before changing this verdict; repository-static harness checks cannot close it.
- **Uncertainty**: all effective provider consumption and authentication behavior in this task.
- **Blocker**: provider-runtime access and explicit authorization are absent.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-GOV-001 | human index | `README.md#overview`; `README.md#canonical-owners`; `README.md#top-level-areas` | Workspace purpose and the two contradicted root summaries. |
| SRC-WGA-GOV-002 | policy owner | `docs/00.agent-governance/README.md#overview`; `docs/00.agent-governance/README.md#current-adapter-surface-matrix`; `docs/00.agent-governance/rules/bootstrap.md#jit-loading-sequence` | Policy authority, current adapter classification, and JIT owner. |
| SRC-WGA-GOV-003 | policy owner | `docs/00.agent-governance/rules/agentic.md#context-hierarchy-defaults`; `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/rules/quality-standards.md#current-contract`; `docs/00.agent-governance/rules/postflight-checklist.md#validation-and-refresh` | Execution, approval, validation, result, and handoff responsibility split. |
| SRC-WGA-GOV-004 | machine owner | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/contracts/harness-contract.json#evidenceClasses` | Exact role inventory and evidence-class separation. |
| SRC-WGA-GOV-005 | machine owner | `docs/00.agent-governance/contracts/provider-runtime-evidence.json#providers` | Provider observation and runtime verdict state. |
| SRC-WGA-GOV-006 | human index | `docs/00.agent-governance/harness-catalog.md#machine-contract-and-inventory-boundary`; `AGENTS.md#agentsmd`; `GEMINI.md#geminimd`; `.agents/GEMINI.md#purpose` | Readable role projection and gateway/local-adapter boundaries. |
| SRC-WGA-GOV-007 | policy owner | `docs/00.agent-governance/providers/agents-md.md#gateway-integrity-rules`; `docs/00.agent-governance/providers/claude.md#qa-evidence-resolution`; `docs/00.agent-governance/providers/codex.md#qa-evidence-resolution`; `docs/00.agent-governance/providers/gemini.md#qa-evidence-resolution` | Thin-gateway and provider evidence boundaries. |

## Review and Freshness

- Review status: `Approved` by independent specification and quality reviews.
- Review disposition: four bounded findings and one reviewed provisional
  roadmap input are accepted as dated audit evidence; WGIA-009 owns admission
  and WGIA-010 owns any canonical-owner correction.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: the linked root, Stage 00, and machine-contract surfaces.
- Refresh triggers: purpose, gateway classification, root canonical-owner or
  top-level-area summary, JIT route, role inventory, provider shim/evidence,
  operating contract, observation commit, finding verdict, or review change.
- Deeper evidence: hosted, provider-runtime, credential-bearing, remote, and
  live lanes remain `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
