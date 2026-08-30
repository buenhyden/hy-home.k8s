---
title: 'Validation Tooling Ownership Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-08-31
artifact_id: "SPEC-0066"
---

# Validation Tooling Ownership Technical Specification (Spec)

## Overview

Direct human approval on 2026-08-31 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

`scripts/README.md` states the rule that governs the directory: consolidation is
considered only when four conditions hold, and deletion requires a precheck whose
reference sweep is `rg -n "scripts/<name>\.sh|<name>\.sh" .`. It then concludes
that the current scripts are kept separate, and records the count it reasoned
over as eight.

`scripts/` holds forty-eight tracked files. Thirty-nine are Python. The stated
conclusion is still true of the eight shell scripts it was written about, so no
gate reports a defect, and the thirty-nine Python modules have never entered the
criteria that decide consolidation, deletion, or ownership.

The same narrowing is compiled into the gate. `validate-repo-quality-gates.sh`
defines `script_ref_pattern = re.compile(r"scripts/[A-Za-z0-9_.-]+\.sh")` and
applies it at two sites. The character class excludes `/`, so a reference to a
script at any depth below `scripts/` matches nothing, and a `.py` reference has
never matched. A restructure therefore does not break this rule; it silences it.

This Spec makes the rule reach its subject before moving the subject, then moves
`scripts/` and `tests/` onto one role-first structure with one owner per fact.

## Strategic Boundaries & Non-goals

In scope: the tracked contents of `scripts/` and `tests/`, the two script
reference rules in `validate-repo-quality-gates.sh`, `scripts/README.md` and
`tests/README.md`, and the runner and hook surfaces that name a moved path.

Protected: `docs/00.agent-governance/contracts/validation-surfaces.json` is read
but not rewritten. Its routes are `^scripts/.*$` and `^tests/.*$`, and the
selection contract was exercised against the proposed paths before this Spec was
written: five hypothetical restructured paths select the same sixteen validators
as the current paths, with `unmatchedPaths` empty. A restructure that requires
editing the surface contract is out of contract and must stop.

Non-goals: no validator's failure semantics change; no declared `argv` loses
`--self-test`; no live, hosted, provider-runtime, or cluster evidence is claimed.
The `scripts` surface fan-out — sixteen validators on any change — is
investigated and its disposition recorded, but reducing it is not promised here:
its declared fallback states that validator changes rerun every dependent static
lane, and narrowing that is a separate authority decision.

## Contracts

1. A tracked reference to an executable under `scripts/` is checked for
   existence regardless of the file's extension or its depth in the tree.
2. `scripts/README.md` governs every tracked file under `scripts/`. Its
   consolidation criteria and deletion precheck name no single extension.
3. A module under `scripts/validation/` does not import another module under
   `scripts/validation/`. Shared code is reached only through `scripts/lib/`.
4. A case table has exactly one owner. No module under `scripts/` reads a path
   under `tests/`.
5. One module-loading convention holds across `scripts/`, and one across
   `tests/`.
6. A repository-internal commit pin is either resolved through a sealed
   migration record or is itself the sealed record's coordinate.

## Core Design

The structure is role-first. Domain is the second axis, never the first, because
a tree that mixes both at the top has two valid homes for most files and drifts
on the next addition.

```
scripts/
├── README.md              entry point only
├── docs/                  the directory's own inventory, tiers, command contract
├── lib/                   shared modules with no entry point
├── validation/
│   ├── agent/ document/ archive/ gitops/ ci/
│   └── cases/             the single owner of case tables
├── qa/                    aggregate, selection, and lane runners
└── setup/                 generators
tests/                     mirrors the scripts tree; stays top-level
```

`tests/` stays at the top level rather than moving under `scripts/validation/`.
The two are separate routed surfaces with different protection levels —
`scripts` is `protected`, `tests` is `review`. Merging them would place every
case-table edit behind the protected approval boundary. Mirroring satisfies the
requirement that tests be split along the same responsibility units as the
production modules without moving that boundary.

Case tables move to `scripts/validation/cases/` rather than staying under
`tests/`. Thirteen production modules currently read `tests/fixtures/`, and
thirteen modules carry a `--self-test`; the fixtures serve both and are owned by
neither. Moving them under the validators makes production read its own
directory and makes tests read upward into production, which is the direction
that composes. Removing `--self-test` instead was rejected: it appears in the
declared `argv` of a routed validator, so removing it would edit the protected
surface contract this Spec does not touch.

Order is forced by the silence. The reference rule must reach `.py` and reach
depth **before** anything moves. A move made first would be verified by a rule
that no longer looks, and the resulting green would carry no information.

## Data Modeling & Storage Strategy

Case tables are JSON and keep their current schemas; only their path owner
changes. Each move is a rename that Git records; no case table is rewritten in
the same commit that moves it, so a reviewer can read a pure rename.

`scripts/document-taxonomy-migration.json` is not a migration residue and does
not move to an archive. Three validators read it as an authority table —
`validate-links-and-owners.py`, `reference_information_architecture.py`, and
`validate-markdown-profiles.py`. `migrate-document-work-units.py` is likewise
referenced by `validate-links-and-owners.py` and `archive_validation.py`, so it
cannot be deleted as a completed one-off until those references are promoted to
`lib/`. Both are recorded here as refused deletion candidates with their reason.

## Interfaces & Data Structures

Every moved path changes three strings that must move together: the module's own
location, the `argv` of any validator that names it, and the runner text that
invokes it. `validate_required_validators_have_a_runner` compares the two latter
by substring, so a partial update fails loudly rather than silently — this is the
one existing rule that already survives the restructure correctly.

## Edge Cases & Error Handling

A reference inside a sealed Stage 98 migration record names a path as it existed
at a pinned commit. The corrected reference rule must not require such a path to
exist in the current tree; that is the exact defect Spec 0065 removed in four
owners, and reintroducing it here would undo that work.

A `.md` line that mentions a script inside a fenced historical transcript is a
record, not a live reference. The corrected rule resolves a moved path through
the sealed migration record rather than through a hard-coded redirect map, so
the map does not grow with each move.

## Failure Modes & Fallback / Human Escalation

If the corrected reference rule cannot be made to go red on the current tree,
the rule is not reaching its subject and the restructure stops: a green from a
rule that cannot fail is the condition this Spec exists to remove.

If a move requires editing `validation-surfaces.json`, the move is out of
contract. Stop, record the path that failed to route, and escalate.

Rollback is per commit. Each commit is one logical unit — one rule, one role
directory, or one module split — so any single step reverts without unwinding
the rest.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'
python3 scripts/select-affected-surfaces.py --root . --lane affected \
  --paths-file <paths> --delimiter nul --format json
```

These are repository-static. They do not prove native agent discovery, hook
delivery, authenticated provider runtime, CI, or live cluster readiness.

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-VTO-001 | The script-reference rule reaches every executable extension at every depth under `scripts/`, proven by a case that fails on the current tree before the fix |
| VAL-VTO-002 | `scripts/README.md` governs all forty-eight tracked files, and its consolidation criteria and deletion precheck name no single extension |
| VAL-VTO-003 | Every module sits in one role directory, and no `validation/` module imports another `validation/` module |
| VAL-VTO-004 | Case tables have one owner under `scripts/validation/cases/`, and no module under `scripts/` reads a path under `tests/` |
| VAL-VTO-005 | One module-loading convention holds across `scripts/`, and one across `tests/` |
| VAL-VTO-006 | No tracked file under `scripts/` or `tests/` exceeds the 800-line ceiling |
| VAL-VTO-007 | Every repository-internal commit pin is classified, and each retired pin is resolved through a sealed record while each kept pin names the record it belongs to |
| VAL-VTO-008 | The declared validator set and the executed runner set name each other exactly, and every CLI has a declared route or a recorded Tier C reason |
| VAL-VTO-009 | Surface selection is unchanged by the restructure, evidenced by identical validator sets before and after |
| VAL-VTO-010 | Gates and the full suite pass in a clean checkout at the branch tip |

## Traceability

This Spec has no PRD or AD. Its authority is the direct human approval recorded
in `## Overview`.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — standalone, direct approval | VAL-VTO-001 | RED-first case against the uncorrected rule, then its passing result |
| N/A — standalone, direct approval | VAL-VTO-002 | Tracked-file census compared against the count the document reasons over |
| N/A — standalone, direct approval | VAL-VTO-003 | Import census across `scripts/validation/` recorded in the Task |
| N/A — standalone, direct approval | VAL-VTO-004 | Grep for `tests/` inside `scripts/`, expected empty |
| N/A — standalone, direct approval | VAL-VTO-005 | Loader census before and after, recorded as counts per convention |
| N/A — standalone, direct approval | VAL-VTO-006 | Line-count census over tracked files |
| N/A — standalone, direct approval | VAL-VTO-007 | Pin classification table reviewed in the Task before any pin is retired |
| N/A — standalone, direct approval | VAL-VTO-008 | Declared `argv` set differenced against runner and hook invocations |
| N/A — standalone, direct approval | VAL-VTO-009 | `select-affected-surfaces.py` output compared before and after |
| N/A — standalone, direct approval | VAL-VTO-010 | Gate and suite output recorded in the reciprocal Task |

### Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-vto-000.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR 0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
