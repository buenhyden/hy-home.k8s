---
title: 'Workspace Engineering Gap-only Research Refresh Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-08-10
artifact_id: "SPEC-0056"
---

# Workspace Engineering Gap-only Research Refresh Technical Specification (Spec)

## Overview

This specification designs a gap-only external-source refresh of the existing
`docs/90.references/research/0001-workspace-engineering/` pack. It does not create a new
dated pack and does not repeat the broad research completed by
[Spec 053](../0053-workspace-engineering-research-pack-consolidation/spec.md).
The refresh admits only two evidence classes selected by the human requester:

1. a requested question with no material external-source treatment in the
   existing pack; or
2. a requested question whose existing result is `Partial` because its
   external basis is materially incomplete and can be strengthened without
   provider-runtime, hosted, remote, credential-bearing, or live evidence.

The user approved this design direction and the written specification on
2026-08-09, selected subagent-driven execution, and directed the result to be
integrated into the existing `0001-workspace-engineering` pack. WERG-000 activates the
reciprocal [Plan](./plan.md)
and [Task](./plan.md)
through a standalone execution relation governed by
[ADR-0022](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md).
Direct human approval on 2026-08-09 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.
This active execution does not reopen terminal Spec 053 or create a second
Plan/Task relation for Spec 053.

The primary consumers are documentation writers, platform and security
engineers, quality reviewers, governance stewards, and AI agents that use the
research pack to distinguish current source-backed guidance from local
implementation evidence and deeper evidence that remains `DEFER`.

## Strategic Boundaries & Non-goals

### Authorized scope

- Re-audit every requested category only to decide whether it satisfies the
  gap-only admission rule; do not re-research a category that already has an
  adequate official-source basis.
- Research the currently admitted document-family questions: PRD, AD,
  Policy, Runbook, and Release approval/evidence semantics beyond version
  numbering.
- Research explicit Verification versus Validation terminology, responsibility,
  evidence, and failure meaning across SDLC, QA, delivery, and operations.
- Research only newly sharpened Kubernetes and infrastructure security
  questions that are not already closed by the pack, including the necessity
  boundary for kube-state-metrics Secret metadata RBAC, ingress/default-deny
  policy design, Pod Security and workload hardening, and immutable Git,
  image, and chart identity.
- Compare every admitted external claim with exact current repository paths or
  selectors and classify the result without changing the implementation owner.
- Integrate accepted evidence into exactly five research-pack owners:
  `README.md`, `m0004-spec-driven-sdlc-and-document-contracts.md`,
  `m0008-ci-cd-github-actions-and-qa.md`,
  `m0007-kubernetes-infrastructure-and-security.md`, and
  `m0012-source-coverage.md`.
- Use disjoint research workers, independent content and quality review,
  logical-unit commits, and repository-static validation.

### Protected surfaces and non-goals

- Do not create a new research folder, add a parallel report, or recreate
  deleted predecessor packs.
- Do not rewrite or refresh the complete harness, loop, workspace application,
  Claude, Codex, common-agent environment, spec-driven development, broad
  Kubernetes/infrastructure, SDLC, Diataxis, LLM-WIKI, CI/CD, GitHub Actions,
  QA, security, AI-agent, Agency Agents, model-routing, or memory analysis when
  its existing official-source coverage is adequate.
- Do not obtain or infer authenticated provider execution, provider discovery,
  effective permissions, hosted CI, branch protection, artifacts, remote
  state, cluster state, CNI enforcement, Vault/ESO contents, credentials,
  secrets, or live platform behavior.
- Do not add a Release profile, change a document lifecycle, change a
  validator, modify RBAC, NetworkPolicy, workload security context, image,
  chart, Git revision, workflow, GitOps desired state, or infrastructure
  configuration merely because the research identifies a gap.
- Do not modify existing `docs/98.archive/**` records, terminal Spec 053
  evidence, or the current audit-pack RIA contract.
- Do not retain downloaded pages, temporary extraction files, generated
  research notes, or other one-off artifacts in the tracked tree.

## Contracts

### C-WERG-001 — gap-only admission

Every requested topic receives an admission result before external research:
`complete-existing`, `admit-unresearched`,
`admit-under-sourced-partial`, or `exclude-deep-evidence`. Only the two
`admit-*` states authorize new source and claim rows. Existing adequate
research is referenced, not rewritten.

### C-WERG-002 — existing-pack ownership

All accepted findings are integrated into the existing
`0001-workspace-engineering` owners. No new pack, addendum, duplicate topic owner, or
parallel current navigation is created. The pack date remains its original
identity; every new source and claim records the separate check date
`2026-08-10`.

### C-WERG-003 — primary-source provenance

Every new external claim has an official or primary URL, source ID, checked
date, adopted scope, explicitly rejected inference, refresh trigger, and
claim-level mapping. Secondary material is permitted only when no primary
owner exists and is labeled as non-authoritative.

### C-WERG-004 — workspace reconciliation

Every accepted claim names one or more exact repository paths or selectors and
states the `As-Is`, evidence gap, bounded target, admission dependency, and
evidence depth. An external recommendation is never promoted into a workspace
rule by the research pack.

### C-WERG-005 — Verification and Validation separation

The refresh defines Verification and Validation from an explicit external
source basis, maps both terms to current workspace terminology, and records
their actors, inputs, evidence, failure meaning, and SDLC or operational stage.
Syntax or schema validity cannot prove that an implementation satisfies an
approved requirement; requirement satisfaction cannot excuse malformed or
inadmissible inputs.

### C-WERG-006 — evidence-depth integrity

Repository-static evidence is kept separate from hosted,
provider-runtime, remote, credential-bearing, and live evidence. Missing
authority or environment yields `DEFER`; it is never presented as a successful
external-source conclusion or local implementation result.

### C-WERG-007 — identifier and cross-link stability

Existing requirement, source, and claim IDs remain unchanged. New accepted
sources and claims use the next mechanically verified sequential IDs. A new
Verification/Validation requirement row is added only if the admission audit
confirms that no existing row owns the requested concept. All changed links
resolve to the final surviving owner and heading.

### C-WERG-008 — bounded history and cleanup

Design, document-family plus Verification/Validation research, Kubernetes
security research, and final index/ledger/cross-link closure are separate
logical commits. Each commit is internally reviewable. One-off files are
removed before the final validation and no empty commit is created when an
admission lane yields no content change.

## Core Design

### Research admission matrix

| Requested area | Initial design classification | Admission question |
| --- | --- | --- |
| PRD and AD | `admit-under-sourced-partial` | Do official product and architecture requirement sources add semantics that the current local-only rows do not establish? |
| Policy and Runbook | `admit-under-sourced-partial` | Do official control/procedure sources add owner, exception, rehearsal, recovery, or evidence rules absent from the current local-only rows? |
| Release | `admit-under-sourced-partial` | Which approval, evidence, traceability, and rollback record semantics are distinct from SemVer and from the approved local no-release-notes decision? |
| Verification and Validation | `admit-unresearched` | Which external definition cleanly separates conformance to design from fitness or requirement satisfaction, and how does it map to current workspace lanes? |
| Kubernetes security deltas | conditional `admit-under-sourced-partial` | Which exact KSM RBAC, ingress/default-deny, Pod Security/workload, and supply-chain questions remain absent after line-level comparison with the existing report? |
| All other requested areas | `complete-existing` unless disproved | Does the pack already contain a material official-source claim, local mapping, uncertainty boundary, and refresh trigger for the requested question? |
| Runtime, hosted, remote, credential, and live evidence | `exclude-deep-evidence` | Does answering require authority or an environment outside repository-static research? |

The initial classifications are hypotheses, not permission to duplicate text.
The implementation Plan must run a deterministic pre-research comparison and
record the final admission result for every requested category.

### Owner integration map

| Existing owner | Bounded addition |
| --- | --- |
| `README.md` | Add a `2026-08-10` gap-only refresh boundary; add or reconcile the explicit Verification/Validation request owner; update only source/status cells whose admitted evidence changed. |
| `m0004-spec-driven-sdlc-and-document-contracts.md` | Add official external semantics for admitted PRD, AD, Policy, Runbook, and broader Release-record questions; preserve local profile/lifecycle facts and the Spec 052 DOC-G1/DOC-G5 decisions. |
| `m0008-ci-cd-github-actions-and-qa.md` | Add the externally sourced Verification/Validation distinction and a responsibility/evidence/failure matrix across SDLC, QA, delivery, and operations. |
| `m0007-kubernetes-infrastructure-and-security.md` | Add only line-level admitted security deltas after proving the current report does not already close the question. |
| `m0012-source-coverage.md` | Append only new source and claim rows, including checked date, adoption boundary, rejected inference, refresh trigger, workspace evidence, uncertainty, and owner link. |

### Research and review flow

```text
requested categories + existing source/claim ledger + current workspace
                              |
                              v
                   deterministic gap admission
                              |
                  +-----------+-----------+
                  |                       |
          complete/excluded            admitted
          reference only          official-source research
                                          |
                                          v
                             claim/workspace reconciliation
                                          |
                                          v
                              five existing pack owners
                                          |
                                          v
                           content review -> quality review
                                          |
                                          v
                          staged/full validation -> finish
```

### Source priority

1. Official standards bodies and government publications for terminology,
   lifecycle, assurance, and security practices.
2. Official project and product documentation for Kubernetes, GitHub, and
   relevant supply-chain mechanisms.
3. Canonical repository owners for current local implementation and policy.
4. Official project repositories, releases, and design documents when the
   owned documentation is insufficient.
5. Explicitly labeled secondary material only when no primary owner exists.

## Data Modeling & Storage Strategy

### Admission record

Each requested category is evaluated with:

| Field | Meaning |
| --- | --- |
| Request owner | Existing `REQ-WERPC-*` row or proposed new row. |
| Existing owner and heading | Current pack file and exact section. |
| Existing source IDs | Source rows already supporting the question. |
| Existing claim IDs | Claim rows already expressing the conclusion. |
| Coverage test | Material external definition, workspace mapping, uncertainty boundary, and refresh trigger. |
| Admission state | One of the four states in C-WERG-001. |
| Reason | Exact missing question or evidence-depth exclusion. |

The admission inventory is implementation evidence, not a new tracked research
artifact. Its accepted results are summarized in the source/migration ledger
and Task.

### Source and claim rows

New source rows preserve the existing ledger schema and add no parallel source
register. New claim rows preserve the existing state and evidence vocabulary.
The next source and claim identifiers are determined from the final tracked
ledger immediately before authoring; the specification does not preclaim
their numbers or counts.

### Snapshot identity

The directory identity remains `0001-workspace-engineering`. New material is visibly
labeled as a `2026-08-10 gap-only source refresh`. This separates the original
consolidated snapshot from later source verification without pretending that
all original sources were rechecked on the later date.

### One-off data lifecycle

Fetched pages, extracts, query results, and scratch matrices stay outside the
tracked tree. Only reviewed claims, source metadata, and execution evidence are
retained. Temporary content is discarded after its accepted facts are recorded
and before branch completion.

## Interfaces & Data Structures

### Inputs

- The exact current thirteen-file `0001-workspace-engineering` pack.
- The 32-row request matrix and current source/claim registers.
- The current repository paths cited by each candidate question.
- Official external sources checked on 2026-08-10.
- Spec 053 terminal boundaries, Spec 052 document decisions, ADR-0022, and the
  repository validation contracts.

### Outputs

- One reviewed gap-admission result for every requested category.
- Additive source and claim records only for admitted questions.
- In-place updates to the five existing research owners.
- A reciprocal Plan and Task after written Spec approval.
- Logical commits with targeted, affected, staged, aggregate, all-files, diff,
  and independent-review evidence.

### Compatibility rules

- Existing headings and anchors remain stable unless a changed claim requires
  a new narrowly scoped heading.
- Existing source and claim rows are not renumbered, overwritten, or assigned a
  later check date.
- Existing `Verified`, `Partial`, and `DEFER` states change only when the new
  evidence directly supports the transition and its evidence depth.
- Existing terminal Spec 053, predecessor-disposition, archive, and RIA records
  remain historical evidence and are not reopened.

## Edge Cases & Error Handling

| Edge case | Required behavior |
| --- | --- |
| The candidate question is already materially covered. | Classify `complete-existing`; cite the existing owner in execution evidence and make no research-content edit. |
| An official source describes a desired practice but the workspace has no matching owner or decision. | Record `Partial` or `DEFER`, name the admission dependency, and do not invent policy. |
| Two standards use different Verification/Validation terminology. | Preserve both source contexts, choose no silent universal definition, and state the repository mapping explicitly. |
| A Release source discusses release notes rather than auditable release records. | Keep it separate from Spec 052 DOC-G5 and reject it as evidence for the broader record contract. |
| Kubernetes guidance is already present but lacks one exact local selector. | Add only the missing selector comparison; do not duplicate the upstream explanation. |
| A source URL is unstable, secondary, inaccessible, or cannot support the claim. | Find the official owner or mark the claim unproven; do not cite a search result page as authority. |
| The repository changes after the observation identity. | Re-run the affected admission comparison and refresh only impacted claims before staging. |
| A validator requires unrelated policy, runtime, or pack changes. | Stop, preserve the failure, and escalate instead of broadening scope. |

## Failure Modes & Fallback / Human Escalation

- If no question in a planned research lane passes the admission gate, that
  lane becomes a documented no-op and produces no empty commit.
- If an external source conflicts with an accepted repository decision, the
  research records the conflict and routes it to the decision owner; it does
  not modify the decision.
- If Verification/Validation terminology cannot be mapped without changing the
  canonical quality contract, the research remains descriptive and the policy
  change is escalated separately.
- If Kubernetes analysis identifies a material vulnerability, the research
  records the bounded finding and proposed owner. Manifest or live remediation
  requires a separate approved security task.
- If exact staged validation cannot distinguish this refresh from RIA or
  protected-history drift, execution pauses before commit and requests a
  contract-owner decision.
- Remote publication, push, pull request, merge, branch deletion, and worktree
  removal remain separate finishing choices.

## Verification Commands

The implementation Plan will bind exact paths and evidence, but the required
repository-static lanes include:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-reference-information-architecture.py --root . --self-test
python3 scripts/validate-reference-information-architecture.py --root .
git diff --check
git diff --cached --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

The Plan must also define deterministic admission, source-row, claim-row,
workspace-selector, request-owner, protected-path, and one-off-residue checks.
Repository-static success does not establish hosted, provider-runtime, remote,
credential-bearing, or live success.

## Success Criteria & Verification Plan

| Criterion | Success condition | Evidence |
| --- | --- | --- |
| VAL-WERG-001 | Every requested category has exactly one gap-admission state and only admitted questions receive new research. | Deterministic admission inventory plus reviewer approval. |
| VAL-WERG-002 | The research result changes no pack directory or topic owner outside the five authorized existing files. | Exact Git path set and scope review. |
| VAL-WERG-003 | Every new source row has an official/primary URL, `2026-08-10` check date, adopted scope, rejected inference, and refresh trigger. | Ledger parser and source review. |
| VAL-WERG-004 | Every new claim has source linkage, exact workspace evidence, uncertainty, status, and surviving owner. | Claim parser, path/selector probe, and content review. |
| VAL-WERG-005 | Verification and Validation have externally sourced definitions plus an explicit workspace responsibility/evidence/failure matrix. | Focused report contract and independent review. |
| VAL-WERG-006 | Document-family additions distinguish external semantics from local profile/lifecycle facts and preserve Spec 052 decisions. | Section comparison and cross-link validation. |
| VAL-WERG-007 | Kubernetes additions are limited to line-level gaps not already closed by the existing report. | Pre/post duplication audit and security review. |
| VAL-WERG-008 | Existing IDs, original checked dates, terminal evidence, anchors, and historical records remain stable. | Diff audit, registry, links/owners, RIA, and protected-path checks. |
| VAL-WERG-009 | No tracked download, scratch matrix, generated research note, compatibility artifact, or other one-off residue remains. | Tracked/untracked residue inventory and reviewer confirmation. |
| VAL-WERG-010 | Logical commits and canonical targeted, affected, staged, tests, all-files, formatter, rerun, and diff evidence are complete. | Task handoff, Git log, validation results, and whole-branch review. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — direct human approval on 2026-08-09 authorizes this standalone gap-admission design; no separate PRD/AD program owner is asserted | VAL-WERG-001 | Written Spec review and exact admission inventory |
| N/A — the same direct approval governs in-place integration into the existing pack | VAL-WERG-002 | Exact changed-path scope and pack-owner review |
| N/A — the same direct approval governs primary-source provenance | VAL-WERG-003 | Source-register parser and primary-source review |
| N/A — the same direct approval governs exact workspace reconciliation | VAL-WERG-004 | Claim, path, and selector verification |
| N/A — the same direct approval requests explicit Verification and Validation treatment | VAL-WERG-005 | Source-backed terminology and workspace matrix review |
| N/A — the same direct approval preserves existing document-family and decision authority | VAL-WERG-006 | Spec 052 and document-family authority comparison |
| N/A — the same direct approval limits Kubernetes additions to proven research gaps | VAL-WERG-007 | Kubernetes pre/post duplication audit and security review |
| N/A — the same direct approval preserves identifiers, history, anchors, and protected state | VAL-WERG-008 | Terminal-owner diff review and strict links/RIA validation |
| N/A — the same direct approval requires one-off research residue cleanup | VAL-WERG-009 | Tracked and untracked one-off residue inventory |
| N/A — the same direct approval requires logical commits and canonical validation | VAL-WERG-010 | Git history, canonical validation sequence, and whole-branch review |

### Related inputs and future execution owners

- **Research-pack terminal design**: [Spec 053](../0053-workspace-engineering-research-pack-consolidation/spec.md)
- **Direct-approval lineage decision**: [ADR-0022](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Document taxonomy decisions**: [Spec 052](../../../../03.specs/0052-document-taxonomy-consolidation/spec.md)
- **Current research pack**: [2026-08-08 WER](../../../../90.references/research/0001-workspace-engineering/README.md)
- **Plan**: [active gap-only refresh Plan](./plan.md)
- **Task**: [active gap-only refresh Task](./plan.md)
