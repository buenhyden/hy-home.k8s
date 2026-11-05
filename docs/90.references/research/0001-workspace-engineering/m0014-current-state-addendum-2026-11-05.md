---
title: "Reference: Current-State Addendum 2026-11-05"
version: "0.1.0"
type: "reference/research"
status: "draft"
owner: "platform"
updated: "2026-11-05"
layer: "references"
artifact_id: "RES-0001-m0014"
---

# Reference: Current-State Addendum 2026-11-05

## Overview

This addendum records, on 2026-11-05, where the local repository statements
in the published members m0001 to m0012 of this pack no longer describe the
repository. The members stay unchanged under the Stage 90 rule that a
published member is not rewritten for a later state; a reader combines each
member with the matching row below. It also records the passages inside
those members that contradict or repeat each other, so a reader knows which
statement is the latest.

## Reference Type

Repository-static observation of this repository at branch
`docs/requirements-conformance` on 2026-11-05, compared line by line with the
dated local claims of m0001 to m0012. No external source was re-read and no
runtime, hosted or cluster state was observed.

## Authority Boundary

This addendum establishes only what the tracked files said on 2026-11-05. It
is not a requirement, decision or policy. The current owners are the linked
Stage 01, 02 and 05 documents, `.agents/governance/`, the registries and the
implementing files. External-source claims in the members are not
re-evaluated here.

## Scope

### Research Questions

1. Which local claims of m0001 to m0012 does the current repository
   contradict, and what does it say instead?
2. Which statements inside one member contradict a later statement of the
   same member, and which one is the latest?
3. Which passages inside one member are material repetitions?

### Method

Read-only reviews compared every local path, count, setting, state and
owner named in m0001 to m0012 with the tracked tree, `git log` and the
registries by direct tracked-file reads, citing file and line. Findings marked uncertain by the reviews are
left out. Line numbers refer to the members as published at commit
`726e1956`.

## Definitions / Facts

### Claim-Source Matrix

The repository-wide current state that most corrections below rely on:

| Claim | Source | Verification state |
| --- | --- | --- |
| The agent registry admits 17 roles, 4 permission classes and 17 skills for two providers (Claude, Codex), with 17 role files under each of `.claude/agents/` and `.codex/agents/`; `.agents/agents/` and `.gemini/` do not exist | `python3 scripts/validate-agent-governance.py --root .` output; `.agents/roles/registry.json` | verified 2026-11-05 |
| Model, effort and tool bindings live in `.claude/bindings.json` and `.codex/bindings.json`; the registry holds only a capability tier per role; `.agents/governance/model-selection.md` owns selection | Those files | verified 2026-11-05 |
| Stage 00 (`docs/00.agent-governance/**`), Stage 04 (`docs/04.execution/**`), the harness catalog, `contracts/*.json`, `memory/README.md`, `memory/progress.md`, the bootstrap/JIT import chain and the agent-loop contract file are retired; shared governance lives in `.agents/governance/` and gateways import `.agents/workflows/work-lifecycle.md` | Repository tree; root `CLAUDE.md`; `.agents/governance/context-and-memory.md` | verified 2026-11-05 |
| `.claude/settings.json` and `.codex/hooks.json` each register one `PreToolUse` hook; `.codex/config.toml` is tracked; Claude auto memory and Codex native memories are disabled; no project MCP server is registered | Those files; `.claude/provider.md` | verified 2026-11-05 |
| Reusable context is kept in the shared workspace memory store (`scripts/workspace_memory.py`, Git-ignored `.workspace-memory/`) with short-term, long-term and domain tiers; it is never Task evidence | `.agents/governance/context-and-memory.md` | verified 2026-11-05 |
| Local QA owns purpose QA through `scripts/qa.py` (profiles `quick`, `staged`) and `scripts/validation/registry.json`; results are `PASS`, `NOT_RUN`, `NOT_APPLICABLE`, `FAIL`, `DEFER`; full, ci and all-files sweeps are retired | `scripts/qa.py`; `.agents/governance/quality.md`; ADR-0048 | verified 2026-11-05 |
| `.github/workflows/` holds `ci.yml` (jobs `ci-summary` for branch and commit metadata, and PR-only `style-pr`), `greetings.yml` and `labeler.yml`; the required checks are `ci-summary` and `style-pr`; `independent-review` was removed on 2026-11-03; Gitleaks runs only as a pre-commit hook | `.github/workflows/`; `.github/rulesets/main-protection.md`; `.pre-commit-config.yaml` | verified 2026-11-05 |
| Releases are prepared from `CHANGELOG.md` with `scripts/release.py`; tag `v0.1.0` exists; no Release Record is created | RUN-0012; `.agents/governance/sdlc.md`; `git tag` | verified 2026-11-05 |
| Document profiles live in `docs/99.templates/registry.json` (schema version 10): `sdlc/requirement`, `sdlc/architecture-description`, `sdlc/architecture-decision`, `sdlc/spec`, `sdlc/plan`, `sdlc/task`, `operation/*`, `reference/*`; there is no `sdlc/prd`, `sdlc/ard`, `sdlc/guide`, `document-profiles.json` or `standaloneExecutions` | `docs/99.templates/registry.json` | verified 2026-11-05 |
| A Spec package holds `spec.md`, `plan.md` and `tasks/` under `docs/03.specs/####-<slug>/`; only SPEC-0141 is open; completed packages and the Retention Catalog left the tree and Git history recovers them; `docs/98.archive/` is unvalidated | `docs/03.specs/`; ADR-0053 | verified 2026-11-05 |
| Traefik is the Argo-managed in-cluster ingress controller (chart 42.1.3, NodePorts 30080/30443); the k3d router binds `192.168.0.14:80/443` to those NodePorts; the k3d API binds `192.168.0.13:6550`; there is no `traefik/` copy in this repository | `gitops/apps/root/platform-traefik-app.yaml`; `infrastructure/k3d/k3d-cluster.yaml`; ADR-0043, ADR-0050 | verified 2026-11-05 |
| ESO reaches OpenBao over HTTPS (`https://openbao.hy.home.arpa`, CA `openbao-ca`) through the ClusterSecretStore still named `vault-backend`, requesting the `vault` and API-server audiences; `eso-read.hcl` grants read on four KV paths | The ClusterSecretStore manifest in `gitops/platform/eso/`; the ESO read policy in `infrastructure/vault/policies/`; ADR-0041, ADR-0054 | verified 2026-11-05 |
| Static infrastructure checks are `scripts/validate-infrastructure-contracts.sh`; live verifiers are six `infrastructure/verify/verify-*.sh` scripts plus `run-all.sh` | `infrastructure/README.md`; `infrastructure/verify/` | verified 2026-11-05 |
| Namespaces carry Pod Security labels (`platform` and `monitoring` restricted, other platform namespaces audit/warn restricted, `apps` baseline audit/warn, `istio-system` privileged); the adminer Rollout sets a pod and container `securityContext`; Alloy runs `v1.18.1`; thirteen declarations track `targetRevision: main` | `gitops/platform/namespaces/`; `gitops/workloads/adminer/rollout.yaml`; `gitops/platform/monitoring/alloy-k8s-logs.yaml`; `gitops/` | verified 2026-11-05 |

### Findings

#### Superseded local claims per member

| Member | Superseded local claims (published line numbers) | Current state |
| --- | --- | --- |
| m0001 | Counts `roles=12 permissionClasses=3 skills=16 handoffs=34 projections=36` (541-547, 558-559); 12 roles / 4 surfaces / 48 adapters, `.agents/agents/`, `.gemini/` (266-273, 332-336, 383-386); "no project `.codex/config.toml`" (184); bootstrap-to-postflight chain, harness catalog and progress ledger (114-134, 179); Spec 058, Spec 0054, Stage 04 Plan/Task (143, 147, 230, 451); Stage 00 as authority (97, 583); runtime discovery and model resolution "none observed" (558, 562-563) | Registry, gateway, hook and Spec rows of the matrix above; `.claude/provider.md` records discovery of every role projection and `sonnet` resolving on `claude 2.1.283` (2026-09-27) |
| m0002 | `memory/progress.md`, `rules/agentic.md`, `contracts/*`, `.codex/CODEX.md:102-105` (142-149, 302-306); "no project `.codex/config.toml`" (146); `agent-loop-lifecycle.json` state machine with two retries and three recovery actions (160-163, 205-226); eight QA phases and `SKIP` (230-233); durable progress ledger (149, 257); JIT bootstrap and Spec 058 (252, 282, 292-300); Stage 00 canonical rules (113) | The stop rule is in `.agents/workflows/work-lifecycle.md` (same check failing twice without new information, or two changes without progress); QA and retirement rows of the matrix above |
| m0003 | Twelve projections per provider (170, 182, 259); six hook events per provider and `.codex/CODEX.md:46-47` (255-259, 280-283); missing `.codex/config.toml` (180, 207, 343, 351); intended MCP baseline (183); progress ledger (185, 208); bootstrap import (151, 155, 203, 217); runtime model mapping DEFER (186); `providers/claude.md`, Spec 058 (245, 247, 291); Stage 00 policy owner (110) | Registry, hook, binding and gateway rows of the matrix above |
| m0004 | Profiles `sdlc/prd`, `sdlc/ard`, `sdlc/ad`, `sdlc/guide`, "sdlc/release gap" (162-173, 249-260, 621); states `draft/active/done/accepted/archived` (144, 162-173); five-key frontmatter (199); Stage 00 routing and the stage-authoring matrix (47, 214, 609); `docs/03.specs/[0-9]{3}-*` and `docs/04.execution/**` paths, Plan 9 and Task 6 headings, 53/71/69 tallies (286-289, 464-475); old body-contract columns, enforced statuses and validator line numbers (286-287, 481-508); release as unowned DEFER (172, 188, 298-306, 740-757); Guide Type, eight guides, DOC-G1, WORK-013 (168, 375-447, 673-689); `document-profiles.json`, Spec 052, Spec 0058, ADR-0022, `standaloneExecutions` (300, 419, 518, 577, 582, 843-855) | Profile and Spec package rows of the matrix above; each profile's states are its `lifecycle.status_domain`; stage routing is owned by `.agents/governance/sdlc.md`; release ownership is ADR-0048 and RUN-0012; the only guide is `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` |
| m0005 | `sdlc/guide`, DOC-G1 to DOC-G3, Spec 052 `active`, WORK-013 (109, 133, 179-192); `document-profiles.json:733` and the Spec 052 path (217-222); eight guides, `standaloneExecutions`, baseline `a5d2dfbb` (322-338); LLM-WIKI routing and `content/reference` (111, 135); PRD/ARD names (125); stage-routing and stage-authoring documents (251) | `operation/guide` with one guide; knowledge routing is `.agents/knowledge/` (ADR-0036); the chain is Requirement Package, Architecture Description, ADR, Spec, Plan and Task; routing lives in `.agents/governance/sdlc.md` and `document-authoring.md` |
| m0006 | Stage 00 knowledge-routing owners (317-318); "no new routing owner is created" (310-311) | `.agents/knowledge/README.md`, `project-map.md` and `domains.md` with `scripts/validate-knowledge-surface.py` (ADR-0036) |
| m0007 | `traefik/` reference-only gateway copy (229-232, 426, 467); `verify-contracts-static.sh` and five live verifiers (265, 556, 825, 998); `infrastructure/tests/verify-network-policies.sh` (247); k3d host ports `80:80`/`443:443` (558, 830); Vault Kubernetes auth with audience `vault`, six-path policy and HTTP local-only exception (221-227, 735-738, 868-869, 1033-1036); no Pod Security labels (282-285, 461); adminer without `securityContext` (341-348, 410, 422); ten or twelve `main` sources (369-371, 725); Alloy `v1.13.1` (717-718); `docs/00.agent-governance/memory/progress.md` (812) | Infrastructure rows of the matrix above; adminer still sets no `serviceAccountName`, `automountServiceAccountToken` or `readOnlyRootFilesystem` |
| m0008 | Five workflows including `generate-changelog.yml` and `stale.yml` (147, 177, 234, 249, 374, 481, 566, 721, 725); job layouts `changes`/`pre-commit`/`*-static` and `branch-policy`/`qa`/`ci-summary`, and `qa.py ci` (245-253, 370, 480-485); `ci-summary` aggregating `needs` (253, 380, 483); changelog workflow, artifact and git-cliff action (254, 316-317, 524, 731); `stale.yml` (257, 388-391, 525); four Python lock jobs (315, 485); Gitleaks in CI (283, 316); `validation-surfaces.json`, Stage 00, `quality-standards.md`, `infrastructure/tests/` (253, 277, 383-384, 608-613, 729, 734, 739); eight-step lane vocabulary and all-files completion evidence (270-279, 322); one required check and an empty ruleset list (477, 698); `.github/README.md` (160-161, 889); `hadolint` hook (605-608) | Workflow, QA and release rows of the matrix above; `ci.yml` pull-request types are `opened`, `synchronize`, `reopened` and `edited`; Dependabot covers GitHub Actions weekly with a 7-day cooldown; write permissions exist only in `greetings.yml` and `labeler.yml`; the repository surface is described in `.github/AGENTS.md` and `.github/repository-surface.md` |
| m0009 | Twelve roles and "no role reads the architecture boundary", `evals/` and `policy/` (104-113, 194, 524-531); SPEC-0075 and SPEC-0076 through the Retention Catalog (483, 533-535, 555); `harness-catalog.md`, `contracts/harness-contract.json`, `.agents/agents/` (188-218); Stage 00 roster-admission owners (374-378, 437-440, 551-556) | 17 roles including architect, governance-steward, ci-workflow-engineer, repo-tooling-engineer and agent-evaluator; evaluations live in `.agents/evaluations/`; Spec rows of the matrix above |
| m0010 | Tier-to-model binding declared in the registry (130-132); `model-policy.md`, `contracts/agent-model-fitness.json`, `.agents/agents/`, `.gemini/agents/` (220, 242-249, 279-284, 310-313, 367); Stage 00 model-policy owner | Binding and model-selection rows of the matrix above |
| m0011 | `contracts/agent-checkpoint.schema.json` and a closed checkpoint contract (111-117, 218-224, 274-277, 527); tiers with `progress.md` as durable owner (141-146); `memory/README.md`, `memory/progress.md`, `contracts/harness-contract.json` as existing (144, 306-311); provider memory described without the local disabled settings (43-45, 456-462); Stage 00 memory and checkpoint owners (439-443, 511-515) | Ignored checkpoints are optional recovery aids without a schema; memory rows of the matrix above |
| m0012 | `.agents/agents/`, `docs/00.agent-governance/**`, Spec 052, `docs/04.execution/**`, `document-profiles.json`, `templates/sdlc/architecture/*`, `.github/README.md`, `infrastructure/tests/`, `scripts/validate-repo-quality-gates.sh`, `.gemini/`, `docs/90.references/llm-wiki/` (575, 674, 689, 718-724, 746-794, 808, 1026-1036, 1153-1192); five workflows and 12 roles / 4 surfaces / 48 adapters (572, 689, 770, 806, 842); pinned line references such as `.codex/CODEX.md:102-105` and `infrastructure/README.md:106-110` (821-859); SPEC-0124 and SPEC-0125 (445-490) | Rows of the matrix above; templates live under `docs/99.templates/templates/`; pinned line numbers no longer match and must be re-read; SPEC-0124 and SPEC-0125 left the tree and Git history recovers them |

#### Contradictions inside a member

| Member | Earlier statement | Later or controlling statement |
| --- | --- | --- |
| m0003 | Four sub-areas "not admitted" (480-498) | Direct support recorded (553); the later line controls |
| m0004 | `document-profiles.json` (300, 419) and `sdlc/ad` as current (621) | `registry.json` (281-282); the matrix at 163-164 names ARD; the registry row above controls |
| m0005 | Anchor `#ditaxis-baseline` (385); `document-profiles.json` (217, 251) | `#diátaxis-baseline` (434) is the working anchor; `registry.json` (327, 456) controls |
| m0007 | No Pod Security labels (283-285) and adminer without `securityContext` (345-346); Argo CD chart unpinned (722-727) | Labels present (959-960, 1032-1033); hardening present (1028-1032); chart pinned to 10.4.0 (385-390, 993-994) |
| m0008 | Three-job note (245-249) versus five-job layout (253, 729); REQ-WERPC-024 `Verified` (722) versus "no row is promoted to `Verified`" (494, 499) | Different dated cycles; neither describes the current repository, the workflow row above does |
| m0009 | Branch head "byte-identical" to the `ebe9c99` pin (209-211, 255); "no candidate is adopted" (148-150, 489) | Withdrawn at 73 and 457-459; "adapt, not adopt; five roles are proposed" (532), since admitted |
| m0010 | Codex precedence conflict "resolved" (CLM-134, 49) | "No single authoritative Codex precedence chain" (175-200); the 2026-09-05 entry controls the Claude subagent order |
| m0011 | Ledger "remains" and "confirmed" (306-311, 378-397) | Ledger retired (122-129, 223) |
| m0012 | "Only WERPC-008 may delete predecessor files" and "records repository-static paths" (1317-1323) | Current provenance is external-only and no repository observation is made (34, 1329-1333); the earlier text is not a current rule |

#### Material repetition inside a member

| Member | Repeated passages (lines) |
| --- | --- |
| m0001 | REQ-006 As-Is, Gap and Disposition (236-282 and 298-354); 383-396 and 430-448 |
| m0002 | Static-verified and provider-DEFER disposition (290-315 and 346-397) |
| m0003 | Twelve-adapter and six-hook observations (243-287 and 304-364) |
| m0004 | REQ-014 Guide disposition (375-404, 414-447, 673-689); REQ-011 (262-277, 613-633); REQ-018 (298-306, 740-757); family matrices (77-90, 160-173); ISO and SSDF caveats (67-71, 142-150) |
| m0005 | DOC-G1 to DOC-G3 and WORK-013 (171-192, 294-313, 355-378, 394-414); HTTP 429 history (162, 267-277) |
| m0007 | Final request dispositions (752-755, 880-886, 1104-1186); delta table and prose (311-405, 407-411) |
| m0008 | Workflow inventory (207-214, 531-532); permissions and SHA pins (234-241, 374-378, 566-573, 721, 733); concurrency (260-264, 525-529, 730); NASA source date (148, 185-188, 428-429); "not observed in this cycle" (24, 34, 99) |
| m0009 | As-Is and gap blocks (279-298, 326-343); baseline (104-113, 356-378) |
| m0010 | Three Codex and Claude disagreements (175-200, 212-218, 251-260); As-Is and Final disposition (279-295, 310-346) |
| m0011 | Provider and MCP table (263-268, 317-323); Gap and Final disposition (279-293, 330-347); MCP supersession note (176-189, 246-250) |
| m0012 | The same URL under different source IDs: config reference (SRC-WERPC-049, 010), subagents (011, 045), memory (004, 051), sub-agents (007, 046), models (136, 010), ISO 72089 (110, 053), ISO 74393 (111, 054), SRE incident guide (018, 057), NIST SP 800-218 (015, 033), artifact attestations (107, 065), pip secure installs (151, 043), Kubernetes policy (026, 034), Gatekeeper (028, 034) |

Imperative passages in m0001 (193-206, 219-224), m0002 (207, 259-278),
m0003 (66-72, 203-231), m0004 (191-228), m0005 (141-152), m0008 (270-272,
291), m0009 (144-165), m0010 (111-165) and m0011 (148-166) read like rules.
They are research recommendations of their dated cycles, not policy; the
current rules are in `.agents/governance/`.

## Sources

| Source | Grade | Retrieved | Relevance |
| --- | --- | --- | --- |
| [Agent registry](../../../../.agents/roles/registry.json) and `scripts/validate-agent-governance.py` | Repository primary | 2026-11-05 | Roles, providers, projections |
| [Common governance hub](../../../../.agents/README.md) | Repository primary | 2026-11-05 | Current owners of QA, lifecycle, memory and model selection |
| [Document registry](../../../99.templates/registry.json) | Repository primary | 2026-11-05 | Profiles and states |
| [`.github/rulesets/main-protection.md`](../../../../.github/rulesets/main-protection.md) and `.github/workflows/` | Repository primary | 2026-11-05 | Hosted checks and workflows |
| [`infrastructure/README.md`](../../../../infrastructure/README.md) and `gitops/` | Repository primary | 2026-11-05 | Platform and verifier facts |
| [ADR-0054](../../../02.architecture/decisions/0054-platform-decision-current-state-amendment.md) and [ADR-0055](../../../02.architecture/decisions/0055-governance-decision-current-state-amendment.md) | Repository decision | 2026-11-05 | Current clause amendments |

## Review and Freshness

Refresh this addendum, or add a later dated one, when a named owner, count or
path changes again, or when a member of this pack is revised or succeeded.

### Limitations

Repository-static only; no runtime, hosted or cluster observation. Line
numbers are fixed to the published members at `726e1956`. Findings the
reviews marked uncertain are omitted.

### Recommendations

A later research cycle can succeed the most out-of-date members (m0004,
m0008, m0012) with fresh members instead of relying on this addendum; the
choice belongs to the pack owner.

## Related Documents

- [Pack router](README.md)
- [Source ledger](m0012-source-coverage.md)
- [Stage 90 rules](../../AGENTS.md)
