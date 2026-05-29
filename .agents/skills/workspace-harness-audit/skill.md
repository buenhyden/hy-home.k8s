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

## Workflow Steps

1. Read `AGENTS.md`, `.claude/CLAUDE.md`, governance rules, templates, and the
   current user task contract before editing.
2. Inventory all requested target paths and mark each `complete`, `partial`, or
   `unknown`; do not mark unreviewed areas complete.
3. Use `grill-with-docs` when the prompt requests plan stress-testing; answer
   questions from repository evidence before asking the human.
4. When the prompt names additive review skills or frameworks, record whether
   each one was applied, skipped, missing, or in conflict with the active task
   contract. If a named skill is design-only but the human explicitly requests
   implementation, use it as a review lens and document that boundary.
   Prefer this repository's canonical spec/task/plan stage over off-taxonomy
   design-doc locations unless the human explicitly asks for a separate design
   document.
5. Map each task area to required repo-local and external `SKILL.md` paths.
   Check exact path existence and record missing paths as Gaps.
6. Run or reuse up to six role-based subagent reviews only when evidence is
   current. Preserve each role's Summary, Ledger, candidates, and Unknowns in
   the plan/task record.
7. Create or update the Coverage Ledger, Integrated Gap Analysis, Implementation
   Plan, deletion/consolidation/deferred/unknown tables, verification results,
   checklist gate, and Final Report.
8. Implement only linked P1/P2 items with clear verification and rollback.
   Defer live cluster, Vault, ArgoCD, CI policy, and secret-boundary changes.
9. Run repo-static verification and record skipped live checks with reason,
   alternative evidence, and follow-up.
10. Before completion, audit every explicit input requirement against current
    files and command output; unresolved or weak evidence stays in the plan.
11. When follow-up work resolves or changes an item previously recorded as
    deferred, add a current-state overlay that links the new evidence instead
    of silently leaving the older plan as the only visible status.
12. When the prompt names an execution workflow skill, record the plan load,
    critical review, task execution, verification, and finish boundary instead
    of only recording that the skill was mentioned.

## Expected Outputs

- Spec/task/plan evidence under the canonical docs stage tree.
- Task-to-skill path check results with present/missing status.
- P1/P2 implementation evidence and P3 follow-up records.
- Final report with skill/harness updates and verification evidence.
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
- Treating static validation as proof of live k3d, ArgoCD, Vault, or ESO health.
- Applying a named skill in chat without preserving the application boundary in
  durable task or plan evidence.
- Leaving older P3 deferral rows as the only visible status after a later
  approved plan implements part of that deferred work.
- Treating a named execution skill as satisfied by a mention without recording
  the actual plan execution flow.
