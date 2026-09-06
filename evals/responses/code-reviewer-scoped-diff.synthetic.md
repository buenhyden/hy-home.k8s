Scope: review of the staged change to the pre-action guard registration.
Snapshot: branch `codex/governance-follow-up`, HEAD 7e8a0b62, base 4053793a.
Approval boundary: read-only review; no commit, push, or merge authorized.

Findings. `.codex/hooks.json` registers `PreToolUse` on the shell and patch
tool classes and runs the guard at `.claude/hooks/k8s-pre-edit.sh`. The
handler carries a finite timeout, so a hung guard cannot stall a turn. The
registration is configuration; it does not show that the client delivered
the event.

One gap. `.agents/governance/approval-and-safety.md` still describes the
guard as covering structured file tools only. That sentence now understates
the matcher.

Lane results: repo-static PASS for the governance validator; native event
delivery DEFER, unobserved on this client.
Residual risk: a program that opens files itself stays outside the guard.
Next owner: platform, to correct the approval boundary sentence.
