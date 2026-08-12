---
title: 'Task: Workspace Engineering Research Pack Consolidation'
type: sdlc/task
status: done
owner: platform
updated: 2026-08-09
artifact_id: "TASK-053"
---

# Task: Workspace Engineering Research Pack Consolidation

## Overview

This Task records execution and review evidence for the ten WERPC work
packages that replace three dated research packs with one source-backed
`2026-08-08-wer` pack. Rows advance only after the logical commit, required
repository-static gates, implementation report, specification review, and
quality review are accepted.

External source observations are dated evidence, not live provider or platform
proof. No hosted CI, provider-runtime, remote, credential-bearing, secret-value,
or live-cluster result is produced or claimed.

## Inputs

- **Specification**:
  [Spec 053](spec.md)
- **Plan**:
  [Workspace Engineering Research Pack Consolidation Implementation Plan](plan.md)
- **Standalone execution decision**:
  [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Predecessor specification**: `Spec 017` at
  `docs/03.specs/017-workspace-engineering-research-pack/spec.md`
- **Conflicting program**: `Spec 052` at
  `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- **Approved requirement source**: direct 2026-08-08 human request and explicit
  Spec 053 approval in the current Codex task
- **Design commit**: `37c714d04e1ab20816f2719fdc09f6dc42acef72`
- **Execution branch base**: `37c714d04e1ab20816f2719fdc09f6dc42acef72`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WERPC-000 | VAL-WER-008, VAL-WER-011 | Activate reciprocal execution and supersede only WDTC-002/WORK-002 | platform | Done | Active reciprocal lifecycle is recorded; WDTC-002/WORK-002 is superseded to Spec 053 and WERPC-008; all required focused, diff, and repository quality checks passed before this logical commit | Design commit; strict registry, Markdown profile, and links/owners checks; repository quality gate; optional all-files pre-commit INTERRUPTED/SKIP with required-gate fallback; self-review; this logical commit |
| WERPC-000A | VAL-WER-008, VAL-WER-011 | Add typed direct-approval standalone execution lineage without changing program lineage | platform | Done | Closed schema-v8 relation, parser projection, structural/link/eligibility diagnostics, ADR-0022, exact-pair terminal eligibility, disjoint rendered execution graphs, and bounded post-closure ADR handling are implemented without changing existing program-lineage semantics | RED/GREEN mutation history remains in the progress ledger. Final staged evidence: registry self-test 132 cases and strict 501 paths; standalone link fixture 8 cases and full links self-test/strict PASS; eligibility 58 cases and production PASS; residue closure 25 cases and production PASS with frozen guards 13/29; affected unit tests 2/2 PASS; Markdown profiles and cached diff PASS; complete repository quality gate PASS; Python and governance reviews Approved. |
| WERPC-001 | VAL-WER-001, VAL-WER-002, VAL-WER-003 | Create exact pack shape, coverage matrix, source register, and predecessor disposition baseline | docs-researcher | Done | Created the exact thirteen-file pack with REQ-WERPC-001 through REQ-WERPC-032, one primary file-and-heading owner per request, current workspace evidence, three dated predecessor source-register entries, 25 full-hash file dispositions, and 35 text-exact H3 split rows | Exact 13/25 counts, Markdown profiles, strict registry, strict links/owners, diff check, full repository quality gate, self-review, and this logical commit |
| WERPC-002 | VAL-WER-004, VAL-WER-005, VAL-WER-006, VAL-WER-007 | Research governance, harness, loop, Claude, Codex, and common environment | docs-researcher | Done | Three detailed references define the harness/loop machine, workspace control plane, and Claude/Codex surface matrix; ten dated official primary-source rows and nine bounded claim rows distinguish static configuration, native discovery, and authenticated/runtime evidence; the collection index and README inventory contract include the new pack | Fresh-review RED: strict links/owners reported 26 collection-index omissions. Fix-round RED: the full gate exposed the missing new-pack README inventory row. GREEN: exact 13-file tree/table projections, active54/new7 README contract, Markdown profiles, registry self-test/strict, strict links, harness semantics, Reference IA production, cached diff, and the full repository gate PASS; documentation and Python fresh reviews Approved; this logical commit. |
| WERPC-003 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research spec-driven SDLC, document families, Diátaxis, and LLM-WIKI | docs-researcher | Done | Three references record dated primary-source support, a complete document-family matrix, Diátaxis scope rules, LLM-WIKI generator/drift boundary, and a Release absence finding; `SRC-WERPC-014`–`022` and `CLM-WERPC-003-01`–`13` preserve claim limits | Source/claim audit, Markdown profiles, registry self-test/strict, strict links, LLM-WIKI check, Reference IA production, cached diff, and complete repository quality gate PASS; fresh review Approved with no finding; this logical commit |
| WERPC-004 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research Kubernetes, infrastructure, GitOps, and security | docs-researcher | Done | Primary-source and repository-static analysis is complete: layered platform/trust-boundary model, control/evidence matrix, As-Is/gap/target matrix, and deferred-validation backlog; `SRC-WERPC-023`–`034` and `CLM-WERPC-004-01`–`11` preserve source, claim, and evidence-depth limits | Focused worktree diff, Markdown profiles, strict links/owners, and harness validation PASS; fresh content review Approved with no finding; exact staged Reference IA, cached diff, and complete repository quality gate PASS; hosted CI, remote/live, secret, credential, and cluster evidence remain DEFER; this logical commit. |
| WERPC-005 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research CI/CD, GitHub Actions, and QA | quality-engineer | Done | Static delivery/QA analysis, five-workflow control inventory, lane/failure/evidence taxonomy, security/supply-chain boundary, and adoption matrix are complete; `SRC-WERPC-035`–`044` and `CLM-WERPC-005-01`–`10` preserve source and evidence limits | Actions security, CI Python contract, affected-surface, Markdown profile, strict links/owners, and worktree diff checks PASS; fresh review Approved with no finding; exact staged Reference IA, cached diff, and complete repository quality gate PASS; hosted CI, branch/ruleset, secret, artifact, OIDC, deployment, remote, and live evidence remain DEFER; this logical commit. |
| WERPC-006 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research AI agents, pinned agency-agents, model routing, and memory tiers | docs-researcher | Done | Three references separate local static roster/model/memory contracts from provider/runtime evidence; the Agency Agents comparison is pinned to `ebe9c99acb5c96f9468de368d8bead775387d1a7`; `SRC-WERPC-045`–`052` and `CLM-WERPC-006-01`–`08` record limits | Focused diff/profile/strict-link/harness-semantics/model-fitness checks PASS; fresh review Approved; full-gate RED for two upstream script URLs misclassified as local paths was fixed by one pinned upstream-directory link; exact staged Reference IA, cached diff, and complete repository gate PASS; no provider execution, install, credential, remote, hosted, or live action occurred; this logical commit. |
| WERPC-007 | VAL-WER-008, VAL-WER-010, VAL-WER-011 | Migrate links, observations, indexes, machine contracts, validators, and fixtures | platform | Done | Current research navigation, RIA/agent/active-corpus contracts, validators, schemas, projections, fixtures, templates, Guide 0010, and mutable historical links are migrated; RIA-protected audit bytes remain exact and their future predecessor targets require a fail-closed sourceCommit/byte/disposition proof | Initial RIA RED: 88 tests with 10 failures/1 error; initial agent cutover RED: 37 tests with one fixture error; protected-link RED: expected no finding but got `LINK-BROKEN`; the pre-review harness attempt exposed the phase-bounded README fixture cardinality RED. Fresh review found the production disposition-header mismatch and inherited Git configuration; exact production-table and hostile-config probes failed before their fixes. The final gate then exposed closure source/current identity drift and a stale-currentness hit in the predecessor migration ledger; exact projection refresh plus a parser-gated, single-file transition exception closed them without widening to the other 24 predecessor files. GREEN: isolated staged RIA 88/88 and direct validator, agent cutover 37/37, active-corpus 19/19, registry self-test/strict, links strict/self-test, archive validation, hardened Git boundary, exact-delete-clone strict links, Python compile, cached diff, complete repository quality gate, and complete harness PASS; exact occurrence closure 732 lines/70 files and 70 reviewed rows. Three README fixture rows remain only for exact pre-deletion active54 equality and must be removed atomically in WERPC-008; Python and QA re-reviews Approved; this logical commit. |
| WERPC-008 | VAL-WER-003, VAL-WER-008, VAL-WER-009, VAL-WER-010 | Prove readiness and delete the 25 predecessor files | platform | Done | The exact 25 tracked predecessor files and three now-empty roots are deleted without redirects; the surviving pack remains exactly 13 files; README/RIA/agent-cutover contracts are settled to the post-deletion state while sourceCommit provenance remains | Pre-gate exact25, RIA, strict links/owners, and archive PASS; three root-absence checks and exact13 shape PASS; README active51/retired23 contract; RIA production and one staged 88/88 run PASS; agent cutover self-test/production PASS; links self-test/strict PASS; complete repository gate and harness PASS. Later optional unit reruns encountered only environment-dependent FIFO `Errno 95` and one load-sensitive 1.5-second bound and are not claimed as PASS; required lanes passed; this logical commit. |
| WERPC-009 | VAL-WER-001–012 | Run final audit/review/cleanup and close reciprocal lifecycle | supervisor | Done | All twelve criteria have deterministic terminal evidence; Spec/Plan/Task, indexes, and standalone execution state are reciprocal `done`; no Stage 98 or scratch residue was introduced | Exact 13/32/25/35/52/51 counts; 49 current source rows dated 2026-08-08; 12/12 reference source/freshness sections; post-deletion 732-line/66-file classification equality; three absent roots; closure RED `CLOSURE-AUTHORITY-SCOPE` for Spec 053 followed by an exact one-path allowlist/test GREEN; archive, harness, and required full gate PASS; fresh whole-branch read-only review Approved; optional all-files pre-commit INTERRUPTED/SKIP at strict repository quality after earlier hooks passed and no worktree mutation; this logical closure commit |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/**` except existing `docs/98.archive/**` records;
  `scripts/**` and `tests/**` only for path-contract and fixture migration
- **Forbidden Paths**: existing `docs/98.archive/**` records, `gitops/**`,
  `infrastructure/**`, `traefik/**`, `policy/**`, ignored credential/secret
  state, user stashes, and paths outside the isolated worktree
- **Approval Required**: any live, hosted, remote, credential-bearing,
  secret-reading, push, merge, publication, third-party mutation, or change to
  active runtime/provider/platform behavior
- **Static Validation**: focused commands in each Plan task and
  `bash scripts/validate-repo-quality-gates.sh .` before every commit
- **Live Validation**: `DEFER` — not authorized and not required for this
  descriptive research pack
- **Secret / Vault Handling**: no secret value, token, kubeconfig, ignored
  credential file, Vault payload, or provider credential is read or printed
- **Rollback Plan**: one logical commit per row; WERPC-008 is the isolated
  deletion commit; Git history retains the predecessor content
- **Evidence Location**: this Task, the new source/migration ledger, the
  progress ledger, Git commits, and the SDD ledger review packages

## Verification Summary

The specification and design commit are approved. WERPC-000 is done:
`python3 scripts/validate-document-contract-registry.py --root . --mode strict`,
`python3 scripts/validate-links-and-owners.py --root . --mode strict`,
`git diff --check`, and `bash scripts/validate-repo-quality-gates.sh .` passed
on the final pre-commit tree. The optional `pre-commit run --all-files` attempt
was interrupted after it stalled and rewrote only detect-secrets metadata in
`.secrets.baseline`; that incidental change was restored exactly and the
optional lane is `SKIP`, not `PASS`. The passing required strict, diff, and full
repository gate results are the fallback evidence. The results are
repository-static only; provider-runtime, hosted CI, remote, and live
validation remain `DEFER`.
WERPC-001 is done with the thirteen-file shape, request-owner matrix, dated
predecessor source-register interface, 25 full-hash file dispositions, and 35
text-exact H3 split rows. It does not claim external currentness: later topical
work must recheck predecessor URLs. Its strict registry, strict links/owners,
and full repository quality-gate results are repository-static only.
WERPC-000A implements the approved typed standalone-execution contract without
changing `programLineage`. Registry, links/owners, eligibility, residue closure,
the affected unit tests, Markdown profiles, cached diff, and the complete
repository quality gate passed on the final reviewed staged tree.
WERPC-002 is done: its source ledger has official, dated primary sources with
refresh triggers and claim boundaries; the topical references retain `DEFER`
for native discovery, authenticated/runtime, hosted CI, remote, and live
claims. The collection-index and README-inventory REDs were closed without
changing the immutable baseline, and both fresh reviews plus the final staged
Reference IA and complete repository quality gate passed. The attempted
Reference IA `--staged` variant is recorded as an inapplicable-mode `SKIP`; the
Plan's production `--root .` command passed. WERPC-003 is done: its nine dated
source rows and thirteen bounded claim rows support the complete document-family
matrix, Release absence gap, Diátaxis mapping, and LLM-WIKI boundary. Fresh
review returned Approved with no finding, and Reference IA production plus the
complete repository quality gate passed on the exact staged tree. WERPC-004 is
done: its 12 dated source rows and 11 bounded claims cover the
platform hierarchy, GitOps/secret trust boundaries, static-versus-runtime
controls, and As-Is/gap/target matrix. Focused checks passed, fresh content
review was Approved with no finding, and Reference IA production plus the
complete repository quality gate passed on the exact staged tree. All
remote/live/secret evidence remains `DEFER`.
WERPC-005 is done: its dated source/claim registers and current workflow/QA
analysis passed focused validation, fresh review returned Approved with no
finding, and Reference IA production plus the complete repository quality gate
passed on the exact staged tree. It does not promote repository-static workflow
evidence to hosted CI, administration, credential, artifact, OIDC, deployment,
remote, or live evidence. WERPC-006 is done: its exact Agency Agents pin, eight
dated sources, and eight bounded claims distinguish role/model/memory static
contracts from provider/runtime behavior. Focused checks passed, fresh review
was Approved, the upstream-script-path RED was corrected, and Reference IA plus
the complete repository gate passed on the exact staged tree. WERPC-007 is
implemented and ready for fresh review: its exact tracked occurrence inventory
is 732 lines across 70 files, every hit has one reviewed classification row,
and focused RIA, agent-cutover, active-corpus, registry, link, archive, compile,
and diff validations pass. RIA production was first proven in an isolated
clone. A migration reviewer later staged the exact 53-file scope while proving
index authority; cached scope/diff checks and the actual staged RIA 88/88 plus
direct validator pass, with no forbidden diff. Its unrequested harness and
full-gate starts were interrupted with exit 130 and are not PASS evidence. The
pre-review harness attempt exposed and led to restoration of the
three phase-bounded README fixture rows; its focused registry self-test now
passes. Fresh review then found and closed the production disposition-header
and inherited Git-configuration defects; an exact-delete clone passes strict
links, and Python plus QA re-review are Approved. The controller then audited
and replaced an over-broad 25-file currentness exception with the reviewed
exact disposition parser and a single predecessor-ledger exception, refreshed
the exact active-corpus closure identities, and reran both the complete
repository quality gate and full harness successfully. WERPC-007 is done.
WERPC-008 is done: all 25 enumerated predecessor files and the three empty
directories are absent, the new pack remains exactly 13 files, all 25
dispositions are completed, and post-deletion README, RIA, and agent-cutover
contracts pass the required repository-static gates. WERPC-009 closes the
reciprocal lifecycle: deterministic audit confirmed exact 13 pack files, 32
unique request-owner rows, 52 source rows, 51 bounded claim rows, 25 completed
file dispositions, 35 split dispositions, three absent predecessor roots, zero
Stage 98 branch diff, no tracked temporary/scratch residue, no unsupported
deep-evidence success claim, and 11 logical pre-closure
implementation commits. The post-deletion occurrence table exactly matches 732
lines across 66 files. Required repository-static validation passed with
strict links/owners, Reference IA, archive validation, harness, and the complete
repository quality gate. The first terminal harness run exposed
`CLOSURE-AUTHORITY-SCOPE` for newly done Spec 053; an exact-set unit test
reproduced the missing post-closure authority, and the bounded one-path registry
addition made the targeted test, closure self-test, production closure check,
and full harness pass without accepting any unknown Spec. The optional
all-files pre-commit run passed its early
hooks but was interrupted at the long-running strict repository-quality hook;
it is `SKIP`, not `PASS`, and made no worktree change. Push, merge, PR creation,
worktree removal, hosted CI, provider-runtime, remote, credential, secret, and
live validation remain outside the approved scope.

### Terminal Acceptance Matrix

| Criterion | Result | Deterministic terminal evidence |
| --- | --- | --- |
| VAL-WER-001 | PASS | The tracked successor pack contains exactly 13 files: one README and twelve declared references. |
| VAL-WER-002 | PASS | The README contains 32 sequential, unique request rows; every row has one linked primary owner and one nonempty workspace-evidence cell. |
| VAL-WER-003 | PASS | The ledger contains 25 unique file dispositions with full 40-hex source commits and 35 reviewed section-split rows. |
| VAL-WER-004 | PASS | The source register has 52 rows; SRC-WERPC-004–052 are 49 current rows with URLs, 2026-08-08 checks, adopted/rejected scopes, and refresh triggers; all twelve references expose Sources and Review and Freshness sections. |
| VAL-WER-005 | PASS | The 32 requirement states and 51 claim rows use only the five-state vocabulary and retain repository evidence plus uncertainty boundaries. |
| VAL-WER-006 | PASS | Provider and common-environment references keep Claude, Codex, shared static controls, native discovery, authentication, and runtime evidence as separate surfaces. |
| VAL-WER-007 | PASS | The 32-owner matrix covers every requested harness, loop, SDLC/document, documentation, platform, delivery, security, agent, model, and memory topic. |
| VAL-WER-008 | PASS | Current navigation and machine consumers route to the successor; strict links/owners and RIA pass; every remaining predecessor-token line is classified by an exact 732-line/66-file table. |
| VAL-WER-009 | PASS | All 25 predecessor files and all three roots are absent; the successor remains exactly 13 files; residue scan found no task-created scratch artifact. |
| VAL-WER-010 | PASS | The branch diff contains zero `docs/98.archive/**` path changes and archive validation passes. |
| VAL-WER-011 | PASS | Eleven logical commits before closure, eleven work-package SDD reports, and one bounded WERPC-002 fix report preserve per-unit evidence and review history. |
| VAL-WER-012 | PASS | Fresh whole-branch review is Approved and required Reference IA, strict links, archive, harness, diff, and complete repository-static quality gates pass; deeper evidence remains DEFER. |

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WERPC-000](plan.md#work-breakdown) | Done. | Active Spec/Plan/Task and collection indexes; bounded PRD-008/AD-0011 exception; superseded WDTC-002/WORK-002 route; required strict, diff, and repository-quality checks passed; optional all-files pre-commit INTERRUPTED/SKIP with required-gate fallback; self-review. |
| N/A — WERPC-000A shares the Plan and Spec sources above | Done. | Typed standalone execution, exact-pair/approval/owner/state/overlap/terminal tests, bounded closure authority, two independent reviews, and the complete repository quality gate PASS. |
| N/A — WERPC-001 shares the Plan and Spec sources above | Done. | Exact thirteen-file pack; 32 unique request-primary-owner rows; three dated predecessor source entries; 25 file rows with matching full source commits; 35 text-exact H3 split dispositions; strict registry, strict links/owners, cached diff, and full repository quality gate PASS on the staged tree. |
| N/A — WERPC-002 shares the Plan and Spec sources above | Done. | Dated source/claim ledger (SRC-WERPC-004–013; CLM-WERPC-002-01–009); detailed harness/loop, provider-surface, and common-control-plane references; exact 13 tree/row collection projections; active54/new7 README inventory contract with baseline67/active47/retired20 preserved; documentation and Python fresh reviews Approved; final Reference IA production and complete repository quality gate PASS. |
| N/A — WERPC-003 shares the Plan and Spec sources above | Done. | Three detailed references; `SRC-WERPC-014`–`022` and `CLM-WERPC-003-01`–`13`; complete family matrix with Release absence gap; Diátaxis partial application/tutorial-explanation gap; LLM-WIKI generator/schema/drift/freshness and llms.txt/MCP/search/RAG boundaries; fresh review Approved; final Reference IA production and complete repository quality gate PASS. |
| N/A — WERPC-004 shares the Plan and Spec sources above | Done. | `SRC-WERPC-023`–`034`, `CLM-WERPC-004-01`–`11`, platform/security reference, REQ-WERPC-008/009/025 status cells, focused checks PASS, fresh content review Approved, and final staged Reference IA/cached-diff/complete quality gate PASS. |
| N/A — WERPC-005 shares the Plan and Spec sources above | Done. | CI/CD/GitHub Actions/QA reference, REQ-WERPC-022–024 coverage status, `SRC-WERPC-035`–`044`, and `CLM-WERPC-005-01`–`10`; focused checks PASS; fresh review Approved; exact staged Reference IA/cached diff/complete quality gate PASS. |
| N/A — WERPC-006 shares the Plan and Spec sources above | Done. | Three detailed references; fixed Agency Agents source pin `ebe9c99acb5c96f9468de368d8bead775387d1a7`; `SRC-WERPC-045`–`052`; `CLM-WERPC-006-01`–`08`; focused checks PASS; fresh review Approved; upstream-path RED fixed; staged Reference IA/cached diff/complete quality gate PASS. |
| N/A — WERPC-007 shares the Plan and Spec sources above | Done. | RED/GREEN migration evidence; RIA-protected historical-link proof with valid and fail-closed negative fixtures; 732/70 exact occurrence closure and 70-row classification; isolated staged RIA 88/88 plus direct validator; agent 37/37; active corpus 19/19; registry self-test/strict; links strict/self-test; exact production disposition parse and post-delete clone; hardened Git hostile-config probe; archive validation; Python compile; cached diff; complete repository gate; and full harness PASS. The three phase-bounded README fixture rows remain until atomic WERPC-008 deletion. Python and QA re-reviews Approved; this logical commit. |
| N/A — WERPC-008 shares the Plan and Spec sources above | Done. | Exact25 pre-gate; three absent predecessor roots; exact13 surviving pack; completed 25-row disposition table; README active51/retired23; RIA production; agent-cutover self-test/production; links self-test/strict; archive; cached diff; complete repository gate; and full harness PASS. Optional filesystem-sensitive unit reruns are recorded honestly and do not replace the passing required lanes; this logical commit. |
| N/A — WERPC-009 shares the Plan and Spec sources above | Done. | VAL-WER-001–012 criterion walk, exact13/32/52/25 counts, three absent roots, zero Stage 98 diff, no tracked residue, no unsupported deep-evidence PASS claim, strict links/owners, Reference IA, archive, harness, complete quality gate, lifecycle/index/registry `done` transition, and branch-finishing handoff. |
