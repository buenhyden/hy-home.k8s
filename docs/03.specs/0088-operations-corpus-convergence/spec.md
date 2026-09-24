---
title: "Operations Corpus Convergence Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0088"
---

# Operations Corpus Convergence Technical Specification (Spec)

## Overview

The request owner asked on 2026-09-25 for a full audit of the active Stage 05
corpus against the current implementation, the historical Operations surfaces
in Stage 98, and the scripts that validate them, and for the drift,
duplication, historical residue, and dead automation found to be removed in
logical local commits. This Spec owns that round.

## Strategic Boundaries & Non-goals

In scope: every document under `docs/05.operations/`; the Stage 98 units that
hold former Operations documents; `scripts/**` and the tests that are the only
consumers of code removed here; and this package.

Out of scope: any change to `gitops/`, `infrastructure/`, or `.github/`; any
frozen record, sealed ledger, or retained body; any registry profile, state, or
edge; remote branch protection; push, pull request, or merge; and any live
cluster, OpenBao, or provider action.

## Contracts

- Each Stage 05 family keeps its purpose. A Guide explains, a Policy decides
  allowed, disallowed, exception, and evidence, a Runbook orders commands,
  verification, and recovery, and an Incident or Postmortem records one real
  event. A rule or recovery path has one owning document and every other
  document links to it.
- Stage 05 states current facts that `gitops/`, `infrastructure/`, and the
  accepted ADRs support. A statement they contradict is corrected, not kept for
  history.
- The Stage 05 index is the human description of the high-risk command marker
  rule. The repository quality validator's command-boundary rules are its only
  machine owner.
- A script, branch, or helper is removed only when it has no current semantic
  consumer, no unique diagnostic, and no unique function. A test that is the
  only caller of production code is not a consumer that justifies keeping it.
- A Stage 98 unit is removed only through an approved Retention Assessment row
  under [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).

## Core Design

The round runs as ordered local commits: validation cleanup first, because the
quality validator pins Stage 05 prose; then the Stage 05 content; then this
package's evidence. Every commit passes staged QA over its exact index.

## Data Modeling & Storage Strategy

Git holds every removed byte. No redirect, compatibility copy, or recovery
ledger is added.

## Interfaces & Data Structures

`scripts/select-affected-surfaces.py` keeps only the `json` output format that
its one caller, the provider write guard, uses. No other interface changes.

## Edge Cases & Error Handling

A cleanup that would change a registry-wide invariant or a sealed-admission
path is recorded as a named deferral with its conflict and next owner instead
of being forced.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the commit. No gate, test assertion, or marker rule is
weakened to pass. A protected action becomes a handoff item.

## Verification Commands

```bash
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/qa.py staged
python3 scripts/qa.py full
git diff --check
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-OCC-001 | Each Stage 05 rule and recovery path has one owning document, and no Stage 05 document restates an `.agents` rule it can link | Review and the link gate |
| VAL-OCC-002 | Stage 05 facts agree with `gitops/`, `infrastructure/`, and the accepted ADRs | Survey recorded in the Task |
| VAL-OCC-003 | The Stage 05 marker description matches the validator's command-boundary rules, and those rules detect secret-value output regardless of flag order | Focused unit test and repository quality gate |
| VAL-OCC-004 | Each Stage 98 Operations unit is removed or kept with its current consumer, unique responsibility, and removal condition recorded | Task |
| VAL-OCC-005 | Dead or duplicate script logic with no current consumer is removed, and each retained candidate records why | Focused tests and the Task |
| VAL-OCC-006 | Staged QA passes for each commit and full QA passes on the final tree | Staged and full QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[convergence Task](tasks/tsk-0001-converge-operations-corpus.md) owns the
evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OCC-001 | Review and the link gate |
| [REQ-0004-FR-0003](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-OCC-002 | Survey recorded in the Task |
| [REQ-0004-NFR-0002](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-OCC-003 | Focused unit test and repository quality gate |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OCC-004 | Task |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OCC-005 | Focused tests and the Task |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OCC-006 | Staged and full QA |
