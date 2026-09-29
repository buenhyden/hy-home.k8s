Scope: review of the read-only permission class definition.
Snapshot: branch `docs/0074-0075-governance-design`, HEAD 0b2deb0d, base f5f355f1.
Approval boundary: read-only review.

Finding. The policy at `.agents/governance/approval-and-safety.md` states that
"a read-only role is prevented from writing by the operating system on every
supported provider", so the class is enforced rather than advisory.

Lane results: repo-static PASS from `python3 scripts/qa.py quick`.
Next owner: platform.
