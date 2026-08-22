---
title: 'Document Taxonomy Consolidation Architecture Description'
type: sdlc/ad
status: active
owner: platform
updated: 2026-08-11
artifact_id: "AD-0011"
---

# Document Taxonomy Consolidation Architecture Description (AD)

## Overview

This architecture implements
[PRD-0008](../../01.requirements/0008-workspace-document-taxonomy-consolidation.md)
as one repository-local control plane for SDLC documents, template and profile
contracts, AI-agent governance, and validation. It organizes change evidence
around a Stage 03 work unit, retires the separate Stage 04 execution tree,
keeps Stage 05 operations stable, and assigns one authority to each rule and
evidence class.

The physical structure is deliberately local. ISO/IEC/IEEE 12207 provides a
lifecycle-process framework, ISO/IEC/IEEE 15289 permits information items to be
combined or split for a selected lifecycle, and GitHub Spec Kit and OpenSpec
show coherent Spec/Plan/Task change packages. None of those sources mandates
this repository's numbered folders, stable slugs, frontmatter, or validators.

## Boundaries & Non-goals

The architecture governs tracked documentation, document and agent-governance
machine contracts, templates, validation orchestration, supporting tests and
fixtures, generated documentation artifacts, and local Git evidence. It does
not govern GitOps desired state, live Kubernetes or Vault behavior, provider
authentication, hosted CI administration, credentials, publication, or remote
mutation.

Existing Stage 98 payload bytes, digests, source commits/blobs, legacy-envelope
identity, and recovery result are immutable in every phase. WORK-105 and
WORK-106 also preserve every existing path and wrapper byte. The sole
existing-record path/wrapper exception is the exact 93-row, ledger-gated
WORK-107 outer rehome defined below; WORK-108 and later restore full path and
wrapper immutability. Outside that bounded event, this program may append a
new ArchiveEnvelope for unique retired history and update the central index,
but it may not edit an existing record.

Stage 90 dated observations retain the facts and paths observed at their
cutoff. A current navigational index or an explicit historical annotation may
change when its contract allows; observation prose is not silently rewritten
to look current.

Existing PRD, AD, ADR, and Spec numbers remain stable. Accepted ADRs are
append-only decision evidence; changed decisions use a successor record rather
than rewriting an unrelated or accepted predecessor.

Explicit non-goals are `docs/05.operations` renumbering, a Release family or
`releases/` collection, removal of numbered stage prefixes, new tutorial or
explanation families, a parallel agent-system registry, provider adapter
redesign, and consolidation of validators with different failure semantics.

## Quality Attributes

| Attribute | Measure | Linked requirement |
| --- | --- | --- |
| Stable addressing | Stage 05 and every lifecycle identifier remain stable; mutable active filenames contain no date identity. | REQ-0008-FR-0002 through REQ-0008-FR-0004 |
| Work-unit locality | A retained Plan or Task has exactly one Stage 03 Spec sibling and one registry-owned lineage. | REQ-0008-FR-0001, REQ-0008-FR-0004 |
| Authority uniqueness | Each human rule and machine contract has one canonical owner; projections do not restate inventories. | REQ-0008-FR-0005, REQ-0008-FR-0006 |
| Historical integrity | Existing ArchiveEnvelope content is byte-stable and dated observation meaning is preserved. | REQ-0008-FR-0008, REQ-0008-FR-0009 |
| Fail-closed migration | Transition and terminal modes reject uncovered, ambiguous, or stale routes before a commit. | REQ-0008-FR-0010, REQ-0008-FR-0016 |
| Evidence honesty | Static declaration, provider enforcement, hosted CI, and remote/live observation cannot promote one another. | REQ-0008-FR-0013, REQ-0008-FR-0014 |
| Minimal enforcement | Similar scripts are merged only when owner, inputs, error semantics, and evidence outputs are the same. | REQ-0008-FR-0011, REQ-0008-FR-0012 |
| Reversibility | Each logical commit has an explicit mapping, validation result, and rollback unit. | REQ-0008-FR-0008 through REQ-0008-FR-0012 |

## System Overview & Context

### Target repository topology

```text
docs/
  00.agent-governance/   human policy, provider deltas, harness contracts
  01.requirements/       PRD                         <NNN>-<slug>.md
                         optional SRS                srs-<NNN>-<slug>.md
                         optional Interface Req.     ifc-<NNN>-<slug>.md
  02.architecture/
    descriptions/        AD                          ad-<NNNN>-<slug>.md
    decisions/           ADR                         <NNNN>-<slug>.md
  03.specs/              work unit                   <NNN>-<slug>/
    <NNN>-<slug>/
      spec.md             technical contract
      plan.md             ordered implementation design, when required
      tasks.md            execution state and evidence, when required
  05.operations/
    guides/ incidents/ policies/ runbooks/
  90.references/         dated research, audits, reference, data
  98.archive/            append-only ArchiveEnvelope records and index
  99.templates/          canonical forms and support rationale
scripts/                 declared validation and repository automation
```

`docs/03.specs/` has no terminal route. Its numeric slot remains unused;
number continuity is less valuable than avoiding a second broad path rewrite
and preserving stable Stage 05 links. A work unit may have only `spec.md`.
`plan.md` requires its sibling Spec, and `tasks.md` requires both siblings.

### Authority topology

| Plane | Canonical owner | Projection boundary |
| --- | --- | --- |
| Agent-facing document routing and execution policy | `docs/00.agent-governance/rules/document-authoring.md` | Root/provider gateways and skills route to it but do not copy the full rules. |
| Document route, profile, heading, status, template, and relationship values | `docs/99.templates/support/document-profiles.json` plus schema | Stage 00, templates, README indexes, and validators consume or explain values; they do not redefine them. |
| Template selection and lifecycle rationale | `docs/99.templates/support/document-contract.md` and `document-lifecycle.md` | Template forms contain author prompts and required structure only. |
| Agent system, role, permission, evidence, risk, approval, and provenance shape | Existing `harness-contract.json` plus schema | Provider adapters contain provider-native deltas only; no separate agent registry is introduced. |
| Validator lane and command selection | `validation-surfaces.json` | Pre-commit, affected selection, CI, and aggregate wrappers invoke the declared owner. |
| Historical evidence | Stage 98 archive index and immutable envelopes | Active documents link through the index; they do not rewrite archive payloads. |

### Migration state model

The route migration has three explicit states:

1. `legacy`: current Stage 03 Spec and Stage 04 Plan/Task routes are valid.
2. `transition`: only enumerated source and target pairs may coexist; one work
   unit cannot have two active owners, and unlisted new-route paths fail.
3. `terminal`: Stage 03 fixed-name routes are valid and every live Stage 04
   execution path or consumer fails.

Tests and registry compatibility land before document moves. An explicit
source-to-target mapping drives `git mv`; runtime slug inference is forbidden.
The terminal contract is activated only after old-route consumer count is zero.

### Material disposition model

Every candidate receives one disposition:

- `move-current`: current Spec/Plan/Task evidence moves without semantic loss;
- `archive-unique`: unique history becomes a new immutable ArchiveEnvelope and
  gains an index entry;
- `retain-observation`: dated fact text remains at its observation owner;
- `merge-successor`: non-duplicated content is integrated into a named current
  owner with provenance;
- `delete-redundant`: exact duplicate, reproducible generated output,
  superseded one-shot data, or zero-consumer helper is removed after evidence;
- `retain-contract`: a similar-looking validator remains because its rule,
  negative fixture, error semantics, or evidence lane is distinct.

No file is removed solely because it is old, large, legacy-labelled, or
similar in name to another file.

## Data Architecture

### Document identity and date policy

Identity is carried by a stable stage identifier or slug. Mutable authoring and
review dates remain in frontmatter. A date may remain in a path only when it is
part of immutable observation or event identity: dated Stage 90 packs and
snapshots, real Incident/Postmortem identities, and Stage 98 mirror paths.

Cross-stage lineage continues to use the registry's closed program or
standalone relationship data and reciprocal document links. This program does
not add ad-hoc frontmatter keys that compete with that owner. Accepted
[ADR-0024](../decisions/0024-terminal-artifact-identity-and-archive-layout.md)
owns the terminal form and archive-layout direction, and the PRD-0008 program
projection names that decision without rewriting accepted predecessor records.

### Stable Stage 98 migration invariant

WORK-105 and WORK-106 change no Stage 98 path or byte. WORK-105 acceptance and
a green WORK-106 validator tranche are both preconditions. WORK-107 only may
then replace the outer record location and terminal wrapper identity for the exact existing
93-record corpus, and only through a schema-versioned 93-row migration ledger
with one source, one unique target, and action `moved` per row. WORK-108 and later
return Stage 98 to an immutable path-and-byte state. For every row, the
archived payload bytes, `content_sha256` digest, `source_commit`, and
`source_blob` provenance remain exact.

The ledger also binds the legacy envelope identity and the terminal record so
both remain independently verifiable during review. Old-envelope proof must
succeed before any source removal, and read-only recovery from both the legacy
envelope and the terminal record must reproduce the same payload bytes. A
missing row, shared target, payload or digest drift, source-commit/blob drift,
unrecoverable legacy envelope, or unequal recovery result stops the migration.
This invariant replaces only the earlier mirror-path requirement; it preserves
the full-body, provenance, retention, and recovery guarantees.

### AI-agent governance extension

The existing harness contract gains a closed `agentSystems` policy and record-
shape section rather than a separate registry. Each admitted system or
workflow declares purpose, intended and prohibited use, accountable risk
owner, lifecycle state, actor context, trustworthiness risks, treatment,
residual risk, review date, tool and data boundaries, human oversight, and
deterministic stop conditions. Actual approval, trace, evaluation, and action
results are append-only redacted evidence at an approved Task, Runbook,
Incident, or provider-runtime evidence owner; the harness stores their required
shape and immutable evidence references, not the runtime event bodies.

Today `approval-boundaries.md` supplies the human `Evidence Location` routing
input. The target harness closes that selection through
`evidenceOwnerPolicies`: owner type
(`task`, `runbook-record`, `incident`, or `provider-runtime-record`), canonical
owner reference, allowed append principal class, immutability rule, retention
class, validator, and trust anchor. Repository records bind to a reviewed Git
blob and commit; provider records bind to the closed
`provider-runtime-evidence.json` identity and its observed provider evidence.
An unverified or self-asserted principal, mutable reference, missing trust
anchor, or owner that does not match the approval surface remains `DEFER` and
cannot authorize execution. Agents may propose redacted evidence, but only the
declared human/operator or provider evidence controller can attest it.
The harness schema, approval-boundary projection, provider evidence contract,
and validators change in one later logical implementation unit; this staged
design does not claim that resolver exists or is enforced yet.

The external sources below were observed on 2026-08-09 and inform local
controls; fields beyond their bounded product or framework claims are local
adaptations. Refresh the source ledger when an upstream source, harness schema,
approval boundary, or evidence policy changes. The risk policy is informed by
[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework),
[NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), and the
[ISO/IEC 42001 public summary](https://www.iso.org/standard/42001), without
claiming certification or implemented provider controls.

Closed subordinate policy and evidence-reference shapes cover:

- untrusted prompt/context and tool-output boundaries, prompt-injection and
  data-exfiltration controls, and an escalation owner, based on
  [OWASP agentic threats](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/);
- per-tool input/output validation, handoff coverage, enforcement availability,
  and fail mode, because [OpenAI tool guardrails](https://openai.github.io/openai-agents-js/guides/guardrails/)
  do not automatically cover every tool or handoff path;
- action-bound approval policy, action class, requester and approver principal,
  normalized/redacted target digest, arguments digest, authority scope,
  issue/expiry time, decision, approval evidence reference, and result evidence
  reference; [OpenAI HITL](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)
  informs the pre-action pause/resume boundary while the audit fields are local
  controls;
- trace ID, configuration digest, redaction, retention, access, and availability,
  because tracing may be unavailable under some runtime policies; a risk tier
  that requires tracing stops or remains `DEFER` unless an approved operator
  Runbook records a bounded exception;
- evaluation suite, trial count, grader version, trajectory evidence,
  adjudication, and promotion decision; [Anthropic's agent evaluation
  guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
  informs the task/trial/grader/trace/outcome distinction while versioning,
  adjudication, and promotion fields are local controls;
- instruction, skill, hook, and tool component source, revision, digest,
  reviewer, admission date, and supplier trust, using
  [SLSA provenance](https://slsa.dev/spec/v1.2/provenance) as a bounded model.

Each control separates `designEnforcementDisposition` from
`observedEnforcementEvidenceRef`. The design value may be `enforceable`,
`advisory`, or `unavailable`; observed enforcement remains `DEFER` without a
matching provider-runtime record. A repository-static PASS proves schema and
tracked content only; it cannot set provider enforcement, action execution, or
remote observation to PASS.

### Validator and script ownership

`validate-repo-quality-gates.sh` remains the aggregate repository gate. The
pre-commit and affected-surface runners converge on one declared selection and
orchestration contract. `validate-harness.sh` is retired only after every
consumer migrates. Registry, Markdown profile, links/owners, archive, security,
CI, and agent semantic validators remain separate when they have different
failure contracts.

The active-corpus and historical-lifecycle validators are quarantined for
disposition, not assumed dead. Each needs an input-consumer graph, unique-rule
inventory, and negative-fixture comparison. The final declared executable set
must equal the tracked executable set for governed lanes.

### Memory and generated data

The live progress ledger becomes a bounded current window. Closed sections
move through the approved archive mechanism and remain discoverable from an
index. Tracked stale `graphify-out/**` output is removed only after its current
consumers and reproducibility are proved; future generated output belongs in
ignored scratch unless a governed snapshot route explicitly admits it.

## Infrastructure & Deployment

Implementation occurs in the isolated local branch
`codex/docs-sdlc-governance-consolidation` through logical-unit commits. No
dependency is deployed and no remote or live action is part of this
architecture.

Each structural tranche follows tests-first contract migration, production
change, focused validation, affected validation, all-files validation, and a
diff/archive review. The pre-change baseline failures are preserved as named
evidence: document-registry temporary-memory allocation, detect-secrets
adjudication/baseline drift, and one Markdown heading violation. A tranche may
not reinterpret them as success or suppress the owning gates.

The migration stops before commit when any target exists unexpectedly, a
mapping source is missing, an existing archive path changes, an observation
body changes without disposition, a route has zero or multiple owners, a
deleted script has a consumer or unique negative fixture, an evidence class is
promoted, or a required repository-static gate fails.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0008-FR-0001](../../01.requirements/0008-workspace-document-taxonomy-consolidation.md#functional-requirements) | Stage 03 work-unit locality and retired Stage 04 execution route | [ADR-0024](../decisions/0024-terminal-artifact-identity-and-archive-layout.md) and [Spec 052](../../03.specs/0052-document-taxonomy-consolidation/spec.md) |
| N/A — REQ-0008-FR-0002 through REQ-0008-FR-0004 share the PRD source above. | Stable filename identity, Stage 05 stability, and registry-owned reciprocal lineage | N/A — ADR-0024 and Spec 052 share the target owners above. |
| N/A — REQ-0008-FR-0005 through REQ-0008-FR-0007 share the PRD source above. | Authority uniqueness, template parity, and explicit Release exclusion | N/A — ADR-0024 and Spec 052 share the target owners above. |
| N/A — REQ-0008-FR-0008 through REQ-0008-FR-0010 share the PRD source above. | Reviewed disposition, archive integrity, and fail-closed route transition | N/A — Spec 052 owns the migration contract. |
| N/A — REQ-0008-FR-0011 and REQ-0008-FR-0012 share the PRD source above. | Validator semantic preservation and consumer/fixture proof | N/A — Spec 052 owns script reconciliation. |
| N/A — REQ-0008-FR-0013 and REQ-0008-FR-0014 share the PRD source above. | Existing harness owner, risk/approval/provenance records, and evidence non-promotion | N/A — ADR-0024 and Spec 052 share the target owners above. |
| N/A — REQ-0008-FR-0015 through REQ-0008-NFR-0002 share the PRD source above. | Recoverable cleanup, green baseline, suspended-program safety, and local-only scope | N/A — Spec 052 owns the execution and verification design. |
