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
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Sequence

import yaml
from environment_admission import Admission, AdmissionError, _process_start
import test_cluster_environment as CLUSTER_ENV
import test_cluster_vm as VM

PREFIX = "hyk8s-test-"
LABEL = "hy-home.k8s/run"
RUNTIME = ".workspace-test"
K3S_IMAGE = CLUSTER_ENV.K3S_IMAGE
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
    timeout: float = STEP_TIMEOUT,
    preexec_fn: Any = None,
) -> str:
    try:
        result = subprocess.run(
            list(command),
            env=env,
            input=input_text if input_text is not None else "",
            capture_output=True,
            text=True,
            timeout=min(STEP_TIMEOUT, timeout),
            **({"preexec_fn": preexec_fn} if preexec_fn is not None else {}),
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
        lines = [
            re.sub(r"\x1b\[[0-9;]*m", "", line)
            for line in (result.stderr or result.stdout).strip().splitlines()
        ] or [""]
        # k3d's last line is a FATA summary; its cause is the first ERRO line.
        detail = next((line for line in lines if line.startswith("ERRO")), lines[-1])
        raise ClusterError(
            f"CLUSTER_STEP_FAILED: {' '.join(command[:3])}: {detail[:200]}"
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


free_port = CLUSTER_ENV.free_port
create_command = CLUSTER_ENV.create_command
tool_environment = CLUSTER_ENV.tool_environment


def _write_kubeconfig(name: str, path: Path, env: dict[str, str], runner=None) -> None:
    text = (runner or _run)(["k3d", "kubeconfig", "get", name], env=env)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(text)


def _verify_loopback(name: str, runner=None) -> None:
    """The API port must be published on 127.0.0.1 only."""

    output = (runner or _run)(["docker", "port", f"k3d-{name}-server-0", "6443/tcp"])
    bindings = [line.strip() for line in output.splitlines() if line.strip()]
    if not bindings or any(not b.startswith("127.0.0.1:") for b in bindings):
        raise ClusterError(f"CLUSTER_EXPOSED: API published on {bindings}")


def _state_dir(root: Path, run_id: str) -> Path:
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
        raise ClusterError("CLUSTER_SCHEMA: a run ID is 8 lowercase letters or digits")
    return root / RUNTIME / run_id


def _write_state(root: Path, run_id: str, record: dict[str, Any]) -> None:
    CLUSTER_ENV.write_state(_state_dir(root, run_id), record)


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
    return CLUSTER_ENV.labelled_runs(_run)


def _resources_absent(run_id: str) -> bool:
    name = PREFIX + run_id
    return name not in {
        c.get("name") for c in list_clusters()
    } and CLUSTER_ENV.network_name(run_id) not in CLUSTER_ENV.network_names(
        _run, run_id
    )


def _cleanup_owned(run_id: str, env: dict[str, str]) -> bool:
    """Delete only resources whose current Docker labels match this run."""
    name = PREFIX + run_id
    network = CLUSTER_ENV.network_name(run_id)
    listed = {c.get("name") for c in list_clusters()}
    if name in listed:
        if labelled_runs().get(name) != run_id:
            return False
        _run(["k3d", "cluster", "delete", name], env=env)
    if network in CLUSTER_ENV.network_names(_run, run_id):
        _run(["docker", "network", "rm", network])
    return _resources_absent(run_id)


def up(
    root: Path,
    selection: Sequence[str],
    *,
    authority: str | None,
    run_id: str | None = None,
    admission: Admission | None = None,
    vm_capsule: Path | None = None,
) -> dict[str, Any]:
    # A live cluster action names the operator approval it runs under, or it
    # does nothing (infrastructure/AGENTS.md rule 1). The name is recorded, not
    # authenticated: whether the approval is real stays the caller's check.
    if not isinstance(authority, str) or not authority.strip():
        raise ClusterError("CLUSTER_AUTHORITY: name the operator approval for this run")
    apps = catalog(root)
    ordered = plan(apps, selection)
    rendered = {app: render(root, apps[app]["path"]) for app in ordered}
    try:
        profile = (
            CLUSTER_ENV.verified_guest_profile(vm_capsule)
            if vm_capsule is not None
            else {
                "cpu": 2,
                "memory_mib": 4096,
                "disk_mib": 4096,
                "seconds": 600,
                "instances": 1,
                "server_memory": "4g",
                "memory_margin_mib": 1024,
                "disk_margin_mib": 1024,
            }
        )
    except ValueError as exc:
        raise ClusterError(str(exc)) from exc
    try:
        CLUSTER_ENV.require_product_disk_cap(vm_capsule)
    except ValueError as exc:
        raise ClusterError(str(exc)) from exc
    run_id = run_id or uuid.uuid4().hex[:8]
    state = _state_dir(root, run_id)
    name = PREFIX + run_id
    network = CLUSTER_ENV.network_name(run_id)
    try:
        admission = admission or Admission(
            root,
            memory_margin_mib=profile["memory_margin_mib"],
            disk_margin_mib=profile["disk_margin_mib"],
        )
        token = admission.reserve(
            run_id,
            "cluster",
            ordered,
            {
                key: profile[key]
                for key in ("cpu", "memory_mib", "disk_mib", "seconds", "instances")
            },
            {
                "cluster": name,
                "network": network,
                "pid": os.getpid(),
                "start_ticks": _process_start(os.getpid()),
            },
        )
    except AdmissionError as exc:
        raise ClusterError(str(exc)) from exc
    record = {
        "run_id": run_id,
        "cluster": name,
        "network": network,
        "admission_token": token,
        "apps": ordered,
        "authority": authority.strip(),
        "pid": os.getpid(),
        "pid_start_ticks": _process_start(os.getpid()),
        "status": "creating",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "expires_at": time.time() + profile["seconds"],
    }
    deadline = time.monotonic() + profile["seconds"]

    def limited(command, **kwargs):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ClusterError(
                "CLUSTER_TIMEOUT: selected environment exceeded its budget"
            )
        if command[:3] in (
            ["k3d", "cluster", "create"],
            ["docker", "network", "create"],
        ):

            def before_create() -> None:
                os.setsid()
                admission.write_child_receipt(
                    token, "network" if command[0] == "docker" else None
                )

            kwargs["preexec_fn"] = before_create
        return _run(command, timeout=remaining, **kwargs)

    try:
        existing = {c.get("name") for c in list_clusters()}
    except (ClusterError, OSError, ValueError):
        admission.release(token, lambda _: True)  # only read-only discovery occurred
        raise
    if name in existing:
        admission.release(token, lambda _: True)  # no external resource was started
        raise ClusterError(f"CLUSTER_EXISTS: {name} already exists")
    try:
        state.mkdir(parents=True, mode=0o700)
        _write_state(root, run_id, record)
        try:
            if vm_capsule is None:
                CLUSTER_ENV.arm_expiry_timer(
                    limited,
                    root,
                    run_id,
                    token,
                    max(1, math.ceil(record["expires_at"] - time.time())),
                )
        except ValueError as exc:
            raise ClusterError(str(exc)) from exc
        limited(CLUSTER_ENV.create_network_command(network, run_id))
        try:
            CLUSTER_ENV.verify_network(limited, network, run_id)
        except ValueError as exc:
            raise ClusterError(str(exc)) from exc
        env = tool_environment(state)
        limited(
            create_command(
                name,
                run_id,
                free_port(),
                network,
                profile["server_memory"],
                profile["pause_tar"] if vm_capsule is not None else None,
            ),
            env=env,
        )
        try:
            CLUSTER_ENV.enforce_node_cpu(limited, name)
        except ValueError as exc:
            raise ClusterError(str(exc)) from exc
        _verify_loopback(name, limited)
        try:
            CLUSTER_ENV.verify_node_network(limited, name, network)
        except ValueError as exc:
            raise ClusterError(str(exc)) from exc
        _write_kubeconfig(name, state / "kubeconfig", env, limited)
        limited(
            [
                "kubectl",
                "wait",
                "--for=condition=Ready",
                "node",
                "--all",
                "--timeout=120s",
            ],
            env=env,
        )
        if vm_capsule is not None:
            try:
                record = record | CLUSTER_ENV.apply_selected_guest(
                    limited, root, apps, ordered, rendered, env, run_id, profile
                )
            except ValueError as exc:
                raise ClusterError(str(exc)) from exc
        else:
            for app in ordered:
                limited(
                    [
                        "kubectl",
                        "apply",
                        "--dry-run=server",
                        "-k",
                        str(root / apps[app]["path"]),
                    ],
                    env=env,
                )
                limited(
                    ["kubectl", "apply", "-k", str(root / apps[app]["path"])], env=env
                )
                for namespace in sorted(
                    {
                        item.get("metadata", {}).get("name")
                        for item in rendered[app]
                        if item.get("kind") == "Namespace"
                    }
                    - {None}
                ):
                    for item in CLUSTER_ENV.namespace_limits(namespace):
                        limited(
                            ["kubectl", "apply", "-f", "-"],
                            env=env,
                            input_text=json.dumps(item),
                        )
    except BaseException:
        deleted = False
        lease = None
        with contextlib.suppress(ClusterError, ValueError, OSError):
            lease = next(
                (
                    row
                    for row in admission.active_for_run(run_id)
                    if row["token"] == token
                ),
                None,
            )
            deleted = bool(
                lease
                and _cluster_owned(root, admission, lease, run_id, token, name)
                and _cleanup_owned(run_id, tool_environment(state))
            )
        if deleted:
            try:
                admission.release(
                    token,
                    lambda row: (
                        _cluster_owned(root, admission, row, run_id, token, name)
                        and not CLUSTER_ENV.create_inflight(admission, row["token"])
                        and _resources_absent(row["run_id"])
                    ),
                )
            except (AdmissionError, ClusterError, ValueError, OSError):
                deleted = False
        if deleted:
            if (
                lease
                and _read_state(root, run_id)
                and _cluster_owned(root, admission, lease, run_id, token, name)
            ):
                shutil.rmtree(state, ignore_errors=True)
            with contextlib.suppress(ValueError, ClusterError, OSError):
                CLUSTER_ENV.disarm_expiry_timer(_run, run_id, token)
        else:
            if state.is_dir():
                with contextlib.suppress(OSError, ValueError):
                    _write_state(root, run_id, record | {"status": "failed"})
        raise
    record["status"] = "up"
    _write_state(root, run_id, record)
    return record


_lease_matches_cluster = CLUSTER_ENV.lease_matches_cluster


def _cluster_owned(
    root: Path,
    admission: Admission,
    lease: dict[str, Any],
    run_id: str,
    token: str,
    name: str,
) -> bool:
    return CLUSTER_ENV.cluster_state_matches(
        root, admission, lease, run_id, token, name, _read_state
    )


def down(
    root: Path, run_id: str, *, admission: Admission | None = None
) -> dict[str, Any]:
    record = _read_state(root, run_id)
    if record and record.get("environment_kind") == "vm":
        from test_cluster_vm_lifecycle import down_host

        return down_host(sys.modules[__name__], root, record, admission=admission)
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
    admission = admission or Admission(root)
    token = record.get("admission_token")
    lease = next(
        (
            row
            for row in admission.active_for_run(run_id)
            if isinstance(token, str)
            and _cluster_owned(root, admission, row, run_id, token, name)
        ),
        None,
    )
    if lease is None:
        raise ClusterError("CLUSTER_NOT_OWNED: exact cluster lease is unavailable")
    if not CLUSTER_ENV.await_create_quiescent(admission, token):
        raise ClusterError(
            "CLUSTER_CLEANUP: exact cluster create is still active or unverified"
        )
    if not _cluster_owned(root, admission, lease, run_id, token, name):
        raise ClusterError("CLUSTER_NOT_OWNED: exact run state changed before cleanup")
    if not _cleanup_owned(run_id, tool_environment(_state_dir(root, run_id))):
        raise ClusterError(
            f"CLUSTER_CLEANUP: owned resources for {name} remain or are unverified"
        )
    try:
        admission.release(
            token,
            lambda row: (
                _cluster_owned(root, admission, row, run_id, token, name)
                and not CLUSTER_ENV.create_inflight(admission, row["token"])
                and _resources_absent(row["run_id"])
            ),
        )
    except AdmissionError as exc:
        raise ClusterError(str(exc)) from exc
    with contextlib.suppress(ValueError, ClusterError, OSError):
        CLUSTER_ENV.disarm_expiry_timer(_run, run_id, token)
    if _read_state(root, run_id) and _cluster_owned(
        root, admission, lease, run_id, token, name
    ):
        shutil.rmtree(_state_dir(root, run_id), ignore_errors=True)
    return {"deleted": name}


def expire(
    root: Path, run_id: str, token: str, *, admission: Admission | None = None
) -> dict[str, str]:
    """An owned timer may reclaim only its exact expired lease and resources."""
    admission = admission or Admission(root)
    record = _read_state(root, run_id)
    if record and record.get("environment_kind") == "vm":
        if not CLUSTER_ENV.vm_expiry_due(root, run_id, token, admission, record):
            return {"kept": run_id}
        try:
            return down(root, run_id, admission=admission)
        except (ClusterError, VM.VmError):
            from test_cluster_vm_lifecycle import recover_vm_intents

            if token not in recover_vm_intents(
                root, admission, _read_state, only_token=token
            ):
                raise
            return {"deleted": VM.unit_name(run_id)}
    lease = next(
        (
            row
            for row in admission.active_for_run(run_id)
            if _cluster_owned(root, admission, row, run_id, token, PREFIX + run_id)
        ),
        None,
    )
    if lease is None:
        return {"kept": run_id}
    if time.time() < (
        record.get("expires_at")
        if record
        else lease["created_at"] + lease["budget"]["seconds"]
    ):
        return {"kept": run_id}
    if (not record or record.get("status") != "up") and not CLUSTER_ENV.creator_gone(
        lease["intent"].get("pid"), lease["intent"].get("start_ticks")
    ):
        return {"kept": run_id}
    if CLUSTER_ENV.create_inflight(admission, token):
        return {"kept": run_id}
    if not _cluster_owned(root, admission, lease, run_id, token, PREFIX + run_id):
        return {"kept": run_id}
    if not _cleanup_owned(run_id, tool_environment(_state_dir(root, run_id))):
        raise ClusterError("CLUSTER_CLEANUP: owned resources remain or are unverified")
    admission.release(
        token,
        lambda row: (
            _cluster_owned(root, admission, row, run_id, token, PREFIX + run_id)
            and (
                (record and record.get("status") == "up")
                or CLUSTER_ENV.creator_gone(
                    row["intent"].get("pid"), row["intent"].get("start_ticks")
                )
            )
            and not CLUSTER_ENV.create_inflight(admission, row["token"])
            and _resources_absent(row["run_id"])
        ),
    )
    with contextlib.suppress(ValueError, ClusterError, OSError):
        CLUSTER_ENV.disarm_expiry_timer(_run, run_id, token)
    if _read_state(root, run_id) and _cluster_owned(
        root, admission, lease, run_id, token, PREFIX + run_id
    ):
        shutil.rmtree(_state_dir(root, run_id), ignore_errors=True)
    return {"deleted": PREFIX + run_id}


def status(root: Path) -> list[dict[str, Any]]:
    labels = labelled_runs()
    return [
        {
            "name": c["name"],
            "owned": CLUSTER_ENV.owned_cluster(
                root, c["name"], labels, _read_state, PREFIX
            ),
        }
        for c in list_clusters()
        if str(c.get("name", "")).startswith(PREFIX)
    ] + VM.status_host(root, _read_state)


def sweep(root: Path, *, admission: Admission | None = None) -> dict[str, list[str]]:
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
        if not CLUSTER_ENV.owned_cluster(root, name, labels, _read_state, PREFIX):
            result["unowned"].append(name)
            continue
        record = _read_state(root, name[len(PREFIX) :]) or {}
        active_creator = not CLUSTER_ENV.creator_gone(
            record.get("pid"), record.get("pid_start_ticks")
        )
        still_leased = record.get("status") == "up" and time.time() < record.get(
            "expires_at", float("inf")
        )
        if still_leased or (record.get("status") != "up" and active_creator):
            result["kept"].append(name)
            continue
        try:
            down(root, record["run_id"], admission=admission)
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
        if record and record.get("environment_kind") == "vm":
            if (
                CLUSTER_ENV.vm_start_inflight(root, record, admission) is not False
                or record.get("status") == "up"
                and time.time() < record.get("expires_at", 0)
                and VM.is_active(root, record)
            ):
                result["kept"].append(record["unit"])
            else:
                try:
                    down(root, directory.name, admission=admission)
                    result["deleted"].append(record["unit"])
                except (ClusterError, VM.VmError):
                    result["failed"].append(record["unit"])
    if admission is not None:
        releasable: dict[str, dict[str, Any]] = {}

        def eligible(lease):
            if not _cluster_owned(
                root,
                admission,
                lease,
                lease["run_id"],
                lease["token"],
                PREFIX + lease["run_id"],
            ) or lease["intent"].get("unit"):
                return False
            record = _read_state(root, lease["run_id"])
            intent = lease["intent"]
            creator = intent.get("pid")
            active = not CLUSTER_ENV.creator_gone(creator, intent.get("start_ticks"))
            future = time.time() < lease["created_at"] + lease["budget"]["seconds"]
            if (
                (active and (not record or record.get("status") != "up"))
                or (future and record and record.get("status") == "up")
                or CLUSTER_ENV.create_inflight(admission, lease["token"])
            ):
                return False
            return True

        from test_cluster_vm_lifecycle import recover_vm_intents

        recover_vm_intents(root, admission, _read_state)
        cleaned: set[str] = set()
        for lease in admission.active_for_binding():
            if not eligible(lease):
                continue
            try:
                if _cleanup_owned(
                    lease["run_id"], tool_environment(_state_dir(root, lease["run_id"]))
                ):
                    cleaned.add(lease["token"])
            except (ClusterError, OSError, ValueError):
                continue

        def absent(lease):
            if (
                lease["token"] not in cleaned
                or not eligible(lease)
                or not _resources_absent(lease["run_id"])
            ):
                return None
            record = _read_state(root, lease["run_id"])
            if record:
                releasable[lease["token"]] = lease
            return True

        released = admission.recover(absent)
        for token in released:
            lease = releasable.get(token)
            run_id = lease["run_id"] if lease else None
            record = _read_state(root, run_id) if run_id else None
            if (
                lease
                and record
                and _cluster_owned(
                    root, admission, lease, run_id, token, PREFIX + run_id
                )
            ):
                try:
                    shutil.rmtree(_state_dir(root, run_id))
                except OSError:
                    result["failed"].append(PREFIX + run_id)
    return result


probe_policy = CLUSTER_ENV.probe_policy


def probe(root: Path, run_id: str, target: str, cidr: str) -> dict[str, Any]:
    """Reachability of target from an open and a LAN-denied harness namespace.

    Each pod prints its own connect result; a pod without one makes the probe
    invalid. A closed port on the same host must read as unreachable from the
    open namespace, or the probe is not valid.
    """

    host, _, port = target.rpartition(":")
    if not HOST.fullmatch(host) or not PORT.fullmatch(port):
        raise ClusterError("CLUSTER_SCHEMA: target is HOST:PORT")
    record = _read_state(root, run_id)
    if record is None:
        raise ClusterError("CLUSTER_NOT_OWNED: no run state")
    authority = record.get("authority")
    if not isinstance(authority, str) or not authority.strip():
        raise ClusterError("CLUSTER_AUTHORITY: the run names no operator approval")
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
    return CLUSTER_ENV.doctor(root, _run, ClusterError, K3S_IMAGE, RUNTIME)


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
        if name == "up":
            sub.add_argument(
                "--authority",
                required=True,
                help="the operator approval this live run is made under",
            )
            sub.add_argument("--vm-capsule", type=Path, help=argparse.SUPPRESS)
            sub.add_argument(
                "--vm", action="store_true", help="use an owned bounded local VM"
            )
            sub.add_argument("--run-id", help="owned eight-character run ID")
    probe_parser = commands.add_parser("probe")
    probe_parser.add_argument("run_id")
    probe_parser.add_argument("--target", required=True)
    probe_parser.add_argument("--deny-cidr", required=True)
    down_parser = commands.add_parser("down")
    down_parser.add_argument("run_id")
    expire_parser = commands.add_parser("expire")
    expire_parser.add_argument("run_id")
    expire_parser.add_argument("token")
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
            if args.vm:
                from test_cluster_vm_lifecycle import up_host

                result = up_host(
                    sys.modules[__name__],
                    root,
                    args.apps,
                    args.authority,
                    run_id=args.run_id,
                )
            else:
                result = up(
                    root,
                    args.apps,
                    authority=args.authority,
                    run_id=args.run_id,
                    vm_capsule=args.vm_capsule,
                )
        elif args.command == "probe":
            result = probe(root, args.run_id, args.target, args.deny_cidr)
        elif args.command == "down":
            result = down(root, args.run_id)
        elif args.command == "expire":
            result = expire(root, args.run_id, args.token)
        elif args.command == "status":
            result = status(root)
        else:
            result = sweep(root, admission=Admission(root))
    except (ClusterError, AdmissionError, VM.VmError) as exc:
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
