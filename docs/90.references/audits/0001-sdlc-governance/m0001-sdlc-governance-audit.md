---
title: "SDLC Governance Audit"
version: "0.2.0"
type: "reference/audit"
status: "published"
owner: "platform"
updated: "2026-11-06"
layer: "references"
artifact_id: "AUD-0001-m0001"
---

# Reference: SDLC Governance Audit

## Overview

This report assesses whether the repository's governance keeps Requirement,
Architecture, Spec, Plan and Task in their roles and connected, as observed on
2026-11-06 at `main` `3ec90be8`. Readers are the operator and document
authors deciding on governance changes.

## Reference Type

A dated assurance assessment. It informs SPEC-0146 (completed; summarized in the [REQ-0003 Archived Lineage](../../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage))
and the operator decisions listed under Remediation.

## Authority Boundary

This report establishes observations and findings only. Current rules live in
`.agents/governance/` and the Stage 99 registry; this report cannot approve,
accept or override them.

## Scope

The question: does the current system make each artifact's role clear, link
the artifacts both ways, gate stage transitions, control architecture change,
and say what to do when artifacts or implementation disagree? Excluded:
product manifests, live, hosted and provider-runtime behavior.

### Criteria and Inspected Surface

| Criterion | In-scope surface |
| --- | --- |
| Artifact roles and ownership | `.agents/governance/sdlc.md`, `document-lifecycle.md`, `docs/03.specs/AGENTS.md` |
| Traceability | Stage 99 `registry.json` profiles `sdlc/*` and their `body_contract` |
| Stage gates and change-kind proportionality | `sdlc.md` transitions and change-kind tables, `quality.md` |
| Architecture governance | AD and ADR templates and profiles, `sdlc.md` |
| Conflict handling | `agent-execution.md`, `work-lifecycle.md`, `document-lifecycle.md` |
| Agent instruction loading | `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.codex/`, `.agents/roles/registry.json` |

## Definitions / Facts

### Observed Evidence

| Observation | Source and input | Result |
| --- | --- | --- |
| Inventory: one flow owner (`sdlc.md`, `governance/contract`), lifecycle owner (`document-lifecycle.md`), quality owner (`quality.md`), work procedure (`.agents/workflows/work-lifecycle.md`); document form owned only by `docs/99.templates/registry.json` and its templates | Files at `3ec90be8` | Single owner per concern; provider gateways import, not copy |
| Templates exist for Requirement, AD, ADR, Spec, Plan, Task; no separate Feature Spec: the Stage 03 Spec carries both feature behavior and acceptance | `docs/99.templates/templates/{requirements,architecture,specs}/` | Present and registry-bound through `template_source` |
| Machine-checked links: Requirement → AD/Spec; AD → ADR/Spec; ADR → Spec; Spec → Requirement; Plan → Spec criterion and Task; Task → Spec criterion, with reciprocal evidence | `registry.json` `relationships.body_contract` | Enforced by `validate-markdown-profiles.py` |
| Task completion needs PASS evidence rows and one Criterion Acceptance row per criterion; acceptance is the operator's | `sdlc/task` `task_execution`, `docs/03.specs/AGENTS.md` rules 3 to 6 | Enforced, not a checkbox |
| Change kinds set proportional records: a small correction needs no package | `sdlc.md` Change kinds | Present |
| A Spec's Traceability accepts only `sdlc/requirement` sources; the template never asked for constraining AD/ADR | `sdlc/spec` profile, `spec.template.md` | Architecture → Spec exists only from the Architecture side |
| No rule said which side wins when implementation and an approved document disagree | `agent-execution.md` covers protected authority; `work-lifecycle.md` resolves contradictions at intake and stops on conflict; `context-and-memory.md` covers memory only | Partial |
| Spec template had no prompt for open questions; the "unclear Spec blocks Plan" rule was implicit in `document-lifecycle.md` (contradicting evidence returns to `in-review`) | `spec.template.md`, `document-lifecycle.md` | Partial |
| Plan template asked for architecture in Context but not for a compliance check | `plan.template.md` | Partial |
| Spec Kit, OpenSpec, Cursor rules, Copilot instructions and `AGENTS.override.md` are absent | `ls` at `3ec90be8` | Not used; nothing to align |
| Claude loads root `CLAUDE.md` and its imports; this session's context showed them loaded | This session's system context | Observed for Claude only |

### Findings and Gaps

| Finding or gap | Severity | Evidence |
| --- | --- | --- |
| F-01: A Spec need not name the Architecture Descriptions or ADRs that constrain it | P1 | `sdlc/spec` sources; template prompts |
| F-02: No rule for a divergence between implementation and an approved Requirement, Architecture or Spec | P1 | Conflict-handling rows above |
| F-03: Open questions and assumptions in a Spec have no prompt, and their effect on approval is implicit | P2 | `spec.template.md` |
| F-04: The Plan lacks an architecture compliance check prompt | P2 | `plan.template.md` |
| F-05: The ADR template does not ask for the requirement IDs it serves | P3 | `decision.template.md` |
| F-06: Codex native loading of `AGENTS.md` was not observed in this audit | UNKNOWN | No Codex session run |
| F-07: The Task validator accepted evidence-shaped rows (`EVD-###`, nine cells) inside the Task Table and then bound them as work items that could be neither deleted nor completed | P2 | Observed 2026-11-06 on an unpushed SPEC-0146 commit; strict checks PASS on the misplaced rows, then `TASK-ITEM-DELETE` and `TASK-ITEM-EDGE` refused every forward fix |

## Sources

Repository files at `main` `3ec90be8`, read on 2026-11-06. External
practice (Spec Kit, arc42, ADR) enters only through the citations `sdlc.md`
already makes; this audit added none.

## Review and Freshness

Refresh when `sdlc.md`, `document-lifecycle.md` or an `sdlc/*` profile
changes. Current truth is owned by those files, not this report.

### Remediation

| Remediation | Owner | Due or decision date |
| --- | --- | --- |
| F-01 to F-03: `sdlc.md` `Cross-artifact conformance`; Spec template prompts (SPEC-0146 WORK-001, WORK-002) | platform | Done 2026-11-06 under SPEC-0146; criteria accepted (REQ-0003 Archived Lineage, recover with `git show ca3ead4c:<path>`) |
| F-04: Plan template compliance-check prompt (WORK-002) | platform | Done 2026-11-06 under SPEC-0146 (REQ-0003 Archived Lineage) |
| F-05: ADR template requirement prompt (WORK-002) | platform | Done 2026-11-06 under SPEC-0146 (REQ-0003 Archived Lineage) |
| D-1: make the Spec → AD/ADR statement machine-checked | operator | Resolved 2026-11-06 by SPEC-0147: a required `Architecture` column in the Spec Lifecycle Traceability table; link-target and reciprocal checks were not added |
| D-2: the lifecycle gate refuses creation in `approved` or `published`, so approval and publication are separate commits | operator | Resolved 2026-11-06: drafted `f3d71d9a`, approved `4fcdf22a` |
| F-06: observe Codex loading in a Codex session | operator | Accepted deferral |
| R-1: whether a Spec's `Architecture` cell names the right AD or ADR, and F-02 and F-03, stay reviewer-judged. A link-target check would need a second typed link column in the body-contract schema, and the content is semantic | operator | Decided 2026-11-06: no automation; the semantic review in `quality.md` is the control |
| F-07: refuse a Task Table row whose ID is not a work-item ID or whose cell count differs from the header | operator | Open; needs its own Stage 03 package (executable behavior) |

Existing documents are not rewritten; the prompts reach documents through
the templates, and `sdlc.md` scopes its rules by change kind.

### Verification State

Pre-approval observations on the staged index, branch
`docs/sdlc-cross-artifact-conformance` from `3ec90be8`, 2026-11-06:

- PASS: `validate-document-contract-registry`, `validate-markdown-profiles`,
  `validate-links-and-owners` and `validate-document-lifecycle` in
  `--mode strict`, and lifecycle `--mode staged` (05:18Z).
- PASS: `unittest discover -p 'test_document*.py'` 153 OK, and
  `test_repository_form_contracts`, `test_task_execution_contract`,
  `test_task_acceptance_boundaries` 52 OK, on the bytes before the review
  fixes; the fixes touched prose only.
- PASS with fixes: an independent read-only review found one BLOCK (this
  report claimed a run it did not record) and advisories; all were fixed.
- Observed enforcement: the lifecycle gate refused `LIFECYCLE-CREATE` for
  documents created `approved` or `published`, and `TASK-PARENT-APPROVAL` for
  Task execution or evidence under a `draft` Spec. So the SPEC-0146 Task
  evidence waited for the approval commit `4fcdf22a` (D-2, resolved).
- UNKNOWN: Codex loading (F-06). Not machine-checked by decision R-1: F-02, F-03 and the content of the SPEC-0147 column; its presence is checked. Open: F-07.

These are observations, not the Task's criterion evidence or a remediation
PASS.

## Related Documents

- [Audit pack](./README.md)
- [Software Development Lifecycle](../../../../.agents/governance/sdlc.md)
- [Document Lifecycle Policy](../../../../.agents/governance/document-lifecycle.md)
- SPEC-0146 (completed; summarized in the [REQ-0003 Archived Lineage](../../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage))
