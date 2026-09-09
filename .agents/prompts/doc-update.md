---
title: "Documentation Update Prompt Contract"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-09-07"
---

# Documentation Update Prompt Contract

## Overview

Identifier `doc-update`. Assemble the request that locates the canonical owner
for a change and proposes a difference against it, so a correction lands at the
one document that owns the statement instead of being copied into several.

## Authority Boundary

Profile selection, section contracts and lifecycle states belong to the Stage 99
registry and the document authoring policy. This contract routes a request to
them; it defines no form and overrides no profile.

## Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Changed path set | `git status --porcelain` | Identifies which owners the change touches |
| Local difference | `git diff` | Shows what statement became untrue |
| Owner candidates | `git ls-files 'docs/**/README.md' '.agents/**/*.md'` | Supplies the routers that name canonical owners |

The subject input is `Changed path set`. When it is empty the contract
refuses, because no statement has changed owner.

## Output

A proposed difference against one named owner path, with the reason the
statement changed. Where more than one document states the same fact, the
output names the single owner and the duplicates to remove rather than editing
each copy.

## Validation

The proposal is judged by the document contract registry and the markdown
profile validator on the target path, and by link and owner validation when it
changes a route. Sealed and completed records are not rewritten to match a new
form.

## Refusal Conditions

- No owner can be resolved for the statement, which means the owner must be
  decided before the text is written.
- The target is a sealed archive record or a completed Task whose body is
  historical evidence.
- The proposal would create a second document stating the same contract.

## Related Documents

- [Common Prompt Contracts](README.md)
- [Document Authoring](../governance/document-authoring.md)
- Document profiles and templates (`docs/99.templates/README.md`)
