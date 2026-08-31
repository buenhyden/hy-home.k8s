# scripts

> 저장소 유지보수, 정적 검증, 자동화 보조 스크립트의 현재 실행 계약을 정리하는 진입 문서다.

## Overview

`scripts/`는 k3d/GitOps 저장소를 live cluster mutation 없이 검증하기 위한 repo-backed 유틸리티를 보관한다.
현재 shell entrypoint와 Python module의 보존·통합·삭제 여부는 extension이나
고정 파일 수가 아니라 현재 consumer, 고유 진단, recovery 책임으로 결정한다.
`render-platform-chart-kinds.sh`는 기본 로컬/CI bundle이 아니라 platform
AppProject allow-list 변경 시 실행하는 manual review helper다.

이 영역은 GitOps manifest 자체(`gitops/`)나 live runtime 점검(`infrastructure/tests/`)을 대체하지 않는다.
대신 CI, post-edit hook, 필수 품질 게이트, 수동 검증 문서가 호출하거나 허용하는 반복 가능한 정적 검증 명령을 제공한다.

보존 근거(retention evidence), 명령·문서 표면(command/documentation surface), broad reference sweep은 분리해서 판단한다.
Tier A와 Tier B만 보존 근거이며, Tier C는 유지보수자가 갱신해야 하는 명령 계약 표면일 뿐 그 자체로 보존 근거가 아니다.
현재 실행 표면의 `scripts/` 참조는 routing registry의 실제 argv에서 파생한
executable suffix와 임의 depth에 대해 tracked regular file을 가리켜야 하지만,
참조가 있다는 사실만으로 보존 근거가 되지는 않는다. 비종결 Stage 03은
proposal이며 current executable을 주장하지 않는다. 종결 문서와 Stage 90은
reachable Git을 기본 recovery owner로 사용하고, Stage 98은 선행 Archive
validator가 소유한다.

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
├── agent_registry_compat.py         # Import-only delegation for transitional registry CLI names
├── archive_cutover.py               # ARWB-003 local/manual atomic production cutover proof
├── archive_cutover_manifest.py      # Import-only finite archive/lifecycle cutover constants
├── archive_recovery.py              # Private ARWB-001 exact Git-object and ArchiveEnvelope.v1 fixture capability
├── archive_validation.py            # Import-only ARWB-002 archive, history, authority, and immutability validation
├── check-secret-handling.sh          # GitOps/infrastructure/examples manifest plaintext secret pattern scan
├── document_authority.py             # Bounded terminal Stage 99 document authority validation
├── document_contracts.py             # Closed registry v8 loader with archive-envelope, value, role, admission, lifecycle, evidence, lineage, inventory, and classifier projections
├── document_lifecycle.py             # Pure immutable base/proposed document lifecycle comparison and stable diagnostics
├── json_schema_validation.py        # Shared offline JSON Schema evaluation for agent/document owners
├── migrate-document-work-units.py     # WORK-109 reviewed four-digit work-unit migration apply and manifest loader
├── render-platform-chart-kinds.sh    # Manual Helm chart render review for platform AppProject allow-list impact
├── run-validation-lane.py            # Shell-free local affected/staged/all-files validator runner
├── select-affected-surfaces.py       # NUL-only path-to-validator and CI-job selector
├── validate-agent-evaluations.py # Transitional CLI delegating to the neutral agent registry
├── validate-agent-governance-ci.py # Closed agent-governance selector, job, summary, routing, and static-evidence contract
├── validate-agent-governance-closure.py # Transitional CLI delegating closure checks to the neutral agent registry
├── validate-agent-harness-contract.py # Neutral agent registry schema and graph validation
├── validate-agent-harness-semantics.py # Registry-backed neutral and native role semantics and projection parity
├── validate-agent-legacy-cutover.py # Retired surfaces, current instruction consumers, and historical proof adapter
├── validate-agent-model-fitness.py # Transitional CLI delegating to the neutral agent registry
├── validate-agent-provider-config.py # Closed provider source, surface, model, MCP, and local-observation contract
├── validate-agent-provider-canaries.py # Redacted provider evidence-lane and no-mutation canary records
├── validate-agent-provider-evidence.py # Routed aggregate for the two focused provider validators
├── validate-agent-roster-admission.py # Transitional CLI delegating to the neutral agent registry
├── validate-agent-roster-currentness.py # Transitional CLI delegating to the neutral agent registry
├── validate-affected-surfaces.py     # Affected-surface schema, fixture, and tracked-path coverage validation
├── validate-ci-python-contract.py    # Hashed CI lock, frozen hook revisions, history, and pre-commit contract
├── validate-document-contract-registry.py # Registry v8 schema, ArchiveEnvelope.v1, typed lifecycle/evidence and program lineage, inventory, routes, Stage 00 owners, and Current reference packs
├── validate-document-lifecycle.py    # Deterministic staged/ref/snapshot lifecycle validator
├── validate-gitops-change-set.py   # Identity-only GitOps change-set review with portable non-regular fixture coverage
├── validate-links-and-owners.py      # Full-corpus links, stage/collection indexes, authority mirrors, owners, and migration-ledger validation
├── validate-markdown-profiles.py       # Registry-driven Markdown semantics and retired-debt guard
├── validate-gitops-structure.sh      # ArgoCD root app, kustomization structure, and resource completeness validation
├── validate-github-actions-security.py # Immutable Action identity, least-privilege permission, and seven-day artifact-retention validation
├── validate-harness.sh               # Repo-static harness validation wrapper over existing gates (no live checks)
├── validate-k8s-manifests.sh         # YAML syntax and optional kube-linter validation
├── validate-policy-gates.sh          # OPA/Conftest-style policy gate with built-in fallback
├── validate-repo-quality-gates.sh    # Repository governance, workflow, docs, and inventory gates
├── validate-workspace-boundary.py    # Staged root-ignore object and isolated `_workspace` ignore validation
├── validation/
│   ├── current_executable_references.py # Current/proposal/history/sealed executable-reference owner
│   ├── registry.json                    # Validation surface, lane, command, and CI routing owner
│   └── registry.schema.json             # Closed validation routing schema
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
surface, agent-harness-semantics, roster-currentness 정본 validator를 strict
blocking mode로 호출하고 executable-reference 의미는
`validation/current_executable_references.py`에 위임한다. Registry가
role/skill/projection membership을,
semantics가 role prose와 permission parity를, provider-config가 native
metadata와 thin root gateway를 소유한다. Wrapper 내부에는 아직 별도 소유자로
이관하지 않은 Claude pre-edit/session-start/lifecycle 등록 검사와 pre-edit/
lifecycle-hook simulation, operations index, GitOps, infrastructure, CI/QA, security,
version/supply-chain처럼 정본 validator로 대체되지 않은 workspace domain
검사만 남긴다. Validation lane, result, handoff 의미는
`docs/00.agent-governance/policies/quality.md`가 소유한다.
로컬 완료 순서 `targeted -> affected -> staged -> tests -> all-files -> formatter-review -> rerun -> diff-checks`도 같은 문서가 단독으로 소유하며, 이 README는 현재 command와 inventory만 유지한다.

## Operations

### Working Procedure

1. 새 스크립트를 만들기 전에 이 README의 Tier 기준과 command-contract allowlist를 확인한다.
2. 스크립트는 한 가지 검증 책임만 가져야 하며, 반복 실행해도 결과가 달라지지 않아야 한다.
3. secret, credential, live cluster mutation, publish/deploy 동작은 이 폴더의 기본 경로에 추가하지 않는다.
4. 스크립트를 추가·삭제·리네임하면 아래 command-contract allowlist의 파일을 함께 검토한다.
5. 새 참조가 Tier A/B 보존 근거인지, Tier C 명령·문서 표면인지 분리해서 기록한다.
6. 스크립트 삭제 또는 리네임은 별도 task/plan에 연결하고, rollback 방법과
   broad reference sweep 결과를 먼저 기록한다.
7. 변경 후 [Agent Quality Standards](../docs/00.agent-governance/policies/quality.md)의 canonical eight-step completion sequence를 실행하고 각 결과를 기록한다.

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
| `validate-repo-quality-gates.sh` | Keep | Tier A: CI `repo-quality-static`와 post-edit repository quality hook이 직접 실행한다. | root README, `scripts/README.md`, PR template, `.github/README.md`, `.claude/settings.json`, docs quality guidance | 문서 구조, registry/Markdown/link 계약, stage index, active 01-05 currentness, operations/security/GitOps/infrastructure matrices, workflow·script·agent inventory를 검증한다. CI Python/Gitleaks/history 계약 self-test/production 검사를 affected-surface 검사보다 먼저 실행한다. 호출자 환경의 PATH·hint를 신뢰하지 않고 고정 system 후보 또는 passwd-home의 exact `.local/bin/gitleaks`만 보안 검증해 classifier hint로 전달한다. ACER-003 additive migration validator는 blocking이며, 전체 93-record archive cutover proof는 explicit local/manual로 유지한다. |
| `validate-gitops-structure.sh`   | Keep     | Tier A: CI `manifest-static` job이 직접 실행한다.                                                                                                                      | root README, `scripts/README.md`, PR template, `.claude/settings.json`, GitOps READMEs                                                                                                    | ArgoCD root app, root app kind, root app manifest count, root/platform/workload hierarchy boundary, GitOps kustomization structure, sibling manifest resource completeness를 검증한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `validate-harness.sh` | Keep | Tier C manual wrapper: 하네스 변경을 한 명령으로 검증하는 로컬 진입점이다. CI/hook이 직접 실행하지 않고 기존 Tier A/B 게이트를 그대로 호출한다. | root README, `scripts/README.md`, PR template, harness implementation map | `validate-repo-quality-gates.sh`, `validate-gitops-change-set.py --root . --base-ref HEAD`, `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, `check-secret-handling.sh`, `validate-vault-eso-contracts.py --self-test`와 `--root .`, `validate-policy-gates.sh`, `infrastructure/tests/verify-contracts-static.sh`, `git diff --check`를 순서대로 실행하는 repo-static wrapper다. 추가 live cluster 검사는 실행하지 않는다. |
| `validate-k8s-manifests.sh`      | Keep     | Tier A: CI `manifest-static`와 post-edit manifest hook이 직접 실행한다.                                                                                                | root README, `scripts/README.md`, PR template, `.claude/settings.json`, `docs/00.agent-governance/hooks/post-validate.sh`, GitOps READMEs                            | manifest YAML syntax와 선택적 `kube-linter` 검증을 수행한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `check-secret-handling.sh`       | Keep     | Tier A: CI `manifest-static`와 post-edit manifest hook이 직접 실행한다.                                                                                                | root README, `scripts/README.md`, PR template, `.claude/settings.json`, `docs/00.agent-governance/hooks/post-validate.sh`, GitOps READMEs                            | GitOps, infrastructure, examples manifest의 plaintext secret pattern을 검사한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `render-platform-chart-kinds.sh` | Deferred | Tier C manual review: platform Helm chart render review와 AppProject allow-list 영향 검토에서 실행한다.                                                                | `scripts/README.md`, `gitops/README.md`, 006 SDD evidence                                                                                                                                 | `gitops/apps/root`의 Helm chart Application을 `helm template --include-crds`로 렌더링하고, 렌더링된 kind가 platform AppProject allow-list에 포함되는지 확인한다. 기본 CI에서는 원격 chart fetch 변동성을 피하기 위해 실행하지 않는다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `validate-policy-gates.sh`       | Keep     | Tier A: CI `manifest-static` job이 직접 실행한다.                                                                                                                      | `.github/workflows/ci.yml`, `scripts/README.md`, `policy/conftest/kubernetes.rego`, CI/QA guide, 006 SDD evidence                                                                         | Conftest가 있으면 Rego policy bundle을 실행하고, 없으면 같은 핵심 Kubernetes/GitOps 정책을 built-in fallback으로 검증한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

#### Python Validator Inventory

The repository quality gate derives tracked script paths for Python syntax
and README coverage without a fixed script or helper census. Import-only
helpers retain their documented callers and do not become duplicate CLI or
semantic owners.

| 스크립트 | 결정 | 보존 근거 | 검증 범위 | 공개 flag와 결과 의미 |
| --- | --- | --- | --- | --- |
| `agent_registry_compat.py` | Keep | Import-only delegation shared by transitional admission, evaluation, model-fitness, and currentness CLIs. | Calls the neutral registry owner and exercises bounded registry mutations; no independent roster, fitness, or runtime authority. | No CLI; the compatibility entrypoints retain their public arguments and diagnostics. |
| `json_schema_validation.py` | Keep | Import-only mechanism shared by the agent registry and Stage99 document registry. | Embedded schema references, deterministic validation errors and typed redacted configuration/evaluation failures; no external schema retrieval. Each caller retains its policy and public diagnostic codes. | `schema_errors(schema, instance)`; no CLI or independent authority. Recovery/core regressions prove both consumers. |
| `archive_recovery.py` | Keep | Tier C ARWB-001 recovery library and explicit CLI; the focused unit test and archive validators import it, while recovery writes are confined to a new operating-system temporary path. | Requires full unambiguous SHA-1/SHA-256 Git object IDs and canonical raw paths; isolates Git config, graft, replacement, lazy-fetch, prompt, and pathspec behavior; bounds subprocesses; and translates failures to payload-free diagnostics. It validates ArchiveEnvelope.v1 and the exact WORK-107 14-field migration ledger, recovers legacy envelopes by commit/path/blob, and verifies stable payload/provenance without restoring into a repository route. | Run `python3 scripts/archive_recovery.py --root . --record <stable-record> --verify` or use `--output <new-temp-path>`. `python3 -m unittest tests/test_archive_recovery.py` proves the 27-case recovery contract. Production admission, corpus validation, historical-link resolution, and cutover remain ARWB-002/003 work. |
| `archive_validation.py` | Keep | Tier C ARWB-002 import-only validator; focused tests import immutable interfaces directly and the ARWB-003 production cutover consumes them. | Parses ArchiveEnvelope.v1 through `archive_recovery.py`, proves source bytes and provenance from full Git objects, enforces unique `original_path` authority, resolves historical links only against `source_commit` plus `original_path`, rejects current reactivation/direct individual-archive links, and binds the exact stable 93-row migration document by canonical shape and pinned SHA-256 without redundant Git reconstruction. | Import-only; it has no CLI. `python3 -m unittest tests/test_archive_validation.py` proves 44 focused cases, including bounded Git process/output budgets. Production corpus orchestration belongs to `archive_cutover.py`; this module never inspects ignored `_workspace` children. |
| `archive_cutover.py` | Keep | ARWB-003 local/manual production cutover proof with stable WORK-107 projection; it is intentionally absent from hosted/live workflows. | Preserves the immutable 31-record/202-link base proof while validating the exact stable 93-record repository, 711 historical links, 93-to-93 migration ledger, payload/source provenance, reason-dependent replacement, registry/template authority, current-authority exclusions, stable index projection, and retired-authority cleanup. Every non-null replacement is resolved through a bounded stage-zero index blob and registry-selected current authored document. Exact recovered payloads are classified with `gitleaks`; output is suppressed and diagnostics remain path-only. | Run `python3 scripts/archive_cutover.py --root .` explicitly in a full-history local worktree with `gitleaks` installed; current exit `0` reports only `records=93 historical_links=711 secret_clean=93`, while any partial state emits `ARCHIVE-CUTOVER-INCOMPLETE` plus fixed diagnostics. It does not traverse ignored `_workspace` children. |
| `archive_cutover_manifest.py` | Keep | Tier B import-only finite manifest consumed by archive cutover, active-corpus migration, document-lifecycle validation, and the focused archive-cutover regression. | Owns the immutable archive-path and registry-cutover constants shared by those callers without performing I/O or changing their failure semantics. | Import-only; it has no CLI. Existing production validators and tests remain the execution owners. |
| `validate-agent-roster-admission.py` | Transitional CLI | Delegates to the terminal agent registry through the shared compatibility module; retained only until CLI migration. | No separate snapshot, fitness, admission, or roster authority remains. | `--root .` (roster-currentness also accepts its positional root); focused tests use `tests.test_validate_agent_compatibility_clis`. PASS is repository-static only. |
| `validate-agent-evaluations.py` | Transitional CLI | Delegates to the terminal agent registry through the shared compatibility module; retained only until CLI migration. | No separate snapshot, fitness, admission, or roster authority remains. | `--root .` (roster-currentness also accepts its positional root); focused tests use `tests.test_validate_agent_compatibility_clis`. PASS is repository-static only. |
| `validate-agent-governance-ci.py` | Transitional CI contract | Validates selection, invocation, summary results, and least privilege. | Delegates focused checks without promoting local results to hosted/provider/live evidence. | `--root .` and focused CI-contract tests; ownership simplification continues under Spec 0054. |
| `validate-agent-governance-closure.py` | Transitional registry adapter | Retained root CLI delegates to the neutral registry validator. | No independent closure snapshot or generic QA-evidence record; current Spec/Plan/Task and owner gates retain their responsibilities. | `--root .`; `--self-test` exercises a bounded runtime-claim negative. Repository-static results do not prove provider/runtime/CI/live execution. |
| `validate-agent-model-fitness.py` | Transitional CLI | Delegates to the terminal agent registry through the shared compatibility module; retained only until CLI migration. | No separate snapshot, fitness, admission, or roster authority remains. | `--root .` (roster-currentness also accepts its positional root); focused tests use `tests.test_validate_agent_compatibility_clis`. PASS is repository-static only. |
| `validate-agent-harness-contract.py` | Current CLI | Validates `.agents/registry.json` and its schema. | Closed Codex/Claude support, role/skill/permission/handoff/projection integrity, safe reads, and secret-free evidence. | `--root .`; focused tests in `test_validate_agent_registry.py` and `test_validate_agent_harness_contract.py`. No runtime readiness claim. |
| `validate-agent-harness-semantics.py` | Current CLI | Validates neutral and native role semantics. | Role behavior, operative instructions, permissions, handoffs, and projection parity; native metadata retains its provider boundary. | `--root .`; focused tests in `test_validate_agent_harness_semantics.py`. No production semantics self-test or matrix fixture. |
| `validate-agent-legacy-cutover.py` | Keep | Retired-role and GitHub-hub absence, terminal-successor regularity, and current instruction consumers. | Uses Git-index candidates and bounded root-dirfd reads. Canonical document, native-registry, helper-role, and validated argv owners distinguish instructions from enforcement/test declarations; unknown text fails closed. Historical references require exact bytes and applicable terminal dispositions. Migration path fields are separate declarations; prose and free-text fields remain scanned. | `--root .`; `--self-test` is write-free. Focused regressions cover plain and rendered instructions, field-scoped migration declarations, typed retention data, symlinks, swaps, resource limits, closed Git execution, and redacted diagnostics. This is not arbitrary-code static analysis or provider/runtime/CI/live evidence. |
| `validate-agent-provider-{config,canaries,evidence}.py` | Current CLIs | Config and canaries own focused provider evidence; evidence composes them. | Codex/Claude configuration and redacted, non-transitive evidence lanes; safe-path and input validation. | `--root .`; focused tests in provider-config and provider-canaries modules. Static configuration does not prove native discovery or authenticated execution. |
| `validate-agent-loop-lifecycle.py` | Keep | Tier B Spec 043 loop lifecycle validator registered on the seven agent/governance/script/test surfaces and invoked by the aggregate after provider evidence. | Validates the four memory classes, retry/termination state contract, atomic/redacted synthetic checkpoint boundary, repository-wins resume, promotion/refresh/expiry/archive-GC/conflict, compaction, handoff, and five exact bounded reviewed feedback destinations. | `--self-test` runs the closed mutation matrix; `--root .` validates repository inputs. PASS is repo-static only: ignored `.agent-work/checkpoint.json` is neither read nor written, and no provider discovery, hook delivery, permissions, model resolution, authenticated execution, hosted CI, remote, credential-bearing, live, or actual checkpoint execution is proved. |
| `validate-agent-checkpoint.py` | Keep | Tier B Spec 043 checkpoint/memory lifecycle validator registered on the same seven surfaces; its aggregate self-test owns production-fixture validation before mutations. | Validates atomic/redacted synthetic checkpoint schema, repository-wins resume, all four authority-bounded memory classes, promotion/refresh/expiry/archive-GC/conflict, compaction, and handoff. | `--root . --self-test` is the canonical aggregate invocation. PASS is repo-static only; it does not read or write ignored `.agent-work/checkpoint.json` or establish provider/runtime/CI/remote/live checkpoint execution. |
| `validate-workspace-boundary.py` | Keep | Tier B ARWB-004 validator invoked by `validate-repo-quality-gates.sh` in self-test and production modes; CI workflow wiring remains unchanged. | Requires exactly one stage-zero `100644` `_workspace/README.md`, rejecting extra or force-added members, conflicts, executable mode, symlink, gitlink, nonregular, or malformed index records. The root `.gitignore` must also be one stage-zero `100644` index entry with a full SHA-1/SHA-256 blob ID. Production performs four bounded actual-repository Git queries: workspace and root-ignore `ls-files --stage -z`, then `cat-file -s` and `cat-file blob` for the immutable root-ignore OID. The size is capped before the exact blob is retrieved. Only that blob is written to an isolated temporary Git context; `check-ignore --no-index` queries for the literal probe and README paths run there, never against the actual worktree. All Git uses fixed absolute Git, closed config/environment, `shell=False`, suppressed diagnostics, and a timeout. The validator never lists, walks, globs, stats, opens, reads, or hashes actual `_workspace` children and never opens the worktree root `.gitignore`; failures contain only a stable code and validated path. | `--self-test` runs isolated repositories, hostile ignored-child policies, SHA-1/SHA-256 and blob-bound injections, malformed/stage/ignore cases, and actual-path traversal/open sentinels while permitting isolated policy evaluation. `--root .` performs the production index/object proof and isolated ignore evaluation. Exit `0` emits one PASS line; exit `1` emits one stable path-only diagnostic. |
| `run-validation-lane.py` | Keep | Tier B Spec 031 local consumer used by shared post-edit and lifecycle hooks | Imports validation-surface schema v2, consumes NUL path records, selects `affected`, `staged`, or `all-files` validator IDs, and invokes only approved argv arrays with `shell=False`. The staged mode selects contract validators for the exact staged path set; it does not replace plain `pre-commit run` against the exact Git index. Every validator runs with a closed environment, fixed absolute trusted PATH, and absolute resolved interpreter; ambient shell/Python/Node startup variables and ambient Gitleaks hints are absent. It enumerates only exact fixed-system candidates or the current effective-passwd-home `.local/bin/gitleaks`, rejects symlink/writable/unowned/repository/`/tmp` candidates, requires effective owner/group/other execute permission on the file and traversal permission on every required directory, handles root semantics explicitly, and passes one absolute hint without adding its directory to PATH. Repository quality requires return code zero and exactly one `[PASS] repository quality gates passed` stdout line. Existing affected Markdown propagates through repeated `--include-path`; no paths and missing optional tools retain their bounded `SKIP`/fallback semantics. Child stdout/stderr never enters the result; byte counts and SHA-256 digests provide bounded non-secret metadata. | `--root`, `--lane affected\|staged\|all-files`, `--paths-file`, required `--delimiter nul`; stable `PASS`/`SKIP`/`FAIL`/`DEFER` lines include absolute command/tool, scope, limitation, and evidence class. The all-files runner is supplemental and does not replace `pre-commit run --all-files`; exit `1` means a contract, marker, selection, required-tool, or command failure. |
| `select-affected-surfaces.py` | Keep | Tier B Spec 031 selector consumed by local/CI integrations in later ASQA units | NUL-terminated UTF-8 path records, exact-one surface selection, lane-filtered validated argv IDs, maximum protection level, and sorted CI job output. Only absent unmatched inputs may use complete canonical Migration proof to select the current terminal surface; existing paths and pure contract/argv queries never use recovery. Original inputs and lane remain unchanged. It never invokes a shell or accepts newline-delimited machine input. | `--root`, `--lane affected\|staged\|all-files\|ci`, `--paths-file`, required `--delimiter nul`, `--format json\|github-output`; exit `0` emits stable sorted output, exit `1` reports a stable contract/path rule ID. |
| `validate-affected-surfaces.py` | Keep | Tier A affected-surface contract gate introduced by Spec 031 | Draft 2020-12 schema, duplicate-key-rejecting schema/contract/fixture decoding, closed semantic references, exact three-validator affected Markdown path-input ownership, twenty-two registered validators, and exact closure-validator ownership on the twelve existing agent-governance surfaces. It also enforces shell-metacharacter-free argv arrays, exact case-sensitive direct-script executable tokens (`bash`, `python3`, `node`) with no path prefix, normalized script operands, fail-closed exact/combined/assignment interpreter-eval options, wrapper rejection, mandatory surface fallbacks, positive/negative/mutation fixtures, NUL-based `git ls-files` coverage, and a temporary Git proof that `--no-renames --name-only -z` preserves both sides of a rename. Existing path nodes are inspected with `lstat` without traversal: production inventory requires a present regular file or one of the exact six shared-content symlinks with its canonical relative target, while missing synthetic proposal paths remain selectable. Interpreter options are examined only before the script operand or `--`; identically named script arguments after the operand remain data. | `--root`, `--self-test`; self-test reports `surfaces=22 mutation_cases=38`, while production reports `validators=22`; `PASS`/exit `0` means all tracked paths have exactly one surface and the fixture contract passes, while `FAIL`/exit `1` names the stable rule ID. |
| `validate-ci-python-contract.py` | Keep | Tier A Spec 039 contract gate invoked by `validate-repo-quality-gates.sh` before affected-surface validation. | Rejects lexical-root escape, every symlink or non-directory root/parent component, and every symlink or non-regular final owner before reading the exact three-line `.github/requirements/ci-validation.in` owner, its fully resolved `.txt` lock, the technology-inventory mirror, the CI workflow, or `.pre-commit-config.yaml`. Root, parent, and final files are descriptor-bound with `lstat(dir_fd)` plus no-follow `open`/`fstat` identity comparison, and final regular-file opens are nonblocking. Every one of the sixteen Linux/CPython 3.12 packages must use `==` and one or more lowercase SHA-256 hashes; the lock digest and package count must match the inventory. All four validation jobs require the exact binary-only/hash-required install command. A bounded fail-closed shell guard joins backslash-newline continuations, preserves comments, quotes, control operators, reserved-command boundaries, subshells, and command substitutions, then unwraps `env`, `sudo`, `command`, `time`, `nohup`, `exec`, and `!`. Direct pip and `python -m pip` share an exact parser for every current valued, valueless, alias, and short global-option class; separate and equals values are consumed exactly, while dynamic values and unknown or ambiguous globals fail closed. The guard rejects additional Python/Python N/Python N.M module installs and direct pip/pip N/pip N.M installs through quoted, bare, absolute, or relative launchers; recursively checks bounded static `sh`/`bash`/`dash`/`zsh`/`ksh -c` and command-substitution payloads; rejects normalized quoted or wrapper-prefixed eval/source/dot/alias/coproc/builtin forms; and unconditionally rejects every executable outside the explicit current safe-command set, including every `xargs` form. Tar command delegates (`--to-command`, compression programs, checkpoint actions, remote/info scripts, `-I`, `-F`, and old-style equivalents), coreutils install strip-program execution, and Git cat-file/diff external diff, textconv, and filter options are command-specifically rejected for their full, equals, and subcommand-accepted abbreviated long-option spellings after quote, wrapper, and inline assignment normalization. Git option scanning ends at exact `--`; exact safe `diff --text`, negated options, operands after the terminator, and ambiguous or invalid shorter prefixes are not classified as execution boundaries. Parser errors, recursion/input overflow, shell stdin, functions, heredoc, process substitution, arrays, and multiline quoting fail closed independently of payload spelling. Comments and exact `echo`/`printf`/`grep` or near-basename controls such as `mypython`/`pipx` remain non-executing controls whose arguments are not reinterpreted. Jobs outside the exact owners may not take over Python setup or any such install. Every non-local pre-commit repo must use its exact unique 40-character frozen commit and retain one exact anchored source-tag line inside its own repo stanza; moved comments or unrelated blocks cannot satisfy provenance. The local repo is the sole rev-exempt entry. The validator also preserves the explicit all-files/show-diff, verified Gitleaks, and history contracts. Parsing is local, duplicate-safe, and network-free. | `--self-test`, `--root`; exit `0` reports the validated job/direct-pin counts, while exit `1` emits one of thirteen stable `CI-*` rule IDs, including `CI-PYTHON-LOCK`, `CI-PRECOMMIT-REV`, and the value-free `CI-PYTHON-INPUT` root boundary. The self-test contains thirty-three cases, including wrapper, control/substitution, continuation, nested-shell, dynamic-indirection, absolute-path, versioned-launcher, and direct-pip bypass mutations. The `.in` file owns direct versions; the `.txt` file is the Linux/CPython 3.12 resolved lock, and the technology inventory owns its exact digest and frozen-hook mapping. |
| `validate-document-contract-registry.py` | Current document gate | Validates the Stage 99 registry and exact-one profile routing. | Schema, path, identity, lifecycle, template, and current-authority consistency; named untracked inputs are explicit and safe-path checked. Agent role authority belongs separately to `.agents/registry.json`. | `--root`, strict mode, optional profile/include paths, and focused contract tests. No retired provider admission branch. |
| `validate-document-lifecycle.py` | Keep | Registry-owned lifecycle state and evidence gate | Compares duplicate-safe registry and document blobs from the staged index or explicit commits. It validates retained authored profile/status/edge changes and reciprocal transition evidence. Same-status body maintenance, classification-only Reference creation, frontmatter-free package/pack router creation, and reviewed deletion are not lifecycle events; Markdown/profile checks own proposed content, link/owner checks own consumer-zero, and Git owns ordinary recovery. Archive-specific validation separately protects sealed payload bytes and rejects unproved Archive creation. Inputs remain bounded, inherited Git steering is removed, includes are additive, and snapshot mode reports `DEFER` rather than claiming transition history. | `--root`, `--mode staged\|ci\|explicit-ref\|snapshot`, mode-specific refs, or repeatable `--include-path`; exit `0` is clean (or snapshot `DEFER`), `1` is a lifecycle/evidence violation, and `2` is an invocation/ref/provenance failure. |
| `validate-gitops-change-set.py` | Keep | Tier A PSH-004 gate consumed by `manifest-static` and the repository quality gate | Exact `kustomize.config.k8s.io/v1beta1` Kustomization `resources` graphs are reduced to immutable `(apiVersion, kind, namespace, name)` identities. Every serialized identity/path token is ASCII grammar-checked before output; paths are safe repository-relative evidence only, so a path-only move is one `RETAIN`. Unsupported dialects/directives, remote or unsafe paths, symlinks, non-regular entries, cycles, duplicate YAML keys/identities, malformed tokens, and unavailable Git parents fail closed with value-free diagnostics. | `--self-test` runs the exact fixture, portable FIFO-or-directory non-regular boundary, durable negative renderer, and temporary Git-history/shallow-clone cases; or use `--root` with `--base-ref`. `--base-ref HEAD` is the local static comparison. Forty-zero uses the first HEAD parent only when that object is available, returns the empty graph only for a true root, and otherwise fails. Exit `0` emits only `ADD\|DELETE\|RETAIN apiVersion kind namespace/name path`. |
| `validate-github-actions-security.py` | Keep | Tier A PSH-003 security gate; self-test and repository modes are both required repository-quality aggregate evidence. | Duplicate-key-rejecting YAML, non-erasing typed `uses` parser/source parity, immutable remote SHA and Docker digest references, same-line human version comments, fail-closed non-symlink repository/workflow/zizmor inputs, explicit top-level `contents: read`, mandatory exact three-job write consumers, default-deny writes, `write-all` rejection, `unpinned-uses` suppression rejection, and integer-only seven-day retention on every `actions/upload-artifact` step. | `--self-test`, `--root`; self-test `PASS` preserves the exact eleven primary, ten repository-boundary, twenty-one required-write, and four artifact-retention JSON cases, plus five internal uses-shape, one boolean-retention, four malformed artifact-structure, and one mixed-case artifact-owner cases. Repository `PASS` enforces immutable Action identities, least-privilege permissions, and transient seven-day artifact retention; either mode failing blocks the aggregate gate. |
| `validate-vault-eso-contracts.py` | Keep | Tier A PSH-005 gate consumed by `manifest-static`, the affected-surface registry, local harness, and repository quality gate. | Reads only the fixed Vault store, TokenReview binding, external Service/EndpointSlice, verify-only HCL, and bootstrap inputs. It enforces local-only HTTP annotations, exact ESO identity/audience, one TokenReview subject, the six-path read/list policy, HTTPS plus readable CA, `/dev/tty` token input, stdin header/secret flow, and no insecure or noninteractive fallback. | `--self-test` runs the exact ten-case non-secret fixture; `--root` performs repository-static validation. Exit `0` prints a fixed PASS line, exit `1` emits only fixed path/diagnostic text, and exit `2` is a configuration or CLI failure. |
| `validate-markdown-profiles.py` | Keep | Tier B semantic document gate; Spec 029 SMDV-004 invokes it through the repository orchestrator. | Registry-selected Frontmatter keyset/order and v8 scalar kind, constant, enum, pattern, nullability, conditional, date, owner, title, placeholder, and ArchiveEnvelope.v1 form semantics. The gate also owns H1/H2, fence, residue, append-fragment, native/generated structural N/A, and imported README handoff semantics. A bounded Git-index inventory retains GitHub issue/workflow ownership, derives OpenAPI/GraphQL/protobuf ownership from the registry's typed native role, and rejects only an exact leading parsed five-key `sdlc/*` envelope. Its closed native fixture is 5 positive plus 5 negative cases (`10/10`); legal YAML document markers, non-SDLC multi-document mappings, and GraphQL/protobuf comment lookalikes remain controls. The finite Spec-033-owned `template-compatibility.json` is a no-growth retirement guard and contains no active debt admission. | `--root`, optional `--mode strict` (the default), `--format text\|json`, repeatable `--include-path`, mutually exclusive `--self-test`/`--inventory`; exit `0` is strict-clean, `1` is a document, native-envelope, or baseline-admission violation, and `2` is configuration or CLI failure, including a retired compatibility value. |
| `validate-links-and-owners.py` | Keep | Tier B cross-document semantic gate; Spec 029 SMDV-004 invokes it through the repository orchestrator. | All registry `current_paths` links; the three stage indexes; three Git-index-derived collection tree/table mirrors; reciprocal Stage 00 current-authority and Current reference-pack pointer/member/lifecycle mirrors; deterministic current-owner keys; the exact fourteen-column Spec 030 migration ledger; and typed registry-v8 program lineage. One root/blockquote-aware block view masks comments, fences, raw HTML, and indented code before both heading evidence and links are interpreted. Raw/fence opacity is applied in a prepass; list/blockquote ownership and lazy-continuation provenance are then resolved before final per-container indented/Setext masking, so outer opaque state remains authoritative without hiding owned list paragraphs. Rendered lines retain container identity and depth: every root/quote, quote/root, quote-depth, sibling-segment, or list-item transition inserts a hard inline-token boundary for labels, destinations, and full-reference identifiers, while a soft break inside one container remains renderable. Ordered and unordered markers use their marker width and CommonMark one-to-four-space padding to determine continuation indentation; five or more spaces use one padding space and preserve the remainder as content. An empty marker line always uses marker width plus one regardless of trailing whitespace, while same-line content retains the one-to-four versus five-or-more distinction. Marker and continuation tabs advance to four-column stops, preserving overshoot as content indentation. Each stripped list item is rendered again, propagating nested list, fence, raw-HTML, indented-code, and table opacity while retaining normal list paragraph links. An active list or blockquote paragraph carries a non-block unmarked lazy continuation in the same container; blank, fence, raw, heading, thematic, blockquote, and list-sibling lines remain boundaries, while indentation cannot start code until the paragraph closes. The link scanner supports balanced, escaped, and angle-bracket destinations; treats only CR, LF, and CRLF as line endings; rejects U+0020 and ASCII controls in bare destinations while retaining non-ASCII spaces as destination or title content; permits only space/tab plus at most one line ending as a component separator; rejects whitespace before nested bare-destination parentheses close; rejects unescaped `<` inside angle brackets; unescapes only CommonMark ASCII punctuation; requires an empty remainder or one valid single-, double-, or parenthesized-title remainder; rejects an unescaped nested `(` in parenthesized inline and definition titles; and resolves only definitions whose destination and optional title parse completely, including destination and title continuations at zero through four visual columns or one tab, blank-free multiline titles, and full/collapsed/shortcut references. Definition labels use an escape-aware closing-bracket scan across nonblank soft line endings, so `\\]` remains label content instead of terminating the definition; whitespace-normalized multiline labels retain their raw line endings in the 999-code-point cap and complete definition source span. Definition collection tracks rendered paragraph state: a definition-looking line cannot interrupt an ordinary paragraph, while blank and rendered block boundaries preserve admission. ATX/thematic leaf blocks close definition paragraph state, and Setext does so only with eligible preceding content, so a following valid definition is admitted before immediate indented-code masking. A complete valid definition is a nonparagraph block for subsequent Setext and indented-code admission. The same complete definition spans drive container-local paragraph state: a valid quoted/list definition closes lazy admission, whereas an invalid definition-looking line remains paragraph text. Each lazy append re-evaluates the accumulated owned lines, so a newly completed multiline definition closes admission without reclassifying lazy delimiter lookalikes as explicit Setext. Lazy-line provenance is retained on rendered container lines and the joined rendered view, so later definition-span scans cannot promote an unmarked delimiter after provenance-bearing lines are recomposed. Explicitly marked quote/list continuation uses explicit state instead: a Setext delimiter can close the paragraph, while normal marked content keeps it open. A normalized reference label must contain a non-whitespace character before it can register or resolve; its raw bracket content is capped at 999 Unicode code points before case-folding or whitespace collapse, including line endings and escape source characters. Space-, tab-, and soft-break-only or 1000-plus labels remain plain text across definition, shortcut, full, collapsed, and failed-inline fallback paths. Inline destinations are parsed contextually through the optional title and actual outer closer instead of using generic parenthesis pairs, so `)` inside a quoted title and `)(` inside an angle destination remain content. A failed inline candidate may fall back to a matching shortcut reference; its invalid `(...)` suffix remains literal and unconsumed. List items, ATX/setext headings, thematic breaks, and GFM table rows/cells introduce hard inline boundaries while ordinary same-paragraph soft breaks remain valid. ATX and thematic leaf blocks admit an immediately following indented code block. A Setext delimiter does so only when it closes an eligible preceding paragraph in the same container; standalone `=+` or one/two-hyphen lookalikes remain paragraph content, while standalone `---` remains thematic. Closing-token-order state resolves all candidates before suppressing nested links: only a successfully resolved image suppresses candidates in its alt subtree, unresolved image openers leave their internal links eligible, an outer link containing an image remains valid, and independent inline/full/collapsed/shortcut links may follow unresolved or escaped literal brackets; only consumed reference suffixes remain suppressed. Nested-link filtering propagates resolved-image and source-consumed eligibility down the paired-bracket tree and candidate-bearing subtree state back up in linear work; hard-boundary positions are indexed once, labels are materialized only for surviving links, and output remains in source order. Every successfully consumed inline link/image destination and title is a non-candidate source span; each complete valid definition is likewise masked across its exact first and continuation lines, while an invalid definition remains rendered text. A complete definition followed by ordinary four-space content still closes before that indented-code line; four-column content is absorbed only while destination/title grammar is incomplete. A malformed title on the destination line invalidates the definition, while a malformed title-looking next line after a complete destination is left rendered and does not discard that definition. Synthetic inline hard boundaries are added only after complete definition spans and open-paragraph continuations are mapped per root, quote, or list container, so Setext/thematic-looking definition continuations stay owned, definition lookalikes inside ordinary paragraphs are not promoted, and real post-definition delimiters remain boundaries. Link destinations decode only unescaped numeric/named CommonMark character references before percent decoding and POSIX path normalization. Local-path classification consumes that exact parsed target without generic Unicode trimming, so leading or trailing NBSP, EM SPACE, IDEOGRAPHIC SPACE, or controls cannot collapse onto a canonical owner. Rendered lifecycle cells collapse links, remove valid inline HTML markup and attributes while retaining visible child text, and decode character references outside code spans and backslash escapes before NFKC/case normalization; escaped ampersands and invalid references stay literal. Complete valid inline suffixes use one monotonic left-to-right token/stack pass: completed definitions and HTML are consumed when reached, a code opener consumes through its next equal-length closer, and only a then-active bracket opener may atomically commit a suffix; no candidate may use its own delimiter to change opener visibility, no global fixed point is used, and orphan `](` suffixes own nothing. Complete reference-definition destination/title spans and quote-aware inline HTML tokens likewise claim their source before code pairing; two sorted interval sweeps preserve same-endpoint, nesting, and partial-overlap semantics while keeping HTML inside a destination as link syntax and a link-like suffix inside HTML as attribute content, and backticks inside the winning spans cannot participate; outside code odd backslash parity escapes an opener and even parity does not, an escaped adjacent run can open code only from its unescaped tail, and an already-open span closes on the next equal-length raw run regardless of a backslash inside the span. A source-order-preserving sorted two-pointer overlap sweep excludes HTML candidates intersecting the resulting non-overlapping code spans in near-linear time while treating touching endpoints as disjoint; overlapped candidates remain literal, owned angle destinations remain link grammar, and only remaining valid CommonMark opening/closing tag tokens—including quoted, unquoted, and multiline attributes—become non-whitespace opaque identities before link scanning. A reversible side-channel intern registry maps each distinct HTML token to a unique base-6399 unprefixed BMP private-use sequence of the same source length, while every raw BMP private-use character is injectively escaped under a reserved `E000` prefix; encoded-to-source offsets restore original lifecycle-cell labels; opaque token starts are indexed once and each label uses a measured binary interval lookup that inspects only intersecting tokens; reference-label normalization rehydrates structured token source only for CommonMark whitespace normalization and Unicode case folding, so case-equivalent markup matches while raw text and different canonical tags or attributes stay distinct across shortcut, collapsed, and full references; visible Markdown between tags remains active, while escaped or invalid openers remain Markdown text. Line-start valid comments are block-opaque through the first closing `-->` line, including trailing Markdown and the overlapping opener/closer form; HTML comment, processing-instruction, declaration, and CDATA blocks close root/quote/list paragraph state before lazy or code admission; inline comments instead use strict escape-aware grammar, preserving invalid internal `--`. Inline HTML tokens cannot cross a blank paragraph boundary. Type-7 HTML blocks use the same quote-aware valid-tag grammar so quoted `>` remains attribute content and invalid attributes do not create opacity. These spans prevent bracket-looking destination, title, or HTML-attribute content from becoming a shortcut reference. Lifecycle-cell normalization scans a code-masked offset-stable view for syntax, then restores each display label from the original offsets, so a code-formatted label inside a real link normalizes while a code-wrapped link lookalike does not become authority evidence. Unmatched inline openers are memoized to prevent repeated suffix scans. After valid link syntax and HTML ownership is removed, one ownership cursor advances across every paragraph/container segment while equal-length backtick runs are paired in near-linear time: odd backslash parity suppresses only an outside-code opener, even parity keeps it active, and an already-open span accepts a backslash-prefixed closer. Brackets inside paired spans are excluded before link pairing, unmatched openers cannot mask a later paragraph, and same-container soft-break code spans remain intact. Invalid destination/title and invalid HTML-looking text own no source, so their backticks keep normal code-span semantics. Program checks compare relation state with Spec frontmatter, enforce rendered reciprocal links, admit only the exact ADR-0017/Spec-033 successor record, build current Plan/Task incoming and undirected adjacency once, cache each connected component and safe Spec-seed result, and close only the component reachable from each relation Spec: the first original tranche not done or archived may have no component before planning or exactly one reciprocal direct-Spec pair with relation-state parity after planning begins, every remaining original tranche and follow-up has no component, and all active execution components must be seeded by one registry relation Spec, while disconnected draft-only components remain outside current execution ownership. Authority detection finds family/transition columns by normalized header name, accepts optional-colon/pipe GFM delimiter cells with one or more hyphens, rejects header/delimiter/row lines carrying lazy-continuation provenance, preserves every transition per family, permits wrapper columns, and recognizes reference/inline wrappers while excluding non-rendered tables. The self-test verifies 345 lineage cases, including independent valid-link/HTML containment, code-wrapped HTML/code overlap, deeply nested bracket-tree suppression and blank-separated owned-backtick paragraph sweeps at 2k, 4k, and 8k, plus execution-component chains at 500, 1k, 2k, and 4k and opaque-label/token sweeps at 2k, 4k, and 8k with exact results, monotonic ownership, malformed/image controls, endpoint/source-order controls, cached-result identity, CommonMark ASCII-control versus Unicode-space character predicates, exact Unicode-space local-path and reciprocal/execution false-evidence negatives, indexed opaque-label work bounds, and linear work-count bounds, ordered diagnostic counts, and one exact stable tuple projection, and caps both the 20k unmatched-bracket scan and the 500 unique unmatched-backtick-run scan below two seconds. It reads no network or secret content and does not dereference provider symlink adapters. | `--root`, optional `--mode strict` (the default), `--format text\|json`, repeatable `--include-path`, mutually exclusive `--self-test`/`--inventory`; JSON inventory returns the exact ordered registry population. Exit `0` is strict-clean, `1` is a document violation, and `2` is configuration or CLI failure, including a retired compatibility value. |

ACER-006의 terminal frontier 관측 범위는 동결된 PRD-0006의 Spec 038–040
Plan/Task 세 family로 제한한다. 이후 프로그램의 Stage 04 문서는 이 역사적
residue validator에 재편입하지 않으며, 현재 프로그램 관계와 실행 쌍의
유효성은 document registry, cross-document, lifecycle validator가 소유한다.
내부 terminal shape 검사는 여전히 관측 범위에 주입된 rogue active row를
fail-closed로 거부한다.

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
| `render-platform-chart-kinds.sh` | development-helper/reusable  | No        | No        | Tier C manual review helper이며 platform Helm chart render 결과와 AppProject allow-list coverage를 재현 가능하게 검토한다.                            |
| `validate-policy-gates.sh`       | operations-critical/reusable | No        | No        | Tier A manifest-static policy helper이며 Conftest/Rego bundle 또는 built-in fallback으로 GitOps policy gates를 검증한다.                              |

2026-06-04 broad reference sweep 기준 unused 또는 one-off 삭제 후보는 없다. `render-platform-chart-kinds.sh`는 Tier C manual helper이므로 기본 local/remote QA gate에는 포함하지 않지만, platform Helm chart Application이나 AppProject allow-list 변경 시 유지되는 재현 명령이다.

### 통합하지 않는 기준

스크립트 통합은 같은 trigger, 같은 scan domain, 같은 failure semantics, 별도 command contract 없음이라는 네 조건을 모두 만족할 때만 검토한다.
현재 스크립트는 repository governance, GitOps structure, Kubernetes manifest syntax, plaintext secret scan처럼 서로 다른 실패 의미와 명령 계약을 가진다.
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
| `.github/README.md`                                         | GitHub governance routing 표면                                 |
| `.claude/settings.json`                                     | Claude command allowlist 표면                                  |
| `.claude/CLAUDE.md`                                         | repository runtime baseline의 generated-script ownership 참조  |
| `docs/00.agent-governance/hooks/post-validate.sh`           | post-edit validation 실행 표면                                 |
| `docs/00.agent-governance/hooks/lifecycle-guard.sh`         | Stop/SubagentStop/PreCompact lifecycle validation 실행 표면    |
| `docs/90.references/README.md`                              | references index와 generated-index maintenance note            |
| `gitops/README.md`                                          | GitOps validation command 표면                                 |
| `gitops/workloads/README.md`                                | workload validation command 표면                               |
| `docs/README.md`                                            | docs quality gate command 표면                                 |
| `docs/00.agent-governance/policies/document-authoring.md`  | active generated-index routing contract                        |

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
suppression fail closed. Every `actions/upload-artifact` step must set an
integer `retention-days: 7`; missing, quoted, boolean, and other values fail
closed. The changelog artifact is transient review evidence, not publication.
Only the upload-artifact owner/repository prefix is case-folded for retention
matching, so GitHub-equivalent owner/repository case variants cannot bypass the
rule; raw `uses` validation remains unchanged.
Malformed `jobs`, job, present `steps`, and step-list-member shapes fail with
stable diagnostics before malformed structure can crash validation or bypass
artifact retention.

```bash
python3 scripts/validate-github-actions-security.py --self-test
python3 scripts/validate-github-actions-security.py --root .
```

During PSH-002 the first command is GREEN and the second is intentionally RED
with fourteen mutable references, three missing workflow defaults, and one
suppression. Repository-quality-gate integration waits for PSH-003; this
bounded RED state is not a gate bypass or remote/runtime evidence.

shared role semantics는 공통 계약에 surface-owned model, tool,
reasoning-effort 값을 복제하지 않고 responsibility, output, prohibition,
stop, handoff, capability tier, required evidence만 소유한다. 검증기는
Markdown adapter의 YAML frontmatter와 본문, Codex adapter의 TOML
`developer_instructions`를 surface-specific 형식으로 읽는다. YAML은 duplicate
key, non-mapping frontmatter, non-scalar `name`을 fail-closed로 거부한다.
Semantic matching은 fenced code, HTML comment, strikethrough, revoked 또는
contradictory line을 제외한 operative Markdown에서 whitespace만 정규화한다.

현재 역할·권한·handoff·skill·projection 경로의 machine authority는
`.agents/registry.json`이며 harness-contract CLI는 해당 registry를 검증한다.
Context와 memory 규칙은 [Context and Memory Policy](../docs/00.agent-governance/policies/context-and-memory.md)가
단독으로 소유한다.

```bash
python3 scripts/validate-agent-harness-contract.py --self-test
python3 scripts/validate-agent-harness-contract.py --root .
```

Registry checks derive roles, permissions, skills, and projections from
`.agents/registry.json`. They do not preserve a separate harness snapshot,
fixed roster census, or provider-runtime claim. Codex runs explicit validation;
Claude native settings may invoke shared hooks when actually loaded.

Agent validation uses the neutral registry and Codex/Claude projections:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .
python3 scripts/validate-agent-provider-evidence.py --root .
python3 -m unittest tests.test_validate_agent_registry tests.test_validate_agent_harness_contract tests.test_validate_agent_harness_semantics tests.test_validate_agent_compatibility_clis
```

The registry owns exact roles, permissions, tiers, handoffs, skills, and
projection paths. Provider configuration owns native metadata; each result
retains its evidence class. Unsupported custom hook graphs and separate
snapshot/census fixtures are not current authority. The admission, evaluation,
model-fitness, and roster-currentness CLI names are temporary adapters to the
registry until their approved CLI retirement; they no longer own independent
readiness matrices. The semantics CLI has no production self-test; focused
tests exercise its bounded mutations.

document contract registry 명령은 다음 다섯 flag 표면을 제공한다.

```bash
python3 scripts/validate-document-contract-registry.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict --profile test/sample --include-path tests/fixtures/document-contracts/candidate.md
python3 scripts/validate-document-contract-registry.py --root . --self-test
```

`--root`, optional `--mode strict`, `--profile`, repeatable `--include-path`,
`--self-test`만 공개 flag로 사용한다. 모드를 생략해도 strict이며 퇴역한
compatibility 값은 argparse exit `2`로 거부한다. 기본 inventory는 strict Git
index에서 얻은 tracked file만 포함하고 filesystem walk나 broad
untracked discovery를 하지 않는다. 명시한 `--include-path`만 POSIX 상대 경로,
ignore 상태, symlink-free `lstat()`, regular Markdown target 순으로 검사해
추가한다. 모든 route 검사 전에 `Draft202012Validator` 기반 `jsonschema`
preflight를 수행한다. `PASS`와 exit `0`은 선택 scope가 schema, inventory,
exactly-one classification을 통과했다는 뜻이며, `FAIL`과 non-zero exit는 rule
ID 또는 입력 경계 위반을 뜻한다. Repository 실행은 classification 성공/실패
모두 `baseline=<n> new=<n> uncovered=<n> ambiguous=<n>` 요약을 출력하며,
baseline inventory 실측값이 `433`이 아니면 classification 전에 실패한다.
`--self-test` PASS는 production
`validate_registry()`와 `classify_paths()`를 사용하는 mutation 119개,
complete closed-v8 typed projection, 64-profile/30-template inventory,
root/nested duplicate-key와 noncanonical archive-envelope probe, private
generic conditional-value 및 v5/v6 migration fixture, README와 route probe가
모두 기대 rule-ID와 projection에 일치했다는 뜻이다.
이 명령은 repository-static이며 live
cluster나 remote provider readiness를 입증하지 않는다.

Document lifecycle validator는 다음 명시적 base 표면만 제공한다.

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-document-lifecycle.py --root . --mode ci --base-ref origin/main --to-ref HEAD
python3 scripts/validate-document-lifecycle.py --root . --mode explicit-ref --from-ref HEAD^ --to-ref HEAD
python3 scripts/validate-document-lifecycle.py --root . --mode snapshot
python3 scripts/validate-document-lifecycle.py --root . --self-test
```

`staged`는 worktree가 아니라 `HEAD:path`와 `:path`를 비교하고, `ci`는
명시한 두 commit의 유일한 merge base를 계산한다. `explicit-ref`는 명시한
두 direct commit object만 사용하며 환경변수로 ref를 추론하거나 annotated
tag를 암시적으로 peel하지 않는다. Raw tree/blob/annotated tag는 exit `2`로
닫히고 commit을 직접 가리키는 lightweight tag만 통과한다. 모든 inherited
`GIT_*` 값은 subprocess와 imported registry/inventory 호출에서 제거되고,
고정된 noninteractive 환경과 config가 replacement, graft, external diff,
text conversion, hook, fsmonitor steering을 차단한다. 요청 root가 정확한
non-bare worktree인지도 각 평가에서 다시 확인한다. 모든 diff는
`--ignore-submodules=none`을 강제하여 local config 또는 tracked
`.gitmodules`의 `ignore=all`이 governed Markdown gitlink 변경을 숨기지
못하게 하며, regular blob이 아닌 결과는 exit `2`로 닫힌다. `snapshot`은 현재
profile/status를 검사하되 transition history에 정확히 한 개의
`LIFECYCLE-BASE-DEFER`를 출력하고 PASS를 출력하지 않는다. 모든 ref와
include path는 fail-closed이며, additive include는 다른 changed document의
위반을 필터링하지 않는다. exit `1`은 lifecycle 위반, exit `2`는 argument,
ref, merge-base, repository identity, blob provenance 오류다. `--self-test`의
124개 사례는 42개 production edge와 governed/unclassified A/D/M/R, Git
환경·root·ref·submodule 경계, 모든 nested fixture shape와 closure mutation
13개를 포함한다. Base mode와 admission operation에는 문자열 membership
검사 전에 타입 검증을 적용하여 list/dict 같은 unhashable 값도 고정 실패한다.

Markdown profile validator는 `--self-test`, `--root`, optional
`--mode strict`, `--format text|json`, repeatable `--include-path`,
`--inventory`를 제공한다. 모드를 생략해도 strict이며 퇴역한 compatibility
값은 argparse exit `2`로 거부한다. Text와 JSON은 같은
`(path, profile, ruleId, debtToken)` 정렬을 사용하고 모든 진단을
`FAIL`로 처리한다. Spec-033 소유 `template-compatibility.json`은
`compatibilityDebt`와 `semanticDebtCaps`의 재도입을 막는 finite no-growth
retirement guard로만 남는다. 새 path/rule/token, 퇴역 필드 재도입, 비정상
fixture는 통과하지 않는다. 이 명령은 tracked repository content만 읽으며
외부 URL, live cluster, provider runtime readiness를 검증하지 않는다.

| Command                                           | Argument Contract                                                                      | Scan / Validation Scope                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Result Semantics                                                                                                                                                                                   |
| ------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/validate-repo-quality-gates.sh .` | 선택 인자는 repository root다. | 문서 taxonomy, registry-selected README/템플릿, 01-05 stage/currentness, operations/security/GitOps/infrastructure, workflow·script·agent inventory를 검증한다. Full-history와 `gitleaks`가 필요한 ARWB-003 cutover는 포함하지 않는다. | `PASS`는 repository governance gate 통과를 뜻하고, `ERR`는 계약 drift를 뜻한다. |
| `python3 scripts/archive_cutover.py --root .` | `--root`는 exact repository worktree root다. | immutable base proof와 exact WORK-107 93-to-93 stable migration ledger를 결합해 93 ArchiveEnvelope.v1 records, 711 historical links, source provenance/digest, dual recovery, replacement authority, registry/template, stable index membership을 원자적으로 검증한다. | exit `0`은 aggregate `records=93 historical_links=711 secret_clean=93`만 출력한다. 실패는 `ARCHIVE-CUTOVER-INCOMPLETE`와 fixed path-only diagnostics를 출력하며 payload/secret match를 노출하지 않는다. |
| `python3 scripts/validate-agent-harness-contract.py --self-test`; `python3 scripts/validate-agent-harness-contract.py --root .` | 첫 command는 bounded negative fixture이고, 둘째는 exact repository root와 terminal registry를 사용한다. | Codex/Claude만 허용하는 registry graph, permission boundary, registry-declared projection routing, sensitive-content exclusion을 검증한다. | exit `0`은 repo-static registry contract PASS다. Exit `1`은 contract finding, exit `2`는 CLI/input boundary failure이며 provider-runtime/CI/remote/live evidence를 뜻하지 않는다. |
| `python3 scripts/validate-agent-roster-admission.py --root .` | Transitional CLI delegating to the shared registry compatibility module. | Validates the current neutral registry rather than an independent admission, evaluation, or fitness snapshot. | Repository-static integrity only; no model execution or provider-runtime promotion. |
| `python3 scripts/validate-agent-evaluations.py --root .` | Transitional CLI delegating to the shared registry compatibility module. | Validates the current neutral registry rather than an independent admission, evaluation, or fitness snapshot. | Repository-static integrity only; no model execution or provider-runtime promotion. |
| `python3 scripts/validate-agent-governance-ci.py --root . --self-test`; `python3 scripts/validate-agent-governance-ci.py --root .` | 첫 command는 repository inputs와 분리된 exact six-row truth table 및 45-case mutation matrix이고, 둘째는 exact repository root와 closed contract/schema/fixture 및 provider-evidence aggregate source manifest를 사용한다. | Selector output, dedicated static job, exact dependency-install/gate/delegated run-line sequence, exact `ci-summary` job/verdict-step/env shape와 pinned full-script SHA-256, twelve route classes, eighteen delegated commands including the closure self-test/production pair, sole provider-evidence aggregate CI owner, and sole repository-static `agent-checkpoint` self-test owner, provider aggregate exact path/SHA-256/focused-validator literal과 static-only residue boundary, aggregate/pre-commit order, ten local-QA owner/consumer surfaces, workflow-level inherited secret/provider env, skipped validation/summary step, custom/default shell, extra run command, summary job permissions/env/defaults와 agent/summary job·step `continue-on-error` 차단, full-SHA/least-permission security boundary, result vocabulary, canonical `repo-static`/`provider-runtime`/`ci`/`remote-live` evidence vocabulary, and the single Spec046 deferred owner를 검증한다. | Self-test PASS는 six truth와 45 mutation, production PASS는 12 route classes, 18 delegated checks, six truth rows, one deferred owner, ten QA surfaces다. Exact machine-output inventory는 위 Script Inventory row가 한 번만 소유한다. 둘 다 repository-static evidence일 뿐 hosted CI, branch protection, provider runtime/auth/model, remote, live evidence를 뜻하지 않는다. |
| `python3 scripts/validate-agent-governance-closure.py --root . --self-test`; `python3 scripts/validate-agent-governance-closure.py --root .` | Both commands delegate to the same neutral registry authority. | Self-test adds one bounded runtime-claim rejection; public unexpected failures are redacted. Closure artifacts do not duplicate roster, model, memory, QA, or Task authority. | PASS is repository-static registry evidence only, never hosted CI, authenticated provider execution, remote/live, or actual checkpoint evidence. |
| `python3 scripts/validate-agent-model-fitness.py --root .` | Transitional CLI delegating to the shared registry compatibility module. | Validates the current neutral registry rather than an independent admission, evaluation, or fitness snapshot. | Repository-static integrity only; no model execution or provider-runtime promotion. |
| `python3 scripts/validate-agent-provider-evidence.py --root .` | Composes the focused configuration and canary validators. | Codex/Claude configuration, safe inputs, redaction, and independent evidence lanes. | Repository-static evidence only; executable presence does not prove discovery, authentication, hosted CI, or live readiness. |
| `bash scripts/validate-gitops-structure.sh`       | 인자를 받지 않는다. 스크립트가 속한 repository에서 실행된다.                           | ArgoCD root app, root application kind, root app manifest, `clusters/local` root/ApplicationSet boundary, root app local source path boundary, `gitops/**/kustomization.yaml` syntax, sibling manifest resource completeness를 검증한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | exit `0`은 필요한 GitOps 구조가 있고 parse 가능하며 root/platform/workload hierarchy와 각 `kustomization.yaml`의 sibling YAML manifest 참조가 유효하다는 뜻이다.                                   |
| `bash scripts/validate-harness.sh` | 인자를 받지 않는다. 스크립트 위치 기준 repository root에서 실행된다. | `validate-repo-quality-gates.sh`, `validate-gitops-change-set.py --root . --base-ref HEAD`, `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, `check-secret-handling.sh`, `validate-vault-eso-contracts.py --self-test`와 `--root .`, `validate-policy-gates.sh`, `infrastructure/tests/verify-contracts-static.sh`, `git diff --check`를 순서대로 실행한다. 추가 live cluster 검사는 실행하지 않는다. | exit `0`은 모든 repo-static 하네스 게이트가 통과했다는 뜻이다. 하위 게이트 실패는 그대로 전파된다. |
| `python3 scripts/validate-vault-eso-contracts.py --self-test` | 추가 인자를 받지 않는다. | `tests/fixtures/vault-eso-contracts.json`의 정확한 10개 non-secret mutation을 production validator 함수에 적용한다. | exit `0`은 정확한 10개 case가 기대 diagnostics와 일치했다는 뜻이고, fixture/schema/mutation drift는 실패한다. |
| `python3 scripts/validate-vault-eso-contracts.py --root .` | `--root`는 repository root만 허용한다. | 다섯 개 고정 공개 입력만 읽어 Vault/ESO identity, audience, TokenReview, policy, bootstrap secret-process/TLS 계약을 검증한다. | exit `0`은 repo-static 계약 통과이며 live Vault, ESO, secret value, credential, 또는 production TLS readiness 증거가 아니다. |
| `bash scripts/validate-k8s-manifests.sh .`        | 선택 인자는 arbitrary subpath가 아니라 repository root다.                              | `gitops/`, `infrastructure/`, `examples/sample-app/`, `examples/**/{gitops,kubernetes}/`, `traefik/` 아래 YAML을 검사하고, `kube-linter`가 있으면 함께 실행한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | exit `0`은 YAML syntax가 통과했고 optional `kube-linter`도 실패하지 않았다는 뜻이다. `SKIP optional kube-linter`는 local YAML-only validation이며 kube-linter coverage가 아니다. 잘못된 repo root 또는 YAML 0건은 실패한다. |
| `bash scripts/check-secret-handling.sh .`         | 선택 인자는 arbitrary subpath가 아니라 repository root다.                              | `gitops/`, `infrastructure/`, `examples/sample-app/`, `examples/**/{gitops,kubernetes}/` 아래 YAML에서 quoted literal 값을 포함한 plaintext secret pattern을 검사하되 ExternalSecret-like resource는 제외한다. Finding 출력은 값을 `<redacted>`로 숨긴다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | exit `0`은 검사 대상 파일이 있고 plaintext secret pattern이 없다는 뜻이다. 잘못된 repo root, YAML 0건, finding은 실패한다.                                                                         |
| `bash scripts/render-platform-chart-kinds.sh .`   | 선택 인자는 repository root다. 생략하면 스크립트 위치 기준 repository root를 사용한다. | `gitops/apps/root`의 Helm chart Application을 렌더링하고 `gitops/clusters/local/appproject-platform.yaml` allow-list와 비교한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | exit `0`은 모든 렌더링 kind가 platform AppProject allow-list에 포함된다는 뜻이다. Helm 렌더 실패 또는 누락 kind는 실패한다.                                                                        |
| `bash scripts/validate-policy-gates.sh .`         | 선택 인자는 repository root다. 생략하면 스크립트 위치 기준 repository root를 사용한다. | `policy/conftest/kubernetes.rego`와 built-in fallback으로 plaintext Secret, `CreateNamespace=true`, AppProject wildcard, `latest` image 정책을 검사한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | exit `0`은 Conftest 또는 fallback policy gate가 통과했다는 뜻이다. Conftest 미설치는 `SKIP optional conftest`와 fallback 실행으로 보완하며, conftest coverage로 보고하지 않는다. policy violation은 실패한다.                                                      |

Production `post-validate.sh`와 `run-validation-lane.py`에는 self-test 환경변수나
필수 validator `SKIP` 경로가 없다. Post-edit hook은 항상 real affected lane을
실행한다. 전체 입력의 surface 선택을 완료한 뒤, 삭제된 Markdown은 현재
문서의 `--include-path` 인자에서만 제외한다. Migration proof나 후속 validator의
실패를 생략하지 않으며 원래 lane과 입력 수를 유지한다. Aggregate의 재귀 없는 검증은 전용
`tests/test_run_validation_lane.py`,
`tests/test_post_validate_runner_result.py`,
`tests/test_provider_post_validate_hook.py`에서 순수 selector, closed subprocess,
exact marker, runner-log 경계로 격리된다. Manifest 7개와 docs 4개 validator가 모두
실행되는지, 기존 Markdown 경로 전달, hostile PATH/BASH_ENV 차단, missing/SKIP/
duplicate result 거부를 검증한다. 테스트 환경은 production hook 결과를 변경할 수
없다.

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
- `graphify`: 사용자가 명시적으로 요청할 때 설치된 외부 도구의 절차를 따른다. 저장소가 관리하는 그래프 산출물이나 재생성 계약은 없으며, 평소에는 현재 소스와 인덱스를 직접 확인한다.

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
- [Agent Governance Bootstrap](../docs/00.agent-governance/skills/work-lifecycle.md)
- [scripts Inventory Remediation Plan](../docs/98.archive/README.md#document-index)
