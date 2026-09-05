---
title: "Retired Provider Residue Disposition Technical Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-03"
layer: "specs"
artifact_id: "SPEC-0070"
---

# Retired Provider Residue Disposition Technical Specification (Spec)

## Overview

[ADR-0030](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
removed Gemini and Antigravity as supported providers and explicitly rejected
retaining them as dormant ones. The tracked corpus still names them 667 times
across 74 files.

Almost all of that is history and must stay. A closed Spec that planned Gemini
work, a superseded ADR that decided it, a sealed archive ledger that recorded
its migration, a dated Stage 90 observation, and a test that proves the surface
no longer exists are all accurate records. Editing them would falsify the
repository's account of its own past.

Seven surfaces are different. Five are live executable or configuration
surfaces that still admit a removed provider's path, so a file the decision
deleted would still be routed, matched, or labeled if it reappeared. Two are
authored documents with a current lifecycle status that still present the
removed providers as candidate surfaces, adapters, and canary subjects — an
active document asserting a provider set the accepted decision replaced.

This Spec disposes of those six and states the rule that separates them from the
627 mentions it preserves.

Measured counts below are point-in-time audit evidence recorded on 2026-09-02.
They are not permanent governance invariants.

## Strategic Boundaries & Non-goals

In scope: the `common/root-provider-shim` path pattern in
`docs/99.templates/registry.json`; the provider case branch in
`docs/00.agent-governance/hooks/post-validate.sh`; the gateway glob in
`.github/labeler.yml`; the retired-provider environment variable in
`tests/test_provider_post_validate_hook.py`; and the current provider assertions
in `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`
and `docs/01.requirements/0003-workspace-agent-governance-platform.md`.

Out of scope: every closed Stage 03 Spec, Plan, and Task; the superseded
[ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
and [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md);
ADR-0030's own account of what it removed; the Stage 98 archive and its sealed
migration ledgers; dated Stage 90 research observations; Git-backed recovery
evidence for the retired transition mapping; the tests that assert the removed
surfaces are absent; and the credential denylist literals in
`scripts/validate-agent-governance-ci.py`.

The two authored documents are revised, not superseded. Neither has a successor,
and each is the only Architecture Description and Requirement Package for the
agent governance platform. Marking them superseded would leave the platform with
no current owner, which is a worse outcome than a stale paragraph.

## Contracts

- **C1 — No live surface admits a removed provider.** A tracked path pattern,
  glob, case branch, or environment variable that names a removed provider's
  gateway or projection root is removed.
- **C2 — An active document states the current provider set.** A document whose
  lifecycle status is current does not present a removed provider as a
  supported surface, adapter, model candidate, or canary subject.
- **C3 — History is preserved unchanged.** A record whose lifecycle status is
  closed, superseded, or archived keeps its provider content byte-for-byte.
- **C4 — Absence proofs are preserved.** A test asserting that a removed
  provider's surface does not exist is kept and continues to pass.
- **C5 — A prohibition is not an assertion.** A credential or secret denylist
  entry naming a removed provider is kept. Forbidding a literal does not claim
  the provider exists, and removing the entry would narrow a security control
  for no governance benefit.

## Core Design

### The classification rule

The disposition turns on whether a mention is an assertion about the present or
a record of the past, not on the word itself. A retired-provider name is
residue when the file that carries it is consulted to decide current behavior:
a live pattern that would match, a live branch that would run, or a current
document a reader would follow. The same name in a closed Plan is a fact about
what was planned.

This is why 627 of 667 mentions are preserved. A sweep that counted the word
rather than its liveness would delete the repository's evidence that the removal
happened, including the tests that prove it.

### Live surfaces

`common/root-provider-shim` matches `^(?:AGENTS\.md|CLAUDE\.md|GEMINI\.md)$`.
The third alternative names a gateway ADR-0030 deleted, so the profile would
admit and govern a file that must not exist. The alternation drops to the two
current gateways.

`post-validate.sh` lists `GEMINI.md` in the case pattern that decides which
changed paths trigger validation. The branch cannot be reached by a tracked
file today and would silently start validating a reintroduced gateway if one
appeared.

`.github/labeler.yml` labels changes touching `GEMINI.md`. The glob matches
nothing and would silently label a reintroduced gateway.

`test_provider_post_validate_hook.py` sets `GEMINI_PROJECT_DIR` in the hook's
test environment. The hook reads only `CLAUDE_PROJECT_DIR`, so the variable is
inert; it is removed as dead setup rather than as an absence proof, which C4
distinguishes.

`.gitignore` carries `.opencode/skills/` with a `.gitkeep` negation under an
`# opencode Skills` heading. This is a wider case than the rest: OpenCode was
never one of the providers ADR-0030 removed, because it was never a declared
provider at all. `.agents/registry.json` names `claude` and `codex`, the
directory does not exist, and those three lines are the only trace of the name
anywhere in the repository. An ignore rule for a provider the governance never
admitted reserves a path the control plane does not recognize, so it is removed
with the rest rather than left as the one unexplained provider name in the
tracked corpus.

### Active documents

`AD-0006` carries a component-table row declaring `.gemini/**` a Gemini-native
projection surface, an adapter-field row for Gemini metadata, a model-candidate
sentence naming `gemini-3-pro-preview` and `gemini-3-flash-preview`, a canary
requirement naming three providers, and external links to the Gemini CLI
documentation. Each is revised to the two-provider architecture ADR-0030
established. The document's structure, other rows, and every non-provider claim
are unchanged.

`REQ-0003` carries a surface-inventory row for `.gemini/**`, an acceptance
criterion clause about a `.gemini`-surface-absent claim, a three-surface count,
and six external Gemini documentation source links. The same treatment applies.
Where a requirement's acceptance clause depends on the retired surface, the
clause is restated against the current surface set rather than deleted, so the
acceptance count and its identifiers stay stable.

Both documents' `updated` dates advance and their `version` values do not: under
C3 of SPEC-0071 a version is not incremented by a governance correction, and
under this Spec the documents assert the same requirements against a smaller
provider set.

## Data Modeling & Storage Strategy

No schema, contract, or registry profile shape changes. One profile's
`pathPattern` string loses an alternation branch. No frontmatter key is added,
removed, or reordered, and no artifact identity changes.

The two authored documents keep their identities, `AD-0006` and `REQ-0003`, and
their lifecycle status stays current. No Stage 98 record is created, because
nothing is retired to the archive: a revised active document is not an archived
one, and the prior text is recoverable from Git history.

## Interfaces & Data Structures

The changed interfaces are four literal patterns:

| Surface | Before | After |
| --- | --- | --- |
| `registry.json` profile | `^(?:AGENTS\.md\|CLAUDE\.md\|GEMINI\.md)$` | `^(?:AGENTS\.md\|CLAUDE\.md)$` |
| `post-validate.sh` case | `AGENTS.md \| CLAUDE.md \| GEMINI.md \| ...` | `AGENTS.md \| CLAUDE.md \| ...` |
| `.github/labeler.yml` | glob list including `GEMINI.md` | glob list without it |
| hook test environment | `GEMINI_PROJECT_DIR` set | key absent |

## Edge Cases & Error Handling

Narrowing the `common/root-provider-shim` pattern must not orphan a tracked
path. The audit confirms no tracked file matches the removed alternative, so the
strict contract registry run must still report zero uncovered paths after the
change; if it does not, a file exists that the audit missed and the change is
reverted rather than forced.

Removing external documentation links from `AD-0006` and `REQ-0003` must not
break a link the strict link validator resolves. Those links are absolute
external URLs, which the validator does not resolve, so their removal is a
content change rather than a link change.

`REQ-0003` acceptance criterion identifiers are referenced by closed Specs. The
criterion is restated rather than renumbered or deleted, because a closed Spec's
traceability row naming a criterion must continue to resolve.

A test asserting a removed provider's absence must keep passing unchanged. If
narrowing a pattern causes such a test to fail, the pattern change is wrong, not
the test.

## Failure Modes & Fallback / Human Escalation

If any change to a live pattern causes a validator to report an uncovered path,
an unresolved link, or a failing absence proof, the change is reverted and the
finding is recorded before retrying. A residue removal that breaks a proof of
the removal is self-defeating.

Rollback is a Git revert of the owning commit. No sealed payload, archive
digest, or external surface is touched, so rollback requires no coordination
beyond the repository.

Escalate to the human owner if revising `AD-0006` or `REQ-0003` would change the
meaning of a requirement rather than its provider inventory, or if a mention the
audit classified as historical turns out to be consulted by a live surface.

## Verification Commands

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-agent-governance-ci.py --root .
python3 -m unittest discover --start-directory tests --top-level-directory tests
bash scripts/validate-repo-quality-gates.sh .
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-RPR-001 | No live path pattern, glob, case branch, or environment variable names a removed provider's gateway or projection root | Sweep over registry profiles, hook scripts, workflow configuration, and test environments |
| VAL-RPR-002 | Narrowing the root provider shim pattern leaves zero uncovered and zero ambiguous paths | Strict document contract registry run |
| VAL-RPR-003 | No document with a current lifecycle status presents a removed provider as a supported surface, adapter, model candidate, or canary subject | Current-document sweep across Stage 01, 02, and 00 |
| VAL-RPR-004 | Closed Stage 03 records, superseded ADRs, Stage 98 payloads, Stage 90 observations, and historical migration rows are byte-identical | Diff scope review over the owning commit |
| VAL-RPR-005 | Every test asserting a removed provider's absence still passes unchanged | Full suite run with the absence tests unmodified |
| VAL-RPR-006 | Credential denylist literals naming removed providers are retained | Denylist content assertion |
| VAL-RPR-007 | `AD-0006` and `REQ-0003` keep their identities, current status, and acceptance identifiers | Frontmatter and criterion identifier comparison before and after |
| VAL-RPR-008 | No closed record's traceability link to a revised acceptance criterion is broken | Strict link and owner validation |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — ADR-0030 provider removal clause | VAL-RPR-001 | Live-surface residue sweep |
| N/A — ADR-0030 provider removal clause | VAL-RPR-002 | Strict registry coverage run |
| N/A — ADR-0030 provider removal clause | VAL-RPR-003 | Current-document assertion sweep |
| N/A — history preservation boundary | VAL-RPR-004 | Commit diff scope review |
| N/A — history preservation boundary | VAL-RPR-005 | Unmodified absence-proof suite run |
| N/A — security control preservation | VAL-RPR-006 | Denylist content assertion |
| N/A — identity and acceptance stability | VAL-RPR-007 | Frontmatter and identifier comparison |
| N/A — identity and acceptance stability | VAL-RPR-008 | Strict link and owner validation |

### Related Documents

- [Current Spec Index](../README.md#current-spec-index)
- [ADR-0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- [AD-0006 — workspace agent governance platform](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- [REQ-0003 — workspace agent governance platform](../../01.requirements/0003-workspace-agent-governance-platform.md)
- [SPEC-0065 — transition residue retirement](../../98.archive/completed/03.specs/0065-transition-residue-retirement/spec.md)
- [Quality Policy](../../00.agent-governance/policies/quality.md)
