---
title: "Archive Record: Task: Affected Surface and Agent QA"
type: "content/archive"
status: "archived"
owner: "platform"
updated: "2026-07-18"
original_type: "task"
original_path: "docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md"
archived_on: "2026-07-18"
archive_reason: "completed-lineage"
replacement: null
source_commit: "a12aedfb71ccabd329dabc83bd2863474d1126b0"
source_blob: "7f8293bcd152aaaafcbeee15d4a77109c56e140a"
content_sha256: "fe8c79bc62deda32ff9f91a005f4aa879179fcc6548c57d43a351a424a507017"
---
<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->
---
title: 'Task: Affected Surface and Agent QA'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-14
---

# Task: Affected Surface and Agent QA

## Overview

This Task tracks six bounded changes that establish deterministic affected-path
validation and provider-neutral agent-role evidence. ASQA-001 starts reciprocal
Spec, Plan, Task, and Stage-index lineage. ASQA-002 through ASQA-006 then define
the surface registry, connect local and CI consumers, enforce ten-role semantics
across thirty tracked local/Claude/Codex adapters, and close the shared QA
handoff contract.

**2026-07-14 terminology correction:** ASQA-001 through ASQA-006 remain done,
and the recorded 480/33/20 results are unchanged. Current validation describes
thirty tracked role adapters across `local`, `claude`, and `codex` surfaces;
historical `three providers`, `native adapters`, and `cross-provider` wording
below is evidence terminology, not a Gemini CLI runtime claim.

**2026-07-14 path-input correction:** Validation-surface schema v2 propagates
existing affected Markdown to the exact three document validators, including
untracked edits. CI uses `git diff --no-renames --name-only -z`, and a fifth
range case plus a temporary Git rename proof ensure both sides of a protected-
to-document rename remain selected.

## Inputs

- **Parent Spec**: [Affected Surface and Agent QA Technical Specification](../../03.specs/031-affected-surface-agent-qa/spec.md)
- **Parent Plan**: [Affected Surface and Agent QA Implementation Plan](../plans/2026-07-12-affected-surface-agent-qa.md)
- **Document Validation Baseline**: Completed Specs 029 and 030 provide strict
  profile, index, link, and reciprocal execution-lineage validation.
- **Path Contract Baseline**: Spec 026 owns normalized repository-relative POSIX
  exact and anchored-regex route semantics.
- **Adapter Baseline**: The Stage 00 roster contains ten shared roles and thirty
  tracked adapters across `local`, `claude`, and `codex`; surface-specific
  model/tool metadata remains with its existing owner. Gemini CLI native
  `.gemini/**` remains absent/`DEFER`.

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| ASQA-001 | Start reciprocal Spec, Plan, Task, unique active Stage-index lineage, and strict durable-ledger coverage | platform | Done | GREEN lineage assertion, exact fourteen-column Task ledger row, focused strict document QA, and logical commit `0ab20d3 docs(execution): start affected surface agent qa` |
| ASQA-002 | Define the affected-surface registry, schema, selector, and positive/negative path fixtures | platform | Done | RED empty-selector exit `1`; GREEN 19/19 surface and 630 pre-stage/635 exact-index tracked-path coverage, 21 positive paths, 4 exact selection cases, 5 rejection cases, 4 post-script/`--` boundary positives, 29 route/argv/lane/job/protection/fallback/evidence mutations, exact executable tokens, direct-script/wrapper boundaries, fail-closed interpreter-eval options and surface fallbacks, NUL/output self-tests, Python compile, strict document QA, full quality gate, and focused pre-commit; logical commit `feat(qa): define affected-surface validation contract` |
| ASQA-003 | Drive local hooks and pre-commit lanes from validated selector output without newline path transport | platform | Done | Fixture-first RED/GREEN, 636-path tracked coverage, bounded/redacted shell-free runner evidence, three tracked-wiring payload/no-file/control-byte/root/symlink/alias simulations, zero pre-commit invocation on invalid input, shell/JSON/Python syntax checks, strict document QA, full quality gate, focused pre-commit, and exact thirteen-path staging; logical commit `refactor(hooks): drive local validation from affected surfaces` |
| ASQA-004 | Select existing CI jobs from NUL-delimited changed paths and preserve Spec 032 workflow ownership | platform | Done | Fixture-first RED/GREEN for four push/PR range cases, exact selector job/GitHub-output parity, initial/zero-before fail-safe, 636-path contract coverage, canonical quality-gate and Action-inventory alignment, actionlint and zizmor PASS, protected-job digest equality, and exact eight-path staging; logical commit `ci(qa): select jobs from affected-surface registry` |
| ASQA-005 | Enforce responsibility, output, prohibition, stop, handoff, capability-tier, and evidence semantics for ten roles and thirty adapters | platform | Done | Fixture-first RED exposed all eight unimplemented `ROLE-*` rules; GREEN validates 10 roles × 3 tracked surfaces × 8 categories × remove/replace = 480 source-to-parser exact-rule mutations, 33 malformed-YAML/non-operative-Markdown adversarial cases, and 20 shared-negation-vocabulary probes, all thirty local/Claude/Codex adapters, surface-metadata exclusion, metadata/import hash invariance, roster currentness, strict document QA, full quality gate, all-files pre-commit, and exact 37-path staging; logical commit `feat(agents): enforce cross-provider role semantics` |
| ASQA-006 | Align thin gateways, Stage 00 QA governance, repository gates, lifecycle, and independent-review evidence | platform | Done | Full repository-static QA bundle, exact twenty-five-path staging, explicit lane limitations, and independent reviewer agent `/root/review_adm006_adm007_conflict` disposition `APPROVED FOR LIFECYCLE CLOSURE (C0/H0/M0/L0)`; rollback unit is logical commit `docs(agents): align provider qa evidence contracts` |

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
use temporary NUL files; Claude settings, local/Antigravity
`.agents/hooks.json`, and Codex wiring retain their tracked JSON surface roles.
Payload paths containing C0/DEL bytes, boundary
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

ASQA-004 extended the fixture and its owning validator before changing the
workflow. The RED self-test failed with `SURFACE-LOCAL-CI-MISMATCH` because the
`changes` job still contained copied dorny filters and lacked canonical
selector wiring. GREEN covers ordinary push `before..head`, initial or
zero-`before` head-tree selection, and pull-request `base..head` cases. The
five cases compare both exact selected job IDs and the three sorted GitHub
boolean outputs while covering docs, `_workspace/README.md`, policy, GitOps,
infrastructure, secrets, Traefik, shared agents, templates, and workflow paths.
The workflow now writes `git diff --no-renames --name-only -z` output directly to the
runner-temporary NUL file and passes that file to the selector; no command
substitution or newline decoding is used. Initial pushes and unavailable push
base objects conservatively select the head tree, and manual dispatch selects
the head tree. The obsolete `dorny/paths-filter@v4.0.1` owner is removed; the
remaining `uses:` multiset and order, top-level permissions, branch-policy,
pre-commit, repo-quality-static, manifest-static, and ci-summary bodies have
matching pre/post SHA-256 digests. Self-test, 636-path contract validation,
actionlint, zizmor, strict document QA, full repository quality, focused
pre-commit, and diff checks pass. This is repository-static evidence only;
remote GitHub execution, provider runtime consumption, and live Kubernetes or
cloud state remain `DEFER`.

The first full quality-gate reproduction exposed two residual copied-filter
assertions and the obsolete dorny Action inventory row; its nested shared and
Codex hook simulations then failed only because their selected
`repository-quality` child correctly propagated that gate failure. ASQA-004
now runs the affected-surface self-test and root inventory at the quality-gate
entry point, checks the canonical changes-job outputs, full-history checkout,
NUL producers, selector invocation, and absence of dorny/filter ownership, and
removes exactly the obsolete current-inventory row. The existing Spec 032 Plan
is intentionally unchanged; any stale future-plan dorny wording remains a
Spec 032 handoff rather than active current inventory or ASQA-004 behavior.

Later rows retain their own fixture-first RED/GREEN evidence. ASQA-002 and
ASQA-003 reject unmatched or ambiguous paths and unsafe path transport;
ASQA-006 reports every lane as PASS, SKIP, FAIL, or DEFER and records
independent review before lifecycle closure.

ASQA-005 began with a validator shell that emitted the exact eight unimplemented
rule IDs and exited `1`. The completed provider-neutral JSON contract and schema
own responsibility, output, prohibited action, stop condition, handoff,
capability tier, and required evidence claims for the exact ten current roles;
they reject provider-owned `model`, `tools`, and `modelReasoningEffort` fields.
The production parser reads YAML frontmatter plus Markdown for local/Antigravity
and Claude and TOML `developer_instructions` for Codex, normalizing whitespace
only. Its fixture executes all 480 role/adapter/category/remove-or-replace
combinations against adapter source through the production YAML/TOML/Markdown parser and
requires each mutation to return exactly its distinct `ROLE-*` rule ID,
including current `ROLE-ADAPTER-STEM` failures. YAML duplicate keys, non-mapping metadata,
and non-scalar names fail closed. Thirty-three additional adversarial cases prove
that fenced, absolute/list-container-indented, and indented-tilde code, HTML
comments, strikethrough, blockquote/nested/lazy continuation, forward/backward
revocation, external negation, inline-code-only claims, and quoted/nested
headings cannot satisfy a semantic claim. Each category claim must equal a
complete normalized paragraph/list-item unit in its owning section. The smallest
surface-specific body changes add topic-specific stop, bounded capability, and
evidence claims while all owned metadata and scope-import hashes remain equal
to their pre-edit values. Focused
semantic and roster checks, strict document checks, the full repository quality
gate, all-files pre-commit, diff checks, and exact A4/M33 staging form the final
repo-static evidence; provider runtime consumption, remote CI, credentials,
secrets, and live Kubernetes or cloud state remain `DEFER`.

Forward, backward, and contextual negation share one ten-state vocabulary,
including `false`, `not true`, invalidation, revocation/retraction/supersession,
contradiction, non-operative status, and non-applicability. Twenty generated
source-to-parser probes exercise every state in both directions so the three
recognizers cannot drift independently.

### ASQA-006 Completion Handoff

ASQA-006, its Spec, Plan, and Task are complete. Independent reviewer agent
`/root/review_adm006_adm007_conflict` approved lifecycle closure with
`C0/H0/M0/L0`; the ignored review package is
`.superpowers/sdd/asqa006-provisional-review.md`.

- **Scope**: Stage 00 validation evidence governance, thin provider routing,
  repository quality orchestration, and reciprocal Spec/Plan/Task evidence.
- **Changed paths**: the exact twenty-five paths listed by Plan Task 6; no
  Spec 032-owned Action identity, workflow permission, or protected-domain file.
- **Acceptance IDs**: ASQA-006 and VAL-SPC-001 through VAL-SPC-005.
- **Commands and tool/version**: the exact ASQA-006 command block above ran
  with Python 3.12.3, GNU Bash 5.2.21, and pre-commit 4.5.1; strict registry,
  Markdown-profile, and cross-document commands also ran directly.
- **Lane results**: `affected` PASS (`640` tracked paths, `19/19` surfaces,
  zero uncovered/ambiguous); `all-files` PASS for every applicable pre-commit
  hook, with Dockerfile lint `SKIP` because no files matched; `staged` PASS on
  the exact twenty-five-path index (non-applicable file-type hooks reported
  `SKIP`); `message/manual` is `DEFER` because no commit message or explicit
  manual-stage invocation exists; local `ci`
  selection and static workflow checks PASS through repository quality, while
  remote CI and runtime-native `remote/live` evidence remain `DEFER`.
- **Limitations**: repo-static files do not prove native Claude/Codex adapter
  discovery/consumption or any Gemini CLI native implementation, remote GitHub execution, credentials,
  secrets, Kubernetes convergence, Argo CD, Vault, ESO, or cloud state. The
  first staged pre-commit launch could not create the linked-worktree Git index
  lock in the filesystem sandbox; the same command was rerun with the approved
  Git-index permission and passed.
- **Reviewer**: independent reviewer agent
  `/root/review_adm006_adm007_conflict`; disposition `APPROVED FOR LIFECYCLE
  CLOSURE (C0/H0/M0/L0)` with no protected-surface change finding.
- **Rollback**: revert the logical ASQA-006 commit
  `docs(agents): align provider qa evidence contracts` before any dependent
  Spec 032 work; the controller creates that commit from this exact staged unit.
- **Residual risk**: remote CI, provider runtime consumption, credentials,
  secrets, and live Kubernetes/Argo CD/Vault/ESO/cloud lanes remain `DEFER`.
- **Next owner**: Spec 032, [Protected Surface and Supply Chain
  Hardening](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md),
  for Action identity, permissions, and protected-domain repository-static
  hardening; remote/live owners remain separately approval-gated.

## Traceability

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Lineage ADR](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- [Affected Surface and Agent QA Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
- [Affected Surface and Agent QA Plan](../plans/2026-07-12-affected-surface-agent-qa.md)
- [Protected Surface and Supply Chain Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
