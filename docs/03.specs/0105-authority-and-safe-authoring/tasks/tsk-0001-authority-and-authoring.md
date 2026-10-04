---
title: "Authority and Safe Authoring Execution"
version: "1.1.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0001"
---

# Task: Authority and Safe Authoring

## Overview

One execution stream owns P01 observations, changes, command outcomes and
handoff. The current request approves this bounded implementation; automation
and independent review supply evidence rather than authorization.

## Inputs

- [Spec](../spec.md) and [Plan](../plan.md).
- User's P01 request: authorized reversible local policy/configuration/docs,
  necessary non-secret management records, subagents and logical commits.
- Source basis: clean `main`, HEAD `f6501e46a0d35858c598c207e726a0e89c92d7d7`;
  direct current sources replace unavailable K03/K06/K11 register details.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-P01-001 | Trace source and actual consumers | platform | Completed | Direct baseline and independent traces reconciled | Source and consumer comparison below |
| WORK-002 | VAL-P01-002, VAL-P01-003, VAL-P01-004, VAL-P01-005 | Repair authorized owners and consumers | platform | Completed | Repairs and scoped independent review accepted | Changed-path disposition below |
| WORK-003 | VAL-P01-006 | Validate, review and commit | platform | Completed | Implementation commit, exact-index and full QA observed | Verification Summary |

## Approval and Safety Boundaries

- **Allowed Paths**: P01 common governance and affected skills/provider notes;
  existing approval/guard/evaluation implementations and tests; this package
  and its Stage 03 navigation.
- **Forbidden Paths**: secret values, authentication, user memory and settings,
  plugin source, unrelated changes, frozen historical bodies.
- **Approval Required**: remote push/PR/merge/publication, live actions, destructive
  cleanup and native configuration changes have no approval. Local logical
  commits and reversible scoped authoring are authorized by the current request.
- **Static Validation**: focused tests, affected quick, exact-index staged,
  actual Commitizen message validation, and one local full; outcomes below.
- **Live Validation**: DEFER; no live operation is authorized.
- **Secret / Vault Handling**: no read, print or actual secret access.
- **Rollback Plan**: preserve baseline and scope; forward revert only these
  logical commits under the repository Git policy, with no history reset.
- **Evidence Location**: this Task; no parallel progress ledger.

## Verification Summary

### Snapshot and preflight

Worktree: the primary checkout of `hy-home.k8s` observed through Git; execution branch
`codex/p01-authority-safety`, base `main` at the observed HEAD above.
`rtk git status --short` and cached stat reported no changes before work;
`rtk git branch --show-current` and `rtk git rev-parse HEAD` observed the base.
`rtk git switch -c codex/p01-authority-safety` created the local branch.
No reset, remote or live command ran.

Default shell execution repeatedly failed before command startup with
`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Bounded native
approval escalation successfully ran read-only Git/source queries and branch
creation. Sandbox/trust settings were not changed. RTK 0.49.0 and Python 3.12.3
were observed; pre-commit resolves to the account-local `~/.local/bin/pre-commit`.
Effective `core.hooksPath` is `scripts/githooks` from local `.git/config`;
existing hook chain is preserved. The workspace `.git/hooks/commit-msg` is absent;
the actual intake message in `.git/COMMIT_EDITMSG` passed pinned Commitizen
explicitly. This is message evidence, not hook-installation evidence.

The QA runner owns its per-child envelope: 1,200 seconds, 4 MiB stdout,
1 MiB stderr and 2 seconds cleanup grace at this input. Preflight used the
existing tools and cached pinned pre-commit environments. Required Kustomize
was missing from the trusted system PATH. The current operator explicitly
approved SHA-256-verified CI-pinned 5.8.1 installation, then performed the
password-required system install. Public release archive SHA-256 was
`029a7f0f4e1932c52a0476cf02a0fd855c0bb85694b82c338fc648dcb53a819d`;
installed and extracted binary digests matched
`f7b1605aa5143e0dcbd754a4d43c47ad7a560c540b1356b064d69fe236164494`.
Observed version was `v5.8.1`, root-owned mode 0755. No temporary PATH override
was used. Conftest uses the existing local read-only/no-network Docker fallback,
pinned to `v0.69.0@sha256:a38ba21668929a00dce2fe6ee43d1312228340bce5fd243f47dd0ce90516e558`.
No system or provider configuration was weakened.

Installation approval binding: approving actor is the requesting user in this
trusted conversation (no separate external identity was supplied); the assistant
verified the public release and the same user reported executing the system
install. Operation/subject was a single root-owned mode-0755 install of the
verified Kustomize binary to `/usr/local/bin/kustomize`, not ongoing system
administration. Reviewed input was CI-pinned 5.8.1 at the baseline revision
above plus the archive digest. Original non-secret references are question
`call_OUoocXHeDxniSJ7xPJDNqvLc`, whose answer approved installation after
pinned-version verification, and execution handoff
`call_v8o5rhM1iLp7Qel8vIsg5AD7`, whose answer reported installation complete.
These English descriptions summarize the original conversation answers. Validity
was this required local QA setup; the latest supplied conversation contains
no withdrawal or changed target. This is observation of the current user
instruction, not independent identity authentication or a revocation-service
PASS. The initial noninteractive sudo attempt failed because a password was
required; the later installed-file/version/digest observations verify the
result, not who typed the password. No password or credential was read.

An attempted temporary commit-message write through `apply_patch` was rejected
by the observed `HOOK-PATH-ROOT` guard. No alternate writer retried that rejected
path. Normal Git message handling and the existing explicit Commitizen route
were used. Native escalations addressed the shell startup failure; they do not
prove OS enforcement or hook delivery for another role/provider.

A progress query `ps -eo pid,ppid,etime,args` was overbroad and returned
unrelated host process arguments. It is not approval or QA evidence; its raw
output is not copied here. Further progress checks use the owned QA session
output only. No environment dump or credential file was read.

### Source and consumer comparison

Original source revision for this table is
`f6501e46a0d35858c598c207e726a0e89c92d7d7`; paths name real observed owners and
callers, not proposed filenames. K03/K06/K11 register contents were unavailable,
so their asserted facts were reverified directly. Current links below identify
the repaired consumer; Git preserves the original lines.

Original approval anchors: approval-and-safety lines 19–21, 31–38, 74–76;
context-and-memory 89–101; work-lifecycle 49–54; quality 164–184;
`.agents/prompts/handoff.md` 42–47; Task template 30–39;
`scripts/validation/repository/quality.py` 2251–2266;
`scripts/archive_dispositions.py` 755–760;
`scripts/validate-document-lifecycle.py` 2554–2605;
`.agents/roles/code-reviewer.md` 39–57. These original locations separate
operator facts, structural checks and read-only responsibilities.

| Same action / completion condition | Original rule and actual consumer | Current owner and disposition |
| --- | --- | --- |
| Write an approved operating document or synthetic command example | `.agents/governance/approval-and-safety.md` allowed scoped authoring, but `.agents/evaluations/run-agent-evaluations.py` `EXTERNAL` graded dangerous command words as action claims; `grade()` consumes it | Approval and safety owns permission; evaluator now checks affirmative first-person execution claims. Warning, instruction and fake quoted example controls pass; strong quoted execution claims fail. Evaluator is a heuristic, not authorization. |
| Cite a prohibited command in visible prose | `scripts/validation/repository/quality.py` command loops rejected inert quoted prohibitions and separately checked direct main push; actual repository-quality gate executes both loops | Same quality consumer accepts only same-line `prohibited-example:` / `do-not-run:` followed by a matching single-backtick quote in visible Markdown prose. No shell/fence/comment or unquoted duplicate exception. Safety owns permission; marker syntax grants no execution authority. |
| Display actual Secret YAML/JSON | Original quality regex allowed a raw-output line with nearby `redacted` / `metadata-only`; `docs/05.operations/README.md` copied that exception. Claude native declarations deny Secret reads | Safety owns Secret access. Both quality loops reject runnable raw YAML/JSON output, including spaced/equals long options, regardless of adjacent redaction words. Operations copy now describes safe metadata and the canonical boundary. Native denies stay unchanged. |
| Repair a conflicting policy on explicit request | Agent execution's stop guidance could consume the very local rule being repaired as a permanent veto | `.agents/governance/agent-execution.md` owns precedence/conflict routing; latest scoped intent updates the owner and affected consumers together. Actual native restrictions and role limits still apply. |
| Authenticate approval actor, operation, subject and revision | Task template and `quality.py` validate field structure; archive/disposition and lifecycle callers check records and Git objects. No caller authenticates an approving actor | `.agents/governance/approval-and-safety.md` operator route binds actual approving actor/executor, operation, subject, reviewed revision, original trusted source and validity/revocation. Task template points there. Missing, mismatched, expired, revoked or unavailable authority stops the dependent action; no fake approval generator or authentication PASS was added. |
| Use historical approval or recovery evidence | `.agents/governance/context-and-memory.md` already isolates historical approvals; archive consumers verify object identity, type, path and digest. REQ-0003 Overview still introduced archived SPEC-0072 as the current contract | Current `.agents` owners and registry are authoritative. REQ-0003 now labels SPEC-0072 historical. Frozen archive objects, registry and recovery validators are preserved; historical evidence grants no current authority. |
| Reviewer reports a needed document repair | Registry read-only classes and required risk-report procedure permit evidence/review, not edits. Quality requires independent review, not recurring human authorization | Registry remains role owner; approved writer and Task own repairs. Approval and safety reuses valid scoped approval; quality's independent verdict supplies quality evidence. No reviewer class, tool set or sandbox changed. |
| Required QA exceeds tools, time or output budget | Quality runner envelope and work-lifecycle stop taxonomy were described together with protected actions | Quality owns resource preflight; runner owns executable limits. Lifecycle routes there. Budget approval never authorizes Secret/live action; safety denial never becomes a budget waiver. No wrapper, command variant, false SKIP or disabled gate used. |

Application path: common governance → `.agents/roles/registry.json` permission
class / required skills → explicitly read role and skill → provider projection
→ registered hook adapter → shared `scripts/provider_write_guard.py`
→ actual tool/executable. `.codex/provider.md`, `.codex/CODEX.md`,
`.codex/hooks.json`, `.codex/hooks/pre-tool-use.sh`, `.claude/settings.json`
and `.claude/hooks/pre-tool-use.sh` were inspected. Structured edits are the
shared guard's input; shell observations are advisory, not a complete shell
parser. No shell text or command example is itself a tool invocation.

Codex registry read-only classes bind OS `read-only`; Claude classes retain
Bash with instruction/native-pattern limits. These differ materially. Static
projection validation proves declaration consistency only. No provider runtime
probe, sandbox reduction or formal enforcement parity is claimed. The script
README's obsolete blanket hook-enforcement wording now points to this boundary.

Existing negative historical checks remain owned by archive/lifecycle tests:
missing/ambiguous objects and wrong path (`test_archive_recovery.py`), wrong
source object (`test_archive_disposition_lifecycle.py`), digest/payload mutation
(`test_archive_validation.py`) and cutover malformed/missing/wrong-base evidence
(`test_document_lifecycle_archive_cutover.py`). They validate recovery integrity,
not approval identity. No test freezes deleted filenames or historical counts.

### Changed-path disposition

| Files | Disposition and preserved owner |
| --- | --- |
| This `spec.md`, `plan.md`, and Task | Added actual P01 contract, order and sole execution record; initial states committed before canonical transitions |
| `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md` | Updated active navigation and reciprocal requirement link; historical basis no longer presented as current authority |
| `.agents/governance/approval-and-safety.md` | Supplemented existing permission owner with authoring/execution distinction, operator route and scoped policy repair |
| `.agents/governance/agent-execution.md` | Clarified existing conflict owner and independent safe progress |
| `.agents/governance/quality.md`, `.agents/workflows/work-lifecycle.md` | Separated resource preflight from protected authorization and linked the existing owner |
| `docs/99.templates/templates/specs/task.template.md` | Existing approval field routes to operator source verification; shape does not authenticate |
| `scripts/validation/repository/quality.py`, `tests/test_repository_quality_rules.py` | Repaired shared command decisions and minimal behavior regressions at existing AST test seam |
| `.agents/evaluations/run-agent-evaluations.py`, `tests/test_agent_evaluations.py`, `.agents/evaluations/README.md` | Repaired action-claim heuristic and its documented scope; retained existing synthetic corpus |
| `docs/05.operations/README.md`, `scripts/README.md` | Removed misleading redaction/enforcement copies and routed current consumers to owners |

No tracked file was removed. No archive unit was reopened, moved, deleted or
formatted. Registry, role permissions, provider projections, hook registration,
native deny patterns and executable runner limits are unchanged.

### Actual checks and input boundaries

- Intake exact-index staged over five document paths: six gates PASS after
  an earlier FAIL found missing reciprocal link, multiple criterion IDs per
  trace cell and checkout-specific prose. Those authoring defects were fixed.
  Agent governance, document registry, lifecycle, links, profiles and repository
  quality passed on the repaired intake index.
- Intake logical commit: `6041e00` (`docs(governance): define P01 authority and
  authoring work unit`). Actual message subsequently passed
  `pre-commit run commitizen --hook-stage commit-msg --commit-msg-filename .git/COMMIT_EDITMSG`.
  This does not claim a workspace commit-msg hook ran.
- Evaluator baseline RED: five benign mention cases falsely failed. Focused
  grading and then 25 evaluator tests / 19 synthetic cases passed after repair.
  Review exposed quoted, adverb and `invoked` / `used` claim misses; genuine
  failing regressions preceded their corrections. Quoted fake `used` example
  produced one additional RED failure; narrowing `used` to unquoted CLI tokens
  passed grading 9/9, evaluator module 25/25 and corpus 19/19 (12 declared
  negative cases). Strong execution verbs retain quoted-command detection.
  Final evaluator bytes passed pinned Ruff lint/format without mutation.
- Scanner baseline RED proved a runnable raw Secret command with adjacent
  `redacted metadata-only` passed the old decision. Further long-output RED
  cases preceded the repaired GREEN. Safe metadata type and inert prohibitions
  pass; raw output, runnable push, fence/comment and outside-quote controls fail.
- `python3 -m unittest tests.test_repository_quality_rules tests.test_current_executable_references tests.test_agent_evaluations -q`:
  42 tests PASS on the reviewed implementation before the final evaluator
  refinement. Expected negative-fixture diagnostics inside the suite are not
  repository failures.
- Pinned Ruff formatting changed two files on first run: formatter FAIL with
  mutation, followed by scoped Ruff lint PASS. Optional Black invocation failed
  because it is absent; Black is not the repository formatter and was not
  installed. Final changed bytes require their scoped checks.
- `python3 scripts/qa.py quick`: 14 selected gates PASS over the 15-path
  working-tree implementation snapshot. Later Task evidence corrections are
  covered separately by the exact-index result below.
- First implementation `python3 scripts/qa.py staged`: 13 gates PASS and
  markdown-profiles FAIL because two verbatim Korean answers violated the
  Task's English-first profile. The answers were summarized in English with
  original reference IDs preserved; no validator or policy was weakened.
- Repaired implementation `python3 scripts/qa.py staged`: all 14 selected
  gates PASS over the final 15-path index. Pinned Commitizen PASS over the
  actual `.git/COMMIT_EDITMSG`; normal `git commit -F .git/COMMIT_EDITMSG`
  produced `cff8712c5e9aaa06f082e57b2d90e53bd260c7cc`. Validated index and
  committed tree both equal `0c18c463bb1c1892dfff2570e82fce3dd9f27615`.
- `python3 scripts/qa.py full`: exit 0, all 24 required gates PASS over the
  clean working-tree implementation at that commit, 1,294 source paths and
  baseline `f6501e46a0d35858c598c207e726a0e89c92d7d7`. Full ran once; unit
  discovery and pinned manual all-files pre-commit each ran once in that mode.
  Unit stdout/stderr SHA-256:
  `963625a972a510be2c8bc6c17e938fb0ffd71ff0058d1badb921e34506f18357` /
  `c4d958d6bd5eba0bd75bac2dd2bc4b1ed750c4913dc70b8570bd390ee90ae18d`.
  Pre-commit stdout SHA-256:
  `ed873238f5f28f072a6c188ccf9690cf67d65abe1554872445869f431282d5ae`.
  All reported required children completed with rc 0, complete output and
  cleanup. No formatter changed the checked snapshot.
- Platform depth limits remain explicit: live-observation DEFER to operator;
  external CRD schema-policy DEFER for unavailable schemas; syntax rows DEFER
  to their separately passing required gate; sample-app product-semantic SKIP
  as not applicable. Full PASS does not claim those deferred depths passed.
- Subsequent changes are package lifecycle metadata and this evidence record
  only. They receive fresh document/index validation at the closing commit
  boundary. The full result belongs to the implementation commit above, not
  the later document bytes. No implementation regression or full result is
  reused as proof for changed inputs; no self-SHA write loop is required.
  The preliminary closing-index run was interrupted (exit 130) to correct a
  list-continuation indentation and clarify this completion boundary; it is
  not PASS evidence. Closing Commitizen passed the actual candidate message.
  This terminal candidate is committed only after fresh exact-index document
  gates pass. Its own closing gate/commit result is recorded in the command
  transcript and final handoff, rather than self-cited inside a moving input.

### Review and delivery

Actual independent read-only reviewer `/root/approval_trace` inspected approval
sources, structural callers, policy/template and Task evidence; `/root/guard_trace`
inspected guard/evaluator semantics and changed consumer guidance.
`/root/secret_boundary_review` independently found the raw-output marker defect
and reviewed the repaired security boundary; no unresolved HIGH/CRITICAL issue
was reported. Final evaluator refinement passed scoped guard and security
review. Approval/Task evidence corrections passed scoped read-only review.
Authors `/root/doc_guard_fix` and `/root/eval_fix` owned disjoint checker
and evaluator files, respectively; neither supplies independent certification
of its own changes. Review is not authorization.

Installed Superpowers 6.4.2 using-superpowers, brainstorming and
subagent-driven-development definitions were explicitly read; the sole selected
execution method is subagent-driven-development. Repository roles and required
skills were read explicitly. Current approved scope and Stage 03 ownership
replace external skill defaults for design reapproval, docs/plans, extra ledgers
and repeated full suites. No unverified skill-version claim or private global
memory/plugin modification is made.

Hosted CI, provider runtime hook delivery, remote/live and main integration:
DEFER, unobserved and unauthorized here. Primary PR and archive follow-up: none
created; no merge. Finished source stays intact until separately authorized
disposition. Rollback uses reviewed forward reverts of this branch's logical
commits; baseline/history and user configuration are preserved. The operator
owns any later system-tool disposition.

Primary integration target is `main`, one SPEC-0105 implementation PR when
remote delivery is authorized. No PR or archive follow-up exists. A later
strict-retention follow-up would reference this same Spec only after final
source integration and separate disposition approval; it starts no new
execution unit. This completed package stays intact in Stage 03.

### Acceptance reconciliation

| Criterion | Observed local acceptance |
| --- | --- |
| VAL-P01-001 | Original-revision rule/consumer comparison and existing owners above; copied redaction/enforcement/current-contract claims corrected |
| VAL-P01-002 | Benign authoring and affirmative execution regressions, raw-output RED/GREEN, final evaluation corpus and required static gates PASS |
| VAL-P01-003 | Operator-supplied binding and original-source observation reviewed; authentication is manual. Missing/mismatch/revocation grants no permission. Full unit discovery and archive-cutover integrity gate PASS; no fake authentication result |
| VAL-P01-004 | Read-only registry/projections unchanged and governance gate PASS; distinct read-only reviewer identities supplied scoped quality findings, authors made repairs |
| VAL-P01-005 | Quality/runner resources and safety authorization have distinct owners; actual required-tool approval/setup and unchanged envelope, no bypass or false SKIP |
| VAL-P01-006 | Intake and implementation commits, actual quick/index/message/full outcomes, independent review, delivery limits and forward-revert rollback recorded |

Final reviewed executable identities: evaluator
`ec6e595f928b693fae9a24fb852f8bdfeaf2696af27afb0d8ba8a8d085ee7add`,
repository quality
`b1ac164ed331940f1f4d79ae0e6297d8de749765e2ebc801587a8252f5fcde59`.
Current application anchors: role registry 70–93 / 213–216; reviewer role 31–62;
`.agents/skills/risk-report/SKILL.md` 7–8; Claude settings 12–26 / 76–85; Codex hook registration
4–13; shared guard 617–664 (shell advice 517–534); repository quality
1965–2003 / 2036–2043 / 2125–2144; evaluator 50–64 / 278–281; quality resource
owner 64–85; runner 1667–1682 / 1765–1829. Paths are the owners identified above.

Residual limits: approval source authentication is manual, not a repository
record result. The static command scanner does not cover every multiline form,
pre-resource flag, Secret `.data` jsonpath or custom output template. The
evaluator recognizes a bounded claim grammar; indirect/passive and ambiguous
language, including quoted `used` commands, requires human review. Neither substitutes for actual authorization
or native enforcement. Policy continues to forbid actual unauthorized access.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Completed | Source/consumer comparison and preserved owners |
| [WORK-002](../plan.md#work-breakdown) | Completed | Scoped repairs, regressions and independent review |
| [WORK-003](../plan.md#work-breakdown) | Completed | Implementation commit and actual mandatory local checks above |
