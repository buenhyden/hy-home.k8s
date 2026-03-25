# Claude Engine Governance

Governance for the Claude family of models, optimized for **Tool-Use** and **Agentic Autonomy**.

## 1. Core Engine Philosophy

- **Greedy Autonomy**: Claude should use tools proactively without asking for permission if the action is safe and aligns with the task.
- **Precise Reasoning**: Leverage Claude's ability to follow complex, nested instructions and technical constraints.

## 2. Tool-Use Protocol

- Always verify current directory state using `list_dir` or `find_by_name` before deep editing.
- Prefer targeted `replace_file_content` over full file rewrites for existing files.
- Document all tool calls in the task summary.

## 3. Metadata Awareness

- Respect the `layer:` metadata.
- If a document is missing metadata, promptly add it based on the 01-11 taxonomy.
