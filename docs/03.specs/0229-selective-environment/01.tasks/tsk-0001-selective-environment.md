---
title: "Selective Validation Environment and Aggregate Resource Boundary Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-23"
artifact_id: "SPEC-0229-TSK-0001"
parent_ids: ["SPEC-0229-PLAN-0001"]
---

# Task: Selective Validation Environment and Aggregate Resource Boundary

## 문서 개요

### 목적과 독자

This Task records P07 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator, reviewers and implementers use it to
distinguish prepared documents from implemented and observed behavior.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0006. This Task owns P07 work state,
results and criterion decisions. The [SPEC-0223 Task](../../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
retains earlier residue and its ledger pointer; P07 may append a matching
closure only after actual evidence.

## 내용 계약

### 입력과 전제

The current human request selects P07-ENVIRONMENT from package
`workspace_governance_remediation_1_1_0_20261120`, authorizing bounded
implementation, validation and commit/push/PR/merge. D07, Q03, current
execution contract, k8s profile/findings and this workspace are inputs.
Intake found branch `codex/p01-ci-routing`, HEAD
`c7ed0be33e60e05294e341b46a395215c4345900` and a clean index/worktree.
P00–P06 and eleven earlier streams are not re-executed. This first draft
records preparation only: neither parent approval nor technical PASS nor
criterion acceptance has occurred for P07.

For one bounded local capability observation, the platform owner separately
checked the current human P07 request and found no revocation in this thread.
The exact target was only Docker container `hyk8s-test-p07quota`, labeled
`hy-home.k8s/run=p07quota`, from the cached `alpine:3.24.3` image. The root
executor created/started it with network `none`, CPU 0.25, memory 64 MiB,
PIDs 32 and `storage-opt size=32M`, then attempted at most 40 MiB of dummy
writes for at most 60 seconds to observe actual `ENOSPC` or unsupported
storage quota behavior. No production endpoint, host mount, Docker socket
inside the container or global daemon setting is part of that operation.
After checking the exact container name and label, the executor deletes only
that container; the task-owned preparation journal is
`/tmp/p07-environment-wwh6mHCV`. EVD-006–EVD-008 record the actual result:
the configured 32 MiB disk limit allowed a 40 MiB write, so hard-cap
enforcement `failed`; owned cleanup passed. This is no permission for
broader host/VM mutation. Aggregate admission was not active during this
small capability probe; it started no product service.

A separate cost-free user-service capability check is prepared under the
same current P07 local-environment request, whose original trusted user
message and absence of revocation were checked by the platform owner. Its
only target is transient user unit `hyk8s-p07-capability` under UID 1000,
using the canonical user bus `/run/user/1000/bus`. The root assistant is
the executor. `systemd-run --user --collect` will set `CPUQuota=200%`,
`MemoryMax=4G` and `RuntimeMaxSec=30`; the pinned validation Python will
read only its own `/proc/self/cgroup` and that cgroup's `cpu.max` and
`memory.max`, then exit. If the exact unit still exists, the executor
stops only that unit and verifies collection. No VM is started, image or
package downloaded, host-global setting changed, or production endpoint
contacted in this check. The actual user unit reported `cpu.max` as
`200000 100000` and `memory.max` as `4294967296`, confirming those two
hard caps for this transient user service. This does not prove VM boot,
guest disk or LAN isolation.
The current explicit user-manager check reported `is-system-running=degraded`
and `Linger=yes`; an earlier failure caused by a missing default user-bus
environment is not evidence that the canonical bus is unsupported. QEMU
8.2.2 is installed, but `/dev/kvm` is inaccessible; TCG and any bounded
VM capability require separate actual observation. The user's lack of
knowledge of an existing VM does not establish one or authorize new root
privileges.

The current P07 environment construction next targets only run token
`p07vm001` under `.workspace-test/p07vm001`, with transient user unit
`hyk8s-test-p07vm001-vm` under UID 1000. The root assistant is executor;
the run expires 600 seconds after its recorded start and one deadline covers
provision, boot and any stop/restart. The unit must set `CPUQuota=200%`,
`MemoryMax=4G`, `MemorySwapMax=0`, `RuntimeMaxSec` to the original remaining
deadline minus five seconds, `TimeoutStopSec=5`, `SendSIGKILL=yes`,
`LimitCORE=0` and `KillMode=control-group`. Before creating the VM unit or
guest files beyond the initial private intent, arm only the owned token's
`hyk8s-owned-p07vm001-${token}.timer` and corresponding `.service` for
expiry cleanup. The timer shares the original 600-second deadline; the
executor records its exact token and unit identities, and stops/removes only
those units and verified files after child/process absence. A failed or
unverified timer arm stops VM creation and retains the run intent for recovery.
This is a planned target, not a runtime PASS. QEMU 8.2.2 uses TCG, two guest vCPUs and
3072 MiB guest memory; no `/dev/kvm` access or host-global setting is
requested. The fixed raw guest disk is 4080 MiB, with approximately
0.52 MiB OVMF_VARS and at most 1 MiB logs/metadata/keys, within a 4 GiB
owned file budget. Conversion has a separate preparation lease while the
source QCOW remains at most 512 MiB. The official Ubuntu 24.04 minimal
2026-11-05 release was checked against the root HTTPS manifest SHA256
`406630c08b5e545fcc7209854b129d47e3af822db128c9f19336593b5a2d3fe0`;
its 72-byte QCOW header reports virtual size 3758096384 bytes. The actual
OVMF_VARS source is 540672 bytes. These observations establish input
identity and size, not a running VM.

Provisioning may download only the verified public image and signed apt
packages before product runtime. The VM network plan is one QEMU user NIC
with `restrict=on`, `ipv6=off`, only loopback host-forwarded SSH and no
guest-forward metadata path. Only current public scripts, GitOps sources and
complete Application declarations may be copied into the guest; no
credentials, provider configuration or `.git` history. The guest creates
a fresh Git repository and records the host input digest. One run-owned
SSH key is generated for this VM only, is consumed without an agent or
private-value log, and is deleted only after the exact owned unit stops.
The executor stops/collects only `hyk8s-test-p07vm001-vm` and deletes only
the verified token's files under `.workspace-test/p07vm001`; the failed
Docker quota result remains in EVD-007. VM boot, guest ENOSPC, LAN deny,
selected readiness and cleanup remain `NOT_RUN` until actually observed.
This preparation is within the current P07/D07 local-environment scope;
it does not authorize a new account, subscription, root privilege or
global host change.

The separate current P07/Q03 actual-model review is prepared as native run
`p07review01`, under the root operator. Before invoking the model, shared
admission reserves kind `native`, empty service closure, 2 CPU, 4096 MiB
memory, 64 MiB disk, 600 seconds and zero product instances, with owned unit
intent `hyk8s-p07-review`. Only a public candidate SHA manifest and scoped
diff packet under `/tmp/p07-environment-wwh6mHCV/review-packet` are inputs;
the adjacent result uses filtered logging. The user unit sets
`CPUQuota=200%`, `MemoryMax=4G`, `MemorySwapMax=0`, `RuntimeMaxSec=600`,
`KillMode=control-group` and `LimitCORE=0`. The single selected path is
Codex CLI 0.169.0, `gpt-6-sol`/high, a fresh read-only parent profile with
root deny, minimal runtime plus executable/packet read, and network false.
It uses no daemon, user config, persistence, hooks, plugins, apps, multi-agent
or host skill discovery; approval mode is never. The process limit is
595 seconds with 5 seconds to kill. The operator ran the initial actual
model review; one follow-up is reserved only after an actual repair. Current
ChatGPT authentication status was rechecked, but no Claude quota call, new
account, subscription or global trust change is part of this plan. The
original trusted P07/Q03 request still covers the selected review and no
revocation was observed. The lease releases only after exact unit and child
absence; result digests and findings remain in this Task, and owned temporary
files are removed after delivery. The initial model process exited 0 after
353.938 seconds, but its source verdict is `FAIL` with four HIGH blockers
recorded in EVD-016. Its model-invoked OS boundary check passed separately
in EVD-017; EVD-018 records owned unit and lease cleanup. One post-repair
review and actual VM remain `NOT_RUN`. Provider charge is `null`/unobserved;
a time bound does not guarantee a dollar amount.

The one allowed post-repair actual model check is prepared as distinct native
run `p07review02`, after the first owned unit was collected. It uses the
same current P07/Q03 trusted request, whose validity and absence of
revocation were rechecked; this is no new parent or criterion approval.
Shared admission reserves kind `native`, empty service closure, 2 CPU,
4096 MiB memory, 64 MiB disk, 600 seconds and zero product instances with
new run token and the same exact unit name `hyk8s-p07-review`. A new public
repair packet under `/tmp/p07-environment-wwh6mHCV/review-packet-repair`
contains the prior four HIGH findings, the source repair diff, the focused
dispatcher and stop-grace consumers, and a candidate SHA manifest. Only
this packet and the installed executable are readable under the fresh
Codex CLI 0.169.0 root-deny/minimal profile; network remains false.
The requested model is `gpt-6-sol`/high using current ChatGPT authentication,
without user config, daemon, hooks, plugins, apps, multi-agent or host skill
discovery. The owned user unit sets `CPUQuota=200%`, `MemoryMax=4G`,
`MemorySwapMax=0`, `RuntimeMaxSec=595`, `TimeoutStopSec=5`,
`SendSIGKILL=yes`, `KillMode=control-group` and `LimitCORE=0`; the model
process is bounded by 595 seconds plus five seconds to kill within the one
600-second run. The root operator releases its lease only after that exact
unit and all children are absent. No Claude call or global user-data change
is planned. Actual second model invocation, verdict and provider charge
were then observed: the process exited 0 after 226.255 seconds, but its
source verdict is `FAIL` with three HIGH and one MEDIUM finding in EVD-021.
The first review's four HIGH findings and startup diagnostics remain
historical facts. Actual provider charge remains `null`/unobserved; no
further model call was started before checking current account metadata and
the new repair scope. VM runtime remains `NOT_RUN`.

One additional finite P07 review is prepared as native run `p07review03`
only after the second review's new lifecycle defects and three related
architecture findings are repaired and a frozen selected QA packet exists.
The root operator verified the installed Codex CLI 0.169.0 stdio
`account/rateLimits/read` response without invoking a model or changing
credentials: ordinary use allowed, existing `prolite` plan, 69% of the
10080-minute weekly window used (31% remaining), no spend control or rate
limit reached and no secondary window reported. Account identifiers are
not recorded. This is evidence of current remaining existing allowance,
not free use or a dollar charge guarantee; EVD-024 records the exact read.
The same current P07/Q03 request remains valid and unrecalled. The third
run uses a new token, shared admission kind `native`, empty service closure,
2 CPU, 4096 MiB memory, 64 MiB disk, 600 seconds and zero product instances.
It reuses the collected unit name `hyk8s-p07-review` with CPUQuota=200%,
MemoryMax=4G, MemorySwapMax=0, LimitCORE=0, KillMode=control-group,
`RuntimeMaxSec` equal to the original remaining deadline minus five seconds,
`TimeoutStopSec=5` and `SendSIGKILL=yes`. A fresh public repair packet at
`/tmp/p07-environment-wwh6mHCV/review-packet-lifecycle` contains only the
new lifecycle repair diff, related affected consumers and source digest.
The same installed CLI, `gpt-6-sol`/high request, fresh root-deny/minimal
read-only packet/executable scope, network false, no daemon/user config,
hooks, plugins, apps, multi-agent or host skill discovery, never approval
and 595+5-second process bound apply. Lease release again requires exact
unit and all children absent. No Claude call or new payment is planned.
The third model process exited 0 after 201.215 seconds, but its source
verdict is `FAIL` with three HIGH lifecycle defects in EVD-025. The
model-invoked read-only boundary and exact owned native cleanup passed
separately in EVD-026–EVD-027; actual provider charge remains
`null`/unobserved. Any further failure requires actual repairs, a current
remaining-limit check and a new finite review scope, not an automatic retry
loop. VM boot, guest ENOSPC, LAN and selected readiness remain `NOT_RUN`.

After EVD-025, the root operator read current installed CLI account metadata
again without a model call or account change. Ordinary use remained allowed
on the existing `prolite` plan; the 10080-minute weekly window was 77% used
with 23% remaining, and no secondary window, spend control or rate limit was
reported. EVD-028 records this actual metadata read; it is neither a free-use
claim nor an observed dollar charge. One finite fourth source review is
prepared as native run `p07review04` only after the three new HIGH durability
defects, affected caller paths and focused regressions are repaired and a
frozen packet exists. It will use the same current P07/Q03 authority and
selected CLI 0.169.0 `gpt-6-sol`/high fresh read-only boundary, no Claude,
reset, payment, global config or credentials change. Shared admission remains
native/empty closure with 2 CPU, 4096 MiB memory, 64 MiB disk, 600 seconds
and zero product instances; the owned `hyk8s-p07-review` unit retains
CPUQuota=200%, MemoryMax=4G, MemorySwapMax=0, LimitCORE=0,
KillMode=control-group, `RuntimeMaxSec` at the remaining deadline minus
five seconds, `TimeoutStopSec=5` and `SendSIGKILL=yes`. The new public
packet `/tmp/p07-environment-wwh6mHCV/review-packet-durability` will include
only the three durability repairs, affected callers, prior review findings
and source digest. The packet/executable-only root-deny/minimal read scope,
network false, no daemon/user config, hooks, plugins, apps, multi-agent or
host skill discovery, never approval and 595+5-second process bound remain.
Lease release still requires exact unit and all children absent. This fourth
model process exited 0 after 203.899 seconds, but its source verdict is
`FAIL` with two HIGH and two MEDIUM findings in EVD-032. The selected CLI
read-only boundary passed separately in EVD-033 and exact owned cleanup
passed in EVD-034. Actual provider charge remains `null`/unobserved.
The two HIGH cleanup proof failures require source repair; no fifth model
review is planned before current remaining-allowance metadata, a frozen
repair packet and a finite scoped rationale are available. VM boot, guest
ENOSPC, LAN and selected readiness remain `NOT_RUN`.

After the EVD-032 defects and affected host lifecycle caller were repaired,
the root operator obtained a fresh cost-free installed CLI account read:
ordinary use allowed on the existing `prolite` plan, 92% of the weekly
10080-minute window used and 8% remaining, no secondary window, spend
control or rate limit reached. EVD-036 records the actual metadata read;
no model, reset, credit purchase, payment, account identifier or provider
charge was observed in that check. The source candidate is frozen with
architect conditional PASS on the affected five source hashes and selected
QA in EVD-037–EVD-038. One finite fifth native run `p07review05` is prepared
to check only EVD-032's two HIGH/two MEDIUM triggers and their affected host
callers/current cap paths. It reuses the same current P07/Q03 authority,
the collected `hyk8s-p07-review` unit, CLI 0.169.0 `gpt-6-sol`/high fresh
root-deny/minimal read-only parent, installed executable plus new public
packet `/tmp/p07-environment-wwh6mHCV/review-packet-final`, network false,
no daemon/user config, hooks, plugins, apps, multi-agent, host skill
discovery or Claude call. Shared admission remains native/empty closure,
2 CPU, 4096 MiB memory, 64 MiB disk, 600 seconds and zero product
instances; the unit retains CPUQuota=200%, MemoryMax=4G, MemorySwapMax=0,
LimitCORE=0, KillMode=control-group, `RuntimeMaxSec` at the original
remaining deadline minus five seconds, `TimeoutStopSec=5` and
`SendSIGKILL=yes`, with 595+5-second process bound. Exact unit and child
absence precedes token-bound lease release. The fifth model process exited
0 after 152.146 seconds. EVD-039 records the actual blocking source
verdict: the previous two HIGH and two MEDIUM findings were resolved, but
a new MEDIUM VM state-identity concurrency gap remains. EVD-040 records
the selected read-only boundary and EVD-041 the exact owned cleanup
separately. Provider charge remains `null`/unobserved, not a dollar cap.
No broad review or automatic further retry is planned without new
authority or external budget facts. Actual VM boot, guest ENOSPC, LAN and
selected readiness remain `NOT_RUN`.

The final VM state/deletion repair delta is classified HIGH under
QUAL-R016, so it requires an actual enforced read-only review of the delta
before runtime. An installed CLI `account/rateLimits/read` response after
EVD-039 showed ordinary use allowed on the existing `prolite` plan, 95% of
the 10080-minute weekly window used and 5% remaining, no secondary window,
spend control or rate limit reached; EVD-042 records this cost-free metadata
read, not a charge guarantee. One finite `p07review06` is planned only after
the source, focused QA and contextual review packet freeze. It checks
EVD-039's state-identity MEDIUM and two directly related lifecycle windows
in the changed three source/QA files; it does not replay the unchanged core
or full 17-file review. The same current P07/Q03 authority applies, with no
new privilege, account, subscription, reset or payment. The collected
`hyk8s-p07-review` unit and installed CLI 0.169.0 `gpt-6-sol`/high use a
fresh root-deny/minimal changed-packet/executable read profile, network
false, no daemon/user config, hooks, plugins, apps, multi-agent, host skill
discovery or Claude call. Shared native admission is 2 CPU, 4096 MiB
memory, 64 MiB disk, 180 seconds and zero product instances. The owned
user unit retains CPUQuota=200%, MemoryMax=4G, MemorySwapMax=0,
LimitCORE=0, KillMode=control-group, RuntimeMax at the original remaining
deadline minus five seconds, `TimeoutStopSec=5` and `SendSIGKILL=yes`;
the CLI has a 175+5-second process bound. Exact unit and child absence
precedes token-bound lease release. The sixth model process exited 0 after
121.855 seconds. EVD-044 records that EVD-039's state-identity defect was
resolved, but a new blocking MEDIUM recovery retry gap remains. EVD-045
records selected tool isolation, and EVD-046 exact review-run cleanup,
separately. Source repair and focused regression for the new gap are
required; no further model call is planned before new cost and scope facts.
Actual VM boot, ENOSPC, LAN and selected readiness remain `NOT_RUN`.

After EVD-044, a fresh cost-free installed CLI account read showed ordinary
use still allowed on `prolite`, 98% of the weekly 10080-minute window used
and 2% remaining, with no secondary window, spend control or rate limit
reached. EVD-047 records this actual metadata read; it does not assert free
use or a dollar charge. One last finite tiny `p07review07` source repair
confirmation is planned only after the known MEDIUM recovery gap is fixed,
focused QA passes and the contextual delta is reviewed. Its packet contains
only the changed recovery function, pure callback/helper interfaces, new
failure tests and EVD-044's verdict; the unchanged five-source/core review
is not repeated. The same current P07/Q03 authority, installed CLI 0.169.0
`gpt-6-sol`/high and fresh root-deny/minimal packet/executable read,
network-false boundary apply without new scope, account, subscription,
reset, payment, global config, hooks, plugins, apps, multi-agent, host skill
discovery or Claude. Shared native admission is 2 CPU, 4096 MiB memory,
64 MiB disk, 120 seconds and zero product instances. The collected owned
`hyk8s-p07-review` unit retains CPUQuota=200%, MemoryMax=4G,
MemorySwapMax=0, LimitCORE=0, KillMode=control-group, RuntimeMax at the
original remaining deadline minus five seconds, `TimeoutStopSec=5` and
`SendSIGKILL=yes`; CLI process bound is 115+5 seconds. Exact unit/child
absence precedes token-bound release. The seventh model process exited 0
after 65.823 seconds. EVD-049 records its nonblocking verdict on the
changed recovery path and explicit closure of EVD-044's MEDIUM; EVD-050
records the selected boundary and EVD-051 exact owned cleanup separately.
The current known source blockers are closed by matching repair evidence;
this is not an actual VM result or formal six-criterion acceptance. Actual
VM boot, ENOSPC, LAN and selected readiness remain `NOT_RUN` until observed.

EVD-048 records the final frozen synthetic checks after the recovery repair:
the registered cluster suite passed 123/123, dispatcher 42/42, validation
routing 173/173 and 748 affected paths had no uncovered or ambiguous route.
The hash-stable focused trace passed 165/165 tests and hit 2998/3643
executable lines (82.3%); its first 69.4% measurement omitted imports and is
invalid. Ruff passed on the changed Python files. These checks do not establish
VM or product runtime behavior.

The planned `p07vm001` operation was attempted through the execution runner
after the source blockers were resolved, with the selected
`platform-network-policies` closure and the 600-second bound. The automatic
approval review rejected the command before execution because the account
usage limit prevented review, with availability stated for 2026-11-27.
No VM unit, image, cluster, product workload or live network probe was started;
EVD-052 records this as deferred, not as a runtime pass or an observed product
failure. The Docker 32 MiB quota probe remains an actual failure (EVD-007),
and the current-context, P06 Desktop→SSH and P12 containment findings retain
their existing owners.

On 2026-11-23 the operator entered `prompts/P07-ENVIRONMENT.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
at `main@fe700f835ec18392e857a476e58a62f6a1110656`, resuming this Task with
bounded implementation, verification and commit/push/PR/merge. Claude Code
ran the unchanged `p07vm001` route once (EVD-053): QEMU started under TCG but
guest SSH never answered before the 600-second deadline, and the owned expiry
timer cleaned up the exact unit and run files (EVD-054). The likely cause is a
source defect: the provisioning NIC forwarded NoCloud metadata through a
`guestfwd` TCP chardev, which carries one stream, while cloud-init opens a new
HTTP connection per file. The operator chose to repair the defect and retry
once with KVM, keeping the 600-second bound, and to grant KVM by a
non-persistent `/dev/kvm` ACL as their own host action. The repair spawns one
bounded loopback relay per guest connection, uses `accel=kvm`/`-cpu host` only
when `/dev/kvm` is readable and writable (TCG otherwise), and sends guest
serial output to the owned unit journal under a 2000-line per-run rate limit
instead of discarding it (EVD-055). Two later reads after the operator
reported running the ACL command still showed no user ACL and no access, so
the single post-repair retry was not started; it is not spent on TCG. The
operator then applied the ACL from a separate terminal, because `sudo` needs
a password there. With KVM the single retry `p07vm002` (EVD-057) booted the
guest, fetched metadata through the relay and reached SSH, confirming the
first repair. It then failed because cloud-init 26.2 counts the deprecated
`nocloud-net` datasource name as a recoverable error, so `cloud-init status
--wait` exits 2. Owned cleanup passed (EVD-058). The seed now uses
`ds=nocloud` (EVD-059), not a weaker exit-code check. The `/dev/kvm` ACL was
absent again after the run (EVD-060), and D07's one retry is spent. The
operator then authorized exactly one more bounded run and reapplied the ACL.
Run `p07vm003` (EVD-061) passed provisioning, cloud-init status and the
restricted reboot, then failed at the in-guest selected `up`: guest-side
shared admission demands the full cluster disk reservation plus a 1024 MiB
margin from a guest whose whole disk is 4080 MiB. This is a design defect in
how admission applies inside the bounded VM, whose own disk is already the hard
cap; changing it alters admission semantics and needs a further authorized
run, so it is handed off rather than repaired here. Owned cleanup passed
(EVD-062). EVD-063 corrects that explanation: the guest already reserves its
own 1024 MiB plus 128 MiB, and the real cause was too little free guest disk.
After the operator asked for the remaining causes to be resolved, four more
KVM runs each passed one more step. Cleaning apt caches gave 1577 MiB free and
the guest ENOSPC check passed (EVD-064, EVD-065), so the supported VM route
enforces the disk cap while EVD-007's Docker route stays a recorded FAIL; the restricted guest could not reach the
host-side endpoint (EVD-066). k3d then needed a recorded gateway on the
isolated network (EVD-067), the gateway check had to tolerate guest Docker
fields (EVD-068), and finally the k3s server did not start within k3d's
180-second wait (EVD-069). All owned cleanups passed (EVD-070) and the repairs
have synthetic PASS (EVD-071). `/dev/kvm` carries udev's `uaccess` tag, so
systemd-logind removes manual ACLs on this seatless host; the operator's
`kvm` group membership is persistent but reaches the user systemd manager that
starts VM units only after its next restart or a host reboot.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for six
[Spec criteria](../spec.md#criteria): current environment and bounded native
routes, aggregate admission, selected k3d, actual LAN isolation, P06
permission carry and focused evidence handoff.

##### Inputs and Authority

The current user P07 message is the scoped request reference. The exact draft
Spec and Plan require a nonauthor review and a current DOCLIFE-R008 receipt
before dependent source implementation. EVD-003 records the exact parent
review and EVD-035 records the current scoped execution request; neither is
formal parent approval or criterion acceptance.

- **Allowed Paths**: [Plan WORK-001](../plan.md#work-units) names the bounded source, test, environment-guide, product-description and current Task/ledger consumers. Its minimal shared admission/environment helper scope includes `scripts/test_cluster_environment.py` as a cohesive module extracted from `scripts/test_cluster.py`. The necessary isolated VM route uses `scripts/test_cluster_vm.py`, with `scripts/test_cluster_vm_transport.py` owning NoCloud/dummy HTTP, SSH/image stream and probe transport, and `scripts/test_cluster_vm_lifecycle.py` owning VM host lifecycle and exact token-bound cleanup through a host-only lazy dependency; these are cohesive physical splits. Focused `tests/test_test_cluster_vm.py`, `tests/test_test_cluster_vm_boundaries.py`, `tests/test_test_cluster_lifecycle.py` and `tests/test_test_cluster_durability.py` split the same cluster lifecycle, VM and native durability regressions; the latter may move cohesive existing native durability cases from the crowded lifecycle module without duplicating fixtures. `scripts/run-contract-tests.py` selects them in the existing `test-cluster` suite. These physical splits add no new wrapper, validation gate, check ID, CLI or behavior criterion.
- **Forbidden Paths**: other repositories, accepted prior implementation, production services/credentials, global trust or payment settings, P08–P17 implementation and deletion of the input package.
- **Approval Required**: the current human P07 request covers draft authoring, bounded implementation, selected checks and ordinary Git delivery. Actual host firewall/VM or cluster mutation needs its exact target, executor, reviewed state, rollback and current operator authority under [approval policy](../../../00.workspace/04.quality/approval-and-safety.md); no such action is approved by this draft.
- **Static Validation**: focused admission and component regressions; strict profile, link, lifecycle and selected affected QA on actual changed files.
- **Live Validation**: controlled network isolation and selected k3d only after the host and authority prerequisites; retain `failed` or `DEFER` when unmet.
- **Secret / Vault Handling**: no credential values, raw authentication files, operating kubeconfig, production endpoint probes or Docker socket passed to reviewers.
- **Rollback Plan**: revert the reviewed implementation commit through normal Git while retaining factual failures and prior P06 evidence; release only verified run-owned resources.
- **Evidence Location**: this Task's Results for P07; SPEC-0223 Task/ledger for inherited W09-H02 and W07-H05; hosted PR result for delivery.

#### Execution Log

##### Work Performed

Current P07 authoring began with the exact package and current repository
state. The draft review and scoped execution receipt are recorded above.
The bounded disk capability probe was run before product service startup;
its failure and owned cleanup are recorded below. Source implementation
and integrated verification have separate results and remain in progress.

##### Blockers and Decisions

W09-H02 is a recorded production LAN egress failure: product namespaces may
allow `192.168.0.13`, and a prior selective probe launched no product pod.
Until host/container or VM isolation is actually enforced and checked by a
disposable selected-namespace probe pod against controlled positive and
negative endpoints, product workload startup remains blocked. W07-H05 is the
original Desktop→SSH reviewer failure; the separate P06 CLI result does not
close it. Q03 already authorizes finite actual native observation within
existing account limits. The P06 Claude weekly limit was observed at 99%; a
new paid call needs current available quota and must not be repeated merely
for a new document. Any new root, cost or deletion conflict stops only its
dependent action. P12's worker containment is a separate later owner.
The host's Docker Engine 29.9.2 accepted `size=32M` but allowed 40 MiB
inside the owned probe container, so per-run hard-disk enforcement is
`failed` on that tested route. An alternate bounded VM or supported driver
has not been observed; the user's lack of information about one is not an
authorization or proof of its existence. Product workload startup remains
blocked until an actual supported disk and network boundary is established.

The Plan's provisional 600-second cap applies to selected component and
native representative runs. Existing generic `work_parallel` worker and
integration runs retain a finite timeout of at most 86400 seconds. Shared
admission validates and persists the actual requested timeout for each kind:
component/native at most 600 seconds, generic worker/integration at most
86400 seconds. It must not silently shorten, chunk or renew a caller's
timeout. CPU, memory and disk admission remain finite. This is a bounded
implementation interpretation of the current P07 request, not a new user
decision or evidence of technical implementation.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | FAIL | Seven actual VM runs each failed at a later step; the latest (EVD-069) creates the k3d server but k3s does not start within 180 seconds. The VM disk cap is enforced (EVD-065; EVD-007's Docker route stays FAIL) and restricted VM egress is denied (EVD-066); all owned cleanups passed. Selected readiness, the namespace probe pod and W09-H02 remain open; six operator criterion decisions remain pending |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | observation | Current branch and HEAD `c7ed0be33e60e05294e341b46a395215c4345900` before P07 draft | Local Git, current checkout | `git status --short --branch; git rev-parse HEAD` | 0 | PASS | Branch `codex/p01-ci-routing`, clean index/worktree, before P07 document writes; no environment or native success claimed | false | none |
| EVD-002 | [AC-0006](../spec.md#criteria) | WORK-001 | automated | Current P07 draft brief and current request records for the three new package documents at intake HEAD | `scripts/validate-execution-brief.py`, contract 3.0.0 | `python3 scripts/validate-execution-brief.py --root . --brief /tmp/p07-docbrief-xRuVgz/brief.json --current-request /tmp/p07-docbrief-xRuVgz/current-request.json --operation state-change --action author_p07_drafts --path docs/03.specs/0229-selective-environment/spec.md --path docs/03.specs/0229-selective-environment/plan.md --path docs/03.specs/0229-selective-environment/01.tasks/tsk-0001-selective-environment.md` | 0 | PASS | `PASS BRIEF: current request and scope match; authorization is separate`. The temp brief is task-owned and will be deleted after its factual record; this check does not grant parent approval, live authority or user acceptance | false | none |
| EVD-003 | [AC-0006](../spec.md#criteria) | WORK-001 | review | {"spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4"} | Nonauthor draft meaning reviewer, exact frozen parent bytes | Independent semantic review | none | PASS | Reviewer resolved three initial FIX findings and focused rereview of final Plan scope found zero BLOCK/FIX; document meaning only, with no native readonly source-write proof or formal parent approval | true | none |
| EVD-004 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"a161776516093d06e20ec0df577424bddbdfec91bd26d04b7f54f821e3c4921a","validity":"confirmed","revocation":"none"} | Current trusted human interaction and exact parent hashes, checked by platform owner; R008 receipt shape checked by lifecycle validator | Scoped execution approval | none | PASS | This records the current P07 source execution scope only. It grants no formal Spec/Plan approval, criterion acceptance, global host authority or runtime success; no revocation observed in the current thread | true | none |
| EVD-005 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"b8ced75c1892a435219f95719c2ee60bb0ed3c4efb575c4bf8efd5fdc587aa10","validity":"confirmed","revocation":"none"} | Current trusted P07 user request and focused nonauthor Task artifact review; exact parent hashes unchanged | Scoped execution approval | none | PASS | R008 binds the current Task scope including the physical helper split. EVD-004 is an earlier request revision; no formal parent approval, runtime success or criterion acceptance follows | true | none |
| EVD-006 | [AC-0003](../spec.md#criteria) | WORK-001 | observation | Exact owned `hyk8s-test-p07quota` container, cached alpine:3.24.3, Docker Engine 29.9.2 on hy-home-server; 60-second preparation budget | Docker CLI, no product service or production endpoint | `docker start -a hyk8s-test-p07quota` | none | FAIL | The attached CLI timed out at 60 seconds; this alone says nothing about actual disk enforcement. Container state and logs were read separately in EVD-007 | false | none |
| EVD-007 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Exact owned run with `storage-opt size=32M`, CPU 0.25, memory 64 MiB, PIDs 32, network none; started 2026-11-20T06:46:16Z, finished 06:46:29Z | Docker Engine 29.9.2, host hy-home-server; `/tmp/p07-environment-wwh6mHCV/disk-quota-probe.json` | `docker inspect hyk8s-test-p07quota`; `docker logs hyk8s-test-p07quota` | 0 | FAIL | Docker accepted 32 MiB StorageOpt but container exited 0, OOMKilled=false, logs show `40+0 records` and 41943040 bytes successfully written to `/quota-test`. Actual per-run hard disk cap failed; product workload startup stays blocked on this host until a supported enforced boundary is proven | true | none |
| EVD-008 | [AC-0003](../spec.md#criteria) | WORK-001 | observation | Exact container name and `hy-home.k8s/run=p07quota` label after failed quota probe | Docker Engine 29.9.2, host hy-home-server; same task journal | `docker rm hyk8s-test-p07quota`; `docker inspect hyk8s-test-p07quota` | 0 | PASS | Label check matched; remove exit 0; subsequent inspect exit 1 with `no such object`. Only owned test container was removed; disk-cap failure remains open | true | none |
| EVD-009 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"d56a54cb2b9a0d31b3054ba2d32e9cfe4e778b77237a1d7bb383d7795e7fef5f","validity":"confirmed","revocation":"none"} | Current trusted P07 request, focused nonauthor Task VM artifact review, unchanged parent hashes | Scoped execution approval | none | PASS | R008 binds the current Task scope including exact VM helper/test/existing suite paths. EVD-004/005 remain historical earlier revisions; neither formal parent approval nor actual VM success or criterion acceptance follows | true | none |
| EVD-010 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Transient owned user unit `hyk8s-p07-capability.service`, UID 1000 canonical bus, CPUQuota=200%, MemoryMax=4G, RuntimeMaxSec=30 | User systemd and pinned Python; `/tmp/p07-environment-wwh6mHCV/user-cgroup-probe.json` | `systemd-run --user --collect` with own-cgroup read; user unit status after exit | 0 | PASS | Invocation `d361ec9915dc4c74b57b22dcd9990e82`, own `cpu.max=200000 100000`, `memory.max=4294967296`, runtime 36 ms, unit LoadState after `not-found`. Only user-service CPU/memory hard-cap capability and collection observed; VM, disk and LAN remain unobserved | false | none |
| EVD-011 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"cc27777e37e3dc6133ee3875ef3c0061790fc98cb1736682b2865b3ae6e6e4c9","validity":"confirmed","revocation":"none"} | Current trusted P07 request, focused nonauthor Task transport-split review, unchanged parent hashes | Scoped execution approval | none | PASS | R008 binds the current Task scope including the cohesive VM transport module. Earlier receipts remain historical request revisions; this grants no new behavior, formal parent approval, VM runtime success or criterion acceptance | true | none |
| EVD-012 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"c21add7614a8901a4081c6fa455532e0d651cda17f7505baeeb9983d7d887d14","validity":"confirmed","revocation":"none"} | Current trusted P07 request and unchanged exact parent review; test file split stays in the same cluster suite | Scoped execution approval | none | PASS | R008 binds the current Task scope including the focused VM boundary test module. EVD-004/005/009/011 remain historical request revisions; no new behavior, formal parent approval, VM runtime success or criterion acceptance follows | true | none |
| EVD-013 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Codex CLI 0.169.0, scoped dummy packet `/tmp/p07-environment-wwh6mHCV/review-packet`, root deny/minimal read plus installed executable and packet read, network false; public dummy, forbidden write and outside sentinel | Actual Codex CLI sandbox preflight on current host; operator used supported escalation only for sandbox startup | `codex sandbox -C /tmp/p07-environment-wwh6mHCV/review-packet -P p07-review`; `/usr/bin/python3 boundary-probe.py` | 0 | PASS | Public dummy read succeeded; source write denied `EROFS` errno 30; outside synthetic file hidden `ENOENT` errno 2; AF_INET socket creation denied `EPERM` errno 1. Actual OS boundary check only: no model review, source correctness, Desktop repair, global trust or sandbox bypass claimed | true | none |
| EVD-014 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | automated | Frozen P07 source candidate in the current checkout; selected cluster suite across three existing test modules | Pinned `/home/hyunyoun/.venvs/hyhome-validation/bin/python`, registered `test-cluster` contract suite; QA owner observation | `/home/hyunyoun/.venvs/hyhome-validation/bin/python scripts/run-contract-tests.py --root . --suite test-cluster` | 0 | PASS | 78/78 focused synthetic tests PASS in 1.628 seconds on the frozen source candidate. This checks admission, VM helper and pre-workload probe failure paths in test doubles; actual VM boot, ENOSPC, selected pod and LAN behavior remain NOT_RUN | true | none |
| EVD-015 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | observation | Frozen P07 candidate, four focused Python modules: cluster, VM, VM boundaries and dispatcher | Pinned Python, in-process stdlib `trace.Trace(count=True, trace=False)` and `unittest.defaultTestLoader.loadTestsFromNames`; QA owner observation | Inline `rtk proxy /home/hyunyoun/.venvs/hyhome-validation/bin/python` with `trace.Trace.runfunc` over the four modules | 0 | PASS | 117/117 focused synthetic tests PASS in 35.208 seconds. Executable changed-source lines hit 2570/3156, weighted 81.4%; child-process/native VM lines are excluded. This does not prove host disk, guest ENOSPC, LAN or product readiness | false | none |
| EVD-016 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable public P07 candidate diff and SHA manifest, selected requirements and current consumers; thread `01a1f832-829d-7bf2-a9bb-956cbdb55558` | Actual Codex CLI 0.169.0, requested `gpt-6-sol`/high, fresh read-only parent, 595+5-second bound; `/tmp/p07-environment-wwh6mHCV/review-final.md` | Bounded Codex CLI `exec --json` focused review of the public packet | 0 | FAIL | Model completed in 353.938 seconds and found four HIGH blockers: `down(A)` can release B's lease from a mismatched token; direct no-workload k3d start lacks hard disk cap; tracked public file may change to a symlink between `lstat` and read; expiry may release a live in-flight create. Verdict blocking despite process exit 0. Usage input 2615077, cached 2491520, output 15920 including reasoning-count 12630; provider charge `null`/unobserved, no reasoning text retained. Source repair and one bounded post-repair review remain pending | true | none |
| EVD-017 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual model invocation and read-only public packet, dummy source and outside sentinel | Codex CLI 0.169.0 model-invoked tools, root-deny/minimal plus packet/executable read, network false | Actual model boundary probes in thread `01a1f832-829d-7bf2-a9bb-956cbdb55558` | 0 | PASS | Model tool read of public dummy succeeded, write denied `EROFS` errno 30, outside synthetic file hidden `ENOENT` errno 2, AF_INET socket denied `EPERM` errno 1. This proves that selected CLI parent boundary, not source correctness, P06 Desktop repair or P12 worker containment | true | none |
| EVD-018 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review01`, owned `hyk8s-p07-review` user unit and admission token after model exit | User systemd and shared admission; actual root operator observation | Verify unit collection, MainPID and native lease postcondition | 0 | PASS | Unit invocation `13b6df8fbc034fb494d4578869beca6f` collected to `not-found`, MainPID 0 and no child; shared native lease count for `p07review01` is 0. Own cgroup reported `cpu.max=200000 100000`, `memory.max=4294967296`, `memory.swap.max=0`. No VM or Docker resource cleanup claimed | true | none |
| EVD-019 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Startup event stream from the same actual Codex CLI invocation | Native CLI event read-back; global user files neither read nor changed | Inspect selected run `item_errors` and warnings | 0 | FAIL | Seven startup items were observed: legacy global `docs-researcher`, `explorer`, `reviewer` role file names were missing under `~/.codex/agents` twice each (six), plus one under-development `skip_host_skill_discovery` warning. Multi-agent was disabled; this is not an MCP permission failure and does not establish the cause of earlier P06 Desktop errors. P08 native binding owner receives this residual | false | none |
| EVD-020 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"9ae6ac7b0f15b7d1d13e5997c111e4d63f20ad77e4f5ff3dacc95969acbdcd7e","validity":"confirmed","revocation":"none"} | Current trusted P07 request and unchanged exact parent review; cohesive lifecycle test split stays in existing cluster suite | Scoped execution approval | none | PASS | R008 binds the current Task scope including `tests/test_test_cluster_lifecycle.py`; EVD-012 is the prior request revision. This grants no new behavior, parent approval, native review success, VM runtime success or criterion acceptance | true | none |
| EVD-021 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable public repair packet and prior four HIGH findings, 14 candidate hashes matched manifest; thread `01a1f84a-bfe4-70b2-89bf-26dbc121a026` | Actual Codex CLI 0.169.0, requested `gpt-6-sol`/high, fresh read-only parent; `/tmp/p07-environment-wwh6mHCV/review-final-repair.md` | Bounded Codex CLI `exec --json` focused post-repair review | 0 | FAIL | Model completed in 226.255 seconds but found three HIGH and one MEDIUM: VM sweep can stop an active creator/controller and release its lease; direct k3d `down` can release an in-flight create; VM release omits workspace identity; crash after VM parent deletion can strand its preparation worker lease. Original direct wrong-token, every-live-node disk cap and anchored public-file findings were repaired, while expiry remains open through these active-start paths. Usage input 1161780, cached 1072000, output 10661 including reasoning-count 7818; provider charge `null`/unobserved, no reasoning text retained. This is a blocking source verdict despite CLI exit 0; no VM runtime proof | true | none |
| EVD-022 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual post-repair public packet and model-invoked dummy boundary probes | Codex CLI 0.169.0 fresh root-deny/minimal packet/executable read profile, network false | Actual model boundary probes in thread `01a1f84a-bfe4-70b2-89bf-26dbc121a026` | 0 | PASS | Public read succeeded; source write denied `EROFS`, outside synthetic file remained hidden and AF_INET socket was denied. This confirms the selected CLI parent boundary for this call, not source correctness, VM isolation, Desktop repair or worker containment. Seven known startup diagnostics were again observed and remain a distinct P08 native binding residual, not an MCP permission failure | true | none |
| EVD-023 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review02` after second model exit; same owned user unit, run token and native lease | User systemd and shared admission, root operator postcondition read | Verify unit LoadState/MainPID, proof process start identity, lease run/kind/workspace/binding/unit and release | 0 | PASS | Exact unit was collected to `not-found`, MainPID 0, recorded PID/start identity absent. Release callback matched run, kind, workspace, binding and unit; remaining `p07review02` native leases 0. This proves only review-run cleanup; EVD-021 source blockers and VM runtime remain open | true | none |
| EVD-024 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Existing authenticated Codex CLI 0.169.0 account metadata, without account identifier values | Installed CLI stdio account API; `/tmp/p07-environment-wwh6mHCV/native-remaining-usage.json` | `account/rateLimits/read` | 0 | PASS | Ordinary use allowed; existing `prolite` plan, 69% of 10080-minute weekly window used and 31% remaining; spendControlReached=false, rateLimitReachedType=null, no secondary window. Ephemeral RPC server exited. No model call, reset, credit purchase, credential read/change or provider charge observation occurred in this metadata check | false | none |
| EVD-025 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable public lifecycle packet, prior review findings and 15 candidate files matching its SHA manifest; thread `01a1f864-01e2-7eb0-89f5-8be76c19dcbf` | Actual Codex CLI 0.169.0, requested `gpt-6-sol`/high, fresh read-only parent; `/tmp/p07-environment-wwh6mHCV/review-final-lifecycle.md` | Bounded Codex CLI `exec --json` focused lifecycle review | 0 | FAIL | Model completed in 201.215 seconds but found three HIGH defects: stale k3d sweep/recover removes run state before exact lease release, so cleanup/release failure can strand the lease; collected VM unit `is-active unknown` is treated as an in-flight start forever instead of confirming `LoadState=not-found` and process absence; VM `rmtree` can remove `owner.json` before other files, leaving an unrecoverable partial directory on crash. Second-review VM sweep, create receipt and workspace checks addressed their cited triggers; preparation-child release and recovery were repaired. New lifecycle defects remain blocking despite exit 0. Usage input 746401, cached 656896, output 9708 including reasoning-count 7309; provider charge `null`/unobserved, no reasoning text retained. No VM runtime proof | true | none |
| EVD-026 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual third lifecycle review packet and model-invoked dummy boundary probes | Codex CLI 0.169.0 fresh root-deny/minimal packet/executable read profile, network false | Actual model boundary probes in thread `01a1f864-01e2-7eb0-89f5-8be76c19dcbf` | 0 | PASS | Public read succeeded; source write denied `EROFS`, outside synthetic file hidden `ENOENT`, and AF_INET socket denied `EPERM`. This confirms the selected CLI parent boundary for this call only, not source correctness or VM isolation. The seven known startup diagnostics recurred and remain the separate P08 native-binding residual; they are not an MCP permission failure | true | none |
| EVD-027 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review03` after third model exit; owned `hyk8s-p07-review` user unit, process identity, run token and native lease | User systemd and shared admission; root operator postcondition read | Verify unit LoadState, proof PID/start absence, lease run/kind/workspace/binding/unit and release | 0 | PASS | Release callback matched exact run, kind, workspace, binding and unit; unit collected to `not-found`, recorded PID/start absent and native lease count 0. This proves review-run cleanup only; EVD-025 source defects and VM runtime remain open | true | none |
| EVD-028 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Existing authenticated Codex CLI 0.169.0 account metadata after the third native review, without account identifier values | Installed CLI stdio account API; `/tmp/p07-environment-wwh6mHCV/native-remaining-usage-after-lifecycle.json` | `account/rateLimits/read` | 0 | PASS | Ordinary use allowed on existing `prolite` plan; 77% of 10080-minute weekly window used and 23% remaining; no secondary window, spend control or rate limit reported. Ephemeral RPC read only: no model call, reset, credit purchase, credential read/change, provider charge or VM runtime observation. Finite fourth review remains NOT_RUN | false | none |
| EVD-029 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | automated | Frozen post-native3 repair candidate copied into `p07review04` public packet; six changed source SHA256 values stable before/after QA: admission `8df040c5`, cluster `eb41fb22`, environment `2ef9a5a9`, VM `33eb3901`, transport `9cf4dcb2`, dispatcher `1ea33ea2` (prefixes) | Pinned `/home/hyunyoun/.venvs/hyhome-validation/bin/python`; QA owner selected repository suites | Registered `test-cluster` suite, `tests/test_work_parallel.py`, affected validation route inventory, Ruff on P07 source/tests/runner | 0 | PASS | Cluster 101/101 and dispatcher 42/42 synthetic tests passed; affected routing covered 748 paths with zero uncovered or ambiguous; Ruff passed. This is a frozen static/synthetic source checkpoint, not actual VM boot, ENOSPC, LAN or readiness. EVD-025 remains a historical FAIL until a matching actual post-repair review | true | none |
| EVD-030 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | observation | Same frozen post-native3 repair candidate across five focused unittest modules; six source SHA256 values stable before/after trace | Pinned Python in-process stdlib `trace.Trace(count=True, trace=False)` and `unittest.defaultTestLoader.loadTestsFromNames`; QA owner observation | Inline focused trace on cluster, cluster lifecycle, VM, VM boundaries and dispatcher tests | 0 | PASS | 143/143 focused tests passed and changed-source executable lines hit 2809/3408, weighted 82.4%. Child-process/native VM lines are excluded. The earlier mixed hook-stash trace was invalid and is not used as evidence; this PASS does not settle EVD-025 or actual VM behavior | false | none |
| EVD-031 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"c9738359345e03880aa010b7c581fe097639b01548517d2d0be9f0bc820a5eb0","validity":"confirmed","revocation":"none"} | Current trusted P07 request and unchanged exact parent review; host-only VM lifecycle helper is a physical split within existing behavior | Scoped execution approval | none | PASS | R008 binds the current Task scope including `scripts/test_cluster_vm_lifecycle.py`; EVD-020 is the prior request revision. This grants no new behavior, formal parent approval, source review success, VM runtime success or criterion acceptance | true | none |
| EVD-032 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable public durability repair packet, prior three HIGH findings and 15 files matching SHA manifest; thread `01a1f874-3c14-72e0-bbbe-171c722f8d8e` | Actual Codex CLI 0.169.0, requested `gpt-6-sol`/high, fresh read-only parent; `/tmp/p07-environment-wwh6mHCV/review-final-durability.md` | Bounded Codex CLI `exec --json` focused fourth source review | 0 | FAIL | Model completed in 203.899 seconds but found two HIGH: failed `systemctl is-active` with misleading inactive output can authorize VM artifact deletion; VM `owner.json` and directory can be deleted before lease release, stranding loaded-inactive cleanup if release fails. Two MEDIUM: native sweep omits state cluster identity recheck; owner replacement lacks parent directory fsync. Earlier cleanup ordering, not-found recovery and partial deletion paths improved but these findings remain blocking despite exit 0. Usage input 565438, cached 429824, output 9055 including reasoning-count 6887; provider charge `null`/unobserved, no reasoning text retained. Synthetic tests were not rerun by this reviewer; no VM runtime proof | true | none |
| EVD-033 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual fourth durability review packet and model-invoked dummy boundary probes | Codex CLI 0.169.0 fresh root-deny/minimal packet/executable read profile, network false | Actual model boundary probes in thread `01a1f874-3c14-72e0-bbbe-171c722f8d8e` | 0 | PASS | Public read succeeded; source write denied `EROFS`, outside synthetic file hidden `ENOENT`, and AF_INET socket denied `EPERM`. All 15 public packet files matched SHA manifest. This is selected CLI parent boundary evidence, not source correctness or VM isolation. The seven known startup diagnostics recurred separately under P08 native-binding residual | true | none |
| EVD-034 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review04` after fourth model exit; owned `hyk8s-p07-review` user unit, proof process identity, run token and native lease; `/tmp/p07-environment-wwh6mHCV/review-cleanup-durability.json` | User systemd and shared admission; root operator exact callback and postcondition read | Verify unit LoadState, proof PID/start absence, lease run/kind/workspace/binding/unit and release | 0 | PASS | Callback matched exact run, native kind, workspace, binding and unit; unit collected to `not-found`, proof PID/start absent and shared native lease count 0. Root independently confirmed `/proc/<proofpid>` absent for all four review proofs. This proves only review-run cleanup and process absence; EVD-032 source blockers and actual VM runtime remain open | true | none |
| EVD-035 | [AC-0006](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P07-ENVIRONMENT.md request of 2026-11-20 in this conversation for package workspace_governance_remediation_1_1_0_20261120, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0229","SPEC-0229-PLAN-0001","SPEC-0229-TSK-0001"],"reviewed_spec_sha256":"8fffd52aa5a300cd3b19c3262fd7ccc3dc42b6214fa2c0f4a8971ab3fcb67c34","reviewed_plan_sha256":"9d205b95c3ec259c9cc22ffd97e91d9c7b840a3d726ea60977c717fab495e6b4","request_revision":"36c76398b51f06e282ed6f8bcd42c990bed87778b584031ba1661b8ed2055c87","validity":"confirmed","revocation":"none"} | Current trusted P07 request and unchanged exact parent review; cohesive native durability test split stays in existing cluster suite | Scoped execution approval | none | PASS | R008 binds the current Task scope including `tests/test_test_cluster_durability.py`; EVD-031 is the prior request revision. This grants no new behavior, formal parent approval, source review success, VM runtime success or criterion acceptance | true | none |
| EVD-036 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Existing authenticated Codex CLI 0.169.0 account metadata after fourth native review, without account identifier values | Installed CLI stdio account API; `/tmp/p07-environment-wwh6mHCV/native-remaining-usage-before-final.json` | `account/rateLimits/read` | 0 | PASS | Ordinary use allowed on existing `prolite` plan; 92% of 10080-minute weekly window used and 8% remaining; no secondary window, spend control or rate limit reached. Ephemeral RPC read only: no model call, reset, credit purchase, payment, credential change or provider charge observation. One finite fifth focused review remains NOT_RUN | false | none |
| EVD-037 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | automated | Frozen post-native4 repair candidate with five affected source hashes reviewed by architect and seven changed source SHA prefixes stable before/after QA: admission `8df040c5`, cluster `95e96d85`, environment `05d25af2`, VM `1b7d7d1e`, host lifecycle `7dfaf22d`, transport `9cf4dcb2`, dispatcher `1ea33ea2` | Pinned `/home/hyunyoun/.venvs/hyhome-validation/bin/python`; QA owner selected repository suites | Registered `test-cluster` suite, `tests/test_work_parallel.py`, validation-routing suite and affected route inventory | 0 | PASS | Cluster 114/114 across five modules, dispatcher 42/42 and validation-routing 173/173 synthetic tests passed; affected routing covered 748 paths with zero uncovered or ambiguous. This is static/synthetic source evidence, not actual VM boot, ENOSPC, LAN or readiness. EVD-032 remains historical source FAIL until matching actual review | true | none |
| EVD-038 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | observation | Same frozen post-native4 repair candidate across six focused unittest modules; seven changed source hashes stable before/after trace | Pinned Python in-process stdlib `trace.Trace(count=True, trace=False)` and `unittest.defaultTestLoader.loadTestsFromNames`; QA owner observation | Inline focused trace on cluster, cluster lifecycle, cluster durability, VM, VM boundaries and dispatcher tests | 0 | PASS | 156/156 focused tests passed and changed-source executable lines hit 2914/3535, weighted 82.4%. Child-process/native VM lines are excluded; this does not settle EVD-032 or actual VM behavior | false | none |
| EVD-039 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable public final repair packet, prior two HIGH/two MEDIUM findings and 17 files matching SHA manifest; thread `01a1f898-c6b7-75b3-a795-1efb43cefb5c` | Actual Codex CLI 0.169.0, requested `gpt-6-sol`/high, fresh read-only parent; `/tmp/p07-environment-wwh6mHCV/review-final-final.md` | Bounded Codex CLI `exec --json` focused fifth source review | 0 | FAIL | Model completed in 152.146 seconds and found prior failed-unit query, lease-release retry, native sweep identity and directory-sync findings resolved. One new blocking MEDIUM remains: VM finalization can overwrite or delete a changed `state.json` because it does not reread exact run/token/unit/workspace/binding before phase writes and removal; intent recovery checks token without workspace/binding. Retain state and leases when current identity differs. Usage input 493406, cached 434176, output 7315 including reasoning-count 4850; provider charge `null`/unobserved, no reasoning text retained. Source verdict blocking despite process exit 0; synthetic tests were not rerun by reviewer and actual VM remains NOT_RUN | true | none |
| EVD-040 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual fifth final repair packet and model-invoked dummy boundary probes | Codex CLI 0.169.0 fresh root-deny/minimal packet/executable read profile, network false | Actual model boundary probes in thread `01a1f898-c6b7-75b3-a795-1efb43cefb5c` | 0 | PASS | Public read succeeded; source write denied `EROFS`, outside synthetic file hidden `ENOENT`, and AF_INET socket denied `EPERM`. All 17 public packet files matched SHA manifest. This is selected CLI parent boundary evidence, not source correctness or VM isolation. The seven known startup diagnostics recurred separately under P08 native-binding residual | true | none |
| EVD-041 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review05` after fifth model exit; owned `hyk8s-p07-review` unit and proof PID 1980408/start 97602581; `/tmp/p07-environment-wwh6mHCV/review-cleanup-final.json` | User systemd and shared admission; root operator exact postcondition read | Verify unit LoadState/MainPID, proof process absence, lease run/native/workspace/binding/intent-unit and release | 0 | PASS | Unit LoadState `not-found`, MainPID 0, recorded PID/start absent; release matched exact run, native kind, workspace, binding and intent unit; remaining token lease rows 0. This proves only fifth review-run cleanup, not EVD-039 source correctness or VM runtime | true | none |
| EVD-042 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Existing authenticated Codex CLI 0.169.0 account metadata after fifth native review, without account identifier values | Installed CLI stdio account API; root operator cost-free read | `account/rateLimits/read` | 0 | PASS | Ordinary use allowed on existing `prolite` plan; 95% of 10080-minute weekly window used and 5% remaining; no secondary window, spend control or rate limit reached. No model call, reset, credit purchase, payment, credential change or provider charge observation occurred in this metadata read. One finite sixth changed-delta review remains NOT_RUN | false | none |
| EVD-043 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | automated | Frozen five-file changed-delta packet before sixth native review: environment `ce9e1c87`, VM lifecycle `fcc888f5`, cluster `95e96d85`, admission `8df040c5`, durability test `ffdd611d` SHA256 prefixes; architect and independent contextual review found no actionable defect | Pinned Python, QA owner registered affected repository suites | `test-cluster`, `tests/test_work_parallel.py`, validation-routing and affected route inventory | 0 | PASS | Cluster 121/121, dispatcher 42/42, validation-routing 173/173 synthetic tests passed; 748 affected paths had zero uncovered or ambiguous. This is frozen static QA, not sixth model source verdict or actual VM runtime | true | none |
| EVD-044 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable five-file changed-delta packet and prior VM state-identity finding; thread `01a1f8ac-f055-7080-9fc3-632a1429d573` | Actual Codex CLI 0.169.0, requested `gpt-6-sol`/high, fresh read-only parent; `/tmp/p07-environment-wwh6mHCV/review-final-delta.md` | Bounded 175+5-second Codex CLI `exec --json` focused sixth source review | 0 | FAIL | Model completed in 121.855 seconds and verified EVD-039's state-identity race resolved by exact run/token/unit/workspace/binding checks under shared lock. One new blocking MEDIUM remains: intent recovery releases the parent lease before recording a cleanup phase or removing the private run directory; interruption or removal failure leaves creating state/no lease with no retry path. Keep the parent intent through metadata removal and make exact-identity retry idempotent. Usage input 648138, cached 606464, output 5317 including reasoning-count 3486; provider charge `null`/unobserved, no reasoning text retained. This read-only review ran no tests or live VM operation | true | none |
| EVD-045 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual sixth changed-delta packet and model-invoked dummy boundary probes | Codex CLI 0.169.0 fresh root-deny/minimal packet/executable read profile, network false | Actual model boundary probes in thread `01a1f8ac-f055-7080-9fc3-632a1429d573` | 0 | PASS | Public read succeeded; source write denied `EROFS`, outside synthetic file hidden `ENOENT`, and AF_INET socket denied `EPERM`. All five packet hashes matched; same seven startup diagnostics recurred separately. This proves selected CLI parent isolation, not source correctness, VM runtime or Desktop repair | true | none |
| EVD-046 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review06` after sixth model exit; owned `hyk8s-p07-review` unit and proof PID 2150587/start 97734723 | User systemd and shared admission; root operator exact postcondition read | Verify unit LoadState/MainPID, proof process absence, lease run/native/workspace/binding/intent-unit and release | 0 | PASS | Unit collected to `not-found`, recorded proof PID/start absent, exact token-bound native lease released and remaining token rows 0. This proves only sixth review-run cleanup, not EVD-044 source correctness or VM runtime | true | none |
| EVD-047 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Existing authenticated Codex CLI 0.169.0 account metadata after sixth native review, without account identifier values | Installed CLI stdio account API; root operator cost-free read | `account/rateLimits/read` | 0 | PASS | Ordinary use allowed on existing `prolite` plan; 98% of 10080-minute weekly window used and 2% remaining; no secondary window, spend control or rate limit reached. No model call, reset, credit purchase, payment, credential change or provider charge observation in this metadata read. One finite tiny seventh changed-delta review remains NOT_RUN | false | none |
| EVD-048 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | automated | Frozen seven-source P07 candidate after native6 recovery repair; lifecycle SHA256 `572dcb319819d0a1f4c7840a117c06cfb0379df519864fe76b460cb1014c79b1`; other six source hashes unchanged from EVD-043 | Pinned validation Python and QA-selected repository checks | Registered `test-cluster`, dispatcher, validation-routing, affected route inventory, Ruff and hash-pinned stdlib trace | 0 | PASS | Cluster 123/123, dispatcher 42/42, routing 173/173; 748 affected paths with zero uncovered/ambiguous; 165/165 traced tests; 2998/3643 executable lines (82.3%); Ruff passed. The first 69.4% trace omitted import execution and is invalid. Synthetic/source checks only; VM runtime remains unobserved | true | none |
| EVD-049 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | review | Immutable seven-file recovery-only packet; lifecycle `572dcb319819d0a1f4c7840a117c06cfb0379df519864fe76b460cb1014c79b1`; thread `01a1f8b4-6e2e-7e91-ae39-c6a620937277` | Codex CLI 0.169.0 `gpt-6-sol`/high, fresh root-deny read-only parent, network disabled; `/tmp/p07-environment-wwh6mHCV/review-final-intent.md` | Bounded 115+5-second CLI review of intent-recovery retry repair | 0 | PASS | Completed in 65.823 seconds; confirmed the recovery retry gap identified by EVD-044 is repaired and found no actionable issue in the changed path. Input 109483, cached 90624, output 3096 including reasoning-count 2039; charge `null`/unobserved. All seven packet hashes matched. This narrow review did not run tests or live operations | true | none |
| EVD-050 | [AC-0005](../spec.md#criteria) | WORK-001 | observation | Same actual seventh recovery-only review packet; thread `01a1f8b4-6e2e-7e91-ae39-c6a620937277` | Same Codex CLI 0.169.0 root-deny/minimal profile; network disabled | Model-invoked public read, source write, outside-file and AF_INET socket probes | 0 | PASS | Public read succeeded; write returned `EROFS`, outside synthetic file `ENOENT`, AF_INET socket `EPERM`; all seven packet hashes matched. Seven startup diagnostics recurred. This establishes only the selected CLI parent boundary, not Desktop enforcement or VM isolation | true | none |
| EVD-051 | [AC-0002](../spec.md#criteria), [AC-0005](../spec.md#criteria) | WORK-001 | observation | Exact native run `p07review07`; owned unit `hyk8s-p07-review`; proof PID 2238823/start 97783814; `/tmp/p07-environment-wwh6mHCV/review-cleanup-intent.json` | User systemd and shared admission; root operator exact postcondition read | Verify exact unit, process identity, run/kind/workspace/binding/unit intent and release | 0 | PASS | Unit `not-found`, MainPID 0 and proof PID/start absent; exact native token lease released with zero remaining rows. This proves only review-run cleanup, not source or VM behavior | true | none |
| EVD-052 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0005](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | observation | Planned run `p07vm001`, selected `platform-network-policies`; command was submitted to the execution runner under the current P07 request | Managed execution approval review; denial reported that usage limit prevented review and named 2026-11-27 as the next availability | Attempted `python scripts/test_cluster.py --root . up --vm --run-id p07vm001 --authority P07-bounded-VM platform-network-policies` | none | DEFER | The approval review rejected the command before execution. No VM, image download, cluster or product workload started. This is an unavailable approval-review resource, not a product runtime failure. Retry only when the review route is available; actual boot, guest ENOSPC, controlled LAN probes, selected readiness and cleanup remain unobserved | true | none |
| EVD-053 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Run `p07vm001` at `main@fe700f835ec18392e857a476e58a62f6a1110656`, selected closure `platform-namespaces`, `platform-network-policies`; started 2026-11-23T11:30:09Z under the package 1.2.0 P07 request; deadline epoch 1795434012 | Claude Code root executor; QEMU 8.2.2 TCG (`/dev/kvm` inaccessible), user systemd owned unit `hyk8s-test-p07vm001-vm`, CPUQuota=200%, MemoryMax=4G | `python3 scripts/test_cluster.py --root . up --vm --run-id p07vm001 --authority P07-bounded-VM platform-network-policies` | 2 | FAIL | `VM_READY: owned unit exited before guest readiness` after 596 seconds. Image download, SHA verification and raw conversion completed in about 33 seconds and QEMU started; owner state stayed `provisioning`, run `known_hosts` stayed empty, so guest SSH never answered. The unit hit `RuntimeMaxSec` with 2 min 28.7 s total CPU (2.1 GiB memory peak), which indicates an idle guest rather than CPU-bound TCG progress. Serial output is `null`, so the guest-side cause is unobserved. Guest ENOSPC, LAN deny, selected readiness and product workload were not reached | true | none |
| EVD-054 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Exact token `0beca2f5…` expiry timer and service for `p07vm001` after EVD-053 | User systemd journal; `test_cluster.py status`; `/proc` reads of recorded controller PID 3019703 and QEMU PID 3026077 | `test_cluster.py expire p07vm001 <token>` via the owned timer at 2026-11-23T11:40:30Z | 0 | PASS | Expiry deleted `hyk8s-test-p07vm001-vm`; timer and service collected; `.workspace-test` empty; `status` returned `[]`; both recorded processes absent. The private admission database was not read directly in this check. Owned cleanup only; it does not resolve EVD-053 or EVD-007 | true | none |
| EVD-055 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | automated | Working-tree repair of `scripts/test_cluster_vm.py`, `scripts/test_cluster_vm_transport.py` and `tests/test_test_cluster_vm.py` on `main@fe700f835ec18392e857a476e58a62f6a1110656` | Pinned `/home/hyunyoun/.venvs/hyhome-validation/bin/python`; Ruff | Three new tests first, then `scripts/run-contract-tests.py --root . --suite test-cluster`; `ruff check scripts tests`; `ruff format --check` on changed files | 0 | PASS | Before the repair the three new tests failed (single `tcp:` chardev guestfwd, fixed TCG, missing relay). After it the suite passed 126/126 across five modules: per-connection `cmd:` relay served three sequential NoCloud requests, KVM is selected only with device access and TCG otherwise, serial reaches the owned unit journal. Synthetic evidence only; it does not prove guest boot, ENOSPC, LAN deny or readiness, and EVD-053 stays open until an actual retry | true | none |
| EVD-056 | [AC-0002](../spec.md#criteria) | WORK-001 | observation | Host `/dev/kvm` after the operator twice reported running `sudo setfacl -m u:hyunyoun:rw /dev/kvm` | `getfacl /dev/kvm`; read and write `os.access` on `/dev/kvm` as UID 1000 | `getfacl /dev/kvm; python3 -c "import os; print(os.access(...))"` | 0 | DEFER | Both reads showed only `user::rw-` and access `False`; the operator-granted KVM precondition for the single post-repair VM retry is unmet, so no VM was started. Not a runtime PASS or FAIL | true | none |
| EVD-057 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Single post-repair run `p07vm002` at `d13ae6cdade3aca9b0b421e89f6a9788c24d63c6`, same closure and 600-second bound; started 2026-11-23T12:00:39Z after the operator's `/dev/kvm` ACL was observed (`user:hyunyoun:rw-`, access `True`) | Claude Code root executor; QEMU 8.2.2 `accel=kvm`, owned unit `hyk8s-test-p07vm002-vm`, guest serial in the unit journal | `python3 scripts/test_cluster.py --root . up --vm --run-id p07vm002 --authority P07-bounded-VM platform-network-policies` | 2 | FAIL | Failed after 84 seconds with `VM_STEP: ssh exit 2` at `cloud-init status --wait`, which printed `status: done`. The guest booted, cloud-init read `DataSourceNoCloudNet [seed=dmi,http://10.0.2.100/]` through the per-connection relay, installed `docker.io` and finished in 52.9 seconds, and guest SSH answered, so the EVD-053 metadata-forward cause is confirmed repaired. The journal shows the cause of exit 2: cloud-init 26.2 reports the `nocloud-net` datasource name as DEPRECATED, a recoverable error. Restricted reboot, guest ENOSPC, LAN deny and selected readiness were not reached | true | none |
| EVD-058 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Exact run `p07vm002` after EVD-057 | `test_cluster.py down`; user systemd; `test_cluster.py status`; `pgrep -a qemu-system` | `python3 scripts/test_cluster.py --root . down p07vm002` | 0 | PASS | `down` deleted `hyk8s-test-p07vm002-vm`; no `hyk8s*` unit remained, `.workspace-test` was empty, `status` returned `[]` and no QEMU process existed. Owned cleanup only | true | none |
| EVD-059 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | automated | Working-tree repair of the provisioning SMBIOS seed in `scripts/test_cluster_vm.py` and its regression in `tests/test_test_cluster_vm.py` | Pinned validation Python; Ruff | Extended relay command test first, then `scripts/run-contract-tests.py --root . --suite test-cluster`; `ruff check scripts tests` | 0 | PASS | The extended test failed on `ds=nocloud-net`; after changing the seed to `ds=nocloud;s=http://10.0.2.100/` the suite passed 126/126 and Ruff passed. Synthetic only; EVD-057 stays open until an actual run | true | none |
| EVD-060 | [AC-0002](../spec.md#criteria) | WORK-001 | observation | Host `/dev/kvm` after EVD-058, about four minutes after EVD-057 observed the ACL | `getfacl /dev/kvm`; read and write `os.access` on `/dev/kvm` as UID 1000 | `getfacl /dev/kvm; python3 -c "import os; print(os.access(...))"` | 0 | DEFER | The user ACL was no longer present (`user::rw-` only) and access was `False`; the cause of the removal was not observed. The D07 single post-repair retry was spent by EVD-057, so any further VM run needs both renewed KVM access and a new operator authorization | true | none |
| EVD-061 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | One additional run `p07vm003` authorized by the operator beyond D07's spent retry, at `05a536a7fa0fad0b2c2895400c21026d5d653fc4`, same closure and 600-second bound; started 2026-11-23T12:12:22Z after `/dev/kvm` ACL and access `True` were observed | Claude Code root executor; QEMU 8.2.2 `accel=kvm`, owned unit `hyk8s-test-p07vm003-vm`, guest serial in the unit journal | `python3 scripts/test_cluster.py --root . up --vm --run-id p07vm003 --authority P07-bounded-VM platform-network-policies` | 2 | FAIL | Failed after 264 seconds at the last controller step, the in-guest selected `up`: `ENV_LIMIT: insufficient currently available host disk`. Cloud-init finished in 44.7 seconds with the `nocloud` seed and `status --wait` passed (EVD-057 cause repaired in fact); the journal shows the guest powered off and booted a second time. The restricted SSH probe, capsule transfer and guest ENOSPC check precede that step and each raises on failure, so they completed, but their individual results were not recorded, so LAN deny and ENOSPC are not separately evidenced here. Cause: the guest re-runs shared admission, which reserves the cluster disk budget plus a 1024 MiB margin from the guest root filesystem, while the whole guest disk is 4080 MiB with Docker and images already installed. No k3d cluster or product workload started | true | none |
| EVD-062 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Exact run `p07vm003` after EVD-061 | `test_cluster.py down`; user systemd; `test_cluster.py status`; `pgrep -a qemu-system` | `python3 scripts/test_cluster.py --root . down p07vm003` | 0 | PASS | `down` deleted `hyk8s-test-p07vm003-vm`; no `hyk8s*` unit remained, `.workspace-test` was empty, `status` returned `[]` and no QEMU process existed. Owned cleanup only | true | none |
| EVD-063 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | review | EVD-061 cause text against `verified_guest_profile` in `scripts/test_cluster_environment.py` | Root operator source read | none | none | PASS | Correction of EVD-061's cause: the guest admission reserves the guest profile, 1024 MiB disk plus a 128 MiB margin, not the host run budget plus 1024 MiB. The actual cause was guest free space below 1152 MiB at the selected `up`. EVD-061's observed failure stands; only its explanation is corrected here | true | none |
| EVD-064 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Run `p07vm004`, 2026-11-23T12:25:49Z, `main@4d4d56a7` plus working-tree repair that cleans apt caches before shutdown and records each boundary result in owner state | Claude Code root executor; QEMU 8.2.2 `accel=kvm` after the operator re-applied the `/dev/kvm` ACL and access `True` was read | `python3 scripts/test_cluster.py --root . up --vm --run-id p07vm004 --authority P07-bounded-VM platform-network-policies` | 2 | FAIL | Reached the in-guest `k3d cluster create`, which rolled back after 17 seconds; only the k3d FATA summary was surfaced. Owner state recorded `provision_probe` guest reachable as designed, `restricted_probe` `guest_restricted=true`, and `guest_enospc` `enospc=true, free_mib=1577`, so the guest admission reservation passed | true | none |
| EVD-065 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Guest ENOSPC step of `p07vm004` and again `p07vm005` inside the fixed 4080 MiB raw VM disk | Same KVM VM route; guest `posix_fallocate` larger than the whole filesystem | `_guest_enospc` through the owned SSH session | 0 | PASS | Both runs recorded `enospc=true` with 1577 MiB free before the request and free space restored afterwards: the per-run disk cap is enforced by the bounded VM disk. This is the supported hard-disk boundary used instead of the failed Docker `storage-opt` route; the host k3d route stays refused without it. It is a different route and command from EVD-007, so it does not resolve that Docker-route FAIL | true | none |
| EVD-066 | [AC-0004](../spec.md#criteria) | WORK-001 | observation | Restricted-phase probe of `p07vm004` and `p07vm005` after the guest rebooted on the `restrict=on` NIC | Owned host dummy endpoint with nonce; guest HTTP attempt to `10.0.2.2:<owned port>` | `probe_phase(restricted=True)` | 0 | PASS | `local_live=true` and `guest_restricted=true` in both runs: the restricted VM cannot reach the host-side endpoint while the endpoint is live. This is VM-level egress isolation only; the selected-namespace probe pod in W09-H02 was not reached, so W09-H02 stays open | true | none |
| EVD-067 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Run `p07vm005`, 2026-11-23T12:34:01Z, with the k3d diagnostic now carrying the first `ERRO` line | Claude Code root executor; QEMU 8.2.2 `accel=kvm` after the operator re-applied the `/dev/kvm` ACL and access `True` was read | Same `up --vm` command with run ID `p07vm005` | 2 | FAIL | `k3d cluster create: ERRO[0017] failed to gather environment information used for cluster creation: failed to get host IP`. A disposable host probe of two owned no-container networks (both removed by name and label) showed an isolated `--internal` network records no IPAM gateway unless `--subnet/--gateway` are given, which k3d needs for its host-IP lookup | true | none |
| EVD-068 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Run `p07vm006`, 2026-11-23T12:45:44Z, with the owned network created with a fixed explicit subnet and gateway | Claude Code root executor; QEMU 8.2.2 `accel=kvm` after the operator re-applied the `/dev/kvm` ACL and access `True` was read | Same `up --vm` command with run ID `p07vm006` | 2 | FAIL | `CLUSTER_NETWORK: isolated owned network is unverified`: the new exact IPAM equality rejected the guest Docker 29.1.3 output. The check now compares only the single config's subnet and gateway and reports the observed value | true | none |
| EVD-069 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Run `p07vm007`, 2026-11-23T12:53:30Z, after the IPAM check repair | Claude Code root executor; QEMU 8.2.2 `accel=kvm` after the operator re-applied the `/dev/kvm` ACL and access `True` was read | Same `up --vm` command with run ID `p07vm007` | 2 | FAIL | Network verification passed and k3d created the server container, then `ERRO[0197] Failed Cluster Start: Failed to start server k3d-hyk8s-test-991f8c2a-server-0` within k3d's 180-second wait; the cause after the node name was cut by the 160-character VM diagnostic bound. Selected readiness, the namespace probe pod and product workload were not reached | true | none |
| EVD-070 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Runs `p07vm004`–`p07vm007` after each failure | `test_cluster.py down` for 004 and 005; the failure path's own owned cleanup for 006 and 007; user systemd; `status`; `pgrep -a qemu-system` | `python3 scripts/test_cluster.py --root . down <run>` where state remained | 0 | PASS | Each exact unit was deleted and its expiry timer stopped; no `hyk8s*` unit, `.workspace-test` entry, status row or QEMU process remained after any run. Owned cleanup only | true | none |
| EVD-071 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria), [AC-0006](../spec.md#criteria) | WORK-001 | automated | Working-tree repairs on `main@4d4d56a7`: boundary results and apt cleanup in `scripts/test_cluster_vm.py`, first k3d `ERRO` line in `scripts/test_cluster.py`, explicit owned subnet/gateway and tolerant IPAM check in `scripts/test_cluster_environment.py`, with their tests | Pinned validation Python; Ruff | Each new or extended test first, then `scripts/run-contract-tests.py --root . --suite test-cluster`; `ruff check scripts tests` | 0 | PASS | Every new assertion failed before its repair; the suite then passed 127/127 across five modules and Ruff passed. Synthetic only; EVD-069 stays an open FAIL | true | none |

##### Resolution Links

EVD-007 is the unresolved required hard-disk enforcement failure. A later
actual PASS must name and match it; EVD-008 proves only owned cleanup.
EVD-016 is a separate unresolved blocking source review. Its four HIGH
findings require code repair and a fresh bounded review before source
readiness can be claimed; EVD-017's selected CLI sandbox PASS and EVD-018's
owned native cleanup do not resolve them. EVD-019 is an observed P08 native
binding residual, not a reason to erase P07's review result.
EVD-021 is the separate post-repair blocking review with three HIGH and one
MEDIUM lifecycle finding. Some original mechanisms were fixed, but the
active-start and workspace-identity defects required further repair;
EVD-022's sandbox PASS did not resolve source findings. EVD-023 records the
second review's exact owned cleanup.
EVD-025 is the third blocking source review. Its three HIGH state-retention,
collected-unit and partial-directory defects require repair and selected
revalidation. EVD-026's selected CLI sandbox PASS and EVD-027's exact owned
cleanup do not resolve them. VM boot, guest ENOSPC, LAN and selected readiness
remain unobserved; no repeated review or runtime success is inferred.
EVD-032 is the fourth blocking source review. Its two HIGH proof-loss paths
and two MEDIUM identity/durability paths remain for source repair and
selected revalidation. EVD-033's sandbox PASS and EVD-034's exact review-run
cleanup PASS do not resolve them; the
earlier synthetic PASS predates this review and is not a VM runtime result.
EVD-039's fifth review verifies that EVD-032's four triggers were repaired,
but opens a distinct blocking MEDIUM VM state-identity concurrency defect.
EVD-040's sandbox PASS and EVD-041's exact review-run cleanup PASS cannot
resolve it. The reviewed synthetic PASS is not an actual VM runtime result.
EVD-044's sixth changed-delta review confirms EVD-039's state-identity
defect repaired but identifies a distinct parent-intent release-before-
metadata-removal recovery retry gap. EVD-045's sandbox PASS and EVD-046's
exact review-run cleanup PASS cannot resolve this new MEDIUM source defect.
EVD-049's recovery-only review confirms the defect recorded in EVD-044 is
repaired; EVD-050 and EVD-051 separately
record its execution boundary and cleanup. EVD-052 was rejected before
execution; EVD-053 then actually ran the same route and failed, which supersedes
that deferral in fact without resolving it, and EVD-054 records only the owned
expiry cleanup. EVD-055's synthetic repair
PASS does not resolve EVD-053; only a matching actual retry can. EVD-056
records the unmet KVM precondition for that retry. EVD-057 is the actual
retry: it confirms the metadata-forward repair in fact but fails on a
distinct datasource-name cause, so neither EVD-053 nor EVD-057 is resolved.
EVD-058 records owned cleanup, EVD-059 the synthetic repair and EVD-060 the
missing KVM access afterwards. EVD-061 confirms the EVD-059 repair in fact
but fails on the guest-side admission disk reservation; EVD-053, EVD-057 and
EVD-061 all stay unresolved FAILs, and EVD-062 records only owned cleanup.
EVD-063 corrects EVD-061's explanation. EVD-065 is an actual enforced VM
disk cap on a different route; EVD-007 stays the unresolved Docker-route FAIL. EVD-064, EVD-067, EVD-068 and EVD-069 are later
FAILs; EVD-069 is the open runtime blocker. EVD-066 is VM-level isolation only
and does not close W09-H02.
Historical W09-H02 and W07-H05 stay under their original Task and ledger
owner.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0002](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0003](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0004](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0005](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0006](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |

##### Remaining Conditions

Draft review, current scoped R008 receipt, source implementation, focused
repository checks and both source-review blockers now have matching evidence.
Seven actual VM runs failed, each later than the one before; all owned
cleanups passed. Confirmed: VM boot, NoCloud provisioning, restricted reboot,
guest ENOSPC on the fixed VM disk (EVD-065; the Docker route of EVD-007
stays an unsupported FAIL) and restricted
VM egress denial (EVD-066). Open: the k3s server start inside the guest
(EVD-069), then selected readiness, the selected-namespace probe pod and
W09-H02.
All six operator criterion decisions remain pending; no criterion acceptance
is inferred from implementation, review, tests or merge.

#### Handoff

##### Promotion Receipt

The Plan's AD-0007 product-boundary promotion is intended, not yet reflected
or verified. Environment guide publication follows its own lifecycle.

##### Next Owner

The environment owner first surfaces the full k3s start failure: capture
the server container's last log lines on a failed `k3d cluster create` and
widen the bounded VM diagnostic so the cause is recorded, with a focused
failing regression. Likely areas are k3s system images that are absent in the
restricted guest and the 1536 MiB server memory cap; neither is confirmed.
After the host reboots, the user systemd manager carries the `kvm` group and
the per-run ACL step is no longer needed. Each further run keeps the
600-second and resource limits, records its result against EVD-069, and stops
on a repeated cause instead of looping. Then the operator records the six
criterion decisions separately.
Only after those P07 gates does the next package input remain
`prompts/P08-NATIVE-BRIEF.md`; this Task does not execute P08.

## 적용과 확인

### 적용 방법

Use this Task for factual P07 evidence and leave criteria pending until the
operator records decisions.

### 확인 기준

The initial draft and brief do not prove admission, network denial, native
enforcement, hosted CI or user acceptance. Each needs its actual result.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [P07 Plan](../plan.md) |
| verifies | [P07 Spec](../spec.md) |
| cites | [SPEC-0223 Task](../../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md) |

### 외부 근거

The package D07 and sources are dated design inputs. Installed-client,
host and cluster claims require local evidence recorded in Results.
