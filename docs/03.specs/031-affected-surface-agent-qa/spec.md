---
title: 'Affected Surface and Agent QA Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-14
---

# Affected Surface and Agent QA Technical Specification (Spec)

## Overview

This Spec creates one affected-surface-to-validator contract and aligns local
hooks, pre-commit, AI-agent obligations, provider gateways, and CI selectors
with it. It closes the gap where repository validators consume paths that the
current CI and agent feedback loops do not select.

## Strategic Boundaries & Non-goals

This tranche owns validation selection, execution lanes, evidence vocabulary,
and shared agent QA semantics. It does not force provider adapters into one
syntax, claim provider runtime availability from files, or replace protected-
surface domain validators owned by Spec 032.

## Contracts

- **Config Contract**:
  `docs/00.agent-governance/contracts/validation-surfaces.json` maps changed
  path patterns to required validators and lanes and validates against the
  adjacent `validation-surfaces.schema.json`. It uses the same normalized POSIX
  exact-or-anchored-regex path semantics as Spec 026. Local and CI selection
  must have positive and negative fixtures derived from this owner.
- **Data / Interface Contract**: Validation results use PASS, SKIP, FAIL, or
  DEFER. The owning Task records scope, changed paths, acceptance IDs, commands,
  tool/version, per-lane result, limitations, reviewer, rollback, residual risk,
  and next owner as defined by
  [`quality-standards.md`](../../00.agent-governance/rules/quality-standards.md).
- **Governance Contract**: AI agents run affected-file checks during work,
  staged checks before commit, all-files plus domain checks before completion,
  and record independent review for protected changes.

## Core Design

- **Component Boundary**: Path registry, selector script, pre/post edit hooks,
  pre-commit configuration, CI path filter/jobs, Stage 00 validation rules,
  root provider shims, local `.agents` roles, and Claude/Codex native adapters. Within
  workflows this Spec owns changed-path detection, selector outputs, and job
  selection only; Spec 032 owns Action identity, permissions, and protected
  domain behavior.
- **Key Dependencies**: Strict document validation from Spec 029 and migrated
  paths from Spec 030. After Spec 030 strict cutover, every program-created
  authored document must add its exact fourteen-column row to the durable
  [Document Migration Evidence Ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
  in the same creation commit; validator or ledger coverage must not be weakened
  to admit an unaccounted path.
- **Tech Stack**: JSON contract, repository scripts, pre-commit, GitHub Actions,
  shared role fixtures, and surface-specific Markdown/TOML/settings formats.

Validation lanes:

- `affected`: changed paths and directly required fast checks.
- `staged`: standard pre-commit file hooks.
- `all-files`: all applicable file hooks plus repository quality.
- `message/manual`: commit-message and explicit manual stages, recorded
  separately from `--all-files`.
- `ci`: deterministic jobs selected from the affected-surface contract.
- `remote/live`: separately approved evidence; unavailable lanes remain DEFER.

The registry explicitly covers tracked `_workspace/README.md`, `.gitignore`, `.env.example`,
root configs, Stage 00/99, provider gateways, `.github`, `gitops`,
`infrastructure`, `policy`, `scripts`, `secrets`, tests, and Traefik.
Ignored `_workspace/**` scratch children are never Git changed-path inputs and
must not trigger CI; only the tracked boundary README and ignore contract do.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: `ValidationSurface` declares path patterns,
  local validators, CI jobs, protected level, fallback, and evidence lane.
  `AgentRoleContract` declares responsibility, outputs, prohibited actions,
  stop conditions, handoffs, and capability tier.
- **Migration / Transition Plan**: Add registry and selector fixtures, align
  local hooks, align CI filters/jobs, update shared roles and provider gateways,
  then remove duplicated path conditions.

## Interfaces & Data Structures

### Core Interfaces

```json
{
  "id": "repository-document-contract",
  "routes": [
    {"kind": "regex", "value": "^docs/.*$"},
    {"kind": "exact", "value": "_workspace/README.md"},
    {"kind": "exact", "value": ".gitignore"}
  ],
  "validators": ["document-contract", "repository-quality"],
  "ciJobs": ["repo-quality-static"]
}
```

## Edge Cases & Error Handling

- `pre-commit run --all-files` does not prove `commit-msg` or `manual` stages;
  run and report those separately when applicable.
- A hook with no matching files is SKIP, not PASS.
- Missing optional tools report tool SKIP and fallback PASS/FAIL independently.
- Normalize tracked changed paths exactly as Spec 026; reject `..`, leading
  `./`, case aliases, symlink traversal, and first-match precedence.
- Provider discovery, entitlement, remote CI, and live state cannot be inferred
  from adapter files and remain separate evidence lanes.
- A surface-specific adapter file may have different syntax while still being required
  to express the same role semantics.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: A changed path selects no validator or local and CI
  selections disagree.
- **Fallback**: Fail the selector fixture and repair the canonical mapping; do
  not silently run a generic subset.
- **Human Escalation**: New tool permissions, provider defaults, model promotion,
  or remote/live authority require a separate approved decision and evaluation.

## Verification Commands

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
pre-commit run --all-files
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Every protected and validator-consumed path has positive and
  negative local/CI selector fixtures; uncovered paths are zero.
- **VAL-SPC-002**: `pre-commit --all-files`, message/manual stages, repository
  quality, and domain gates are described and evidenced without scope overclaim.
- **VAL-SPC-003**: Shared/local and provider-native agent surfaces reject missing or
  wrong responsibility, output, prohibited action, stop, or handoff semantics.
- **VAL-SPC-004**: Duplicate path conditions in hooks, Stage 00 prose, and CI are
  removed or checked as generated/consuming views of the canonical registry.
- **VAL-SPC-005**: Workflow edits preserve the responsibility handoff: this
  tranche owns selectors/job routing, while Spec 032 owns Action references,
  permissions, and protected domain steps.

### Implementation Status

ASQA-001 through ASQA-006 are complete. The Stage 00 lane/result/handoff
contract, thin provider routing, repository quality orchestration, and
cross-surface role semantics are aligned. The machine owner is
`agent-role-semantics` v2 with `adapterSurfaces = [local, claude, codex]`; this
preserves the completed 480-case result without treating `.agents/**` as
Gemini CLI native evidence. Independent reviewer agent
`/root/review_adm006_adm007_conflict` approved lifecycle closure with
`C0/H0/M0/L0`; remote CI, native provider consumption, credentials, secrets,
and live infrastructure remain `DEFER` for their separately authorized owners.

## Traceability

### Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Migration Spec**: [Authored Document Migration](../030-authored-document-migration/spec.md)
- **Audit**: [CI, QA, Automation, Pipeline, and Workflow](../../90.references/audits/2026-07-11-weia/ci-qa-automation-pipeline-workflow.md)

### Delivery and References

- **Implementation Plan**: [Affected Surface and Agent QA Implementation Plan](../../04.execution/plans/2026-07-12-affected-surface-agent-qa.md)
- **Execution Task**: [Affected Surface and Agent QA Task](../../04.execution/tasks/2026-07-12-affected-surface-agent-qa.md)
- **Next Spec**: [Protected Surface and Supply Chain Hardening](../032-protected-surface-supply-chain-hardening/spec.md)
- **pre-commit Semantics**: [pre-commit documentation](https://pre-commit.com/)
- **Agent Governance**: [Harness Catalog](../../00.agent-governance/harness-catalog.md)
