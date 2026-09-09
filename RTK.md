# RTK - Rust Token Killer (Cross-Agent SSOT)

**Usage**: Token-optimized CLI proxy for interactive agent-issued shell commands.

## Rule

Prefix interactive shell commands issued by an agent in this workspace with
`rtk` when the proxy supports the command. Use `rtk proxy <cmd>` for compatible
raw passthrough when no specialized subcommand applies.

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
In WSL, also check the local install path before treating RTK as absent:

```bash
/home/hy/.local/bin/rtk --version
/home/hy/.local/bin/rtk gain
```

If `/home/hy/.local/bin/rtk --version` works but `which rtk` returns nothing,
the current shell PATH is incomplete. If `rtk gain` fails with a tracking
database initialization error, do not inspect private databases or credential
files; run the underlying command directly and record the PATH/DB limitation in
the active task evidence instead of blocking repository validation.
