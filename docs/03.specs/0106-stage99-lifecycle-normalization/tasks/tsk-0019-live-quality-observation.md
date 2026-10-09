---
title: "Current Live Quality Observation"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0019"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Current Live Quality Observation

## Overview

This Task owns [WORK-019](../plan.md#work-breakdown) and one decision for
[VAL-P08-019](../spec.md#success-criteria--verification-plan). Authorized
read-only operator observations preceded this Task's authorship; their real
times and results are adopted below. The user's later request also retires
the former HA PostgreSQL K8s consumers, keeps Valkey cluster excluded, and aligns the local
contract with actual Docker management/development services. The parent Spec
and Plan and completed
[P08 Task0018](tsk-0018-operations-quality-and-architecture.md) remain
completed. This draft records inputs and a prospective local source change;
it is not acceptance of every product quality scenario or permission to run a
new protected operation.

## Inputs

- [REQ-0004](../../../01.requirements/0004-current-local-gitops-platform.md)
  remains in-review and owns the six scenarios, measures, environments and
  undecided thresholds. Active
  [AD-0007](../../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
  owns the current single-host topology, source paths and evidence limits.
  Proposed [ADR-0049](../../../02.architecture/decisions/0049-external-data-service-contract-alignment.md)
  identifies the partial ADR-0044/0046 data-service amendment; the proposed
  creation is not itself acceptance or live reconciliation.
- Operator receipts are in ignored checkout-root
  `_workspace/residual-controls/`: `live-observations.json` (SHA-256
  `c7160d35c0f06606fbf40dab785cc0e1bc8d036820b9a92c7f3031bb35d3adae`),
  `live-extra-observations.json` (`063f30401cc99b7e255c49a871232c143bfadb5a065e73331cc6e57c95fd2171`),
  `adminer-declared-tls-route.json`
  (`aceaeeb0982da06eb8c3c3b597fe4acbff497917264179010b9f2331cad8dc7b`),
  and `live-numeric-observations.json`
  (`0a754a6512b911d5baf32d8e0e9ebc2b7ca3b454205710e63fcd7b4ad83c3266`).
  Subsequent `prometheus-runtime-observations.json` and
  `data-environment-observations.json` record the authorized operator
  telemetry and Docker metadata samples at 05:36 UTC.
  Their companion `.stdout.txt` files hold the observed non-secret values.
  These hashes identify inputs, not approval or an immutable archive.
- The operator selected Kubernetes context `k3d-hyhome`; status reads ran at
  2026-10-09 05:13:07–08 UTC with a 15-second request timeout. Repository-backed
  Argo applications reported revision
  `3793510b04d77d3548145d89a934ed5e3888301e`; chart-backed entries
  reported chart versions. Later host/TLS and numeric reads occurred at
  approximately 05:26–05:29 UTC. The receipts retain individual command,
  target, exit status, response and stdout digest.
- No credential was read. The public Prometheus gateway redirected both
  unauthenticated requests; an already authorized Docker operator transport
  then returned the selected non-secret numeric Prometheus samples. Its result
  does not validate public-gateway authentication. Any future protected
  operation requires its own operator authority and evidence.
- Tracked external `hy-home.docker` source in
  `infra/04-data/{mng-db,dev-db}/docker-compose.yml` distinguishes
  `mng-valkey`'s default LAN `192.168.0.13:26379` → container `6379`,
  `mng-pg`'s host-loopback `127.0.0.1:25432` → `5432`, `dev-pg`'s
  host-loopback `127.0.0.1:25433` → `5432`, and `dev-valkey`'s Docker-only
  `dev_data_net:6379` with no host publish. The K8s
  source at the earlier observation revision had required management Valkey
  plus `15432/15433` opt-in `postgres-ha`/`pg-router` tuples. The current
  unaccepted local source removes those PostgreSQL tuples and retains only
  management Valkey under `gitops/platform/external-services/`. Neither the
  historical tuples nor localhost PG are a new K8s PG endpoint.
  Source and Docker metadata observations remain separate from authenticated
  SQL, Valkey protocol or in-cluster reachability evidence.
- At the earlier live-observation revision, the
  [Adminer Rollout](../../../../gitops/workloads/adminer/rollout.yaml) set
  `ADMINER_DEFAULT_SERVER` to the former HA write `:15432`. The current
  unaccepted local source removes that default, without redirecting it to
  management/development PostgreSQL. The older UI HTTP 200 and Rollout
  Healthy sample did not demonstrate a DB login or query, and no later live
  reconciliation or DB result is claimed.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-019 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | Bind dated observations to six REQ-0004 scenarios and align current local K8s consumers with Docker management/development services; preserve unmeasured recovery and public-gateway boundaries | platform | frontmatter | NOT_RUN | EVD-P08-019-001, EVD-P08-019-002, EVD-P08-019-003, EVD-P08-019-004, EVD-P08-019-005, EVD-P08-019-006, EVD-P08-019-007, EVD-P08-019-008, EVD-P08-019-009, EVD-P08-019-010, EVD-P08-019-011, EVD-P08-019-012, EVD-P08-019-013, EVD-P08-019-014, EVD-P08-019-015, EVD-P08-019-016, EVD-P08-019-017, EVD-P08-019-018 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P08-019-001 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Kubernetes readiness and GitOps snapshot | `k3d-hyhome` `/readyz`, node and Argo Application status at 05:13 UTC; 1 server and 3 agents Ready, API `ok`, 22 Applications Synced/Healthy | PASS | `_workspace/residual-controls/live-observations.json` and companion stdout | yes | none |
| EVD-P08-019-002 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Secret/TLS controller status, not secret contents or recovery | `vault-backend` ClusterSecretStore Ready; six ExternalSecrets Ready; five Certificates Ready at 05:13 UTC | PASS | `_workspace/residual-controls/live-observations.json` and companion stdout | yes | none |
| EVD-P08-019-003 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | External desired tuples and host reachability | At the earlier source revision, six EndpointSlice tuples existed; TCP accepted Loki 3100, Tempo 3200, Alloy 4317/4318, required management Valkey 26379 | PASS | `_workspace/residual-controls/live-extra-observations.json`, `live-numeric-observations.json`, `external-endpoints.stdout.txt` | yes | none |
| EVD-P08-019-004 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Preserve former HA PostgreSQL connection observation | At the earlier source revision, desired EndpointSlice tuples included opt-in `postgres-ha`/`pg-router` write 15432/read 15433, but host TCP connections to both were refused; profile/runtime applicability was not established. This did not test `mng-pg` or `dev-pg`. | FAIL | `_workspace/residual-controls/live-numeric-observations.json` | no | none |
| EVD-P08-019-005 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Declared Adminer route and Rollout | At the earlier source revision, `apps/adminer` Rollout was Healthy, ready/desired 1/1; declared `adminer.hy-k8s.home.arpa` returned HTTP 200 with TLS verification success, body discarded. Rollout source then defaulted DB server to former HA write `:15432`; no DB login/query result was observed. | PASS | `_workspace/residual-controls/live-observations.json`, `adminer-declared-tls-route.json`, former `gitops/workloads/adminer/rollout.yaml` at reported source revision | yes | none |
| EVD-P08-019-006 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Preserve wrong-target response | Undeclared `adminer.hy.home.arpa` returned HTTP 404; the corrected declared route in EVD-P08-019-005 returned 200. The 404 is not a failure of the declared service. | PASS | `_workspace/residual-controls/live-extra-observations.json` | no | none |
| EVD-P08-019-007 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Host recovery prerequisite and Loki readiness | Host inotify watch limit 1024; Loki `/ready` HTTP 200 | PASS | `_workspace/residual-controls/live-extra-observations.json` | yes | none |
| EVD-P08-019-008 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Direct non-secret log aggregate | Loki `sum(count_over_time({cluster="k3d-hyhome"}[5m]))` HTTP 200, vector value 2749 | PASS | `_workspace/residual-controls/live-numeric-observations.json` | yes | none |
| EVD-P08-019-009 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected Argo CD telemetry numeric sample | External public Prometheus `up{cluster="k3d-hyhome",namespace="argocd"}` and `count(argocd_app_info{cluster="k3d-hyhome"})` both returned HTTP 302 without credentials; this transport yielded no series values | DEFER | `_workspace/residual-controls/live-numeric-observations.json` | yes | none |
| EVD-P08-019-010 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Recovery-duration and threshold handoff | No failure injection, rebuild or first-failure-to-first-healthy timing; REQ-0004 thresholds remain owner decisions | DEFER | [REQ-0004](../../../01.requirements/0004-current-local-gitops-platform.md); no operator receipt | no | none |
| EVD-P08-019-011 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Management/development interface source and runtime metadata review | At the earlier source revision, tracked Docker Compose and K8s interface source showed management Valkey LAN 26379 as required ArgoCD target; management PG loopback 25432, development PG loopback 25433, development Valkey Docker-only 6379; optional HA PG 15432/15433 was separate. At 05:36 UTC all four Docker containers reported Up 18 hours (healthy); both localhost PG ports accepted TCP. No `pg-router` appeared in selected container metadata. | PASS | `hy-home.docker/infra/04-data/{mng-db,dev-db}/docker-compose.yml`, former `gitops/platform/external-services/{valkey-external,postgres-external}.yaml` at reported source revision, `_workspace/residual-controls/data-environment-observations.json` | yes | none |
| EVD-P08-019-012 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected Argo CD telemetry numeric sample | At 05:36 UTC authorized Docker operator transport returned five declared Argo CD component `up` samples, all value 1, and `count(argocd_app_info{cluster="k3d-hyhome"})` value 22; no credential file or secret read | PASS | `_workspace/residual-controls/prometheus-runtime-observations.json` | yes | EVD-P08-019-009 |
| EVD-P08-019-013 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected document checks and independent semantic review | The then-scoped document inputs awaited root-owned selected checks and review at intake; no result was asserted then | DEFER | This Task; root's pending QA/review receipt | yes | none |
| EVD-P08-019-014 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected document checks and independent semantic review | Actual links-and-owners check on the staged source failed: the Adminer Rollout relative link resolved under `docs/gitops`, and the two implementation README routers used disallowed deep AD targets. Preserve this failing source observation; repaired links require a new check on changed inputs. | FAIL | `_workspace/residual-controls/source-staged-qa-fail.json`, SHA-256 `7ccce692f75bf4a5e1bfb267caa466a7cdfcd68cb6034ebd20a538d9a16ea72c`; `links-and-owners-diagnostic.json`, SHA-256 `527c7f3120eb9c2fee103661b305142b1e7d9a6b7f24bc24c53e92ce90475358`; log SHA-256 `0f97946899bd0f08342d38158a328977cd0da40fe429ff56abda03d70078842e` | yes | none |
| EVD-P08-019-015 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected document checks and independent semantic review | The same staged QA run rejected new Task0019 creation from absent directly to `in-progress`; `sdlc/task` requires its first tracked state to be `draft`. The Task now starts at draft, while the earlier operator observations retain their actual times and results. A new check on committed draft input must resolve this failure. | FAIL | `_workspace/residual-controls/document-lifecycle-diagnostic.json`, SHA-256 `f94012a5c8d1d52998cc2fab03372287414954b02db2562cf2eb6deca911fd86`; `_workspace/residual-controls/source-staged-qa-fail.json`, SHA-256 `7ccce692f75bf4a5e1bfb267caa466a7cdfcd68cb6034ebd20a538d9a16ea72c` | yes | none |
| EVD-P08-019-016 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected document checks and independent semantic review | At source index tree `96cf651343e7eabb00a9895783d011f70eef50b5`, 10 of 11 selected gates passed, but `markdown-profiles` rejected this newly drafted Task's first row `DEFER`: a draft Task row must use `NOT_RUN`. The earlier live PASS rows remain received inputs; no operator observation is reset. This failure predates the user's HA/cluster retirement extension and awaits changed-input QA. | FAIL | `_workspace/residual-controls/corrected-source-staged-qa-fail.json`, SHA-256 `0de0d916b41e5f342f7772964fc87ca53bbdf436ce950f82c99d320002daa9b4`; `corrected-source-markdown-diagnostic.json`, SHA-256 `396a4d8e094667f41aa764a561f5969292d03b6657ca5a9c1e35582bf2bdfaf8`; prior log SHA-256 `20f5d3483c610db9a3c2372c5da3c39d27526b31c2abe3cf7243036578a8e2e1` | yes | none |
| EVD-P08-019-017 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | External contract source and consumer focused review | At local base `32be232908da7cff71ff1003349407fb2a2993da` and tracked Docker revision `77a80bc1478c3dfb46cfe8b8de97aa971817c494`, the assigned implementation removed the HA PostgreSQL manifest/consumer while preserving management Valkey and observability tuples. Its author observed 3/3 focused RED then 3/3 GREEN, 9/9 owned-module PASS, three Bash syntax checks and Ruff checks; independent network-reviewer read-only review returned PASS for current port/bind alignment. The receipt lists exact eight changed-file hashes. This is focused local source evidence, not final exact-index QA, remote merge or live reconciliation. | PASS | `_workspace/residual-controls/external-alignment-implementation-review.json`, SHA-256 `edcbbc597e86461a56fce39f10e8d5b145bd2a680c15886ce5de72d0c38286b3` | yes | none |
| EVD-P08-019-018 | [VAL-P08-019](../spec.md#success-criteria--verification-plan) | WORK-019 | Selected document checks and independent semantic review | At staged source tree `725e5f8cd90f7add8729f82503806550f95f9b0d`, 20 selected gates passed and `markdown-profiles` failed with `DOC-MATRIX-PARITY` for both current GitOps README matrices. The unchanged reader still expected retired PostgreSQL write/read and former `postgres-app-secret` rows. The source consumer must change to the new current row set; restoring retired rows would misstate the user's contract. No final source QA PASS is claimed. | FAIL | `_workspace/residual-controls/external-alignment-staged-qa-fail.json`, SHA-256 `cca17ffa16b0e47047383694669d6c51f023f0c31f9d5ec76e89a0fd5bda5a3d`; `external-alignment-markdown-diagnostic.json`, SHA-256 `28995d9ee071df897bb66b6165870c75628d3df9beeb9b88267946b70a1260c1` | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-P08-019](../spec.md#success-criteria--verification-plan) | pending | EVD-P08-019-001, EVD-P08-019-002, EVD-P08-019-003, EVD-P08-019-004, EVD-P08-019-005, EVD-P08-019-006, EVD-P08-019-007, EVD-P08-019-008, EVD-P08-019-009, EVD-P08-019-010, EVD-P08-019-011, EVD-P08-019-012, EVD-P08-019-013, EVD-P08-019-014, EVD-P08-019-015, EVD-P08-019-016, EVD-P08-019-017, EVD-P08-019-018 | Preserve the dated observations and the current source retirement as distinct inputs. EVD-P08-019-012 resolves only the selected numeric telemetry DEFER, not public-gateway authentication. EVD-P08-019-017 supports focused implementation/review, not final QA. EVD-P08-019-013 through -016 and -018 remain required pending/failing document checks until a changed-input PASS explicitly resolves them. Accept local source/consumer alignment only after selected checks and independent review; actual ArgoCD reconciliation and live removal require later operator evidence. Recovery and product thresholds remain separate REQ-owned handoffs. | platform for local contract acceptance; operator for live reconciliation; REQ-0004 Platform Owner with Security Reviewer, external service owner and application owner for undecided thresholds |

## Approval and Safety Boundaries

- **Allowed Paths**: This Task, its owning `spec.md` and `plan.md`,
  [RUN-0001](../../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md),
  [POL-0001](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md),
  [POL-0007](../../../05.operations/policies/0007-app-gitops-onboarding-policy.md),
  [AD-0007](../../../02.architecture/descriptions/0007-current-local-gitops-platform.md),
  [ADR-0049](../../../02.architecture/decisions/0049-external-data-service-contract-alignment.md)
  and its [decision router](../../../02.architecture/decisions/README.md),
  [GitOps router](../../../../gitops/README.md) and
  [infrastructure router](../../../../infrastructure/README.md). The user's
  current local source change also authorizes separately owned
  `gitops/platform/external-services/{kustomization.yaml,postgres-external.yaml}`,
  `gitops/platform/network-policies/apps-egress.yaml`,
  `gitops/workloads/adminer/rollout.yaml`,
  `infrastructure/{bootstrap-local.sh,verify/verify-external-services.sh}`,
  `scripts/validate-infrastructure-contracts.sh`,
  `tests/test_infrastructure_tempfiles.py` and
  `.agents/skills/external-service-contract-audit/references/external-service-contracts.md`;
  document, manifest and script writers keep distinct file ownership. The
  six non-secret operator receipts and external Docker Compose source above
  are read-only inputs.
- **Forbidden Paths**: Secret values, Vault/private credential files, live
  cluster mutation, Docker bind or credential changes, remote deployment and
  frozen archive bodies.
- **Approval Required**: The received operator observations were authorized
  and executed before this Task was written. Further public-gateway auth or
  protected query needs its own operator approval and target/revision check;
  this Task does not supply that approval. Fault injection, restart, deploy, remote write and
  server configuration change are outside this execution.
- **Static Validation**: Selected Stage 99 task/profile, relationship, link,
  lifecycle and Markdown style checks, plus affected manifest/script consumer
  checks on final local inputs; root owns commands, exact index snapshots and
  result receipts. Earlier failures remain in EVD-P08-019-014 through -016;
  current changed-source acceptance is pending.
- **Live Validation**: EVD-P08-019-001 through -008 and -011/-012 are bounded
  received observations at the older source revision. Public-gateway requests
  redirected (EVD-P08-019-009),
  then the selected numeric values were obtained through an authorized
  operator transport (EVD-P08-019-012). The newer source has not been
  reconciled or observed in-cluster; ArgoCD automatic prune and the actual
  retired-resource state remain operator-owned DEFER. Recovery duration was
  not exercised (EVD-P08-019-010).
- **Secret / Vault Handling**: No credential or secret-value read or output.
  An authorized platform operator owns the future authenticated query.
- **Rollback Plan**: If local source alignment is rejected before integration,
  reverse the scoped manifests/scripts/docs as a reviewed logical change.
  Any later live rollback requires a separately authorized operator plan;
  preserve original receipt bytes and completed prior Tasks.
- **Evidence Location**: This Task records the acceptance decision and
  references ignored checkout-root `_workspace/residual-controls/` receipts.
  The checkout scratch is not a durable archived proof; the owner must retain
  an approved non-secret evidence location before relying on it after cleanup.

## Verification Summary

The received snapshots at the earlier source revision support API, node, Argo, secret-controller,
Certificate, Adminer Rollout, declared Adminer TLS, external tuple, selected
host port, Docker container metadata, Loki and Prometheus numeric observations
at their stated times. These are status, response and aggregate samples only;
the Docker operator transport does not prove the public gateway's auth path.
The user's subsequent local source retirement is a different input and has no
post-change live PASS. Scenario disposition against REQ-0004:

| Scenario | Dated observation and current local source | Remaining measurement or owner |
| --- | --- | --- |
| GitOps reproducibility | 22 Applications Synced/Healthy at observed revisions | Static selected-target render completeness and repeated reconciliation remain unmeasured; Platform Owner |
| Secret and TLS recovery | SecretStore/ExternalSecret/Certificate Ready status and one declared Adminer TLS success | Recovery time from actual failure, completeness and threshold remain unmeasured; Platform Owner and Security Reviewer |
| External interfaces | At the older source revision, EndpointSlices included optional HA PostgreSQL write/read; management Valkey LAN 26379 accepted TCP, while HA 15432/15433 refused and selected metadata showed no `pg-router`. Both management PG loopback 25432 and development PG loopback 25433 accepted host TCP, with each container healthy; development Valkey was healthy on Docker-only `dev_data_net:6379`, so a host-port probe was not applicable. The newer local source removes HA K8s consumers, keeps Valkey cluster excluded, and retains management Valkey. | Changed-source tuple/consumer checks and later actual ArgoCD reconciliation remain unobserved here; authenticated database/Valkey operation and K8s DB connection are not established. Platform Owner and external service owner |
| Telemetry | Loki ready and 2749 log events in one five-minute aggregate; five declared Argo CD component `up` samples all 1 and labelled application-info count 22 through authorized Docker operator transport | Public gateway returned HTTP 302 without credentials, so its authenticated behavior remains unverified; platform operator owns any separate gateway test |
| Workload onboarding | At the older source revision, Adminer Rollout was ready/desired 1/1 and declared host HTTP 200 with verified TLS while its DB default targeted HA write `:15432`. Newer local source removes that default and supplies no replacement. | The sampled HA port refused TCP and no DB login/query succeeded; newer source has no post-change live result or K8s-to-management/development PG path. Application owner, external service owner and Platform Owner |
| Single-host recovery | One server and three agents Ready; host inotify limit 1024 | Actual rebuild duration and decision threshold remain unmeasured; Platform Owner |

The wrong undeclared Adminer host's 404 and former HA PostgreSQL TCP refusals
remain visible in the factual evidence. Neither replaces the declared Adminer
route result or proves a required platform outage. Dated Docker metadata
and loopback TCP acceptance do not establish authenticated SQL, application
read/write, K8s reachability or recovery. The local retirement change also
does not prove cluster reconciliation or remote deployment. No all-scenario product acceptance,
disaster recovery, public-gateway authentication, native/hosted check or
common edition adoption is claimed here.
