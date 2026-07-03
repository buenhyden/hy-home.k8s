---
name: workspace-harness-audit
description: Use when auditing hy-home.k8s workspace-wide WSL2/k3d/ArgoCD GitOps harness, SDD lifecycle, agent governance, or checking whether a broad workspace improvement prompt is fully reflected.
---

# workspace-harness-audit

## Purpose

Keep broad workspace improvement work complete, evidence-backed, and bounded to
safe implementation in `hy-home.k8s`.

## When to Use

- Full workspace Gap analysis or harness improvement request.
- Review of whether a prior broad prompt was fully reflected.
- Changes that span docs lifecycle, GitOps, scripts, QA, CI/CD, and agent
  governance.

## When NOT to Use

- Narrow docs cleanup, template conformance, README/index drift, link drift, or
  duplicate-H1 fixes; use `docs-stage-conformance`.
- Live cluster incident response, unless the task is only planning or
  documenting approved read-only checks.
- Generic Kubernetes manifest authoring when `gitops-workflow`,
  `k8s-validate`, or `k8s-security-audit` is the narrower match.
- Browser scrape codification or UI automation skill creation.

## Workflow Phases

### Phase 1 - Intake and Evidence Boundary

**Entry Criteria**

- A broad workspace, harness, governance, or cross-provider improvement request
  is active.
- The requested scope is inside `hy-home.k8s` and can be assessed from repo
  evidence before live runtime claims are made.

**Actions**

1. Read the appropriate root provider shim (`AGENTS.md`, `CLAUDE.md`, or
   `GEMINI.md`), the relevant runtime baseline, Stage 00 governance rules,
   templates, and the current user task contract before editing.
2. Inventory requested target paths and mark each `complete`, `partial`, or
   `unknown`; do not mark unreviewed areas complete.
3. Map each task area to required repo-local and external `SKILL.md` paths.
   Check exact path existence and record missing paths as Gaps.
4. When the prompt names additive skills or frameworks, record the boundary:
   applied, skipped, missing, near-miss, or in conflict with the active task.
   Use `agent-sort` as the ECC DAILY/LIBRARY classification lens,
   `eval-harness` as the deterministic eval lens, and `enhance-prompt` as a UI
   prompt near-miss that is a default no-op unless the task is prompt/UI work.

**Exit Criteria**

- The task contract, target paths, named-skill boundary, live-check boundary,
  and evidence sources are recorded in the Plan/Task evidence or working
  ledger.

### Phase 2 - Four-Element Harness Mapping

**Entry Criteria**

- Phase 1 has identified the active scope and evidence boundary.

**Actions**

1. Map the four harness elements for common Stage 00, Claude, and Codex
   surfaces before proposing edits:
   - instruction and settings documents: how the agent learns what to do
   - architecture constraints: what blocks unsafe or off-domain action
   - feedback loops: how outputs are validated and routed for repair
   - knowledge stores: where durable rationale and compacted context live
2. Preserve the relationship `instructions -> constraints -> feedback ->
   knowledge -> next-session instructions`; do not reduce the audit to a file
   inventory.
3. Classify ECC surfaces as `DAILY` or `LIBRARY` from repo evidence. Do not
   create a separate skill-library router when the existing `.agents/skills`
   SSoT and `harness-catalog.md` routing already cover searchable library use.
4. Use `grill-with-docs` only when the prompt requests plan stress-testing;
   answer questions from repository evidence before asking the human.

**Exit Criteria**

- Every harness element has a common owner, provider adapter behavior,
  feedback path, and knowledge-store path, with unknowns explicitly marked.

### Phase 3 - Plan and Change Selection

**Entry Criteria**

- Phase 2 has a complete or explicitly gap-marked harness map.

**Actions**

1. Create or update the Coverage Ledger, Integrated Gap Analysis,
   Implementation Plan, deletion/consolidation/deferred/unknown tables,
   verification results, checklist gate, and Final Report.
2. Prefer this repository's canonical spec/task/plan stage over off-taxonomy
   design-doc locations unless the human explicitly asks for a separate design
   document.
3. Implement only linked P1/P2 items with clear verification and rollback.
   Defer live cluster, Vault, ArgoCD, CI policy, and secret-boundary changes
   unless the human gives explicit approval.
4. When follow-up work resolves or changes an item previously recorded as
   deferred, add a current-state overlay that links the new evidence instead
   of silently leaving the older plan as the only visible status.

**Exit Criteria**

- The implementation scope is tied to Plan/Task IDs, affected files, validation
  commands, rollback expectations, and out-of-scope live/runtime boundaries.

### Phase 4 - Implementation and Drift Garbage Collection

**Entry Criteria**

- Phase 3 has selected scoped changes with validation commands.

**Actions**

1. Check documentation language/template boundaries: human-facing README and
   overview prose should prefer Korean; explicit AI-agent-facing sections such
   as `AI Agent Requirements` should prefer English; every authored document
   family must route to the canonical template mapping.
2. Treat code drift, document drift, and structure drift as harness feedback.
   Remove temporary/debug artifacts and disallowed scratch naming, archive
   conflicting active docs only with Tombstones and replacement evidence, and
   add deterministic regression checks when possible.
3. Keep shared validation controls in tracked Claude settings, shared hooks,
   provider hook JSON wiring, scripts, and validators. Treat Hookify
   `.local.md` rules as ignored local advisory files, not shared policy.
4. When the prompt names an execution workflow skill, record the plan load,
   critical review, task execution, verification, and finish boundary instead
   of only recording that the skill was mentioned.

**Exit Criteria**

- The smallest durable surface that prevents recurrence has been updated:
  rule, prompt/skill, hook, validator, template, README index, archive
  Tombstone, or memory entry.

### Phase 5 - Verification Criteria and Handoff

**Entry Criteria**

- Phase 4 changes are complete and no known temporary/debug artifacts remain.

**Actions**

1. Run repo-static verification and record skipped live checks with reason,
   alternative evidence, and follow-up.
2. Treat `eval-harness` completion as explicit command evidence: no inferred
   PASS and no live k3d, ArgoCD, Vault, ESO, or secret readiness from static
   checks.
3. Before completion, audit every explicit input requirement against current
   files and command output; unresolved or weak evidence stays in the plan.
4. Record repo-changing work only in the canonical progress ledger at
   `docs/00.agent-governance/memory/progress.md`.

**Verification Criteria**

- `bash scripts/validate-repo-quality-gates.sh .` passes or any failure is
  documented with a scoped remediation.
- `git diff --check`, relevant JSON parsing, shell syntax, generated-index
  freshness, and changed-file pre-commit evidence are recorded when applicable.
- `rg --files | rg '(^|/)progress\.md$'` returns only
  `docs/00.agent-governance/memory/progress.md`.
- Hookify local advisory files remain ignored and untracked.

**Exit Criteria**

- The handoff names changed surfaces, validation evidence, skipped checks, and
  any follow-up work without implying unverified live runtime readiness.

## Expected Outputs

- Spec/task/plan evidence under the canonical docs stage tree.
- Task-to-skill path check results with present/missing status.
- P1/P2 implementation evidence and P3 follow-up records.
- Final report with skill/harness updates and verification evidence.
- Four-element control model showing instruction documents, architecture
  constraints, feedback loops, and knowledge stores for common Stage 00,
  Claude, and Codex surfaces.
- Documentation language/template boundary evidence and drift garbage
  collection evidence for code, document, and structure drift.
- Named-skill application evidence, including any skill/task-contract boundary
  decisions.
- Current-state overlays for stale deferrals after approved follow-up work.
- Execution-skill evidence showing plan review, task execution, verification,
  and finish boundary when requested by the human.

## Common Mistakes

- Reducing coverage because implementation time is limited.
- Listing external skill paths without checking whether they exist.
- Keeping raw subagent ledgers only in chat instead of durable plan/task
  evidence.
- Moving recurring rules into `AGENTS.md` instead of `harness-catalog.md` or a
  repo-local skill.
- Treating Claude, Codex, and Gemini hook wiring as equal permission gates; only
  Claude has a native permission gate in this repository.
- Marking a harness element Ready because files exist without showing how it
  connects to the other three elements.
- Treating static validation as proof of live k3d, ArgoCD, Vault, or ESO health.
- Leaving `AI Agent Requirements` sections in reader-localized prose when the
  section is meant to be an agent execution contract.
- Adding drift notes without wiring a rule, hook, validator, template, README,
  archive Tombstone, or memory update that prevents recurrence.
- Applying a named skill in chat without preserving the application boundary in
  durable task or plan evidence.
- Leaving older P3 deferral rows as the only visible status after a later
  approved plan implements part of that deferred work.
- Treating a named execution skill as satisfied by a mention without recording
  the actual plan execution flow.
