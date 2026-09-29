Scope: split the provider parity follow-up into two bounded packages.
Snapshot: branch `codex/governance-follow-up`, HEAD 5ee949a0, base 4053793a.
Approval boundary: routing only; no write, commit, push, or merge authorized.

Routing. The Codex hook registration goes to k8s-implementer, bounded to
`.codex/hooks.json` and `.claude/settings.json`. The registry scope binding
goes to quality-engineer, bounded to `.agents/roles/registry.json` and
`scripts/validate-agent-governance.py`. The two packages share no file, so a
single writer owns each and neither waits on the other.

Escalation. If the Codex payload shape turns out to differ from the published
contract in `.codex/provider.md`, that package stops and returns rather than
widening its own boundary.

Lane results: none run by this role; routing produces no gate evidence.
Residual risk: both packages touch the governance validator's failure
vocabulary and must not land the same rule twice.
Next owner: k8s-implementer first, then quality-engineer.
