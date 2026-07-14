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
├── fixtures/
│   ├── agent-role-semantics.json     # Thirty-adapter semantic mutation matrix
│   ├── agent-roster-currentness.json # Canonical roster validator self-test cases
│   ├── github-actions-security.json  # Immutable Action and least-privilege cases
│   ├── markdown-profiles.json       # Registry profile matrix, mutations, and fixed date cases
│   ├── links-and-owners.json        # Cross-document link, index, owner, and ledger cases
│   ├── validation-surfaces.json     # Affected path, selection, rejection, and contract mutation cases
│   └── document-contracts/
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
| Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | Repo-static |
| Markdown profile self-test | `python3 scripts/validate-markdown-profiles.py --self-test` | Repo-static |
| Markdown profile compatibility | `python3 scripts/validate-markdown-profiles.py --root . --mode compatibility` | Repo-static finite-debt evidence |
| Cross-document self-test | `python3 scripts/validate-links-and-owners.py --self-test` | Repo-static link/index/owner/ledger mutation evidence |
| Cross-document compatibility | `python3 scripts/validate-links-and-owners.py --root . --mode compatibility` | Repo-static exact ledger-transition debt evidence |
| Cross-document inventory | `python3 scripts/validate-links-and-owners.py --root . --inventory --format json` | Repo-static ordered registry population |
| Agent role semantics fixture | `python3 scripts/validate-agent-role-semantics.py --self-test` | Repo-static 480-case category mutation evidence |
| Agent role semantics repository check | `python3 scripts/validate-agent-role-semantics.py --root .` | Repo-static thirty-adapter semantic coverage |
| Agent roster currentness fixture | `python3 scripts/validate-agent-roster-currentness.py . --self-test` | Repo-static |
| Agent roster currentness repository check | `python3 scripts/validate-agent-roster-currentness.py .` | Repo-static |
| Affected-surface fixture | `python3 scripts/validate-affected-surfaces.py --self-test` | Repo-static exact-route, argv, output, and NUL-transport evidence |
| Affected-surface repository coverage | `python3 scripts/validate-affected-surfaces.py --root .` | Repo-static tracked-path coverage; no ignored scratch traversal |
| Affected/all-files local runner | `python3 scripts/run-validation-lane.py --root . --lane affected\|all-files --paths-file <file.nul> --delimiter nul` | Repo-static shell-free execution of contract-selected argv; no-path and optional-tool `SKIP`, remote/live `DEFER`, and fallback evidence remain distinct |
| GitHub Actions security fixture | `python3 scripts/validate-github-actions-security.py --self-test` | Repo-static exact eleven primary, ten boundary, twenty-one required-write JSON cases, plus five internal uses-shape cases |
| GitHub Actions security repository check | `python3 scripts/validate-github-actions-security.py --root .` | PSH-002 bounded RED evidence; aggregate-gate integration is deferred to PSH-003 |
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
workspace-domain and provider-native metadata checks. Provider-neutral semantic
validation does not copy model/tool/effort fields; those values and exact scope
imports remain native adapter evidence. Report `affected`, `staged`,
`all-files`, `message/manual`, `ci`, and `remote/live` through the canonical
contract in `docs/00.agent-governance/rules/quality-standards.md`; static
adapter PASS does not prove provider runtime consumption.

### Evidence Boundaries

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
- `tests/fixtures/document-contracts/readme-profile-cases.json` schema v2는
  현재 `activePaths` 52개와 ADM-006 `retiredPaths` 20개를 분리해 보존한다.
  active baseline 47개와 retired baseline 20개가 immutable baseline 67개를
  재구성하고, 나머지 active 5개는 program-created handoff다. Retired 행은
  기존 profile/heading disposition과 `retiredBy`, provider-correct snapshot
  destination을 유지하며, 여덟 parser 사례는 active 경로만 참조한다.
- `tests/fixtures/document-contracts/template-compatibility.json`은 canonical form,
  template-mode inheritance, authored migration debt의 no-growth 기준을 고정한다.
  `affectedPaths`는 path/profile/rule/token을 정확히 결합하며 required
  89/247, residue 188/410, delimiter 24, unsupported 175/617/400 distinct
  tokens, duplicate 1, required-residue overlap 51, union 266을 초과하거나
  사용되지 않은 record을 남기면 실패한다.
- `tests/fixtures/markdown-profiles.json`은 60개 registry profile의 applicability를
  `validate-document`, `append-fragment`, `classification-only`, `excluded`로
  정확히 구분한다. Fixed `2026-07-12` 기준일, leap-day,
  template placeholder, append context, stable rule-ID mutation은 모두 production
  entry point를 통과한다.
- `tests/fixtures/links-and-owners.json`은 fence 및 HTML comment 밖의 inline/reference
  link, URL decode 경계, 선언된 세 index, owner-key 정규화·제외·중복, exact
  fourteen-column ledger를 production component로 검증한다. Semantic debt fixture는
  ADM-002가 ledger와 468-path self-row를 같은 commit에서 만들 때 제거하는 exact
  `LEDGER-MISSING` 한 건만 허용하며 alias, glob, growth, duplicate, unknown rule을
  configuration error로 거부한다.
- `tests/fixtures/agent-roster-currentness.json`은 이름이 정확히 `valid`,
  `missing-role`, `provider-mismatch`, `stale-count`, `bad-owner`인 사례 5개만
  허용한다. 각 이름의 mutation과 `expected_errors` 집합은 hardcoded
  per-case schema로 고정되며 self-test는 mutation 실행 전에 fixture
  semantics가 schema와 일치하는지 확인한다. 그 뒤 각 mutation을 확장하고
  repository 검증과 동일한 production `validate_contract()`를 호출해 실제
  오류 집합과 `expected_errors` 집합을 정확히 비교한다.
- `stale-count`는 `8 local agents`, `Eight local provider adapters`, `eight
  shared roles`, `8 role stems`의 고정된 네 variant를 각각 독립적으로
  거부한다. `bad-owner`는 canonical bootstrap label을 유지한 채 target만
  `rules/persona.md`로 바꿔 exact Markdown label/target 검사를 입증한다.
  Canonical owner link에는 일반 inline link만 인정되며 image syntax와
  leading-only 또는 trailing-only half-backtick label은 동일한 label/target을
  담아도 canonical link로 인정되지 않는다.
- `tests/fixtures/agent-role-semantics.json`은 정확히 10개 role, Gemini/Claude/
  Codex 3개 provider, responsibility/output/prohibition/stop/handoff/capability-
  tier/evidence/provider-stem 8개 category, remove/replace 2개 mutation의
  480-case Cartesian matrix를 고정한다. 모든 case는 production parser와
  validator를 사용하고 하나의 서로 다른 `ROLE-*` rule ID만 반환해야 한다.
  Mutation은 파싱된 객체가 아니라 provider source에 적용되어 480개 모두
  YAML/TOML/operative-Markdown parser를 다시 통과한다. 추가 33개 adversarial
  case는 duplicate/non-mapping/non-scalar YAML, fenced/absolute-or-list-
  container-indented code, HTML comment, strikethrough, blockquote/nested/lazy
  continuation, forward/backward revocation, external negation, inline-code-
  only claim, quoted/nested H1 우회를 거부한다. Category claim은 소유 section의
  paragraph/list-item unit 전체와 정확히 같아야 한다. `false`, `not true`,
  `invalid`, revoked 계열과 non-operative/non-applicable 상태는 단일 10-state
  vocabulary와 forward/backward 20개 production-parser probe로 동기화한다.
  공통 계약은 provider-native `model`, `tools`, `modelReasoningEffort`를
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
  Codex, Gemini provider runtime을 실행하지 않으며 provider-native runtime
  readiness를 입증할 수 없다.
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
