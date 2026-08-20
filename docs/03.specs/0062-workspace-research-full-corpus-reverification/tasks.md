---
title: 'Workspace Research Full-Corpus Reverification Task'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-20
artifact_id: "TASK-0062"
---

# Workspace Research Full-Corpus Reverification Task (Task)

## Overview

This Task is the execution ledger for `WRFR-000` through `WRFR-009` in the
reciprocal [Plan](plan.md), implementing [Spec 0062](spec.md). Direct human
approval on 2026-08-20 activates the standalone execution relation. The
activation commit is `docs: activate full-corpus research reverification`.
`WRFR-001` has completed closed-corpus evidence intake and allocation; the
current next owner is `WRFR-002`.

The target is a 2026-08-20 external-source and workspace reverification of all
thirty-six existing `REQ-WERPC-*` owners, integrated into the existing
`2026-08-08-wer` pack. `WRFR-001` is complete: guarded checker construction and
direct review, artifact-inventory initialization and recovery, immutable
baseline capture, five reviewed closed-corpus reports, exact-union validation,
and final ID allocation all completed in the ignored SDD workspace. No remote
GitHub query or tracked research/integration implementation has occurred, and
no successor work package has staged or committed execution work.

## Inputs

- [Spec 0062](spec.md)
- [Plan](plan.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [Research collection contract](../../90.references/research/README.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)

### Approved design baseline

| Field | Baseline |
| --- | --- |
| Canonical research pack | `docs/90.references/research/2026-08-08-wer/` |
| Pack Markdown files | 14 |
| Request owners | 36, exact IDs `001..036` |
| Source IDs | 90, terminal `SRC-WERPC-090` |
| Claim IDs | 135, terminal `CLM-WERPC-012-04` |
| New source start | `SRC-WERPC-091` |
| New claim block | `CLM-WERPC-013-NN`, starting `01` |
| Matrix states | 23 `Verified`, 1 `Verified gap`, 12 `Partial` |
| Evidence date | 2026-08-20 |
| Execution branch | `codex/2026-08-20-full-corpus-reverification` |
| Design commit | `60b1c89e38ae6a72d6cbde7e74bd580604e3a80c` |

### Closed workstream assignment

| Workstream | Exact request IDs | Topical owners |
| --- | --- | --- |
| Agent engineering | 001, 002, 026–032 | harness/loop, agents, model, memory |
| Provider/common | 003–006 | workspace governance, provider status |
| SDLC/documentation | 007, 010–021, 034–036 | SDLC/contracts, Diataxis, LLM-WIKI |
| Platform/security | 008, 009, 025 | Kubernetes/infrastructure/security |
| Delivery/quality | 022–024, 033 | CI/CD, Actions, QA, V&V |

The union is exact and disjoint. Research agents may write only their ignored
structured report. They may not edit repository files, allocate final IDs,
stage, or commit.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WRFR-000 | VAL-WRFR-012, 013 | Activate standalone lifecycle and SDD workspace | platform | Done | Activated by direct approval on 2026-08-20 in `docs: activate full-corpus research reverification` | Active standalone Spec/Plan/Task relation; next owner `WRFR-001` |
| WRFR-001 | VAL-WRFR-001..007, 009 | Freeze baseline, collect five read-only reports, allocate IDs | platform + research agents | Done | Exact 36-row union validated; all report reviews approved; one source and six claims allocated | Registered reports and allocation; next owner `WRFR-002` |
| WRFR-002 | VAL-WRFR-002..005, 008, 013 | Integrate agent engineering findings | agent integrator | Queued | Not executed | Next owner; reviewed agent report and allocation slice ready |
| WRFR-003 | VAL-WRFR-002..005, 008, 013 | Integrate provider/common findings | provider integrator | Queued | Not executed | Awaiting reviewed provider report/allocation |
| WRFR-004 | VAL-WRFR-002..005, 008, 013 | Integrate SDLC/documentation findings | documentation integrator | Queued | Not executed | Awaiting reviewed SDLC report/allocation |
| WRFR-005 | VAL-WRFR-002..005, 008, 013 | Integrate platform/security findings | platform/security integrator | Queued | Not executed | Awaiting reviewed platform report/allocation |
| WRFR-006 | VAL-WRFR-002..005, 008, 011, 013 | Integrate delivery/quality and read-only GitHub evidence | delivery/security integrator | Queued | Not executed | Pre-remote security review required |
| WRFR-007 | VAL-WRFR-006..010, 013 | Integrate source, claim, scope, and pack projections | sole ledger integrator | Queued | Not executed | Awaiting all five topical commits |
| WRFR-008 | VAL-WRFR-008, 010, 013 | Reconcile indexes, links, lifecycle, and progress | documentation integrator | Queued | Not executed | Awaiting terminal parsed counts |
| WRFR-009 | VAL-WRFR-010, 012..015 | Run terminal lanes, whole-branch review, closure, cleanup | platform + QA | Queued | Not executed | Awaiting WRFR-008 |

## Approval and Safety Boundaries

- **Allowed Paths**: the exact files listed under each Plan work package, this
  Plan's unique ignored SDD workspace returned from the guarded helper-Plan
  alias, and exact temporary alias
  `/tmp/0062-workspace-research-full-corpus-reverification-plan.md`.
- **Forbidden Paths**: any new research directory or topic report; policy,
  manifest, workflow, application, runtime, credential, secret, primary-checkout
  staged RIA, sibling worktree, sibling SDD workspace, and unlisted `/tmp` path.
- **Shared helper marker**: `.superpowers/sdd/.gitignore` is validated as exact
  helper state and restored to its recorded initial state. An initially absent
  marker is removed only when no foreign sibling exists; otherwise cleanup stops
  fail-closed without deleting foreign state or claiming completion.
- **Approval Required**: written Plan approval before WRFR-000; pre-remote
  security approval before any GitHub query; human finishing choice before push,
  merge, publication, branch deletion, or worktree cleanup.
- **External Research**: read-only official/primary-source retrieval; search is a
  locator and never substitutes for reading the source.
- **Remote GitHub**: exactly the nine Plan allowlisted metadata classes, at most
  once each, through the guarded checker; no dispatch, rerun, approval, merge,
  settings mutation, raw logs, tokens, or secret-bearing data.
- **Static Validation**: task-local closed-corpus checker, domain validators,
  document registry, Markdown profiles, links/owners, RIA, affected/staged lanes,
  aggregate quality, pre-commit, all-files, formatter review, and diff checks.
- **Live Validation**: `DEFER`; no live cluster, infrastructure, provider runtime,
  deployment, user, operator, or stakeholder activity is authorized.
- **Secret / Vault Handling**: no secret value, token, credential, raw workflow
  log, Vault payload, or recovery material may be read, printed, or stored.
- **Rollback Plan**: revert the exact logical commit for a tracked work package;
  no remote or live state exists to roll back. Guarded ignored artifacts remain
  available until their final consumer and are then removed with exact-path
  absence proof.
- **Evidence Location**: durable results in this Task, pack owners, source/claim
  ledger, scope index, Stage 03 index, ADR 0022, and durable progress; transient
  reports/review packages in this Plan's ignored SDD workspace only.

### WRFR-001 one-time inventory recovery amendment

Direct review changed the registered checker and appended its evidence to the
registered Task 2 report. Because the inventory binds immutable files through
device, inode, size, `mtime_ns`, `ctime_ns`, and SHA-256, truncating the report
back to its bound 32217-byte prefix cannot restore its former `ctime_ns` and is
forbidden. The sole recovery is the Plan-defined
`artifact-rebind-checker-review` command. It has no target argument and may
replace only the existing `full-corpus-check.py` and `task-2-report.md` records,
at the same two indices, in one inventory CAS.

Before fresh direct review, the controller must complete steps 1–3 below. Step
4 then obtains the required approvals. All four steps must complete before any
stateful recovery; after the report is frozen in step 2, direct-review approval
evidence goes only to mutable `progress.md`:

1. summarize all post-registration Task 2 review evidence in mutable
   `progress.md`;
2. append this amendment and final recovery-review evidence to
   `task-2-report.md`, capture its approved SHA-256, and freeze that report
   permanently;
3. record the exact inventory SHA-256, old checker SHA-256, approved new checker
   SHA-256, old report SHA-256
   `75f08066115632b145d7f210f6de4ab91029b180a5923c9337272c35893afa0b`,
   and approved frozen-report SHA-256;
4. obtain fresh Python and security direct approval for the amended tracked
   contract, exact checker bytes, full normal/optimized self-test output, and
   frozen report identity.

The stateful command is authorized only after those approvals. It validates
the exact inventory path/digest/schema, both old records, both guarded new
targets, every other immutable artifact's complete registered FileVersion, and
both mutable entries. It replaces exactly two same-index records, uses the old
complete inventory FileVersion for CAS, re-reads both targets before and after
CAS, postvalidates the exact new inventory, and rolls back exact old inventory
bytes only against the exact CAS-returned new FileVersion. Concurrent update or
rollback failure is preserved and fails closed. `artifact-register` remains
unchanged, duplicate registration remains rejected, no generic report rebind
exists, and all later WRFR-001 evidence goes only to mutable `progress.md`.

### WRFR-001 evidence intake completion

The exact final registered artifact identities are:

| Artifact | SHA-256 |
| --- | --- |
| `research-agent-engineering.json` | `f0dd1038b056d3f2bdc5e6c5e457e4f3c6cd93cdd5ab75375780101da9eca5b1` |
| `research-provider-common.json` | `bf5728c6d4f69dce90cff533058372e243ffed28ed5b5ee8949444212250ce86` |
| `research-sdlc-documentation.json` | `be273b3dad1b6b4f50d12285cf9114406ba5c3af94ded7646a71ceda5b47ae85` |
| `research-platform-security.json` | `edff89e3b29fdcaa658044ffc768b7c297e39a02936bd39657c90bb759a7fbce` |
| `research-delivery-quality.json` | `f55cc2285577530544c48f26fb497184b43bb9822236e46a736294ed8695d993` |
| `allocation.json` | `04025a6ecc56853d773bac598e2c8895a408a2d6a9252be9727f4264c50fe40b` |
| `artifact-inventory.json` | `39ef8f41848340daf9a0756a80611bcb549960080fc4bb5c8007a4ce625c8567` |

All five final source-fidelity reviews returned `Approved`. The final
cross-workstream quality review returned `Approved` with
Critical/Important/Minor `0/0/0`. The reports contain exactly 36 disjoint rows:
external results are 3 `changed`, 32 `unchanged`, and 1 `unreachable`; workspace
results are 29 `confirmed`, 6 `drifted`, and 1 `absent`; dispositions are 20
`Verified`, 4 `Verified gap`, and 12 `Partial`.

The allocation contains the sole new source `SRC-WERPC-091` for
`REQ-WERPC-009`; claims `CLM-WERPC-013-01..03` belong to
`REQ-WERPC-011..013`, and claims `CLM-WERPC-013-04..06` belong respectively to
`REQ-WERPC-008`, `009`, and `025`. The exact workstream slices remain those in
the closed assignment above. There is no duplicate, gap, reservation, or new
request owner.

The registered NASA SWE-047 traceability URL was unavailable for
`REQ-WERPC-033`; that row remains `Partial`/`human-judgement` and adopts no new
traceability claim from the failed retrieval. The official GitHub Environments
URL was unavailable for `REQ-WERPC-022` and `023`; neither row adopts an
environment claim from it. The sole out-of-ledger source observation accepted
for allocation is the official K3s v1.35 release-family page for
`REQ-WERPC-009`, with live-cluster and patch-suitability inferences rejected.

The immutable baseline retains row 020's originally observed legacy selector.
Validation normalizes only that observation to the real `#ditaxis-baseline`
anchor. Every report row must include its normalized baseline selector;
additional exact owner selectors remain permitted. `validate-research` and
`residue` both passed after allocation registration. The frozen Task 2 report
remains SHA-256
`bb5e198e7c99a7c510296d12cf9c7f94eb8af4eed4ea9a6eedec91e085379598`
and was not appended.

### Stop conditions

Execution stops only for a destructive or irreversible action, a
security-sensitive action not already approved, an external side effect such as
push/merge/publication, or a Plan defect that leaves every path forward a guess.
All other conflicts receive a recorded SDD ruling and continue under the Spec.

## Verification Summary

WRFR-000 activation and WRFR-001 evidence intake are complete. Initial design
evidence included:

- isolated worktree created from clean tracked `HEAD`;
- primary checkout's unrelated staged RIA files excluded from the branch;
- pre-authoring `bash scripts/validate-repo-quality-gates.sh .` passed;
- strict document registry passed with 538 paths after Spec indexing;
- strict Markdown profiles reported zero violations;
- strict cross-document links and owners passed;
- design commit `60b1c89e38ae6a72d6cbde7e74bd580604e3a80c` contains only Spec 0062 and the Stage 03 index entry.

WRFR-001 then validated the immutable `14/36/90/135` baseline, five registered
reports and their exact 36-row union, the final allocation, and whole-workspace
artifact residue. These results prove the closed-corpus public-source and
repository-static intake only. They do not prove remote GitHub state, provider
runtime, hosted CI, live infrastructure, or user validation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-WRFR-001](spec.md) | Done for intake | The checker validated the exact `001..036` report union |
| [VAL-WRFR-002](spec.md) | Intake passed; integration pending | All 36 rows carry closed external and repository-static evidence fields |
| [VAL-WRFR-003](spec.md) | Done | The five registered reports retain the exact closed workstream assignment |
| [VAL-WRFR-004](spec.md) | Intake review passed; integration pending | All report-local reviews and the cross-report quality review approved the registered bytes |
| [VAL-WRFR-005](spec.md) | Intake passed; integration pending | Baseline-selector membership and evidence-depth boundaries passed guarded validation |
| [VAL-WRFR-006](spec.md) | Intake passed; ledger integration pending | All rows use the closed outcome vocabulary and passed checker validation |
| [VAL-WRFR-007](spec.md) | Intake passed; ledger integration pending | Every row carries a valid blocking-class disposition combination |
| [VAL-WRFR-008](spec.md) | Not executed | WRFR-002..008 own the existing-owner append-only contract |
| [VAL-WRFR-009](spec.md) | Allocation passed; ledger integration pending | WRFR-001 allocated source 091 and claims 013-01..06 without gaps or duplicates |
| [VAL-WRFR-010](spec.md) | Not executed | WRFR-007..009 own the shared projection sequence |
| [VAL-WRFR-011](spec.md) | Not executed | WRFR-006 and WRFR-009 own the nine-class remote/security contract |
| [VAL-WRFR-012](spec.md) | Workspace passed; cleanup pending | WRFR-001 residue validation passed; WRFR-009 still owns exact cleanup |
| [VAL-WRFR-013](spec.md) | In progress | This WRFR-001 evidence commit precedes controller-owned post-commit review |
| [VAL-WRFR-014](spec.md) | Not executed | WRFR-009 owns the whole-branch review gate |
| [VAL-WRFR-015](spec.md) | Not executed | WRFR-009 owns the terminal lane sequence |

### Related Documents

- [Spec 0062](spec.md)
- [Plan](plan.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [ADR 0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Durable progress ledger](../../00.agent-governance/memory/progress.md)
