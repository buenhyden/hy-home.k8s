---
title: 'Task: Affected Surface and Agent QA'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-14
---

# Task: Affected Surface and Agent QA

## Overview

This Task tracks six bounded changes that establish deterministic affected-path
validation and provider-neutral agent-role evidence. ASQA-001 starts reciprocal
Spec, Plan, Task, and Stage-index lineage. ASQA-002 through ASQA-006 then define
the surface registry, connect local and CI consumers, enforce ten-role semantics
across thirty provider adapters, and close the shared QA handoff contract.

## Inputs

- **Parent Spec**: [Affected Surface and Agent QA Technical Specification](../../03.specs/031-affected-surface-agent-qa/spec.md)
- **Parent Plan**: [Affected Surface and Agent QA Implementation Plan](../plans/2026-07-12-affected-surface-agent-qa.md)
- **Document Validation Baseline**: Completed Specs 029 and 030 provide strict
  profile, index, link, and reciprocal execution-lineage validation.
- **Path Contract Baseline**: Spec 026 owns normalized repository-relative POSIX
  exact and anchored-regex route semantics.
- **Provider Baseline**: The Stage 00 roster contains ten shared roles and thirty
  Claude, Codex, and Gemini adapters; provider-native model and tool metadata
  remain with their existing owners.

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| ASQA-001 | Start reciprocal Spec, Plan, Task, unique active Stage-index lineage, and strict durable-ledger coverage | platform | Active | GREEN lineage assertion, exact fourteen-column Task ledger row, and focused strict document QA; logical commit `docs(execution): start affected surface agent qa` |
| ASQA-002 | Define the affected-surface registry, schema, selector, and positive/negative path fixtures | platform | Done | RED empty-selector exit `1`; GREEN 19/19 surface and 630 pre-stage/635 exact-index tracked-path coverage, 21 positive paths, 4 exact selection cases, 5 rejection cases, 4 post-script/`--` boundary positives, 29 route/argv/lane/job/protection/fallback/evidence mutations, exact executable tokens, direct-script/wrapper boundaries, fail-closed interpreter-eval options and surface fallbacks, NUL/output self-tests, Python compile, strict document QA, full quality gate, and focused pre-commit; logical commit `feat(qa): define affected-surface validation contract` |
| ASQA-003 | Drive local hooks and pre-commit lanes from validated selector output without newline path transport | platform | Done | Fixture-first RED/GREEN, 636-path tracked coverage, bounded/redacted shell-free runner evidence, three-provider hook payload/no-file/control-byte/root/symlink/alias simulations, zero pre-commit invocation on invalid input, shell/JSON/Python syntax checks, strict document QA, full quality gate, focused pre-commit, and exact thirteen-path staging; logical commit `refactor(hooks): drive local validation from affected surfaces` |
| ASQA-004 | Select existing CI jobs from NUL-delimited changed paths and preserve Spec 032 workflow ownership | platform | Draft | Local/CI parity fixtures, actionlint, and separately reported zizmor evidence; logical commit `ci(qa): select jobs from affected-surface registry` |
| ASQA-005 | Enforce responsibility, output, prohibition, stop, handoff, capability-tier, and evidence semantics for ten roles and thirty adapters | platform | Draft | Semantic mutation self-tests and roster-currentness checks; logical commit `feat(agents): enforce cross-provider role semantics` |
| ASQA-006 | Align thin gateways, Stage 00 QA governance, repository gates, lifecycle, and independent-review evidence | platform | Draft | Full static QA bundle with lane limitations and reviewer findings; logical commit `docs(agents): align provider qa evidence contracts` |

The exact validation commands for each logical unit are:

**ASQA-001**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [Path('docs/03.specs/031-affected-surface-agent-qa/spec.md'), Path('docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md'), Path('docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md')]
for source in paths:
    text = source.read_text(encoding='utf-8')
    assert source.exists()
    for target in paths:
        if target != source:
            assert target.name in text
PY
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
git diff --check
pre-commit run --files docs/03.specs/031-affected-surface-agent-qa/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md docs/04.execution/tasks/README.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
python3 - <<'PY'
import subprocess
expected = {
    'docs/03.specs/031-affected-surface-agent-qa/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md',
    'docs/04.execution/tasks/README.md',
    'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
}
staged = {
    item.decode()
    for item in subprocess.check_output(
        ['git', 'diff', '--cached', '--name-only', '-z']
    ).split(b'\0')
    if item
}
unstaged = subprocess.check_output(['git', 'diff', '--name-only', '-z'])
assert staged == expected, (sorted(staged), sorted(expected))
assert unstaged == b'', unstaged
PY
```

**ASQA-002**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 -m py_compile scripts/validate-affected-surfaces.py scripts/select-affected-surfaces.py
```

**ASQA-003**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 -m py_compile scripts/run-validation-lane.py
bash -n docs/00.agent-governance/hooks/*.sh
python3 -m json.tool .claude/settings.json >/dev/null
python3 -m json.tool .agents/hooks.json >/dev/null
python3 -m json.tool .codex/hooks.json >/dev/null
pre-commit run validate-affected-surfaces --all-files
```

**ASQA-004**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
pre-commit run actionlint --files .github/workflows/ci.yml
pre-commit run zizmor --files .github/workflows/ci.yml
```

**ASQA-005**

```bash
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
```

**ASQA-006**

```bash
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --all-files
```

## Approval and Safety Boundaries

- **Allowed Paths**: ASQA-001 is limited to this Task, its parent Spec and Plan,
  their three Stage indexes, and the new Task's single row in the durable
  migration ledger: exactly seven paths. Later units may change only the exact paths in
  their parent Plan `Files` lists: the Stage 00 surface and role contracts,
  selector/runner/validator scripts and fixtures, shared hooks and provider hook
  configurations, pre-commit, the existing CI workflow's selection boundary,
  thirty role adapters, thin provider gateways, QA governance, inventories,
  execution evidence, and the canonical progress ledger.
- **Forbidden Paths**: Spec 032-owned Action identities, workflow or job
  permissions, manifest-static and protected-domain behavior; provider model,
  reasoning-effort, or native tool metadata; ignored `_workspace/**` children;
  credentials, authentication state, secrets, generated local output, and any
  path outside the active Plan unit are excluded.
- **Approval Required**: Human approval is required before workflow merge,
  protected-role behavior changes, new tool permissions, model promotion,
  remote push or merge, publication, credential access, or live mutation.
- **Static Validation**: Run the exact command block for the active ASQA row,
  its RED fixture first where specified by the Plan, `git diff --check`, focused
  pre-commit, exact staged-path proof, and independent review for protected
  changes. A no-file lane is `SKIP`, not `PASS`.
- **Live Validation**: DEFER. Repository-static selectors, fixtures, adapter
  bodies, and workflow syntax do not prove provider discovery, remote CI,
  Kubernetes convergence, or cloud availability.
- **Secret / Vault Handling**: Do not read, print, enumerate, move, or modify
  secret values, tokens, certificates, kubeconfigs, Vault data, provider auth
  files, shell history, or ignored local state.
- **Rollback Plan**: Revert completed ASQA logical commits newest-first.
  Selector, consumer, adapter, and governance evidence stay in their owning
  commit so no consumer remains after its contract is reverted.
- **Evidence Location**: This Task, its parent Plan, the durable migration
  ledger, logical commits, the canonical progress ledger after ASQA-006, and ignored
  `.superpowers/sdd/asqa*-report.md` review packages.
- **GitOps Impact**: None. ASQA-004 changes job selection only and ASQA-006 does
  not alter desired state or protected-domain commands.
- **Kubernetes Impact**: None. No live cluster command is authorized.
- **Operations / Runbook Impact**: None. This tranche changes validation and
  agent-QA contracts rather than operational procedures.

## Verification Summary

ASQA-001 began from the expected RED state on 2026-07-14: the canonical Task
path did not exist, so the three-document lineage assertion exited 1 before it
could inspect reciprocal links. GREEN requires all three documents to name one
another, one active index row per document, exactly six ASQA rows, strict
registry/Markdown/link checks, `git diff --check`, focused pre-commit, and an
exact seven-path staged set (six execution-lineage documents plus the Task's
single durable-ledger row) with no unstaged tracked changes. This evidence is
repository-static and does not prove manual or commit-message hook stages,
remote CI, provider runtime consumption, secrets, or live infrastructure.

ASQA-002 began with the fixture, schema, and an intentionally empty selector;
the self-test printed `affected-surface selector is not implemented` and exited
`1`. GREEN validates 19 disjoint surfaces, ten shell-free argv validators, and
three selectable CI jobs. It classifies all 630 tracked paths with zero
uncovered or ambiguous paths before staging and 635 after the exact nine-path
index was assembled; exercises 21 requested-root paths,
four exact selection sets, five normalization/case/symlink/unmatched rejections,
four post-script/`--` boundary positives, and twenty-nine route/argv/lane/job/
protection/fallback/evidence mutations, including minimal, combined, and long
assignment shell/Python/Node interpreter evaluation, wrapper/option-before-
script rejection, executable path-prefix/case-alias rejection, and a
non-optional surface `SKIP`; and preserves
newline data inside NUL-delimited records.
JSON keys/sets and GitHub output booleans are sorted and stable. This is
repository-static evidence only: local hook consumption begins in ASQA-003 and
CI workflow consumption begins in ASQA-004, while remote CI and live systems
remain DEFER.

ASQA-003 added five hook-consumer selection cases. Its RED run intentionally
expected the no-file case to retain `review`; production selection returned
`none` and failed with `SURFACE-SELF-TEST`. GREEN pins the corrected empty
selection plus `_workspace/README.md`, `.gitignore`, policy, and shared-agent
paths. The local runner imports the validated contract, invokes approved argv
arrays with `shell=False`, and emits deterministic command/tool/scope/
limitation/evidence fields. Shared hooks preserve provider payload extraction,
protected-domain warnings, formatting, lifecycle advisory/block semantics, and
use temporary NUL files; Claude, Gemini, and Codex wiring remains native to its
existing JSON surface. Payload paths containing C0/DEL bytes, boundary
whitespace, non-normalized or external paths, or any symlink component fail
before a formatter or pre-commit command is invoked. Present scalar path aliases
must each be non-empty strings and cannot shadow each other; the sole present
`files`/`paths` alias must be a list containing only non-empty path strings,
while an explicit empty list preserves no-files `SKIP`. The lifecycle hook does
not extract payload paths; it constructs its changed-path input directly from
NUL-delimited Git inventory. Runner child stdout/stderr is represented only by
bounded byte-count and SHA-256 metadata, never copied verbatim. No-path and
unavailable optional tools are `SKIP`, the
optional fallback is a separate record, and remote/live work is always
`DEFER`. These outcomes are repository-static and do not prove provider event
delivery, remote CI, Kubernetes convergence, or cloud state.

Later rows retain their own fixture-first RED/GREEN evidence. ASQA-002 and
ASQA-003 must reject unmatched or ambiguous paths and unsafe path transport;
ASQA-004 must prove local/CI selection parity without changing Spec 032-owned
workflow controls; ASQA-005 must fail independently for each semantic category
and provider form; ASQA-006 must report every lane as PASS, SKIP, FAIL, or DEFER
and record independent review before lifecycle closure.

## Traceability

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Lineage ADR](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Affected Surface and Agent QA Plan](../plans/2026-07-12-affected-surface-agent-qa.md)
- [Protected Surface and Supply Chain Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
