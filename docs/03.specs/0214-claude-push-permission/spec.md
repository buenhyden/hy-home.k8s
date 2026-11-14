---
title: "Claude Delivery Permissions and CI/CD Governance"
version: "1.2.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0214"
---

# Claude Delivery Permissions and CI/CD Governance Technical Specification (Spec)

## Overview

This approved change contract widens the tracked Claude permission settings so that an agent can run the delivery commands the user named, on the user's request, without a native prompt, and states the delivery boundary once at the CI/CD governance owner. On 2026-11-14 the user asked for commit, push, pull request creation, inspection, approval and merge, tag, release, `gh release` and `gh workflow` in the allow list, with forced merge and direct pushes to `main` forbidden, and for the rules to be reflected in the CI/CD governance.

At `main` `511e106f` the tracked `.claude/settings.json` allows inspection, `git merge`, `gh pr create`, `gh pr merge` and run inspection (lines 4-25), asks for `gh api`, `git -C` and every push (lines 26-30), and denies 197 rules (lines 31-229). Among them are `gh release create` (46), `gh workflow run` (47), the commit amend form (81), the force, delete, mirror and prune push forms (83-86, 184-189, 226-228), `gh release delete` (214), `gh run cancel` (215) and both administrator merge orders (216, 225). `scripts/validate-agent-governance.py` pins the three lists by exact, order-sensitive equality (tuples at lines 90-320, compared at lines 1537-1547 under `AGENT-NATIVE-PERMISSION`). This package changes the lists, the pin, the regressions in `tests/test_agent_governance.py`, the Claude provider note, the parity sentence of the Codex provider note, the release-ownership text and one new subsection of the Git policy, the executor lines of the release runbook, and the `release.py` row of the scripts README. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-claude-push-permission.md) records execution.

## Strategic Boundaries & Non-goals

- In scope:
  - `permissions.allow`, `permissions.ask` and `permissions.deny` of `.claude/settings.json`, and nothing else in that file;
  - the three tuples and the comment at lines 112-116 of `scripts/validate-agent-governance.py`;
  - `tests/test_agent_governance.py`;
  - the permission bullet of `.claude/provider.md` (lines 43-56);
  - the parity sentence of `.codex/provider.md` (lines 63-64), as text only;
  - in `.agents/governance/git.md`, the Release ownership text (lines 112-133), a new `#### Agent delivery commands` subsection, and the frontmatter `version` and `updated`;
  - the executor lines 35-38, 66 (Step 5 of the Actions table) and 112-116 of `docs/05.operations/runbooks/0012-main-release-preparation-runbook.md`, with its frontmatter;
  - the `release.py` row of `scripts/README.md` (line 94);
  - this package, the Stage 03 README entry and reviewed `.secrets.baseline` entries.
- Not in this package:
  - `.claude/settings.local.json` and any other ignored personal settings, which the validator leaves outside the pin on purpose (comment at lines 1537-1540);
  - the `gh api` and `git -C` ask rules, which the user's words do not name;
  - every other part of `.codex/`: `.codex/rules/default.rules`, `.codex/config.toml`, hooks, bindings and projections, so the rules digest pin (validator line 37) stays;
  - hooks, `scripts/provider_write_guard.py`, workflows, remote branch protection and rulesets (`.github/AGENTS.md` rule 9);
  - `approval-and-safety.md`, `quality.md`, the CI/CD guide GDE-0010 and `.github/AGENTS.md`, which need no change (see the policy bullet in Contracts);
  - the behavior of `scripts/release.py`;
  - ADR-0048 and AD-0006, which this change stays within (see Core Design);
  - any registry.
- Wave relation: this is a direct user request outside the v14.7 wave plan of SPEC-0161, not a W03 item. The SPEC-0161 Primary Writers table (Task lines 247-259) names W01 for `git.md`, W05 for `tests/`, W07 for `.claude/provider.md` and `.codex/provider.md`, and W03 for current Stage 05 documents. `.claude/settings.json` and the governance validator are unassigned. Each of these files is edited here under the user's request. The package appends no decision row to the SPEC-0161 Task, writes no entry to the work residue ledger, and leaves SPEC-0161 R147-17 (W07, Task line 169) open.
- Registry Schema Version: NO_CHANGE. No key, value or shape of `docs/99.templates/registry.json` changes, and `.agents/roles/registry.json` (`schema_version` 2) and `.claude/bindings.json` are untouched.
- No commit, push, PR or merge of this package without the user's approval; its own delivery follows the rules in force when it runs.
- Open question: none.

### Decisions

The user's successive wordings and answers on 2026-11-14 (Asia/Seoul), verbatim:

1. "`allow 목록에 git commit, push, pr 생성 및 확인 그리고 승인, merge 포함. 단, 강제 병합만 금지.`"
2. Answer "Governed package (Recommended)": move the catch-all push rule (the `Bash(...)` rule that matches every push command) from the ask list to the allow list in the tracked `.claude/settings.json`, keep the force, delete, mirror and prune denies, deny forced merge `gh pr merge --admin`, update the validator pin, its tests and `.claude/provider.md`, and record the refspec residual risk. (Option text; the push rule is described, not quoted, because the repository quality check refuses a literal push command in Markdown.)
3. Answer "Keep them (Recommended)": every existing deny stays (force push, push `--delete`, `--mirror` and `--prune`, the commit amend form, `gh pr merge --admin`).
4. "`allow 목록에 git commit, push, pr 생성 및 확인 그리고 승인, merge 포함. 단, 강제 병합, main에 직접 push 금지`"
5. "`allow 목록에 git commit, push, pr 생성 및 확인 그리고 승인, merge, tag, release, gh relase, gh workflow 포함. 단, 강제 병합, main에 직접 push 금지. 이를 CI/CD와 관련한 거버넌스, 체계, 규칙에 정리하여 반영`"
6. Answers to the three questions the draft raised:
   - `gh release` and `gh workflow` against the kept denies: "Lift create/run denies". `Bash(gh release create:*)` (settings line 46, validator line 137) and `Bash(gh workflow run:*)` (settings line 47, validator line 138) are removed. `Bash(gh release delete*)` (settings line 214, validator line 305) and `Bash(gh run cancel*)` (settings line 215, validator line 306) are separate rule lines that the answer does not name, so they stay. No new deny is added for `gh release edit` or `upload`, or for `gh workflow enable` or `disable`. The one-producer release rule in git.md is amended to say who may publish and how a Release stays traceable.
   - Superseded by answer 7: Tag force and delete: "Allow". No tag deny is added. The permission does not change the policy: git.md line 127 keeps tags as immutable history, so a tag rewrite stays forbidden by policy and is now unprompted (see Residual risk).
   - Codex parity for the direct-push deny: "Leave .codex unchanged (Recommended)". The Codex rules and configuration are unchanged; only the provider note's parity sentence is corrected, because the change makes it inaccurate.
7. Answer "Harden tags in 0214 (Recommended)" (2026-11-14), given after implementation to the finding that git.md forbids tag rewrite and deletion while the settings allowed `git tag -f` and `git tag -d`: deny the tag force and delete forms that a pattern can express, derived the same way as the push forms, and record the rest as residual.
8. Answer "Deny fetch tag forms (Recommended)" (2026-11-14), given after an independent review found that the allowed `git fetch` moves or deletes local tags: deny a fetch into a `refs/tags/` destination and tag pruning with four rules, keep plain, tag and forced branch fetches allowed, and record every fetch form the four rules miss as residual.
9. Answer "Add the 2 clean rules (Recommended)" (2026-11-14), given to the dry-run finding that the answer 8 rules miss some fetch forms: append `Bash(git fetch *:tags/*)` for an unqualified `tags/<name>` destination, and widen `Bash(git fetch *--prune-t*)` in place to `Bash(git fetch *--prune-*)` for the shortest tag-pruning prefix. The other missed forms stay residual.
10. Answer "Add 2 rules, then finish (Recommended)" (2026-11-14), given after a re-review found that a fetch can still write into `refs/tags/` through refspecs read from standard input or a refspec map: append `Bash(git fetch *--stdin*)` and `Bash(git fetch *--refm*)`, record the remaining fetch forms as residual, and finish the package.

Derived by the drafter from those words. These are for review and are not user decisions:

- **`gh pr ready` is part of the pull request flow.** The user's words do not name it. It is allowed because it moves a draft pull request the agent created toward the approval and merge the user did name.
- **A kept deny must stay true after the allow list widens.** Before this change, a push asked and a commit fell to the default prompt. Once they are allowed, any form the old denies miss would run with no control. The following are therefore denied:
  - The force refspec `+<ref>`. It is the force push that answer 3 keeps denied, and unlike a `:<ref>` deletion it can be matched; it also covers force-pushing a tag (`+refs/tags/v1`).
  - Git's abbreviated long options (gitcli(7)): a unique prefix such as `--de`, `--m`, `--pru` or `--al` acts as `--delete`, `--mirror`, `--prune` or `--all`.
  - Short-option clusters with the dangerous letter second, such as `-uf` and `-ud`.
  - The amend option in any position and under any unique prefix, because answer 3 keeps the commit amend form.
  - The hook-bypass option of git.md lines 58-59, under its shortest unique prefix and in any Git command, and its commit short form in first position only; after other options or inside a cluster it stays residual.
- **A push with no named destination counts as a direct push to `main`.** Such a push goes where configuration sends it. `push.default` is `current` in this clone (observed 2026-11-14; not tracked), and the primary checkout is on `main`, so a bare push there is a direct push to `main`. The bare forms, the forms that name only a remote or only options that an agent commonly types, `HEAD`, `@`, `--all` and `--branches` are denied; an agent names the branch instead.

## Contracts

- **Allow list.** `permissions.allow` keeps its 20 rules in order and appends nine, in this order: `Bash(git commit *)`, the catch-all push rule (a push rule with argument part `*`, as defined under the deny table below), `Bash(git tag *)`, `Bash(gh pr ready *)`, `Bash(gh pr review --approve*)`, `Bash(gh pr review * --approve*)`, `Bash(gh release *)`, `Bash(gh workflow *)`, `Bash(python3 scripts/release.py *)`. Already allowed and unchanged: `git merge *` (line 16), `gh pr view`, `checks`, `list` and `diff` (lines 17-20), `gh pr create *` (21) and `gh pr merge *` (22).
  - `gh pr review` is allowed for approval only; a request-changes or comment review keeps the default prompt, unless its text contains the text `--approve` after a space (for example `-b "ok --approve"`), which matches the approval rule. That is a review, not a merge, and the guard test records it.
  - GitHub refuses an approving review of one's own pull request, and the review requirement is a count of 0 (git.md lines 96-100; main-protection.md lines 20-23). The approval rule therefore removes a prompt and grants no merge authority.
- **Ask list.** `permissions.ask` becomes `Bash(gh api *)`, `Bash(git -C *)`. `gh api` can reach any endpoint, including a merge or a protection change, and `git -C` puts every Git command out of reach of the prefix rules, so both keep a prompt.
- **Deny list.** `permissions.deny` drops `Bash(gh release create:*)` and `Bash(gh workflow run:*)`. It keeps the other 195 rules unchanged and in order, so forced merge stays denied by `Bash(gh pr merge * --admin*)` and `Bash(gh pr merge --admin*)`, and `gh release delete` (also `delete-asset`) and `gh run cancel` stay denied. Several kept rules become subsets of new ones and still stay, as answer 3 requires. It appends these 62 rules, in this order, for 257 in total. In the first four groups, every pattern in the Rules column is the argument part of a `Bash(...)` push rule: the full rule is `Bash(`, then the Git push command and a space, then the pattern and `)`. The pattern *(none)* stands for the bare push rule, which holds the Git push command alone. `.claude/settings.json` and the tests own the exact strings.

| Group | Rules | Matches | Basis |
| --- | --- | --- | --- |
| Force | `* +*`, `*--for*`, `-f*`, `*-uf*`, `*-qf*`, `*-vf*`, `*-nf*`, `*-4f*`, `*-6f*` | a `+` refspec; `--force`, `--force-with-lease` and `--force-if-includes` and their prefixes in any position; `-f` and clusters that start with `f` (`-fu`); two-letter clusters that end in `f` | answer 3, derived |
| Delete, mirror, prune | `*--de*`, `-d*`, `* -d*`, `*-ud*`, `*-qd*`, `*-vd*`, `*-nd*`, `*-4d*`, `*-6d*`, `*--m*`, `*--pru*` | `--delete` from `--de` on; `-d` and clusters that start or end with `d`; `--mirror` from `--m` on; `--prune` from `--pru` on | answer 3, derived |
| `main` as destination | `* main`, `* main *`, `*:main`, `*:main *`, `*heads/main`, `*heads/main *` | `origin main`, `-u origin main`, `<remote> main`, `main` among several refspecs, `<src>:main`, `HEAD:main`, `:main`, `main:main`, `heads/main`, `refs/heads/main`, `<src>:heads/main` | wordings 4 and 5 |
| Implicit destination | *(none)*, `origin`, `* origin`, `* HEAD`, `* HEAD *`, `* @`, `* @ *`, `*--al*`, `*--b*`, `-u`, `--set-upstream`, `--follow-tags`, `origin -u`, `origin --follow-tags` | a bare push; a push that names only a remote; `HEAD` and `@`; `--all` from `--al` on and `--branches` from `--b` on; the option-only pushes an agent commonly types | wordings 4 and 5, derived |
| Commit and hooks | `Bash(git commit *--am*)`; the hook-bypass rule; the commit short-form rule | `--amend` from `--am` on, in any position; the hook bypass on commit, push and merge under any unique prefix; the commit short form in first position only | answer 3 and git.md lines 58-59, derived |
| Tag force and delete | `Bash(git tag -f*)`, `Bash(git tag * -f*)`, `Bash(git tag *--forc*)`, `Bash(git tag *-af*)`, `Bash(git tag *-ef*)`, `Bash(git tag *-if*)`, `Bash(git tag *-sf*)`, `Bash(git tag -d*)`, `Bash(git tag * -d*)`, `Bash(git tag *--d*)`, `Bash(git tag *-ed*)`, `Bash(git tag *-id*)` | `-f` and clusters that start with `f`, in any position; `--force` from `--forc` on (Git refuses `--f`, `--fo` and `--for` as ambiguous with `--format`); the two-letter clusters `-af`, `-ef`, `-if` and `-sf`; `-d` and clusters that start with `d`, in any position; `--delete` from `--d` on; the two-letter clusters `-ed` and `-id` | answer 7 and git.md line 127, derived |
| Fetch into local tags | `Bash(git fetch *:refs/tags/*)`, `Bash(git fetch *--prune-*)`, `Bash(git fetch -P*)`, `Bash(git fetch * -P*)`, `Bash(git fetch *:tags/*)`, `Bash(git fetch *--stdin*)`, `Bash(git fetch *--refm*)` | a refspec whose destination is written `refs/tags/<name>` or `tags/<name>`, with or without `+` or a force option; `--prune-tags` from `--prune-` on; `-P` and clusters that start with `P`, in any position; refspecs read from standard input (`--stdin`); `--refmap` from `--refm` on (Git refuses `--ref` as ambiguous with `--refetch`) | answers 8 to 10 and git.md line 127 |

- **The two hook-bypass rules.** They are named by reference to git.md line 59 rather than written out, because a local plugin hook refuses shell lines that carry them. The first has the shape of the existing executable-option rule `Bash(git *--upload-pack*)` (settings line 217), with the git.md line 59 option shortened to its shortest prefix that still differs from `--no-verbose` in place of `--upload-pack`. The second is the commit-prefix rule `Bash(git commit` plus a space, the option's one-letter commit short form and `*)`. The implementer writes both with the structured edit tool inside the repository.
- **Matching model.** Matching follows the repository model `_bash_rule_matches` (tests lines 1107-1123): the rule matches the command text from its first character, `*` matches any text, and a trailing `:*` is read as the legacy space-plus-`*` form.
  - Not denied, by design: a source-side `main` (`main:feat/a`, `refs/heads/main:refs/heads/feat/a`); names that only end in `main` (`domain`, `main-fix`, `HEAD:mainline`); `HEAD:<branch>`; `+` inside a name (`feat/a+b`); `-u origin <branch>`, `--set-upstream origin <branch>`, `--follow-tags origin <branch>`, `--dry-run`, `--porcelain`, `--atomic` and `-o <option>` with a named branch; `git commit -am`; a tag message file `-F <file>`, `--format` and `--no-force`; a plain fetch, `git fetch --tags`, `git fetch -p <remote>` and a forced branch fetch (`-f origin main:x`).
  - Over-denied, by design:
    - a bare or `HEAD` push from a feature branch, and a push that writes `--tags` before the remote `origin` (an agent writes the remote `origin` first and `--tags` after it, or names the tag);
    - `--force-if-includes` on its own;
    - a branch whose name contains `heads/main`, `--de`, `--m`, `--al`, `--b`, `--for`, `--pru`, or a two-letter cluster such as `-ud`, `-nf` or `-uf` (`feat/heads/main`, `feat/x-udp`, `feat/a--demo`, and realistic infrastructure names such as `feat/add-nfs` and `feat/add-ufw`); rename such a branch before pushing it;
    - a push option whose text contains ` main `, ` HEAD ` or ` @ `;
    - a commit message whose text contains `--am` or the hook-bypass prefix;
    - a fetch whose text contains `:refs/tags/`, `:tags/`, `-P` after a space or `--prune-`, including an explicit tag-sync refspec `refs/tags/*:refs/tags/*` given without force or pruning, and a fetch that creates a new tag through a `tags/<name>` destination (`main:tags/x`); and any fetch with `--stdin` or `--refm`, whatever its refspecs;
    - a tag name, list pattern or tag message whose text contains `-f` or `-d` after a space, or `--d`, `--forc`, `-af`, `-ef`, `-if`, `-sf`, `-ed` or `-id` (`feat-edit`, `v1-idp`, or a `main-<sha>` tag whose SHA starts with `af`, `ef` or `ed`); rename the tag or reword the message.
  - While drafting, these lists were checked as follows. These are drafting inputs only; the Task re-runs them as tests.
    - A scratch probe under that model classified about 100 commands with these results.
    - Dry runs of Git 2.43 against a scratch bare remote showed `--de`, `--m`, `--mi`, `--pru`, `--al`, `--b`, `--force-w`, `-uf` and `-ud` acting as the full options, `@` resolving to `refs/heads/main`, and `--d`, `--pr` and `--for` refused as ambiguous.
    - `heads/main` resolving to `refs/heads/main` follows git-push(1) destination matching; the scratch output for it was cut off and is not evidence.
    - For the tag group (answer 7), dry runs of Git 2.43 against scratch repositories, recorded in the Task, showed:
      - `--d`, `--del`, `--forc`, `-fa`, `-fe`, `-fi`, `-af`, `-ef`, `-if`, `-ed`, `-id` and `-aef` acting as force or delete;
      - `--f`, `--fo` and `--for` refused as ambiguous with `--format`;
      - `-df`, `-fd`, `-ad`, `-sd`, `-vd`, `-ld`, `-lf`, `-vf`, `-nf` and `-nd` refused;
      - `-sf` parsed and stopped only for lack of a signing key;
      - `-ied` deleted the tag.
    - For the fetch group (answer 8), dry runs of Git 2.43 against scratch repositories, recorded in the Task, showed:
      - a `refs/tags/` destination with `+`, `-f` or `--forc` moving a tag;
      - `--prune-tags`, `--prune-t`, `-P`, `-P -p`, `-Pp`, and `-p` with a `refs/tags/*:refs/tags/*` refspec deleting one;
      - forms the answer 8 rules missed included: a destination written `tags/<name>` and `--prune-`, both denied under answer 9, and `-pP`, a forced tag fetch (`-f --tags`, `--tags -f`, `-ft`) and a forced `tag <name>` refspec;
      - `main:tags/x` creating a new tag `refs/tags/x` without moving `v1`;
      - a plain fetch, `--tags` alone, `-p` alone and `-f <remote> main:x` leaving the tag unchanged;
      - for answer 10, `--stdin` with a `+refs/tags/v1:refs/tags/v1` refspec file and `--refmap='+refs/*:refs/*'` (also as `--refm`) moving a tag, and `--ref` refused as ambiguous with `--refetch`;
      - still missed: the glob refspecs `'+refs/*:refs/*'` (from a detached HEAD) and `'+refs/t*:refs/t*'` moving a tag, `-p` with `'refs/t*:refs/t*'` deleting one, and a shell-quoted destination `+main:"refs/tags/v1"` moving one.
- **Residual risk.** The following now run without a prompt, and this package does not claim to cover them:
  - Forbidden by policy but not denied, after the user's answers:
    - Tag rewrites that no deny rule matches stand against git.md line 127 (tags are immutable history) and ADR-0048 (publication never moves tags). Examples, not a complete list:
      - a `git tag` cluster of three or more letters in which `f` or `d` is neither first nor second (`-aef`, `-ied`);
      - a remote tag deletion through the refspec `:refs/tags/<tag>`;
      - fetch forms that the fetch rules miss: a cluster with `P` after its first letter (`-pP`), a forced tag fetch (`-f --tags`, `-ft`), a forced `tag <name>` refspec, a glob refspec whose destination covers `refs/tags/` (`'+refs/*:refs/*'`, `'refs/t*:refs/t*'`, with `-p` also deleting) and a quoted or split destination;
      - a tag refspec or tag pruning set in configuration (`remote.<name>.fetch`, `fetch.pruneTags`, `remote.<name>.pruneTags`), which a plain or pruning fetch then applies.

      A remote tag rewrite is still refused when it uses a force or delete option or `+`.
    - A Release or tag made without the producer, through a direct `gh release create`, `gh release edit` or `gh release upload`, or a `v` tag pushed by name or with `--tags`, against the amended git.md release rule and ADR-0048 lines 146-147.
    - `gh workflow enable` and `disable`, which change a remote setting against `.github/AGENTS.md` rule 9.
  - Code that the allowed commands run:
    - `python3 scripts/release.py *` runs whatever that working-tree file contains. An agent that edits the file and then runs it executes that code without a prompt.
    - Commit, push and merge commands run the repository's Git hooks (through `scripts/githooks/chained-hook.sh` and the workspace hooks it chains) without a prompt.
  - Not matchable by any pattern:
    - A refspec deletion of a branch or tag other than `main` (for example, a refspec deletion of `feat/a` on the remote `origin`). A rule ending in `:*` is read as the legacy prefix form (tests lines 1366-1368), so no pattern can express the deletion.
    - Short-option clusters of three or more letters in which `f` or `d` is neither first nor second (`-uvf`, `-vuf`, `-qud`, and the tag clusters `-aef` and `-ied`). The rules cannot express "any cluster containing f".
    - The commit short form of the hook bypass after other options or inside a cluster (`-an`). A pattern for it would also refuse ordinary commit messages.
    - In every rule group above, push, tag, fetch, commit and the others alike, a quoted, escaped or variable argument, including an option (`"main"`, `$BRANCH`, `"--force"`): the rules match the command text, not the arguments the shell passes.
    - Pushes whose only arguments are options other than the exact forms denied (a push whose only argument is `-q` or `-v`); a revision suffix (`main~0`); a glob refspec (`'refs/heads/*'`); a bare push to a remote other than `origin`; and destinations set by `remote.<name>.push` or `push.default`.
  - Not matched by a deny, and unprompted only where they also match an allow rule: option-first forms such as `gh release --repo <r> delete`. Aliases, `bash -c`, scripts and other programs that run Git themselves match no allow rule, so they fall to the default prompt. `git -C` and `gh api` keep their prompt.
- **What mitigates the residual risk, as far as the repository evidences.**
  - Every push force, delete, mirror and prune form that a pattern can express stays denied: the kept rules (settings lines 83-86, 184-189, 226-228), the unique-prefix rules, and the two-letter clusters above. The longer clusters stay residual.
  - `git reflog expire` and `git gc --prune` stay denied (204-205), so a remote branch deleted or overwritten from a checkout can be pushed again from that checkout's branch or reflog.
  - Git.md lines 67-69 still require explicit approval for each force push, branch deletion or amend, and work-lifecycle line 122 forbids inferring push or merge approval.
  - Remote `main` protection is intended to require pull requests, block force pushes and deletion, and enforce administrators (main-protection.md lines 19, 27, 28 and 41-43). A read-back on 2026-11-11T23:46Z observed force push and deletion disabled, administrators enforced, strict required contexts, merge commits only and 0 required reviews (SPEC-0161 Task lines 230 and 235). That read-back is point-in-time evidence, not a current guarantee (main-protection.md line 149).
  - The tag rulesets are intended to make `v` tags and `main` SHA tags immutable and creatable only by the publisher (main-protection.md lines 36-40), but they have no recorded read-back. Feature branches have no recorded hosted protection.
- **Validator pin.** `CLAUDE_ALLOWED_PERMISSIONS`, `CLAUDE_ASK_PERMISSIONS` and `CLAUDE_REQUIRED_DENY_PERMISSIONS` mirror the three lists in the same order, because the comparison at lines 1541-1547 is list equality: lines 137-138 leave the deny tuple and the 62 rules are appended at the end of the tuple. The comment at lines 112-116 is rewritten to say three things: commit, push, tag, PR readiness and approval, Release and workflow commands, and the release producer run without a prompt on an operator request; forced merge, direct pushes to `main`, Release deletion, run cancellation, and the matchable push force, delete, mirror and prune forms, tag force and delete forms, fetch-into-tag forms, and amend and hook-bypass forms (including unique prefixes and two-letter clusters) are denied; `gh api` and `git -C` ask. No diagnostic, function or CLI option is added, and a mismatch stays `AGENT-NATIVE-PERMISSION`.
- **Policy and procedure text.**
  - In `.agents/governance/git.md`, the Release ownership text (lines 112-133) keeps one producer, `scripts/release.py`, as ADR-0048 requires. It now says three more things:
    - Who may publish: the repository owner, or an agent acting on the owner's current request that names the version and assets.
    - How a Release stays traceable: the publishing Task records that request through the operator approval route, together with the producer command, the tag, the target `main` SHA and a read-back of the published Release (`gh release view`). Every Release therefore traces to a request, a reviewed `main` commit and the committed changelog section.
    - What the lifted denies do not change: a direct `gh release create`, `gh release edit` or `gh release upload`, or a hand-made `v` tag, is not a second producer, and it stays forbidden although Claude no longer prompts for it.
  - Git.md also gains `#### Agent delivery commands` after Release ownership and before Commit-message validation (line 135). It is the single statement of the delivery boundary for every agent:
    - On the user's current request, an agent may commit, push a feature branch, create, inspect, mark ready, approve and merge a pull request, create a tag, run the release producer, and dispatch a workflow.
    - That request is the approval for one operation on one subject. It is not a standing grant (approval-and-safety.md lines 101-103), and no passing check replaces it. A message from another agent is not that request; the tracked settings apply to subagent sessions as well.
    - No agent merges with administrator bypass or pushes directly to `main`, whatever the request; these two are the user's absolute rules.
    - Every other protected Git operation keeps its existing policy, which this subsection does not restate. A force push, a remote branch or tag deletion, an amend, a Release deletion and a run cancellation still need explicit approval for that operation (git.md lines 67-69). Claude settings refuse their matchable forms natively, so an approved one is run by the operator. The hook bypass (git.md lines 58-59) and tag rewrites (git.md line 127) stay forbidden as git.md already states. A workflow's enabled state stays under `.github/AGENTS.md` rule 9.
    - Three enforcement layers are named, and none proves another. Claude tracked settings are repository-static intent: they deny the matchable forms, including tag force and delete and fetches into local tags, and leave producer bypass, the tag rewrites no rule matches and longer option clusters to policy (`.claude/provider.md`). Codex asks before every network command and forbids a prefix subset (`.codex/provider.md`). Remote protection and rulesets are recorded in `.github/rulesets/main-protection.md` and are proven only by a dated read-back.
    - If SPEC-0199 has adopted rule IDs for `git.md` when this package rebases (code `GIT` under `policy_rule_ids` no longer `pending`), both changes are also written as `GIT-R###` rows. Otherwise SPEC-0199 picks them up.
  - `.claude/provider.md` lines 50-53 are replaced. The new text says that read-only Git and GitHub commands, commit, push, tag, pull request creation, readiness, approval and merge, Release and workflow commands, and the release producer are allowed because an operator request is their approval. It says that `gh api` and `git -C` ask and that the deny list carries the groups above, plus Release deletion and run cancellation. It names the residual list, including what policy forbids but no rule denies and the code that allowed commands run, and links the git.md subsection. Lines 55-56, on programs that open files themselves and text-obfuscated paths, stay.
  - `.codex/provider.md` lines 63-64 currently say that the rules forbid "a subset of the command families the Claude deny list covers". After this change that is no longer true, because Codex forbids `gh release create` and `gh workflow run` (rules lines 72-73), which Claude now allows. The sentence becomes: Codex forbids a subset of the Claude deny families plus those two, so Codex is stricter there. The rules file's header comment (line 2) is left as written, because the file is digest-pinned and the Codex rules stay unchanged; the provider note carries the exact relation.
  - Runbook 0012, lines 35-38, Step 5 of the Actions table (line 66) and lines 112-116: the executor of `publish --execute` becomes the operator or an agent acting on the operator's current request that names the version and assets. The separate approval is that request, recorded through the operator approval route, and the remote checks are unchanged. `--execute` keeps its operator-approved boundary marker (Stage 05 rule 3).
  - `scripts/README.md` line 94, the `release.py` row, calls `publish --execute` operator work. It says instead that the operator, or an agent on the operator's current request that names the version and assets, runs it as an operator-approved step.
  - Unchanged, with the reason:
    - `approval-and-safety.md` line 52 already lists push, PR creation and merge as approval boundaries, and line 51 lists publishing and remote dispatch. An operator request is that approval, as it already is for the allowed `gh pr create` and `gh pr merge`, and lines 101-103 still forbid reusing an old approval.
    - `quality.md` Delivery ownership (lines 277-291) routes evidence, not permission.
    - GDE-0010 and `.github/AGENTS.md` carry no permission statement that this change contradicts; rule 9 of the latter is the policy that the residual `gh workflow enable` and `disable` would breach.
- **Failing-first regressions.**
  - `test_delivery_commands_are_allowed_and_raw_api_asks` (tests lines 1261-1311):
    - Feature-branch pushes (including `-u origin <branch>`, `--set-upstream origin <branch>` and `--follow-tags origin <branch>`), commit, `git commit -am`, tag creation, `gh pr ready`, both approval orders, `gh release create`, `gh workflow run` and the release producer move to the `allow` expectations.
    - `git -C sub push origin main` and `gh api` stay `ask`.
    - The forced-merge, `main`, `heads/main`, implicit-destination, `@`, option-only, force-refspec, amend and hook-bypass cases are `deny`, and so are `gh release delete`, `gh release delete-asset` and `gh run cancel`.
    - Each unique-prefix and two-letter cluster case is `deny`: `--del`, `--de`, `--dele` after the refspec, `--mirr`, `--m`, `--pru` in both positions, `--forc`, `--force-w` in both positions, `-fu`, `-uf`, `-qf`, `-vf`, `-nf`, `-ud`, `-du`, `-qd` after the remote, `--al`, `--b`, `--branches`, `--amen` in both positions and `--am`.
    - For answer 7, the tag force cases `-f`, `-fa`, `-a -f`, `-m a -f`, `--forc`, `--force`, `-af`, `-ef`, `-if`, `-sf` and `-m a -af` and the tag delete cases `-d`, `--d`, `--del`, `--delete`, `-i -d`, `-ed` and `-id` are `deny`. A tag created with `-F <file>` and a listing with `--format` are over-match guards asserted `allow`. A tag named `main-ef0123` and a tag message containing `-f` after a space are over-denials asserted `deny`. Against the settings before answer 7, these 20 deny expectations fail, because those settings decided `allow`.
    - For answer 8, the fetch cases are `deny`:
      - a `refs/tags/` destination with `+`, `-f` or `--forc`;
      - `+refs/tags/v1:refs/tags/v1`;
      - `-p` with `refs/tags/*:refs/tags/*`;
      - `--prune-tags`, `--prune-t`, `-P`, `-P -p`, `-Pp` and `-p -P`.

      A plain fetch, `--tags` with and without a remote, `-p <remote>` and `-f origin main:x` are guards asserted `allow`. An explicit `refs/tags/*:refs/tags/*` refspec without force or pruning is an over-denial asserted `deny`. Against the settings before answer 8, these 12 deny expectations fail, because those settings decided `allow`.
    - For answer 9, `-f . HEAD:tags/v1`, `. +HEAD:tags/v1` and `--prune- origin` move from the residual `allow` expectations to `deny`. `main:tags/x`, which creates a new tag, is an over-denial asserted `deny`. Against the settings before answer 9, these 4 deny expectations fail, because those settings decided `allow`.
    - For answer 10, `--stdin origin < refs.txt`, `--refmap='+refs/*:refs/*' origin refs/tags/v1` and the same with `--refm` are `deny`. Against the settings before answer 10, these 3 deny expectations fail, because those settings decided `allow`.
    - The over-match guards above are `allow`, and the documented over-denials are `deny`.
    - A guard asserts that `gh pr review 1 --request-changes -b "ok --approve"` is `allow`, while `-b "--approve"` falls to the default prompt.
    - A refspec deletion of `feat/a` on the remote `origin`, a push of `x` to `origin` with the cluster `-uvf`, a push whose only argument is `-q`, a commit that carries the short hook-bypass form after other options or inside a cluster (`-an`), the three-letter tag clusters `git tag -aef v1 -m a` and `git tag -ied v1`, and the fetch residuals (`-pP`, `-f --tags`, `-ft`, a forced `tag v1` refspec, the glob refspecs `'+refs/*:refs/*'`, `'+refs/t*:refs/t*'` and `-p` with `'refs/t*:refs/t*'`, and the quoted destination `+main:"refs/tags/v1"`) are asserted `allow` under a comment naming each as a recorded residual, so a later change has to update the test on purpose.
    - The SPEC-0114 comment at lines 1292-1293 is rewritten.
    - Against the current settings, each new `allow` and `deny` expectation fails, because today it decides `ask`, `deny` or the default prompt.
  - `test_lost_native_denial_and_wildcard_allow_reject` (lines 727-747) gains three mutations, each rejected with `AGENT-NATIVE-PERMISSION`: the catch-all push rule (argument part `*`) moved back to ask, the push rule with argument part `* main` removed, and `Bash(gh pr merge * --admin*)` removed. Before the change, the first two fail because the rule they act on is absent. The forced-merge mutation already passes and is recorded as a regression, not as failing-first.
  - `test_deletion_and_history_destruction_is_denied` keeps `gh release delete v1` and `gh run cancel 1` (tests lines 1355-1356) unchanged. No current test asserts the two lifted denies.
  - Whole validator: with the new pin and the old settings, `python3 scripts/validate-agent-governance.py --root .` exits non-zero with `AGENT-NATIVE-PERMISSION`; with the new settings it passes.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view and its release-production row (line 72: one SemVer tag and Release producer, and publication remains an authorized external operation). ADR-0048 lines 146-147 make `scripts/release.py` the sole SemVer tag and GitHub Release producer, and ADR-0052 line 39 keeps releases as tags on reviewed `main` commits. This change stays within all three. It lifts a native permission and amends who may run the producer and how its output is traced, but it creates no second producer. Making a direct `gh release create` a sanctioned publication path would be a departure that needs an ADR-0048 amendment first, and this package does not make it. No component changes. The change is configuration plus its pin and tests: the tracked settings hold the single list, the validator holds the reviewed copy, and the tests decide commands with the same matcher model. How a running Claude client matches the rules is separate runtime evidence (REQ-0003-FR-0009) and is not claimed.

## Data Modeling & Storage Strategy

No data changes. The settings file keeps its shape: three lists plus `disableBypassPermissionsMode: "disable"` (line 230).

## Interfaces & Data Structures

No new interface. The `.claude/settings.json` lists change as above, the validator CLI and its diagnostics are unchanged, and the test module stays in its suite (`agent-governance`, `scripts/run-contract-tests.py` line 76). The release entrypoint is the documented `python3 scripts/release.py --root . {prepare,publish} --version vX.Y.Z ...` (runbook 0012 lines 90-92 and 115; CLI at `scripts/release.py` lines 671-698).

## Edge Cases & Error Handling

- A deny always wins over an allow or an ask, and no allow can override a deny (provider note lines 45-46).
- A command that matches both a new allow and a kept deny is denied (`gh release delete`, `gh run cancel`, the commit amend form, the tag force and delete forms, the fetch-into-tag forms).
- An ambiguous abbreviation (for push `--d`, `--pr` and `--for`; for tags `--f`, `--fo` and `--for`) is refused by Git itself. The deny list covers the unique push and tag ones and, for fetch, `--prune-tags` from `--prune-` on and `--refmap` from `--refm` on.
- The client judges a compound shell line; the test model judges one command, and the Task records only what the tests and the validator decide.
- If the deny list misses a push but hosted protection refuses it, the push fails remotely. The agent stops and reports, and never retries with a force, bypass or `gh api` form.

## Failure Modes & Fallback / Human Escalation

If a later session shows the client matching a rule differently from the model, the observation is recorded in that session's Task, and either the rule is narrowed or the residual is recorded; no allow is widened to compensate. If an agent finds that a requested operation is forbidden by policy but not denied (a tag rewrite, a Release made outside the producer, or an option form the deny list cannot express), it stops and asks the user rather than relying on the missing prompt. Rollback is a revert of the implementation commit:

- push returns to ask, and commit, tag, review, release and workflow commands return to the default prompt;
- the `gh release create` and `gh workflow run` denies return;
- the added denies, the git.md text, both provider-note sentences, the runbook lines and the scripts README row leave together.

## Verification Commands

- `python3 scripts/validate-agent-governance.py --root .`: fails first with the new pin and the old settings, then passes.
- `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry` and `python3 scripts/run-contract-tests.py --root . --suite agent-governance`.
- The four strict document validators of `docs/AGENTS.md` rule 8 over the tree, before and after the change, and `python3 scripts/validate-document-lifecycle.py --root . --mode staged`.
- `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `ruff format --check scripts tests`, `python3 scripts/qa.py staged` and the commit hooks on the exact index.
- Evidence limit: all of these are repository-static. They do not establish native rule matching or hosted protection.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-DELIVERYPERM-001 | The three lists equal the Contracts: 29 allow, 2 ask and 257 deny. Exactly `Bash(gh release create:*)` and `Bash(gh workflow run:*)` leave the deny list, every other pre-existing deny is present and in order, the validator pin mirrors the lists, and the whole validator and the named mutations fail first and then pass. |
| VAL-DELIVERYPERM-002 | The decision regressions pass for every allow, ask, deny, unique-prefix, cluster, over-match guard and recorded residual case. The git.md release text and subsection, both provider-note sentences, the runbook lines and the `scripts/README.md` `release.py` row state the boundary once, keep one release producer, limit the absolute ban to forced merge and direct pushes to `main`, and keep the three enforcement layers apart. The strict document validators, affected-surface routing, ruff, exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DELIVERYPERM-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Governance validator and mutation tests, failing first. |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DELIVERYPERM-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Decision regressions, strict document validators, and review of the statement that keeps static and hosted controls apart. |
