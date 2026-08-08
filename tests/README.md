# tests

> k3d/GitOps 저장소의 전역 검증 기준과 cross-repo evidence를 설명하는 진입 문서다.

## Overview

`tests/`는 애플리케이션 테스트 피라미드를 강제하는 폴더가 아니다. 이 저장소의 기본 검증 모델은 k3d GitOps 구성, Kubernetes manifest, secret handling, shell script, repository governance를 정적으로 확인하는 것이다.

실제 실행 가능한 검증 스크립트는 `scripts/`와 `infrastructure/tests/`에 둔다. 이 폴더는 여러 경로를 가로지르는 장기 테스트 산출물이나 evidence가 필요할 때만 확장한다.

### Audience

이 README의 주요 독자:

- Platform maintainers
- Operators
- Documentation writers
- AI agents

### Scope

#### In Scope

- 저장소 전체 검증 모델 설명
- k3d/GitOps/static validation evidence의 해석 기준
- 향후 cross-repo integration 또는 e2e evidence를 둘 때의 기준

#### Out of Scope

- 애플리케이션 단위 테스트 피라미드
- 소스 코드와 co-location되는 unit test 규칙
- live k3d bootstrap, ArgoCD sync, 외부 Vault 변경 같은 승인 필요 작업
- CI 원격 실행 결과를 로컬에서 통과한 것으로 간주하는 문서화

## Structure

```text
tests/README.md
tests/fixtures/agent-checkpoint.json
tests/fixtures/agent-evaluations.json
tests/fixtures/agent-governance-ci.json
tests/fixtures/agent-governance-closure.json
tests/fixtures/agent-harness-contract.json
tests/fixtures/agent-harness-semantics.json
tests/fixtures/agent-legacy-cutover.json
tests/fixtures/agent-loop-lifecycle.json
tests/fixtures/agent-model-fitness.json
tests/fixtures/agent-provider-runtime-evidence.json
tests/fixtures/agent-roster-admission.json
tests/fixtures/agent-roster-currentness.json
tests/fixtures/document-contracts/native-surface-cases.json
tests/fixtures/document-contracts/readme-profile-cases.json
tests/fixtures/document-contracts/registry-cases.json
tests/fixtures/document-contracts/template-compatibility.json
tests/fixtures/document-contracts/template-source-parity.json
tests/fixtures/document-lifecycle.json
tests/fixtures/github-actions-security.json
tests/fixtures/gitops-change-set/base/kustomization.yaml
tests/fixtures/gitops-change-set/base/removed-service.yaml
tests/fixtures/gitops-change-set/base/retained-configmap.yaml
tests/fixtures/gitops-change-set/cases.json
tests/fixtures/gitops-change-set/head/added-service.yaml
tests/fixtures/gitops-change-set/head/kustomization.yaml
tests/fixtures/gitops-change-set/head/moved-retained-configmap.yaml
tests/fixtures/links-and-owners.json
tests/fixtures/markdown-profiles.json
tests/fixtures/reference-information-architecture/current-owner.json
tests/fixtures/reference-information-architecture/generator-collision.json
tests/fixtures/reference-information-architecture/minimal-valid.json
tests/fixtures/reference-information-architecture/overlay-mutation.json
tests/fixtures/reference-information-architecture/policy-copy.json
tests/fixtures/reference-information-architecture/snapshot-mutation.json
tests/fixtures/reference-information-architecture/source-freshness.json
tests/fixtures/validation-surfaces.json
tests/fixtures/vault-eso-contracts.json
tests/test_active_corpus_eligibility.py
tests/test_active_corpus_migrations.py
tests/test_active_corpus_retention.py
tests/test_active_corpus_role_audit.py
tests/test_archive_cutover.py
tests/test_archive_recovery.py
tests/test_archive_validation.py
tests/test_document_lifecycle_agent_roster_cutover.py
tests/test_document_lifecycle_archive_cutover.py
tests/test_document_strict_cutover.py
tests/test_k8s_pre_edit_hook.py
tests/test_post_validate_runner_result.py
tests/test_provider_post_validate_hook.py
tests/test_reference_information_architecture.py
tests/test_run_validation_lane.py
tests/test_validate_agent_checkpoint.py
tests/test_validate_agent_evaluations.py
tests/test_validate_agent_governance_ci.py
tests/test_validate_agent_governance_closure.py
tests/test_validate_agent_harness_contract.py
tests/test_validate_agent_legacy_cutover.py
tests/test_validate_agent_loop_lifecycle.py
tests/test_validate_agent_model_fitness.py
tests/test_validate_agent_provider_canaries.py
tests/test_validate_agent_provider_config.py
tests/test_validate_agent_roster_admission.py
tests/test_validate_ci_python_contract.py
tests/test_validate_gitops_change_set.py
tests/test_workspace_boundary.py
```

## Configuration Boundary

This tree owns repository contract fixtures and validation entrypoints, not
application coverage policy or live environment state. Fixtures must remain
non-secret and deterministic; credentials, kubeconfigs, runtime diagnostics,
and secret values stay outside the repository.

## Validation

Use the exact focused commands and PASS/SKIP semantics in the validation model
below, then run `bash scripts/validate-repo-quality-gates.sh .` and applicable
pre-commit hooks. Do not report an unavailable optional tool or static check as
live readiness.

The sole local completion-order owner is
[Agent Quality Standards](../docs/00.agent-governance/rules/quality-standards.md):
`targeted -> affected -> staged -> tests -> all-files -> formatter-review -> rerun -> diff-checks`.
This README records current test commands and inventories without redefining
those step or result semantics.

## Operations

### Working Procedure

1. 기본 검증 기준은 [scripts/README.md](../scripts/README.md)와 [infrastructure/README.md](../infrastructure/README.md)를 먼저 확인한다.
2. manifest나 GitOps 구조를 바꾸면 `scripts/`와 `infrastructure/tests/`의 정적 검증을 함께 실행한다.
3. 이 폴더에는 여러 하위 시스템을 동시에 검증하는 산출물이 있을 때만 새 파일을 추가한다.
4. live cluster evidence는 사람 승인 bootstrap 또는 break-glass 절차로만 기록하며, 로컬 정적 검증과 분리해서 보고한다.

### Validation Model

| Area | Command | Evidence class |
| --- | --- | --- |
| Archive recovery/envelope fixture | `python3 -m unittest tests/test_archive_recovery.py` | Repo-static private-fixture evidence for SHA-1/SHA-256 Git identity, literal canonical paths, deterministic bounded Git execution, stable non-disclosing errors and representations, raw blob bytes, UTF-8 admission, duplicate-key rejection, byte-identical canonical frontmatter, typed archive-time replacement evidence, archive-to-archive rejection, metadata dependency, marker/payload-to-EOF grammar, final-newline preservation, collision safety, and worktree-byte substitution rejection; not production archive authority or corpus evidence |
| Archive validation fixture | `python3 -m unittest tests/test_archive_validation.py` | Repo-static import-only evidence for metadata order/type, Git blob and digest identity, payload mutation, mirrored path, source-tree-only historical links, current-tree confusion rejection, inventory-independent archive reactivation, active direct individual-archive links, duplicate `original_path` authority, archive immutability, finite current status/profile and exact public input contracts, private verified canonical CommonMark loading/return-shape checks, and payload-free diagnostics; not production archive authority or 31/202 corpus evidence |
| Archive cutover regression | `python3 -m unittest tests/test_archive_cutover.py` | Production worktree snapshot evidence that the cutover is atomic and emits named `ARCHIVE-CUTOVER-INCOMPLETE` diagnostics for any partial state; the GREEN snapshot preserves the immutable 31-record/202-link base proof and derives the ledger-backed 43-record/362-link/43-secret-clean aggregate, registry v8/template authority, manifest closure, and index-only replacement evolution. Real temporary-Git mismatches prove a staged draft or invalid UTF-8 blob is rejected even when the worktree copy is current, while a stage-zero regular current blob remains authoritative without a worktree copy; sanitized bounded blob errors fail closed without displaying payload or secret matches. |
| Active corpus migration regression | `python3 -m unittest tests/test_active_corpus_migrations.py`; `python3 scripts/validate-active-corpus-migrations.py --root . --self-test`; `python3 scripts/validate-active-corpus-migrations.py --root .` | Nineteen focused methods plus the exact thirty-two-case closed mutation matrix reject partial/skipped/reordered batches, explicit first through fifth prior-prefix drift, active source residue, payload byte drift, wrong first through sixth rollback parent, index membership drift, direct current archive links, duplicate originals, rogue archive additions, unsafe paths, hostile Git steering, and self-referential batch commits. The added security cases prove the classifier uses only the revalidated exact absolute hint, rejects relative/wrong-basename/repository/`/tmp` candidates, preserves detected-versus-classifier diagnostics, and applies actual effective owner/group/other execute plus directory traversal semantics, including root behavior. Production proves six complete pairs/twelve records, base-plus-additive 43/362, twelve secret-clean payloads, six repaired consumers in batch 6, and fifteen unique repaired current-or-migrated-original Markdown consumers across all batches. |
| Archive lifecycle cutover regression | `python3 -m unittest tests/test_document_lifecycle_archive_cutover.py`; `python3 -m unittest tests/test_document_lifecycle_agent_roster_cutover.py`; `python3 scripts/validate-document-lifecycle.py --root . --self-test`; `python3 scripts/validate-document-lifecycle.py --root . --mode staged` | Seventeen archive-focused methods and thirteen closed archive self-test fixtures retain the exact base `f8a54dd` staged/CI v7-to-v8 transition containing pinned registry blobs, all 31 same-path archive profile conversions, and the retired/new template pair. Independent temporary Git commit/index fixtures prove staged and explicit-ref byte-exact rejection for existing archive metadata/payload mutations while source-removal plus new mirrored archive creation remains allowed; malformed, missing, and noncommit identities fail closed. The same consumer additionally admits only staged/CI Spec 044 finite roster cutover from exact base `e324d4c1fa49ef7e508fa07c32e7f054f5a3a05e`: exactly `.agents/agents/{docs-researcher,quality-engineer}.md` and `.claude/agents/{docs-researcher,quality-engineer}.md`, with exact base/proposed Git-blob semantic projection+harness evidence for `10/3/30` to `12/4/48`; that cutover evidence does not establish admission/runtime/provider/live readiness. AREA-003 repository-static evaluation readiness is complete, while observed same-suite evaluation and final admission remain `DEFER`. Six focused roster tests and 24 roster-cutover self-test controls reject wrong mode/base/profile/path, any extra or missing path, base cutover paths, invalid inventory/surface-plan/projection, and malformed/missing/non-object/duplicate-key contract blobs fail closed. Partial, extra, wrong-base, wrong-registry-OID, missing-pair, registry drift, unrelated-profile, snapshot, and explicit-ref finite-cutover projections remain fail-closed without payload or secret scanning. |
| Workspace boundary regression | `python3 -m unittest tests/test_workspace_boundary.py`; `python3 scripts/validate-workspace-boundary.py --self-test`; `python3 scripts/validate-workspace-boundary.py --root .` | Sixteen focused methods plus the isolated self-test prove exact stage-zero `100644` README and root-ignore cardinality; full SHA-1/SHA-256 root-ignore OIDs; bounded immutable blob retrieval; extra/force-added, symlink/gitlink/nonregular/conflict, malformed-index, startup, and timeout rejection; and stable path-only diagnostics. Two hostile ignored-child policies and one divergent worktree-root policy prove only the staged root blob controls probe ignored/README unignored results. Four actual-repository index/object queries precede three isolated-context init/ignore queries; no actual-worktree `check-ignore` runs. Actual-path traversal/open/stat sentinels allow only isolated policy evaluation. |
| Active corpus retention regression | `python3 -m unittest tests/test_active_corpus_retention.py`; `python3 scripts/validate-active-corpus-retention.py --root . --self-test`; `python3 scripts/validate-active-corpus-retention.py --root .` | Thirty-eight ACER-001 focused methods plus the 27-case closed self-test prove the exact 110-row immutable candidate census, six-row delta, pair cardinality, source blobs/statuses, ledger and non-authoritative Spec-link evidence, explicit unresolved eligibility axes, two retained active controls, 24-record Stage 05 input, the pinned 29-file helper input, exact one-test proposal delta, proposed 30-file helper counts, and four dated official-method sources. Missing/extra/duplicate rows, premature eligibility or lineage inference, unowned DEFER, synthetic events, helper tracker promotion, helper observation/delta/proposed-count drift, unsafe candidate/control/Stage 05/helper paths, non-string diagnostic payloads, parent-relative paths, schema/count/control/source drift, wrong commit/blob/tree object, hostile Git steering, and ignored-workspace access fail closed with single-line value-free diagnostics. |
| Active corpus eligibility regression | `python3 -m unittest tests/test_active_corpus_eligibility.py`; `python3 scripts/validate-active-corpus-eligibility.py --root . --self-test`; `python3 scripts/validate-active-corpus-eligibility.py --root .` | Focused contract checks plus closed self-tests prove the 110-row pinned join, 12 eligible rows across the exact six complete pairs, 98 owned `DEFER` rows, retained Spec 037 controls, canonical archive routing, rollback readiness without a claimed cutover, and value-free path rejection. |
| Active corpus role audit regression | `python3 -m unittest tests/test_active_corpus_role_audit.py`; `python3 scripts/validate-active-corpus-role-audit.py --root . --self-test`; `python3 scripts/validate-active-corpus-role-audit.py --root .` | Repo-static ACER-004 evidence preserves the exact frozen 33-file helper ledger (12 Python, 14 JSON, 6 YAML, 1 README) and exact 24-record Stage 05 corpus while separately admitting exactly 33 identity-bound post-closure helpers. The prior RIA, harness, provider-evidence, checkpoint, loop-lifecycle, document strict-cutover, and GCQE-001/002 helpers are extended only by the three Spec 044 admission/evaluation/model-fitness fixtures, their three focused Python regressions, the exact agent-roster lifecycle cutover regression, the AGQC-002 governance-CI and AGQC-003 legacy-cutover fixture/regression pairs, and the Spec 046 closure-contract fixture/regression pair. The resulting current 66-file inventory is 28 Python, 31 JSON, 6 YAML, and 1 README. Production temporary-Git tests reject regular, sorted, README-listed helpers outside that exact identity/role manifest with `ROLE-AUDIT-HELPER-ADMISSION`; supported extensions alone confer no role. Every admitted helper remains an authoritative index/worktree or descriptor-bound proposed read and exact sorted `Structure` member; approved negative strings remain fixture data. |
| Reference information architecture regression | `python3 -m unittest tests/test_reference_information_architecture.py`; focused aggregate selector: `python3 -m unittest tests.test_reference_information_architecture.ReferenceInformationArchitectureTests.test_aggregate_runs_self_test_before_production -v`; `python3 scripts/validate-reference-information-architecture.py --self-test`; production: `python3 scripts/validate-reference-information-architecture.py --root . [--contract <path>] [--staged\|--commit git-sha1:<C3>] [--require-settled-baselines]` | The aggregate invokes exactly one isolated self-test before exactly one normal `--root` production check, without changing CI topology or the LLM-wiki generator owner. `--self-test` accepts no validation-mode arguments; normal, staged, and literal explicit-commit evidence modes are mutually exclusive, while terminal settlement is orthogonal. Exits are `0` for the named repository-static scope, `1` for ordered `RIA-CONTRACT`, `RIA-BOUNDARY`, `RIA-SNAPSHOT`, `RIA-OVERLAY`, `RIA-TRANSITION`, `RIA-SOURCE`, `RIA-GENERATOR`, or `RIA-DUPLICATE` findings, and `2` for input/configuration failure. Fixed bounded Git argv and descriptor-safe reads reject unsafe root/path/symlink/untracked authority, ambient Git steering, ignored `_workspace` traversal, and payload-bearing diagnostics; explicit mode alone provides C3 lineage evidence, and no mode claims CI, provider, remote, or live state. |
| Active corpus residue closure regression | `python3 -m unittest tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests`; focused terminal methods: `python3 -m unittest tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_spec039_frontier_accepts_active_and_exact_advanced_states tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_spec039_advanced_frontier_partitions_reciprocal_controls tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_spec039_reciprocal_controls_reject_malformed_frontiers tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_spec040_final_frontier_partitions_reciprocal_controls tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_spec040_frontier_rejects_closed_missing_and_duplicate_states tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_spec040_frontier_rejects_wrong_relation_and_document_authority tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_terminal_frontier_self_test_covers_active_advanced_final_and_blocked tests.test_active_corpus_retention.ActiveCorpusResidueClosureContractTests.test_production_validator_accepts_only_exact_frontier_shapes`; `python3 scripts/validate-active-corpus-residue-closure.py --root . --self-test`; `python3 scripts/validate-active-corpus-residue-closure.py --root .` | Forty-seven focused methods, 85 methods in the full retention module, and the isolated 23-case self-test preserve 12 migrated rows, 100 current `DEFER`/0 `retain`, exact 48/1/3 cardinality with four partial owned `DEFER`, terminal Spec 037 source facts, frozen 13 accepted-ADR / 29 generic done-Spec guards, exact object binding, and eight empty findings. The production CLI admits only the exact current Spec 039-active frontier (`active 2/1`, terminal controls `2/1`, terminal Specs `1`), the exact Spec 039-done / activated Spec 040 frontier (`active 2/1`, terminal controls `4/2`, terminal Specs `2`), or the exact final Spec 040-done frontier (`active 0/0`, terminal controls `6/3`, terminal Specs `3`). The final shape also requires the exact tracked ADR-0020 path as accepted platform-owned `sdlc/adr` terminal program-closure authority, removes only that exact authority from the immutable generic ADR guard, and leaves early ADR-0020 acceptance or any rogue accepted ADR visible as count drift. Production counts are derived only after complete row paths, lineage identities, pair cardinality, authority fields, indexed object-identity form, terminal authority, and registry relation tuples match that state-specific shape; the direct entrypoint regression proves a final frontier plus a well-formed rogue active pair is rejected. Spec 039 and Spec 040 reciprocal Plan/Task plus their done Specs leave generic active/done-Spec projections only when they are not terminal-owned. Missing, duplicate, mixed, wrong-authority, wrong-relation, wrong/missing/early ADR-0020 authority, or closed Spec 040 without exact done reciprocal Plan/Task inputs fail closed. Parent staging remains required for production index equality; PASS does not imply commit, CI, provider, remote, or live readiness. |
| Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | Repo-static |
| Document strict cutover regression | `python3 tests/test_document_strict_cutover.py` | Six focused tests prove that all three public document validators default to strict, accept only explicit strict, reject the retired compatibility value with argparse exit `2`, keep current command contracts free of compatibility invocations and stale v7 claims, prevent retired Stage 99 archive profile/form reintroduction, and preserve the exact Spec 033 no-growth retirement guard while the retired semantic-debt fixture remains absent. |
| Markdown profile self-test | `python3 scripts/validate-markdown-profiles.py --self-test` | Repo-static |
| Markdown profile repository check | `python3 scripts/validate-markdown-profiles.py --root .`; `python3 scripts/validate-markdown-profiles.py --root . --mode strict` | Repo-static strict-only evidence; omitting the mode is equivalent to explicit strict |
| Cross-document self-test | `python3 scripts/validate-links-and-owners.py --self-test` | Repo-static link, stage/collection-index, Stage 00 and Current-pack lifecycle-mirror, owner, and ledger mutation evidence |
| Cross-document repository check | `python3 scripts/validate-links-and-owners.py --root .`; `python3 scripts/validate-links-and-owners.py --root . --mode strict` | Repo-static strict-only evidence; the retired compatibility value is an argparse exit `2` boundary |
| Cross-document inventory | `python3 scripts/validate-links-and-owners.py --root . --inventory --format json` | Repo-static ordered registry population |
| Agent harness contract fixture | `python3 scripts/validate-agent-harness-contract.py --self-test`; `python3 -m unittest tests/test_validate_agent_harness_contract.py` | Repo-static exact 37-case closed evidence, including stable stale-cutoff and stale-evaluation-state rejection, plus focused authoritative cutoff, twelve-suite repository-static readiness, Claude supervisor least-privilege tools, role/projection, all-current consumer selection, zero legacy consumer, exact validator registration and exact eight-surface routing, permission, evidence, memory, sensitive-content, and regular-file boundary regressions. PASS does not establish actual evaluation/admission or provider-runtime/CI/remote/live readiness. |
| Agent harness contract repository check | `python3 scripts/validate-agent-harness-contract.py --root .` | Repo-static current `12/4/48`, achieved target mirror `12/4/48`, four evidence classes, four memory classes, fourteen `harness-contract/1.0.0/current` consumers, and zero legacy compatibility consumers; no provider-runtime, CI, remote, or live inference |
| Agent roster admission fixture | `python3 scripts/validate-agent-roster-admission.py --self-test`; `python3 -m unittest tests/test_validate_agent_roster_admission.py` | Exact 59-case closed mutation matrix plus thirteen focused tests for repository-static projection authorization, achieved/current separation, two projected candidates, seven final-admission conditions, four evaluation/memory classes, nine deferred evidence classes, eight surface plans, rollback, closed schema, path/symlink, and sensitive-memory boundaries |
| Agent roster admission repository check | `python3 scripts/validate-agent-roster-admission.py --root .` | Repo-static `state=repository-static-projected verdict=DEFER`, current `12/4/48`, achieved target mirror `12/4/48`; evaluation-backed final admission and provider runtime/hosted CI/remote/live promotion remain deferred |
| Agent evaluation fixture | `python3 scripts/validate-agent-evaluations.py --self-test`; `python3 -m unittest tests/test_validate_agent_evaluations.py` | Exact 60-case closed mutation matrix plus thirty-three focused tests for exact harness suite/version binding, twelve role suites × four classes의 48 role-specific executable synthetic scenarios, stable identity/digest, generic-placeholder rejection, twelve adjudication-readiness records, roster-admission candidate/source digest에 직접 결합된 two rollback records, nine high-risk independent reviews, four promotion blockers, redacted data, four memory boundaries, raw root와 five governed inputs의 fail-closed symlink/non-regular/path-escape/sensitive-content/non-disclosing read boundaries |
| Agent evaluation repository check | `python3 scripts/validate-agent-evaluations.py --root .` | Repo-static `roles=12 fixtureClasses=4 corpusRecords=48 highRiskRoles=9 adjudicationRecords=12 rollbackRecords=2 promotionBlocks=4 deferredEvidence=9`; readiness review alone is `PASS`, while execution, runtime, provider resolution, authentication, live action, evaluation/admission/model decisions remain `DEFER` |
| Agent-governance CI fixture | `python3 scripts/validate-agent-governance-ci.py --root . --self-test`; `python3 -m unittest tests/test_validate_agent_governance_ci.py` | Exact `truth_cases=6 mutation_cases=45` inventory and thirty-two focused artifact, schema, semantic, path/symlink/non-regular, duplicate-key, topology, inherited-secret, skipped-step, custom/default-shell, exact-run-sequence, exact-summary-shape/digest, job/step fail-open, security, closure routing/order, explicit-root aggregate invocation, canonical evidence vocabulary, provider-evidence aggregate ownership/removal/source-digest boundary, local-QA order/inventory, and evidence-boundary regressions |
| Agent-governance CI repository check | `python3 scripts/validate-agent-governance-ci.py --root .` | Repo-static `route_classes=12 delegated_checks=18 truth_rows=6 deferred_owners=1 qa_surfaces=10`; PASS includes the closure self-test/production pair and sole repository-static checkpoint self-test delegation alongside harness-semantics and legacy-cutover delegation, proves only the closed selector/job/summary/route/delegation/security/local-QA contract, and leaves the Spec046 hosted CI, branch protection, provider runtime/auth/model discovery, provider resume/handoff canary, remote, and live evidence `DEFER` |
| Agent-governance closure fixture | `python3 scripts/validate-agent-governance-closure.py --root . --self-test`; `python3 -m unittest tests/test_validate_agent_governance_closure.py` | Closed Spec 046 program-lineage, provider, roster/model-fitness, four-class memory, QA/review/handoff, non-transitive evidence-lane, sensitive-content, path, schema, and mutation evidence. Repository-static PASS never promotes hosted CI, provider discovery/auth/model execution, remote/live, or provider-local memory to durable proof. |
| Agent-governance closure repository check | `python3 scripts/validate-agent-governance-closure.py --root .` | Validates the pinned upstream program authorities and exact repository-static closure projection while retaining every external or unexecuted lane as owned `ABSENT`/`DEFER`; PASS is contract evidence only. |
| Agent model-fitness fixture | `python3 scripts/validate-agent-model-fitness.py --self-test`; `python3 -m unittest tests/test_validate_agent_model_fitness.py` | Exact 33-case closed mutation matrix plus 28 focused tests for authoritative cutoff, harness observation separation, tracked incumbent values, checked Spec 042 validator import, exact ten-source ledger and `publishedAtUtc` cutoff-day UTC semantics, provider source ownership/classification/confidence/date binding, exact quality/safety/cost/latency thresholds, checked AREA-003 validator import and nested corpus/input/fixture-manifest digest validation, suite/adjudication/rollback binding, 48 provider tuples, fallback, decision-plane separation, and fail-closed root/input symlink, intermediate-path, non-regular, containment, semantic-drift, and non-disclosing CLI boundaries |
| Agent model-fitness repository check | `python3 scripts/validate-agent-model-fitness.py --root .` | Repository-static `roles=12 providers=4 tuples=48 mappingReady=21 mappingDeferred=27 fitnessDeferred=48 thresholdDeferred=48 promotionDeferred=48 canaryDeferred=48 runtimeDeferred=48`; local 12 and fixed-cutoff Claude high-risk 9 mappings are ready, while current-only Claude/Codex and mixed/unresolved Gemini mappings remain deferred. No result proves model execution, threshold fitness, promotion, provider runtime resolution, authentication, hosted CI, remote, or live evidence |
| Agent loop lifecycle regression | `python3 -m unittest tests.test_validate_agent_loop_lifecycle`; `python3 scripts/validate-agent-loop-lifecycle.py --self-test`; `python3 scripts/validate-agent-loop-lifecycle.py --root .` | Focused contract, destination-ID/order/owner-reference, review, and raw-promotion mutations prove the four memory classes, atomic/redacted synthetic checkpoint boundary, repository-wins resume, promotion/refresh/expiry/archive-GC/conflict, compaction, handoff, and five bounded reviewed feedback destinations. PASS does not read or write ignored checkpoints or establish provider/runtime/CI/remote/live/actual checkpoint execution. |
| Agent checkpoint lifecycle regression | `python3 scripts/validate-agent-checkpoint.py --root . --self-test` | Closed checkpoint mutations validate atomic/redacted synthetic checkpoint shape, repository-wins resume, promotion/refresh/expiry/archive-GC/conflict, compaction, and handoff. Its repo-static PASS is not provider discovery, hook delivery, permission, model, authenticated, hosted-CI, remote, credential-bearing, live, or actual checkpoint-execution evidence. |
| Provider evidence contract fixture | `python3 scripts/validate-agent-provider-evidence.py --root . --self-test`; `python3 -m unittest tests.test_validate_agent_provider_config tests.test_validate_agent_provider_canaries` | Thirty-six focused tests plus exact config 13-case and canary 8-case closed mutation sets for duplicate keys, cutoff confidence, local/prior observation provenance, current Gemini repository-static surface with absent native discovery, model/fallback/fitness gates, MCP role bounds, secret-like values, redaction, non-transitive verdicts, no-mutation canaries, and explicit-root propagation from a foreign working directory. The regressions independently cover aggregate and standalone-canary raw symlink/lexical-`..` roots, descriptor-bound parent/final identity swaps, a symlink governed parent, all five JSON owner classes as final symlink/directory/FIFO nodes, outside-repository current role/file projections, missing-parent expected absence, an existing regular-file/non-directory declared-absent parent, and every existing declared-absent node including a broken symlink; input failures emit value-free `PNME-INPUT` with exit `2`. |
| Provider evidence repository check | `python3 scripts/validate-agent-provider-config.py --root .`; `python3 scripts/validate-agent-provider-canaries.py --root .`; composed route: `python3 scripts/validate-agent-provider-evidence.py --root .` | Repo-static four-provider, ten-source, eight-model, seven-MCP, twelve-canary contract evidence only; executable presence or absence never proves authenticated provider runtime, model resolution, CI, remote, or live readiness |
| Agent harness semantics fixture | `python3 scripts/validate-agent-harness-semantics.py --self-test` | Repo-static 768-case category mutation evidence plus nine closed Gemini-native five-field metadata mutations; model/tool candidates are deliberately outside adapter frontmatter |
| Agent harness semantics repository check | `python3 scripts/validate-agent-harness-semantics.py --root .` | Repo-static 48-adapter semantic coverage across local, Claude, Codex, and Gemini surfaces |
| Agent legacy cutover fixture | `python3 scripts/validate-agent-legacy-cutover.py --root . --self-test`; `python3 -m unittest tests/test_validate_agent_legacy_cutover.py` | Closed `positive_cases=3 mutation_cases=24` zero-consumer, retired-path, canonical replacement, historical-evidence, duplicate-key, tracked-only Git candidate-source, hostile environment/executable, timeout/pipe cleanup, candidate/path/file resource bounds, root-dirfd swap closure, ignored and non-ignored untracked sentinels, staged consumer, bounded diagnostic, symlink/non-regular, and GitHub hub cutover evidence plus thirty-two focused tests |
| Agent legacy cutover repository check | `python3 scripts/validate-agent-legacy-cutover.py --root .` | Repository-static deterministic Git-index-only result `scanned_files=809 evidence_references=43 active_consumers=0`; ignored and non-ignored untracked paths are never opened or counted, retired role-semantics compatibility surfaces and the retired GitHub hub path are absent, current consumers select harness owners, and `.github/README.md` is canonical; closed limits are 10-second execution, 2-second cleanup, 262144/16384-byte Git pipes, 2048 candidates, 1024-byte paths, 8388608-byte regular files, and 512-byte diagnostic detail; no hosted/provider/runtime/remote/live claim |
| Agent roster currentness fixture | `python3 scripts/validate-agent-roster-currentness.py . --self-test` | Repo-static |
| Agent roster currentness repository check | `python3 scripts/validate-agent-roster-currentness.py .` | Repo-static |
| Affected-surface fixture | `python3 scripts/validate-affected-surfaces.py --root . --self-test` | Repo-static `surfaces=22 mutation_cases=38` duplicate-JSON, exact-route, argv, output, NUL-transport, existing-node and exact shared-symlink-target boundaries, plus focused agent-harness/loop/checkpoint, Spec 044 admission/evaluation/model-fitness, Spec 045 agent-governance CI selection, and Spec 046 closure-validator selection evidence across the required agent/governance/script/test surfaces |
| Affected-surface repository coverage | `python3 scripts/validate-affected-surfaces.py --root .` | Repo-static tracked-path coverage; no ignored scratch traversal |
| Affected/staged/all-files local runner | `python3 scripts/run-validation-lane.py --root . --lane affected\|staged\|all-files --paths-file <file.nul> --delimiter nul`; `python3 -m unittest tests/test_run_validation_lane.py tests/test_post_validate_runner_result.py tests/test_provider_post_validate_hook.py` | Repo-static shell-free execution of contract-selected argv under a closed startup environment and fixed absolute tool search path. Twenty-two production-isolation, staged-lane selection, marker-cardinality, hostile PATH/BASH_ENV/PYTHONPATH/Gitleaks-hint, exact secure passwd-home executable, unsafe candidate, effective owner/group/other execute and full directory traversal, root semantics, pure selector/runner, hook-log, and actual provider-entry regressions prove caller state cannot forge success. The staged runner uses the exact staged path set but remains separate from plain `pre-commit run` against the Git index; the all-files runner does not replace `pre-commit run --all-files`. The secure executable hint never broadens PATH. Claude, Codex, and Gemini commands execute the production hook in a bounded fixture: valid manifest/docs payloads preserve all 7/4 validators and existing Markdown path arguments, while malformed JSON fails closed. |
| CI Python and frozen-hook supply-chain regression | `python3 -m unittest tests/test_validate_ci_python_contract.py`; `python3 scripts/validate-ci-python-contract.py --self-test`; `python3 scripts/validate-ci-python-contract.py --root .` | 77개 focused test와 33-case self-test가 임시 최소 저장소 및 실제 root에서 exact three-line direct input, fully resolved 16-package Linux/CPython 3.12 lock, 모든 패키지의 exact pin/SHA-256 hash, inventory digest, 네 validation job의 exact binary-only/hash-required install, validation set 밖 Python/pip install 소유권 부재를 검증한다. 양쪽 job ownership에 적용되는 closed bypass matrix는 `sudo`/`command`/`time`/`env` 등의 wrapper, quoted·bare·absolute·relative·versioned Python/pip launcher, pip global option의 separate/equals/literal/dynamic/unknown 분류, 제어문·subshell·command substitution, backslash-newline continuation, nested shell `-c`, 동적 command-position indirection을 검사한다. 별도 unsupported-grammar matrix는 literal `pip` 유무와 무관하게 normalized quoted/wrapped eval/source/dot/alias/coproc/builtin, function, heredoc, process substitution, shell stdin, array, multiline quote를 차단한다. 명시적으로 분류되지 않은 executable과 모든 `xargs` 형태는 인자 내용과 무관하게 fail closed이고, tar/install의 외부 command 실행 옵션과 Git cat-file/diff의 full·equals·subcommand별 accepted long-option abbreviation도 quoted, wrapper, inline config assignment 정규화 뒤 거부된다. Git exact `--` terminator 이후 operand, exact safe `diff --text`, negated options, ambiguous/invalid shorter prefix는 안전 대조군으로 유지된다. executable `ci-summary` truth-table 회귀는 selected PASS/FAIL/SKIP/missing/cancelled 동작을 보존한다. 64KiB 입력과 6단계 재귀로 제한된 fail-closed guard는 parser/recursion ambiguity를 같은 stable workflow rule로 거부하면서 comments, exact `echo`/`printf`/`grep` controls, `mypython`, `pipx`, 현재 명시 safe-command set을 안전 대조군으로 유지한다. 12개 non-local pre-commit repo의 unique 40-character frozen commit과 자기 repo stanza 내부의 exact anchored source-tag provenance를 요구하고 moved-comment 우회, tag/branch/abbreviation/wrong or missing rev/duplicate/local-rev를 차단한다. Symlink/비정규 root·parent·final node와 descriptor-bound identity swap을 다섯 governed input에서 fail-closed로 검사한다. 열세 stable rule ID의 exact duplicate-free inventory와 파생 self-test count를 검증하며 validator 자체는 네트워크를 사용하지 않는다. |
| GitHub Actions security fixture | `python3 scripts/validate-github-actions-security.py --self-test` | Tier A required aggregate evidence preserving exactly eleven primary, ten repository-boundary, twenty-one required-write, and four exact artifact-retention JSON cases, plus five internal uses-shape, one boolean-retention, four malformed artifact-structure, and one mixed-case artifact-owner cases |
| GitHub Actions security repository check | `python3 scripts/validate-github-actions-security.py --root .` | Tier A required aggregate evidence; `PASS` enforces immutable Action identities, least-privilege permissions, and integer-only seven-day artifact retention |
| GitOps identity change-set fixture | `python3 scripts/validate-gitops-change-set.py --self-test`; `python3 -m unittest tests/test_validate_gitops_change_set.py` | Repo-static exact one ADD, one DELETE, and one path-only RETAIN plus portable FIFO-or-directory non-regular, unsafe-ref/path, symlink/non-regular, cycle, duplicate, malformed-token, unsupported-dialect/directive, multi-document, root/two-commit, and shallow-parent rejection coverage; forbidden manifest values remain excluded |
| GitOps identity change-set repository check | `python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD` | Repo-static identity-only rows; no Argo CD prune or reconciliation claim |
| Vault/ESO contract fixture | `python3 scripts/validate-vault-eso-contracts.py --self-test` | Repo-static exact ten-case non-secret mutation evidence |
| Vault/ESO repository check | `python3 scripts/validate-vault-eso-contracts.py --root .` | Repo-static identity, audience, policy, local-only transport, and bootstrap process-boundary evidence; no live or secret-value claim |
| External service contracts | `bash infrastructure/tests/verify-contracts-static.sh` | Repo-static |
| GitOps structure | `bash scripts/validate-gitops-structure.sh` | Repo-static |
| Kubernetes manifests | `bash scripts/validate-k8s-manifests.sh .` | Repo-static with Optional tool `kube-linter` when installed |
| Secret handling | `bash scripts/check-secret-handling.sh .` | Repo-static |
| Policy gates | `bash scripts/validate-policy-gates.sh .` | Repo-static with Optional tool `conftest` when installed |
| Shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | Repo-static |
| Live runtime checks | `bash infrastructure/tests/run-all.sh` after approved bootstrap | Live/operator-owned |

Repository quality is an orchestrator boundary: it invokes the registry,
Markdown-profile, cross-document, affected-surface, agent-harness-contract,
provider-evidence, loop lifecycle self-test and production check, checkpoint
self-test, agent-role-semantic, and roster-currentness validators in strict
blocking mode,
then runs only retained
workspace-domain and surface-specific metadata checks. Shared semantic
validation does not copy model/tool/effort fields; those values and exact scope
imports remain surface-specific adapter evidence. Report `affected`, `staged`,
`all-files`, `message/manual`, `ci`, and `remote/live` through the canonical
contract in `docs/00.agent-governance/rules/quality-standards.md`; static
adapter PASS does not prove provider runtime consumption.

### Evidence Boundaries

- `tests/test_archive_recovery.py` creates only temporary isolated Git
  repositories. Its fifteen cases recover committed SHA-1 and SHA-256 blob
  bytes through Git objects, mutate a worktree control without accepting those
  bytes, and cover missing/full-versus-abbreviated object IDs, wrong paths,
  non-UTF-8 input, noncanonical raw paths including DEL, literal metacharacter
  filenames, metadata reason/replacement dependencies, duplicate frontmatter
  keys, noncanonical CRLF/spacing serialization, exact v1 marker placement,
  payload collision text, final-newline states, payload-free representations,
  isolated hostile Git state, bounded subprocesses, and stable root/startup/
  timeout/object-format errors. Its inline-link count is explicitly a bounded
  candidate metric, not historical resolution evidence. The test does not read
  or migrate `docs/98.archive`, activate a registry/form/predicate, inspect
  ignored `_workspace` children, or claim the 31-record/202-link corpus proof.

- `tests/test_archive_validation.py` creates only temporary isolated Git
  repositories and passes immutable archive/current-document inputs directly to
  the import-only ARWB-002 interfaces. Its twenty-two cases prove canonical
  envelope/provenance/integrity checks, literal source-commit link existence,
  canonical rendered CommonMark reuse, mirror and unique-authority rules,
  reactivation/current-direct-link rejection, and mutation/deletion rejection.
  A current-worktree-only target remains a historical miss. Malformed sequence,
  mapping, inventory, status, profile, path, adapter import/call, and adapter
  return-shape inputs fail with fixed value-free diagnostics; a poisoned
  predictable module cache is ignored. Payload-derived Markdown/link and caller
  values are absent from representations and diagnostics. It does
  not enumerate or modify `docs/98.archive`, activate a route/form/predicate,
  activate production archive authority or inspect ignored `_workspace` children.

- `tests/test_archive_cutover.py` invokes the local/manual ARWB-003 validator on
  the repository snapshot and exercises bounded partial projections. The
  expanded cases preserve the exact closed 31-record/202-link base proof while
  the current ledger-backed GREEN is 43 records, 362 links, and 43 secret-clean
  payloads; they also cover named RED output, structured manifest/external-table
  rejection; recovery-grade hostile Git isolation; stable root, registry,
  startup, and timeout diagnostics; stale retired role; direct current link;
  duplicate original owner; immutable-envelope/index replacement separation;
  archive, missing, unselected, template, draft, and archived replacement
  targets; and missing required envelope replacement. Repeated partial
  projections stub only the already-proven secret-classifier call while still
  exercising production envelope/provenance/history logic. The validator
  suppresses classifier stdout/stderr, never includes payload bytes in report
  objects, and inventories tracked/untracked `docs` paths without traversing
  ignored `_workspace` children.

- `tests/test_active_corpus_migrations.py` imports the ACER-003 closed validator
  and proves the complete six-pair eligible corpus as exactly six complete
  pairs/twelve records. Fifteen focused methods plus the exact thirty-two-case self-test
  cover partial/skipped/reordered batches, explicit first through fifth prior-prefix
  drift, source residue, payload drift, the exact six-parent rollback chain,
  index drift, current direct archive links, duplicate originals, rogue archive
  additions, unsafe paths, hostile Git steering, and forbidden self-referential
  batch commits. The production result is 43 aggregate archive records, 362
  historical links, twelve secret-clean new payloads, six repaired consumers in
  batch 6, and fifteen unique repaired current-or-migrated-original consumers
  across all batches.

- `tests/test_active_corpus_role_audit.py` imports the ACER-004 validator and
  treats `tests/**` as repository-static validation support, never a second
  Stage 04 execution tracker. Its production check derives tracked plus
  proposed nonignored inventories without `HEAD`; tracked inputs are recovered
  from exact index OIDs and must equal descriptor-bound `O_NOFOLLOW` worktree
  bytes, while untracked proposals use the descriptor reader directly. The
  focused tests prove validator/aggregate self-attestation, staged/worktree
  divergence rejection, path-replacement binding, symlink/FIFO rejection, and
  actual README frontmatter/Task/status-table tracker rejection. Exact
  production-path Git fixtures additionally prove a non-README tracked helper
  drift and an unsafe untracked helper proposal fail through `build_observed`.
  Every helper crosses the read boundary, while semantic scans exclude
  intentional JSON fixture and Python assertion strings. The isolated
  self-test and focused negatives also reject missing, extra, duplicate,
  unsafe, unordered, malformed, synthetic-event, copied-prompt,
  stale-live-claim, and unowned-finding states. Empty Incident and Postmortem
  collections remain valid until a real event exists, and no runtime or
  live-readiness result is inferred.

- `tests/test_workspace_boundary.py` passes synthetic NUL-delimited index bytes
  through the production parser and creates only isolated temporary Git
  repositories for tracked, force-added, missing, and symlink states. It pins
  four exact actual-repository Git index/object argv tuples and three isolated
  init/ignore tuples under a closed `shell=False` runner. Full SHA-1/SHA-256
  IDs, size and exact-blob bounds, malformed, conflict, nonregular, mode,
  ignore, startup, and timeout failures are covered. Two hostile cases create
  an ignored `_workspace/.gitignore`: one cannot hide a wrong root policy and
  one cannot override a correct root policy. Actual-root traversal/open/stat
  sentinels permit the temporary context but reject the real `_workspace` tree
  and worktree root `.gitignore`. Neither the test nor validator uses actual-
  worktree `check-ignore`; only the staged root ignore blob is authoritative.

- `tests/fixtures/gitops-change-set/` base/head resource graphs contain one added
  Service, one deleted Service, and the same ConfigMap identity at a moved path.
  The self-test must emit exactly those three sorted identity rows, represent the
  path-only move as one `RETAIN`, and exclude `DO_NOT_EMIT_SENTINEL`, `data:`,
  `spec:`, and `stringData:`. Paths are evidence only; manifest body keys and
  values are not output or equality inputs.
- `tests/fixtures/vault-eso-contracts.json` contains exactly ten named
  non-secret cases. The self-test deep-copies the valid local contract,
  applies one mutation at a time, and compares fixed diagnostics from the four
  production validators; it does not contact Vault/ESO or read a credential,
  secret value, ignored certificate, runtime setting, or history.
- `tests/fixtures/github-actions-security.json`은 정확히 11개 primary case로 remote SHA,
  same-line version comment, local Action, Docker digest, workflow default,
  exact job-write allowlist, `write-all`, `unpinned-uses` suppression을 동일한
  production 함수에 통과시킨다. 별도의 정확히 10개 repository boundary
  case는 missing/empty root와 directory, root/directory/file symlink,
  non-regular workflow, zizmor symlink를 내용 읽기 전에 거부한다. 정확히
  21개 required-write case는 세 workflow/job 각각에 exact/extra-read positive와
  missing-job/missing-permissions/all-read/missing-write/extra-write mutation을
  적용한다. JSON cardinality를 바꾸지 않는 5개 internal case는 quoted-local
  positive와 numeric/null/mapping/list `uses` mutation을 production parser/source
  parity 경로에 통과시켜 비문자열 occurrence가 양쪽에서 함께 사라지지 않게
  한다. PSH-002에서 fixture는 PASS하지만 repository
  mode는 현재 14개 mutable reference, 3개 missing default, 1개 suppression의
  정확히 18개 finding으로 의도적으로 FAIL한다. 이 RED는 PSH-003 입력이며
  아직 aggregate repository quality gate나 remote/runtime readiness 증거가 아니다.

- `tests/fixtures/document-contracts/registry-cases.json`의 각 사례는 하나의
  mutation과 정확한 기대 rule ID 목록을 담는다. 이 fixture는 비밀값을
  포함하지 않으며 registry/config self-test의 repo-static 입력으로만
  사용한다.
- `tests/fixtures/document-contracts/readme-profile-cases.json` schema v3는
  현재 `activePaths` 51개와 `retiredPaths` 23개를 분리해 보존한다. Active
  baseline 45개와 retired baseline 22개가 immutable baseline 67개를
  재구성하며, program-created handoff는 active 6개와 retired 1개다.
  ADM-006의 20행은 provider-correct snapshot destination과 uncovered route를
  유지하고, WERPC-008의 3행은 삭제된 predecessor README 경로와 새 pack
  README 목적지 및 snapshot route를 보존한다. 여덟 parser 사례는 active
  경로만 참조한다.
- `tests/fixtures/document-contracts/template-compatibility.json`은 Spec 033
  소유의 finite no-growth retirement guard다. Schema v2는
  `compatibilityDebt`와 `semanticDebtCaps`가 퇴역 필드로 계속 부재함을
  고정하고, registry-derived canonical form 수가 Markdown 27개와 native
  3개임을 검증한다. 이 파일은 debt admission이나 `DEFER` 목록을 소유하지
  않는다.
- `tests/fixtures/markdown-profiles.json`은 registry의 정확한 64개 행을
  `validate-document` 55개, `classification-only` 7개,
  `append-fragment` 1개, `excluded` 1개로 구분한다. Fixed `2026-07-12`
  기준일, leap-day,
  template placeholder, append context, stable rule-ID mutation은 모두 production
  entry point를 통과한다.
- `tests/fixtures/document-contracts/native-surface-cases.json`은 GitHub issue
  form, workflow, OpenAPI, GraphQL, protobuf의 정확한 5개 family와 positive
  5개/leading SDLC five-key negative 5개를 별도의 `10/10` 경계로 검증한다.
  이 수는 64-row profile applicability에 더하지 않으며, native syntax
  toolchain coverage나 하나의 합산 case total로 보고하지 않는다.
- `tests/fixtures/links-and-owners.json`은 synthetic Stage 00 current-authority
  declaration과 exact README mirror의 reciprocal lifecycle cases를 소유하며,
  production 32-path set을 복제하지 않는다. 같은 79-case schema v2 fixture는
  Current
  research/audit pointer, member lifecycle, accepted/active/done 상태, 누락·교체·순서·
  fenced lookalike와 Git-derived collection tree/table add/remove/equal-count swap,
  nested research pack, machine JSON, escaped-pipe status-prose 무관성, GFM body
  short-row padding/extra-cell truncation과 HTML comment 안에 숨은 tree의 거부도
  검증한다. 또한 fence 및 HTML comment 밖의 inline/reference
  link, URL decode 경계, 선언된 세 stage index, owner-key 정규화·제외·중복, exact
  fourteen-column ledger를 production component로 검증한다. Semantic debt fixture는
  ADM-002가 ledger와 468-path self-row를 같은 commit에서 만들 때 제거하는 exact
  `LEDGER-MISSING` 한 건만 허용하며 alias, glob, growth, duplicate, unknown rule을
  configuration error로 거부한다. Program-lineage 실행 사례는 registry relation
  Spec에 연결되지 않은 active Plan/Task component를 fail-closed로 거부하며,
  relation에 연결된 component의 dependency-ready·reciprocal·direct-Spec 규칙과
  함께 검증한다.
- `tests/fixtures/agent-roster-currentness.json`은 이름이 정확히 `valid`,
  `missing-role`, `surface-mismatch`, `stale-count`, `bad-owner`,
  `missing-current-phrase`인 사례 6개만
  허용한다. 각 이름의 mutation과 `expected_errors` 집합은 hardcoded
  per-case schema로 고정되며 self-test는 mutation 실행 전에 fixture
  semantics가 schema와 일치하는지 확인한다. 그 뒤 각 mutation을 확장하고
  repository 검증과 동일한 production `validate_contract()`를 호출해 실제
  오류 집합과 `expected_errors` 집합을 정확히 비교한다.
- `stale-count`는 `8 local agents`, `Eight local role adapters`, `eight
  shared roles`, `8 role stems`의 고정된 네 variant를 각각 독립적으로
  거부한다. `bad-owner`는 canonical bootstrap label을 유지한 채 target만
  `rules/persona.md`로 바꿔 exact Markdown label/target 검사를 입증한다.
  Canonical owner link에는 일반 inline link만 인정되며 image syntax와
  leading-only 또는 trailing-only half-backtick label은 동일한 label/target을
  담아도 canonical link로 인정되지 않는다.
  `missing-current-phrase`와 duplicate probe는 canonical roster phrase가 정확히
  한 번이어야 한다는 cardinality 계약을 고정한다.
- `tests/fixtures/agent-harness-contract.json`은 정확한 21개 mutation과 기대
  `HARNESS-*` rule을 고정한다. `tests/test_validate_agent_harness_contract.py`는
  current/target projection 분리, four-class evidence와 memory authority,
  exact 14-consumer/version, duplicate-key·schema·sensitive payload·symlink 및
  orphan projection 경계를 production 함수에 통과시킨다. 이 두 helper
  identity만 post-closure manifest에 허용되며 같은 확장자의 copy/sibling
  경로는 `ROLE-AUDIT-HELPER-ADMISSION`으로 실패한다.
- `tests/fixtures/agent-roster-admission.json`은 59개 closed mutation의
  `AREA-ADM-*` 기대 rule과 current `12/4/48`, achieved target mirror
  `12/4/48`, 두 repo-static projected role record, 일곱 final-admission condition,
  네 evaluation/memory class, 아홉 deferred evidence class, 여덟 surface
  plan을 고정한다.
  `tests/test_validate_agent_roster_admission.py`는 조기 `PASS`, 누락 rollback,
  unsafe path/symlink, secret-like durable memory, harness projection drift를
  production 함수와 동일한 경계에서 거부한다.
- `tests/fixtures/agent-evaluations.json`은 exact 60개 closed mutation과
  canonical harness에 결합된 열두 role × 네 fixture class의 48개 역할별
  실행형 synthetic scenario, stable identity/digest, 12 adjudication-readiness
  record, 2 rollback record, 아홉 high-risk independent review, 네 promotion
  blocker, same-suite/grader 및 synthetic/redacted privacy 계약을 고정한다.
  두 rollback record는 governed `agent-roster-admission.json`의 exact candidate
  reference, 원본 rollback 객체와 deterministic source digest에 결합된다.
  `tests/test_validate_agent_evaluations.py`는 generic placeholder residue와
  역할별 path/tool/prohibited-action/handoff 경계 drift, quality/safety 전에
  cost/latency를 판정하는 상태, runtime/provider/auth/live/evaluation/admission/
  model 권한을 조기 승격하는 상태를 거부한다. 또한 repository root와
  contract/schema/fixture/harness/roster-admission 입력과 raw repository
  root의 symlink, non-regular node, 중간 경로 symlink, `..` 탈출을 읽기
  전에 `AREA-EVAL-INPUT`으로 비노출 차단한다.
- `tests/fixtures/agent-governance-ci.json`은 selected/result 조합의 exact
  six-row truth table과 45개 closed mutation을 고정한다.
  `tests/test_validate_agent_governance_ci.py`의 32 focused tests는 adjacent
  schema, unknown key/version, result/evidence vocabulary, selector/job/summary,
  twelve route classes, eighteen delegated checks including the closure
  self-test/production pair, provider-evidence aggregate
  단일 CI owner와 exact path/source SHA-256/two-focused-validator manifest,
  canonical evidence vocabulary, aggregate/pre-commit/CI order,
  canonical local-QA owner/sequence/runner/inventory,
  full-SHA와 least-permission 경계, duplicate JSON/YAML, symlink/non-regular
  input, workflow-level inherited provider/secret env, agent validation 및
  summary job/step `continue-on-error`, validation step skip, step/workflow/job
  custom/default shell, dependency-install/gate/delegated command 밖의 extra
  run line, exact summary job/verdict-step/env shape, summary permissions,
  summary provider/secret env, pinned full-script SHA-256 drift,
  secret/provider-canary read, hosted-result preclaim, 그리고
  Spec046 `DEFER` ownership drift를 production 함수에서
  fail closed로 거부한다.
- `tests/fixtures/agent-model-fitness.json`은 33개 closed mutation과
  열두 role × 네 provider의 48 tuple, AREA-003 same-suite/corpus/
  adjudicator/rollback binding, configured incumbent, risk rationale,
  fail-closed fallback, exact quality/safety/cost/latency threshold object,
  authoritative cutoff를 고정한다.
  `tests/test_validate_agent_model_fitness.py`의 28 focused tests는
  `2026-07-10 10:00 Asia/Seoul` provider/model authority와 harness의
  repository-observation provenance를 분리하고, checked Spec 042 validator의
  exact source ID set·`publishedAtUtc` cutoff-day UTC semantics와 source
  ownership·classification·confidence·date basis에서 파생한 mapping readiness를
  임의 승격하거나 observed fitness·threshold·promotion·canary·runtime
  `PASS`로 전이하는 조기 승격을 거부한다. Model contract/schema/fixture,
  provider-evidence와 checked validator/schema, checked AREA-003
  validator/schema/evaluation/admission,
  harness 및 48 adapter 입력은 root·중간·최종 symlink, non-regular node,
  containment 탈출, unknown/cross-provider source-ID, stale scenario/input/
  fixture/global digest와 semantic rollback/suite drift를 `AREA-FIT-*`
  규칙으로 비노출 차단한다.
- `tests/fixtures/agent-provider-runtime-evidence.json`은 provider config와
  config에는 정확한 13개, canary에는 정확한 8개 mutation과 기대
  `PNME-*` rule을 고정한다.
  `tests/test_validate_agent_provider_config.py`와
  `tests/test_validate_agent_provider_canaries.py`는 closed schema, fixed
  cutoff, separate prior/current observations, current Gemini repo-static
  projection with absent native discovery, candidate
  model gates, MCP bounds, twelve redacted evidence-lane records, and
  no-cross-lane promotion을 production 함수에 통과시킨다.
- `tests/fixtures/agent-harness-semantics.json`은 정확히 12개 role, local/Claude/
  Codex/Gemini 4개 adapter surface, responsibility/output/prohibition/stop/handoff/capability-
  tier/evidence/adapter-stem 8개 category, remove/replace 2개 mutation의
  768-case Cartesian matrix를 고정한다. 모든 case는 production parser와
  validator를 사용하고 하나의 서로 다른 `ROLE-*` rule ID만 반환해야 한다.
  Mutation은 파싱된 객체가 아니라 adapter source에 적용되어 768개 모두
  YAML/TOML/operative-Markdown parser를 다시 통과한다. 추가 33개 adversarial
  case는 duplicate/non-mapping/non-scalar YAML, fenced/absolute-or-list-
  container-indented code, HTML comment, strikethrough, blockquote/nested/lazy
  continuation, forward/backward revocation, external negation, inline-code-
  only claim, quoted/nested H1 우회를 거부한다. Category claim은 소유 section의
  paragraph/list-item unit 전체와 정확히 같아야 한다. `false`, `not true`,
  `invalid`, revoked 계열과 non-operative/non-applicable 상태는 단일 10-state
  vocabulary와 forward/backward 20개 production-parser probe로 동기화한다.
  공통 계약은 surface-owned `model`, `tools`, `modelReasoningEffort`를
  schema로 거부하며, operative prose에서만 whitespace를 정규화한다.
- `tests/fixtures/validation-surfaces.json`은 13개 selection case를 포함해 요청된 tracked root별 positive
  path, validator/CI selection 집합, `../`, leading `./`, case alias, symlink
  traversal, unmatched path rejection과 route, minimal/combined/assignment
  shell/Python/Node interpreter-eval argv, wrapper trampoline, executable path
  prefixes/case alias, option-before-script,
  lane, job, protection, validator/surface fallback, evidence mutation을 production
  selector에 통과시킨다. Bash/Python/Node의 script operand 뒤 `-c`/`-e`는
  positive case로 유지하고 `bash -- scripts/validate-harness.sh -c` 경계도 통과시켜
  script argument를 interpreter option으로 오인하지 않는 것을 검증한다.
  Selector self-test는 JSON과
  GitHub output ordering, NUL termination, newline-containing record의 단일-record
  보존도 검증하며 shell parsing이나 first-match precedence를 사용하지 않는다.
  Schema v3의 다섯 CI range case와 임시 Git rename proof는
  `--no-renames`가 보호 경로 rename의 old/new 양끝을 모두 전달하는지
  검증한다. `contract-bulk-document-escalation`은 document profile contract,
  migration ledger, archived Spec을 함께 선택할 때 네 document validator와
  `pre-commit`/`repo-quality-static` job이 protected 수준으로 유지되는 것을
  고정한다. Contract schema v2의 exact document-validator path input은
  valid existing/invalid untracked Markdown PostToolUse probe로 함께 고정한다.
  Hook-consumer selection cases additionally pin `_workspace/README.md`,
  `.gitignore`, `policy/conftest/kubernetes.rego`,
  `.agents/agents/network-reviewer.md`, and the empty path set. Shared hooks
  write temporary `.nul` files only after fail-closed payload validation.
  C0/DEL bytes (including NUL, newline, and tab), boundary whitespace,
  non-normalized or external paths, and any symlink component are rejected
  before formatter or pre-commit invocation; records are never reconstructed
  through newline iteration. Present `file_path`/`path` aliases are type-checked
  before alias-count rejection, so `null` cannot shadow a later valid value;
  `files`/`paths` permit only one string-list alias, with `files: []` retaining
  explicit no-files semantics. Empty objects, nulls, and mixed list items fail.
- Roster fixture와 repository 검사는 repo-static evidence만 제공한다. Claude,
  Codex, local/Antigravity adapter runtime을 실행하지 않으며, absent인 Gemini
  CLI native surface를 포함한 어떤 runtime readiness도 입증할 수 없다.
- Repo-static 검증 통과는 live k3d 운영 검증 완료를 의미하지 않는다.
- Optional tool 검증은 `kube-linter`나 `conftest`가 설치되어 실제 실행됐을 때만 해당 도구 coverage로 보고한다. 미설치 `SKIP`은 fallback 또는 syntax 검증 통과로 따로 기록한다.
- Live/operator-owned 검증은 사람 승인 bootstrap 또는 break-glass 맥락에서만 실행하고, repo-static evidence와 섞어 보고하지 않는다.
- `tests/`는 application coverage target의 canonical owner가 아니다. 신규
  testable application/source code는 해당 application test surface에서 90%
  coverage target을 검토하고, Bash/YAML/Markdown infrastructure 변경은
  validation-matrix evidence로 검증한다.
- `pre-commit`, `kube-linter`, `actionlint`, `zizmor`, `graphify`, `rtk` 같은 optional local tools가 없으면 통과로 간주하지 않고 제한사항으로 보고한다.
- 외부 Vault, 실제 Kubernetes API, ArgoCD reconciliation 상태는 승인된 live check가 없으면 검증 범위 밖이다.

### Link Basis

이 README의 링크 기준 위치는 `tests/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [Repository README](../README.md)
- [scripts README](../scripts/README.md)
- [infrastructure README](../infrastructure/README.md)
- [Agentic execution rules](../docs/00.agent-governance/rules/agentic.md)
- [Local harness catalog](../docs/00.agent-governance/harness-catalog.md)
