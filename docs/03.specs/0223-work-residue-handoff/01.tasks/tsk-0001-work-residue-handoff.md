---
title: "Work Residue Handoff"
version: "0.6.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0223-TSK-0001"
parent_ids: ["SPEC-0223-PLAN-0001"]
---

# Task: Work Residue Handoff

## Scope

### Objective and Parent

This Task runs the [Plan](../plan.md) for the [Spec](../spec.md): it hosts the
live work residue table, exits SPEC-0161, SPEC-0221 and SPEC-0222, and removes
the Task header transition adapter whose removal condition is their exit.

### Inputs and Authority

On 2026-11-19 (Asia/Seoul) the user asked to analyze the Specs, Plans and
Tasks under `docs/03.specs/` and delete what conflicts or differs with the
current implementation
(`docs/03.specs 폴더내 task, plan, spec을 분석하여 현재 구현과 상충되거나 충돌되면 삭제하고, 차이가 나면 삭제하고 정리한다.`).
Asked how to handle SPEC-0161, the user chose "Delete now, move
residues (Recommended)": a new residue host, then the deletion of all three
packages. Input revision: `93f130a8`.

- **Allowed Paths**: `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`, `docs/02.architecture/decisions/0063-affected-pr-gitops-validation.md`, `docs/99.templates/registry.json`, `.secrets.baseline`, `scripts/document_contracts.py` and its readers, `tests/`
- **Forbidden Paths**: `_workspace/`, `docs/98.archive/`, every residue's owner, state and resume condition
- **Approval Required**: none beyond the user's decision above; history removal stays with Q07-CUTOVER
- **Static Validation**: `python3 scripts/qa.py staged` on each commit
- **Live Validation**: not applicable; no runtime change
- **Secret / Vault Handling**: no secret is read; `.secrets.baseline` only loses entries of deleted files
- **Rollback Plan**: revert the commits newest first
- **Evidence Location**: this Task

#### P00 intake, 2026-11-20 Asia/Seoul

The current request is P00-RECONCILE, revision 1.0.0. Its input is the local
package `_workspace/workspace_governance_remediation_1_0_0_20261119/`, whose
manifest identifies `workspace_governance_remediation` 1.0.0. Read together:
`dependencies/execution-contract.md`, `questions.md`, `sources.md`,
`designs/D00-reconcile.md`, `baseline-4.2.0.md`, `workspaces/k8s.md` and
`evidence/k8s-findings.json`. Other workspace profiles and the older 4.2.0
package are not inputs. The manifest supplies the successor prompt names.

This request authorizes local reconciliation of the existing residue host;
it does not reapprove or reopen WORK-001 to WORK-003. The write scope is this
Task, profile `sdlc/task`, using
`docs/99.templates/02.templates/03.specs/task.template.md`. Preserve all past
EVD rows, criterion decisions, ledger pointers and resume conditions. The
classification below is evidence for the current request, not a second
execution ledger or an implementation claim for P01 to P17. Each successor
records its actual changes at its canonical owner and assigned Task.

No commit or external mutation is requested: preserve the index. Selected
validation is working-tree `python3 scripts/qa.py quick`, the residue gate
and diff checks; no new wrapper or prose-only test. Risk is low: evidence and
planning prose only, with no Kubernetes behavior change. Rollback removes
only the P00 additions and restores this Task's previous version/date.
Native trust, paid provider work, raw session reads, live cluster changes,
remote deletion and history rewriting are outside this execution.

#### P01 current authorization

On 2026-11-20 Asia/Seoul the user supplied the same package and selected
`prompts/P01-CI-ROUTING.md` only, explicitly requesting implementation,
verification, commit, push, pull request and merge. The input revision is
1.0.0; `dependencies/designs/D01-ci-routing.md` supplies the target, with
execution-contract, questions, sources and k8s profile/findings re-read.
P00 is retained predecessor evidence, not repeated work. The requested eleven
previously completed/merged work streams are not reimplemented; tests below
protect the newly changed consumers, not acceptance replay.

The current write boundary is the existing CI workflow and contract, affected
registry/runner and their regressions, shared document parsers and scoped
manifest validators, and their current quality/Git/architecture owners.
This is the P01 disposition of W06-H03, hosted coverage; its resume condition
is updated in this Task and the ledger together to the actual remaining PR
evidence, without changing any past EVD or criterion decision. W06-H02's
changed-manifest/lock observation kept distinct. The original Spec/Plan's
WORK-001 to WORK-003 and accepted criteria remain the completed residue
transfer; the following P01 evidence never re-labels their acceptance as CI
acceptance. No new Spec or parallel progress ledger is created for this
existing residue-host follow-up. QUAL-R006 and the actual execution registry
own the promoted CI contract; this Task owns the implementation evidence.

Risk is high because selection omissions can produce false success. The user
owns the original authorization and final criterion acceptance; the current
request authorizes the delivery actions, without authorizing deployment,
credentials, remote setting changes, other P prompts or history rewrite.
Rollback reverts the P01 change through a normal reviewed PR; no force push.
Workers own disjoint CI, document and platform files. Dispatch preflights
passed against this request and HEAD `6c352064`; all writers preserve other
edits. Read-only security/correctness reviews are policy restrictions, not
native Desktop sandbox evidence. P00's pre-existing uncommitted Task prose
is preserved in this delivery.

## Execution Log

### Work Performed

| Item | Work Unit | Owner | Status | Blocker |
| --- | --- | --- | --- | --- |
| WORK-001 | WORK-001 | platform | completed | none |
| WORK-002 | WORK-002 | platform | completed | none |
| WORK-003 | WORK-003 | platform | completed | none |

The analysis read the three packages and every consumer that names them. Every
path in the three Specs and Plans exists. The conflicts are: SPEC-0221 and
SPEC-0222 are completed with every criterion accepted, so DOCLIFE-R008
requires their exit; the SPEC-0161 Spec covers the W00 v14.7 intake while its
Task became the log of every later package; and `scripts/document_contracts.py`
and the registry keep a transition adapter and retained-form exceptions whose
own removal condition is these exits. WORK-001 moved the 30 open
residue rows here (all but T99-H03 from SPEC-0161) and repointed their ledger
entries; no owner, state or resume condition changed. The user then ran the
handed-over deletion, so W09-H03 closed: none of the ten approved paths
remains, and the 4.2.0 package, `.workspace-memory/` and `sessions/` stay.

WORK-002 used the WORK-001 commit `49f7a6f2` as the recovery source. Every
file matched its blob byte for byte before deletion. The guard hook refused
the agent's `git rm`, so the user ran it. Only the REQ-0003 lineage and proofs
still name the deleted paths. Citations by ID, such as `SPEC-0161 EVD-191`,
stay as the Spec states. ADR-0063 changed only its link target, and its
sentence and facts are unchanged.

WORK-003 ran on `eac89a91`, after WORK-002 merged, so no base Task carries the
recorded header. A test that a recorded header is not read failed first. The
cumulative history replay reads only commits between a comparison base and its
tip, which now all carry the core header; the older history readers stay with
Q07-H01. A one-item core Task takes its status from the frontmatter, so the
fixtures that exercised an item state or owner on a single item now use two
items or a changed criterion.

### Blockers and Decisions

No blocker remains for the original WORK-001 to WORK-003. P00 records the
following current reconciliation without changing their accepted outcomes.

#### P00 snapshot and existing obligations

Root: the current `hy-home.k8s` checkout; Git common-dir: `.git` under that
root. Both absolute paths were resolved by EVD-009; branch `main`; HEAD and profile base:
`6c352064909511300a862dff85ee82e4200b1e1c`. The initial worktree and index
were clean; `git diff PROFILE_SHA..HEAD --stat` was empty. No checkout,
clone, reset or source-worktree cleanup was performed. Installed surfaces:
`codex-cli 0.169.0`, Claude Code `2.1.328`, Python `3.12.3`. Version output
does not prove hook trust or permission enforcement. Codex reported that it
could not create PATH aliases on the read-only filesystem; version reporting
still succeeded.

GitHub searches on 2026-11-20 returned no open PR and latest merged PRs
[330](https://github.com/buenhyden/hy-home.k8s/pull/330),
[329](https://github.com/buenhyden/hy-home.k8s/pull/329),
[327](https://github.com/buenhyden/hy-home.k8s/pull/327),
[328](https://github.com/buenhyden/hy-home.k8s/pull/328) and
[326](https://github.com/buenhyden/hy-home.k8s/pull/326).
They introduce no delta after the profile HEAD. PR 327 moved the workspace
and category paths; PR 328 records its hosted run. PR 330 converted the
history-dependent checks, not the final Q07 data. PR merge, static checks,
native runtime and user acceptance remain separate facts.

This [Spec](../spec.md) and [Plan](../plan.md) keep their accepted exit and
adapter-removal obligations; this Task remains the live residue host.
[SPEC-0224](../../0224-workspace-path-cutover/spec.md) and its
[Task](../../0224-workspace-path-cutover/01.tasks/tsk-0001-workspace-path-cutover.md)
already have accepted VAL-CUTOVER-001 to VAL-CUTOVER-003, with DOC-H01 left.
[SPEC-0225](../../0225-q07-history-bound-checks/spec.md) and its
[Task](../../0225-q07-history-bound-checks/01.tasks/tsk-0001-q07-history-bound-checks.md)
have accepted VAL-HISTORY-001 to VAL-HISTORY-004, with Q07-H01 data left.
Their moves, baseline mechanism and retained-form marker are excluded from
reimplementation. P05 owns later package disposition after consumer and
residue succession; P17 owns final numbering. Neither an old W11 acceptance
nor the current prompt accepts the unresolved provider or network failures.

#### P00 owner and consumer inventory

`git ls-files` enumerated the current files under every area below, including
Stage 98's README and placeholders. This table records the owner routes and
affected consumers, not a fixed corpus count. Old unnumbered category paths
in the baseline resolve to these current numbered paths.

| Area and current owner | Actual consumers and relevant files | Successor |
| --- | --- | --- |
| `docs/00.workspace/` | `03.process/{sdlc,document-authoring,document-lifecycle,git}.md`, `04.quality/{quality,approval-and-safety,formatting-and-linting}.md`, `01.project/glossary.md`, AD-0006 and workspace ADRs; read by gateways, roles, QA and document authors | P03/P05; preserve PR 327 layout |
| `docs/01.requirements/` and `docs/02.architecture/` | REQ-0001 to REQ-0004; product AD-0004/0005/0007 and `02.decisions/`; lifecycle, runbooks and GitOps consumers; REQ-0002 mechanism text remains W04-H07 | P05; architect owns structure |
| `docs/03.specs/` | Packages 0223/0224/0225, their Plans and `01.tasks/`, and `work-residue-ledger.json`; lifecycle, acceptance and ledger readers | P05/P16/P17; preserve actual acceptance |
| `docs/05.operations/` | `02.policies/`, `03.runbooks/`, guide/incident routers; operational callers and core Steps/Failure/Enforcement/escalation fields | P05/P14-K8S |
| `docs/90.references/` and `docs/98.archive/` | Numbered research/audit/data collections and published members; retained forms, ADR-0026/0028 links and lineage readers; Stage 98 is unvalidated, not authority | P05/P17; no P00 deletion |
| `docs/99.templates/` | `registry.json`, `01.contracts/`, `02.templates/`; `document_contracts.py`, generator, profile/link/lifecycle validators and document-content QA | P04; adopted metadata and text need repair |
| `.agents/` and root gateways | Governance, workflows, roles/registry, skills, prompts, knowledge maps; `.codex/` and `.claude/` projections, bindings and provider notes consume them | P03/P06/P08/P09 |
| Native hooks | `.codex/hooks.json`, `.codex/hooks/{pre-tool-use,session-capture}.sh`; `.claude/settings.json`, `.claude/hooks/{session-start,k8s-pre-edit,session-capture}.sh`; shared `provider_write_guard.py` and `session_capture.py` | P06/P08/P10; configuration is not delivery |
| `scripts/` and `tests/` | `workspace_memory.py`, `session_{capture,analysis}.py`, `work_{forecast,parallel}.py`, `test_cluster.py`, `review_delta.py`, `semver_grammar.py`; their existing focused regressions | P07/P09/P10/P11/P12 |
| QA, CI and Git hooks | `validation/registry.json`, `qa.py`, `run-validation-lane.py`, selected style/nonstyle and purpose validators; `.github/workflows/ci.yml`, requirements lock, ruleset record, `.pre-commit-config.yaml`, `scripts/githooks/{chained-hook.sh,pre-commit,commit-msg,pre-push}` | P01/P02/P13; configured hooksPath is this checkout's `scripts/githooks` |

#### P00 findings decisions

The IDs below are the package's k8s findings. `Maintain` excludes only the
stated implemented guarantee. Existing tests without a recorded run are
coverage, not new PASS evidence. P00 read the frozen SPEC-0161 evidence from
the exact Task path in REQ-0003's recovery proof at `49f7a6f2`, without
restoring that package. Reused evidence: EVD-180 numeric-version checks;
EVD-193/195/197 memory regressions;
EVD-196/198 actual Claude/Codex memory roundtrip and search in a synthetic
repository (no project-hook proof); EVD-206/208/223 cluster regressions and
EVD-224 selective live lifecycle/probe; EVD-213/214 forecast regression and
Claude measurement; EVD-215 to EVD-218 shell dispatcher, patch hardening and
integration; EVD-219 review-delta regressions; EVD-226 clean-clone regression
coverage. Those are past results over their stated inputs, not new runtime
runs on this HEAD. In particular EVD-208 is PASS for the repaired tool and
isolated-namespace probes; it does not establish whole-cluster LAN denial.

| Finding | Disposition | Current implementation, consumer and evidence | Remaining work |
| --- | --- | --- | --- |
| K8S-01 | Supplement | Ledger has 30 entries, 28 open and 2 terminal; source Tasks retain each obligation and closure | Individual decisions below; P16 cannot blanket-accept native failures |
| K8S-02 | Supplement | Stage 99 `shared_contract` says adopted with unverified approval fields; document consumers read that contract | P04 reconcile adoption meaning and compatibility; invent no approval |
| K8S-03 | Maintain | Workspace AD/ADRs and policy split exist under `docs/00.workspace/`; SPEC-0224 EVD-010/013 and accepted criteria | Exclude directory relocation; P03 removes only remaining duplication |
| K8S-04 | New | `docs/00.workspace/01.project/glossary.md` owns shared terms; `.agents/knowledge/glossary.md` is absent | P03 split common definitions from K8s vocabulary with its validator consumers |
| K8S-05 | Maintain | `scripts/semver_grammar.py` checks numeric ASCII X.Y.Z; SPEC-0161 EVD-180 records numeric fixtures, ordering and 104 passing semver/frontmatter tests; `tests/test_semver_grammar.py` is existing coverage, not newly run here | Exclude parser rewrite; P04 documents version-change meaning |
| K8S-06 | Supplement | Registry/forms and document readers exist; SPEC-0205/0211 text defects remain in this Task | P04 correct content at each owner; no corpus-count test |
| K8S-07 | Supplement | Work lifecycle intake and `validate-execution-brief.py` exist; parallel runner consumes a brief; native configs lack prompt-submit briefing | P08 add native delivery at actual supported events; retain brief contract |
| K8S-08 | Unobserved | Codex provider note and W08-H03 cite SPEC-0161 EVD-201: lifecycle hooks parsed but untrusted | P08/P10 normal user hook review and actual event observation; no trust bypass |
| K8S-09 | Supplement | W07-H05 preserves Desktop/SSH workspace-write and null-profile FAIL, EVD-163/167 | P06 repair or explicitly choose another verified surface; denial probe on the exact path |
| K8S-10 | Maintain | Risk-based review policy and `review_delta.py` exist; SPEC-0161 EVD-219 records regression PASS; SPEC-0224 EVD-006 records an independent review, not runtime isolation | Exclude review-policy rebuild; apply to new high-risk changes in P06 |
| K8S-11 | Maintain | `workspace_memory.py` implements common-dir store, CAS/revision, idempotency, provenance, retrieval, quota and backup; SPEC-0161 EVD-193/195/197 regressions and EVD-196/198 two-provider synthetic-store roundtrip/search PASS | Exclude core and that roundtrip replay; P09 verifies changed workspace binding/adapters and actual current-workspace use; no broker without its trust condition |
| K8S-12 | Supplement | `session_capture.py`/`session_analysis.py` store metadata and count rules; W08-H05 cites EVD-222 mixed failure types | P10 call correlation and classification; Q-02 limits content/TTL/new external transmission |
| K8S-13 | Supplement | `session_analysis.py` uses fixed `hy-home-k8s-session-analysis` units; separate workspace installs can collide | P10 workspace-specific units and two-workspace regression; not runtime-only deferral |
| K8S-14 | Maintain | `work_forecast.py` records forecast, elapsed/active/waits and scores; SPEC-0161 EVD-213 regression PASS and EVD-214 Claude measurement; Codex use still W10-H01 | P11 native roundtrip only; no unsupported calibration claim |
| K8S-15 | Supplement | `work_parallel.py` has DAG/clones/path and resource leases/fencing/integration; SPEC-0161 EVD-215 to EVD-218 regression and shell integration PASS; W10-H02/H03 bound containment | P12 provider adapter and OS containment/state gap; retain shell DAG |
| K8S-16 | Maintain | `test_cluster.py` has small owned k3d, isolated kubeconfig, closure limit and failure cleanup; SPEC-0161 EVD-206/208/223 regressions and EVD-224 selective live PASS with no product pod | P07/P14-K8S selected component modes; base runner stays |
| K8S-17 | New | Cluster app limit and dispatcher conflict set apply per invocation; no workspace-wide atomic admission/aggregate CPU-memory cap | P07/P12 shared admission with concurrent refusal/release checks |
| K8S-18 | Supplement | W09-H02 records the whole-cluster isolation defect despite EVD-208/224 PASS for separate deny-namespace probes; product policies still allow production LAN | P07/P14-K8S host/VM deny boundary before product pods; P00 has no fresh network probe |
| K8S-19 | Supplement | `ci.yml` PR leaves cover metadata/style/CI-lock/GitOps identity; main metadata N/A does not test features; SPEC-0224 EVD-013 covers those hosted leaves only | P01 affected implementation/document leaves and outcome aggregation; no full-suite-on-every-event |
| K8S-20 | Unobserved | Chained hook and configured hooksPath exist; actual hook latency/global chain not measured | P02 separate setup, selected leaf and wait costs; no new pre-push full test |
| K8S-21 | Maintain | `_workspace/README.md` cleanup boundary exists; W09-H03 terminal with this Task EVD-002 | P15/P17 consumer-based cleanup only; preserve package through P17 |
| K8S-22 | Supplement | SPEC-0225 EVD-002/003/004/006 and accepted criteria cover code conversion; DOC-H01/Q07-H01/T99-H03 preserve remaining data | P17 coordinated final numbering, links and disposition; do not repeat PR 330 |

#### P00 individual residue routing

This is a classification of the existing live rows, not new residue entries.
The original source row retains its state, owner and resume condition. Every
entry is assessed once; 30/28 is this observation, not a permanent count gate.
The default source is this Task's Residue Handoff; DOC-H01 and SDLC-H01 are
in the SPEC-0224 Task linked above. Known defects below require repair, not
an observation waiver. Conditional applicability does not cancel an obligation.

| Decision and kind | Existing entry | Evidence and successor owner |
| --- | --- | --- |
| Unobserved; native event | AGENT-04 | P08/P16 provider owner observes nested/resume/compact delivery on trusted surfaces |
| Maintain; future cutover | DOC-12 | P17 doc owner; numbering only after applicable work, not another directory move |
| Maintain; future cutover | DOC-H01 | SPEC-0224 EVD-010; P17 doc owner keeps ID renumbering/Stage 98 disposition |
| Maintain; future cutover | Q07-H01 | SPEC-0225 accepted code conversion; P17 data owner handles lineage, git-show citations, reference identity bounds and dormant historical_tables |
| Maintain; conditional refresh | R147-17 | `.codex/provider.md` already distinguishes static/native evidence; P06/P08 provider owner reobserves on next native edit |
| Maintain; terminal exclusion | SDLC-H01 | SPEC-0224 EVD-010/013; workspace move complete; P17 removes terminal pointer at package exit |
| Supplement; current text defect | SPEC-0205-STALE-TEXT | P04 form/registry owner corrects the listed Plan, AGENTS and TemplateDefinition wording |
| Supplement; current text defect | SPEC-0211-REGISTRY-TEXT | P04 registry owner corrects recorded labels, copies, particles and duplicate diagnostic descriptions |
| Maintain; future disposition | T99-H03 | P17 reference/architecture owners preserve published facts and ADR-0026/0028 consumers before disposing predecessors |
| Supplement; current content gap | W04-H02 | P05 runbook owner supplies the listed Expected Result/On Failure cells; no invented runtime outcome |
| Supplement; current content gap | W04-H03 | P05 architecture owner supplies Failure boundaries for AD-0004/0005/0007 and gitops README interfaces |
| Supplement; current evidence gap | W04-H04 | P05 reference owner reobserves version/application/limits and audit requirement facts under RUN-0011 |
| Supplement; current enforcement gap | W04-H05 | P05 policy owner gives ROLLOUT/ONBOARD rules a check or explicit semantic-review enforcement |
| Supplement; current owner gap | W04-H06 | P05 operations owner names escalation and break-glass approver; do not invent a contact or authorization |
| Supplement; current owner mismatch | W04-H07 | P05 requirement/architecture owners move REQ-0002 mechanism meaning to AD-0005; keep acceptance intent |
| Unobserved; selected hosted leaf | W06-H02 | EVD-211 covered docs only; P01/P14-K8S observes a PR actually selecting CI lock or changed GitOps manifest |
| Supplement; current coverage gap | W06-H03 | P01 CI owner implements affected feature/doc checks beyond current hosted leaves |
| Supplement; required rejection coverage | W07-H03 | P06 safety/validation owner verifies W01-B negative cases; QA/status/hash never grants approval |
| Supplement; recorded runtime FAIL | W07-H05 | EVD-163/167; P06 host owner repairs Desktop/SSH boundary or names an alternate verified path; original path stays failed |
| Maintain; future trust condition | W08-H01 | P09 memory owner: same-account strings are unauthenticated; broker/OS boundary only before another account/untrusted/remote writer |
| Maintain; future search condition | W08-H02 | P09 retrieval owner: particle/inflection miss or scale/p95 condition triggers upgrade; no vector/broker work now |
| Unobserved; native capture | W08-H03 | EVD-201; P08/P10 user reviews hooks, provider owner observes Codex lifecycle and Claude compact |
| Unobserved; real catch-up | W08-H04 | EVD-222 proves first 03:00 KST run, not downtime recovery; P10 scheduler owner observes real catch-up |
| Supplement; current attribution defect | W08-H05 | EVD-222; P10 capture/analysis owner adds call ID and distinct deliberate-negative/permission/hook/error outcomes |
| Supplement; known isolation defect | W09-H02 | EVD-208/224 cover selective probes, not whole-cluster denial; P07/P14-K8S environment operator establishes LAN deny before product pods; no blanket W11 acceptance |
| Maintain; terminal exclusion | W09-H03 | This Task EVD-002; previously approved ten paths already absent; no repeat deletion |
| Unobserved; provider roundtrip | W10-H01 | EVD-214; P11 Codex owner uses the same forecast store for create/start/finish/score |
| Unobserved; provider worker | W10-H02 | EVD-216 shell-only user choice; P12 provider owner resolves Q-03 cost/surface scope before model workers |
| Supplement; current containment defect | W10-H03 | EVD-215; P12 runner/OS owner closes setsid/out-of-clone writes/disk/state-persistence gaps before provider/untrusted workers |
| Unobserved; future scheduled result | W10-H04 | EVD-221/222; P13 analysis owner checks candidate 1 after 2026-11-21 03:00 Asia/Seoul, over 2026-11-20; no future success claim |

#### P00 execution order and questions

The next input is `prompts/P01-CI-ROUTING.md` in the same package. Continue
P01 affected QA, P02 local feedback, P03 ownership/vocabulary, P04 common
forms/adoption, P05 current docs/SDLC, P06 independent-review execution,
P07 aggregate environment limits and isolation, P08 native briefing,
P09 memory integration, P10 sessions/timer, P11 forecast integration,
P12 provider parallelism/containment, P13 observable improvements,
P14-K8S selected product validation, P15 consumer cleanup, P16 explicit
acceptance, then P17-FINAL-CUTOVER. The manifest's k8s predecessors govern
dependency order; a blocked protected step holds only its dependents. No
successor implementation is claimed by this list.

Q-01 applies only to P17 remote history/PR/tag/artifact/locked-backup deletion;
current-tree planning proceeds without that authority. Q-02 applies to P10's
new redacted content, retention and paid external transmission, which differ
from the current metadata-only policy. Event identity/cursor/atomicity work
does not depend on expanding collection. Q-03 applies to P06/P08/P10/P12
supported surfaces and any additional model usage; retain the recorded
shell-only cost choice until changed. Normal supported CLI implementation is
not blanket-blocked by a Desktop gap. Q-04 concerns Blog public text and is
not applicable here. No OPEN01 to OPEN14 question is reopened; P00 itself
needs no additional decision to record these distinctions.

Implementation and local verification of P00 mean this reconciliation is
written and checked. User acceptance of P00 is not yet recorded. Historical
acceptances above remain valid for their own criteria. Provider/runtime,
hosted feature regressions and live service validation are not performed by
this documentation change; successor owners must repair the named defects
before claiming their runtime success.

#### P01 implementation and verification

Current branch `codex/p01-ci-routing` starts at `6c352064`, the unchanged
profile HEAD. The initial sole dirty path was this Task's P00 record. A dated
read-back of `main` protection confirms `ci-summary` and `style-pr` from
App 15368, strict latest-head checks, administrator enforcement and zero
required approving reviews. Merge commits are enabled; squash/rebase are
not. This is observed remote configuration, not a hosted test result.

| Consumer / current requirement | Implementation and retained behavior | Verification / acceptance boundary |
| --- | --- | --- |
| PR cumulative input | Exact base/head/two-parent merge binding; NUL diff contains both moved sides and deletions; no last-commit shortcut | CI metadata/plan regressions; user acceptance pending |
| One affected plan | Registry `pull-request` profile selects current affected static consumers, excluding the local repository-quality aggregate; saved plan binds base, head and registry | Valid empty is N/A; missing base, unknown paths and altered plans fail |
| Selector/config self checks | Profile coverage cannot remove affected leaves; changing registry/schema/selector/runner forces routing contract and regression checks even if its own route changes | Three review counterexamples failed first, then passed |
| Required aggregate | Existing `style-pr` requires plan success and success of selected style/purpose steps; skipped selected, missing, cancelled and failed outcomes block | CI negative tests cover every outcome; no workflow path filter or new merge queue |
| Document consumers | Existing links/profile leaves run once in a shared invocation with bounded text, index, registry, frontmatter and heading caches; unchanged inbound/body scope remains | Cache identity, changed content, symlink and separate failure regressions; no persistent result reuse across trust boundaries |
| Manifest consumers | Changed paths select Kustomization owners and reverse dependencies; the global raw identity index compares base/head including deletions; shared render/schema changes broaden their actual consumers | Partial render/schema PASS is separate from product-semantic, unsupported CRD and live DEFER |
| CI environment and trust | Pinned Actions, reviewed-base style config and hashed Python lock retained; candidate purpose code gets read-only token, no secrets/persisted credentials | Selected Kustomize binary hash and Conftest image digest; no production operation |

| Execution point | Input and check | Reuse / remaining guarantee |
| --- | --- | --- |
| Commit before/during | Exact index via existing staged-qa and message hooks | Existing local contract unchanged; no post-commit sweep |
| Push before/during/after | Existing chained ref hook and remote transfer/protection | No added pre-push test; do not replay staged leaves merely for push |
| PR before/during/after | Local selected evidence, then bound cumulative test-merge plan, style and purpose, always-run aggregate | Hosted evidence needs the actual run; no second post-PR suite |
| Merge before/during/after | Latest required checks and reviewed candidate, merge commit, integrated tree comparison | Main push metadata N/A is not a product PASS; no identical post-merge replay |

Observed focused results (Python 3.12.3 in the existing pinned validation venv):

- Initial PR-plan tests: five ERROR results before the missing API was
  implemented; the first five then PASS. Selection/profile tests plus the
  plan cases PASS, 53 tests in 3.26 seconds after three review-found omission
  cases first failed and were corrected.
- Pure runner selection/result vocabulary/platform-report/plan cases: 26
  PASS in 2.49 seconds before the later self-exclusion corrections; those
  corrections have their separate 53-test evidence above.
- Document worker: 52 focused scope/frontmatter/cache tests PASS in 8.6
  seconds; the duplicate-read case failed first. Combined links and profile
  CLI reports both PASS. This is local evidence, not hook delivery.
- Platform worker: 31 focused assurance/GitOps identity cases PASS. Negative
  tests caught a deleted shared base omitted from an overlay and false
  control-root DELETE rows, both corrected. The initial pinned Kustomize scoped
  static run renders seven related roots with PASS; at that point CRD schema
  and partial global product semantics were DEFER. The later review repair
  below adds complete cross-root identity coverage. No cluster was started.
- CI worker: `python3 scripts/run-contract-tests.py --root . --suite
  ci-metadata` reports 90 PASS; strict CI Python contract and Actions security
  checks PASS. Workflow plan/aggregate cases cover cumulative changes,
  deletions, base mismatch, empty diff and non-success outcomes.
- Independent security review reproduced configuration self-exclusion and a
  tooling route with no hosted consumer. Both are fixed with regressions;
  `.rtk` now has an explicit routing-contract consumer. The review also
  corrected a stale QUAL-R031 claim. No remaining HIGH security finding was
  reported. Final correctness review, exact-index QA and hosted execution
  are recorded at delivery, not presumed from these focused results.

Later correctness review found three issues and the fixes have focused
negative regressions: combined document leaves now return a closed JSON report
with independent leaf exits; the runner rejects malformed/missing reports and
records a passing link leaf separately from a failing profile leaf. Raw syntax
and policy gates now consume only selected YAML inputs via the existing
assurance entrypoint, preserving `conftest verify` and broadening on their
actual global parser/policy inputs. The GitOps identity checker keeps its original global bounded raw YAML
traversal, which detects identical identities in different files while
deduplicating reuse of one shared base path. This is a genuine global consumer
index, not Kustomize execution. The earlier scoped-identity attempt was removed
when it lost that negative guarantee; actual expensive Kustomize rendering
remains scoped to affected roots. The platform worker's final 36 focused cases PASS, including empty scope,
missing root, deleted base, cross-root collision and symlink ancestry.

The saved plan also computes actual nonempty render/policy targets before
requesting external tool downloads. A deletion-only PR whose consumers have no
remaining targets does not depend on unused Kustomize or Conftest downloads.

The first exact-index staged QA completed the document regressions in 480.830
seconds, QA-runner regressions in 592.779 seconds and routing regressions in
29.192 seconds, all PASS. It rejected two delivery details: this Task embedded
the machine's checkout path, and the two changed shell helpers differed from
the pinned shfmt format. The portable root description and shell whitespace
were corrected before a new exact-index run. These were failed gates, not
runtime observation deferrals; no validation hook was bypassed.

A same-input local comparison on `docs/README.md` ran fresh processes over a
warm filesystem (N=1 per mode, downloads excluded): separate links/profile
commands PASS in 21.319 seconds total; the shared invocation PASS in 19.364
seconds. This single pair is not a p95 or a general speed guarantee. Baseline
hosted PR 330 CI run 44532788099 took 41 seconds end to end: style-pr queue
3 seconds, job 38 seconds, checkout 5 seconds, Python setup/install 6 seconds,
plan below the one-second timestamp resolution, lint 18 seconds and aggregate
below one second. CI-lock and GitOps leaves were skipped. This older run had
no affected purpose guarantee, so its wall time is not a same-coverage speed
comparison with P01. The final PR's own step times must be reported separately.

P01 implementation, final exact-index staged QA, commit-message checks and
hosted verification are complete. [PR 331](https://github.com/buenhyden/hy-home.k8s/pull/331)
integrated commit `e9f72ced7297e86c287b9634958ea838ac01bec7` as
`60ff97bd63c87e233cc00cb1f4ac64b53d7bdf16`. Its test merge was
`43d84095135e08b5d5769da3e224bc20ef9eae96` over base `6c352064`.
`git diff --exit-code e9f72ced7297e86c287b9634958ea838ac01bec7 HEAD`
was empty after fast-forwarding to the integrated result. These identities
describe this execution; they create no general approval gate.

[CI run 44581637168](https://github.com/buenhyden/hy-home.k8s/actions/runs/44581637168)
completed successfully on 2026-11-19 UTC (2026-11-20 Asia/Seoul). Both required
checks passed, and all 25 selected purpose leaves passed. No unrelated memory,
forecast or parallel-worker suite was selected. Hosted document regressions
took 300.365 seconds, QA-runner regressions 65.795 seconds and routing
regressions 8.002 seconds. The shared links/profile invocation took 17.363
seconds for both leaf results; it is not two separately timed executions.

| Hosted phase | Observed elapsed time | Boundary |
| --- | --- | --- |
| CI end to end | 479 seconds | Run creation to completion; N=1 |
| style-pr queue / job | 3 / 475 seconds | Run creation to job start / job start to completion |
| Checkout | 6 seconds | Reviewed base and complete candidate history |
| Python setup / dependency installation | Below one second / 2 seconds | Existing runner tool cache; locked dependency installation |
| Candidate binding and plan | Below one second | One saved cumulative plan |
| Selected style | 20 seconds | Reviewed-base configuration |
| Selected tool preparation | 3 seconds | Kustomize download and pinned Conftest pull |
| Purpose execution | 438 seconds | Related static contracts and regressions |
| Aggregate | Below one second | Required selected outcomes verified |

The new hosted run has more guarantees than baseline PR 330, so their wall
times are not a same-coverage speed comparison. Timestamp values below one
second are limited by the API's one-second resolution. These are observations,
not a p95 claim. Platform rendering and static policy passed; absent external
CRD schemas and live observation remain DEFER. The platform report routes its
syntax depth to the separate manifest leaf. W06-H03 is terminal on EVD-016.
W06-H02 remains open because this PR changed neither the CI lock nor a GitOps
manifest; a workflow-triggered CI contract PASS does not satisfy that input
condition. P14-K8S retains actual manifest/runtime observation.

The six task-owned temporary execution briefs, PR-body file, style path list
and merge-message file were removed; the input package, other active work,
persistent memory and reusable QA cache were retained. This delivery receipt
is checked through the existing document consumers without replaying unchanged
implementation suites. User acceptance of P01 is pending. Q-01 to
Q-04 add no P01 dependency: no remote history deletion, new transcript
collection, paid provider observation or Blog publication boundary is needed.
After P01's delivery result, the next input is
`prompts/P02-LOCAL-FEEDBACK.md` in this same package; its prerequisites are
P00's retained reconciliation and P01's actual selected-CI result. Do not
start P02 automatically.

### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [VAL-RESIDUE-001](../spec.md#criteria) | PASS | EVD-001 |
| WORK-002 | [VAL-RESIDUE-002](../spec.md#criteria) | PASS | EVD-005 |
| WORK-003 | [VAL-RESIDUE-003](../spec.md#criteria) | PASS | EVD-007 |

## Verification Evidence

### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | automated | Staged WORK-001 index on `93f130a8` | pinned `hyhome-validation` venv | `python3 scripts/validate-work-residue-ledger.py --root .` | 0 | PASS | this Task, Residue Handoff | true | none |
| EVD-002 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | observation | The ten paths the user approved under SPEC-0161 EVD-226, after the user ran the handed-over deletion command in this session, 2026-11-19 | `test -e` per path | `test -e PATH` for each of the ten paths | 0 | PASS | this Task | true | none |
| EVD-003 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | review | {"spec_sha256": "5ede5efa66a40122c5d0651d8ba854b8f9929da56a68cfd27cfde2b5dfc81b94", "plan_sha256": "98c32d79128a767feee943a1afc5cea719771db3fe1c39b3ef368a7f194fab51"} | read-only code-reviewer sub-agent, separate context | Independent semantic review | none | PASS | this Task; review: no BLOCK, four FIX applied (adapter readers named, VAL-RESIDUE-003 added, consumer list completed, count of 30 stated), NOTE: WORK-003 after WORK-002 | true | none |
| EVD-004 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | observation | {"actor": "user", "approval_ref": "user answer 'Approve (Recommended)' of 2026-11-19 in this session", "review_ref": "EVD-003", "scope": ["SPEC-0223", "SPEC-0223-PLAN-0001"], "reviewed_spec_sha256": "5ede5efa66a40122c5d0651d8ba854b8f9929da56a68cfd27cfde2b5dfc81b94", "reviewed_plan_sha256": "98c32d79128a767feee943a1afc5cea719771db3fe1c39b3ef368a7f194fab51", "validity": "confirmed", "revocation": "none"} | none | Spec/Plan first-record approval | none | PASS | this Task | true | none |
| EVD-005 | [VAL-RESIDUE-002](../spec.md#criteria) | WORK-002 | automated | Staged exit index on `49f7a6f2`: the nine files of SPEC-0161, SPEC-0221 and SPEC-0222 deleted; REQ-0003 lineage rows and recovery proof; 42 terminal ledger entries of the deleted Tasks removed; registry `historical_tables` emptied and the Spec and Plan retained forms removed; four baseline entries, the Stage 03 and Stage 99 README sentences, ADR-0063's link and the retained-form tests removed | pinned `hyhome-validation` venv | strict lifecycle, profile, link and registry validators; ledger gate; `git grep` for the three package paths | 0 | PASS | REQ-0003 Archived Lineage; this Task | true | none |
| EVD-006 | [VAL-RESIDUE-003](../spec.md#criteria) | WORK-003 | automated | `test_a_task_table_under_the_retired_recorded_header_is_not_read` on `eac89a91` before the removal | pinned `hyhome-validation` venv | `python -m unittest tests.test_task_execution_contract` (one test) | 1 | FAIL | the recorded header was still read as `recorded` | false | none |
| EVD-007 | [VAL-RESIDUE-003](../spec.md#criteria) | WORK-003 | automated | Branch `claude/task-adapter-removal` on `eac89a91`: `TASK_RECORDED_HEADERS`, its helpers, the `pre_core` branch and the unreachable `TASK-HEADER-MIXED` result removed; readers in the link and profile validators read only the core header; the two pre-core registry transition test classes, the mixed-header test and the cumulative-history replay across the pre-core column names deleted; fixtures moved to the core form; `tests/task_rows.py` keeps the compact fixture renaming test-side | pinned `hyhome-validation` venv | the new test, `tests.test_task_execution_contract`, `tests.test_task_acceptance_contract`, `tests.test_task_acceptance_boundaries`, `tests.test_document_lifecycle_completion`, `tests.test_common_form_tree`, `ruff check` and `git grep` for `TASK_RECORDED_HEADERS` | 0 | PASS | this Task | true | none |
| EVD-008 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | observation | `main` `91ba3a10` after the Q07 path cutover (SPEC-0224); the eight checks named by Q07-H01 | `git grep` and source reads | Read each Q07-H01 check in `scripts/`, `tests/` and the registry | 0 | PASS | this Task, Residue Handoff Q07-H01: the `historical_tables` path is gone (value `[]`; the schema key and its reader in `scripts/validate-work-residue-ledger.py` stay), and the other seven checks stay active. They are `FIRST_ADR_OUTSIDE_RETAINED_RANGE` (`scripts/document_contracts.py`) with the ADR-0001 to ADR-0061 registry bounds; `reserved_codes` `PLAT`, `OBS` and the never-shrink check (`scripts/document_lifecycle.py`); the Archived Lineage reservations of `document_lifecycle.py` and `document-generator.py`; `reachable_git_path_exists` used by `scripts/validation/repository/quality.py`, with 31 `git show <sha>:` references in 12 current files; the cumulative replay of up to 256 first-parent commits over registry majors 10 to 21; the requirement-path tests in `tests/test_common_form_tree.py` and `tests/test_document_artifact_identity.py`; and `historical_major` in `scripts/document_contracts.py`. None of them reads a category folder, so the path cutover did not touch them | false | none |
| EVD-009 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | observation | P00 1.0.0 on `main` `6c352064`; same-SHA k8s profile and current tree, 2026-11-20 Asia/Seoul | Git; GitHub connector; installed Codex/Claude version commands | `git status --short`; `git rev-parse --show-toplevel --git-common-dir --abbrev-ref HEAD`; `git rev-parse HEAD`; `git diff PROFILE_SHA..HEAD --stat`; `git ls-files` over the owner inventory; GitHub open/merged PR searches; `codex --version`; `claude --version` | 0 | PASS | this Task, P00 snapshot, owner inventory and individual decisions; no open PR, no post-profile local delta; hosted/native execution is not established | false | none |
| EVD-010 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | automated | Initial P00 Task prose on `6c352064`; source index read-only in the active execution environment | Python 3.12.3 in `/home/hyunyoun/.venvs/hyhome-validation/` | `/home/hyunyoun/.venvs/hyhome-validation/bin/python3 scripts/qa.py quick` | 1 | FAIL | QA could not create `.git/qa-read-index-*`; environment restriction before selected checks, not a document verdict | true | none |
| EVD-011 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | automated | Same initial P00 prose, before the subsequent historical-evidence citation corrections | Same validation venv; native permission granted for QA temporary Git-index/snapshot files | `/home/hyunyoun/.venvs/hyhome-validation/bin/python3 scripts/qa.py quick` | 0 | PASS | Five selected leaves: document-contract-registry, document-lifecycle, work-residue-ledger, links-and-owners and markdown-profiles; all repository-static; source index and HEAD preserved | true | EVD-010 |
| EVD-012 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | automated | P00 table after historical-evidence correction; package finding IDs, current ledger IDs and original Task at HEAD | Python standard library; inline, no script file | Assert each input finding and ledger ID has one classification; compare original EVD, live Residue Handoff and Criterion Decisions against HEAD; `git diff --cached --name-only -z`; `git diff --check` | 0 | PASS | Each of the 22 findings and 30 entries occurs once; original evidence, residue and acceptance rows unchanged; index clean | false | none |
| EVD-013 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | review | P00-only Task diff on `6c352064`, after evidence-citation corrections; no executable or governance contract change | Independent code-reviewer subagent in separate context, read-only by policy | Semantic diff review against P00 completion conditions | none | PASS | Two FIX findings resolved: numeric-version validation now cites actual EVD-180; EVD-208 PASS probes distinguished from whole-cluster LAN defect. No remaining BLOCK/FIX. No native read-only enforcement claim | false | none |
| EVD-014 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | automated | Final P00 classification, corrected historical citations and EVD-009 to EVD-013 on `main` `6c352064`; only this receipt and the Next Owner receipt wording added afterwards | Python 3.12.3 in `/home/hyunyoun/.venvs/hyhome-validation/`; same selected QA configuration | `/home/hyunyoun/.venvs/hyhome-validation/bin/python3 scripts/qa.py quick` | 0 | PASS | All five selected document/ledger leaves PASS; inline preservation/coverage assertions and `git diff --check` PASS; no staged, hosted, native or live execution claimed | false | none |
| EVD-015 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | automated | Final P01 exact staged tree producing `e9f72ced`, after portable Task paths and pinned shell formatting were corrected | Existing pinned validation venv and active chained pre-commit/commit-msg hooks | `git commit -m 'ci: route PR checks through affected purpose validation'` invokes `python3 scripts/qa.py staged`, Commitizen and generated-message checks | 0 | PASS | Exact-index QA and both message hooks PASS; focused negative tests and independent correctness/security review recorded above; no hook bypass | false | none |
| EVD-016 | [VAL-RESIDUE-001](../spec.md#criteria) | WORK-001 | observation | P01 W06-H03 follow-up; PR 331 head `e9f72ced`, test merge `43d84095`, CI run 44581637168, integrated merge `60ff97bd` | GitHub ubuntu-latest, pinned Actions and dependency lock, read-only candidate; GitHub jobs/logs API and local Git tree comparison | `python3 -I scripts/run-validation-lane.py --root . --lane affected --plan-file "$RUNNER_TEMP/pr-plan.json" --combine-documents`; `gh run view 44581637168 --job 135763534198 --log`; `git diff --exit-code e9f72ced7297e86c287b9634958ea838ac01bec7 HEAD` after integration | 0 | PASS | Both required checks and all 25 selected purpose leaves PASS; integrated tree identical; hosted scope/times above. Closes the W06-H03 implementation/hosted-coverage residue, not P01 user acceptance, W06-H02 or live/CRD guarantees | false | none |

### Resolution Links

No required earlier failure is open; EVD-011 resolves the environment failure
EVD-010. The earlier EVD-006 remains a non-required historical negative test.
The Resolves column names the row each PASS row closes.

### Residue Handoff

| ID | Residue | State | Owner | Resume condition | Closure |
| --- | --- | --- | --- | --- | --- |
| AGENT-04 | Legacy row `AGENT-04` of `Requirement Changes`: direct, wrapper and nested hook delivery | open | W07 | When a trusted Claude and Codex session can observe nested, resume and compact hook delivery (RUNTIME-CLOSE) | none |
| DOC-12 | Legacy row `DOC-12` of `Conflicts`: display renumbering of Stage 01, 02 and 03; also an OPEN row of Requirement Changes | open | Q07 | After W11 and every applicable docs task, in the separate Q07 task | none |
| Q07-H01 | No legacy row: before the final cutover rewrites history and renumbers documents, no check, test or generator may depend on a past SHA, Task, reserved number or old registry generation (SPEC-0219 audit, W11-ACCEPT, SPEC-0161 EVD-227). Read on `91ba3a10` (EVD-008); SPEC-0225 converted the code: only the current registry MAJOR is read, tests find requirement documents by route, reserved codes reset only with a raised `policy_rule_ids.baseline`, and the ADR retained form is selected by the `retained_form` marker. Left for the cutover as data, by the user's choice of 2026-11-19: the Archived Lineage identity reservations and the `git show <sha>:` citations of current documents, removed with the rewrite; the `identity_bound` of the RES-0001 and AUD-0001 reference retained forms, whose published members cannot take a marker; and the dormant `work_residue.historical_tables` key | open | Q07 | In the Q07-CUTOVER task, after W11 | none |
| R147-17 | Legacy row `R147-17` of `Requirement Changes`: harness static versus live provider evidence | open | W07 | At the next provider note edit or at RUNTIME-CLOSE | none |
| SPEC-0205-STALE-TEXT | No legacy row: three texts left stale by the H2-list removal of SPEC-0205 and outside its Spec scope: the Plan sentence "a draft until its review and approval receipts exist", the word `sections` in `docs/99.templates/AGENTS.md`, and the TemplateDefinition `validation` strings of `docs/99.templates/registry.json` that say "keep heading lists". Transferred from the closed SPEC-0205 Task (EVD-111) | open | W04+ platform | When the owner of the Plan text, of the Stage 99 `AGENTS.md` and of the registry TemplateDefinition text next edits them in its own package | none |
| SPEC-0211-REGISTRY-TEXT | No legacy row: wording faults found by the W03-H34 read of `docs/99.templates/registry.json` at `d0ae8cf6` (SPEC-0211 Task EVD-019), beyond `SPEC-0205-STALE-TEXT`: four "keep empty heading lists" pack strings, one "listed their H2 headings" and the provider-native twin "H2 lists" strings; copied or wrong TemplateDefinition and profile text (the data-pack consumer path names the collection README, the collection and runtime-governance template texts copy the stage and implementation texts, the postmortem extension removal names incident lineage, two `review` strings do not name their form, the governance-document form calls itself a provider note); one failure named by both `BODY-HEADING-REQUIRED` and `BODY-H3-REQUIRED`; "A audit" and "a operations policy"; about 28 Korean object particles (`을` for `를`) in generated `required_content`. Recorded under SPEC-0211 (user answer "Residue to owners, close H34 (Recommended)", 2026-11-15) | open | W04+ platform | When the owner of those registry TemplateDefinition, form and profile texts next edits them in its own package | none |
| T99-H03 | Disposal of the 13 published predecessors and their two identity-bound retained forms; accepted ADR-0026 and ADR-0028 still link to RES-0001-m0007 | open | Q07 | At Q07-CUTOVER, after every work package's acceptance | none |
| W04-H02 | Core Steps cells that the runbooks do not state: Expected Result in RUN-0001 steps 1, 2 and 5, RUN-0002 steps 1 to 4, RUN-0008 steps 1 and 3 and RUN-0009 step 4; On Failure in RUN-0010 steps 3 and 5 and RUN-0011 steps 2 to 4 | open | platform | When the runbook owner observes or states each result and failure action | none |
| W04-H03 | Interface Failure cells with no stated failure boundary: AD-0004, AD-0005, AD-0007 and the gitops README; the gitops README OpenBao, Prometheus and Grafana consumer | open | platform | When the architecture owner states each interface's failure boundary | none |
| W04-H04 | Reference core cells with no stated fact: Version, Application or Limits in the source tables of research m0013 to m0026 and pack 0002 m0001; Requirement in audit findings F-01 to F-09 and F-06 Acceptance | open | platform | When the reference maintainer re-observes the sources under RUN-0011 or states the requirement | none |
| W04-H05 | Policy rules whose Enforcement names only a runbook: POL-0004 ROLLOUT-R001, R002, R005, R006, R007, R013, R014, R015, R020 to R024; POL-0007 ONBOARD-R013 | open | platform | When each rule gains a check or is reclassified as semantic review | none |
| W04-H06 | No runbook names a distinct escalation contact; RUN-0012 Next Owner reads none; RUN-0009 and RUN-0010 break-glass steps name no approver beyond human approval | open | platform | When the Stage 05 owner names the escalation contact and approver | none |
| W04-H07 | Mechanism text in approved REQ-0002: AC05 declarations and rationale belong to AD-0005. The REQ-0003 FR-0017 part moved to AD-0006 on 2026-11-18 (EVD-188) | open | platform | When the Requirement owner revises REQ-0002 with approval | none |
| W06-H02 | No legacy row: a hosted `style-pr` run in which the CI lock leaf, or the GitOps identity leaf over a changed GitOps manifest, is selected and executes. ADR-0063 was accepted on 2026-11-18; the GitOps leaf has run only on documentation changes under `gitops/` (EVD-211) | open | W06 | At the first pull request that changes a GitOps manifest or the CI lock | none |
| W06-H03 | No legacy row: the 2026-11-12 target of hosted PR-time affected implementation and product checks beyond style, CI lock and GitOps identity (QUAL-R006). P01 implements the selected purpose profile and PR 331 observed its execution; user acceptance and live guarantees remain separate | terminal | W06 | After the P01 pull request records the selected affected purpose checks on its exact candidate and run, reconcile the remaining acceptance or observation conditions | EVD-016 |
| W07-H03 | No legacy row: W01-B, rejection tests (an approval is not a Git object, status, checkbox, successful QA or reviewer verdict; no check grants integration; no approval is inferred from a role name or hash). Frozen SPEC-0166 Requirement Trace, W01-B row; its Handoffs table does not list it. Recover the frozen Task as for W05-H04. Seeded under W03-D81 by SPEC-0213 | open | W07 | At the next approval or receipt validator change, or at W11-ACCEPT | none |
| W07-H05 | No legacy row: the Windows Desktop over SSH read-only reviewer ran its shell with workspace write (EVD-163 FAIL); the client sent a null request profile (EVD-167 FAIL). Recorded under RUNTIME-CLOSE on 2026-11-18 | open | W07 | When the Desktop host owner supplies the outgoing turn permission fields or a client fix, rerun the read-only reviewer write denial on that path | none |
| W08-H01 | No legacy row: the memory store takes `owner` and `approval_ref` as caller-supplied strings, and any process of the same local account can open the SQLite file directly, so the store authenticates neither. D06 asks for an OS or broker boundary before an untrusted writer uses it. Recorded under W08-MEMORY on 2026-11-18 | open | W08 | When a second local account, an untrusted writer or a remote host must use the store | none |
| W08-H02 | No legacy row: memory `search` normalizes case and whitespace only, so a query with a Korean particle or inflection the memory lacks (for example `저장소를` against `저장소`) does not match, and context tokens per result are not measured. Recorded under W08-RETRIEVAL on 2026-11-18 | open | W08 | When a real memory query misses because of a particle or inflection, or when current memories exceed 1,000 or live search p95 exceeds 100 ms | none |
| W08-H03 | No legacy row: session capture delivery not yet observed. Codex 0.169.0 runs the new lifecycle entries only after the user trusts them in `/hooks` (EVD-201), and Claude `PreCompact` did not occur in EVD-200. Recorded under W08-CAPTURE on 2026-11-18 | open | W08 | When the user has reviewed the Codex hooks in `/hooks`, observe a Codex session and a Claude compaction in `session_capture.py status` | none |
| W08-H04 | No legacy row: the catch-up of `hy-home-k8s-session-analysis.timer` after real downtime is not yet observed (EVD-204). Its first scheduled run over a captured day was observed on 2026-11-19 at 03:00 KST (EVD-222). Recorded under W08-ANALYSIS on 2026-11-18, narrowed under W10-OBSERVE on 2026-11-19 | open | W08 | After the host has been off across a 03:00 KST run, read `session_analysis.py status` and the journal for the catch-up run | none |
| W08-H05 | No legacy row: capture keeps a failed tool result's flag but not its call ID, so the analysis counts failures per day only. On 2026-11-18 one count mixed hook refusals, deliberate test failures, permission denials and tool errors, which have different owners (EVD-222). Recording the call ID, an identifier allowed by CTX-R022, would attribute failures to tools. Recorded under W10-OBSERVE on 2026-11-19 | open | W08 | At the next capture schema change, or when a failure candidate cannot be acted on | none |
| W09-H02 | No legacy row: the product network policies allow egress to 192.168.0.13 from `apps`, `platform`, `monitoring` and other namespaces, and NetworkPolicies only add allowances, so a test workload with pods in those namespaces could reach the production LAN. Blocking it for a whole test cluster needs a host firewall rule on its Docker network or a dedicated VM, which need root (EVD-208). The approved closure runs no product pod. Recorded under W09-ENV on 2026-11-18 | open | W09 | Before a test cluster runs product pods in a namespace whose policy allows 192.168.0.13, or when the user provides a host firewall rule or a dedicated VM | none |
| W09-H03 | No legacy row: the user-approved temporary material under `_workspace/`, `.workspace-test/` and `.qa-evidence/handoff/` is not yet deleted, because the agent's `rm` was denied | terminal | operator | When the user runs the handed-over deletion of the approved ignored paths (EVD-226) | EVD-002 |
| W10-H01 | No legacy row: a Codex session creating, starting, finishing and scoring a record in the same `.workspace-memory/forecast.sqlite3` that Claude used; the CLI is provider-neutral source, but no Codex run was made (EVD-214) | open | W10 | At the next authorized Codex session in this workspace | none |
| W10-H02 | No legacy row: real provider workers (`claude -p` or `codex exec`) dispatched by `scripts/work_parallel.py`. The user chose shell workers on 2026-11-19 to spend no model usage, so provider delegation through the dispatcher is unobserved (EVD-216) | open | W10 | When the user authorizes model usage for provider workers | none |
| W10-H03 | No legacy row: a worker runs with the caller's own permissions. A process that calls `setsid` leaves the killed group, a worker can write outside its clone, total disk use has no quota, and a worker started in the moment before the dispatcher saves its state is not in `state.json` (EVD-215). OS containment, such as a cgroup or a dedicated sandbox, would close these | open | W10 | Before an untrusted or provider worker is dispatched | none |
| W10-H04 | No legacy row: the first recheck of the accepted failure candidate 1, reviewed on 2026-11-19 KST, is the run at 03:00 KST on 2026-11-21 over 2026-11-20, so whether it reports `met`, `recurred` or `inconclusive` is not yet observed. Days analyzed before the change are not backfilled, which can only leave the candidate `unverified` (EVD-221, EVD-222) | open | W10 | After the 2026-11-21 03:00 KST run, read `session_analysis.py candidates` for candidate 1 | none |

## Acceptance Decision

### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [VAL-RESIDUE-001](../spec.md#criteria) | accept | accepted | EVD-001, EVD-002 | User answer 'Accept all (Recommended)' of 2026-11-19 in this session | user | platform | none |
| [VAL-RESIDUE-002](../spec.md#criteria) | accept | accepted | EVD-005 | User answer 'Accept all (Recommended)' of 2026-11-19 in this session | user | platform | none |
| [VAL-RESIDUE-003](../spec.md#criteria) | accept | accepted | EVD-007 | User answer 'Accept all (Recommended)' of 2026-11-19 in this session | user | platform | none |

### Remaining Conditions

The user accepted every criterion on 2026-11-19. This package stays as the live residue host until Q07; each open residue row names its owner.

## Handoff

### Promotion Receipt

The Plan promotes no durable contract.

### Next Owner

P01 implementation, selected QA and hosted verification are delivered in
PR 331; EVD-015 and EVD-016 record the actual results. Its receipt-only
follow-up is checked by the selected document consumers. P01 user acceptance
is pending. The next input is P02-LOCAL-FEEDBACK after this delivery record,
using P00 reconciliation and the P01 selected-CI result; do not start it automatically.
The P00 handoff below is retained predecessor context.

WORK-001 to WORK-003 remain completed and accepted; do not rerun them.
For P00, the source and residue classification is implemented, with final
selected repository-static QA (EVD-014) and independent semantic review
recorded above. The final receipt-only append is checked separately for
document profile and links, without replaying unchanged behavior suites.
No new P00 user acceptance is recorded. The next input is
`_workspace/workspace_governance_remediation_1_0_0_20261119/prompts/P01-CI-ROUTING.md`;
the CI owner starts the affected-check routing work and the other residue
owners follow the P00 allocation and their original resume conditions.

No one-use script, fixture or `_workspace/` output was created. Inline
checks left no script to delete; QA owns and cleans its private temporary
snapshots. Its reusable local evidence cache is distinct from task scratch.
Keep this input package through P17 and leave the older package, other active
work, `.workspace-memory/` and sessions untouched. Hosted execution, native
hook delivery, Desktop/SSH denial, cluster-wide LAN isolation and the dated
candidate recheck are not newly observed here. The known defects require
repair at their named successor, not an observation-only waiver.
