"""One audited stdlib-only gate: immutable runtime, exact tree, bounded source lookup."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

GATE = "agent-evaluation-cases"
IMAGE = "docker.io/library/python@sha256:c90be507635af19768837aa7eeb2f4ce89a74d62962a335497b9df8edfb7f19d"
RUNTIME = {
    "image": IMAGE,
    "platform": "linux/amd64",
    "python": "/usr/local/bin/python3",
    "version": "3.12.14",
}
ARGV = ["python3", ".agents/evaluations/run-agent-evaluations.py", "--root", "."]
ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/local/bin:/usr/bin:/bin",
    "TZ": "UTC",
    "NO_COLOR": "1",
}
HOSTED = {**RUNTIME, "inputs": "committed-tree-v1"}
FULL_STEP = "Validate repository checkout"
COMPLEMENT_STEP = "Validate repository complement"
ISOLATED_STEP = "Validate isolated repository gate"
PUSH_PREFIX = "Locate PR proof for push "
FILE_LIMIT = 8 * 1024 * 1024


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def partition(registry, name):
    full = registry["profiles"]["full"]
    require(
        registry["profileAliases"]["ci"] == "full" and len(full) == len(set(full)),
        "invalid full profile",
    )
    validators = {row["id"]: row for row in registry["validators"]}
    isolated = [key for key in full if validators[key].get("reuse", {}).get("hosted")]
    require(isolated == [GATE], "unaudited isolated gate")
    gate = validators[GATE]
    require(
        gate["reuse"]["hosted"] == HOSTED
        and gate["argv"] == ARGV
        and gate["optional"] is False,
        "changed isolated contract",
    )
    require(name in ("isolated", "complement"), "invalid partition")
    return (
        isolated if name == "isolated" else [key for key in full if key not in isolated]
    )


def git(root, *arguments):
    root = Path(root).resolve(strict=True)
    env = {
        **ENVIRONMENT,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    result = subprocess.run(
        [
            "/usr/bin/git",
            "-c",
            f"safe.directory={root}",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "core.fsmonitor=false",
            *arguments,
        ],
        cwd=root,
        env=env,
        capture_output=True,
        timeout=30,
        check=True,
    )
    require(len(result.stdout) <= 16 * 1024 * 1024, "Git output exceeds bound")
    return result.stdout


def stable_leaf_state(metadata):
    return (
        metadata.st_mode,
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_nlink,
        metadata.st_uid,
        metadata.st_gid,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def raw_leaf(root, path):
    parts = PurePosixPath(path).parts
    require(
        parts
        and str(PurePosixPath(path)) == path
        and not path.startswith("/")
        and not any(p in (".", "..", ".git") for p in parts),
        "unsafe committed path",
    )
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor
            )
            os.close(descriptor)
            descriptor = child
        metadata = os.stat(parts[-1], dir_fd=descriptor, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode):
            target = os.readlink(parts[-1], dir_fd=descriptor)
            require(
                not os.path.isabs(target)
                and (root / path).resolve().is_relative_to(root),
                "escaping committed symlink",
            )
            require(
                stable_leaf_state(metadata)
                == stable_leaf_state(
                    os.stat(parts[-1], dir_fd=descriptor, follow_symlinks=False)
                ),
                "committed symlink changed",
            )
            return "120000", os.fsencode(target)
        require(stat.S_ISREG(metadata.st_mode), "unsafe committed file")
        leaf = os.open(
            parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor
        )
        with os.fdopen(leaf, "rb") as source:
            before = os.fstat(source.fileno())
            require(
                stat.S_ISREG(before.st_mode) and before.st_size <= FILE_LIMIT,
                "committed file exceeds bound",
            )
            payload = source.read(FILE_LIMIT + 1)
            require(
                stable_leaf_state(before)
                == stable_leaf_state(os.fstat(source.fileno()))
                and stable_leaf_state(before)
                == stable_leaf_state(
                    os.stat(parts[-1], dir_fd=descriptor, follow_symlinks=False)
                )
                and len(payload) <= FILE_LIMIT,
                "committed input changed",
            )
        return ("100755" if before.st_mode & stat.S_IXUSR else "100644"), payload
    finally:
        os.close(descriptor)


def require_committed_checkout(root, expected):
    root = root.resolve()
    require(
        re.fullmatch(r"[0-9a-f]{40}", expected)
        and git(root, "rev-parse", "HEAD").decode().strip() == expected,
        "wrong committed checkout",
    )
    require(not git(root, "ls-files", "--others", "-z"), "untracked committed input")
    require(
        not git(root, "diff", "--cached", "--name-only", "-z", expected, "--"),
        "index differs from committed tree",
    )
    entries = git(root, "ls-tree", "-r", "-z", expected).split(b"\0")
    for entry in filter(None, entries):
        metadata, path = entry.split(b"\t", 1)
        mode, kind, identity = metadata.decode().split()
        require(
            kind == "blob" and mode in ("100644", "100755", "120000"),
            "unsafe committed mode",
        )
        actual_mode, payload = raw_leaf(root, os.fsdecode(path))
        observed = hashlib.sha1(
            b"blob " + str(len(payload)).encode() + b"\0" + payload
        ).hexdigest()
        require(
            mode == actual_mode and identity == observed,
            "raw checkout differs from committed tree",
        )
    require(
        git(root, "rev-parse", "HEAD").decode().strip() == expected,
        "committed checkout moved",
    )


def effective_argv():
    return [RUNTIME["python"], "-I", "-B", *ARGV[1:]]


def isolated(root, expected):
    require(
        sys.executable == RUNTIME["python"]
        and sys.version.split()[0] == RUNTIME["version"],
        "wrong isolated interpreter",
    )
    require_committed_checkout(root, expected)
    registry = json.loads((root / "scripts/validation/registry.json").read_bytes())
    partition(registry, "isolated")
    result = subprocess.run(
        effective_argv(), cwd=root, env=ENVIRONMENT, timeout=120, check=False
    )
    require_committed_checkout(root, expected)
    return result.returncode


def input_identity(tree, registry_blob, workflow_blob, lock_blob):
    data = {
        "tree": tree,
        "registry": registry_blob,
        "workflow": workflow_blob,
        "lock": lock_blob,
        "runtime": RUNTIME,
        "argv": effective_argv(),
        "environment": ENVIRONMENT,
    }
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def steps(job):
    rows = job["steps"]
    require(
        0 < len(rows) <= 100 and len({row["number"] for row in rows}) == len(rows),
        "invalid job steps",
    )
    require(
        all(type(row["number"]) is int and 0 < row["number"] <= 10000 for row in rows),
        "invalid step number",
    )
    return rows


def successful(value):
    require(
        value["status"] == "completed" and value["conclusion"] == "success",
        "hosted source failed",
    )


def step(job, name):
    selected = [row for row in steps(job) if row["name"] == name]
    require(len(selected) == 1, "missing or ambiguous hosted step")
    successful(selected[0])
    return selected[0]


def job_partition(core, run, github, *, main):
    run_id, attempt = run["id"], run["run_attempt"]
    rows = github.pages(f"actions/runs/{run_id}/attempts/{attempt}/jobs", field="jobs")
    names = {"qa", "branch-policy", "ci-summary", "qa-isolated", "qa-source"}
    require(
        len(rows) == len(names)
        and {row["name"] for row in rows} == names
        and len({core.positive(row["id"]) for row in rows}) == len(rows),
        "ambiguous hosted jobs",
    )
    jobs = {row["name"]: row for row in rows}
    for name, row in jobs.items():
        require(
            row["run_id"] == run_id
            and row["run_attempt"] == attempt
            and row["head_sha"] == run["head_sha"],
            "wrong hosted job source",
        )
        if name in ({"branch-policy", "qa-isolated"} if main else {"qa-source"}):
            require(
                row["status"] == "completed" and row["conclusion"] == "skipped",
                "unexpected hosted job",
            )
        elif name == "qa-source" and main:
            require(
                row["status"] == "completed"
                and row["conclusion"] in ("success", "skipped"),
                "failed lookup job",
            )
        else:
            successful(row)
    qa = jobs["qa"]
    checkouts = [
        row for row in steps(qa) if row["name"].startswith(core.CHECKOUT_PREFIX)
    ]
    require(len(checkouts) == 1, "ambiguous checkout")
    checkout = checkouts[0]
    successful(checkout)
    commit = core.sha(checkout["name"][len(core.CHECKOUT_PREFIX) :])
    aggregate = [
        row
        for row in steps(qa)
        if row["name"] in (FULL_STEP, COMPLEMENT_STEP)
        or row["name"].startswith("Reuse isolated gate ")
    ]
    require(len(aggregate) == 3, "incomplete partition steps")
    passed = [row for row in aggregate if row["conclusion"] == "success"]
    require(
        len(passed) == 1
        and all(
            row["status"] == "completed" and row["conclusion"] in ("success", "skipped")
            for row in aggregate
        ),
        "partition executed twice or failed",
    )
    require(checkout["number"] < passed[0]["number"], "wrong checkout order")
    mode = passed[0]["name"]
    require(
        mode != COMPLEMENT_STEP if main else mode == COMPLEMENT_STEP,
        "wrong event partition",
    )
    if not main:
        isolated = jobs["qa-isolated"]
        isolated_checkout = step(isolated, core.CHECKOUT_PREFIX + commit)
        executed = step(isolated, ISOLATED_STEP)
        require(
            isolated_checkout["number"] < executed["number"],
            "wrong isolated checkout order",
        )
    return jobs, commit, mode


def isolated_record(core, github, baseline, jobs, commit):
    return {
        "gate": GATE,
        "job": core.positive(jobs["qa-isolated"]["id"]),
        "runtime": RUNTIME,
        "input": input_identity(
            commit["tree"]["sha"],
            baseline[core.REGISTRY_PATH][1],
            baseline[core.CI_PATH][1],
            baseline[core.LOCK_PATH][1],
        ),
    }


def source_text(proof):
    source = proof.record["source"]
    isolated = proof.record["isolated"]
    return f"{source['run']}:{source['attempt']}:{isolated['job']}:{isolated['input']}"


def source_for_main(core, github, before, after, app_id):
    before, after = core.sha(before), core.sha(after)
    current = github.commit(after)
    baseline = github.controls(github.commit(github.baseline))
    require(
        github.controls(current) == baseline
        and github.controls(github.commit(before)) == baseline,
        "changed main control closure",
    )
    comparison = github.get(f"compare/{before}...{after}")
    require(
        comparison["status"] == "ahead"
        and comparison["merge_base_commit"]["sha"] == before,
        "push base is not an ancestor",
    )
    count, commits = core.positive(comparison["total_commits"]), comparison["commits"]
    require(
        count <= core.MAX_COMMITS
        and len(commits) == count
        and commits[-1]["sha"] == after
        and len({row["sha"] for row in commits}) == count,
        "incomplete push history",
    )
    for commit in commits:
        require(
            github.controls(github.commit(core.sha(commit["sha"]))) == baseline,
            "push changes protected control closure",
        )
    pulls = github.pages(f"commits/{after}/pulls")
    require(len(pulls) == 1, "ambiguous integrated PR")
    pr = github.get(f"pulls/{core.positive(pulls[0]['number'])}")
    require(
        pr["state"] == "closed"
        and pr["merged"] is True
        and pr["merge_commit_sha"] == after
        and pr["base"]["ref"] == "main"
        and core.repo_matches(pr["base"]["repo"], github),
        "wrong merged PR",
    )
    runs = github.pages(
        f"actions/workflows/{github.workflow_id}/runs?event=pull_request&head_sha={core.sha(pr['head']['sha'])}&status=success",
        field="workflow_runs",
    )
    matches = []
    for run in runs:
        event = {
            "action": "completed",
            "repository": run["repository"],
            "workflow_run": run,
        }
        # Rebuild every field from authenticated provider/Git data. The check
        # supplies no trusted input identities or executable bytes.
        try:
            fresh = core._verify_pr(event, github, proof_base=before, merged_to=after)
            require(isinstance(fresh, core.Proof), "PR candidate rejected")
        except (
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            AttributeError,
            RecursionError,
        ):
            # An ineligible historical run cannot hide a later valid candidate.
            # Provider transport errors still fail the complete lookup closed.
            continue
        if (
            fresh.record["pr"] != pr["number"]
            or fresh.record["checkout"]["tree"] != current["tree"]["sha"]
        ):
            continue
        expected = isolated_record(
            core,
            github,
            baseline,
            {"qa-isolated": {"id": fresh.record["isolated"]["job"]}},
            current,
        )
        require(fresh.record["isolated"] == expected, "candidate input/runtime changed")
        checks = github.pages(
            f"commits/{fresh.record['checkout']['commit']}/check-runs",
            field="check_runs",
        )
        for check in checks:
            proof = core.read_check(check, app_id)
            if isinstance(proof, core.Proof) and proof.record == fresh.record:
                matches.append(proof)
    require(len(matches) == 1, "missing or ambiguous authenticated PR proof")
    return matches[0]


def main_reuse(core, github, jobs, after, mode):
    if mode == FULL_STEP:
        return None
    require(mode.startswith("Reuse isolated gate "), "unsupported main partition")
    source = jobs["qa-source"]
    successful(source)
    markers = [row for row in steps(source) if row["name"].startswith(PUSH_PREFIX)]
    require(len(markers) == 1, "missing push-before identity")
    successful(markers[0])
    before, observed_after = markers[0]["name"][len(PUSH_PREFIX) :].split(" ")
    require(observed_after == after, "wrong push-after identity")
    proof = source_for_main(
        core, github, before, after, int(os.environ["QA_VERIFIER_APP_ID"])
    )
    require(
        mode == "Reuse isolated gate " + source_text(proof), "lookup source changed"
    )
    return {
        "gate": GATE,
        "pr": proof.record["pr"],
        "run": proof.record["source"]["run"],
        "attempt": proof.record["source"]["attempt"],
        "job": proof.record["isolated"]["job"],
        "checkout": proof.record["checkout"]["commit"],
        "input": proof.record["isolated"]["input"],
    }


def lookup(root, before, after):
    spec = importlib.util.spec_from_file_location(
        "qa_provenance", Path(__file__).with_name("qa_provenance.py")
    )
    core = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = core
    spec.loader.exec_module(core)
    try:
        github = core.GitHubReader(
            os.environ["GH_TOKEN"],
            os.environ["GITHUB_REPOSITORY"],
            int(os.environ["GITHUB_REPOSITORY_ID"]),
            int(os.environ["QA_CI_WORKFLOW_ID"]),
            after,
            root=root,
        )
        proof = source_for_main(
            core, github, before, after, int(os.environ["QA_VERIFIER_APP_ID"])
        )
        value = source_text(proof)
        print(f"[REUSED] {GATE} source={value} evidence=authenticated-pr-proof")
    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        OSError,
        RecursionError,
    ):
        value = ""
        print("[INFO] No authenticated equivalent PR proof; execute all full gates")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write("source=" + value + "\n")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("isolated", "lookup"))
    parser.add_argument("--commit", required=True)
    parser.add_argument("--before")
    args = parser.parse_args()
    root = Path.cwd()
    if args.operation == "isolated":
        return isolated(root, args.commit)
    return lookup(root, args.before, args.commit)


if __name__ == "__main__":
    raise SystemExit(main())
