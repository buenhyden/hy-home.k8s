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
tests/
├── test_active_corpus_retention.py    # ACER-001 pinned census and hostile-boundary regression
├── test_active_corpus_eligibility.py  # ACER-002 pinned dry-run eligibility regression
├── test_archive_cutover.py            # ARWB-003 production snapshot atomic-cutover regression test
├── test_document_lifecycle_archive_cutover.py # Finite staged/CI archive lifecycle admission regression
├── test_post_validate_runner_result.py # Exact post-validate runner-log cardinality regression
├── test_provider_post_validate_hook.py # Closed provider entry and hostile payload integration regression
├── test_archive_recovery.py           # ARWB-001 isolated Git-object and ArchiveEnvelope.v1 fixture tests
├── test_archive_validation.py         # ARWB-002 isolated archive/history/current-authority validator tests
├── fixtures/
│   ├── agent-role-semantics.json     # Thirty-role-adapter semantic mutation matrix
│   ├── agent-roster-currentness.json # Canonical roster validator self-test cases
│   ├── github-actions-security.json  # Immutable Action and least-privilege cases
│   ├── markdown-profiles.json       # Registry profile matrix, mutations, and fixed date cases
│   ├── links-and-owners.json        # Link, stage/collection index, authority mirror, owner, and ledger cases
│   ├── validation-surfaces.json     # Affected path, selection, rejection, and contract mutation cases
│   ├── vault-eso-contracts.json     # Exact non-secret Vault/ESO mutation cases
│   └── document-contracts/
│       ├── native-surface-cases.json  # Five native families and exact SDLC-envelope negatives
│       ├── readme-profile-cases.json  # README route and semantic-validator handoff cases
│       ├── registry-cases.json        # Document registry contract cases
│       ├── semantic-compatibility-debt.json # Exact Spec 030 ledger transition debt
│       └── template-compatibility.json # Canonical template and migration-debt contract
└── README.md                         # This file
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

## Operations

### Working Procedure

1. 기본 검증 기준은 [scripts/README.md](../scripts/README.md)와 [infrastructure/README.md](../infrastructure/README.md)를 먼저 확인한다.
2. manifest나 GitOps 구조를 바꾸면 `scripts/`와 `infrastructure/tests/`의 정적 검증을 함께 실행한다.
3. 이 폴더에는 여러 하위 시스템을 동시에 검증하는 산출물이 있을 때만 새 파일을 추가한다.
4. live cluster evidence는 사람 승인 bootstrap 또는 break-glass 절차로만 기록하며, 로컬 정적 검증과 분리해서 보고한다.

### Validation Model

| Area | Command | Evidence class |
| --- | --- | --- |
| Archive recovery/envelope fixture | `python3 -m unittest tests/test_archive_recovery.py` | Repo-static private-fixture evidence for SHA-1/SHA-256 Git identity, literal canonical paths, deterministic bounded Git execution, stable non-disclosing errors and representations, raw blob bytes, UTF-8 admission, duplicate-key rejection, byte-identical canonical frontmatter, metadata dependency, marker/payload-to-EOF grammar, final-newline preservation, collision safety, and worktree-byte substitution rejection; not production archive authority or corpus evidence |
| Archive validation fixture | `python3 -m unittest tests/test_archive_validation.py` | Repo-static import-only evidence for metadata order/type, Git blob and digest identity, payload mutation, mirrored path, source-tree-only historical links, current-tree confusion rejection, inventory-independent archive reactivation, active direct individual-archive links, duplicate `original_path` authority, archive immutability, finite current status/profile and exact public input contracts, private verified canonical CommonMark loading/return-shape checks, and payload-free diagnostics; not production archive authority or 31/202 corpus evidence |
| Archive cutover regression | `python3 -m unittest tests/test_archive_cutover.py` | Production worktree snapshot evidence that the cutover is atomic and emits named `ARCHIVE-CUTOVER-INCOMPLETE` diagnostics for any partial state; the GREEN snapshot proves 31 records, 202 historical links, 31 secret-clean exact Git-blob payloads, registry v8/template authority, manifest closure, and current index-only routing without displaying payload or secret matches |
| Archive lifecycle cutover regression | `python3 -m unittest tests/test_document_lifecycle_archive_cutover.py`; `python3 scripts/validate-document-lifecycle.py --root . --self-test`; `python3 scripts/validate-document-lifecycle.py --root . --mode staged` | Fourteen focused methods and thirteen closed self-test fixtures admit only the exact base `f8a54dd` staged/CI v7-to-v8 transition containing the pinned base/proposed registry blobs, all 31 same-path archive profile conversions, and the retired/new template pair. The Git-object regression resolves both pinned commits through absolute `/usr/bin/git` with a closed deterministic environment, isolated configuration, replacement objects disabled twice, a timeout, and commit-type verification before path resolution; malformed, missing, and noncommit identities fail closed. Partial, extra, wrong-base, wrong-registry-OID, missing-pair, registry drift, unrelated-profile, snapshot, and explicit-ref projections remain fail-closed without payload or secret scanning. |
| Workspace boundary regression | `python3 -m unittest tests/test_workspace_boundary.py`; `python3 scripts/validate-workspace-boundary.py --self-test`; `python3 scripts/validate-workspace-boundary.py --root .` | Sixteen focused methods plus the isolated self-test prove exact stage-zero `100644` README and root-ignore cardinality; full SHA-1/SHA-256 root-ignore OIDs; bounded immutable blob retrieval; extra/force-added, symlink/gitlink/nonregular/conflict, malformed-index, startup, and timeout rejection; and stable path-only diagnostics. Two hostile ignored-child policies and one divergent worktree-root policy prove only the staged root blob controls probe ignored/README unignored results. Four actual-repository index/object queries precede three isolated-context init/ignore queries; no actual-worktree `check-ignore` runs. Actual-path traversal/open/stat sentinels allow only isolated policy evaluation. |
| Active corpus retention regression | `python3 -m unittest tests/test_active_corpus_retention.py`; `python3 scripts/validate-active-corpus-retention.py --root . --self-test`; `python3 scripts/validate-active-corpus-retention.py --root .` | Thirty-eight focused methods plus the 27-case closed self-test prove the exact 110-row immutable candidate census, six-row delta, pair cardinality, source blobs/statuses, ledger and non-authoritative Spec-link evidence, explicit unresolved eligibility axes, two retained active controls, 24-record Stage 05 input, the pinned 29-file helper input, exact one-test proposal delta, proposed 30-file helper counts, and four dated official-method sources. Missing/extra/duplicate rows, premature eligibility or lineage inference, unowned DEFER, synthetic events, helper tracker promotion, helper observation/delta/proposed-count drift, unsafe candidate/control/Stage 05/helper paths, non-string diagnostic payloads, parent-relative paths, schema/count/control/source drift, wrong commit/blob/tree object, hostile Git steering, and ignored-workspace access fail closed with single-line value-free diagnostics. |
| Active corpus eligibility regression | `python3 -m unittest tests/test_active_corpus_eligibility.py`; `python3 scripts/validate-active-corpus-eligibility.py --root . --self-test`; `python3 scripts/validate-active-corpus-eligibility.py --root .` | Focused contract checks plus closed self-tests prove the 110-row pinned join, 12 eligible rows across the exact six complete pairs, 98 owned `DEFER` rows, retained Spec 037 controls, canonical archive routing, rollback readiness without a claimed cutover, and value-free path rejection. |
| Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | Repo-static |
| Markdown profile self-test | `python3 scripts/validate-markdown-profiles.py --self-test` | Repo-static |
| Markdown profile compatibility | `python3 scripts/validate-markdown-profiles.py --root . --mode compatibility` | Repo-static finite-debt evidence |
| Cross-document self-test | `python3 scripts/validate-links-and-owners.py --self-test` | Repo-static link, stage/collection-index, Stage 00 and Current-pack lifecycle-mirror, owner, and ledger mutation evidence |
| Cross-document compatibility | `python3 scripts/validate-links-and-owners.py --root . --mode compatibility` | Repo-static exact ledger-transition debt evidence |
| Cross-document inventory | `python3 scripts/validate-links-and-owners.py --root . --inventory --format json` | Repo-static ordered registry population |
| Agent role semantics fixture | `python3 scripts/validate-agent-role-semantics.py --self-test` | Repo-static 480-case category mutation evidence |
| Agent role semantics repository check | `python3 scripts/validate-agent-role-semantics.py --root .` | Repo-static thirty-role-adapter semantic coverage across local/Claude/Codex surfaces |
| Agent roster currentness fixture | `python3 scripts/validate-agent-roster-currentness.py . --self-test` | Repo-static |
| Agent roster currentness repository check | `python3 scripts/validate-agent-roster-currentness.py .` | Repo-static |
| Affected-surface fixture | `python3 scripts/validate-affected-surfaces.py --self-test` | Repo-static exact-route, argv, output, and NUL-transport evidence |
| Affected-surface repository coverage | `python3 scripts/validate-affected-surfaces.py --root .` | Repo-static tracked-path coverage; no ignored scratch traversal |
| Affected/all-files local runner | `python3 scripts/run-validation-lane.py --root . --lane affected\|all-files --paths-file <file.nul> --delimiter nul`; `python3 -m unittest tests/test_run_validation_lane.py tests/test_post_validate_runner_result.py tests/test_provider_post_validate_hook.py` | Repo-static shell-free execution of contract-selected argv under a closed startup environment and fixed absolute tool search path. Fifteen production-isolation, marker-cardinality, hostile PATH/BASH_ENV/PYTHONPATH, pure selector/runner, hook-log, and actual provider-entry regressions prove caller state cannot forge success. Claude, Codex, and Gemini commands execute the production hook in a bounded fixture: valid manifest/docs payloads preserve all 7/4 validators and existing Markdown path arguments, while malformed JSON fails closed. |
| GitHub Actions security fixture | `python3 scripts/validate-github-actions-security.py --self-test` | Tier A required aggregate evidence preserving exactly eleven primary, ten repository-boundary, twenty-one required-write JSON cases, plus five internal uses-shape cases |
| GitHub Actions security repository check | `python3 scripts/validate-github-actions-security.py --root .` | Tier A required aggregate evidence; `PASS` enforces immutable Action identities and least-privilege permissions |
| GitOps identity change-set fixture | `python3 scripts/validate-gitops-change-set.py --self-test` | Repo-static exact one ADD, one DELETE, and one path-only RETAIN plus durable unsafe-ref/path, symlink/non-regular, cycle, duplicate, malformed-token, unsupported-dialect/directive, multi-document, root/two-commit, and shallow-parent rejection coverage; forbidden manifest values remain excluded |
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
Markdown-profile, cross-document, affected-surface, agent-role-semantic, and
roster-currentness validators in strict blocking mode, then runs only retained
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
  expanded cases cover the closed 31-record, 202-link, and 31-secret-clean
  GREEN; named RED output; complete structured manifest and external-table
  rejection; recovery-grade hostile Git isolation; stable root, registry,
  startup, and timeout diagnostics; stale retired role; direct current link;
  duplicate original owner; and missing replacement. Repeated partial
  projections stub only the already-proven secret-classifier call while still
  exercising production envelope/provenance/history logic. The validator
  suppresses classifier stdout/stderr, never includes payload bytes in report
  objects, and inventories tracked/untracked `docs` paths without traversing
  ignored `_workspace` children.

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
  현재 `activePaths` 52개와 ADM-006 `retiredPaths` 20개를 분리해 보존한다.
  active baseline 47개와 retired baseline 20개가 immutable baseline 67개를
  재구성하고, 나머지 active 5개는 program-created handoff다. Retired 행은
  historical profile/heading disposition과 `retiredBy`, provider-correct
  snapshot destination을 유지하되 현재 registry에서는 반드시 uncovered로
  남는다. 여덟 parser 사례는 active 경로만 참조한다.
- `tests/fixtures/document-contracts/template-compatibility.json`은 canonical form,
  template-mode inheritance, authored migration debt의 no-growth 기준을 고정한다.
  `affectedPaths`는 path/profile/rule/token을 정확히 결합하며 required
  89/247, residue 188/410, delimiter 24, unsupported 175/617/400 distinct
  tokens, duplicate 1, required-residue overlap 51, union 266을 초과하거나
  사용되지 않은 record을 남기면 실패한다.
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
  configuration error로 거부한다.
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
- `tests/fixtures/agent-role-semantics.json`은 정확히 10개 role, local/Claude/
  Codex 3개 adapter surface, responsibility/output/prohibition/stop/handoff/capability-
  tier/evidence/adapter-stem 8개 category, remove/replace 2개 mutation의
  480-case Cartesian matrix를 고정한다. 모든 case는 production parser와
  validator를 사용하고 하나의 서로 다른 `ROLE-*` rule ID만 반환해야 한다.
  Mutation은 파싱된 객체가 아니라 adapter source에 적용되어 480개 모두
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
- `tests/fixtures/validation-surfaces.json`은 요청된 tracked root별 positive
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
  검증한다. Contract schema v2의 exact document-validator path input은
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
