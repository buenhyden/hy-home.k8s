---
title: "Governance Decision Current-State Amendment"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-11-05"
layer: "architecture"
artifact_id: "ADR-0055"
---

# ADR-0055: Governance Decision Current-State Amendment

## Overview

The operator approved on 2026-11-05 a scoped amendment that brings the
accepted clauses of seven governance ADRs in line with the current repository.
It replaces only the clauses named below.
[ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md),
[ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md),
[ADR-0033](./0033-common-document-contract-v9.md),
[ADR-0036](./0036-common-knowledge-and-prompt-surfaces.md),
[ADR-0047](./0047-agent-contract-and-resource-ownership.md),
[ADR-0048](./0048-local-qa-and-semver-release-ownership.md) and
[ADR-0053](./0053-unvalidated-archive.md) stay accepted for every other
clause, and their bodies stay as dated decision history. This decision changes
no validator, registry or governance file.

## Context

The 2026-11-05 Stage 02 review recorded, in each ADR's Traceability, accepted
clauses that later decisions or the implementation replaced without restating
them. Rule 3 of the Stage 02 instructions forbids rewriting them in place, and
[ADR-0047](./0047-agent-contract-and-resource-ownership.md) and
[ADR-0049](./0049-external-data-service-contract-alignment.md) set the
pattern of one accepted record that replaces named clauses. The current
sources are:

- [ADR-0053](./0053-unvalidated-archive.md) and
  [`docs/98.archive/README.md`](../../98.archive/README.md): the archive is
  outside the document inventory and has no validator, Tombstone, Migration
  record or recovery identity.
- [`docs/02.architecture/AGENTS.md`](../AGENTS.md) rule 3 and
  [document lifecycle](../../../.agents/governance/document-lifecycle.md): a
  replaced Stage 02 document is summarized in the owning AD's Archived Lineage
  and deleted; the profile allows only `supersedes`.
- [`docs/99.templates/registry.json`](../../99.templates/registry.json):
  `schema_version` 10 with the `lifecycle_domains` key.
- [`.agents/evaluations/`](../../../.agents/evaluations/README.md): holds
  `harnesses/`, `templates/`, `README.md` and `results.md`; root `evals/` and
  its runner were retired under SPEC-0107.
- [`CHANGELOG.md`](../../../CHANGELOG.md) and
  [`scripts/release.py`](../../../scripts/release.py): the committed release
  owner under ADR-0048.
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) and
  [`.markdownlint-cli2.yaml`](../../../.markdownlint-cli2.yaml): both exclude
  `docs/98.archive/` except its `README.md`.

## Decision

The operator, as request owner, approved these replacements on 2026-11-05.
Compliance is confirmed by the strict document checks and by comparing each
clause with the source named in Context.

1. **Archive clauses.** ADR-0030's "minimal Git-backed lookup layer" with
   Migration and Tombstone records and its recovery-identity rules, ADR-0031's
   "bounded Archive validator" and "bounded safety and readability checks",
   ADR-0033's generation-aware Archive validation, v7/v8 historical-reader
   branch, `archive` family and `evidence` mode, and ADR-0048's recurring
   Archive checks for safe-path, integrity and source recovery, its named
   Archive regressions for validator changes and its "Archive boundary" label
   for REQ-0003-FR-0027 are replaced by
   ADR-0053: the archive is unvalidated and Git history alone recovers a
   document.
2. **Superseded ADR retention.** ADR-0030's "superseded ADRs remain in Stage 02
   and link reciprocally" with `superseded_by`, and ADR-0031's "accepted and
   superseded ADRs remain in Stage 02", are replaced by: a superseded or
   withdrawn ADR is summarized in the owning AD's Archived Lineage table and
   deleted in the same change; the successor names it in `supersedes` and
   Traceability.
3. **Registry identity.** ADR-0031's `lifecycleDomains` reads
   `lifecycle_domains`. ADR-0033's version 9 contract is succeeded by
   generation 10: the profile families are `common`, `evaluation`,
   `governance`, `operation`, `reference` and `sdlc`, and the modes are
   `authored`, `router`, `template`, `native` and `non-target`.
4. **Release ownership.** ADR-0033's Non-goal that adds no Release Record or
   CHANGELOG owner, and its external-release-evidence mode, are replaced by
   ADR-0048: `CHANGELOG.md` and `scripts/release.py` own release preparation.
5. **Evaluation ownership.** ADR-0036 Decision 3's sentence "Memory, rule,
   evaluation and script directories stay unadopted" with `evals/` owning the
   runner, its matching Consequences, and the Alternatives reason that an
   evaluation harness "already owns its runner" are replaced by: `.agents/evaluations/` is the adopted evaluation evidence
   owner (ADR-0047 clause 5). ADR-0047's "exclusive runner" is replaced by: the
   package holds evaluation forms and results and no runner; ADR-0048 retired
   it, and `scripts/validation/registry.json` owns gate selection. ADR-0047's
   pending knowledge-surface migration is recorded as implemented.
6. **Secret backend name.** "Vault" in the Non-goals of ADR-0036, ADR-0047 and
   ADR-0048 means the OpenBao backend
   ([ADR-0041](./0041-openbao-secret-backend.md)).
7. **Archive lint scope.** ADR-0053's "its files are excluded from formatters
   and Markdown lint" reads: its files other than `docs/98.archive/README.md`
   are excluded; the README stays formatted and linted as the stage index.

## Explicit Non-goals

- Changing a validator, the registry, governance text or configuration.
- Restoring any archive check, Tombstone, Migration record or `superseded`
  state.
- Restoring an evaluation runner or recurring grading.
- Replacing any of the amended ADRs as a whole.

## Consequences

- **Positive**: every accepted governance decision reads true against the
  repository, and the dated clarifications in the amended ADRs point to one
  approving record.
- **Negative**: a reader must combine each amended ADR with this record.
- **Operational**: none; the replaced clauses already had no implementing
  check.

## Alternatives

- **Successor ADRs that supersede each document**: rejected; it would delete
  seven records whose other clauses stay current and churn every inbound link.
- **Restoring the replaced checks and runner**: rejected; ADR-0048 and
  ADR-0053 removed them deliberately.
- **Editing the accepted clauses in place**: rejected by Stage 02 rule 3.

## Traceability

The amendment applies only to the clauses named in the Decision. The amended
ADRs keep their original bodies, and their 2026-11-05 clarifications refer to
this record.

- **Requirement**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
  FR-0012, FR-0013, FR-0015, FR-0020, FR-0023, FR-0024, FR-0027, FR-0029 and
  FR-0031.
- **Architecture**: [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Specification**: N/A — no Spec package; the implementation already exists.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md) | Replaces the Stage 98 lookup-layer, recovery-identity and superseded-ADR retention clauses | N/A — no Spec package; documentation amendment |
| [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Replaces the Archive validator and ADR retention clauses and the registry key name | N/A — no Spec package; documentation amendment |
| [ADR-0033](./0033-common-document-contract-v9.md) | Replaces the Archive generation, family and mode clauses and the release Non-goal | N/A — no Spec package; documentation amendment |
| [ADR-0036](./0036-common-knowledge-and-prompt-surfaces.md) | Replaces Decision 3's evaluation clause, its Consequences and the Vault name | N/A — no Spec package; documentation amendment |
| [ADR-0047](./0047-agent-contract-and-resource-ownership.md) | Replaces the exclusive-runner clause, the pending-migration status and the Vault name | N/A — no Spec package; documentation amendment |
| [ADR-0048](./0048-local-qa-and-semver-release-ownership.md) | Replaces the recurring Archive check, Archive regression and Archive-boundary clauses and the Vault name | N/A — no Spec package; documentation amendment |
| [ADR-0053](./0053-unvalidated-archive.md) | Replaces only the lint-exclusion scope | N/A — no Spec package; documentation amendment |
