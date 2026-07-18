---
title: 'Reference: Spec SDLC CI QA Formatting Research'
type: content/reference
status: accepted
owner: platform
updated: 2026-07-14
---

# Reference: Spec SDLC CI QA Formatting Research

## Overview

이 문서는 스펙 주도 개발(Spec-driven development), SDLC 문서 체계,
CI/QA 증적, 포맷팅, 린팅, 구문 검증을 현재 리포지토리와 외부 1차 자료를
대조해 정리한다. 조사 기준일은 2026-07-10이며, 저장소 사실은 현재 tracked
파일과 repo-static 검사 결과로만 판단한다. 저장소 재계수는
`ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`을 고정 기준으로 삼아
2026-07-11에 실행했다.

이 문서는 설명용 Stage 90 reference다. 템플릿, 라이프사이클, CI, 훅,
검증 스크립트, 릴리스 승인 또는 live 운영 절차를 재정의하지 않는다.

### Purpose

- GitHub Spec Kit의 스펙 주도 흐름을 로컬 Stage 01-05 체계와 비교한다.
- PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
  Postmortem, Release artifact, Reference, Archive Record의 목적과
  추적 관계를 명확히 한다.
- 포맷팅, 린팅, 구문, 구조, 매니페스트, 비밀, 정책, 릴리스, live runtime
  증적을 서로 다른 QA lane으로 분리한다.
- 확인된 공백은 활성 파일을 수정하지 않고 위험, 권고, 후속 정본 경로로
  기록한다.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-repo-audit
- Source checked: 2026-07-10
- Repo observation date: 2026-07-11 at fixed base
  `ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`
- Refresh trigger: SDLC route/lifecycle, Stage 99 template, CI workflow,
  pre-commit hook, validator, release workflow, incident inventory,
  `.editorconfig`, `.prettierrc.json`, `.prettierignore`, 또는 지정 외부 원문
  변경. 세 formatting source 중 하나가 변경되면 formatting evidence를 다시
  검증한다.

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

### Workspace SDLC Fixed Snapshot

아래 계수는 작업 트리가 아닌 고정 commit
`ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7`의 첫 frontmatter block에서
`status`를 읽은 2026-07-11 repo-static 결과다. Stage 01–05 authored
document의 path/status stream SHA-256은
`253fcd638675527ddc6d1df59a04628f3dadfff47a55de1ac9893a927a7f17fd`다.
Reference는 `docs/90.references/**`의 non-README Markdown, README는 Stage
01–05와 Stage 90의 index surface로 별도 계수했다.

| Family | Fixed path basis | Count and fixed-snapshot status |
| --- | --- | --- |
| PRD | `docs/01.requirements/*.md` | 4: 4 `active` |
| ARD | `docs/02.architecture/requirements/*.md` | 4: 4 `active` |
| ADR | `docs/02.architecture/decisions/*.md` | 9: 9 `accepted` |
| Spec | `docs/03.specs/*/spec.md` | 20: 16 `draft`, 4 `active`, 0 `done` |
| Agent design | `docs/03.specs/*/agent-design.md` | 1: 1 `draft` |
| Plan | `docs/04.execution/plans/*.md` | 41: 41 `done` |
| Task | `docs/04.execution/tasks/*.md` | 43: 43 `done` |
| Guide | `docs/05.operations/guides/*.md` | 8: 8 `active` |
| Policy | `docs/05.operations/policies/*.md` | 7: 7 `active` |
| Runbook | `docs/05.operations/runbooks/*.md` | 9: 9 `active` |
| Incident | `docs/05.operations/incidents/YYYY/INC-*/INC-*.md` | 0: authored record 없음 |
| Postmortem | `docs/05.operations/incidents/YYYY/INC-*/postmortem.md` | 0: authored record 없음 |
| Reference | `docs/90.references/**/*.md`, README 제외 | 29: 26 `draft`, 3 `active` |
| README | Stage 01–05와 Stage 90의 `README.md` | 22: frontmatter-free index, status 비적용 |

Reference path/status stream SHA-256은
`88fc1208c298d637a4e9235c58c007370d583a4b733b49d8206b6d4762e9fd1a`,
README path stream SHA-256은
`6e1944d7ff8ef3e1c5a22b02e827bb51271006d639ea4d6558836834618ffdf3`다.
README 22개는 Stage 01 1개, Stage 02 3개, Stage 03 1개, Stage 04
3개, Stage 05 5개, Stage 90 9개다.

세 hash는 다음 명령으로 재현한다. 모든 경로는 `LC_ALL=C`에서
bytewise `sort`하며, path/status stream은 path와 status 사이에 tab
separator, 각 record 끝에 LF newline을 `printf '%s\t%s\n'`으로
명시한다. Status는 각 문서의 첫 `---` frontmatter block에서만
첫 `status:` key 값을 읽고, 없으면 `MISSING`을 쓴다. README stream은
status 없이 정렬된 path만 record당 LF 하나로 입력한다.

```bash
export LC_ALL=C
base=ab3556b8d5a9ae6f469a751057d9ad5ef261cdf7

# Stage 01–05 non-README path<TAB>status<LF> stream.
git ls-tree -r --name-only "$base" -- \
  docs/01.requirements docs/02.architecture docs/03.specs \
  docs/04.execution docs/05.operations |
  awk '/\.md$/ && $0 !~ /\/README\.md$/ { print }' |
  sort |
  while IFS= read -r doc; do
    doc_status=$(git show "$base:$doc" |
      awk 'NR == 1 && $0 == "---" { fm=1; next }
        fm && $0 == "---" { exit }
        fm && /^status: / { sub(/^status: /, ""); print; exit }')
    printf '%s\t%s\n' "$doc" "${doc_status:-MISSING}"
  done |
  sha256sum

# Stage 90 Reference non-README path<TAB>status<LF> stream.
git ls-tree -r --name-only "$base" -- docs/90.references |
  awk '/\.md$/ && $0 !~ /\/README\.md$/ { print }' |
  sort |
  while IFS= read -r doc; do
    doc_status=$(git show "$base:$doc" |
      awk 'NR == 1 && $0 == "---" { fm=1; next }
        fm && $0 == "---" { exit }
        fm && /^status: / { sub(/^status: /, ""); print; exit }')
    printf '%s\t%s\n' "$doc" "${doc_status:-MISSING}"
  done |
  sha256sum

# Stage 01–05 plus Stage 90 README path<LF> stream.
git ls-tree -r --name-only "$base" -- \
  docs/01.requirements docs/02.architecture docs/03.specs \
  docs/04.execution docs/05.operations docs/90.references |
  awk '/(^|\/)README\.md$/ { print }' |
  sort |
  while IFS= read -r doc; do
    printf '%s\n' "$doc"
  done |
  sha256sum
```

Expected outputs in command order are
`253fcd638675527ddc6d1df59a04628f3dadfff47a55de1ac9893a927a7f17fd`,
`88fc1208c298d637a4e9235c58c007370d583a4b733b49d8206b6d4762e9fd1a`, and
`6e1944d7ff8ef3e1c5a22b02e827bb51271006d639ea4d6558836834618ffdf3`.

기존 2026-07-10 관찰의 `42/43 done` Task 수치는 당시 진행 중이던
hardening Task 1개가 `draft`였던 이전 시점의 역사적 사실이다. 그
문맥은 보존하되, 본 audit의 고정 스냅샷 수치는 `43/43 done`으로
정정한다. 정정 후에도 20개 Spec이 16 `draft`, 4 `active`, 0
`done`이므로 draft-Spec/done-Task 비대칭 판정은 그대로다.

추가 정적 사실은 다음과 같다.

- `docs/99.templates/templates/sdlc/`에는 Markdown, supplemental harness
  task contract, OpenAPI, GraphQL, protobuf를 포함한 19개 파일이 있다.
- Stage 99은 PRD부터 Postmortem까지의 route를 정의하지만 Release
  전용 document route/template은 없다.
- Incident/Postmortem 0개는 실제 사고 부재나 대응 준비 성숙도를
  단정하지 않는 중립 관찰이다.
- 공유 lifecycle 언어의 정본은 Stage 99 SDLC governance이며,
  아래의 확장 전이는 policy가 아닌 research candidate다.

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

#### Document Role Matrix

| Document | Purpose | Primary input | Required output | Decision/evidence owner | Expected state path |
| --- | --- | --- | --- | --- | --- |
| PRD | 문제, 가치, 요구, 성공·수용 기준 | Stakeholder evidence, business goal | Numbered requirements and acceptance boundary | Product Manager | `draft -> active -> done` |
| ARD | 시스템 경계와 품질 속성 | PRD, current constraints | Reference architecture and quality requirements | System Architect | `draft -> active -> accepted` |
| ADR | 하나의 중요 선택과 결과 | ARD, alternatives, constraints | Context, decision, status, consequences | System Architect/decision approver | `draft -> active -> accepted` |
| Spec | 구현·검증 가능한 contract | PRD requirements, ARD/ADR | Design, contracts, requirement coverage, verification criteria | Engineering owner | `draft -> active -> done` |
| Plan | 실행 순서와 gate | Accepted baseline Spec, ADR | Phases, risk, approval, rollout/rollback | Tech/QA lead | `draft -> active -> done` |
| Task | 실제 실행·검증 원장 | Plan, Spec | Status, commands, results, limitations, review/commit evidence | Engineer/QA | `draft -> active -> done` |
| Guide | 안정 상태의 이해·how-to | Stable Spec, operator context | Reproducible reader guidance | Technical Writer/operator | `draft -> active -> accepted` |
| Policy | 필수·허용·금지 control | Spec, security/operations requirements | Scope, controls, exceptions, evidence and review rule | Operations/control owner | `draft -> active -> accepted` |
| Runbook | 순서가 있는 운영·복구 절차 | Policy, Spec, observed operations | Preconditions, steps, verification, rollback/recovery | Operator | `draft -> active -> accepted` |
| Incident | 사고 사실·영향·timeline·대응 상태 | Runtime evidence, alerts, runbook | Factual response record and stabilization evidence | Incident commander/operations-security | `draft -> active -> accepted` |
| Postmortem | 원인·기여 요인·재발 방지 학습 | Stabilized Incident and evidence | RCA, detection gaps, owned actions, documentation feedback | Operations/security and reviewers | `draft -> active -> accepted` |
| Release | 배포 단위의 승인·artifact·provenance·rollback 증적 후보 | Accepted change, tag/commit, build and rollout evidence | Decision-dependent readiness/release record | Release coordinator/operator | No route or lifecycle; ADR-first decision required |
| Reference | 느리게 변하는 사실·외부 source snapshot | Stable facts, inventories, primary sources | Authority, source, freshness, limitations | Technical Writer/Governance Steward | New authoring starts `draft`; no shared terminal path |
| README | 폴더 진입점과 current index | Canonical owners and child inventory | Navigation, scope, current-state index, owner links | Folder owner | Frontmatter/status not applicable |

Archive Record는 독립 사업 산출물이 아니라 이전 active-stage 문서의
provenance-verified full-body 보존 표면이다. `archived` only이며 original type/path,
archive reason, replacement, source commit/blob, payload digest와 exact payload를 남겨야 한다.

#### Document Necessity and Retention Matrix

`Keep`, `Consolidate`, `Archive`, `Decline`은 현재 파일에 대한 즉시 조치가
아니라 후속 정본 작업이 판정할 research criteria다.

| Document | Retention basis | Principal overlap risk | Keep / Consolidate / Archive / Decline criteria |
| --- | --- | --- | --- |
| PRD | 요구와 acceptance lineage가 살아 있는 동안 | Spec의 implementation detail, Policy control 중복 | **Keep** current intent; **Consolidate** same scope/role; **Archive** superseded intent after replacement; **Decline** solution-only request without product requirement. |
| ARD | 현재 boundary/quality attribute를 설명하는 동안 | ADR decision, Spec design 중복 | **Keep** reusable architecture requirements; **Consolidate** duplicate domain views; **Archive** replaced architecture; **Decline** single decision only—use ADR. |
| ADR | 결정·supersession 이력으로 영구 보존 | ARD narrative, Policy prose 중복 | **Keep** consequential choice; **Consolidate** tightly coupled choices before acceptance; **Archive/supersede** with replacement link, never erase; **Decline** reversible routine choice. |
| Spec | 구현 contract가 current이거나 evidence lineage에 필요한 동안 | PRD what/why, Plan sequencing 중복 | **Keep** one current contract per feature; **Consolidate** duplicate active specs; **Archive** obsolete contract after replacement; **Decline** work lacking executable acceptance criteria. |
| Plan | rollout 또는 audit lineage가 필요한 동안 | Task status/evidence 중복 | **Keep** approved execution decomposition; **Consolidate** same rollout stream; **Archive** cancelled/superseded plan with reason; **Decline** trivial work fully owned by an existing Task contract. |
| Task | 실행·검증·review evidence로 영구 보존 | Plan checklist, progress ledger 중복 | **Keep** auditable results/limitations; **Consolidate** duplicate trackers before execution; **Archive** abandoned duplicate with replacement; **Decline** evidence-free status copy. |
| Guide | 독자가 재현할 현재 정보인 동안 | Runbook steps, Reference facts 중복 | **Keep** stable explanatory workflow; **Consolidate** audience-identical guides; **Archive** stale instructions; **Decline** emergency executable procedure—use Runbook. |
| Policy | control과 review/exception 의무가 현행인 동안 | Guide advice, ADR rationale 중복 | **Keep** enforceable durable control; **Consolidate** conflicting controls; **Archive** retired policy after replacement; **Decline** non-normative tips. |
| Runbook | 운영·복구 절차가 실행 가능한 동안 | Guide how-to, Incident timeline 중복 | **Keep** executable verified procedure; **Consolidate** same trigger/recovery path; **Archive** invalid procedure; **Decline** conceptual explanation. |
| Incident | 실제 사고 fact record로 영구 보존 | Postmortem analysis 중복 | **Keep** every real scoped incident; **Consolidate** only duplicate record IDs; **Archive** through a governed Archive Record if relocated, not erased; **Decline** synthetic exercise in the real-incident route. |
| Postmortem | 학습·action lineage로 영구 보존 | Incident chronology, Task action log 중복 | **Keep** material learning/action analysis; **Consolidate** duplicate analysis for one incident; **Archive** superseded copy; **Decline** no-analysis chronology. |
| Release | 채택 시 artifact/promotion/provenance retention 기간 | Task evidence, changelog, Git tag 중복 | **Keep** only if ADR identifies distinct consumer/control; **Consolidate** into Task/tag evidence when sufficient; **Archive** superseded release record without deleting immutable artifact history; **Decline** a new route when no consumer exists. |
| Reference | source가 재사용되고 freshness를 평가할 가치가 있는 동안 | Guide, Policy, dated audit 중복 | **Keep** dated pack을 Stage 90 index의 `Current`/`Historical`로 보존; **Consolidate** 중복 Current coverage를 하나의 indexed pack으로 통합; **Delete**는 Stage 90 retention/governance 판정과 index update가 있을 때만; **Archive**는 현행 route가 아니며 future governance proposal이 필요; **Decline** feature-local or normative content. |
| README | 폴더와 current index가 존재하는 동안 | Lifecycle governance body 복제 | **Keep** one entrypoint per routed folder; **Consolidate** duplicated policy into owner links; **Archive** only with removed/moved folder contract; **Decline** nested index with no navigation consumer. |

현행 `docs/98.archive` Archive Record contract은 Stage 01–05의 이전
active-stage 문서에만 적용된다. Stage 90 Reference를 그 경로로
이동하는 것은 현재 허용된 retention 조치가 아니며, 필요하다면
별도 governance proposal이 route, template, index, migration을 먼저 정의해야
한다.

### Research Candidate State Transition and Semantic Lineage Contract

다음은 현행 policy를 변경하지 않고 후속 Stage 00/99 proposal을
평가하기 위한 candidate invariant다.

```text
PRD: draft -> active -> done
ARD/ADR: draft -> active -> accepted
Spec: draft -> active -> done
Plan/Task: draft -> active -> done
Operations: draft -> active -> accepted
Archive: full-body record plus provenance, replacement, and preservation reason
```

- **Approval evidence**: `draft -> active`는 scope/owner/acceptance review,
  terminal promotion은 role-specific acceptance와 Task validation/review evidence를
  필요로 한다. Approval 본문은 Task, review record, decision section 또는
  승인된 외부 record의 link owner에 남기고 boolean metadata로 대체하지
  않는다.
- **Reverse transition**: terminal state에서 묵시적으로 `active`로 돌리지
  않는다. 현재 계약을 다시 열어야 하면 사유, approver, affected
  lineage, 재검증 결과를 Task/decision evidence에 남기고 기존
  terminal evidence를 보존하는 새 revision 또는 supersession을 기본으로
  한다.
- **Numbering**: 신규 feature의 PRD·Spec 3자리 번호는 기본적으로
  일치시키되, 역사적 mismatch는 재번호화하지 않고 explicit link로
  보존한다. 하나의 umbrella PRD/ARD가 복수 Spec을 지원하는 예외는
  각 Spec이 umbrella owner와 자신이 구현하는 requirement ID를 명시하고,
  index/coverage review가 one-to-many를 보여줄 때만 허용하는 candidate다.
- **Semantic coverage**: 각 PRD requirement ID는 정확히 하나 이상의
  Spec design/acceptance row로 연결되고, 각 Spec criterion은 Plan/Task work
  item과 Task validation result로 연결되어야 한다. Link 해석 성공은
  `requirement -> Spec -> Task -> validation` coverage를 증명하지 않는다.
- **Asymmetry gate**: fixed base의 16 draft Specs/43 done Tasks는 Task 완료가
  parent Spec의 terminal promotion을 자동 의미하지 않음을 보여준다.
  반대로 Spec promotion은 Task 증적 누락을 숨기지 않아야 한다. 후속
  audit은 feature lineage별 상태와 coverage를 별도로 판정해야 한다.
- **Archive**: body를 복제한 두 번째 current surface를 만들지 않고
  ArchiveEnvelope.v1 payload와 provenance, replacement 또는 보존 이유를 남긴다.

모든 handoff는 `Related Documents` 또는 route-owned equivalent link와
semantic coverage evidence를 함께 가져야 한다.

### Profile-Specific Frontmatter Benchmark

현재 정본의 대부분 non-README authored profile은 다음 공통 다섯
key를 required baseline으로 사용한다.

```yaml
title: '<Document Title>'
type: <profile-family>/<document-role>
status: draft
owner: platform
updated: YYYY-MM-DD
```

Archive Record는 canonical schema에 따라 공통 다섯 key에
`original_type`, `original_path`, `archived_on`, `archive_reason`, `replacement`,
`source_commit`, `source_blob`, `content_sha256`를 추가로 필수화한다. 따라서
공통 five-key baseline을 모든 profile의 전체 allowed-key set으로 해석하지 않는다.

Fixed-base validator는 required/extra key, exact `type`, `owner: platform`,
공통 status set(`draft`, `active`, `accepted`, `done`, `archived`),
`updated`의 `YYYY-MM-DD` 형태, README frontmatter 금지, route/profile 일치,
index의 status/updated parity를 검사한다. 하지만 authored document의
`YYYY-MM-DD` placeholder도 형태상 통과하며, 실제 calendar date, future date,
빈 title/title placeholder, H1-title 일치, document family별 allowed state는
검증하지 않는다. 따라서 정확한 현재 판정은 “5-key shape와
일부 value gate가 repository-static으로 있다”이지 “metadata semantics가
완전하다”가 아니다.

| Profile/key | Candidate semantics | Required automation consumer before adoption | Benchmark decision |
| --- | --- | --- | --- |
| Common current five | Classification, coarse lifecycle, repository owner, last material update | Existing route/profile/index validator | **Keep**. `owner: platform`은 현재 canonical repository owner로 정규화되지만 human approver를 의미하지 않는다. |
| Common `id` | Rename에도 불변인 semantic lineage identity | Cross-stage coverage/index resolver with uniqueness and immutability checks | **Conditional**. Filename/path만으로 해결할 수 없는 lineage consumer가 승인될 때만 추가한다. |
| Common `created` | 최초 작성일; `updated`와 분리된 age basis | Freshness/retention report that validates `created <= updated` | **Conditional**. Git history로 충분하면 중복 metadata를 늘리지 않는다. |
| Common `review_due` | 다음 의미 검토 기한 | Scheduled report/CI warning with owner and overdue workflow | **Conditional**. Future date가 의도된 유일 date class이며 consumer 없이 전 문서에 강제하지 않는다. |
| Common `supersedes` | 이전 semantic owner/ID에 대한 replacement edge | Bidirectional link resolver, cycle/dangling check, archive migration | **Conditional**. Archive `replacement` owner와 충돌하지 않는 방향성을 먼저 결정한다. |
| Reference `source_checked` | 인용한 외부 source를 마지막으로 재검증한 날 | Reference freshness report/runbook and valid-date check | **Recommended profile candidate**, not common. Source를 쓰지 않는 repo-only reference의 N/A 처리를 정의해야 한다. |
| Incident `incident_id` | Folder/record와 같은 stable incident identity | Incident route/index uniqueness and filename parity validator | **Recommended Incident candidate** when real records exist. Common `id`와 중복 채택하지 않는다. |
| Incident `severity` | Approved impact classification | Incident dashboard/escalation consumer with enumerated scale | **Conditional Incident candidate**. Scale/owner를 Policy/Runbook이 정하기 전에 free text로 추가하지 않는다. |
| Incident `incident_state` | Response state distinct from document `status` | Incident workflow/index that validates allowed response transitions | **Conditional Incident candidate**. `status`(문서 성숙도)와 response state(사고 진행)를 혼합하지 않는다. |

후속 schema/validator proposal의 value gate는 다음을 함께 평가해야 한다.

- `title`은 non-empty이고 template placeholder가 아니며 대응하는 H1과
  의미적으로 일치해야 한다.
- `updated`, `created`, `source_checked`는 실제 ISO calendar date이고
  observation/commit date보다 미래이어서는 안 된다. `review_due`는 유일하게
  미래일 수 있다. Placeholder는 template에서만 허용하고 authored
  document에서는 거부한다.
- `status`는 공통 set 포함여부에서 멈추지 않고 PRD/Spec/Plan/Task의
  `done`, ARD/ADR/Operations의 `accepted`, Archive Record의 `archived` 같은
  profile-specific allowed state를 검사해야 한다.
- Approval 내용, 근거, 대안, 수용 판정, 상세 severity 판단, source
  요약은 본문/Task/review owner에 남긴다. Frontmatter에는 검색·routing·
  validation에 필요한 identity, state, date, edge만 두어 body를 복제하지
  않는다.
- 하나의 consumer를 위해 필요한 key는 해당 profile에만 추가한다.
  모든 authored document에 보편 확장하지 않는다.

### Release, Incident Exercise, and AI-Agent QA Decision Gates

#### Release: ADR-First Home-Lab Decision

현재 tag workflow의 changelog preview artifact와 Task evidence를 넘어선 별도
Release document는 필수로 간주하지 않는다. 먼저 ADR이 다음을
판정해야 한다.

| Gate question | Decline/consolidate separate Release route | Adopt Release route candidate |
| --- | --- | --- |
| Consumer | Human operator가 tag/changelog/Task로 충분히 판정 | Promotion, audit, provenance 또는 rollback consumer가 독립 record를 필요로 함 |
| Frequency/cost | 낮은 배포 빈도와 수동 운영에서 중복 유지비가 더 큼 | 반복 release와 검증 누락 비용이 template/validator 비용보다 큼 |
| Distinct evidence | Task에 artifact identity, validation, approval, rollback을 충분히 연결 | SBOM/provenance, promotion environment, approver, rollback target의 분리 owner가 필요 |
| Adoption consequence | 새 문서 family를 만들지 않고 현재 owner를 강화 | ADR 승인 후 PRD/ARD/Spec/Plan/Task로 route, template, profile, validator, CI, Policy/Runbook, migration/rollback을 함께 설계 |

#### Incident/Postmortem Exercise Gate

실제 Incident/Postmortem 0개는 결함이 아니라 중립 사실이다. 다만
approved tabletop/exercise 증적도 0개이므로 response readiness는
`Unverified`, not failed다. 준비를 검증할 필요가 승인되면 다음 gate를
적용한다.

1. Policy/Runbook owner가 scope, participants, synthetic marker, success and stop
   criteria, secret/live-command boundary를 승인한다.
2. Spec/Plan/Task가 scenario, observations, validation, gaps, follow-up owner를
   담당한다. Synthetic exercise를 실제
   `docs/05.operations/incidents/YYYY/INC-*`에 사고처럼 저장하지 않는다.
3. Timeline, escalation, communication, recovery, evidence capture의 실제 성공/실패를
   기록하고 미사용 tool과 미실행 live check를 명시한다.
4. 통과는 연습이 한 번 수행됐음을 증명할 뿐, 실제 사고 없음,
   재발 방지 성공, live controller readiness를 증명하지 않는다.

#### AI-Agent QA Benchmark Summary

본 Stage 90 reference는 AI-agent QA의 비교 benchmark와 dated summary만
소유한다. 활성 의무와 완료 경계의 정본은
[Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md)와
[CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)다.
아래는 그 정본을 대체하지 않는 risk-based benchmark 요약이며,
충돌 시 Stage 00/05 owner가 우선한다.

- 반복 중에는 changed-file pre-commit과 affected-lane validation으로
  빠른 feedback을 얻고, 위험에 맞는 최소 범위를 매 edit 후 재실행한다.
- PR/merge 전에는 `pre-commit run --all-files`를 필수로 실행한다.
  Hook, validator, toolchain, global formatting/ignore contract를 변경한 뒤에도
  동일한 all-files gate를 필수로 실행한다.
- 모든 hook의 PASS/SKIP/FAIL을 기록하고 optional 또는 unavailable tool,
  sandbox/network limitation, 확인하지 못한 CI/live evidence를 숨기지 않는다.
- PostToolUse는 edit-scoped formatter/style/repo feedback이지 full-suite proof가
  아니다. Tracked hook JSON은 provider host가 실제로 consumed했음을
  자동 증명하지 않으며, explicit command evidence를 대체하지 않는다.
- `pre-commit run --all-files`도 GitHub event, branch protection, path filter,
  remote permission, 또는 live Kubernetes/Argo CD/Vault/ESO 상태를 증명하지
  않는다.

### QA Evidence Lane Matrix

| Evidence lane | Active local owner / command | What it proves | What it does not prove | 2026-07-10 verdict |
| --- | --- | --- | --- | --- |
| Formatting | `.editorconfig`; `.prettierrc.json`; `.prettierignore`; `trailing-whitespace`, `end-of-file-fixer`, `mixed-line-ending`; `shfmt`; `git diff --check` | configured editor/Prettier policy와 ignore scope, hook이 실제 실행한 file hygiene, shell formatting, pending diff whitespace 상태 | Prettier config 존재만으로 Prettier 실행, semantic correctness, Markdown policy 전체, live readiness | Configured; Prettier의 pre-commit/CI 실행 wiring은 확인되지 않음 |
| Linting | `markdownlint-cli2`, `shellcheck`, `actionlint`, `zizmor`, `hadolint`, `kube-linter` hooks | 각 도구 범위의 style/static anti-pattern | compiler/runtime 성공, 모든 security issue | Implemented; hook/file scope와 도구 가용성에 한정 |
| Syntax / parse | Automated data/manifest: `check-yaml`, `check-json`, `check-toml`, `validate-k8s-manifests.sh`의 PyYAML parse. Shell: CI/QA guide의 수동 `bash -n <script>`와, matching shell edit 뒤 실행되도록 세 provider JSON에 선언된 shared `post-validate.sh`/`lifecycle-guard.sh`의 repository-wide `bash -n` | data/manifest parser 통과와, 실제 수동 또는 shared-hook 실행이 검사한 shell 파일의 grammar 통과 | Kubernetes schema/admission, application behavior, 실행하지 않은 shell syntax, 또는 tracked JSON만으로 provider host가 hook을 native consumption했다는 사실 | Data/manifest parse는 wired. Shell syntax는 explicit manual/shared-hook evidence이며 dedicated CI job, repo-quality, harness command가 아님; provider consumption은 Unverified |
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
  도구다. Shell의 `bash -n`은 CI/CD QA guide에서 수동 단일 파일 명령으로
  실행할 수 있고, tracked provider JSON은 matching shell edit 뒤 shared
  `post-validate.sh` 또는 Stop/SubagentStop의 `lifecycle-guard.sh`가 호출될 때
  repository-wide `bash -n`을 실행하도록 선언한다. 이는 dedicated GitHub CI
  job이 아니며 `validate-repo-quality-gates.sh`나 `validate-harness.sh`의 command도
  아니다. 수동 실행 또는 shared-hook 결과가 기록되지 않았거나 provider host의
  wiring consumption이 확인되지 않으면 automated/native shell syntax evidence로
  승격하지 않는다.
- `pre-commit run --all-files`는 hook matrix를 재현하지만 GitHub event context,
  branch policy, path-filter result, remote permission/ruleset을 재현하지 않는다.

### Document Maturity Gap Register

아래 항목은 조사 결과와 권고다. 이 작업은 나열한 활성 owner를 변경하지
않는다.

| Gap | Classification | Severity | Risk rationale | Recommendation | Canonical follow-up |
| --- | --- | --- | --- | --- | --- |
| 20개 Spec 중 16개가 `draft`, 0개가 `done`인 반면 Stage 04 Task 43개 전부가 `done` | Implementation gap | High | 실행 완료 evidence가 parent contract의 lifecycle 성숙도로 환류되지 않아 독자가 current/complete contract를 잘못 판단할 수 있다. | feature lineage별 Spec/Plan/Task를 대조해 human-approved lifecycle promotion 또는 명시적 잔여 gap을 기록하는 별도 audit를 제안한다. | `docs/99.templates/support/sdlc-governance.md`; 각 Stage 03 Spec/Stage 04 Task; 새 scoped Spec/Plan/Task |
| Release 전용 template/route/readiness record가 없고 tag workflow는 changelog preview artifact만 생성 | Implementation gap | High | release 승인, artifact identity, SBOM/provenance, promotion/rollback evidence가 하나의 추적 가능한 contract로 묶이지 않는다. | Release document가 필요한지 먼저 architecture/governance decision으로 결정하고, 채택 시 route/template/CI/operations를 하나의 변경 단위로 설계한다. | `docs/99.templates/support/{sdlc-governance,template-routing}.md`; `.github/workflows/generate-changelog.yml`; 새 PRD/ARD/ADR/Spec/Plan/Task |
| 실제 Incident/Postmortem record와 tabletop exercise evidence가 0개 | Unverified | Medium | 사건이 없었다는 사실과 대응·학습 절차가 연습됐다는 사실을 구분할 수 없다. 가짜 incident 문서를 만들면 오히려 evidence가 오염된다. | 별도 승인된 tabletop exercise 계획과 synthetic 표기를 갖춘 evidence 방식을 설계하고 실제 사건 folder와 혼동하지 않도록 한다. | `docs/05.operations/incidents/README.md`; incident/postmortem templates; 새 Spec/Plan/Task 및 운영 runbook |
| lifecycle handoff가 링크·review 중심이고 semantic trace completeness 자동 검사가 제한적 | Implementation gap | Medium | PRD requirement에서 Task validation까지 ID coverage가 빠져도 단순 link 존재 검사만으로는 누락을 찾기 어렵다. | 기존 route gate를 변경하기 전에 lineage ID와 상태 전이 invariant를 정의하고 fixture 기반 validator proposal을 평가한다. | `docs/99.templates/support/sdlc-governance.md`; `scripts/validate-repo-quality-gates.sh`; 새 Spec/Plan/Task |
| GitHub Actions `uses:`가 version tag이고 full-length commit SHA가 아님 | Implementation gap | High | 공식 secure-use 지침의 immutable action source 보장을 충족하지 않으며 upstream tag 이동 위험이 남는다. | action pinning과 update automation의 failure mode를 검토한 별도 CI security hardening proposal을 만든다. | `.github/workflows/*.yml`; `.github/dependabot.yml`; Stage 00 approval boundary; 새 Spec/Plan/Task |
| Prettier configuration/ignore policy는 있으나 pre-commit/CI execution wiring이 확인되지 않음 | Needs strengthening | Low | 개발자별 수동 실행 여부에 따라 configured formatting policy와 실제 결과가 달라질 수 있고, config 존재만으로 enforcement를 오판할 수 있다. | 적용 대상과 기존 Markdown/shell formatters의 중복·충돌을 평가한 뒤 Prettier를 수동 도구로 유지할지 별도 hook/CI gate로 승격할지 결정한다. | `.prettierrc.json`; `.prettierignore`; `.pre-commit-config.yaml`; `.github/workflows/ci.yml`; 새 scoped Spec/Plan/Task |

### Implementation Checklist

- lifecycle·route 변경은 Stage 99 support contract, Stage 00 routing,
  validator, Stage README를 같은 논리 단위로 검토한다.
- CI/hook/tool 변경은 `.github/workflows/**`, `.pre-commit-config.yaml`,
  `.editorconfig`, `scripts/README.md`, CI/CD QA guide와 Task evidence로
  라우팅한다.
- release/provenance 추가는 dedicated decision과 Spec/Plan/Task 없이
  changelog workflow에 암묵적으로 넣지 않는다.
- incident readiness를 검증할 때 실제 incident와 exercise evidence를
  명확히 구분하고 secret·live 명령 경계를 지킨다.
- AI agent는 iteration 중 changed-file/affected-lane를 쓰되 PR/merge 전과
  hook·validator·toolchain·global-format 변경 후에는
  `pre-commit run --all-files`와 skipped/unavailable 기록을 남긴다.
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

Repo-backed sources checked on 2026-07-11 at the fixed base where counts are
stated; current owner wording was also compared with the worktree:

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

- Review cadence: SDLC/template/CI/hook/release/incident contract 또는
  `.editorconfig`, `.prettierrc.json`, `.prettierignore` 변경 시.
- Last reviewed: 2026-07-11
- Next review trigger: lifecycle transition change, release route/template
  decision, incident exercise/record creation, validator scope change,
  `.editorconfig`, `.prettierrc.json`, `.prettierignore` change, or any of the
  11 external source revisions.
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
