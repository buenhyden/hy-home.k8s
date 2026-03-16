# Agent Framework Contract

Shared cross-agent contract for the `hy-home.k8s` repository. This file serves as the **Explicit Trigger** for all AI Agent rules.

## 1. Rule-Based Entrypoint

This repository uses a **Lazy Loading Protocol**. Agents MUST NOT load all instructions into memory. Instead, identify the relevant **Rule** or **Scope** based on the current user intent.

### Instruction Protocol

Detailed instructions are strictly managed via the **Gateway**:

- **Unified Gateway**: [agent-instructions.md](docs/agentic/agent-instructions.md)
- **Rules & Scopes**: Dispatched from the Gateway above.

## 2. Skill Autonomy

Agents have **Greedy Autonomy** to use any available skill in the runtime (e.g., `writing-plans`, `edit-file`, `run-command`). Do not wait for permission to use a relevant tool to fulfill a request.

## 3. Metadata Compliance

All documentation created or modified MUST include `layer:` metadata in the frontmatter.

- `layer: "meta"`: Governance and root documentation.
- `layer: "infra"`: Host, cluster, and networking.
- `layer: "gitops"`: ArgoCD and Sealed Secrets.
- `layer: "app"`: Application logic and manifests.
- `layer: "ops"`: Runbooks and incident reports.

## 4. Documentation Standards

- **Flattened Hierarchy**: All docs belong in `docs/<type>/`.
- **Plural Paths**: Execution documents reside in plural directories (e.g., `docs/plans/`, `docs/specs/`).
- **Template Driven**: Use `templates/` for all new documents.
