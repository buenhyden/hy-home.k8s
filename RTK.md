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
In that case, run the underlying command directly and record the limitation in
the completion summary instead of blocking repository validation.
