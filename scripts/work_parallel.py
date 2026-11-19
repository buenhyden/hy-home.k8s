#!/usr/bin/env python3
"""Dispatch planned work units to isolated workers, then integrate (W10-PARALLEL).

A plan is a transient projection of the owning Task: each unit names its
inputs (`depends_on`), its outputs (`owned_paths`), the shared resources it
locks, the services it starts, the brief action it runs under, and the worker
command. `run` validates the plan, then starts every ready unit whose locks do
not overlap a running unit, within `max_workers`, the CPU count, half the
available memory and the concurrent service union limit of `test_cluster.py`.

Each attempt runs in its own shared clone of the base commit with its upstream
results applied, in its own process group. Every lock is also an exclusive
`flock` across runs with a generation that increases on each acquisition; that
generation is the attempt's fencing token. A result is promoted only when the
attempt still holds every token and changed nothing outside its owned paths, so
a timed-out, cancelled or superseded attempt can never be integrated. A failed
unit blocks only its downstream. Cancel kills every worker group and removes
its clone. The integrator applies the promoted patches to a fresh clone in
dependency order and runs the integration check there; a worker PASS never
stands in for it. The source checkout is never written: the result is
`candidate.patch` in the run directory. `sweep` reclaims the workers and clones
of a dispatcher that died. A clone is file separation, not a sandbox: a worker
runs with the caller's own permissions and can write outside its clone.
"""

from __future__ import annotations

import argparse
import fcntl
import graphlib
import hashlib
import importlib.util
import json
import os
import re
import resource
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path, PurePosixPath
from typing import Any, Callable

SCRIPTS = Path(__file__).resolve().parent
RUNTIME = ".workspace-test/parallel"
ID = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")
RESOURCE = re.compile(r"[a-z0-9][a-z0-9.-]*:[A-Za-z0-9._/-]+")
RUN = re.compile(r"[0-9a-f]{8}")
BASE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/^~@-]{0,199}")
UNIT_KEYS = {
    "id",
    "action",
    "depends_on",
    "owned_paths",
    "resources",
    "services",
    "command",
    "timeout",
    "retries",
    "memory_mb",
}
PLAN_KEYS = {"task_ref", "base", "max_workers", "integration_check", "units"}
FAILED = {"failed", "refused", "expired", "blocked", "cancelled"}
MAX_TIMEOUT = 24 * 3600
MAX_RETRIES = 3
OUTPUT_LIMIT = 16 * 1024 * 1024
GIT_TIMEOUT = 120
GRACE = 2.0
STATE_LIMIT = 1024 * 1024


def _load(name: str, file: str):
    if str(SCRIPTS) not in sys.path:  # validate-execution-brief imports validation.*
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLUSTER = _load("_work_parallel_test_cluster", "test_cluster.py")


class ParallelError(ValueError):
    """A refused plan, lease or result; the message starts with its code."""


def _fail(code: str, message: str) -> ParallelError:
    return ParallelError(f"{code}: {message}")


def _strings(value: Any, what: str, *, empty: bool = True) -> list[str]:
    if (
        not isinstance(value, list)
        or (not empty and not value)
        or not all(
            isinstance(item, str) and item.strip() and "\0" not in item
            for item in value
        )
    ):
        raise _fail("PARALLEL_PLAN", f"{what} must be a list of non-empty strings")
    return value


def _owned(path: str) -> str:
    pure = PurePosixPath(path)
    if (
        pure.is_absolute()
        or path.startswith("./")
        or any(part in ("", ".", "..") for part in path.rstrip("/").split("/"))
        or ".git" in pure.parts
    ):
        raise _fail(
            "PARALLEL_PLAN", f"owned path {path!r} is not a plain relative path"
        )
    return path


def covers(owned: str, path: str) -> bool:
    """An owned file covers itself; an owned `dir/` covers everything below it."""
    return owned == path or (owned.endswith("/") and path.startswith(owned))


def _overlap(first: list[str], second: list[str]) -> bool:
    return any(
        covers(a, b) or covers(b, a) or a.rstrip("/") == b.rstrip("/")
        for a in first
        for b in second
    )


def load_plan(
    data: Any, *, closure: Callable[[list[str]], list[str]] | None = None
) -> dict[str, Any]:
    """Validate a plan; return it with defaults and each unit's service closure."""
    if not isinstance(data, dict) or set(data) != PLAN_KEYS:
        raise _fail("PARALLEL_PLAN", f"a plan has exactly {sorted(PLAN_KEYS)}")
    if not isinstance(data["task_ref"], str) or not data["task_ref"].strip():
        raise _fail("PARALLEL_PLAN", "task_ref is required")
    if not isinstance(data["base"], str) or not BASE.fullmatch(data["base"]):
        raise _fail("PARALLEL_PLAN", "base must be a revision name, not an option")
    workers = data["max_workers"]
    cpus = os.cpu_count() or 1
    if type(workers) is not int or not 1 <= workers <= cpus:
        raise _fail("PARALLEL_PLAN", f"max_workers must be 1..{cpus} (CPU count)")
    _strings(data["integration_check"], "integration_check", empty=False)
    if not isinstance(data["units"], list) or not data["units"]:
        raise _fail("PARALLEL_PLAN", "units must be a non-empty list")
    units: list[dict[str, Any]] = []
    for raw in data["units"]:
        if not isinstance(raw, dict) or not set(raw) <= UNIT_KEYS:
            raise _fail("PARALLEL_PLAN", f"a unit has only {sorted(UNIT_KEYS)}")
        unit = {
            "depends_on": [],
            "resources": [],
            "services": [],
            "timeout": 600,
            "retries": 0,
            "memory_mb": 256,
            **raw,
        }
        if not isinstance(unit.get("id"), str) or not ID.fullmatch(unit["id"]):
            raise _fail("PARALLEL_PLAN", f"unit id {unit.get('id')!r} is invalid")
        if any(u["id"] == unit["id"] for u in units):
            raise _fail("PARALLEL_PLAN", f"duplicate unit {unit['id']}")
        if not isinstance(unit.get("action"), str) or not unit["action"].strip():
            raise _fail("PARALLEL_PLAN", f"{unit['id']} names no brief action")
        _strings(unit["depends_on"], "depends_on")
        for path in _strings(unit.get("owned_paths"), "owned_paths", empty=False):
            _owned(path)
        for name in _strings(unit["resources"], "resources"):
            if not RESOURCE.fullmatch(name) or name.startswith("path:"):
                raise _fail("PARALLEL_PLAN", f"resource {name!r} is not kind:name")
        _strings(unit.get("command"), "command", empty=False)
        timeout, retries, memory = unit["timeout"], unit["retries"], unit["memory_mb"]
        if (
            type(timeout) not in (int, float)
            or not 0 < timeout <= MAX_TIMEOUT
            or type(retries) is not int
            or not 0 <= retries <= MAX_RETRIES
            or type(memory) is not int
            or memory <= 0
        ):
            raise _fail(
                "PARALLEL_PLAN", f"{unit['id']} has a bad timeout, retries or memory"
            )
        unit["closure"] = _closure(unit, closure)
        units.append(unit)
    ids = {u["id"] for u in units}
    graph = {}
    for unit in units:
        missing = sorted(set(unit["depends_on"]) - ids)
        if missing:
            raise _fail(
                "PARALLEL_DEPENDENCY", f"{unit['id']} needs unknown {missing[0]}"
            )
        graph[unit["id"]] = unit["depends_on"]
    try:
        order = list(graphlib.TopologicalSorter(graph).static_order())
    except graphlib.CycleError as exc:
        raise _fail("PARALLEL_DEPENDENCY", f"cycle {exc.args[1]}") from None
    by_id = {u["id"]: u for u in units}
    return {**data, "units": [by_id[uid] for uid in order]}


def _closure(unit: dict[str, Any], closure) -> list[str]:
    services = _strings(unit["services"], "services")
    if not services:
        return []
    for name in services:
        if name.lower() in CLUSTER.WHOLE or any(ch in name for ch in "*?["):
            raise _fail("PARALLEL_SERVICES", f"{name} selects everything")
    if closure is None:
        raise _fail("PARALLEL_SERVICES", "services need a closure resolver")
    try:
        apps = sorted(set(closure(services)))
    except Exception as exc:  # the resolver's own refusal, e.g. SELECTION_ROOT
        raise _fail("PARALLEL_SERVICES", str(exc)) from None
    if len(apps) > CLUSTER.APP_LIMIT:
        raise _fail(
            "PARALLEL_SERVICES",
            f"{unit['id']} closure of {len(apps)} exceeds {CLUSTER.APP_LIMIT}",
        )
    return apps


class Leases:
    """Exclusive `flock` leases with a fencing generation per key."""

    def __init__(self, directory: Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.held: dict[str, tuple[int, int]] = {}
        self.shared: dict[frozenset, list[int]] = {}

    def _file(self, key: str) -> Path:
        return self.directory / (
            hashlib.sha256(key.encode()).hexdigest()[:32] + ".lock"
        )

    def _generation(self, key: str) -> int:
        try:
            return int(self._file(key).read_text().strip() or 0)
        except FileNotFoundError:
            return 0

    def acquire(self, keys, shared=()) -> dict[str, int] | None:
        """All keys or none; None when another holder has one of them.

        `keys` are exclusive and carry a fencing generation. `shared` keys
        (the directories above an owned path) are held shared, so a run that
        owns a whole directory excludes every run owning a path below it.
        """
        fds: list[int] = []
        for key in sorted(set(shared) - set(keys)):
            fd = os.open(self._file(key), os.O_RDONLY | os.O_CREAT, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                os.close(fd)
                for held in fds:
                    os.close(held)
                return None
            fds.append(fd)
        got: dict[str, int] = {}
        for key in sorted(set(keys)):
            fd = os.open(self._file(key), os.O_RDWR | os.O_CREAT, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                os.close(fd)
                self.release(got)
                for held in fds:
                    os.close(held)
                return None
            generation = int(os.pread(fd, 32, 0).strip() or 0) + 1
            os.ftruncate(fd, 0)
            os.pwrite(fd, str(generation).encode(), 0)
            os.fsync(fd)
            self.held[key] = (fd, generation)
            got[key] = generation
        self.shared[frozenset(got.items())] = fds
        return got

    def release(self, tokens: dict[str, int]) -> None:
        for fd in self.shared.pop(frozenset(tokens.items()), []):
            os.close(fd)
        for key, generation in tokens.items():
            held = self.held.get(key)
            if held and held[1] == generation:
                os.close(held[0])
                del self.held[key]

    def check(self, tokens: dict[str, int]) -> None:
        for key, generation in tokens.items():
            held = self.held.get(key)
            if (
                held is None
                or held[1] != generation
                or self._generation(key) != generation
            ):
                raise _fail(
                    "PARALLEL_FENCED", f"{key} token {generation} is not current"
                )


def lock_keys(owned: list[str], resources: list[str]) -> tuple[list[str], list[str]]:
    """Exclusive keys for owned paths and resources; shared keys for their parents."""
    exclusive = [f"path:{p}" for p in owned] + list(resources)
    shared = {
        "path:" + "/".join(parts[:i]) + "/"
        for p in owned
        for parts in [p.rstrip("/").split("/")]
        for i in range(1, len(parts))
    }
    return exclusive, sorted(shared - set(exclusive))


def _git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    # A worker runs as the same user: ignore its replace refs and any global
    # config it could have written.
    env.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_NO_REPLACE_OBJECTS="1",
    )
    return env


# Settings a worker could set in its clone's config to change what the
# dispatcher's own git calls report or write.
SAFE_CONFIG = [
    part
    for item in (
        "core.hooksPath=/dev/null",
        "core.fsmonitor=false",
        "core.attributesFile=/dev/null",
        "diff.noprefix=false",
        "diff.mnemonicPrefix=false",
    )
    for part in ("-c", item)
]


def _git_meta(clone: Path) -> str:
    """Digest of the clone's config and info files, which only git should own."""
    digest = hashlib.sha256()
    git_dir = clone / ".git"
    files = [git_dir / "config", *sorted((git_dir / "info").rglob("*"))]
    for path in files:
        digest.update(str(path.relative_to(git_dir)).encode() + b"\0")
        if path.is_symlink():
            digest.update(b"link:" + os.readlink(path).encode())
        elif path.is_file():
            with path.open("rb") as handle:
                digest.update(handle.read(OUTPUT_LIMIT + 1))
    return digest.hexdigest()


def _git(cwd: Path, *args: str, binary: bool = False, data: bytes | None = None):
    """Run git with bounded output; a clone's own hooks and fsmonitor never run."""
    command = ["git", *SAFE_CONFIG]
    with (
        tempfile.TemporaryFile() as out,
        tempfile.TemporaryFile() as err,
        tempfile.TemporaryFile() as source,
    ):
        if data is not None:
            source.write(data)
            source.seek(0)
        try:
            code = subprocess.run(
                [*command, *args],
                cwd=cwd,
                env=_git_env(),
                stdin=source if data is not None else subprocess.DEVNULL,
                stdout=out,
                stderr=err,
                timeout=GIT_TIMEOUT,
                check=False,
                preexec_fn=_limit_output,
            ).returncode
        except (OSError, subprocess.SubprocessError) as exc:
            raise _fail("PARALLEL_GIT", f"git {args[0]}: {exc}") from None
        if code != 0:
            err.seek(0)
            tail = err.read(4096).decode(errors="replace")
            raise _fail("PARALLEL_GIT", f"git {args[0]} exited {code}: {tail[-400:]}")
        out.seek(0)
        data = out.read(OUTPUT_LIMIT + 1)
    if len(data) > OUTPUT_LIMIT:
        raise _fail("PARALLEL_GIT", f"git {args[0]} output exceeds {OUTPUT_LIMIT}")
    return data if binary else data.decode().strip()


def _paths(cwd: Path, *args: str) -> list[str]:
    """NUL-separated path output, kept byte-exact (no strip, no rename pairing)."""
    raw = _git(cwd, *args, binary=True)
    return [p.decode(errors="surrogateescape") for p in raw.split(b"\0") if p]


def _limit_output() -> None:
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_LIMIT, OUTPUT_LIMIT))


def _prepare_child() -> None:
    """Bound output and clear an inherited signal mask so cancel reaches the child.

    A caller such as `qa.py` may run with SIGINT and SIGTERM blocked; a worker
    that kept that mask would ignore SIGTERM and run on until SIGKILL.
    """
    _limit_output()
    signal.pthread_sigmask(signal.SIG_SETMASK, set())


def _available_mb() -> int:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) // 1024
    return 0


def _live_members(pgid: int) -> bool:
    """Whether the group has a member that is not a zombie.

    `killpg(pgid, 0)` also succeeds for a group of unreaped zombies, which a
    child subreaper (such as the validation runner) keeps. Only the public
    `/proc/<pid>/stat` state and group fields are read.
    """
    for stat in Path("/proc").glob("[0-9]*/stat"):
        try:
            fields = stat.read_text().rsplit(")", 1)[1].split()
        except (OSError, IndexError):
            continue
        if len(fields) > 2 and fields[2] == str(pgid) and fields[0] not in ("Z", "X"):
            return True
    return False


def _kill_group(pid: int, proc: subprocess.Popen | None = None) -> None:
    """TERM, then KILL, the whole process group; reap our own leader meanwhile."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(pid, sig)
        except (ProcessLookupError, PermissionError):  # gone, or not ours
            return
        deadline = time.monotonic() + GRACE
        while time.monotonic() < deadline:
            if proc is not None:
                proc.poll()  # a zombie leader keeps the group alive until reaped
            if not _live_members(pid):
                return
            time.sleep(0.02)


def _remove(run_dir: Path, path: Path) -> None:
    if path.parent == run_dir and path.name.startswith("clone-"):
        shutil.rmtree(path, ignore_errors=True)


def brief_preflight(root: Path, brief: Path, current: Path):
    """The existing brief check for each dispatch; it checks scope, not authority."""
    module = _load("_work_parallel_brief", "validate-execution-brief.py")
    records = []
    for path in (brief, current):
        raw = module.read_bytes(Path(path), max_bytes=module.BYTE_LIMIT)
        records.append(json.loads(raw, object_pairs_hook=module._unique_object))

    def preflight(unit: dict[str, Any]) -> None:
        try:
            module.check(
                records[0],
                records[1],
                Path(root),
                operation="dispatch",
                action=unit["action"],
                paths=list(unit["owned_paths"]),
            )
        except module.BriefError as exc:
            raise _fail("PARALLEL_BRIEF", str(exc)) from None

    preflight.revision = str(records[0].get("revision", ""))
    return preflight


class _Run:
    def __init__(self, root, plan, runtime, preflight, cancel, brief_revision, poll):
        self.root = Path(root).resolve()
        self.plan = plan
        self.preflight = preflight
        self.cancel = cancel or threading.Event()
        self.brief_revision = brief_revision
        self.poll = poll
        self.id = secrets.token_hex(4)
        self.dir = Path(runtime) / self.id
        self.dir.mkdir(parents=True)
        # Held for the dispatcher's lifetime; `sweep` treats a lockable run as dead.
        self.alive = (self.dir / "dispatcher.lock").open("w")
        fcntl.flock(self.alive, fcntl.LOCK_EX)
        self.leases = Leases(Path(runtime) / "locks")
        self.base = _git(self.root, "rev-parse", "--verify", plan["base"] + "^{commit}")
        self.units = {u["id"]: u for u in plan["units"]}
        self.order = [u["id"] for u in plan["units"]]
        self.rec = {
            uid: {
                "state": "pending",
                "attempts": 0,
                "reason": None,
                "started": None,
                "finished": None,
                "tokens": None,
                "changed": [],
                "ignored": [],
                "expired": [],
            }
            for uid in self.order
        }
        self.running: dict[str, dict[str, Any]] = {}
        self.checking: subprocess.Popen | None = None
        self.pids: list[int] = []
        self.timing = {"setup": 0.0, "workers": 0.0, "integration_seconds": 0.0}
        self.memory = _available_mb() // 2
        self.t0 = time.monotonic()
        self._save()

    def now(self) -> float:
        return round(time.monotonic() - self.t0, 3)

    def _save(self) -> None:
        state = {
            "run": self.id,
            "dispatcher": os.getpid(),
            "workers": [
                {"unit": uid, "pid": w["proc"].pid, "clone": str(w["clone"])}
                for uid, w in self.running.items()
            ]
            + (
                [{"unit": "integration", "pid": self.checking.pid}]
                if self.checking
                else []
            ),
        }
        temp = self.dir / "state.json.tmp"
        temp.write_text(json.dumps(state))
        temp.replace(self.dir / "state.json")

    def env(self, **extra: str) -> dict[str, str]:
        return {
            **os.environ,
            "HYK8S_PARALLEL_RUN": self.id,
            "HYK8S_PARALLEL_TASK_REF": self.plan["task_ref"],
            "HYK8S_PARALLEL_BRIEF_REVISION": self.brief_revision,
            "HYK8S_PARALLEL_BASE": self.base,
            **extra,
        }

    def conflicts(self, unit) -> bool:
        if len(self.running) >= self.plan["max_workers"]:
            return True
        used = sum(self.units[uid]["memory_mb"] for uid in self.running)
        if used and used + unit["memory_mb"] > self.memory:
            return True
        services = set(unit["closure"])
        for uid in self.running:
            other = self.units[uid]
            if _overlap(unit["owned_paths"], other["owned_paths"]) or set(
                unit["resources"]
            ) & set(other["resources"]):
                return True
            services |= set(other["closure"])
        return len(services) > CLUSTER.APP_LIMIT

    def upstream(self, uid: str) -> list[str]:
        seen: set[str] = set()
        stack = list(self.units[uid]["depends_on"])
        while stack:
            dep = stack.pop()
            if dep not in seen:
                seen.add(dep)
                stack.extend(self.units[dep]["depends_on"])
        return [d for d in self.order if d in seen]

    def clone(self, name: str, patches: list[str]) -> tuple[Path, str]:
        path = self.dir / f"clone-{name}"
        _git(
            self.dir,
            "clone",
            "--quiet",
            "--shared",
            "--no-checkout",
            str(self.root),
            str(path),
        )
        _git(path, "remote", "remove", "origin")
        _git(path, "checkout", "--quiet", "--detach", self.base)
        for dep in patches:
            patch = self.dir / f"{dep}.patch"
            if patch.stat().st_size:
                _git(path, "apply", "--index", "--binary", str(patch))
        _git(path, "add", "-A")
        return path, _git(path, "write-tree")

    def start(self, uid: str) -> None:
        unit, rec = self.units[uid], self.rec[uid]
        tokens = self.leases.acquire(*lock_keys(unit["owned_paths"], unit["resources"]))
        if tokens is None:  # another run holds a lock; try again later
            return
        try:
            self.preflight(unit)
        except ParallelError as exc:
            self.leases.release(tokens)
            rec.update(state="refused", reason=str(exc))
            return
        rec["attempts"] += 1
        begin = time.monotonic()
        clone = self.dir / f"clone-{uid}-{rec['attempts']}"
        try:
            clone, tree = self.clone(clone.name[6:], self.upstream(uid))
            self.timing["setup"] += time.monotonic() - begin
            env = self.env(
                HYK8S_PARALLEL_UNIT=uid,
                HYK8S_PARALLEL_ATTEMPT=str(rec["attempts"]),
                HYK8S_PARALLEL_TOKENS=json.dumps(tokens, sort_keys=True),
            )
            meta = _git_meta(clone)  # the baseline, before the worker can run
            with (self.dir / f"{uid}-{rec['attempts']}.log").open("wb") as log:
                proc = subprocess.Popen(
                    unit["command"],
                    cwd=clone,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    preexec_fn=_prepare_child,
                )
        except (ParallelError, OSError, ValueError, subprocess.SubprocessError) as exc:
            self.leases.release(tokens)
            _remove(self.dir, clone)
            code = exc if isinstance(exc, ParallelError) else f"PARALLEL_EXEC: {exc}"
            rec.update(state="failed", reason=str(code))
            return
        self.pids.append(proc.pid)
        rec["started"] = self.now()
        self.running[uid] = {
            "proc": proc,
            "clone": clone,
            "tree": tree,
            "meta": meta,
            "tokens": tokens,
            "begin": time.monotonic(),
            "deadline": time.monotonic() + unit["timeout"],
        }
        self._save()

    def stop(self, uid: str) -> dict[str, Any]:
        work = self.running.pop(uid)
        _kill_group(work["proc"].pid, work["proc"])
        work["proc"].wait(timeout=GRACE)
        self.timing["workers"] += time.monotonic() - work["begin"]
        self.rec[uid]["finished"] = self.now()
        return work

    def settle(self, uid: str, work: dict[str, Any], code: int | None) -> None:
        unit, rec = self.units[uid], self.rec[uid]
        try:
            if code == 0:
                try:
                    self.promote(uid, work)
                except (ParallelError, OSError) as exc:
                    rec.update(state="failed", reason=str(exc))
                return
            reason = "PARALLEL_TIMEOUT" if code is None else f"PARALLEL_EXIT: {code}"
            rec["expired"].append(
                {"attempt": rec["attempts"], "reason": reason, "tokens": work["tokens"]}
            )
            if rec["attempts"] <= unit["retries"]:
                rec["state"] = "pending"
            else:
                rec.update(state="expired" if code is None else "failed", reason=reason)
        finally:
            self.leases.release(work["tokens"])
            _remove(self.dir, work["clone"])

    def promote(self, uid: str, work: dict[str, Any]) -> None:
        unit, rec = self.units[uid], self.rec[uid]
        clone = work["clone"]
        if _git_meta(clone) != work["meta"]:
            rec.update(
                state="refused", reason="PARALLEL_GITCONFIG: worker changed .git"
            )
            return
        _git(clone, "add", "-A")
        # One snapshot tree feeds both the ownership list and the patch, through
        # plumbing that ignores porcelain diff settings.
        snapshot = _git(clone, "write-tree")
        compare = ["diff-tree", "-r", "--no-renames", "--no-ext-diff", "--no-textconv"]
        changed = _paths(clone, *compare, "--name-only", "-z", work["tree"], snapshot)
        rec["changed"] = changed
        rec["ignored"] = _paths(
            clone, "ls-files", "-z", "--others", "--ignored", "--exclude-standard"
        )
        outside = [
            p for p in changed if not any(covers(o, p) for o in unit["owned_paths"])
        ]
        if outside:
            rec.update(
                state="refused", reason=f"PARALLEL_OWNERSHIP: {', '.join(outside)}"
            )
            return
        try:
            self.leases.check(work["tokens"])
        except ParallelError as exc:
            rec.update(state="refused", reason=str(exc))
            return
        patch = _git(
            clone,
            *compare,
            "-p",
            "--binary",
            "--full-index",
            work["tree"],
            snapshot,
            binary=True,
        )
        (self.dir / f"{uid}.patch").write_bytes(patch)
        rec.update(state="promoted", tokens=work["tokens"])

    def loop(self) -> bool:
        while True:
            if self.cancel.is_set():
                return False
            for uid in self.order:
                rec = self.rec[uid]
                if rec["state"] != "pending":
                    continue
                bad = [
                    d
                    for d in self.units[uid]["depends_on"]
                    if self.rec[d]["state"] in FAILED
                ]
                if bad:
                    rec.update(state="blocked", reason=f"PARALLEL_BLOCKED: {bad[0]}")
            for uid, work in list(self.running.items()):
                code = work["proc"].poll()
                if code is None and time.monotonic() < work["deadline"]:
                    continue
                self.settle(uid, self.stop(uid), code)
                self._save()
            for uid in self.order:
                rec = self.rec[uid]
                if (
                    rec["state"] == "pending"
                    and uid not in self.running
                    and all(
                        self.rec[d]["state"] == "promoted"
                        for d in self.units[uid]["depends_on"]
                    )
                    and not self.conflicts(self.units[uid])
                ):
                    self.start(uid)
            if not self.running and all(
                r["state"] != "pending" for r in self.rec.values()
            ):
                return True
            time.sleep(self.poll)

    def integrate(self) -> tuple[dict[str, Any], str | None]:
        promoted = [uid for uid in self.order if self.rec[uid]["state"] == "promoted"]
        if not promoted:
            return {"state": "SKIPPED", "returncode": None}, None
        begin = time.monotonic()
        path = None
        try:
            path, _ = self.clone("integration", [])
            for uid in promoted:
                patch = self.dir / f"{uid}.patch"
                if not patch.stat().st_size:
                    continue
                # The patch file sits beside the worker clones, where a worker can
                # reach it: read it once, apply those bytes, then check the paths
                # the index actually changed, not what the patch text claims.
                with patch.open("rb") as handle:
                    payload = handle.read(OUTPUT_LIMIT + 1)
                if len(payload) > OUTPUT_LIMIT:
                    reason = f"PARALLEL_PATCH: {uid} patch exceeds {OUTPUT_LIMIT} bytes"
                    return {"state": "REFUSED", "unit": uid, "reason": reason}, None
                before = _git(path, "write-tree")
                try:
                    _git(path, "apply", "--index", "--binary", "-", data=payload)
                except ParallelError as exc:
                    return {"state": "CONFLICT", "unit": uid, "reason": str(exc)}, None
                after = _git(path, "write-tree")
                owned = self.units[uid]["owned_paths"]
                outside = [
                    p
                    for p in _paths(
                        path,
                        "diff-tree",
                        "-r",
                        "--no-renames",
                        "--name-only",
                        "-z",
                        before,
                        after,
                    )
                    if not any(covers(o, p) for o in owned)
                ]
                if outside:
                    reason = (
                        f"PARALLEL_OWNERSHIP: {uid} patch touches {', '.join(outside)}"
                    )
                    return {"state": "REFUSED", "unit": uid, "reason": reason}, None
            candidate = self.dir / "candidate.patch"
            candidate.write_bytes(
                _git(path, "diff", "--cached", "--binary", self.base, binary=True)
            )
            with (self.dir / "integration.log").open("wb") as log:
                self.checking = subprocess.Popen(
                    self.plan["integration_check"],
                    cwd=path,
                    env=self.env(HYK8S_PARALLEL_UNIT="integration"),
                    stdin=subprocess.DEVNULL,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    preexec_fn=_prepare_child,
                )
            proc = self.checking
            self.pids.append(proc.pid)
            self._save()
            deadline = time.monotonic() + MAX_TIMEOUT
            while proc.poll() is None and not self.cancel.is_set():
                if time.monotonic() > deadline:
                    break
                time.sleep(self.poll)
            code = proc.poll()
            _kill_group(proc.pid, proc)
            proc.wait(timeout=GRACE)
            self.checking = None
            self._save()
            if code is None and self.cancel.is_set():
                return {"state": "CANCELLED", "returncode": None}, None
            state = "PASS" if code == 0 else "FAIL"
            return {"state": state, "returncode": code}, str(candidate)
        except (ParallelError, OSError, ValueError, subprocess.SubprocessError) as exc:
            return {"state": "ERROR", "reason": str(exc)}, None
        finally:
            if path is not None:
                _remove(self.dir, path)
            self.timing["integration_seconds"] = round(time.monotonic() - begin, 3)

    def execute(self) -> dict[str, Any]:
        finished = False
        try:
            finished = self.loop()
        finally:
            for uid in list(self.running):
                work = self.stop(uid)
                self.leases.release(work["tokens"])
                _remove(self.dir, work["clone"])
                self.rec[uid].update(state="cancelled", reason="PARALLEL_CANCELLED")
            if not finished:
                for rec in self.rec.values():
                    if rec["state"] == "pending":
                        rec.update(state="cancelled", reason="PARALLEL_CANCELLED")
            self._save()
        if finished:
            integration, candidate = self.integrate()
        else:
            integration, candidate = {"state": "SKIPPED", "returncode": None}, None
        if not finished or integration["state"] == "CANCELLED":
            state = "cancelled"
        elif integration["state"] == "PASS" and all(
            r["state"] == "promoted" for r in self.rec.values()
        ):
            state = "completed"
        else:
            state = "failed"
        report = {
            "run": self.id,
            "task_ref": self.plan["task_ref"],
            "base": self.base,
            "state": state,
            "units": self.rec,
            "integration": integration,
            "candidate": candidate,
            "pids": self.pids,
            "timing": {
                **{k: round(v, 3) for k, v in self.timing.items()},
                "elapsed": self.now(),
                "max_workers": self.plan["max_workers"],
            },
        }
        (self.dir / "report.json").write_text(json.dumps(report, indent=2))
        (self.dir / "state.json").unlink(missing_ok=True)
        self.alive.close()
        return report


def run(
    root: Path,
    plan: Any,
    *,
    runtime: Path,
    preflight: Callable[[dict[str, Any]], None],
    closure: Callable[[list[str]], list[str]] | None = None,
    cancel: threading.Event | None = None,
    brief_revision: str = "",
    poll: float = 0.02,
) -> dict[str, Any]:
    root = Path(root).resolve()
    if closure is None:

        def closure(selection):
            return CLUSTER.plan(CLUSTER.catalog(root), selection)

    checked = load_plan(plan, closure=closure)
    return _Run(
        root, checked, runtime, preflight, cancel, brief_revision, poll
    ).execute()


def _environ(pid: int) -> bytes:
    try:
        return Path(f"/proc/{pid}/environ").read_bytes()
    except OSError:
        return b""


def _group_alive(pid: int) -> bool:
    try:
        os.killpg(pid, 0)
    except (ProcessLookupError, PermissionError):  # gone, or another user's
        return False
    return _live_members(pid)


def sweep(runtime: Path) -> list[str]:
    """Reclaim workers and clones whose dispatcher is gone; return the run IDs.

    A run is dead when its `dispatcher.lock` can be locked. A worker group is
    killed when its leader still carries the run marker, or when the leader is
    gone but the group lives on: Linux does not reuse a PID while it still names
    a process group, so that group is still the worker's.
    """
    cleaned = []
    for run_dir in sorted(Path(runtime).glob("*/")):
        if not RUN.fullmatch(run_dir.name):
            continue
        try:
            with (run_dir / "dispatcher.lock").open("a") as lock:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    continue  # the dispatcher is alive
                with (run_dir / "state.json").open("rb") as handle:
                    state = json.loads(handle.read(STATE_LIMIT))
                if state.get("run") != run_dir.name:
                    continue
                marker = f"HYK8S_PARALLEL_RUN={run_dir.name}".encode()
                for worker in state["workers"]:
                    pid = int(worker["pid"])
                    environ = _environ(pid)
                    if marker in environ.split(b"\0") or (
                        not environ and _group_alive(pid)
                    ):
                        _kill_group(pid)
        except (OSError, ValueError, KeyError, TypeError):
            continue  # gone, being swept, or unreadable: leave it for a person
        shutil.rmtree(run_dir, ignore_errors=True)
        cleaned.append(run_dir.name)
    return cleaned


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    runner = sub.add_parser("run", help="validate, dispatch and integrate a plan")
    runner.add_argument("--root", type=Path, default=Path.cwd())
    runner.add_argument("--runtime", type=Path)
    runner.add_argument("--plan", type=Path, required=True)
    runner.add_argument("--brief", type=Path, required=True)
    runner.add_argument("--current-request", type=Path, required=True)
    sweeper = sub.add_parser("sweep", help="reclaim runs whose dispatcher died")
    sweeper.add_argument("--root", type=Path, default=Path.cwd())
    sweeper.add_argument("--runtime", type=Path)
    args = parser.parse_args(argv)
    runtime = args.runtime or args.root / RUNTIME
    # An inherited block would stop the operator's cancel from arriving.
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGINT, signal.SIGTERM})
    try:
        if args.command == "sweep":
            print(json.dumps({"cleaned": sweep(runtime)}))
            return 0
        with args.plan.open("rb") as handle:
            plan = json.loads(handle.read(STATE_LIMIT))
        preflight = brief_preflight(args.root, args.brief, args.current_request)
        cancel = threading.Event()
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda *_: cancel.set())
        report = run(
            args.root,
            plan,
            runtime=runtime,
            preflight=preflight,
            cancel=cancel,
            brief_revision=preflight.revision,
        )
    except (ParallelError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0 if report["state"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
