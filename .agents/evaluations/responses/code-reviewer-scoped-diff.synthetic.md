Scope: review of the staged change to the pre-action guard registration.
Snapshot: branch `docs/0074-0075-governance-design`, HEAD 0b2deb0d, base f5f355f1.
Approval boundary: read-only review; no commit, push, or merge authorized.

Findings. `.codex/hooks.json` registers `PreToolUse` on the shell and patch
tool classes and runs `.codex/hooks/pre-tool-use.sh`, this provider's own
adapter. The handler carries a finite timeout, so a hung guard cannot stall a
turn. The registration is configuration; it does not show that the client
delivered the event.

One residual risk. The adapter forwards to `scripts/provider_write_guard.py`,
which resolves the affected-surface selector from the project directory. A
project directory pointed at another tree therefore supplies data to the
selector, and the guard must never let it supply the program instead.

Lane results: repo-static PASS from `python3 scripts/validate-agent-governance.py --root .`
and `python3 -m unittest tests.test_k8s_pre_edit_hook`; native event delivery
DEFER, unobserved on this client.
Residual risk: a program that opens files itself stays outside the guard.
Next owner: platform, to record the delivery question as an open runtime item.
