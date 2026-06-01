# RTK - Rust Token Killer (Cross-Agent SSOT)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

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
