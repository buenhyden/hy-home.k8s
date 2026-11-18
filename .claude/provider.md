---
title: "Claude Provider Notes"
version: "1.10.0"
type: "governance/provider"
status: "active"
owner: "platform"
updated: "2026-11-18"
---

# Claude Provider Notes

## Overview

Describe Claude-native loading, permissions, and hooks without duplicating
shared execution policy or the agent roster.

## Authority Boundary

Root `CLAUDE.md` is the thin Claude gateway and must not import the Codex
gateway. `.claude/CLAUDE.md` is the local baseline;
`.claude/settings.json` carries native permission and hook declarations.
Their limit is set in
[agent execution](../.agents/governance/agent-execution.md#owner).

## Governance Context

Load the gateway, [work lifecycle](../.agents/workflows/work-lifecycle.md), relevant
responsibility, and current Task. [Claude bindings](bindings.json) own native
model, effort, skill and tool values; Markdown role projections consume those
values. The neutral registry owns responsibility and permission-class meaning.
A role's native departure is declared in the binding table; its ceiling is
[SAFE-R019](../.agents/governance/approval-and-safety.md#execution-controls).

## Current Contract

Each `.claude/skills/<id>` is a relative link to
`../../.agents/skills/<id>`. `disable-model-invocation: true` requires explicit
invocation. The common procedure retains the selected role and user scope.

- Use `.claude/agents/*.md` projections selected by the neutral registry for
  authorized delegation through the available runtime mechanism.
- Read shared skills through `.claude/skills`, a view of the neutral owner.
  File presence alone does not prove native discovery or use.
- Tracked permissions are the allow, ask and deny rules in
  `.claude/settings.json`; their design record SPEC-0114 is in Git history.
  Deny is checked first and no allow can
  override it. A rule matches command text from its first character, so deny
  carries option-first forms (`kubectl * delete *`), positional push forms and
  Bash path patterns for secret files: in a session probe a `Read` deny did not
  stop `cat` on the same path. Read-only Git and GitHub commands, commit,
  push, tag, pull request creation, readiness, approval and merge, Release and
  workflow commands and the release producer are allowed because an operator
  request is their approval; `gh api` and `git -C` ask, because a prefix rule
  cannot see their effect; `disableBypassPermissionsMode` is `disable`. The
  deny list carries forced merge; a push to `main` by name, `heads/main` or an
  implicit destination (a bare push, a remote alone, `HEAD`, `@`, `--all`,
  `--branches` and the common option-only forms); the `+` force refspec; the
  push force, delete, mirror and prune options and the tag force and delete
  options, with their unique prefixes and two-letter clusters; a fetch into a
  `refs/tags/` or `tags/` destination, tag pruning, and a fetch with `--stdin`
  or a refspec map; the amend and hook-bypass options; Release deletion and
  run cancellation.
  Executable-carrying Git options (`--upload-pack`, `--receive-pack`,
  `--exec`, `--output`) are denied, together with the unique abbreviations
  that an allowed command accepts (`--upl`, `--rece`, push `--e`, and
  ls-remote `--u` and `--exe`); a receive-pack or upload-pack program set in
  configuration is not seen. Residual, not coverage: a tag rewrite that
  no deny rule matches (for example a longer `git tag` cluster, a refspec
  deletion of a tag, a fetch form the fetch rules miss, or a configured
  tag refspec or tag pruning), a Release or `v` tag made outside the release
  producer, and `gh workflow enable` or `disable` are forbidden by policy but
  not denied; the release producer and the Git hooks that commit, push and
  merge run are working-tree code that runs without a prompt; a refspec
  deletion such as `origin :branch`, option clusters of three or more letters,
  the short hook-bypass form after other options or in a cluster, quoted,
  escaped or variable arguments, including options, and configured push
  destinations cannot be matched. The
  [Git policy](../.agents/governance/git.md#agent-delivery-commands) states
  the delivery boundary once for every agent.
  Programs that open files themselves and text-obfuscated paths cannot be
  matched; they stay residual risk, not coverage.
- Tracked settings register `.claude/hooks/k8s-pre-edit.sh` for pre-action
  safety, on the shell, structured file and notebook tools, and
  `.claude/hooks/session-start.sh` on `SessionStart` for `compact|resume`, which
  only prints the reading instruction and runs no QA. The pre-tool adapter
  exits 2 with a reason on stderr when it refuses a call. Its command also
  sets `onFailure: "block"` on Claude Code 2.1.295 and later so startup
  failure, timeouts and invalid JSON count as refusals in a client that
  loads the hook. The [hook reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)
  defines those cases. The pre-tool script is this provider's thin adapter;
  the boundary itself is owned by
  `scripts/provider_write_guard.py`, which the adapter resolves from its own
  checkout so a project directory pointed at another tree supplies data and
  never the program. It enforces a boundary only when the intended runtime
  loads it, and its shell observation is advisory: a shell write is reported,
  never blocked. A program that opens files itself stays outside it; see
  [approval and safety](../.agents/governance/approval-and-safety.md).
  Run QA explicitly; edit, Stop, and compaction events do not run whole QA.
  Observed on Claude Code 2.1.327 (2026-11-18, SPEC-0161 EVD-191):
  - after a compaction, the session received the `SessionStart` hook's
    additional context;
  - the pre-tool adapter refused a structured `Write` outside the checkout
    (`HOOK-PATH-ROOT`), both in the main session and in a nested sub-agent;
  - the `Read(./secrets/**)` and `Bash(* secrets/*)` deny rules refused a read
    of a tracked non-secret file there, also in both;
  - an approved local read passed.
  A `claude -p --resume` run on 2.1.327 (2026-11-18, SPEC-0161 EVD-192) ran
  the `SessionStart` hook for `resume` and received its additional context.
- Tracked settings also register `.claude/hooks/session-capture.sh` on
  `SessionStart`, `Stop`, `PreCompact`, `SubagentStop` and `SessionEnd`. It
  forwards the payload to `scripts/session_capture.py hook`, which records one
  pointer row and returns; [context and memory](../.agents/governance/context-and-memory.md)
  CTX-R022 owns what it keeps. Observed on Claude Code 2.1.327 (2026-11-18,
  SPEC-0161 EVD-200): a `claude -p` run and its `--resume` delivered
  `SessionStart` (`startup`, `resume`), `Stop` and `SessionEnd`, and a scan
  then read the whole transcript as `complete`. The running session also
  picked up the changed settings and delivered `Stop` and `SubagentStop`, the
  latter with the sub-agent's own transcript path. `PreCompact` delivery stays
  unobserved.
- Here the `read-only-evidence` permission class withholds the structured
  write tools while leaving a shell available, so a shell write is prohibited
  by policy and observed advisorily rather than blocked. How this differs from
  Codex, and why it is not parity, is owned by
  [SAFE-R018](../.agents/governance/approval-and-safety.md#execution-controls).
- Claude loads root `CLAUDE.md`, not a folder `AGENTS.md`: with a `CLAUDE.md`
  present, Claude Code 2.1.319 reads no `AGENTS.md`, and the setting that loads
  both is ignored in project settings (observed 2026-11-06). Each folder that
  has an `AGENTS.md` therefore has a sibling `CLAUDE.md` whose whole content is
  `@AGENTS.md`; Claude loads it, with the import, once Claude reads, writes or
  edits a file in that folder (SPEC-0151; new 2.1.319 sessions observed the
  import after one Read and after one Write). The documentation says it
  reloads on demand after a compaction; that is not yet observed here.
  The repository quality check refuses a missing or altered import. The root
  `AGENTS.md` is the Codex gateway and is not imported. The pre-action guard
  also names the target's folder `AGENTS.md` paths on every write, and a
  `SessionStart` hook on `compact|resume` re-injects the instruction to read
  them again; `systemMessage` reaches only the user.
- Keep managed, project, and user instruction precedence intact. Use imports
  for shared context rather than copying policy into provider files.
- `settings.json` sets `autoMemoryEnabled: false`, and the validator rejects
  any other value: both providers keep reusable context in the shared
  workspace memory store owned by
  [context and memory](../.agents/governance/context-and-memory.md). Existing
  native memory files are neither deleted nor imported. A setting proves
  intent only; whether a session honors it is separate runtime evidence.
- Reviewed and not adopted on 2026-10-27 (SPEC-0125, Git history): no project MCP server
  is registered (no `.mcp.json` and no MCP key in tracked settings), no IDE
  shortcut, code-action or inline-edit configuration is tracked, and no
  model-generated test cases or hook-based automatic memory collection are
  used. Adding any of them is a separate scoped change.
- Treat ignored local warning files as auxiliary context, not shared policy or
  a substitute for repository validators.
- Do not add native metadata fields from assumptions about another client
  version. Verify the intended runtime contract when configuration changes.

Role projections carry the documented model aliases rather than a pinned
generation identifier, and [Claude bindings](bindings.json) own which alias
each capability tier binds. An alias keeps the selection stable
when a generation changes, and the validator rejects a projection whose model
does not resolve from the binding. Observed on `claude 2.1.263` (2026-09-06).
On `claude 2.1.283` (2026-09-27) an authorized session observed discovery of
every role projection, `sonnet` resolving to `claude-sonnet-5`, withheld
structured write tools for `read-only-evidence`, and delivery of the pre-edit
hook. The client exposes no `Grep` or `Glob` tool, although projections declare
both. The SPEC-0086 Task recorded that evidence; recover it with
`git show bc8e8125:docs/98.archive/completed/03.specs/0086-provider-native-runtime-observation/tasks/tsk-0001-observe-provider-native-runtime.md`.
Projections also carry `effort`, which the provider binding table owns per
tier, with a role override where effort or model genuinely differs.
Models stay aliases (`fable`, `opus`, `sonnet`, `haiku`), so each one follows
the newest generation of its family. Only supervisor and architect bind
`fable`. A running session keeps the definitions it loaded at start, so verify
a changed projection from a new session. Native macOS and Linux builds from
2.1.117 removed `Grep` and `Glob`, moved search into Bash, and drop the unknown
names silently. SPEC-0098 therefore gives every role's Claude scope `Bash`, and
`Grep` and `Glob` stay for the builds that still ship them. How the two read-only
roles that held no shell confine it is owned by
[SAFE-R018](../.agents/governance/approval-and-safety.md#execution-controls). The SPEC-0097 and SPEC-0098 Tasks recorded that evidence; recover
them with
`git show bc8e8125:docs/98.archive/completed/03.specs/0097-claude-model-and-effort-binding/tasks/tsk-0001-bind-claude-model-and-effort.md`
and
`git show 9a509be9:docs/98.archive/completed/03.specs/0098-claude-search-grant-and-retention/tasks/tsk-0001-grant-search-and-retain-packages.md`.
These are configuration intent; availability and resolution remain separate
runtime evidence. The native `Task` tool remains a documented alias for `Agent`.
See [subagent fields](https://code.claude.com/docs/en/sub-agents),
[model IDs](https://support.claude.com/en/articles/11940350-claude-code-model-configuration),
and [settings](https://code.claude.com/docs/en/settings).

## Validation and Refresh

Validate registry/projection semantics, tool metadata, settings, and hook
configuration after relevant changes. Separately evidence native discovery,
permission enforcement, hooks, model resolution, and authenticated operation.
Repository-static or hosted CI results cannot establish runtime success.

## Related Documents

- [Claude Baseline](CLAUDE.md)
- [Agent Registry](../.agents/roles/registry.json)
- [Model Selection](../.agents/governance/model-selection.md)
- [Quality Policy](../.agents/governance/quality.md)
