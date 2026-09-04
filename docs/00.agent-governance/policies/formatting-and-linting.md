---
title: "Formatting and Linting Policy"
version: "1.2.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-04"
---

# Formatting and Linting Policy

## Overview

Each file type has one formatting and linting owner, each rule is declared
once, and each suppression states why it exists. A configuration file that no
tool reads is not a convention; it is drift that reads like one.

## Authority Boundary

This policy owns which tool covers which file type, where a shared byte rule
is declared, and the discipline for suppressing a rule. It does not own lane,
result, or completion order, which belong to [quality](quality.md); validator
selection, which belongs to the validation-surface registry; or the rules
inside a tool's own configuration. Terminal-document immutability belongs to
[document lifecycle](document-lifecycle.md).

## Governance Context

`.pre-commit-config.yaml` is the single enforcement surface. It runs from the
local aggregate and from the hosted pre-commit job over the same pinned hook
revisions, so a rule added there applies to both lanes at once. `.editorconfig`
reaches editors only and proves nothing about committed bytes.

## Current Contract

- Declare a shared byte rule at most twice: once in `.editorconfig` as an
  editor hint, once in `.pre-commit-config.yaml` as enforcement. Where the two
  disagree, the hook decides. Do not add a third declaration in a tool that
  targets one file type.
- Keep no configuration for a file type the repository does not contain.
  When the last target of a tool disappears, remove the tool and its
  configuration in the same change rather than leaving an unread file.
- Do not add a second tool that enforces a rule an existing tool already
  enforces. Extend the owner instead.
- Declare which file types a tool covers and which rules it applies. Do not
  inherit either from the tool's own defaults. A pinned revision still moves
  when it is raised, and one release can both widen a default rule set and
  hand a formatter a file type another tool already owns, changing what the
  hosted lane enforces with no change in this repository.
- Scope a rule by capability, not by exclusion. Prefer configuring a checker
  to understand a file shape over excluding the tree that has that shape.
- State a cause for every suppression and classify it as a deliberate
  authoring convention, a rule blocked by documents the lifecycle policy
  forbids editing, or living debt to be retired by fixing the documents.
  A bare disabled rule hides which of the three it is.
- Linters report during validation. A tool that rewrites files while a
  validation lane runs would edit outside the change under review, so
  automatic fixing stays with the whitespace hooks that own it.
- Never suppress a rule for a whole file when the conflict is one rule.
  A whole-file exemption silently drops every other rule on that file.
- Exclude frozen Archive payloads from every auto-fixing formatter. Validate
  their envelope, manifest, source commit/blob, digest, and historical links
  without changing their body bytes. Apply current formatting only to active
  documents and newly authored current-generation Archive records.

## Validation and Refresh

Measure a suppression before changing it: remove it in a copy of the tracked
corpus outside the working tree, run the tool over that copy, and classify
each finding by the lifecycle status of the document holding it. Findings
confined to terminal documents cannot be retired by editing; findings in
current documents can. Re-measure when a blocking document changes state or
when a hook revision moves, and record the result in the owning Task.

## Related Documents

- [Quality Policy](quality.md)
- [Document Lifecycle Policy](document-lifecycle.md)
- [Git Policy](git.md)
