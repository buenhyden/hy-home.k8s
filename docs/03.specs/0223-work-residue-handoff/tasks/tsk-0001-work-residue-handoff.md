---
title: "Work Residue Handoff"
version: "0.4.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-19"
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

None is open.

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

### Resolution Links

No earlier failure is open; the Resolves column names the row each PASS row closes.

### Residue Handoff

| ID | Residue | State | Owner | Resume condition | Closure |
| --- | --- | --- | --- | --- | --- |
| AGENT-04 | Legacy row `AGENT-04` of `Requirement Changes`: direct, wrapper and nested hook delivery | open | W07 | When a trusted Claude and Codex session can observe nested, resume and compact hook delivery (RUNTIME-CLOSE) | none |
| DOC-12 | Legacy row `DOC-12` of `Conflicts`: display renumbering of Stage 01, 02 and 03; also an OPEN row of Requirement Changes | open | Q07 | After W11 and every applicable docs task, in the separate Q07 task | none |
| DOC-H01 | No legacy row: the DOC-PATH-PLAN path plan, adopted by the user on 2026-11-19 (SDD-PATHS), with its hand-edit consumers and preconditions; the category moves, the W owner moves of SDLC-H01, the renumbering and the Stage 98 disposal run once at the cutover after a full validator run on a copy (EVD-212) | open | Q07 | In the Q07-CUTOVER task, after every package is closed and Q07-H01 is converted | none |
| Q07-H01 | No legacy row: before the final cutover rewrites history and renumbers documents, convert or remove the checks that depend on history or numbering, found by the SPEC-0219 audit. These are the registry `work_residue.historical_tables` path to this Task; the retained ADR range (`FIRST_ADR_OUTSIDE_RETAINED_RANGE`, the registry ADR identity bound); `policy_rule_ids.reserved_codes` and the never-shrink check; the Archived Lineage identity reservations read by `document_lifecycle.py` and `document-generator.py`; `reachable_git_path_exists` in `scripts/validation/current_executable_references.py` with every `git show <sha>:` reference in current documents; the cumulative-history replay range; and the tests that read requirement files 0001 to 0004 by path; and the Task base-revision read with an older registry (`historical_major` in `scripts/document_contracts.py`), found by W11-ACCEPT (EVD-227) | open | Q07 | In the Q07-CUTOVER task, after W11 | none |
| R147-17 | Legacy row `R147-17` of `Requirement Changes`: harness static versus live provider evidence | open | W07 | At the next provider note edit or at RUNTIME-CLOSE | none |
| SDLC-H01 | No legacy row: the user adopted `docs/00.workspace/` as the physical owner of the W layer on 2026-11-18 and chose to move it once with the final path cutover. The move takes the W rows of the SDLC-R036 table and splits approval and safety along its rule lists, updating routers, validators, registry routes and links in one change (EVD-209) | open | Q07 | In the Q07-CUTOVER task, together with the SDD-PATHS renumbering | none |
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
| W06-H03 | No legacy row: the 2026-11-12 target of hosted PR-time affected implementation and product checks beyond style, CI lock and GitOps identity (QUAL-R006) | open | W06 | When a successor decision selects the next hosted affected leaf | none |
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

platform runs WORK-002 and WORK-003; the residue owners act at their resume conditions.
