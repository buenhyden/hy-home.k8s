---
title: 'Agent Roster Evaluation and Admission Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-26
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

The current-source observation cutoff for model and provider-capability
decisions is **2026-07-26 Asia/Seoul**. Later changes must be recorded as
separate currentness evidence and must not silently alter approved role
boundaries or accepted model decisions.

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

- **Claude**: compare the incumbent with account-available `opus`, `fable`,
  `sonnet`, and `haiku` aliases or exact IDs. High-risk work begins with a
  high-capability candidate; bounded low-risk work may begin with `sonnet` or
  `haiku`. `model` and `effort` enter an adapter only after official schema,
  allowlist, and runtime-resolution evidence.
- **Codex**: compare the incumbent with the installed runtime's documented
  demanding and balanced candidates, including `gpt-5.6` and
  `gpt-5.6-terra` where available. `model_reasoning_effort` is chosen per role
  and exact model/client support; no union of example values is treated as a
  universal enum.
- **Gemini CLI**: compare `gemini-3-pro-preview`,
  `gemini-3-flash-preview`, and supported Auto routing where available.
  Subagent model selection is independent of the parent `/model` choice.
  Agent-scoped generation settings require native parse and runtime evidence.
- **local/Antigravity**: retain its current model labels as an incumbent local
  projection until an approved local runtime evaluation replaces them. Local
  evidence is not reused as Gemini CLI discovery or model-resolution proof.

Use the following official sources for provider model releases and schemas.

- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Codex model catalog](https://developers.openai.com/api/docs/models)
- [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/)
- [Gemini CLI model selection](https://geminicli.com/docs/cli/model/)
- [Gemini CLI generation settings](https://geminicli.com/docs/cli/generation-settings/)

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
- Gemini CLI: `name`, `description`, `kind`, `tools`, `model`, `max_turns`, and
  `timeout_mins`; the native settings owner manages reasoning/model
  configuration.
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

The first three commands are planned Spec 044 deliverables and are not claimed
to exist in this draft. Their fixtures must cover exact 12/48 equality,
provider-native metadata/model mapping, new-role admission, external-catalog
rejection, eval baselines, adjudication, and rollback.

## Success Criteria & Verification Plan

- **VAL-AREA-001**: The canonical roster exactly matches the 12 roles above and
  has no extra or duplicate role and no ambiguous owner.
- **VAL-AREA-002**: Each of the four surfaces implements every one of the 12
  stems exactly once and passes 48-adapter set equality and provider-native
  field validation.
- **VAL-AREA-003**: `docs-researcher` and `quality-engineer` have non-overlapping
  input, output, authority, stop, and handoff contracts and least-privilege
  adapters.
- **VAL-AREA-004**: New-role admission fixtures reject unsupported upstream
  personas, overlapping owners, excess authority, and candidates without
  evaluation or rollback.
- **VAL-AREA-005**: All 12 roles have versioned positive, negative,
  refusal/stop, and handoff corpora together with incumbent baselines.
- **VAL-AREA-006**: High-risk roles and model promotions undergo independent
  adjudication, with quality and safety prioritized over cost and latency.
- **VAL-AREA-007**: Claude, Codex, Gemini CLI, and local/Antigravity adapters
  express role-specific model/reasoning profiles in provider-native forms and
  do not pretend unsupported fields exist.
- **VAL-AREA-008**: A model or role promotion passes both the Spec 042 canary
  and a same-version evaluation, and rolls back to the verified incumbent on
  failure.

## Traceability

- **PRD**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **ARD**: [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Predecessors**: [Spec 041](../041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../042-provider-native-runtime-and-model-evidence/spec.md), and
  [Spec 043](../043-agent-harness-loop-lifecycle/spec.md)
- **Agent design**: [Workspace Agent Roster and Projection Design](../041-stage-00-agent-governance-contract/agent-design.md)
- **Successor**: [Spec 045](../045-agent-governance-ci-qa-cutover/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-FUN-12](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AREA-001 | Canonical-role validation proves the exact 12-role set. |
| [REQ-PRD-FUN-12](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AREA-002 | Four-surface validation proves exact 48-adapter parity. |
| [REQ-PRD-FUN-12](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AREA-003 | Role-contract fixtures prove the two new roles are bounded and non-overlapping. |
| [REQ-PRD-FUN-15](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AREA-004 | Admission negative fixtures reject direct catalog import, overlap, excess authority, and missing evidence. |
| [REQ-PRD-MET-06](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AREA-001 | Canonical set validation reports zero missing, extra, or duplicate role. |
| [REQ-PRD-MET-06](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AREA-002 | Native-schema and semantic fixtures report zero adapter mismatch. |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AREA-005 | Versioned role corpora and incumbent baselines prove evaluation coverage. |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AREA-006 | Independent adjudication proves safety and quality precede cost optimization. |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AREA-007 | Provider-native field validation proves role-specific model/reasoning mapping. |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AREA-008 | Provider canary, same-version eval, and rollback prove promotion fitness. |
