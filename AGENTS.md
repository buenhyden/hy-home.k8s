# Agent Instructions

Shared cross-agent contract for the `hy-home.k8s` repository.

## Rule-Based Entrypoint

This repository uses a **Lazy Loading Protocol** for instructions. Agents MUST NOT load all instructions into memory at once. Instead, identify the relevant **Rule** based on the current task scope and import the corresponding **Scope** file.

### Instruction Map

Detailed instructions and personas are managed in `docs/agentic/`:

- **Primary Entrypoint**: [docs/agentic/agent-instructions.md](docs/agentic/agent-instructions.md)
- **Domain Rules**: `docs/agentic/rules/`
- **Task Scopes**: `docs/agentic/scopes/`

## Skill Autonomy

Agents have **Full Autonomy** to use any available skill in the runtime (e.g., `writing-plans`, `edit-file`, `run-command`). Do not wait for explicit permission to use a relevant tool that helps fulfill the user request.

## Metadata Compliance

All documentation created or modified MUST include `layer:` metadata in the frontmatter.

- `layer: "meta"`: Root documentation and project governance.
- `layer: "infra"`: Infrastructure and cluster definitions.
- `layer: "architecture"`: Design and decision records.
- `layer: "product"`: Requirements and vision.
