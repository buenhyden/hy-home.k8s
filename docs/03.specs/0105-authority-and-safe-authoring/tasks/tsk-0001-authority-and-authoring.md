---
title: "Authority and Safe Authoring Execution"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
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
| WORK-002 | VAL-P01-002, VAL-P01-003, VAL-P01-004, VAL-P01-005 | Repair authorized owners and consumers | platform | In progress | Owner and consumer repairs under final review | Changed-path disposition below |
| WORK-003 | VAL-P01-006 | Validate, review and commit | platform | In progress | Focused tests and intake commit observed; final gates pending | Verification Summary |

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
- Final affected quick, implementation exact-index staged and local full:
  pending. No previous input result is claimed for changed base/index/bytes.

### Review and delivery

Actual independent read-only reviewer `/root/approval_trace` inspected approval
sources, structural callers, policy/template and Task evidence; `/root/guard_trace`
inspected guard/evaluator semantics and changed consumer guidance.
`/root/secret_boundary_review` independently found the raw-output marker defect
and reviewed the repaired security boundary; no unresolved HIGH/CRITICAL issue
was reported. Final evaluator refinement passed scoped security review; Task
acceptance and final gates remain pending. Authors `/root/doc_guard_fix` and `/root/eval_fix` owned disjoint checker
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
| [WORK-002](../plan.md#work-breakdown) | In progress | Scoped repairs, regressions and independent review |
| [WORK-003](../plan.md#work-breakdown) | In progress | Actual commands above; final gates pending |
