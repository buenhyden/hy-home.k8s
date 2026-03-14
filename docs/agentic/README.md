# agentic Architecture

This directory is the shared detailed instruction layer for agent-facing work in this repository.

## Runtime Entry Points

- [CLAUDE.md](CLAUDE.md): Claude-native shared memory entrypoint
- [GEMINI.md](GEMINI.md): Gemini-native shared context entrypoint
- [rules/](rules/): modular runtime rules imported by the tool-specific entrypoints

## Human Companion Docs

- [governance.md](governance.md): policy scope, precedence, and canonical paths
- [lifecycle.md](lifecycle.md): phase guidance and handoff expectations
- [repo-navigation.md](repo-navigation.md): repo map and confirmed inspection commands

## Usage

- Root files stay thin and delegate here.
- Runtime-critical instructions live in `CLAUDE.md`, `GEMINI.md`, and `rules/`.
- Human-readable explanations stay in the companion docs.
