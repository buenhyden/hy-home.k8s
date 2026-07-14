# scripts

> 저장소 유지보수, 정적 검증, 자동화 보조 스크립트의 현재 실행 계약을 정리하는 진입 문서다.

## Overview

`scripts/`는 k3d/GitOps 저장소를 live cluster mutation 없이 검증하기 위한 repo-backed 유틸리티를 보관한다.
2026-07-04 기준 현재 `*.sh` 스크립트 8개는 모두 유지 대상이며, unused 또는 one-off 삭제 후보는 없다. 단, `render-platform-chart-kinds.sh`는 기본 로컬/CI bundle이 아니라 platform AppProject allow-list 변경 시 실행하는 manual review helper다.

이 영역은 GitOps manifest 자체(`gitops/`)나 live runtime 점검(`infrastructure/tests/`)을 대체하지 않는다.
대신 CI, post-edit hook, 필수 품질 게이트, 수동 검증 문서가 호출하거나 허용하는 반복 가능한 정적 검증 명령을 제공한다.

보존 근거(retention evidence), 명령·문서 표면(command/documentation surface), broad reference sweep은 분리해서 판단한다.
Tier A와 Tier B만 보존 근거이며, Tier C는 유지보수자가 갱신해야 하는 명령 계약 표면일 뿐 그 자체로 보존 근거가 아니다.
tracked text의 `scripts/*.sh` 참조는 삭제·리네임 safety net으로 모두 실제 파일을 가리켜야 하지만, 참조가 있다는 사실만으로 보존 근거가 되지는 않는다.

### Audience

이 README의 주요 독자:

- Platform maintainers
- Operators
- Documentation writers
- AI Agents

### Scope

#### In Scope

- 저장소 문서, GitOps 구조, manifest syntax, secret handling을 검증하는 작은 스크립트
- CI와 로컬 수동 검증에서 반복 실행할 수 있는 deterministic check
- 선택 도구가 없을 때의 local fallback 안내
- 현재 스크립트 유지 여부, 보존 근거, 명령 계약 표면

#### Out of Scope

- live cluster mutation을 수행하는 `kubectl apply`, `kubectl patch`, 배포 스크립트
- 외부 Vault, PostgreSQL, Valkey, Observability runtime을 직접 변경하는 스크립트
- GitOps manifest의 원천 파일
- `infrastructure/tests/`가 담당하는 runtime 또는 contract-level 검증 절차

## Structure

```text
scripts/
├── check-secret-handling.sh          # GitOps/infrastructure/examples manifest plaintext secret pattern scan
├── document_contracts.py             # Typed document registry, inventory, and classifier library
├── generate-llm-wiki-index.sh        # LLM Wiki generated Markdown index refresh/check
├── render-platform-chart-kinds.sh    # Manual Helm chart render review for platform AppProject allow-list impact
├── run-validation-lane.py            # Shell-free local affected/all-files validator runner
├── select-affected-surfaces.py       # NUL-only path-to-validator and CI-job selector
├── validate-agent-role-semantics.py # Provider-neutral semantic contract validation for thirty native role adapters
├── validate-agent-roster-currentness.py # Canonical three-provider roster and catalog owner-pointer validation
├── validate-affected-surfaces.py     # Affected-surface schema, fixture, and tracked-path coverage validation
├── validate-document-contract-registry.py # Registry v2 schema, inventory, route, and Stage 00 declaration validation
├── validate-gitops-change-set.py   # Identity-only GitOps object and deletion change-set review
├── validate-links-and-owners.py      # Full-corpus links, indexes, Stage 00 mirror, owners, and migration-ledger validation
├── validate-markdown-profiles.py       # Registry-driven Markdown semantics and finite compatibility debt
├── validate-gitops-structure.sh      # ArgoCD root app, kustomization structure, and resource completeness validation
├── validate-github-actions-security.py # Immutable Action identity and least-privilege permission validation
├── validate-harness.sh               # Repo-static harness validation wrapper over existing gates (no live checks)
├── validate-k8s-manifests.sh         # YAML syntax and optional kube-linter validation
├── validate-policy-gates.sh          # OPA/Conftest-style policy gate with built-in fallback
├── validate-repo-quality-gates.sh    # Repository governance, workflow, docs, and inventory gates
└── README.md                         # This file
```

## Configuration Boundary

Scripts are repository automation entrypoints, not permission to mutate live
systems. Preserve documented argument, environment, protected-surface, and
optional-tool contracts; credentials and secret values remain external inputs
and must not be logged or committed.

## Validation

Run the focused command contract for a changed script, then
`bash scripts/validate-repo-quality-gates.sh .` and the applicable pre-commit
hooks. A skipped optional tool or repository-static PASS is not live/runtime
readiness evidence.

`validate-repo-quality-gates.sh`는 일반 문서, affected path, agent role
semantics를 다시 구현하지 않는다. Python/PyYAML/JSON Schema 전제 조건을
확인한 뒤 document registry, Markdown profile, cross-document, affected-
surface, agent-role-semantics, roster-currentness 정본 validator를 strict
blocking mode로 호출한다. Wrapper 내부에는 provider-native model/tool/effort,
scope-import, operations index, GitOps, infrastructure, CI/QA, security,
version/supply-chain처럼 정본 validator로 대체되지 않은 workspace domain
검사만 남긴다. Validation lane, result, handoff 의미는
`docs/00.agent-governance/rules/quality-standards.md`가 소유한다.

## Operations

### Working Procedure

1. 새 스크립트를 만들기 전에 이 README의 Tier 기준과 command-contract allowlist를 확인한다.
2. 스크립트는 한 가지 검증 책임만 가져야 하며, 반복 실행해도 결과가 달라지지 않아야 한다.
3. secret, credential, live cluster mutation, publish/deploy 동작은 이 폴더의 기본 경로에 추가하지 않는다.
4. 스크립트를 추가·삭제·리네임하면 아래 command-contract allowlist의 파일을 함께 검토한다.
5. 새 참조가 Tier A/B 보존 근거인지, Tier C 명령·문서 표면인지 분리해서 기록한다.
6. 스크립트 삭제 또는 리네임은 별도 task/plan에 연결하고, rollback 방법과
   broad reference sweep 결과를 먼저 기록한다.
7. 변경 후 최소한 `bash scripts/validate-repo-quality-gates.sh .`와 `git diff --check`를 실행한다.

### 보존 기준 (Tier A/B/C)

| Tier                              | 의미                                                                                                       | 보존 근거    |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------ |
| Tier A / 자동 실행 게이트         | CI job 또는 post-edit hook이 스크립트를 직접 실행한다.                                                     | 예           |
| Tier B / 필수 간접 품질 게이트    | 필수 품질 게이트가 스크립트를 간접 실행하고, 스크립트가 generated artifact 또는 check contract를 소유한다. | 예, indirect |
| Tier C / 문서·수동·허용 목록 표면 | README, PR template, docs, allowlist, manual command reference에만 등장한다.                               | 아니오       |

Shell syntax coverage는 Bash 문법 검증 범위일 뿐 보존 근거가 아니다.
문법 검증에 포함된다는 사실만으로 스크립트를 유지하지 않는다.

### Script Inventory

| 스크립트                         | 결정     | 보존 근거                                                                                                                                                              | 명령·문서 표면                                                                                                                                                                            | 목적                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `validate-repo-quality-gates.sh` | Keep     | Tier A: CI `repo-quality-static`와 post-edit repository quality hook이 직접 실행한다.                                                                                  | root README, `scripts/README.md`, PR template, `.github/ABOUT.md`, `.claude/settings.json`, `docs/00.agent-governance/hooks/post-validate.sh`, `.codex/hooks.json`, docs quality guidance | 문서 구조, registry-selected README required/allowed H2, structural template coverage, `docs/98.archive` stage별 Tombstone index와 05.operations mirror coverage, active 01-05 stale runtime/OIDC/hook/CI/Rollouts/app-onboarding currentness contract rejection, `reference.template.md` archive wording 금지, `docs/05.operations` 인덱스/frontmatter 동기화, operations high-risk command boundary, incidents/postmortem boundary, `.env.example`/`.env` key-only parity, scripts inventory decision/Tier/classification/executable contract, tracked script reference sweep, examples role matrix와 sample-app/adminer reference boundary, app onboarding secret path contract, Vault policy write boundary, Docker network mutation boundary, RBAC create boundary, GitOps service/workload coverage matrix, GitOps image/workload-kind policy matrix, GitOps AppProject allow-list rationale matrix, GitOps namespace ownership matrix, kube-linter exclusion matrix, Traefik route/serverlb boundary, destructive Git deny list, external service contract matrix, secret management responsibility matrix, infrastructure coverage/test inventory, WSL2 runtime prerequisite matrix, bootstrap boundary matrix, GitHub workflow responsibility matrix, 템플릿 위치, workflow 중복, 스크립트 참조, obsolete 파일, version inventory drift, generated LLM Wiki freshness, agent mirror, canonical JIT runtime contract, Hookify local rule frontmatter/ignore 상태를 검증한다. |
| `validate-gitops-structure.sh`   | Keep     | Tier A: CI `manifest-static` job이 직접 실행한다.                                                                                                                      | root README, `scripts/README.md`, PR template, `.claude/settings.json`, GitOps READMEs                                                                                                    | ArgoCD root app, root app kind, root app manifest count, root/platform/workload hierarchy boundary, GitOps kustomization structure, sibling manifest resource completeness를 검증한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `validate-harness.sh` | Keep | Tier C manual wrapper: 하네스 변경을 한 명령으로 검증하는 로컬 진입점이다. CI/hook이 직접 실행하지 않고 기존 Tier A/B 게이트를 그대로 호출한다. | root README, `scripts/README.md`, PR template, harness implementation map | `validate-repo-quality-gates.sh`, `validate-gitops-change-set.py --root . --base-ref HEAD`, `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, `check-secret-handling.sh`, `validate-vault-eso-contracts.py --self-test`와 `--root .`, `validate-policy-gates.sh`, `infrastructure/tests/verify-contracts-static.sh`, `git diff --check`를 순서대로 실행하는 repo-static wrapper다. 추가 live cluster 검사는 실행하지 않는다. |
| `validate-k8s-manifests.sh`      | Keep     | Tier A: CI `manifest-static`와 post-edit manifest hook이 직접 실행한다.                                                                                                | root README, `scripts/README.md`, PR template, `.claude/settings.json`, `docs/00.agent-governance/hooks/post-validate.sh`, `.codex/hooks.json`, GitOps READMEs                            | manifest YAML syntax와 선택적 `kube-linter` 검증을 수행한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `check-secret-handling.sh`       | Keep     | Tier A: CI `manifest-static`와 post-edit manifest hook이 직접 실행한다.                                                                                                | root README, `scripts/README.md`, PR template, `.claude/settings.json`, `docs/00.agent-governance/hooks/post-validate.sh`, `.codex/hooks.json`, GitOps READMEs                            | GitOps, infrastructure, examples manifest의 plaintext secret pattern을 검사한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `generate-llm-wiki-index.sh`     | Keep     | Tier B indirect: 필수 `validate-repo-quality-gates.sh`가 `--check`로 간접 실행하고 `docs/90.references/llm-wiki/wiki-index.md` generated artifact contract를 소유한다. | root README, `scripts/README.md`, `.claude/settings.json`, LLM Wiki guide, references README, generated wiki index, document stage routing                                                | `docs/90.references/llm-wiki/wiki-index.md`를 Markdown-only canonical-owner link map으로 결정적으로 재생성하거나 검사한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `render-platform-chart-kinds.sh` | Deferred | Tier C manual review: platform Helm chart render review와 AppProject allow-list 영향 검토에서 실행한다.                                                                | `scripts/README.md`, `gitops/README.md`, 006 SDD evidence                                                                                                                                 | `gitops/apps/root`의 Helm chart Application을 `helm template --include-crds`로 렌더링하고, 렌더링된 kind가 platform AppProject allow-list에 포함되는지 확인한다. 기본 CI에서는 원격 chart fetch 변동성을 피하기 위해 실행하지 않는다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `validate-policy-gates.sh`       | Keep     | Tier A: CI `manifest-static` job이 직접 실행한다.                                                                                                                      | `.github/workflows/ci.yml`, `scripts/README.md`, `policy/conftest/kubernetes.rego`, CI/QA guide, 006 SDD evidence                                                                         | Conftest가 있으면 Rego policy bundle을 실행하고, 없으면 같은 핵심 Kubernetes/GitOps 정책을 built-in fallback으로 검증한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

#### Python Validator Inventory

| 스크립트 | 결정 | 보존 근거 | 검증 범위 | 공개 flag와 결과 의미 |
| --- | --- | --- | --- | --- |
| `run-validation-lane.py` | Keep | Tier B Spec 031 local consumer used by shared post-edit and lifecycle hooks | Imports the validated affected-surface contract, consumes NUL path records, selects `affected` or `all-files` validator IDs, and invokes only approved argv arrays with `shell=False`. Remote/live validators are always `DEFER`; no paths and missing optional tools are `SKIP`, with fallback evidence reported separately. Child stdout/stderr never enters the result; fixed status, return code, byte counts, and SHA-256 digests provide bounded non-secret metadata. | `--root`, `--lane affected\|all-files`, `--paths-file`, required `--delimiter nul`; stable `PASS`/`SKIP`/`FAIL`/`DEFER` lines include command, tool, scope, limitation, and evidence class. Exit `1` means a contract, selection, required-tool, or command failure. |
| `select-affected-surfaces.py` | Keep | Tier B Spec 031 selector consumed by local/CI integrations in later ASQA units | NUL-terminated UTF-8 path records, exact-one surface selection, lane-filtered validated argv IDs, maximum protection level, and sorted CI job output. It never invokes a shell or accepts newline-delimited machine input. | `--root`, `--lane affected\|staged\|all-files\|ci`, `--paths-file`, required `--delimiter nul`, `--format json\|github-output`; exit `0` emits stable sorted output, exit `1` reports a stable contract/path rule ID. |
| `validate-affected-surfaces.py` | Keep | Tier A affected-surface contract gate introduced by Spec 031 | Draft 2020-12 schema, closed semantic references, shell-metacharacter-free argv arrays, exact case-sensitive direct-script executable tokens (`bash`, `python3`, `node`) with no path prefix, normalized script operands, fail-closed exact/combined/assignment interpreter-eval options, wrapper rejection, mandatory surface fallbacks, positive/negative/mutation fixtures, and NUL-based `git ls-files` coverage without following symlink children. Interpreter options are examined only before the script operand or `--`; identically named script arguments after the operand remain data. | `--root`, `--self-test`; `PASS`/exit `0` means all tracked paths have exactly one surface and the fixture contract passes, while `FAIL`/exit `1` names the stable rule ID. |
| `validate-document-contract-registry.py` | Keep | Tier A document contract registry gate | Repository-static v2 `jsonschema` preflight, mode-aware Git inventory, exactly-one route classification, and normalized tracked-regular Stage 00 current-authority declaration checks. 기본 inventory는 tracked-only이고 named untracked candidate만 `lstat()`으로 검사하며 ignored path와 symlink는 열거나 순회하지 않는다. | `--root`, `--mode compatibility\|strict`, `--profile`, repeatable `--include-path`, `--self-test`; `PASS`/exit `0`은 선택 scope 통과, `FAIL`/non-zero는 rule-ID 또는 입력 경계 위반을 뜻한다. |
| `validate-gitops-change-set.py` | Keep | Tier A PSH-004 gate consumed by `manifest-static` and the repository quality gate | Exact `kustomize.config.k8s.io/v1beta1` Kustomization `resources` graphs are reduced to immutable `(apiVersion, kind, namespace, name)` identities. Every serialized identity/path token is ASCII grammar-checked before output; paths are safe repository-relative evidence only, so a path-only move is one `RETAIN`. Unsupported dialects/directives, remote or unsafe paths, symlinks, non-regular entries, cycles, duplicate YAML keys/identities, malformed tokens, and unavailable Git parents fail closed with value-free diagnostics. | `--self-test` runs the exact fixture plus durable negative renderer and temporary Git-history/shallow-clone cases; or use `--root` with `--base-ref`. `--base-ref HEAD` is the local static comparison. Forty-zero uses the first HEAD parent only when that object is available, returns the empty graph only for a true root, and otherwise fails. Exit `0` emits only `ADD\|DELETE\|RETAIN apiVersion kind namespace/name path`. |
| `validate-github-actions-security.py` | Keep | Tier A PSH-003 security gate; self-test and repository modes are both required repository-quality aggregate evidence. | Duplicate-key-rejecting YAML, non-erasing typed `uses` parser/source parity, immutable remote SHA and Docker digest references, same-line human version comments, fail-closed non-symlink repository/workflow/zizmor inputs, explicit top-level `contents: read`, mandatory exact three-job write consumers, default-deny writes, `write-all` rejection, and `unpinned-uses` suppression rejection. | `--self-test`, `--root`; self-test `PASS` preserves the exact eleven primary, ten repository-boundary, twenty-one required-write JSON cases, and five internal uses-shape cases. Repository `PASS` enforces immutable Action identities and least-privilege permissions; either mode failing blocks the aggregate gate. |
| `validate-vault-eso-contracts.py` | Keep | Tier A PSH-005 gate consumed by `manifest-static`, the affected-surface registry, local harness, and repository quality gate. | Reads only the fixed Vault store, TokenReview binding, external Service/EndpointSlice, verify-only HCL, and bootstrap inputs. It enforces local-only HTTP annotations, exact ESO identity/audience, one TokenReview subject, the six-path read/list policy, HTTPS plus readable CA, `/dev/tty` token input, stdin header/secret flow, and no insecure or noninteractive fallback. | `--self-test` runs the exact ten-case non-secret fixture; `--root` performs repository-static validation. Exit `0` prints a fixed PASS line, exit `1` emits only fixed path/diagnostic text, and exit `2` is a configuration or CLI failure. |
| `validate-markdown-profiles.py` | Keep | Tier B semantic document gate; Spec 029 SMDV-004 invokes it through the repository orchestrator. | Registry-selected Frontmatter, H1/H2, fence, residue, append-fragment, native/generated structural N/A, and imported README handoff semantics. Compatibility debt is read only from the finite Spec-030-owned fixture. | `--root`, `--mode compatibility\|strict`, `--format text\|json`, repeatable `--include-path`, mutually exclusive `--self-test`/`--inventory`; exit `0` is clean or exact compatibility `DEFER`, `1` is a document violation/strict debt, and `2` is configuration or CLI failure. |
| `validate-links-and-owners.py` | Keep | Tier B cross-document semantic gate; Spec 029 SMDV-004 invokes it through the repository orchestrator. | All registry `current_paths` links, the three declared indexes, reciprocal Stage 00 current-authority lifecycle and README mirror equality, deterministic current-owner keys, and the exact fourteen-column Spec 030 migration ledger. It reads no network or secret content and does not dereference provider symlink adapters. | `--root`, `--mode compatibility\|strict`, `--format text\|json`, repeatable `--include-path`, mutually exclusive `--self-test`/`--inventory`; JSON inventory returns the exact ordered registry population. Exit `0` is clean or the exact compatibility ledger `DEFER`, `1` is a document violation/strict debt, and `2` is configuration or CLI failure. |

### Script Classification Matrix

이 표는 task contract의 script classification 용어를 `scripts/` SSoT에 직접
남긴다. 현재 분류는 삭제나 통합을 승인하지 않으며, 새 스크립트가 추가되면
`one-off`, `reusable`, `operations-critical`, `development-helper`, `unknown`
중 하나 이상으로 분류하고 삭제·통합 후보 여부를 별도 task/plan에 연결한다.

| 스크립트                         | 분류                         | 삭제 후보 | 통합 후보 | 근거                                                                                                                                                  |
| -------------------------------- | ---------------------------- | --------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `validate-repo-quality-gates.sh` | operations-critical/reusable | No        | No        | Tier A governance gate이며 repository-wide docs, workflow, script, GitOps, infrastructure, examples, agent-runtime drift를 한 명령 계약으로 검증한다. |
| `validate-gitops-structure.sh`   | operations-critical/reusable | No        | No        | Tier A manifest-static gate이며 ArgoCD root app, ApplicationSet, hierarchy, kustomization completeness를 별도 실패 의미로 검증한다.                   |
| `validate-harness.sh` | development-helper/reusable | No | No | Tier C manual wrapper이며 새 로직 없이 기존 repo-static 게이트를 묶는 단일 하네스 검증 진입점이다. live cluster 검사는 포함하지 않는다. |
| `validate-k8s-manifests.sh`      | operations-critical/reusable | No        | No        | Tier A manifest-static gate이며 YAML syntax와 선택적 kube-linter 검증을 담당한다.                                                                     |
| `check-secret-handling.sh`       | operations-critical/reusable | No        | No        | Tier A manifest-static gate이며 plaintext secret pattern scan과 redacted finding 출력을 담당한다.                                                     |
| `generate-llm-wiki-index.sh`     | development-helper/reusable  | No        | No        | Tier B indirect helper이며 generated LLM Wiki index 재생성과 `--check` freshness contract를 소유한다.                                                 |
| `render-platform-chart-kinds.sh` | development-helper/reusable  | No        | No        | Tier C manual review helper이며 platform Helm chart render 결과와 AppProject allow-list coverage를 재현 가능하게 검토한다.                            |
| `validate-policy-gates.sh`       | operations-critical/reusable | No        | No        | Tier A manifest-static policy helper이며 Conftest/Rego bundle 또는 built-in fallback으로 GitOps policy gates를 검증한다.                              |

2026-06-04 broad reference sweep 기준 unused 또는 one-off 삭제 후보는 없다. `render-platform-chart-kinds.sh`는 Tier C manual helper이므로 기본 local/remote QA gate에는 포함하지 않지만, platform Helm chart Application이나 AppProject allow-list 변경 시 유지되는 재현 명령이다.

### 통합하지 않는 기준

스크립트 통합은 같은 trigger, 같은 scan domain, 같은 failure semantics, 별도 command contract 없음이라는 네 조건을 모두 만족할 때만 검토한다.
현재 스크립트는 repository governance, GitOps structure, Kubernetes manifest syntax, plaintext secret scan, generated LLM Wiki index라는 서로 다른 실패 의미와 명령 계약을 가진다.
따라서 현재 스크립트는 삭제·통합·리네임하지 않고 분리 유지한다.

### 삭제·리네임 precheck

스크립트를 삭제하거나 이름을 바꾸려면 아래 precheck가 모두 통과해야 한다.
현재 스크립트 8개는 이 기준을 통과한 삭제 후보가 아니므로 유지한다.

1. linked Spec/Plan/Task가 삭제 또는 리네임 이유, 영향 범위, rollback 방법을
   명시한다.
2. command-contract allowlist 표면을 먼저 확인한다.
3. broad reference sweep을 실행해 allowlist 밖의 활성 참조를 찾는다.

   ```bash
   rg -n "scripts/<name>\\.sh|<name>\\.sh" .
   ```

4. 결과를 Tier A/B 보존 근거, Tier C 명령 표면, historical/superseded
   evidence로 분류한다.
5. Tier A/B 참조가 남아 있거나 역할 대체가 검증되지 않았으면 삭제하지 않는다.
6. 삭제 또는 리네임 후에는 README, CI, hook, docs, GitOps, operations 문서의
   cross-link와 명령 예시를 함께 갱신한다.

### 명령 계약 허용 목록

이 표가 command-contract allowlist maintenance surface다.
`scripts/validate-repo-quality-gates.sh`는 아래 명시 파일에서 `scripts/<name>.sh` 형식의 활성 명령 계약 참조만 검사한다.
새 스크립트를 추가·삭제·리네임할 때는 이 표면을 갱신하거나 확인한다.
별도로, 같은 gate는 tracked text 전체에서 `scripts/*.sh` 참조가 dangling 상태가 아닌지 확인한다.
이 broad reference sweep은 삭제·리네임 안전장치이며, 모든 참조를 Tier A/B 보존 근거로 승격하지 않는다.

| 표면                                                        | 유지보수 이유                                                  |
| ----------------------------------------------------------- | -------------------------------------------------------------- |
| `README.md`                                                 | root-level 수동 검증 명령 표면                                 |
| `scripts/README.md`                                         | 현재 스크립트 inventory, retention tier, command contract SSoT |
| `.github/workflows/ci.yml`                                  | CI job 실행과 path-filter 계약                                 |
| `.github/PULL_REQUEST_TEMPLATE.md`                          | reviewer-facing 수동 검증 checklist                            |
| `.github/ABOUT.md`                                          | GitHub governance routing 표면                                 |
| `.claude/settings.json`                                     | Claude command allowlist 표면                                  |
| `.claude/CLAUDE.md`                                         | local runtime baseline의 generated-script ownership 참조       |
| `docs/00.agent-governance/hooks/post-validate.sh`           | post-edit validation 실행 표면                                 |
| `docs/00.agent-governance/hooks/lifecycle-guard.sh`         | Stop/SubagentStop/PreCompact lifecycle validation 실행 표면    |
| `.codex/hooks.json`                                         | Codex event hook wiring 표면                                   |
| `docs/05.operations/guides/0009-llm-wiki-curation-guide.md` | LLM Wiki generator 운영 guide                                  |
| `docs/90.references/README.md`                              | references index와 generated-index maintenance note            |
| `docs/90.references/llm-wiki/README.md`                     | LLM Wiki reference-only boundary와 generator command           |
| `docs/90.references/llm-wiki/wiki-index.md`                 | generated artifact metadata와 freshness contract               |
| `gitops/README.md`                                          | GitOps validation command 표면                                 |
| `gitops/workloads/README.md`                                | workload validation command 표면                               |
| `docs/README.md`                                            | docs quality gate command 표면                                 |
| `docs/00.agent-governance/rules/document-stage-routing.md`  | active generated-index routing contract                        |

### Command Contract

GitHub Actions security validation uses one production path for its fixture and
repository modes. Remote Actions require exact forty-character commit SHAs,
Docker Actions require `sha256` digests, and both retain same-line human version
comments. Workflows set top-level `contents: read`; only the exact greeting,
label, and stale job write sets are allowed and all three consumers are
required when their workflow exists. The root, `.github`, workflows directory,
workflow YAMLs, and optional zizmor YAML are inspected without resolving
symlinks; missing/empty boundaries and non-regular inputs fail before content
is read. Parsed and source `uses` collectors preserve non-string occurrences;
numeric, null, mapping, list, and other non-string shapes fail the same-line
scalar contract rather than disappearing from both views. Duplicate YAML keys,
`write-all`, missing/reduced/unknown/expanded write sets, and `unpinned-uses`
suppression fail closed.

```bash
python3 scripts/validate-github-actions-security.py --self-test
python3 scripts/validate-github-actions-security.py --root .
```

During PSH-002 the first command is GREEN and the second is intentionally RED
with fourteen mutable references, three missing workflow defaults, and one
suppression. Repository-quality-gate integration waits for PSH-003; this
bounded RED state is not a gate bypass or remote/runtime evidence.

provider-neutral role semantics는 공통 계약에 provider model, tool,
reasoning-effort 값을 복제하지 않고 responsibility, output, prohibition,
stop, handoff, capability tier, required evidence만 소유한다. 검증기는
Markdown adapter의 YAML frontmatter와 본문, Codex adapter의 TOML
`developer_instructions`를 provider-native 형식으로 읽는다. YAML은 duplicate
key, non-mapping frontmatter, non-scalar `name`을 fail-closed로 거부한다.
Semantic matching은 fenced code, HTML comment, strikethrough, revoked 또는
contradictory line을 제외한 operative Markdown에서 whitespace만 정규화한다.

```bash
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
```

첫 번째 명령은 정확히 10 roles × 3 providers × 8 categories ×
remove/replace = 480 mutation을 production validator에 통과시키고 각 결과가
하나의 category-specific rule ID만 내는지 확인한다. 또한 공통 계약에
`model`, `tools`, `modelReasoningEffort`가 추가되면 schema 오류로 거부한다.
480개 모두 provider source를 실제 YAML/TOML/Markdown parser에 다시 통과하며,
33개 고정 adversarial case가 malformed YAML, absolute/list-container
indented code, indented tilde fence, comment, strikethrough, blockquote/nested/
lazy quote, forward/backward revocation, external negation, inline-code-only
claim 우회를 거부한다. Claim은 category 소유 section의 정규화된 paragraph
또는 list-item unit 전체와 정확히 같을 때만 인정한다. 하나의 10-state
negation vocabulary는 forward/backward 양방향 20개 source probe로 고정한다.
두 번째 명령은 30개 adapter의 stem, responsibility, output, prohibited
action, stop condition, handoff, provider-neutral capability tier, required
evidence를 검증한다. 두 결과는 repo-static evidence이며 provider runtime
consumption이나 live 권한을 입증하지 않는다.

Repository quality는 위 두 명령과 affected-surface/roster validator를
blocking entry point에서 실행한다. Native model, tool, reasoning-effort,
scope-import currentness는 provider-neutral contract에 복제하지 않고 wrapper의
provider metadata 검사에 남긴다.

canonical roster와 owner-link 검증은 fixture self-test와 repository input에
동일한 production contract를 사용한다.

```bash
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
```

첫 번째 명령은 이름이 정확히 `valid`, `missing-role`, `provider-mismatch`,
`stale-count`, `bad-owner`인 fixture case 5개만 허용하고, production
`validate_contract()`의 실제 오류 집합과 각 `expected_errors` 집합을 정확히
비교한다. 각 case 이름은 고정된 mutation과 정확한 `expected_errors` 집합에
매핑되며, `stale-count`의 catalog variant도 `8 local agents`, `Eight local
provider adapters`, `eight shared roles`, `8 role stems` 네 값으로 고정된다.
Self-test는 mutation 실행 전에 이 case semantics를 hardcoded schema와
비교한다. 두 번째 명령은 세 provider adapter stem set, 30-file inventory,
대소문자를 구분하지 않는 numeric/spelled stale eight-role prose, canonical
harness Markdown label과 정확한 상대 link target 쌍을 확인한다. Canonical
owner link는 일반 inline link만 인정하므로 image syntax와 leading-only 또는
trailing-only half-backtick label은 올바른 label/target을 사용해도 거부한다.
두 명령 모두 repo-static 검사이며 provider runtime readiness를 입증하지
않는다.

document contract registry 명령은 다음 다섯 flag 표면을 제공한다.

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
python3 scripts/validate-document-contract-registry.py --root . --mode strict --profile test/sample --include-path tests/fixtures/document-contracts/candidate.md
python3 scripts/validate-document-contract-registry.py --root . --self-test
```

`--root`, `--mode compatibility|strict`, `--profile`, repeatable
`--include-path`, `--self-test`만 공개 flag로 사용한다. 기본 inventory는
mode-aware Git index에서 얻은 tracked file만 포함하고 filesystem walk나 broad
untracked discovery를 하지 않는다. 명시한 `--include-path`만 POSIX 상대 경로,
ignore 상태, symlink-free `lstat()`, regular Markdown target 순으로 검사해
추가한다. 모든 route 검사 전에 `Draft202012Validator` 기반 `jsonschema`
preflight를 수행한다. `PASS`와 exit `0`은 선택 scope가 schema, inventory,
exactly-one classification을 통과했다는 뜻이며, `FAIL`과 non-zero exit는 rule
ID 또는 입력 경계 위반을 뜻한다. Repository 실행은 classification 성공/실패
모두 `baseline=<n> new=<n> uncovered=<n> ambiguous=<n>` 요약을 출력하며,
baseline inventory 실측값이 `433`이 아니면 classification 전에 실패한다.
`--self-test` PASS는 production
`validate_registry()`와 `classify_paths()`를 사용하는 mutation 9개가 모두
기대 rule-ID 집합과 일치했다는 뜻이다. 이 명령은 repository-static이며 live
cluster나 remote provider readiness를 입증하지 않는다.

Markdown profile validator는 `--self-test`, `--root`,
`--mode compatibility|strict`, `--format text|json`, repeatable
`--include-path`, `--inventory`를 제공한다. Text와 JSON은 같은
`(path, profile, ruleId, debtToken)` 정렬을 사용한다. Compatibility
mode는 Spec-030-owned fixture의 정확한 266개 경로 합집과 1,299개
진단만 `DEFER`하고, strict mode는 같은 진단을 `FAIL`한다. 새
path/rule/token, 사용되지 않은 debt record, cap 증가, 비정상 fixture는
통과하지 않는다. 이 명령은 tracked repository content만 읽으며
외부 URL, live cluster, provider runtime readiness를 검증하지 않는다.

| Command                                           | Argument Contract                                                                      | Scan / Validation Scope                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Result Semantics                                                                                                                                                                                   |
| ------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/generate-llm-wiki-index.sh`         | 인자를 받지 않는다.                                                                    | `docs/90.references/llm-wiki/wiki-index.md`를 generator에 정의된 canonical owner 링크맵으로 재생성한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | exit `0`은 generated Markdown index를 갱신했다는 뜻이다.                                                                                                                                           |
| `bash scripts/generate-llm-wiki-index.sh --check` | `--check`만 지원한다.                                                                  | 현재 `wiki-index.md`가 generator output과 일치하는지 비교한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | exit `0`은 generated index가 최신이라는 뜻이고, 불일치 또는 누락은 실패한다.                                                                                                                       |
| `bash scripts/validate-repo-quality-gates.sh .`   | 선택 인자는 repository root다.                                                         | 문서 taxonomy, registry-selected README required/allowed H2, structural template coverage, required template headings, archive Tombstone coverage와 01-05 stage index, active 01-05 stale runtime/OIDC/hook/CI/Rollouts/app-onboarding currentness contract rejection, `reference.template.md` archive wording 금지, `docs/05.operations` 인덱스/frontmatter 동기화, operations high-risk command boundary, incidents/postmortem boundary, `.env.example`/`.env` key-only parity, scripts inventory decision/Tier/classification/executable contract, tracked script reference sweep, examples role matrix와 sample-app/adminer reference boundary, app onboarding secret path contract, Vault policy write boundary, RBAC create boundary, GitOps service/workload coverage matrix, GitOps image/workload-kind policy matrix, GitOps AppProject allow-list rationale matrix, GitOps namespace ownership matrix, kube-linter exclusion matrix, Traefik route/serverlb boundary, destructive Git deny list, infrastructure coverage/test inventory, WSL2 runtime prerequisite matrix, workflow 계약, script 참조, runtime mirror inventory, Hookify local rule shape, version inventory를 검증한다. | `PASS`는 repository governance gate 통과를 뜻하고, `ERR`는 계약 drift를 뜻한다.                                                                                                                    |
| `bash scripts/validate-gitops-structure.sh`       | 인자를 받지 않는다. 스크립트가 속한 repository에서 실행된다.                           | ArgoCD root app, root application kind, root app manifest, `clusters/local` root/ApplicationSet boundary, root app local source path boundary, `gitops/**/kustomization.yaml` syntax, sibling manifest resource completeness를 검증한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | exit `0`은 필요한 GitOps 구조가 있고 parse 가능하며 root/platform/workload hierarchy와 각 `kustomization.yaml`의 sibling YAML manifest 참조가 유효하다는 뜻이다.                                   |
| `bash scripts/validate-harness.sh` | 인자를 받지 않는다. 스크립트 위치 기준 repository root에서 실행된다. | `validate-repo-quality-gates.sh`, `validate-gitops-change-set.py --root . --base-ref HEAD`, `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, `check-secret-handling.sh`, `validate-vault-eso-contracts.py --self-test`와 `--root .`, `validate-policy-gates.sh`, `infrastructure/tests/verify-contracts-static.sh`, `git diff --check`를 순서대로 실행한다. 추가 live cluster 검사는 실행하지 않는다. | exit `0`은 모든 repo-static 하네스 게이트가 통과했다는 뜻이다. 하위 게이트 실패는 그대로 전파된다. |
| `python3 scripts/validate-vault-eso-contracts.py --self-test` | 추가 인자를 받지 않는다. | `tests/fixtures/vault-eso-contracts.json`의 정확한 10개 non-secret mutation을 production validator 함수에 적용한다. | exit `0`은 정확한 10개 case가 기대 diagnostics와 일치했다는 뜻이고, fixture/schema/mutation drift는 실패한다. |
| `python3 scripts/validate-vault-eso-contracts.py --root .` | `--root`는 repository root만 허용한다. | 다섯 개 고정 공개 입력만 읽어 Vault/ESO identity, audience, TokenReview, policy, bootstrap secret-process/TLS 계약을 검증한다. | exit `0`은 repo-static 계약 통과이며 live Vault, ESO, secret value, credential, 또는 production TLS readiness 증거가 아니다. |
| `bash scripts/validate-k8s-manifests.sh .`        | 선택 인자는 arbitrary subpath가 아니라 repository root다.                              | `gitops/`, `infrastructure/`, `examples/sample-app/`, `examples/**/{gitops,kubernetes}/`, `traefik/` 아래 YAML을 검사하고, `kube-linter`가 있으면 함께 실행한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | exit `0`은 YAML syntax가 통과했고 optional `kube-linter`도 실패하지 않았다는 뜻이다. `SKIP optional kube-linter`는 local YAML-only validation이며 kube-linter coverage가 아니다. 잘못된 repo root 또는 YAML 0건은 실패한다. |
| `bash scripts/check-secret-handling.sh .`         | 선택 인자는 arbitrary subpath가 아니라 repository root다.                              | `gitops/`, `infrastructure/`, `examples/sample-app/`, `examples/**/{gitops,kubernetes}/` 아래 YAML에서 quoted literal 값을 포함한 plaintext secret pattern을 검사하되 ExternalSecret-like resource는 제외한다. Finding 출력은 값을 `<redacted>`로 숨긴다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | exit `0`은 검사 대상 파일이 있고 plaintext secret pattern이 없다는 뜻이다. 잘못된 repo root, YAML 0건, finding은 실패한다.                                                                         |
| `bash scripts/render-platform-chart-kinds.sh .`   | 선택 인자는 repository root다. 생략하면 스크립트 위치 기준 repository root를 사용한다. | `gitops/apps/root`의 Helm chart Application을 렌더링하고 `gitops/clusters/local/appproject-platform.yaml` allow-list와 비교한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | exit `0`은 모든 렌더링 kind가 platform AppProject allow-list에 포함된다는 뜻이다. Helm 렌더 실패 또는 누락 kind는 실패한다.                                                                        |
| `bash scripts/validate-policy-gates.sh .`         | 선택 인자는 repository root다. 생략하면 스크립트 위치 기준 repository root를 사용한다. | `policy/conftest/kubernetes.rego`와 built-in fallback으로 plaintext Secret, `CreateNamespace=true`, AppProject wildcard, `latest` image 정책을 검사한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | exit `0`은 Conftest 또는 fallback policy gate가 통과했다는 뜻이다. Conftest 미설치는 `SKIP optional conftest`와 fallback 실행으로 보완하며, conftest coverage로 보고하지 않는다. policy violation은 실패한다.                                                      |

`HY_HOME_K8S_SKIP_HOOK_SIMULATION=1`은 `docs/00.agent-governance/hooks/*` wrapper가
`validate-repo-quality-gates.sh`를 재귀 호출하지 않도록 사용하는 internal bypass다.
일반 수동 검증 계약이 아니며, maintainer가 직접 실행하는 품질 게이트에서는 기본값처럼
hook simulation을 포함해야 한다.

### Local Tool Availability

필수 도구:

- `python3`
- Python `PyYAML`
- Python `jsonschema`

선택 도구:

- `pre-commit`: 전체 hook matrix를 로컬에서 실행할 때 사용한다. 없으면 repo-backed 스크립트 묶음을 먼저 실행하고 CI 결과를 확인한다.
- `kube-linter`: `validate-k8s-manifests.sh`가 PATH에서 발견하면 실행한다. 없으면 해당 스크립트가 kube-linter 단계만 skip하고 YAML syntax는 계속 검증한다.
- `conftest`: `validate-policy-gates.sh`가 PATH에서 발견하면 Rego bundle을 실행한다. 없으면 built-in fallback policy check를 계속 실행한다.
- `helm`: `render-platform-chart-kinds.sh` manual review helper를 실행할 때 필요하다. 기본 local/remote QA bundle에는 포함하지 않는다.
- `graphify`: 선택적 지식 그래프 갱신 도구다. 없으면 직접 source inspection 결과를 기록한다.

### Kube-linter Exclusion Matrix

이 표는 `.kube-linter.yaml`의 현재 제외 목록과 제외 사유를 연결한다.
`validate-repo-quality-gates.sh`는 YAML exclusion 목록, inline rationale,
이 표의 row order가 일치하는지 검증한다. 이 표는 kube-linter를 필수
로컬 도구로 승격하지 않으며, 실제 enforcement 변경은 별도 CI/tooling
hardening pass에서 다룬다.

| Excluded check              | Current rationale                                                                        | Boundary                                                                                                                               | Follow-up                                                            |
| --------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `no-read-only-root-fs`      | Home lab workloads may need writable filesystems during local bootstrap.                 | Excluded by `.kube-linter.yaml`; YAML syntax, GitOps structure, secret scan, and repo-quality guardrails still run.                    | Revisit before production or shared-cluster hardening.               |
| `no-anti-affinity`          | Local k3d capacity does not make strict anti-affinity a default requirement.             | Excluded by `.kube-linter.yaml`; availability requirements stay in explicit architecture or operations docs.                           | Revisit when HA scheduling policy becomes mandatory.                 |
| `unset-cpu-requirements`    | Local development workloads do not require CPU requests by default.                      | Excluded by `.kube-linter.yaml`; resource policy remains a separate hardening decision.                                                | Revisit before enforcing workload resource budgets.                  |
| `unset-memory-requirements` | Local development workloads do not require memory requests by default.                   | Excluded by `.kube-linter.yaml`; resource policy remains a separate hardening decision.                                                | Revisit before enforcing workload resource budgets.                  |
| `run-as-non-root`           | Some upstream images used in the lab still require root during bootstrap.                | Excluded by `.kube-linter.yaml`; security review remains explicit and no plaintext secret policy is relaxed.                           | Revisit per image before production-like hardening.                  |
| `latest-tag`                | Some bootstrap or upstream defaults may be unpinned before a pinning decision.           | Excluded by `.kube-linter.yaml`; active GitOps image tag policy is guarded by `gitops/README.md` and `validate-repo-quality-gates.sh`. | Revisit after image pinning failure mode and CI policy are approved. |
| `dangling-service`          | Argo Rollouts progressive delivery can stage services before rollout wiring is complete. | Excluded by `.kube-linter.yaml`; GitOps structure and manifest syntax validation still run.                                            | Revisit after rollout/service wiring policy is narrowed.             |

### Link Basis

이 README의 링크 기준 위치는 `scripts/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [Root README](../README.md)
- [GitHub CI Workflow](../.github/workflows/ci.yml)
- [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)
- [Pre-commit Config](../.pre-commit-config.yaml)
- [Claude Settings](../.claude/settings.json)
- [Infrastructure Tests](../infrastructure/tests/)
- [Agent Governance Bootstrap](../docs/00.agent-governance/rules/bootstrap.md)
- [LLM Wiki Curation Guide](../docs/05.operations/guides/0009-llm-wiki-curation-guide.md)
- [Generated LLM WIKI Index](../docs/90.references/llm-wiki/wiki-index.md)
- [scripts Inventory Remediation Plan](../docs/04.execution/plans/2026-05-09-scripts-inventory-remediation.md)
