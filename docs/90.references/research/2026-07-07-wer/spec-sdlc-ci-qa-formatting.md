---
title: 'Reference: Spec SDLC CI QA Formatting Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-10
---

# Reference: Spec SDLC CI QA Formatting Research

## Overview

이 문서는 스펙 주도 개발(Spec-driven development), SDLC 문서 체계,
CI/QA 증적, 포맷팅, 린팅, 구문 검증을 현재 리포지토리와 외부 1차 자료를
대조해 정리한다. 조사 기준일은 2026-07-10이며, 저장소 사실은 현재 tracked
파일과 repo-static 검사 결과로만 판단한다.

이 문서는 설명용 Stage 90 reference다. 템플릿, 라이프사이클, CI, 훅,
검증 스크립트, 릴리스 승인 또는 live 운영 절차를 재정의하지 않는다.

## Purpose

- GitHub Spec Kit의 스펙 주도 흐름을 로컬 Stage 01-05 체계와 비교한다.
- PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
  Postmortem, Release artifact, Reference, Archive Tombstone의 목적과
  추적 관계를 명확히 한다.
- 포맷팅, 린팅, 구문, 구조, 매니페스트, 비밀, 정책, 릴리스, live runtime
  증적을 서로 다른 QA lane으로 분리한다.
- 확인된 공백은 활성 파일을 수정하지 않고 위험, 권고, 후속 정본 경로로
  기록한다.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-repo-audit
- Source checked: 2026-07-10
- Repo observation date: 2026-07-10
- Refresh trigger: SDLC route/lifecycle, Stage 99 template, CI workflow,
  pre-commit hook, validator, release workflow, incident inventory, 또는 지정
  외부 원문 변경.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-10에 확인한 저장소 문서·템플릿·검증 lane의 설명형 스냅샷.
  - 아래에 명시한 외부 원문과 로컬 구현의 비교 및 후속 권고.
- **Not authoritative for**:
  - 활성 SDLC 상태 전이, template route, CI job, 훅 버전, policy gate,
    release 승인 또는 live 운영 절차.
  - live Kubernetes, Argo CD, Vault, ESO, credential, secret 또는 deployment
    readiness.
  - PRD/ARD를 보편 표준으로 선언하는 것. 두 명칭과 본문 구성은 이
    워크스페이스 및 업계 관행이며, 아래 외부 기준이 강제하는 범용 문서
    표준이 아니다.

## Scope

- 포함: spec-driven development, secure SDLC, 문서 목적·route·lifecycle,
  traceability, formatting, linting, syntax/parse, repo structure, manifest,
  secret, policy, artifact/release, live-evidence 경계.
- 제외: 활성 템플릿·스크립트·CI·policy·manifest 변경, live/remote 실행,
  secret 값 확인, release/publish 동작.

## Definitions / Facts

### Workspace SDLC Snapshot

2026-07-10 repo-static 조사 결과는 다음과 같다.

- `docs/99.templates/templates/sdlc/`에는 19개 파일이 있다. 이 수에는
  Markdown 문서 양식, supplemental harness task contract, OpenAPI, GraphQL,
  protobuf 양식이 포함된다.
- `docs/99.templates/support/sdlc-governance.md`와
  `template-routing.md`는 PRD부터 Postmortem까지의 구조 route를 정의하지만
  Release 전용 문서 route와 template은 없다.
- `docs/05.operations/incidents/`의 tracked 파일은 `README.md` 하나뿐이다.
  실제 `sdlc/incident` 또는 `sdlc/postmortem` 문서는 0개다. 이는 실제 사고가
  있었다는 증거도, 대응 준비가 검증됐다는 증거도 아니다.
- Stage 03에는 20개 parent `spec.md`가 있고 frontmatter 상태는
  `draft` 16개, `active` 4개, `done` 0개다. Stage 04 task 문서는 43개이며
  42개가 `done`, 현재 hardening task 1개가 `draft`다. 따라서 완료 증적과
  parent Spec 성숙도 사이에 구조적 비대칭이 있다.
- 공유 lifecycle은 PRD/Spec/Plan/Task가 `done`, ARD/ADR/Operations가
  `accepted`, Archive Tombstone이 `archived`로 종결된다. 이 상태 언어의
  정본은 Stage 99 SDLC governance다.
- `.github/workflows/ci.yml`은 6개 job을 선언한다. 이 문서에서는 job DAG
  전체가 아니라 각 QA 증적의 owner와 증명 범위만 다룬다. 파이프라인
  토폴로지의 주 소유 문서는 `automation-pipeline-workflow-qa.md`다.

### External SDLC Benchmark

아래 표는 2026-07-10에 확인한 11개 지정 원문의 성격과 로컬 적용 의미를
구분한다. `Standard`는 공개 규격·정부 기준, `Official guidance`는 도구 또는
플랫폼 소유자의 지침, `Primary practice`는 원 저자·운영 조직이 공개한
실무 관행이다.

| Source | Authority kind | Verified benchmark | Workspace interpretation |
| --- | --- | --- | --- |
| GitHub Spec Kit | Official upstream project | 의도/요구를 spec으로 만들고 plan, tasks, implementation으로 구체화하며 constitution, clarify, analyze, checklist 같은 보조 단계를 제공한다. | 로컬 PRD/ARD/ADR → Spec → Plan/Task → 구현·검증 흐름은 같은 traceability 원리를 이미 가지지만 Spec Kit 설치 또는 명령 호환을 뜻하지 않는다. |
| NIST SP 800-218 SSDF 1.1 | Government standard/guidance | 보안 실무를 특정 SDLC 하나로 대체하지 않고 각 조직의 SDLC에 통합하는 공통 상위 관행을 제시한다. | secret, policy, workflow security, verification evidence는 마지막 점검이 아니라 각 Stage의 acceptance/verification에 연결해야 한다. |
| NIST SP 800-61 Rev. 3 | Government standard/guidance | incident response를 CSF 2.0 위험 관리 전반에 통합해 준비, 탐지, 대응, 복구 효과를 높이도록 권고한다. | Incident/Postmortem 양식의 존재만으로 준비가 증명되지 않는다. 연습 또는 실제 사건의 승인된 evidence가 별도로 필요하다. |
| Google SRE postmortem culture | Primary operational practice | 사건 학습을 반복 방지로 연결하고 개인 비난보다 기여 요인, 시스템, 개선 action에 집중한다. | 로컬 Incident는 사실·대응 상태, Postmortem은 원인·예방·문서 feedback loop를 소유하도록 분리한 것이 적합하다. |
| Nygard/Cognitect ADR | Primary architecture practice | 작은 단일 결정 기록에 Context, Decision, Status, Consequences를 남기고 superseded 결정을 보존한다. | 로컬 ADR의 단일 결정, 순차 번호, accepted/archived lifecycle, replacement trace가 이 관행과 대응한다. 보편 규격은 아니다. |
| GitHub Actions secure use | Official platform guidance | 최소 `GITHUB_TOKEN` 권한, secret 취급, untrusted input 경계, third-party Action의 full-length commit SHA pinning을 권고한다. | `ci.yml`의 `permissions: contents: read`와 `persist-credentials: false`는 정적 근거다. 반면 현재 `uses:`는 version tag이므로 immutable SHA pinning 충족으로 보고할 수 없다. |
| pre-commit | Official tool guidance | `.pre-commit-config.yaml`이 hook 저장소와 실행 구성을 선언하며 `pre-commit run --all-files`로 전체 파일 검사를 수행한다. | 로컬 hook matrix는 빠른 toolchain feedback owner지만 개별 hook의 범위와 optional 도구 경계를 그대로 기록해야 한다. |
| EditorConfig | Official specification/project | charset, EOL, indentation, trailing whitespace, final newline 같은 editor property를 표준화한다. | 로컬 `.editorconfig`는 UTF-8, LF, final newline, space indentation을 정의하고 Markdown trailing whitespace 제거는 예외로 둔다. |
| Prettier | Official tool guidance | AST를 parse하고 자체 규칙으로 다시 출력해 일관된 코드 formatting을 제공한다. | Root `.prettierrc.json`과 `.prettierignore`가 formatting/ignore policy를 선언한다. 그러나 `.pre-commit-config.yaml`과 `.github/workflows/**`에는 Prettier 실행 wiring이 확인되지 않아 자동 enforcement로 보고할 수 없다. |
| CommonMark 0.31.2 | Language specification | Markdown block/inline parsing 규칙과 예제를 정의한다. | CommonMark는 Markdown syntax 기준이며 `markdownlint-cli2`의 style rule 또는 로컬 필수 heading 계약과 동일하지 않다. |
| YAML 1.2.2 | Language specification | YAML character, whitespace, node, collection, document stream의 syntax를 정의한다. | YAML parse 성공은 Kubernetes schema, GitOps 구조, secret, policy 또는 live admission 성공을 증명하지 않는다. |

PRD와 ARD는 위 11개 원문이 표준화한 보편 문서 명칭이 아니다. 이
워크스페이스에서 PRD는 제품 의도와 수용 기준, ARD는 경계·품질 속성·참조
아키텍처를 소유하도록 선택한 industry/workspace convention이다. ADR은
Nygard의 primary practice에 직접 대응하지만 ISO나 NIST 규격으로 취급하지
않는다.

### Spec-Driven Development and Local Flow

로컬 흐름은 `Spec -> Plan -> Tasks -> Implement`만으로 시작하지 않는다.
Stage 01 제품 의도와 Stage 02 아키텍처 요구·결정이 Stage 03 Spec의 입력이
되고, Stage 04가 실행 순서와 evidence를 보존하며, 안정화된 지식과 사고
학습은 Stage 05로 승격된다.

| Flow step | Local canonical owner | Required handoff evidence |
| --- | --- | --- |
| What/why | Stage 01 PRD | problem, personas/use cases, requirements, acceptance criteria, scope |
| Architecture boundary | Stage 02 ARD/ADR | quality attributes, system context, alternatives, decision consequences |
| Implementation contract | Stage 03 Spec and feature-local helper contracts | upstream links, contracts, design, verification commands and success criteria |
| Execution decomposition | Stage 04 Plan | work breakdown, risks, verification gates, rollback and approval boundary |
| Execution evidence | Stage 04 Task | task status, commands, results, limitations, review and commit evidence |
| Stable operation/learning | Stage 05 Guide/Policy/Runbook/Incident/Postmortem | reproducible guidance, controls, executable recovery, facts, learning actions |

GitHub Spec Kit은 비교 benchmark이지 로컬 route owner가 아니다. 로컬
정본은 `stage-authoring-matrix.md`, `document-stage-routing.md`, Stage 99
support contract와 실제 template이다.

### Lifecycle and Traceability Matrix

| Document | Purpose | Primary inputs | Decision/evidence owner | Lifecycle | Local route |
| --- | --- | --- | --- | --- | --- |
| PRD | 사용자/운영자 가치, 문제, 요구, 성공·수용 기준을 정의한다. | 문제 진술, business goal, stakeholder evidence | Product Manager; acceptance owner | `draft -> active -> done / archived` | `docs/01.requirements/<###-Numbering>-<feature-or-system>.md` |
| ARD | 시스템 경계, 품질 속성, 데이터·배포·운영 관점을 참조 구조로 정의한다. | PRD, 현행 시스템·제약 | System Architect; architecture requirement owner | `draft -> active -> accepted / archived` | `docs/02.architecture/requirements/####-<system-or-domain>.md` |
| ADR | 하나의 중요한 선택, 대안, 결과와 후속 supersession을 기록한다. | ARD, alternatives, constraints | System Architect; decision owner | `draft -> active -> accepted / archived` | `docs/02.architecture/decisions/####-<short-title>.md` |
| Spec | upstream 의도를 구현 가능한 contract와 검증 기준으로 바꾼다. | PRD, ARD, ADR | Engineering owner; implementation-contract owner | `draft -> active -> done / archived` | `docs/03.specs/<###-Numbering>-<feature-id>/spec.md` |
| Plan | Spec을 순서, 위험, gate, rollout/rollback으로 분해한다. | Spec, PRD, ADR | Tech/QA lead; execution-plan owner | `draft -> active -> done / archived` | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` |
| Task | 실제 작업 상태, 검증, 제한, review, commit 증적을 보존한다. | Plan, Spec | Engineer/QA; execution-evidence owner | `draft -> active -> done / archived` | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` |
| Guide | 안정 상태의 이해, onboarding, how-to를 설명한다. | Stable Spec, operations context | Technical Writer/operator; reproducibility owner | `draft -> active -> accepted / archived` | `docs/05.operations/guides/####-<topic>.md` |
| Policy | 적용 범위, required/allowed/disallowed control, 예외와 증적을 규정한다. | Spec, security/compliance requirement | Operations owner; control owner | `draft -> active -> accepted / archived` | `docs/05.operations/policies/####-<policy>.md` |
| Runbook | 즉시 실행할 순서, 검증, rollback/recovery를 정의한다. | Policy, Spec, operational evidence | Operator; procedure-evidence owner | `draft -> active -> accepted / archived` | `docs/05.operations/runbooks/####-<topic>.md` |
| Incident | 확인된 영향, 상태, timeline, response evidence를 사실 중심으로 기록한다. | Runtime evidence, alerts, runbook | Incident commander/operations-security | `draft -> active -> accepted / archived` | `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` |
| Postmortem | 원인, 기여 요인, 탐지 공백, 예방 action과 문서 feedback을 분석한다. | Closed/stabilized Incident, evidence | Operations/security and reviewers | `draft -> active -> accepted / archived` | `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` |
| Release artifact | 변경 목록, tag와 배포 가능한 artifact의 release evidence를 보존한다. | Accepted change, commit/tag, build evidence | Release coordinator; artifact/provenance owner | 전용 SDLC lifecycle 없음 | 전용 doc route 없음; `.github/workflows/generate-changelog.yml`이 tag 기반 changelog artifact만 생성 |
| Reference | 느리게 변하는 사실, 외부 source snapshot, authority/freshness를 제공한다. | Stable facts, inventories, primary sources | Technical Writer/Governance Steward | authoring은 `draft`; 공유 SDLC 전이표에는 없음 | `docs/90.references/<category>/<topic>.md` |
| Archive Tombstone | 이전 경로, archive 이유, replacement를 metadata-only로 보존한다. | Superseded/obsolete active doc, replacement evidence | Governance Steward | `archived` only | `docs/98.archive/<original-docs-subpath>` |

모든 handoff는 `Related Documents` 또는 route owner가 정의한 동등한 link
section으로 이어져야 한다. 링크 존재는 semantic completeness를 자동으로
증명하지 않으므로 Task evidence와 lifecycle state를 함께 검토해야 한다.

### QA Evidence Lane Matrix

| Evidence lane | Active local owner / command | What it proves | What it does not prove | 2026-07-10 verdict |
| --- | --- | --- | --- | --- |
| Formatting | `.editorconfig`; `.prettierrc.json`; `.prettierignore`; `trailing-whitespace`, `end-of-file-fixer`, `mixed-line-ending`; `shfmt`; `git diff --check` | configured editor/Prettier policy와 ignore scope, hook이 실제 실행한 file hygiene, shell formatting, pending diff whitespace 상태 | Prettier config 존재만으로 Prettier 실행, semantic correctness, Markdown policy 전체, live readiness | Configured; Prettier의 pre-commit/CI 실행 wiring은 확인되지 않음 |
| Linting | `markdownlint-cli2`, `shellcheck`, `actionlint`, `zizmor`, `hadolint`, `kube-linter` hooks | 각 도구 범위의 style/static anti-pattern | compiler/runtime 성공, 모든 security issue | Implemented; hook/file scope와 도구 가용성에 한정 |
| Syntax / parse | Automated: `check-yaml`, `check-json`, `check-toml`, `validate-k8s-manifests.sh`의 PyYAML parse. Manual: CI/QA guide의 단일 파일 `bash -n <script>` | 자동 lane은 대상 data/manifest parser 통과를, 수동 `bash -n`은 실제 실행한 특정 shell 파일의 grammar 통과를 증명 | Kubernetes schema/admission, application behavior, 실행하지 않은 shell 파일 syntax | Data/manifest parse는 wired; shell syntax는 manual이며 repo-quality/harness가 실행하지 않음 |
| Repo-structural | `bash scripts/validate-repo-quality-gates.sh .` | docs taxonomy, template route/headings, inventory, references와 repository contracts | remote CI/ruleset, runtime state | Implemented repo-static gate |
| Manifest | `validate-gitops-structure.sh`; `validate-k8s-manifests.sh .`; `infrastructure/tests/verify-contracts-static.sh` | desired-state parse, GitOps hierarchy/resource references, static platform contracts | API-server admission, reconciliation, workload health | Implemented static lane; kube-linter는 설치 시 실행 |
| Secret | pre-commit `gitleaks`, `detect-secrets`; `bash scripts/check-secret-handling.sh .` | configured scan 범위에서 secret pattern/plaintext manifest finding 부재 | 외부 Vault/ESO 값·권한·rotation readiness | Implemented static scan; secret 값 열람 권한 아님 |
| Policy | `bash scripts/validate-policy-gates.sh .` | Conftest 설치 시 Rego와 항상 실행되는 built-in fallback의 선언 정책 | cluster admission policy 또는 모든 Kubernetes security control | Implemented fallback; 이 환경의 Conftest는 미설치 |
| Artifact / release | `.github/workflows/generate-changelog.yml` on `v*.*.*`; git-cliff; uploaded `CHANGELOG.md` artifact | tag event에서 changelog preview artifact를 만들도록 선언됨 | tracked changelog merge, release approval, artifact integrity, SBOM, provenance/attestation, deployment | Partial; dedicated release readiness/provenance contract 없음 |
| Live runtime | operator-approved Stage 05 policy/runbook과 별도 승인 evidence | 승인된 대상에 실제로 수행한 관측 결과만 증명 | 승인·실행하지 않은 Kubernetes/Argo CD/Vault/ESO 상태 | Not run and not inferred in this audit |

### Formatting, Linting, and Syntax Interpretation

- **Formatting**은 텍스트를 정규 형태로 만드는 책임이다. 이 저장소에는
  EditorConfig와 Prettier config/ignore policy가 모두 있다. 실제 자동 실행이
  확인된 owner는 file-hygiene hooks, `shfmt`, diff hygiene이며, Prettier는
  pre-commit/CI wiring이 확인되지 않아 configured policy와 enforced formatter를
  구분해야 한다.
- **Linting**은 parse 가능한 입력 안에서 style, portability, security
  anti-pattern을 찾는다. `markdownlint-cli2`, `shellcheck`, `actionlint`,
  `zizmor`, `hadolint`, `kube-linter`는 서로 대체 관계가 아니다.
- **Syntax/parse**는 입력이 parser grammar에 맞는지 확인한다. CommonMark와
  YAML 1.2.2는 언어 기준이며, local required heading이나 Kubernetes semantic
  validation을 자동으로 제공하지 않는다.
- `actionlint`는 pre-commit/CI에 wired된 GitHub Actions workflow lint/parser
  도구다. 반면 shell의 `bash -n`은 CI/CD QA guide가 제시한 수동 단일 파일
  명령이며 `validate-repo-quality-gates.sh`나 `validate-harness.sh`가 실행하지
  않는다. 수동 실행 기록이 없으면 automated shell syntax evidence로
  승격하지 않는다.
- `pre-commit run --all-files`는 hook matrix를 재현하지만 GitHub event context,
  branch policy, path-filter result, remote permission/ruleset을 재현하지 않는다.

### Document Maturity Gap Register

아래 항목은 조사 결과와 권고다. 이 작업은 나열한 활성 owner를 변경하지
않는다.

| Gap | Classification | Severity | Risk rationale | Recommendation | Canonical follow-up |
| --- | --- | --- | --- | --- | --- |
| 20개 Spec 중 16개가 `draft`, 0개가 `done`인 반면 Stage 04 Task 43개 중 42개가 `done` | Implementation gap | High | 실행 완료 evidence가 parent contract의 lifecycle 성숙도로 환류되지 않아 독자가 current/complete contract를 잘못 판단할 수 있다. | feature lineage별 Spec/Plan/Task를 대조해 human-approved lifecycle promotion 또는 명시적 잔여 gap을 기록하는 별도 audit를 제안한다. | `docs/99.templates/support/sdlc-governance.md`; 각 Stage 03 Spec/Stage 04 Task; 새 scoped Spec/Plan/Task |
| Release 전용 template/route/readiness record가 없고 tag workflow는 changelog preview artifact만 생성 | Implementation gap | High | release 승인, artifact identity, SBOM/provenance, promotion/rollback evidence가 하나의 추적 가능한 contract로 묶이지 않는다. | Release document가 필요한지 먼저 architecture/governance decision으로 결정하고, 채택 시 route/template/CI/operations를 하나의 변경 단위로 설계한다. | `docs/99.templates/support/{sdlc-governance,template-routing}.md`; `.github/workflows/generate-changelog.yml`; 새 PRD/ARD/ADR/Spec/Plan/Task |
| 실제 Incident/Postmortem record와 tabletop exercise evidence가 0개 | Unverified | Medium | 사건이 없었다는 사실과 대응·학습 절차가 연습됐다는 사실을 구분할 수 없다. 가짜 incident 문서를 만들면 오히려 evidence가 오염된다. | 별도 승인된 tabletop exercise 계획과 synthetic 표기를 갖춘 evidence 방식을 설계하고 실제 사건 folder와 혼동하지 않도록 한다. | `docs/05.operations/incidents/README.md`; incident/postmortem templates; 새 Spec/Plan/Task 및 운영 runbook |
| lifecycle handoff가 링크·review 중심이고 semantic trace completeness 자동 검사가 제한적 | Implementation gap | Medium | PRD requirement에서 Task validation까지 ID coverage가 빠져도 단순 link 존재 검사만으로는 누락을 찾기 어렵다. | 기존 route gate를 변경하기 전에 lineage ID와 상태 전이 invariant를 정의하고 fixture 기반 validator proposal을 평가한다. | `docs/99.templates/support/sdlc-governance.md`; `scripts/validate-repo-quality-gates.sh`; 새 Spec/Plan/Task |
| GitHub Actions `uses:`가 version tag이고 full-length commit SHA가 아님 | Implementation gap | High | 공식 secure-use 지침의 immutable action source 보장을 충족하지 않으며 upstream tag 이동 위험이 남는다. | action pinning과 update automation의 failure mode를 검토한 별도 CI security hardening proposal을 만든다. | `.github/workflows/*.yml`; `.github/dependabot.yml`; Stage 00 approval boundary; 새 Spec/Plan/Task |
| Prettier configuration/ignore policy는 있으나 pre-commit/CI execution wiring이 확인되지 않음 | Needs strengthening | Low | 개발자별 수동 실행 여부에 따라 configured formatting policy와 실제 결과가 달라질 수 있고, config 존재만으로 enforcement를 오판할 수 있다. | 적용 대상과 기존 Markdown/shell formatters의 중복·충돌을 평가한 뒤 Prettier를 수동 도구로 유지할지 별도 hook/CI gate로 승격할지 결정한다. | `.prettierrc.json`; `.prettierignore`; `.pre-commit-config.yaml`; `.github/workflows/ci.yml`; 새 scoped Spec/Plan/Task |

## Implementation Checklist

- lifecycle·route 변경은 Stage 99 support contract, Stage 00 routing,
  validator, Stage README를 같은 논리 단위로 검토한다.
- CI/hook/tool 변경은 `.github/workflows/**`, `.pre-commit-config.yaml`,
  `.editorconfig`, `scripts/README.md`, CI/CD QA guide와 Task evidence로
  라우팅한다.
- release/provenance 추가는 dedicated decision과 Spec/Plan/Task 없이
  changelog workflow에 암묵적으로 넣지 않는다.
- incident readiness를 검증할 때 실제 incident와 exercise evidence를
  명확히 구분하고 secret·live 명령 경계를 지킨다.
- Stage 90 reference의 권고를 구현 완료로 해석하지 않는다.

## Sources

Official, standards-body, upstream, and primary-practice sources checked on
2026-07-10:

- GitHub Spec Kit: <https://github.com/github/spec-kit>
- NIST SSDF SP 800-218 Version 1.1:
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- NIST SP 800-61 Revision 3:
  <https://csrc.nist.gov/pubs/sp/800/61/r3/final>
- Google SRE, Postmortem Culture:
  <https://sre.google/sre-book/postmortem-culture/>
- Michael Nygard/Cognitect, Documenting Architecture Decisions:
  <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- GitHub Actions secure use:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- pre-commit: <https://pre-commit.com/>
- EditorConfig: <https://editorconfig.org/>
- Prettier: <https://prettier.io/docs/>
- CommonMark 0.31.2: <https://spec.commonmark.org/0.31.2/>
- YAML 1.2.2: <https://yaml.org/spec/1.2.2/>

Repo-backed sources checked on 2026-07-10:

- [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document Stage Routing](../../../00.agent-governance/rules/document-stage-routing.md)
- [SDLC Governance](../../../99.templates/support/sdlc-governance.md)
- [Template Routing](../../../99.templates/support/template-routing.md)
- [Frontmatter Schema](../../../99.templates/support/frontmatter-schema.md)
- [Stage 01 Requirements](../../../01.requirements/README.md)
- [Stage 02 Architecture](../../../02.architecture/README.md)
- [Stage 03 Specs](../../../03.specs/README.md)
- [Stage 04 Execution](../../../04.execution/README.md)
- [Stage 05 Operations](../../../05.operations/README.md)
- [Incident Index](../../../05.operations/incidents/README.md)
- [Stage 99 Templates](../../../99.templates/README.md)
- [CI/CD & QA Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts Inventory](../../../../scripts/README.md)
- [CI workflow](../../../../.github/workflows/ci.yml)
- [Changelog workflow](../../../../.github/workflows/generate-changelog.yml)
- [Pre-commit configuration](../../../../.pre-commit-config.yaml)
- [EditorConfig](../../../../.editorconfig)
- [Prettier configuration](../../../../.prettierrc.json)
- [Prettier ignore policy](../../../../.prettierignore)

Historical integration context:

- [2026-07-04 SDLC research snapshot](../2026-07-04-wer/spec-sdlc-ci-qa-formatting.md)
  was read as dated context. Still-valid source distinctions and evidence-lane
  analysis were rechecked before inclusion; the Historical file was not edited.

## Review and Freshness

- Review cadence: SDLC/template/CI/hook/release/incident contract 변경 시.
- Last reviewed: 2026-07-10
- Next review trigger: lifecycle transition change, release route/template
  decision, incident exercise/record creation, validator scope change, or any
  of the 11 external source revisions.
- Evidence limitation: this audit used repository files, deterministic static
  checks, and read-only external sources. No live runtime, remote GitHub,
  credential, secret value, release, publish, provider runtime, or third-party
  mutation was performed.

## Related Documents

- **Current research pack**: [README.md](README.md)
- **Workspace baseline**:
  [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Automation and CI topology**:
  [automation-pipeline-workflow-qa.md](automation-pipeline-workflow-qa.md)
- **Infrastructure security reference**:
  [kubernetes-infrastructure-security.md](kubernetes-infrastructure-security.md)
- **Current hardening Spec**:
  [Workspace Engineering Research Pack](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Current hardening Plan**:
  [Fact-First Hardening Plan](../../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current hardening Task**:
  [Fact-First Hardening Task](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Reference maintenance runbook**:
  [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
