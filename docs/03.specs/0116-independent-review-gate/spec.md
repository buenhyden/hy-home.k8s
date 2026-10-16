---
title: "Independent Review Merge Gate"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0116"
---

# Independent Review Merge Gate Technical Specification (Spec)

## Overview

[SPEC-0115 Task 0005](../0115-r10-local-remediation/tasks/tsk-0005-r13-residual-controls.md)
EVD-012 and the `SEC-P01-001` record in
[main protection](../../../.github/rulesets/main-protection.md) keep one HIGH
risk open. `main` requires `ci-summary` and `style-pr` from GitHub Actions App
`15368`, both defined in the PR-editable `.github/workflows/ci.yml`. A pull
request can rewrite that workflow so that jobs with the same names and the same
App report success. Required approving reviews are zero because the only human
collaborator authors every pull request and GitHub forbids self-approval.

On 2026-10-16 the operator asked for an AI agent to act as a separate reviewer
and then required that no AI model API be called. This Spec adds a merge gate
whose result can only come from a credential that no workflow can reach: a
dedicated review GitHub App whose private key exists only on the operator's
machine. A local, read-only reviewer agent running under the operator's
existing provider subscription produces a structured verdict; a stdlib
publisher binds it to the pull request's current head and creates the
`independent-review` check run as that App. Main protection then requires that
check from that App ID. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-independent-review-gate.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - `scripts/independent_review.py` and its focused tests;
  - the operator procedure in
    [RUN-0013](../../05.operations/runbooks/0013-independent-review-check-runbook.md);
  - creation and single-repository installation of the review App by the
    operator, and the first observed check run from it;
  - adding `independent-review` from the review App to classic `main`
    protection, with before/after read-back, and updating the main protection
    record and the EVD-012 disposition.
- Non-goals:
  - any call to an AI model API from CI or from the publisher, and any model
    API key in GitHub or in this repository;
  - a `pull_request_target` or other hosted reviewer workflow;
  - a second GitHub account or a non-zero required approval count;
  - moving `ci-summary` or `style-pr` off App `15368`;
  - provider permission changes that stop an agent session from running the
    publisher (left as residual risk below).

## Contracts

- The publisher accepts only a verdict with exactly `head_sha`, `reviewer`,
  `decision`, `summary` and `findings`; each finding has exactly `severity`
  (`critical`, `high`, `medium`, `low`), `path` and `message`. Any other shape
  exits 1 without a network call.
- The conclusion is `success` only for `decision: approve` with no `critical`
  or `high` finding; every other verdict publishes `failure`.
- Before publishing, the publisher reads the pull request with the App's
  installation token and requires it to be open against `main` with
  `head.sha` equal to the verdict's `head_sha`. The check run is created on
  that SHA only, so any later push leaves the new head without it; strict
  required checks separately make the reviewed head include the latest `main`.
- The installation token is requested for this one repository with only
  `checks: write` and `pull_requests: read`. The private key file must be a
  regular, non-symlink file with no group or other permission bits. The key
  and model credentials never enter the repository, GitHub secrets,
  environments or workflow files.
- The publisher holds the review App key, so it runs only from a trusted copy:
  the `origin/main` blob, never the pull request worktree. A pull request that
  changes the publisher is reviewed with that diff read by the operator before
  publishing. This package's own pull request is the one bootstrap exception:
  the publisher comes from the independently reviewed commit of this branch.
- The operator reads every verdict before publishing it.
- The reviewer must be a registered read-only reviewer role in a session that
  did not author or modify the reviewed changes, per
  [semantic review](../../../.agents/governance/quality.md#semantic-review).
  The publisher records the reviewer name; it cannot authenticate it.

## Core Design

```text
operator ─ local reviewer agent (read-only, fresh session, provider subscription)
             └─ verdict.json (head_sha, decision, findings)
operator ─ scripts/independent_review.py --repo R --pr N --verdict verdict.json
             ├─ App JWT signed by openssl with the local key (mode 0600)
             ├─ installation token: this repo, checks:write, pull_requests:read
             ├─ GET pull: open, base main, head.sha == verdict.head_sha
             └─ POST check-runs: independent-review @ head.sha, App <review>
main protection: ci-summary@15368, style-pr@15368, independent-review@<review>
```

A pull request that edits `ci.yml` can still forge the two Actions checks,
but no workflow can mint a token for the review App, so the third required
check stays missing or failed until the operator publishes a reviewed verdict
for that exact head. `enforce_admins` stays enabled, so the operator also
needs that check.

## Data Modeling & Storage Strategy

The verdict is a transient local JSON file, outside the repository. The
durable record is the check run itself (App, head SHA, conclusion, title and
summary) plus the Task evidence row that names it. The App private key lives
only in the operator's local configuration directory and is never copied,
printed or committed.

## Interfaces & Data Structures

```json
{"head_sha": "<40 hex>", "reviewer": "security-auditor",
 "decision": "approve", "summary": "...",
 "findings": [{"severity": "medium", "path": "a.py", "message": "..."}]}
```

Command: `python3 -I <trusted publisher copy> --repo OWNER/NAME --pr N
--verdict FILE [--check-only]`, with `REVIEW_APP_ID` and
`REVIEW_APP_KEY_FILE` in the environment. Output on success:
`independent-review id=… app=… head=… conclusion=… <url>`; on any error
`FAIL: <reason>` on stderr and exit 1.

## Edge Cases & Error Handling

- Head moved after review: publish refuses (`verdict head_sha is not the pull
  request's current head`); re-review the new head.
- Closed, merged or non-`main` pull request: publish refuses.
- Key file with group/other bits, symlink or missing: refuses before signing.
- GitHub HTTP or network failure, openssl failure or timeout, or an
  unexpected response shape: `FAIL` with a bounded reason only; no token or
  key material is printed. The installation token is revoked after use. A failure leaves the required check
  missing, which blocks merge.
- Oversized text is rejected (summary and message 4,000 characters, 100
  findings); the rendered check summary is capped at 60,000 characters.

## Failure Modes & Fallback / Human Escalation

- Lost or exposed key: the operator revokes it in the App settings and
  generates a new one; earlier check runs stay as history.
- Review App unavailable or misconfigured: merges stay blocked. Recovery is
  to fix the App or, by a separate reviewed operator decision with
  before/after read-back, remove the required check. Nothing here grants a
  bypass.
- Reviewer finds a blocking issue: publish the `failure` verdict, repair in a
  new commit and review the new head.
- Residual: the operator, and any local agent session the operator lets run
  the publisher with the key path, can publish without a genuine review. The
  gate removes forgery by PR-edited workflows; it does not make a solo
  operator independent of themself.
- Residual: the reviewer reads attacker-controllable pull request content
  (this is a public repository) and can be steered toward `approve` by prompt
  injection. The attack moves from workflow forgery to reviewer steering, and
  the operator's reading of the verdict is the remaining control.
- Residual: no provider deny rule covers the review key directory; only the
  default permission prompt stops a local agent from reading it. A scoped
  provider-permission follow-up may add Read and Bash denies for that path.

## Verification Commands

- `python -m unittest tests/test_independent_review.py` — verdict shape,
  conclusion rule, rendering and truncation, key mode and owner, an
  openssl-verified JWT and its claim window, `publish()` head/base refusal,
  token scope, check body and token revocation, and `main()` error exits.
- `python3 -I scripts/independent_review.py --check-only …` — offline verdict
  validation.
- `gh api repos/buenhyden/hy-home.k8s/branches/main/protection` before and
  after the protection change, and `gh api
  repos/buenhyden/hy-home.k8s/commits/<head>/check-runs` for the observed App
  ID. Static checks cannot establish remote state.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-IR-001 | Publisher tests pass on the implementation; staged QA on the exact index; independent read-only review of the script. |
| VAL-IR-002 | RUN-0013 and the README routes pass selected document checks and independent review against this Spec. |
| VAL-IR-003 | The operator-created review App is installed only on this repository with `checks: write` and `pull_requests: read`; an observed `independent-review` check run on a real PR head reports that App's ID, not `15368`. |
| VAL-IR-004 | Before/after `main` protection read-back shows only `independent-review` from the review App added; a PR is observed blocked without that check and mergeable with it; the main protection record and EVD-012 disposition state what is closed and what remains. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-IR-001 | Focused tests, staged QA and independent review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-IR-002 | Document checks and independent review |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-IR-003 | Operator-approved App creation and observed check run |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-IR-004 | Authenticated protection read-back and observed merge state |
