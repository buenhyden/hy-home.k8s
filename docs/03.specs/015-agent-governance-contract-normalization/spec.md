---
title: 'Agent Governance Contract Normalization Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-04
---

# Agent Governance Contract Normalization Technical Specification (Spec)

## Overview

This document defines the design for normalizing the AI-agent governance,
provider-adapter, and validation surfaces in `hy-home.k8s`. The target surfaces
are the root provider shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`),
provider runtime directories (`.agents/`, `.claude/`, `.codex/`), GitHub control
and CI surfaces (`.github/`), and the canonical governance stage
(`docs/00.agent-governance/`).

The work keeps the repository's existing architecture: Stage 00 owns durable
agent governance; `.agents/` owns provider-neutral shared assets; provider
adapters expose native runtime files and wiring; validators and CI close the
feedback loop.

## Strategic Boundaries & Non-goals

This spec owns the design for a single normalization pass across agent
governance, provider adapters, and QA/CI enforcement.

In scope:

- Resolve contradictions, duplicated policy, old wording, and ambiguous
  frontmatter or section contracts in the target surfaces.
- Keep root provider shims thin and route durable policy to Stage 00 owners.
- Preserve provider-native capability differences instead of forcing one
  provider's metadata model onto every adapter.
- Align hooks, CI, PR templates, and repository validators with the documented
  governance contract where deterministic checks are reasonable.
- Record external official-source basis for Claude, Codex, Gemini, and GitHub
  Actions capability boundaries.

Out of scope:

- Changing live k3d, ArgoCD, Vault, ESO, or Kubernetes resources.
- Creating a new provider runtime family.
- Replacing the current docs stage taxonomy or template routing model.
- Rewriting non-target SDLC, operations, reference, or archive documents except
  when they must be touched for direct traceability or validation evidence.
- Claiming live runtime readiness from repo-static validation.

## Related Inputs

- **PRD**: No separate PRD exists for this governance normalization pass. The
  upstream requirement is the approved user request to normalize the target
  AI-agent governance, frontmatter, section, contract, provider-adapter, QA,
  and CI/CD surfaces.
- **ARD**: No separate ARD exists. The architectural baseline is the current
  Stage 00 canonical core plus provider-adapter model.
- **Related ADRs**: No new ADR is required unless implementation discovers a
  provider capability decision that changes the architecture rather than merely
  documenting the current contract.

Official capability basis:

- Codex custom instructions with `AGENTS.md`:
  <https://developers.openai.com/codex/guides/agents-md>
- Codex subagents:
  <https://developers.openai.com/codex/subagents>
- Codex CLI and configuration:
  <https://developers.openai.com/codex/cli>
- Claude Code settings:
  <https://code.claude.com/docs/en/settings>
- Claude Code hooks:
  <https://code.claude.com/docs/en/hooks>
- Claude Code subagents:
  <https://code.claude.com/docs/en/sub-agents>
- Gemini CLI commands and hierarchical memory:
  <https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md>
- GitHub Actions:
  <https://docs.github.com/en/actions>

Repository inputs:

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/common-governance.md`
- `docs/00.agent-governance/harness-catalog.md`
- `docs/00.agent-governance/harness-implementation-map.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/providers/*.md`
- `docs/00.agent-governance/rules/*.md`
- `.github/workflows/ci.yml`
- `.agents/hooks.json`, `.claude/settings.json`, `.codex/hooks.json`
- `scripts/validate-repo-quality-gates.sh`

## Contracts

- **Config Contract**: Root shims stay frontmatter-free and thin. Stage 00
  owns durable policy. Provider runtime baselines own provider-specific loading
  order, hook behavior notes, and validation expectations without duplicating
  long policy bodies.
- **Data / Interface Contract**: Provider agent definitions remain
  provider-native: Claude uses Markdown frontmatter with native `tools:`;
  Gemini uses `.agents/agents/*.md` as Gemini-tier agent reference indexes;
  Codex uses `.codex/agents/*.toml` with `model` and
  `model_reasoning_effort`.
- **Governance Contract**: Capability parity is role parity, not identical key
  parity. The same role, scope imports, guardrails, handoff, and postflight
  expectations must be preserved across providers, while native metadata
  syntax may differ.

## Core Design

- **Component Boundary**:
  - Governance Core: `docs/00.agent-governance/**`, root shims, provider
    notes, harness catalog, subagent protocol, common governance, and model
    policy.
  - Provider Adapters: `.agents/**`, `.claude/**`, and `.codex/**`, including
    agent definitions, runtime baselines, hooks wiring, skills, workflows, and
    output styles.
  - Validation & Automation: `.github/**`, shared hook scripts, repository
    validators, CI workflow, PR template, and validation evidence surfaces.
- **Key Dependencies**:
  - `docs/99.templates/support/template-routing.md` for authored document
    route ownership.
  - `docs/00.agent-governance/rules/documentation-protocol.md` for language,
    template, README, and memory ledger coupling.
  - `scripts/validate-repo-quality-gates.sh` as the primary repo-static gate.
- **Tech Stack**:
  - Markdown and TOML provider-adapter files.
  - JSON hook wiring for Claude, Codex, and Gemini surfaces.
  - GitHub Actions YAML for CI.
  - Shell and Python-backed repository validation scripts.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Treat each governance document as a contract surface with one canonical
    owner.
  - Treat each provider adapter as a projection of the canonical contract into
    provider-native syntax.
  - Treat hooks, validators, and CI workflow files as enforcement projections,
    not independent policy owners.
- **Migration / Transition Plan**:
  - Inventory contract drift before edits.
  - Normalize Stage 00 owner language first.
  - Normalize provider adapters second.
  - Normalize validation and GitHub control surfaces third.
  - Commit each logical unit separately with validation evidence.

## Interfaces & Data Structures

### Core Interfaces

```text
Official capability
-> Stage 00 canonical contract
-> Provider adapter surface
-> Hook / CI / QA validation
-> Memory and task evidence
```

The interface is document-to-document traceability rather than a software API.
Every durable rule must have exactly one canonical owner, and every adapter or
automation surface must point back to that owner.

## API Contract (If Applicable)

This work exposes no external API. No `api-spec.md`, OpenAPI, GraphQL, or
protobuf contract is required.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Governance/documentation implementer with review support from
  subagents when useful.
- **Inputs**: User request, Stage 00 governance, provider adapter files,
  GitHub control surfaces, repository validators, and official external
  provider documentation.
- **Outputs**: Normalized governance contracts, aligned provider adapters,
  validation updates where needed, README/index updates where affected, and
  progress evidence.
- **Success Definition**: The repository has a consistent, provider-aware
  agent governance contract that passes repo-static validation and clearly
  separates native provider capabilities from behavioral mirrors.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - Repository search and inspection with `rg`, `sed`, and Git commands.
  - File edits via patch-based changes.
  - Validation through repository shell scripts, JSON/TOML/YAML parsing, and CI
    workflow inspection.
  - Optional subagents for independent audit/review tasks.
- **Permission Boundary**:
  - No live cluster mutation.
  - No secret value inspection.
  - No remote push, publish, or third-party mutation without explicit approval.
- **Failure Handling**:
  - If an official source contradicts current repo wording, update the
    canonical Stage 00 contract before touching adapters.
  - If a validator cannot deterministically enforce a rule, document the
    boundary and keep manual validation evidence in the task/progress record.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Agents must load the root shim for their
  provider, then Stage 00 bootstrap, scope, provider note, progress ledger, and
  postflight checklist just in time.
- **Policy Constraints**: Durable policy belongs in Stage 00, template support,
  operations policy, or the owning stage document. README files and root shims
  summarize and route; they do not own full contract bodies.
- **Versioning Rule**: Capability claims tied to vendor behavior must carry a
  source basis and freshness note when they are changed.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Use the active spec, implementation plan, and task
  record once implementation begins.
- **Long-term Memory**: Update
  `docs/00.agent-governance/memory/progress.md` for repo-changing work and
  reusable lessons.
- **Retrieval Boundary**: Do not store secrets, credentials, private runtime
  databases, or unredacted token material in memory.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Confirm target documents are in scope before editing.
  - Read the owning canonical contract before changing an adapter.
  - Use official external sources for provider capability assertions.
- **Output Guardrails**:
  - Keep root shims thin.
  - Keep `.github` Markdown control files frontmatter-free.
  - Keep README sections consistent with the repository README contract.
  - Avoid creating duplicate policy sections in README or provider adapter
    files.
- **Blocked Conditions**:
  - Missing route/template mapping for a new authored document.
  - Validator failures that cannot be classified as optional-tool skips.
  - A provider capability claim that cannot be supported by repository or
    official external evidence.
- **Escalation Rule**:
  - Ask the human before changing branch strategy, deleting work, pushing,
    publishing, mutating third-party resources, or changing credentials.

## Evaluation (If Applicable)

- **Eval Types**:
  - Structural validation: frontmatter, README, link, route, JSON/TOML/YAML,
    provider mirror, and hook wiring checks.
  - Contract validation: targeted scans for duplicate policy ownership,
    provider capability drift, legacy wording, and stale CI/QA claims.
  - Review validation: final spec/compliance and quality review of the
    normalized surfaces.
- **Metrics**:
  - Required repository gates pass.
  - No active target file retains unsupported legacy frontmatter keys or
    duplicated policy sections.
  - Provider adapter parity is explicit and capability-aware.
  - Validation evidence records optional-tool skips separately from failures.
- **Datasets / Fixtures**:
  - Target repository files listed in this spec.
  - Official provider documentation links in Related Inputs.
  - Existing repository validators and CI workflow.
- **How to Run**:
  - Run the verification commands in this spec and focused scans defined in
    the implementation task record.

## Edge Cases & Error Handling

- **Provider-native mismatch**: If one provider supports a native control and
  another only supports behavioral wiring, document the difference in the
  capability matrix instead of forcing identical metadata keys.
- **Historical evidence noise**: Progress ledger history may intentionally
  contain older terms. Active-target scans should classify history separately
  from current contract drift.
- **GitHub-native Markdown**: `.github/ABOUT.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/SECURITY.md` remain
  frontmatter-free even though they are active control surfaces.
- **Optional tool absence**: Missing optional tools such as `kube-linter` or
  `conftest` are not failures when validators provide documented fallback or
  skip evidence.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Stage 00 documents disagree about canonical ownership.
  **Fallback**: Update the owner document first, then update summaries and
  adapters.
  **Human Escalation**: Required only if the owner cannot be determined from
  repo evidence.
- **Failure Mode**: Provider documentation has changed since the current
  repository baseline.
  **Fallback**: Update the provider-specific note and capability matrix with a
  source freshness note.
  **Human Escalation**: Required when the change would remove an expected local
  runtime surface.
- **Failure Mode**: A validator needs broad new behavior beyond deterministic
  text/structure checks.
  **Fallback**: Keep the rule documented and add focused scans or manual
  evidence first.
  **Human Escalation**: Required before adding heavyweight dependencies or
  network-dependent CI gates.

## Verification Commands

```bash
git diff --check
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

Additional focused checks should include:

```bash
python3 -m compileall scripts >/tmp/hy-home-k8s-compileall.log
python3 - <<'PY'
from pathlib import Path
import tomllib
for path in sorted(Path('.codex/agents').glob('*.toml')):
    tomllib.loads(path.read_text())
PY
```

YAML workflow parsing, provider mirror scans, and official-source freshness
checks should be recorded in the implementation task evidence when those
surfaces change.

## Success Criteria & Verification Plan

- **VAL-AGC-001**: Stage 00 documents identify a single canonical owner for
  governance rules, provider capability parity, subagent protocol, model tiers,
  hooks, QA, CI/CD, and memory.
- **VAL-AGC-002**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` remain
  frontmatter-free thin gateways and do not duplicate durable policy bodies.
- **VAL-AGC-003**: `.agents`, `.claude`, and `.codex` adapters preserve role
  parity while representing provider-native metadata accurately.
- **VAL-AGC-004**: `.github` control surfaces remain GitHub-native and
  frontmatter-free while reflecting canonical QA/CI and security owners.
- **VAL-AGC-005**: Repository validation gates pass, and any optional-tool
  limitation is explicitly recorded.
- **VAL-AGC-006**: Repo-changing work is recorded in the canonical progress
  ledger and each logical work unit is committed separately.

## Related Documents

- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Bootstrap Governance**: [../../00.agent-governance/rules/bootstrap.md](../../00.agent-governance/rules/bootstrap.md)
- **Common Governance**: [../../00.agent-governance/common-governance.md](../../00.agent-governance/common-governance.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Harness Implementation Map**: [../../00.agent-governance/harness-implementation-map.md](../../00.agent-governance/harness-implementation-map.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Spec Template**: [../../99.templates/templates/sdlc/specs/spec.template.md](../../99.templates/templates/sdlc/specs/spec.template.md)
- **Plan**: `../../04.execution/plans/2026-07-04-agent-governance-contract-normalization.md`
- **Tasks**: `../../04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
