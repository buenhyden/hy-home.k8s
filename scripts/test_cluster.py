#!/usr/bin/env python3
"""Workspace-owned, throwaway k3d test clusters for selected GitOps apps (W09-ENV).

`plan` derives the closure of the selected root Applications from their own
rendered manifests: an app needs the local app that creates each namespace it
uses (Application overrides such as a destination namespace are not read).
Empty, whole (`all`, wildcards), root App-of-Apps, chart-sourced, CRD-dependent
and cyclic selections are refused, and a closure above APP_LIMIT is refused.
`up` creates one cluster per run: one server, no load balancer, the API
published on 127.0.0.1 only (checked after creation), a run-ID label on its
node container, and its own kubeconfig in the git-ignored
`.workspace-test/<run>/`; every cluster tool runs with that kubeconfig, so the
default kubeconfig is never changed. Only `doctor` reads the default
kubeconfig's current-context name. A failed or interrupted `up` deletes its
cluster, or leaves a `failed` state that `sweep` reclaims. `down`, `status`
and `sweep` treat a cluster as owned only when its name, Docker label and state
file all match a run of this workspace. No secret, host socket or production
kubeconfig is passed into a cluster.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any, Sequence

import yaml

PREFIX = "hyk8s-test-"
LABEL = "hy-home.k8s/run"
RUNTIME = ".workspace-test"
K3S_IMAGE = "rancher/k3s:v1.35.0-k3s1"
PROBE_IMAGE = "busybox:1.37"
APP_LIMIT = 4
STEP_TIMEOUT = 300
OUTPUT_LIMIT = 32 * 1024 * 1024
POLICY_SETTLE_SECONDS = 5
RUN_ID = re.compile(r"[a-z0-9]{8}")
HOST = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]{0,252}")
PORT = re.compile(r"[0-9]{1,5}")
BUILTIN_GROUPS = frozenset(
    {
        "core",
        "apps",
        "batch",
        "rbac.authorization.k8s.io",
        "networking.k8s.io",
        "discovery.k8s.io",
        "policy",
        "autoscaling",
        "coordination.k8s.io",
        "scheduling.k8s.io",
        "storage.k8s.io",
    }
)
ROOT_KINDS = frozenset({"Application", "ApplicationSet", "AppProject"})
WHOLE = frozenset({"all", "root", "everything"})


class ClusterError(Exception):
    """A stable diagnostic: CODE: detail."""


def _group(api_version: str) -> str:
    return api_version.split("/")[0] if "/" in api_version else "core"


def _run(
    command: Sequence[str],
    *,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
    check: bool = True,
) -> str:
    try:
        result = subprocess.run(
            list(command),
            env=env,
            input=input_text if input_text is not None else "",
            capture_output=True,
            text=True,
            timeout=STEP_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ClusterError(
            f"CLUSTER_STEP_FAILED: {command[0]} {type(exc).__name__}"
        ) from exc
    if len(result.stdout) > OUTPUT_LIMIT:
        raise ClusterError(
            f"CLUSTER_STEP_FAILED: {command[0]} output exceeds the limit"
        )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()[-1:] or [""]
        raise ClusterError(
            f"CLUSTER_STEP_FAILED: {' '.join(command[:3])}: {detail[0][:200]}"
        )
    return result.stdout


def render(root: Path, path: str) -> list[dict[str, Any]]:
    output = _run(["kubectl", "kustomize", str(root / path)])
    return [doc for doc in yaml.safe_load_all(output) if isinstance(doc, dict)]


def _entry(root: Path, doc: dict[str, Any]) -> dict[str, Any]:
    spec = doc.get("spec") or {}
    sources = spec.get("sources") or [spec.get("source") or {}]
    entry: dict[str, Any] = {
        "name": doc["metadata"]["name"],
        "path": None,
        "status": "supported",
        "reason": None,
        "creates": set(),
        "uses": set(),
    }
    source = sources[0]
    if len(sources) != 1 or not source.get("path"):
        entry.update(status="unsupported", reason="a remote chart source")
        return entry
    entry["path"] = source["path"]
    try:
        items = render(root, source["path"])
    except (ClusterError, yaml.YAMLError) as exc:
        entry.update(status="unsupported", reason=f"a render failure ({exc})"[:200])
        return entry
    for item in items:
        kind, group = item.get("kind"), _group(item.get("apiVersion", ""))
        metadata = item.get("metadata") or {}
        if kind in ROOT_KINDS:
            entry.update(status="root", reason="the App-of-Apps root")
        elif group not in BUILTIN_GROUPS and entry["status"] == "supported":
            entry.update(status="unsupported", reason=f"the CRD group {group}")
        if kind == "Namespace":
            entry["creates"].add(metadata.get("name"))
        if metadata.get("namespace"):
            entry["uses"].add(metadata["namespace"])
    return entry


def catalog(root: Path) -> dict[str, dict[str, Any]]:
    """Every root Application with its support status, created and used namespaces."""

    apps: dict[str, dict[str, Any]] = {}
    for file in sorted((root / "gitops" / "apps" / "root").glob("*.yaml")):
        for doc in yaml.safe_load_all(file.read_text(encoding="utf-8")):
            if isinstance(doc, dict) and doc.get("kind") == "Application":
                entry = _entry(root, doc)
                apps[entry["name"]] = entry
    providers = {
        namespace: app["name"]
        for app in apps.values()
        if app["status"] == "supported"
        for namespace in app["creates"]
    }
    for app in apps.values():
        missing = sorted(app["uses"] - set(providers))
        if app["status"] == "supported" and missing:
            app.update(
                status="unsupported", reason=f"no local app creates {missing[0]}"
            )
        app["requires"] = sorted(
            {providers[n] for n in app["uses"] if n in providers} - {app["name"]}
        )
    return apps


def plan(apps: dict[str, dict[str, Any]], selection: Sequence[str]) -> list[str]:
    if not selection:
        raise ClusterError("SELECTION_EMPTY: name at least one application")
    for name in selection:
        if name.lower() in WHOLE or any(ch in name for ch in "*?["):
            raise ClusterError(f"SELECTION_WHOLE: {name} selects everything")
        if name not in apps:
            raise ClusterError(f"SELECTION_UNKNOWN: {name}")
        if apps[name]["status"] == "root":
            raise ClusterError(f"SELECTION_ROOT: {name} is {apps[name]['reason']}")
    ordered: list[str] = []
    visiting: set[str] = set()

    def visit(name: str) -> None:
        app = apps[name]
        if app["status"] != "supported":
            raise ClusterError(f"SELECTION_UNSUPPORTED: {name} needs {app['reason']}")
        if name in ordered:
            return
        if name in visiting:
            raise ClusterError(f"SELECTION_CYCLE: {name} requires itself")
        visiting.add(name)
        for required in app["requires"]:
            visit(required)
        visiting.discard(name)
        ordered.append(name)

    for name in selection:
        visit(name)
    if len(ordered) > APP_LIMIT:
        raise ClusterError(f"SELECTION_LIMIT: {len(ordered)} apps exceed {APP_LIMIT}")
    return ordered


def free_port() -> int:
    with socket.socket() as probe_socket:
        probe_socket.bind(("127.0.0.1", 0))
        return probe_socket.getsockname()[1]


def create_command(name: str, run_id: str, port: int) -> list[str]:
    return [
        "k3d",
        "cluster",
        "create",
        name,
        "--servers",
        "1",
        "--agents",
        "0",
        "--no-lb",
        "--api-port",
        f"127.0.0.1:{port}",
        "--image",
        K3S_IMAGE,
        "--kubeconfig-update-default=false",
        "--kubeconfig-switch-context=false",
        "--runtime-label",
        f"{LABEL}={run_id}@server:0",
        "--k3s-arg",
        "--disable=traefik@server:0",
        "--k3s-arg",
        "--disable=servicelb@server:0",
        "--k3s-arg",
        "--disable=metrics-server@server:0",
        "--wait",
        "--timeout",
        "180s",
    ]


def tool_environment(state: Path, base: dict[str, str] | None = None) -> dict[str, str]:
    environment = {k: v for k, v in (base or os.environ).items() if k != "KUBECONFIG"}
    environment["KUBECONFIG"] = str(state / "kubeconfig")
    return environment


def _write_kubeconfig(name: str, path: Path, env: dict[str, str]) -> None:
    text = _run(["k3d", "kubeconfig", "get", name], env=env)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(text)


def _verify_loopback(name: str) -> None:
    """The API port must be published on 127.0.0.1 only."""

    output = _run(["docker", "port", f"k3d-{name}-server-0", "6443/tcp"])
    bindings = [line.strip() for line in output.splitlines() if line.strip()]
    if not bindings or any(not b.startswith("127.0.0.1:") for b in bindings):
        raise ClusterError(f"CLUSTER_EXPOSED: API published on {bindings}")


def _state_dir(root: Path, run_id: str) -> Path:
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
        raise ClusterError("CLUSTER_SCHEMA: a run ID is 8 lowercase letters or digits")
    return root / RUNTIME / run_id


def _write_state(root: Path, run_id: str, record: dict[str, Any]) -> None:
    directory = _state_dir(root, run_id)
    descriptor, name = tempfile.mkstemp(prefix="state.", dir=directory)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(record, handle)
    os.replace(name, directory / "state.json")


def _read_state(root: Path, run_id: str) -> dict[str, Any] | None:
    with contextlib.suppress(ClusterError, OSError, ValueError):
        record = json.loads(
            (_state_dir(root, run_id) / "state.json").read_text(encoding="utf-8")
        )
        if isinstance(record, dict) and record.get("run_id") == run_id:
            return record
    return None


def list_clusters() -> list[dict[str, Any]]:
    return json.loads(_run(["k3d", "cluster", "list", "-o", "json"]) or "[]") or []


def labelled_runs() -> dict[str, str]:
    """Cluster name to run ID, read from the run label on the node containers."""

    output = _run(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"label={LABEL}",
            "--format",
            f'{{{{.Label "k3d.cluster"}}}} {{{{.Label "{LABEL}"}}}}',
        ]
    )
    runs = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 2:
            runs[parts[0]] = parts[1]
    return runs


def up(
    root: Path, selection: Sequence[str], *, run_id: str | None = None
) -> dict[str, Any]:
    apps = catalog(root)
    ordered = plan(apps, selection)
    run_id = run_id or uuid.uuid4().hex[:8]
    state = _state_dir(root, run_id)
    name = PREFIX + run_id
    if name in {c.get("name") for c in list_clusters()}:
        raise ClusterError(f"CLUSTER_EXISTS: {name} already exists")
    state.mkdir(parents=True, mode=0o700)
    record = {
        "run_id": run_id,
        "cluster": name,
        "apps": ordered,
        "pid": os.getpid(),
        "status": "creating",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    _write_state(root, run_id, record)
    env = tool_environment(state)
    try:
        _run(create_command(name, run_id, free_port()), env=env)
        _verify_loopback(name)
        _write_kubeconfig(name, state / "kubeconfig", env)
        for app in ordered:
            _run(["kubectl", "apply", "-k", str(root / apps[app]["path"])], env=env)
    except BaseException:
        deleted = False
        with contextlib.suppress(ClusterError):
            _run(["k3d", "cluster", "delete", name], env=env)
            deleted = True
        with contextlib.suppress(ClusterError):
            deleted = deleted or name not in {c.get("name") for c in list_clusters()}
        if deleted:
            shutil.rmtree(state, ignore_errors=True)
        else:
            _write_state(root, run_id, record | {"status": "failed", "pid": None})
        raise
    record["status"] = "up"
    _write_state(root, run_id, record)
    return record


def _owned(root: Path, name: str, labels: dict[str, str]) -> bool:
    if not name.startswith(PREFIX):
        return False
    run_id = name[len(PREFIX) :]
    return (
        RUN_ID.fullmatch(run_id) is not None
        and _read_state(root, run_id) is not None
        and labels.get(name) == run_id
    )


def down(root: Path, run_id: str) -> dict[str, Any]:
    record = _read_state(root, run_id)
    name = PREFIX + run_id
    listed = {c.get("name") for c in list_clusters()}
    if (
        record is None
        or record.get("cluster") != name
        or (name in listed and labelled_runs().get(name) != run_id)
    ):
        raise ClusterError(
            f"CLUSTER_NOT_OWNED: {name} has no matching run state and label"
        )
    if name in listed:
        _run(
            ["k3d", "cluster", "delete", name],
            env=tool_environment(_state_dir(root, run_id)),
        )
    shutil.rmtree(_state_dir(root, run_id), ignore_errors=True)
    return {"deleted": name}


def status(root: Path) -> list[dict[str, Any]]:
    labels = labelled_runs()
    return [
        {"name": c["name"], "owned": _owned(root, c["name"], labels)}
        for c in list_clusters()
        if str(c.get("name", "")).startswith(PREFIX)
    ]


def _alive(pid: Any) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def sweep(root: Path) -> dict[str, list[str]]:
    """Reclaim owned clusters left by a dead or failed `up`; report the rest."""

    result: dict[str, list[str]] = {
        "deleted": [],
        "failed": [],
        "kept": [],
        "unowned": [],
    }
    labels = labelled_runs()
    listed = {str(c.get("name", "")) for c in list_clusters()}
    for name in sorted(n for n in listed if n.startswith(PREFIX)):
        if not _owned(root, name, labels):
            result["unowned"].append(name)
            continue
        record = _read_state(root, name[len(PREFIX) :]) or {}
        if record.get("status") == "up" or _alive(record.get("pid")):
            result["kept"].append(name)
            continue
        try:
            down(root, record["run_id"])
            result["deleted"].append(name)
        except ClusterError:
            result["failed"].append(name)
    runtime = root / RUNTIME
    for directory in sorted(runtime.iterdir()) if runtime.is_dir() else []:
        record = (
            _read_state(root, directory.name)
            if RUN_ID.fullmatch(directory.name)
            else None
        )
        stale = record is None or (
            record.get("cluster") not in listed and not _alive(record.get("pid"))
        )
        if directory.is_dir() and stale and record is not None:
            shutil.rmtree(directory, ignore_errors=True)
    return result


def probe_policy(cidr: str) -> dict[str, Any]:
    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {"name": "deny-production-lan"},
        "spec": {
            "podSelector": {},
            "policyTypes": ["Egress"],
            "egress": [{"to": [{"ipBlock": {"cidr": "0.0.0.0/0", "except": [cidr]}}]}],
        },
    }


def probe(root: Path, run_id: str, target: str, cidr: str) -> dict[str, Any]:
    """Reachability of target from an open and a LAN-denied harness namespace.

    Each pod prints its own connect result; a pod without one makes the probe
    invalid. A closed port on the same host must read as unreachable from the
    open namespace, or the probe is not valid.
    """

    host, _, port = target.rpartition(":")
    if not HOST.fullmatch(host) or not PORT.fullmatch(port):
        raise ClusterError("CLUSTER_SCHEMA: target is HOST:PORT")
    if _read_state(root, run_id) is None:
        raise ClusterError("CLUSTER_NOT_OWNED: no run state")
    env = tool_environment(_state_dir(root, run_id))
    _run(["kubectl", "create", "namespace", "hyk8s-probe-open"], env=env, check=False)
    _run(["kubectl", "create", "namespace", "hyk8s-probe-denied"], env=env, check=False)
    _run(
        ["kubectl", "apply", "-n", "hyk8s-probe-denied", "-f", "-"],
        env=env,
        input_text=json.dumps(probe_policy(cidr)),
    )
    # A new namespace gets its default service account asynchronously, and the
    # policy controller needs a moment to install the rule.
    for namespace in ("hyk8s-probe-open", "hyk8s-probe-denied"):
        for _ in range(30):
            try:
                _run(
                    ["kubectl", "get", "serviceaccount", "default", "-n", namespace],
                    env=env,
                )
                break
            except ClusterError:
                time.sleep(1)
    time.sleep(POLICY_SETTLE_SECONDS)

    def reach(namespace: str, check_port: str) -> str | None:
        output = _run(
            [
                "kubectl",
                "run",
                f"probe-{uuid.uuid4().hex[:6]}",
                "-n",
                namespace,
                "--image",
                PROBE_IMAGE,
                "--restart=Never",
                "--rm",
                "-i",
                "--quiet",
                "--pod-running-timeout=180s",
                "--",
                "sh",
                "-c",
                # Wait so kubectl attaches before a fast connect exits.
                'sleep 2; nc -z -w 5 "$1" "$2"; echo rc=$?',
                "probe",
                host,
                check_port,
            ],
            env=env,
            check=False,
        )
        codes = re.findall(r"^rc=(\d+)\r?$", output, re.M)
        if len(codes) != 1:
            return None
        return "reachable" if codes[0] == "0" else "unreachable"

    open_target = reach("hyk8s-probe-open", port)
    closed_control = reach("hyk8s-probe-open", "1")
    denied_target = reach("hyk8s-probe-denied", port)
    valid = (
        open_target == "reachable"
        and closed_control == "unreachable"
        and denied_target is not None
    )
    return {
        "target": target,
        "denied_cidr": cidr,
        "open_namespace": open_target,
        "closed_port_control": closed_control,
        "denied_namespace": denied_target,
        "valid": valid,
        "denied": valid and denied_target == "unreachable",
    }


def doctor(root: Path) -> dict[str, Any]:
    def version(command: Sequence[str]) -> str | None:
        with contextlib.suppress(ClusterError):
            return _run(command).strip().splitlines()[0][:120]
        return None

    default = Path.home() / ".kube" / "config"
    context = None
    if default.is_file():
        with contextlib.suppress(ClusterError):
            context = _run(
                ["kubectl", "config", "current-context"],
                env={**os.environ, "KUBECONFIG": str(default)},
            ).strip()
    usage = shutil.disk_usage(root)
    tools = {
        name: version(command)
        for name, command in {
            "docker": ["docker", "version", "--format", "{{.Server.Version}}"],
            "k3d": ["k3d", "version"],
            "kubectl": ["kubectl", "version", "--client"],
        }.items()
    }
    return {
        "host": {
            "system": platform.platform(),
            "cpus": os.cpu_count(),
            "disk_free_gib": round(usage.free / 2**30, 1),
        },
        "tools": tools,
        "ready": all(tools.values()),
        "docker_socket_root_equivalent": Path("/var/run/docker.sock").exists(),
        "default_kubeconfig_current_context": context,
        "k3s_image": K3S_IMAGE,
        "runtime": str(root / RUNTIME),
    }


def _interrupt(signum: int, frame: Any) -> None:
    raise KeyboardInterrupt()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    commands.add_parser("catalog")
    for name in ("plan", "up"):
        sub = commands.add_parser(name)
        sub.add_argument("apps", nargs="*")
    probe_parser = commands.add_parser("probe")
    probe_parser.add_argument("run_id")
    probe_parser.add_argument("--target", required=True)
    probe_parser.add_argument("--deny-cidr", required=True)
    down_parser = commands.add_parser("down")
    down_parser.add_argument("run_id")
    commands.add_parser("status")
    commands.add_parser("sweep")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    for signum in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(signum, _interrupt)
    try:
        if args.command == "doctor":
            result: Any = doctor(root)
        elif args.command == "catalog":
            result = {
                name: {
                    k: sorted(v) if isinstance(v, set) else v for k, v in app.items()
                }
                for name, app in catalog(root).items()
            }
        elif args.command == "plan":
            result = plan(catalog(root), args.apps)
        elif args.command == "up":
            result = up(root, args.apps)
        elif args.command == "probe":
            result = probe(root, args.run_id, args.target, args.deny_cidr)
        elif args.command == "down":
            result = down(root, args.run_id)
        elif args.command == "status":
            result = status(root)
        else:
            result = sweep(root)
    except ClusterError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print(
            "CLUSTER_INTERRUPTED: run `sweep` to reclaim any leftover of this workspace",
            file=sys.stderr,
        )
        return 130
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
