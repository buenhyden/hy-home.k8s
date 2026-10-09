---
title: "Provider, Context and Skill Governance Follow-up"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0005"
parent_ids: ["SPEC-0105-PLAN-0001"]
---

# Task: Provider, Context and Skill Governance Follow-up

## Overview

This Task owns the new P07 local execution for
[WORK-009](../plan.md#work-breakdown) and
[VAL-P01-009](../spec.md#success-criteria--verification-plan). The completed
parent Spec and Plan route this follow-up without restarting earlier Tasks.
[Task 0004](tsk-0004-current-contract-review.md) remains blocked on its own
common-edition and protected actual-PR/control obligations; P07 local work
does not decide them.

## Inputs

- Intake observed clean local `main` at
  `34828945b1ce084b7287dfeebde757ff8500af7a`, with empty index and no
  unstaged changes. The isolated branch `codex/p07-provider-governance` and
  `.worktrees/p07-provider-governance` start at that commit. Ignored
  checkout-root `_workspace/p07-provider-governance/intake-input.json`
  records the initial writer/scope map; it is an intake observation, not an
  implementation or validation result.
- The Spec/Plan/Task draft intake passed six selected exact-index gates with
  rc 0 on tree `10880150f683f214770ec6f312e276fcb750abac`, with the index
  unchanged. `_workspace/p07-provider-governance/intake-index-qa.json` has
  SHA-256 `3293114f1b361f0a7d72f435155762cd1608d00126f44b67fdce583fc773b6b8`
  and its log SHA-256 is
  `8f26ad19d28212bb67255b0fad2e5d7567ee35f12d30718515f2742307cfb4e6`.
  The actual message SHA-256
  `3c123c3563eef49f0af0eddbb5d291738e5bef77136a8fb29af9a391e2ff7a11`
  passed the pinned message check; a normal commit created
  `c718b2d653d9adcbcacbe8a30ce346041888bf4f` at that tree.
  `_workspace/p07-provider-governance/intake-commit.json` has SHA-256
  `db179411defc7da0e1294b78e3ce583da59c2c7092f2eafdab7621a141abf99d`.
  These are intake-document results, not P07 implementation or native proof.
- The ready-state Task alone passed six selected exact-index gates with rc 0
  on unchanged tree `4a8b854be33b42bb8ec0d8a1903e6f30f5900a7b`, and its
  actual message check and normal commit returned rc 0. Commit
  `0033d009bf9a1bd7b3c9b5603f1a2e969245f35a` records the legal
  draft-to-ready edge, not the P07 implementation. Ignored
  `_workspace/p07-provider-governance/ready-index-qa.json` has SHA-256
  `aba81011ae877769cb18f934423624cf0920660561c175b673b129d8ca18e8ba`;
  `ready-commit.json` has SHA-256
  `5c9d51c2e2803585ec8c188961d8207945fd8e6ab851bfd3a9f46b1c2090eaef`.
- The first P07 source, reviewed permanent documents and this Task were
  committed as `c64edee2f7d579bafe0fb125ae2ad962e6f5ebd8` after a
  selected staged check. Scope review then found the validation registry's
  generic `scripts/` and `tests/` fallback selected unrelated Archive and
  K8S gates for this agent-governance input. Follow-up routing work starts
  from that commit on `codex/p07-agent-validation-routing` in
  `.worktrees/p07-agent-validation-routing`. That observation was the input
  to the separate routing correction recorded below, not the final state.
- The routing correction and Task progress were committed as
  `d8fedf3ee6a763aee955e0d2b734de7db9272769`; `git merge --ff-only`
  then advanced clean local `main` from the intake base
  `34828945b1ce084b7287dfeebde757ff8500af7a` to that commit at tree
  `3b277f3b6b9af02e1d9b65e1c3e83f0952b134a6`. The two source units,
  their distinct selected checks and the local integration are observed.
  The closing Task document itself awaits its own final index/message/normal
  commit; the terminal delivery receipt records that administrative step
  after it occurs without a self-referential future commit ID here.
- A subsequent read-only remote-ref check observed `origin/main` at
  `d8fedf3ee6a763aee955e0d2b734de7db9272769`, equal to local main.
  Cached `origin/main` matched and its reflog said `update by push`, but
  the push initiator is unverified. The root execution record contains local
  commits, a local fast-forward and read-only ref commands, with no explicit
  push or remote merge command. This observation is not P07 PR, hosted style,
  native runtime, publication or common-edition proof.
- The current user's P07 request authorizes scoped local investigation,
  policy and consumer repair, selected validation, normal logical commits,
  local main integration and owned cleanup. Remote push, PR, dispatch,
  deployment, tag/Release, paid runtime, trust bypass, private/global
  configuration and credential operations are outside this authorization.
- [SPEC-0105](../spec.md), [Plan WORK-009](../plan.md#work-breakdown),
  [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md)
  and [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
  give the current change lineage. Neutral owners are
  [model selection](../../../../.agents/governance/model-selection.md),
  [context and memory](../../../../.agents/governance/context-and-memory.md),
  [work lifecycle](../../../../.agents/workflows/work-lifecycle.md) and the
  [role registry](../../../../.agents/roles/registry.json). Native facts and
  configuration belong to [Codex](../../../../.codex/provider.md) and
  [Claude](../../../../.claude/provider.md) provider surfaces.
- The attached `WGOV-CORE / 3.0.0-draft.2` is a proposal. The user's C02
  correction directs first establishment of one common candidate when no
  existing approved source is found. The same review candidate
  `3.0.0-draft.3` has proposed owner `buenhyden` and proposed
  Project-Template path `.agents/governance/shared-standard.md`; no final
  approved source revision, approval reference, local adoption or joint
  four-repository adoption is established here. C01/C03/C08/C10 guide
  comparison, not native authority or an intake prerequisite.
- Initial read-only observations: the current model-selection policy still
  refers to stopping at an observed elapsed/shared budget and to a remaining
  retry budget, while work-lifecycle and quality already reject business
  deadlines, session timeboxes and reserve approvals. The neutral registry
  stores concrete per-provider model/effort bindings consumed by schema,
  validator, tests and projections. Whether those values migrate to native
  owners is a coupled design and consumer decision; no file move or native
  runtime result is presumed from this intake.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-009 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | Compare current neutral/native model, skill, context, loop and workspace owners; repair verified local conflicts with affected consumers and evidence | platform | frontmatter | PASS | EVD-P07-024 through EVD-P07-028 resolve the planned checks with actual reviewed source, selected regression/QA, messages and local main integration; native runtime and common-edition approval remain separate next-owner work |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P07-001 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Current registry, schema, validator, provider notes/configuration and projections; focused mismatched-owner and valid-control cases | NOT_RUN | Pending exact source, commands and results in this Task | yes | none |
| EVD-P07-002 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Current registered skill packages, actual callers, sidecars, hook adapters and trust/cancellation paths; focused changed-behavior and refusal cases | NOT_RUN | Pending inventory, commands and results in this Task | yes | none |
| EVD-P07-003 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Context, memory, loop and workspace boundaries | Current model/context/workflow policies, memory pointers and temporary workspace consumers; actual budget, no-progress, cancellation and technical-limit distinctions | NOT_RUN | Pending source/consumer comparison and selected checks in this Task | yes | none |
| EVD-P07-004 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Provider-runtime and common-edition boundary | Repository-static input versus dated native observation, unavailable protected session and proposed common edition; separate next owners and no synthetic PASS | NOT_RUN | Pending evidence classification and actual limitations in this Task | yes | none |
| EVD-P07-005 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Final local index, message, review and integration | Final changed index, selected named regressions, actual candidate message, independent reviewers and local main input when source exists | NOT_RUN | Pending exact checks, review, normal commits and observed integration in this Task and Git | yes | none |
| EVD-P07-006 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | On original `34828945b1ce084b7287dfeebde757ff8500af7a`, `python3 -B` ran the ignored checkout-root `native-binding-red-probe.py` in two isolated coordinated-widening cases; the receipt records its exact argv and worktree. Both cases unexpectedly passed the old validator while neutral read-only class disallowed mutation; process rc 1, two failing tests. This is the pre-repair safety gap, not native enforcement evidence | FAIL | `_workspace/p07-provider-governance/red-result.json`, SHA-256 `9725bfed7a147815dda3f68d568a60090f0400b1cab1e82a3f5e3586b6211006`; stderr SHA-256 `de086720d72497e0efd0f3d6613218a30707dde471eaf39d30c45ef7a6670914` | yes | none |
| EVD-P07-007 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Read-only static inventory of 61 tracked skill-package/Claude-link paths, registry refs, Stage99 skill profile, validator/selector, hook adapters and named test consumers. This maps current readers but is not invocation or skill effect proof | PASS | `_workspace/p07-provider-governance/skill-consumer-inventory.json`, SHA-256 `0a5b50797371c97b148e4f44b1bbcc5be3c0c90c87a94b34fd8122e4d7d3e4a1` | yes | none |
| EVD-P07-008 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Independent architect reviewed existing AD-0006/ADR lineage and approved a neutral role/class/skill/path owner plus provider-native concrete binding tables, with existing projections as checked consumers and closed independent capability ceilings. This is design review, not implemented source or native runtime | PASS | `_workspace/p07-provider-governance/architecture-review.json`, SHA-256 `633e2cc240faf5b3866dc5cb160626d5e80119f49cc821dc3f057140ee628979` | yes | none |
| EVD-P07-009 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Provider-runtime and common-edition boundary | Read-only installed CLI/help/bundled catalog observation saw Codex 0.160.0, Claude 2.1.295 and relevant model/effort syntax. Version-command numeric rc and independent upstream pipeline rc were not retained. No authenticated model access, role discovery, hook delivery or permission enforcement was tested; runtime remains DEFER with the native operator | PASS | `_workspace/p07-provider-governance/native-support-observation.json`, SHA-256 `159deaa4ff27da998c76efa5cc625b9c7ba45f868456ca74fa077ed71d77a021` | yes | none |
| EVD-P07-010 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Independent code reviewer examined the six source files identified by `core-applied-source.json`; found and then verified repair of omitted binding paths in candidate admission and current native scan. Direct reader checks candidate membership and stable bytes; exact-index QA must separately establish indexed-byte input | PASS | `_workspace/p07-provider-governance/source-code-review.json`, SHA-256 `8edb42d98cd1756251e88603be9f4f4d62d46562c753a7e4a1482edcdeeda490` | yes | none |
| EVD-P07-011 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Independent security reviewer examined the same six source files and found the static neutral-ceiling gap repaired, while Claude shell prohibition and native runtime enforcement remain separate advisory/unobserved boundaries; reviewer ran no tests or native sessions | PASS | `_workspace/p07-provider-governance/source-security-review.json`, SHA-256 `a51c3ece105a9f9874498aa59c26052d44b35cbe352b8b046279b873d61f83d0` | yes | none |
| EVD-P07-012 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Focused `unittest` of registry, governance and consumers on the first source/test snapshot returned rc 1: 120 tests, 70 assertion failures and 8 errors. Copied fixtures intentionally reduced their role registries but retained native binding overrides for removed roles, causing premature `AGENT-NATIVE-BINDING` errors; this was not a passing suite | FAIL | `_workspace/p07-provider-governance/binding-focused-green.json`, SHA-256 `7618beb81eac654e29ae87df9a01b569964716ed79f5c4824feb794eab83b2d9`; log SHA-256 `47b6b6fa730d76af31d7d8de8ea7f07f6a3e1dd5fa0660f8db733b4877fd9d5e` | yes | none |
| EVD-P07-013 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | After fixture repair, the governance module still returned rc 1: 58 tests, one error from a copied registry using reduced roles with full-root native bindings. The named input was repaired and passed separately; no full 58-case rc 0 is inferred from that named result | FAIL | `_workspace/p07-provider-governance/binding-governance-postfixture.json`, SHA-256 `25f9424cdd531e14a337ad29247719eec18a73028ca1ae9cfc4bc84da29c9248`; log SHA-256 `54ed5080bd557fe83c17fdb0f38877d83063c0d816ffcf1e8f5411a29e45d641` | yes | none |
| EVD-P07-014 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Later combined three-module command returned rc 1: 122 tests, 121 passing and one diagnostic assertion failure. The shared bounded JSON parser correctly emits `AGENT-REGISTRY-INPUT` for duplicate keys, while the new test expected `AGENT-NATIVE-BINDING`; production guard remained unchanged | FAIL | `_workspace/p07-provider-governance/binding-focused-final.json`, SHA-256 `002a8086676f66eded44ac897f39aa3eac1b0e8fa18640cc7a91b60827415594`; log SHA-256 `b176b3ffb074cc76d0dbcc5894b989bd6a40b8bb220867a828414c8171d76d38` | yes | none |
| EVD-P07-015 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | On final test bytes the failed duplicate-key/wrong-provider named case returned rc 0, one test passing, after matching its diagnostic to the existing bounded parser. This resolves the one EVD-P07-014 assertion failure; the complete 122-case final-byte command was not rerun and final index admission is pending | PASS | `_workspace/p07-provider-governance/binding-final-resolution.json`, SHA-256 `1bd3664c241902b280a886dbf5b1a071f4f670f216df43223c01407c46b456f3` | yes | EVD-P07-014 |
| EVD-P07-016 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Final-byte `unittest tests.test_validate_agent_registry -q` returned rc 0, all 24 registry module cases passing; this is a scoped module proof, not a final three-module or staged-index admission | PASS | `_workspace/p07-provider-governance/binding-registry-finalmodule.json`, SHA-256 `49e1d41a65de2875c4c4bdb388974247a62e83eb958d4ab7ee022f710b6deda3`; log SHA-256 `74a7dcb15517e19b3c476e0ef28d2f1bd4d5e3dbd199e3b7623a3c65be4f019a` | yes | none |
| EVD-P07-017 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Final-byte `unittest tests.test_agent_governance tests.test_agent_governance_consumers -q` returned rc 0, 98 cases passing on the current source and copied-document inputs. Together with EVD-P07-016's separately observed 24-case rc 0, the three affected modules have current-input PASS in two commands; there is no single final 122-case command receipt. This refresh resolves the changed-input failures at EVD-P07-012 through EVD-P07-014 without erasing them | PASS | `_workspace/p07-provider-governance/binding-governance-consumers-currentdocs.json`, SHA-256 `4e498c6faf3ef7789882a64662ee5085edb18588a39d12e05fa26a720c8bf54d`; log SHA-256 `1defe0d5c635a6c060eb46b12aa1401aec2d81884e686e4c2e98ace516a9577d` | yes | EVD-P07-012, EVD-P07-013, EVD-P07-014 |
| EVD-P07-018 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Independent code and security rereview of the exact 20-file implementation snapshot passed scoped static review after the binding-candidate HIGH and current owner/ceiling wording MEDIUM corrections. The reviewers did not run tests or native sessions; source, tests and eleven permanent documents are hash-bound in the receipt | PASS | `_workspace/p07-provider-governance/implementation-review.json`, SHA-256 `8e2d357c1ab14316ff0bbca3dc4b0350b32239ee1d20a2408d9ae799e6f17f12` | yes | none |
| EVD-P07-019 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | The checked static source, skill inventory, current-input tests and reviewed current owners now distinguish provider binding values from neutral class ceilings; the negative coordinated-widening input in EVD-P07-006 is rejected by the repaired static consumer. Related policy removes invented elapsed/shared allocation gates, repairs the knowledge router and preserves actual cancellation/technical/resource and expiry boundaries. This does not establish native skill invocation, hook delivery, permission enforcement, authenticated model access or final common-edition approval; those dependent lanes remain with the native operator and common owner | PASS | EVD-P07-007, EVD-P07-009, EVD-P07-016 through EVD-P07-018 and the reviewed current governance/provider documents | yes | EVD-P07-006 |
| EVD-P07-020 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Final local index, message, review and integration | First source unit: actual `python scripts/qa.py staged` on 21 changed paths returned rc 0 with 17 gate PASS and unchanged index tree `929438a093d062c1871e0c1a42e47a03fd7cbd78`; pinned Commitizen message check and normal commit returned rc 0, producing `c64edee2f7d579bafe0fb125ae2ad962e6f5ebd8`. This proves that source unit's admission only, not local main integration or whole P07 acceptance | PASS | `_workspace/p07-provider-governance/source-index-qa.json`, SHA-256 `017948c1d250d2757a2cbbddec21ee3f114b9df220e15827152ab9d3d0bc1246`, log SHA-256 `216b5c7739307e4325f804444c9044466f6357402025db5c662994f8d1c545c9`; `source-commit.json`, SHA-256 `9f5f6c51e10bc4d94d5fb61747a4c93cf29916ebe9f8b4bb0731c19766fa6b22` | yes | none |
| EVD-P07-021 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Read-only `match_route` review at `c64edee2` on the five changed agent source/test paths found that the generic `scripts/` route selected nine gates, including K8S and Archive, while the generic `tests/` route selected four, including Archive. All 17 selected gates had returned rc 0 at EVD-P07-020; the FAIL here is the purpose-selection decision, not a claim that a validator failed. A narrow route and meaningful negative control are still pending | FAIL | `_workspace/p07-provider-governance/routing-scope-observation.json`, SHA-256 `da1a47676c751167ef77d7fe929d749bf36d77e289ff8f0264eb4805de8c17f6`; selection in EVD-P07-020 | yes | none |
| EVD-P07-022 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Against `c64edee2`, one named affected/staged selector test returned rc 1 with 12 failing subcases for six agent source/test paths: generic `scripts`/`tests` surface IDs were selected instead of `agent-implementation-contract`. The original stderr exceeded the tool output bound and was not saved; the receipt preserves the observed summary and bounded selections, not a reconstructed transcript | FAIL | `_workspace/p07-agent-validation-routing/routing-red.json`, SHA-256 `dc7706788ba1cb6ef19ecacd181d673e8156eee99b1c5e9da5068d0ad8e7b132` | yes | none |
| EVD-P07-023 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Corrected route in `scripts/validation/registry.json` and focused selector/test fixture inputs returned rc 0: three named affected-surface tests passed and the read-only registry contract checked 1304 tracked paths, 30/32 surfaces and 24 validators with no uncovered or ambiguous paths. New path-specific route selects the agent contract without unrelated Archive/K8S fallback; final changed-index admission remains pending | PASS | `_workspace/p07-agent-validation-routing/routing-final.json`, SHA-256 `b2c1237390211d71b1aceef69d0b2a7f95bc7eee2b24573bd77ee8ce39787817`; named-test log SHA-256 `4fb90f13b55dd4dd2e7825871088ab3d8e0243f9c3115d058439b5d8ebd926b4`; registry log SHA-256 `7d1ae07f468e3e1950a776b5d29e625e2c9fba9966e08b56b2f3a5e288c57905` | yes | EVD-P07-021, EVD-P07-022 |
| EVD-P07-024 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | The final registry module's 24 cases and current-input governance/consumer modules' 98 cases returned rc 0 in their two recorded commands; independent code/security review found the neutral ceiling and required binding candidates correctly separated from native tables/projections. After the validation registry changed, the affected agent-governance leaf returned rc 0 on an isolated exact-index snapshot with unchanged private input. These static checks resolve the planned ownership check, not native provider enforcement | PASS | EVD-P07-016 through EVD-P07-019; `_workspace/p07-provider-governance/routing-agent-index-prerequisite.json`, SHA-256 `3f8b715ac428e1c939df925a19c8ad601f8548436306938458e6c4ae646d5648`, log SHA-256 `24f9fe5ed9fe817d5245a1a0534632b0ef0005e2f7c9ba916e9a137dc2c6b1bc` | yes | EVD-P07-001 |
| EVD-P07-025 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Current skill/caller inventory and checked consumers retain the explicit skill-read and hook/trust boundaries. The initially broad agent source/test route was reproduced as twelve RED subcases; the corrected selector/fixture passed its three named tests and current affected-surface contract, and its four-path staged index passed eight selected gates with unchanged tree. No native skill invocation or hook delivery was claimed | PASS | EVD-P07-007, EVD-P07-021 through EVD-P07-023, EVD-P07-027 | yes | EVD-P07-002 |
| EVD-P07-026 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Context, memory, loop and workspace boundaries | Reviewed current model/context/safety policy, AD-0006 and provider routers identify neutral versus native owners; the knowledge router now names its actual Structure navigation. They remove invented elapsed/shared worker and reserve gates while preserving observed request/resource limits, `Retry-After`, cancellation, no-progress stops, technical process bounds and knowledge/approval validity. The reviewed source/index and current document checks support this local contract only | PASS | EVD-P07-018 through EVD-P07-020, EVD-P07-027; `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md` and current `.agents/governance/` owners | yes | EVD-P07-003 |
| EVD-P07-027 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Final local index, message, review and integration | Routing unit: selected `scripts/qa.py staged` on four changed paths returned rc 0 with eight gates PASS, unchanged index tree `3b277f3b6b9af02e1d9b65e1c3e83f0952b134a6`; actual Commitizen message check and normal commit returned rc 0 at `d8fedf3ee6a763aee955e0d2b734de7db9272769`. Clean local `main` advanced by `git merge --ff-only` from `34828945b1ce084b7287dfeebde757ff8500af7a` to that commit, including first unit `c64edee2f7d579bafe0fb125ae2ad962e6f5ebd8`. The first 17-gate unit and reviewed route/test correction are separately bound by EVD-P07-020 through EVD-P07-025. The root execution record contains no explicit push or remote merge command; any remote update and its initiator are assessed in EVD-P07-029 | PASS | `_workspace/p07-provider-governance/routing-index-qa.json`, SHA-256 `fe8c0d1638b1f81c19ec598723b0839b77e6ff388dcf6cb7de0bca9bbb1ae591`, log SHA-256 `3ca0382bf9d68bebb65a306f01a7add84f66a37230bc1c8fd462952779c56d23`; `routing-commit.json`, SHA-256 `00fc1c82c115b02b1c9f55e94b1df548b37198306575e0467f1660609a297606`; `source-local-integration.json`, SHA-256 `620355446c9634c7949c864f0e694918affbc6b868516c0f4d7225645c59cdc1` | yes | EVD-P07-005 |
| EVD-P07-028 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Provider-runtime and common-edition boundary | The static repository work and local integration in EVD-P07-024 through EVD-P07-027 are distinguishable from protected native/account and remote results. The installed CLI/help catalogue and retained native asset bytes are observations only; authenticated model/skill discovery, hook delivery, provider permission enforcement, a final approved WGOV edition and joint four-repository adoption remain unverified with their actual owners. Existing Task 0004 and external CI/release HIGH findings retain their separate obligations | PASS | EVD-P07-009, EVD-P07-011, EVD-P07-018, EVD-P07-024 through EVD-P07-027; `_workspace/p07-provider-governance/preserved-native-assets.json`, SHA-256 `c44e3a73482a6f5375b0cef150543bf696db801ed21e6b35d615424f362a13c8` | yes | EVD-P07-004 |
| EVD-P07-029 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Provider-runtime and common-edition boundary | Read-only `git ls-remote origin refs/heads/main` returned rc 0 and observed remote main at `d8fedf3ee6a763aee955e0d2b734de7db9272769`, matching local and cached origin/main. Cached reflog says `update by push`; who initiated the push is unverified. The root's recorded commands include no explicit push or remote merge. This narrows EVD-P07-027's phrase about remote action to root-invoked work and does not establish PR, hosted style, native runtime, publication or common approval | PASS | `_workspace/p07-provider-governance/remote-source-readback.json`, SHA-256 `69e7cb70fb8fd38a89b1fd2d51568148a94cc24ea97c328fe7cc0b78c0a80943` | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-P01-009](../spec.md#success-criteria--verification-plan) | accepted | EVD-P07-024, EVD-P07-025, EVD-P07-026, EVD-P07-027, EVD-P07-028 | Local P07 neutral/provider contract and affected selector accepted at the actual reviewed source revisions and clean main fast-forward. Native runtime/account/permission and final common edition or joint adoption are unverified separate decisions; Task 0004, SEC-P01-001 and SEC-P06-001 remain with their existing owners. The later closing Task document check/commit and owned worktree cleanup are recorded in a terminal delivery receipt after they occur, without inventing their OIDs here | platform for maintained local policy, native tables and consumers; native operator for protected runtime; buenhyden/common-standard owner for final edition; CI/security and repository/release operators for their existing HIGH findings |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package, assigned neutral governance/workflow,
  role/skill registry and provider-static consumers, their focused tests and
  existing navigation touched by the change, with one writer per file.
- **Forbidden Paths**: frozen Archive payloads, another writer's in-progress
  files, unrelated private/global configuration, credentials, secrets and live
  Kubernetes/Vault resources.
- **Approval Required**: scoped local inspection/repair, normal commits,
  main integration and owned cleanup are in the current request. Remote or
  paid execution, settings, trust, publication, dispatch, deployment and
  secret/live actions need their own actual authorization; this Task grants
  none of them.
- **Static Validation**: select focused negative and valid-control cases for
  changed behavior, profile/link checks for authored documents, and current
  exact-index/message gates from the actual validation registry. Preserve
  failure inputs and same-check resolutions.
- **Live Validation**: DEFER provider-native discovery, hook delivery,
  authenticated model resolution and remote/live results without their
  authorized environment and actual observed input.
- **Secret / Vault Handling**: read non-secret repository declarations and
  public metadata only; do not read, print, store or transmit credentials or
  private provider configuration.
- **Rollback Plan**: forward-correct the isolated branch and preserve previous
  Task evidence; protected external actions would need their own operator
  recovery decision.
- **Evidence Location**: this Task, reviewed Git commits and bounded ignored
  command receipts. The one-time
  `_workspace/p07-provider-governance/delivery.json` records the closing
  Task's own commit and cleanup after they occur; it is not a progress ledger.

## Verification Summary

Intake and ready-state documents each passed six selected exact-index gates,
actual message checks and normal commits. The neutral/native source migration
preserved its two-case negative input, actual test failures, their scoped
resolutions and independent reviews. Final current-input 24-case registry and
98-case governance/consumer commands each returned rc 0; no single final
122-case command was run. The first source unit passed 17 selected gates and
committed as `c64edee2f7d579bafe0fb125ae2ad962e6f5ebd8`. A later scope
review found unrelated Archive/K8S gate selection; a named RED test reproduced
it. The corrected route passed three focused tests, the affected-surface
contract and eight selected staged gates, and committed as
`d8fedf3ee6a763aee955e0d2b734de7db9272769`. Its updated agent-governance
prerequisite returned rc 0 on an isolated unchanged index. Local `main`
fast-forwarded to that commit, so VAL-P01-009's scoped local execution is
accepted. Native runtime/account behavior, final common approval and joint
adoption were not established. A read-only remote-ref check observed remote
`main` at the local integration commit, but push initiator and hosted PR/style
producer results remain unverified; no explicit remote write command is in
the root execution record. Those follow-up decisions retain their separate
owners; the earlier Task 0004 remains blocked
on its own obligations. The closing Task document's final check, commit and
owned cleanup are recorded in `_workspace/p07-provider-governance/delivery.json`
after they occur.
