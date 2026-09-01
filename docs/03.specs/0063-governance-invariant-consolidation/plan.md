---
title: 'Governance Invariant Consolidation Implementation Plan'
version: "1.0"
type: sdlc/plan
layer: "03.specs"
status: done
owner: platform
updated: 2026-08-30
artifact_id: "SPEC-0063-PLAN-0001"
---

# Governance Invariant Consolidation Implementation Plan (Plan)

## Overview

This plan sequences the consolidation designed in
[Spec 0063](spec.md). The order is set by dependency, not by the order the
constraints were stated: the machinery that pins the archived copies is retired
before the copies are deleted, because deleting them first would fail the
validators still holding those pins.

## Context

Measured baseline on 2026-08-29, in a clean `main` checkout:

| Measure | Value |
| --- | --- |
| Markdown under `docs/` | 796 |
| `scripts/` lines | 68,282 |
| `tests/` lines | 35,464 |
| Distinct 40-hex pins in `scripts/` | 253 across 18 files |
| Constants bound to completed migrations | 141, of which 49 are pins |
| Rule identifiers in the retirement candidates | 376 |
| Retirement-candidate validator lines | 13,631 |
| Corresponding test lines | 9,795 |
| Full-body copies under `docs/98.archive/changes/` | 76 (1.4 MB) |
| Validators declared in the contract but not run by the gate | 2 |
| Validators run by the gate but not declared | 11 |

## Goals & In-Scope

Retire completed-migration machinery, relocate the current invariants inside it,
execute the ADR-0030 Stage 98 boundary, unify the contract and the gate, and
correct the authored documents the diagnosis proves stale.

## Non-Goals & Out-of-Scope

No reduction of invariants over the current tree. No change to completed Spec,
Plan, or Task records, dated research and audit snapshots, or pinned evidence
ledgers. No amendment of ADR-0030.

## Work Breakdown

Every task ends with gates and the suite green in a clean checkout. Freeze
source files for the duration of a suite run: the archive owner loads its
sibling link validator from disk at call time, so a mid-run edit pairs a new
file against an already-imported module and produces import errors that are not
regressions.

Baseline command, referred to below as **the full check**:

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-agent-governance-closure.py --root .
python3 -m unittest discover -s tests
```

### WP-001 — Diagnosis

Produces the finding table. No source change.

- [ ] Record the contract-versus-gate divergence in both directions.

```bash
python3 - <<'EOF'
import json, re
from pathlib import Path
d = json.loads(Path("docs/00.agent-governance/contracts/validation-surfaces.json").read_text())
gate = Path("scripts/validate-repo-quality-gates.sh").read_text()
declared = {}
for v in d["validators"]:
    script = next((a for a in v.get("argv", []) if a.startswith(("scripts/", "infrastructure/"))), None)
    declared[v["id"]] = script
print("declared but not run:", sorted(i for i, s in declared.items() if s and s not in gate))
runs = set(re.findall(r"scripts/(?:validate|check)[a-z-]*\.(?:py|sh)", gate))
print("run but not declared:", sorted(r for r in runs if r not in set(filter(None, declared.values()))))
EOF
```

Expected on the 2026-08-29 baseline: two declared and not run
(`agent-governance-closure`, `document-lifecycle`), eleven run and not declared.

- [ ] Record every repository path named inside governance JSON that does not exist.

```bash
python3 - <<'EOF'
import re
from pathlib import Path
root = Path(".")
pat = re.compile(r"(?:docs|scripts|tests|gitops|infrastructure|\.agents|\.claude|\.codex|\.github)/[A-Za-z0-9_./-]+")
for p in sorted(Path("docs").rglob("*.json")):
    if "98.archive" in p.parts:
        continue
    for m in sorted(set(pat.findall(p.read_text(encoding="utf-8")))):
        if m.endswith((".md", ".py", ".sh", ".json", ".yaml", ".yml")) and not (root / m).exists():
            print(p, "->", m)
EOF
```

Verify each hit by hand before recording it: a match starting mid-path is a
false positive, as `tests/verify-contracts-static.sh` was for
`infrastructure/tests/verify-contracts-static.sh`.

- [ ] Record prose enumerations that disagree with the machine declaration.

```bash
python3 - <<'EOF'
import re
from pathlib import Path
text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
body = text[re.search(r"^jobs:\s*$", text, re.M).end():]
print("real jobs:", re.findall(r"^  ([a-zA-Z0-9_-]+):\s*$", body, re.M))
EOF
grep -rn "검사 job\|정적 게이트" docs/05.operations --include="*.md"
```

- [ ] Record documents naming surfaces ADR-0030 removed, and separate those that
      already carry a non-authoritative disclaimer.

```bash
grep -rniIl "gemini\|antigravity" docs/00.agent-governance docs/01.requirements \
  docs/02.architecture/descriptions docs/05.operations --include="*.md"
grep -n "non-authoritative" docs/01.requirements/0003-workspace-agent-governance-platform.md \
  docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md
```

A document carrying the disclaimer is a preserved record with removal deferred
to WP-003 of Spec 0054. Its verdict is preserve, not correct.

- [ ] Record every fact owned in more than one place, with both owners named.
      Known instances: `updated:` in frontmatter and in the stage README index
      row; the executed validator set in the gate script and in the contract.

- [ ] Write the findings into the Task record as a table of document, claim,
      machine fact, verdict, and disposition. Verdicts are correct, archive, or
      preserve.

- [ ] Commit.

```bash
git add docs/03.specs/0063-governance-invariant-consolidation/tasks/tsk-0001-gic-000.md
git commit -m "docs(spec): record the WP-001 governance diagnosis"
```

### WP-002 — Discard list and approval gate

Produces the classified rule list. No source change. **WP-003 does not start
until this list is approved and the approval is recorded in the Task.**

- [ ] Enumerate the rule identifiers in the retirement candidates.

```bash
grep -ohE '"[A-Z][A-Z0-9]+(-[A-Z0-9]+)+"' \
  scripts/validate-active-corpus-*.py scripts/validate-agent-legacy-cutover.py \
  scripts/archive_cutover.py | sort -u > /tmp/gic-rules.txt
wc -l /tmp/gic-rules.txt
```

Expected on the baseline: 376.

- [ ] Classify each rule by the mechanical test: a rule reading a hardcoded
      commit, blob, or digest constant, or reading a fixed past commit through
      Git, is a completed-migration proof. A rule reading only the working tree,
      index, `HEAD`, or a current contract is a current invariant.

```bash
for f in scripts/validate-active-corpus-*.py scripts/validate-agent-legacy-cutover.py; do
  echo "== $f"
  grep -nE "[0-9a-f]{40}|[0-9a-f]{64}|ls-tree|cat-file|rev-parse" "$f" | head -20
done
```

- [ ] Narrow the candidates by coverage. For each candidate validator, remove
      its two gate lines, run the suite, and record which tests fail. A
      validator whose removal fails no test is already dead.

```bash
cp scripts/validate-repo-quality-gates.sh /tmp/gic-gate-backup.sh
grep -v "validate-active-corpus-eligibility.py" scripts/validate-repo-quality-gates.sh \
  > /tmp/gate-probe.sh && mv /tmp/gate-probe.sh scripts/validate-repo-quality-gates.sh
python3 -m unittest discover -s tests 2>&1 | tail -20
cp /tmp/gic-gate-backup.sh scripts/validate-repo-quality-gates.sh
```

Repeat per candidate. Restore the backup after every probe; do not commit a
probe.

- [ ] For every rule proposed to stay, write one line naming the failure it
      prevents. A rule with no such line moves to the retirement column.

- [ ] Record the classified list in the Task and request approval. Stop here.

- [ ] Commit.

```bash
git add docs/03.specs/0063-governance-invariant-consolidation/tasks/tsk-0001-gic-000.md
git commit -m "docs(spec): record the WP-002 discard list for approval"
```

### WP-003 — Retirement

One commit per validator. Relocate retained rules **before** deleting their
host. Order runs from fewest dependents to most: eligibility, retention,
migrations, role audit, residue closure.

For each validator, in order:

- [ ] Move every rule the discard list marks as a current invariant into its new
      standing host, with its tests, as its own commit. Run the full check.

- [ ] Delete the validator, its test module, and its two gate lines.

```bash
git rm scripts/validate-active-corpus-eligibility.py tests/test_active_corpus_eligibility.py
python3 - <<'EOF'
from pathlib import Path
p = Path("scripts/validate-repo-quality-gates.sh")
lines = [l for l in p.read_text(encoding="utf-8").splitlines(keepends=True)
         if "validate-active-corpus-eligibility.py" not in l]
p.write_text("".join(lines), encoding="utf-8")
EOF
```

- [ ] Remove the constants the deleted validator alone owned.

```bash
grep -rn "WORK105_\|WP004\|CUTOVER_BASE_COMMIT" scripts/*.py | grep -v "^scripts/archive_" | head
```

- [ ] Run the full check. Expected: gates exit 0, suite OK.

- [ ] Commit, naming the retired rule identifiers in the body.

```bash
git add -A
git commit -m "refactor(validation): retire the active-corpus eligibility proof

Retires <rule ids>. The proof read a fixed base commit, so it could only
break as history advanced past it. <n> current invariants moved to <host>
in the preceding commit."
```

Then reduce `scripts/validate-agent-legacy-cutover.py` to its retained rules.
Keep `retired_document_owner` and its `HOOK-DOC-RETIRED` rejection: it maps
retired document forms to their successor profile, and holding zero live
targets is its success condition. Keep its contract wiring intact.

### WP-004 — Stage 98 execution

- [ ] Confirm every archived copy still carries recovery coordinates.

```bash
python3 - <<'EOF'
import json, re, glob
ok = bad = 0
for f in glob.glob("docs/98.archive/migrations/*.md"):
    for m in re.finditer(r"```json\n(\[.*?\])\n```", open(f).read(), re.S):
        try:
            rows = json.loads(m.group(1))
        except Exception:
            continue
        for r in rows:
            if isinstance(r, dict) and isinstance(r.get("stable_path"), str) and "98.archive/changes/" in r["stable_path"]:
                ok += bool(r.get("source_commit") and r.get("source_blob"))
                bad += not (r.get("source_commit") and r.get("source_blob"))
print("with coordinates:", ok, "without:", bad)
EOF
```

Expected: 76 with coordinates, 0 without. **If any row lacks coordinates, stop
and resolve it before deleting anything.**

- [ ] Delete the copies and null their `stable_path`, keeping `legacy_path`,
      `source_commit`, and `source_blob`.

```bash
git rm -r docs/98.archive/changes
```

- [ ] Create a Tombstone only where a deleted stable path needs a durable
      replacement owner. ADR-0030 forbids one Tombstone per source where a
      Migration and Git recovery suffice.

- [ ] Run the full check, then commit.

```bash
git add -A
git commit -m "docs(archive): execute the ADR-0030 Stage 98 boundary

Removes 76 full-body copies. Every ledger row keeps legacy_path,
source_commit, and source_blob, so Git remains the full-content archive."
```

### WP-005 — Contract and gate unification

- [ ] Write the failing test asserting the executed set equals the declared set.
      Add it to `tests/test_validate_agent_governance_ci.py`, which already reads
      `validation-surfaces.json`, rather than creating a new module.

```python
def test_gate_runs_exactly_the_declared_validators(self) -> None:
    contract = json.loads(
        (ROOT / "docs/00.agent-governance/contracts/validation-surfaces.json").read_text()
    )
    gate = (ROOT / "scripts/validate-repo-quality-gates.sh").read_text()
    declared = {
        script
        for validator in contract["validators"]
        for script in validator["argv"]
        if script.startswith(("scripts/", "infrastructure/"))
    }
    executed = set(re.findall(r"(?:scripts|infrastructure)/[a-z0-9/._-]+\.(?:py|sh)", gate))
    executed.discard("scripts/validate-repo-quality-gates.sh")
    self.assertEqual(executed, declared)
```

- [ ] Run it. Expected: FAIL, listing the two declared-and-unrun and the
      remaining run-and-undeclared entries.

```bash
python3 -m unittest tests.test_validate_agent_governance_ci.AgentGovernanceCiArtifactTests.test_gate_runs_exactly_the_declared_validators -v
```

- [ ] Declare the validators the gate runs but the contract omits, and add the
      two declared validators the gate omits to the gate.

- [ ] Run the test. Expected: PASS.

- [ ] Run the full check, then commit.

```bash
git add -A
git commit -m "feat(validation): make the contract the single owner of the gate set

The gate script and the contract each held a partial list, diverging in both
directions. The declared set is now the only owner and a test asserts the
executed set equals it."
```

### WP-006 — Document and template correction

- [ ] Apply each WP-001 disposition. Correct where the claim contradicts a
      machine fact; leave preserved records alone; archive only what ADR-0030
      admits.

- [ ] When a document's `updated:` changes, change the matching stage README
      index row in the same commit. The date is owned in both places and the
      gate compares them.

- [ ] Re-run WP-001's diagnosis commands. Expected: no findings remain except
      those recorded as preserved.

- [ ] Run the full check, then commit.

## Verification Plan

After every commit, in a clean checkout, not a linked worktree:

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-agent-governance-closure.py --root .
python3 -m unittest discover -s tests
```

Source files are frozen for the duration of a suite run. The archive owner
loads its sibling link validator from disk at call time, so editing a validator
mid-run pairs a new file against an already-imported module and produces
import errors that are not regressions.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A retirement removes a current invariant | WP-002 approval gate; one commit per retirement; single-commit revert |
| A deletion loses content | All 76 rows carry `source_commit` and `source_blob`; Git holds the bodies |
| A worktree masks a filesystem check | Verify in a clean checkout only |
| Editing a byte-pinned consumer | Identify pinned paths before editing; move the pin or leave the file alone |
| Verification cost | One gate-and-suite pass takes about 20 minutes; batching per commit is cheaper than reverting a batch |

## Completion Criteria

The Spec criteria VAL-GIC-001 through VAL-GIC-006 hold, and the final commit
passes gates and the full suite in a clean checkout.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-GIC-001](spec.md#success-criteria--verification-plan) | WP-001 diagnosis | [SPEC-0063-TSK-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-002](spec.md#success-criteria--verification-plan) | WP-002 discard list | [SPEC-0063-TSK-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-003](spec.md#success-criteria--verification-plan) | WP-003 retirement | [SPEC-0063-TSK-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-004](spec.md#success-criteria--verification-plan) | WP-004 Stage 98 execution | [SPEC-0063-TSK-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-005](spec.md#success-criteria--verification-plan) | WP-005 contract unification | [SPEC-0063-TSK-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-006](spec.md#success-criteria--verification-plan) | WP-006 document correction | [SPEC-0063-TSK-0001](tasks/tsk-0001-gic-000.md) |

### Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-gic-000.md)
