# RTK - Rust Token Killer (Cross-Agent SSOT)

**Usage**: Token-optimized CLI proxy for interactive agent-issued shell commands.

## Rule

Route interactive shell commands issued by an agent in this workspace through
RTK. How depends on whether the host already does it:

- When a host hook rewrites commands through RTK and the host says that
  command output is already condensed, run commands in their native form. Re-run
  one as `rtk proxy <cmd>` only when its result is unusable: empty when output
  was clearly expected, contradicting its exit code, or garbled.
- Otherwise prefix each command with `rtk` when the proxy supports it, and use
  `rtk proxy <cmd>` for compatible raw passthrough when no specialized
  subcommand applies.

This rule governs commands the agent runs. Keep portable human examples,
CI/workflow commands, validation-registry argv, and shell or hook internals in
their native command form unless that consumer explicitly invokes RTK.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

If `which rtk` returns nothing, the current shell cannot use the RTK proxy.
Also check the user-local install path before treating RTK as absent:

```bash
~/.local/bin/rtk --version
~/.local/bin/rtk gain
```

If `~/.local/bin/rtk --version` works but `which rtk` returns nothing,
the current shell PATH is incomplete. If `rtk gain` fails with a tracking
database initialization error, do not inspect private databases or credential
files; run the underlying command directly and record the PATH/DB limitation in
the active task evidence instead of blocking repository validation.
