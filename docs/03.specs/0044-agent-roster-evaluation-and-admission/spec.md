---
title: 'Agent Roster Evaluation and Admission Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-30
artifact_id: "SPEC-0044"
---

# Agent Roster Evaluation and Admission Technical Specification (Spec)

## Overview

This Spec establishes a canonical workspace AI Agent roster of 12 roles and
defines a 48-adapter contract that projects every role onto four adapter
surfaces: local/Antigravity, Claude, Codex, and Gemini CLI. It retains the ten
existing roles and adds only `docs-researcher` and `quality-engineer` to close
the recurring official-documentation research and QA/evaluation evidence gaps
identified by the Current audit.

Adding roles is not an end in itself. A single admission gate combines each
role's inputs, outputs, allowed tools, prohibited actions, stop conditions,
handoffs, evaluation corpus, and provider-specific model/reasoning profile so
that static file presence is not mistaken for actual role fitness. The
external [`agency-agents`](https://github.com/msitarzewski/agency-agents)
repository is only an idea catalog for comparing responsibility and evaluation
patterns; it is not roster or instruction authority.

The provider/model evidence cutoff for model and provider-capability decisions
is **2026-07-10 10:00 Asia/Seoul** (`2026-07-10 01:00 UTC`), as owned by
[`provider-runtime-evidence.json`](../../00.agent-governance/contracts/provider-runtime-evidence.json).
The Spec 042 source ledger was reconciled on 2026-07-28 and distinguishes
dated cutoff evidence from current-only observation evidence. Later changes
must be recorded as separate currentness evidence and must not silently alter
approved role boundaries or accepted model decisions.

This Spec is closed at the repository-static readiness and gate-enforcement
boundary. The current tracked inventory is exactly 12 roles across four
provider surfaces and 48 role/provider tuples. AREA-003 repository-static
evaluation readiness is complete, AREA-004 mapping readiness is `PASS` for 21
tuples and `DEFER` for 27, and every configured incumbent is retained.
Observed evaluation, result adjudication, final admission, model fitness,
threshold satisfaction, promotion, canary, provider runtime/authentication,
model resolution, hosted CI, remote, and live evidence remain `DEFER` as
applicable; this closure records none of those outcomes as observed.

## Strategic Boundaries & Non-goals

- **In scope**: the exact 12-role set; 48-adapter set equality across four
  surfaces; non-overlapping contracts for `docs-researcher` and
  `quality-engineer`; new-role admission; versioned offline evaluation corpora;
  independent adjudication; provider-specific model/effort optimization; and
  promotion and rollback evidence.
- **Protected boundaries**: roles use only delegated paths and tools. Evaluation
  fixtures and adapters must not contain secret values, private transcripts,
  authentication material, shell history, or live-mutation authority.
- **Non-goals**: directly copying upstream personas; treating role-count growth
  as maturity; forcing provider adapters into a shared syntax; claiming static
  parity as runtime discovery; manipulating live incidents or Kubernetes;
  automatically promoting model aliases without evidence.
- **Dependency boundary**: this Spec consumes the machine-readable harness
  contract from Spec 041 and provider schema/runtime canaries from Spec 042; it
  does not duplicate ownership of either.

## Contracts

The canonical role set contains exactly the following 12 roles. No other active
roster is permitted.

1. `supervisor`
2. `code-reviewer`
3. `doc-writer`
4. `gitops-reviewer`
5. `incident-responder`
6. `k8s-implementer`
7. `network-reviewer`
8. `observability-reviewer`
9. `security-auditor`
10. `wiki-curator`
11. `docs-researcher`
12. `quality-engineer`

Each stem must exist exactly once in `.agents/agents`, `.claude/agents`,
`.codex/agents`, and `.gemini/agents`. Parity is FAIL if 12 x 4 set equality
does not hold, provider-required metadata is missing, or shared role semantics
are absent. `.agents` is the local/Antigravity surface, whereas `.gemini` is the
native Gemini CLI surface; neither substitutes for the other.

Tracked repository inventory and roster admission are independent lifecycle
axes. AREA-001 owns the `contract-only` / `DEFER` gate. AREA-002 may transition
the exact tracked set to `repository-static-projected` and authorize only the
12-role / 4-surface / 48-adapter projection while the admission verdict remains
`DEFER`. Its candidate decisions are projections, not operational or final
admissions. AREA-003 owns the versioned four-class evaluation, incumbent
baseline, independent adjudication, and rollback evidence required before a
separate evaluation-backed final admission transition can return `PASS`.
Provider discovery, authentication, model resolution, hosted CI, remote, live,
and runtime activation remain separate evidence classes even after final
roster admission.

`docs-researcher` is a read-only role that verifies official primary sources
and the cutoff, then produces a source ledger, conflict notes, and confidence
limits. It does not write document bodies, decide policy, change code, or
install or authenticate providers. `quality-engineer` designs
test/fixture/CI/QA evidence and classifies execution results. It does not own
product code, security sign-off, live mutation, or workflow approval. Neither
role absorbs the responsibilities of the existing `doc-writer`,
`code-reviewer`, `security-auditor`, or `supervisor` roles.

A new role is admitted to the roster only if every condition below passes.

- A recurring or approved requirement demonstrates an unowned deliverable.
- An overlap analysis demonstrates that strengthening an existing role cannot
  resolve the gap.
- Inputs, outputs, permissions, prohibited actions, stop conditions, handoffs,
  and owner are explicit.
- Provider-native metadata and a least-privilege tool set are designed for all
  four adapters.
- Positive, negative/adversarial, refusal/stop, and handoff evaluations pass
  alongside a baseline.
- An independent adjudicator approves the quality, safety, cost, and latency
  thresholds.
- Rollback to the previous roster/model after a failed promotion is
  reproducible.

External catalog entries, including those in `agency-agents`, are recorded only
as potential evidence for these conditions. File count, persona popularity, or
the existence of an upstream prompt is not admission evidence.

## Core Design

### Role contract and evaluation flow

1. Read the role stems, shared semantics, adapter surfaces, and contract version
   from the Spec 041 `harness-contract.json`.
2. Each role-specific corpus covers representative successful work,
   boundary/error cases, prohibited actions, and correct handoffs, and records
   provenance and privacy class.
3. Establish a baseline with the incumbent model/profile, then run the
   candidate against the same corpus and grader.
4. Separate deterministic grading from independent human/reviewer
   adjudication. High-risk security, incident, GitOps, and Kubernetes decisions
   must not be promoted from a single model's self-grade.
5. Optimize cost and latency only for candidates that first meet quality and
   safety thresholds. A single critical miss, secret disclosure, scope escape,
   or unsafe live action blocks promotion.
6. Apply only approved results to the canonical model map and all four
   adapters, then rerun parity and evaluation regressions.

### Role-specific model and reasoning profiles

The profiles below are defaults based on each role's risk, context length, tool
authority, cost, and latency. A specific model ID must be confirmed as actually
available by cutoff sources and an authenticated Spec 042 canary.

| Role | Default capability / reasoning | Optimization basis and escalation |
| --- | --- | --- |
| `supervisor` | top / xhigh | Long-context decomposition, approval boundaries, multi-result synthesis, and termination decisions. Synthesis defects or high-risk ambiguity escalate to independent top-tier review. |
| `code-reviewer` | worker / high | Prioritize seeded-defect, severity, and file-evidence accuracy. Cost reductions are allowed only after the false-negative threshold is met. |
| `doc-writer` | worker / medium | Optimize template/link correctness, multilingual clarity, and the unsupported-claim rate. Source conflicts escalate to a high profile. |
| `gitops-reviewer` | worker / high | Must not miss desired-state ownership or sync/release risk. High-risk findings require independent domain review. |
| `incident-responder` | top / high | Handles incomplete long-context evidence and causal uncertainty. Recovery execution always transfers to human/operator approval. |
| `k8s-implementer` | worker / high | Bounded writes, schema/security correctness, and minimal diffs are critical. Secret exposure or a scope miss blocks promotion. |
| `network-reviewer` | worker / high | Prioritizes missed high-risk findings in routing, isolation, DNS, and TLS. Live probes are prohibited. |
| `observability-reviewer` | worker / high | Evaluates scrape/alert/SLO interpretation accuracy together with unsupported live claims. |
| `security-auditor` | top / high | Prioritizes minimizing critical misses, refusal behavior, and redaction over cost, and requires independent/human sign-off. |
| `wiki-curator` | worker / medium | Repeatedly verifies canonical owner/link accuracy, generator idempotence, and artifact refusal at low cost. |
| `docs-researcher` | worker / high | Evaluates official-source currentness, conflict resolution, cutoff compliance, and citation accuracy without write authority. |
| `quality-engineer` | worker / high | Evaluates fixture coverage, negative-test sensitivity, result classification, and reproducibility without owning product/security sign-off. |

Provider mapping follows these rules.

- **Claude**: compare incumbent repository labels (`opus 4.8`,
  `sonnet 4.6`) with the fixed-cutoff Fable 5, Opus 4.8, Sonnet 5, and
  Haiku 4.5 families. High-risk work begins with a high-capability candidate;
  bounded low-risk work may begin with a worker candidate. An exact `model`
  alias/ID and `effort` become an accepted provider mapping only after dated
  primary-source, allowlist, native parse, runtime-resolution, and same-suite
  fitness evidence.
- **Codex**: compare incumbent repository mappings (`gpt-5.5`,
  `gpt-5.3-codex`) with fixed-cutoff candidates including `gpt-5.6-sol`,
  `gpt-5.6-terra`, `gpt-5.6-luna`, and a bounded `gpt-5.4-mini` route where
  the cited product surface supports them. `model_reasoning_effort` is chosen
  per role and exact model/client support; no union of example values is
  treated as a universal enum, and publication does not prove local
  entitlement or resolution.
- **Gemini CLI**: keep the local/Antigravity `Gemini 3.1 Pro` and
  `Gemini 3.5 Flash` labels as incumbent local evidence. Evaluate the
  fixed-cutoff API families `gemini-3.1-pro-preview`, `gemini-3.5-flash`, and
  `gemini-3.1-flash-lite` separately from Gemini CLI's unresolved pro, flash,
  and Auto routes. API lifecycle never proves CLI/account availability;
  `.gemini/**` native schema parsing and runtime resolution must identify any
  accepted CLI ID and generation setting.
- **local/Antigravity**: retain its current model labels as an incumbent local
  projection until an approved local runtime evaluation replaces them. Local
  evidence is not reused as Gemini CLI discovery or model-resolution proof.

Use the following official sources for provider model releases and schemas.

- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Claude model overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [GPT-5.6 release](https://openai.com/index/gpt-5-6/)
- [Codex release `rust-v0.144.1`](https://github.com/openai/codex/releases/tag/rust-v0.144.1)
- [Codex release `rust-v0.145.0-alpha.2`](https://github.com/openai/codex/releases/tag/rust-v0.145.0-alpha.2)
- [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/)
- [Gemini CLI release `v0.50.0`](https://github.com/google-gemini/gemini-cli/releases/tag/v0.50.0)
- [Gemini CLI release `v0.51.0-preview.0`](https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0)
- [Gemini CLI memory](https://geminicli.com/docs/tools/memory/)
- [Gemini API model catalog](https://ai.google.dev/gemini-api/docs/models)

## Data Modeling & Storage Strategy

The canonical roster, role-contract version, provider mapping, and evaluation
suite reference live in the Spec 041 machine harness contract. Do not create a
separate Markdown roster or provider-specific copies of shared policy.

The role evaluation manifest contains at least these fields.

- `suiteVersion`, `roleId`, `roleContractVersion`, `fixtureId`, `fixtureVersion`;
- provenance, privacy class, risk class, input digest, expected behavior;
- allowed paths/tools, prohibited action, stop/handoff expectation;
- provider, model ID, reasoning profile/effort, config source, canary reference;
- grader/rubric version, quality/safety/cost/latency metrics;
- incumbent/candidate comparison, adjudicator, decision, rollback reference.

Corpora are managed as synthetic or redacted fixtures that contain no secrets,
authentication material, private transcripts, or production data. Large raw
run logs are not canonical documents; only the summaries and digests required
for approval are retained as Stage 04 Task evidence. Compare incumbent
baselines and promotion results under the same suite version, and establish a
new baseline whenever the corpus or grader changes.

## Interfaces & Data Structures

Provider adapters preserve shared semantics while using native metadata as-is.
The list below is an observation-time candidate schema and must not be claimed
as a cutoff-proven contract until supported by dated cutoff evidence or a
native-schema canary.

- Claude: `name`, `description`, `model`, `tools`; include `effort` and
  `maxTurns` only when verified.
- Codex: `name`, `description`, `developer_instructions`, `model`,
  `model_reasoning_effort`.
- Gemini CLI: `name`, `description`, `kind: local`, `max_turns`, and
  `timeout_mins`. Generic tool aliases and exact CLI model resolution are not
  repository-static evidence; they remain provider-runtime `DEFER` until a
  native parser/canary proves the exact field and accepted value.
- local/Antigravity: `name`, `description`, `model`, and the repository-local
  body contract.

Parity-validator inputs are the canonical role set and the inventories of all
four surfaces. Output distinguishes missing, extra, duplicate, metadata
mismatch, and semantic mismatch by role and surface. The existence of 48 files
alone does not produce PASS.

Evaluation-runner inputs are an immutable fixture and the candidate tuple
`(provider, model, reasoning profile, adapter version)`. Output includes
redacted metrics, result class, grader version, adjudication, and rollback, and
stores neither full private prompts nor provider credentials.

## Edge Cases & Error Handling

- If a provider does not support a model ID or reasoning field, do not apply an
  arbitrary fallback; record the candidate as FAIL or DEFER.
- Provider-specific metadata differences are not parity mismatches. Only
  missing shared role semantics or required native fields are mismatches.
- Even when a role can assist several domains, reject new-role admission if its
  canonical deliverable owner overlaps another role. Strengthen the existing
  role's handoff or vocabulary instead.
- If an evaluation corpus would require an actual secret or private transcript,
  substitute a synthetic fixture. If the substitute cannot prove the decision,
  retain a human-only gate.
- Do not promote a candidate that misses safety or quality thresholds, even if
  it costs less.
- A preview, deprecated, or unavailable model cannot become the canonical
  default without an authenticated canary and rollback.

## Failure Modes & Fallback / Human Escalation

- If 12/48 set equality or semantic parity breaks, restore the last verified
  roster and isolate the failing role/surface.
- A critical miss, secret disclosure, out-of-scope write, unsafe action, or
  invalid bypass of human approval stops candidate promotion and escalates to
  the security/platform owner.
- Keep the incumbent when the independent adjudicator cannot establish the
  candidate's superiority over the baseline.
- If provider entitlement or native resolution is unverified, record only the
  repository-static mapping; do not promote it to runtime-ready.
- If admission evidence does not establish recurring work or a distinct
  deliverable, do not create a new agent. Record the existing owner and the
  follow-up evaluation path instead.

## Verification Commands

```bash
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-agent-evaluations.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

The first three commands are Spec 044 deliverables. Their repository-static
PASS results do not establish evaluation-backed final admission or any
provider-runtime evidence. Their fixtures must cover exact 12/48 equality,
provider-native metadata/model mapping, new-role admission, external-catalog
rejection, eval baselines, adjudication, and rollback.

## Success Criteria & Verification Plan

- **VAL-AREA-001**: The canonical roster exactly matches the 12 roles above and
  has no extra or duplicate role and no ambiguous owner.
- **VAL-AREA-002**: Each of the four surfaces implements every one of the 12
  stems exactly once and passes 48-adapter set equality and provider-native
  field validation as a `repository-static-projected` / `DEFER` transition.
- **VAL-AREA-003**: `docs-researcher` and `quality-engineer` have non-overlapping
  input, output, authority, stop, and handoff contracts and least-privilege
  adapters.
- **VAL-AREA-004**: New-role admission fixtures reject unsupported upstream
  personas, overlapping owners, excess authority, and candidates without
  evaluation or rollback.
- **VAL-AREA-005**: All 12 roles have versioned positive, negative,
  refusal/stop, and handoff corpora together with incumbent baselines.
- **VAL-AREA-006**: The repository-static gate requires independent
  adjudication for high-risk roles and any model promotion, with quality and
  safety prioritized over cost and latency; observed result adjudication and
  promotion remain `DEFER`.
- **VAL-AREA-007**: Claude, Codex, Gemini CLI, and local/Antigravity adapters
  express role-specific model/reasoning profiles in provider-native forms and
  do not pretend unsupported fields exist.
- **VAL-AREA-008**: The promotion gate requires both a Spec 042 canary and a
  same-version evaluation before a model or role promotion, and requires
  rollback to the verified incumbent on failure; no promotion or rollback
  execution is observed by this Spec.

AREA-002 satisfies only the repository projection criterion. Final roster
admission remains `DEFER`. AREA-003 supplies repository-static four-class
corpus, adjudication-readiness, rollback-source, and explicit final-decision
records, but it does not supply observed same-suite evaluation, result
adjudication, or final admission. No subset of VAL-AREA-001 through
VAL-AREA-006 weakens that gate.

Observed implementation commit
`258955b3e0d999ec4ebc3de561d0db39ce11ac3c`, AREA-004 postflight commit
`a15d5e10a4848aca013848571ba6d56c3568b5c3`, and AREA-005 semantic
reconciliation commit `7891368e3d29e5e9e5e8ada4023118d331e38000`
complete the repository-static Spec 044 work. AREA-005 requirements were
`COMPLIANT`; quality and security were `APPROVED`; focused model checks,
staged lifecycle, strict registry over 463 tracked paths, the full repository
aggregate, all-files pre-commit, and diff checks passed. This reciprocal
closure proposal does not preclaim its own future commit SHA or postflight
evidence update. The next workstream is Spec 045.

## Traceability

- **PRD**: [PRD 003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **AD**: [AD 0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Predecessors**: [Spec 041](../0041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../0042-provider-native-runtime-and-model-evidence/spec.md), and
  [Spec 043](../0043-agent-harness-loop-lifecycle/spec.md)
- **Agent design**: [Workspace Agent Governance Program Design](../0041-stage-00-agent-governance-contract/spec.md)
- **Successor**: [Spec 045](../0045-agent-governance-ci-qa-cutover/spec.md)
- **Execution Plan**: [Agent Roster Evaluation and Admission Implementation Plan](plan.md)
- **Task evidence**: [Agent Roster Evaluation and Admission Task](README.md#task-records)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AREA-001 | Canonical-role validation proves the exact 12-role set. |
| N/A — VAL-AREA-002 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-002 | Four-surface validation proves exact 48-adapter parity. |
| N/A — VAL-AREA-003 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-003 | Role-contract fixtures prove the two new roles are bounded and non-overlapping. |
| N/A — VAL-AREA-004 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-004 | Admission negative fixtures reject direct catalog import, overlap, excess authority, and missing evidence. |
| N/A — repeated VAL-AREA-001 metric shares the PRD-0003 source linked above | VAL-AREA-001 | Canonical set validation reports zero missing, extra, or duplicate role. |
| N/A — repeated VAL-AREA-002 metric shares the PRD-0003 source linked above | VAL-AREA-002 | Native-schema and semantic fixtures report zero adapter mismatch. |
| N/A — VAL-AREA-005 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-005 | Versioned role corpora and incumbent baselines prove evaluation coverage. |
| N/A — VAL-AREA-006 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-006 | Independent adjudication proves safety and quality precede cost optimization. |
| N/A — VAL-AREA-007 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-007 | Provider-native field validation proves role-specific model/reasoning mapping. |
| N/A — VAL-AREA-008 shares the PRD-0003 source linked in VAL-AREA-001 | VAL-AREA-008 | Provider canary, same-version eval, and rollback prove promotion fitness. |
