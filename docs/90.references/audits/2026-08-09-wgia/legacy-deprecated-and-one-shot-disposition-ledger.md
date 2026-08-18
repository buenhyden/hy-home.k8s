---
title: 'Audit: Legacy, Deprecated, and One-shot Disposition Ledger'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Legacy, Deprecated, and One-shot Disposition Ledger

## Overview

This report owns candidate provenance, consumer evidence, replacement routing,
Keep/Integrate/Correct/Delete/DEFER decisions, and post-delete gates for
Legacy, Deprecated, duplicate, and one-shot artifacts. WGIA-009 rejects seven
legacy-name active owners as noncandidates and inventories the exact fifteen
one-shot paths already approved for integration with Spec 052 `WORK-001`.
None is currently deletion-ready because live consumers remain unresolved.

## Reference Type

Dated repository-static cleanup disposition ledger. It is not a delete list,
retirement policy, compatibility owner, or authorization for removal.

## Authority Boundary

Candidate classification follows current policy, provenance, consumers, and
replacement ownership rather than names. Existing audit packs are historical
evidence and Stage 98 is immutable. No current row is `Delete`; a future change
would require a new reviewed zero-consumer and post-delete proof.

## Scope

Included: exact tracked candidate paths, observation-state last-change commits,
current consumers and selectors, surviving owners, integration decisions,
evidence, historical routes, and post-delete gates. Excluded: name-only
classification, historical pack deletion, Stage 98 edits, implementation of
Spec 052 `WORK-001`, unproven removal, Current cutover, and destructive action.

## Definitions / Facts

### Legacy and Deprecated Documents

`docs/99.templates/support/legacy-cleanup-rules.md`, the five current
legacy-cutover contract/schema/validator/fixture/test surfaces, and this dated
ledger are active owners or consumers whose names contain legacy vocabulary.
They are rejected as noncandidates: basename vocabulary is not lifecycle or
one-shot evidence and cannot create a cleanup decision.

### One-shot Documents and Scripts

Spec 052 `REQ-WDTC-010`, its corpus-reduction contract, and the queued
`WORK-001` execution owner identify exactly fifteen one-shot paths: five census
JSON files, five exclusive validators, four focused regressions, and the
zero-referent cutover-manifest helper. They are candidates for `Integrate with
WORK-001`, not pre-approved `Delete` rows. Current live consumers must be
migrated and the complete WORK-001 zero-referent and post-change gates must
pass before any deletion can be proposed.

### Cleanup Disposition Convention

Every candidate row requires: candidate path, full source commit, candidate
class, exact current consumers, surviving replacement owner, one decision from
`Keep`, `Integrate`, `Correct`, `Delete`, or `DEFER`, supporting evidence, and
focused plus aggregate post-delete gates. Any missing field fails closed to
`DEFER`. `Delete` additionally requires zero current consumers, valid rendered
links, exact historical recovery, green post-delete checks, and independent
review.

`Exact current consumers` means every tracked machine projection, runtime or
test import/load, validator constant, aggregate invocation, and active human
index that must change if the candidate path becomes absent. Approved
Spec/Plan/Task citations, source-commit-bounded research/audit observations,
and this report's own evidence are recorded under Evidence or Historical route;
they remain recoverable references but are not mislabeled as executable or
current-index consumers.

### Candidate Discovery and Consumer Classification

| Candidate set | Exact result | Decision basis |
| --- | --- | --- |
| Filename candidates at observation commit | Six exact tracked paths: legacy-cutover contract, schema, validator, fixture, regression, and cleanup-rules owner. | Inspect each path's current contract role and literal consumers; do not classify by basename. |
| Filename candidates at starting HEAD `5db8fa365d1953861e80f1031003b08f69b132fd` | The same six plus this new dated disposition ledger: seven exact paths. | The ledger was absent at observation commit and was created at full commit `4611c0b5a555f0acb535b969adc58529d1ba8195`. |
| Content vocabulary | `git grep` reports 2,355 starting-HEAD tracked line hits and 2,360 after the five matched WGIA-009 Task evidence lines, with explicit Stage 98/audit/progress exclusions. | Rejected as name-only/content-only evidence; no hit is promoted without exact consumer and owner proof. |
| Retired agent surfaces | The five machine-declared retired paths are absent, five replacements exist, and the legacy-cutover validator reports zero active retired consumers. | Prior deletion is already closed historical evidence; absent paths are not new tracked candidates. |
| Existing historical audit packs | Six source-commit-bounded packs remain protected historical evidence. | `Keep`; they are not cleanup candidates and their bodies remain unchanged. |
| `docs/98.archive/**` | Protected archive corpus with zero observation-to-current or worktree diff. | `Keep`; immutable boundary, never a WGIA-009 candidate. |

The seven filename matches are explicitly rejected as candidates. Their
current ownership proves why vocabulary is insufficient:

| Rejected name-only path | Exact active consumers / owner evidence | Rejection reason |
| --- | --- | --- |
| `docs/00.agent-governance/contracts/agent-legacy-cutover.json` | `scripts/validate-agent-legacy-cutover.py#CONTRACT_PATH`; `tests/test_validate_agent_legacy_cutover.py#CONTRACT_PATH`; `scripts/reference_information_architecture.py#AGENT_LEGACY_CUTOVER_PATH` | Active machine contract, not a `Legacy` artifact. |
| `docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json` | `docs/00.agent-governance/contracts/agent-legacy-cutover.json#$schema`; `scripts/validate-agent-legacy-cutover.py#SCHEMA_PATH`; `scripts/reference_information_architecture.py#AGENT_LEGACY_CUTOVER_SCHEMA_PATH` | Active schema, not a `Legacy` artifact. |
| `scripts/validate-agent-legacy-cutover.py` | `.github/workflows/ci.yml#jobs.agent-governance-static`; `.pre-commit-config.yaml#validate-agent-legacy-cutover`; `scripts/validate-repo-quality-gates.sh#validate-agent-legacy-cutover`; `tests/test_validate_agent_legacy_cutover.py#VALIDATOR_PATH` | Active blocking validator, not a `Legacy` artifact. |
| `tests/fixtures/agent-legacy-cutover.json` | `scripts/validate-agent-legacy-cutover.py#FIXTURE_PATH`; `tests/test_validate_agent_legacy_cutover.py#FIXTURE_PATH`; `scripts/validate-active-corpus-role-audit.py#POST_CLOSURE_HELPER_MANIFEST` | Active mutation fixture, not a `Legacy` artifact. |
| `tests/test_validate_agent_legacy_cutover.py` | `scripts/validate-agent-legacy-cutover.py#PACKAGE_REFERENCES`; `scripts/validate-active-corpus-role-audit.py#POST_CLOSURE_HELPER_MANIFEST`; `tests/README.md#agent-legacy-cutover-fixture` | Active regression, not a `Legacy` artifact. |
| `docs/99.templates/support/legacy-cleanup-rules.md` | `scripts/archive_cutover.py#STALE_CONTRACT_SURFACES`; `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md#docs99templatessupportlegacy-cleanup-rulesmd`; `docs/04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md#wgia-009--disposition-ledger-and-integrated-roadmap`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#wgia-009-focused-evidence` | Active cleanup-rule owner, not a `Legacy` artifact. |
| `docs/90.references/audits/2026-08-09-wgia/legacy-deprecated-and-one-shot-disposition-ledger.md` | `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#audit-pack-components`; `docs/04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md#new-audit-pack`; `docs/90.references/audits/2026-08-09-wgia/README.md#request-coverage`; `docs/90.references/audits/2026-08-09-wgia/remediation-and-integration-roadmap.md#related-documents` | Active dated evidence owner, not a candidate merely because its title names the audited classes. |

### Candidate Disposition Ledger

`Source commit` is the last commit that defines the candidate at the
observation commit. The exact candidate set is the fifteen tracked paths named
by the approved Spec 052 `WORK-001` globs. Every row remains `Integrate` because
live consumers prevent zero-referent proof; no row is a `Delete` decision.

| Candidate path | Source commit | Observation state | Candidate class | Exact current consumers | Replacement / surviving canonical owner | Decision | Evidence | Historical route | Focused post-delete gates | Aggregate post-delete gates | Reviewer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/90.references/data/active-corpus-eligibility-ledger.json` | `414905ce4219a6c98088115485b37ad084e2951a` | Tracked one-shot evidence. | `one-shot` | `.gitleaks.toml#rules[id=generic-api-key].allowlists[1].paths`; `docs/90.references/README.md#reference-index`; `docs/90.references/data/README.md#data-reference-index`; `docs/90.references/data/active-corpus-migration-results.json#/eligibilityInput`; `docs/90.references/data/active-corpus-residue-closure.json#/sourceLedgers/1/path`; `docs/90.references/data/reference-information-architecture.json#/dataAssets/1/repositoryEvidence/0`; `scripts/validate-active-corpus-eligibility.py#LEDGER_PATH`; `scripts/validate-active-corpus-migrations.py#ELIGIBILITY_PATH`; `scripts/validate-active-corpus-residue-closure.py#SOURCE_PATHS`; `tests/test_active_corpus_eligibility.py#ActiveCorpusEligibilityTests.test_rejects_unsafe_path_without_echoing_payload`; `tests/test_active_corpus_retention.py#ActiveCorpusResidueClosureContractTests.test_closure_schema_normalizes_pair_keys_to_lineage_ids` | WORK-001 reduced current tree; RIA/data indexes, Gitleaks scope, validators, and regressions must be updated atomically. | `Integrate` | `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-2-wdtc-001--delete-the-completed-migration-census`; exact tracked-consumer scan; consumers are nonzero. | `git show 414905ce4219a6c98088115485b37ad084e2951a:docs/90.references/data/active-corpus-eligibility-ledger.json`; `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md#mutable-reference-classification`. | Eligibility/migration/residue self-tests and production; RIA/data-index/Gitleaks equality; zero-referent scan. | Full quality gate, strict registry/profiles/links, secret handling, archive validation/cutover, RIA, diff and Stage 98. | Pending WGIA-009 reviews; WORK-001 deletion requires a new independent review. |
| `docs/90.references/data/active-corpus-migration-results.json` | `468211cfc747d0234cda8e6ff372804593bb2e1f` | Tracked one-shot evidence. | `one-shot` | `docs/90.references/README.md#reference-index`; `docs/90.references/data/README.md#data-reference-index`; `docs/90.references/data/active-corpus-residue-closure.json#/sourceLedgers/2/path`; `docs/90.references/data/reference-information-architecture.json#/dataAssets/2/repositoryEvidence/0`; `scripts/archive_cutover.py#MIGRATION_RESULTS_PATH`; `scripts/validate-active-corpus-migrations.py#LEDGER_PATH`; `scripts/validate-active-corpus-residue-closure.py#SOURCE_PATHS`; `tests/test_active_corpus_migrations.py#VALIDATOR` | WORK-001 reduced tree, but `archive_cutover.py` must first lose or replace its live dependency. | `Integrate` | `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-2-wdtc-001--delete-the-completed-migration-census`; live archive-cutover dependency blocks `Delete`. | `git show 468211cfc747d0234cda8e6ff372804593bb2e1f:docs/90.references/data/active-corpus-migration-results.json`; dated WGIA security evidence remains historical. | Migration/residue regressions and archive-cutover production; zero-referent scan. | Full quality gate, strict documents, archive validation/cutover, RIA, diff and Stage 98. | Pending reviews; WORK-001 must resolve the live import/data dependency. |
| `docs/90.references/data/active-corpus-residue-closure.json` | `468211cfc747d0234cda8e6ff372804593bb2e1f` | Tracked one-shot evidence. | `one-shot` | `docs/90.references/README.md#reference-index`; `docs/90.references/data/README.md#data-reference-index`; `docs/90.references/data/reference-information-architecture.json#/dataAssets/4/repositoryEvidence/0`; `scripts/validate-active-corpus-residue-closure.py#LEDGER_PATH`; `tests/test_active_corpus_retention.py#RESIDUE_LEDGER_PATH` | WORK-001 reduced tree; RIA/data indexes and residue regression must be migrated together. | `Integrate` | `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-2-wdtc-001--delete-the-completed-migration-census`; exact live consumer inventory; no zero-referent proof. | `git show 468211cfc747d0234cda8e6ff372804593bb2e1f:docs/90.references/data/active-corpus-residue-closure.json`; Spec 047/CSSR Plan/Task citations remain dated decision evidence. | Residue self-test/production and retention regression; RIA/data-index equality. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; deletion remains WORK-001-owned. |
| `docs/90.references/data/active-corpus-retention-census.json` | `46b79fcd633bb4d38f34c929f70855810e21352b` | Tracked one-shot evidence. | `one-shot` | `.gitleaks.toml#rules[id=generic-api-key].allowlists[0].paths`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#/referencePolicy/protectedEvidenceFiles/0/path`; `docs/90.references/README.md#reference-index`; `docs/90.references/data/README.md#data-reference-index`; `docs/90.references/data/active-corpus-migration-results.json#/censusInput`; `docs/90.references/data/active-corpus-eligibility-ledger.json#/candidateRows/*/trackedCurrentConsumers`; `docs/90.references/data/active-corpus-residue-closure.json#/sourceLedgers/0/path`; `docs/90.references/data/reference-information-architecture.json#/dataAssets/0/repositoryEvidence/0`; `scripts/validate-active-corpus-retention.py#SNAPSHOT_PATH`; `scripts/validate-active-corpus-eligibility.py#CENSUS_PATH`; `scripts/validate-active-corpus-migrations.py#CENSUS_PATH`; `scripts/validate-active-corpus-residue-closure.py#SOURCE_PATHS`; `scripts/validate-agent-legacy-cutover.py#PROTECTED_EVIDENCE_FILES`; `tests/fixtures/agent-legacy-cutover.json#/mutationCases/14/mutation/path`; `tests/fixtures/agent-legacy-cutover.json#/mutationCases/15/mutation/path`; `tests/fixtures/agent-legacy-cutover.json#/mutationCases/16/mutation/path`; `tests/test_validate_agent_legacy_cutover.py#AgentLegacyCutoverValidatorTests.test_missing_protected_evidence_is_rejected`; `tests/test_validate_agent_legacy_cutover.py#AgentLegacyCutoverValidatorTests.test_protected_reference_removal_is_rejected` | WORK-001 reduced tree after migrating the legacy-cutover protection, active-corpus projections, RIA/data indexes, regressions, and Gitleaks allowlist. | `Integrate` | `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-2-wdtc-001--delete-the-completed-migration-census`; protected-evidence and allowlist consumers block `Delete`. | `git show 46b79fcd633bb4d38f34c929f70855810e21352b:docs/90.references/data/active-corpus-retention-census.json`; WER source-coverage record remains commit-bounded evidence. | Retention/eligibility/migration/residue/legacy-cutover gates and allowlist exactness; zero-referent scan. | Full quality gate, secret-handling lane, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; security/protected-evidence migration is required. |
| `docs/90.references/data/active-corpus-role-audit.json` | `38a2fe6b90bad694d0a9a021c7edce8d800e03ea` | Tracked one-shot evidence. | `one-shot` | `docs/90.references/README.md#reference-index`; `docs/90.references/data/README.md#data-reference-index`; `docs/90.references/data/active-corpus-residue-closure.json#/sourceLedgers/3/path`; `docs/90.references/data/active-corpus-residue-closure.json#/acer004Dependency/path`; `docs/90.references/data/reference-information-architecture.json#/dataAssets/3/repositoryEvidence/0`; `scripts/validate-active-corpus-residue-closure.py#SOURCE_PATHS`; `scripts/validate-active-corpus-role-audit.py#LEDGER_PATH`; `tests/test_active_corpus_role_audit.py#ActiveCorpusRoleAuditTests` | WORK-001 reduced tree after role-audit helper ownership and RIA/data indexes are retired together. | `Integrate` | `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md#task-2-wdtc-001--delete-the-completed-migration-census`; role-audit validator/tests still consume the ledger. | `git show 38a2fe6b90bad694d0a9a021c7edce8d800e03ea:docs/90.references/data/active-corpus-role-audit.json`. | Role-audit/residue self-tests and production; helper-manifest equality; RIA/data indexes. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; coupled role-audit retirement required. |
| `scripts/archive_cutover_manifest.py` | `4ccc616cbc16543cef9d5efbd381efc72b7c24c9` | Tracked one-shot helper with live imports. | `one-shot` | `scripts/archive_cutover.py#EXPECTED_ARCHIVE_PATHS`; `scripts/validate-document-lifecycle.py#EXPECTED_ARCHIVE_PATHS`; `scripts/validate-active-corpus-migrations.py#EXPECTED_ARCHIVE_PATHS`; `tests/test_document_lifecycle_archive_cutover.py#CUTOVER_MANIFEST` | Move required constants to a surviving canonical module or retain the helper; current WORK-001 zero-referent premise is not met. The missing `scripts/README.md#script-inventory` row is separately admitted as `WGA-RMP-HAR-001`, not falsely counted as an existing consumer. | `Integrate` | Approved WORK-001 plus three production imports and one regression import; `Delete` is blocked. | `git show 4ccc616cbc16543cef9d5efbd381efc72b7c24c9:scripts/archive_cutover_manifest.py`; Spec 052/WGIA citations remain decision evidence. | Archive-cutover and document-lifecycle regressions/production; import and zero-referent scans. | Full quality gate, archive validation/cutover, lifecycle, strict documents, diff and Stage 98. | Pending reviews; WORK-001 must reconcile the live imports first. |
| `scripts/validate-active-corpus-eligibility.py` | `4869365198799eb876447021e601621f8a36e426` | Tracked one-shot validator. | `one-shot` | `scripts/README.md#structure`; `scripts/README.md#python-validator-inventory`; `scripts/README.md#command-contract`; `scripts/validate-repo-quality-gates.sh#validate-active-corpus-eligibility`; `tests/README.md#structure`; `tests/README.md#validation-model`; `tests/test_active_corpus_eligibility.py#VALIDATOR` | WORK-001 reduced gate and inventories after its ledger/test are retired atomically. | `Integrate` | Approved WORK-001; aggregate/docs/test consumers remain. | `git show 4869365198799eb876447021e601621f8a36e426:scripts/validate-active-corpus-eligibility.py`; WER source-coverage record remains commit-bounded evidence. | Eligibility self-test/production and focused regression; aggregate-command and inventory equality. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; no zero-referent proof. |
| `scripts/validate-active-corpus-migrations.py` | `468211cfc747d0234cda8e6ff372804593bb2e1f` | Tracked one-shot validator with live dynamic load. | `one-shot` | `scripts/archive_cutover.py#_load_migration_validator`; `scripts/README.md#structure`; `scripts/README.md#python-validator-inventory`; `scripts/README.md#command-contract`; `scripts/validate-repo-quality-gates.sh#validate-active-corpus-migrations`; `tests/README.md#validation-model`; `tests/test_active_corpus_migrations.py#VALIDATOR` | WORK-001 reduced gate only after `archive_cutover.py` loses or replaces its dynamic dependency. | `Integrate` | Approved WORK-001; live dynamic load blocks `Delete`. | `git show 468211cfc747d0234cda8e6ff372804593bb2e1f:scripts/validate-active-corpus-migrations.py`. | Migration regression/self-test/production; archive-cutover production; aggregate/inventory equality. | Full quality gate, archive validation/cutover, strict documents, diff and Stage 98. | Pending reviews; live dynamic dependency must be resolved. |
| `scripts/validate-active-corpus-residue-closure.py` | `b703ff7a1e96d9070f500a18943aa356157814cf` | Tracked one-shot validator. | `one-shot` | `scripts/README.md#structure`; `scripts/README.md#python-validator-inventory`; `scripts/README.md#command-contract`; `scripts/validate-repo-quality-gates.sh#validate-active-corpus-residue-closure`; `tests/README.md#validation-model`; `tests/test_active_corpus_retention.py#RESIDUE_VALIDATOR_PATH`; `tests/test_active_corpus_retention.py#ActiveCorpusResidueClosureContractTests` | WORK-001 reduced gate/inventories after residue evidence and test assertions move or retire. | `Integrate` | Approved WORK-001; aggregate/docs/test consumers remain. | `git show b703ff7a1e96d9070f500a18943aa356157814cf:scripts/validate-active-corpus-residue-closure.py`; CSSR/WDTC citations remain decision evidence. | Residue self-test/production and retention module; aggregate/inventory equality. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; no zero-referent proof. |
| `scripts/validate-active-corpus-retention.py` | `46b79fcd633bb4d38f34c929f70855810e21352b` | Tracked one-shot validator. | `one-shot` | `scripts/README.md#structure`; `scripts/README.md#python-validator-inventory`; `scripts/README.md#command-contract`; `scripts/validate-repo-quality-gates.sh#validate-active-corpus-retention`; `tests/README.md#validation-model`; `tests/test_active_corpus_retention.py#VALIDATOR_PATH`; `tests/test_active_corpus_retention.py#ActiveCorpusRetentionContractTests` | WORK-001 reduced gate/inventories after census and coupled tests retire. | `Integrate` | Approved WORK-001; aggregate/docs/test consumers remain. | `git show 46b79fcd633bb4d38f34c929f70855810e21352b:scripts/validate-active-corpus-retention.py`; WER source-coverage record remains commit-bounded evidence. | Retention self-test/production and focused module; aggregate/inventory equality. | Full quality gate, strict documents, secret handling, archive validation, diff and Stage 98. | Pending reviews; no zero-referent proof. |
| `scripts/validate-active-corpus-role-audit.py` | `36402a9de9aa1dd43006f95bac9cd630a8ae73ab` | Tracked one-shot validator. | `one-shot` | `scripts/README.md#structure`; `scripts/README.md#python-validator-inventory`; `scripts/README.md#command-contract`; `scripts/validate-repo-quality-gates.sh#validate-active-corpus-role-audit`; `tests/README.md#validation-model`; `tests/test_active_corpus_role_audit.py#VALIDATOR_PATH`; `tests/test_active_corpus_role_audit.py#ActiveCorpusRoleAuditTests` | WORK-001 reduced gate/inventories after helper ownership and dated evidence are rerouted. | `Integrate` | Approved WORK-001; aggregate/docs/test consumers remain, while this audit's own citation is evidence rather than a live consumer. | `git show 36402a9de9aa1dd43006f95bac9cd630a8ae73ab:scripts/validate-active-corpus-role-audit.py`; WGIA/WDTC citations remain decision evidence. | Role-audit self-test/production and regression; aggregate/inventory equality. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; coupled evidence migration required. |
| `tests/test_active_corpus_eligibility.py` | `414905ce4219a6c98088115485b37ad084e2951a` | Tracked one-shot regression. | `one-shot` | `docs/90.references/data/active-corpus-role-audit.json#/helperTests/entries/21/path`; `docs/90.references/data/active-corpus-role-audit.json#/readmeRemediation/finalInventory/21`; `scripts/validate-active-corpus-role-audit.py#FROZEN_HELPER_PATHS`; `tests/README.md#structure`; `tests/README.md#validation-model` | WORK-001 reduced test inventory after role-audit helper ownership retires. | `Integrate` | Approved WORK-001; role-audit ledger/validator and test indexes remain live consumers. | `git show 414905ce4219a6c98088115485b37ad084e2951a:tests/test_active_corpus_eligibility.py`. | Eligibility regression plus role-audit self-test/production and helper-manifest equality. | Full quality gate, strict documents, archive validation, diff and Stage 98. | Pending reviews; coupled role-audit retirement required. |
| `tests/test_active_corpus_migrations.py` | `468211cfc747d0234cda8e6ff372804593bb2e1f` | Tracked one-shot regression. | `one-shot` | `docs/90.references/data/active-corpus-role-audit.json#/helperTests/entries/22/path`; `docs/90.references/data/active-corpus-role-audit.json#/readmeRemediation/finalInventory/22`; `scripts/validate-active-corpus-role-audit.py#FROZEN_HELPER_PATHS`; `tests/README.md#structure`; `tests/README.md#validation-model` | WORK-001 reduced test inventory after migration validator and role-audit ownership retire. | `Integrate` | Approved WORK-001; role-audit ledger/validator and test indexes remain consumers. | `git show 468211cfc747d0234cda8e6ff372804593bb2e1f:tests/test_active_corpus_migrations.py`. | Migration regression/self-test plus role-audit helper-manifest equality. | Full quality gate, archive cutover/validation, strict documents, diff and Stage 98. | Pending reviews; coupled retirement required. |
| `tests/test_active_corpus_retention.py` | `b703ff7a1e96d9070f500a18943aa356157814cf` | Tracked one-shot regression. | `one-shot` | `docs/90.references/data/active-corpus-retention-census.json#/activation/helperTests/proposalDelta/entries/0/path`; `docs/90.references/data/active-corpus-role-audit.json#/helperTests/entries/23/path`; `docs/90.references/data/active-corpus-role-audit.json#/readmeRemediation/finalInventory/23`; `scripts/validate-active-corpus-retention.py#HELPER_PROPOSAL_PATH`; `scripts/validate-active-corpus-role-audit.py#FROZEN_HELPER_PATHS`; `tests/README.md#structure`; `tests/README.md#validation-model` | WORK-001 reduced test inventory after retention/residue assertions and role-audit ownership retire. | `Integrate` | Approved WORK-001; census, role-audit ledger/validator, retention validator, and test indexes still consume the path. | `git show b703ff7a1e96d9070f500a18943aa356157814cf:tests/test_active_corpus_retention.py`; ACER/WDTC citations remain decision evidence. | Retention/residue regressions and self-tests; role-audit helper equality. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; coupled retirement required. |
| `tests/test_active_corpus_role_audit.py` | `36402a9de9aa1dd43006f95bac9cd630a8ae73ab` | Tracked one-shot regression. | `one-shot` | `docs/90.references/data/active-corpus-role-audit.json#/helperTests/proposalDelta/add/0/path`; `docs/90.references/data/active-corpus-role-audit.json#/helperTests/entries/24/path`; `docs/90.references/data/active-corpus-role-audit.json#/readmeRemediation/addedInventoryRows/9`; `docs/90.references/data/active-corpus-role-audit.json#/readmeRemediation/finalInventory/24`; `scripts/validate-active-corpus-role-audit.py#PROPOSAL_PATH`; `scripts/validate-active-corpus-role-audit.py#FROZEN_HELPER_PATHS`; `tests/README.md#structure`; `tests/README.md#validation-model` | WORK-001 reduced test inventory after role-audit and dated evidence are rerouted. | `Integrate` | Approved WORK-001; role-audit ledger/validator and test indexes remain consumers, while this audit's own citation is evidence rather than a live consumer. | `git show 36402a9de9aa1dd43006f95bac9cd630a8ae73ab:tests/test_active_corpus_role_audit.py`; WGIA citations remain dated evidence. | Role-audit regression/self-test/production; helper-manifest and test-index equality. | Full quality gate, strict documents, archive validation, RIA, diff and Stage 98. | Pending reviews; coupled evidence retirement required. |

The current WGIA-009 decision count is `Integrate=15`, `Delete=0`. No focused
or aggregate post-delete command was executed as deletion evidence. Spec 052
`WORK-001` retains implementation ownership and must first resolve every live
consumer above; only a future proof-complete, independently reviewed transition
may change any row to `Delete`.

### Blockers

| Blocker ID | Cause | Impact | Affected requests | Release condition | Owner | Evidence depth | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-WGA-DSP-001 | The initial unstaged production active-corpus migration run reported path-only `MIGRATION-SECRET-CLASSIFIER` for protected historical material; no payload or secret value was inspected. | The unsupported standalone invocation could not establish the required lane. | `REQ-WGA-025`, `REQ-WGA-026`; `VAL-WGA-010`, `VAL-WGA-012`. | Exact staged aggregate execution passed production migration with six batches, 12 records, 43 archive records, 362 historical links, 12 secret-clean records, and 15 repaired consumers while Stage 98 stayed unchanged. | active-corpus and security-classifier owners | `repository-static` | `Resolved` |
| BLK-WGA-DSP-002 | Initial RIA production rejected dirty/unsettled comparison inputs during authoring. | The unsupported dirty-worktree state could not establish current production evidence. | `REQ-WGA-025`, `REQ-WGA-026`; `VAL-WGA-012`. | Exact staged aggregate execution passed RIA self-test and production without changing the RIA owner or Current projection. | primary agent and RIA validation owner | `repository-static` | `Resolved` |
| BLK-WGA-DSP-003 | In an exact staged state, the combined active-corpus module run executes 150 tests with 149 PASS and one failure: `ActiveCorpusEligibilityTests.test_closed_self_test_matrix_covers_the_required_negative_boundaries` expects 53 self-test cases while the validator executes 57. | Production/self-test gates pass, but the broader unit family cannot be claimed PASS until its stale closed-matrix expectation is reconciled by the canonical test owner. This does not authorize test, validator, or candidate deletion in WGIA-009. | `REQ-WGA-026`; `VAL-WGA-010`, `VAL-WGA-012`. | Reconcile the eligibility test expectation with the current canonical validator under the active-corpus owner, then rerun the same 150-test module set with zero failures. | active-corpus test/contract owner; existing WORK-001 for coupled retirement; WGIA-014 for terminal validation | `repository-static` | `Open` |

### Finding Convention

Every material finding uses the complete pack field set and closed verdict/depth
vocabularies. A cleanup decision is separate from a finding verdict; neither
field can be inferred from the other.

#### WGA-DSP-001 — Exact candidates are classified without authorizing deletion

- **Request IDs**: `REQ-WGA-025`, `REQ-WGA-026`.
- **Scope**: tracked candidate provenance, consumers, replacement/owner routing, disposition, historical recovery, and post-delete gates.
- **Expected state**: every actual candidate is complete, name-only hits are rejected, protected history stays unchanged, and `Delete` appears only with proof-complete zero-consumer evidence.
- **Observed state**: seven legacy-name active surfaces are rejected as name-only noncandidates; the exact fifteen Spec 052 `WORK-001` one-shot paths have complete `Integrate` rows with live consumers and full observation source commits; 2,355 starting-HEAD/2,360 authored-worktree vocabulary line hits are rejected as candidate proof; `Delete=0`.
- **Evidence**: `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-007--deletion-by-proof`; `docs/99.templates/support/legacy-cleanup-rules.md#active-vs-historical-references`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#scanPolicy`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#referencePolicy`; `scripts/validate-agent-legacy-cutover.py#main`; `scripts/validate-active-corpus-role-audit.py#main`; `scripts/archive_validation.py#validate_archive_immutability`; `docs/98.archive/README.md#stage-contract`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#wgia-009-focused-evidence`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: active legacy-name owners remain available, and the one-shot set is routed without duplicating or prematurely executing `WORK-001`; WGIA-013 has no current direct `Delete` row, while Spec 052 retains the future zero-referent implementation decision.
- **Disposition**: `Integrate`.
- **Canonical owner**: this dated ledger for candidate evidence; Spec 052 Plan/Task `WORK-001` for implementation; current data, script, test, archive, lifecycle, RIA, and historical owners remain active until that work proves otherwise.
- **Verification**: exact seven-row noncandidate and fifteen-row/full-hash/consumer/decision probes; legacy-cutover, active-corpus, RIA, links, archive, registry, profiles, diff, and Stage 98 checks.
- **Uncertainty**: the candidate set, integration route, production active-corpus lane, and staged RIA lane are exact; live consumer migration, the one stale eligibility unit expectation, and future `WORK-001` deletion proof remain unresolved.
- **Blocker**: `BLK-WGA-DSP-003` remains open; `BLK-WGA-DSP-001` and `BLK-WGA-DSP-002` are resolved by the exact staged aggregate PASS. Every hypothetical future deletion must independently re-enter the full proof gate.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-DSP-001 | policy owner | `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-007--deletion-by-proof`; `docs/99.templates/support/legacy-cleanup-rules.md#active-vs-historical-references` | Classification and proof boundary. |
| SRC-WGA-DSP-002 | machine owner | `docs/00.agent-governance/contracts/agent-legacy-cutover.json#scanPolicy`; `docs/00.agent-governance/contracts/agent-legacy-cutover.json#replacementSurfaces`; `docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json#properties` | Exact current cutover evidence shape. |
| SRC-WGA-DSP-003 | evidence producer | `scripts/validate-agent-legacy-cutover.py#main`; `scripts/validate-links-and-owners.py#main`; `scripts/archive_validation.py#ARCHIVE_ROOT`; `scripts/README.md#script-inventory` | Consumer, history, and boundary evidence. |
| SRC-WGA-DSP-004 | historical snapshot | `docs/90.references/audits/2026-05-24-whga/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-02-whia/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-03-wdgh/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-04-wdcn/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-05-wea/README.md#snapshot-contract`; `docs/90.references/audits/2026-07-11-weia/README.md#snapshot-contract`; `docs/98.archive/README.md#document-index` | Historical interpretation and recovery only. |

## Review and Freshness

- Review status: `Approved` after content and quality fix-round re-review.
- Review disposition: `Approved` for the bounded repository-static
  classification and routing; fifteen `Integrate` decisions, seven
  rejected name-only noncandidates, and `Delete=0` are bounded
  results. One open unit-test blocker and the unresolved `WORK-001` live
  consumers keep the finding `Partial`; two authoring-state validation blockers
  are resolved by the exact staged aggregate PASS. This is not implementation
  or deletion approval.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: current cleanup policy, legacy-cutover machine contract,
  exact candidate consumers/replacements, and this dated evidence ledger.
- Refresh triggers: candidate, source commit, class, consumer, replacement,
  decision, evidence, post-delete gate, historical route, observation commit,
  or protected-boundary change.
- Hosted, provider-runtime, remote, credential-bearing, and live evidence
  remains `DEFER` unless a later authorized decision requires it.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/0055-workspace-governance-audit-and-remediation/spec.md)
- [Legacy Cleanup Rules](../../../99.templates/support/document-lifecycle.md)
- [Implementation Task](../../../03.specs/0055-workspace-governance-audit-and-remediation/tasks.md)
- [Prior Current Audit](../2026-07-11-weia/README.md)
