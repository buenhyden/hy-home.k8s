---
title: "Workspace Engineering External Research Refresh"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0099"
---

# Workspace Engineering External Research Refresh Technical Specification (Spec)

## Overview

Refresh the existing [workspace engineering research pack](../../90.references/research/0001-workspace-engineering/README.md) using current primary external evidence and design concrete follow-up workspace investigations. The user's direct request of 2026-09-27 authorizes this bounded documentation change and local logical commits. It does not authorize a workspace implementation audit. Origin/main was re-observed at `fc469fd139e6b92d98cc8aabeb3f3e7141f18a54`; the research worktree uses branch `codex/research-refresh`. The original checkout and its index are preserved.

## Strategic Boundaries & Non-goals

Allowed writes are the existing pack, the two Stage 90 research/reference routers when navigation requires it, this package and its Stage 03 routing entry, and explicitly disclosed current consumers of a changed research path or anchor. Read governance, templates, minimal execution history and exact link consumers solely to author and validate documents.

Excluded: changes to policies, provider/agent/skill/hook settings, CI, infrastructure, applications, manifests, scripts, tests, templates or validators; provider experiments; cluster, cloud, Vault or Argo CD access; private settings, conversation logs, memory stores, credentials or secrets; other workspaces; new packs, LLM-WIKI, root plans or duplicate ledgers; historical evidence rewrites; push, PR, merge, destructive cleanup or branch/worktree removal. The separate `0002-archive-retention-and-provenance` pack is outside scope.

## Contracts

- External findings and product/version facts need directly read primary sources. Search summaries and HTTP success alone cannot establish support. Restricted standards catalogues establish public metadata only; PDF tables/figures need screen inspection when relied upon.
- Preserve report paths, identities, existing REQ/SRC/CLM IDs and anchors, or disclose and execute an exact consumer cutover before removal. Historical dates and local observations retain their original meaning.
- Every current workspace result is `not observed in this cycle`. Repository-static document checks do not establish hosted CI, provider runtime or live behavior. Conditional priorities derive from external risk and dependencies, not discovered local defects.
- Define separate external claim judgments (`Verified`, `Partial`, `Unverified`, `DEFER`, `Contradicted`), source refresh outcomes, workspace observations and follow-up approval/evidence boundaries.
- Cover U01–U39 individually, retaining repeated original items as aliases to their shared research responsibility. Each has one primary report owner and exact section, REQ, claim/source and follow-up question mappings.
- Follow-up questions carry ID, U/REQ, external claim/source, scope, question, canonical file types, candidate selectors, required evidence, verification and acceptance, approval/risk, this-cycle result, next role and refresh trigger. Unobserved candidate paths are code literals.

## Core Design

### Structure ruling

Compare preservation with substantive rewriting, redistribution between existing members, and adding independently necessary members. Select the user-default existing pack and `m0001`–`m0013` identities with refreshed bodies and sources: the existing topic owners cover the requested scope. No new member or relocation is needed. Current external synthesis leads; dated historical provenance follows under permitted subheadings. This is a change-specific organization choice, not a new Stage 02 decision.

### Ownership interface

| Owner | Input | Output and boundary |
| --- | --- | --- |
| External researcher | Assigned topic questions and primary sources | Dated source/claim findings; no local truth or policy decisions |
| Doc writer | Returned research evidence and settled profile | Assigned member bodies; no navigation or source truth invention |
| Integration owner / wiki curator | Member evidence and exact consumers | README, shared IDs, m0012, m0013, current navigation and commits |
| Independent reviewer | Spec, final documents and source mappings | Coverage, evidence-boundary and diff review disposition |

The repository lifecycle and these canonical documents take precedence over external skill proposals for `docs/superpowers/` or a second ledger. Requested execution skills choose one actual execution method; independent research delegation and later authoring do not run duplicate work.

## Data Modeling & Storage Strategy

The pack README owns purpose, research contract, one link per report, refresh/succession and evidence limits. Topic members own synthesis and dated evidence. `m0012` owns source/claim/requirement mapping and file/section dispositions (`retain`, `reverify`, `substantive refresh`, `consolidate duplication`, `expand`, `preserve history`, `insufficient evidence`). `m0013` projects those references into scope questions without copying mutable verdicts. This Task alone owns execution evidence; Git owns recovery.

## Interfaces & Data Structures

Source records identify publisher/type, original and final URL, revision/version, publication/modification date separately from access date, directly read section/selector, supported claim IDs, limitations/conflicts and refresh trigger. Unknown exact revisions remain explicitly unknown. Each substantial topic covers definition, purpose, components, rules, management, implementation choices, trade-offs, prerequisites, failure cases, verification and exclusions, followed by workspace questions.

Topic coverage includes common instruction/context and cross-provider governance; harnesses/loops; provider-native versus custom surfaces and IDE/SDK; spec-driven SDLC, document/issue management; Diátaxis/C4/ADR/arc42/README; LLM wiki, retrieval and resource boundaries; Kubernetes/host/infrastructure/security/supply chain; delivery/Actions/hooks/QA and verification versus validation; agency-agents revision/license/roles; model/cost/limits; and memory lifecycle, poisoning and deletion. The full user topic detail remains the acceptance input; a broad heading alone does not satisfy it.

## Edge Cases & Error Handling

Inaccessible, conflicting or uncertain sources retain their exact limits and alternative primary evidence. Missing evidence remains incomplete; blanket DEFER rows cannot substitute for completed external investigation. Preserve old IDs without renumbering. Historical retired paths remain dated history and are not mechanically rewritten into current observations. Avoid broad negative support claims unless bounded by checked products, versions and sources.

## Failure Modes & Fallback / Human Escalation

Stop at the work-lifecycle repeated-failure, no-progress, unavailable-environment or authority boundary. Preserve completed findings and name the next evidence and owner. Do not relax required gates or widen scope to repair unrelated baseline defects. Remove only task-owned scratch after durable handoff; keep branch and worktree. Roll back through bounded forward reversal of this branch's reviewed paths, preserving unrelated work and IDs.

## Verification Commands

Resolve targeted commands from `scripts/validation/registry.json` and run the current QA interface:

```bash
python3 scripts/qa.py quick --root . --base-ref HEAD
python3 scripts/qa.py staged --root . --base-ref HEAD
python3 scripts/qa.py full --root . --base-ref HEAD
```

The baseline may differ per check; record it. Targeted profile/link/lifecycle checks precede quick, each exact-index staged check precedes its local commit, and final full follows final commits. Full owns unit discovery and all-files pre-commit; do not repeat them on unchanged input. Inspect both diffs, stage exact paths, validate actual commit messages and preserve active hooks.

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-WER-001 | One existing pack, correct profiles/headings/identity/lifecycle, no duplicate authority | Profile, lifecycle, navigation review |
| VAL-WER-002 | Every U01–U39 and requested topic detail has one primary owner, section, REQ, claim/source and question | m0012 individual coverage and independent review |
| VAL-WER-003 | Substantive primary-source research with current dates, product/revision limits, conflicts and historical dispositions | Member source records and m0012 dispositions |
| VAL-WER-004 | All scope questions are executable evidence contracts; workspace findings are unobserved | m0013 and member question review |
| VAL-WER-005 | Historical meaning, IDs/anchors and current consumers preserved or explicitly cut over | Link/owner checks and diff review |
| VAL-WER-006 | Ordered QA, actual-message validation, consistent local logical commits, retained branch/worktree and complete handoff | Task, command records and Git |

## Traceability

The [Plan](plan.md) owns order and risks; the [Task](tasks/tsk-0001-refresh-external-research.md) owns execution evidence. Existing completed consolidation work is history, not an active owner or a reopened package. No new durable requirement or architecture artifact is needed for this directly requested refresh.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — direct scoped user request dated 2026-09-27; no new Requirement Package | VAL-WER-001 | Profile and navigation checks |
| N/A — direct scoped user request dated 2026-09-27; U01–U39 are research aliases | VAL-WER-002 | Individual source-coverage review |
| N/A — direct scoped user request dated 2026-09-27 | VAL-WER-003 | Primary-source review |
| N/A — direct scoped user request dated 2026-09-27 | VAL-WER-004 | Scope-question contract review |
| N/A — direct scoped user request dated 2026-09-27 | VAL-WER-005 | Links, identities and provenance review |
| N/A — direct scoped user request dated 2026-09-27 | VAL-WER-006 | Ordered QA and Task evidence |
