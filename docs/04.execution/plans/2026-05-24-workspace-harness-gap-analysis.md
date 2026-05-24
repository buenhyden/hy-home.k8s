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
| PLN-008 | Apply `office-hours` reflection to initial-contract coverage | this plan, linked task, `workspace-harness-audit` skill, progress ledger | REQ-INPUT-REFLECTION | Office-hours boundary recorded and repo quality gate PASS |

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
| VAL-PLN-011 | Named skill evidence | Office-hours/input-contract reflection and heading hygiene | `rg -n "^# " docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` plus repo quality gate | only document title remains as H1; office-hours section present |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Full-scope audit becomes broad runtime change | High | Limit implementation to P1/P2 and defer P3 |
| Skill routing duplicates gateway policy | Medium | Keep `AGENTS.md` thin and record routing in `harness-catalog.md` |
| Static checks are mistaken for live health | Medium | Label live checks as unknown/deferred |
| Optional tools are unavailable locally | Medium | Record skipped reason and CI follow-up |
| Empty root app set passes validation | Medium | Add explicit non-kustomization root app manifest assertion |
| Named design-only review skill conflicts with implementation request | Low | Use the skill as a review lens, record the boundary, and keep implementation governed by the direct task contract |

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

## Coverage Ledger

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

## Integrated Gap Analysis

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

## Implementation Plan

## P1 Low risk / Immediate implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `docs/00.agent-governance/scopes/docs.md` | Add `wiki-curator` to Subagent Bridge | `grill-with-docs`; `agent-md-refactor`; `claude-md-improver` | T-004 | repo quality gate | Revert line |
| improvement | `docs/00.agent-governance/scopes/infra.md` | Add `gitops-reviewer` to Subagent Bridge | `grill-with-docs`; `agent-md-refactor`; `claude-md-improver` | T-004 | repo quality gate | Revert line |
| supplementation | `docs/00.agent-governance/subagent-protocol.md` | Clarify `_workspace/` scratch boundary | `grill-with-docs`; `subagent-driven-development`; `agent-md-refactor` | T-005 | repo quality gate | Revert paragraph |
| addition | spec/task/plan docs | Create traceability docs and indexes | `grill-with-docs`; `documentation-writer`; `doc-coauthoring`; `gstack-document-release`; `humanizer` | T-001 | repo quality gate and link checks | Remove added docs/index entries |
| supplementation | this plan and linked task | Record input reflection audit and exact external skill path check result | `grill-with-docs`; `workspace-harness-audit` | T-010, T-011 | repo quality gate | Revert follow-up sections |
| supplementation | Final Report section layout | Add explicit `Skill and Harness Updates` section | `documentation-writer`; `humanizer`; `workspace-harness-audit` | T-010 | repo quality gate | Revert report section edit |
| supplementation | Implementation Plan skill column | Add row-level `Required skill` evidence for P1/P2/P3 work | `grill-with-docs`; `workspace-harness-audit` | T-013 | repo quality gate | Revert table-column edit |

## P2 Medium risk / Limited implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `scripts/validate-gitops-structure.sh` | Fail when root app manifest count is zero | `bash-scripting`; `senior-devops`; `kubernetes-specialist`; repo-local `k8s-validate` | T-006 | `bash scripts/validate-gitops-structure.sh`; shell syntax | Revert script hunk |
| supplementation | `scripts/README.md` | Document hook simulation bypass as internal | `bash-scripting`; `documentation-writer`; `humanizer` | T-006 | repo quality gate | Revert README paragraph |
| supplementation | `harness-catalog.md` | Add external requested skill routing and skill type boundary | `grill-with-docs`; `agent-md-refactor`; `claude-md-improver` | T-005 | repo quality gate | Revert sections |
| addition | `.claude/skills/workspace-harness-audit/skill.md` and `harness-catalog.md` | Capture repeated workspace-wide audit workflow as repo-local Skill | `writing-skills`; `skill-creator`; `write-a-skill`; `skill-improver` | T-012 | repo quality gate | Remove skill and catalog row |

## P3 High risk / Deferred

| Action type | Target | Deferral reason | Pre-check | Required skill | Follow-up work |
| --- | --- | --- | --- | --- | --- |
| deferral | ESO NetworkPolicy | Kubernetes semantic behavior | Confirm DNS/API egress and live ESO needs | `senior-devops`; `kubernetes-specialist`; `kubernetes-architect`; repo-local `k8s-security-audit` | Separate GitOps manifest task |
| deferral | Vault policy | Secret access policy | Confirm Vault runtime path and rollback | `senior-devops`; `architect-review`; repo-local `k8s-security-audit` | Add HCL plus static test |
| deferral | AppProject app `ExternalSecret` | Permission model change | Confirm onboarding contract | `senior-devops`; `kubernetes-specialist`; repo-local `gitops-workflow` | Update AppProject/examples/docs |
| deferral | Bootstrap CR ownership | ArgoCD ownership design | Decide managed owner model | `senior-architect`; `architecture`; `kubernetes-architect`; repo-local `gitops-workflow` | Architecture and runbook update |
| deferral | GitHub Actions SHA pinning | CI policy decision | Review supply-chain risk | `senior-devops`; `devops-engineer`; `devops-troubleshooter` | Update workflows and inventory |
| deferral | Local Claude settings | Ignored local runtime behavior | Verify precedence | `claude-md-improver`; `agent-md-refactor`; `hook-development` | Tighten local file if needed |
| deferral | Live checks | Requires approved runtime context | Human approval | `senior-devops`; `testing-qa`; `kubernetes-deployment` | Run live read-only tests |
| deferral | Historical raw subagent ledgers | Original raw role outputs are not authoritative current-state files | Future subagent runs must persist raw Summary/Ledger tables into plan/task evidence | `subagent-driven-development`; `workspace-harness-audit` | Enforce through `workspace-harness-audit` skill |

## Input Reflection Follow-up

## Unreflected or Weakly Reflected Input Tasks

| Input task | Existing reflection | Gap judgment | Implementation |
| --- | --- | --- | --- |
| Verify exact required external `SKILL.md` paths and record missing paths as Gaps | Paths were listed in `harness-catalog.md`, but no durable path-check result was recorded | weak reflection | Added path-check result to this plan/task; all listed paths were present in the current WSL environment |
| Create or improve reusable Skills for repeated workflows where appropriate | Repeated routing was consolidated into `harness-catalog.md` only | partial reflection | Added `.claude/skills/workspace-harness-audit/skill.md` and cataloged it |
| Include `Skill and Harness Updates` in the Final Report | Final Report used the shorter later contract | weak reflection | Added the explicit section and kept the rest of the report intact |
| Preserve subagent Summary and Ledger output format | Plan preserves summaries and integrated ledgers, not raw role output tables | partial reflection | Current raw outputs are not reconstructed; future runs must preserve raw role tables through the new Skill workflow |
| Record chosen skill group before each implementation task | Skill routing existed, but implementation plan rows did not carry `Required skill` evidence | weak reflection | Added `Required skill` columns to P1/P2/P3 implementation rows |

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

## Office-Hours Reflection Follow-up

### Application Boundary

`/home/hy/gstack/.agents/skills/gstack-office-hours/SKILL.md` was applied as a
problem-framing and stress-test lens for this follow-up. Its design-doc-only
hard gate conflicts with the active human request to implement the safe plan, so
implementation remains governed by the direct task contract and this repository's
P1/P2/P3 safety rules. The office-hours preamble was not run because it writes
to `~/.gstack` outside the workspace; current repository evidence replaced that
step.

### Infra-Adapted Forcing Questions

| Office-hours question | Repository-specific answer | Result |
| --- | --- | --- |
| Q2 Status quo | The workspace already has Spec 006, linked task/plan, Hybrid Refresh evidence, and static verification, but named `office-hours` application was not durably recorded. | Add plan/task/progress evidence. |
| Q4 Narrowest wedge | The smallest safe implementation is documentation evidence plus skill guardrail updates; no runtime, GitOps, secret, or CI semantics need to change. | Implement P1 docs/skill updates only. |
| Other questions | Product-demand and customer-persona questions are not material for this internal infra governance refresh. | Record as N/A rather than expanding scope. |

### Initial Contract Delta Ledger

| Initial or follow-up requirement | Current reflection | Gap judgment | Action |
| --- | --- | --- | --- |
| Review all entered matters with `grill-with-docs` | `grill-with-docs` was used for previous reflection and Hybrid Refresh, but no office-hours delta table existed. | weak reflection | Add this contract delta ledger and task evidence. |
| Apply `office-hours` review to omissions in the Hybrid Refresh plan | No durable plan/task entry existed for `office-hours`. | gap | Record application boundary and forcing-question result. |
| Consider medium and high risk, not only low risk | P1/P2/P3 tables already preserve low, medium, and high-risk treatment. | complete | Keep high-risk P3 deferrals unchanged. |
| Preserve exact external `SKILL.md` path checks | Hybrid path-level ledger is present and all requested paths are marked present. | complete | No new path check required. |
| Preserve fresh six-role subagent outputs | Hybrid section preserves current read-only role tables. | complete | No subagent rerun required for this delta. |
| Handle template-change impact rules | No `docs/99.templates/` file changed in this implementation series. | N/A recorded | Keep explicit no-template-change note. |
| Apply deletion/consolidation/legacy safeguards | No deletion or consolidation was implemented; candidates remain deferred. | complete | Keep deferred items. |
| Create task-sized commits | Prior work used task-sized commits; this delta is isolated as its own verified commit unit. | complete | Keep this office-hours reflection as a separate commit. |

### Office-Hours Delta Gap Analysis

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Skills/harness | Named `office-hours` review was applied in the conversation but not preserved in durable evidence. | this plan before this section; linked task before T-021 | Future refreshes could repeat the omission. | Low | supplementation | P1 |
| Documentation lifecycle | `Input Reflection Follow-up` remained a post-title H1. | this plan | Heading hierarchy drift weakens template conformance. | Low | consolidation | P1 |
| Skills/harness | `workspace-harness-audit` did not explicitly require named-skill application boundary evidence. | `.claude/skills/workspace-harness-audit/skill.md` | Future named-skill conflicts could stay implicit. | Low | improvement | P1 |

### Office-Hours Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| supplementation | linked plan/task/progress | Record office-hours application boundary, initial-contract delta, verification, and handoff. | `office-hours`; `grill-with-docs`; `workspace-harness-audit`; `documentation-writer` | T-021, T-022, T-023 | repo quality gate; heading check; `git diff --check` | Revert this section and task/progress entries. |
| consolidation | linked plan | Demote remaining post-title H1 to H2. | `workspace-harness-audit`; `documentation-writer` | T-022 | heading check | Revert heading line. |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Require durable named-skill application boundary evidence. | `workspace-harness-audit`; `skill-improver`; `writing-skills` | T-022 | repo quality gate | Revert skill hunk. |

### Office-Hours Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| `office-hours` preamble writing to `~/.gstack` | Writes outside workspace and is not required for repository-static evidence. | Human approval for external write location. | Run only if a future design-doc workflow needs gstack project files. |
| Live k3d/ArgoCD/Vault/ESO checks | High-risk/external runtime boundary remains unchanged. | Explicit read-only live-check approval. | Use the existing P3 live validation plan. |

### Office-Hours Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task Office-Hours summary |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task Office-Hours summary |
| `bash scripts/validate-gitops-structure.sh` | PASS | linked task Office-Hours summary |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task Office-Hours summary |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task Office-Hours summary |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task Office-Hours summary |
| shell syntax check | PASS | linked task Office-Hours summary |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task Office-Hours summary |
| `.env.example` and `.env` key comparison | PASS; key names matched without printing values | linked task Office-Hours summary |
| plan H1 heading check | PASS; only the document title remains as H1 | linked task Office-Hours summary |
| `git diff --check` | PASS | linked task Office-Hours summary |

## Hybrid Refresh - 2026-05-24

### Summary

- Overall status: committed workspace harness artifacts remain valid as the
  baseline, but the fresh review found additional low/medium-risk evidence and
  guardrail gaps that are safe to close without changing Kubernetes, ArgoCD,
  Vault, secret, or CI/CD semantics.
- Largest Gap: live/runtime truth is still unverified and remains out of scope
  without explicit approval; `SessionStart` previously made live read-only
  probes automatic, which conflicted with no-live audit tasks.
- Immediately implementable: status/metadata alignment, plan heading cleanup,
  path-level external skill evidence, `SessionStart` live-probe opt-in,
  scratch ignore coverage, meta runtime ownership wording, and scripts/examples
  evidence freshness.
- Needs deferral: ESO DNS/API egress, Vault `platform/notifications`, app
  `ExternalSecret` AppProject permission, bootstrap CR ownership, GitHub
  Actions SHA pinning, local Claude permission precedence, graphify local
  cleanup, and live k3d/ArgoCD/Vault/ESO validation.
- Unknown areas: live runtime health, `.env` value freshness, remote CI/ruleset
  state, optional toolchain coverage, `.agent/` absence intent, and ignored
  graphify ownership.

### Hybrid Coverage Ledger

| Area | Target path | Investigation status | Representative files read | Gap count | Deletion/consolidation/deferral candidate count | Unknown items | Next action |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| Documentation lifecycle | `docs/00.agent-governance/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`, `docs/99.templates/` | complete | spec/plan/task, stage READMEs, templates, progress ledger | 6 | 5 | live runtime, `.agent/`, optional toolchain | Align status/metadata/headings and preserve fresh outputs |
| Agent governance | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.codex/`, `.agents/`, `.agent/` | partial | gateway shims, runtime baseline, settings, hooks, scope files, harness catalog | 6 | 8 | permission precedence, no-live hook behavior, graphify intent | Implement opt-in live probes and ownership wording |
| Scripts | `scripts/` | complete | `scripts/README.md`, five shell scripts, CI/hook references | 3 | 5 | scanner fixtures, optional lint tools | Refresh inventory date and keep validator hardening |
| GitOps infrastructure | `gitops/`, `infrastructure/`, `traefik/`, `examples/` | partial | root apps, AppProjects, ESO/Vault manifests, examples READMEs, Traefik README | 8 | 8 | live ArgoCD/Vault/ESO, cloud latest | Defer semantic changes; refresh examples evidence wording |
| Environment/QA/CI | `.env.example`, `.env`, `.github/`, `.pre-commit-config.yaml`, `tests/`, `infrastructure/tests/` | partial | env key comparison, workflows, static tests, QA READMEs | 5 | 6 | `.env` values, remote CI/rulesets, optional tools | Keep static verification; defer live and policy checks |
| Skills/harness | `.claude/skills/`, `.agents/skills/`, hooks, subagent protocol, harness catalog | partial | `workspace-harness-audit`, skill catalog, hooks, `.gitignore` | 7 | 7 | local mirrors, raw historical ledgers, Codex provider note intent | Add path-level skill ledger and scratch guardrail |

### Hybrid Integrated Gap Analysis

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Documentation lifecycle | Spec status was `draft` while stage README marked the spec `Active` | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/README.md` | Lifecycle promotion ambiguity | Medium | improvement | P1 |
| Documentation lifecycle | Plan had multiple H1 sections after the document title | `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` | Template/heading consistency drift | Low | consolidation | P1 |
| Documentation lifecycle | Harness catalog and subagent protocol metadata lagged current 2026-05-24 content | `docs/00.agent-governance/harness-catalog.md`; `docs/00.agent-governance/subagent-protocol.md` | Freshness evidence weaker | Low | improvement | P1 |
| Agent governance | `SessionStart` hook ran live read-only `k3d`/`kubectl get` probes automatically | `.claude/hooks/session-start.sh`; `.claude/settings.json`; `.codex/hooks.json` | No-live audit tasks can touch live state before approval | Medium | improvement | P2 |
| Agent governance | Meta scope did not explicitly own tracked hook/skill/Codex runtime contract surfaces | `docs/00.agent-governance/scopes/meta.md`; `harness-catalog.md` | Runtime ownership ambiguity | Low | supplementation | P1 |
| Skills/harness | External `SKILL.md` path evidence was area-level, not path-by-path | `harness-catalog.md`; linked task | Missing-path audit replayability weaker | Low | supplementation | P1 |
| Skills/harness | `_workspace/` scratch paths were allowed by skills/protocol but not ignored | `.claude/skills/incident-postmortem/skill.md`; `.gitignore`; `subagent-protocol.md` | Temporary scratch files could be staged | Medium | improvement | P2 |
| Skills/harness | Workflow/reference-pattern skill distinction lacked per-skill metadata | `harness-catalog.md` | Skill review expectations can drift | Low | supplementation | P1 |
| Scripts | `scripts/README.md` retained 2026-05-17 inventory wording after 2026-05-24 hardening | `scripts/README.md`; linked task | Evidence freshness weaker | Low | improvement | P1 |
| GitOps infrastructure | Examples snapshot wording mixed older dates with the current version inventory | `examples/README.md`; `examples/aws/docs/README.md`; `examples/azure/docs/README.md`; `docs/90.references/versions/tech-stack-version-inventory.md` | Cloud examples freshness evidence weaker | Low | supplementation | P1 |
| GitOps infrastructure | ESO DNS/API egress remains unresolved | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml` | ESO reconciliation risk | High | deferral | P3 |
| GitOps infrastructure | Vault policy lacks `platform/notifications` coverage | `infrastructure/vault/policies/eso-read.hcl`; `argocd-notifications-secret.yaml` | Notification secret sync risk | High | deferral | P3 |
| GitOps infrastructure | AppProject and sample app ExternalSecret contract remain inconsistent | `appproject-apps.yaml`; `examples/sample-app/external-secret.yaml` | App onboarding drift | Medium | deferral | P3 |
| CI/CD | GitHub Actions SHA pinning and skipped-job/ruleset behavior need policy review | `.github/workflows/ci.yml`; `.github/zizmor.yml` | Supply-chain and required-check ambiguity | Medium | deferral | P3 |

### Hybrid Implementation Plan

#### P1 Low risk / Immediate implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | Set status to `active` and add hybrid refresh acceptance criterion | `grill-with-docs`; `documentation-writer`; `workspace-harness-audit` | T-016 | repo quality gate | Revert status/criterion |
| consolidation | linked plan | Demote post-title H1 sections and add Hybrid Refresh evidence | `grill-with-docs`; `documentation-writer`; `humanizer` | T-014, T-016 | repo quality gate | Revert heading/evidence section |
| supplementation | linked plan/task | Preserve fresh role review outputs and path-level external skill checks | `grill-with-docs`; `subagent-driven-development`; `workspace-harness-audit` | T-014, T-015 | repo quality gate | Revert Hybrid Refresh sections |
| supplementation | `docs/00.agent-governance/scopes/meta.md` | Clarify meta ownership of hooks, skills, Codex wiring, and supervisor exception | `claude-md-improver`; `agent-md-refactor`; `workspace-harness-audit` | T-017 | repo quality gate | Revert scope wording |
| improvement | `docs/00.agent-governance/harness-catalog.md`, `subagent-protocol.md` | Refresh metadata and add per-skill contract type | `claude-md-improver`; `agent-md-refactor`; `skill-improver` | T-017 | repo quality gate | Revert metadata/table changes |
| improvement | `scripts/README.md`, `examples/README.md`, cloud docs READMEs | Refresh evidence wording without changing examples or scripts | `documentation-writer`; `humanizer`; `grill-with-docs` | T-018 | repo quality gate | Revert wording |

#### P2 Medium risk / Limited implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `.claude/hooks/session-start.sh` | Make live k3d/kubectl startup probes opt-in via `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1` | `hook-development`; `writing-rules`; `agent-md-refactor` | T-019 | shell syntax; repo quality gate | Revert hook guard |
| improvement | `.gitignore` | Ignore `_workspace/` and `_workspace_prev/` scratch directories | `workspace-harness-audit`; `agent-md-refactor` | T-019 | repo quality gate; `git status` | Revert ignore lines |

#### P3 High risk / Deferred

| Action type | Target | Deferral reason | Required pre-check | Required skill | Follow-up work |
| --- | --- | --- | --- | --- | --- |
| deferral | ESO NetworkPolicy DNS/API egress | Kubernetes semantic change | Confirm DNS/API targets and live ESO behavior | `senior-devops`; `kubernetes-specialist`; `k8s-security-audit` | Separate manifest task |
| deferral | Vault `platform/notifications` policy | Secret access policy change | Confirm Vault path and rollback | `senior-devops`; `architect-review`; `k8s-security-audit` | Separate security/GitOps task |
| deferral | AppProject ExternalSecret permission and sample key format | App onboarding permission/secret model change | Decide intended app secret onboarding model | `gitops-workflow`; `kubernetes-specialist`; `architect-review` | Update AppProject/examples/docs together |
| deferral | `gitops/clusters/local` bootstrap CR ownership | ArgoCD ownership design change | Choose bootstrap-owned vs reconciled owner model | `senior-architect`; `kubernetes-architect`; `gitops-workflow` | Separate architecture/runbook plan |
| deferral | GitHub Actions SHA pinning and skipped-job policy | CI/CD policy change | Review supply-chain and branch ruleset requirements | `senior-devops`; `devops-engineer`; `devops-troubleshooter` | Separate CI governance task |
| deferral | `.claude/settings.local.json` broad allows | Ignored local runtime precedence unknown | Verify Claude settings precedence without destructive commands | `claude-md-improver`; `hook-development`; `agent-md-refactor` | Local hardening task |
| deferral | Live k3d/ArgoCD/Vault/ESO validation | Requires live runtime context | Explicit approval and read-only command scope | `senior-devops`; `testing-qa`; `kubernetes-deployment` | Run live validation scripts |

### Hybrid Path-Level External Skill Check

| Skill path | Result |
| --- | --- |
| `/home/hy/.agents/skills/grill-with-docs/SKILL.md` | present |
| `/home/hy/.agents/skills/documentation-writer/SKILL.md` | present |
| `/home/hy/.agents/skills/humanizer/SKILL.md` | present |
| `/home/hy/gstack/.agents/skills/gstack-document-release/SKILL.md` | present |
| `/home/hy/.agents/skills/technical-blog-writing/SKILL.md` | present |
| `/home/hy/.agents/skills/doc-coauthoring/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-skills/SKILL.md` | present |
| `/home/hy/.codex/trailofbits-skills/plugins/skill-improver/skills/skill-improver/SKILL.md` | present |
| `/home/hy/.agents/skills/skill-creator/SKILL.md` | present |
| `/home/hy/.agents/skills/write-a-skill/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/subagent-driven-development/SKILL.md` | present |
| `/home/hy/.agents/skills/hook-development/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/hookify/local/skills/writing-rules/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/claude-md-management/1.0.0/skills/claude-md-improver/SKILL.md` | present |
| `/home/hy/.agents/skills/claude-md-improver/SKILL.md` | present |
| `/home/hy/.agents/skills/agent-md-refactor/SKILL.md` | present |
| `/home/hy/.agents/skills/bash-scripting/SKILL.md` | present |
| `/home/hy/.agents/skills/senior-devops/SKILL.md` | present |
| `/home/hy/.agents/skills/senior-architect/SKILL.md` | present |
| `/home/hy/.agents/skills/architect-review/SKILL.md` | present |
| `/home/hy/.agents/skills/architecture/SKILL.md` | present |
| `/home/hy/.agents/skills/kubernetes-specialist/SKILL.md` | present |
| `/home/hy/.agents/skills/kubernetes-architect/SKILL.md` | present |
| `/home/hy/.agents/skills/kubernetes-deployment/SKILL.md` | present |
| `/home/hy/.agents/skills/senior-qa/SKILL.md` | present |
| `/home/hy/.agents/skills/testing-qa/SKILL.md` | present |
| `/home/hy/.codex/trailofbits-skills/plugins/testing-handbook-skills/skills/coverage-analysis/SKILL.md` | present |
| `/home/hy/.agents/skills/devops-engineer/SKILL.md` | present |
| `/home/hy/.agents/skills/devops-troubleshooter/SKILL.md` | present |

### Hybrid Raw Subagent Output Preservation

The six fresh role reviews were rerun in read-only mode and are preserved below
in the requested table shape. The original subagent messages used absolute
paths in several cells; this plan keeps the same evidence targets while using
repository-relative paths where that improves readability.

#### Documentation Lifecycle Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| SDD chain is connected, but Spec lifecycle state conflicted with the index: Spec `draft`, README `Active`, Plan/Task `done`. | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/README.md`; linked plan/task | Lifecycle promotion ambiguity | Medium | partial | Align spec status and index state. |
| Current Plan preserves required evidence, but used multiple H1 sections after the document title. | linked plan | Heading hierarchy weakened template consistency | Low | partial | Demote appended report sections while preserving content. |
| README freshness for current Spec/Plan/Task artifacts is good. | `docs/03.specs/README.md`; `docs/04.execution/plans/README.md`; `docs/04.execution/tasks/README.md` | Navigation intact | Low | complete | Keep current indexes. |
| Original raw role Summary/Ledger tables were not durably archived. | linked plan; `memory/progress.md` | Replayability weaker than prompt contract | Medium | partial | Preserve fresh role tables in this Hybrid Refresh; keep historical gap noted. |
| P3 runtime, secret-policy, GitOps ownership, CI, and live validation remain deferred or unknown. | linked plan; `memory/progress.md` | Static docs cannot prove live readiness | High | partial | Keep separate owner-approved follow-up work. |
| Harness governance content was newer than metadata dates. | `harness-catalog.md`; `subagent-protocol.md` | Freshness metadata under-reported content | Low | partial | Refresh metadata when editing. |
| External skill path evidence was area-level rather than path-by-path. | linked plan; `harness-catalog.md`; linked task | Replayability weaker | Low | partial | Store path-by-path results. |

#### Documentation Lifecycle Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | Template sections, related links, and verification plan are present; lifecycle state needed alignment. | partial | spec and `docs/03.specs/README.md` | Spec template and stage index checked | Align status and README state. |
| linked plan | Coverage, gap analysis, input reflection, verification, and final report are present; heading hierarchy was noncanonical. | partial | linked plan | Plan template headings checked | Normalize headings. |
| linked task | Task IDs T-001 through T-013, verification summary, skipped checks, and related links are recorded. | complete | linked task | Task template checked | Keep as baseline evidence. |
| `memory/progress.md` | Progress entries capture the gap-analysis pass and input-reflection follow-up. | complete | progress ledger | Progress coupling checked | Append for future repo-changing work. |
| `harness-catalog.md` | Workspace harness skill and task-to-skill routing are cataloged; metadata date was stale. | partial | harness catalog | Runtime roster SSoT checked | Refresh metadata. |
| `subagent-protocol.md` | Scratch workspace boundary is captured; metadata date was stale. | partial | subagent protocol | Protocol checked | Refresh metadata. |
| `.claude/skills/workspace-harness-audit/skill.md` | Broad audit Skill covers inventory, skill paths, raw ledger preservation, and P3 deferral. | complete | skill file | Baseline skill checked | Use for future broad refreshes. |
| Scoped README files | Current Spec/Plan/Task indexes satisfy scoped README contract. | complete | stage READMEs | Link/section scan checked | Keep current. |
| Legacy references | Legacy path references appear in routing policy, templates, historical context, or migration guidance. | complete | governance/templates/historical plans | Legacy scan checked | Retain documented migration references. |
| Current validation evidence | Baseline records PASS results; fresh validation must be rerun after edits. | partial | linked task/progress | Existing evidence checked | Rerun static gates. |

#### Documentation Lifecycle Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| linked plan report sections | consolidation | Multiple post-template H1 sections fragmented one Plan document. | linked plan | Plan readability and template conformance | Demote headings. |
| historical raw subagent ledgers | deferral | Raw role output format was acknowledged missing from earlier durable evidence. | linked plan; progress | Audit replayability | Preserve fresh tables now; do not reconstruct older unavailable outputs. |
| legacy/superseded docs | retain | Historical records remain referenced and replacement context exists. | linked plan; spec README | Architecture and operations history | Do not delete. |
| P3 GitOps/Vault/CI/live items | deferral | Require semantic/runtime or owner-approved checks. | linked plan/progress | Runtime readiness | Track as separate tasks. |
| `.agents/rules/graphify.md`, `.agents/workflows/graphify.md` | deletion candidate | Ignored local surfaces are local-only drift. | linked plan | Local context only | Defer owner decision. |

#### Documentation Lifecycle Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live k3d/ArgoCD/Vault/ESO health | Live commands were not approved or run. | Run owner-approved read-only live validation. |
| `.env` value freshness | Values were intentionally not read or printed. | Human-only secret review. |
| GitHub branch protection/rulesets | Not represented in the worktree. | Inspect repository settings through approved GitHub path. |
| Optional local toolchain current state | Baseline recorded missing optional tools; refresh did not run all optional tool checks. | Recheck in CI or provisioned local shell. |
| `.agent/` absence | Missing path intent is not proven. | Owner decision or governance note. |
| Current external `SKILL.md` path existence | Docs reviewer did not recheck filesystem paths directly. | Use the path-level check in this Hybrid Refresh. |

#### Agent Governance Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Gateway thinness and native instruction priority are mostly coherent. | `AGENTS.md`; `CLAUDE.md`; `GEMINI.md`; `.claude/CLAUDE.md` | Root files route instead of duplicating policy | Low | keep | Keep routing in `harness-catalog.md` and skills. |
| Local Claude settings remain the largest provider/runtime ambiguity. | `.claude/settings.local.json`; `.claude/settings.json` | Local allows may conflict with shared deny boundaries | Medium | defer | Verify precedence before local hardening. |
| SessionStart hook could run live read-only probes automatically. | `.claude/hooks/session-start.sh`; `.claude/settings.json`; `.codex/hooks.json` | No-live tasks could touch live state | Medium | supplement | Make probes opt-in or approval-gated. |
| Broad workspace audit workflow is correctly outside the gateway. | `.claude/skills/workspace-harness-audit/skill.md`; `harness-catalog.md` | Reduces prompt drift | Low | keep | Continue using the Skill. |
| Historical raw subagent ledgers remain weak evidence. | linked plan; progress | Replayability weaker | Medium | defer | Preserve current raw tables. |
| Runtime ownership is partly implicit for skills, hooks, and Codex files. | `scopes/meta.md`; `harness-catalog.md` | Role separation can be ambiguous | Low | supplement | Clarify meta/runtime ownership language. |

#### Agent Governance Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Thin gateway/provider shims. | complete | root shims | line-count and routing checked | Preserve. |
| `.claude/CLAUDE.md` | Runtime baseline clear; no-live interaction with SessionStart needed clarification. | partial | runtime baseline and hook | no-live opt-out absent | Add guard/documentation. |
| `CLAUDE.local.md` | Not present. | complete | workspace root | absence checked | No action. |
| `.agent/` | Path absent. | unknown | `.gitignore`; linked plan | intent unknown | Keep unknown; do not create. |
| `.agents/skills/**` | Existing local mirrors are non-canonical; new workspace skill mirror absence is acceptable. | complete | `.agents/skills/`; `.claude/skills/`; catalog | mirror policy checked | Keep ignored. |
| `.agents/rules`, `.agents/workflows` | Local graphify guidance can drift. | partial | ignored `.agents/` files | ignored/untracked | Defer owner decision. |
| `.claude/settings.json` | Shared settings block mutation families and wire hooks. | complete | settings JSON | mutation deny present | Keep. |
| `.claude/settings.local.json` | Broad local allows need precedence review. | partial | local settings | ignored/local-only | Verify precedence. |
| `.claude/hooks/session-start.sh` | Live read-only probes were automatic. | partial | hook script | read-only but live | Make opt-in. |
| `.claude/hooks/post-validate.sh`, lifecycle hooks | Static validation and lifecycle checks are scoped. | complete | hook scripts | shared validation surface | Preserve. |
| `.claude/agents/**`, `.codex/agents/**` | Eight Claude agents have matching Codex mirrors. | complete | agent folders | pair inventory complete | Preserve same-change mirror rule. |
| `.codex/hooks.json` | Reuses Claude hooks as context/validation wiring. | complete | Codex hooks | boundary documented | Preserve. |
| `harness-catalog.md` | Centralizes skill routing and readiness semantics. | complete | catalog | external skill paths present | Keep SSoT. |
| `workspace-harness-audit` skill | Captures repeated broad audit workflow. | complete | skill file | covers path checks and P1/P2/P3 | Use for next refresh. |
| `subagent-protocol.md` | Dispatch and scratch boundary explicit. | complete | protocol | role separation preserved | Preserve. |
| `meta.md` scope | Runtime file ownership wording was weak. | partial | meta scope | documentation-level gap | Clarify ownership. |

#### Agent Governance Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.claude/settings.local.json` | deferral | Local broad allows may weaken shared boundaries depending on precedence. | local/shared settings | Local Claude runtime | Verify precedence, then narrow if needed. |
| `.claude/hooks/session-start.sh` | consolidation | Live probes belonged behind explicit no-live/opt-in behavior. | hook and settings | Claude/Codex startup | Add opt-in guard. |
| `.agents/rules/graphify.md` | deletion candidate | Ignored local rule can generate drift. | `.gitignore` | Local operator context | Defer owner decision. |
| `.agents/workflows/graphify.md` | deletion candidate | References external graphify skill outside repo SSoT. | `.gitignore` | Local operator context | Defer owner decision. |
| runtime file ownership | consolidation | Hook/skill/Codex ownership was not explicit in scope ownership. | meta scope/catalog | Governance role separation | Clarify. |
| historical raw subagent ledgers | deferral | Earlier raw tables not durable current-state files. | linked plan/skill | Replayability | Preserve future/current raw tables. |
| `.agent/` | deferral | Path absent and ignored, intent unknown. | `.gitignore` | Local runtime discovery | Keep absent unless requested. |

#### Agent Governance Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Claude local/project permission precedence | Broad local settings were not live-tested. | Verify without destructive commands. |
| No-live task handling for SessionStart | Hook opt-out was not documented before this change. | Validate opt-in behavior. |
| `.agent/` absence | Missing path intent is unknown. | Ask owner before creating. |
| Live k3d/ArgoCD/Vault/ESO health | Live commands prohibited. | Run only after approval. |
| GitHub branch protection/rulesets | Not in worktree. | Inspect GitHub settings separately. |
| `.env` value freshness | Secret values intentionally not read. | Human-only review. |
| Graphify local surfaces owner intent | Ignored local files may be intentional or stale. | Ask owner. |

#### Scripts Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Current `scripts/` inventory is five shell scripts; no one-off or unknown script found. | `scripts/README.md`; `scripts/` | Deletion scope stays narrow | Low | keep | Retain scripts. |
| Four scripts are operations-critical validators; LLM Wiki generator is reusable helper with `--check`. | `scripts/README.md`; CI; hooks | Avoids cleanup misclassification | Low | keep | Preserve contracts. |
| GitOps root app validator hardening is implemented. | `validate-gitops-structure.sh`; linked task | Empty root app set fails statically | Low | verify | Keep root app count assertion. |
| Hook simulation bypass is internal-only. | `scripts/README.md`; hooks; quality gate | Reduces misuse | Low | keep | Keep manual validation unbypassed. |
| Script command-reference validation is allowlist-scoped. | `scripts/README.md`; quality gate | New reference surfaces can drift | Medium | monitor | Update allowlist with new script surfaces. |
| `scripts/README.md` used a 2026-05-17 inventory snapshot after 2026-05-24 hardening. | `scripts/README.md`; linked plan | Evidence freshness weaker | Low | refresh evidence | Refresh wording. |
| Secret scanner tolerance lacks fixture coverage. | `check-secret-handling.sh`; `tests/README.md` | False positive/negative regressions can hide | Medium | test hardening | Add fixtures only in scanner task. |
| Optional local toolchain unavailable. | QA docs and task | Local validation limited | Medium | deferral | Treat optional tools as CI/provisioned evidence. |

#### Scripts Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `validate-repo-quality-gates.sh` | Central governance validator tied to CI, hooks, inventory, docs contracts, and simulations. | operations-critical/reusable | script | CI, hooks, README | Keep; split only preserving public command. |
| `validate-gitops-structure.sh` | Checks root app existence, kind, count, kustomization parsing, and completeness. | operations-critical/reusable | script | CI, PR template, GitOps README | Preserve zero-root-app semantics. |
| `validate-k8s-manifests.sh` | YAML parser with optional kube-linter. | operations-critical/reusable | script | CI, hooks, tests README | Report optional kube-linter skip. |
| `check-secret-handling.sh` | Plaintext-secret scanner redacts matched values. | operations-critical/reusable | script | CI, hooks, PR template | Add fixtures before broadening. |
| `generate-llm-wiki-index.sh` | Generated index helper; `--check` is quality-gate mode. | development-helper/reusable | script | quality gate, LLM Wiki docs | Keep; use `--check` for read-only checks. |
| `scripts/README.md` | Inventory, retention tiers, command contracts, tools, and bypass warning present. | reusable | README | root README, PR template, tests README | Refresh evidence date. |

#### Scripts Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `scripts/*.sh` | no deletion candidate | All five scripts have Tier A or B retention evidence. | README, CI, hooks | CI/hooks/manual validation | Do not delete. |
| `validate-repo-quality-gates.sh` | deferral | Large validator but high blast radius if split casually. | script and CI | Repo governance gate | Defer splitting. |
| `check-secret-handling.sh` | deferral | Regex behavior lacks fixtures. | scanner and tests README | Secret static gate | Add fixtures in dedicated task. |
| `validate-k8s-manifests.sh` | deferral | Optional kube-linter unavailable locally. | validator and tests README | Manifest validation | Confirm lint in CI/toolchain. |
| `scripts/README.md` | evidence refresh | Snapshot date predates 2026-05-24 hardening. | README and linked plan | Reviewer evidence | Refresh wording. |

#### Scripts Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live k3d/ArgoCD/Vault/ESO health | Live commands out of scope. | Separate approved read-only checks. |
| `.env` value freshness | Secret values not inspected. | Human-only review. |
| Secret scanner tolerance | No fixture suite run or created. | Add positive/negative fixtures before scanner changes. |
| Remote CI/ruleset state | Worktree cannot prove GitHub settings. | Inspect GitHub checks/settings if needed. |
| Optional toolchain coverage | Optional tools unavailable. | Run in CI/provisioned shell. |

#### GitOps Infrastructure Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Static GitOps/manifests baseline is structurally healthy. | validators and static tests | Root App-of-Apps, Kustomize, YAML, contracts, secret scan pass | Low | keep | Keep static gates as merge prerequisites. |
| ESO egress policy is narrower than adjacent namespace policies. | `external-secrets-egress-to-vault.yaml`; adjacent policies | ESO may need DNS/API egress | High | deferred fix | Separate GitOps task with live ESO validation. |
| Vault policy lacks ArgoCD notifications path. | `eso-read.hcl`; notifications ExternalSecret | Slack token sync can fail | High | deferred fix | Add policy in separate security change. |
| Apps AppProject omits ExternalSecret while onboarding example includes it. | `appproject-apps.yaml`; sample app | Secret-backed app can be rejected | Medium | deferred fix | Decide onboarding model first. |
| Sample app Vault key format differs from active ClusterSecretStore usage. | sample ExternalSecret; platform ESO manifests | Copy-paste onboarding risk | Medium | consolidation | Align sample in separate app onboarding task. |
| Bootstrap CR ownership split remains. | bootstrap script and cluster manifests | Drift possible | High | design deferral | Decide owner model. |
| Cloud example freshness evidence is mixed. | examples READMEs; version inventory | Weak freshness evidence | Low | evidence refresh | Normalize wording to inventory. |
| Original raw subagent ledger preservation remained weak. | linked plan/progress/skill | Replayability weaker | Medium | future-process fix | Preserve fresh tables. |

#### GitOps Infrastructure Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `gitops/apps/root` | 17 non-kustomization ArgoCD Application manifests. | pass | root kustomization and validator | GitOps structure PASS | Keep assertion. |
| `gitops/clusters/local/root-application.yaml` | Root app targets `gitops/apps/root` on `main`. | pass | root application | Static contract PASS | Keep entrypoint. |
| `applicationset-apps.yaml` | Workload ApplicationSet uses project `apps`; ExternalSecret caveat remains. | pass with caveat | ApplicationSet/AppProject | Static PASS | Fix secret model separately. |
| `appproject-apps.yaml` | Allows workloads but omits `external-secrets.io/ExternalSecret`. | gap | AppProject and sample | P3 already recorded | Update after decision. |
| ESO egress policy | Allows only Vault IP/port. | gap | NetworkPolicy | Compared adjacent policies | Separate task. |
| Vault ESO policy | Omits `platform/notifications`. | gap | Vault HCL and ExternalSecret | Static contract partial | Separate task. |
| external service contracts | PostgreSQL, Vault, Valkey contracts present. | pass | platform external services | static contract PASS | Keep; live unknown. |
| k3d config | Matches version inventory and disables bundled Traefik/servicelb. | pass | k3d config/version inventory | YAML PASS | Keep. |
| `traefik/` | Reference-only helper boundary is clear and YAML valid. | pass | Traefik README/configs | YAML PASS | Keep separate from GitOps. |
| `examples/sample-app` | ExternalSecret excluded from sample kustomization by default. | pass with caveat | sample app | syntax/secret scan PASS | Keep disabled until model fixed. |
| `examples/aws`, `examples/azure` | Reference-only boundary documented; snapshot wording lagged inventory. | weak evidence | examples READMEs and version inventory | repo-static only | Refresh wording. |

#### GitOps Infrastructure Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| AppProject `Namespace` whitelist | deletion candidate | Namespace appears platform-owned while ApplicationSet uses `CreateNamespace=true`. | platform namespace and ApplicationSet | AppProject least privilege | Defer. |
| `gitops/clusters/local` bootstrap resources | consolidation | AppProject/ApplicationSet/root app are bootstrap-applied. | bootstrap script and manifests | Bootstrap/ownership | Separate design task. |
| sample ExternalSecret | consolidation | RemoteRef key format includes mount prefix unlike active platform pattern. | sample and platform ESO | App onboarding | Separate app onboarding task. |
| Vault policy | deferral | Adding notifications changes secret access policy. | HCL and ExternalSecret | Vault/ESO/ArgoCD | Separate security change. |
| ESO egress policy | deferral | DNS/API egress is runtime semantic change. | NetworkPolicy | ESO reconciliation | Separate NetworkPolicy task. |
| examples snapshot wording | consolidation | Mixed date evidence. | examples and version inventory | Cloud references | Refresh wording. |
| `traefik/` | keep | Reference-only helper boundary explicit. | README and YAML | Local UI helper | Retain. |

#### GitOps Infrastructure Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live k3d, ArgoCD, ESO, Vault, PostgreSQL, Valkey, TLS, and NetworkPolicy behavior | Live commands out of scope. | Approved live validation only. |
| Vault secret value freshness | Values not inspected. | Secret-safe operator review. |
| Official cloud latest support state | External provider freshness not queried. | Refresh version inventory from official sources. |
| kube-linter findings | Optional tool unavailable. | Run in prepared environment. |
| GitHub rulesets and remote CI | Not in worktree. | Separate CI/governance review. |

#### Environment Quality Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.env.example` and local `.env` key names match; `.env` remains ignored/untracked. | env files and `.gitignore` | Template consistency intact without values | Low | keep | Keep key-name-only comparison. |
| Static quality gates passed in read-only refresh. | validators and static tests | Committed baseline structurally healthy | Low | keep | Continue static gate bundle. |
| Secret handling has static layers, but live Vault/ESO remains deferred. | pre-commit, gitleaks, secret scanner, plan | Runtime secret reconciliation not proven | High | defer | Separate approved live checks. |
| Local lint toolchain incomplete. | pre-commit, tests README, scripts README | Local review cannot reproduce all lint/security checks | Medium | improve | Install tools or rely on CI. |
| Workflows are structurally checked, but actions are tag-pinned with `unpinned-uses` disabled. | workflows, zizmor, quality gate | Supply-chain hardening remains policy decision | Medium | defer | Decide SHA pinning separately. |
| Path-filtered CI jobs can skip by design. | CI workflow | Skipped-check interpretation depends on branch protection | Medium | verify | Confirm rulesets. |
| Raw subagent ledgers were not reconstructed historically. | plan and skill | Replayability weaker | Medium | defer | Preserve fresh tables. |
| Live QA scripts exist but were not run. | infrastructure live tests | Runtime health unknown | High | defer | Run only after approval. |

#### Environment Quality Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.env.example`, `.env` | Key names match; values not printed. | pass | env files | key-name-only comparison | Keep. |
| `.env` tracking | `.env` ignored and untracked; `.env.example` tracked. | pass | `.gitignore`; env template | git ls-files check | Keep local-only. |
| Secret scanners | Gitleaks, detect-secrets, and manifest scanner configured. | coverage | configs and scanner | secret scan PASS | Keep layered static scan. |
| manifest validation | YAML passes; kube-linter optional and skipped locally. | skipped check risk | validator and config | manifest check PASS with skip | Install or use CI evidence. |
| CI workflow | Required jobs and summary present. | pass | workflow and gate | quality gate PASS | Keep dependencies. |
| workflow syntax | YAML parser passes; actionlint unavailable locally. | partial | workflow/pre-commit | local actionlint missing | Verify in CI/toolchain. |
| action pinning | Tag pins accepted by current config. | deferred risk | zizmor/workflows/inventory | quality gate allows only disable | Decide SHA policy separately. |
| test model | Static infra validation, no app unit/typecheck stack. | context | tests/scripts READMEs | no app config found | Add tests when app code exists. |
| static contracts | Infra static contracts pass. | pass | static contract script | PASS | Keep. |
| live tests | Live scripts call runtime surfaces and were not run. | deferred | infrastructure live tests | not executed | Run with approval. |

#### Environment Quality Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| GitHub Actions SHA pinning | deferral | SHA pinning stronger than current tag policy. | `.github/zizmor.yml` | CI supply chain | Separate task. |
| Local optional QA tools | deferral | Tooling not installed. | pre-commit config | Local QA parity | Install or use CI. |
| Live runtime checks | deferral | Live scripts require prohibited runtime commands. | live test scripts | Runtime QA | Approved read-only pass. |
| historical raw subagent ledgers | deferral | Earlier docs summarized role outputs only. | linked plan | Replayability | Preserve fresh tables. |
| `.env` value freshness | deferral | Secret-sensitive. | linked plan | Environment correctness | Human-only review. |
| CI skipped-job interpretation | improvement candidate | Path filters and rulesets interact outside worktree. | workflow and GitHub docs | CI governance | Verify rulesets. |

#### Environment Quality Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| `.env` value correctness | Values intentionally not inspected. | Human-only review. |
| Live k3d/ArgoCD/Vault/ESO health | Live commands out of scope. | Approved read-only validation. |
| Remote CI run status | Remote checks not queried. | Inspect GitHub checks. |
| Full local pre-commit result | `pre-commit` unavailable. | Run in prepared toolchain or CI. |
| Full workflow lint/security result | `actionlint` and `zizmor` unavailable locally. | Run CI/pre-commit jobs. |
| kube-linter semantic result | `kube-linter` unavailable. | Install or use CI. |
| Historical raw role tables | Earlier committed files lack authoritative raw tables. | Preserve tables during current/future audits. |

#### Skills & Harness Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Agent and Codex mirror surfaces are structurally aligned; repo quality gate passed. | quality gate; `.claude/agents/`; `.codex/agents/` | No tracked mirror drift | Low | keep | Keep mirror checks. |
| External `SKILL.md` paths are recorded and present, but durable verification was grouped by area. | catalog, plan, task | Path replayability weaker | Low | evidence hardening | Add path-level ledger. |
| `workspace-harness-audit` captures broad audit workflow; historical raw ledgers remain deferred. | skill and plan | Future protected, original less replayable | Medium | deferral | Keep deferral and preserve fresh raw tables. |
| SessionStart hooks ran live probes automatically. | hook/settings/Codex hooks/spec | Live state could be touched before approval | Medium | hook boundary | Make probes opt-in. |
| Local Claude settings allow broad command families. | local settings and local Hookify rules | Shared deny boundary may be weakened if precedence wins | High | governance check | Verify and harden later. |
| `_workspace/` scratch paths are authorized but not ignored. | incident/RCA skills, protocol, `.gitignore` | Scratch files could be staged | Medium | guardrail | Add ignore/check coverage. |
| Meta scope says no dedicated subagent while supervisor imports meta. | meta scope; supervisor; catalog | Routing wording ambiguous | Low | documentation fix | Clarify supervisor exception. |
| Workflow/reference distinction is prose only. | catalog and skill files | Reviewers may apply wrong checklist expectations | Low | catalog refinement | Add per-skill type column. |
| Governance document dates were stale. | catalog, protocol, progress | Freshness signals weaker | Low | metadata fix | Refresh metadata. |

#### Skills & Harness Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `workspace-harness-audit` skill | Reusable broad audit workflow exists. | confirmed OK | skill and catalog | contract checked | Keep. |
| External requested skills | All checked paths present; committed evidence was area-level. | weak evidence | catalog/plan | path check | Store path-level results. |
| `.agents/skills/` | Local mirrors are ignored/non-canonical. | local-only | `.agents/skills/`; `.claude/skills/` | validator checks existing mirrors | No tracked action. |
| graphify local files | Ignored graphify workflow remains outside repo SSoT. | deferral | `.agents/`; `.claude/CLAUDE.md` | local-only | Defer owner decision. |
| SessionStart hook | Performs live `k3d`/`kubectl get` checks automatically. | confirmed gap | hook/settings/Codex hooks | live checks deferred in spec/plan | Gate behind opt-in. |
| local settings | Broad local allows include destructive/live families. | local risk | settings.local | Hookify warns only | Verify precedence. |
| scratch boundary | `_workspace/` and `_workspace_prev/` named but not ignored. | guardrail gap | skills/protocol/gitignore | absent now | Ignore or validate cleanup. |
| meta/supervisor bridge | Supervisor imports `meta` while meta says no dedicated subagent. | wording drift | supervisor and meta scope | other bridge rows ok | Clarify. |
| raw subagent ledgers | Original role output tables not durably archived. | deferred evidence gap | plan/skill | plan records limitation | Preserve current/future tables. |
| skill type distinction | Catalog lacked per-skill type metadata. | weak routing | catalog and skills | reference skills differ | Add type column. |

#### Skills & Harness Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.claude/hooks/session-start.sh` live probes | consolidation | Live health checks were automatic hook behavior. | spec and hook | startup | Make opt-in. |
| `.claude/settings.local.json` | deferral | Broad local permissions may weaken command boundaries. | local/shared settings | local runtime | Verify precedence. |
| graphify local files | deletion/consolidation | Ignored workflow can drift. | `.agents/`; `.gitignore` | local exploration | Remove locally or promote only if mandatory. |
| `_workspace/`, `_workspace_prev/` | consolidation | Scratch paths described but not ignored. | skills and `.gitignore` | scratch output | Add ignore/check coverage. |
| historical raw subagent ledgers | deferral | Original tables not authoritative committed artifacts. | plan and skill | replayability | Keep limitation; preserve fresh/current tables. |
| `.agents/skills/workspace-harness-audit/skill.md` | deferral | Local mirror absent but `.agents/` is not SSoT. | mirrors and catalog | local convenience | Do not add unless operator needs it. |
| per-skill type metadata | consolidation | Workflow/reference distinction not machine-checkable per skill. | catalog and skills | skill routing | Add type column. |

#### Skills & Harness Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Actual runtime effect of SessionStart live probes | Live commands not run. | Run only with explicit approval. |
| Settings precedence | Local/shared merge behavior not verified. | Non-destructive permission simulation or provider docs. |
| `.agents/skills/workspace-harness-audit` mirror absence | Operator intent unknown. | Ask local operator or document existing-only mirror policy. |
| Graphify local workflow intent | Optional local or mandatory unknown. | Owner decision. |
| Historical raw role table source | Not in committed artifacts. | Preserve directly in future/current audits. |
| Codex provider note location | `agents-md.md` may cover Codex, but no `codex.md`. | Confirm provider mapping before adding file. |

### Hybrid Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task Hybrid Refresh section |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task Hybrid Refresh section |
| `bash scripts/validate-gitops-structure.sh` | PASS; root app manifest count: 17 | linked task Hybrid Refresh section |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task Hybrid Refresh section |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task Hybrid Refresh section |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task Hybrid Refresh section |
| shell syntax check | PASS | linked task Hybrid Refresh section |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task Hybrid Refresh section |
| `.env.example` and `.env` key comparison | PASS after Bash rerun; key names matched without printing values | linked task Hybrid Refresh section |
| Path-level external `SKILL.md` check | PASS; all listed paths present | this plan; linked task |
| `git diff --check` | PASS | linked task Hybrid Refresh section |
| Live k3d/ArgoCD/Vault/ESO validation | skipped by task boundary | Deferred Items |

### Hybrid Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | Hybrid refresh plan and existing Spec 006 |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Six fresh role reviews, file inventory, path check, static verification plan |
| Are modification scope and forbidden scope separated? | pass | Hybrid P1/P2/P3 tables |
| Are existing patterns, compatibility, and dependency rules stated? | pass | GitOps-first, no-live default, gateway-thin, template-first, task-to-skill routing |
| Are test, lint, and type-check commands identified? | pass | Verification Plan and Hybrid Verification Results |
| Are completion criteria measurable? | pass | Spec VAL-SPC-006-006, task T-014 through T-020 |
| Are recurring instructions moved or planned for `AGENTS.md` or Skills? | pass | `workspace-harness-audit` skill and `harness-catalog.md` |

### Hybrid Final Report

| Section | Hybrid refresh result |
| --- | --- |
| Baseline Instruction Check | Rechecked gateway shims, governance docs, templates, `.claude/`, `.codex/`, `.agents/`, and missing `.agent/`; no gateway expansion was needed. |
| Coverage Ledger Summary | All target areas were inventoried; static documentation/scripts were mostly complete, while GitOps/runtime/CI/live areas remain partial or unknown where external state is required. |
| Subagent Summary | Six fresh read-only role reviews completed and are preserved above in role table shape. |
| Integrated Gap Analysis Summary | New safe gaps were documentation evidence, metadata, no-live hook boundary, scratch ignore coverage, and skill-path replayability; high-risk runtime/secret/CI policy items remain deferred. |
| spec/task/plan Updates | Existing Spec 006, linked plan, linked task, and progress ledger were updated in place. |
| Implementation Changes | Implemented only P1/P2 guardrail and evidence changes; no Kubernetes resource semantics, ArgoCD structure, Vault policy, secret/env policy, CI structure, or live checks were changed. |
| Deletion, Consolidation, and Deferred Items | No deletion performed; graphify local cleanup, AppProject/Vault/NetworkPolicy/bootstrap/CI/live items remain deferred with pre-checks. |
| Verification | Repo-static bundle passed; optional `kube-linter` and live validation remain explicitly skipped/deferred. |
| Checklist Gate | Passed with evidence recorded above. |
| Remaining Risks and Next Work | Live runtime state, `.env` values, GitHub rulesets, optional toolchain, `.claude/settings.local.json` precedence, and P3 GitOps/security decisions remain open. |

## Verification Results

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

## Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | User task contract and this plan summary |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Six subagent reviews and repo-static checks |
| Are modification scope and forbidden scope separated? | pass | P1/P2/P3 sections |
| Are existing patterns, compatibility, and dependency rules stated? | pass | AGENTS thin gateway, GitOps-first, template-first rules |
| Are test, lint, and type-check commands identified? | pass | Verification Plan |
| Are completion criteria measurable? | pass | Completion Criteria and verification commands |
| Are recurring instructions moved or planned for `AGENTS.md` or Skills? | pass | Routing consolidated into `harness-catalog.md` |

## Final Report

### 1. Baseline Instruction Check

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

### 2. Coverage Ledger Summary

| Area | Investigation status | Gap count | Candidate count | Unknown |
| --- | --- | ---: | ---: | --- |
| Documentation | complete | 4 | 6 | live parity, strict exception policy |
| Scripts | complete | 2 | 1 | secret scan depth |
| GitOps/infrastructure | partial | 8 | 6 | live cluster, Vault, external reachability |
| Environment/QA/CI | partial | 4 | 4 | optional tools, CI/rulesets, env values |
| Agent governance | partial | 6 | 5 | local precedence, `.agent/` absence |

### 3. Subagent Summary

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | complete | Lifecycle and templates are healthy; one historical plan/task exception | live runtime parity |
| Agent Governance Reviewer | complete | Gateway/mirrors coherent; local settings and graphify local surfaces deferred | local permission precedence |
| Scripts Reviewer | complete | All scripts retained; root app count and hook env docs need hardening | env bypass audience |
| GitOps Infrastructure Reviewer | complete | Semantic GitOps gaps in ESO, Vault, AppProject, bootstrap ownership | live ArgoCD/Vault state |
| Environment Quality Reviewer | complete | Env keys match; CI/static gates clear; optional tools missing | remote CI/rulesets |
| Skills & Harness Reviewer | complete | Scope bridge drift and scratch convention need correction | live hook behavior |

### 4. Integrated Gap Analysis Summary

| Area | Key Gap | Risk | Action | Priority |
| --- | --- | --- | --- | --- |
| Agent governance | stale scope bridge rows | Low | update | P1 |
| Agent governance | task-to-skill routing not consolidated | Medium | add to catalog | P2 |
| Scripts | root app manifest count not asserted | Medium | harden validator | P2 |
| GitOps | ESO/Vault/AppProject semantic gaps | High | defer | P3 |
| CI/CD | tag pinning accepted risk | Medium | defer | P3 |

### 5. spec/task/plan Updates

| Document | Change | Linked work |
| --- | --- | --- |
| `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | New technical contract | T-001 |
| `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` | New plan with ledgers and report | T-002 |
| `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md` | New execution evidence | T-003 |
| stage README indexes | New entries | T-001 |
| `memory/progress.md` | Progress and evidence entry | T-009 |

### 6. Skill and Harness Updates

| Target | Action | Skill used | Reason |
| --- | --- | --- | --- |
| `.claude/skills/workspace-harness-audit/skill.md` | Added repo-local workflow Skill | `writing-skills`, `write-a-skill`, `skill-creator`, `skill-improver` guidance | Capture repeated broad workspace audit workflow and prevent future omission of skill path checks or raw ledger preservation |
| `docs/00.agent-governance/harness-catalog.md` | Added skill inventory row and retained external requested skill routing | `grill-with-docs`, `agent-md-refactor` routing principles | Keep `AGENTS.md` thin while centralizing harness routing |
| Required external `SKILL.md` paths | Verified exact paths | `grill-with-docs` plus task-specific skill routing | Satisfy missing-path Gap recording contract; no missing paths found |

### 7. Implementation Changes

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

### 8. Deletion, Consolidation, and Deferred Items

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| `.agents/rules/graphify.md` | deletion candidate | ignored local drift | local ignored only | defer owner decision |
| `gitops/clusters/local` ownership | consolidation | bootstrap CR drift | static review partial | defer design |
| ESO NetworkPolicy | deferred | runtime semantic change | manifest review | separate task |
| Vault policy | deferred | secret access policy | manifest/HCL review | separate task |
| SHA pinning | deferred | CI policy | workflow/zizmor review | separate task |
| historical raw subagent ledgers | deferred | original raw role output tables are not current-state files | current plan has integrated summaries | preserve raw Summary/Ledger tables in future runs through `workspace-harness-audit` |

### 9. Verification

| Command or method | Result | Record location |
| --- | --- | --- |
| Full verification bundle | PASS; optional `kube-linter` unavailable and live checks deferred | task verification summary |
| External required skill path check | PASS; no missing paths | input reflection follow-up |

### 10. Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Goal clear | pass | task contract |
| Related files discovered | pass | ledger |
| Scope separated | pass | P1/P2/P3 |
| Existing patterns stated | pass | governance links |
| Commands identified | pass | verification plan |
| Criteria measurable | pass | completion criteria |
| Recurring rules routed | pass | harness catalog |

### 11. Remaining Risks and Next Work

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
