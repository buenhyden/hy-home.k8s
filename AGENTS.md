Read `.agents/workflows/work-lifecycle.md` before acting.
Read `RTK.md` before acting.

# AGENTS.md

Thin GPT/Codex provider gateway for `hy-home.k8s`. The common core comes
first; the Codex-only reads follow in their own block.

- Shared execution policy: `.agents/governance/agent-execution.md`
- Role and skill authority: `.agents/roles/registry.json`
- Responsibilities: `.agents/roles/README.md`
- Validation and handoff: `.agents/governance/quality.md`
- Document authoring: `docs/99.templates/README.md`

Tracked projections are repository-static configuration, not native discovery
or runtime enforcement evidence.

Codex-only provider reads:

Read `.codex/provider.md` before acting.
Read `.codex/CODEX.md` before acting.

Read each selected role and its required `.agents/skills/<id>/SKILL.md`
procedures explicitly before acting; explicit reads complement native discovery; invocation grants no authority.
