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
tests/fixtures/agent-governance-ci.json
tests/fixtures/agent-loop-lifecycle.json
tests/fixtures/agent-provider-runtime-evidence.json
tests/fixtures/document-contracts/native-surface-cases.json
tests/fixtures/document-contracts/readme-profile-cases.json
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
tests/fixtures/markdown-profiles.json
tests/fixtures/validation-surfaces.json
tests/fixtures/vault-eso-contracts.json
tests/test_affected_surface_migration.py
tests/test_archive_cutover.py
tests/test_archive_historical_proof.py
tests/test_archive_recovery.py
tests/test_archive_validation.py
tests/test_current_executable_references.py
tests/test_document_lifecycle_agent_roster_cutover.py
tests/test_document_lifecycle_archive_cutover.py
tests/test_document_lifecycle_migration.py
tests/test_document_strict_cutover.py
tests/test_generic_migration_recovery.py
tests/test_k8s_pre_edit_hook.py
tests/test_migrate_document_work_units.py
tests/test_post_validate_runner_result.py
tests/test_provider_post_validate_hook.py
tests/test_run_validation_lane.py
tests/test_validate_agent_checkpoint.py
tests/test_validate_agent_compatibility_clis.py
tests/test_validate_agent_core_cutover.py
tests/test_validate_agent_governance_ci.py
tests/test_validate_agent_governance_closure.py
tests/test_validate_agent_harness_contract.py
tests/test_validate_agent_harness_semantics.py
tests/test_validate_agent_legacy_cutover.py
tests/test_validate_agent_loop_lifecycle.py
tests/test_validate_agent_provider_canaries.py
tests/test_validate_agent_provider_config.py
tests/test_validate_agent_registry.py
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
[Agent Quality Standards](../docs/00.agent-governance/policies/quality.md):
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
| Generic migration and offline schema regression | `python3 -m unittest tests.test_generic_migration_recovery tests.test_validate_agent_core_cutover` | Disposable real Git/public recovery proof, per-edge and cross-record composition, canonical Stage99 form, FIFO rejection, typed action errors and shared offline schema evaluation. Transport mocks prohibit HTTP/URL/socket/DNS/file-resource retrieval; embedded references remain supported. No production index or lifecycle approval. |
| Retired validation-surface selection | `python3 -m unittest tests.test_affected_surface_migration` | Current classification stays authoritative. Only absent unmatched inputs use complete Git-backed migration proof and current terminal routing; composition, deletion, index/source drift, unsafe or recreated sources, pure owner calls, and isolated loader cleanup are covered. No retired provider route, production-index waiver, or runtime evidence. |
| Archive recovery/envelope fixture | `python3 -m unittest tests/test_archive_recovery.py` | Repo-static private-fixture evidence for SHA-1/SHA-256 Git identity, literal canonical paths, deterministic bounded Git execution, stable non-disclosing errors and representations, raw blob bytes, UTF-8 admission, duplicate-key rejection, byte-identical canonical frontmatter, typed archive-time replacement evidence, archive-to-archive rejection, metadata dependency, marker/payload-to-EOF grammar, final-newline preservation, collision safety, and worktree-byte substitution rejection; not production archive authority or corpus evidence |
| Archive validation fixture | `python3 -m unittest tests/test_archive_validation.py` | Repo-static import-only evidence for metadata order/type, Git blob and digest identity, payload mutation, mirrored path, source-tree-only historical links, current-tree confusion rejection, inventory-independent archive reactivation, active direct individual-archive links, duplicate `original_path` authority, archive immutability, finite current status/profile and exact public input contracts, private verified canonical CommonMark loading/return-shape checks, and payload-free diagnostics; not production archive authority or 31/202 corpus evidence |
| Archive cutover regression | `python3 -m unittest tests/test_archive_cutover.py` | Production worktree snapshot evidence that the cutover is atomic and emits named `ARCHIVE-CUTOVER-INCOMPLETE` diagnostics for any partial state; the GREEN snapshot preserves the immutable 31-record/202-link base proof and derives the ledger-backed 43-record/362-link/43-secret-clean aggregate, registry v8/template authority, manifest closure, and index-only replacement evolution. Real temporary-Git mismatches prove a staged draft or invalid UTF-8 blob is rejected even when the worktree copy is current, while a stage-zero regular current blob remains authoritative without a worktree copy; sanitized bounded blob errors fail closed without displaying payload or secret matches. |
| Archive and agent-registry lifecycle regression | `python3 -m unittest tests/test_document_lifecycle_archive_cutover.py`; `python3 -m unittest tests/test_document_lifecycle_agent_roster_cutover.py`; `python3 scripts/validate-document-lifecycle.py --root . --mode staged` | Archive-focused tests preserve sealed migration and immutable recovery rules. The agent-registry regression verifies that current neutral and Claude Markdown projections route through terminal document profiles, the provider set is exactly Codex and Claude, and the retired Spec 044 mutable-base/four-surface admission gate is no longer lifecycle authority. |
| Workspace boundary regression | `python3 -m unittest tests/test_workspace_boundary.py`; `python3 scripts/validate-workspace-boundary.py --self-test`; `python3 scripts/validate-workspace-boundary.py --root .` | Sixteen focused methods plus the isolated self-test prove exact stage-zero `100644` README and root-ignore cardinality; full SHA-1/SHA-256 root-ignore OIDs; bounded immutable blob retrieval; extra/force-added, symlink/gitlink/nonregular/conflict, malformed-index, startup, and timeout rejection; and stable path-only diagnostics. Two hostile ignored-child policies and one divergent worktree-root policy prove only the staged root blob controls probe ignored/README unignored results. Four actual-repository index/object queries precede three isolated-context init/ignore queries; no actual-worktree `check-ignore` runs. Actual-path traversal/open/stat sentinels allow only isolated policy evaluation. |
| Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | Repo-static |
| Document strict cutover regression | `python3 tests/test_document_strict_cutover.py` | Strict-only validator contracts, terminal Stage 99 authority, Stage 05 owner/identity boundaries, retired-stage link absence, and current Incident/Postmortem template alignment. |
| Markdown profile repository check | `python3 scripts/validate-markdown-profiles.py --root .`; `python3 scripts/validate-markdown-profiles.py --root . --mode strict` | Repo-static strict-only evidence; omitting the mode is equivalent to explicit strict |
| Cross-document repository check | `python3 scripts/validate-links-and-owners.py --root .`; `python3 scripts/validate-links-and-owners.py --root . --mode strict` | Repo-static strict-only evidence; the retired compatibility value is an argparse exit `2` boundary |
| Cross-document inventory | `python3 scripts/validate-links-and-owners.py --root . --inventory --format json` | Repo-static ordered registry population |
| Agent registry regression | `python3 -m unittest tests.test_validate_agent_registry tests.test_validate_agent_harness_contract` | Closed providers, roles, permissions, references, projections, and safe-input mutations. |
| Agent registry repository check | `python3 scripts/validate-agent-harness-contract.py --root .` | Registry-derived repository-static integrity; no prose census or provider-runtime claim. |
| Agent compatibility CLI | `python3 -m unittest tests.test_validate_agent_compatibility_clis` | Transitional CLI delegates to `.agents/registry.json`; no separate snapshot or runtime fitness authority. |
| Agent-governance CI fixture | `python3 scripts/validate-agent-governance-ci.py --root . --self-test`; `python3 -m unittest tests/test_validate_agent_governance_ci.py` | Exact `truth_cases=6 mutation_cases=45` inventory and thirty-two focused artifact, schema, semantic, path/symlink/non-regular, duplicate-key, topology, inherited-secret, skipped-step, custom/default-shell, exact-run-sequence, exact-summary-shape/digest, job/step fail-open, security, closure routing/order, explicit-root aggregate invocation, canonical evidence vocabulary, provider-evidence aggregate ownership/removal/source-digest boundary, local-QA order/inventory, and evidence-boundary regressions |
| Agent-governance CI repository check | `python3 scripts/validate-agent-governance-ci.py --root .` | Repo-static `route_classes=12 delegated_checks=18 truth_rows=6 deferred_owners=1 qa_surfaces=10`; PASS includes the closure self-test/production pair and sole repository-static checkpoint self-test delegation alongside harness-semantics and legacy-cutover delegation, proves only the closed selector/job/summary/route/delegation/security/local-QA contract, and leaves the Spec046 hosted CI, branch protection, provider runtime/auth/model discovery, provider resume/handoff canary, remote, and live evidence `DEFER` |
| Agent-governance closure regression | `python3 scripts/validate-agent-governance-closure.py --root . --self-test`; `python3 -m unittest tests.test_validate_agent_governance_closure` | Thin registry delegation, public CLI modes, typed runtime-claim rejection, and fixed unexpected-failure redaction. No duplicate closure fixture, snapshot census, or generic QA-evidence record. |
| Agent-governance closure repository check | `python3 scripts/validate-agent-governance-closure.py --root .` | Repository-static neutral registry validation through the retained compatibility CLI; no provider/runtime/hosted-CI/live claim. |
| Agent loop lifecycle regression | `python3 -m unittest tests.test_validate_agent_loop_lifecycle`; `python3 scripts/validate-agent-loop-lifecycle.py --self-test`; `python3 scripts/validate-agent-loop-lifecycle.py --root .` | Focused contract, destination-ID/order/owner-reference, review, and raw-promotion mutations prove the four memory classes, atomic/redacted synthetic checkpoint boundary, repository-wins resume, promotion/refresh/expiry/archive-GC/conflict, compaction, handoff, and five bounded reviewed feedback destinations. PASS does not read or write ignored checkpoints or establish provider/runtime/CI/remote/live/actual checkpoint execution. |
| Agent checkpoint lifecycle regression | `python3 scripts/validate-agent-checkpoint.py --root . --self-test` | Closed checkpoint mutations validate atomic/redacted synthetic checkpoint shape, repository-wins resume, promotion/refresh/expiry/archive-GC/conflict, compaction, and handoff. Its repo-static PASS is not provider discovery, hook delivery, permission, model, authenticated, hosted-CI, remote, credential-bearing, live, or actual checkpoint-execution evidence. |
| Provider evidence regression | `python3 -m unittest tests.test_validate_agent_provider_config tests.test_validate_agent_provider_canaries` | Safe-input, native config, redaction, and non-transitive Codex/Claude evidence. Current root gateways must retain their owner/provider pointers and thin-router boundary; missing gateways and embedded roster policy fail closed. |
| Provider evidence repository check | `python3 scripts/validate-agent-provider-config.py --root .`; `python3 scripts/validate-agent-provider-canaries.py --root .`; composed route: `python3 scripts/validate-agent-provider-evidence.py --root .` | Registry-derived Codex/Claude configuration and canary contract evidence only; executable presence or absence never proves authenticated provider runtime, model resolution, CI, remote, or live readiness |
| Agent semantics regression | `python3 -m unittest tests.test_validate_agent_harness_semantics` | Focused operative-prose and projection mutations; no production self-test matrix. |
| Agent semantics repository check | `python3 scripts/validate-agent-harness-semantics.py --root .` | Neutral/Claude/Codex semantic and permission parity, not native runtime consumption. |
| Agent legacy cutover regression | `python3 scripts/validate-agent-legacy-cutover.py --root . --self-test`; `python3 -m unittest tests.test_validate_agent_legacy_cutover tests.test_archive_historical_proof` | Minimal fixtures exercise current plain/rendered instructions, exact historical bytes plus terminal disposition, typed path-only migration declarations, native/document precedence, validated helper/argv ownership, retention snapshot mutation, unknown text, retired-path absence, regular successors, root-dirfd swaps, closed Git execution, limits, and redacted diagnostics. Public recovery tests use temporary real Git; omitted unrelated owner contexts are explicit. |
| Agent legacy cutover repository check | `python3 scripts/validate-agent-legacy-cutover.py --root .` | Git-index-only candidate validation with current canonical owners. Ignored and other untracked content is not read. Full source recovery requires synchronized reviewed index/worktree bytes; stale-index failures are not waived. No fixed whole-corpus counts, progress-prefix exemption, arbitrary-code dependency-analysis claim, or provider/runtime/CI/live promotion. |
| Agent roster currentness fixture | `python3 scripts/validate-agent-roster-currentness.py . --self-test` | Repo-static |
| Agent roster currentness repository check | `python3 scripts/validate-agent-roster-currentness.py .` | Repo-static |
| Affected-surface fixture | `python3 scripts/validate-affected-surfaces.py --root . --self-test` | Repo-static `surfaces=22 mutation_cases=38` duplicate-JSON, exact-route, argv, output, NUL-transport, existing-node and exact shared-symlink-target boundaries, plus focused agent-harness/loop/checkpoint, Spec 044 admission/evaluation/model-fitness, Spec 045 agent-governance CI selection, and Spec 046 closure-validator selection evidence across the required agent/governance/script/test surfaces |
| Affected-surface repository coverage | `python3 scripts/validate-affected-surfaces.py --root .` | Repo-static tracked-path coverage; no ignored scratch traversal |
| Current executable-reference regression | `python3 -m unittest tests.test_current_executable_references` | Registry-derived executable suffixes and arbitrary depth; current tracked-regular enforcement; Stage 03 proposal isolation; Git-first terminal/Stage 90 recovery; Stage 98 delegation to the Archive owner. Repository-static only. |
| Affected/staged/all-files local runner | `python3 scripts/run-validation-lane.py --root . --lane affected\|staged\|all-files --paths-file <file.nul> --delimiter nul`; `python3 -m unittest tests/test_run_validation_lane.py tests/test_post_validate_runner_result.py tests/test_provider_post_validate_hook.py` | Repo-static shell-free execution of contract-selected argv under a closed startup environment and fixed absolute tool search path. Twenty-two production-isolation, staged-lane selection, marker-cardinality, hostile PATH/BASH_ENV/PYTHONPATH/Gitleaks-hint, exact secure passwd-home executable, unsafe candidate, effective owner/group/other execute and full directory traversal, root semantics, pure selector/runner, hook-log, and actual provider-entry regressions prove caller state cannot forge success. The staged runner uses the exact staged path set but remains separate from plain `pre-commit run` against the Git index; the all-files runner does not replace `pre-commit run --all-files`. The secure executable hint never broadens PATH. Claude native hook commands execute the production hook in a bounded fixture: valid manifest/docs payloads preserve all 7/4 validators and existing Markdown path arguments, while malformed JSON fails closed. |
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
contract in `docs/00.agent-governance/policies/quality.md`; static
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

  treats `tests/**` as repository-static validation support, never a second
  Stage 04 execution tracker. Its production check derives tracked plus
  proposed nonignored inventories without `HEAD`; tracked inputs are recovered
  from exact index OIDs and must equal descriptor-bound `O_NOFOLLOW` worktree
  bytes, while untracked proposals use the descriptor reader directly. The
  sealed helper membership remains historical: only a complete generic
  Migration proof can close an absent member through its recovered source and
  non-self successor. The outer audit obtains that proof once when needed;
  artifact-role classification remains pure. Temporary Git tests exercise
  source identity, per-path disposition, chained successors, duplicates,
  source reappearance and successor regularity without restoring retired
  fixtures or adding replacement authorities to the current helper inventory.
  This proof checks its own reviewed index/worktree boundary, even when a
  caller disables the role audit's ordinary index comparison. The
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

- `tests/fixtures/document-contracts/readme-profile-cases.json` schema v3는
  현재 production README inventory와 Stage 04 retirement handoff를
  정렬·중복 없이 보존한다. 고정 개수나 과거 branch census를 재구성하지
  않으며, 각 active 경로가 registry-selected profile과 일치하는지 검증한다.
- `tests/fixtures/document-contracts/template-compatibility.json`은 Spec 033
  소유의 finite no-growth retirement guard다. Schema v2는
  `compatibilityDebt`와 `semanticDebtCaps`가 퇴역 필드로 계속 부재함을
  고정하고, registry-derived canonical form 수가 Markdown 27개와 native
  3개임을 검증한다. 이 파일은 debt admission이나 `DEFER` 목록을 소유하지
  않는다.
- `tests/fixtures/markdown-profiles.json`은 registry profile별 applicability와
  positive/negative mutation을 구분한다. Fixed `2026-07-12` 기준일,
  leap-day, template placeholder, append context, stable rule-ID mutation은
  모두 production entry point를 통과한다. Fixture 총개수는 계약이 아니다.
- `tests/fixtures/document-contracts/native-surface-cases.json`은 GitHub issue
  form, workflow, OpenAPI, GraphQL, protobuf의 정확한 5개 family와 positive
  5개/leading SDLC five-key negative 5개를 별도의 `10/10` 경계로 검증한다.
  이 수는 64-row profile applicability에 더하지 않으며, native syntax
  toolchain coverage나 하나의 합산 case total로 보고하지 않는다.
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

- `tests/fixtures/agent-provider-runtime-evidence.json`과 focused provider
  tests는 Codex/Claude configuration, safe input, redacted canaries, 그리고
  evidence-lane 사이의 암묵적 승격 금지를 검증한다. 실행되지 않은 runtime
  결과를 성공으로 표시하지 않는다.
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
- Agent registry와 projection 검증은 repository-static evidence만 제공한다.
  Claude/Codex native discovery, authentication, enforcement, 실행은 별도 증거가 필요하다.
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
- [Agentic execution rules](../docs/00.agent-governance/policies/agent-execution.md)
- [Local harness catalog](../docs/00.agent-governance/roles/README.md)
