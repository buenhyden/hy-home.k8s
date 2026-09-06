---
title: "Provider Write-Guard Ownership and Enforcement Honesty Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0074"
---

# Provider Write-Guard Ownership and Enforcement Honesty Technical Specification (Spec)

## Overview

SPEC-0073 declared one execution scope per role on both providers, bound each
capability tier to one native model, and extended the pre-action guard beyond
the structured file tools. Direct observation of the resulting tree found four
conditions that declaration alone does not settle.

The shared guard is registered by both providers but owned by one of them: the
Codex registration invokes a script inside the Claude adapter directory, so a
provider-neutral control lives under a provider-specific owner.

The guard does not see Codex patch writes. A Codex `apply_patch` payload
arrives with its patch text in the same field a shell command uses, and the
guard parses that field only as a shell command line. A manifest write that
produces a Kubernetes and secret-handling warning through the Claude path was
observed to return with no message and no error through the Codex path, for
both the string and the argument-vector form of the payload. The guard's own
design keeps shell-derived guesses out of the structured path pipeline, so on
that provider the manifest, secret-adjacency and document-route checks do not
run at all.

Guard delivery on Codex is unproven rather than merely unobserved. The
installed client's project path table names `.codex/hooks` while the
repository registers `.codex/hooks.json`. That evidence is indicative, not
conclusive, and no local command in the installed client lists loaded hooks,
so the question is answerable only from a fresh session.

The `read-only-evidence` permission class means different real authorities on
the two providers. On Codex it maps to an operating-system `read-only`
sandbox. On Claude it grants `Read`, `Grep`, `Glob` and `Bash`, and a shell
can write; the guard's shell detection is advisory by design and never blocks.
Two role documents in that class additionally offer to edit when a human asks,
an action the class has no structured write tool to perform.

The evaluation harness holds three cases, all synthetic and all written to
pass. Its groundedness criterion checks only that a cited path exists on disk,
and its boundary criterion is a regular expression. Every negative fixture
lives inside a unit test rather than as an evaluation artifact, so the harness
demonstrates wiring and not failure detection.

This specification gives the shared guard one owner outside either provider
directory, makes patch envelopes parse as data, states what each provider
actually enforces, and makes the evaluation harness reproduce the failures it
claims to detect. It introduces no new common surface; SPEC-0075 owns that.

## Strategic Boundaries & Non-goals

Authorized scope covers `scripts/`, `.claude/hooks/`, `.claude/settings.json`,
`.codex/hooks/`, `.codex/hooks.json`, the provider notes and adapter READMEs,
`.agents/roles/` role bodies and the role registry, `.agents/governance/`
policy text bearing on enforcement claims, `tests/` and `evals/`. Every change
is a reviewable local commit.

Protected surfaces stay unchanged. `gitops/`, `infrastructure/`, `traefik/`,
`policy/` and `examples/` are read as evidence of the platform this guard
protects; no behavioural change is made in them. No live Kubernetes, ArgoCD or
Vault operation occurs. No push, pull request, merge, release or remote
workflow dispatch occurs. No credential, token, kubeconfig, plaintext secret,
shell history or environment dump is read, printed or stored. Configuration
under the user's home directory is not modified.

Explicit non-goals. No knowledge, prompt, evaluation, rule or script directory
is created under `.agents/`; SPEC-0075 owns surface adoption. No shell parser
is built that claims to detect every write; the shell path stays advisory and
says so. No hook response field is used on a provider that does not document
it, and no unsupported field is relied on as a fail-closed control. No hook is
registered on a stop, compaction or session event, because such an event would
re-enter this repository's own validation. No permission class is added or
removed, and no class gains mutation authority it does not have today.

## Contracts

**Guard ownership.** The shared write-boundary logic has one owner under
`scripts/`. Each provider directory holds only its own thin adapter and its own
native registration. No provider directory executes a program owned by the
other.

**Payload normalization.** Each provider payload is normalized explicitly
before the shared checks run. A structured file tool, a patch envelope and a
shell command are distinct input shapes with distinct parsers. A patch
envelope is read as data and never executed.

**Equal treatment of equal writes.** A write to a given repository path
receives the same manifest, secret-adjacency and document-route evaluation
regardless of which provider and which structured mechanism produced it.

**Advisory stays advisory.** Shell-derived write targets remain outside the
structured path pipeline and outside any hard block, and the documents state
that limitation rather than implying complete shell coverage.

**Honest enforcement claims.** A registered configuration file is not evidence
that a client discovered, loaded or delivered it. Where delivery is unproven,
the documents say so and name the boundary that actually holds instead. Static
parity is never reported as runtime enforcement.

**Permission truth.** A permission class name describes what the registry
grants, not what an operating system enforces. Where the two providers differ
in real authority under one class name, the difference is documented, not
described as parity. A role guardrail never offers an action the role's tool
scope cannot perform.

**Evaluation honesty.** A synthetic passing case is wiring evidence only. Each
enumerated failure mode has an evaluation artifact that reproduces it. Added
pattern coverage is reported as coverage of enumerated modes, never as
semantic understanding.

## Core Design

### Guard ownership and provider adapters

The guard logic moves from the inline program inside the Claude adapter into a
module under `scripts/`, invoked with an explicit provider argument. The Claude
adapter keeps its current path and becomes a thin wrapper that forwards
standard input and names its provider. A matching thin adapter appears under
`.codex/hooks/`, and the Codex registration points at that adapter instead of
the Claude one. The existing governance validator already requires each
provider's registered command to reference an existing file under that
provider's own hook directory, so the new arrangement is checkable by the
validator the repository already runs.

The program the adapters execute always resolves from the project directory.
A root derived from tool input continues to select data only, never an
executable, so the guard cannot be made to run code from the tree it guards.

### Payload normalization and patch parsing

Normalization routes by input shape rather than by provider name, so a shape
supported by both providers is handled once.

A structured file tool contributes its scalar path field, its path collection
or its edit list to the structured path pipeline, as it does today. A patch
envelope contributes its add, update, delete and move targets to the same
pipeline, so those paths receive the checks a structured write already
receives; both the string form and the argument-vector form of the payload are
accepted. A shell command keeps its current treatment: recognized redirection,
tee and in-place edit targets produce an advisory note and stay out of the
structured pipeline, because an unparsed guess reaching the affected-surface
selector would turn a guess into a hard block.

The patch parser reads the envelope's file headers. It does not apply, stage,
execute or interpret the patch body, and a body that resembles a command is
inert text to it.

### Enforcement statements

The provider notes and adapter READMEs are corrected to distinguish three
things that the current text blends: what the repository registers, what the
installed client documents, and what has been observed to run. Codex hook
delivery is recorded as an open runtime item with a named verification
procedure and a named next owner. The design does not depend on that item
resolving favourably: for non-authoring roles on Codex the enforced boundary is
the operating-system sandbox, which is independent of the hook.

The response contract is recorded per provider from the installed clients
rather than assumed to be shared. Fields a provider documents as unsupported
are not emitted to that provider, and a non-zero exit with a reason on standard
error is used as the blocking mechanism where the client documents it.

### Permission scope and role guardrails

Each role in the read-only evidence class is examined for whether its
responsibility and required skills actually need a shell. A role that does not
drops `Bash` through the registry's existing per-role native override field,
which the documentation-research role already uses, so no new mechanism is
introduced and the shared class definition is unchanged. A role that runs
repository commands keeps the shell, and the policy text states plainly that
the class means no structured write tool, with shell writes prohibited by
policy and detected advisorily rather than blocked.

The two role guardrails that offer an edit on request are corrected to match
the class they belong to. The asymmetry between an operating-system sandbox on
one provider and a tool allowlist on the other is written down as an accepted,
documented difference rather than presented as parity.

### Evaluation depth

The harness gains evaluation artifacts for the failure modes the governance
depends on: a citation that does not support the claim beside it, a claimed
external action outside the approved boundary, a success claim with no executed
command behind it, and a handoff missing required fields. Each is an evaluation
case and response pair, so the harness itself demonstrates the failure rather
than delegating that proof to a unit test.

The groundedness criterion extends from path existence to a content anchor:
when a cited path is presented next to a quoted span, that span must appear in
the cited file. A criterion for unverified success claims is added. Both
additions are deterministic and local; the harness documentation states that
they cover enumerated modes and do not establish semantic understanding, and
that a synthetic response remains wiring evidence rather than model quality.

## Data Modeling & Storage Strategy

No database, index or cache is introduced. New state is tracked Python under
`scripts/`, tracked shell adapters under the two provider hook directories,
tracked JSON and Markdown under `evals/`, and tracked tests under `tests/`.

The guard holds no persistent state. Its inputs are one payload per invocation
and repository files it reads; its outputs are one advisory message or one
rejection. Temporary files are bounded and removed on every exit path,
including rejection. No payload content, path list or diagnostic is written to
a durable location, so no guard invocation can accumulate a record of what an
agent attempted.

Evaluation cases and responses keep the existing case and response format and
the existing path selection, so the added negative artifacts route through the
validation surface that already covers `evals/`. Role permission data stays in
the single role registry; the per-role override field records a narrower native
scope without duplicating the shared class definition.

Historical statements are preserved rather than rewritten. Provider notes keep
the client identity and observation date already recorded and gain a current
dated observation beside them.

## Interfaces & Data Structures

**Guard input.** A JSON object on standard input carrying a tool name and a
tool input object. Recognized shapes are a scalar path field, a path
collection, an edit list, a patch envelope as a string or an argument vector,
and a shell command string. Conflicting aliases, wrong types, multiple roots
and unparsable bodies are rejected.

**Guard invocation.** The adapters pass an explicit provider argument. The
module resolves its interpreter and helper programs from the project directory
only.

**Guard output.** A JSON object carrying an advisory message on success, or a
rejection written to standard error with a stable machine-readable code and a
non-zero status. Emitted response fields are limited to those the receiving
client documents.

**Registry surface.** The per-role native scope override maps a provider
identifier to that role's narrowed tool list. Permission classes, their
mutation and delegation behaviour, and the provider scope tables keep their
current shape and meaning.

**Evaluation surface.** A case carries an identifier, a role, a prompt, a
response path and a response class. A response is Markdown judged by named
criteria. Added criteria report a criterion name only; no response body is
echoed into a result line.

## Edge Cases & Error Handling

A patch envelope that names no file produces no structured path and no false
warning. A patch that names several files produces one evaluation per file. A
move yields both the source and the destination. A malformed envelope is
rejected as malformed transport, because silence is the defect being repaired.
A patch body containing text that resembles a shell command or another patch
header is treated as inert data.

A path outside the repository, a path escaping through a symbolic link, a path
mixing absolute and relative roots, a payload carrying several conflicting
roots, and a path resolving into a retired authority root are each rejected
before any check reads them. A path inside a linked worktree resolves against
that worktree's own root.

An oversized payload, an unparsable JSON body, a missing interpreter, an
exceeded timeout and an abnormal exit are errors, not passes. A required tool
that is absent fails rather than reporting a diagnostic skip.

An evaluation citation naming a path that does not exist, or quoting a span
absent from the file it cites, fails groundedness. A response asserting a
passing result with no executed command behind it fails the success-claim
criterion.

## Failure Modes & Fallback / Human Escalation

If the guard cannot execute, the policy position is conservative, but the
documentation states each runtime's actual behaviour rather than assuming the
call halts. Where a client continues past a hook error, that fact is recorded
and the boundaries that actually hold — the native permission configuration and
the operating-system sandbox — are named as the remaining controls.

If the Codex client does not discover the registered hook file, the guard
provides no boundary on that provider. The design does not depend on it. The
read-only sandbox remains the enforced boundary for non-authoring roles there,
and the unproven delivery is recorded as an open runtime item with a
verification procedure and a next owner rather than as a passing check.

If narrowing a role's tool scope removes a capability that role genuinely
needs, the narrowing is reverted for that role and the reason recorded, rather
than the role working around the scope through another provider path.

If a baseline gate fails after a change, the failure is separated from the
recorded clean baseline of the current tree and treated as a regression of the
change. A repair is bounded: the same check failing twice with no new
information, two consecutive changes with no observable progress, a repair
requiring wider scope, or an unmet authority stops the work and reports it. No
contract, gate or test is weakened to end the loop.

Rollback is per logical commit through revert. Escalation goes to the user for
any push, pull request, merge, release, credentialed run, global configuration
change, or any decision that would widen approved scope or weaken a control.

## Verification Commands

`python3 -m unittest discover -s tests -t .` judges the guard regressions,
including the patch-envelope case that must fail on the current tree and pass
after the change.

`python3 scripts/validate-agent-governance.py --root .` judges registry
integrity, projection parity, native metadata, permission scopes and the hook
registration of both providers.

`python3 scripts/run-agent-evaluations.py --root .` judges the evaluation
cases, including the added negative artifacts.

`python3 scripts/qa.py staged` judges the exact index during work, and
`python3 scripts/qa.py full` judges the final tree.

The recorded baseline of the current tree is twenty-one gates passing under
`python3 scripts/qa.py full`. Any gate that stops passing after a change is a
regression of that change.

These commands produce repository-static evidence only. They do not establish
that either client discovered a file, loaded a role, honoured a permission,
resolved a model or delivered a hook event. Those require a fresh authenticated
session and are reported separately.

## Success Criteria & Verification Plan

VAL-PWG-001. The shared guard has one owner under `scripts/`, each provider
registers only its own adapter, and no provider directory executes the other's
program. Proven by the governance validator and by reading both registrations.

VAL-PWG-002. A patch envelope naming a Kubernetes manifest produces the same
structured evaluation as the equivalent structured write, for both the string
and the argument-vector payload form. Proven by a regression test that fails on
the current tree and passes after the change.

VAL-PWG-003. No document claims that a provider discovered, loaded or delivered
the registered hook without an observation supporting it, and each unproven
item names its verification procedure and next owner. Proven by document review
against the recorded client identities.

VAL-PWG-004. Read-only evidence roles carry a shell only where the role needs
one, no role guardrail offers an action its tool scope cannot perform, and the
provider difference in real authority is documented rather than claimed as
parity. Proven by the governance validator and role review.

VAL-PWG-005. Narrowing uses the registry's existing per-role override, the
shared permission classes are unchanged in count and behaviour, and the
registry remains the single owner of permission, stop and handoff meaning.
Proven by registry schema validation and diff review.

VAL-PWG-006. Each enumerated failure mode has an evaluation artifact that
reproduces it, and the harness documentation states that added coverage is of
enumerated modes rather than semantic understanding. Proven by the evaluation
runner and by review of the harness documentation.

VAL-PWG-007. Repository-static, provider-runtime, hosted and live evidence stay
in separate classes, and no result is promoted between classes without the
matching observation. Proven by review of the package Task evidence.

VAL-PWG-008. The change is delivered as logical, independently reviewable
commits with proportionate validation and a revertible boundary per commit.
Proven by diff scope review and the recorded gate results per commit.

## Traceability

Requirement inputs come from
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
and the current structural view in
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
The provider enforcement package this specification continues is
[SPEC-0073](../0073-provider-native-enforcement-parity/spec.md); this package
repairs conditions observed in the tree that specification produced and does
not reopen its decisions. Common surface adoption is owned separately by
[SPEC-0075](../0075-common-knowledge-and-prompt-surfaces/spec.md), which
depends on this package only for execution order, not for contract.
[Implementation Plan](plan.md) owns ordered work, entry and exit gates, and
rollback. Its package Task owns execution results, per-lane evidence, and the
limits that remain unobserved.

### Lifecycle Traceability

| Requirement ID                                                                        | Spec criterion | Verification method                                   |
| ------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------- |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-001    | Governance validator and native registration review   |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-002    | Failing-then-passing guard regression test            |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-003    | Provider note review against recorded client identity |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-004    | Permission scope validation and role guardrail review |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-005    | Registry schema validation and diff review            |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-006    | Evaluation runner and harness documentation review    |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-007    | Package Task evidence review                          |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PWG-008    | Diff scope review and per-commit gate results         |
