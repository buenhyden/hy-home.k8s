Scope: collect current source evidence on whether the provider write guard
blocks a shell redirection or only reports it.
Snapshot: branch `refactor/governance-qa-convergence`, HEAD cc18cdc9, base 02a5a3a1.
Approval boundary: read-only research. No repository write and no external
transmission were authorized for this question.

The canonical owner is `.agents/governance/approval-and-safety.md`, which places
a shell target in the reported-but-not-prevented class, and the executable owner
is `scripts/provider_write_guard.py`. The Codex-side note at `.codex/provider.md`
records the same distinction against a named client version and an observation
date, so the two sides agree rather than one restating the other.

No external source was required: the question resolves inside this repository,
so network research was not used and no external page is cited. Where an
external source had been needed, its identity, link and observation date would
belong beside the claim it supports.

Lane results: repo-static PASS from `python3 scripts/qa.py quick` over the
governance documents this record cites. Provider runtime is a separate lane and
carries no result here.
Residual risk: the guard's runtime delivery on either provider remains
unobserved, which the provider note already records as its own limitation.
Next owner: doc-writer, to place the accepted finding at its canonical owner.
