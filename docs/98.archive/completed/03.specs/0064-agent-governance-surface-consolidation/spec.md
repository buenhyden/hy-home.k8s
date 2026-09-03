---
title: 'Agent Governance Surface Consolidation Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-08-30
artifact_id: "SPEC-0064"
---

# Agent Governance Surface Consolidation Technical Specification (Spec)

## Overview

The four agent-governance surfaces must state only what is currently true, with
one owner per fact. This Spec covers `docs/00.agent-governance/`, `.agents/`,
`.claude/` and `.codex/`: 98 tracked files audited on six axes, being
duplication, contradiction, legacy reference, orphaned artifact, gate and
fixture excess, and commit-pin density.

Direct human approval on 2026-08-30 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

The audit produced three defects and rejected eight candidates. The rejected
candidates are part of the deliverable: a sweep that is not corrected reports
noise as fact, and this execution records why each was dropped.

## Strategic Boundaries & Non-goals

The eight rejected candidates are out of scope and are not to be changed. They
are the seven responsibility documents against twelve registry roles, which
`roles/README.md` declares a router rather than a roster; the nine Stage 00
contracts, each of which has a consumer; `post-validate-runner-result.py`,
invoked by `post-validate.sh`; `infrastructure/tests/verify-contracts-static.sh`,
which exists; the `.claude/skills` and `.codex/skills` symlinks, which preserve a
single owner; the four gateway files, which carry no duplicated policy; and the
stale paths inside the progress ledger body, which `memory/README.md` protects.

Spec 0054 retains the remainder of its approved progress-owner retirement. Only
the ledger artifact transfers here, and the transfer is recorded in both.

Provider runtime behavior is out of scope. This execution changes repository
state only and proves nothing about native discovery, hook delivery, or
authenticated operation.

## Contracts

- `.agents/registry.json` and `.agents/contracts/agent-registry.schema.json` own
  role semantics and provider projection.
- `docs/99.templates/registry.json` owns profiles, lifecycle domains, and
  standalone execution relations.
- `scripts/document_lifecycle.py` refuses a governed Markdown deletion that no
  sealed migration admits.
- `scripts/validate-links-and-owners.py` composes redirects from generic
  migration documents in `_historical_migration_proof`.
- ADR-0030 places full archive content in Git history rather than in a tracked
  body copy.

## Core Design

Three defects are corrected, each at the owner that states the wrong fact.

The progress ledger contradicts itself. `memory/README.md` states that the
directory retains historical context pending disposition and that new-work
status must not be appended, while the ledger's own header instructs the reader
to use the progress template for new entries and names
`docs/00.agent-governance/harness-catalog.md` as current runtime truth. That file
was removed. The ledger is 19086 lines and holds 232 of the 234 commit pins
across all four surfaces; the other three surfaces hold none.

The ledger is retired to a minimal Stage 98 tombstone. Its body is not copied:
ADR-0030 makes Git history the full-content archive, and the tombstone carries
only the recovery coordinates. Twelve documents link the ledger, of which eight
are terminal and cannot be edited, so the sealed migration row must make the
legacy path resolve before the file is deleted.

`.agents/skills/ops-runbook/skill.md` instructs an agent to save output under
`docs/05.operations/playbooks/`, which does not exist. Only
`docs/05.operations/runbooks/` is owned, so the alternative is removed rather
than created.

`.codex/rules/` holds one `.gitkeep` and is referenced nowhere. It is removed.

## Data Modeling & Storage Strategy

MIG-0007 is a `content/archive-migration` document with one ledger row whose
`legacy_path` is the retired ledger and whose recovery coordinates are its
source commit, source blob, and content digest. The row is the redirect source
that keeps the eight terminal links resolvable, and the recovery proof that the
938 KB body remains reachable from Git after deletion.

## Interfaces & Data Structures

The migration document keeps the three sections its profile admits, being
Overview, Migration Ledger, and Recovery. Any additional block is an H3 under
Recovery. The document is created in `draft` and sealed in a separate change,
because a migration may only be created mutable and `LIFECYCLE-DELETE` reads
only sealed rows.

## Edge Cases & Error Handling

Eight of the twelve inbound links come from terminal Spec and Plan documents
whose bytes are fixed. If the sealed row does not make the legacy path resolve,
those links break with no repair path, because the citing documents cannot be
edited. The redirect is therefore proved against the link validator before the
deletion is staged, not after.

The four remaining inbound links are Stage 90 audit references in `draft`, which
are mutable and are repointed to the tombstone.

## Failure Modes & Fallback / Human Escalation

If the redirect cannot be proved, WP-002 stops and the ledger stays in place
with its contradiction corrected but its body retained; the residual is reported
rather than forced. Deleting a governed artifact whose citations cannot resolve
is not a trade this execution may make on its own.

## Verification Commands

- `bash scripts/validate-repo-quality-gates.sh .`
- `python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'`
- `python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry`
- `python3 scripts/validate-document-lifecycle.py --root . --mode strict`

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-AGS-001 | The diagnosis records every finding and every rejected candidate with the machine fact that decided it |
| VAL-AGS-002 | The progress ledger is retired to a minimal Stage 98 tombstone that keeps its recovery coordinates, and no inbound link breaks |
| VAL-AGS-003 | No surface instructs an agent to write to a path the repository does not own |
| VAL-AGS-004 | No tracked artifact in the four surfaces is unreferenced by any consumer |
| VAL-AGS-005 | Gate and full suite pass in a clean checkout at the branch tip |

## Traceability

This Spec has no PRD or AD. Its authority is the direct human approval recorded
in `## Overview`.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — standalone, direct approval | VAL-AGS-001 | Diagnosis table reviewed against the cited commands |
| N/A — standalone, direct approval | VAL-AGS-002 | Link validator run before and after deletion, with counts recorded |
| N/A — standalone, direct approval | VAL-AGS-003 | Cited paths resolved against the tracked tree |
| N/A — standalone, direct approval | VAL-AGS-004 | Consumer sweep re-run with full paths after correction |
| N/A — standalone, direct approval | VAL-AGS-005 | Gate and suite output recorded in the reciprocal Task |

### Related Documents

- [Plan](./plan.md)
- [Task](./tasks/tsk-0001-ags-000.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR 0030 — authority-first SDLC and agent governance convergence](../../../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
