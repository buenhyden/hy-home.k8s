---
title: 'Workspace Engineering Research Pack Consolidation Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-09
artifact_id: "SPEC-0053-PLAN-0001"
---

# Workspace Engineering Research Pack Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development`; assign each WERPC task to a fresh
> worker, complete specification and quality review before advancing, and use
> checkbox (`- [ ]`) state in this Plan only as an execution checklist. The
> Task document is the durable result and evidence owner.

**Goal:** Publish one source-backed `0001-workspace-engineering` research pack that owns the
complete approved scope, preserves reviewed provenance from all 25 predecessor
files, migrates current consumers without weakening controls, and removes the
three predecessor directories.

**Architecture:** The work uses a fail-closed staged cutover. Research and
workspace evidence are synthesized into twelve focused references plus a pack
index and migration ledger before any current link or machine projection is
changed; deletion occurs only after exact coverage, source, ownership, and
reference gates pass. Repository-static, provider-runtime, hosted, remote, and
live evidence remain separate throughout.

**Tech Stack:** Markdown using the Stage 90 reference and snapshot-pack
profiles, official and primary web sources, Git object and tracked-file
plumbing, Python 3 standard-library checks, the existing reference-information
architecture validators, unittest fixtures, pre-commit when installed, and the
repository quality-gate shell entrypoint.

## Global Constraints

- The output root is exactly
  `docs/90.references/research/0001-workspace-engineering/`.
- The pack contains exactly one `README.md` and the twelve reference filenames
  declared by Spec 053.
- External source checks use the observation date `2026-08-08`; material
  external facts use official or primary URLs and a named refresh trigger.
- Local implementation status uses only `Implemented`, `Partial`, `Missing`,
  `Unverified`, or `Deferred`.
- Repository-static configuration and checks never establish provider
  discovery, authentication, model resolution, hosted execution, event
  delivery, remote state, or live platform readiness.
- All 25 predecessor files and split material sections require reviewed
  dispositions before deletion.
- Existing `docs/98.archive/**` records are immutable; no existing archive
  payload, digest, envelope, or link is rewritten.
- No compatibility README, redirect, copied predecessor pack, tracked scratch
  file, migration helper, or one-off artifact remains at handoff.
- No runtime agent role, provider model assignment, hook permission, workflow
  behavior, GitOps desired state, infrastructure manifest, or active policy is
  changed merely because the research recommends it.
- No live Kubernetes, Argo CD, Vault, ESO, cloud, provider-runtime, hosted-CI,
  remote, credential-bearing, secret-reading, push, merge, or publication
  action is authorized.
- Each WERPC task is one reviewable logical commit. The repository quality gate
  must pass before every commit.
- Durable implementation reports and review packages live in the SDD ledger;
  repository evidence is summarized in the Task document and progress ledger.

---

## Overview

This Plan executes the approved
[Spec 053](spec.md).
It replaces, validates, and removes the `2026-07-04-wer`, `2026-07-07-wer`, and
`2026-08-07-wer` live packs while preserving recoverability through Git history
and a file- and section-level migration ledger. The Plan does not reopen the
completed Spec 017 and does not create Stage 98 copies of the predecessor
packs.

The human approved the specification on 2026-08-08 and had already selected
subagent-driven execution. This Plan therefore hands off directly to
`superpowers:subagent-driven-development` after its own self-review and commit.

## Context

The execution branch base is the approved design commit
`37c714d04e1ab20816f2719fdc09f6dc42acef72`. The baseline has 25 tracked predecessor files: 8 under
`2026-07-04-wer`, 10 under `2026-07-07-wer`, and 7 under `2026-08-07-wer`.
Current mutable consumers include authored specifications, plans, tasks,
operations guidance, audit observations, reference indexes, machine contracts,
validators, and test fixtures.

Spec 052 and its active Plan/Task currently prescribe archiving only the
`2026-07-04-wer` pack. Spec 053 supersedes that unexecuted work item for the
three-pack replacement only: Spec 052 retains every other taxonomy work
package, while its WDTC-002/WORK-002 route becomes `Superseded` and points to
WERPC-008. PRD-0008 and AD-0011 receive a bounded exception note so two active
programs do not prescribe incompatible retention behavior.

[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
records the approved standalone relation between Spec 053 and this exact
Plan/Task pair. No separate PRD or AD is part of that lifecycle, and the
existing `programLineage` contract remains unchanged.

The project-local `deep-research` workflow applies. Exa and Firecrawl are not
callable in the current session, so workers use the available web-search and
page-open tools while preserving the same primary-source, full-page reading,
cross-reference, gap-labeling, and fact/inference separation rules. Broad
Codex facts use the `openai-docs` Codex manual helper first; remaining OpenAI
gaps use official OpenAI documentation only. Claude, Kubernetes, GitHub,
Diátaxis, security, and upstream project claims use their official or primary
owners.

### Legacy Task ledger inputs

This Task records execution and review evidence for the ten WERPC work
packages that replace three dated research packs with one source-backed
`0001-workspace-engineering` pack. Rows advance only after the logical commit, required
repository-static gates, implementation report, specification review, and
quality review are accepted.

External source observations are dated evidence, not live provider or platform
proof. No hosted CI, provider-runtime, remote, credential-bearing, secret-value,
or live-cluster result is produced or claimed.

- **Specification**:
  [Spec 053](spec.md)
- **Plan**:
  [Workspace Engineering Research Pack Consolidation Implementation Plan](plan.md)
- **Standalone execution decision**:
  [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Predecessor specification**: `Spec 017` at
  `docs/03.specs/0017-workspace-engineering-research-pack/spec.md`
- **Conflicting program**: `Spec 052` at
  `docs/03.specs/0052-document-taxonomy-consolidation/spec.md`
- **Approved requirement source**: direct 2026-08-08 human request and explicit
  Spec 053 approval in the current Codex task
- **Design commit**: `37c714d04e1ab20816f2719fdc09f6dc42acef72`
- **Execution branch base**: `37c714d04e1ab20816f2719fdc09f6dc42acef72`
## Goals & In-Scope

- Activate reciprocal Spec/Plan/Task lifecycle and resolve the Spec 052
  retention conflict.
- Create the exact thirteen-file pack shape and deterministic topic ownership.
- Build a 25-file plus split-section disposition ledger with Git provenance.
- Research every approved category against current official/primary sources
  and current repository evidence.
- Separate workspace fact, external fact, predecessor evidence, analysis, and
  recommendation in every material finding.
- Migrate mutable navigation, dated-observation annotations, indexes,
  contracts, validators, and fixtures to the surviving owner.
- Delete all three predecessor directories only after pre-deletion gates pass.
- Run focused, strict, archive, harness, full repository, residue, and
  independent review gates and close the lifecycle honestly.

## Non-Goals & Out-of-Scope

- Modifying existing Stage 98 records or using the archive as a replacement
  location for the three old packs.
- Rewriting Git history or dropping any user stash.
- Implementing recommendations in provider, GitOps, Kubernetes,
  infrastructure, CI, security, roster, model, or memory control surfaces.
- Claiming official support, runtime availability, authentication, hosted CI,
  deployment, remote, or live evidence from local files or validators.
- Installing research plugins or changing user/provider credentials.
- Pushing the branch, opening a pull request, merging, or deleting the branch
  without a separate finishing choice from the human.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WERPC-000 | Activate the approved execution path and reconcile the Spec 052 conflict | Design commit | Human approval of Spec 053 | Active reciprocal documents, superseded WDTC-002/WORK-002 route, green gates |
| WERPC-001 | Establish exact pack shape, requirement ownership, source inventory, and predecessor disposition baseline | WERPC-000 | 25 tracked predecessor files enumerated | Thirteen valid new files, unique request owners, 25/25 file rows, source commits |
| WERPC-002 | Research workspace governance, harness engineering, loop engineering, Claude, Codex, and the common environment | WERPC-001 | Pack contracts and source rules exist | Three reviewed references with provider-surface separation |
| WERPC-003 | Research spec-driven SDLC, document families, Diátaxis, and LLM-WIKI | WERPC-001 | Pack contracts and source rules exist | Three reviewed references with complete named-document coverage |
| WERPC-004 | Research Kubernetes, infrastructure, GitOps, and security | WERPC-001 | Pack contracts and source rules exist | One reviewed platform/security reference with evidence-depth matrix |
| WERPC-005 | Research CI/CD, GitHub Actions, and QA | WERPC-001 | Pack contracts and source rules exist | One reviewed delivery/QA reference with local workflow inventory |
| WERPC-006 | Research AI agents, pinned agency-agents, model routing, and memory tiers | WERPC-001 | Pack contracts and source rules exist | Three reviewed references with pinned upstream and provider-local boundaries |
| WERPC-007 | Migrate mutable links, dated observations, indexes, reference-IA contracts, validators, and fixtures | WERPC-002–006 | All target headings exist and research reviews pass | No dangling current link, all old-path occurrences classified, focused tests green |
| WERPC-008 | Prove cutover readiness and delete all three predecessor directories | WERPC-007 | 25/25 and split-section coverage; zero unclassified mutable references | Three exact absence checks, strict/archive/harness/full gates green |
| WERPC-009 | Reconcile indexes and evidence, run whole-branch review, clean residue, and close | WERPC-008 | All implementation commits and task reviews accepted | VAL-WER-001–012 evidence, terminal QA, no scratch, honest done state |

### File Structure

### New pack files

- `docs/90.references/research/0001-workspace-engineering/README.md` — pack boundary,
  evidence classes, reading order, request-to-primary-owner matrix, and current
  workspace evidence routing.
- `m0001-workspace-governance-and-common-agent-environment.md` — workspace purpose,
  common Claude/Codex governance, rules, environment, templates, scripts, and
  application route.
- `m0002-harness-and-loop-engineering.md` — harness elements and the
  Observe/Plan/Act/Verify/Learn loop, recovery, termination, evaluation, and
  workspace application controls.
- `m0003-provider-implementation-status.md` — Claude/Codex upstream product
  surfaces, local adapters, status, evidence depth, parity, and gaps.
- `m0004-spec-driven-sdlc-and-document-contracts.md` — spec-driven development,
  SDLC, and PRD/AD/ADR/guide/incident/postmortem/policy/release/runbook
  contracts.
- `m0005-documentation-architecture-and-diataxis.md` — Diátaxis modes and the
  workspace documentation architecture mapping.
- `m0006-llm-wiki-and-knowledge-routing.md` — deterministic knowledge routing,
  indexes, JIT retrieval, freshness, authority, and drift control.
- `m0007-kubernetes-infrastructure-and-security.md` — Kubernetes, infrastructure,
  GitOps, RBAC, NetworkPolicy, secrets, policy-as-code, supply chain, and
  security boundaries.
- `m0008-ci-cd-github-actions-and-qa.md` — CI/CD, GitHub Actions, formatting,
  linting, syntax, testing, promotion, rollback, and evidence lanes.
- `m0009-ai-agents-and-agency-agents.md` — agent-system design, pinned
  `msitarzewski/agency-agents`, roster comparison, and admission decisions.
- `m0010-agent-model-routing-and-configuration.md` — task-characteristic model and
  reasoning selection, evaluation, fallback, cost/latency, and promotion.
- `m0011-agent-memory-tiers-and-management.md` — working, durable, domain-scoped,
  and provider-local auxiliary memory lifecycle.
- `m0012-source-coverage.md` — source register, 25-file and
  split-section dispositions, mutable-reference classification, omissions,
  corrections, and cutover evidence.

### Lifecycle and navigation files

- Modify `docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md`
  and
  `docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md`
  with the approved three-pack exception and Spec 053 owner.
- Modify `docs/03.specs/0052-document-taxonomy-consolidation/spec.md`,
  `docs/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md`, and
  `docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records` so
  WDTC-002/WORK-002 is superseded without changing other Spec 052 work.
- Modify Spec 053, the Specs/Plans/Tasks indexes, and
  `docs/00.agent-governance/memory/progress.md` for reciprocal lifecycle and
  evidence.
- Modify `docs/90.references/research/README.md` and applicable parent/readme
  consumers to route to the new pack.

### Machine-contract and test surfaces

- Inspect and migrate
  `docs/90.references/data/reference-information-architecture.json`, its schema,
  `scripts/reference_information_architecture.py`,
  `tests/test_reference_information_architecture.py`, and the four
  `tests/fixtures/reference-information-architecture/*.json` fixtures named by
  the old-path inventory.
- Inspect and migrate
  `docs/00.agent-governance/contracts/agent-legacy-cutover.json`,
  `scripts/validate-agent-legacy-cutover.py`,
  `tests/test_validate_agent_legacy_cutover.py`, and
  `tests/fixtures/agent-legacy-cutover.json`; preserve source-commit-pinned
  historical entries, but remove current-authority dependence on deleted files.
- Inspect and migrate current-pack/readme/affected-lane fixtures in
  `scripts/validate-document-contract-registry.py`,
  `scripts/validate-links-and-owners.py`,
  `tests/fixtures/document-contracts/readme-profile-cases.json`,
  `tests/fixtures/links-and-owners.json`, and
  `tests/fixtures/validation-surfaces.json`.
- Inspect active-corpus ledgers and validators that name predecessor paths;
  update generated owners and focused tests together or record a dated,
  source-commit-bound no-change disposition. Do not hand-edit generated data
  without its canonical producer.

### Deleted files

- Delete exactly the 25 tracked files under:
  `docs/90.references/research/2026-07-04-wer/`,
  `docs/90.references/research/2026-07-07-wer/`, and
  `docs/90.references/research/2026-08-07-wer/` in WERPC-008.

### Interfaces

The README coverage table produces this Markdown interface for all research
tasks:

```text
Request ID | Requested topic | Primary owner | Workspace evidence |
External source class | Status
```

The source and migration ledger produces these interfaces for WERPC-007 and
WERPC-008:

```text
Source ID | Owner topic | URL | Source class | Checked on | Adopted scope |
Rejected scope | Refresh trigger

Old path | Source commit | Topic or heading | Verification | New owner |
Disposition | Reason and evidence

Occurrence path | Occurrence class | Action | Current owner | Evidence
```

Every topic reference uses these exact material-finding fields:

```text
Claim class | Status | Workspace evidence | External source IDs | Analysis |
Canonical follow-up owner | Refresh trigger
```

### Task Details

### Task 1: WERPC-000 — activate lifecycle and reconcile the conflicting route

**Files:**

- Create: this Plan and
  `docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records`
- Modify: Spec 053, PRD-0008, AD-0011, Spec 052, the Spec 052 Plan/Task,
  `docs/03.specs/README.md`, `docs/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md`,
  `docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records`, and the progress ledger

**Interfaces:**

- Consumes: approved Spec 053 and completed design commit `37c714d0`.
- Produces: active WERPC lifecycle, WERPC task IDs, and the single owner for
  replacing WDTC-002/WORK-002.

- [x] **Step 1: Record the bounded supersession rule**

  In PRD-0008 and AD-0011, state that the direct 2026-08-08 human approval and
  Spec 053 replace only the three-pack retention route; every unrelated
  taxonomy requirement and architecture decision remains active.

- [x] **Step 2: Supersede the unexecuted Spec 052 package**

  Change Spec 052 asset R-3 and Plan package WDTC-002 from archive execution to
  a cross-program supersession record. Change Task WORK-002 to `Superseded`,
  with result text naming Spec 053 and WERPC-008. Do not mark it `Done` and do
  not touch WORK-001 or WORK-003 through WORK-015.

- [x] **Step 3: Activate reciprocal lifecycle**

  Set Spec 053, this Plan, and its Task to `active`; add reciprocal relative
  links and update the three collection indexes with the same status and date.

- [x] **Step 4: Run focused lifecycle checks**

  Run:

  ```bash
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Expected: all commands exit 0, and the strict link result reports no broken
  reciprocal target.

- [x] **Step 5: Run the full gate and commit**

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  git add docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md \
    docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md \
    docs/03.specs/0052-document-taxonomy-consolidation/spec.md \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/spec.md \
    docs/03.specs/README.md docs/03.specs/plans docs/03.specs/tasks \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: activate research pack consolidation"
  ```

  Expected: quality gate PASS and one commit containing only lifecycle,
  execution, conflict, index, and progress files.

### Task 2: WERPC-001 — establish pack, coverage, source, and migration contracts

**Files:**

- Create: all thirteen files listed under **New pack files**
- Modify: WERPC Task and progress ledger

**Interfaces:**

- Consumes: WERPC lifecycle and the exact 25-file tracked baseline.
- Produces: request IDs `REQ-WERPC-001` through `REQ-WERPC-032`, one primary
  owner per row, source IDs, the 25-file disposition baseline, and stable
  headings used by every later task.

- [ ] **Step 1: Capture the tracked predecessor baseline**

  Run and retain the output in the migration ledger:

  ```bash
  git ls-files \
    'docs/90.references/research/2026-07-04-wer/**' \
    'docs/90.references/research/2026-07-07-wer/**' \
    'docs/90.references/research/2026-08-07-wer/**'
  ```

  Expected: exactly 25 paths, split 8/10/7 by directory. For each path, obtain
  the last content-bearing commit with `git log -1 --format=%H -- <path>` and
  record that full 40-character object name in the file-level row.

- [ ] **Step 2: Create profile-complete pack files**

  Create README from the snapshot-pack README profile and each non-README file
  from `reference.template.md`. Use the exact required H2 headings plus focused
  analysis headings; do not insert author prompts, empty sections, or future
  content markers. Initial unsupported implementation rows use `Unverified`,
  never a guessed positive status.

- [ ] **Step 3: Populate the coverage matrix**

  Add one row for each separately named request: harness, loop, workspace
  application, Claude, Codex, common system, spec-driven development,
  Kubernetes, infrastructure, SDLC, PRD, AD, ADR, guide, incident,
  postmortem, policy, release, runbook, Diátaxis, LLM-WIKI, CI/CD, GitHub
  Actions, QA, security, AI-agent systems, agency-agents, model routing, and
  short/long/domain memory. Where one request contains multiple named document
  families, allocate separate rows so uniqueness is mechanically reviewable.

- [ ] **Step 4: Populate file- and section-level migration rows**

  Add all 25 exact old paths. Read every old H2/H3 inventory with:

  ```bash
  rg -n '^#{2,3} ' \
    docs/90.references/research/2026-07-04-wer \
    docs/90.references/research/2026-07-07-wer \
    docs/90.references/research/2026-08-07-wer
  ```

  Add split-section rows whenever one old file maps to more than one new
  reference. Every correction or omission includes the supporting source or
  duplicate owner.

- [ ] **Step 5: Run deterministic structure and coverage checks**

  Run:

  ```bash
  test "$(find docs/90.references/research/0001-workspace-engineering -maxdepth 1 -type f | wc -l)" -eq 13
  test "$(git ls-files 'docs/90.references/research/2026-07-04-wer/**' 'docs/90.references/research/2026-07-07-wer/**' 'docs/90.references/research/2026-08-07-wer/**' | wc -l)" -eq 25
  python3 scripts/validate-markdown-profiles.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  git diff --check
  ```

  Expected: exact counts and all validators exit 0.

- [ ] **Step 6: Run full QA, record evidence, and commit**

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  git add docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: establish consolidated research pack"
  ```

### Task 3: WERPC-002 — research governance, harness, loop, and providers

**Files:**

- Modify: `m0001-workspace-governance-and-common-agent-environment.md`,
  `m0002-harness-and-loop-engineering.md`, `m0003-provider-implementation-status.md`, the
  source/migration ledger, WERPC Task, and progress ledger

**Interfaces:**

- Consumes: request owner rows and source-record schema from WERPC-001.
- Produces: current common-environment model, harness/loop model, provider
  comparison, source IDs, workspace status rows, and recommendations routed to
  canonical owners.

- [ ] **Step 1: Inventory current workspace evidence**

  Inspect `AGENTS.md`, `CLAUDE.md`, `.codex/**`, `.claude/**`, `.agents/**`,
  `docs/00.agent-governance/**`, relevant hooks, templates, validation
  contracts, and scripts. Record exact tracked paths and distinguish static
  adapter presence from native discovery or runtime use.

- [ ] **Step 2: Fetch current Codex primary evidence**

  Run the OpenAI Docs Codex manual helper from the installed skill directory,
  read the generated outline, and deep-read only the sections for AGENTS.md,
  config, hooks, skills, plugins, MCP, multi-agent behavior, sandbox, and
  product surfaces. Use official OpenAI-domain fallback only for a material gap
  not resolved by the manual.

- [ ] **Step 3: Fetch Claude and engineering primary evidence**

  Search and open official Anthropic Claude Code documentation for memory,
  settings, hooks, subagents, skills, MCP, permissions, and model/config
  boundaries. For harness and loop concepts, use original evaluation,
  observability, software feedback-loop, or standards sources rather than
  comparison blogs.

- [ ] **Step 4: Write the three analyses**

  Use explicit tables for upstream surface, local owner, evidence depth,
  five-state status, gap, and recommended owner. Keep Claude Code, Claude API,
  Codex CLI, Codex app/cloud, OpenAI API model catalogs, tracked adapters, and
  authenticated runtime resolution as separate rows.

- [ ] **Step 5: Cross-check material claims**

  Every material external fact has a source ID, exact URL, checked date
  `2026-08-08`, and refresh trigger. A claim supported by only one source is
  marked as single-source or `Unverified`; analysis and recommendation are
  labeled rather than written as facts.

- [ ] **Step 6: Validate and commit**

  ```bash
  python3 scripts/validate-markdown-profiles.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git add docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: research harness loop and provider systems"
  ```

### Task 4: WERPC-003 — research spec-driven SDLC, documents, Diátaxis, and LLM-WIKI

**Files:**

- Modify: `m0004-spec-driven-sdlc-and-document-contracts.md`,
  `m0005-documentation-architecture-and-diataxis.md`,
  `m0006-llm-wiki-and-knowledge-routing.md`, the source/migration ledger, WERPC Task,
  and progress ledger

**Interfaces:**

- Consumes: repository document profiles/templates and WERPC-001 source schema.
- Produces: exact role/trigger/input/output/lifecycle/evidence rules for all
  named documents, Diátaxis mapping, and LLM knowledge-routing design.

- [ ] **Step 1: Inventory canonical document and wiki owners**

  Inspect stages 01 through 05, `docs/99.templates/**`, document contracts and
  validators, `docs/90.references/llm-wiki/**`, its generator, and current
  generated index. Record current implementation and gaps without copying
  active policy into Stage 90.

- [ ] **Step 2: Read primary external sources**

  Deep-read Diátaxis at `https://diataxis.fr/`, authoritative spec-driven or
  requirements/architecture decision sources, GitHub documentation guidance,
  and primary incident/postmortem/runbook sources. Map only concepts supported
  by the source; label the workspace mapping as analysis.

- [ ] **Step 3: Write the document-family contract matrix**

  Give PRD, AD, ADR, Spec, Plan, Task, guide, incident, postmortem, policy,
  release, and runbook separate rows with purpose, trigger, required inputs,
  required outputs, owner, lifecycle, evidence depth, cross-links, anti-pattern,
  and repository status.

- [ ] **Step 4: Write Diátaxis and LLM-WIKI analyses**

  Separate tutorial, how-to, reference, and explanation. Describe deterministic
  indexes, canonical authority routing, just-in-time retrieval, freshness,
  invalidation, generated-output checking, and drift handling for LLM-WIKI.

- [ ] **Step 5: Update source and migration dispositions**

  Map every applicable predecessor section to one surviving heading. Record
  stale or duplicate omissions with a specific source or selected primary
  owner.

- [ ] **Step 6: Validate and commit**

  ```bash
  python3 scripts/validate-markdown-profiles.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git add docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: research spec driven documentation systems"
  ```

### Task 5: WERPC-004 — research Kubernetes, infrastructure, and security

**Files:**

- Modify: `m0007-kubernetes-infrastructure-and-security.md`, the source/migration
  ledger, WERPC Task, and progress ledger

**Interfaces:**

- Consumes: platform request rows and current GitOps/security evidence.
- Produces: layered platform model, threat/control matrix, evidence-depth
  status, and follow-up owners.

- [ ] **Step 1: Inventory current platform evidence read-only**

  Inspect `gitops/**`, `infrastructure/**`, `traefik/**`, `policy/**`, relevant
  workflows, platform contracts, validators, operations owners, and version
  inventories. Do not read ignored credentials, kubeconfig, secret values, or
  contact a live endpoint.

- [ ] **Step 2: Read official platform and security sources**

  Use official Kubernetes, Argo CD/GitOps, External Secrets, Vault, OPA,
  NetworkPolicy/RBAC, NIST, CISA/NSA, SLSA, and applicable supply-chain
  documentation. Record product/version scope and checked date.

- [ ] **Step 3: Write the layered analysis**

  Separate repository desired state, rendering/schema checks, policy checks,
  remote GitOps reconciliation, live workload state, secret backend state, and
  cloud/provider state. For each control, record threat, preventive/detective
  role, local evidence, status, deeper evidence needed, and owner.

- [ ] **Step 4: Reconcile predecessor material**

  Integrate current Kubernetes/infrastructure/security findings from all old
  owners; correct version- or implementation-sensitive claims and record every
  disposition.

- [ ] **Step 5: Validate and commit**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git add docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: research kubernetes infrastructure security"
  ```

### Task 6: WERPC-005 — research CI/CD, GitHub Actions, and QA

**Files:**

- Modify: `m0008-ci-cd-github-actions-and-qa.md`, the source/migration ledger, WERPC
  Task, and progress ledger

**Interfaces:**

- Consumes: current workflow, hook, formatter, linter, test, validation, and
  release evidence.
- Produces: local/hosted lane map, job/control inventory, QA taxonomy, security
  rules, and follow-up owners.

- [ ] **Step 1: Inventory repository delivery controls**

  Inspect `.github/workflows/**`, workflow contracts, pre-commit, formatting,
  lint, syntax, tests, affected routing, aggregate gates, release documents,
  and rollback owners. Distinguish declared workflows from observed hosted
  runs.

- [ ] **Step 2: Read official GitHub and delivery sources**

  Deep-read GitHub Actions syntax, security hardening, permissions, reusable
  workflow, artifact/attestation, dependency pinning, environments, and OIDC
  documentation plus primary CI/CD and supply-chain sources.

- [ ] **Step 3: Write CI/CD and QA matrices**

  Map trigger, job, dependency, tool, failure semantics, evidence depth,
  promotion, rollback, concurrency, least privilege, cache/artifact trust, and
  status. Give formatting, linting, syntax, unit, integration, render/schema,
  policy, security, browser/end-to-end, and live validation separate rows.

- [ ] **Step 4: Reconcile predecessor material and sources**

  Integrate both automation/QA predecessor files and the 2026-08-07 GitHub
  Actions reference, correcting current workflow and evidence claims from the
  repository.

- [ ] **Step 5: Validate and commit**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git add docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: research ci github actions and qa"
  ```

### Task 7: WERPC-006 — research agents, agency-agents, model routing, and memory

**Files:**

- Modify: `m0009-ai-agents-and-agency-agents.md`,
  `m0010-agent-model-routing-and-configuration.md`,
  `m0011-agent-memory-tiers-and-management.md`, the source/migration ledger, WERPC
  Task, and progress ledger

**Interfaces:**

- Consumes: current roster/model/memory contracts and WERPC source schema.
- Produces: pinned upstream comparison, Adopt/Adapt/Skip decisions, model
  routing system, memory lifecycle system, and canonical follow-up owners.

- [ ] **Step 1: Inventory local agent, model, and memory owners**

  Inspect the harness catalog, agent roster and schemas, provider role files,
  model policy, evaluation/admission contracts, memory rules, progress/current
  memory, and relevant validators. Separate tracked desired configuration from
  native discovery and runtime use.

- [ ] **Step 2: Pin and inspect agency-agents**

  Resolve the current default-branch commit of
  `https://github.com/msitarzewski/agency-agents`, record the 40-character
  commit and retrieval date, and inspect the repository at that object. Base
  roster claims on that pin, not an unpinned branch rendering.

- [ ] **Step 3: Read provider-primary model and memory sources**

  Use the OpenAI manual/official docs route for Codex and model surfaces and
  official Anthropic documentation for Claude settings, models, subagents,
  and memory. Do not infer availability on one product surface from another.

- [ ] **Step 4: Write agent and agency analysis**

  Compare responsibilities, inputs, outputs, tools, risk, verification, and
  gaps. For each upstream role family, record `Adopt`, `Adapt`, or `Skip`, the
  local owner, rationale, admission evidence, and duplication risk.

- [ ] **Step 5: Write model and memory analyses**

  Define routing by task risk, complexity, context, modality, tool use,
  latency, cost, reasoning effort, fallback, eval, canary, promotion, and
  rollback. Define working/short-term, durable/long-term, domain-scoped, and
  provider-local auxiliary memory by authority, content, write gate,
  retrieval, freshness, invalidation, retention, privacy, and deletion.

- [ ] **Step 6: Validate and commit**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git add docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: research agent model and memory systems"
  ```

### Task 8: WERPC-007 — migrate links, observations, contracts, validators, and fixtures

**Files:**

- Modify: every current navigational, dated-observation, index, contract,
  validator, and fixture owner classified in the migration ledger
- Test: `tests/test_reference_information_architecture.py`,
  `tests/test_validate_agent_legacy_cutover.py`, and focused validator suites

**Interfaces:**

- Consumes: stable new headings, source ledger, and occurrence-classification
  rows.
- Produces: surviving links, source-commit-bound historical exceptions,
  current machine projections, and zero unclassified mutable old-path
  occurrences.

- [ ] **Step 1: Capture the complete current occurrence inventory**

  Run this repository-wide tracked search and record every path in the ledger:

  ```bash
  git grep -n -E '2026-07-04-wer|2026-07-07-wer|2026-08-07-wer' -- . \
    ':!docs/98.archive/**' \
    ':!docs/90.references/research/2026-07-04-wer/**' \
    ':!docs/90.references/research/2026-07-07-wer/**' \
    ':!docs/90.references/research/2026-08-07-wer/**'
  ```

  Classify each occurrence as current navigation, dated observation,
  machine-owned projection, source-commit-pinned historical evidence, Spec 053
  cutover provenance, or stale invalid reference.

- [ ] **Step 2: Write failing focused fixtures before machine changes**

  Update test inputs to expect `0001-workspace-engineering` as the surviving research
  owner and to reject current navigation to the three deleted pack roots. Run:

  ```bash
  python3 -m unittest tests.test_reference_information_architecture -v
  python3 -m unittest tests.test_validate_agent_legacy_cutover -v
  ```

  Expected RED: assertions still resolve current paths or counts through a
  predecessor owner. Save the rule IDs and failure summaries in the SDD
  implementation report.

- [ ] **Step 3: Migrate human-readable current links**

  Rewrite navigational links to the exact new primary owner and heading. For a
  dated mutable observation, preserve the observed path as text only when its
  historical meaning requires it and add an adjacent current-lookup link. Do
  not edit Stage 98. Update the research index tree and tables to contain only
  the new live pack.

- [ ] **Step 4: Migrate machine contracts with their producers**

  Update reference-IA, agent cutover, current-pack/readme, affected-lane, and
  active-corpus projections together with schemas, constants, producers, and
  fixtures. Keep pinned `sourceCommit` evidence when it deliberately addresses
  a historical Git tree. Do not remove a rule or relax negative coverage to
  accommodate deletion.

- [ ] **Step 5: Run focused GREEN checks**

  ```bash
  python3 -m unittest tests.test_reference_information_architecture -v
  python3 -m unittest tests.test_validate_agent_legacy_cutover -v
  python3 scripts/validate-reference-information-architecture.py --root .
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  ```

  Expected: all commands exit 0; negative fixtures still fail for their named
  invalid mutation, while production validation passes.

- [ ] **Step 6: Prove occurrence closure before deletion**

  Re-run the Step 1 search. Every remaining hit must be one of: Spec 053/this
  Plan/Task cutover provenance, the new migration ledger, an explicitly
  annotated dated observation, a synthetic negative fixture, or pinned
  source-commit evidence. The ledger must have one reviewed classification and
  owner for every remaining hit; any unclassified hit blocks WERPC-008.

- [ ] **Step 7: Run full QA and commit**

  ```bash
  python3 scripts/archive_validation.py --root .
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check
  git add docs scripts tests
  git commit -m "docs: migrate research pack consumers"
  ```

  Expected: no change under `docs/98.archive/**` and one control-preserving
  migration commit.

### Task 9: WERPC-008 — delete predecessor packs after fail-closed readiness

**Files:**

- Delete: the exact 25 predecessor files
- Modify: source/migration ledger, WERPC Task, and progress ledger

**Interfaces:**

- Consumes: reviewed 25/25 file coverage, split-section dispositions, source
  ledger, and occurrence classification.
- Produces: one live `0001-workspace-engineering` pack and three absent predecessor roots.

- [x] **Step 1: Re-run pre-deletion gates**

  ```bash
  test "$(git ls-files 'docs/90.references/research/2026-07-04-wer/**' 'docs/90.references/research/2026-07-07-wer/**' 'docs/90.references/research/2026-08-07-wer/**' | wc -l)" -eq 25
  python3 scripts/validate-reference-information-architecture.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/archive_validation.py --root .
  ```

  Expected: exact baseline count and all validators exit 0. Stop without
  deletion if any migration row, section disposition, source, or occurrence
  classification is incomplete.

- [x] **Step 2: Delete only the enumerated predecessor files**

  Use `apply_patch` to delete the 25 files from the tracked baseline. Do not
  issue recursive filesystem deletion and do not create redirects.

- [x] **Step 3: Prove exact absence and pack shape**

  ```bash
  test ! -e docs/90.references/research/2026-07-04-wer
  test ! -e docs/90.references/research/2026-07-07-wer
  test ! -e docs/90.references/research/2026-08-07-wer
  test "$(find docs/90.references/research/0001-workspace-engineering -maxdepth 1 -type f | wc -l)" -eq 13
  ```

- [x] **Step 4: Run post-deletion validation**

  ```bash
  git diff --check
  python3 scripts/validate-reference-information-architecture.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/archive_validation.py --root .
  bash scripts/validate-harness.sh
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: all commands exit 0. If a command fails, restore only the deletion
  unit before commit, correct the missing migration, and repeat; never weaken a
  gate.

- [x] **Step 5: Record deletion evidence and commit**

  ```bash
  git add docs/90.references/research \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records \
    docs/00.agent-governance/memory/progress.md
  git commit -m "docs: retire predecessor research packs"
  ```

### Task 10: WERPC-009 — final audit, review, cleanup, and lifecycle closure

**Files:**

- Modify: new pack README/ledger as evidence requires, Spec 053, this Plan,
  WERPC Task, Specs/Plans/Tasks/research indexes, and progress ledger
- Inspect: complete branch diff and all tracked/untracked residue

**Interfaces:**

- Consumes: all WERPC implementation commits and accepted per-task review
  packages.
- Produces: VAL-WER-001 through VAL-WER-012 evidence, terminal lifecycle, and
  a clean branch ready for the finishing skill.

- [x] **Step 1: Run criterion-by-criterion deterministic checks**

  Verify exact 13-file shape, unique request ownership, 25/25 plus split-section
  disposition coverage, source-date/refresh-trigger coverage, five-state
  vocabulary, provider-surface separation, all topic families, migrated
  consumers, three absent roots, zero Stage 98 diff, logical commit inventory,
  and SDD review packages. Record results against VAL-WER-001 through
  VAL-WER-012 in the Task.

- [x] **Step 2: Run optional and required QA with honest outcomes**

  ```bash
  git diff --check
  python3 scripts/validate-reference-information-architecture.py --root .
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/archive_validation.py --root .
  bash scripts/validate-harness.sh
  pre-commit run --all-files
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: required commands PASS. If pre-commit is unavailable, record
  `SKIP` and the exact fallback lanes; do not record it as PASS.

- [x] **Step 3: Run whole-branch specification review**

  Dispatch a fresh strongest-available reviewer over the complete branch diff,
  Spec 053, this Plan, the task evidence, and the SDD ledger. Fix every Critical
  or Important finding through the bounded SDD fix loop and re-run affected
  gates.

- [x] **Step 4: Scan for residue and evidence overclaims**

  ```bash
  git status --short
  git diff --name-only $(git merge-base HEAD main)..HEAD -- docs/98.archive
  git ls-files | rg '(^|/)(tmp|temp|scratch|draft-output)(/|$)|\.bak$|\.orig$'
  rg -n 'hosted.*PASS|provider-runtime.*PASS|live.*PASS|remote.*PASS' \
    docs/90.references/research/0001-workspace-engineering \
    docs/03.specs/0053-workspace-engineering-research-pack-consolidation/README.md#task-records
  ```

  Expected: no archive-path diff, no task-created residue, and no unsupported
  evidence-depth PASS claim. Existing unrelated residue is reported, not
  deleted.

- [x] **Step 5: Close reciprocal lifecycle and commit**

  Set Spec 053, this Plan, and its Task to `done`; update collection indexes,
  WERPC evidence rows, source/migration cutover evidence, and progress. Run the
  full quality gate once more and commit:

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  git add docs
  git commit -m "docs: close research pack consolidation"
  ```

- [x] **Step 6: Hand off to branch finishing**

  Invoke `superpowers:finishing-a-development-branch`. Do not push, merge,
  create a PR, or remove the worktree until the human selects a finishing
  option.

## Verification Plan

| Work package | Deterministic check | Evidence lane |
| --- | --- | --- |
| WERPC-000 | strict document registry, links/owners, diff, full gate | repository-static |
| WERPC-001 | exact 13/25 counts, profile, link, full gate | repository-static |
| WERPC-002 | source/claim review, provider separation, harness and full gates | repository-static + dated external observation |
| WERPC-003 | document-family coverage, LLM-WIKI check, profiles, links, full gate | repository-static + dated external observation |
| WERPC-004 | platform evidence-depth review, links, harness, full gate | repository-static + dated external observation |
| WERPC-005 | workflow/QA inventory, links, full gate | repository-static + dated external observation |
| WERPC-006 | pinned upstream commit, provider source review, links, harness, full gate | repository-static + dated external observation |
| WERPC-007 | focused RED/GREEN tests, reference-IA, registry, links, archive, full gate | repository-static |
| WERPC-008 | readiness gates, exact absence, strict/archive/harness/full gates | repository-static |
| WERPC-009 | VAL-WER walk, whole-branch review, full QA, residue and archive diff | repository-static |

No command in this Plan proves provider-runtime, hosted-CI, remote, credential,
secret-value, or live-platform state. Those lanes remain `Deferred` or
`Unverified` and are never converted to PASS by inference.

### Legacy Task verification evidence

The specification and design commit are approved. WERPC-000 is done:
`python3 scripts/validate-document-contract-registry.py --root . --mode strict`,
`python3 scripts/validate-links-and-owners.py --root . --mode strict`,
`git diff --check`, and `bash scripts/validate-repo-quality-gates.sh .` passed
on the final pre-commit tree. The optional `pre-commit run --all-files` attempt
was interrupted after it stalled and rewrote only detect-secrets metadata in
`.secrets.baseline`; that incidental change was restored exactly and the
optional lane is `SKIP`, not `PASS`. The passing required strict, diff, and full
repository gate results are the fallback evidence. The results are
repository-static only; provider-runtime, hosted CI, remote, and live
validation remain `DEFER`.
WERPC-001 is done with the thirteen-file shape, request-owner matrix, dated
predecessor source-register interface, 25 full-hash file dispositions, and 35
text-exact H3 split rows. It does not claim external currentness: later topical
work must recheck predecessor URLs. Its strict registry, strict links/owners,
and full repository quality-gate results are repository-static only.
WERPC-000A implements the approved typed standalone-execution contract without
changing `programLineage`. Registry, links/owners, eligibility, residue closure,
the affected unit tests, Markdown profiles, cached diff, and the complete
repository quality gate passed on the final reviewed staged tree.
WERPC-002 is done: its source ledger has official, dated primary sources with
refresh triggers and claim boundaries; the topical references retain `DEFER`
for native discovery, authenticated/runtime, hosted CI, remote, and live
claims. The collection-index and README-inventory REDs were closed without
changing the immutable baseline, and both fresh reviews plus the final staged
Reference IA and complete repository quality gate passed. The attempted
Reference IA `--staged` variant is recorded as an inapplicable-mode `SKIP`; the
Plan's production `--root .` command passed. WERPC-003 is done: its nine dated
source rows and thirteen bounded claim rows support the complete document-family
matrix, Release absence gap, Diátaxis mapping, and LLM-WIKI boundary. Fresh
review returned Approved with no finding, and Reference IA production plus the
complete repository quality gate passed on the exact staged tree. WERPC-004 is
done: its 12 dated source rows and 11 bounded claims cover the
platform hierarchy, GitOps/secret trust boundaries, static-versus-runtime
controls, and As-Is/gap/target matrix. Focused checks passed, fresh content
review was Approved with no finding, and Reference IA production plus the
complete repository quality gate passed on the exact staged tree. All
remote/live/secret evidence remains `DEFER`.
WERPC-005 is done: its dated source/claim registers and current workflow/QA
analysis passed focused validation, fresh review returned Approved with no
finding, and Reference IA production plus the complete repository quality gate
passed on the exact staged tree. It does not promote repository-static workflow
evidence to hosted CI, administration, credential, artifact, OIDC, deployment,
remote, or live evidence. WERPC-006 is done: its exact Agency Agents pin, eight
dated sources, and eight bounded claims distinguish role/model/memory static
contracts from provider/runtime behavior. Focused checks passed, fresh review
was Approved, the upstream-script-path RED was corrected, and Reference IA plus
the complete repository gate passed on the exact staged tree. WERPC-007 is
implemented and ready for fresh review: its exact tracked occurrence inventory
is 732 lines across 70 files, every hit has one reviewed classification row,
and focused RIA, agent-cutover, active-corpus, registry, link, archive, compile,
and diff validations pass. RIA production was first proven in an isolated
clone. A migration reviewer later staged the exact 53-file scope while proving
index authority; cached scope/diff checks and the actual staged RIA 88/88 plus
direct validator pass, with no forbidden diff. Its unrequested harness and
full-gate starts were interrupted with exit 130 and are not PASS evidence. The
pre-review harness attempt exposed and led to restoration of the
three phase-bounded README fixture rows; its focused registry self-test now
passes. Fresh review then found and closed the production disposition-header
and inherited Git-configuration defects; an exact-delete clone passes strict
links, and Python plus QA re-review are Approved. The controller then audited
and replaced an over-broad 25-file currentness exception with the reviewed
exact disposition parser and a single predecessor-ledger exception, refreshed
the exact active-corpus closure identities, and reran both the complete
repository quality gate and full harness successfully. WERPC-007 is done.
WERPC-008 is done: all 25 enumerated predecessor files and the three empty
directories are absent, the new pack remains exactly 13 files, all 25
dispositions are completed, and post-deletion README, RIA, and agent-cutover
contracts pass the required repository-static gates. WERPC-009 closes the
reciprocal lifecycle: deterministic audit confirmed exact 13 pack files, 32
unique request-owner rows, 52 source rows, 51 bounded claim rows, 25 completed
file dispositions, 35 split dispositions, three absent predecessor roots, zero
Stage 98 branch diff, no tracked temporary/scratch residue, no unsupported
deep-evidence success claim, and 11 logical pre-closure
implementation commits. The post-deletion occurrence table exactly matches 732
lines across 66 files. Required repository-static validation passed with
strict links/owners, Reference IA, archive validation, harness, and the complete
repository quality gate. The first terminal harness run exposed
`CLOSURE-AUTHORITY-SCOPE` for newly done Spec 053; an exact-set unit test
reproduced the missing post-closure authority, and the bounded one-path registry
addition made the targeted test, closure self-test, production closure check,
and full harness pass without accepting any unknown Spec. The optional
all-files pre-commit run passed its early
hooks but was interrupted at the long-running strict repository-quality hook;
it is `SKIP`, not `PASS`, and made no worktree change. Push, merge, PR creation,
worktree removal, hosted CI, provider-runtime, remote, credential, secret, and
live validation remain outside the approved scope.

### Terminal Acceptance Matrix

| Criterion | Result | Deterministic terminal evidence |
| --- | --- | --- |
| VAL-WER-001 | PASS | The tracked successor pack contains exactly 13 files: one README and twelve declared references. |
| VAL-WER-002 | PASS | The README contains 32 sequential, unique request rows; every row has one linked primary owner and one nonempty workspace-evidence cell. |
| VAL-WER-003 | PASS | The ledger contains 25 unique file dispositions with full 40-hex source commits and 35 reviewed section-split rows. |
| VAL-WER-004 | PASS | The source register has 52 rows; SRC-WERPC-004–052 are 49 current rows with URLs, 2026-08-08 checks, adopted/rejected scopes, and refresh triggers; all twelve references expose Sources and Review and Freshness sections. |
| VAL-WER-005 | PASS | The 32 requirement states and 51 claim rows use only the five-state vocabulary and retain repository evidence plus uncertainty boundaries. |
| VAL-WER-006 | PASS | Provider and common-environment references keep Claude, Codex, shared static controls, native discovery, authentication, and runtime evidence as separate surfaces. |
| VAL-WER-007 | PASS | The 32-owner matrix covers every requested harness, loop, SDLC/document, documentation, platform, delivery, security, agent, model, and memory topic. |
| VAL-WER-008 | PASS | Current navigation and machine consumers route to the successor; strict links/owners and RIA pass; every remaining predecessor-token line is classified by an exact 732-line/66-file table. |
| VAL-WER-009 | PASS | All 25 predecessor files and all three roots are absent; the successor remains exactly 13 files; residue scan found no task-created scratch artifact. |
| VAL-WER-010 | PASS | The branch diff contains zero `docs/98.archive/**` path changes and archive validation passes. |
| VAL-WER-011 | PASS | Eleven logical commits before closure, eleven work-package SDD reports, and one bounded WERPC-002 fix report preserve per-unit evidence and review history. |
| VAL-WER-012 | PASS | Fresh whole-branch review is Approved and required Reference IA, strict links, archive, harness, diff, and complete repository-static quality gates pass; deeper evidence remains DEFER. |

## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A predecessor section is lost during consolidation | 25-file and split-section ledger blocks deletion until every row has a reviewed disposition | WERPC-001 reviewer |
| External documentation changed after the old packs | Re-open official/primary pages, date every source 2026-08-08, and mark unsupported claims Unverified | Topic researcher |
| Claude/Codex product surfaces are collapsed | Separate API, CLI/app/cloud, tracked adapter, discovery, auth, model resolution, and hosted/runtime rows | WERPC-002 reviewer |
| Historical evidence is falsified by link rewriting | Preserve dated text, add a current lookup, and keep source-commit-pinned evidence unchanged | WERPC-007 reviewer |
| A validator passes only because coverage was removed | Write negative fixture first and migrate contract, producer, test, and fixture together | WERPC-007 reviewer |
| Spec 052 later executes its old archive package | Mark WDTC-002/WORK-002 superseded and route it to WERPC-008 before research work begins | WERPC-000 reviewer |
| Stage 98 is accidentally changed | Run archive-path diff and archive validation at migration, deletion, and closure gates | Every cutover reviewer |
| Temporary research output is committed | Keep retrieval caches under approved temporary storage; retain only source ledger evidence; run residue scan | WERPC-009 reviewer |
| Concurrent work changes main | Continue in the isolated worktree and compare against the recorded merge base; do not reset or consume user stashes | Primary agent |

Rollback is commit-scoped. Before WERPC-008, reverting any research or migration
commit leaves the old packs live. WERPC-008 is a single deletion commit and can
be reverted without altering Stage 98 or Git history.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `docs/**` except existing `docs/98.archive/**` records;
  `scripts/**` and `tests/**` only for path-contract and fixture migration
- **Forbidden Paths**: existing `docs/98.archive/**` records, `gitops/**`,
  `infrastructure/**`, `traefik/**`, `policy/**`, ignored credential/secret
  state, user stashes, and paths outside the isolated worktree
- **Approval Required**: any live, hosted, remote, credential-bearing,
  secret-reading, push, merge, publication, third-party mutation, or change to
  active runtime/provider/platform behavior
- **Static Validation**: focused commands in each Plan task and
  `bash scripts/validate-repo-quality-gates.sh .` before every commit
- **Live Validation**: `DEFER` — not authorized and not required for this
  descriptive research pack
- **Secret / Vault Handling**: no secret value, token, kubeconfig, ignored
  credential file, Vault payload, or provider credential is read or printed
- **Rollback Plan**: one logical commit per row; WERPC-008 is the isolated
  deletion commit; Git history retains the predecessor content
- **Evidence Location**: this Task, the new source/migration ledger, the
  progress ledger, Git commits, and the SDD ledger review packages
## Completion Criteria

- The exact thirteen new pack files exist and all required topics have one
  primary owner plus current workspace evidence.
- Every material external fact has an appropriate URL, checked date
  `2026-08-08`, and refresh trigger.
- Every old file and split material section has a reviewed disposition and Git
  provenance.
- Mutable current consumers resolve to the new owner or carry an explicit
  source-commit/datetime-bound historical classification.
- Focused contract tests, strict link/owner validation, reference-IA, archive,
  harness, and full repository quality gates pass.
- The three predecessor directories and task-created one-off artifacts do not
  exist.
- Existing Stage 98 records have no branch diff.
- SDD reports and both task-level review gates are accepted; final whole-branch
  review has no unresolved Critical or Important finding.
- Spec, Plan, Task, indexes, task evidence, and progress agree on `done`.

## Traceability

- [Spec 053](spec.md)
- [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [WERPC Task](README.md#task-records)
- Predecessor `Spec 017` at
  `docs/03.specs/0017-workspace-engineering-research-pack/spec.md`
- Conflicting `Spec 052` at
  `docs/03.specs/0052-document-taxonomy-consolidation/spec.md`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WER-001](spec.md#success-criteria--verification-plan) | WERPC-001, WERPC-009 | [Exact thirteen-file inventory](tasks/tsk-0003-werpc-001.md) |
| N/A — VAL-WER-002 shares the Spec source above | WERPC-001, WERPC-009 | [Unique request-to-primary-owner matrix](tasks/tsk-0003-werpc-001.md) |
| N/A — VAL-WER-003 shares the Spec source above | WERPC-001–009 | [25-file and split-section disposition ledger](tasks/tsk-0003-werpc-001.md) |
| N/A — VAL-WER-004 shares the Spec source above | WERPC-002–006, WERPC-009 | [Source register and per-reference freshness review](tasks/tsk-0004-werpc-002.md) |
| N/A — VAL-WER-005 shares the Spec source above | WERPC-002–006, WERPC-009 | [Workspace evidence and five-state status review](tasks/tsk-0004-werpc-002.md) |
| N/A — VAL-WER-006 shares the Spec source above | WERPC-002 | [Provider/common-environment surface matrix review](tasks/tsk-0004-werpc-002.md) |
| N/A — VAL-WER-007 shares the Spec source above | WERPC-002–006 | [Requirement owner matrix and task reviews](tasks/tsk-0004-werpc-002.md) |
| N/A — VAL-WER-008 shares the Spec source above | WERPC-007 | [Focused tests and classified occurrence closure](tasks/tsk-0009-werpc-007.md) |
| N/A — VAL-WER-009 shares the Spec source above | WERPC-008, WERPC-009 | [Exact path absence and residue scan](tasks/tsk-0010-werpc-008.md) |
| N/A — VAL-WER-010 shares the Spec source above | WERPC-007–009 | [Archive diff and archive validation](tasks/tsk-0009-werpc-007.md) |
| N/A — VAL-WER-011 shares the Spec source above | All packages | [SDD ledger, per-task reports/reviews, commit and gate inventory](tasks/tsk-0001-werpc-000.md) |
| N/A — VAL-WER-012 shares the Spec source above | WERPC-009 | [Whole-branch review, full QA, and evidence-depth audit](tasks/tsk-0011-werpc-009.md) |

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WERPC-000](plan.md#work-breakdown) | Done. | Active Spec/Plan/Task and collection indexes; bounded PRD-0008/AD-0011 exception; superseded WDTC-002/WORK-002 route; required strict, diff, and repository-quality checks passed; optional all-files pre-commit INTERRUPTED/SKIP with required-gate fallback; self-review. |
| N/A — WERPC-000A shares the Plan and Spec sources above | Done. | Typed standalone execution, exact-pair/approval/owner/state/overlap/terminal tests, bounded closure authority, two independent reviews, and the complete repository quality gate PASS. |
| N/A — WERPC-001 shares the Plan and Spec sources above | Done. | Exact thirteen-file pack; 32 unique request-primary-owner rows; three dated predecessor source entries; 25 file rows with matching full source commits; 35 text-exact H3 split dispositions; strict registry, strict links/owners, cached diff, and full repository quality gate PASS on the staged tree. |
| N/A — WERPC-002 shares the Plan and Spec sources above | Done. | Dated source/claim ledger (SRC-WERPC-004–013; CLM-WERPC-002-01–009); detailed harness/loop, provider-surface, and common-control-plane references; exact 13 tree/row collection projections; active54/new7 README inventory contract with baseline67/active47/retired20 preserved; documentation and Python fresh reviews Approved; final Reference IA production and complete repository quality gate PASS. |
| N/A — WERPC-003 shares the Plan and Spec sources above | Done. | Three detailed references; `SRC-WERPC-014`–`022` and `CLM-WERPC-003-01`–`13`; complete family matrix with Release absence gap; Diátaxis partial application/tutorial-explanation gap; LLM-WIKI generator/schema/drift/freshness and llms.txt/MCP/search/RAG boundaries; fresh review Approved; final Reference IA production and complete repository quality gate PASS. |
| N/A — WERPC-004 shares the Plan and Spec sources above | Done. | `SRC-WERPC-023`–`034`, `CLM-WERPC-004-01`–`11`, platform/security reference, REQ-WERPC-008/009/025 status cells, focused checks PASS, fresh content review Approved, and final staged Reference IA/cached-diff/complete quality gate PASS. |
| N/A — WERPC-005 shares the Plan and Spec sources above | Done. | CI/CD/GitHub Actions/QA reference, REQ-WERPC-022–024 coverage status, `SRC-WERPC-035`–`044`, and `CLM-WERPC-005-01`–`10`; focused checks PASS; fresh review Approved; exact staged Reference IA/cached diff/complete quality gate PASS. |
| N/A — WERPC-006 shares the Plan and Spec sources above | Done. | Three detailed references; fixed Agency Agents source pin `ebe9c99acb5c96f9468de368d8bead775387d1a7`; `SRC-WERPC-045`–`052`; `CLM-WERPC-006-01`–`08`; focused checks PASS; fresh review Approved; upstream-path RED fixed; staged Reference IA/cached diff/complete quality gate PASS. |
| N/A — WERPC-007 shares the Plan and Spec sources above | Done. | RED/GREEN migration evidence; RIA-protected historical-link proof with valid and fail-closed negative fixtures; 732/70 exact occurrence closure and 70-row classification; isolated staged RIA 88/88 plus direct validator; agent 37/37; active corpus 19/19; registry self-test/strict; links strict/self-test; exact production disposition parse and post-delete clone; hardened Git hostile-config probe; archive validation; Python compile; cached diff; complete repository gate; and full harness PASS. The three phase-bounded README fixture rows remain until atomic WERPC-008 deletion. Python and QA re-reviews Approved; this logical commit. |
| N/A — WERPC-008 shares the Plan and Spec sources above | Done. | Exact25 pre-gate; three absent predecessor roots; exact13 surviving pack; completed 25-row disposition table; README active51/retired23; RIA production; agent-cutover self-test/production; links self-test/strict; archive; cached diff; complete repository gate; and full harness PASS. Optional filesystem-sensitive unit reruns are recorded honestly and do not replace the passing required lanes; this logical commit. |
| N/A — WERPC-009 shares the Plan and Spec sources above | Done. | VAL-WER-001–012 criterion walk, exact13/32/52/25 counts, three absent roots, zero Stage 98 diff, no tracked residue, no unsupported deep-evidence PASS claim, strict links/owners, Reference IA, archive, harness, complete quality gate, lifecycle/index/registry `done` transition, and branch-finishing handoff. |
