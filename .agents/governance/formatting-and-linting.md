---
title: "Formatting and Linting Policy"
version: "1.6.1"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-13"
---

# Formatting and Linting Policy

## Purpose

### Objective

Each formatting and linting rule has one semantic owner. Git normalization,
editor hints and hook delivery may project that rule for their distinct jobs,
and each suppression states why it exists. A configuration file that no tool
reads is not a convention; it is drift that reads like one.

### Authority

This policy owns which tool covers which file type, where a shared byte rule
is declared, and the discipline for suppressing a rule. It does not own lane,
result, or completion order, which belong to [quality](quality.md); validator
selection, which belongs to the validation-surface registry; or the rules
inside a tool's own configuration. Terminal-document immutability belongs to
[document lifecycle](document-lifecycle.md).

- [Quality Policy](quality.md)
- [Document Lifecycle Policy](document-lifecycle.md)
- [Git Policy](git.md)

## Scope

### Applies To

`.gitattributes` owns Git text and line-ending normalization.
`.pre-commit-config.yaml` owns hook integration, including pinned revisions,
stages, arguments and exclusions. Its local staged and selected manual QA
invocations share the same rule owner; the hosted `ci-summary` job is not a
formatter. The separate PR-only `style-pr` job may invoke the same selected style
rule against its own merge input; it does not certify local purpose or
document-content checks. `.editorconfig` reaches editors only and proves nothing
about committed bytes.

### Exclusions

Exclusions of files from formatters and linters are stated under Requirements.

## Rules

### Requirements

- Keep one semantic owner for each rule. Project it only where a complementary
  layer needs it: `.gitattributes` for Git normalization, `.editorconfig` for
  editor hints, and hook or tool configuration for validation and rewriting.
  Mirrored values across those layers are not separate rules; document their
  purpose and validate that the committed result agrees.
- For an ordinary authored document or README router edit, select only the
  applicable document-facing style rules on changed files. Keep the common
  diff and commit-message checks and the active hook chain; do not add shell,
  Python, infrastructure or whole-tree formatting merely because the file is
  Markdown. A change to a formatting rule or hook configuration needs its own
  focused contract regression under [quality](quality.md#ordinary-document-selection).
- The selected lint and format rules run on the final logical index as the
  `selected-style` gate inside the `staged-qa` hook (`qa.py staged`), one run
  before a local commit. Reuse a successful identical style leaf under
  [quality](quality.md#validation-lane-contract) instead of running it again in
  another local caller. A hosted PR
  style check uses the same declared rules on its distinct PR merge input and
  records its own SHA/run; a successful local result cannot stand in for it.
  A deployment style check requires an actual deployment workflow and observed
  run; no such result follows from a tracked rule alone.
- Keep no configuration for a file type the repository does not contain.
  When the last target of a tool disappears, remove the tool and its
  configuration in the same change rather than leaving an unread file.
- Do not add a second tool that enforces a rule an existing tool already
  enforces. Extend the owner instead.
- Explicitly declare file types or rules when that projection preserves an
  ownership boundary. A pinned tool may intentionally retain reviewed defaults.
  Before raising its revision, measure default changes, check whether they widen
  the rule set or claim another tool's file type, and validate the resulting
  corpus behavior before accepting the upgrade.
- Scope a rule by capability, not by exclusion. Prefer configuring a checker
  to understand a file shape over excluding the tree that has that shape.
- State a cause for every suppression and classify it as a deliberate
  authoring convention, a rule blocked by documents the lifecycle policy
  forbids editing, or living debt to be retired by fixing the documents.
  A bare disabled rule hides which of the three it is.
- Linters report. Shfmt, Ruff format and whitespace hooks rewrite their input
  files. QA runs them inside an isolated snapshot, detects changed bytes and
  fails without modifying the source tree/index. An explicitly approved fix
  uses the same pinned hooks with `--files` naming only reviewed source paths;
  inspect the diff, restage and refresh the affected evidence afterward.
- ShellCheck and shfmt cover shell scripts under `scripts/`, `infrastructure/`
  and both provider hook directories, plus the extensionless
  `scripts/githooks/` entries (`pre-commit`, `commit-msg`, `pre-push`). Ruff's explicit Python type restriction
  keeps Markdown with its own reporting linter.
- Never suppress a rule for a whole file when the conflict is one rule.
  A whole-file exemption silently drops every other rule on that file.
- Exclude `docs/98.archive/` from every auto-fixing formatter and from
  Markdown lint: it is unvalidated history. The three whitespace hooks share
  one hook-local exclusion for it, which also covers the raw paired-trial
  outputs `.agents/evaluations/harnesses/*/baseline.md` and `with-skill.md`
  (Markdown lint ignores the same files). Secret scanners are not excluded.

### Enforcement

Measure a suppression before changing it: remove it in a copy of the tracked
corpus outside the working tree, run the tool over that copy, and classify
each finding by the lifecycle status of the document holding it. Findings
confined to terminal documents cannot be retired by editing; findings in
current documents can. Re-measure when a blocking document changes state or
when a hook revision moves, and record the result in the owning Task.

## Exceptions

### Exception Conditions

Exception and escalation conditions are stated under Requirements.

### Approval and Review

Approval and review conditions are stated under Requirements.

## Ownership

### Responsibilities

Responsibilities are stated under Authority and Requirements.

### Change and Adoption

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
