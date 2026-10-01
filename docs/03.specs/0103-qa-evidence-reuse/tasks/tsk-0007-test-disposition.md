---
title: "Active QA test disposition"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0007"
---

# Task: Active QA test disposition

## Overview

Execute [Plan WP-007](../plan.md) against [SPEC-0103](../spec.md). The active
CI/QA/validation audit retains every discovered module and removes two redundant
assertions: a gate-owned positive corpus check and a repeated forbidden-key check. Independent semantic review
and final integration evidence remain pending; this record does not close them.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the [quality policy](../../../../.agents/governance/quality.md).
- Criterion: VAL-QER-012; caller authority: `scripts/validation/registry.json`.
- Test responsibility: [tests README](../../../../tests/README.md); exact form:
  `docs/99.templates/templates/specs/task.template.md`, profile `sdlc/task`.
- Starting snapshot: branch `codex/qa-evidence-implementation`, HEAD/base
  `7ad42d2e`, linked worktree named `qa-evidence-implementation/hy-home.k8s`.
  The assigned paths were clean. Tasks 0001/0002 are prior reviewed work.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-007 | VAL-QER-012 | Trace active test callers and distinct failure meanings; retire proven redundant or obsolete tests | platform | In Progress | Audit complete; two redundant methods removed; independent review pending | Inventory, retirement proof, and commands below |

## Approval and Safety Boundaries

- **Allowed Paths**: proved obsolete/redundant/conflicting tests and fixtures,
  their direct callers when justified, `.agents/governance/quality.md` if needed,
  and this Task. Actual edits: this Task, `tests/test_external_service_contracts.py`, and
  `tests/test_document_strict_cutover.py`.
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault
  mutation, archived Spec bodies, other Task records and Spec/Plan contracts.
- **Approval Required**: local implementation and commit are assigned; no push,
  hosted mutation, deployment, or native-provider trust change is authorized here.
- **Static Validation**: focused negative evidence before deletion, final discovery,
  registry/discovery/ownership tests, quick, exact-index staged, and one unit aggregate.
- **Live Validation**: DEFER to Task 0006 for hosted CI; no live check requested.
- **Secret / Vault Handling**: no secret values read or recorded.
- **Rollback Plan**: restore only the removed methods from parent `7ad42d2e` in a
  forward change if gate ownership or retained negative coverage regresses.
- **Evidence Location**: this one-time table and command results; no permanent
  inventory script or second execution registry.

## Verification Summary

### Coverage map and discovery

`unit-tests` declares exactly `python3 -m unittest discover -s tests -t .`, is
required in `all-files`/`ci`, and remains unchanged. The loader default pattern is
`test*.py`; all current matching modules are the 56 `test_*.py` files below, so
an explicit `test_*.py` inventory and exact argv discover the same cases.

The one-time census used `unittest.TestLoader().discover('tests', top_level_dir='.')`,
recursively flattened the suite, counted `case.id()` and owning modules, and
checked `loader.errors`. Baseline: **56 modules / 1,290 cases / no load errors**.
Final: **56 modules / 1,288 cases / 1,288 unique IDs / no load errors**. Subtests
are assertion scenarios within those cases, not extra discovered cases. The
external-service module changes from 12 to 11 cases and strict-cutover from
58 to 57; all other counts are stable.

Owner/evidence coverage is: registry and runner source for discovery and gates;
module AST, test bodies, target calls, imports and helper consumers for assertion
families; direct gate source for standalone tests; retained negative execution
and exact diff for the retirement. This is a semantic source audit and runnable
regression evidence, not a claim of measured application branch coverage.

### One-time module disposition

All module names below are relative to `tests/`. Caller **U** means the exact
`unit-tests` discovery above through `qa.py` / `run-validation-lane.py` and hosted
`ci.yml`'s `qa.py ci`. **A** additionally means
`run-archive-contract-tests.py` in quick/staged. Case counts describe the baseline;
only the explicitly marked retirement changes them. Size is an inspection cue,
never a deletion criterion. "Keep" means no equivalent replacement or absent
current contract was proved.

| Module | Caller / cases | Distinct assertions or failure meaning; candidate examined | Decision |
| --- | --- | --- | --- |
| `test_affected_surface_migration.py` | U / 16 | Deleted-source routing needs complete current Git proof; lanes, loader cleanup, NUL CLI and unsafe aliases fail closed; historical-name candidate | Keep: proof-aware routing is current |
| `test_agent_evaluations.py` | U / 24 | Groundedness, authority, boundary, handoff and expected-failure grading; response/citation path, schema, byte and disclosure bounds | Keep: tests the grader, not provider quality |
| `test_agent_governance.py` | U / 53 | Shared owner, native projections, skill closure, model/sandbox binding, hook wiring and snapshot failure; 1,022-line size candidate | Keep: distinct provider/permission boundaries |
| `test_agent_governance_consumers.py` | U / 39 | Retired instruction consumers versus proved history; held bytes, descriptor races, bounded Git/pipe cleanup and diagnostics; 1,099-line legacy/size candidate | Keep: active history/security reader contract |
| `test_archive_catalog_reverification.py` | U+A / 16 | Catalog objects, reachability, modes, exact retained bytes, missing members, default branch and shallow history | Keep: full-history proof is not stale inventory |
| `test_archive_citation_decision.py` | U+A / 10 | Ordered citation rules by source/target profile and incident exemption | Keep: decision function and integration callers differ |
| `test_archive_cutover.py` | U / 36 | Atomic partition/index parity, sealed mappings, replacement authority, inventory bounds and payload-free errors; 1,246-line one-off/size candidate | Keep: finite sealed recovery proof still consumed |
| `test_archive_disposition_lifecycle.py` | U+A / 46 | Exact bodies/packages, required members, approved removal, prior/merge catalog persistence, recreation denial | Keep: lifecycle transitions and history differ from catalog parsing |
| `test_archive_disposition_routes.py` | U / 29 | Mirrored class/status routing, source terminal edges, additive sealed records and current-authority rejection | Keep: legacy generation remains recoverable |
| `test_archive_dispositions.py` | U+A / 25 | Retention classes, envelope/catalog grammar, rebased links, scope routes and index parsers | Keep: parsing and projection contracts |
| `test_archive_generation_fixture.py` | U / 1 | Derived legacy registry equals the exact merged Git blob; one-off fixture candidate | Keep: validates shared historical fixture fidelity; absent-history skip is explicit |
| `test_archive_historical_proof.py` | U / 23 | Held archive payload, source identity and exact consumer mentions; import isolation and false-history rejection; 817-line candidate | Keep: proof admission and import behavior |
| `test_archive_reappraisal.py` | U+A / 29 | Assessment table/schema, removal approval/hold and citation eligibility | Keep: current reappraisal contract |
| `test_archive_recovery.py` | U / 39 | Exact Git recovery, envelope collisions, path/output confinement, bounded protocols, durable-ref choice; 1,158-line legacy/size candidate | Keep: recovery and security boundaries |
| `test_archive_registry_contract.py` | U+A / 18 | Unit/mode/citation registry validation, fixed legacy membership and archive-gate wiring | Keep: legacy membership is sealed provenance, not a deletion quota |
| `test_archive_validation.py` | U / 96 | Envelope immutability, migration generations, inventory/index parity, bounded readers, composition and current authority; 3,021-line size candidate | Keep: distinct rule IDs, modes and historical proofs; no broad rewrite justified |
| `test_check_secret_handling.py` | U / 2 | Kiali secret reference allowed while plaintext is rejected | Keep: both sides of secret scanner boundary |
| `test_ci_qa_workflow.py` | U / 14 | One QA owner, fail-closed summary, delivery policy, named checkout, strict tool publication, cache and wall-clock budget | Keep: workflow semantics, not duplicate execution |
| `test_commit_contracts.py` | U / 4 | Authored message syntax, generated exceptions, historic punctuation and changelog first-match | Keep: current versus historical grammar is deliberate |
| `test_common_agents_archive_routes.py` | U / 7 | Successor closure and exact sealed identities; current owner diagnostics; navigation rejects copied status; one-off candidate | Keep: immutable recovery and current navigation remain distinct |
| `test_common_agents_document_routes.py` | U / 10 | Current common routes, synthetic response exclusion, native metadata, hidden corpus, English and retained identity | Keep: document routing differs from runtime projection validation |
| `test_completed_state_migration.py` | U / 6 | Current completed spelling, historical done normalization, frozen bodies, no reopening and per-commit registry replay | Keep: apparent conflicting spelling is generation-specific |
| `test_current_executable_references.py` | U / 12 | Current executable existence versus terminal Git-first recovery, data exclusions, proposal semantics and delegation | Keep: current and historical callers require opposite outcomes |
| `test_document_artifact_identity.py` | U / 8 | Path-bound IDs, duplicate IDs outside include scope, verified moves and reserved historical identities | Keep: identity safety |
| `test_document_language.py` | U / 27 | Prose/code/fence classification, language profiles, pending/terminal handling and contradictory registry rules; exact-body candidate | Keep: identical assertion body calls language-specific diagnostics |
| `test_document_lifecycle_agent_roster_cutover.py` | U / 3 | Two-provider boundary, neutral/Claude profiles and absence of retired finite roster authority; legacy/overlap candidate | Keep: provider boundary plus lifecycle target exported to migration tests |
| `test_document_lifecycle_archive_cutover.py` | U / 54 | Exact finite-manifest admission, modes, OIDs, current lifecycle graph and sealed target reachability; 1,804-line candidate | Keep: finite history still participates in admission |
| `test_document_lifecycle_cumulative_history.py` | U / 21 | First-parent cumulative creation, dirty-tree isolation, invalid edges, merge/copy/rename denial and proof budgets; 885-line candidate | Keep: history topology and evidence budgets |
| `test_document_lifecycle_migration.py` | U / 25 | Proposed Git bytes and trusted policy before regex compilation; moves, sealed publication and index drift | Keep: proposed-state security differs from current recovery |
| `test_document_strict_cutover.py` | U / 58 → 57 | Closed Stage 99 authority, templates, identity/relationships, retired capacity and strict CLI; 1,296-line legacy/size candidate | Retire only `test_retired_program_and_standalone_planes_are_absent`; retain exact root-key set and all other current/sealed checks |
| `test_documentation_link_boundary.py` | U / 28 | Archive citations, held catalog proofs, outside-doc stage references, normalization and exact machine exceptions | Keep: caller integration and normalization are distinct |
| `test_external_service_contracts.py` | U / 12 → 11 | Service/backend joins, selector exclusion, namespace/address/DNS/path safety and CLI failures; positive corpus rerun candidate | Retire only `test_actual_repository_contracts`; retain all 11 behavioral cases |
| `test_generic_migration_recovery.py` | U / 42 | Generic sealed moves, bounded held-input proof, CLI, literal/symlink consumers, composition and drift; 1,361-line candidate | Keep: shared fixtures plus independent current/historical failures |
| `test_infrastructure_tempfiles.py` | U / 6 | Stubbed verification commands prove private concurrent tempdirs, failure status, signal cleanup and cleanup-error precedence | Keep: no live verification is executed |
| `test_json_schema_validation.py` | U / 5 | Local refs, invalid schema redaction, offline external-ref rejection and no deprecation warning | Keep: shared helper has its own boundary |
| `test_k8s_pre_edit_hook.py` | U / 54 | Provider payload forms, confined paths/worktrees, pinned executable, patch transport and advisory shell observation; 835-line candidate | Keep: provider boundary; no claim of native event delivery |
| `test_markdown_render_cache.py` | U / 4 | Render provenance, lazy definitions, caller-owned mapping and text-only cache behavior | Keep: equal strings need not carry equal provenance |
| `test_prompt_input.py` | U / 22 | Read-only prompt assembly, input limits, staged/unstaged subjects, command allowlist and no network | Keep: security and user-input semantics |
| `test_qa_runner.py` | U / 39 | Isolated final/index snapshots, symlinks/races, redacted diagnostics, tool ownership and exact reuse invalidation; 1,188-line candidate | Keep: prior Task 0002 changes are outside this cleanup |
| `test_readme_navigation.py` | U / 29 | Direct-child routing, completeness, copied status, pending/exempt paths and registry contradictions; exact-body candidate | Keep: same-looking assertion calls navigation-specific diagnostics |
| `test_reference_pack_routes.py` | U / 10 | Stage 90 category routes, missing/duplicate/nonregular topology, exact index drift and retired wiki claims | Keep: targeted topology, not generic gate PASS |
| `test_repository_quality_rules.py` | U / 3 | Synthetic visible headings, residue lines and secret-value output detection | Keep: isolated diagnostics rather than full corpus reruns |
| `test_run_validation_lane.py` | U / 74 | Closed subprocess environment, trusted tools, timeout/overflow/descendants/signals, dispatch and evidence reuse; 2,333-line candidate | Keep: security cleanup scenarios have distinct failure meanings |
| `test_validate_affected_surfaces.py` | U / 11 | Fixture routing, CI range/rename, gate coverage deduplication, NUL transport and bounded Git failures | Keep: registry selector behavior |
| `test_validate_agent_core_cutover.py` | U / 6 | Parent symlink, redacted JSON/schema/CLI errors, tier fragments and offline refs; legacy-name candidate | Keep: still calls current agent registry implementation |
| `test_validate_agent_harness_contract.py` | U / 12 | Current registry loader path/size/UTF-8/duplicate-key safety, projection symlink and isolated CLI dispatch; legacy-name candidate | Keep: historic filename does not mean obsolete target |
| `test_validate_agent_registry.py` | U / 27 | Closed providers/roles/skills, narrowing-only permissions, handoffs, models and provider-specific overrides | Keep: provider boundary; loader is imported by governance tests |
| `test_validate_ci_python_contract.py` | U / 70 | Pinned/hash-locked dependencies, command grammar/bypass rejection, credential-free full checkout and approved setup; 1,438-line candidate | Keep: security matrix varies launchers/options/jobs with distinct bypasses |
| `test_validate_github_actions_security.py` | U / 5 | Fixture-driven permissions, action pinning, checkout tokens, retained artifacts and malformed workflow shapes | Keep: subtests preserve distinct supply-chain failures |
| `test_validate_gitops_change_set.py` | U / 8 | Exact object identities, FIFO/directory rejection and bounded Git errors through shared synthetic cases | Keep: independent GitOps behavior |
| `test_validate_knowledge_surface.py` | U / 8 | Stale/sensitive facts, missing owners/entries, copied policy and registry admission | Keep: owner map semantics |
| `test_validate_vault_eso_contracts.py` | U / 2 | Exact mutation diagnostics and internal input/security boundaries via shared helpers | Keep: case count hides multiple required subtests |
| `test_validation_bounded_io.py` | U / 6 | Parent/leaf links, same-size and growing races, encoding/byte limits, process timeout/output bounds | Keep: shared primitive boundary differs from caller diagnostics |
| `test_validation_profiles.py` | U / 20 | Gate/profile ownership, aliases, skills, registry races/size/duplicate keys and reuse admission | Keep: profile completeness and safe declaration parsing |
| `test_validation_tooling_ownership.py` | U / 20 | Hook/validator ownership, fixture consumers, discovery completeness, no production self-tests or gate reruns | Keep: protects the aggregate and fixture retirement contract |
| `test_workspace_boundary.py` | U / 16 | Exact index ignore policy, no child traversal, modes/OIDs/NUL bounds and sanitized Git | Keep: workspace/index isolation |

### Standalone callers, imports and fixtures

| Active path | Distinct failure meaning / overlap analysis | Disposition |
| --- | --- | --- |
| `archive-contract-tests` → `scripts/run-archive-contract-tests.py` → the six U+A modules above (144 cases) | Early archive contract regression gate in quick/staged; `coveredBy: unit-tests` suppresses repeat when aggregate is selected | Keep caller and six modules; routing deduplication is tested by `test_covered_gate_runs_once_per_profile_and_lane` |
| `policy-gates` → `scripts/validate-policy-gates.sh` → `conftest verify --policy policy/conftest` → `kubernetes_test.rego` (16 rules) | Triggering/non-triggering Secret, Application/ApplicationSet namespace, AppProject wildcard, nested/latest images and AnalysisTemplate count/numeric-condition scenarios | Keep all security/GitOps tests; `conftest test` separately validates corpus and cannot replace negative rule verification |
| `agent-evaluation-cases` → `.agents/evaluations/run-agent-evaluations.py` → 19 case JSON / synthetic response pairs | Role-specific expected groundedness, authority, external boundary and handoff failures; unit tests separately check grader false-positive/false-negative behavior | Keep; recorded responses establish synthetic grading, not remote agent quality |
| `pre-commit` → pinned external hooks at manual stage | Formatting, syntax, secrets, Actions and manifest lint; no direct repository Python unittest invocation | Keep; these are independent tool gates, not duplicate discovered test callers |
| `affected_surface_mutations.py` / `fixtures/validation-surfaces.json` | Consumed by `test_validate_affected_surfaces.py`; malformed registry, selected paths and range/transport scenarios | Keep; independent consumer remains |
| `git_fixture.py` | Consumed by archive recovery/validation/routes, generic migration, completed-state and cumulative-history tests | Keep exact temporary Git-object construction |
| `archive_generation_fixture.py` | Consumed by generation fidelity, disposition-route, lifecycle archive-cutover and generic migration suites | Keep; frozen-generation fixture remains tested against Git |
| `gitops_change_set_cases.py` / `fixtures/gitops-change-set/` | Consumed by `test_validate_gitops_change_set.py`; base/head manifests, identity and nonregular-resource scenarios | Keep every fixture; no final consumer removed |
| `vault_eso_contract_cases.py` / `fixtures/vault-eso-contracts.json` | Consumed by `test_validate_vault_eso_contracts.py`; required security mutation diagnostic families | Keep every fixture |
| `fixtures/github-actions-security.json` | Consumed by `test_validate_github_actions_security.py`; supply-chain and workflow mutation families | Keep |

Test-to-test imports were traced: affected-surface migration, archive historical
proof and document lifecycle migration use `test_generic_migration_recovery`
fixtures; completed-state migration uses the archive-lifecycle `VALIDATOR`;
lifecycle migration uses the roster-lifecycle `VALIDATOR`/`ROOT`; governance uses
the registry test's loader. These import modules/functions or instantiate the
fixture owner, not duplicate `TestCase` classes into discovery. Final IDs are
unique. No import, fixture or direct caller becomes dead when the two methods
are removed. Extracting all these helpers would widen the diff without a proved
retirement benefit, so their current consumers and failure checks are retained.

The two identical AST method bodies named `test_consistent_contract_passes`
are not semantic duplicates: `self.faults()` reaches
`_document_language_registry_diagnostics` in one module and
`_readme_navigation_registry_diagnostics` in the other. Likewise, multiple
symlink/timeout tests cross different public consumers and diagnostics. The
legacy `done` expectations are intentionally restricted to old/frozen registry
generations; current `completed` expectations do not conflict. A second semantic duplicate in strict-cutover reads the same raw registry
as the retained archive assertion and is also covered by the strict exact-root-key
assertion; its removal is proved below. No truly obsolete module or contradictory
same-contract expectation was proved. Oversized suites
were retained because moving or deleting their distinct failures would not be
a supported cleanup. The existing test README and Task criterion already state
the retirement boundary, so no quality-policy duplication was added.

### Retirement proof

Removed `ExternalServiceContractsTests.test_actual_repository_contracts`.
It called `validate_documents(ROOT, sorted((ROOT / PREFIX).glob('*.yaml')))` and
asserted `[]`, without mutation, diagnostic contract or routing assertion. The
registered `external-service-contracts` gate calls the same validator from its
CLI over tracked and nonignored YAML/YML input under the same prefix; that gate
runs in quick, staged and full. The gate's corpus selection also covers YML and
fails on an absent inventory, so the removed positive check was no broader.

Before removal, the registered gate passed and four selected tests passed:
the retiring positive check plus retained backend mismatch, CLI failure and
path-confinement cases. A temporary in-memory mutation replaced
`validate_documents` with a function returning `[]`; the retained backend/CLI
checks produced **five assertion failures across two cases, zero errors**
(three port-field subtests, missing backend and CLI failure). Thus the retained
checks detect a disabled validator. The first harness attempt let unittest
reload the class checker and observed zero failures; the corrected harness
froze `setUpClass` around the patched checker. No source mutation was made.

The retained full module preserves positive backend translation and selector
exclusion, negative namespace/address/DNS/selector validation, redacted malformed
inputs, path escape/symlink rejection and CLI inclusion of new nonignored input.
No security or GitOps negative behavior, module, fixture, gate or caller is
removed. Recovery is the parent Git object; no archive document is created for
a removed test method.

The second removed method is
`Stage99TerminalAuthorityTests.test_retired_program_and_standalone_planes_are_absent`.
It asserted absence of `programLineage` and `standaloneExecutions` in the raw
Stage 99 registry. The retained strict
`test_v9_registry_uses_the_common_public_model` asserts the complete root-key set,
and retained archive
`ArchiveTransitionLinkTest.test_public_registry_has_no_retired_execution_rosters`
asserts those same two absences against the same raw file. All three passed
before deletion. Adding each forbidden key independently to an in-memory copy
made **both retained assertions fail**: four expected failures across the two
mutations. No archive test was changed. This removes repeated positive inventory
work without removing the historical/current authority boundary.

### Commands and results

Commands below ran from the stated worktree through `rtk proxy`; displayed argv
omit that transparent wrapper. Tool identities: Python 3.12.3 and RTK 0.49.0. Final lane
results are recorded before handoff. Sandbox startup once failed with
`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; authorized
escalated local execution was then used, without changing provider trust.

| Step | Exact command / observation | Result |
| --- | --- | --- |
| Baseline discovery | `python3 -m unittest` loader API with `discover('tests', top_level_dir='.')`; recursive ID/module census | PASS: 56 / 1,290; no load errors; no tests executed by census |
| Before-retirement checks | `python3 -m unittest -v tests.test_external_service_contracts.ExternalServiceContractsTests.test_missing_or_mismatched_backend_rejects tests.test_external_service_contracts.ExternalServiceContractsTests.test_cli_includes_new_nonignored_manifest_and_redacts_failure tests.test_external_service_contracts.ExternalServiceContractsTests.test_paths_cannot_escape_or_follow_links tests.test_external_service_contracts.ExternalServiceContractsTests.test_actual_repository_contracts` | PASS: 4 tests, 0.094s |
| Retained negative mutation | In-memory `mock.patch.object(Cases, 'setUpClass')` plus `mock.patch.object(Cases.checker, 'validate_documents', return_value=[])`; run mismatch/CLI cases; assert 2 run, 5 failures, 0 errors | PASS: expected RED observed before deletion |
| Retained corpus gate | `python3 .agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py --root .` | PASS: static joins valid |
| Focused, registry and discovery | `python3 -m unittest tests.test_external_service_contracts tests.test_validation_profiles tests.test_validate_affected_surfaces tests.test_validation_tooling_ownership` | PASS: 62 tests, 7.481s |
| Final discovery | Same loader census; additionally compare unique `case.id()` values | PASS: 56 / 1,288; 1,288 unique; no load errors |
| Strict duplicate negative proof | Invoke the three named methods unchanged; for each forbidden key patch strict class `registry` and archive `json.loads` with the same extended dict | PASS: baseline 3 assertions; both retained checks reject each key (4 expected failures) |
| Strict/discovery focused | `python3 -m unittest tests.test_document_strict_cutover.Stage99TerminalAuthorityTests.test_v9_registry_uses_the_common_public_model tests.test_validation_tooling_ownership` | PASS: 21 tests / 5.961s |
| Diagnostic raw aggregate | `python3 -m unittest discover -s tests -t .` | FAIL: 1,289 tests / 1058.968s / 9 failures, 13 errors; unstaged Task/index mismatch; superseded by isolated final validation below |
| Baseline failure comparison | `qa.repository_snapshot(Path.cwd(), staged=True)` at unchanged index HEAD `7ad42d2e`; subprocess `python3 -m unittest -v tests.test_archive_recovery.PinnedMigrationRecoveryCliTest.test_cli_verifies_exact_sealed_mig0004_through_pinned_recovery tests.test_archive_validation.ArchiveTransitionLinkTest.test_active_source_cannot_use_declared_migration_or_tasks_aliases` | PASS: 2 tests / 75.624s; baseline inputs, no edits to source or index |
| Interrupted isolated attempt | `python3 scripts/qa.py full` on tree `002bfa84d873247fe73a110e36074989bdf9cb20` | Interrupted (exit 130): source review found MD012 duplicate blank line; 19 gates had passed and unit aggregate had started, without a completion result. Supervisor directed normal interruption before correcting the known-invalid Task input |
| Focused Markdown | `pre-commit run markdownlint-cli2 --files docs/03.specs/0103-qa-evidence-reuse/tasks/tsk-0007-test-disposition.md` | PASS after MD012 repair; subsequent change only records this result |
| Isolated full | `python3 scripts/qa.py full` on tree `e2b4310b9e75b90f2073cb7f8672cf6d50da06a6` | FAIL overall: pre-commit Ruff formatter modified pre-existing `tests/test_ci_qa_workflow.py` in the disposable snapshot. Unit-tests and all 22 non-pre-commit gates PASS; completed pipes and cleanup |
| Final focused checks | `python3 -m unittest tests.test_external_service_contracts tests.test_validation_profiles tests.test_validate_affected_surfaces tests.test_validation_tooling_ownership tests.test_document_strict_cutover.Stage99TerminalAuthorityTests.test_v9_registry_uses_the_common_public_model` | PASS: 63 tests / 7.525s; final test bytes |
| Initial affected lane | `python3 scripts/qa.py quick` | FAIL only repository-quality: this Task included a machine-local absolute checkout path; 6 other gates PASS. Repaired to a portable worktree name |
| Final affected lane | `python3 scripts/qa.py quick` on tree `fa30de75389d523eadbf45f0815e53103b6cdd72` | PASS: all 7 selected gates; complete pipes and cleanup. Subsequent edits only record evidence |
| Exact index | `python3 scripts/qa.py staged` on trees `e3593e0291bdc9d31dfe989e19681bcf072397e9` and final implementation tree `c5e22a8b83ecdddfd516ba4f682328768c04ae4e` | PASS: all 7 selected gates on each distinct Task-evidence snapshot; complete pipes and cleanup |
| Diff and file hooks | `git diff --check`; `git diff --cached --check`; `pre-commit run --files docs/03.specs/0103-qa-evidence-reuse/tasks/tsk-0007-test-disposition.md tests/test_document_strict_cutover.py tests/test_external_service_contracts.py` | PASS: exact three-file set; applicable file hooks including Ruff, Markdown and secrets passed; irrelevant file types explicitly skipped |
| Implementation commit | `git commit -m "test: retire proven redundant QA tests"` | PASS: `e0c6955e74ae15e958976908b666866eab922fd5`; hooks were not disabled or changed |
| Message verification | `pre-commit run commitizen --hook-stage commit-msg --commit-msg-filename /tmp/task7-implementation-message.txt`; same argv for `/tmp/task7-evidence-message.txt` | PASS for the actual implementation message extracted with `git log -1 --format=%B` and planned evidence message. Implementation message check occurred after its commit; follow-up message check occurred before its commit |

The removed-method file's final SHA-256 is
`27d620d3421731c9a703474f18a2fdfb12bb81ae5a656c14db558ada34798510`;
the unchanged registry SHA-256 is
`2a1af8e7bb6692b1ceb0511945d06226c8fd2eb0a31ed28966a9e73e87aaa985`.
The strict-cutover test SHA-256 is `912746df3f25f9364c61de823fea204101f00f94dbdab4d60bb7242a559e0bcc`.
These are this observation's inputs, not policy pins. Later Task-only evidence
updates are distinguished from test-code inputs; they do not request another
unchanged unit aggregate.

The isolated full failure was traced with `pre-commit run ruff-format --all-files
--hook-stage manual` inside an exact-index `qa.repository_snapshot(staged=True)`.
Only `tests/test_ci_qa_workflow.py` changed (29 added / 7 removed formatting lines);
97 files were unchanged. The source checkout was not changed. This pre-existing
Task 0002-owned file is outside Task 0007 ownership. The supervisor routes its
repair and fresh full evidence to that owner. The successful unit gate covers
this recorded tree only; it does not prove later changed test bytes.

### Diagnostic aggregate disposition

The direct discovery run began before Task evidence authoring finished. Its
working tree and index diverged, so it is **diagnostic FAIL**, not completion
evidence. Every failure/error reported `RECOVERY-MIGRATION-TARGET: current target
differs between index and worktree`; link wrappers surfaced
`WORK-054 WP-004B migration recovery proof differs`. No timeout or cleanup failure
was observed. The unchanged baseline snapshot passed representative failure and
error cases. Final validation uses QA's isolated, index-consistent snapshot;
no failing archive assertion is deleted or weakened.

Exact raw failure IDs (9 assertions, 8 distinct methods):

- `tests.test_archive_cutover.ArchiveCutoverTest.test_work107_repository_is_exact_stable_93_to_17`
- `tests.test_archive_recovery.PinnedMigrationRecoveryCliTest.test_cli_verifies_exact_sealed_mig0004_through_pinned_recovery`
- `tests.test_archive_validation.ArchiveValidationTest.test_repository_archive_git_snapshot_is_bounded_and_under_sixty_seconds`
- `tests.test_archive_validation.ArchiveValidationTest.test_repository_archive_ignores_retired_stage99_namespace_projection`
- `tests.test_archive_validation.ArchiveValidationTest.test_repository_archive_supports_isolated_package_and_direct_imports` (both `from scripts import archive_validation` and `import archive_validation` subtests)
- `tests.test_archive_validation.ArchiveValidationTest.test_repository_archive_v2_has_closed_namespace_and_index_parity`
- `tests.test_archive_validation.ArchiveValidationTest.test_repository_four_spec_overlaps_use_only_exact_batch_evidence`
- `tests.test_archive_validation.ArchiveValidationTest.test_repository_inventory_separates_exact_archive_migration_controls`

Exact raw error IDs: prefix
`tests.test_archive_validation.ArchiveTransitionLinkTest.` for the following 12:

- `test_active_source_cannot_use_declared_migration_or_tasks_aliases`
- `test_future_accepted_adr_cannot_enter_historical_migration_waiver`
- `test_future_done_task_cannot_enter_historical_migration_waiver`
- `test_mig0004_link_projection_accepts_semantically_valid_row_growth`
- `test_mig0004_link_projection_composes_through_a_later_sealed_row`
- `test_mig0004_link_projection_drops_a_vacated_endpoint`
- `test_removed_directory_link_needs_every_file_proved`
- `test_terminal_current_progress_uses_no_historical_projection`
- `test_terminal_route_does_not_project_an_active_stale_owner_edge`
- `test_work054_historical_projection_rejects_undeclared_retired_edge`
- `test_work109_manifest_targets_compose_through_exact_mig0002`
- `test_work109_projection_drops_a_vacated_move_and_keeps_coverage`

The thirteenth is
`tests.test_archive_validation.ArchiveValidationTest.test_mig0004_recovery_is_integrated_sealed_and_semantic`.
The tool display truncated two headers; a bounded rerun of the two
`test_terminal_*` methods recovered both exact IDs and the same expected
configuration error (2 cases / 2 errors). No second raw aggregate was run.

### Review, limits and handoff

Implementation commit: `e0c6955e74ae15e958976908b666866eab922fd5`
(`test: retire proven redundant QA tests`), based on `7ad42d2e`. This later
Task-only evidence change records its final dispositions without naming its
own future commit. Final test bytes remain those of the recorded full unit
gate; the Task-only change receives affected and exact-index document checks.

Hook observation: repository-local `core.hooksPath` resolves to `scripts/githooks`;
both configured hook wrappers are present. Their shared `chained-hook.sh`
attempts a configured global hook and then a common Git-directory workspace
hook, treating an absent nonexecutable target as no work. The latter targets
are absent in this clone; that does not mean the configured wrappers are absent.
The successful commit output contains no per-hook trace, so this record makes
no automatic Commitizen execution claim. File hooks passed explicitly before
the implementation commit; its actual message passed explicit pinned Commitizen
afterward. No hook configuration was changed; the follow-up message is checked
before commit.

- Writer: `/root/implement_task7`, scoped quality responsibility; self-review
  confirms only two method removals (12 lines total) and this evidence record.
- Independent reviewer: `/root` or its separately assigned read-only reviewer,
  **PENDING**. The writer does not certify independent review. Reviewer should
  check each disposition family, gate equivalence and retained negative proof.
- Hosted CI/full integration: **DEFER** to Task 0006 and the supervising agent's
  final SHA/run; local test success makes no hosted or provider-runtime claim.
- Required full lane: **FAIL** from the pre-existing CI test formatting defect;
  supervisor owns the Task 0002 repair and refreshed integration evidence.
- Residual risk: source/AST family audit cannot prove all possible semantic
  equivalences. Unproved candidates stay. A standalone unittest invocation still
  tests behavior; current-corpus correctness belongs to the registered gate.
- Next owner: supervisor for independent semantic review, final integration and
  durable completion evidence. No external action or additional cleanup inferred.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-007](../plan.md#work-breakdown) | In progress: VAL-QER-012 audit complete; two redundant assertions retired; focused/quick/staged PASS, full FAIL from pre-existing formatting; independent review pending | Module/caller table, retained-negative proof and command results in this record |
