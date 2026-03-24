# Agent Framework Contract

Shared contract for `hy-home.k8s`. This is the **Explicit Trigger** for all AI rules.

## 1. Lazy Loading Protocol

Agents MUST NOT load all instructions. Identify **Intent** and load **Scope**.

- **Gateway**: [agent-instructions.md](docs/00.agent/agent-instructions.md)
- **Persona**: [persona-matrix.md](docs/00.agent/rules/persona-matrix.md)

## 2. Shared Directives

- **Spec-First**: Changes require `docs/04.specs/`.
- **Metadata**: All docs MUST include `layer:` frontmatter.
- **Verify**: `pre-commit run --all-files` before commit.

## 3. Scope Index

- **00-06**: [Agent](docs/00.agent/), [PRD](docs/01.prd/), [ARD](docs/02.ard/), [ADR](docs/03.adr/), [Spec](docs/04.specs/), [Plan](docs/05.plans/), [Task](docs/06.tasks/)
- **07-11**: [Guide](docs/07.guides/), [Ops](docs/08.operations/), [Runbook](docs/09.runbooks/), [Incident](docs/10.incidents/), [Postmortem](docs/11.postmortems/)
- **90-99**: [Ref](docs/90.references/), [Template](docs/99.templates/)
