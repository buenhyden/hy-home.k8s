---
title: "Hosted QA Cleanup"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0015"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Hosted QA Cleanup

## Overview

Execute the explicitly requested hosted QA removal with honest remaining CI
results and fail-closed provenance. This follows completed local integration;
it does not discard passing regressions or earlier evidence.

## Inputs

- [VAL-P02-015](../spec.md#success-criteria--verification-plan) and
  [WORK-015](../plan.md#work-breakdown).
- Latest user instruction: remove failing GitHub Actions tests/QA stages,
  integrate locally independently of remote results, and reflect origin/main.
- Accepted local main `3ff0ab627f887d7d75aa545560a051477731d285`.
- CI/quality/governance owners' read-only bounded consumer plans; source writes
  were held until the observed ready endpoint. At early C3 intake, disjoint
  source writes were released and functional RED/GREEN remained NOT_RUN until
  observed; EVD-P02-156 and EVD-P02-158 now record those actual outcomes.
- Latest finish permission covers only the four named development refs and
  three development worktrees after verified local/origin integration and
  structured-evidence preservation; no cleanup has executed.
- Later actual-duration criterion also removes jobs with an observed duration
  of at least ten minutes (600 seconds).
  Root's public metadata records PR135 run `37412890658`, job `112105040334`,
  qa step13 from 04:16:22 to 04:41:30, 25m08s at old head `179a88c9`.
  This is the historical failing QA job already targeted for removal; configured
  timeout values are not duration proof. Other jobs need actual observations,
  not invented timings or an additional broad workflow rewrite.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-015 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | Retire hosted full-QA execution and update direct consumers | platform | frontmatter | PASS | accepted | EVD-P02-157, EVD-P02-158, EVD-P02-161; observed local implementation only |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-150 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Scope and registered-form creation preflight | Local accepted main 3ff0ab62; original registered Task form | PASS | Ignored C1 preflight26741069 and commit4c1eab5e | accepted |
| EVD-P02-151 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Observed C1 actual-index/message checks and permitted independent review | Draft indexfea596b6 committed4c1eab5e; unchanged initial source inputs | PASS | External C1 final manifest108ae019 and ignored C1 postreceipt5a1d1ce4 | accepted |
| EVD-P02-152 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Historical failing hosted QA and actual duration input | Old PR135 head179a88c9, run37412890658/job112105040334/step13 | FAIL | Root public job metadata 04:16:22 to 04:41:30, 25m08s; historical only, not current source verdict | rejected |
| EVD-P02-153 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Observed ready-index/message checks and separate permitted review | Corrected index44f79bfe committed2f7f94f6; exact messagef27e757b | PASS | External C2 final manifest10c8edbf; ignored postreceipt85b2115f; six fresh gates, exact configured message, selection metadata only | accepted |
| EVD-P02-154 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Historical completed QA job duration input, distinct from step timings | Runs37412890658/37405907769/37419380702; jobs112105040334/112090899701/112125139531 | FAIL | Primary-root ignored p02-task15-hosted-job-duration.receipt.json bfd42c72: actual jobs1528s/1472s/901s; bounded recent sample, historical failures only | rejected |
| EVD-P02-155 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Package audit applicability and tool gap | Current unchanged Python lock; no Node consumer | NOT_RUN | External applicability receipt00c46e24: npm NOT_APPLICABLE, pip-audit executable/module absent DEFER; no audit execution, installation or network | pending |
| EVD-P02-156 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | New three-job baseline admission RED | Original direct consumer before repair | FAIL | External contract-red receipt1a534343: CI-TOPOLOGY required old five jobs, actual0.566s; expected RED preserved | rejected |
| EVD-P02-157 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Final owned Python scoped hooks | Current four Python files and exact eight declared hook inputs | PASS | External owned-hooks4 receipt5ebd3868: pinned three hooks completed, no formatter delta; eight-input scope only | accepted |
| EVD-P02-158 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Explicit direct consumer GREEN | Manifest e8273449, full fourteen inputs with PR72991f93, frozen index455a2c02 | PASS | External quality-focused receipt614085cc and proof3e62d326: actual79/79, total59.039s, max2.726s, each60s | accepted |
| EVD-P02-159 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Earlier formatter findings | Initial owned hook inputs before explicit writer correction | FAIL | Original owned-hooks receipt48ab149a and hooks3 receipt2701fc32 retained; initial secrets NOT_RUN, no final-input reuse | rejected |
| EVD-P02-160 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | First actual implementation-index canonical result | Index73b2fda0, actual thirteen selected gates | FAIL | Original staged receipt8aa74e7f and cause012b34e8: twelve PASS, repository-quality FAIL, actual243.528s; message and selection NOT_RUN | rejected |
| EVD-P02-161 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Observed corrected C3 actual-index/message checks, review and normal commit | Repaired indexfacfc6fd committedfe8ced85; unchanged implementation sources | PASS | External corrected final manifest97d14dee and ignored C3 postreceipt d8045ba5: thirteen fresh gates237.483s, exact message1.071s, selection metadata and separate permitted review | accepted |
| EVD-P02-162 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Original isolated prospective SPEC0106 completion | Same-base fe8ced85, sole Task candidate2a99f389, clone index67dd2d2b; parsed Spec trace omitted VAL015 | FAIL | Original receipt9fb61f82: rc1, 6.522s, COMPLETION-TRACE; full collector cleanup, no actual Task reflection or same-input retry | rejected |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec/Plan/Task; `scripts/README.md` current delivery
  guidance only; `.github/workflows/ci.yml`, `.github/workflows/qa-verifier.yml`,
  `.github/repository-surface.md`, `.github/rulesets/main-protection.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`; `scripts/validate-ci-python-contract.py`,
  `scripts/validation/repository/quality.py`, `tests/test_validate_ci_python_contract.py`,
  `tests/test_ci_qa_workflow.py`; `.agents/governance/quality.md` current delivery
  guidance and `.agents/workflows/work-lifecycle.md` Completion step 2 only.
- **Forbidden Paths**: Registry/schema/Archive, production regressions and proof
  implementation, old Task evidence, native/private/global configuration,
  hooks, limits, remote protection administration and all unrelated consumers.
- **Approval Required**: Latest explicit user scope authorizes these normal
  commits, local integration and origin/main reflection without remote-QA
  dependence. Remote writes belong to the separately assigned delivery owner;
  authentication and observed remote outcomes are not inferred. The later explicit
  cleanup grant applies only to refs `codex/p01-authority-evidence`,
  `codex/p02-task-summary`, `codex/reference-pack-fixtures`, `codex/p02-ci-cleanup`
  and worktrees `.worktrees/p01-authority-evidence`, `.worktrees/p02-task-summary`,
  `.worktrees/p02-ci-cleanup` after observed local/origin-main integration,
  main-reachable commits, clean state and known structured-evidence preservation
  with hash audit. Final cleanup results go in the ignored terminal attachment;
  no recursive unrelated/private deletion, reset or force is authorized.
- **Static Validation**: Actual registered-form creation metadata; bounded named
  RED/GREEN, scoped final-byte tools, each actual-index staged/message and
  separate review; prospective scoped completion then fresh actual closing
  checks. Full/affected/discovery execution remains NOT_RUN.
- **Live Validation**: DEFER; no cluster, runtime or native trust operation.
- **Secret / Vault Handling**: No secret reads; private raw direct audit remains
  NOT_OBSERVED/DEFER and is not granted by this CI instruction.
- **Rollback Plan**: Reviewed normal forward correction with reachable commit
  history and original evidence preserved. Owned branch/worktree cleanup is
  conditional on the explicit final integration and preservation checks.
- **Evidence Location**: This Task and exact structured check receipts; ignored
  proposal/closing attachments capture actual identities without self-SHA edits.

## Verification Summary

At initial draft intake, only scope was authored. The target hosted topology is branch-policy, qa-isolated and
ci-summary; the summary reports full QA NOT_RUN and never fabricates proof.
Provenance verification is explicitly inactive while its Python refusals and
dependent publisher gating remain. Direct stale consumer changes are bounded;
passing production tests and local validation registry entries are retained.

Four normal commits will record draft, ready, implementation and completion.
Workflow, registered-validator/tests and governance writers own disjoint paths;
this document writer alone stages and commits. At initial intake, creation,
source RED/GREEN, own index/message checks and closing acceptance were pending.
No current-source or hosted PASS is inferred from the removal request. Removed
GitHub QA and excluded local full/affected execution remain NOT_RUN; remote
outcomes and integrated-main results are recorded only if observed.


Readiness now records observed C1 registered-form C010 provenance, unchanged
regular template and absent prior target, six fresh canonical gates, exact
configured message and selection-only metadata. Permitted independent
structured/public-source review and the normal draft commit completed with
clean source; private raw direct audit remains NOT_OBSERVED/DEFER. Disposable
message semantic entries and configs matched; raw index-change cause is UNKNOWN.
At readiness intake, own ready-index/message checks, functional RED/GREEN,
implementation, completion, origin/main reflection and conditional cleanup were
pending. The historical
25m08s failing QA observation is input to removal, not a current PASS or proof.


Execution records observed ready-index six fresh gates, exact configured message,
selection-only metadata and separate permitted structured/public-source review.
The normal ready commit and public postidentity completed with clean state;
root then released disjoint source owners for the approved fifteen paths.
At early execution intake, WORK-015 work-unit acceptance and own C3/terminal
checks remained pending.
Private raw direct audit stays NOT_OBSERVED/DEFER; local full/affected execution
and hosted full QA remain NOT_RUN.

Actual job timing is separate from the earlier step13 observation: old job
112105040334 ran 04:16:02Z to 04:41:30Z, 1528s (25m28s), while step13 ran
25m08s. Job112090899701 ran 1472s (24m32s); job112125139531 ran
2026-10-06T05:36:46Z to 05:51:47Z, 901s (15m01s). Each observed completed
QA job exceeded the actual 600-second cutoff and failed. In the bounded recent
six-workflow sample, stale/changelog/Labeler/Greeting jobs took 4/7/5/6 seconds;
provenance had no executed job. The still-unconcluded run37428671826 was excluded.
These observations support the same qa removal, not additional workflow scope
or current source acceptance. Configured timeout values prove no elapsed time.

The package audit gap is separate: no Node package/lock consumer makes npm audit
NOT_APPLICABLE; absent pip-audit tooling leaves Python audit DEFER/NOT_RUN against
the unchanged lock. No audit PASS is claimed and no install/network action was
performed. The delivery operator must retain this gap in the terminal handoff;
any later environment/tool provision and audit outcome requires its own observed
record. At early C3 intake, functional source results, current C3 acceptance, closing
reflection and conditional cleanup had not yet been observed.

The metadata-only duration receipt is preserved under the primary-root ignored
`.worktrees/proposal/p02-task15-hosted-job-duration.receipt.json`, hashbfd42c72;
it records nine bounded remote query groups, not a full historical audit. Its
initial out-of-root structured-write attempt was blocked HOOK-PATH-ROOT and
remains NOT_RUN; the existing approved repository-owned record is observed.
This is duration input evidence, not hosted full-QA or current implementation PASS.


Implementation now records the actual final scoped hooks and 79 fresh named
GREEN methods, with complete declared-byte proof and stable source/index inputs.
The fourteen-input GREEN boundary is distinct from the eight-input hook scope;
neither certifies global or hosted full QA. The synthetic summary matrix covers
one hundred local event/result combinations, not one hundred GitHub jobs.
Earlier RED and formatter failures remain original observations, including
unexecuted secrets where recorded. Corrections were explicit writer edits;
source-changing attempts required fresh hooks and final-input GREEN, not AST
reuse or a repetition of an unchanged failed input. The obsolete PR sentence
mismatch was corrected before GREEN; no test ran on that blocked candidate.
At the initial implementation-candidate intake, own C3 canonical/message
acceptance, normal implementation commit, terminal completion, local/origin-main
reflection and cleanup were pending.
Private raw direct audit remains NOT_OBSERVED/DEFER; the recorded results are
collector structured evidence with separate public-source review.


The first actual C3 index invocation failed its repository-quality gate because
the current hub Scope omitted the strict consumer's generic QA gate phrase.
The other twelve gate results remain observations of that failed input, never
a new overall PASS. Exact message and selection checks were NOT_RUN. The root
selected a one-sentence hub correction that names only current PR branch and
isolated checks as the QA gate; hosted full QA remains NOT_RUN. No strict source,
Schema, Registry or proof implementation changed. After the original CI writer
stopped without a tool result and the old line was confirmed unchanged, root
explicitly delegated this sole hub sentence to the document writer; no refusal
or unobserved execution is inferred. All other CI files are preserved.
The hub and this Task are outside the original focused fourteen and hook eight
input maps; only complete unchanged scope/config/tool/mode/trust proof permits
scoped attribution. At repaired C3 intake, the candidate required all thirteen fresh canonical
gates, exact configured message and separate final review; those observed
results are now EVD-P02-161. Corrected C3 acceptance and terminal/integration/
cleanup were pending at that intake.


Local fixture/contract implementation acceptance now rests on observed final
source checks, corrected C3 actual-index/message acceptance, independent
permitted structured/public-source review and the normal implementation commit.
It does not certify hosted execution, package audit, origin/main reflection or
cleanup. Those outcomes remain separately observed delivery responsibilities.

At prospective intake, this isolated completed input asserted neither the actual
tracked Task status nor a C4 verdict. WORK-015 PASS denotes observed local
implementation only. Prospective completion, actual reflection and closing
checks were NOT_RUN at that intake; the actual tracked Task was in-progress.
Source reflection requires observed scoped prospective completion and separate
review. Any actual reflected closing candidate requires fresh staged QA,
SPEC0106 scoped completion, exact configured message and independent final
review to PASS before a normal completion commit. Actual outputs, closing OID,
local-main reflection and retained structured-evidence hashes belong in the
ignored terminal attachment, with no self-SHA rewrite. Origin delivery and
conditional cleanup belong to the separately assigned delivery owner. Original
failures, metadata qualifications, private raw direct NOT_OBSERVED/DEFER and
local full/affected NOT_RUN remain unchanged; no hosted PASS is asserted.

The first isolated prospective completion failed with COMPLETION-TRACE because
VAL-P02-015 was defined but absent from the parsed Spec trace table. EVD-P02-162
preserves that failed input and result. This revised nonauthoritative proposal
adds only the missing VAL015 trace row and a consistent Spec patch version;
the Spec remains completed and earlier trace rows remain unchanged. Revised
prospective completion and all actual closing checks remain pending until
separately observed. No original failure is promoted to PASS.
