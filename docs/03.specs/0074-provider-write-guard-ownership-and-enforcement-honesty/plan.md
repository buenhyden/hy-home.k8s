---
title: "Provider Write-Guard Ownership and Enforcement Honesty Implementation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0074-PLAN-0001"
---

# Provider Write-Guard Ownership and Enforcement Honesty Implementation Plan

## Global Constraints

- One work package is one logical commit. Rollback is `git revert` of that
  commit; no history rewrite, force update, branch deletion, or worktree
  removal is authorized.
- A behavior change demonstrates its failing case before its fix and shows the
  passing result after it.
- The staged profile gates each logical commit; the full profile gates handoff.
  Neither is repeated on unchanged bytes and `--no-verify` is never used.
- Repository-static results never report as native discovery, native
  enforcement, hosted CI, or live behavior.
- Push, pull-request creation, merge, and hosted execution are not authorized
  by this plan and are not implied by any passing check in it.
- The recorded pre-change baseline is twenty-one gates passing under
  `python3 scripts/qa.py full`. Any gate that stops passing is a regression of
  the change that preceded it, not a pre-existing condition.
- Observed client identities for every capability claim in this plan are
  `claude 2.1.263` and `codex-cli 0.153.4` on Ubuntu 24.04 under WSL2,
  observed 2026-09-06.
- No hook is registered on a stop, compaction, or session event on either
  provider.

## Overview

This plan executes [SPEC-0074](spec.md). It moves the shared write-boundary
program out of a provider directory, teaches it to read patch envelopes as
data so a Codex write receives the checks a Claude write already receives,
replaces enforcement claims that observation does not support, narrows the
Claude read-only tool scope where a role does not need a shell, and makes the
evaluation harness reproduce the failures it claims to detect.

The plan changes no Kubernetes, ArgoCD, Vault, or cluster desired state, and
introduces no common surface; SPEC-0075 owns surface adoption.

## Context

The guard exists and runs. `.claude/settings.json` registers it on the shell
and structured file tools, and `.codex/hooks.json` registers it on the shell
and `apply_patch`. Both registrations invoke the same script, which lives at
`.claude/hooks/k8s-pre-edit.sh` and carries its logic as an inline program.

Four observations, made against the tree at `f5f355f1`, set the work.

A synthetic `Write` payload naming `gitops/test.yaml` produced the Kubernetes
manifest advisory. The equivalent `apply_patch` payload naming the same path
produced no output and exit status zero, in both the patch-string and the
argument-vector form. The guard reads `tool_input.command` only through a
shell tokenizer that looks for redirection, `tee`, and in-place `sed`; a patch
envelope contains none of those, so no path is recovered. Shell-derived
targets are deliberately excluded from the structured path pipeline, so on
that provider the manifest, secret-adjacency, and document-route checks never
execute.

The installed Codex client's project path table lists `.codex/config.toml`,
`.codex/agents`, `.codex/hooks`, `.agents`, and `.agents/skills`. The
repository registers `.codex/hooks.json`. The client exposes no command that
lists loaded hooks, so whether the registration is discovered is answerable
only from a session.

The same client's hook contract is partly observable: `PreToolUse` supports
`permissionDecision`, `permissionDecisionReason`, and `systemMessage`, treats
`decision:approve`, `continue:false`, `stopReason`, and `suppressOutput` as
unsupported, and blocks on a non-zero exit that writes a reason to standard
error.

The `read-only-evidence` class maps to `["Read","Grep","Glob","Bash"]` on
Claude and to the `read-only` sandbox on Codex. `.agents/roles/code-reviewer.md`
and `.agents/roles/incident-responder.md` offer an edit on request that the
class has no structured write tool to perform. `.agents/roles/docs-researcher.md`
already narrows its own scope through the registry's `native_scope_override`
field, so the mechanism this plan uses exists and is validated today.

`evals/` holds three cases, all synthetic and all written to pass. Its
`groundedness` criterion checks path existence only; its `boundary` criterion
is a regular expression. Every negative fixture lives in
`tests/test_agent_evaluations.py` rather than as an evaluation artifact.

## Goals & In-Scope

- One owner for the shared guard under `scripts/`, with a thin adapter and a
  native registration per provider.
- A patch envelope parsed as data, contributing its targets to the structured
  path pipeline for both payload forms.
- Provider notes that separate what the repository registers, what the client
  documents, and what has been observed to run.
- A read-only evidence class whose documented meaning matches what it grants,
  with per-role narrowing where a role does not need a shell.
- Evaluation artifacts that reproduce each enumerated failure mode, and a
  groundedness criterion that anchors a citation to content.

## Non-Goals & Out-of-Scope

- No `.agents/knowledge/`, `.agents/prompts/`, `.agents/evaluations/`,
  `.agents/rules/`, or `.agents/scripts/` directory. SPEC-0075 owns adoption.
- No shell parser claiming complete write detection. The shell path stays
  advisory and the documents say so.
- No use of a hook response field on a provider that documents it as
  unsupported, and no reliance on such a field as a fail-closed control.
- No permission class added, removed, or granted mutation authority.
- No change to `gitops/`, `infrastructure/`, `traefik/`, `policy/`, or
  `examples/` behavior.
- No hosted continuous integration workflow, no push, and no merge.

## Work Breakdown

| ID     | Work package                                                                                                       | Depends on     | Entry gate                        | Exit evidence                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------ | -------------- | --------------------------------- | ------------------------------------------------------------------------------------------------- |
| WP-001 | Extract the guard program into `scripts/provider_write_guard.py` and reduce the Claude hook to a thin adapter        | None           | VAL-PWG-001 approved              | Existing guard unit tests pass unchanged; governance validator accepts the registration            |
| WP-002 | Add the Codex adapter under `.codex/hooks/` and repoint `.codex/hooks.json` at it                                   | WP-001         | VAL-PWG-001 approved              | No provider directory invokes the other's program; governance validator hook check passes          |
| WP-003 | Parse patch-envelope targets as data into the structured path pipeline                                              | WP-002         | VAL-PWG-002 approved              | Failing envelope test before, passing after, for both payload forms                                |
| WP-004 | Correct provider notes and adapter READMEs and record Codex hook delivery as an open runtime item                   | WP-003         | VAL-PWG-003 approved              | Reviewed provider text against recorded client identity; link and profile validation               |
| WP-005 | Determine per-role shell need and narrow the Claude scope through the registry override where a role needs none     | WP-004         | VAL-PWG-004, VAL-PWG-005 approved | Failing parity test before, passing after; registry schema validation                              |
| WP-006 | Correct the two role guardrails and state the class meaning at its policy owner                                     | WP-005         | VAL-PWG-004 approved              | Reviewed role and policy text; governance validator                                                |
| WP-007 | Add one evaluation artifact per enumerated failure mode                                                             | WP-006         | VAL-PWG-006 approved              | Each new case fails the criterion it targets before the criterion work, and is graded after        |
| WP-008 | Anchor groundedness to content, add an unverified-success criterion, and state the coverage limit in the harness doc | WP-007         | VAL-PWG-006 approved              | Failing grading tests before, passing after; the runner reports criterion names only               |
| WP-009 | Record evidence-class separation, the deferred runtime items, their blockers, and their next owners in the Task      | WP-008         | VAL-PWG-007 approved              | Task evidence review; no repository-static result presented as runtime evidence                    |
| WP-010 | Review the final diff scope, run the full profile, and record per-commit gate results and the rollback boundary      | WP-009         | VAL-PWG-008 approved              | Full profile result against the recorded baseline; per-commit revert boundary named                |

### WP-001: Extract the guard program

**Files:** Create `scripts/provider_write_guard.py`. Modify
`.claude/hooks/k8s-pre-edit.sh`. Test `tests/test_k8s_pre_edit_hook.py`.

**Interfaces.** Produces a module invoked as
`python3 scripts/provider_write_guard.py --provider {claude|codex}` reading one
JSON payload on standard input, writing an advisory JSON object on standard
output, and writing `[FAIL] <CODE>` to standard error with exit status 2 on
rejection. Consumes nothing from earlier packages.

- [ ] Run `python3 -m unittest tests.test_k8s_pre_edit_hook -v` and record the
      passing baseline, so the extraction is proven behavior-preserving.
- [ ] Move the inline program body into `scripts/provider_write_guard.py`
      unchanged except for reading `--provider` and resolving `PROJECT_DIR`
      from the argument or the environment.
- [ ] Reduce `.claude/hooks/k8s-pre-edit.sh` to forwarding standard input to
      `python3 "$PROJECT_DIR/scripts/provider_write_guard.py" --provider claude`,
      keeping `PROJECT_DIR` resolution and the rule that the executed program
      always comes from the project directory.
- [ ] Re-run the same unit module. Expected: identical passing result.
- [ ] Re-run the two probe payloads from the specification's Context and record
      that Claude behavior is unchanged.
- [ ] Run `python3 scripts/validate-agent-governance.py --root .`. Expected:
      PASS, because the registered command still names an existing file under
      `.claude/hooks/`.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-002: Add the Codex adapter

**Files:** Create `.codex/hooks/pre-tool-use.sh`. Modify `.codex/hooks.json`,
`.codex/README.md`. Test `tests/test_k8s_pre_edit_hook.py`.

**Interfaces.** Produces `.codex/hooks/pre-tool-use.sh`, which forwards
standard input to the module with `--provider codex`. Consumes the module
interface from WP-001.

- [ ] Write a failing test asserting that the command string in
      `.codex/hooks.json` does not reference any path under `.claude/`.
- [ ] Run it. Expected: FAIL, because the current registration names
      `.claude/hooks/k8s-pre-edit.sh`.
- [ ] Add `.codex/hooks/pre-tool-use.sh` as the Codex-side thin adapter.
- [ ] Repoint `.codex/hooks.json` at the new adapter, keeping the existing
      matcher, the ten-second timeout, and the status message.
- [ ] Update `.codex/README.md` so the structure list names the adapter
      directory instead of describing the Claude script as shared.
- [ ] Run the test. Expected: PASS.
- [ ] Run `python3 scripts/validate-agent-governance.py --root .`. Expected:
      PASS, because the Codex registration now names an existing file under
      `.codex/hooks/`.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-003: Parse patch envelopes as data

**Files:** Modify `scripts/provider_write_guard.py`. Test
`tests/test_k8s_pre_edit_hook.py`.

**Interfaces.** Produces a normalizer that routes a payload by shape. A patch
envelope contributes its `Add File`, `Update File`, `Delete File`, and
`Move to` targets to the same structured path list a `file_path` field feeds.
Consumes the module interface from WP-001.

- [ ] Write the failing test. It sends the two payloads below and asserts that
      each produces the Kubernetes manifest advisory that the equivalent
      `Write` payload produces.

```python
PATCH_STRING = {
    "tool_name": "apply_patch",
    "tool_input": {
        "command": (
            "*** Begin Patch\n"
            "*** Update File: gitops/test.yaml\n"
            "@@\n-a\n+b\n"
            "*** End Patch\n"
        )
    },
}

PATCH_ARGV = {
    "tool_name": "apply_patch",
    "tool_input": {
        "command": [
            "apply_patch",
            "*** Begin Patch\n"
            "*** Add File: gitops/new.yaml\n"
            "+data\n"
            "*** End Patch\n",
        ]
    },
}
```

- [ ] Run `python3 -m unittest tests.test_k8s_pre_edit_hook -v`. Expected:
      FAIL, because the current guard returns no message and exit status zero
      for both payloads.
- [ ] Implement the envelope parser. It reads only the file-header lines, adds
      each target through the existing structured path entry point so symbolic
      link, root, and retired-path rejection still apply, yields both the
      source and the destination for a move, and treats the patch body as
      inert text. It never applies, stages, or executes the patch.
- [ ] Run the test. Expected: PASS for both payload forms.
- [ ] Add and run the boundary cases: an envelope naming no file produces no
      message and no error; an envelope naming several files produces one
      evaluation per file; a malformed envelope is rejected as malformed
      transport rather than ignored; a body containing text resembling a shell
      command produces no shell target.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-004: Correct the enforcement statements

**Files:** Modify `.codex/provider.md`, `.codex/README.md`,
`.claude/provider.md`, `.claude/README.md`.

**Interfaces.** Produces provider text that separates registration,
documented client capability, and observed behavior. Consumes the arrangement
from WP-002.

- [ ] Replace text implying the Codex registration is delivered with text
      stating what is registered, what the client documents, and that delivery
      is unobserved.
- [ ] Record the open runtime item: whether the installed client discovers
      `.codex/hooks.json`, the procedure that answers it, and the next owner.
- [ ] Record the observed `PreToolUse` response contract per provider, and
      state that unsupported fields are not emitted to the provider that
      rejects them.
- [ ] State that for non-authoring roles on Codex the enforced boundary is the
      operating-system sandbox, independent of the hook.
- [ ] State that the shell path is advisory on both providers and does not
      detect every write.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-005: Narrow the read-only scope where a role needs no shell

**Files:** Modify `.agents/roles/registry.json`. Test
`tests/test_agent_governance.py`.

**Interfaces.** Produces per-role `native_scope_override` entries for the
Claude provider. Consumes the existing override field the documentation
research role already uses; adds no new registry mechanism.

- [ ] For each role in the read-only evidence class, read its responsibility
      and every skill it references, and record whether the role needs a shell
      to produce its evidence. Record the determination per role with its
      reason before changing anything.
- [ ] Write the failing test asserting that a role recorded as needing no
      shell carries no `Bash` in its Claude projection.
- [ ] Run it. Expected: FAIL.
- [ ] Add the override for each such role and re-render its Claude projection
      so the `tools` field matches, because the governance validator compares
      the projection to the registry scope exactly.
- [ ] Run the test and `python3 scripts/validate-agent-governance.py --root .`.
      Expected: PASS.
- [ ] Confirm the three shared permission classes are unchanged in count and
      behavior by diffing the `permission_classes` array.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-006: Correct the role guardrails and the class meaning

**Files:** Modify `.agents/roles/code-reviewer.md`,
`.agents/roles/incident-responder.md`,
`.agents/governance/approval-and-safety.md`.

- [ ] Replace the edit-on-request carve-out in both role guardrails with the
      restriction the class actually imposes, matching the unconditional
      phrasing the other roles in the class already use.
- [ ] State at the approval policy that the class means no structured write
      tool, that shell writes are prohibited by policy and detected
      advisorily rather than blocked, and that the operating-system sandbox on
      Codex is a different and stronger boundary.
- [ ] State that the difference between the two providers is accepted and
      documented, not parity.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-007: Add the evaluation artifacts

**Files:** Create four case files under `evals/cases/` and four response files
under `evals/responses/`. Modify `evals/README.md`.

**Interfaces.** Produces cases in the existing format: an identifier, a role,
a prompt, a response path, and a response class. Consumes the existing runner.

- [ ] Add a case whose response cites a path that exists but quotes a span
      absent from it.
- [ ] Add a case whose response claims an external action outside the approved
      boundary.
- [ ] Add a case whose response asserts a passing result with no executed
      command behind it.
- [ ] Add a case whose response omits a required handoff field.
- [ ] Run `python3 scripts/run-agent-evaluations.py --root .`. Expected: the
      boundary case and the handoff case already fail; the citation case and
      the success-claim case still pass, which is the gap WP-008 closes.
- [ ] Record that observed split in the Task before proceeding.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-008: Anchor groundedness and add the success-claim criterion

**Files:** Modify `scripts/run-agent-evaluations.py`, `evals/README.md`. Test
`tests/test_agent_evaluations.py`.

**Interfaces.** Produces two criteria. The groundedness criterion additionally
requires that a quoted span presented next to a cited path appears in that
file. The success-claim criterion fails a response asserting a passing result
with no executed command recorded beside it. Both report a criterion name only
and never echo a response body.

- [ ] Write the failing unit tests for both criteria using the WP-007
      artifacts as inputs.
- [ ] Run `python3 -m unittest tests.test_agent_evaluations -v`. Expected:
      FAIL.
- [ ] Implement both criteria deterministically and locally, with no model
      call and no network access.
- [ ] Run the unit module and the runner. Expected: PASS, and the two
      previously passing negative artifacts now fail the criteria they target.
- [ ] State in `evals/README.md` that the added criteria cover enumerated
      failure modes and do not establish semantic understanding, and that a
      synthetic response remains wiring evidence rather than model quality.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-009: Record the evidence classes and the deferred items

**Files:** Modify the package Task.

- [ ] Record each result under its evidence class: repository-static,
      provider-runtime, hosted, or live.
- [ ] Record each deferred runtime item with its blocker, the procedure that
      would answer it, and its next owner. The Codex hook discovery question
      and both providers' discovery, permission, model resolution, and hook
      delivery remain deferred.
- [ ] Confirm no repository-static result is written as runtime evidence.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-010: Review scope and close the package

**Files:** Modify the package Task.

- [ ] Review the full diff for scope, removing any task-owned scratch residue.
- [ ] Run `python3 scripts/qa.py full`. Expected: twenty-one gates passing,
      matching the recorded baseline.
- [ ] Record per-commit gate results and the revert boundary for each commit.
- [ ] Record the handoff fields the quality policy requires, including
      failures, skipped optional tools, unavailable runtime checks, review
      disposition, rollback, residual risk, and next owner.
- [ ] Commit.

## Verification Plan

Each work package runs its focused checks during implementation, then the
staged profile against its exact index snapshot before its commit. The full
profile runs once on the final working tree before handoff.

A behavior change runs its failing case first and records the failure, then
runs the same case after the fix and records the pass. A document-only package
runs the profile, link, and lifecycle validators that its paths route to.

Invoking a document validator directly rather than through `scripts/qa.py`
compares against the Git index and is not a substitute for the lane the entry
point selects; the direct invocation is not used as evidence.

No command in this plan establishes native discovery, native permission
enforcement, model resolution, or hook delivery on either provider.

## Risks & Mitigations

Extracting the guard could change its behavior silently. The extraction package
runs the existing unit module before and after and re-runs the recorded probe
payloads, so a behavior change appears as a test difference rather than as a
weakened boundary.

Parsing a patch envelope could be mistaken for applying it. The parser reads
file-header lines only, and its boundary cases include a body containing text
that resembles a command, so an executable interpretation would fail a test.

Narrowing a role's tool scope could remove a capability the role needs. The
determination is recorded per role with its reason before any change, and a
role that turns out to need a shell has its narrowing reverted with the reason
recorded rather than working around the scope by another path.

Adding evaluation criteria could be read as claiming semantic judgement. The
harness documentation states the coverage limit, and the criteria are named
after the enumerated modes they detect.

The Codex hook may not be delivered at all. The design does not depend on it;
the sandbox remains the enforced boundary for non-authoring roles there, and
the question is recorded as deferred rather than resolved by assumption.

## Completion Criteria

Every criterion from VAL-PWG-001 through VAL-PWG-008 has its named evidence.
The full profile matches the recorded baseline. Each work package is one
revertible commit. Every deferred item names its blocker and next owner, and
no repository-static result is reported as runtime evidence.

## Traceability

[SPEC-0074](spec.md) owns the change contract and the criteria. The package
Task owns execution results, per-lane evidence, and the limits that remain
unobserved.

### Lifecycle Traceability

| Spec criterion                                             | Work package                                           | Expected Task                                                                     |
| ---------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| [VAL-PWG-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002                                         | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-002](spec.md#success-criteria--verification-plan) | WP-003                                                 | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-003](spec.md#success-criteria--verification-plan) | WP-004                                                 | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-004](spec.md#success-criteria--verification-plan) | WP-005, WP-006                                         | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-005](spec.md#success-criteria--verification-plan) | WP-005                                                 | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-006](spec.md#success-criteria--verification-plan) | WP-007, WP-008                                         | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-007](spec.md#success-criteria--verification-plan) | WP-009                                                 | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
| [VAL-PWG-008](spec.md#success-criteria--verification-plan) | WP-010                                                 | [tsk-0001](tasks/tsk-0001-establish-write-guard-ownership-and-enforcement-honesty.md) |
