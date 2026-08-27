---
title: 'Workspace Research Full-Corpus Refresh Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-17
artifact_id: "PLAN-0059"
---

# Workspace Research Full-Corpus Refresh Plan (Plan)

## Overview

This plan executes the fifth refresh cycle designed by
[Spec 0059](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md)
over the existing
[2026-08-08 WER pack](../../90.references/research/2026-08-08-wer/README.md).
It sequences thirteen work packages, `WRFC-000` through `WRFC-012`, so that
external source re-observation, workspace re-observation, blocking-class
closure, scope re-projection, and cross-link reconciliation each land as one
logical commit with its own repository-static evidence.

The five research packages `WRFC-002` through `WRFC-006` run in parallel
through read-only subagents. Every other package is sequential, and cross-link
reconciliation is deliberately placed after all content work so that link and
owner validation observes the terminal shape.

## Context

Twenty-three human request lines expand onto the thirty-six `REQ-WERPC` owner
rows the pack already registers, because two request lines each name six
document families. The request scope is byte-equivalent to
Spec 057 at
`docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md`,
and Specs 055, 056, and 057 each re-tested the same twelve `Partial` rows
without promoting any of them.

This cycle therefore does not repeat a twelve-row sample. It re-observes all
thirty-six owners, which reaches the twenty-four `Verified` rows that have gone
unchecked since 2026-08-08, and it closes each retained `Partial` or `DEFER`
row against further repository-static re-testing by naming the evidence class
that blocks it.

Two inherited hazards shape the sequencing. The Markdown formatter re-pads every
cell of a table to its widest cell and previously inflated the source ledger from
797 KB to 3.0 MB, so ledger rows are written through a shell heredoc. And
`scripts/validate-active-corpus-residue-closure.py` refuses to let a Spec reach
`done` unless it is registered in `POST_CLOSURE_SPEC_AUTHORITY_PATHS`, a step the
Spec 057 plan omitted and which is scheduled explicitly here.

A third hazard was discovered during setup and is recorded for successors: the
`post-validate.sh` PostToolUse hook resolves `select-affected-surfaces.py`
against `CLAUDE_PROJECT_DIR`, so an edit made inside a linked worktree fails
`SURFACE-PATH-NORMALIZATION` and is rejected. This cycle therefore executes on a
branch in the primary checkout rather than in a worktree.

### Legacy Task ledger inputs

This Task tracks execution evidence for the `WRFC-000` through `WRFC-012` work
packages defined by the human-approved
[Spec 0059](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md)
and its reciprocal
[Plan](plan.md). It records
the full-corpus external and workspace re-observation of all thirty-six
`REQ-WERPC` owner rows, the blocking-class closure over every retained `Partial`
and `DEFER` row, scope re-projection, cleanup, cross-link reconciliation, and
lifecycle registration.

All evidence recorded here is repository-static or public-documentation
evidence. No live cluster, hosted CI run, provider-runtime, remote,
credential-bearing, or deployment evidence was collected or claimed.

- [Spec 0059](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md)
- [Plan](plan.md)
- [2026-08-08 WER pack](../../90.references/research/2026-08-08-wer/README.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)

### Topic ledger

`WRFC-001` derived the ledger from the pack coverage matrix rather than
restating it. The parse returned thirty-six `REQ-WERPC` rows, numbered `001`
through `036`, with zero duplicate identifiers and zero numbering gaps.

The twenty-three human request lines expand onto exactly those thirty-six
owners. Two request-line pairs are duplicates of each other: the line naming the
SDLC document set and the line naming `SPEC, TASK, PLAN, PRD, AD, ADR` resolve
to the same six owners, and the line naming the operations document set and the
line naming `guide, incident, postmortem, policy, release, runbook` resolve to
the same six owners. Two further lines each expand onto more than one owner: the
Claude-and-Codex status line onto `REQ-WERPC-004` and `005`, and the AI-agents
line onto `REQ-WERPC-026` and `027`. The union of all request lines equals the
thirty-six-row ledger exactly, with no request line left unmapped and no owner
row left unclaimed.

Package assignment covered the ledger exactly once: nine rows to `WRFC-002`,
four to `WRFC-003`, sixteen to `WRFC-004`, three to `WRFC-005`, and four to
`WRFC-006`.

### External observation result

All thirty-six rows were re-observed on 2026-08-17. Six returned `changed` and
thirty returned `unchanged`. No row returned `unreachable`.

| Request ID    | External | What changed                                                                   |
| ------------- | -------- | ------------------------------------------------------------------------------ |
| REQ-WERPC-004 | changed  | Claude Code advanced from observed `2.1.220` to `2.1.233` (2026-08-14)         |
| REQ-WERPC-006 | changed  | Claude memory and subagent pages gained fields beyond the adopted scope        |
| REQ-WERPC-008 | changed  | kube-state-metrics `v2.14.0` pin versus upstream `v2.19.1`                     |
| REQ-WERPC-011 | changed  | `ISO/IEC/IEEE DIS 29148` entered ballot; 2018 edition not yet superseded       |
| REQ-WERPC-021 | changed  | `llms.txt` now v2; MCP current revision `2026-07-28` supersedes the cited path |
| REQ-WERPC-025 | changed  | Argo CD `sourceIntegrity` shipped GA in `3.5.0` and `3.5.1`                    |

The absence of any `unreachable` row is itself a delta. Prior cycles recorded
`diataxis.fr` behind HTTP 429 on three separate attempts and fell back to the
upstream source that builds the site. On 2026-08-17 the published page responded
directly, so the `SRC-WERPC-067` fallback was not needed. Two other hosts,
`iso.org` and once `docs.aws.amazon.com`, returned HTTP 403 to direct retrieval;
both were resolved through a search-mediated fallback rather than recorded as
unreachable, and that host-flakiness class is recorded for successors.

### Fired refresh triggers

Two rows had refresh triggers that the pack itself had written down, and both
fired. This is a contract signal rather than an opinion.

- `REQ-WERPC-008` and `REQ-WERPC-025` share the Argo CD `sourceIntegrity`
  trigger. The pack described the facility as forward-looking and labeled
  version 3.5; it is now shipped in stable `3.5.0` (2026-08-04) and `3.5.1`
  (2026-08-12).
- `REQ-WERPC-008` also carries the kube-state-metrics version trigger. The
  repository pins `v2.14.0` at
  `gitops/platform/monitoring/kube-state-metrics.yaml:114`, five minor versions
  behind upstream `v2.19.1` (2026-06-10). The upstream standard `ClusterRole`
  still grants `secrets` `list` and `watch`, so the pack's security claim is
  unchanged. **Correction, 2026-08-18:** this row originally added that upstream
  introduced a `serviceaccounts` resource absent at `v2.14.0`. That was wrong and
  is withdrawn. A direct diff of the shipped standard `ClusterRole` at both tags
  shows them byte-identical except the version label; the real divergence is that
  this repository's role has always been a trimmed subset of upstream's. See the
  dated correction in the Kubernetes and security report.

### Workspace observation result

All thirty-six rows returned `confirmed` except `REQ-WERPC-018`, which returned
`absent` as expected: a case-insensitive search across
`docs/99.templates/registry.json` returns zero matches for a
`release` profile, confirming the `DOC-G5` decided gap is intact rather than
drifted.

One repository-static sub-claim was partially closed by new evidence. A
repository-wide search for `kube_secret_` found zero matches in any tracked
Grafana dashboard, Prometheus rule, or alert configuration; only the research
documents themselves mention the string. That closes the in-repository half of
the `REQ-WERPC-008` consumer-need sub-claim. It cannot close the claim outright,
because `gitops/platform/monitoring/kube-state-metrics.yaml:3` states the real
consumer is an external Docker-hosted Prometheus outside this repository's
tracked paths, whose query set remains `DEFER`.

### Blocking-class closure

`WRFC-007` assigned exactly one blocking class to every retained `Partial` and
`DEFER` row. Twelve rows are unblocked. Ten are reachable by repository-static
work. Fourteen are structurally unreachable and are closed against further
static re-testing.

| Class            | Rows                                                       | Reachable by static work |
| ---------------- | ---------------------------------------------------------- | ------------------------ |
| none             | 007, 011, 012, 013, 015, 016, 017, 019, 027, 029, 030, 031 | n/a                      |
| repo-static      | 003, 004, 005, 006, 010, 021, 024, 034, 035, 036           | yes                      |
| provider-runtime | 001, 002, 026, 028, 032                                    | no                       |
| hosted-ci        | 022, 023                                                   | no                       |
| live-cluster     | 008, 009, 025                                              | no                       |
| human-judgement  | 014, 018, 020, 033                                         | no                       |

The fourteen rows in the last four classes are the reason Specs 055, 056, and
057 each promoted nothing. Their blocking evidence is an authenticated provider
runtime, a hosted CI run, a live cluster, or a named human or stakeholder
judgement. No amount of repository reading obtains any of those. Recording the
class terminates the re-test loop: a successor cycle cites this closure instead
of re-observing the row, and reopens it only on the named condition.

### Status effect

No status changed. All thirty-six rows recorded `statusEffect` of `no-change`;
no row was promoted, demoted, or contradicted. Under Spec 058 `C-WRFC-004` a
cycle that promotes nothing is a success provided the delta and its boundaries
are recorded, and the six `changed` external results plus the two fired triggers
are that delta.

Three of the six `changed` rows — `REQ-WERPC-004`, `011`, and `021` — carry
status `Verified` and were therefore outside the twelve-row `Partial` sample
that the three preceding cycles re-tested. Full-corpus scope is what reached
them.

### Cleanup record

| Artifact                        | Tracked | Consumers                                                                    | Decision            |
| ------------------------------- | ------- | ---------------------------------------------------------------------------- | ------------------- |
| `/tmp/mainchk.2121327` worktree | no      | none; registration was already `prunable`                                    | removed             |
| `graphify-out/GRAPH_TREE.html`  | yes     | none found; absent from `README.md:146` and from `.markdownlint-cli2.yaml`   | contract-corrected  |
| `graphify-out/GRAPH_REPORT.md`  | yes     | `README.md:146`, `.codex/CODEX.md:45`, harness catalog, four validator rules | retained            |
| `graphify-out/graph.json`       | yes     | `README.md:146`, `.codex/hooks.json:32` PreToolUse                           | retained            |
| `graphify-out/graph.html`       | yes     | `README.md:146`, `.markdownlint-cli2.yaml:52`                                | retained            |
| `__pycache__` directories       | no      | none; already ignored                                                        | retained as ignored |

`graphify-out/` as a whole is live convention, not one-off residue: `README.md`
documents it, `.codex/hooks.json` reads `graph.json` at `PreToolUse`,
`.codex/CODEX.md` instructs reading `GRAPH_REPORT.md`, the harness catalog lists
it as a knowledge store, and four validator or profile rules name it explicitly.
Deleting it would break those consumers, so Spec 058 places that deletion out of
scope.

The one genuine defect is narrower. `README.md:146` declares that only
`GRAPH_REPORT.md`, `graph.json`, and `graph.html` are tracked, yet
`GRAPH_TREE.html` is tracked as a fourth file and is the only one of the four
missing from the `.markdownlint-cli2.yaml` ignore list. Under Spec 058
`C-WRFC-010` a tracked-file deletion requires a named human decision, so this
cycle corrects the documented contract to match the tracked reality rather than
deleting tracked content on its own authority.
## Goals & In-Scope

- Derive the thirty-six-row topic ledger from the pack rather than restating it.
- Re-observe every owner row externally and in the workspace, as separate
  results.
- Assign exactly one blocking class to every retained `Partial` or `DEFER` row,
  and record what evidence would reopen it.
- Re-project the ten governance scopes from `docs/00.agent-governance/scopes/`.
- Reconcile the documented `graphify-out/` tracking contract with the actual
  tracked file set.
- Reconcile pack file count, owner-row count, source ID count, and claim ID
  count across the pack README, the collection README, and the ledger.
- Register Spec 058 across every lifecycle surface that a closed cycle Spec
  requires.
- Land one commit per work package and integrate the branch into `main`.

## Non-Goals & Out-of-Scope

- Creating a new research pack, a duplicate report, or a parallel scope-view
  folder.
- Creating, renumbering, or rewriting any existing requirement, source, or claim
  identifier.
- Adding any H2 heading to any touched document.
- Live k3d, ArgoCD, Vault, ESO, cluster, gateway, or registry inspection.
- Hosted CI execution, workflow dispatch, deployment, promotion, or rollback.
- Provider-runtime discovery, authentication, hook delivery, permission
  enforcement, or model resolution evidence.
- Deleting `graphify-out/GRAPH_REPORT.md`, `graph.json`, or `graph.html`, which
  are live convention referenced by `README.md`, `.codex/CODEX.md`,
  `.codex/hooks.json`, the harness catalog, and four validator or profile rules.
- Any change to `.worktrees/docs-sdlc-governance-consolidation` or its branch.
- Pushing any branch to a remote or publishing any artifact.

## Work Breakdown

| ID       | Package                    | Depends on    | Parallel |
| -------- | -------------------------- | ------------- | -------- |
| WRFC-000 | Cycle setup and baseline   | none          | no       |
| WRFC-001 | Topic ledger derivation    | WRFC-000      | no       |
| WRFC-002 | Agent-system research      | WRFC-001      | yes      |
| WRFC-003 | Governance and providers   | WRFC-001      | yes      |
| WRFC-004 | SDLC and documentation     | WRFC-001      | yes      |
| WRFC-005 | Platform and security      | WRFC-001      | yes      |
| WRFC-006 | Delivery evidence          | WRFC-001      | yes      |
| WRFC-007 | Blocking-class closure     | WRFC-002..006 | no       |
| WRFC-008 | Scope re-projection        | WRFC-007      | no       |
| WRFC-009 | Cleanup and contract fix   | WRFC-001      | no       |
| WRFC-010 | Cross-link reconciliation  | WRFC-002..009 | no       |
| WRFC-011 | Lifecycle registration     | WRFC-010      | no       |
| WRFC-012 | Validation and integration | WRFC-011      | no       |

### WRFC-000 — cycle setup and baseline

Capture the full validation lane before any content change, so that a later
failure is attributable. Record the branch, its base commit, and the observation
that `.worktrees/docs-sdlc-governance-consolidation` is left untouched.

### WRFC-001 — topic ledger derivation

Parse the pack README coverage matrix and assert thirty-six unique
`REQ-WERPC` rows with no numbering gap. Map each of the twenty-three human
request lines onto its owners and assert the union is exactly the thirty-six
rows. A mismatch fails the package rather than being reconciled silently.

### WRFC-002 through WRFC-006 — parallel research

Each package receives its owner rows, the current recorded status, the pinned
source set, and the workspace paths named by the coverage matrix. Each returns
one dated finding block per row carrying an external result, a workspace result,
a status effect, a blocking class, and a reopen condition. Subagents are
read-only by tool grant, which enforces the Spec `C-WRFC-009` write boundary
structurally rather than by instruction.

Package assignment covers the ledger exactly once: nine rows to `WRFC-002`,
four to `WRFC-003`, sixteen to `WRFC-004`, three to `WRFC-005`, and four to
`WRFC-006`.

### WRFC-007 — blocking-class closure

Assign one blocking class per retained `Partial` or `DEFER` row and mark it
reachable or structurally unreachable by repository-static work. This package
may not change a status; it records why a status persists.

### WRFC-008 — scope re-projection

Re-derive scope membership from `docs/00.agent-governance/scopes/` and re-test
the unowned canonical path set, then update the pack scope application index.

### WRFC-009 — cleanup and contract fix

Enumerate every reference to each cleanup candidate before acting. Remove only
untracked transient artifacts that no contract references. Where the documented
contract and the tracked file set disagree, correct the contract rather than
delete tracked content, and record the decision.

### WRFC-010 — cross-link reconciliation

Reconcile the four counts across the pack README, the collection README, and the
ledger, then apply cross-link and reference updates. This is the last content
commit of the cycle.

### WRFC-011 — lifecycle registration

Add the Stage 03 and Stage 04 index rows and tree entries, the
`standaloneExecutions` entry in `document-profiles.json`, the ADR 0022 lineage
row, the `POST_CLOSURE_SPEC_AUTHORITY_PATHS` allowlist entry, its mirrored test
fixture, and the durable progress ledger record.

### WRFC-012 — validation and integration

Run the full lane, compare against the `WRFC-000` baseline, integrate the branch
into `main`, and remove the cycle branch. Report any worktree that could not be
removed under the active permission boundary.

## Verification Plan

| ID           | Package       | Verification                                                              |
| ------------ | ------------- | ------------------------------------------------------------------------- |
| VAL-WRFC-001 | WRFC-001      | Thirty-six unique rows derived from the pack, no gap, request union exact |
| VAL-WRFC-002 | WRFC-002..006 | Every row records external and workspace results separately               |
| VAL-WRFC-003 | WRFC-007      | Every retained Partial or DEFER row carries one blocking-class record     |
| VAL-WRFC-004 | WRFC-002..006 | Source and claim IDs unique, sequential, none rewritten                   |
| VAL-WRFC-005 | WRFC-002..006 | Pack file count unchanged at fourteen, no H2 added                        |
| VAL-WRFC-006 | WRFC-002..006 | Every unreachable source recorded as such, never as unchanged             |
| VAL-WRFC-007 | WRFC-008      | Scope projection re-derived, unowned-path set re-tested                   |
| VAL-WRFC-008 | WRFC-010      | Pack README, collection README, and ledger agree on four counts           |
| VAL-WRFC-009 | WRFC-010      | Cross-link reconciliation is the last content commit                      |
| VAL-WRFC-010 | WRFC-009      | graphify tracking contract and tracked file set agree                     |
| VAL-WRFC-011 | WRFC-010      | Ledger byte size recorded before and after, under 1 MB                    |
| VAL-WRFC-012 | WRFC-012      | All ten verification commands pass against the recorded baseline          |
| VAL-WRFC-013 | WRFC-000..012 | One commit per package, no temporary file survives, branch merged         |

Verification commands are owned by
[Spec 0059](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md)
and are not restated here.

### Legacy Task verification evidence

Baseline captured before any content change, on the cycle branch based at
`e98af463`:

- `bash scripts/validate-repo-quality-gates.sh .` → `[PASS] repository quality gates passed`
- `python3 scripts/validate-links-and-owners.py --self-test` → `[PASS] cross-document validator self-test passed`
- `python3 scripts/validate-links-and-owners.py --root . --mode strict` → `PASS CROSS-DOCUMENT`
- `python3 scripts/validate-document-contract-registry.py --root . --mode strict` → `PASS document contract registry: 512 paths`
- `python3 scripts/validate-markdown-profiles.py --root . --mode strict` → `PASS SUMMARY . - actual="0"`
- `python3 scripts/validate-reference-information-architecture.py --self-test` → `Reference information architecture self-test: PASS`
- `python3 scripts/validate-affected-surfaces.py --root .` → `[PASS] affected surface validation passed: paths=863 surfaces=22/22 validators=22 ci_jobs=4 uncovered=0 ambiguous=0`

The lane was already green before this cycle began. These results are evidence of
no regression, not of a newly attained state. Terminal lane results are recorded
by `WRFC-012`.
## Risks & Mitigations

| Risk                                             | Mitigation                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------- |
| Cycle repeats Spec 057 and adds nothing          | Full-corpus scope plus terminal blocking-class closure, both new this cycle |
| Formatter inflates the source ledger             | Heredoc writes plus recorded before/after byte size                         |
| Spec cannot reach `done`                         | `POST_CLOSURE_SPEC_AUTHORITY_PATHS` registration scheduled in WRFC-011      |
| Subagent writes cause identifier collision       | Read-only tool grant; orchestrator is sole identifier allocator             |
| Unreachable source silently read as unchanged    | `C-WRFC-003` forbids it; `VAL-WRFC-006` checks it                           |
| Link validation observes an intermediate shape   | Reconciliation ordered last by `C-WRFC-008`                                 |
| Tracked content deleted without consumer proof   | `C-WRFC-010` requires enumeration and a named human decision                |
| Hook rejects edits made inside a linked worktree | Execute on a branch in the primary checkout; recorded in Context            |
| Branch integration conflicts with `main`         | Stop and report; no history rewrite                                         |

### Legacy Task approval and rollback boundaries

- Direct human approval on 2026-08-17 authorized this cycle, selecting
  full-corpus scope over a twelve-row repeat and full Spec/Plan/Task lifecycle
  documents over a research-only change, and selecting append-in-place over a
  new dated research pack.
- No live k3d, ArgoCD, Vault, ESO, cluster, gateway, or registry command was
  run. No workflow was dispatched, re-run, or merged.
- No secret value was read, echoed, or recorded.
- Research subagents were granted `Read`, `Grep`, `Glob`, `WebFetch`, and
  `WebSearch` only. The Spec `C-WRFC-009` write boundary is therefore enforced
  by tool grant rather than by instruction, and the orchestrating session
  remained the sole allocator of source and claim identifiers.
- Dependabot PR 50 on the remote, bumping `actions/stale` from `10.4.0` to
  `11.0.0` against `.github/workflows/stale.yml:22`, was observed read-only. It
  was neither approved, merged, nor dispatched.
- `.worktrees/docs-sdlc-governance-consolidation` and its branch were left
  untouched. It carries thirty-six commits absent from `main`, `main` carries
  seventy-seven commits absent from it, and it holds staged uncommitted changes
  belonging to a different session.
- No branch was pushed to any remote and no artifact was published.

### Recorded harness limitation

The `post-validate.sh` `PostToolUse` hook resolves
`scripts/select-affected-surfaces.py` against `CLAUDE_PROJECT_DIR`. An edit made
inside a linked worktree therefore fails `SURFACE-PATH-NORMALIZATION` with
`path must be repository-relative`, and `scripts/document_contracts.py:603`
excludes `.worktrees` from the surface map entirely. A worktree-based attempt was
abandoned for this reason and the cycle executed on a branch in the primary
checkout. Successor cycles should plan for a branch rather than a worktree until
that hook is made worktree-aware, which is a shared-tooling decision and is not
made here.

The permission boundary active in this session denied `rm -rf`,
`git worktree remove --force`, and `git branch -D`. The abandoned worktree was
freed non-destructively with `git checkout --detach` so that its branch name
could be reused; its removal is reported as a residual item rather than claimed
as complete.

### Out-of-ledger observations

These findings do not map onto any of the thirty-six owner rows, so under
`C-WRFC-001` they create no requirement row and are recorded here instead.

- `docs/00.agent-governance/model-policy.md` still links
  `https://developers.openai.com/codex/subagents` and
  `https://developers.openai.com/codex/guides/agents-md` in its Related
  Documents section. The pack recorded on 2026-08-10 that
  `developers.openai.com/codex` permanently redirects to `learn.chatgpt.com/docs`.
  This is an uncorrected stale reference in a governance owner, not in the pack.
- `infrastructure/k3d/k3d-cluster.yaml:5` pins `rancher/k3s:v1.35.0-k3s1` while
  upstream has shipped `v1.35.5`, `v1.35.6`, and a `v1.36.X` line.
  `REQ-WERPC-009` has no registered external source row, so this drift has no
  ledger home; it reinforces the pack's own 2026-08-12 note at
  `kubernetes-infrastructure-and-security.md:396`.
- The MCP revision jump to `2026-07-28` is broader than the Resources capability
  cited by `REQ-WERPC-021`. Any other owner still citing `2025-06-18` for tools,
  prompts, or authorization needs the same supersession note.
- Frontmatter `updated:` lags the newest dated body section in several pack
  files. This is the pack's stated convention rather than a contradiction, but it
  means `updated:` cannot be read as the latest observation date for any pack
  file without reading the body.
- The `Glob` tool does not traverse the `.claude/skills`, `.claude/workflows`, or
  `.claude/output-styles` symlinks, while `Read` resolves them correctly. An
  agent trusting `Glob` alone could wrongly conclude the shared assets are
  missing. This is a tool artifact, not workspace drift.
- A single-pass `WebFetch` summary inverted a documented precedence order during
  `WRFC-002`; a targeted re-fetch requesting verbatim text returned the correct
  order. Ordering and precedence claims should be confirmed with a verbatim
  re-fetch before adoption.
- `WRFC-004` executed without a shell tool, so checks requiring script execution
  were not run in that package, including
  `bash scripts/generate-llm-wiki-index.sh --check` and fresh repository-wide
  instance tallies. Those counts rest on `Glob` listings plus the pack's
  2026-08-14 tallies and were reported as not independently re-tallied.
- **Both of those limitations were subsequently closed with executed evidence**,
  after the cycle's content commits and before integration.
  `bash scripts/generate-llm-wiki-index.sh --check` returns
  `[PASS] LLM WIKI generated index is current`, so the freshness inferred from
  unchanged frontmatter dates was correct. A fresh frontmatter tally, taken on
  the cycle branch and adjusted for the one Spec, Plan, and Task this cycle adds,
  reproduces the pack's 2026-08-14 baseline exactly apart from one ordinary
  `active`-to-`done` transition per family: Spec 53 as 5 `draft` / 5 `active` /
  43 `done`, Task 71 as 5 / 1 / 65, and Plan 69 as 5 / 1 / 63, against the
  recorded 53 as 5 / 6 / 42, 71 as 5 / 2 / 64, and 69 as 5 / 2 / 62. Zero
  `archived` use in any of the three families still holds, so no pack claim is
  contradicted.
- **One reporting defect was found and did not reach the repository.** The
  `WRFC-004` package verbally reported nine AD, eighteen ADR, and ten Runbook
  dated instances. Direct enumeration returns eight, seventeen, and nine; each
  count was inflated by one because `README.md` was counted as a dated instance.
  Because `C-WRFC-002` required those tallies to be recorded as not re-verified
  rather than asserted, none of the three inflated numbers was ever written into
  the pack. Labelling an unverified count as unverified is what contained it.
## Completion Criteria

- All thirteen packages committed, one commit each.
- All thirteen `VAL-WRFC` criteria satisfied or explicitly recorded as not met.
- Full validation lane green and compared against the `WRFC-000` baseline.
- Branch integrated into `main` and the cycle branch removed.
- Durable progress ledger records the cycle, its evidence, and its handoff.
- No live, hosted, provider-runtime, remote, secret-value, push, publish, or
  deployment evidence claimed.

## Traceability

### Lifecycle Traceability

| Spec criterion                                                                    | Work package  | Expected Task                                                                                                                                 |
| --------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| [VAL-WRFC-001](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-001      | [WRFC-001](README.md#task-records) will record the thirty-six-row topic ledger derived from the pack   |
| [VAL-WRFC-002](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](README.md#task-records) will record separated external and workspace results per row   |
| [VAL-WRFC-003](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-007      | [WRFC-007](README.md#task-records) will record one blocking class per retained Partial or DEFER row    |
| [VAL-WRFC-004](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](README.md#task-records) will record ledger comparison and identifier uniqueness        |
| [VAL-WRFC-005](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](README.md#task-records) will record the unchanged pack inventory and heading-set check |
| [VAL-WRFC-006](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](README.md#task-records) will record every unreachable source as unreachable            |
| [VAL-WRFC-007](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-008      | [WRFC-008](README.md#task-records) will record scope re-derivation and the unowned-path re-test        |
| [VAL-WRFC-008](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-010      | [WRFC-010](README.md#task-records) will record cross-document agreement on all four counts             |
| [VAL-WRFC-009](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-010      | [WRFC-010](README.md#task-records) will record reconciliation as the last content commit               |
| [VAL-WRFC-010](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-009      | [WRFC-009](README.md#task-records) will record the graphify consumer enumeration and contract decision |
| [VAL-WRFC-011](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-010      | [WRFC-010](README.md#task-records) will record ledger byte size before and after                       |
| [VAL-WRFC-012](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-012      | [WRFC-012](README.md#task-records) will record full lane results compared against the baseline         |
| [VAL-WRFC-013](../../03.specs/0059-workspace-research-full-corpus-refresh/spec.md) | WRFC-000..012 | [WRFC-000..012](README.md#task-records) will record one commit per package and the terminal tree state |

### Related Documents

The owning Spec and the reciprocal Task already link reciprocally in the
`#### Lifecycle Traceability` table above, so they are recorded here as code
literals rather than duplicated links.

- Owning Spec: `docs/03.specs/0059-workspace-research-full-corpus-refresh/spec.md`
- Reciprocal Task:
  `docs/03.specs/0059-workspace-research-full-corpus-refresh/README.md#task-records`
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item                                                         | Result  | Evidence                                                                |
| ----------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------- |
| [VAL-WRFC-001](plan.md) | Done    | 36 rows derived from the pack; zero duplicates, zero gaps, union exact  |
| [VAL-WRFC-002](plan.md) | Done    | External and workspace results recorded separately for all 36 rows      |
| [VAL-WRFC-003](plan.md) | Done    | 24 retained rows each carry exactly one blocking class                  |
| [VAL-WRFC-004](plan.md) | Pending | Done                                                                    | 89 source IDs and 131 claim IDs unique and registered; none renumbered |
| [VAL-WRFC-005](plan.md) | Pending | Done                                                                    | Pack file count held at fourteen; every dated section added as H3 |
| [VAL-WRFC-006](plan.md) | Done    | Zero `unreachable` rows; two HTTP 403 hosts resolved by search fallback |
| [VAL-WRFC-007](plan.md) | Pending | Done                                                                    | Ten scopes re-derived; the five unowned canonical paths are unchanged |
| [VAL-WRFC-008](plan.md) | Pending | Done                                                                    | Four counts agree; the collection README was already accurate |
| [VAL-WRFC-009](plan.md) | Pending | Done                                                                    | Reconciliation was the last commit changing research pack content |
| [VAL-WRFC-010](plan.md) | Done    | Consumer enumeration recorded; contract corrected, no tracked deletion  |
| [VAL-WRFC-011](plan.md) | Pending | Done                                                                    | Ledger 816,508 to 841,164 bytes; unchanged after commit; under 1 MB |
| [VAL-WRFC-012](plan.md) | Pending | Done                                                                    | Eight lanes green plus clean diff checks; no regression against baseline |
| [VAL-WRFC-013](plan.md) | Pending | Partial                                                                 | One commit per logical unit; branch merged; one worktree removal blocked |

### Related Documents

The owning Spec and the reciprocal Plan already link reciprocally in the
`#### Lifecycle Traceability` table above and in `## Inputs`, so they are recorded
here as code literals rather than duplicated links.

- Owning Spec: `docs/03.specs/0059-workspace-research-full-corpus-refresh/spec.md`
- Reciprocal Plan:
  `docs/03.specs/0059-workspace-research-full-corpus-refresh/plan.md`
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Durable progress ledger](../../00.agent-governance/memory/progress.md)
