Scope: review of the staged change to the pre-action guard registration.
Snapshot: branch `codex/governance-follow-up`, HEAD 7e8a0b62, base 4053793a.
Approval boundary: read-only review; no commit, push, or merge authorized.

Findings. `.codex/hooks.json` registers `PreToolUse` on the shell and patch
tool classes and runs the guard at `.claude/hooks/k8s-pre-edit.sh`. The
handler carries a finite timeout, so a hung guard cannot stall a turn. The
registration is configuration; it does not show that the client delivered
the event.

One naming risk. The Codex registration runs a script under
`.claude/hooks/`, a provider-named directory now serving both providers. A
reader could take the path as evidence that the guard is Claude-only.
`.claude/README.md` says otherwise, so the risk is navigational rather than
functional, and moving the script would split one implementation in two.

Lane results: repo-static PASS for the governance validator; native event
delivery DEFER, unobserved on this client.
Residual risk: a program that opens files itself stays outside the guard.
Next owner: platform, to correct the approval boundary sentence.
