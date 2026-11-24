"""Owned Docker network and selected-cluster environment checks.

The k3d adapter has no per-node writable-layer disk quota. On the host route
(SPEC-0229 option C) admission accounting plus a polling disk watchdog bound
the run instead: the watchdog kills the node when its measured use passes the
reserved budget or cannot be measured. That is a bound, not a hard cap.
"""

from __future__ import annotations

import contextlib
import fcntl
import http.server
import ipaddress
import json
import os
import platform
import re
import shutil
import socket
import stat
import sys
import threading
import time
import uuid
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from environment_admission import RUN_BUDGET, _process_start

LABEL = "hy-home.k8s/run"
NETWORK_PREFIX = "hyk8s-owned-"
# k3d reads its host IP from the network gateway, and the guest reaches the
# API through that bridge address; --internal blocks forwarding off the bridge
# and the restricted VM NIC blocks the LAN. Only the bounded VM route creates
# this network, one per guest, so a fixed subnet is enough.
OWNED_SUBNET, OWNED_GATEWAY = "172.30.0.0/24", "172.30.0.1"
WORKLOAD_KINDS = frozenset(
    {"Pod", "Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "ReplicaSet"}
)
K3S_IMAGE = "rancher/k3s:v1.35.0-k3s1"
PAUSE_IMAGE = "rancher/mirrored-pause:3.6"
PROBE_IMAGE = "busybox:1.37"
PAUSE_TAR = Path("/home/hyk8s/pause.tar")


@contextlib.contextmanager
def locked_run_dir(directory: Path) -> Any:
    """Serialize cooperating state writers on the private run directory inode."""
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        held, current = os.fstat(descriptor), directory.lstat()
        if (
            not stat.S_ISDIR(held.st_mode)
            or held.st_uid != os.geteuid()
            or held.st_mode & 0o077
            or (held.st_dev, held.st_ino) != (current.st_dev, current.st_ino)
        ):
            raise ValueError("private run directory identity differs")
        yield descriptor
    finally:
        os.close(descriptor)


def read_state_locked(descriptor: int) -> dict[str, Any] | None:
    try:
        state = os.open("state.json", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=descriptor)
    except FileNotFoundError:
        return None
    try:
        file = os.fstat(state)
        if (
            not stat.S_ISREG(file.st_mode)
            or file.st_uid != os.geteuid()
            or file.st_mode & 0o077
            or file.st_size > 4096
        ):
            raise ValueError("private run state ownership differs")
        record = json.loads(os.read(state, 4097))
        if not isinstance(record, dict):
            raise ValueError("private run state is not an object")
        return record
    finally:
        os.close(state)


def write_state_locked(descriptor: int, record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise ValueError("CLUSTER_STATE: run state must be an object")
    payload = json.dumps(record).encode("utf-8")
    if len(payload) > 4096:
        raise ValueError("CLUSTER_STATE: run state exceeds 4096 bytes")
    name = f"state.{uuid.uuid4().hex}"
    state = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
        dir_fd=descriptor,
    )
    try:
        with os.fdopen(state, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, "state.json", src_dir_fd=descriptor, dst_dir_fd=descriptor)
        os.fsync(descriptor)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(name, dir_fd=descriptor)


def write_state(directory: Path, record: dict[str, Any]) -> None:
    with locked_run_dir(directory) as descriptor:
        write_state_locked(descriptor, record)


def free_port() -> int:
    with socket.socket() as probe_socket:
        probe_socket.bind(("127.0.0.1", 0))
        return probe_socket.getsockname()[1]


def expiry_unit(run_id: str, token: str) -> str:
    return f"hyk8s-owned-{run_id}-{token}"


def _user_bus() -> dict[str, str]:
    uid = os.geteuid()
    runtime = Path(f"/run/user/{uid}")
    bus = runtime / "bus"
    try:
        directory, socket = runtime.lstat(), bus.lstat()
    except OSError as exc:
        raise ValueError("CLUSTER_TIMER: user manager bus is unavailable") from exc
    if (
        not stat.S_ISDIR(directory.st_mode)
        or directory.st_uid != uid
        or directory.st_mode & 0o077
        or not stat.S_ISSOCK(socket.st_mode)
        or socket.st_uid != uid
    ):
        raise ValueError("CLUSTER_TIMER: user manager bus ownership is unverified")
    return {
        **os.environ,
        "XDG_RUNTIME_DIR": str(runtime),
        "DBUS_SESSION_BUS_ADDRESS": f"unix:path={bus}",
    }


def creator_gone(
    pid: Any, ticks: Any, process_start: Callable[[int], int | None] = _process_start
) -> bool:
    if type(pid) is not int or pid <= 0 or type(ticks) is not int or ticks <= 0:
        return False
    current = process_start(pid)
    if current is not None:
        return current != ticks
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    except OSError:
        return False
    return False


def create_inflight(admission: Any, token: str) -> bool:
    """A missing receipt is safe only while release holds the cluster gate."""
    return any(
        _receipt_inflight(admission.child_receipt_path(token, phase))
        for phase in (None, "network")
    )


def _receipt_inflight(path: Path) -> bool:
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    try:
        meta = os.fstat(descriptor)
        if (
            not stat.S_ISREG(meta.st_mode)
            or meta.st_uid != os.geteuid()
            or meta.st_mode & 0o077
            or not 0 < meta.st_size <= 128
        ):
            return True
        data = os.read(descriptor, 129).decode("ascii").strip().split()
        if len(data) != 4:
            return True
        pid, ticks, pgid, uid = map(int, data)
        if uid != os.geteuid() or pgid != pid or pid <= 0 or ticks <= 0:
            return True
        if _process_start(pid) == ticks:
            return True
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return False
        except OSError:
            return True
        return True
    except (OSError, ValueError, UnicodeError):
        return True
    finally:
        os.close(descriptor)


def await_create_quiescent(admission: Any, token: str, seconds: float = 0.5) -> bool:
    """Wait briefly for the exact create receipt; unknown identity stays held."""
    deadline = time.monotonic() + seconds
    while create_inflight(admission, token):
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)
    return True


def lease_matches_cluster(
    lease: dict[str, Any], admission: Any, run_id: str, token: str, name: str
) -> bool:
    return (
        lease["token"] == token
        and lease["run_id"] == run_id
        and lease["kind"] == "cluster"
        and lease["binding_id"] == admission.binding_id
        and lease["workspace_id"] == admission.workspace_id
        and lease["intent"].get("cluster") == name
    )


def cluster_state_matches(
    root: Path,
    admission: Any,
    lease: dict[str, Any],
    run_id: str,
    token: str,
    name: str,
    read_state: Callable[..., Any],
) -> bool:
    if Path(root).resolve() != admission.root or not lease_matches_cluster(
        lease, admission, run_id, token, name
    ):
        return False
    record = read_state(root, run_id)
    if record is None:
        try:
            (root / ".workspace-test" / run_id / "state.json").lstat()
        except FileNotFoundError:
            return True
        return False
    return (
        record.get("run_id") == run_id
        and record.get("cluster") == name
        and record.get("admission_token") == token
        and record.get("environment_kind") is None
    )


def owned_cluster(
    root: Path,
    name: str,
    labels: dict[str, str],
    read_state: Callable[[Path, str], dict[str, Any] | None],
    prefix: str,
) -> bool:
    if not name.startswith(prefix):
        return False
    run_id = name[len(prefix) :]
    return bool(
        re.fullmatch(r"[a-z0-9]{8}", run_id)
        and read_state(root, run_id)
        and labels.get(name) == run_id
    )


def lease_matches_vm(
    lease: dict[str, Any], admission: Any, run_id: str, token: str, directory: Path
) -> bool:
    from test_cluster_vm import unit_name

    return (
        lease["token"] == token
        and lease["run_id"] == run_id
        and lease["kind"] == "cluster"
        and lease["binding_id"] == admission.binding_id
        and lease["workspace_id"] == admission.workspace_id
        and lease["intent"].get("unit") == unit_name(run_id)
        and lease["intent"].get("vm_dir") == str(directory)
    )


def lease_matches_vm_child(
    lease: dict[str, Any], admission: Any, run_id: str, parent_token: str
) -> bool:
    return (
        lease["run_id"] == run_id
        and lease["kind"] == "worker"
        and lease["binding_id"] == admission.binding_id
        and lease["workspace_id"] == admission.workspace_id
        and lease["intent"].get("parent_token") == parent_token
    )


def vm_start_inflight(root: Path, record: dict[str, Any], admission: Any) -> bool:
    """Keep an unfinished VM start until its exact creator and unit are gone."""
    if record.get("status") not in {"creating", "failed"}:
        return False
    if admission is None:
        return True
    try:
        import test_cluster_vm as vm

        run_id, token = record["run_id"], record["admission_token"]
        paths = vm.paths_for(root, run_id)
        leases = admission.active_for_run(run_id)
        lease = next((row for row in leases if row["token"] == token), None)
        if lease is None:
            return not (
                not leases
                and record.get("workspace_id") == admission.workspace_id
                and record.get("binding_id") == admission.binding_id
            )
        intent = lease["intent"]
        if (
            lease["kind"] != "cluster"
            or lease["binding_id"] != admission.binding_id
            or lease["workspace_id"] != admission.workspace_id
            or intent.get("unit") != vm.unit_name(run_id)
            or intent.get("vm_dir") != str(paths.directory)
        ):
            return True
        if not creator_gone(
            intent.get("pid"), intent.get("start_ticks"), vm._process_start
        ):
            return True
        owned = vm.VmRun(root, run_id, token)
        return not owned.absent_owned()
    except (OSError, ValueError, KeyError, StopIteration, TypeError):
        return True


def vm_external_stop_safe(
    owned: Any, lease: dict[str, Any], record: dict[str, Any]
) -> bool:
    """A live creator may be interrupted only through its exact running unit."""
    if record.get("status") == "up" or creator_gone(
        lease["intent"].get("pid"), lease["intent"].get("start_ticks")
    ):
        return True
    try:
        owner = owned._owner()
        state = vm_unit_state(owned.runner, owned.run_id) or {}
        return (
            state.get("LoadState") == "loaded"
            and state.get("ActiveState") == "active"
            and state.get("MainPID") == str(owner.get("main_pid"))
            and owned._same_process(owner.get("main_pid"), owner.get("main_start"))
        )
    except (OSError, ValueError, KeyError):
        return False


def vm_unit_state(runner: Callable[..., Any], run_id: str) -> dict[str, str] | None:
    """Read one successful exact inventory of the owned user unit."""
    from test_cluster_vm import _invoke, unit_name

    output = _invoke(
        runner,
        [
            "systemctl",
            "--user",
            "show",
            "--property=LoadState",
            "--property=ActiveState",
            "--property=MainPID",
            f"{unit_name(run_id)}.service",
        ],
        env=_user_bus(),
    )
    pairs = [line.split("=", 1) for line in output.splitlines()]
    if len(pairs) != 3 or any(len(pair) != 2 for pair in pairs):
        return None
    state = dict(pairs)
    return state if set(state) == {"LoadState", "ActiveState", "MainPID"} else None


def vm_unit_stopped(runner: Callable[..., Any], run_id: str) -> bool:
    state = vm_unit_state(runner, run_id) or {}
    return (
        state.get("LoadState") in {"loaded", "not-found"}
        and state.get("ActiveState") in {"inactive", "failed"}
        and state.get("MainPID") == "0"
    )


def vm_is_active(root: Path, record: dict[str, Any]) -> bool:
    import test_cluster_vm as vm

    try:
        owned = vm.VmRun(root, record["run_id"], record["admission_token"])
        owner = owned._owner()
        state = vm_unit_state(owned.runner, owned.run_id) or {}
        return (
            state.get("LoadState") == "loaded"
            and state.get("ActiveState") == "active"
            and state.get("MainPID") == str(owner.get("main_pid"))
            and owned._same_process(owner.get("main_pid"), owner.get("main_start"))
        )
    except (KeyError, OSError, ValueError):
        return False


def vm_status_host(
    root: Path, read_state: Callable[[Path, str], dict[str, Any] | None]
) -> list[dict[str, Any]]:
    from test_cluster_vm import RUN_ID

    runtime = root / ".workspace-test"
    records = (
        (
            read_state(root, path.name)
            for path in runtime.iterdir()
            if path.is_dir() and RUN_ID.fullmatch(path.name)
        )
        if runtime.is_dir()
        else ()
    )
    return [
        {
            "name": record["unit"],
            "owned": vm_is_active(root, record),
            "environment_kind": "vm",
            "status": record["status"],
        }
        for record in records
        if record and record.get("environment_kind") == "vm"
    ]


def vm_expiry_due(
    root: Path, run_id: str, token: str, admission: Any, record: dict[str, Any]
) -> bool:
    from test_cluster_vm import paths_for

    directory = paths_for(root, run_id).directory
    leases = admission.active_for_run(run_id)
    return (
        record.get("admission_token") == token
        and (
            any(
                lease_matches_vm(row, admission, run_id, token, directory)
                for row in leases
            )
            or not leases
            and record.get("workspace_id") == admission.workspace_id
            and record.get("binding_id") == admission.binding_id
        )
        and time.time() >= record.get("expires_at", float("inf"))
        and vm_start_inflight(root, record, admission) is False
    )


def vm_state_matches(record: Any, admission: Any, run_id: str, token: str) -> bool:
    from test_cluster_vm import unit_name

    return (
        isinstance(record, dict)
        and record.get("run_id") == run_id
        and record.get("environment_kind") == "vm"
        and record.get("admission_token") == token
        and record.get("unit") == unit_name(run_id)
        and record.get("workspace_id") == admission.workspace_id
        and record.get("binding_id") == admission.binding_id
    )


def remove_vm_run_parent_locked(
    descriptor: int, parent: Path, admission: Any, run_id: str, token: str
) -> None:
    """Remove exact current state while holding its private directory lock."""
    record = read_state_locked(descriptor)
    if not vm_state_matches(record, admission, run_id, token) or os.listdir(
        descriptor
    ) != ["state.json"]:
        raise ValueError("run state binding or artifacts differ")
    held, current = os.fstat(descriptor), parent.lstat()
    if (held.st_dev, held.st_ino) != (current.st_dev, current.st_ino):
        raise ValueError("run directory identity differs")
    os.unlink("state.json", dir_fd=descriptor)
    os.fsync(descriptor)
    parent.rmdir()


def remove_vm_run_parent(parent: Path, admission: Any, run_id: str, token: str) -> None:
    try:
        with locked_run_dir(parent) as descriptor:
            remove_vm_run_parent_locked(descriptor, parent, admission, run_id, token)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        from test_cluster_vm import VmError

        raise VmError("VM_CLEANUP: exact VM run parent is unverified") from exc


def remove_vm_files(
    directory: Path, owner: dict[str, Any], *, finalize: bool = False
) -> bool:
    """Unlink recorded payload first; remove durable owner only after lease release."""
    expected = owner.get("files")
    if not isinstance(expected, dict):
        return False
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        meta = os.fstat(descriptor)
        if meta.st_uid != os.geteuid() or meta.st_mode & 0o077:
            return False
        names = set(os.listdir(descriptor))
        if "owner.json" not in names:
            return False
        names.remove("owner.json")
        if finalize and names:
            return False
        for name in sorted(names):
            file = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
            if (
                not stat.S_ISREG(file.st_mode)
                or file.st_uid != os.geteuid()
                or expected.get(name) != [file.st_dev, file.st_ino]
            ):
                return False
        for name in sorted(names):
            file = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
            if expected[name] != [file.st_dev, file.st_ino]:
                return False
            os.unlink(name, dir_fd=descriptor)
        os.fsync(descriptor)
        if set(os.listdir(descriptor)) != {"owner.json"}:
            return False
        if finalize:
            os.unlink("owner.json", dir_fd=descriptor)
            os.fsync(descriptor)
    finally:
        os.close(descriptor)
    if finalize:
        directory.rmdir()
    return True


def arm_expiry_timer(
    run: Callable[..., str], root: Path, run_id: str, token: str, seconds: int
) -> None:
    """Arm an account user timer before starting any owned Docker resource."""
    linger = run(
        ["loginctl", "show-user", str(os.geteuid()), "--property=Linger", "--value"]
    ).strip()
    if linger != "yes":
        raise ValueError("CLUSTER_TIMER: persistent user manager is unavailable")
    unit = expiry_unit(run_id, token)
    env = _user_bus()
    run(
        [
            "systemd-run",
            "--user",
            f"--unit={unit}",
            f"--on-active={seconds}s",
            "--on-unit-active=60s",
            "--collect",
            sys.executable,
            str(Path(__file__).with_name("test_cluster.py")),
            "--root",
            str(root),
            "expire",
            run_id,
            token,
        ],
        env=env,
    )
    if (
        run(["systemctl", "--user", "is-active", f"{unit}.timer"], env=env).strip()
        != "active"
    ):
        raise ValueError("CLUSTER_TIMER: owned expiry timer did not become active")


def disarm_expiry_timer(run: Callable[..., str], run_id: str, token: str) -> None:
    unit = expiry_unit(run_id, token)
    run(["systemctl", "--user", "stop", f"{unit}.timer"], env=_user_bus(), check=False)


def network_name(run_id: str) -> str:
    return NETWORK_PREFIX + run_id


def labelled_runs(run: Callable[..., str]) -> dict[str, str]:
    """Cluster name to run ID from the node container label."""
    output = run(
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
    labels = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 2:
            labels[parts[0]] = parts[1]
    return labels


ROUTE_SCRIPT = """#!/bin/sh
# k3s chooses its node IP from the default route, which the owned isolated
# network does not provide. A device route without a gateway names eth0 for
# that choice and reaches nothing the isolated bridge did not already reach.
ip route show default | grep -q . || ip route add default dev eth0
"""


def write_route_script(state: Path) -> Path:
    """Write the run-owned k3d entrypoint hook that gives k3s a default route."""
    path = state / "k3d-entrypoint-route.sh"
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o755
    )
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(ROUTE_SCRIPT)
    return path


def create_command(
    name: str,
    run_id: str,
    port: int,
    network: str,
    server_memory: str = "4g",
    pause_tar: str | None = None,
    route_script: str | None = None,
) -> list[str]:
    command = [
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
        "--network",
        network,
        "--servers-memory",
        server_memory,
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
    ]
    if pause_tar is not None:
        # The guest's fixed archive, or the one this run saved for itself.
        if pause_tar != str(PAUSE_TAR) and not (
            Path(pause_tar).is_absolute()
            and pause_tar.endswith(f"/.workspace-test/{run_id}/pause.tar")
        ):
            raise ValueError("CLUSTER_INPUT: pause archive path is unverified")
        command += [
            "--volume",
            f"{pause_tar}:/var/lib/rancher/k3s/agent/images/pause.tar:ro@server:0",
        ]
    if route_script is not None:
        command += [
            "--volume",
            f"{route_script}:/bin/k3d-entrypoint-route.sh:ro@server:0",
        ]
    return command + ["--wait", "--timeout", "180s"]


def tool_environment(state: Path, base: dict[str, str] | None = None) -> dict[str, str]:
    environment = {
        key: value for key, value in (base or os.environ).items() if key != "KUBECONFIG"
    }
    return environment | {"KUBECONFIG": str(state / "kubeconfig")}


ISOLATED_OPTION = "com.docker.network.bridge.gateway_mode_ipv4"


def create_network_command(
    name: str, run_id: str, *, isolated: bool = False
) -> list[str]:
    # On the host route the bridge must hold no host address: an owned test
    # showed a plain --internal network still reaches host services through
    # its gateway address (SPEC-0229 EVD-085).
    option = ["-o", f"{ISOLATED_OPTION}=isolated"] if isolated else []
    return [
        "docker",
        "network",
        "create",
        "--driver",
        "bridge",
        *option,
        "--internal",
        "--subnet",
        OWNED_SUBNET,
        "--gateway",
        OWNED_GATEWAY,
        "--label",
        f"{LABEL}={run_id}",
        name,
    ]


def network_names(run: Callable[..., str], run_id: str) -> set[str]:
    output = run(
        [
            "docker",
            "network",
            "ls",
            "--filter",
            f"label={LABEL}={run_id}",
            "--format",
            "{{.Name}}",
        ]
    )
    return set((output or "").splitlines())


def verify_network(
    run: Callable[..., str], name: str, run_id: str, *, isolated: bool = False
) -> None:
    output = run(["docker", "network", "inspect", name, "--format", "{{json .}}"])
    ipam = None
    try:
        data = json.loads(output)
        ipam = data.get("IPAM", {}).get("Config")
        if (
            data.get("Name") != name
            or data.get("Driver") != "bridge"
            or data.get("Internal") is not True
            or data.get("EnableIPv6") is not False
            or data.get("Labels", {}).get(LABEL) != run_id
            or not isinstance(ipam, list)
            or len(ipam) != 1
            or ipam[0].get("Subnet") != OWNED_SUBNET
            or ipam[0].get("Gateway") != OWNED_GATEWAY
            or (
                isolated
                and (data.get("Options") or {}).get(ISOLATED_OPTION) != "isolated"
            )
        ):
            raise ValueError("network isolation or ownership differs")
    except (TypeError, ValueError, AttributeError) as exc:
        observed = json.dumps(ipam, sort_keys=True)[:120]
        raise ValueError(
            f"CLUSTER_NETWORK: isolated owned network is unverified (ipam={observed})"
        ) from exc


def node_address(run: Callable[..., str], cluster: str, network: str) -> str:
    """Return the server node address on the owned network, inside its subnet."""
    output = run(
        [
            "docker",
            "inspect",
            f"k3d-{cluster}-server-0",
            "--format",
            "{{json .NetworkSettings.Networks}}",
        ]
    )
    try:
        address = ipaddress.ip_address(json.loads(output)[network]["IPAddress"])
        subnet = ipaddress.ip_network(OWNED_SUBNET)
        if address not in subnet or str(address) == OWNED_GATEWAY:
            raise ValueError("node address is outside the owned network")
    except (TypeError, ValueError, KeyError) as exc:
        raise ValueError(
            "CLUSTER_NETWORK: server node address on the owned network is unverified"
        ) from exc
    return str(address)


def verify_node_network(run: Callable[..., str], cluster: str, network: str) -> None:
    output = run(
        [
            "docker",
            "inspect",
            f"k3d-{cluster}-server-0",
            "--format",
            "{{json .NetworkSettings.Networks}}",
        ]
    )
    try:
        attached = json.loads(output)
        if not isinstance(attached, dict) or set(attached) != {network}:
            raise ValueError("unexpected node network attachment")
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "CLUSTER_NETWORK: node is not confined to its owned network"
        ) from exc


def enforce_node_cpu(run: Callable[..., str], cluster: str) -> None:
    node = f"k3d-{cluster}-server-0"
    run(["docker", "update", f"--cpus={RUN_BUDGET['cpu']}", node])
    output = run(
        ["docker", "inspect", node, "--format", "{{json .HostConfig.NanoCpus}}"]
    )
    try:
        if json.loads(output) != RUN_BUDGET["cpu"] * 1_000_000_000:
            raise ValueError("node CPU cap differs")
    except (TypeError, ValueError) as exc:
        raise ValueError("CLUSTER_CPU_LIMIT: node CPU cap is unverified") from exc


def has_product_workload(documents: Sequence[dict[str, Any]]) -> bool:
    return any(doc.get("kind") in WORKLOAD_KINDS for doc in documents)


def verified_pause_tar() -> str:
    try:
        meta = PAUSE_TAR.lstat()
        if (
            not stat.S_ISREG(meta.st_mode)
            or meta.st_uid != 0
            or meta.st_mode & 0o022
            or not 0 < meta.st_size <= 64 * 1024 * 1024
        ):
            raise ValueError("pause archive identity or size differs")
    except (OSError, ValueError) as exc:
        raise ValueError(
            "VM_INPUT: bounded guest pause archive is unavailable"
        ) from exc
    return str(PAUSE_TAR)


def verified_guest_profile(capsule: Path) -> dict[str, Any]:
    from test_cluster_vm import VM_SECONDS, VmError, guest_disk_proof

    proof = guest_disk_proof(capsule)
    remaining = proof.get("deadline", 0) - time.time()
    if type(proof.get("deadline")) is not int or not 0 < remaining <= VM_SECONDS:
        raise VmError("VM_PROOF: parent VM deadline is invalid or expired")
    port, nonce = proof.get("dummy_port"), proof.get("dummy_nonce")
    if (
        type(port) is not int
        or not 49152 <= port <= 65535
        or not isinstance(nonce, str)
        or not re.fullmatch(r"[0-9a-f]{32}", nonce)
    ):
        raise VmError("VM_PROOF: owned boundary endpoint is unverified")
    return {
        "cpu": RUN_BUDGET["cpu"],
        "memory_mib": 1536,
        "disk_mib": 1024,
        "seconds": max(1, int(remaining)),
        "instances": 1,
        "server_memory": "1536m",
        "memory_margin_mib": 256,
        "disk_margin_mib": 128,
        "pause_tar": verified_pause_tar(),
        "dummy_port": port,
        "dummy_nonce": nonce,
    }


def host_pause_tar(run: Callable[..., str], state: Path) -> str:
    """Save the pause and probe images into the run's own archive.

    The isolated node cannot pull, and k3s imports every archive in its
    images directory at start. `k3d image import` left the probe image absent
    in an actual host run (SPEC-0229 EVD-086), so the archive carries it too.
    """
    path = state / "pause.tar"
    for image in (PAUSE_IMAGE, PROBE_IMAGE):
        run(["docker", "pull", image])
    run(["docker", "save", "-o", str(path), PAUSE_IMAGE, PROBE_IMAGE])
    try:
        meta = path.lstat()
        if not stat.S_ISREG(meta.st_mode) or not 0 < meta.st_size <= 64 * 1024**2:
            raise ValueError("pause archive identity or size differs")
    except (OSError, ValueError) as exc:
        raise ValueError("CLUSTER_INPUT: run pause archive is unavailable") from exc
    return str(path)


def start_host_dummy(port: int, nonce: str) -> http.server.ThreadingHTTPServer:
    """Serve the probe's denied endpoint on the host.

    It binds every host address on purpose: a pod that reaches the host by any
    address gets the nonce, and the probe then fails.
    """
    body = nonce.encode()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - http.server API
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args: Any) -> None:
            return

    server = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# The k3s image keeps its data in these anonymous volumes, outside SizeRw.
NODE_VOLUMES = ("/var/lib/rancher/k3s", "/var/lib/kubelet", "/var/lib/cni", "/var/log")


def node_disk_mib(run: Callable[..., str], node: str) -> int:
    """Writable layer plus the node's data volumes, in MiB (rounded up)."""
    layer = int(
        run(
            [
                "docker",
                "container",
                "inspect",
                "--size",
                node,
                "--format",
                "{{.SizeRw}}",
            ]
        ).strip()
    )
    used = run(["docker", "exec", node, "du", "-skx", *NODE_VOLUMES])
    kib = sum(int(line.split()[0]) for line in used.splitlines() if line.strip())
    return -(-(layer + kib * 1024) // (1024 * 1024))


class DiskWatchdog:
    """Kill the node when its disk use passes the reserved budget.

    ponytail: polling bound, not a quota; writes between two polls can
    overshoot by one interval. A kernel quota needs a root-owned filesystem.
    """

    def __init__(
        self,
        run: Callable[..., str],
        node: str,
        limit_mib: int,
        interval: float = 15.0,
    ) -> None:
        self.run, self.node, self.limit, self.interval = run, node, limit_mib, interval
        self.exceeded: str | None = None
        self._failures = 0
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def check(self) -> bool:
        try:
            used = node_disk_mib(self.run, self.node)
        except Exception:  # noqa: BLE001 - three misses in a row fail closed
            self._failures += 1
            if self._failures < 3:
                return True
            reason = "node disk use is unmeasurable"
        else:
            self._failures = 0
            if used <= self.limit:
                return True
            reason = f"node uses {used} MiB, over its {self.limit} MiB budget"
        self.exceeded = reason
        with contextlib.suppress(Exception):
            self.run(["docker", "kill", self.node])
        return False

    def start(self) -> None:
        def loop() -> None:
            while not self._stop.wait(self.interval):
                if not self.check():
                    return

        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=30)


def namespace_limits(namespace: str) -> list[dict[str, Any]]:
    """Small test-namespace defaults; server memory remains the host boundary."""
    return [
        {
            "apiVersion": "v1",
            "kind": "ResourceQuota",
            "metadata": {"name": "hyk8s-test-budget", "namespace": namespace},
            "spec": {
                "hard": {
                    "requests.cpu": "2",
                    "requests.memory": "2Gi",
                    "limits.cpu": "2",
                    "limits.memory": "2Gi",
                    "pods": "8",
                }
            },
        },
        {
            "apiVersion": "v1",
            "kind": "LimitRange",
            "metadata": {"name": "hyk8s-test-defaults", "namespace": namespace},
            "spec": {
                "limits": [
                    {
                        "type": "Container",
                        "default": {"cpu": "500m", "memory": "512Mi"},
                        "defaultRequest": {"cpu": "100m", "memory": "128Mi"},
                        "max": {"cpu": "1", "memory": "1Gi"},
                    }
                ]
            },
        },
    ]


def apply_selected_guest(
    run: Callable[..., str],
    root: Path,
    apps: dict[str, Any],
    ordered: list[str],
    rendered: dict[str, list[dict[str, Any]]],
    env: dict[str, str],
    run_id: str,
    profile: dict[str, Any],
) -> dict[str, Any]:
    """Apply policy, prove the owned boundary, then start selected workloads."""
    products = [
        item
        for app in ordered
        for item in rendered[app]
        if item.get("kind") in WORKLOAD_KINDS
    ]
    ready_kinds = {"Pod", "Deployment", "StatefulSet", "DaemonSet", "Job"}
    if any(item.get("kind") not in ready_kinds for item in products):
        raise ValueError("VM_READY: selected workload readiness is unsupported")
    created: set[str] = set()
    infrastructure = [
        item
        for app in ordered
        for item in rendered[app]
        if item.get("kind") not in WORKLOAD_KINDS
    ]

    def apply(item: dict[str, Any]) -> None:
        content = json.dumps(item)
        run(
            ["kubectl", "apply", "--dry-run=server", "-f", "-"],
            env=env,
            input_text=content,
        )
        run(["kubectl", "apply", "-f", "-"], env=env, input_text=content)

    for item in (entry for entry in infrastructure if entry.get("kind") == "Namespace"):
        apply(item)
        namespace = item.get("metadata", {}).get("name")
        if isinstance(namespace, str):
            created.add(namespace)
            for limit in namespace_limits(namespace):
                apply(limit)
    for item in (entry for entry in infrastructure if entry.get("kind") != "Namespace"):
        apply(item)
    uses = {name for app in ordered for name in apps[app].get("uses", [])}
    candidates = sorted(uses | created)
    namespace = (
        "apps" if "apps" in candidates else (candidates[0] if candidates else None)
    )
    if namespace is None:
        raise ValueError("CLUSTER_NETWORK: selected namespace is unavailable")

    def probe_run(command: list[str], input_text: str | None = None) -> str:
        return run(command, env=env, input_text=input_text)

    probe = selected_namespace_probe(
        probe_run,
        namespace,
        profile["dummy_port"],
        profile["dummy_nonce"],
        run_id,
        profile.get("dummy_host", "10.0.2.2"),
    )
    ready = []
    for item in products:
        kind, metadata = item["kind"], item.get("metadata", {})
        name, target_ns = metadata.get("name"), metadata.get("namespace")
        if not isinstance(name, str) or not isinstance(target_ns, str):
            raise ValueError("VM_READY: selected workload identity is unavailable")
        apply(item)
        target = f"{kind.lower()}/{name}"
        if kind in {"Pod", "Job"}:
            condition = "Ready" if kind == "Pod" else "complete"
            run(
                [
                    "kubectl",
                    "wait",
                    target,
                    "-n",
                    target_ns,
                    f"--for=condition={condition}",
                    "--timeout=120s",
                ],
                env=env,
            )
        else:
            run(
                [
                    "kubectl",
                    "rollout",
                    "status",
                    target,
                    "-n",
                    target_ns,
                    "--timeout=120s",
                ],
                env=env,
            )
        ready.append(target)
    return {"network_probe": probe, "workload_ready": ready}


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


def alive(pid: Any) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def doctor(
    root: Path,
    run: Callable[..., str],
    error: type[Exception],
    image: str,
    runtime: str,
) -> dict[str, Any]:
    def version(command: list[str]) -> str | None:
        with contextlib.suppress(error):
            return run(command).strip().splitlines()[0][:120]
        return None

    default = Path.home() / ".kube" / "config"
    context = None
    if default.is_file():
        with contextlib.suppress(error):
            context = run(
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
        "k3s_image": image,
        "runtime": str(root / runtime),
    }


def probe_boundary(
    local_get: Callable[[], str],
    guest_get: Callable[[], str],
    nonce: str,
    *,
    restricted: bool,
) -> dict[str, bool]:
    if local_get() != nonce:
        raise ValueError("CLUSTER_NETWORK: owned host dummy is not live")
    try:
        guest = guest_get()
    except (OSError, ValueError) as exc:
        raise ValueError("CLUSTER_NETWORK: guest transport is unverified") from exc
    if local_get() != nonce:
        raise ValueError("CLUSTER_NETWORK: owned host dummy stopped during guest probe")
    if (restricted and guest != "blocked") or (not restricted and guest != nonce):
        raise ValueError(
            "CLUSTER_NETWORK: VM network boundary differs from expected phase"
        )
    return {"local_live": True, "guest_restricted": restricted}


def selected_namespace_probe(
    run: Callable[..., str],
    namespace: str,
    dummy_port: int,
    nonce: str,
    run_id: str,
    dummy_host: str = "10.0.2.2",
) -> dict[str, Any]:
    if (
        not re.fullmatch(r"[a-z0-9-]{1,63}", namespace)
        or not re.fullmatch(r"[a-z0-9]{8}", run_id)
        or not re.fullmatch(r"[A-Za-z0-9-]{1,64}", nonce)
        or type(dummy_port) is not int
        or not 1024 <= dummy_port <= 65535
        or dummy_host not in ("10.0.2.2", OWNED_GATEWAY)
    ):
        raise ValueError("CLUSTER_NETWORK: invalid owned probe input")
    server, client = f"hyk8s-probe-s-{run_id}", f"hyk8s-probe-c-{run_id}"
    egress, ingress = f"hyk8s-probe-e-{run_id}", f"hyk8s-probe-i-{run_id}"
    labels = {"hy-home.k8s/run": run_id}
    security = {
        "runAsNonRoot": True,
        "runAsUser": 65532,
        "readOnlyRootFilesystem": True,
        "allowPrivilegeEscalation": False,
        "capabilities": {"drop": ["ALL"]},
    }

    def pod(name: str, role: str, command: list[str]) -> dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "namespace": namespace,
                "labels": labels | {"hyk8s-probe-role": role},
            },
            "spec": {
                "automountServiceAccountToken": False,
                "restartPolicy": "Never",
                "containers": [
                    {
                        "name": role,
                        "image": "busybox:1.37",
                        "imagePullPolicy": "Never",
                        "command": command,
                        "securityContext": security,
                        "resources": {
                            "requests": {"cpu": "10m", "memory": "16Mi"},
                            "limits": {"cpu": "100m", "memory": "64Mi"},
                        },
                    }
                ],
            },
        }

    policy = [
        {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": egress, "namespace": namespace, "labels": labels},
            "spec": {
                "podSelector": {
                    "matchLabels": {"hyk8s-probe-role": "client", **labels}
                },
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "to": [
                            {
                                "podSelector": {
                                    "matchLabels": {
                                        "hyk8s-probe-role": "server",
                                        **labels,
                                    }
                                }
                            }
                        ],
                        "ports": [{"protocol": "TCP", "port": 8080}],
                    },
                    {
                        "to": [{"ipBlock": {"cidr": f"{dummy_host}/32"}}],
                        "ports": [{"protocol": "TCP", "port": dummy_port}],
                    },
                ],
            },
        },
        {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": ingress, "namespace": namespace, "labels": labels},
            "spec": {
                "podSelector": {
                    "matchLabels": {"hyk8s-probe-role": "server", **labels}
                },
                "policyTypes": ["Ingress"],
                "ingress": [
                    {
                        "from": [
                            {
                                "podSelector": {
                                    "matchLabels": {
                                        "hyk8s-probe-role": "client",
                                        **labels,
                                    }
                                }
                            }
                        ],
                        "ports": [{"protocol": "TCP", "port": 8080}],
                    }
                ],
            },
        },
    ]
    manifests = {
        "apiVersion": "v1",
        "kind": "List",
        "items": [
            *policy,
            pod(
                server,
                "server",
                [
                    "sh",
                    "-c",
                    "while true; do printf 'HTTP/1.1 200 OK\\r\\n"
                    f"Content-Length: {len(nonce)}\\r\\nConnection: close\\r\\n\\r\\n%s' '{nonce}'"
                    " | nc -l -p 8080; done",
                ],
            ),
            pod(client, "client", ["sh", "-c", "sleep 180"]),
        ],
    }
    failure: Exception | None = None
    try:
        run(["k3d", "image", "import", "busybox:1.37", "-c", f"hyk8s-test-{run_id}"])
        run(["kubectl", "apply", "-f", "-"], input_text=json.dumps(manifests))
        for name in (server, client):
            try:
                run(
                    [
                        "kubectl",
                        "wait",
                        "pod",
                        name,
                        "-n",
                        namespace,
                        "--for=condition=Ready",
                        "--timeout=60s",
                    ]
                )
            except Exception as exc:
                # A timeout alone hides why: add the phase, the unmet
                # condition and the container's waiting reason, bounded.
                try:
                    state = run(
                        [
                            "kubectl",
                            "get",
                            "pod",
                            name,
                            "-n",
                            namespace,
                            "-o",
                            "jsonpath={.status.phase}"
                            ' {range .status.conditions[?(@.status=="False")]}'
                            "{.reason}:{.message} {end}"
                            "{range .status.containerStatuses[*]}"
                            "{.state.waiting.reason}:{.state.waiting.message}{end}",
                        ]
                    )
                except Exception:  # noqa: BLE001 - the original failure stays
                    state = "state unavailable"
                raise RuntimeError(f"{str(exc)[:40]}; {name}: {state[:200]}") from exc
        ip = run(
            [
                "kubectl",
                "get",
                "pod",
                server,
                "-n",
                namespace,
                "-o",
                "jsonpath={.status.podIP}",
            ]
        ).strip()
        if not re.fullmatch(r"[0-9.]{7,15}", ip):
            raise ValueError("server Pod IP is unverified")
        internal = run(
            [
                "kubectl",
                "exec",
                client,
                "-n",
                namespace,
                "--",
                "wget",
                "-T",
                "3",
                "-qO-",
                f"http://{ip}:8080",
            ]
        ).strip()
        external = run(
            [
                "kubectl",
                "exec",
                client,
                "-n",
                namespace,
                "--",
                "sh",
                "-c",
                f"body=$(wget -T 3 -qO- http://{dummy_host}:{dummy_port}/ 2>/dev/null); "
                'rc=$?; printf \'rc=%s body=%s\' "$rc" "$body"',
            ]
        ).strip()
        if internal != nonce or not re.fullmatch(
            r"rc=[1-9][0-9]*(?: body=)?", external
        ):
            raise ValueError(f"internal={internal == nonce} external={external[:40]!r}")
        return {
            "namespace": namespace,
            "internal_allowed": True,
            "owned_host_denied": True,
        }
    except Exception as exc:
        failure = exc
        # Keep the bounded cause so a failed run shows which step failed.
        raise ValueError(
            "CLUSTER_NETWORK: selected namespace allowed/denied probe failed: "
            f"{type(exc).__name__}: {str(exc)[:280]}"
        ) from exc
    finally:
        cleanup_error = None
        for command in (
            [
                "kubectl",
                "delete",
                "pod",
                server,
                client,
                "-n",
                namespace,
                "--ignore-not-found=true",
                "--wait=true",
            ],
            [
                "kubectl",
                "delete",
                "networkpolicy",
                egress,
                ingress,
                "-n",
                namespace,
                "--ignore-not-found=true",
                "--wait=true",
            ],
        ):
            try:
                run(command)
            except Exception as exc:
                cleanup_error = exc
        if cleanup_error is not None and failure is None:
            raise ValueError(
                "CLUSTER_NETWORK: owned probe cleanup is unverified"
            ) from cleanup_error
