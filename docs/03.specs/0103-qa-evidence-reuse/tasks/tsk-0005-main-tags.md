---
title: "Protected immutable main tag publisher"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0005"
---

# Task: Protected immutable main tag publisher

## Overview

Execute [Plan WP-0005](../plan.md) against the approved [SPEC-0103](../spec.md).
Local implementation publishes only an authenticated successful main tip using
a separate, default-off publisher identity. Independent code and security
reviews passed after the authenticated retry correction. App/environment and
tag-ruleset setup has been observed in part; publisher permission read-back,
denied-write trials and publication remain DEFER. This record claims no tag or
Spec completion.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current
  [quality policy](../../../../.agents/governance/quality.md).
- [Task 3 protected proof](tsk-0003-protected-proof.md) and
  [Task 4 main verdict](tsk-0004-main-reuse.md): v1/v3 PR sources remain separate
  from v2 full main and v4 main with one independently reauthenticated reuse.
- Criterion: VAL-QER-010.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-005 | VAL-QER-010 | Follow Plan Task 5 RED, GREEN, review, and handoff steps | platform | In progress | Local implementation reviewed; protected publication DEFER | Snapshot, partial settings read-back and remaining operator obligations below. |

## Approval and Safety Boundaries

- **Allowed Paths**: .github/workflows/qa-verifier.yml;
  .github/repository-surface.md; scripts/publish_main_tag.py;
  tests/test_publish_main_tag.py; tests/test_ci_qa_workflow.py; this Task and its
  ignored Task 5 report. No additional owner or validation registry changed.
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault
  mutation, archived Spec bodies, and unrelated implementation files.
- **Approval Required**: operator review before separate publisher App installation,
  main-only key environment, effective tag rulesets, activation or publication.
  Approved local source changes do not authorize those external actions.
- **Static Validation**: focused publisher/workflow/provenance tests, affected quick
  and exact-index staged QA, Actions security, pinned ruff/actionlint/zizmor,
  whitespace and actual-message validation.
- **Live Validation**: authenticated App/environment/required-check/ruleset and
  complete bypass-actor read-back; ordinary publisher token denied update/delete;
  exact main tag and retry with source SHA/run/attempt/check ID. Partial settings
  are observed below; permission, denied-write and publication evidence remain DEFER.
- **Secret / Vault Handling**: no secret values read or stored in local evidence.
  Static `qa-verifier.yml` references the publisher and verifier keys in separate
  jobs/steps bound to `qa-tag-publish` and `qa-control`, respectively. At the
  original implementation checkpoint, App installation, environment branch
  restrictions, secret placement and authenticated read-back were DEFER. No App/settings/tag/remote Git/live resource changed.
- **Rollback Plan**: disable environment `QA_TAG_ENABLED`; never move or delete
  published main tags. Revert the local publisher unit only through a reviewed
  forward change, preserving protected verifier and full main QA.
- **Evidence Location**: this Task; ignored working report at
  `.superpowers/sdd/plan/task-5-report.md` carries final evidence-commit identity.

## Verification Summary

### Checked snapshot and implementation

- Worktree: the `qa-evidence-implementation` linked checkout;
  branch `codex/qa-evidence-implementation`; clean starting HEAD
  `8032a095b58a14da7194d8d0460f5ca25d4e23f0`; branch divergence base
  `0ed105b832d85c88b1000ad58959531d1ae23cae`. Implementation commit
  `fba1baac27c619cc0d8416b4466a422759c014c3`, checked tree
  `39d4c6e5b77ab892b2285b8cb180980648ad005b`, contains exactly five approved
  code/test/workflow/hub paths. Corrective commit
  `3211d2cd6c64cabaa93b854bb3c071ce8e8bed00`, checked tree
  `e3a006321efe3094d72a536dbbae02822ac24536`, changes only the publisher,
  its tests and the hub. Earlier tasks were preserved.
- The publisher reuses the existing bounded verifier and parser. It independently
  reconstructs the provider run/current attempt, CI workflow, repository,
  successful jobs/steps, actual checkout and full required gate record before
  accepting the expected verifier App's exact `qa-main-verdict`. v2 requires
  23 PASS; v4 requires 22 PASS plus the one proven original PR reuse. Generic
  `ci-summary`, name-only green, PR v1/v3, incomplete or stale records do not
  authorize publication. Identical exact-source App checks allow a verifier
  retry; conflicting records reject.
- `workflow_run` ref/SHA select protected default-branch control and are not
  the triggering push ref/`after`. Source run `event=push`, `head_branch=main`
  and `head_sha`, the protected record's tested commit and current main commit
  ref must agree for new tag creation. Exact existing commit tags remain
  authenticated no-ops after main advances. No absent push `after` field is
  fabricated. The reviewed CI branch-only push filter excludes tag-originated
  runs. Multi-commit pushes create only their validated tip; observed main
  advancement rejects missing-tag creation.
- A first publisher step has no private key. The second independently repeats
  source and exact-App-check authentication before reading the publisher key.
  It validates the distinct active App and its exact metadata/read+contents/write
  installation ceiling, requests one repository ID and those permissions,
  verifies returned permissions/repository scope, and revokes the token.
  The workflow GITHUB_TOKEN remains read-only; checkout pin and verifier steps
  are unchanged. No PR content, cache or artifact is executed.
- The writer permits exact reference reads and one `POST` create shape for
  `refs/tags/main-<40-hex SHA>`. Same-target commit ref is `noop`; a different
  target, annotated tag or invalid response fails. 409/422 concurrent-create
  responses require an identical read-back; all other API failures stay failures.
  Ref PATCH/DELETE and force are denied locally. Token revocation uses only
  `/installation/token`; it cannot delete a Git ref.
- The job requires successful verifier completion plus successful source main
  push/repository identity before `qa-tag-publish` environment access.
  Environment-owned `QA_TAG_ENABLED` is default-off and checked in both step
  guards and the CLI. Environment variables become available after job start,
  so the job-level source gate does not depend on that environment variable.
  Operators must avoid a same-name repository/organization variable.
- Existing `branches: [main]` QA push filtering excludes tag pushes and
  changelog `v*.*.*` excludes `main-*`. App token-generated events can start
  workflows, so tests check these filters independently of GITHUB_TOKEN's
  non-recursion behavior.

### Executed local evidence

- RED: `python3 -m unittest tests.test_publish_main_tag` failed with ImportError
  because the publisher module did not exist. The new publisher-environment
  workflow test separately failed with `KeyError: publish-main-tag`.
- GREEN: `python3 -m unittest tests.test_publish_main_tag
  tests.test_ci_qa_workflow tests.test_qa_provenance
  tests.test_qa_provenance_hosted`: 86 tests PASS in 1.899 seconds after the retry fix.
  The 20 publisher cases cover wrong events/branch/repository/workflow/SHA/App,
  source attempt/conclusion, actual checkout, stale tip/control bytes,
  complete v2/v4 records, key-read ordering/default-off, token restrictions,
  multi-commit tip, idempotency/collision/concurrency and API failures.
- `python3 -m trace --count --summary --missing --coverdir
  /tmp/qa-task5-fix1-coverage --module unittest tests.test_publish_main_tag`:
  20 PASS; publisher statement coverage 96% over 219 executable lines.
  This is not branch, whole-repository or hosted coverage; no dependency added.
- `python3 scripts/validate-github-actions-security.py --root .`: PASS.
  Pinned `ruff-check`, `ruff-format`, `actionlint` and `zizmor`: PASS on changed
  applicable files. The first formatting run explicitly rewrote the three
  selected Python files; focused results above cover their final bytes.
- `python3 scripts/qa.py quick`: all 8 selected affected gates PASS over the
  five implementation/test/workflow/hub paths. After review repairs, quick
  passed all 12 selected gates over the publisher, its tests, hub and Task draft.
  No full QA or aggregate unit discovery was repeated; Task 6 owns final
  delivery validation.
- Implementation exact-index `python3 scripts/qa.py staged`: all 8 gates PASS
  on the same five paths and tree above. Both working/cached whitespace checks
  and pinned Commitizen over the actual UTF-8 message passed. Normal
  `git commit -F /tmp/qa-task5-commit-message` completed with the existing hook
  path and no bypass; the implementation worktree was clean afterward.
  The corrective three-path index separately passed all 8 staged gates,
  both whitespace checks and actual-message Commitizen, then normal
  `git commit -F /tmp/qa-task5-fix-message` completed. Pre-commit preserved and
  restored the uncommitted Task draft. This final Task-only evidence change
  receives separate document validation; its final commit/tree and results
  are recorded in the ignored Task 5 report and supervisor handoff without
  a self-referential commit rewrite.
- Python 3.12.3 and RTK 0.49.0. The sandbox failed before command execution
  (`bwrap` network namespace setup); scoped tools ran through approved escalation.
  Existing `core.hooksPath=scripts/githooks` remained unchanged, with no bypass.

### Review, activation and residual limits

- Author self-review checked exact diff scope and preserved verifier contracts.
  Independent `review_task5_code` initially returned Spec FAIL / quality Needs
  fixes: same-target retry incorrectly failed after main advanced, and the hub
  still described one QA job. The added later-main retry case was RED before
  correction. Shared exact-tag lookup now allows authenticated same-target
  `noop` while absent stale or conflicting tags fail; source/App authentication
  remains mandatory. The hub now describes the split CI topology.
- Scoped re-review of `fba1baac..3211d2cd`: `review_task5_code` returned Spec PASS /
  quality Approved with no residual finding. `review_task5_security` returned
  static PASS, confirming no stale-source creation or no-proof path. These are
  independent repository-static reviews, not hosted authorization or enforcement.
- An initial Task-draft quick run failed on an unsupported hub H2, a combined
  traceability identifier and an absolute local checkout path. The hub section
  is now H3, the traceability row contains one WORK identifier, and the Task
  records the linked worktree name without a local absolute path. The subsequent
  four-path quick run passed all 12 gates, including document profiles, links,
  lifecycle and repository quality.
- `contents: write` is an App permission ceiling, not immutable tag enforcement.
  Operator activation must observe two active `refs/tags/main-*` rulesets:
  creation permits the publisher through a creation-only bypass, while update
  and deletion forbid publisher bypass. Record separately authorized operator
  bypass, inherited rules and all effective actors. Missing `bypass_actors` from
  an API caller without ruleset-write visibility is unknown, never an empty list.
  App/environment/required-source read-back and ordinary-token denied update/delete
  remain DEFER; local transport-denial tests do not establish remote denial.
- After settings evidence, the operator must observe one successful main
  publication and same-target retry, retaining exact repository/SHA/source
  run/attempt/verdict check ID/tag target. Until then `QA_TAG_ENABLED` stays off.
  Protected main checks can attest full QA before PR reuse is activated.
- GitHub main-ref read and tag POST are separate API operations. The writer
  rechecks main immediately before creation but cannot make an atomic
  compare-main-and-create-tag transaction. A main advance within that final
  API interval can leave a tag on the fully authenticated tested source commit;
  it cannot redirect the tag to an unvalidated commit. No automatic tag cleanup
  is permitted. API ambiguity, bounded lookup failure or stale proof rejects.
- Next owners: supervisor for final evidence review and Task 6 integration;
  operator for all hosted settings, denied-operation and publication observations.

Official contracts were checked on 2026-10-02:
[workflow_run identity](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run),
[ref creation](https://docs.github.com/en/rest/git/refs#create-a-reference),
[installation token narrowing](https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app),
[ruleset bypass read-back](https://docs.github.com/en/rest/repos/rules#get-a-repository-ruleset),
[environment timing](https://docs.github.com/en/actions/reference/workflows-and-actions/variables#configuration-variable-precedence),
[App-created events](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

### Hosted activation supplement — 2026-10-02

- `qa-control` and `qa-tag-publish` each expose the expected secret **name** and
  an exact `main` deployment-branch restriction; no secret value was read.
  Repository variables identify CI workflow 227337643, verifier App 5156553
  and publisher candidate App 5156559. `QA_PROVENANCE_ENABLED` is true;
  `QA_REUSE_ENABLED` and environment `QA_TAG_ENABLED` remain off. The
  publisher App's effective installation permissions have not yet been read
  back, so its ID alone does not satisfy the publisher-identity gate.
- Two active rulesets target `refs/tags/main-*`: creation-only rule 24342332
  has Integration 5156559 as an `always` bypass actor; update/deletion rule
  24341547 has no bypass. These are configuration read-backs, not successful
  denied-write trials. A 404 against a nonexistent tag ref says nothing about
  whether a matching existing tag resists update or deletion.
- Full main QA run 36953307326 passed on `98a6b00e`, and the verifier
  App authored successful `qa-main-verdict` check 110675592214 on that exact
  SHA. The publisher remains disabled; this is verdict evidence, not a tag or
  publisher-permission read-back.
- Safe one-time bootstrap: first observe a protected successful main verdict
  and publisher installation permission ceiling. Then enable environment
  `QA_TAG_ENABLED` for one main push, record the exact source SHA, run/attempt,
  App verdict check ID and resulting `main-<full SHA>` target. Immediately
  attempt ordinary-token update and deletion against that **existing** matching
  ref and record both denials; disable tagging if either denial fails. Finally
  observe a same-target retry. No tag publication or immutability claim is
  made yet. Next owner: operator/supervisor for publisher permission read-back
  and hosted tag/denial trials. Rollback: set `QA_TAG_ENABLED` off;
  retain existing immutable refs rather than moving or deleting them.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-005](../plan.md#work-breakdown) | Local implementation PASS; protected publication DEFER | RED/GREEN and review above; 2026-10-02 settings read-back below; no remote tag or denied-write result claimed. |
