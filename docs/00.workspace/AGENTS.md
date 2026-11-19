# AGENTS.md

Agent instructions for `docs/00.workspace/`, the workspace (W) layer shared by
people and agents. The parent [`docs/AGENTS.md`](../AGENTS.md) still applies.

## Scope

### Allowed Scope

This stage owns how work is done here: local Kubernetes vocabulary (`01.project/`), the
work-system architecture (`02.architecture/`), SDLC, document and Git process
(`03.process/`), quality, formatting and approval (`04.quality/`) and
reproducible local validation preparation (`05.environment/`) and maintenance
(`06.maintenance/`), as SDLC-R036 assigns the W layer.

| Work here | Role (`.agents/roles/`) | Skills | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change a workspace policy or its rule IDs | [governance-steward](../../.agents/roles/governance-steward.md) | `workspace-harness-audit`, `knowledge-map` | `.claude/agents/governance-steward.md` | `.codex/agents/governance-steward.toml` |
| Work-system AD or ADR | [architect](../../.agents/roles/architect.md) | `requirements-to-design`, `docs-stage-routing` | `.claude/agents/architect.md` | `.codex/agents/architect.toml` |
| Author vocabulary, guide, runbook or README text | [doc-writer](../../.agents/roles/doc-writer.md) | `docs-stage-conformance`, `docs-stage-routing` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` |
| Indexes and owner navigation | [wiki-curator](../../.agents/roles/wiki-curator.md) | `docs-stage-conformance`, `knowledge-map` | `.claude/agents/wiki-curator.md` | `.codex/agents/wiki-curator.toml` |

#### Non-goals

Product requirements, product architecture and operations stay in Stages 01,
02 and 05; agent execution rules stay in `.agents/governance/`; provider values
stay in `.claude/` and `.codex/`.

### Instruction Precedence

#### Canonical Sources

Canonical sources are the documents linked or named in the opening paragraph and in the rules under Local Obligations.

## Workflow

### Intake

#### Local Obligations

1. One meaning has one active owner. A rule ID is owned by one policy; SAFE
   and GIT are split between this stage and `.agents/governance/`, and the
   registry `policy_rule_ids` record of each half lists its rule IDs.
2. Do not copy a policy body into `.agents/`, a provider file or a form; link
   the owner instead.
3. Put a decision about how work is done (documents, agents, QA, CI, Git,
   release, disposition) in `02.architecture/02.decisions/`; a product
   platform decision belongs in `docs/02.architecture/02.decisions/`. AD and
   ADR numbers share one sequence across both and are never reused.
4. Create a numbered category folder only when it holds a real document;
   update this stage's README in the same change.
5. A move keeps document IDs, rule IDs and historical bodies (DOCLIFE-R023).

### Execution

Inspecting and changing files follows the rules under Local Obligations.

## Boundaries

### Authority

#### Stop and Escalate

This folder adds no stop condition beyond the work lifecycle's stop rule and the approval and safety policy; if work here needs its own, state it here.

### Secrets and External Effects

#### Protected Actions

This folder adds no protected action beyond the approval and safety policy; if work here can start one, name it here.

## Verification

### Checks

Select the document checks in the parent `AGENTS.md`; a policy change also
selects the governance checks registered for it.

### Reporting

#### Evidence and Limits

This folder adds no evidence rule beyond the quality policy's handoff contract; if a check here has a limit to report, state it here.

#### Handoff

This folder hands off through the work lifecycle's Completion steps with no extra field; if it needs one, state it here.
