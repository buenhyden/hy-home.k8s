---
title: "Agent Contracts and Skill Ownership Implementation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-PLAN-0001"
---

# Agent Contracts and Skill Ownership Implementation Plan

> For agentic workers: after Plan approval, use `superpowers:executing-plans` with the repository work lifecycle. Do not create a new implementer and reviewer for every Task. The owning Task and independent review record each bounded result.

**Goal:** Converge the current agent, skill, document, provider, evaluation, and command owners to the approved SPEC-0102 contract without widening runtime authority.

**Architecture:** Keep the existing registry, Stage 99 profiles, and shared QA registry. Change the narrow authority/consumer contracts first, then add the dedicated external-service skill and move the homogeneous evaluation corpus. Validate each logical unit before converting dependent consumers.

**Tech stack:** Python 3.12 repository validators/tests, YAML manifests, Markdown governance and Stage 99 documents, Claude/Codex native adapters, GitHub Actions. Reuse installed PyYAML and repository `scripts/validation/repository/bounded_io.py`.

**Spec:** [SPEC-0102](spec.md); structural constraint: [ADR-0047](../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md). The user approved both contents on 2026-09-29, initial `draft`/`proposed` states were committed in `8e811506`, and this change records the reviewed lifecycle transitions. The request owner approved this Plan for execution on 2026-09-29. Initial `draft` state was committed in `8e811506`; this approved Plan now transitions to `active`.

## Global Constraints

- External changes require separately scoped operator approval: live cluster, Argo CD, Vault/OpenBao, cloud, remote Git/GitHub, account authentication, personal/global settings and paid provider operations. Evidence excludes sensitive material and raw transcripts.
- Preserve registry permission classes, root gateways, Stage 99 form authority, global QA gate selection, and Stage 98 frozen/retained bodies. A skill cannot grant rights; a static PASS cannot prove native, hosted, remote, or live behavior.
- No new role, generic model runner, speculative native config key, empty output-style/editor/Traefik/command tree, central progress ledger, or mandatory per-Task agent fan-out. Model bindings stay as observed unless an approved and authenticated reason changes them.
- The `governance-steward` must not edit its own role, projection, or registry self-entry. Such a change requires a separately approved operator-owned scope; otherwise that portion is `DEFER` while independent work proceeds.
- Each work package starts with a failing focused check for behavior it changes, ends with a passing focused check and review, and records exact changed bytes, commands, limits, rollback, and next owner in its package-local Task. Existing checks that already prove a preserved behavior need not be duplicated.
- After Plan approval, use `superpowers:executing-plans` and the repository lifecycle. Do not infer permission to push, open PRs, merge, deploy, or reconfigure a provider from Plan approval.

## Overview

This is one dependent Plan for all 33 `VAL-ACS-*` criteria and original T01–T33 scenarios in [SPEC-0102](spec.md). It converts the seven implementation themes into reviewable work packages and a lifecycle setup package. The Plan is not execution state; after approval, package-local Tasks own RED/GREEN evidence, review, commits, rollback, and unfinished work. The linked Tasks now record the approved execution units.

## Context

At the approved design snapshot `efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`, there were 17 registered roles/skills, matching native role projections, and 19 synthetic agent evaluation cases. The unchanged-main baseline passed `python3 scripts/validate-agent-governance.py --root .`, `python3 scripts/run-agent-evaluations.py --root .`, and `python3 scripts/qa.py full` (22/22 gates). Those results do not validate the new bytes. The current R23 link rule and tests admit individual numbered-document plain paths and reject stage README links outside `docs/`; the skill validators allow reachable resources but disallow dedicated `.template.md` assets and skill-local gate scripts. `scripts/prompt-input.py:run_input(root: Path, name: str, argv: Sequence[str]) -> str` captures full subprocess output before truncation. Existing `scripts/validation/repository/bounded_io.py:run(argv: Sequence[str], *, timeout: float, stdout_limit: int, stderr_limit: int, cwd: Path | None, env: Mapping | None, input_bytes: bytes | None) -> CompletedProcess[bytes]` is the first reuse candidate. The eval runner assumes its current parent is `scripts/` and uses `evals/cases/*.json`; relocation must repair imports and all consumers.

## Goals & In-Scope

Deliver the exact R23 normalized owner-link boundary; safe skill-owned templates and registered dedicated validators; one nonduplicative external-service audit; bounded knowledge/handoff/prompt input; aligned neutral roles/native adapters/common workflows/command contracts; one `.agents/evaluations/` owner; and complete T01–T33/static QA evidence. Preserve the individual keep decisions in the Spec. Before each edit, compare the current worktree and actual caller set with this Plan; if evidence invalidates a target, revise the Plan for review rather than silently widening scope.

## Non-Goals & Out-of-Scope

This Plan does not authorize its own execution, Task creation before approval, an approved-status write before valid lifecycle history, or external action. It does not create an issue tracker integration, editor key binding, output style, model runner, live probe, or provider budget configuration to satisfy an unobserved capability. It does not rewrite archived decisions or broad-scan private/global skill caches. Account-specific costs, RPM/TPM, authenticated model availability, native hook delivery, hosted CI and live cluster checks remain separate `DEFER` lanes until an authorized observation.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-000 | Approved-Plan Task setup and legal document lifecycle | Plan approval | User approval recorded; no implementation before it | Package Task(s), initial `draft`/`proposed` document commit, then separately reviewed `active`/`accepted` transition and exact-index QA |
| WP-001 | R23 document owner/link cutover | WP-000; accepted ADR-0047 | Explicit link/semantic consumer list and approved exact machine exceptions | Normalized link positive/negative tests, current consumers converted, historical bodies intact |
| WP-002 | Skill resource and dedicated gate ownership | WP-001 | Central gate owner and bundle resource graph fixed | Reachable safe bundle/template/checker cases pass; traversal/orphan/unsafe argv cases fail |
| WP-003 | External-service contract skill | WP-002 | Real Service/EndpointSlice consumers and scoped secret-free fixtures | New skill plus checker/refs/projections, multi-slice and negative cases, no duplicate security/manifest gate |
| WP-004 | Knowledge, handoff, prompt bounded I/O | WP-001 | Current authority and redaction boundary established | Fact lifecycle/resume tests; bounded subprocess output/partial-result cases pass |
| WP-005 | Role, native, workflow, and command alignment | WP-001–WP-004 | Actual changed contracts and callers enumerated; self-role operator approval if applicable | Registry/adapter parity, role fit, hook/command/workflow regression, unsupported runtime lanes explicit |
| WP-006 | Evaluation corpus ownership cutover | WP-004–WP-005 | Agent-evaluator owner and shared gate route settled | 19 expected failure sets identical; no stale `evals/` callers/root duplicate |
| WP-007 | Final coverage, source freshness, and handoff | WP-001–WP-006 | All logical units reviewed | T01–T33 dispositions, exact-index/final full QA, review, Task handoff, approved local commits |

### WP-000 — Lifecycle and Task entry

**Owner / files:** `supervisor` routes approval; `doc-writer` authors `docs/03.specs/0102-agent-contracts-and-skill-ownership/{spec,plan}.md` and, after Plan approval, `tasks/tsk-0001-*.md`; `architect` owns `docs/02.architecture/decisions/0047-agent-contract-and-resource-ownership.md`; `wiki-curator` maintains the affected Stage 02/03 README rows. No other role edits its own permission contract.

- [ ] After explicit Plan approval, create package-local Task records from the `sdlc/task` profile in initial `queued` state (planned TSK-0001–0008). Record approval source, snapshot, scope, rollback, and each planned WP owner before implementation.
- [ ] Commit newly authored Spec/Plan/ADR/Task/index content in their legal initial `draft`/`proposed` states after staged profile/link/lifecycle QA. This first commit preserves observed initial state; it does not claim approval state.
- [ ] In a separate reviewed change, move approved SPEC-0102 to `active`, ADR-0047 to `accepted`, and the approved Plan to `active`, with profile version transition, reciprocal links, and exact-index lifecycle QA. ADR-0036 remains accepted and receives only a bounded successor relation if that owner approves it.
- [ ] Record the two commit identities and rollback (revert the transition before reverting the initial authoring commit) in TSK-0001. Stop if lifecycle/profile evidence fails; never edit the history gate to force the transition.

### WP-001 — Document authority and normalized links

**Owner / files:** `governance-steward` coordinates shared contract outside its own self-entry; `doc-writer` updates `.agents/governance/document-authoring.md`; `quality-engineer` implements `scripts/validate-links-and-owners.py` and its `tests/test_documentation_link_boundary.py` (another implementer requires explicit Task delegation). Exact current consumers include `.agents/knowledge/domains.md`, `.agents/README.md`, `.agents/skills/archive-cutover/SKILL.md`, `.agents/governance/document-lifecycle.md`, `.codex/provider.md`, `.claude/provider.md`, `.github/repository-surface.md`, and `infrastructure/README.md`. `wiki-curator` handles README navigation; do not alter archived bodies.

- [ ] Add RED T07/T08/T09 fixtures to `tests/test_documentation_link_boundary.py`: direct Markdown, reference, HTML, wiki, blob/raw URL, encoded path, case/separator variants; allowed Stage README navigation and docs-internal tracking; plain-path current-authority dependency review; exact consumer/target/access-kind machine exception. Existing `_stage_boundary_diagnostic` and `_stage_grammar_diagnostics` are the implementation owners.
  Representative RED assertion in the existing `StageLinkBoundaryTests` fixture: `self.assertIsNone(_report(CONSUMER, "docs/03.specs/README.md"))`; the old rule rejects that stage README. Add a direct individual-doc negative assertion in the same class.
- [ ] Amend the current document policy and validator together. Reject every outside-doc direct individual numbered-document link, including historical ones; repoint current authority to owner/README. Keep executable machine reads only under explicit exact exceptions, not a directory wildcard. Audit semantic plain-path consumers manually where parsing cannot prove intent.
- [ ] Run focused document-link tests, affected profile/link/owner checks and a reviewer pass over converted consumers. Record the old/new normalized target mapping and rollback as one logical docs+validator+consumer commit; keep accepted ADR-0036 and Stage 98 bodies unchanged.

### WP-002 — Skill-owned resources and central gates

**Owner / files:** `quality-engineer` implements `scripts/validate-agent-governance.py` (`_validate_skill_bundle`), `scripts/validate-affected-surfaces.py` (`_validate_direct_script_argv`), `scripts/validation/registry.json`, and gate tests; another implementer requires explicit Task delegation. Contract text lives in `.agents/README.md` and the affected `workspace-harness-audit`, `docs-stage-conformance`/routing consumers only where required. Test owners are `tests/test_agent_governance.py`, `tests/test_validate_affected_surfaces.py`, and `tests/fixtures/validation-surfaces.json`.

- [ ] Add RED T01/T02/T03/T05/T29 cases for a linked skill-owned script/template and a central gate that calls it; reject missing/unregistered/orphan resources, traversal, external symlink, unsafe argv, unexpected execution, and missing required tool. Include a valid transitive cycle-safe traversal; fail only unresolvable cycles or unsafe references.
  Representative RED assertion in the existing bundle fixture after `self.place_bundle("assets/report.template.md", reachable=True)`: `self.assertEqual(self.validator.validate_registry(self.root)["roles"], 1)`; the old rule rejects the dedicated template.
- [ ] Permit the specific dedicated template and checker layouts while keeping regular-file/reachability/suffix checks and the central registry as the only global gate admission and result owner. Do not authorize a skill to select its own QA profile.
- [ ] Run focused bundle/affected-surface tests plus registry/profile static checks. Record the exact bundle and gate consumers; rollback reverts validator/registry/layout as one unit before removing accepted resources.

### WP-003 — External-service audit

**Owner / files:** `governance-steward` authors `.agents/skills/external-service-contract-audit/{SKILL.md,references/external-service-contracts.md,agents/openai.yaml}` and the `.agents/roles/registry.json` skill entry; `quality-engineer` implements the registered dedicated checker `.agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py` (or delegates that exact file in a Task); `governance-steward` updates relevant `k8s-implementer`/`gitops-reviewer` skill references; Claude adapter `.claude/skills/external-service-contract-audit` links the canonical package. `quality-engineer` owns `scripts/validation/registry.json`; focused tests live at `tests/test_external_service_contracts.py` with fixtures under `tests/fixtures/external-service-contracts/`. `network-reviewer`, `observability-reviewer`, and `security-auditor` review boundaries. Existing YAML loader patterns are reused; do not import `quality.py` with top-level side effects.

- [ ] Add RED T04/T22/T29 fixtures for selectorless Service plus all matching namespace/service-labelled EndpointSlices, valid repeated identical endpoints deduplicated, split Alloy named-port coverage, frontend/backend difference Valkey `6379→26379`, and negative namespace/name/protocol/targetPort/addressType/malformed/secret-value/escape cases. Selector-managed Services are excluded from this specific join with an explicit result. Include a newly added nonignored YAML manifest in the focused CLI fixture so quick-snapshot coverage cannot omit it.
  Representative RED assertion in new `tests/test_external_service_contracts.py`: with `fixtures = Path(__file__).parent / "fixtures/external-service-contracts/two-slices"` and `paths = sorted(fixtures.glob("*.yaml"))`, assert `validate_documents(fixtures, paths) == []` for repeated identical endpoints and split Alloy ports. Importing the not-yet-written checker must fail RED.
- [ ] Implement `validate_documents(root: Path, paths: Sequence[Path]) -> list[str]` in the dedicated checker, returning deterministic redacted path/field findings; `main(argv: Sequence[str] | None = None) -> int` accepts `--root REPO`, discovers tracked and nonignored new `gitops/platform/external-services/*.yaml` from the QA snapshot through NUL-safe `git ls-files --cached --others --exclude-standard -z` path transport, and exits nonzero on findings, malformed input or missing required tool. The new central gate argv is `python3 .agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py --root .`; `scripts/validation/registry.json` alone chooses profiles and result meaning. Reuse installed PyYAML safe loading and existing argument conventions; do not import side-effecting `quality.py`.
- [ ] Add only the skill-local checker and protocol/reference content consumed by it. Return bounded redacted diagnostics and nonzero on required contract failure; do not contact the service or reimplement schema, ESO/Vault, Rego, or security audits. Register its global invocation solely in the central registry and add explicit skill refs/adapter after the consumer is proven.
- [ ] Run the focused checker suite and selected static gate, then independent GitOps/network/security review. Record a one-unit rollback of new skill, adapter, registry refs, gate and fixtures; external runtime checks remain DEFER.

### WP-004 — Knowledge, safe resume, and bounded prompt input

**Owner / files:** `governance-steward` changes `.agents/governance/context-and-memory.md` only outside its own role; `wiki-curator` adjusts `.agents/knowledge/{README.md,domains.md,project-map.md}` as needed; `supervisor` decides handoff direction; `doc-writer` authors `.agents/workflows/{work-lifecycle,delegated-development}.md` and `.agents/prompts/handoff.md` under that delegation; `repo-tooling-engineer` changes `scripts/prompt-input.py`; `quality-engineer` owns the registered `scripts/validate-knowledge-surface.py` gate and `tests/test_validate_knowledge_surface.py` (or explicitly delegates it), while `repo-tooling-engineer` owns `tests/test_prompt_input.py` and prompt/handoff test updates. `doc-update.md` changes only for observed R23 consumer impact.

- [ ] Add RED T14/T15/T25/T26 tests for the eight fact metadata fields, current authority check before promotion/edit/deletion, expiry/deleted source/derived-cache invalidation, stale branch/HEAD/hash/revoked approval, concurrent writer, redaction, and partial resume.
- [ ] In `tests/test_prompt_input.py`, pin overflow, timeout and nonzero subprocess to no assembled draft, explicit bounded failure and no raw stderr echo. Reuse `bounded_io.run` bytes result, convert to `run_input(...)->str` at the existing boundary, and preserve structured error identity; no new generic runner.
  Representative RED assertion in existing `tests/test_prompt_input.py`: after an over-limit command, `with self.assertRaises(self.module.PromptInputError) as raised: self.module.assemble(self.root, "sample")`; then assert `raised.exception.code == "PROMPT-OUTPUT-LIMIT"` and no assembled draft is returned. The current full capture/truncate path fails this behavior.
- [ ] Keep current policy facts in their canonical owners and work state in the Task. Add bounded metadata and handoff fields without creating a central ledger. Run focused tests/knowledge validator and review sensitive output. Rollback is one logical policy+prompt+test/tool change; remove any derived scratch cache without touching private state.

### WP-005 — Role, native, workflow, and command convergence

**Owner / files:** `governance-steward` coordinates `.agents/roles/registry.json`, selected role bodies excluding its own, `.claude/agents/*.md`, `.codex/agents/*.toml`, and skill sidecars/symlinks; `supervisor` resolves disputed fit. `ci-workflow-engineer` owns scoped `.github/workflows/*.yml` only if a concrete defect is found; `repo-tooling-engineer` owns `.claude/commands/*.md`, `scripts/provider_write_guard.py`, hook adapters, and `scripts/githooks/*` only when a caller/contract test requires change. `quality-engineer` owns governance/permission/hook/workflow/command regression tests. Operator-only self-entry target: `.agents/roles/governance-steward.md`, its registry role row, `.claude/agents/governance-steward.md`, `.codex/agents/governance-steward.toml`.

- [ ] Add RED T10–T13, T16–T19, T23/T27/T28/T30–T33 cases for role-skill fit, provider projection membership and least privilege, hook payload/exit/re-entry, command args/cwd/timeout/callers, workflow approval/required-check production and output evidence. Keep native, hosted and live observation separate.
- [ ] Make only the Spec's per-role/per-skill changes with actual callers. Retain 17 role IDs, existing native bindings, five distinct hosted workflows, four thin Claude slash adapters, and current Git hook chain unless a failing check proves a scoped fix. Preserve registry empty skill-ref option; do not add a filler skill. For `governance-steward` self-entry, require separate operator-owned approval before editing; otherwise record that part DEFER and do not claim R35 complete.
- [ ] For T18, use existing agent evaluation cases and contract review to flag synthetic responses that promise unsupported models, ignore elapsed/shared-budget exhaustion or `Retry-After`, or silently choose a more expensive model. Preserve the baseline 19 cases; any added cases are a separately scored increment. Do not build a test-only budget policy or generic runtime runner. Real account cost/RPM/TPM and native hard enforcement remain DEFER until an authorized measured session.
- [ ] Run focused role/native/hook/command/workflow tests and governance validator. Review each changed adapter against its neutral owner and record a logical registry+projection+consumer commit. Rollback restores matched registry and adapters together; never weaken required CI check or provider sandbox.

### WP-006 — Evaluation owner cutover

**Owner / files:** `agent-evaluator` owns `.agents/evaluations/{README.md,cases/*.json,responses/*.synthetic.md,run-agent-evaluations.py}`; `agent-evaluator` owns the moved runner and `tests/test_agent_evaluations.py`; `quality-engineer` owns central invocation in `scripts/validation/registry.json`, `docs/99.templates/registry.json` route validation, and related gate tests; `repo-tooling-engineer` changes `tests/archive_generation_fixture.py` and `scripts/README.md` with explicit owner delegation where needed; `wiki-curator` updates `README.md`, `.agents/README.md`, and `.agents/knowledge/project-map.md`; `governance-steward` updates `.agents/roles/{agent-evaluator,repo-tooling-engineer}.md` to remove stale eval paths. No retained archive body is rewritten. Source paths are `evals/{README.md,cases/,responses/}` and `scripts/run-agent-evaluations.py`.

- [ ] Freeze baseline 19 expected failure sets and add RED T20/T33 tests for new paths, no stale root paths/callers, no duplicate root copy, and synthetic response instructions treated only as data. Include a failure if the grader import path breaks after moving from `scripts/`.
- [ ] Move the corpus and exclusive runner together; repair the runner's `sys.path`/shared scripts import without copying the implementation, update `CASE_GLOB`, registry argv, case JSON response references, `docs/99.templates/registry.json`, both role bodies, tests and docs atomically. Preserve case IDs and negative cases; leave no empty root `evals/`.
- [ ] Run direct new grader and focused tests to prove exact 19-set parity, then affected QA. Review all path consumers. Rollback restores corpus+runner+registry/tests as one logical move, with no duplicated active source.

### WP-007 — Complete coverage and handoff

**Owner / files:** `quality-engineer` selects final QA; `code-reviewer` and `security-auditor` review scoped changes; `doc-writer` updates only approved Stage 03 Task evidence; `wiki-curator` checks current README navigation. This package changes no new runtime feature file unless a review finds a defect assigned back to its owning WP.

- [ ] Map every VAL-ACS-001–033 and original T01–T33 to a named actual check or explicit DEFER with owner/retry trigger; R35–R39 require per-item changed-file/caller disposition, not prose-only completion. Preserve observed version/source provenance and correct stale current claims, including the external-services README account, without rewriting archived facts.
- [ ] Run each focused check on its final bytes, quick affected selection, staged QA for every logical commit, `git diff --check` and cached diff, then one full QA on the final tree. Record exact snapshot, gate results, optional SKIP and external DEFER separately; do not rerun identical expensive gates without changed input or required mode.
- [ ] Complete independent correctness/security review, repair findings at the owning WP, and update package-local Task handoff with scope, approvals, commands, reviewer, rollback and next owner. Commit only reviewed logical sets after the required hooks; preserve the branch. Push, PR, merge and live changes remain outside this Plan.

## Verification Plan

The original scenario IDs keep their SPEC-0102 meanings: T01/T02 safe bundle, T03/T04 ownership and trigger, T05/T06 required-tool and command error, T07–T09 document owner link, T10–T13 role/native/hook, T14/T15 memory and resume, T16–T19 Git/editor/budget/PR trust, T20 eval cutover, T21/T22 disposition/new value, T23/T24 distribution/operational boundary, T25–T27 knowledge/prompt/style, T28–T33 per-item role/skill/agent/workflow/command and freshness. No test ID is repurposed. Focused tests are written before changed behavior, then executed RED/GREEN. For repository QA, use `python3 scripts/qa.py quick`, exact-index `python3 scripts/qa.py staged`, and final `python3 scripts/qa.py full` according to the quality policy; gate commands/profile membership remain in `scripts/validation/registry.json`. Read-only corpus inspection and manual semantic review complement validators where intent cannot be parsed. Neither a simulated agent response nor a mock `kubectl` proves provider or live operation.

### Focused Command Sets

These are future commands after Plan approval, not tests run while drafting. Each new assertion is run once to show RED, then again after its owning change for GREEN. A pre-existing test may already be GREEN and proves only preserved behavior. `python3 -m unittest` uses current test modules; new `tests.test_external_service_contracts` is created in WP-003.

| Set | Work package | Focused command | Expected evidence |
| --- | --- | --- | --- |
| C1 | WP-001 | `python3 -m unittest tests.test_documentation_link_boundary tests.test_common_agents_document_routes tests.test_readme_navigation` | New R23 case RED then GREEN; manual T09 semantic audit separately |
| C2 | WP-002 | `python3 -m unittest tests.test_agent_governance tests.test_validate_affected_surfaces tests.test_validation_profiles tests.test_validation_tooling_ownership` | Dedicated bundle/gate admission RED then GREEN; unsafe case stays FAIL as input |
| C3 | WP-003 | `python3 -m unittest tests.test_external_service_contracts tests.test_validate_gitops_change_set tests.test_validate_vault_eso_contracts tests.test_check_secret_handling` | New selectorless join RED then GREEN; existing safety contracts preserved |
| C4 | WP-004 | `python3 -m unittest tests.test_validate_knowledge_surface tests.test_prompt_input tests.test_run_validation_lane tests.test_validate_agent_registry` | New stale/overflow cases RED then GREEN; secret output absent |
| C5 | WP-005 | `python3 -m unittest tests.test_validate_agent_registry tests.test_agent_governance tests.test_agent_governance_consumers tests.test_k8s_pre_edit_hook tests.test_ci_qa_workflow tests.test_commit_contracts tests.test_validation_profiles tests.test_prompt_input tests.test_qa_runner` | Current parity plus changed role/hook/command cases; runtime lanes distinct |
| C6 | WP-006 | `python3 -m unittest tests.test_agent_evaluations tests.test_validation_profiles tests.test_validate_affected_surfaces tests.test_archive_generation_fixture` and `python3 .agents/evaluations/run-agent-evaluations.py --root .` | Moved runner executes; same 19 expected failure sets and 12 negatives |
| C7 | WP-007 | `python3 scripts/qa.py quick`, `python3 scripts/qa.py staged`, `python3 scripts/qa.py full` with `git diff --check` and `git diff --cached --check` at required snapshots | Affected/index/final-tree PASS on their own bytes; hosted/native/live not inferred |

### Original Scenario Evidence Routing

The source T IDs and meanings remain in the Spec. The table identifies the intended evidence depth; a scenario marked DEFER is not a pass. C1–C7 name the command sets above.

| Scenario | Owner / command | Planned evidence or limit |
| --- | --- | --- |
| T01 | WP-002 / C2 | Extend existing positive bundle case to reachable dedicated resources. |
| T02 | WP-002, WP-003 / C2, C3 | Escape, symlink, secret and unexpected-execution negatives. |
| T03 | WP-002, WP-005 / C2, C5 | Ownership/caller review plus existing duplicate tests. |
| T04 | WP-003 / C3 | New trigger/counterexample fixture; native automatic selection DEFER. |
| T05 | WP-002, WP-003 / C2, C3, C7 | Required-tool failure remains FAIL; optional skip reason explicit. |
| T06 | WP-003, WP-005 / C3, C5 | cwd, malformed input, timeout, partial-result exit. |
| T07 | WP-001 / C1 | Normalize prohibited reference/wiki/HTML/blob/raw/encoded/case variants. |
| T08 | WP-001 / C1 | Stage README/docs-internal navigation and exact machine exception positive. |
| T09 | WP-001 / C1 + review | Plain-path authority dependency manually audited; regex alone is insufficient. |
| T10 | WP-005 / C5 | Role and delegation permission matrix; native inheritance DEFER. |
| T11 | WP-005 / C5 | Registry/model/projection parity; resolved native model DEFER. |
| T12 | WP-005 / C5 | Hook payload/exit/re-entry fixture; native delivery DEFER. |
| T13 | WP-005 / C5 | Static trust configuration; authenticated discovery DEFER. |
| T14 | WP-004 / C4 | Stale branch/HEAD/hash/approval and concurrent writer stop. |
| T15 | WP-004 / C4 | Fact promotion/expiry/deletion/cache invalidation and no secret. |
| T16 | WP-005 / C5, C7 | Index and commit-hook contract; installed hook delivery separately observed. |
| T17 | WP-005 / review | No editor command installed; native editor action DEFER. |
| T18 | WP-005 / eval review | Synthetic refusal/defer/retry-budget violations; real account limits/enforcement DEFER. |
| T19 | WP-005 / C5 | CI untrusted-input/required-check fixtures; external ticket state DEFER. |
| T20 | WP-006 / C6 | Atomic cutover, 19-set parity, 12 negatives and no stale consumer. |
| T21 | WP-001, WP-004, WP-005 / C1, C4, C5 | Current disposition/resume review; no historical success rewrite. |
| T22 | WP-003 / C3 + review | New skill gap, real consumers, source/license review. |
| T23 | WP-005 / C5 | Sidecar/symlink/CI route static check; other product distribution DEFER. |
| T24 | WP-003, WP-005 / C3, C5 | Static no-live-contact safeguards; actual live action prohibited. |
| T25 | WP-004 / C4 | Knowledge owner, scope, observed time and invalidation. |
| T26 | WP-004 / C4 | Prompt input/output and incomplete/forbidden result. |
| T27 | WP-005 / C5 + review | Result fields protected; unsupported output-style runtime DEFER. |
| T28 | WP-005 / C5 | Before/after role matrix; no role deletion proposed. |
| T29 | WP-002, WP-003 / C2, C3 | Dedicated bundle transition/new skill; no skill merge proposed. |
| T30 | WP-005 / C5 | Projection/name/permission checks; native agent_type/sandbox DEFER. |
| T31 | WP-005 / C5 | Workflow branch/required summary; remote branch protection DEFER. |
| T32 | WP-005 / C5 | CLI help/args/cwd/tool/timeout/caller; editor-native DEFER. |
| T33 | WP-006, WP-007 / C6, C7 | Fresh path/version consumers and final QA; external lanes DEFER. |

### Review Focus

| Input/condition | Owning WP and test |
| --- | --- |
| One Service has two EndpointSlices with an identical repeated endpoint and Alloy ports split across slices; aggregate coverage is valid. | WP-003, T22/T29 positive fixture |
| A Markdown-free plain path keeps a current individual Stage authority dependency after links are removed; reviewer must still flag it. | WP-001, T09 semantic consumer audit |
| The output limit is crossed after a successful subprocess has produced only a prefix; no assembled prompt may present it as complete. | WP-004, T26 overflow fixture |
| A resumed Task has matching HEAD but a changed relevant file hash or revoked approval; mutation stops. | WP-004, T14 stale-state fixture |
| One skill resource points through a cycle to valid local content while another escapes by symlink; traversal terminates safely and only the escape fails. | WP-002, T02 positive/negative resource graph |

## Risks & Mitigations

| Risk | Owner / mitigation / rollback |
| --- | --- |
| R23 normalization blocks legitimate machine reads or leaves plain authority behind. | WP-001 owner enumerates exact consumer/target/access-kind exceptions; tests positive/negative plus manual audit. Revert policy, validator and consumers together. |
| Dedicated resources bypass the central QA decision or enlarge path reach. | WP-002/quality owner keeps registry selection, regular/reachable/safe argv checks. Revert gate and resource admission as one unit. |
| External-service parser misjoins slices or discloses a value. | WP-003/security review, multiple-slice/port negatives and bounded redaction; revert the new package/registration. |
| Handoff or prompt output omits a failure, exposes stderr, or trusts stale approval. | WP-004 fail-closed tests and bounded I/O reuse; revert prompt/tool/policy together, stop dependent writes. |
| Permission/model/hook prose overclaims native behavior. | WP-005 preserves current bindings and registry class, records native DEFER, requires operator-owned self-entry approval. Revert matching registry/projections together. |
| Eval move leaves a second owner or breaks imports. | WP-006 exact 19-set parity and caller-zero; revert corpus, runner, registry and docs together. |
| QA or lifecycle transition rejects changed bytes. | WP-000/WP-007 stop, preserve the failing index/snapshot, repair owning unit; do not weaken gate or rewrite retained history. |

## Completion Criteria

The Plan completes only when an approved Task records each WP's reviewed change, exact paths, T01–T33/VAL-ACS-001–033 disposition, applicable focused/affected/staged/final full PASS, explicit SKIP/DEFER and next owner, no orphan current caller, and logical local commit/rollback evidence. Required static failures remain incomplete. Native trust/discovery/model/hook, account limits, hosted CI, and live cluster results are not labeled PASS without separate authorized observation. Any unresolved operator-only `governance-steward` self-entry keeps its dependent R35 criterion incomplete/DEFER. Plan approval is a separate decision after this draft is reviewed; no Task or implementation starts before it.

## Traceability

[Approved content of SPEC-0102](spec.md#success-criteria--verification-plan) owns every criterion; this Plan assigns its work owner and intended Task. Package-local Tasks below own execution evidence and reciprocal links.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ACS-001](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-002](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0003](tasks/tsk-0003-skill-resource-ownership.md) |
| [VAL-ACS-003](spec.md#success-criteria--verification-plan) | WP-001 | [TSK-0002](tasks/tsk-0002-document-authority-links.md) |
| [VAL-ACS-004](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-005](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-006](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0005](tasks/tsk-0005-knowledge-and-handoff.md) |
| [VAL-ACS-007](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0005](tasks/tsk-0005-knowledge-and-handoff.md) |
| [VAL-ACS-008](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-009](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-010](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-011](spec.md#success-criteria--verification-plan) | WP-007 | [TSK-0008](tasks/tsk-0008-final-verification.md) |
| [VAL-ACS-012](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0003](tasks/tsk-0003-skill-resource-ownership.md) |
| [VAL-ACS-013](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-014](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0005](tasks/tsk-0005-knowledge-and-handoff.md) |
| [VAL-ACS-015](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-016](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-017](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-018](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-019](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-020](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-021](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-022](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0005](tasks/tsk-0005-knowledge-and-handoff.md) |
| [VAL-ACS-023](spec.md#success-criteria--verification-plan) | WP-001 | [TSK-0002](tasks/tsk-0002-document-authority-links.md) |
| [VAL-ACS-024](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0003](tasks/tsk-0003-skill-resource-ownership.md) |
| [VAL-ACS-025](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0003](tasks/tsk-0003-skill-resource-ownership.md) |
| [VAL-ACS-026](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0003](tasks/tsk-0003-skill-resource-ownership.md) |
| [VAL-ACS-027](spec.md#success-criteria--verification-plan) | WP-003 | [TSK-0004](tasks/tsk-0004-external-service-contracts.md) |
| [VAL-ACS-028](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-029](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-030](spec.md#success-criteria--verification-plan) | WP-007 | [TSK-0008](tasks/tsk-0008-final-verification.md) |
| [VAL-ACS-031](spec.md#success-criteria--verification-plan) | WP-005 | [TSK-0006](tasks/tsk-0006-role-and-provider-contracts.md) |
| [VAL-ACS-032](spec.md#success-criteria--verification-plan) | WP-006 | [TSK-0007](tasks/tsk-0007-evaluation-owner-cutover.md) |
| [VAL-ACS-033](spec.md#success-criteria--verification-plan) | WP-007 | [TSK-0008](tasks/tsk-0008-final-verification.md) |

### Execution Tasks

- WORK-001: [TSK-0001: Document lifecycle and approval](tasks/tsk-0001-lifecycle-and-approval.md)
- WORK-002: [TSK-0002: Document authority and normalized links](tasks/tsk-0002-document-authority-links.md)
- WORK-003: [TSK-0003: Skill resource and central gate ownership](tasks/tsk-0003-skill-resource-ownership.md)
- WORK-004: [TSK-0004: External service contract audit](tasks/tsk-0004-external-service-contracts.md)
- WORK-005: [TSK-0005: Knowledge, resume and bounded prompt input](tasks/tsk-0005-knowledge-and-handoff.md)
- WORK-006: [TSK-0006: Role and provider contract alignment](tasks/tsk-0006-role-and-provider-contracts.md)
- WORK-007: [TSK-0007: Evaluation owner cutover](tasks/tsk-0007-evaluation-owner-cutover.md)
- WORK-008: [TSK-0008: Final verification and handoff](tasks/tsk-0008-final-verification.md)
