---
title: 'Workspace Harness Gap Analysis Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-24
---

# Workspace Harness Gap Analysis Implementation Plan

## Overview (KR)

이 문서는 `hy-home.k8s`가 WSL2, WSL Linux native Docker, k3d, ArgoCD GitOps,
External Secrets, Vault, PostgreSQL, Valkey, SDD, QA, CI/CD, AI Agent 협업
규칙을 일관되게 지탱하는지 감사하고 보강하는 실행 계획이다.

## Context

이 작업은 이전 6개 role-based subagent 리뷰와 baseline static verification을
이어받는다. `grill-with-docs` 검토 결과에 따라 `AGENTS.md`는 thin gateway로
유지하고, recurring workflow와 task-to-skill routing은 기존 runtime SSoT인
`docs/00.agent-governance/harness-catalog.md`에 통합한다.

## Goals & In-Scope

- **Goals**:
  - 전체 대상 범위를 `complete`, `partial`, `unknown`으로 기록한다.
  - 모든 Gap, 삭제 후보, 통합 후보, deferred item, unknown item을 분리한다.
  - 안전한 P1/P2만 구현하고 P3는 pre-check와 follow-up으로 남긴다.
- **In Scope**:
  - spec/task/plan evidence, README indexes, progress memory.
  - scope bridge correction, subagent scratch boundary, task-to-skill routing.
  - GitOps root app manifest non-empty validation.
  - script command-contract clarification.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Kubernetes resource semantic changes.
  - ArgoCD App-of-Apps ownership changes.
  - Vault policy writes or secret value inspection.
  - CI/CD pipeline structure changes.
  - AI Agent instruction priority changes.
- **Out of Scope**:
  - live k3d, ArgoCD, Vault, PostgreSQL, Valkey, ESO, or Traefik runtime checks.
  - bulk deletion or ignored local file cleanup.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Record spec/task/plan evidence and indexes | `docs/03.specs`, `docs/04.execution`, `memory/progress.md` | REQ-SDD-TRACE | Repo quality gate PASS |
| PLN-002 | Correct subagent scope bridge drift | `docs/00.agent-governance/scopes/*.md` | REQ-AGENT-ROUTE | Scope imports match bridge rows |
| PLN-003 | Clarify scratch workspace and skill-routing boundaries | `subagent-protocol.md`, `harness-catalog.md` | REQ-HARNESS | Governance docs stay English and gateway remains thin |
| PLN-004 | Harden GitOps root app validation | `scripts/validate-gitops-structure.sh`, `scripts/README.md` | REQ-GITOPS-STATIC | GitOps structure check PASS |
| PLN-005 | Preserve high-risk Gap follow-up | This plan and linked task | REQ-RISK | P3 items have pre-checks and follow-up |
| PLN-006 | Run verification and final checklist | scripts, docs, runtime JSON | REQ-VALIDATION | Commands pass or limitations recorded |
| PLN-007 | Audit unreflected input tasks and close safe follow-up gaps | this plan, linked task, `harness-catalog.md`, `.claude/skills/workspace-harness-audit/skill.md` | REQ-INPUT-REFLECTION | Skill path check PASS and repo quality gate PASS |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository quality and docs governance | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Generated docs | LLM Wiki generated index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-003 | GitOps | Root apps and kustomization structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Manifests | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or optional-tool skip recorded |
| VAL-PLN-005 | Secrets | Plaintext secret pattern scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-006 | Infra | Static infrastructure contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-007 | Shell | Shell syntax check | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS |
| VAL-PLN-008 | Runtime JSON | Claude and Codex JSON parse | `python3 -m json.tool .claude/settings.json`; `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-009 | Env | Key-name-only env comparison | compare `.env.example` and `.env` keys without values | no differences |
| VAL-PLN-010 | Git hygiene | Whitespace sanity | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Full-scope audit becomes broad runtime change | High | Limit implementation to P1/P2 and defer P3 |
| Skill routing duplicates gateway policy | Medium | Keep `AGENTS.md` thin and record routing in `harness-catalog.md` |
| Static checks are mistaken for live health | Medium | Label live checks as unknown/deferred |
| Optional tools are unavailable locally | Medium | Record skipped reason and CI follow-up |
| Empty root app set passes validation | Medium | Add explicit non-kustomization root app manifest assertion |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-static validation listed above.
- **Sandbox / Canary Rollout**: not applicable.
- **Human Approval Gate**: required for live cluster, Vault, ArgoCD, or GitHub
  ruleset changes.
- **Rollback Trigger**: revert this documentation/governance/script change set
  if repo quality or GitOps structure checks cannot pass.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Baseline instructions checked.
- [x] Full target inventory recorded.
- [x] Six subagent results collected.
- [x] Coverage Ledger created.
- [x] Integrated Gap Analysis created.
- [x] Deletion, consolidation, deferral, and unknown items recorded.
- [x] spec/task/plan artifacts created.
- [x] Implementation Plan created.
- [x] P1/P2 changes implemented.
- [x] Verification run and limitations recorded.
- [x] Checklist gate completed.
- [x] Final Report created.
- [x] Input reflection follow-up completed.

# Coverage Ledger

| Area | Target path | Investigation status | Representative files read | Gap count | Deletion/consolidation/deferral candidate count | Unknown items | Next action |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| Documentation | `docs/00.agent-governance/` | complete | `documentation-protocol.md`, `stage-authoring-matrix.md`, `harness-catalog.md` | 2 | 3 | live runtime parity | Update scope bridges and harness catalog |
| Documentation | `docs/01.requirements/` | complete | README, PRD files via lifecycle reviewer | 0 | 0 | external freshness | Keep current |
| Documentation | `docs/02.architecture/` | complete | README, ADR/ARD index, superseded Dashboard ADR | 0 | 1 | strict legacy policy | Keep historical records |
| Documentation | `docs/03.specs/` | complete | README, specs 001-005, this spec | 1 | 0 | live implementation parity | Add this spec and index |
| Documentation | `docs/04.execution/` | complete | plan/task READMEs and current audit docs | 1 | 1 | strict plan/task exception policy | Add plan/task evidence |
| Documentation | `docs/05.operations/` | complete | guide/runbook/policy indexes and superseded onboarding docs | 1 | 3 | live operations state | Defer live checks |
| Documentation | `docs/90.references/` | complete | LLM Wiki README/index, version inventory | 1 | 0 | external latest freshness | Keep generated index checked |
| Documentation | `docs/99.templates/` | complete | README, spec/task/plan/readme templates | 0 | 1 | none | Keep templates unchanged |
| Scripts | `scripts/` | complete | README and five shell scripts | 2 | 1 | secret scan tolerance | Harden GitOps validation and clarify hook env |
| GitOps | `gitops/` | partial | root apps, platform network policies, ESO, argocd notifications | 5 | 3 | live ArgoCD health | Defer semantic/runtime changes |
| Infrastructure | `infrastructure/` | partial | README, bootstrap, static tests, Vault policy | 3 | 2 | live Vault/external reachability | Defer policy/runtime changes |
| Traefik | `traefik/` | complete | README and dynamic configs | 0 | 0 | live route health | Keep helper boundary |
| Examples | `examples/` | partial | sample app, AWS/Azure README/manifests | 2 | 1 | cloud version freshness | Defer sample secret contract alignment |
| Environment | `.env.example`, `.env` | complete | key-name-only comparison | 0 | 0 | value correctness | Keep values uninspected |
| QA | `tests/`, `infrastructure/tests/` | partial | tests README, static/live test scripts | 2 | 2 | live test state | Keep live tests manual |
| CI/CD | `.github/`, `.pre-commit-config.yaml` | partial | CI workflow, pre-commit, zizmor config | 2 | 2 | remote CI/rulesets | Defer SHA/ruleset decisions |
| Agent governance | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.codex/`, `.agents/` | partial | gateways, runtime baseline, agents, hooks, local mirrors | 5 | 5 | local permission precedence | Implement P1/P2 governance fixes |
| Agent governance | `.agent/` | unknown | path missing | 1 | 0 | whether path is intentionally absent | Record as missing path, no file creation |

# Integrated Gap Analysis

## Summary

- Overall status: repository-static baseline is healthy, with targeted harness,
  validation, and documentation-routing gaps.
- Largest Gap: GitOps semantic/runtime readiness around ESO egress, Vault policy,
  AppProject permissions, and bootstrap ownership.
- Immediately implementable: scope bridge drift, scratch boundary,
  task-to-skill routing, root app non-empty validation, hook env documentation.
- Needs deferral: Kubernetes resource semantics, ArgoCD ownership, Vault policy,
  GitHub Actions SHA pinning, live cluster validation.
- Unknown areas: live k3d/ArgoCD/Vault state, optional local toolchain, GitHub
  branch protection/rulesets, `.env` value freshness.

## Gaps by Area

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Agent governance | Docs scope bridge omits `wiki-curator` | `docs/00.agent-governance/scopes/docs.md`; `.claude/agents/wiki-curator.md` | Misleading subagent routing | Low | improvement | P1 |
| Agent governance | Infra scope bridge omits `gitops-reviewer` | `docs/00.agent-governance/scopes/infra.md`; `.claude/agents/gitops-reviewer.md` | Misleading ownership review | Low | improvement | P1 |
| Agent governance | Scratch `_workspace/` convention is skill-local only | `.claude/skills/incident-postmortem/skill.md`; `subagent-protocol.md` | Future ad-hoc runtime folders | Low | supplementation | P1 |
| Agent governance | Prompt-level skill routing is not consolidated | user task contract; `harness-catalog.md` | Repeated task-to-skill rules can drift | Medium | supplementation | P2 |
| Agent governance | Reference-pattern skills are described as uniform workflow contracts | `harness-catalog.md` Skills table | Skill expectations are ambiguous | Medium | supplementation | P2 |
| Agent governance | Required external `SKILL.md` paths were listed but exact path-check evidence was not preserved | user task contract; `harness-catalog.md` | Missing-path Gap requirement lacked durable proof | Low | supplementation | P1 |
| Agent governance | Repeated broad workspace audit workflow was cataloged but not captured as a repo-local Skill | `harness-catalog.md`; previous plan | Future broad audits can omit path checks or raw ledger preservation | Medium | addition | P2 |
| Documentation | Initial Final Report contract included `Skill and Harness Updates`, but the report used the shorter later format | user task contract; this Final Report | Reporting format drift for harness work | Low | supplementation | P1 |
| Agent governance | Raw subagent ledgers are summarized but not durably archived in original role output format | this plan `Subagent Summary` | Replayability weaker than prompt contract | Medium | deferral | P3 |
| Scripts | GitOps root app validator does not fail on zero non-kustomization root app manifests | `scripts/validate-gitops-structure.sh` | Empty App-of-Apps root could partially pass | Medium | improvement | P2 |
| Scripts | Hook simulation skip env is internal but undocumented | `.claude/hooks/post-validate.sh`; `scripts/validate-repo-quality-gates.sh` | Maintainers may misuse bypass | Low | supplementation | P2 |
| GitOps | ESO egress policy may omit DNS/API egress | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml` | ESO reconciliation risk | High | deferral | P3 |
| GitOps | Vault policy omits `platform/notifications` path | `infrastructure/vault/policies/eso-read.hcl`; `argocd-notifications-secret.yaml` | Slack ExternalSecret sync risk | High | deferral | P3 |
| GitOps | AppProject may not permit documented app `ExternalSecret` | `gitops/clusters/local/appproject-apps.yaml`; `examples/sample-app/external-secret.yaml` | App onboarding drift | Medium | deferral | P3 |
| GitOps | `gitops/clusters/local` bootstrap CR ownership is not fully reconciled by root app | `root-application.yaml`; `bootstrap-local.sh` | AppProject/ApplicationSet drift risk | High | deferral | P3 |
| CI/CD | GitHub Actions use tag pinning with `unpinned-uses` disabled | `.github/zizmor.yml`; `.github/workflows/ci.yml` | Supply-chain policy risk | Medium | deferral | P3 |
| Agent governance | `.claude/settings.local.json` broad local allows need precedence review | `.claude/settings.local.json`; `.claude/settings.json` | Local safety ambiguity | Medium | deferral | P3 |
| Agent governance | ignored graphify rules/workflows are outside repo skill SSoT | `.agents/rules/graphify.md`; `.agents/workflows/graphify.md` | Local-only drift | Medium | deferral | P3 |
| QA | Optional local tooling unavailable | `.pre-commit-config.yaml`; local command checks | Local parity gap | Medium | deferral | P3 |
| Environment | `.env` values not inspected | `.env`, `.env.example` | Secret freshness unknown | Medium | deferral | P3 |

## Conflicts/Duplicates

| Target | Description | Impact | Recommended action |
| --- | --- | --- | --- |
| `AGENTS.md` vs requested recurring rules | User asked to consolidate recurring workflow/skill-routing; repo says gateway stays thin | Root gateway could become duplicative | Keep `AGENTS.md` thin and extend `harness-catalog.md` |
| `.claude/settings.local.json` vs shared deny boundary | Local allows may be broader than shared policy | Unknown local permission behavior | Defer until precedence is verified |
| `.agents/rules` and `.agents/workflows` | Ignored local graphify surfaces are outside tracked skill SSoT | Local-only drift | Keep ignored or clean locally after owner decision |
| Plan/task pairing | One historical plan lacks separate task record | Strict automation ambiguity | Keep documented exception unless policy changes |

## Deletion Candidates

| Target | Type | Candidate reason | Reference check | Impact | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.agents/rules/graphify.md` | deletion candidate | Ignored local rule can trigger generated churn | Local ignored only; no tracked references | Local context | Defer owner decision |
| `gitops/clusters/local/appproject-apps.yaml` `Namespace` whitelist | deletion candidate | Namespace ownership appears platform-owned | Requires `CreateNamespace=true` check | AppProject least privilege | Defer |
| Legacy/superseded docs | deletion candidate | Some documents are historical | References remain and replacement pointers exist | Architecture/ops history | Do not delete |

## Consolidation Candidates

| Target | Consolidation reason | Target location | Required pre-check |
| --- | --- | --- | --- |
| task-to-skill routing | Repeated prompt routing should not live in root gateway | `docs/00.agent-governance/harness-catalog.md` | Confirm gateway remains thin |
| `_workspace/` scratch convention | Incident skill has repeated scratch workflow | `docs/00.agent-governance/subagent-protocol.md` | Confirm no durable docs go to scratch |
| `gitops/clusters/local` bootstrap CR ownership | Bootstrap resources are repo-backed but not fully root-managed | Future GitOps bootstrap owner model | Decide ArgoCD ownership pattern |
| `examples/sample-app/external-secret.yaml` Vault key format | Sample path may not match ClusterSecretStore path | Examples and app onboarding docs | Validate intended ESO key semantics |

## Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| ESO NetworkPolicy DNS/API egress | Kubernetes network policy semantic change | Confirm ESO required egress and cluster DNS/API targets | Add manifest change and live ESO validation |
| Vault policy `platform/notifications` | Secret access policy change | Confirm Vault path, runtime policy, and rollback | Add least-privilege HCL and static coverage |
| App `ExternalSecret` permission | AppProject permission change | Confirm intended app onboarding secret model | Update AppProject and examples together |
| Bootstrap CR ownership | ArgoCD ownership model change | Decide bootstrap vs managed-app pattern | Create separate architecture/operations plan |
| GitHub Actions SHA pinning | CI/CD supply-chain policy decision | Confirm accepted risk vs SHA pinning | Update workflows, inventory, and zizmor config |
| `.claude/settings.local.json` | Ignored local runtime file | Verify Claude local/project precedence | Tighten or document local-only scope |
| Live validation | Requires live cluster and secret-safe checks | Human approval and target context | Run read-only live test scripts |

## Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| `.agent/` | Path missing in this checkout | Confirm whether absence is intentional |
| Live k3d/ArgoCD/Vault/ESO health | No live commands approved | Run approved read-only checks |
| Optional local toolchain | Some tools may not be installed | Run `pre-commit run --all-files` in CI/tooling environment |
| GitHub branch protection/rulesets | Not stored in worktree | Inspect GitHub repository settings |
| `.env` value freshness | Values intentionally not read or printed | Human-only secret review |

# Implementation Plan

## P1 Low risk / Immediate implementation

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| improvement | `docs/00.agent-governance/scopes/docs.md` | Add `wiki-curator` to Subagent Bridge | T-004 | repo quality gate | Revert line |
| improvement | `docs/00.agent-governance/scopes/infra.md` | Add `gitops-reviewer` to Subagent Bridge | T-004 | repo quality gate | Revert line |
| supplementation | `docs/00.agent-governance/subagent-protocol.md` | Clarify `_workspace/` scratch boundary | T-005 | repo quality gate | Revert paragraph |
| addition | spec/task/plan docs | Create traceability docs and indexes | T-001 | repo quality gate and link checks | Remove added docs/index entries |
| supplementation | this plan and linked task | Record input reflection audit and exact external skill path check result | T-010, T-011 | repo quality gate | Revert follow-up sections |
| supplementation | Final Report section layout | Add explicit `Skill and Harness Updates` section | T-010 | repo quality gate | Revert report section edit |

## P2 Medium risk / Limited implementation

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| improvement | `scripts/validate-gitops-structure.sh` | Fail when root app manifest count is zero | T-006 | `bash scripts/validate-gitops-structure.sh`; shell syntax | Revert script hunk |
| supplementation | `scripts/README.md` | Document hook simulation bypass as internal | T-006 | repo quality gate | Revert README paragraph |
| supplementation | `harness-catalog.md` | Add external requested skill routing and skill type boundary | T-005 | repo quality gate | Revert sections |
| addition | `.claude/skills/workspace-harness-audit/skill.md` and `harness-catalog.md` | Capture repeated workspace-wide audit workflow as repo-local Skill | T-012 | repo quality gate | Remove skill and catalog row |

## P3 High risk / Deferred

| Action type | Target | Deferral reason | Pre-check | Follow-up work |
| --- | --- | --- | --- | --- |
| deferral | ESO NetworkPolicy | Kubernetes semantic behavior | Confirm DNS/API egress and live ESO needs | Separate GitOps manifest task |
| deferral | Vault policy | Secret access policy | Confirm Vault runtime path and rollback | Add HCL plus static test |
| deferral | AppProject app `ExternalSecret` | Permission model change | Confirm onboarding contract | Update AppProject/examples/docs |
| deferral | Bootstrap CR ownership | ArgoCD ownership design | Decide managed owner model | Architecture and runbook update |
| deferral | GitHub Actions SHA pinning | CI policy decision | Review supply-chain risk | Update workflows and inventory |
| deferral | Local Claude settings | Ignored local runtime behavior | Verify precedence | Tighten local file if needed |
| deferral | Live checks | Requires approved runtime context | Human approval | Run live read-only tests |
| deferral | Historical raw subagent ledgers | Original raw role outputs are not authoritative current-state files | Future subagent runs must persist raw Summary/Ledger tables into plan/task evidence | Enforce through `workspace-harness-audit` skill |

# Input Reflection Follow-up

## Unreflected or Weakly Reflected Input Tasks

| Input task | Existing reflection | Gap judgment | Implementation |
| --- | --- | --- | --- |
| Verify exact required external `SKILL.md` paths and record missing paths as Gaps | Paths were listed in `harness-catalog.md`, but no durable path-check result was recorded | weak reflection | Added path-check result to this plan/task; all listed paths were present in the current WSL environment |
| Create or improve reusable Skills for repeated workflows where appropriate | Repeated routing was consolidated into `harness-catalog.md` only | partial reflection | Added `.claude/skills/workspace-harness-audit/skill.md` and cataloged it |
| Include `Skill and Harness Updates` in the Final Report | Final Report used the shorter later contract | weak reflection | Added the explicit section and kept the rest of the report intact |
| Preserve subagent Summary and Ledger output format | Plan preserves summaries and integrated ledgers, not raw role output tables | partial reflection | Current raw outputs are not reconstructed; future runs must preserve raw role tables through the new Skill workflow |

## Required External Skill Path Check

| Area | Result | Missing paths |
| --- | --- | --- |
| Workspace investigation and analysis | PASS | none |
| Documentation writing | PASS | none |
| Documentation co-authoring and release | PASS | none |
| Repeated workflow and instruction skills | PASS | none |
| Subagent creation and subagent-driven work | PASS | none |
| Hook work | PASS | none |
| Native instruction files and runtime governance | PASS | none |
| Scripts | PASS | none |
| Kubernetes and infrastructure | PASS | none |
| QA | PASS | none |
| CI/CD | PASS | none |

# Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task |
| `bash scripts/validate-gitops-structure.sh` | PASS, root app manifest count: 17 | linked task |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task |
| shell syntax check | PASS | linked task |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task |
| `.env.example` and `.env` key comparison | PASS, key names match without printing values | linked task |
| required external `SKILL.md` path check | PASS, all listed paths present | linked task |
| `git diff --check` | PASS | linked task |

# Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | User task contract and this plan summary |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Six subagent reviews and repo-static checks |
| Are modification scope and forbidden scope separated? | pass | P1/P2/P3 sections |
| Are existing patterns, compatibility, and dependency rules stated? | pass | AGENTS thin gateway, GitOps-first, template-first rules |
| Are test, lint, and type-check commands identified? | pass | Verification Plan |
| Are completion criteria measurable? | pass | Completion Criteria and verification commands |
| Are recurring instructions moved or planned for `AGENTS.md` or Skills? | pass | Routing consolidated into `harness-catalog.md` |

# Final Report

## 1. Baseline Instruction Check

| Target | Checked | Key impact |
| --- | --- | --- |
| `AGENTS.md` | yes | Thin gateway remains primary contract |
| `CLAUDE.md` | yes | Claude shim remains thin |
| `.claude/CLAUDE.md` | yes | Runtime baseline and hook boundaries preserved |
| `CLAUDE.local.md` | yes | Not present |
| `GEMINI.md` | yes | Gemini shim remains thin |
| `docs/00.agent-governance/` | yes | Governance SSoT and matrix-first rules used |
| `docs/99.templates/` | yes | Spec/task/plan templates followed |
| `.agent/` | yes | Missing path recorded as unknown |
| `.agents/` | yes | Ignored local mirrors and graphify surfaces recorded |
| `.claude/` | yes | Agents, hooks, skills, settings reviewed |
| `.codex/` | yes | Agent mirrors and hook wiring reviewed |

## 2. Coverage Ledger Summary

| Area | Investigation status | Gap count | Candidate count | Unknown |
| --- | --- | ---: | ---: | --- |
| Documentation | complete | 4 | 6 | live parity, strict exception policy |
| Scripts | complete | 2 | 1 | secret scan depth |
| GitOps/infrastructure | partial | 8 | 6 | live cluster, Vault, external reachability |
| Environment/QA/CI | partial | 4 | 4 | optional tools, CI/rulesets, env values |
| Agent governance | partial | 6 | 5 | local precedence, `.agent/` absence |

## 3. Subagent Summary

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | complete | Lifecycle and templates are healthy; one historical plan/task exception | live runtime parity |
| Agent Governance Reviewer | complete | Gateway/mirrors coherent; local settings and graphify local surfaces deferred | local permission precedence |
| Scripts Reviewer | complete | All scripts retained; root app count and hook env docs need hardening | env bypass audience |
| GitOps Infrastructure Reviewer | complete | Semantic GitOps gaps in ESO, Vault, AppProject, bootstrap ownership | live ArgoCD/Vault state |
| Environment Quality Reviewer | complete | Env keys match; CI/static gates clear; optional tools missing | remote CI/rulesets |
| Skills & Harness Reviewer | complete | Scope bridge drift and scratch convention need correction | live hook behavior |

## 4. Integrated Gap Analysis Summary

| Area | Key Gap | Risk | Action | Priority |
| --- | --- | --- | --- | --- |
| Agent governance | stale scope bridge rows | Low | update | P1 |
| Agent governance | task-to-skill routing not consolidated | Medium | add to catalog | P2 |
| Scripts | root app manifest count not asserted | Medium | harden validator | P2 |
| GitOps | ESO/Vault/AppProject semantic gaps | High | defer | P3 |
| CI/CD | tag pinning accepted risk | Medium | defer | P3 |

## 5. spec/task/plan Updates

| Document | Change | Linked work |
| --- | --- | --- |
| `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | New technical contract | T-001 |
| `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` | New plan with ledgers and report | T-002 |
| `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md` | New execution evidence | T-003 |
| stage README indexes | New entries | T-001 |
| `memory/progress.md` | Progress and evidence entry | T-009 |

## 6. Skill and Harness Updates

| Target | Action | Skill used | Reason |
| --- | --- | --- | --- |
| `.claude/skills/workspace-harness-audit/skill.md` | Added repo-local workflow Skill | `writing-skills`, `write-a-skill`, `skill-creator`, `skill-improver` guidance | Capture repeated broad workspace audit workflow and prevent future omission of skill path checks or raw ledger preservation |
| `docs/00.agent-governance/harness-catalog.md` | Added skill inventory row and retained external requested skill routing | `grill-with-docs`, `agent-md-refactor` routing principles | Keep `AGENTS.md` thin while centralizing harness routing |
| Required external `SKILL.md` paths | Verified exact paths | `grill-with-docs` plus task-specific skill routing | Satisfy missing-path Gap recording contract; no missing paths found |

## 7. Implementation Changes

| Target | Change | Reason | Linked task |
| --- | --- | --- | --- |
| `docs.md` scope | Add `wiki-curator` bridge | Match actual import | T-004 |
| `infra.md` scope | Add `gitops-reviewer` bridge | Match actual import | T-004 |
| `subagent-protocol.md` | Add scratch boundary | Prevent ad-hoc durable outputs | T-005 |
| `harness-catalog.md` | Add task-to-skill routing and skill type note | Consolidate recurring workflow routing | T-005 |
| `validate-gitops-structure.sh` | Add root app manifest count assertion | Close static validation gap | T-006 |
| `scripts/README.md` | Clarify hook env bypass | Prevent manual misuse | T-006 |
| `.claude/skills/workspace-harness-audit/skill.md` | Add reusable workspace audit workflow | Close repeated-workflow Skill gap | T-012 |
| this plan and linked task | Add input reflection follow-up and skill path check evidence | Close weakly reflected original input tasks | T-010, T-011 |

## 8. Deletion, Consolidation, and Deferred Items

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| `.agents/rules/graphify.md` | deletion candidate | ignored local drift | local ignored only | defer owner decision |
| `gitops/clusters/local` ownership | consolidation | bootstrap CR drift | static review partial | defer design |
| ESO NetworkPolicy | deferred | runtime semantic change | manifest review | separate task |
| Vault policy | deferred | secret access policy | manifest/HCL review | separate task |
| SHA pinning | deferred | CI policy | workflow/zizmor review | separate task |
| historical raw subagent ledgers | deferred | original raw role output tables are not current-state files | current plan has integrated summaries | preserve raw Summary/Ledger tables in future runs through `workspace-harness-audit` |

## 9. Verification

| Command or method | Result | Record location |
| --- | --- | --- |
| Full verification bundle | PASS; optional `kube-linter` unavailable and live checks deferred | task verification summary |
| External required skill path check | PASS; no missing paths | input reflection follow-up |

## 10. Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Goal clear | pass | task contract |
| Related files discovered | pass | ledger |
| Scope separated | pass | P1/P2/P3 |
| Existing patterns stated | pass | governance links |
| Commands identified | pass | verification plan |
| Criteria measurable | pass | completion criteria |
| Recurring rules routed | pass | harness catalog |

## 11. Remaining Risks and Next Work

- Complete live runtime validation only with explicit approval.
- Implement P3 GitOps and security-policy changes as separate reviewed tasks.
- Verify optional toolchain and GitHub rulesets outside this local static pass.
- Do not reconstruct historical raw subagent output tables without authoritative
  source output; preserve them directly in future workspace harness audits.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Tasks**: [../tasks/2026-05-24-workspace-harness-gap-analysis.md](../tasks/2026-05-24-workspace-harness-gap-analysis.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Workspace Harness Audit Skill**: [../../../.claude/skills/workspace-harness-audit/skill.md](../../../.claude/skills/workspace-harness-audit/skill.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
