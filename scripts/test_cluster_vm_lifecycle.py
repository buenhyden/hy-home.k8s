"""Host-only lifecycle for one selected, leased VM environment."""

from __future__ import annotations

import contextlib
import math
import os
import stat
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Callable

from environment_admission import Admission, AdmissionError, _process_start
import test_cluster_environment as ENV
from test_cluster_environment import (
    creator_gone,
    disarm_expiry_timer,
    lease_matches_vm,
    lease_matches_vm_child,
)
import test_cluster_vm as VM


def recover_vm_intents(
    root: Path,
    admission: Any,
    read_state: Callable[..., Any],
    *,
    runner: Callable[..., Any] = subprocess.run,
    only_token: str | None = None,
) -> list[str]:
    """Recover a never-started VM only after exact unit, creator and file absence."""
    import test_cluster_vm as vm

    selected_token: str | None = None

    def absent(lease: dict[str, Any]) -> bool | None:
        if (
            lease["kind"] != "cluster"
            or lease["token"] != selected_token
            or lease["binding_id"] != admission.binding_id
            or lease["workspace_id"] != admission.workspace_id
            or Path(root).resolve() != admission.root
        ):
            return None
        try:
            paths = vm.paths_for(root, lease["run_id"])
            intent = lease["intent"]
            if (
                intent.get("unit") != vm.unit_name(lease["run_id"])
                or intent.get("vm_dir") != str(paths.directory)
                or not creator_gone(
                    intent.get("pid"), intent.get("start_ticks"), vm._process_start
                )
            ):
                return None
            try:
                vm_meta = paths.directory.lstat()
            except FileNotFoundError:
                vm_meta = None
            if vm_meta is not None and (
                not stat.S_ISDIR(vm_meta.st_mode)
                or vm_meta.st_uid != os.geteuid()
                or vm_meta.st_mode & 0o077
                or next(paths.directory.iterdir(), None) is not None
            ):
                return None
            record = (
                ENV.read_state_locked(locked_descriptor)
                if locked_descriptor is not None
                else read_state(root, lease["run_id"])
            )
            if record is not None and not ENV.vm_state_matches(
                record, admission, lease["run_id"], lease["token"]
            ):
                return None
            parent = paths.directory.parent
            try:
                meta = parent.lstat()
            except FileNotFoundError:
                meta = None
            if meta is not None:
                if (
                    not stat.S_ISDIR(meta.st_mode)
                    or meta.st_uid != os.geteuid()
                    or meta.st_mode & 0o077
                ):
                    return None
                entries = (
                    entry for entry in parent.iterdir() if entry != paths.directory
                )
                entry = next(entries, None)
                if next(entries, None) is not None or (entry is None) != (
                    record is None
                ):
                    return None
                if entry is not None:
                    file = entry.lstat()
                    if (
                        entry.name != "state.json"
                        or not stat.S_ISREG(file.st_mode)
                        or file.st_uid != os.geteuid()
                        or file.st_mode & 0o077
                    ):
                        return None
            elif record is not None:
                return None
            state = ENV.vm_unit_state(runner, lease["run_id"])
            if state != {
                "LoadState": "not-found",
                "ActiveState": "inactive",
                "MainPID": "0",
            }:
                return None
            if (
                locked_descriptor is not None
                and ENV.read_state_locked(locked_descriptor) != record
            ):
                return None
            return True
        except (OSError, ValueError, KeyError, TypeError):
            return None

    def child_absent(lease: dict[str, Any]) -> bool | None:
        if lease["kind"] != "worker":
            return None
        run_id = lease["run_id"]
        token = lease["intent"].get("parent_token")
        if (
            not isinstance(token, str)
            or token != selected_token
            or not lease_matches_vm_child(lease, admission, run_id, token)
        ):
            return None
        parent = next(
            (row for row in admission.active_for_run(run_id) if row["token"] == token),
            None,
        )
        if (
            parent is None
            or not lease_matches_vm(
                parent, admission, run_id, token, vm.paths_for(root, run_id).directory
            )
            or lease["intent"].get("vm_source")
            != str(vm.paths_for(root, run_id).source)
        ):
            return None
        return absent(parent)

    def parent_absent(lease: dict[str, Any]) -> bool | None:
        if lease["token"] != selected_token:
            return None
        try:
            vm.paths_for(root, lease["run_id"]).directory.parent.lstat()
        except FileNotFoundError:
            pass
        else:
            return None
        if absent(lease) is not True:
            return None
        if any(
            lease_matches_vm_child(row, admission, lease["run_id"], lease["token"])
            for row in admission.active_for_run(lease["run_id"])
        ):
            return None
        return True

    removed: list[str] = []
    for parent_lease in admission.active_for_binding():
        if parent_lease["kind"] != "cluster" or (
            only_token is not None and parent_lease["token"] != only_token
        ):
            continue
        run_id = parent_lease["run_id"]
        if not isinstance(run_id, str) or not vm.RUN_ID.fullmatch(run_id):
            continue
        paths = vm.paths_for(root, run_id)
        if parent_lease["intent"].get("unit") != vm.unit_name(run_id) or parent_lease[
            "intent"
        ].get("vm_dir") != str(paths.directory):
            continue
        selected_token = parent_lease["token"]
        parent = paths.directory.parent
        lock = (
            ENV.locked_run_dir(parent)
            if parent.is_dir()
            else contextlib.nullcontext(None)
        )
        with lock as locked_descriptor:
            for child in admission.active_for_run(run_id):
                if lease_matches_vm_child(child, admission, run_id, selected_token):
                    try:
                        admission.release(child["token"], child_absent)
                    except AdmissionError:
                        pass
            if absent(parent_lease) is not True:
                continue
            token = selected_token
            try:
                if parent.is_dir():
                    if locked_descriptor is None:
                        raise ValueError("VM intent state appeared during cleanup")
                    record = ENV.read_state_locked(locked_descriptor)
                    if record is not None and not ENV.vm_state_matches(
                        record, admission, run_id, token
                    ):
                        raise ValueError("VM intent state binding differs")
                    if paths.directory.exists():
                        paths.directory.rmdir()
                    if record is not None:
                        ENV.remove_vm_run_parent_locked(
                            locked_descriptor, parent, admission, run_id, token
                        )
                    else:
                        held, current = os.fstat(locked_descriptor), parent.lstat()
                        if (held.st_dev, held.st_ino) != (
                            current.st_dev,
                            current.st_ino,
                        ) or os.listdir(locked_descriptor):
                            raise ValueError(
                                "VM intent directory identity or contents differ"
                            )
                        parent.rmdir()
            except (OSError, ValueError) as exc:
                raise vm.VmError(
                    "VM_CLEANUP: owned VM intent metadata remains"
                ) from exc
            try:
                admission.release(token, parent_absent)
            except AdmissionError:
                continue
            with contextlib.suppress(OSError, ValueError):
                disarm_expiry_timer(runner, run_id, token)
            removed.append(token)
    return removed


def up_host(
    cluster: Any,
    root: Path,
    selection: list[str],
    authority: str,
    *,
    run_id: str | None = None,
    admission: Admission | None = None,
) -> dict[str, Any]:
    if not isinstance(authority, str) or not authority.strip():
        raise VM.VmError("VM_AUTHORITY: name the operator approval for this run")
    clean_authority = authority.strip()
    try:
        if len(clean_authority) > 512 or len(clean_authority.encode("utf-8")) > 512:
            raise VM.VmError("VM_AUTHORITY: approval name exceeds 512 bytes")
    except UnicodeError as exc:
        raise VM.VmError("VM_AUTHORITY: approval name is not UTF-8") from exc
    ordered = cluster.plan(cluster.catalog(root), selection)
    run_id = run_id or uuid.uuid4().hex[:8]
    paths = VM.paths_for(root, run_id)
    if paths.directory.parent.exists():
        raise VM.VmError("VM_OWNERSHIP: run directory already exists")
    deadline = int(time.time()) + VM.VM_SECONDS
    admission = admission or Admission(root)
    creator_start = _process_start(os.getpid())
    if creator_start is None:
        raise VM.VmError("VM_OWNERSHIP: creator identity is unavailable")
    token = admission.reserve(
        run_id,
        "cluster",
        ordered,
        {
            "cpu": VM.VM_CPUS,
            "memory_mib": 4096,
            "disk_mib": 4096,
            "seconds": VM.VM_SECONDS,
            "instances": 1,
        },
        {
            "unit": VM.unit_name(run_id),
            "vm_dir": str(paths.directory),
            "deadline": deadline,
            "pid": os.getpid(),
            "start_ticks": creator_start,
        },
    )
    vm = VM.VmRun(root, run_id, token)
    record = {
        "run_id": run_id,
        "environment_kind": "vm",
        "admission_token": token,
        "workspace_id": admission.workspace_id,
        "binding_id": admission.binding_id,
        "apps": ordered,
        "authority": clean_authority,
        "status": "creating",
        "expires_at": deadline,
        "unit": VM.unit_name(run_id),
    }
    timer_attempted = False
    try:
        paths.directory.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
        cluster._write_state(root, run_id, record)
        timer_attempted = True
        ENV.arm_expiry_timer(
            cluster._run,
            root,
            run_id,
            token,
            max(1, math.ceil(deadline - time.time() + 5)),
        )
        vm.start(
            deadline,
            apps=ordered,
            workspace_id=admission.workspace_id,
            binding_id=admission.binding_id,
        )
        result = vm.wait_ready(deadline)
        with ENV.locked_run_dir(paths.directory.parent) as descriptor:
            current = ENV.read_state_locked(descriptor)
            if (
                not ENV.vm_state_matches(current, admission, run_id, token)
                or current.get("status") != "creating"
                or "cleanup_phase" in current
                or not any(
                    lease_matches_vm(row, admission, run_id, token, paths.directory)
                    for row in admission.active_for_run(run_id)
                )
            ):
                raise VM.VmError(
                    "VM_OWNERSHIP: exact current-workspace VM state is unavailable"
                )
            record = current | {"status": "up", "vm_result": result}
            ENV.write_state_locked(descriptor, record)
        return record
    except BaseException:
        if paths.directory.parent.is_dir():
            with ENV.locked_run_dir(paths.directory.parent) as descriptor:
                current = ENV.read_state_locked(descriptor)
                if (
                    ENV.vm_state_matches(current, admission, run_id, token)
                    and current.get("status") == "creating"
                    and "cleanup_phase" not in current
                    and any(
                        lease_matches_vm(row, admission, run_id, token, paths.directory)
                        for row in admission.active_for_run(run_id)
                    )
                ):
                    try:
                        deleted = vm.stop_owned()
                    except (OSError, ValueError):
                        deleted = False
                    if deleted:
                        if not ENV.vm_state_matches(
                            ENV.read_state_locked(descriptor), admission, run_id, token
                        ):
                            raise VM.VmError(
                                "VM_OWNERSHIP: exact current-workspace VM state is unavailable"
                            )
                        _release_bound(admission, vm)
                        _finish_released(
                            cluster, vm, admission, descriptor, disarm=timer_attempted
                        )
                    else:
                        ENV.write_state_locked(
                            descriptor, current | {"status": "failed"}
                        )
        raise


def _release_bound(admission: Admission, vm: VM.VmRun) -> None:
    run_id, token, directory = vm.run_id, vm.token, vm.paths.directory
    for lease in admission.active_for_run(run_id):
        if ENV.lease_matches_vm_child(lease, admission, run_id, token):
            admission.release(
                lease["token"],
                lambda row: (
                    ENV.lease_matches_vm_child(row, admission, run_id, token)
                    and vm.payload_absent(admission)
                ),
            )
    admission.release(
        token,
        lambda row: (
            ENV.lease_matches_vm(row, admission, run_id, token, directory)
            and vm.payload_absent(admission)
        ),
    )


def _released_metadata(
    vm: VM.VmRun, admission: Admission, record: dict[str, Any]
) -> bool:
    owner_path = vm.paths.directory / "owner.json"
    if owner_path.exists() or owner_path.is_symlink():
        return vm.payload_absent(admission)
    if record.get("cleanup_phase") != "leases-released":
        return False
    if vm.paths.directory.exists() and any(vm.paths.directory.iterdir()):
        return False
    return ENV.vm_unit_stopped(vm.runner, vm.run_id)


def _finish_released(
    cluster: Any,
    vm: VM.VmRun,
    admission: Admission,
    descriptor: int,
    *,
    disarm: bool = True,
) -> None:
    current = ENV.read_state_locked(descriptor)
    if not ENV.vm_state_matches(current, admission, vm.run_id, vm.token):
        raise VM.VmError(
            "VM_OWNERSHIP: exact current-workspace VM state is unavailable"
        )
    ENV.write_state_locked(descriptor, current | {"cleanup_phase": "leases-released"})
    if disarm:
        with contextlib.suppress(OSError, ValueError):
            ENV.disarm_expiry_timer(cluster._run, vm.run_id, vm.token)
    if (vm.paths.directory / "owner.json").exists():
        if not vm.finalize_owned():
            raise VM.VmError("VM_CLEANUP: released owner metadata is unverified")
    elif vm.paths.directory.exists():
        vm.paths.directory.rmdir()
    try:
        ENV.remove_vm_run_parent_locked(
            descriptor, vm.paths.directory.parent, admission, vm.run_id, vm.token
        )
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        raise VM.VmError("VM_CLEANUP: exact VM run parent is unverified") from exc


def down_host(
    cluster: Any,
    root: Path,
    record: dict[str, Any],
    *,
    admission: Admission | None = None,
) -> dict[str, str]:
    run_id, token = record["run_id"], record["admission_token"]
    vm = VM.VmRun(root, run_id, token)
    admission = admission or Admission(root)
    if not ENV.vm_state_matches(record, admission, run_id, token):
        raise VM.VmError(
            "VM_OWNERSHIP: exact current-workspace VM state is unavailable"
        )
    with ENV.locked_run_dir(vm.paths.directory.parent) as descriptor:
        current = ENV.read_state_locked(descriptor)
        if not ENV.vm_state_matches(current, admission, run_id, token):
            raise VM.VmError(
                "VM_OWNERSHIP: exact current-workspace VM state is unavailable"
            )
        leases = admission.active_for_run(run_id)
        lease = next(
            (
                row
                for row in leases
                if ENV.lease_matches_vm(
                    row, admission, run_id, token, vm.paths.directory
                )
            ),
            None,
        )
        if lease is not None:
            if not ENV.vm_external_stop_safe(vm, lease, current):
                raise VM.VmError(
                    "VM_CLEANUP: live VM creator has no verified owned unit to stop"
                )
            if not vm.stop_owned():
                raise VM.VmError("VM_CLEANUP: exact owned VM absence is unverified")
            if not ENV.vm_state_matches(
                ENV.read_state_locked(descriptor), admission, run_id, token
            ):
                raise VM.VmError(
                    "VM_OWNERSHIP: exact current-workspace VM state is unavailable"
                )
            _release_bound(admission, vm)
        elif leases or not _released_metadata(vm, admission, current):
            raise VM.VmError("VM_OWNERSHIP: exact released VM metadata is unverified")
        _finish_released(cluster, vm, admission, descriptor)
    return {"deleted": VM.unit_name(run_id)}
