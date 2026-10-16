---
title: "r13 Residual Control Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0115-TSK-0005"
parent_ids: ["SPEC-0115-PLAN-0001"]
---

# Task: r13 Residual Control Execution

## Overview

Execute the user's four separately bounded residual requests through
[VAL-R13-006–009](../spec.md#success-criteria--verification-plan) and
[WORK-014–017](../plan.md#work-breakdown). The completed
[Tasks 0001](tsk-0001-r10-local-remediation.md),
[0002](tsk-0002-r13-follow-up.md),
[0003](tsk-0003-r13-residual-verification.md) and
[0004](tsk-0004-r13-protection-and-integration.md) retain their historical
evidence and criterion decisions. This Task owns the new common-source/local
C04/C08, native host, additional live and remote SHA-pinning observations.
Each criterion has a separate acceptance decision below.

## Inputs

- The user's current 2026-10-16 request authorizes continuing the four named
  residuals. The clean starting `main` was
  `c49aa468b6d24a511cfb9420f8c56cb09ae5ce0d`; work began on
  `codex/r13-residual-hardening`. The request does not approve a new WGOV
  edition, four-repository adoption, host mutation without an exact operator
  decision, live mutation, or a claim that same-App PR-editable jobs are
  independently protected.
- `WORK-014` concerns only the already approved `WGOV-CORE / 3.0.0` original
  and remaining C04/C08 local applicability. The prior C07 local acceptance
  remains complete. A later source-tree check reproduced the original 67-path
  digest. The four-file `adopted` worktree proposal passed bounded source
  checks and independent semantic review, but integrated staged QA and this
  criterion decision remain pending; prior C07 acceptance is unchanged. C04/C08 purpose labels come from the original first-edition Spec,
  not independent numbered clauses in `standards.md`.
- `WORK-015` began with an AppArmor candidate, dry parse and exact user
  approval. The earlier Task 0003 `bwrap` startup failure remains historical.
  Native automatic review denied a privileged preflight, then the user's broad
  listing and absent-path/source digest checks supplied bounded preflight
  evidence. The first truncated `dd` failed without naming an output target;
  a later full-path operator application and independent installed file
  stat/digest passed. Nonprivileged Codex sandbox startup and bounded
  read-only, workspace, outside-path, network and child-context probes passed
  on their explicit inputs. Independent final outcome review and integrated
  staged QA remain pending; default CLI mode is not claimed writable.
- `WORK-016` covers only the explicitly selected additional read-only live
  checks on the verified `k3d-hyhome` cluster context. EVD-014–019 record the
  four named leaves, two router HEADs and ESO metadata. The first ingress TLS
  failure and one unchanged-input retry PASS remain separate evidence. These
  selected resource and router checks do not establish authentication,
  traffic isolation, deployment of this branch or whole-cluster health.
- `WORK-017` covers the server-side Actions `sha_pinning_required=true`
  hardening and compatible hosted checks. The exact target is
  `buenhyden/hy-home.k8s/actions/permissions`, with only
  `sha_pinning_required` changing from `false` to `true`; Actions remain
  enabled, allowed actions remain `all`, default token permission remains
  read-only and workflow PR approval remains disabled. The current workflow's
  seven external uses were checked for full-SHA compatibility and security
  review passed before the remote setting operation. Admin before/after GETs
  confirmed a single-field false-to-true change with other Actions and
  main-protection fields unchanged. Compatible hosted CI on a new input
  remains unobserved. The absence of
  an independent reviewer and same-App candidate-job forgery risk from Task
  0004 remain separate HIGH limits; a SHA-pinning setting cannot erase them.
- The four rows are first recorded `in-progress` because their scoped
  work has begun. Their selected source, host, live and remote observations
  are recorded separately, while independent final review, integrated QA,
  hosted compatibility and criterion decisions remain pending. No row is
  terminal in this first record.
- On 2026-10-16, after an independent read-only review of this Task at main
  `f208a8c2` (EVD-040, EVD-042), the operator decided all four criteria:
  accept VAL-R13-006 as already applied on `main` by `92849f15` (PR #151),
  accept VAL-R13-007 with its bounded wording and recorded host residual risk,
  accept VAL-R13-008 within its selected scope, and accept VAL-R13-009 after
  recording the hosted run that resolves EVD-011 (EVD-043). The `adopted`
  Registry value described above as a worktree proposal is now the merged
  `main` state. The earlier bullets above are the first-record snapshot; their
  pending statements and the "seven external uses" count are superseded by
  EVD-039–051.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-014 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | Authenticate the approved original and decide/apply local C04/C08 applicability | platform and common owner | completed | PASS | EVD-001 authenticates the original; EVD-013/023–027/031 cover consumers, forms, the adopted delta and the parent-guard repair; EVD-035/036 failures are resolved by EVD-038 integrated staged QA; EVD-039 records the owner's acceptance of the merged `adopted` state |
| WORK-015 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | Prepare native AppArmor input, obtain host decision and verify isolation | native and host operators | completed | PASS | EVD-028/029 preflight, EVD-032 install resolving EVD-030, EVD-033/034 bounded startup and explicit-mode isolation, EVD-038 integrated QA over those rows and EVD-040 independent final outcome review with the recorded host residual risk |
| WORK-016 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | Run and classify the additional selected live checks | GitOps and live operators | completed | PASS | EVD-014–019 selected leaves, first TLS failure and same-check retry, router HEADs and ESO metadata; EVD-042 independent evidence review; broader auth/isolation outside scope |
| WORK-017 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | Verify Actions SHA pinning and compatible hosted CI while retaining same-App HIGH limit | CI and repository protection operators | completed | PASS | EVD-008–010 remote change and source compatibility; EVD-043 hosted CI resolving EVD-011; EVD-044 splits EVD-012 into mitigated required-check forgery and the remaining HIGH limits |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Approved core original authentication | `Project-Template` commit `bc5b70556c57198768119f94c287f93c87964482`; `standards.md` section 6 declares 11 governance, 2 prompt, 5 skill, 4 Stage 99 and 45 template paths | PASS | `/root/residual_remote_common` independently expanded the exact Git tree to 67 paths and recomputed UTF-8-sorted path + NUL + raw blob bytes with no trailing NUL, matching the buenhyden-approved `sha256:aa2523943e35908ba24e4e415793f7aa8099de247aa3628ec1678cd6c91725ee`. Full manifest and command receipt are `/tmp/wgov-core-3-bc5b705-manifest.txt`. Local-object authentication resolves source uncertainty for this input without rewriting Task 0003; the earlier connector file URL returned 404, while current authenticated remote commit GET returned 422 | yes | none |
| EVD-002 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Local C04/C08 applicability and acceptance | Existing WGOV 3.0.0 approval, authenticated original and current k8s adapter/consumers; C04/C08 purposes from `bc5b705:docs/03.specs/0157-wgov-core-first-edition/spec.md:47–51` | NOT_RUN | C04 maps source roles/envelope/language/forms to local document-authoring, Stage 99 and language/Markdown readers; Guide/Policy/Runbook H2/states match, while Korean `.agents` and Incident `open` versus local `detected` are explicit local semantics with zoned closure evidence. C08 maps neutral roles/Skills/context to the role registry/common policy and native bindings/projections/provider notes; shared SQLite remains advisory to Task authority. These are purpose labels, not numbered `standards.md` clauses. This Plan carries the sole `Promotion` receipt; EVD-023 preserves the earlier `candidate` form/policy slice, EVD-024 the focused approved-parent Task/Promotion reader and its independent review, and EVD-025 the independently reviewed proposed four-file `adopted` delta. Audit, Research and Data role meanings were added under existing H2s and independently reviewed against the authenticated source; the source Requirements NFR/interface headings and local FR/NFR/IF rows under `Functional Requirements` were appraised for semantic equivalence. The current worktree proposal does not itself accept local adoption. Earlier links-and-owners exited 2 because the MIG-0004 recovery-proof target differed between index and worktree before link evaluation; coherent integrated staged QA and this criterion decision remain pending. Prior C07 acceptance is not re-decided | yes | none |
| EVD-003 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Native AppArmor preparation | Official AppArmor 4.0.1 source commit `b0eb95457bc2de401920308869d016e696c73664`; candidate `/tmp/r13-native-apparmor-zjtAiR/bwrap-userns-restrict` SHA-256 `11d39094f044f0cda0febb3ad517b830301da6b2ce929664af09ee9e4dd264f9` | PASS | Native owner reported `apparmor_parser -Q -K` exit 0 on the candidate; the named artifact was hashed read-only. This is source review/dry parse only: no host load, policy effect or sandbox isolation observation | yes | none |
| EVD-004 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Scoped host mutation approval | User reply `call_9a263291621743adb4eaea7800815240/0`; exact EVD-003 candidate, `/etc/apparmor.d/bwrap-userns-restrict` root-owned mode `0644`, selected kernel profile add and isolation tests | PASS | User approved host application and isolation validation; supervisor reconfirmed current approval with no revocation message. Executor `/root/residual_native_check` is assigned. Collision preflight and separate privilege-policy review still precede mutation; approval is not evidence of application | yes | none |
| EVD-005 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Loaded-profile collision preflight | Attempted `sudo -n /usr/sbin/aa-status --profiled` on the approved host before any profile application | DEFER | Native automatic review rejected privilege escalation before command launch, so no loaded-profile observation exists. Installed `aa-status --help=legacy` confirms `--profiled` is supported, correcting an initial interpretation, but its count alone would not prove collision-free names. A supported filtered host operator listing must establish that state before mutation; valid user approval is unchanged | yes | none |
| EVD-006 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Nonprivileged loaded-profile query | `aa-status --show=profiles` without privilege | FAIL | The query exited 4 for insufficient access, so it could not substitute for EVD-005's required collision preflight. No profile load occurred | no | none |
| EVD-007 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Native sandbox isolation | Approved host input after collision-free EVD-005 resolution, `codex sandbox -- /usr/bin/true` and bounded read/write/network isolation probes | NOT_RUN | Actual host sandbox startup and isolation have not been tested after an approved policy change; Task 0003's `bwrap` failure remains the latest runtime observation | yes | none |
| EVD-008 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Remote Actions permission baseline | Admin read-only GET of `buenhyden/hy-home.k8s/actions/permissions` at `2026-10-15T23:51:34Z`, actor `buenhyden`, main `c49aa468` | PASS | Remote owner saved `/tmp/r13-actions-sha-before-jwfqo_by.json` mode `0600`: Actions enabled, `allowed_actions=all`, `sha_pinning_required=false`, default token read-only and workflow PR approval disabled; `main` strict `ci-summary`/`style-pr` App `15368`. A second pre-PUT GET matched this snapshot | yes | none |
| EVD-009 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Actions SHA-pinning after-state | Expected EVD-008 snapshot; structured PUT of only `sha_pinning_required=true`; after GET at `2026-10-15T23:51:56Z` | PASS | `/root/ci_commit_range` performed the user-authorized setting update and saved `/tmp/r13-actions-sha-after-e_i_kmxc.json` mode `0600`. GET read-back showed `sha_pinning_required=true` as the only changed field; enabled/all/default-token-read/no-workflow-approval and main strict App-bound contexts, administrator/conversation enforcement, review count zero, no-force/no-delete remained unchanged. This is remote setting evidence, not hosted compatibility or independent producer proof | yes | none |
| EVD-010 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Current workflow SHA compatibility | Current workflow's seven external `uses:` references and the proposed server-side full-SHA requirement | PASS | Source owner found all seven references pinned to full SHAs; security review accepted this bounded compatibility basis. Static source review does not prove the remote after-state or a future hosted run | yes | none |
| EVD-011 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | SHA-pinning hosted compatibility | Actual PR/merge revision after EVD-009, named `ci-summary` and `style-pr` jobs and leaves | NOT_RUN | A new hosted input and its named leaf results remain pending; earlier PR #149 runs do not test this changed server setting | yes | none |
| EVD-012 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Independent workflow producer | PR-editable workflow/inline metadata projection and same-App required jobs under solo operation | DEFER | Server-side SHA pinning constrains external Action identities, not candidate-authored workflow logic or an independent reviewer. The same-App candidate-job forgery HIGH risk remains with the CI/repository protection owner | no | none |
| EVD-013 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Adopted-stage local extension consumer | Current `scripts/document_contracts.py` and focused tests for Task first-recording and Spec/Plan direct approval under `candidate` and `adopted` | PASS | Source writer reproduced two RED tests over six adopted cases, then kept the exact declared extension strings active in both stages; the final focused module passed 17/17 tests, with Ruff check/format and diff check passing. A historical lifecycle test used a test-only current-language projection without changing historical lifecycle fields. An absent-binding fixture initially errored on `REGISTRY_LIFECYCLE_DOMAIN` (4 run, 1 ERROR); removing an invalid draft-to-approved extension edge from that fixture made the same four tests PASS without changing the source guard. Source/test patch `/tmp/r13-adoption-consumer-c49aa468.patch` SHA-256 `f1b7792d2063677bc9c672597de6966bec669d87f3c16bb3999ed371f1cfdf7b`; fixture patch `/tmp/r13-shared-binding-fixture-c49aa468.patch` SHA-256 `c6936ebc2d84bff7451daf4d7cd6dce1f207799c45c81f5faed68e10da088222`. A missing-language source fallback was rejected by native auto-review and was not applied. These focused results are not full-core adoption or full-repository QA | yes | none |
| EVD-014 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Selected cluster leaf | Clean `main` `c49aa468`; explicit `/home/hyunyoun/.kube/config`, `k3d-hyhome` confirmed; `KUBECONFIG` set to that path for `bash infrastructure/verify/verify-cluster.sh` | PASS | Live operator reported rc 0: four nodes Ready, MetalLB Ready and pool `172.18.0.240-172.18.0.250`. Read-only selected verifier output, not whole-cluster or current-branch deployment proof | yes | none |
| EVD-015 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Selected ESO leaf and metadata | Same explicit kubeconfig/context; `bash infrastructure/verify/verify-secrets.sh` and narrow JSONPath GET for `vault-backend` ClusterSecretStore and `argocd/argocd-external-valkey` ExternalSecret | PASS | Verifier rc 0 on readiness/reference fields only. ClusterSecretStore Ready=True transition `2026-10-15T23:38:18Z`; ExternalSecret Ready=True transition `2026-10-14T19:46:09Z`, refresh `2026-10-15T22:46:07Z`. No Secret value or actual OpenBao authentication exchange was inspected | yes | none |
| EVD-016 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Selected NetworkPolicy leaf | Same explicit kubeconfig/context; `bash infrastructure/verify/verify-network-policies.sh` | PASS | Live operator reported rc 0 for named NetworkPolicy objects and selected CIDRs/ports; this object check does not prove actual traffic isolation | yes | none |
| EVD-017 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Selected ingress TLS leaf | Same explicit kubeconfig/context; first `bash infrastructure/verify/verify-ingress-tls.sh` including CA-verified fallback HTTPS HEAD for `argo.hy-k8s.home.arpa:443` through `172.18.0.240` | FAIL | First run rc 1 at the fallback HEAD. Trust versus reachability cause was not established; preserve this first observation. A bounded exact fallback `curl -fIsS --max-time 5 --cacert secrets/certs/rootCA.pem --resolve argo.hy-k8s.home.arpa:443:172.18.0.240 --output /dev/null --write-out 'http_code=%{http_code}\n' https://argo.hy-k8s.home.arpa:443` returned rc 0 / HTTP 200 before one unchanged script retry | yes | none |
| EVD-018 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Selected ingress TLS leaf | Same kubeconfig/context rechecked as `k3d-hyhome`; one unchanged `bash infrastructure/verify/verify-ingress-tls.sh` retry after EVD-017 | PASS | Live operator reported rc 0; the script expressly skipped the router probe, which is recorded separately in EVD-019. This later same-check result resolves the observed first failure without identifying its cause or erasing its historical receipt | yes | EVD-017 |
| EVD-019 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Router CA-verified HTTPS HEADs | Same CA and `curl -fIsS --max-time 5 --cacert secrets/certs/rootCA.pem --resolve` with router `192.168.0.14`: `https://argo.hy-k8s.home.arpa` and `https://hy-k8s.home.arpa/argo` | PASS | First HEAD rc 0 / HTTP 200; second rc 0 / HTTP 301 with redirect matching `https://argo.hy-k8s.home.arpa/`. Only status and redirect match were printed, no raw headers or body. Observation clock after router and ESO checks: `2026-10-15 23:38:58 UTC`. No auth, traffic isolation, deployment SHA or full `run-all` claim | yes | none |
| EVD-020 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Anchored-name operator listing | Trusted user terminal reply `call_322637d6357f4f23a4d604a3b83de514/0`, anchored `bwrap`/`unpriv_bwrap` loaded-profile filter | PASS | User relayed 110 loaded profiles overall and zero matching profiles in each enforce, complain, prompt, kill and unconfined mode under that narrower filter. Independent security review found that a path-named `/usr/bin/bwrap` attachment could be missed. This is bounded user-relayed observation, not broad collision clearance, native privileged-query success, application or isolation proof | no | none |
| EVD-021 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Independent operator handoff review | Canonical 3,089-byte `Native operator handoff` H3 body SHA-256 `4100246882a909a667e31927ca121aecd83dc6cbc98914fe5fa9212485b314bf` (inclusive heading through before next H2), broad `bwrap` filter and SHA-gated no-clobber install/rollback sequence | PASS | `/root/solo_security_review` reviewed the corrected section after its two must-fixes and approved the procedure for the authorized scope. This is document procedure review only; no privileged command, host load or isolation probe ran | yes | none |
| EVD-022 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Advisory role-boundary limit | `/root/solo_security_review` self-report during public AppArmor package inspection | FAIL | The same security reviewer reported downloading public package material to `/tmp` outside its assigned read-only role; it did not install or execute that package. This procedural boundary lapse does not invalidate the static review result, but role enforcement and native host isolation are not proven by it. The scratch files remain untouched pending their owning disposition | no | none |
| EVD-023 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Local C04 form and policy projection | Earlier nine-file `candidate` slice before EVD-025: `.agents/governance/{document-authoring,document-lifecycle}.md`; `docs/99.templates/{registry.json,README.md}`; Plan and AD forms; Audit, Research and Data forms | PASS | Exact SHA-256s, respectively: `ea10a36a4214c955ed62b41a7f96cecf9f203e70e740264c2e803d2b0aa8c173`, `7119d2a8b9ea1d920ec96a9385634557617857a639728d0f390e1c3b7d80a216`, `81c3907576e493f100387987e70c106e92ecd5a3ca34e9f7885b8f248f7294a8`, `6dc72ef1e612fc65a314a6c3f19e7ddc6ab95e98206f9a1fce335149ce9ed815`, `dbf948e6d068359e8c84b62b2787add27999a5decc6c89c6421d7b0bc1d94a54`, `a0ec946a99342b92537813f9de6d323ab1a6d841493b37166ede7caf1a5200fd`, `99ff0d41f7856c4552510b14068a6c76bb2f30800ffbec75ea4c6e6d0a858e6a`, `0889170a0eea7ba4cd5b7c07182be915072de4e1009343add3644614cbe4601e`, `2c8c06a0dc223a177bcb0493a40493f99c0e03addc64884ab8ce1518a8a8e023`. Strict Registry selection PASS 959/0 and selected Markdown PASS 0, reference-pack/shared-binding tests 14/14 PASS, JSON parse/diff check PASS. `/root/final_reconciliation_review` approved this frozen semantic slice against authenticated `bc5` source. That reviewed input was the earlier `candidate` slice; the later proposed `adopted` delta is separate EVD-025. Whole changed-index QA and local acceptance are unclaimed | yes | none |
| EVD-024 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Parent execution and Plan Promotion reader | `scripts/validate-document-lifecycle.py` SHA-256 `07c7d462ec123ab82942218cefeb2d7741bbb5eba7ff53568eda0196d0d7e38d`, `scripts/document_lifecycle.py` `bbe6726bf8a72b0fc44149d47521b44a1db1239add31e1811c709257510876ae`, `tests/test_task_execution_contract.py` `f7d8417914a9bb158aba164bf6610ef857f98a80c13fc6c194afcf47993791f9` | PASS | Owner ran pinned Python `AdoptedExecutionParentTests` and `LifecycleItemTests`: rc 0, 6 tests; Ruff check/format and diff check rc 0. Disposable current-Registry completed SPEC-0114 index with linked Spec constraints and exact sole `none` Promotion returned completion rc 0; missing Promotion returned rc 1 `PLAN-PROMOTION`. Direct current SPEC-0115 Plan/Task5 local guard found zero issues while Spec/Plan are approved and Task5 blocked. `/root/final_reconciliation_review` independently approved these exact three source/test digests and the concrete three-owner Plan receipt. Integrated index QA remains pending; no full historical module PASS is claimed because an unrelated PRE_P03 fixture raised KeyError | yes | none |
| EVD-025 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Proposed local adopted-stage delta | Four current worktree files: `docs/99.templates/registry.json`, `docs/99.templates/README.md`, `.agents/governance/document-authoring.md`, `.agents/governance/document-lifecycle.md` | PASS | SHA-256s respectively `4784a97992293d39e85596eeefbb0cf77f8eaa46c48bacb371104b008b66c681`, `8d5ebd57e61547326083cec3e954cb9794bfc6314066404c30cbc10d188a969c`, `834c789d4bb7c5c232556da46d547a41157aff2960093f3a6eb7bca1b34f5749`, `c47b1a98f0afcf22c0373542b14d53d16d436645660c27757b54d9feb256e9ce`. Governance owner changed only Registry `candidate` to proposed `adopted` plus current prose, preserving exact local extension strings and dated C07 history. Strict Registry 959/0, Markdown 0, shared binding 4/4, JSON parse and diff checks passed on the owned slice; `/root/final_reconciliation_review` independently approved this exact proposed delta. This PASS is source/review evidence only: integrated staged QA and VAL-R13-006 local adoption acceptance remain pending | yes | none |
| EVD-026 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Parent execution guard | Pre-fix `scripts/validate-document-lifecycle.py` SHA-256 `07c7d462ec123ab82942218cefeb2d7741bbb5eba7ff53568eda0196d0d7e38d`; unchanged completed Spec/Plan, newly planted `blocked` Task/Work row, then same Task/Work ID advanced to `in-progress` | FAIL | `/root/security_review` reproduced `compare_lifecycle` rules `[]` for both new blocked record and subsequent active transition, missing `TASK-PARENT-APPROVAL`; a direct new active Task did trigger that rule. Prior `same_existing_work` accepted any Task/Work row, so a new blocked row bypassed the completed-parent guard. This is a required security finding, not a PASS from EVD-024's narrower focused tests | yes | none |
| EVD-027 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Parent execution guard | Corrected validator SHA-256 `fce7e42e8d32f506c50bf6abaacb0d3390012a94a6e6b3c67a9711c9b13601eb`; focused test module SHA-256 `a8a8d7a40c495acb79543345a841d94fa34cc1f48a424fb9da27f4a7b0f8fdaf`; exact EVD-026 two-step input | PASS | Historical exception now requires the comparison-base Task itself `completed`: new blocked record yields `[]`, subsequent active transition yields `['TASK-PARENT-APPROVAL']`; focused six tests, Ruff and diff check passed. Existing SPEC-0105 Task 0004 remains blocked with bytes preserved; future active/PASS evidence under its completed parents requires fresh currently approved authority. `/root/final_reconciliation_review` independently approved the exact source/test repair; integrated staged QA remains pending | yes | EVD-026 |
| EVD-028 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Loaded-profile collision preflight | Trusted user reply `call_14c34db83d464e219b1fa7397592bb39/0` to the security-reviewed broad `bwrap` profile filter | PASS | User relayed 110 loaded profiles overall and zero broad `bwrap` matches in each filtered mode. This operator observation resolves the missing broad collision evidence in EVD-005; native automatic privileged query itself remains denied and this is not profile installation or isolation proof | yes | EVD-005 |
| EVD-029 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Host target and source preflight | Trusted user reply `call_6a416ded4f5a43dab50974b1e03cceeb/0` on all four EVD-021 handoff paths and `/tmp/r13-native-apparmor-zjtAiR/bwrap-userns-restrict` | PASS | All four target/disable/local paths returned absent, including links; source SHA-256 matched exact `11d39094f044f0cda0febb3ad517b830301da6b2ce929664af09ee9e4dd264f9`. The expected `ls` missing-path exit is not an install failure. This is user-relayed preflight, not independent host readback | yes | none |
| EVD-030 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Host profile installation | Trusted user output `call_6a416ded4f5a43dab50974b1e03cceeb/0` and clarification `call_52443077923c48b0afa845645c891187/0`; `sudo dd if=/tmp/r13-native-apparmor-zjtAiR/` | FAIL | The truncated `if=` named a directory, so `dd` failed reading it; it had no `of=` target, and the user stopped at that failed command. This command could not create the target. The overall host state still requires a fresh observation; the exact full-path no-clobber install and EVD-007 runtime test remain unrun | yes | none |
| EVD-031 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Completed-parent policy clarification | `.agents/governance/document-lifecycle.md` SHA-256 `c75ae4893a47ab6fd1ee2fb6c5e5f929395a3047756515603e86d44f5a24c6b3` after EVD-026/027 | PASS | Current policy states that a follow-up record below completed parents does not itself authorize execution: new active `ready`/`in-progress` and actual execution require currently approved owning Spec/Plan; historical compatibility applies only to a previously completed Task's same work/evidence receipt. `/root/final_reconciliation_review` and `/root/security_review` approved this scoped clarification. Existing SPEC-0105 Task 0004 bytes remain unchanged; integrated staged QA and local adoption decision remain pending | yes | none |
| EVD-032 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Host profile installation | Trusted user terminal reply `call_9a67fbee021348159f35869276403a8f/0` after full-path operator procedure; installed `/etc/apparmor.d/bwrap-userns-restrict` read-only stat/SHA by native owner as uid 1000 | PASS | User relayed 112 loaded profiles, exactly `bwrap` and `unpriv_bwrap` in enforce mode and zero matches in other modes. Independent nonprivileged file read returned `root:root`, mode `0644`, 1,936 bytes and SHA-256 `11d39094f044f0cda0febb3ad517b830301da6b2ce929664af09ee9e4dd264f9`, matching approved EVD-003. This later installation observation resolves EVD-030's failed truncated attempt; it does not establish isolation probes | yes | EVD-030 |
| EVD-033 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Native sandbox startup | Nonprivileged uid 1000, installed EVD-032 profile, `codex sandbox -- /usr/bin/true` | PASS | Native owner observed exit 0 and empty stdout. Outer scoped `require_escalated` was needed to launch the host CLI after prior outer `bwrap` failures; the inner Codex sandbox launched. Startup alone does not prove read/write, network, child capability or label enforcement | yes | none |
| EVD-034 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Native sandbox isolation | Installed EVD-032 profile; host uid 1000; explicit `sandbox_mode="read-only"` and `sandbox_mode="workspace-write"` inner Codex sandbox probes with unique temporary names | PASS | Explicit read-only `/tmp` exclusive create exited 1 EROFS and left no file. Explicit workspace-write repo-root unique file and dedicated `/tmp` file each wrote/read/auto-cleaned rc 0 with no residue. Host `/var/tmp` was DAC-writable (mode 1777), but inner workspace-write exclusive create exited 1 EROFS and exact probe path remained absent; `socket.socket()` exited 1 EPERM. Inner child uid 1000, AppArmor `bwrap//&unpriv_bwrap (enforce)`, `CapEff=0000000000000000`, Seccomp 2 and netns `net:[4026539666]`. Default CLI mode separately had `/tmp` and repo `ST_RDONLY` and a temp write EROFS, so no default workspace-write claim. Outer default nested CLI hit an app-server socket mode-0700 setup error; scoped outer launch only enabled the inner probe, which observed enforcement. This bounded result resolves EVD-007, not all possible paths, protocols or runtime configurations | yes | EVD-007 |
| EVD-035 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Selected staged QA | First normal 19-path atomic commit attempt, exact index tree `32b57d2314f6d200ad766830e26e136c7d582fe5`; pinned `/tmp/hyhome-r10-validation/bin` hook chain | FAIL | Staged QA selected 14 gates: 12 emitted PASS, while `repository-quality` failed rc 1 and `selected-nonstyle` failed rc 2 because detect-secrets exited 3. Focused repository-quality diagnostic found 13 non-author multiline form comments across AD/Audit/Data/Research/Plan templates and six missing useful Author prompts at AD System Overview & Context, Audit Reference Type, Research Reference Type/Sources and Data Reference Type/Scope. Independent security review found detector baseline metadata drift only: the staged Registry finding moved from line 6994 to 6996, while all eight finding identities and plugin/filter/version data remained unchanged; no new content finding or tool failure was found. The one-token baseline correction was not present in this failed index. Normal pre-commit exited 1, no commit was created; exact 19-path index/staged tree restored with zero unstaged edits at failure observation. This required aggregate failure remains open until a later actual selected staged QA PASS on corrected input | yes | none |
| EVD-036 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Selected staged QA | Second normal 20-path commit attempt, exact index tree `041dd860fe2f674ac5e56331060a8b9c3d43ce37`; five corrected forms and one-field `.secrets.baseline` SHA-256 `cae90289eea489408ddcf65f8c0995ef748a44ff4e0583fd0b2cc39835560d60` included | FAIL | Staged QA selected 14 gates: 13 PASS, including `repository-quality`, `document-lifecycle`, `links-and-owners`, `markdown-profiles` and `selected-style`; only `selected-nonstyle` failed rc 2 because nested detect-secrets exited 3. The hook aggregate exited 1 with no commit, then restored exact 20-path index and zero unstaged diff. Read-only producer inspection found the nested detector uses the trusted HEAD baseline instead of the same commit's staged baseline; the corrected metadata could not take effect while bundled with Registry. Native `git commit --only --dry-run -- .secrets.baseline` showed a baseline-only commit candidate, but `scripts/qa.py` and `scripts/run-validation-lane.py` use a closed environment and read the canonical index, so `--only` alone would not narrow the actual QA snapshot. This required aggregate failure remains open until an actual corrected-source normal selected QA PASS | yes | none |
| EVD-037 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Baseline metadata prerequisite | Native index-only unstaging of the other 19 paths without worktree changes; baseline-only index tree `6e04d7fdde16ca9d94793f76e38eb6d3c7321987` and normal commit `19375b55810a02547d1812c535935386b263016d` | PASS | The sole committed change was existing Registry detector finding `line_number` 6994 to 6996; eight finding identities and detector plugin/filter/version data remained unchanged per independent security review. Normal baseline-only `Validate Staged QA Snapshot`, `commitizen check`, and generated commit-message exception hooks each passed; both hook stash operations restored the 19 remaining source paths. Post-commit index was empty, all 19 intended source edits remained in the worktree, and Task SHA-256 `09e7adff0aa88aafc81cdfb9b8b14d51fa1ae356f58bb032c76ee0cd4c14cb08` was unchanged. This proves only the prerequisite metadata commit, not resolution of EVD-035 or EVD-036 or local adoption | yes | none |
| EVD-038 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Selected staged QA | Third normal 21-path commit attempt over baseline commit `19375b55`, exact index tree `87f342dbcc609af069f329deaea736bc987f50eb`; pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | An intermediate attempt on tree `584dae0a` without the pinned venv failed `markdown-profiles` rc 1 `TASK-ACCEPTANCE-EVIDENCE` (blank lines split this Task's evidence table) and `selected-style`/`selected-nonstyle` rc 2 because `pre_commit` was unavailable to the default interpreter; no commit was created. After joining the table rows and restoring the pinned PATH, `Validate Staged QA Snapshot`, `commitizen check` and generated commit-message exception hooks passed and produced commit `92849f15`. This corrected-source PASS resolves the EVD-035/036 aggregate failures; it is not itself the local C04/C08 adoption decision | yes | EVD-035, EVD-036 |
| EVD-039 | [VAL-R13-006](../spec.md#success-criteria--verification-plan) | WORK-014 | Local C04/C08 applicability and acceptance | Operator decision on 2026-10-16 after EVD-038 and the EVD-040 review; merged `main` state from `92849f15` (PR #151, merge `26508fe2`) with Registry `stage: adopted` | PASS | buenhyden, the common-source and local adapter owner, accepted the applied local C04/C08 adoption. The integrated staged QA is EVD-038 (tree `87f342db`); the later Task-only commit `0b70a8ea` passed normal staged QA without a separate row. Prior C07 acceptance is unchanged and no new edition or four-repository adoption is inferred | yes | EVD-002 |
| EVD-040 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Independent final outcome review | Fresh read-only `security-auditor` review of this Task at `f208a8c2`, plus a read-only stat/SHA-256 of the installed profile and the kernel userns sysctl | PASS | EVD-032–034 support the criterion: the inner `codex sandbox` on direct host invocation is confined (`bwrap//&unpriv_bwrap (enforce)`, `CapEff=0`, seccomp 2, separate netns, EROFS/EPERM probes); the installed file is still mode `0644` with SHA-256 `11d39094…64f9`. EVD-033/034 were byte-identical in tree `87f342db`, so EVD-038 is their integrated QA. Bounds: the agent's default nested path still fails (outer escalation was needed), so no claim that agent sessions are sandboxed by default; default CLI mode is not claimed writable. Host residual risk: the profile grants `/usr/bin/bwrap` `allow userns` and capabilities host-wide with a stacked `unpriv_bwrap` child while the kernel keeps `apparmor_restrict_unprivileged_userns=1`, an upstream-designed relaxation for every bwrap caller; the host operator owns it and the rollback is the Native operator handoff below. EVD-022 `/tmp` scratch residue remains with the host operator | yes | none |
| EVD-041 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Criterion decision | Operator answer on 2026-10-16 to the EVD-040 bounded wording and host residual risk | PASS | The operator, as host and native owner, chose to record the residual risk and accept rather than remove the profile | yes | none |
| EVD-042 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Independent evidence review | Same `security-auditor` review at `f208a8c2` against EVD-014–019 and `infrastructure/verify/verify-ingress-tls.sh` at `c49aa468` | PASS | The first-failure/retry pair is correctly bounded: the fallback HEAD runs unconditionally, so EVD-018 re-ran the failed leaf, and the router HEADs of EVD-019 are a separate row because the script skips that probe by default. Noted limits: a read-only diagnostic curl ran between EVD-017 and EVD-018; the ClusterSecretStore Ready transition at `23:38:18Z` was about 40 s before the only recorded clock (`23:38:58 UTC`); no per-leaf timestamps were recorded. The operator accepted the criterion within its selected scope | yes | none |
| EVD-043 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | SHA-pinning hosted compatibility | PR #151 `pull_request` run `38856426542` on final head `0b70a8ea`, created `05:33:48Z` on 2026-10-16 after the EVD-009 after-state | PASS | `ci-summary` job `116828803833` succeeded, including branch metadata and PR title/commit-range validation; `style-pr` job `116828803546` succeeded, including base binding, pinned runner install and lint/format. Greeting, Labeler and the `26508fe2` main push run also succeeded. Protection then was the EVD-009 state. The workflows held six external `uses:` in `ci.yml` and eight across all three files, all full SHAs, correcting EVD-010's count without changing its conclusion | yes | EVD-011 |
| EVD-044 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Required-check forgery mitigation | SPEC-0116 Task 0001 and the 2026-10-16 main protection record | PASS | Since `07:03:24Z` `main` also requires `independent-review` from review App `5341483`, whose key no workflow holds; PR #152 was observed `BLOCKED` without it and `CLEAN` with it. This mitigates only same-App required-check forgery. The absent independent human reviewer stays HIGH, because the gate's reviewer is an AI agent under the same solo operator, and the PR-editable workflow body stays owner-accepted HIGH per SPEC-0105 Task 0004. EVD-012 is kept as history | no | none |
| EVD-045 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Actions SHA-pinning read-back | Operator-run `gh api` of `actions/permissions` at `2026-10-16T08:22:11Z` | PASS | `enabled: true`, `allowed_actions: all`, `sha_pinning_required: true`: the EVD-009 setting is unchanged after the PR #151 run of EVD-043 | yes | none |
| EVD-046 | [VAL-R13-007](../spec.md#success-criteria--verification-plan) | WORK-015 | Host residual risk level | Operator decision on 2026-10-16 using the risk-report matrix on the EVD-040 residual | PASS | The host-wide bwrap userns relaxation is **MEDIUM**: likelihood Possible (the relaxation is in force, no misuse observed), impact Moderate (single-user development host). Monitor-only; review cue: an AppArmor, bwrap or kernel userns sysctl change, or an added host user, any of which reopens the rating. Owner: host operator; rollback in the Native operator handoff below | yes | none |
| EVD-047 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Actions credential retirement | Operator-run read-only inventory at `08:22:11Z` and retirement script with before `08:24:26Z` and after `08:24:33Z` read-backs as user `9127269` | PASS | Deleted the unused repository secret `GHCR_TOKEN`, five retired `QA_*` variables and the `qa-control`/`qa-tag-publish` environments with their retired App keys; removed retired publisher App `5156559` from ruleset `24342332` bypass. After: no repository secret, variable or environment; `24342332` bypass empty; `24769894` keeps the operator as SemVer producer. PAT revocation and deletion of Apps `5156553`/`5156559` are operator UI actions not observed here | yes | none |
| EVD-048 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Workflow-body risk regrade | Operator decision on 2026-10-16 after EVD-047, recorded in the main protection record | PASS | The PR-editable workflow body is regraded from HIGH to **MEDIUM** (Possible × Moderate): no credential remains reachable from a same-repository PR workflow, and its token cannot change `main`, protected tag patterns or `independent-review`. Review cue: a new repository secret or access-granting variable, an environment without a `main`-only policy, a workflow requesting write permissions, or a new collaborator. The absent independent human reviewer stays HIGH. This supersedes the workflow-body HIGH wording of EVD-044 | yes | none |
| EVD-049 | [VAL-R13-008](../spec.md#success-criteria--verification-plan) | WORK-016 | Criterion decision | Operator answer on 2026-10-16 after the EVD-042 review | PASS | The operator, as GitOps and live owner, accepted the selected leaves and router HEADs within their stated scope | yes | none |
| EVD-050 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Criterion decision | Operator answer on 2026-10-16 after EVD-043–045 | PASS | The operator, as CI and repository protection owner, accepted the SHA-pinning hardening with compatible hosted CI; required-check forgery is mitigated (EVD-044) and the remaining limits are those of EVD-048 | yes | none |
| EVD-051 | [VAL-R13-009](../spec.md#success-criteria--verification-plan) | WORK-017 | Retired credential revocation | Operator report on 2026-10-16 after EVD-047 | PASS | The operator reported revoking the personal access token behind the deleted `GHCR_TOKEN` and deleting the retired GitHub Apps `5156553` (verifier) and `5156559` (publisher) in the GitHub UI. This is an operator report; no API read-back of the token or App deletion was taken | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-R13-006](../spec.md#success-criteria--verification-plan) | accepted | EVD-001, EVD-002, EVD-013, EVD-023, EVD-024, EVD-025, EVD-026, EVD-027, EVD-031, EVD-035, EVD-036, EVD-037, EVD-038, EVD-039 | Original authenticated, consumers and forms reviewed, the parent-guard bypass repaired, integrated staged QA passed and the owner accepted the merged `adopted` state. EVD-002 is resolved by EVD-039, EVD-026 by EVD-027 and EVD-035/036 by EVD-038. No new edition or four-repository adoption is inferred | buenhyden, common source and local adapter owners |
| [VAL-R13-007](../spec.md#success-criteria--verification-plan) | accepted | EVD-003, EVD-004, EVD-005, EVD-006, EVD-007, EVD-020, EVD-021, EVD-022, EVD-028, EVD-029, EVD-030, EVD-032, EVD-033, EVD-034, EVD-040, EVD-041, EVD-046 | Accepted on bounded wording: approved profile installed and the inner sandbox on direct host invocation confined in explicit modes. Default CLI write behavior and default agent-session sandboxing are not claimed. The host-wide bwrap userns relaxation is a MEDIUM residual risk (EVD-046) owned by the host operator, with rollback in the handoff below; EVD-022 remains an advisory lapse | host operator, native owner and security reviewer |
| [VAL-R13-008](../spec.md#success-criteria--verification-plan) | accepted | EVD-014, EVD-015, EVD-016, EVD-017, EVD-018, EVD-019, EVD-042, EVD-049 | Accepted within the selected leaves and router HEADs; EVD-017 is resolved by EVD-018 and EVD-042 records the intervening diagnostic curl and ESO transition timing. Authentication, traffic isolation, deployment SHA and whole-cluster assurance are not claimed | GitOps and live operators |
| [VAL-R13-009](../spec.md#success-criteria--verification-plan) | accepted | EVD-008, EVD-009, EVD-010, EVD-011, EVD-043, EVD-044, EVD-045, EVD-047, EVD-048, EVD-050 | SHA pinning was set and re-read true (EVD-045), and compatible hosted CI passed on a new input; EVD-011 is resolved by EVD-043. Required-check forgery is mitigated by SPEC-0116 (EVD-044). After the credential retirement (EVD-047) the PR-editable workflow body is MEDIUM (EVD-048); the absent independent human reviewer stays HIGH | CI and repository protection operators |

## Approval and Safety Boundaries

- **Allowed Paths**: The owning Spec/Plan/Task package and explicitly assigned
  source/consumer files for each domain owner; read-only source, live and
  remote inspection under the current request.
- **Forbidden Paths**: Terminal Tasks 0001–0004, sealed Archive payloads,
  credentials, private memory, unapproved host mutation, cluster mutation,
  unreviewed remote setting changes and unsupported common-edition claims.
- **Approval Required**: The user's current four-lane request identifies the
  intent and bounded topics. The later user reply
  `call_9a263291621743adb4eaea7800815240/0` specifically approved the
  EVD-003 artifact for `/etc/apparmor.d/bwrap-userns-restrict` root-owned mode
  `0644`, selected kernel profile add and isolation tests by
  `/root/residual_native_check`. The supervisor found no revocation message.
  Separate privilege-policy review and preflight remain required before the
  privileged action. Native automatic review denied the attempted privileged
  listing before launch; no host application is implied by the user approval.
  The user's current improvement request covers the reviewed
  `buenhyden/hy-home.k8s/actions/permissions` SHA-pinning setting only;
  `/root/ci_commit_range` owns the exact remote PUT/read-back after current
  target/revocation preflight. No standing approval or independent reviewer is
  inferred from solo operation.
- **Static Validation**: Selected Stage 99 profile, relationship, link and
  lifecycle checks on the actual document index; focused source and consumer
  tests for each implemented lane, with independent review before delivery.
- **Live Validation**: Only the named read-only cluster/ESO/NetworkPolicy/TLS
  and router checks belong to WORK-016. Host-native runtime isolation is a
  distinct approved lane; neither is certified by repository-static QA.
- **Secret / Vault Handling**: Record context, object metadata and tool result,
  not kubeconfig contents, Secret values or private data.
- **Rollback Plan**: Revert only a reviewed local source delta through Git.
  Before host application, inspect loaded-profile collision, target path and
  disable symlink; stop on any conflict. If a newly applied host profile fails,
  unload it and remove only the newly created file. Do not change sysctl,
  setuid or global AppArmor disable state. Remote setting owners keep exact
  before snapshots. Reverting `sha_pinning_required=true` to `false` weakens
  the control, so a failed PUT/read-back freezes the operation and reports to
  the user; any later rollback requires an exact operator decision rather
  than an automatic false write. Preserve failed observations.
- **Evidence Location**: This Task owns four separate acceptance decisions;
  raw provider, cluster and remote logs remain with their producing owners.

### Native operator handoff

These are proposed commands for the user-approved host operation, **not an
execution receipt**. The source is the 1,936-byte AppArmor 4.0.1 profile at
`/tmp/r13-native-apparmor-zjtAiR/bwrap-userns-restrict`, expected SHA-256
`11d39094f044f0cda0febb3ad517b830301da6b2ce929664af09ee9e4dd264f9`.
The target is only `/etc/apparmor.d/bwrap-userns-restrict`. The profile can
affect every `/usr/bin/bwrap` user and includes broad setup allowances before
its child restrictions; independent security review of this exact handoff is
required before the operator uses it. Execute each line separately in the
operator's terminal; stop on any unexpected result and do not share a password.

Preflight: the broad `bwrap`-filtered listing must show zero loaded matches.
All four `ls` paths must be absent, including links (`ls` exit 2 is
expected only when all four are absent). The source digest must match exactly.

```sh
sudo /usr/sbin/aa-status --show=profiles --filter.profiles='bwrap'
sudo ls -ld /etc/apparmor.d/bwrap-userns-restrict /etc/apparmor.d/disable/bwrap-userns-restrict /etc/apparmor.d/local/bwrap-userns-restrict /etc/apparmor.d/local/unpriv_bwrap
sha256sum /tmp/r13-native-apparmor-zjtAiR/bwrap-userns-restrict
```

Only after all preflight expectations and the independent security review
hold, install without overwriting an existing target. Check owner, mode and
installed digest before parsing, then check that only `bwrap` and
`unpriv_bwrap` are loaded in enforce mode. `conv=excl` is the no-clobber
condition; a failure stops the sequence.

```sh
sudo dd if=/tmp/r13-native-apparmor-zjtAiR/bwrap-userns-restrict of=/etc/apparmor.d/bwrap-userns-restrict conv=excl status=none
sudo chown root:root /etc/apparmor.d/bwrap-userns-restrict
sudo chmod 0644 /etc/apparmor.d/bwrap-userns-restrict
sudo stat -c '%U:%G %a %n' /etc/apparmor.d/bwrap-userns-restrict
sudo sha256sum /etc/apparmor.d/bwrap-userns-restrict
sudo /sbin/apparmor_parser -Q -K /etc/apparmor.d/bwrap-userns-restrict
sudo /sbin/apparmor_parser -a -K /etc/apparmor.d/bwrap-userns-restrict
sudo /usr/sbin/aa-status --show=profiles --filter.profiles='bwrap'
```

If the newly installed profile must be removed, first compare its SHA-256 to
the exact approved source. Only when it matches, unload it and confirm zero
loaded matches with the broad filter **before** removing the newly created
file. On a digest mismatch, remaining loaded profile or any failed step, stop
for investigation and preserve the input file without automatic deletion.

```sh
sudo sha256sum /etc/apparmor.d/bwrap-userns-restrict
sudo /sbin/apparmor_parser -R -K /etc/apparmor.d/bwrap-userns-restrict
sudo /usr/sbin/aa-status --show=profiles --filter.profiles='bwrap'
sudo rm -- /etc/apparmor.d/bwrap-userns-restrict
```

After installation, separate Codex sandbox startup and bounded read-only
deny, workspace allow, outside-workspace deny, network deny, and child
`CapEff`/label probes remain required before claiming native isolation. This
handoff changes no sysctl, setuid flag, trust store, rule or other profile.

## Verification Summary

All four criteria are accepted by the operator on 2026-10-16 after an
independent read-only review. VAL-R13-006: the approved original's 67-path
digest was reproduced, integrated staged QA passed (EVD-038) and the owner
accepted the merged `adopted` state (EVD-039). VAL-R13-007: the approved
AppArmor profile is installed and the inner sandbox on direct host invocation
is confined in explicit modes; default agent-session sandboxing is not
claimed, and the host-wide bwrap userns relaxation is a recorded residual risk.
VAL-R13-008: the selected live leaves and router HEADs pass within their
scope, with the first TLS failure, the retry and the intervening diagnostic
kept. VAL-R13-009: SHA pinning was set, re-read true at `08:22:11Z`
(EVD-045), and compatible hosted CI passed on PR #151 (EVD-043).
Required-check forgery is now mitigated by SPEC-0116. After the unused
`GHCR_TOKEN` and retired QA credentials were removed (EVD-047), the
PR-editable workflow body is MEDIUM with a review cue (EVD-048), the host bwrap
relaxation is MEDIUM (EVD-046), and the absent independent human reviewer
stays HIGH. The rows are recorded `completed`; the
criterion decisions above are the acceptance.
