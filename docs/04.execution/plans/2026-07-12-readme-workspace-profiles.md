---
title: 'README and Workspace Profiles Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-12
---

# README and Workspace Profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the monolithic README form with six path-derived profiles,
migrate all 67 baseline README files, create five cloud handoff READMEs, and
preserve `_workspace` as temporary non-secret repository-support staging.

**Architecture:** The document registry maps each README path to exactly one
profile and template without frontmatter or hidden markers. Profile-specific
forms define entrypoint responsibilities; a complete 72-path fixture records
route and heading outcomes for Spec 029, while this tranche uses focused
migration assertions rather than creating the production Markdown parser.

**Tech Stack:** Frontmatter-free Markdown, JSON registry/fixtures, Python 3,
Bash, Git, `rg`, `pre-commit`, and repository quality gates.

## Global Constraints

- Specs 026 and 027 must be done before this Plan starts.
- Preserve exactly 67 baseline README dispositions and report the final count separately after adding five handoff READMEs.
- README files remain frontmatter-free and contain exactly one H1.
- Infer profiles from paths; do not add frontmatter, body markers, or first-match route precedence.
- README files are entrypoints and inventories, not lifecycle, schema, policy, contract, or validation owners.
- Use topic-specific content; do not copy template instructions or placeholder bodies into authored READMEs.
- Keep README language appropriate to its readers while using the exact English structural H2 names declared here.
- Create exactly five cloud handoff READMEs: `docs/90.references/cloud-examples/{README.md,aws/README.md,azure/README.md}` and `examples/{aws,azure}/README.md`.
- Do not relocate or delete cloud authored documents in this tranche; Spec 030 owns relocation.
- Never enumerate, read, move, or delete ignored `.env`, token, key, certificate, kubeconfig, shell-history, local-setting, or diagnostic content.
- `_workspace` tracks only `_workspace/README.md`; all scratch children remain ignored, temporary, non-secret, and unforced.
- Keep profile headings closed; an optional heading is valid only when declared in the registry.
- Hand all fence-aware positive/negative cases to Spec 029; do not create its production parser here.
- Use `apply_patch` for content edits; do not push, publish, or mutate live systems.

---

## Overview

This plan implements Spec 028 in six logical commits: execution lineage,
profile forms and inventory fixture, stage/collection migration, snapshot and
cloud handoff migration, implementation/workspace migration, and closure.

## Context

The current `readme.template.md` is a 377-line snippet library with universal
sections and unrelated optional content. The current gate requires the same
seven headings in every README, so repositories, stage indexes, snapshot packs,
implementation entrypoints, and `_workspace` cannot express distinct jobs.

## Goals & In-Scope

- Create six minimal README forms and exact registry heading profiles.
- Classify and migrate every baseline README without ambiguity.
- Create the five cloud handoff entrypoints required before Spec 030 relocation.
- Delete the monolithic snippet library and active references to it.
- Provide complete fixture expectations for Spec 029 production enforcement.
- Preserve the `_workspace` tracked/ignored and secret-safe boundary.

## Non-Goals & Out-of-Scope

- Relocating AWS/Azure authored documents.
- Rewriting non-README authored documents.
- Implementing the durable CommonMark parser.
- Changing provider-native or GitHub-native control Markdown.

## File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Profile forms | Six `docs/99.templates/templates/common/readme-*.template.md` files | Provide minimal path-specific starter structures. |
| Retired form | `docs/99.templates/templates/common/readme.template.md` | Delete after all routes, references, and bodies migrate. |
| Profile registry | `docs/99.templates/support/document-profiles.json` | Own exact path-to-profile/template and H2 requirements. |
| Fixture handoff | `tests/fixtures/document-contracts/readme-profile-cases.json` | Record all final paths and fence-aware positive/negative expectations for Spec 029. |
| Current compatibility gate | `scripts/validate-repo-quality-gates.sh` | Stop enforcing universal seven headings and consume finite migration expectations until Spec 029 replaces it. |
| Baseline README corpus | The 67 paths listed below | Migrate topic-specific entrypoints to one profile each. |
| Cloud handoff | Five new README paths | Route example assets and dated provider snapshots before Spec 030 moves content. |
| Workspace contract | `_workspace/README.md`, `.gitignore` | Preserve one tracked README and ignored non-secret scratch children. |
| Execution evidence | Spec 028, this Plan, same-topic Task, indexes | Maintain reciprocal lineage and validation evidence. |

### Profile heading interfaces

| Profile | Required H2 sequence | Allowed additional H2 |
| --- | --- | --- |
| `readme/repository` | `Overview`, `Repository Map`, `Getting Started`, `Validation`, `Related Documents` | `Prerequisites`, `Configuration`, `Security Boundary` |
| `readme/stage-index` | `Overview`, `Stage Contract`, `Document Index`, `Authoring Workflow`, `Related Documents` | `Lifecycle Handoff` |
| `readme/collection-index` | `Overview`, `Scope`, `Item Index`, `Add and Find`, `Related Documents` | `Selection Rules` |
| `readme/implementation` | `Overview`, `Structure`, `Configuration Boundary`, `Validation`, `Operations`, `Related Documents` | `Prerequisites`, `Troubleshooting` |
| `readme/snapshot-pack` | `Overview`, `Snapshot Contract`, `Report Index`, `Refresh and Succession`, `Evidence Boundary`, `Related Documents` | `Method` |
| `readme/workspace-staging` | `Overview`, `Permitted Artifacts`, `Forbidden Local State`, `Promotion and Cleanup`, `Tracking Rules`, `Related Documents` | none |

The registry and fixture `allowedH2` array for each profile is the ordered
concatenation of its required H2 sequence and the additional H2 values in the
last column, with no duplicates. The additional column is not a standalone
allow-list: every required heading must also be allowed and must never be
reported as unsupported.

### Complete baseline and final profile map

`readme/repository` (1 baseline):

```text
README.md
```

`readme/stage-index` (10 baseline):

```text
docs/README.md
docs/00.agent-governance/README.md
docs/01.requirements/README.md
docs/02.architecture/README.md
docs/03.specs/README.md
docs/04.execution/README.md
docs/05.operations/README.md
docs/90.references/README.md
docs/98.archive/README.md
docs/99.templates/README.md
```

`readme/collection-index` (16 baseline plus one new):

```text
docs/00.agent-governance/memory/README.md
docs/02.architecture/decisions/README.md
docs/02.architecture/requirements/README.md
docs/04.execution/plans/README.md
docs/04.execution/tasks/README.md
docs/05.operations/guides/README.md
docs/05.operations/incidents/README.md
docs/05.operations/policies/README.md
docs/05.operations/runbooks/README.md
docs/90.references/audits/README.md
docs/90.references/data/README.md
docs/90.references/learning/README.md
docs/90.references/llm-wiki/README.md
docs/90.references/research/README.md
docs/99.templates/support/README.md
docs/99.templates/templates/README.md
docs/90.references/cloud-examples/README.md
```

`readme/snapshot-pack` (28 baseline plus two new):

```text
docs/90.references/audits/2026-05-24-whga/README.md
docs/90.references/audits/2026-07-02-whia/README.md
docs/90.references/audits/2026-07-03-wdgh/README.md
docs/90.references/audits/2026-07-04-wdcn/README.md
docs/90.references/audits/2026-07-05-wea/README.md
docs/90.references/audits/2026-07-11-weia/README.md
docs/90.references/research/2026-07-04-wer/README.md
docs/90.references/research/2026-07-07-wer/README.md
examples/aws/docs/README.md
examples/aws/docs/01.requirements/README.md
examples/aws/docs/02.architecture/decisions/README.md
examples/aws/docs/02.architecture/requirements/README.md
examples/aws/docs/03.specs/README.md
examples/aws/docs/04.execution/plans/README.md
examples/aws/docs/04.execution/tasks/README.md
examples/aws/docs/05.operations/guides/README.md
examples/aws/docs/05.operations/policies/README.md
examples/aws/docs/05.operations/runbooks/README.md
examples/azure/docs/README.md
examples/azure/docs/01.requirements/README.md
examples/azure/docs/02.architecture/decisions/README.md
examples/azure/docs/02.architecture/requirements/README.md
examples/azure/docs/03.specs/README.md
examples/azure/docs/04.execution/plans/README.md
examples/azure/docs/04.execution/tasks/README.md
examples/azure/docs/05.operations/guides/README.md
examples/azure/docs/05.operations/policies/README.md
examples/azure/docs/05.operations/runbooks/README.md
docs/90.references/cloud-examples/aws/README.md
docs/90.references/cloud-examples/azure/README.md
```

`readme/implementation` (11 baseline plus two new):

```text
examples/README.md
examples/sample-app/README.md
gitops/README.md
gitops/workloads/README.md
infrastructure/README.md
scripts/README.md
tests/README.md
traefik/README.md
examples/azure/gitops/README.md
examples/azure/infrastructure/README.md
examples/azure/kubernetes/README.md
examples/aws/README.md
examples/azure/README.md
```

`readme/workspace-staging` (1 baseline):

```text
_workspace/README.md
```

Baseline total is `1 + 10 + 16 + 28 + 11 + 1 = 67`. Final total is
`67 + 1 collection handoff + 2 snapshot handoffs + 2 implementation handoffs = 72`.

## Work Breakdown

| Task | Description | Primary validation | Commit |
| --- | --- | --- | --- |
| RWP-001 | Start reciprocal execution lineage | Six links and index rows | `docs(execution): start readme profile tranche` |
| RWP-002 | Create six forms, routes, and complete fixture | 67 baseline and 72 final dispositions | `feat(templates): define readme profiles` |
| RWP-003 | Migrate repository, stage, and collection entrypoints | 27 baseline plus cloud collection handoff | `docs(readme): migrate repository and index profiles` |
| RWP-004 | Migrate snapshot packs and create provider snapshot handoffs | 28 baseline plus two provider indexes | `docs(readme): migrate snapshot pack profiles` |
| RWP-005 | Migrate implementation/workspace entrypoints and create example handoffs | 12 baseline plus two provider entrypoints | `docs(readme): migrate implementation and workspace profiles` |
| RWP-006 | Delete monolith, verify handoff fixtures, and close | 72 exact routes, zero universal markers | `docs(readme): close profile migration evidence` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-PLN-001 | Classification | `python3 scripts/validate-document-contract-registry.py --root . --mode compatibility --profile readme` | README baseline=67, declared final=72, current tracked progression=67 -> 68 -> 70 -> 72, uncovered=0, and ambiguous=0. |
| VAL-PLN-002 | Migration | Focused Python assertion in Task 6 | One H1, profile H2 set, no frontmatter/duplicates/snippet residue. |
| VAL-PLN-003 | Workspace | `git ls-files _workspace` plus ignore checks | Only README tracked; representative scratch ignored. |
| VAL-PLN-004 | Repository | Quality gate and all-files pre-commit | All applicable checks pass. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| README loses component-specific operational matrices | High | Profile headings are structural minima; retain unique content under declared allowed sections or canonical child links. |
| Cloud handoff implies relocation is complete | High | State current path, future Spec 030 destination, snapshot authority boundary, and no live/provider-latest claim. |
| Temporary heading assertion diverges from Spec 029 | Medium | Store expected cases once in JSON and require Spec 029 to consume the same fixture. |
| `_workspace` cleanup touches private ignored data | Critical | Validate tracking/ignore rules only; never list or open ignored children. |
| 72-file migration hides broken links | High | Commit by profile group and run link/quality checks after every group. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate:** Every profile group passes exact route, H1/H2, frontmatter-ban, and link assertions.
- **Sandbox / Canary Rollout:** Migrate one profile group per commit while compatibility mode remains active.
- **Human Approval Gate:** Required for a seventh profile, new durable `_workspace` content, remote publication, or live mutation.
- **Rollback Trigger:** Missing unique README content, broken links, route ambiguity, final count other than 72, or ignored-state access.
- **Prompt / Model Promotion Criteria:** Not applicable.

---

### Task 1: Start the Canonical Execution Chain

**Files:**

- Modify: `docs/03.specs/028-readme-workspace-profiles/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-readme-workspace-profiles.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: done Specs 026–027 and active Spec 028.
- Produces: active `RWP-001` through `RWP-006` execution lineage.

- [ ] **Step 1: Run the failing lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path
spec = Path('docs/03.specs/028-readme-workspace-profiles/spec.md')
plan = Path('docs/04.execution/plans/2026-07-12-readme-workspace-profiles.md')
task = Path('docs/04.execution/tasks/2026-07-12-readme-workspace-profiles.md')
assert task.exists()
for source, target in ((spec,'../../04.execution/plans/2026-07-12-readme-workspace-profiles.md'),(spec,'../../04.execution/tasks/2026-07-12-readme-workspace-profiles.md'),(plan,'../../03.specs/028-readme-workspace-profiles/spec.md'),(plan,'../tasks/2026-07-12-readme-workspace-profiles.md'),(task,'../../03.specs/028-readme-workspace-profiles/spec.md'),(task,'../plans/2026-07-12-readme-workspace-profiles.md')):
    assert target in source.read_text(), (source, target)
PY
```

Expected: FAIL because the Task is absent.

- [ ] **Step 2: Create Task, links, and indexes**

Create an active Task with exact rows `RWP-001` through `RWP-006`, descriptions
from Work Breakdown, first row `Done`, remaining rows `Queued`, and reciprocal
Spec/Plan links. Set this Plan active and add dated active index rows.

- [ ] **Step 3: Validate and commit**

```bash
git diff --check
git add docs/03.specs/028-readme-workspace-profiles/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-readme-workspace-profiles.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-readme-workspace-profiles.md docs/04.execution/tasks/README.md
git commit -m "docs(execution): start readme profile tranche"
```

Expected: commit succeeds.

---

### Task 2: Create Six Profile Forms, Routes, and Fixture Handoff

**Files:**

- Create: `docs/99.templates/templates/common/readme-repository.template.md`
- Create: `docs/99.templates/templates/common/readme-stage-index.template.md`
- Create: `docs/99.templates/templates/common/readme-collection-index.template.md`
- Create: `docs/99.templates/templates/common/readme-implementation.template.md`
- Create: `docs/99.templates/templates/common/readme-snapshot-pack.template.md`
- Create: `docs/99.templates/templates/common/readme-workspace-staging.template.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Create: `tests/fixtures/document-contracts/readme-profile-cases.json`
- Modify: `tests/README.md`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify inventory/target-link rows only: `docs/99.templates/README.md`
- Modify inventory/target-link rows only: `docs/99.templates/templates/README.md`
- Modify: `docs/99.templates/support/template-routing.md`

**Interfaces:**

- Consumes: the six existing authored `readme/*` profiles, their 67 current and
  72 final routes, the profile heading table, and the complete path map in this
  Plan. RWP-002 does not create another authored README profile family.
- Produces: six frontmatter-free forms; six exact-route `template/readme/*`
  profiles bound one-to-one to the existing authored profiles; 72 `paths` rows with keys `path`,
  `profile`, `requiredH2`, `allowedH2`, and `new`; and eight `cases` rows with
  keys `name`, `path`, `document`, and `expected_rule_ids`.
- Preserves `docs/99.templates/templates/common/readme.template.md` until
  RWP-006 as the sole bounded detached compatibility form. Its profile remains
  exact ID `template/readme/common`, owns only that exact route, declares
  `sourceProfileIds: []`, and is not referenced by any authored or
  frontmatter-free profile's `template` field. It is the only ordinary
  source-less template, and both registry fixtures must describe that state.
- Permits both validators to exempt only that exact profile ID and old path
  from ordinary template-source inheritance. No broader empty-source or
  inheritance exception is allowed. RWP-006 removes the form, profile, fixture
  rows, and both exact exemptions atomically.
- Produces 61 registry profiles and 28 tracked Markdown template forms, up from
  55 and 22. Add six profile and six template coverage rows to
  `registry-cases.json`, add six rows to `templateModeCoverage`, and update the
  `DocumentProfileContract.v1` and `TemplateCompatibilityContract.v1` semantic
  digests without changing authored compatibility-debt baselines.
- Defines `--profile readme` as a family alias selecting only IDs beginning
  `readme/` whose class is `readme` and mode is `frontmatter-free`. Exact-ID
  selection remains supported, and `template/readme/*` never counts in the
  family total. The command validates all 72 fixture dispositions while
  reporting current tracked count 67 after RWP-002 and declared final count 72.

- [ ] **Step 1: Create the fixture before forms**

Add one `paths` row for every path in the Complete Map and cases
`valid-profile`, `frontmatter-forbidden`, `duplicate-h1`, `duplicate-h2`,
`unsupported-h2`, `missing-required-h2`, `fenced-heading-ignored`, and
`unclosed-fence`. Use expected rule IDs `README_FRONTMATTER`, `README_H1`,
`README_H2_DUPLICATE`, `README_H2_UNSUPPORTED`, `README_H2_REQUIRED`, and
`README_FENCE`. Every case names a real fixture `path` from `paths`, embeds its
Markdown `document`, and carries `expected_rule_ids`; Spec 029 must resolve the
named path to its production `DocumentProfile` before validating the document.
Each path row's `allowedH2` is the complete ordered `requiredH2` plus additional
H2 set, not only the optional values shown in the heading table.

- [ ] **Step 2: Run missing-form RED check**

```bash
for name in repository stage-index collection-index implementation snapshot-pack workspace-staging; do test -f "docs/99.templates/templates/common/readme-${name}.template.md" || exit 1; done
```

Expected: exit 1.

- [ ] **Step 3: Create minimal forms with exact headings**

Each form contains one placeholder H1, only its required H2 sequence, HTML
comments explaining topic-specific content, and target-relative link guidance.
Do not add `Selection Guide`, `Assembly Rules`, `SNIPPET LIBRARY`, or generic
optional sections.

- [ ] **Step 4: Bind existing authored routes and add template profiles**

Confirm that the existing six authored README profiles classify the 67 current
and 72 final routes from the Complete Map. Prefer shared anchored regex only
where every matched path has the same profile; otherwise use exact routes. Set
frontmatter mode `forbidden`, replace each authored profile's monolith template
reference with its one-to-one form, and set its required and complete allowed
heading arrays from this Plan. Add six template-mode profiles with one exact
form route and one corresponding authored source profile.

Detach `template/readme/common` by setting `sourceProfileIds: []` while keeping
its exact old route and form through RWP-006. Add exact-ID/path guards in both
validators proving it is the sole ordinary source-less template and no
authored/frontmatter-free profile points to the old form. Update both coverage
fixtures and both semantic digests without changing compatibility-debt counts.

Implement the `readme` family alias in the registry CLI. It validates the
fixture path/profile/heading dispositions, counts only authored
frontmatter-free `readme/*` profiles, and reports baseline 67, current 67, and
declared final 72 at the end of RWP-002.

- [ ] **Step 5: Stage the complete atomic scope before GREEN**

The registry self-test and quality gate derive template inventory from
`git ls-files`. Stage the six new forms, new fixture, and every atomic consumer
before running GREEN; do not use `git diff --name-only` as evidence for
untracked forms.

```bash
git add docs/99.templates/templates/common/readme-repository.template.md \
  docs/99.templates/templates/common/readme-stage-index.template.md \
  docs/99.templates/templates/common/readme-collection-index.template.md \
  docs/99.templates/templates/common/readme-implementation.template.md \
  docs/99.templates/templates/common/readme-snapshot-pack.template.md \
  docs/99.templates/templates/common/readme-workspace-staging.template.md \
  docs/99.templates/support/document-profiles.json \
  docs/99.templates/support/template-routing.md \
  docs/99.templates/README.md docs/99.templates/templates/README.md \
  scripts/validate-document-contract-registry.py \
  scripts/validate-repo-quality-gates.sh \
  tests/fixtures/document-contracts/registry-cases.json \
  tests/fixtures/document-contracts/template-compatibility.json \
  tests/fixtures/document-contracts/readme-profile-cases.json tests/README.md
```

- [ ] **Step 6: Assert fixture, forms, bindings, and detached compatibility**

```bash
python3 - <<'PY'
import json
from pathlib import Path
data=json.loads(Path('tests/fixtures/document-contracts/readme-profile-cases.json').read_text())
path_keys={'path','profile','requiredH2','allowedH2','new'}
case_keys={'name','path','document','expected_rule_ids'}
assert len(data['paths']) == 72
assert all(set(row) == path_keys for row in data['paths'])
assert len({row['path'] for row in data['paths']}) == 72
assert sum(row['new'] is False for row in data['paths']) == 67
assert sum(row['new'] is True for row in data['paths']) == 5
expected_cases = (
    ('valid-profile', ()),
    ('frontmatter-forbidden', ('README_FRONTMATTER',)),
    ('duplicate-h1', ('README_H1',)),
    ('duplicate-h2', ('README_H2_DUPLICATE',)),
    ('unsupported-h2', ('README_H2_UNSUPPORTED',)),
    ('missing-required-h2', ('README_H2_REQUIRED',)),
    ('fenced-heading-ignored', ()),
    ('unclosed-fence', ('README_FENCE',)),
)
assert len(data['cases']) == 8
assert all(set(case) == case_keys for case in data['cases'])
case_names=[case['name'] for case in data['cases']]
assert len(case_names) == len(set(case_names)) == 8
actual_cases=tuple(sorted(
    (case['name'], tuple(case['expected_rule_ids'])) for case in data['cases']))
assert actual_cases == tuple(sorted(expected_cases))
rule_ids={rule_id for _, expected in actual_cases for rule_id in expected}
assert rule_ids == {
    'README_FRONTMATTER', 'README_H1', 'README_H2_DUPLICATE',
    'README_H2_UNSUPPORTED', 'README_H2_REQUIRED', 'README_FENCE',
}
fixture_paths={row['path'] for row in data['paths']}
assert all(case['path'] in fixture_paths for case in data['cases'])

expected_headings={
    'repository': (
        ('Overview','Repository Map','Getting Started','Validation','Related Documents'),
        ('Prerequisites','Configuration','Security Boundary')),
    'stage-index': (
        ('Overview','Stage Contract','Document Index','Authoring Workflow','Related Documents'),
        ('Lifecycle Handoff',)),
    'collection-index': (
        ('Overview','Scope','Item Index','Add and Find','Related Documents'),
        ('Selection Rules',)),
    'implementation': (
        ('Overview','Structure','Configuration Boundary','Validation','Operations','Related Documents'),
        ('Prerequisites','Troubleshooting')),
    'snapshot-pack': (
        ('Overview','Snapshot Contract','Report Index','Refresh and Succession','Evidence Boundary','Related Documents'),
        ('Method',)),
    'workspace-staging': (
        ('Overview','Permitted Artifacts','Forbidden Local State','Promotion and Cleanup','Tracking Rules','Related Documents'),
        ()),
}
for row in data['paths']:
    name=row['profile'].removeprefix('readme/')
    assert name in expected_headings and row['profile'] == f'readme/{name}'
    required, additional=expected_headings[name]
    allowed=required+additional
    assert len(allowed) == len(set(allowed))
    assert tuple(row['requiredH2']) == required
    assert tuple(row['allowedH2']) == allowed

for name, (required, _) in expected_headings.items():
    form = Path(f'docs/99.templates/templates/common/readme-{name}.template.md')
    text=form.read_text()
    assert not text.startswith('---\n')
    h1 = [line for line in text.splitlines() if line.startswith('# ')]
    assert len(h1) == 1, (form, h1)
    assert all(marker not in text for marker in (
        'Selection Guide', 'Assembly Rules', 'SNIPPET LIBRARY'))

registry=json.loads(Path('docs/99.templates/support/document-profiles.json').read_text())
profiles={row['id']: row for row in registry['profiles']}
old='docs/99.templates/templates/common/readme.template.md'
legacy=profiles['template/readme/common']
assert legacy['routes'] == [{'kind': 'exact', 'value': old}]
assert legacy['template'] == old and legacy['sourceProfileIds'] == []
assert all(
    row['id'] == 'template/readme/common' or row['sourceProfileIds']
    for row in registry['profiles'] if row['mode'] == 'template'
)
assert all(
    row['template'] != old
    for row in registry['profiles']
    if row['mode'] in {'authored', 'frontmatter-free'}
)
for name, (required, additional) in expected_headings.items():
    authored=profiles[f'readme/{name}']
    template=profiles[f'template/readme/{name}']
    form=f'docs/99.templates/templates/common/readme-{name}.template.md'
    assert authored['template'] == form
    assert template['routes'] == [{'kind': 'exact', 'value': form}]
    assert template['sourceProfileIds'] == [f'readme/{name}']
    assert template['headings'] == authored['headings']
    allowed=required+additional
    assert len(allowed) == len(set(allowed))
    assert tuple(authored['headings']['required']) == required
    assert tuple(authored['headings']['allowed']) == allowed
    actual_h2=[line[3:] for line in Path(form).read_text().splitlines()
               if line.startswith('## ')]
    assert tuple(actual_h2) == required

registry_cases=json.loads(Path('tests/fixtures/document-contracts/registry-cases.json').read_text())
compat=json.loads(Path('tests/fixtures/document-contracts/template-compatibility.json').read_text())
common_profile=next(row for row in registry_cases['profileCoverage']
                    if row['profile'] == 'template/readme/common')
common_template=next(row for row in registry_cases['templateCoverage']
                     if row['profile'] == 'template/readme/common')
common_mode=next(row for row in compat['templateModeCoverage']
                 if row['profile'] == 'template/readme/common')
assert common_profile['path'] == old and common_template['path'] == old
assert common_mode['form'] == old and common_mode['sourceProfiles'] == []
PY
```

Expected: PASS.

- [ ] **Step 7: Run staged GREEN and prove exact cached scope**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility --profile readme
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
python3 - <<'PY'
import subprocess
expected={
    'docs/99.templates/README.md',
    'docs/99.templates/support/document-profiles.json',
    'docs/99.templates/support/template-routing.md',
    'docs/99.templates/templates/README.md',
    'docs/99.templates/templates/common/readme-collection-index.template.md',
    'docs/99.templates/templates/common/readme-implementation.template.md',
    'docs/99.templates/templates/common/readme-repository.template.md',
    'docs/99.templates/templates/common/readme-snapshot-pack.template.md',
    'docs/99.templates/templates/common/readme-stage-index.template.md',
    'docs/99.templates/templates/common/readme-workspace-staging.template.md',
    'scripts/validate-document-contract-registry.py',
    'scripts/validate-repo-quality-gates.sh',
    'tests/README.md',
    'tests/fixtures/document-contracts/readme-profile-cases.json',
    'tests/fixtures/document-contracts/registry-cases.json',
    'tests/fixtures/document-contracts/template-compatibility.json',
}
actual=set(subprocess.run(
    ['git','diff','--cached','--name-only'], check=True,
    capture_output=True, text=True).stdout.splitlines())
assert actual == expected, (sorted(expected-actual), sorted(actual-expected))
PY
git diff --cached --check
git diff --cached --name-only
```

Expected: self-test reports 9 cases, 61 profiles, and 28 templates; README
family classification reports current 67 and declared final 72; repository and
all applicable pre-commit gates pass; and cached scope is exactly the 16 files
listed in this Task.

- [ ] **Step 8: Commit forms and fixture locally**

```bash
git commit -m "feat(templates): define readme profiles"
```

Expected: commit succeeds. Do not push or publish it.

---

### Task 3: Migrate Repository, Stage, and Collection Entrypoints

**Files:**

- Modify: the 1 repository, 10 stage-index, and 16 baseline collection-index paths in the Complete Map
- Create: `docs/90.references/cloud-examples/README.md`

**Interfaces:**

- Consumes: repository/stage/collection forms and registry routes.
- Produces: 28 topic-specific entrypoints with canonical-owner links and no copied contract tables.

- [ ] **Step 1: Run missing collection-handoff RED assertion**

```bash
test -f docs/90.references/cloud-examples/README.md
```

Expected: exit 1 because structural registry classification deliberately
allows a declared future path to remain untracked. The README family command is
GREEN classification evidence after the handoff is created, not this RED.

- [ ] **Step 2: Migrate repository and stage indexes**

Preserve root setup and QA facts under repository headings. For each stage,
describe its role, list actual contained artifacts, link lifecycle rules to
Stage 99/00 owners, and give the real add/find workflow. Do not move policy or
validation prose into README.

- [ ] **Step 3: Migrate collection indexes**

Preserve every current inventory row and unique selection rule under the
collection profile. Replace universal `Audience`, `Structure`, `Link Basis`,
and `How to Work in This Area` only after their unique content has a destination.

- [ ] **Step 4: Create the cloud collection handoff**

`docs/90.references/cloud-examples/README.md` must state that AWS/Azure child
indexes are dated reference destinations, executable assets remain under
`examples/<provider>/`, Spec 030 owns relocation, and no current page claims
live or provider-latest readiness.

- [ ] **Step 5: Validate and commit**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility --profile readme
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git add README.md docs/README.md docs/00.agent-governance/README.md docs/00.agent-governance/memory/README.md docs/01.requirements/README.md docs/02.architecture docs/03.specs/README.md docs/04.execution docs/05.operations docs/90.references/README.md docs/90.references/audits/README.md docs/90.references/data/README.md docs/90.references/learning/README.md docs/90.references/llm-wiki/README.md docs/90.references/research/README.md docs/98.archive/README.md docs/99.templates docs/90.references/cloud-examples/README.md
git commit -m "docs(readme): migrate repository and index profiles"
```

Expected: focused and repository gates PASS.

---

### Task 4: Migrate Snapshot Packs and Create Provider Snapshot Handoffs

**Files:**

- Modify: the 28 baseline snapshot-pack paths in the Complete Map
- Create: `docs/90.references/cloud-examples/aws/README.md`
- Create: `docs/90.references/cloud-examples/azure/README.md`

**Interfaces:**

- Consumes: snapshot-pack form and provider research/snapshot evidence.
- Produces: 30 snapshot indexes with observation boundary, report inventory, refresh/successor, and evidence limits.

- [ ] **Step 1: Run missing-provider-handoff RED check**

```bash
test -f docs/90.references/cloud-examples/aws/README.md && test -f docs/90.references/cloud-examples/azure/README.md
```

Expected: exit 1.

- [ ] **Step 2: Migrate dated audit/research packs**

Preserve snapshot dates, baseline SHA when known, report indexes, Current versus
historical role, successor/resolution, external source limits, and no-live
evidence boundaries. Remove duplicated navigation headings only after merging
their unique links.

- [ ] **Step 3: Migrate example-local snapshot indexes**

For all AWS/Azure `examples/<provider>/docs/**/README.md`, state that content is
a dated migration example, not active main-stage ownership or provider-latest
guidance; retain exact child inventories for Spec 030 relocation.

- [ ] **Step 4: Create provider destination indexes**

Each new `docs/90.references/cloud-examples/<provider>/README.md` records
observation date `2026-07-12`, baseline SHA, current source tree, planned Spec
030 consolidation boundary, report inventory link, refresh trigger on official
provider service/contract changes, and no-live authority boundary.

- [ ] **Step 5: Validate and commit**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility --profile readme
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git add docs/90.references/audits docs/90.references/research/2026-07-04-wer/README.md docs/90.references/research/2026-07-07-wer/README.md docs/90.references/cloud-examples/aws/README.md docs/90.references/cloud-examples/azure/README.md examples/aws/docs examples/azure/docs
git commit -m "docs(readme): migrate snapshot pack profiles"
```

Expected: gates PASS and commit succeeds.

---

### Task 5: Migrate Implementation and Workspace Entrypoints

**Files:**

- Modify: the 11 baseline implementation paths in the Complete Map
- Create: `examples/aws/README.md`
- Create: `examples/azure/README.md`
- Modify: `_workspace/README.md`
- Modify: `.gitignore` only if its `_workspace` rule does not already preserve README-only tracking

**Interfaces:**

- Consumes: implementation/workspace forms and existing component inventories.
- Produces: 13 implementation entrypoints and one secret-safe workspace-staging contract.

- [ ] **Step 1: Capture workspace tracking RED/GREEN baseline**

```bash
test "$(git ls-files _workspace)" = "_workspace/README.md"
git check-ignore -q _workspace/probe.tmp
```

Expected: both PASS before content edits; if the ignore probe fails, patch only
the `_workspace/*` and `!_workspace/README.md` rules.

- [ ] **Step 2: Migrate implementation READMEs**

For examples, GitOps, workloads, infrastructure, scripts, tests, Traefik, and
Azure component directories, retain actual structure, configuration boundary,
validation commands, operational entrypoints, and component-specific matrices.
Move normative rules only by linking their canonical policy/contract owner.

- [ ] **Step 3: Create executable-provider handoffs**

`examples/aws/README.md` and `examples/azure/README.md` must distinguish
executable assets from dated documentation, link the provider snapshot
destination, preserve setup/validation entrypoints, and state that Spec 030
will remove example-local SDLC documents after knowledge consolidation.

- [ ] **Step 4: Normalize `_workspace` without inspecting children**

Use the exact workspace headings. Permit temporary audit scratch, redacted
non-secret dry-run summaries, route inventories, migration ledgers, and
non-secret scan summaries. Forbid credentials, tokens, auth files, shell
history, kubeconfigs, keys, certificates, browser/provider state, personal
diagnostics, and secret-bearing logs. Route promotion to Stage 00/04/90/99 and
require deletion before closure when no durable destination exists.

- [ ] **Step 5: Validate and commit**

```bash
test "$(git ls-files _workspace)" = "_workspace/README.md"
git check-ignore -q _workspace/probe.tmp
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility --profile readme
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git add README.md _workspace/README.md .gitignore examples/README.md examples/sample-app/README.md examples/aws/README.md examples/azure/README.md examples/azure/gitops/README.md examples/azure/infrastructure/README.md examples/azure/kubernetes/README.md gitops/README.md gitops/workloads/README.md infrastructure/README.md scripts/README.md tests/README.md traefik/README.md
git commit -m "docs(readme): migrate implementation and workspace profiles"
```

Expected: tracking and repository gates PASS.

---

### Task 6: Delete the Monolith, Verify Fixture Handoff, and Close

**Files:**

- Delete: `docs/99.templates/templates/common/readme.template.md`
- Modify: `docs/99.templates/README.md`
- Modify: `docs/99.templates/templates/README.md`
- Modify: `docs/99.templates/support/common-documentation-governance.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify: `docs/00.agent-governance/hooks/k8s-pre-edit.sh`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: Spec 028, this Plan, same-topic Task, and Stage 03/04 indexes

**Interfaces:**

- Consumes: all 72 migrated paths and `readme-profile-cases.json`.
- Produces: zero old-form references and an explicit Spec 029 fixture-consumer handoff.

- [ ] **Step 1: Run legacy RED search**

```bash
git ls-files -z -- 'README.md' ':(glob)**/README.md' | \
  xargs -0 -r rg -n 'SNIPPET LIBRARY|Selection Guide|universal seven'
rg -n '(^|/)readme\.template\.md|docs/99\.templates/templates/common/readme\.template\.md|template/readme/common' \
  docs/99.templates docs/00.agent-governance/rules \
  docs/00.agent-governance/hooks scripts tests .agents .claude .codex
```

Expected: old form and active consumer references are found. Deliberately do
not search non-README Specs, Plans, Tasks, Stage 90 research/audits, or Stage 98
history: those records may name the retired form as evidence and are not
runtime or authoring consumers. README entrypoints remain in the first,
README-owned scan because all 72 are migration targets. Generic legacy heading
markers are not scanned across `.agents`, `.claude`, or `.codex`; only exact
old-form/profile references are checked on those active consumer surfaces.

- [ ] **Step 2: Delete old form and update consumers**

Delete `readme.template.md` with `apply_patch`; remove exact profile
`template/readme/common`, its registry and TemplateCompatibility coverage rows,
every exact-ID/path validator exemption, and every active old-form consumer
including the pre-edit hook. Recompute both semantic pins after removing that
state. Preserve the six one-to-one authored/template profile bindings and
forms. Replace route/inventory links with the six forms and replace the
universal heading loop in the current quality gate with a finite reader of
`readme-profile-cases.json`. This temporary check may compare actual H1/H2 to
fixture expectations but must carry removal owner `Spec 029` and must not
become a second canonical heading table.

- [ ] **Step 3: Run focused fence-aware migration assertion**

Use an inline Python state machine that ignores lines between matching backtick
or tilde fences, rejects unclosed fences, collects H1/H2, loads expected
required/allowed headings from the fixture, and asserts one H1, no duplicate
H2, all required H2, no unsupported H2, and no frontmatter for each of 72
paths. Do not save this state machine as the production parser.

- [ ] **Step 4: Prove fixture handoff completeness**

```bash
python3 - <<'PY'
import json
import subprocess
from pathlib import Path
data=json.loads(Path('tests/fixtures/document-contracts/readme-profile-cases.json').read_text())
paths={row['path'] for row in data['paths']}
tracked={
    path
    for path in subprocess.run(
        ['git', 'ls-files', '--', 'README.md', '*/README.md', '**/README.md'],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if path == 'README.md' or path.endswith('/README.md')
}
assert len(paths) == 72
assert paths == tracked, (sorted(paths-tracked), sorted(tracked-paths))
assert {case['name'] for case in data['cases']} == {'valid-profile','frontmatter-forbidden','duplicate-h1','duplicate-h2','unsupported-h2','missing-required-h2','fenced-heading-ignored','unclosed-fence'}
PY
```

Expected: PASS. The Task records that Spec 029 must run these same cases
through its production CommonMark-aware parser.

- [ ] **Step 5: Run final QA**

```bash
test ! -e docs/99.templates/templates/common/readme.template.md
if git ls-files -z -- 'README.md' ':(glob)**/README.md' | \
  xargs -0 -r rg -n 'SNIPPET LIBRARY|Selection Guide|universal seven'; then
  exit 1
fi
if rg -n '(^|/)readme\.template\.md|docs/99\.templates/templates/common/readme\.template\.md|template/readme/common' \
  docs/99.templates docs/00.agent-governance/rules \
  docs/00.agent-governance/hooks scripts tests .agents .claude .codex; then exit 1; fi
python3 - <<'PY'
import json
from pathlib import Path
registry=json.loads(Path('docs/99.templates/support/document-profiles.json').read_text())
registry_cases=json.loads(Path('tests/fixtures/document-contracts/registry-cases.json').read_text())
compat=json.loads(Path('tests/fixtures/document-contracts/template-compatibility.json').read_text())
old_id='template/readme/common'
old_path='docs/99.templates/templates/common/readme.template.md'
assert old_id not in {row['id'] for row in registry['profiles']}
assert old_id not in {row['profile'] for row in registry_cases['profileCoverage']}
assert old_path not in {row['path'] for row in registry_cases['templateCoverage']}
assert old_id not in {row['profile'] for row in compat['templateModeCoverage']}
assert old_path not in {row['form'] for row in compat['templateModeCoverage']}
validator_sources=(
    Path('scripts/validate-document-contract-registry.py'),
    Path('scripts/validate-repo-quality-gates.sh'),
)
for source in validator_sources:
    text=source.read_text()
    assert old_id not in text, source
    assert old_path not in text, source
names=('repository','stage-index','collection-index','implementation','snapshot-pack','workspace-staging')
profiles={row['id']: row for row in registry['profiles']}
for name in names:
    form=f'docs/99.templates/templates/common/readme-{name}.template.md'
    assert profiles[f'readme/{name}']['template'] == form
    assert profiles[f'template/readme/{name}']['template'] == form
PY
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility --profile readme
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --all-files
```

Expected: 72 README paths classify once, searches are empty, and all applicable checks PASS.

- [ ] **Step 6: Close lifecycle, evidence, and commit**

Set Spec, Plan, Task, and three index rows to `done`; record baseline/final
counts, all commands and outcomes, no-secret/no-live limitations, reviewer,
rollback range, five cloud handoff paths, and Spec 029 fixture obligation.

```bash
git add docs/99.templates docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/document-stage-routing.md docs/00.agent-governance/rules/stage-authoring-matrix.md docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-document-contract-registry.py scripts/validate-repo-quality-gates.sh docs/03.specs/028-readme-workspace-profiles/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-readme-workspace-profiles.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-readme-workspace-profiles.md docs/04.execution/tasks/README.md tests/fixtures/document-contracts/registry-cases.json tests/fixtures/document-contracts/template-compatibility.json tests/fixtures/document-contracts/readme-profile-cases.json
git commit -m "docs(readme): close profile migration evidence"
```

Expected: closure commit succeeds.

## Completion Criteria

- [ ] Six profile forms and exact routes exist; the monolithic form is deleted.
- [ ] All 67 baseline and 72 final README paths have exactly one profile.
- [ ] Frontmatter, duplicate structural headings, unsupported headings, and snippet residue are zero.
- [ ] Five cloud handoff READMEs exist with correct execution/snapshot boundaries.
- [ ] `_workspace` tracks only README and keeps ignored private/local state outside scope.
- [ ] Spec 029 fixture handoff is complete and explicitly recorded.
- [ ] Repository quality, all-files, links, reciprocal evidence, and index states pass.

## Related Documents

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Registry Spec**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Template Spec**: [Template Contract Consolidation](../../03.specs/027-template-contract-consolidation/spec.md)
- **Spec**: [README and Workspace Profiles](../../03.specs/028-readme-workspace-profiles/spec.md)
- **Next Spec**: [Semantic Document Validation](../../03.specs/029-semantic-document-validation/spec.md)
- **Task**: [README and Workspace Profiles](../tasks/2026-07-12-readme-workspace-profiles.md)
