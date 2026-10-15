import os
import re
import stat
import subprocess
import sys
import tomllib

base_sha = os.environ.get("BASE_SHA", "")
head_sha = os.environ.get("HEAD_SHA", "")
merge_sha = os.environ.get("MERGE_SHA", "")
title = os.environ.get("PR_TITLE", "")
if any(
    re.fullmatch(r"[0-9a-f]{40}", sha) is None
    for sha in (base_sha, head_sha, merge_sha)
):
    sys.exit("invalid pull request commit identity")
actual = subprocess.run(
    ["git", "-C", "trusted-base", "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
    timeout=10,
).stdout.strip()
if actual != base_sha:
    sys.exit("reviewed base identity mismatch")


def git(*args):
    return subprocess.run(
        ["git", "-C", "candidate-commits", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=15,
    ).stdout


if git("rev-parse", "HEAD").decode("ascii").strip() != merge_sha:
    sys.exit("pull request merge identity mismatch")
if git("rev-parse", "HEAD^1").decode("ascii").strip() != base_sha:
    sys.exit("pull request base parent mismatch")
if git("rev-parse", "HEAD^2").decode("ascii").strip() != head_sha:
    sys.exit("pull request head parent mismatch")
merge_size = git("cat-file", "-s", "HEAD").decode("ascii").strip()
if not merge_size.isdecimal() or int(merge_size) > 65536:
    sys.exit("pull request merge object is invalid or oversized")
merge_headers = git("cat-file", "commit", "HEAD").partition(b"\n\n")[0]
if sum(line.startswith(b"parent ") for line in merge_headers.splitlines()) != 2:
    sys.exit("pull request merge must have exactly two parents")
if git("rev-parse", "--is-shallow-repository").strip() != b"false":
    sys.exit("pull request history is shallow")
fd = os.open("trusted-base/.cz.toml", os.O_RDONLY | os.O_NOFOLLOW)
try:
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
        sys.exit("reviewed message configuration must be a bounded regular file")
    content = os.read(fd, 65537)
finally:
    os.close(fd)
if len(content) > 65536:
    sys.exit("reviewed message configuration exceeds the input bound")
config = tomllib.loads(content.decode("utf-8"))
commitizen = config["tool"]["commitizen"]
grammar = commitizen["customize"]
pattern = grammar["schema_pattern"]
if not isinstance(pattern, str) or not title or "\n" in title or "\r" in title:
    sys.exit("PR title must be one Conventional Commit subject line")
if re.fullmatch(pattern, title) is None:
    sys.exit("PR title does not match the reviewed message schema")
print("pr-title result=validated verdict=PASS")
patterns = {
    name: re.compile(grammar[name])
    for name in (
        "schema_pattern",
        "commit_parser",
        "generated_merge_pattern",
        "generated_revert_pattern",
    )
}
prefixes = commitizen["allowed_prefixes"]
if not isinstance(prefixes, list) or not all(
    isinstance(p, str) and p for p in prefixes
):
    sys.exit("invalid reviewed generated-message prefixes")
commits = (
    git("rev-list", "--max-count=257", f"{base_sha}..{head_sha}")
    .decode("ascii")
    .splitlines()
)
if (
    not commits
    or len(commits) > 256
    or head_sha not in commits
    or any(re.fullmatch(r"[0-9a-f]{40}", sha) is None for sha in commits)
):
    sys.exit("pull request commit range is empty, invalid, or exceeds 256 commits")
for sha in commits:
    size_text = git("cat-file", "-s", sha).decode("ascii").strip()
    if not size_text.isdecimal() or int(size_text) > 65536:
        sys.exit(f"commit object is invalid or exceeds 65536 bytes: {sha}")
    raw = git("cat-file", "commit", sha)
    if len(raw) != int(size_text):
        sys.exit(f"commit object size mismatch: {sha}")
    headers, separator, body = raw.partition(b"\n\n")
    if not separator:
        sys.exit(f"commit message is missing: {sha}")
    message = body.decode("utf-8").rstrip("\n")
    parents = sum(line.startswith(b"parent ") for line in headers.splitlines())
    authored = patterns["schema_pattern"].fullmatch(message) and patterns[
        "commit_parser"
    ].fullmatch(message)
    generated_merge = (
        "Merge" in prefixes
        and parents >= 2
        and patterns["generated_merge_pattern"].fullmatch(message)
    )
    generated_revert = "Revert" in prefixes and patterns[
        "generated_revert_pattern"
    ].fullmatch(message)
    if not (authored or generated_merge or generated_revert):
        sys.exit(f"commit message does not match the reviewed schema: {sha}")
print(f"pr-commits result=validated verdict=PASS count={len(commits)}")
