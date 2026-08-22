---
title: 'Audit: LLM-WIKI, Memory, and Knowledge Management'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: LLM-WIKI, Memory, and Knowledge Management

## Overview

This report audits deterministic LLM-WIKI knowledge routing and the exact four
memory classes at observation commit
`50628b84165479b03efc0a25be075a49c91a9aef`. Starting implementation commit
`d56f2c3429065e9c4642028f905dfcf2a9f748a7` has no LLM-WIKI, generator,
memory-policy, lifecycle, checkpoint, closure-contract, or generated-output
drift from the observation; its relevant current drift is prior WGIA progress
and document-contract fixture documentation only.

## Reference Type

Dated repository-static knowledge and memory audit. It is not a knowledge
router, generator, generated index, memory policy, checkpoint writer, provider
store, runtime readiness claim, or remediation approval.

## Authority Boundary

The LLM-WIKI README owns link-map boundaries, the generator owns generated
bytes, canonical target documents own their content, and Stage 00 contracts own
memory semantics. This report did not edit generated output or its producer,
read ignored checkpoints/provider-local memory, promote temporary context,
inspect private state, or infer runtime retrieval from tracked links.

## Scope

Included: the LLM-WIKI README, six declared input roots, generator, generated
output, byte-drift check, repository lookup routes, review/freshness triggers,
and exactly four memory classes across authority, promotion, conflict,
redaction, freshness, retention, deletion/GC, compaction, resume, and handoff.
Excluded: provider recall, ignored checkpoints, private/user memory, secrets,
retrieval quality, MCP/search/RAG operation, hosted/remote/live state, and
canonical remediation.

## Definitions / Facts

### LLM-WIKI

The LLM-WIKI is a repository-local Markdown owner map, not a search service or
knowledge authority. The RIA relation names one canonical owner, one generator,
six ordered input roots, one generated output, and one check command.

| Role | Exact owner / evidence | Current behavior | Audit result |
| --- | --- | --- | --- |
| Link-map boundary | `docs/90.references/llm-wiki/README.md#current-index-role` | Declares reference-only scope, six inputs, producer, output, and check. | Unique canonical owner. |
| Declared inputs | `docs/90.references/data/reference-information-architecture.json#generatedAssets` | LLM-WIKI README, Agent Governance Hub, Harness Catalog, stage routing, Docs README, and Scripts README in exact order. | RIA relation and README agree. |
| Producer | `scripts/generate-llm-wiki-index.sh#generate_index` | Emits a fixed Markdown map; `--check` regenerates to a temporary file and byte-compares it with tracked output. | Deterministic producer; it does not parse or digest declared input contents. |
| Generated output | `docs/90.references/llm-wiki/wiki-index.md#authority-boundary` | Derived canonical-owner lookup only; hand editing is prohibited. | Output bytes equal producer bytes. |
| Static enforcement | `scripts/validate-repo-quality-gates.sh`; `scripts/reference_information_architecture.py#validate_generated_assets` | Quality gate checks reference-only shape and byte equality; RIA validates unique safe generator relation and command. | Current lookup boundary is enforced repository-statically. |
| Human operation | `docs/05.operations/guides/0009-llm-wiki-curation-guide.md#step-by-step-instructions`; `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md#scenario-c-llm-wiki-ownerlink-change` | Change canonical owner/generator, regenerate, check, and never hand-edit output. | Human refresh route is explicit. |

The generated map contains canonical-owner links across governance, SDLC
stages, operations, references, templates, scripts, GitOps, and examples.
Repository readers route through the root README, reference index, scripts
inventory, curation guide/runbook, tracked knowledge-map skills, quality gate,
and RIA relation. None of these surfaces proves model ingestion or retrieval.

#### Freshness Proof

Byte freshness and review freshness are different. The pre-remediation RED at
the observation commit showed that `bash scripts/generate-llm-wiki-index.sh
--check` passed while both the README and generated output still declared
`2026-05-10` for source/review metadata. All six declared inputs already had
later last-change commits:

| Declared input | Last change at the observation commit |
| --- | --- |
| `docs/90.references/llm-wiki/README.md` | 2026-07-23, commit `0cb1789c80811a6ec5833ae1cfc56b5c12cb327a` |
| `docs/00.agent-governance/README.md` | 2026-07-29, commit `138ce6ac28aa0eebac2b0295e4c50fd78d594db6` |
| `docs/00.agent-governance/harness-catalog.md` | 2026-08-02, commit `4fdea6a068aec6c65681bae32c44b67a5e95f09e` |
| `docs/00.agent-governance/rules/document-stage-routing.md` | 2026-07-30, commit `38a2fe6b90bad694d0a9a021c7edce8d800e03ea` |
| `docs/README.md` | 2026-07-18, commit `787b28fe1f2b1fff16d59936ed2a411e04d25db5` |
| `scripts/README.md` | 2026-08-02, commit `4fdea6a068aec6c65681bae32c44b67a5e95f09e` |

Before remediation, the producer/output themselves last changed 2026-07-03 at
commit `4ec068e4b14f244dd31d991d90241694f15323e4`. That baseline proved byte
equality did not establish source-trigger review freshness. WGIA-010 reviewed
the exact six RIA-declared inputs, updated README/generator source and review
metadata to `2026-08-09`, regenerated `wiki-index.md` only through the
producer, and made the corrected freshness probe plus producer byte check
GREEN. This is the current state reflected by WGA-KNW-002's `Aligned` verdict.

### Memory Tiers and Management

Exactly four classes are selected in identical order by the harness, lifecycle,
checkpoint, and closure contracts. `docs/00.agent-governance/memory/progress.md`
is the durable shared ledger within `durable-long-term`, not a fifth class.

| Class | Authority / owner | Freshness and conflict | Retention / deletion / GC | Promotion and redaction | Compaction and handoff |
| --- | --- | --- | --- | --- | --- |
| `working-short-term` | Active executor; temporary, non-authoritative task context | Re-observe repository/task on resume; observed repository state wins | Task-bounded; discard at reviewed terminal disposition after durable evidence is promoted | Reviewed/redacted reusable evidence may enter `durable-long-term`; prohibited payloads never persist | Replace raw context with bounded reviewed summary; hand off next owner or discard with evidence |
| `durable-long-term` | Canonical SDLC owner or shared progress ledger | Canonical-owner review; document-type owner outranks progress, and newer reviewed evidence reconciles older memory | Retain until canonical owner approves replacement; governed archive preserves provenance | No implicit onward promotion; only non-sensitive reviewed facts, decisions, progress, and handoff evidence | Preserve source/provenance, remove raw prompts, and hand off through canonical Task/progress evidence |
| `domain-scoped` | Canonical domain document owner | Domain-owner review; domain owner wins, ambiguous cross-domain overlap escalates | Archive when superseded/invalidated with original and replacement ownership | Cross-domain evidence may enter `durable-long-term` only after receiving-owner review; no copied sensitive payloads | Merge duplicate scope knowledge under current owner and route handoff by domain/validation owner |
| `provider-local-auxiliary` | Provider runtime or user-local store; advisory only | Re-observe repository before use; repository and canonical owners win every conflict | Provider-owned retention/GC after re-observation; never archived as repository authority | May enter `working-short-term` only after re-observation/classification/redaction; never writes canonical memory directly | Provider compaction is not repository evidence; handoff records only redacted status/retry trigger without transferring authority |

The checkpoint schema requires 20 top-level fields including redaction,
compaction, handoff, and exactly four lifecycle records. Resume is
`repository-wins`, exact identity and a single writer are required, duplicate
resume is prohibited, and actual provider-state reads are disallowed by the
static validator. Closure validation fixes each class's owner, sensitivity,
promotion, retention, compaction, archive/GC, conflict, and handoff projection.

### Blockers

A material blocker requires cause, impact, affected request IDs, release
condition, owner, and evidence depth. Pending work alone is not a blocker.

| ID | Cause | Impact | Affected request IDs | Release condition | Owner | Evidence depth | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-WGA-KNW-001 | Provider-local stores, native compaction, and the ignored checkpoint are outside authorized repository-static inspection. | Static lifecycle alignment cannot be promoted to actual memory retention/deletion, provider recall, compaction, resume, or handoff evidence. | `REQ-WGA-027` | An authorized provider-runtime exercise produces redacted class/promotion/retention/compaction/resume/handoff evidence without exposing private state. | Provider-runtime operator and current provider note; Stage 00 contracts remain static owners. | `provider-runtime` | `DEFER` evidence limitation, not a blocker to the repository-static audit. |

### Finding Convention

Every material finding uses the closed pack fields. Evidence depth is one of
`repository-static`, `provider-runtime`, `hosted`, or `live`; unavailable
deeper evidence remains `DEFER`. A blocker is either a complete object above or
the explicit value `none`.

#### WGA-KNW-001 — Generated ownership and lookup routing align

- **Request IDs**: `REQ-WGA-022`.
- **Scope**: LLM-WIKI owner, six input roots, producer, generated output, check command, lookup routes, and generated-only boundary.
- **Expected state**: one canonical link-map owner and deterministic producer create one generated Markdown output without promoting the map to policy, search, or runtime knowledge.
- **Observed state**: README and RIA ownership relations agree; generator check passes; generated output is reference-only; current lookup routes point to canonical owners and prohibit hand editing/runtime inference.
- **Evidence**: `docs/90.references/llm-wiki/README.md#current-index-role`; `docs/90.references/data/reference-information-architecture.json#generatedAssets`; `scripts/generate-llm-wiki-index.sh#generate_index`; `docs/90.references/llm-wiki/wiki-index.md#authority-boundary`; `scripts/reference_information_architecture.py#validate_generated_assets`; `docs/05.operations/guides/0009-llm-wiki-curation-guide.md#common-pitfalls`; `docs/00.agent-governance/rules/documentation-protocol.md`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: generated lookup ownership, byte drift, and no-hand-edit boundaries are deterministic and do not duplicate target authority.
- **Disposition**: `Keep`.
- **Canonical owner**: LLM-WIKI README for link-map boundary, generator for output bytes, target documents for facts/policy.
- **Verification**: generator `--check`, RIA generator-relation tests, strict profiles/links, and generated-output identity check.
- **Uncertainty**: lookup use, model ingestion, discovery quality, MCP/search/RAG, hosted, provider, remote, and live behavior are not observed.
- **Blocker**: none for repository-static generated ownership.

#### WGA-KNW-002 — LLM-WIKI source-trigger review metadata is refreshed

- **Request IDs**: `REQ-WGA-022`.
- **Scope**: README/output source-reviewed dates and on-source-change freshness trigger across the six declared inputs.
- **Expected state**: a declared input change triggers review, and visible source/review metadata records the reviewed current owner map separately from generator byte equality.
- **Observed state**: WGIA-010 reviewed all six RIA-declared inputs, recorded each current last-change identity in the README, updated source/review metadata to 2026-08-09 in the README and generator, and regenerated `wiki-index.md` only through the producer. The generated byte check passes without introducing a runtime/search claim.
- **Evidence**: `docs/90.references/llm-wiki/README.md#reference-type`; `docs/90.references/llm-wiki/README.md#review-and-freshness`; `docs/90.references/llm-wiki/wiki-index.md#review-and-freshness`; `scripts/generate-llm-wiki-index.sh#generate_index`; `docs/90.references/data/reference-information-architecture.json#generatedAssets`; `docs/90.references/research/2026-08-08-wer/llm-wiki-and-knowledge-routing.md#owner-drift-and-freshness-rules`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: byte-current output and the declared source-review date now describe the same six-input repository-static review event.
- **Disposition**: `Corrected` by admitted roadmap row `WGA-RMP-KNW-001` in WGIA-010.
- **Canonical owner**: LLM-WIKI README for review/freshness declaration; generator for emitted metadata and output regeneration.
- **Verification**: RED returned stale README/generator source and review metadata while generator `--check` still passed; GREEN reports `llm_inputs=6/6 source_checked=2026-08-09 last_reviewed=2026-08-09`, and producer `--check` passes.
- **Uncertainty**: none for the repository-static review ledger; live owner usability and provider consumption remain outside this finding.
- **Blocker**: none at repository-static depth; fresh specification/content and quality reviews are Approved.

#### WGA-KNW-003 — Four-class memory lifecycle aligns repository-statically

- **Request IDs**: `REQ-WGA-027`.
- **Scope**: authority, freshness, retention, deletion/GC, promotion, conflict, redaction, compaction, resume, and handoff for exactly four memory classes.
- **Expected state**: closed machine/policy owners select the same four classes, repository truth wins, promotion is reviewed/redacted, and each class has bounded lifecycle and handoff behavior.
- **Observed state**: memory README, harness, loop, checkpoint, closure, documentation protocol, and postflight projections agree; focused self-test/production validators and relevant tests pass.
- **Evidence**: `docs/00.agent-governance/memory/README.md#four-memory-classes`; `docs/00.agent-governance/contracts/harness-contract.json#memory`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#interfaces`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#required`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#$defs.memoryLifecycle`; `docs/00.agent-governance/contracts/agent-governance-closure.json#memoryLayers`; `docs/00.agent-governance/rules/postflight-checklist.md#validation-and-refresh`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: static authority, promotion, repository-wins, retention/GC, redaction, compaction, resume, and handoff semantics are closed and testable.
- **Disposition**: `Keep`.
- **Canonical owner**: harness/lifecycle/checkpoint/closure machine contracts and the Stage 00 memory policy/index.
- **Verification**: harness, loop, checkpoint, and closure self-test/production checks plus focused memory/generator tests.
- **Uncertainty**: static fixtures do not prove actual provider memory, checkpoint, compaction, deletion, resume, or handoff execution.
- **Blocker**: none for repository-static alignment; `BLK-WGA-KNW-001` limits runtime promotion only.

#### WGA-KNW-004 — Provider-local memory and actual lifecycle execution remain deferred

- **Request IDs**: `REQ-WGA-027`.
- **Scope**: provider-local stores, ignored checkpoint, actual retention/deletion, native compaction, resume, and handoff.
- **Expected state**: advisory/private memory never becomes repository authority, and no deeper-lane claim is made without authorized redacted runtime evidence.
- **Observed state**: static contracts enforce advisory status and repository re-observation; no provider/private/ignored checkpoint was accessed, so actual behavior remains unobserved.
- **Evidence**: `docs/00.agent-governance/contracts/harness-contract.json#memory`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#$defs.resume`; `docs/00.agent-governance/contracts/agent-governance-closure.json#memoryLayers`; `docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md#lifecycle-rules-and-evidence-limits`; `docs/00.agent-governance/harness-implementation-map.md#evidence--progress`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `DEFER`.
- **Impact**: repository-static lifecycle controls are usable governance evidence but cannot establish provider retention, deletion, compaction, resume, or handoff behavior.
- **Disposition**: `Keep`.
- **Canonical owner**: provider-runtime operator for deeper evidence; Stage 00 contracts remain static authority.
- **Verification**: separately authorized, redacted provider-runtime lifecycle evidence with repository re-observation and no private payload exposure.
- **Uncertainty**: provider discovery, memory enablement, retention/GC, private deletion, native compaction, actual checkpoint I/O, resume, handoff, hosted, remote, and live state.
- **Blocker**: `BLK-WGA-KNW-001`; it blocks evidence-depth promotion, not WGIA-006 static completion.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-KNW-001 | human index | `docs/90.references/llm-wiki/README.md#current-index-role`; `docs/90.references/llm-wiki/README.md#review-and-freshness`; `docs/00.agent-governance/memory/README.md#four-memory-classes`; `docs/00.agent-governance/memory/progress.md#work-entries` | Knowledge ownership, freshness, and memory routing. |
| SRC-WGA-KNW-002 | evidence producer | `scripts/generate-llm-wiki-index.sh#generate_index`; `docs/90.references/llm-wiki/wiki-index.md#authority-boundary`; `scripts/validate-agent-harness-contract.py#main`; `scripts/validate-agent-loop-lifecycle.py#main`; `scripts/validate-agent-checkpoint.py#main`; `scripts/validate-agent-governance-closure.py#main` | Deterministic byte and memory-lifecycle validation. |
| SRC-WGA-KNW-003 | machine owner | `docs/90.references/data/reference-information-architecture.json#generatedAssets`; `docs/00.agent-governance/contracts/harness-contract.json#memory`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#$defs.memoryLifecycle`; `docs/00.agent-governance/contracts/agent-governance-closure.json#memoryLayers` | Generated relation and closed memory projections. |
| SRC-WGA-KNW-004 | policy owner | `docs/00.agent-governance/rules/documentation-protocol.md`; `docs/00.agent-governance/rules/postflight-checklist.md#validation-and-refresh`; `docs/05.operations/guides/0009-llm-wiki-curation-guide.md#step-by-step-instructions`; `docs/05.operations/runbooks/0011-reference-maintenance-runbook.md#scenario-c-llm-wiki-ownerlink-change` | No-hand-edit, memory coupling, promotion, and operational refresh routes. |
| SRC-WGA-KNW-005 | historical snapshot | `docs/90.references/research/2026-08-08-wer/llm-wiki-and-knowledge-routing.md#owner-drift-and-freshness-rules`; `docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md#lifecycle-rules-and-evidence-limits` | Source-bounded research context only; current owners win. |

## Review and Freshness

- Review status: fresh WGIA-010 specification/content and quality reviews are
  `Approved` after the one Important contradiction was fixed. The original
  WGIA-006 audit reviews remain Approved.
- Review disposition: `Approved` after WGIA-010 corrected WGA-KNW-002 through
  admitted row `WGA-RMP-KNW-001`; provider/runtime finding WGA-KNW-004 remains
  `DEFER`.
- Evidence observed: 2026-08-09 at exact observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef`, compared with starting commit
  `d56f2c3429065e9c4642028f905dfcf2a9f748a7`.
- Current-truth owners: LLM-WIKI README/generator/target documents and Stage 00
  memory, harness, lifecycle, checkpoint, closure, documentation, and postflight
  owners.
- Refresh triggers: declared source, owner link, generator/output, source-review
  date, memory class, promotion, retention/GC, conflict, redaction, compaction,
  resume, handoff, provider evidence, or observation commit change.
- Provider-runtime, hosted, remote, credential-bearing, private-memory,
  ignored-checkpoint, retrieval, and live evidence remains `DEFER`.
- WGIA-009 admitted freshness row `WGA-RMP-KNW-001`, and WGIA-010 implemented
  its repository-static correction; fresh specification/content and quality
  reviews are Approved. No disposition-ledger row
  exists because no Legacy, Deprecated, one-shot, or deletion candidate was
  found.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/0055-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../../../03.specs/0055-workspace-governance-audit-and-remediation/plan.md)
- [Implementation Task](../../../03.specs/0055-workspace-governance-audit-and-remediation/README.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
- [LLM-WIKI README](../../llm-wiki/README.md)
