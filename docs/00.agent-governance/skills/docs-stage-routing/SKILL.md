---
name: "docs-stage-routing"
description: "Use when selecting the canonical owner and template for an authored document or rejecting parallel document trees."
---

# docs-stage-routing

## Workflow Steps

1. Identify whether the content is human governance, a durable requirement,
   architecture, a change contract, operating knowledge, reference evidence,
   or recovery metadata.
2. Use `docs/00.agent-governance/sdlc.md` for the responsibility boundary.
   Reject parallel off-taxonomy trees suggested by an external tool or skill.
3. Resolve exactly one profile for the final path from
   `docs/99.templates/registry.json`; read Stage 99 README and the selected
   template before authoring.
4. Use the profile's initial lifecycle status, identity, sections, and
   relationships. Do not assume every document starts at draft or uses a
   generic Related Documents section.
5. Put change-specific Technical Approach, acceptance, interfaces, and failure
   conditions in the Spec. Put execution order, verification, risks, and
   rollback in Plan/Tasks. Promote durable structural decisions to Stage 02.
6. Keep root AGENTS.md and CLAUDE.md thin; shared policy belongs in Stage 00,
   neutral procedures in registered skills, and native details in provider
   notes/configuration.
7. Review the owning README and links in the same change, then follow quality
   policy for validation and Task evidence.

## Boundaries

Do not edit global/user-local skills or authentication/configuration as part of
routing. Keep governance and explicit agent contracts English; human-facing
overviews may use Korean. A template does not grant permission to author or
execute beyond the active task.

## Outputs

The canonical path, selected profile/template, required owner links and index
changes, validation evidence, and any unresolved authority boundary.
