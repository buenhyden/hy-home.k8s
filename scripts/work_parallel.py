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
of a dispatcher that died. A clone is file separation, not a sandbox: a command
worker runs with the caller's own permissions and can write outside its clone.

A provider unit (`claude` or `codex`) starts only while its P08 request brief
is current, through the installed CLI's own options with the prompt on stdin.
It runs in a systemd user scope, which caps memory, one CPU, tasks and run time
and whose stop ends every descendant, a `setsid` one too, inside a bwrap mount
namespace that keeps writes in its clone, starts from an empty environment in
its own PID, IPC and UTS namespaces, and hides /run and every other listening
path socket. Host reads and the network stay open, because the provider needs
its API, so abstract sockets and local TCP services stay reachable; disk use is
checked when the result is collected, not enforced as a quota.
"""

from __future__ import annotations

import argparse
import fcntl
import graphlib
import hashlib
import importlib
import importlib.util
import json
import math
import os
import re
import resource
import secrets
import shutil
import signal
import stat
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
    "provider",
    "prompt",
    "model",
    "budget_usd",
}
PROVIDERS = ("command", "claude", "codex")
MODEL = re.compile(r"[a-z0-9][a-z0-9.-]{0,63}")
PROMPT_LIMIT = 16 * 1024
MAX_BUDGET_USD = 10.0
SCOPE_TIMEOUT = 30
SCOPE_ENV = ("PATH", "HOME", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS")
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
ADMISSION = importlib.import_module("environment_admission")
WORKER_DISK_MIB = 1024
INTEGRATION_MEMORY_MIB = 512


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
        _provider_fields(unit)
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


def _provider_fields(unit: dict[str, Any]) -> None:
    """A command unit names its argv; a provider unit names prompt, model, budget."""
    provider = unit.setdefault("provider", "command")
    if provider not in PROVIDERS:
        raise _fail("PARALLEL_PLAN", f"{unit['id']} names unknown provider")
    if provider == "command":
        if {"prompt", "model", "budget_usd"} & set(unit):
            raise _fail("PARALLEL_PLAN", f"{unit['id']} is a command unit")
        _strings(unit.get("command"), "command", empty=False)
        return
    prompt, model = unit.get("prompt"), unit.get("model")
    if (
        "command" in unit
        or not isinstance(prompt, str)
        or not prompt.strip()
        or len(prompt.encode()) > PROMPT_LIMIT
        or not isinstance(model, str)
        or not MODEL.fullmatch(model)
    ):
        raise _fail(
            "PARALLEL_PLAN", f"{unit['id']} needs a bounded prompt and a model name"
        )
    budget = unit.get("budget_usd")
    # Claude's print mode takes a spending cap; Codex exec has none, so its
    # only bound is the unit timeout.
    if provider == "codex":
        if budget is not None:
            raise _fail("PARALLEL_PLAN", f"{unit['id']}: codex takes no budget_usd")
    elif (
        type(budget) not in (int, float)
        or not math.isfinite(budget)
        or not 0 < budget <= MAX_BUDGET_USD
    ):
        raise _fail("PARALLEL_PLAN", f"{unit['id']} needs a finite budget_usd")


def provider_argv(unit: dict[str, Any], clone: Path, binary: str) -> list[str]:
    """The installed CLI's own options; the prompt goes on stdin."""
    if unit["provider"] == "claude":
        return [
            binary,
            "-p",
            "--output-format",
            "json",
            "--model",
            unit["model"],
            "--safe-mode",
            "--strict-mcp-config",
            "--tools",
            "Read,Edit,Write",
            "--permission-mode",
            "acceptEdits",
            "--no-session-persistence",
            "--max-budget-usd",
            str(unit["budget_usd"]),
        ]
    return [
        binary,
        "exec",
        "--json",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--model",
        unit["model"],
        "--cd",
        str(clone),
        "-",
    ]


def parse_result(provider: str, raw: bytes) -> dict[str, Any]:
    """Session, cost, turns and usage from the CLI's JSON; nothing is executed."""
    result: dict[str, Any] = {
        "session": None,
        "cost_usd": None,
        "turns": None,
        "usage": None,
        "error": None,
    }
    events = []
    for line in raw.decode(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict):
            events.append(event)
    if provider == "claude":
        final = next((e for e in reversed(events) if e.get("type") == "result"), None)
        if final is None:
            return {**result, "error": "PARALLEL_RESULT: no result object"}
        result.update(
            session=final.get("session_id"),
            cost_usd=final.get("total_cost_usd"),
            turns=final.get("num_turns"),
            usage=final.get("usage"),
        )
        if final.get("is_error"):
            result["error"] = f"PARALLEL_RESULT: {str(final.get('result'))[:400]}"
        return result
    turns = [e for e in events if e.get("type") == "turn.completed"]
    session = next((e.get("thread_id") for e in events if e.get("thread_id")), None)
    if session is None:
        return {**result, "error": "PARALLEL_RESULT: no thread identity"}
    failed = next(
        (e for e in events if e.get("type") in ("turn.failed", "error")), None
    )
    result.update(
        session=session,
        turns=len(turns),
        usage=turns[-1].get("usage") if turns else None,
    )
    if failed is not None:
        result["error"] = f"PARALLEL_RESULT: {json.dumps(failed)[:400]}"
    return result


def sandbox_available() -> bool:
    """Whether a systemd user scope and bwrap can start here."""
    if not (shutil.which("systemd-run") and shutil.which("bwrap")):
        return False
    try:
        return (
            subprocess.run(
                [
                    "systemd-run",
                    "--user",
                    "--scope",
                    "--quiet",
                    "--",
                    "bwrap",
                    "--ro-bind",
                    "/",
                    "/",
                    "--dev",
                    "/dev",
                    "--proc",
                    "/proc",
                    "true",
                ],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                timeout=SCOPE_TIMEOUT,
                check=False,
            ).returncode
            == 0
        )
    except (OSError, subprocess.SubprocessError):
        return False


def contain(
    argv: list[str],
    *,
    scope: str,
    clone: Path,
    binary: str,
    memory_mb: int,
    timeout: float,
    env: dict[str, str],
    sockets: list[str] | None = None,
) -> list[str]:
    """Wrap a provider worker in its own cgroup and a read-only mount namespace.

    The systemd user scope is the process boundary: stopping it ends every
    descendant, a `setsid` one too, and it caps memory, one CPU, tasks and run
    time. bwrap mounts the host read-only except the clone and a private /tmp,
    starts from an empty environment in its own PID, IPC and UTS namespaces and
    session, and hides /run (the user bus, systemd and container sockets) and
    every other listening path socket, because a read-only mount still lets a
    process connect to a socket that can start code outside. Only the resolver
    under /run is mounted back. The network stays shared, because the provider
    needs its API, so abstract sockets and local TCP services stay reachable,
    and the host stays readable.
    """
    wrapper = [
        "systemd-run",
        "--user",
        "--scope",
        "--quiet",
        f"--unit={scope}",
        "-p",
        f"MemoryMax={memory_mb}M",
        "-p",
        "MemorySwapMax=0",
        "-p",
        "CPUQuota=100%",
        "-p",
        "TasksMax=512",
        "-p",
        f"RuntimeMaxSec={math.ceil(timeout) + SCOPE_TIMEOUT}",
        "--",
        "bwrap",
        "--ro-bind",
        "/",
        "/",
        "--dev",
        "/dev",
        "--proc",
        "/proc",
        "--unshare-pid",
        "--unshare-ipc",
        "--unshare-uts",
        "--unshare-cgroup-try",
        "--new-session",
        "--tmpfs",
        "/tmp",
        "--tmpfs",
        "/run",
        "--ro-bind-try",
        "/run/systemd/resolve",
        "/run/systemd/resolve",
    ]
    for path in sockets or ():
        wrapper += ["--ro-bind", "/dev/null", path]
    wrapper += [
        "--ro-bind",
        binary,
        binary,
        "--bind",
        str(clone),
        str(clone),
        "--chdir",
        str(clone),
        "--die-with-parent",
        "--clearenv",
    ]
    for key, value in sorted(env.items()):
        wrapper += ["--setenv", key, value]
    return wrapper + argv


def listening_sockets(table: str, clone: Path) -> list[str]:
    """Listening path sockets from `/proc/net/unix` that the mounts still show.

    Sockets under /run, /var/run and /tmp are hidden by their own mounts and
    the clone's are the worker's; an abstract socket has no path to mask.
    """
    found = []
    for line in table.splitlines()[1:]:
        fields = line.split(None, 7)
        if len(fields) < 8 or not int(fields[3], 16) & 0x10000:  # __SO_ACCEPTCON
            continue
        path = fields[7]
        if not path.startswith("/") or path.startswith(("/run/", "/var/run/", "/tmp/")):
            continue
        if path == str(clone) or path.startswith(str(clone) + "/"):
            continue
        found.append(path)
    return sorted(set(found))


def _host_sockets(clone: Path) -> list[str]:
    try:
        with open("/proc/net/unix", encoding="utf-8", errors="replace") as handle:
            table = handle.read(OUTPUT_LIMIT)
    except OSError:
        return []
    # ponytail: a socket created after this read stays reachable; a network
    # namespace with an API proxy would close abstract and late sockets too.
    found = []
    for path in listening_sockets(table, clone):
        try:
            if stat.S_ISSOCK(os.lstat(path).st_mode):
                found.append(path)
        except OSError:
            continue  # gone, or behind a directory this user cannot read
    return found


def _systemctl(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["systemctl", "--user", *args],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=SCOPE_TIMEOUT,
        check=False,
    )


def stop_scope(scope: str) -> bool:
    """Stop the scope and every process in it; True once it is gone."""
    try:
        _systemctl("stop", "--quiet", f"{scope}.scope")
        state = _systemctl("is-active", f"{scope}.scope").stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return False
    return state in ("inactive", "failed", "unknown", "")


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


def _prepare_child(admission=None, reservation=None) -> None:
    """Bound output and clear an inherited signal mask so cancel reaches the child.

    A caller such as `qa.py` may run with SIGINT and SIGTERM blocked; a worker
    that kept that mask would ignore SIGTERM and run on until SIGKILL.
    """
    _limit_output()
    signal.pthread_sigmask(signal.SIG_SETMASK, set())
    if admission is not None and reservation is not None:
        admission.write_child_receipt(reservation)


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
    for stat_path in Path("/proc").glob("[0-9]*/stat"):
        try:
            fields = stat_path.read_text().rsplit(")", 1)[1].split()
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


def _tree_mib(path: Path) -> int:
    total = 0
    for directory, _, files in os.walk(path):
        for name in files:
            try:
                total += os.lstat(os.path.join(directory, name)).st_size
            except OSError:
                continue
    return total // (1024 * 1024)


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
    def __init__(
        self,
        root,
        plan,
        runtime,
        preflight,
        cancel,
        brief_revision,
        poll,
        admission,
        request_check=None,
        binaries=None,
    ):
        self.root = Path(root).resolve()
        self.request_check = request_check
        self.binaries = binaries or {}
        self.admission = admission or ADMISSION.Admission(self.root)
        if self.admission.root != self.root:
            raise _fail(
                "ENV_BINDING", "admission workspace does not match dispatcher root"
            )
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
                "provider": self.units[uid]["provider"],
                "scope": None,
                "session": None,
                "cost_usd": None,
                "turns": None,
                "usage": None,
            }
            for uid in self.order
        }
        self.running: dict[str, dict[str, Any]] = {}
        self.checking: subprocess.Popen | None = None
        self.unreleased = False
        self.release_error: str | None = None
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
                {
                    "unit": uid,
                    "pid": w["proc"].pid,
                    "clone": str(w["clone"]),
                    "scope": w["scope"],
                }
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

    def release(self, token: str, scope: str | None = None) -> None:
        def absent(row):
            found = _owned_process_absent(self.admission, row, self.id)
            if found and scope is not None and not stop_scope(scope):
                return False  # a descendant outside the group still runs
            return found

        try:
            self.admission.release(token, absent)
        except (ADMISSION.AdmissionError, OSError) as exc:
            self.unreleased = True
            self.release_error = str(exc)
            raise

    def mark_started(self, token: str, proc: subprocess.Popen) -> None:
        try:
            receipt = self.admission.child_receipt_path(token).read_bytes()
            pid, start, pgid, uid = map(int, receipt.split())
        except (OSError, ValueError) as exc:
            raise _fail(
                "ENV_STATE", f"child process receipt is unavailable: {exc}"
            ) from exc
        if len(receipt) > 128 or (pid, pgid, uid) != (proc.pid, proc.pid, os.geteuid()):
            raise _fail("ENV_STATE", "child process receipt does not match the spawn")
        self.admission.mark_started(token, proc.pid, start)

    def provider_ready(self, unit) -> str | None:
        """For a provider unit, the current brief and the resolved CLI binary."""
        if unit["provider"] == "command":
            return None
        if self.request_check is None:
            raise _fail("PARALLEL_BRIEF", "a provider worker needs a current request")
        try:
            self.request_check()
        except ParallelError:
            raise
        except Exception as exc:  # the brief module's own refusal
            raise _fail("PARALLEL_BRIEF", str(exc)) from None
        found = self.binaries.get(unit["provider"]) or shutil.which(unit["provider"])
        if not found:
            raise _fail("PARALLEL_EXEC", f"{unit['provider']} is not installed")
        return os.path.realpath(found)

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
            binary = self.provider_ready(unit)
        except ParallelError as exc:
            self.leases.release(tokens)
            rec.update(state="refused", reason=str(exc))
            return
        rec["attempts"] += 1
        begin = time.monotonic()
        clone = self.dir / f"clone-{uid}-{rec['attempts']}"
        reservation = None
        proc = None
        try:
            reservation = self.admission.reserve(
                self.id,
                "worker",
                unit["closure"],
                {
                    "cpu": 1,
                    "memory_mib": unit["memory_mb"],
                    "disk_mib": WORKER_DISK_MIB,
                    "seconds": math.ceil(unit["timeout"]),
                    "instances": 0,
                },
                {"unit": uid, "attempt": rec["attempts"], "clone": str(clone)},
            )
            clone, tree = self.clone(clone.name[6:], self.upstream(uid))
            self.timing["setup"] += time.monotonic() - begin
            env = self.env(
                HYK8S_PARALLEL_UNIT=uid,
                HYK8S_PARALLEL_ATTEMPT=str(rec["attempts"]),
                HYK8S_PARALLEL_TOKENS=json.dumps(tokens, sort_keys=True),
                HYK8S_ENV_TOKEN=reservation,
            )
            meta = _git_meta(clone)  # the baseline, before the worker can run
            stem = self.dir / f"{uid}-{rec['attempts']}"
            scope = None
            argv, stdin = unit.get("command"), None
            if binary is not None:
                scope = f"hyk8s-par-{self.id}-{uid}-{rec['attempts']}"
                stem.with_suffix(".prompt").write_text(unit["prompt"])
                argv = contain(
                    provider_argv(unit, clone, binary),
                    scope=scope,
                    clone=clone,
                    binary=binary,
                    memory_mb=unit["memory_mb"],
                    timeout=unit["timeout"],
                    sockets=_host_sockets(clone),
                    env={
                        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                        "HOME": str(Path.home()),
                        "LANG": "C.UTF-8",
                        "TMPDIR": "/tmp",
                        **{
                            k: v
                            for k, v in env.items()
                            if k.startswith("HYK8S_PARALLEL_") or k == "HYK8S_ENV_TOKEN"
                        },
                    },
                )
                # Only what systemd-run needs to reach the user manager.
                env = {k: v for k, v in env.items() if k in SCOPE_ENV}
                stdin = stem.with_suffix(".prompt").open("rb")
            try:
                with (
                    stem.with_suffix(".log").open("wb") as log,
                    stem.with_suffix(".out").open("wb") as out,
                ):
                    proc = subprocess.Popen(
                        argv,
                        cwd=clone,
                        env=env,
                        stdin=stdin or subprocess.DEVNULL,
                        stdout=log if binary is None else out,
                        stderr=subprocess.STDOUT if binary is None else log,
                        start_new_session=True,
                        preexec_fn=lambda: _prepare_child(self.admission, reservation),
                    )
            finally:
                if stdin is not None:
                    stdin.close()
                stem.with_suffix(".prompt").unlink(missing_ok=True)
            rec["scope"] = scope
            self.mark_started(reservation, proc)
        except (
            ParallelError,
            ADMISSION.AdmissionError,
            OSError,
            ValueError,
            subprocess.SubprocessError,
        ) as exc:
            if proc is not None:
                _kill_group(proc.pid, proc)
                try:
                    proc.wait(timeout=GRACE)
                except subprocess.TimeoutExpired:
                    pass
            released = reservation is None
            if reservation is not None:
                try:
                    self.release(reservation, rec["scope"])
                    released = True
                except (ADMISSION.AdmissionError, OSError):
                    pass
            if released:
                self.leases.release(tokens)
            if released:
                _remove(self.dir, clone)
            code = (
                exc
                if isinstance(exc, (ParallelError, ADMISSION.AdmissionError))
                else f"PARALLEL_EXEC: {exc}"
            )
            rec.update(
                state="refused"
                if isinstance(exc, ADMISSION.AdmissionError) and reservation is None
                else "failed",
                reason=str(code),
            )
            return
        self.pids.append(proc.pid)
        rec["started"] = self.now()
        self.running[uid] = {
            "proc": proc,
            "clone": clone,
            "tree": tree,
            "meta": meta,
            "tokens": tokens,
            "reservation": reservation,
            "scope": scope,
            "out": stem.with_suffix(".out"),
            "begin": time.monotonic(),
            "deadline": time.monotonic() + unit["timeout"],
        }
        self._save()

    def stop(self, uid: str) -> dict[str, Any]:
        work = self.running.pop(uid)
        _kill_group(work["proc"].pid, work["proc"])
        if work["scope"] is not None:
            stop_scope(work["scope"])
        try:
            work["proc"].wait(timeout=GRACE)
        except subprocess.TimeoutExpired:
            pass  # verified absence, below, decides whether the lease can release
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
            try:
                self.release(work["reservation"], work["scope"])
            except (ADMISSION.AdmissionError, OSError) as exc:
                rec.update(state="failed", reason=str(exc))
            else:
                self.leases.release(work["tokens"])
                _remove(self.dir, work["clone"])

    def promote(self, uid: str, work: dict[str, Any]) -> None:
        unit, rec = self.units[uid], self.rec[uid]
        clone = work["clone"]
        if work["scope"] is not None:
            with work["out"].open("rb") as handle:
                parsed = parse_result(unit["provider"], handle.read(OUTPUT_LIMIT))
            error = parsed.pop("error")
            rec.update(parsed)
            if error:
                rec.update(state="failed", reason=error)
                return
        used = _tree_mib(clone)
        if used > WORKER_DISK_MIB:  # monitored at collection, not a hard quota
            rec.update(
                state="refused",
                reason=f"PARALLEL_DISK: clone uses {used} MiB of {WORKER_DISK_MIB}",
            )
            return
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
        reservation = None
        proc = None
        released = False
        try:
            reservation = self.admission.reserve(
                self.id,
                "integration",
                [],
                {
                    "cpu": 1,
                    "memory_mib": INTEGRATION_MEMORY_MIB,
                    "disk_mib": WORKER_DISK_MIB,
                    "seconds": MAX_TIMEOUT,
                    "instances": 0,
                },
                {"unit": "integration", "clone": str(self.dir / "clone-integration")},
            )
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
                proc = subprocess.Popen(
                    self.plan["integration_check"],
                    cwd=path,
                    env=self.env(
                        HYK8S_PARALLEL_UNIT="integration", HYK8S_ENV_TOKEN=reservation
                    ),
                    stdin=subprocess.DEVNULL,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    preexec_fn=lambda: _prepare_child(self.admission, reservation),
                )
            self.checking = proc
            self.mark_started(reservation, proc)
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
        except (
            ParallelError,
            ADMISSION.AdmissionError,
            OSError,
            ValueError,
            subprocess.SubprocessError,
        ) as exc:
            return {"state": "ERROR", "reason": str(exc)}, None
        finally:
            if proc is not None:
                _kill_group(proc.pid, proc)
                try:
                    proc.wait(timeout=GRACE)
                except subprocess.TimeoutExpired:
                    pass
                self.checking = None
                self._save()
            if reservation is not None:
                try:
                    self.release(reservation)
                    released = True
                except (ADMISSION.AdmissionError, OSError):
                    pass
            if path is not None and (reservation is None or released):
                _remove(self.dir, path)
            self.timing["integration_seconds"] = round(time.monotonic() - begin, 3)

    def execute(self) -> dict[str, Any]:
        finished = False
        try:
            finished = self.loop()
        finally:
            for uid in list(self.running):
                work = self.stop(uid)
                try:
                    self.release(work["reservation"], work["scope"])
                except (ADMISSION.AdmissionError, OSError) as exc:
                    self.rec[uid].update(state="failed", reason=str(exc))
                else:
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
        if self.unreleased:
            integration = {
                "state": "ERROR",
                "reason": self.release_error
                or "ENV_STATE: owned resource absence is unverified",
            }
            candidate = None
        if self.unreleased:
            state = "failed"
        elif not finished or integration["state"] == "CANCELLED":
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
        if not self.unreleased:
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
    admission=None,
    request_check: Callable[[], None] | None = None,
    binaries: dict[str, str] | None = None,
) -> dict[str, Any]:
    root = Path(root).resolve()
    if closure is None:

        def closure(selection):
            return CLUSTER.plan(CLUSTER.catalog(root), selection)

    checked = load_plan(plan, closure=closure)
    return _Run(
        root,
        checked,
        runtime,
        preflight,
        cancel,
        brief_revision,
        poll,
        admission,
        request_check,
        binaries,
    ).execute()


def _group_alive(pid: int) -> bool | None:
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return None
    return _live_members(pid)


def _owned_process_absent(
    admission, row: dict[str, Any], run_id: str, *, kill: bool = False
) -> bool | None:
    """Verify a reserved child's receipt and group before releasing its lease."""
    if (
        row["run_id"] != run_id
        or row["workspace_id"] != admission.workspace_id
        or row["binding_id"] != admission.binding_id
        or row["kind"] not in {"worker", "integration"}
    ):
        return None
    try:
        descriptor = os.open(
            admission.child_receipt_path(row["token"]), os.O_RDONLY | os.O_NOFOLLOW
        )
    except FileNotFoundError:
        return True if row["pid"] is None else None
    except OSError:
        return None
    try:
        metadata = os.fstat(descriptor)
        if metadata.st_uid != os.geteuid() or not stat.S_ISREG(metadata.st_mode):
            return None
        raw = os.read(descriptor, 128)
    finally:
        os.close(descriptor)
    parts = raw.split()
    if len(raw) >= 128 or len(parts) != 4 or any(not part.isdigit() for part in parts):
        return None
    pid, start_ticks, pgid, uid = (int(part) for part in parts)
    if uid != os.geteuid() or pid <= 0 or pgid != pid or start_ticks <= 0:
        return None
    if row["pid"] is not None and (row["pid"], row["start_ticks"]) != (
        pid,
        start_ticks,
    ):
        return None
    active = _group_alive(pgid)
    if active is None:
        return None
    current_start = ADMISSION._process_start(pid)
    if active and current_start not in (None, start_ticks):
        return None  # PID was reused; the current group is not this child.
    if active and current_start is None and Path(f"/proc/{pid}").exists():
        return None  # a present but unreadable leader cannot establish identity
    if active and kill:
        _kill_group(pgid)
        active = _group_alive(pgid)
    return active is False


def sweep(runtime: Path, *, root: Path | None = None, admission=None) -> list[str]:
    """Reclaim a dead dispatcher's owned groups and clones using persisted receipts."""
    admission = admission or ADMISSION.Admission(root or Path.cwd())
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
                rows = admission.active_for_run(run_dir.name)
                if not rows and any(
                    _group_alive(int(worker["pid"])) is not False
                    for worker in state.get("workers", [])
                ):
                    continue  # a live or unknown group has no ownership receipt
                if any(
                    row["workspace_id"] != admission.workspace_id
                    or row["binding_id"] != admission.binding_id
                    for row in rows
                ):
                    continue
                for worker in state.get("workers", []):
                    scope = worker.get("scope")
                    if scope and scope.startswith(f"hyk8s-par-{run_dir.name}-"):
                        stop_scope(scope)
                for row in rows:
                    admission.release(
                        row["token"],
                        lambda current: _owned_process_absent(
                            admission, current, run_dir.name, kill=True
                        ),
                    )
        except (ADMISSION.AdmissionError, OSError, ValueError, KeyError, TypeError):
            continue  # gone, being swept, or unreadable: leave it for a person
        shutil.rmtree(run_dir, ignore_errors=True)
        if not run_dir.exists():
            cleaned.append(run_dir.name)
    return cleaned


def _request_check(root: Path, request: str | None):
    if not request:
        return None
    module = _load("_work_parallel_request", "request_brief.py")

    def check() -> None:
        try:
            module.current(request, str(Path(root).resolve()))
        except module.Refusal as exc:
            raise _fail("PARALLEL_BRIEF", str(exc)) from None

    return check


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    runner = sub.add_parser("run", help="validate, dispatch and integrate a plan")
    runner.add_argument("--root", type=Path, default=Path.cwd())
    runner.add_argument("--runtime", type=Path)
    runner.add_argument("--plan", type=Path, required=True)
    runner.add_argument("--brief", type=Path, required=True)
    runner.add_argument("--current-request", type=Path, required=True)
    runner.add_argument(
        "--request", help="the P08 request whose recorded brief provider workers need"
    )
    sweeper = sub.add_parser("sweep", help="reclaim runs whose dispatcher died")
    sweeper.add_argument("--root", type=Path, default=Path.cwd())
    sweeper.add_argument("--runtime", type=Path)
    args = parser.parse_args(argv)
    runtime = args.runtime or args.root / RUNTIME
    # An inherited block would stop the operator's cancel from arriving.
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGINT, signal.SIGTERM})
    try:
        if args.command == "sweep":
            print(json.dumps({"cleaned": sweep(runtime, root=args.root)}))
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
            request_check=_request_check(args.root, args.request),
        )
    except (ParallelError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0 if report["state"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
