---
title: 'Research Consolidation and Supersession Map'
type: content/reference
status: active
owner: platform
updated: 2026-08-07
---

# Research Consolidation and Supersession Map

## Overview

This reference consolidates the same-purpose research documents under
`docs/90.references/research/`. It records three things: which older document
each newer document supersedes and how completely, which still-valid facts the
newer document dropped and where they are re-homed, and which claims the Current
pack presents as settled that no longer match the repository.

The consolidation is content-level, not file-level. Every file under
`docs/90.references/research/` is byte-frozen by the reference information
architecture, so no file there was merged, edited, or removed. Newest content
wins by being recorded here as the current owner, with the frozen documents
retained as dated evidence.

The finding that shapes this document is that duplication was not the real
problem. The 2026-07-07 pack already refreshed and integrated the 2026-07-04
pack, document by document, with explicit lineage links. What remained was
stale currency: eight facts the 2026-07-07 pack states as resolved that the
2026-08-07 observation contradicts, seven of them by one month of ordinary
drift and one by a sourcing defect.

### Purpose

- Record the supersession verdict for each same-purpose pair, with evidence.
- Carry forward the still-valid facts the newer pack dropped, so nothing
  useful is stranded in a frozen document.
- Record, with both dated claims, every Current-pack statement that the
  2026-08-07 observation supersedes.
- State which collection owns which topic from 2026-08-07 forward.

## Reference Type

- Type: durable-concept / source-ledger
- Source checked: `2026-08-07`
- Refresh trigger: a new dated research pack; a change to the reference
  information architecture that unfreezes a pack; or a repository change that
  invalidates one of the superseded-claim rows below.

## Authority Boundary

- **Authoritative for**:
  - The supersession verdicts and the carried-forward facts recorded here.
  - The superseded-claim list, each row verified against the working tree on
    2026-08-07.
  - The topic-ownership boundary between `research/` and
    `workspace-research/` from 2026-08-07 forward.
- **Not authoritative for**:
  - The content of any frozen document. This reference does not amend,
    correct, or invalidate a byte-frozen file; it records what a reader should
    know before relying on one.
  - Active policy, contracts, templates, validators, or provider state. Those
    stay with their canonical owners.
  - Whether a superseded claim was correct at its own observation date. Each
    dated claim is treated as accurate for its date.
  - Live cluster, provider runtime, hosted CI, or remote evidence.

## Scope

### In Scope

- The seven same-named document pairs across
  `docs/90.references/research/2026-07-04-wer/` and
  `docs/90.references/research/2026-07-07-wer/`.
- Topic overlap between `docs/90.references/research/2026-07-07-wer/` and
  `docs/90.references/workspace-research/`.
- Within-pack duplication inside `docs/90.references/research/2026-07-07-wer/`.
- The immutability constraint that bounds any file-level consolidation.

### Out of Scope

- Editing, merging, or deleting any file under `docs/90.references/research/`.
- Moving the reference information architecture baseline or the snapshot
  guard.
- Re-running the original external source checks. Dated findings are cited as
  dated, not re-verified.
- Live, provider-runtime, hosted-CI, or remote verification.

## Definitions / Facts

### The Consolidation Constraint

File-level consolidation under `docs/90.references/research/` is not
achievable. Three rules in
`docs/90.references/data/reference-information-architecture.json`, enforced by
`scripts/reference_information_architecture.py`, jointly freeze the tree:

| Surface                                                 | Rule                                                                                                                          | Failure observed 2026-08-07                                                       |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `2026-07-04-wer/` README and its 7 Report Index members | Snapshot guard byte-compares each against the fixed historical source commit; the historical pack set is a validator constant | Appending one newline produced `RIA-SNAPSHOT ... protected snapshot`              |
| `2026-07-07-wer/` README and its 9 members              | Overlay guard byte-compares each against the pack baseline commit, except the declared `Lifecycle` column                     | Editing the pack README produced `RIA-OVERLAY ... protected Current bytes differ` |
| `research/README.md`                                    | Overlay guard byte-compares it except the declared `Status` column                                                            | Adding index rows produced `RIA-OVERLAY ... protected index bytes differ`         |

The `Status` column is the only mutable projection, and the collection README's
own legend fixes its vocabulary to `Index`, `Historical`, `Current pack`, and
`Included`, which already describe the packs correctly. No mutation there would
add information.

This freeze is a retention control, not an obstacle to route around. The
consolidation is therefore recorded here, in the writable collection, and the
frozen documents stay as dated evidence.

### Supersession Map

Each 2026-07-07 document links its 2026-07-04 predecessor. Verdicts below come
from a heading-level and claim-level comparison performed on 2026-08-07.

| Topic                                | Superseding owner (2026-07-07)          | Verdict              | Carried-forward items         |
| ------------------------------------ | --------------------------------------- | -------------------- | ----------------------------- |
| Provider implementation status       | `provider-implementation-status.md`     | Fully superseded     | none                          |
| AI agents roster and gap analysis    | `ai-agents-roster-and-gap-analysis.md`  | Fully superseded     | none                          |
| Workspace governance baseline        | `workspace-governance-baseline.md`      | Superseded with gaps | 3                             |
| Harness and loop engineering         | `harness-and-loop-engineering.md`       | Superseded with gaps | 1 carried, 1 intentional drop |
| Spec, SDLC, CI, QA, formatting       | `spec-sdlc-ci-qa-formatting.md`         | Superseded with gaps | 2                             |
| Kubernetes, infrastructure, security | `kubernetes-infrastructure-security.md` | Superseded with gaps | 3                             |
| Automation, pipeline, workflow, QA   | `automation-pipeline-workflow-qa.md`    | Superseded with gaps | 2                             |

The two fully superseded pairs need nothing. The 2026-07-07 provider document
states the strongest lineage wording in the pack — it records the 2026-07-04
synthesis as integrated after re-verification — and the roster document
re-derives every earlier verdict from a pinned upstream commit.

### Carried-Forward Facts

These statements existed in the 2026-07-04 pack, remain useful, and have no
counterpart in the 2026-07-07 pack. They are recorded here so the frozen
document is not the only place they live. Each is a dated 2026-07-04
observation, not a re-verified current fact.

| ID    | Carried-forward fact                                                                                                                                                                                                                                                               | Source document                         | Current owner to consult                                                                  |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------- |
| CF-01 | Stage language policy: governance docs under `docs/00.agent-governance/**` are English-only; human-facing README and overview text may use Korean; reference metadata, source, freshness, authority boundary, generated-index contracts, and agent routing notes are English-first | `workspace-governance-baseline.md`      | `docs/00.agent-governance/rules/` and `docs/99.templates/support/`                        |
| CF-02 | `.env` key-only parity counts as repo-static security evidence alongside the plaintext secret scan, policy gates, workflow permission checks, and the approval-boundary matrix                                                                                                     | `workspace-governance-baseline.md`      | `scripts/check-secret-handling.sh`                                                        |
| CF-03 | `bash scripts/validate-harness.sh` bundles repo-static gates and adds no live checks. The 2026-07-07 pack mentions this script only negatively                                                                                                                                     | `workspace-governance-baseline.md`      | `scripts/validate-harness.sh`                                                             |
| CF-04 | Task-by-task commit discipline: logical units are committed separately, with the task record naming evidence per unit; isolated worktrees are part of the harness pattern                                                                                                          | `harness-and-loop-engineering.md`       | `docs/00.agent-governance/rules/quality-standards.md`                                     |
| CF-05 | The generated-index freshness gate `bash scripts/generate-llm-wiki-index.sh --check` is a repo-static validation lane                                                                                                                                                              | `spec-sdlc-ci-qa-formatting.md`         | [LLM Wiki and Agent Knowledge Routing](llm-wiki-and-knowledge-routing.md)                 |
| CF-06 | SLSA v1.2 is the current specification and the v1.1 page is retired. The 2026-07-07 pack keeps SLSA only inside the Kubernetes document, without the retirement note                                                                                                               | `spec-sdlc-ci-qa-formatting.md`         | [GitHub Actions and CI Evidence](github-actions-and-ci-evidence.md)                       |
| CF-07 | Argo Rollouts progressive delivery: the Rollout and AnalysisTemplate pattern and its workload example. The 2026-07-07 pack retains only the two kind names inside an AppProject allow-list                                                                                         | `kubernetes-infrastructure-security.md` | `gitops/` manifests and `docs/05.operations/runbooks/`                                    |
| CF-08 | Namespace ownership model: steady-state `CreateNamespace=true` is removed and namespaces stay in explicit desired-state manifests or bootstrap boundaries, with a per-namespace owner matrix                                                                                       | `kubernetes-infrastructure-security.md` | `gitops/` and `docs/05.operations/policies/`                                              |
| CF-09 | Example placeholder images under `examples/sample-app/*` are allowed as template placeholders only, and never imply production readiness                                                                                                                                           | `kubernetes-infrastructure-security.md` | `docs/05.operations/policies/`                                                            |
| CF-10 | Artifact, dependency-cache, and reusable-workflow analysis of the CI workflows                                                                                                                                                                                                     | `automation-pipeline-workflow-qa.md`    | [GitHub Actions and CI Evidence](github-actions-and-ci-evidence.md), gaps CI-G3 and CI-G4 |
| CF-11 | A retired `.github` about-file routed version inventory and action tag policy to the tech-stack version inventory                                                                                                                                                                              | `automation-pipeline-workflow-qa.md`    | `.github/README.md`, which replaced that retired hub                                            |

One 2026-07-04 item is recorded as an intentional drop rather than a gap. The
five-primitive convergence market scan was excluded because the 2026-07-07
harness document states that no market-scan source is used as authority. That
exclusion is preserved here.

### Superseded Current-Pack Claims

The 2026-07-07 pack README contains a `Pack-Wide Contradiction Closure`
section that presents several facts as settled. The rows below were re-observed
in the working tree on 2026-08-07 and no longer hold. Each older claim remains
accurate for its own observation date of 2026-07-10 or 2026-07-12.

| ID    | Claim as recorded (2026-07-10 / 2026-07-12)                                                                                              | Observed 2026-08-07                                                                                                                                          | Verification                                                                              |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| SC-01 | 15 `uses:` occurrences with 0 full commit-SHA pins; all external Actions use version tags; `.github/zizmor.yml` disables `unpinned-uses` | Every remote `uses:` is a full 40-character commit SHA with a version comment; no `.github/zizmor.yml` exists                                                | `.github/workflows/*.yml` read 2026-08-07                                                 |
| SC-02 | 5 workflows and 6 `ci.yml` jobs                                                                                                          | 5 workflows and 7 `ci.yml` jobs: `branch-policy`, `changes`, `pre-commit`, `repo-quality-static`, `agent-governance-static`, `manifest-static`, `ci-summary` | `.github/workflows/ci.yml` parsed 2026-08-07                                              |
| SC-03 | 3 CI path-filter outputs produced by a third-party paths-filter action                                                                   | 4 CI job outputs selected by `scripts/select-affected-surfaces.py` from `docs/00.agent-governance/contracts/validation-surfaces.json`                        | contract and workflow read 2026-08-07                                                     |
| SC-04 | 10 roles across 3 adapter surfaces, 30 files                                                                                             | 12 roles across 4 surfaces, 48 projections                                                                                                                   | `harness-contract.json` `currentInventory` read 2026-08-07                                |
| SC-05 | No `.gemini/agents/` and no tracked `.gemini/settings.json` exist                                                                        | `.gemini/agents/` holds 12 files and `.gemini/settings.json` is tracked                                                                                      | directory listing 2026-08-07                                                              |
| SC-06 | `supervisor` Claude adapter tools are Read, Grep, Glob, Bash, Edit, Write, Task                                                          | `supervisor` Claude adapter tools are Read, Grep, Glob, Task                                                                                                 | `.claude/agents/supervisor.md` frontmatter read 2026-08-07                                |
| SC-07 | Claude Opus 4.8 is current and widely released; nine workers declare `sonnet 4.6`                                                        | Current provider documentation lists `opus 4.8` and `sonnet 4.6` under legacy models; the roster now declares `Sonnet 5` for two roles                       | [Agent Model Routing and Configuration](agent-model-routing-and-configuration.md), MOD-G3 |
| SC-08 | `gpt-5.3-codex` is deprecated on the authentication surface, cited to a published model page                                             | The identifier is not corroborated by any page fetched on 2026-08-07; `gpt-5.6-terra` is                                                                     | [Agent Model Routing and Configuration](agent-model-routing-and-configuration.md), MOD-G4 |

SC-07 and SC-08 are recorded as conflicts, not corrections. The fixed provider
cutoff of `2026-07-10 10:00 KST` is not moved by this reference, and promoting
either row requires an authorized cutoff refresh plus a same-suite evaluation.

One further item is a sourcing defect rather than drift. The 2026-07-07 format
ledger cites a specific ISO/IEC/IEEE 42010 revision for the ARD form and
presents ISO/IEC/IEEE 29148 as grounding the PRD form. Neither standard's
normative text was observed, the 42010 catalog page returned HTTP 403 on
2026-08-07, and no standard defines a PRD. Those two rows are unlabelled
inferences. They are routed as gaps DOC-G8 and DOC-G9 in
[Documentation Architecture and SDLC Document Roles](documentation-architecture-and-diataxis.md).

### Topic Ownership from 2026-08-07

| Topic                                                                                                                                                                                                                                         | Current owner                                                   | Note                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Workspace governance baseline, harness and loop engineering, provider implementation status, spec and SDLC and CI and QA and formatting, Kubernetes and infrastructure and security, automation and pipeline and workflow QA, AI agent roster | `docs/90.references/research/2026-07-07-wer/`                   | Read together with the superseded-claim table above                                       |
| Document type format evidence, document migration disposition                                                                                                                                                                                 | `docs/90.references/research/2026-07-07-wer/`                   | Not same-purpose with each other; one is keyed by template family, the other by file path |
| Diátaxis documentation architecture and SDLC document roles                                                                                                                                                                                   | `workspace-research/documentation-architecture-and-diataxis.md` | New topic; extends the format ledger                                                      |
| LLM knowledge indexes and agent knowledge routing                                                                                                                                                                                             | `workspace-research/llm-wiki-and-knowledge-routing.md`          | New topic; the 2026-07-07 pack has no counterpart                                         |
| GitHub Actions rules, CI selection contract, evidence lanes                                                                                                                                                                                   | `workspace-research/github-actions-and-ci-evidence.md`          | Supersedes the automation document's pin, job, and filter facts                           |
| Task-characteristic model and reasoning-effort routing                                                                                                                                                                                        | `workspace-research/agent-model-routing-and-configuration.md`   | Supersedes the provider document's roster, surface, and model-lifecycle facts             |
| Agent memory tiers and management                                                                                                                                                                                                             | `workspace-research/agent-memory-tiers-and-management.md`       | New topic; extends the harness document's knowledge-store row                             |

Within `docs/90.references/research/2026-07-07-wer/` no two documents share a
purpose. The nearest adjacency is the format ledger against the SDLC document,
and both declare the boundary explicitly: the ledger disclaims route,
frontmatter, and lifecycle authority, which the SDLC document holds.

## Sources

- Repository evidence read 2026-08-07: every document under
  `docs/90.references/research/2026-07-04-wer/` and
  `docs/90.references/research/2026-07-07-wer/`, the five references in this
  collection, `docs/00.agent-governance/contracts/harness-contract.json`,
  `.claude/agents/supervisor.md`, `.gemini/agents/`, `.gemini/settings.json`,
  `.github/workflows/`, and
  `docs/00.agent-governance/contracts/validation-surfaces.json`.
- Immutability evidence observed 2026-08-07:
  `python3 scripts/validate-reference-information-architecture.py --root .`
  returned `RIA-SNAPSHOT ... protected snapshot` for a one-byte change to a
  historical member, and
  `bash scripts/validate-repo-quality-gates.sh .` returned
  `RIA-OVERLAY ... protected Current bytes differ` and
  `RIA-OVERLAY ... protected index bytes differ` for edits to the Current pack
  README and the collection README.
- Contract evidence:
  `docs/90.references/data/reference-information-architecture.json` and
  `scripts/reference_information_architecture.py`, which hold the fixed
  historical pack set, the current pack baselines, and the declared mutable
  index projections.
- Dated claims attributed to the 2026-07-04 and 2026-07-07 packs are cited as
  those packs recorded them. Their external sources were not re-fetched for
  this map.

## Review and Freshness

- Review when a new dated research pack is added, when the reference
  information architecture changes a baseline or the historical pack set, or
  when any superseded-claim row is invalidated by a repository change.
- The superseded-claim table is a dated observation of the working tree on
  2026-08-07. Re-observe rather than reuse it.
- Carried-forward facts are 2026-07-04 observations. They were not
  re-verified against the current repository; consult the named owner before
  relying on one.
- This map does not change the status, lifecycle, or authority of any frozen
  document. Those remain what their own frontmatter and pack README declare.

## Related Documents

- [Workspace Research Collection](README.md)
- [Documentation Architecture and SDLC Document Roles](documentation-architecture-and-diataxis.md)
- [GitHub Actions and CI Evidence](github-actions-and-ci-evidence.md)
- [Agent Model Routing and Configuration](agent-model-routing-and-configuration.md)
- [Research Collection](../research/README.md)
- [Current Research Pack (2026-07-07)](../research/2026-07-07-wer/README.md)
- [Historical Research Pack (2026-07-04)](../research/2026-07-04-wer/README.md)
