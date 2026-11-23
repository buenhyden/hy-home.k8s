#!/usr/bin/env python3
"""One owned, bounded local VM for the P07 selected product environment."""

from __future__ import annotations

import hashlib
import argparse
import json
import math
import os
import re
import secrets
import shutil
import socket
import stat
import struct
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from environment_admission import Admission, _private_dir, _process_start
from test_cluster_environment import _user_bus
import test_cluster_environment as CLUSTER_ENV
import test_cluster_vm_transport as TRANSPORT

MIB = 1024 * 1024
RAW_BYTES = 4080 * MIB
SOURCE_LIMIT = 512 * MIB
GUEST_MEMORY_MIB = 3072
SOURCE_URL = "https://cloud-images.ubuntu.com/minimal/releases/noble/release-20261105/ubuntu-24.04-minimal-cloudimg-amd64.img"
SOURCE_SHA256 = "406630c08b5e545fcc7209854b129d47e3af822db128c9f19336593b5a2d3fe0"
OVMF_CODE = Path("/usr/share/OVMF/OVMF_CODE_4M.fd")
OVMF_VARS = Path("/usr/share/OVMF/OVMF_VARS_4M.fd")
RUN_ID = re.compile(r"[a-z0-9]{8}\Z")
TOKEN = re.compile(r"[0-9a-f]{32}\Z")


class VmError(ValueError):
    """A stable VM_IMAGE, VM_LIMIT, VM_PROOF, or VM_OWNERSHIP diagnostic."""


def _safe_detail(stderr: str | None) -> str:
    line = ((stderr or "").strip().splitlines()[-1:] or [""])[0]
    line = "".join(character if character.isprintable() else " " for character in line)
    line = re.sub(
        r"-----BEGIN [^-]*PRIVATE KEY-----", "[redacted-key]", line, flags=re.I
    )
    line = re.sub(r"(?i)\b(token|password|secret|key)=\S+", r"\1=[redacted]", line)
    line = re.sub(
        r"\b(?:sk-[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9_]{8,})\b", "[redacted]", line
    )
    return line[:160]


@dataclass(frozen=True)
class VmPaths:
    directory: Path
    source: Path
    raw: Path
    vars: Path
    private_key: Path
    public_key: Path
    log: Path
    capsule: Path


def paths_for(root: Path, run_id: str) -> VmPaths:
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
        raise VmError("VM_OWNERSHIP: invalid run ID")
    directory = Path(root).resolve() / ".workspace-test" / run_id / "vm"
    return VmPaths(
        directory,
        directory / "source.qcow2",
        directory / "disk.raw",
        directory / "OVMF_VARS.fd",
        directory / "id_ed25519",
        directory / "id_ed25519.pub",
        directory / "controller.log",
        directory / "capsule.json",
    )


def unit_name(run_id: str) -> str:
    if not RUN_ID.fullmatch(run_id):
        raise VmError("VM_OWNERSHIP: invalid run ID")
    return f"hyk8s-test-{run_id}-vm"


def _invoke(
    run: Callable[..., Any],
    command: list[str],
    *,
    timeout: int = 30,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> str:
    try:
        result = run(
            command,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        detail = _safe_detail(exc.stderr or exc.stdout)
        raise VmError(f"VM_STEP: {command[0]} exit {exc.returncode}: {detail}") from exc
    except subprocess.TimeoutExpired as exc:
        raise VmError(f"VM_STEP: {command[0]} timed out after {timeout}s") from exc
    except OSError as exc:
        raise VmError(f"VM_STEP: {command[0]} {type(exc).__name__}") from exc
    if check and result.returncode != 0:
        raise VmError(
            f"VM_STEP: {command[0]} exit {result.returncode}: {_safe_detail(result.stderr or result.stdout)}"
        )
    return result.stdout


def verify_source(
    image: Path, expected_sha: str, *, run: Callable[..., Any] = subprocess.run
) -> dict[str, Any]:
    """Reject mutated, backed, encrypted, oversized or non-QCOW3 images."""
    image = Path(image)
    try:
        meta = image.lstat()
        if (
            not stat.S_ISREG(meta.st_mode)
            or meta.st_size < 104
            or meta.st_size > SOURCE_LIMIT
        ):
            raise ValueError("bad file type or size")
        digest = hashlib.sha256()
        with image.open("rb") as stream:
            header = stream.read(104)
            digest.update(header)
            while chunk := stream.read(MIB):
                digest.update(chunk)
        if digest.hexdigest() != expected_sha:
            raise ValueError("digest mismatch")
        if header[:4] != b"QFI\xfb" or struct.unpack_from(">I", header, 4)[0] != 3:
            raise ValueError("not QCOW3")
        backing_offset, backing_size = struct.unpack_from(">QI", header, 8)
        virtual_size = struct.unpack_from(">Q", header, 24)[0]
        if (
            backing_offset
            or backing_size
            or virtual_size <= 0
            or virtual_size > RAW_BYTES
        ):
            raise ValueError("backing file or virtual size")
        data = json.loads(
            _invoke(run, ["qemu-img", "info", "--output=json", str(image)])
        )
        if (
            data.get("format") != "qcow2"
            or data.get("virtual-size") != virtual_size
            or data.get("backing-filename")
            or data.get("encrypted")
        ):
            raise ValueError("qemu-img format, backing or size")
        return {
            "sha256": digest.hexdigest(),
            "virtual_size": virtual_size,
            "source_bytes": meta.st_size,
        }
    except (OSError, ValueError, TypeError, KeyError, VmError) as exc:
        raise VmError(
            "VM_IMAGE: official source identity or bounds are unverified"
        ) from exc


def qemu_command(
    paths: VmPaths,
    vm_uuid: str,
    ssh_port: int,
    *,
    provisioning: bool,
    metadata_port: int | None = None,
) -> list[str]:
    try:
        uuid.UUID(vm_uuid)
    except (ValueError, AttributeError) as exc:
        raise VmError("VM_PROOF: invalid VM UUID") from exc
    if type(ssh_port) is not int or not 1024 <= ssh_port <= 65535:
        raise VmError("VM_LIMIT: invalid loopback SSH port")
    if provisioning and (
        type(metadata_port) is not int
        or not 1024 <= metadata_port <= 65535
        or metadata_port == ssh_port
    ):
        raise VmError("VM_LIMIT: invalid metadata port")
    nic = f"user,id=n0,ipv6=off,hostfwd=tcp:127.0.0.1:{ssh_port}-:22"
    if provisioning:
        # A chardev guestfwd carries one stream; NoCloud fetches several files.
        parts = [sys.executable, str(Path(TRANSPORT.__file__).resolve())]
        if any(re.search(r"[^A-Za-z0-9_./+-]", part) for part in parts):
            raise VmError("VM_LIMIT: metadata relay path is not option-safe")
        nic += (
            f",guestfwd=tcp:10.0.2.100:80-cmd:{' '.join(parts)} relay {metadata_port}"
        )
    else:
        nic += ",restrict=on"
    kvm = os.access("/dev/kvm", os.R_OK | os.W_OK)
    command = [
        "qemu-system-x86_64",
        "-nodefaults",
        "-machine",
        "q35,accel=kvm" if kvm else "q35,accel=tcg",
        "-cpu",
        "host" if kvm else "qemu64",
        "-smp",
        "2",
        "-m",
        str(GUEST_MEMORY_MIB),
        "-uuid",
        vm_uuid,
        "-display",
        "none",
        "-monitor",
        "none",
        "-serial",
        "stdio",
        "-drive",
        f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
        "-drive",
        f"if=pflash,format=raw,file={paths.vars}",
        "-drive",
        f"if=virtio,format=raw,file={paths.raw},cache=none",
        "-netdev",
        nic,
        "-device",
        "virtio-net-pci,netdev=n0",
    ]
    if provisioning:
        command += ["-smbios", "type=1,serial=ds=nocloud;s=http://10.0.2.100/"]
    return command


def unit_command(
    paths: VmPaths, run_id: str, token: str, deadline_epoch: int
) -> list[str]:
    if (
        not RUN_ID.fullmatch(run_id)
        or not TOKEN.fullmatch(token)
        or type(deadline_epoch) is not int
        or deadline_epoch <= int(time.time())
    ):
        raise VmError("VM_OWNERSHIP: invalid unit binding or deadline")
    remaining = min(600, math.floor(deadline_epoch - time.time())) - 5
    if remaining < 1:
        raise VmError("VM_LIMIT: insufficient original deadline for bounded VM stop")
    return [
        "systemd-run",
        "--user",
        "--collect",
        f"--unit={unit_name(run_id)}",
        "--property=CPUQuota=200%",
        "--property=MemoryMax=4G",
        "--property=MemorySwapMax=0",
        f"--property=RuntimeMaxSec={remaining}",
        "--property=TimeoutStopSec=5",
        "--property=SendSIGKILL=yes",
        "--property=LimitCORE=0",
        "--property=KillMode=control-group",
        # Guest serial reaches this unit's journal, capped per run.
        "--property=LogRateLimitIntervalSec=600",
        "--property=LogRateLimitBurst=2000",
        sys.executable,
        str(Path(__file__).resolve()),
        "controller",
        "--root",
        str(paths.directory.parents[2]),
        "--run-id",
        run_id,
        "--token",
        token,
        "--deadline",
        str(deadline_epoch),
    ]


def guest_disk_proof(capsule: Path, *, sysroot: Path = Path("/")) -> dict[str, Any]:
    """Check the actual guest identity and sole bounded writable disk."""
    try:
        capsule = Path(capsule)
        meta = capsule.lstat()
        if (
            not stat.S_ISREG(meta.st_mode)
            or meta.st_uid != os.geteuid()
            or meta.st_mode & 0o077
            or meta.st_size > 4096
        ):
            raise ValueError("capsule is not private and regular")
        data = json.loads(capsule.read_text(encoding="utf-8"))
        actual_uuid = (
            (sysroot / "sys/class/dmi/id/product_uuid").read_text().strip().lower()
        )
        sectors = int((sysroot / "sys/block/vda/size").read_text().strip())
        block = sysroot / "sys/block"
        devices = {
            item.name
            for item in block.iterdir()
            if item.name.startswith(("vd", "sd", "nvme"))
        }
        host = data["host_cgroup_proof"]
        if (
            actual_uuid != data["vm_uuid"].lower()
            or devices != {"vda"}
            or sectors * 512 != RAW_BYTES
            or data["disk_bytes"] != RAW_BYTES
            or host["cpu_max"] != "200000 100000"
            or host["memory_max"] != str(4 * 1024**3)
            or host["memory_swap_max"] != "0"
            or host["unit"] != unit_name(data["run_id"])
            or not TOKEN.fullmatch(data["token"])
        ):
            raise ValueError("guest or host proof differs")
        return data
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        raise VmError(
            "VM_PROOF: actual guest disk and parent cgroup are unverified"
        ) from exc


class VmRun:
    """Run-owned VM lifecycle; the controller implementation follows below."""

    def __init__(
        self,
        root: Path,
        run_id: str,
        token: str,
        *,
        runner: Callable[..., Any] = subprocess.run,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if not TOKEN.fullmatch(token):
            raise VmError("VM_OWNERSHIP: invalid admission token")
        self.root = Path(root).resolve()
        self.run_id = run_id
        self.token = token
        self.paths = paths_for(self.root, run_id)
        self.runner = runner
        self.clock = clock
        self.error = VmError
        self._qemu_process: subprocess.Popen[bytes] | None = None
        self._metadata_server: Any = None
        self._dummy_server: Any = None

    def prepare(self, image: Path, expected_sha: str = SOURCE_SHA256) -> dict[str, Any]:
        source = verify_source(image, expected_sha, run=self.runner)
        directory = self.paths.directory
        try:
            _private_dir(directory)
        except ValueError as exc:
            raise VmError("VM_OWNERSHIP: run directory must be private") from exc
        if self.paths.raw.exists() or self.paths.vars.exists():
            raise VmError("VM_OWNERSHIP: VM disk already exists")
        staging = directory / f"disk.{uuid.uuid4().hex}.tmp"
        try:
            descriptor = os.open(
                staging, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
            )
            os.close(descriptor)
            if (directory / "owner.json").exists():
                self._record_files()
            deadline = (
                self._owner().get("deadline")
                if (directory / "owner.json").exists()
                else None
            )
            timeout = self._remaining(deadline) if type(deadline) is int else 600
            _invoke(
                self.runner,
                [
                    "qemu-img",
                    "convert",
                    "-f",
                    "qcow2",
                    "-O",
                    "raw",
                    str(image),
                    str(staging),
                ],
                timeout=timeout,
            )
            if (
                not staging.is_file()
                or staging.is_symlink()
                or staging.stat().st_size != source["virtual_size"]
            ):
                raise VmError("VM_IMAGE: converted raw disk is unverified")
            with staging.open("r+b") as stream:
                stream.truncate(RAW_BYTES)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(staging, self.paths.raw)
            if (directory / "owner.json").exists():
                self._record_files()
            shutil.copyfile(OVMF_VARS, self.paths.vars)
            if self.paths.vars.stat().st_size > MIB:
                raise VmError("VM_LIMIT: firmware variables exceed budget")
            if (directory / "owner.json").exists():
                self._record_files()
            return source | {"raw_bytes": RAW_BYTES}
        except (OSError, VmError) as exc:
            staging.unlink(missing_ok=True)
            raise VmError("VM_IMAGE: verified raw conversion failed") from exc

    def start(
        self,
        deadline_epoch: int,
        *,
        apps: list[str] | None = None,
        workspace_id: str | None = None,
        binding_id: str | None = None,
    ) -> None:
        if (
            type(deadline_epoch) is not int
            or not 0 < deadline_epoch - time.time() <= 600
        ):
            raise VmError("VM_LIMIT: one VM deadline must be within 600 seconds")
        if apps is not None and (
            not isinstance(apps, list)
            or any(
                not isinstance(app, str) or not re.fullmatch(r"[a-z0-9-]{1,64}", app)
                for app in apps
            )
        ):
            raise VmError("VM_INPUT: invalid selected Application closure")
        try:
            _private_dir(self.paths.directory)
            owner = {
                "run_id": self.run_id,
                "token": self.token,
                "unit": unit_name(self.run_id),
                "deadline": deadline_epoch,
                "workspace_id": workspace_id,
                "binding_id": binding_id,
                "vm_uuid": str(uuid.uuid4()),
                "status": "starting",
                "apps": list(apps or []),
                "dummy_port": 49152 + secrets.randbelow(16384),
                "dummy_nonce": secrets.token_hex(16),
                "files": {},
            }
            data = json.dumps(owner, sort_keys=True).encode()
            descriptor = os.open(
                self.paths.directory / "owner.json",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
            )
            try:
                os.write(descriptor, data)
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            directory = os.open(self.paths.directory, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        except (OSError, ValueError) as exc:
            raise VmError("VM_OWNERSHIP: durable VM intent is unavailable") from exc
        try:
            bus = _user_bus()
            _invoke(
                self.runner,
                unit_command(self.paths, self.run_id, self.token, deadline_epoch),
                env=bus,
            )
            active = _invoke(
                self.runner,
                [
                    "systemctl",
                    "--user",
                    "is-active",
                    f"{unit_name(self.run_id)}.service",
                ],
                env=bus,
                check=False,
            ).strip()
            if active != "active":
                raise VmError("VM_UNIT: owned bounded user unit is not active")
        except (ValueError, VmError) as exc:
            raise VmError("VM_UNIT: owned bounded user unit is unverified") from exc

    def _owner(self) -> dict[str, Any]:
        path = self.paths.directory / "owner.json"
        try:
            meta = path.lstat()
            if (
                not stat.S_ISREG(meta.st_mode)
                or meta.st_uid != os.geteuid()
                or meta.st_mode & 0o077
                or meta.st_size > 4096
            ):
                raise ValueError("owner record is not private")
            data = json.loads(path.read_text(encoding="utf-8"))
            if (
                data.get("run_id") != self.run_id
                or data.get("token") != self.token
                or data.get("unit") != unit_name(self.run_id)
            ):
                raise ValueError("owner binding differs")
            return data
        except (OSError, ValueError, AttributeError) as exc:
            raise VmError("VM_OWNERSHIP: durable VM intent is unverified") from exc

    def _require_parent_lease(self) -> None:
        """Bind a direct controller entry to its still active host reservation."""
        try:
            owner = self._owner()
            admission = Admission(self.root)
            lease = next(
                row
                for row in admission.active_for_run(self.run_id)
                if row["token"] == self.token
            )
            intent = lease["intent"]
            if (
                lease["kind"] != "cluster"
                or lease["binding_id"] != admission.binding_id
                or lease["workspace_id"] != admission.workspace_id
                or owner.get("binding_id") != admission.binding_id
                or owner.get("workspace_id") != admission.workspace_id
                or lease["closure"] != sorted(set(owner["apps"]))
                or lease["budget"]
                != {
                    "cpu": 2,
                    "memory_mib": 4096,
                    "disk_mib": 4096,
                    "seconds": 600,
                    "instances": 1,
                }
                or intent.get("unit") != unit_name(self.run_id)
                or intent.get("vm_dir") != str(self.paths.directory)
                or intent.get("deadline") != owner["deadline"]
                or not 0 < owner["deadline"] - lease["created_at"] <= 600
            ):
                raise ValueError("lease and owner differ")
        except (OSError, ValueError, KeyError, StopIteration, TypeError) as exc:
            raise VmError(
                "VM_OWNERSHIP: active outer VM reservation is unverified"
            ) from exc

    def _save_owner(self, owner: dict[str, Any]) -> None:
        if owner.get("token") != self.token or owner.get("run_id") != self.run_id:
            raise VmError("VM_OWNERSHIP: owner binding differs")
        temporary = self.paths.directory / f"owner.{uuid.uuid4().hex}.tmp"
        try:
            descriptor = os.open(
                temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
            )
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(owner, stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.paths.directory / "owner.json")
            directory = os.open(
                self.paths.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            )
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        except OSError as exc:
            temporary.unlink(missing_ok=True)
            raise VmError("VM_OWNERSHIP: owner update is unavailable") from exc

    def _record_files(self) -> None:
        allowed = {
            self.paths.source.name,
            self.paths.raw.name,
            self.paths.vars.name,
            self.paths.private_key.name,
            self.paths.public_key.name,
            self.paths.log.name,
            self.paths.capsule.name,
            "known_hosts",
        }
        files = {}
        for path in self.paths.directory.iterdir():
            if path.name == "owner.json":
                continue
            meta = path.lstat()
            if (
                (
                    path.name not in allowed
                    and not re.fullmatch(r"disk\.[0-9a-f]{32}\.tmp", path.name)
                )
                or not stat.S_ISREG(meta.st_mode)
                or meta.st_uid != os.geteuid()
            ):
                raise VmError("VM_OWNERSHIP: unexpected VM artifact")
            files[path.name] = [meta.st_dev, meta.st_ino]
        self._save_owner(self._owner() | {"files": files})

    def _unit_active(self) -> str:
        try:
            return _invoke(
                self.runner,
                [
                    "systemctl",
                    "--user",
                    "is-active",
                    f"{unit_name(self.run_id)}.service",
                ],
                env=_user_bus(),
                check=False,
            ).strip()
        except (ValueError, VmError) as exc:
            raise VmError("VM_UNIT: user unit status is unavailable") from exc

    def _unit_stopped(self) -> bool:
        return CLUSTER_ENV.vm_unit_stopped(self.runner, self.run_id)

    @staticmethod
    def _same_process(pid: Any, ticks: Any) -> bool:
        return (
            type(pid) is int
            and pid > 0
            and type(ticks) is int
            and ticks > 0
            and _process_start(pid) == ticks
        )

    def absent_owned(self) -> bool:
        owner = self._owner()
        if not self._unit_stopped():
            return False
        return all(
            (owner.get(pid) is None and owner.get(ticks) is None)
            or CLUSTER_ENV.creator_gone(
                owner.get(pid), owner.get(ticks), _process_start
            )
            for pid, ticks in (("main_pid", "main_start"), ("qemu_pid", "qemu_start"))
        )

    def stop_owned(self) -> bool:
        owner = self._owner()
        state = CLUSTER_ENV.vm_unit_state(self.runner, self.run_id)
        if state is None:
            return False
        if state["ActiveState"] == "active":
            pid, ticks = owner.get("main_pid"), owner.get("main_start")
            if (
                state["LoadState"] != "loaded"
                or state["MainPID"] != str(pid)
                or not self._same_process(pid, ticks)
            ):
                return False
            try:
                command = Path(f"/proc/{pid}/cmdline").read_bytes()
                if (
                    self.token.encode() not in command
                    or b"test_cluster_vm.py" not in command
                ):
                    return False
                _invoke(
                    self.runner,
                    [
                        "systemctl",
                        "--user",
                        "stop",
                        f"{unit_name(self.run_id)}.service",
                    ],
                    env=_user_bus(),
                )
            except (OSError, ValueError, VmError):
                return False
        if not self.absent_owned():
            return False
        if self.paths.directory.is_symlink():
            raise VmError("VM_OWNERSHIP: run directory changed to a symlink")
        return CLUSTER_ENV.remove_vm_files(self.paths.directory, owner)

    def payload_absent(self, admission: Admission) -> bool:
        owner = self._owner()
        directory = self.paths.directory.lstat()
        if (
            not stat.S_ISDIR(directory.st_mode)
            or directory.st_uid != os.geteuid()
            or directory.st_mode & 0o077
            or owner.get("workspace_id") != admission.workspace_id
            or owner.get("binding_id") != admission.binding_id
            or not self.absent_owned()
        ):
            return False
        return {path.name for path in self.paths.directory.iterdir()} == {"owner.json"}

    def finalize_owned(self) -> bool:
        owner = self._owner()
        if not self.absent_owned():
            return False
        return CLUSTER_ENV.remove_vm_files(self.paths.directory, owner, finalize=True)

    def wait_ready(self, deadline_epoch: int) -> dict[str, Any]:
        while time.time() < deadline_epoch:
            owner = self._owner()
            if owner.get("deadline") != deadline_epoch:
                raise VmError("VM_READY: owner deadline changed")
            if owner.get("status") == "ready":
                network = owner.get("network_probe")
                if (
                    not isinstance(owner.get("proof"), dict)
                    or not isinstance(owner.get("result"), dict)
                    or owner["result"].get("status") != "up"
                    or not isinstance(network, dict)
                    or network.get("internal_allowed") is not True
                    or network.get("owned_host_denied") is not True
                    or self._unit_active() != "active"
                ):
                    raise VmError(
                        "VM_READY: owned proof, guest result or network probe is unverified"
                    )
                return {
                    "proof": owner["proof"],
                    "result": owner["result"],
                    "network_probe": network,
                }
            if owner.get("status") == "failed" or self._unit_active() != "active":
                raise VmError("VM_READY: owned unit exited before guest readiness")
            time.sleep(0.2)
        raise VmError("VM_READY: original deadline expired before guest readiness")

    def _boot_qemu(
        self, ssh_port: int, *, provisioning: bool, metadata_port: int | None = None
    ) -> None:
        owner = self._owner()
        if (
            time.time() >= owner["deadline"]
            or not self.paths.raw.is_file()
            or not self.paths.vars.is_file()
        ):
            raise VmError("VM_LIMIT: prepared VM or original deadline is unavailable")
        command = qemu_command(
            self.paths,
            owner["vm_uuid"],
            ssh_port,
            provisioning=provisioning,
            metadata_port=metadata_port,
        )
        self._save_owner(
            owner
            | {
                "ssh_port": ssh_port,
                "metadata_port": metadata_port,
                "qemu_command_sha256": hashlib.sha256(
                    json.dumps(command).encode()
                ).hexdigest(),
                "status": "booting-provision" if provisioning else "booting-restricted",
            }
        )
        try:
            process = subprocess.Popen(
                command, stdin=subprocess.DEVNULL, close_fds=True
            )
        except OSError as exc:
            raise VmError("VM_STEP: bounded QEMU process failed to start") from exc
        ticks = _process_start(process.pid)
        if ticks is None:
            process.terminate()
            raise VmError("VM_OWNERSHIP: QEMU process identity is unavailable")
        self._qemu_process = process
        self._save_owner(
            self._owner()
            | {
                "qemu_pid": process.pid,
                "qemu_start": ticks,
                "status": "provisioning" if provisioning else "restricted",
            }
        )

    def _stop_qemu(self, deadline_epoch: int) -> None:
        owner = self._owner()
        process = self._qemu_process
        if process is not None and process.poll() is not None:
            self._qemu_process = None
            return
        if (
            process is None
            or process.pid != owner.get("qemu_pid")
            or not self._same_process(process.pid, owner.get("qemu_start"))
        ):
            raise VmError("VM_OWNERSHIP: provision QEMU identity is unverified")
        process.terminate()
        try:
            process.wait(timeout=max(1, min(10, deadline_epoch - time.time())))
        except subprocess.TimeoutExpired:
            if not self._same_process(process.pid, owner.get("qemu_start")):
                raise VmError("VM_OWNERSHIP: QEMU process changed during stop")
            process.kill()
            process.wait(timeout=5)
        self._qemu_process = None

    def reboot_restricted(self, ssh_port: int, deadline_epoch: int) -> None:
        owner = self._owner()
        if deadline_epoch != owner.get("deadline") or time.time() >= deadline_epoch:
            raise VmError(
                "VM_LIMIT: restricted reboot cannot reset the original deadline"
            )
        self._stop_qemu(deadline_epoch)
        if self._metadata_server is not None:
            self._metadata_server.shutdown()
            self._metadata_server.server_close()
            self._metadata_server = None
        self._boot_qemu(ssh_port, provisioning=False)

    @staticmethod
    def _remaining(deadline_epoch: int) -> int:
        remaining = int(deadline_epoch - time.time())
        if remaining <= 0:
            raise VmError("VM_LIMIT: original 600-second deadline expired")
        return remaining

    @staticmethod
    def _free_port() -> int:
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])

    def _exec(self, command: list[str], **kwargs: Any) -> str:
        return _invoke(self.runner, command, **kwargs)

    def _download_source(self, deadline_epoch: int) -> None:
        TRANSPORT.download_source(self, deadline_epoch)

    def _key(self) -> str:
        if self.paths.private_key.exists() or self.paths.public_key.exists():
            raise VmError("VM_OWNERSHIP: run key already exists")
        self._exec(
            [
                "ssh-keygen",
                "-q",
                "-t",
                "ed25519",
                "-N",
                "",
                "-f",
                str(self.paths.private_key),
            ],
            timeout=20,
        )
        meta = self.paths.private_key.lstat()
        if not stat.S_ISREG(meta.st_mode) or meta.st_mode & 0o077:
            raise VmError("VM_OWNERSHIP: run private key is not private")
        descriptor = os.open(
            self.paths.directory / "known_hosts",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
        )
        os.close(descriptor)
        return self.paths.public_key.read_text(encoding="ascii").strip()

    def _metadata(self, public_key: str) -> int:
        return TRANSPORT.metadata(self, public_key)

    def _ssh_command(self, ssh_port: int, argv: list[str]) -> list[str]:
        return TRANSPORT.ssh_command(self, ssh_port, argv)

    def _ssh(self, ssh_port: int, argv: list[str], deadline_epoch: int) -> str:
        return TRANSPORT.ssh(self, ssh_port, argv, deadline_epoch)

    def _wait_ssh(self, ssh_port: int, deadline_epoch: int) -> None:
        TRANSPORT.wait_ssh(self, ssh_port, deadline_epoch)

    def _copy_public_tree(self, ssh_port: int, deadline_epoch: int) -> str:
        return TRANSPORT.copy_public_tree(self, ssh_port, deadline_epoch)

    def _copy_binary(self, ssh_port: int, name: str, deadline_epoch: int) -> None:
        TRANSPORT.copy_binary(self, ssh_port, name, deadline_epoch)

    def _start_dummy(self) -> None:
        TRANSPORT.start_dummy(self)

    def _stop_dummy(self) -> None:
        TRANSPORT.stop_dummy(self)

    def _probe_phase(
        self, ssh_port: int, *, restricted: bool, deadline_epoch: int
    ) -> dict[str, bool]:
        return TRANSPORT.probe_phase(
            self, ssh_port, restricted=restricted, deadline=deadline_epoch
        )

    def _own_cgroup_caps(self) -> tuple[str, str, str, str]:
        try:
            own = Path("/proc/self/cgroup").read_text().strip().split("0::", 1)[1]
            if unit_name(self.run_id) + ".service" not in own.split("/"):
                raise ValueError("controller is outside its owned user unit")
            group = Path("/sys/fs/cgroup") / own.lstrip("/")
            cpu = (group / "cpu.max").read_text().strip()
            memory = (group / "memory.max").read_text().strip()
            swap = (group / "memory.swap.max").read_text().strip()
            if cpu != "200000 100000" or memory != str(4 * 1024**3) or swap != "0":
                raise ValueError("parent cgroup limits differ")
            return own, cpu, memory, swap
        except (OSError, ValueError, IndexError) as exc:
            raise VmError(
                "VM_LIMIT: owned controller cgroup caps are unverified"
            ) from exc

    def _host_cgroup_proof(self) -> dict[str, Any]:
        owner = self._owner()
        qemu_pid = owner.get("qemu_pid")
        if not self._same_process(qemu_pid, owner.get("qemu_start")):
            raise VmError("VM_PROOF: owned QEMU process is not live")
        try:
            own, cpu, memory, swap = self._own_cgroup_caps()
            child = (
                Path(f"/proc/{qemu_pid}/cgroup").read_text().strip().split("0::", 1)[1]
            )
            if own != child:
                raise ValueError("QEMU is outside the owned user unit")
            qemu_binary = shutil.which("qemu-system-x86_64")
            if qemu_binary is None or not os.path.samefile(
                f"/proc/{qemu_pid}/exe", qemu_binary
            ):
                raise ValueError("QEMU executable differs")
            raw = self.paths.raw.lstat()
            if not stat.S_ISREG(raw.st_mode) or raw.st_size != RAW_BYTES:
                raise ValueError("outer raw disk differs")
            return {
                "cpu_max": cpu,
                "memory_max": memory,
                "memory_swap_max": swap,
                "unit": unit_name(self.run_id),
                "cgroup": own,
                "qemu_pid": qemu_pid,
                "qemu_start": owner["qemu_start"],
            }
        except (OSError, ValueError, IndexError, TypeError) as exc:
            raise VmError(
                "VM_PROOF: actual parent cgroup and disk are unverified"
            ) from exc

    def _capsule(self, input_digest: str, deadline_epoch: int) -> dict[str, Any]:
        owner = self._owner()
        proof = self._host_cgroup_proof()
        capsule = {
            "run_id": self.run_id,
            "token": self.token,
            "vm_uuid": owner["vm_uuid"],
            "disk_bytes": RAW_BYTES,
            "deadline": deadline_epoch,
            "host_binding": Admission(self.root).binding_id,
            "dummy_port": owner["dummy_port"],
            "dummy_nonce": owner["dummy_nonce"],
            "input_digest": input_digest,
            "host_cgroup_proof": proof,
        }
        try:
            descriptor = os.open(
                self.paths.capsule,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
            )
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(capsule, stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
        except OSError as exc:
            raise VmError("VM_PROOF: parent capsule could not be recorded") from exc
        return capsule

    def _send_capsule(self, ssh_port: int, deadline_epoch: int) -> None:
        remote = self._ssh_command(
            ssh_port, ["sh", "-lc", "umask 077; cat > /home/hyk8s/vm-capsule.json"]
        )
        try:
            with self.paths.capsule.open("rb") as stream:
                result = self.runner(
                    remote,
                    stdin=stream,
                    capture_output=True,
                    check=True,
                    timeout=self._remaining(deadline_epoch),
                )
            if result.returncode != 0:
                raise VmError("VM_PROOF: guest capsule transfer failed")
        except (OSError, subprocess.SubprocessError) as exc:
            raise VmError("VM_PROOF: guest capsule transfer failed") from exc
        self._ssh(
            ssh_port,
            [
                "sudo",
                "-n",
                "install",
                "-o",
                "root",
                "-g",
                "root",
                "-m",
                "600",
                "/home/hyk8s/vm-capsule.json",
                "/root/hyk8s-vm-capsule.json",
            ],
            deadline_epoch,
        )
        self._ssh(ssh_port, ["rm", "-f", "/home/hyk8s/vm-capsule.json"], deadline_epoch)

    def _guest_enospc(self, ssh_port: int, deadline_epoch: int) -> None:
        script = (
            "import errno,os,tempfile; fs=os.statvfs('/'); before=fs.f_bavail*fs.f_frsize; "
            "request=max(4279238656,fs.f_blocks*fs.f_frsize)+1048576; "
            "assert before>268435456; fd,name=tempfile.mkstemp(dir='/home/hyk8s'); "
            "failed=False; "
            "\ntry:\n try: os.posix_fallocate(fd,0,request)\n except OSError as e: failed=e.errno==errno.ENOSPC\n"
            "finally: os.close(fd); os.unlink(name)\n"
            "after=os.statvfs('/').f_bavail*os.statvfs('/').f_frsize; "
            "assert failed and after+1048576>=before and after>268435456"
        )
        self._ssh(ssh_port, ["sudo", "-n", "python3", "-c", script], deadline_epoch)

    def controller(self, deadline_epoch: int) -> None:
        owner = self._owner()
        ticks = _process_start(os.getpid())
        if (
            owner.get("deadline") != deadline_epoch
            or time.time() >= deadline_epoch
            or ticks is None
        ):
            raise VmError(
                "VM_LIMIT: controller identity or original deadline is unverified"
            )
        self._require_parent_lease()
        self._own_cgroup_caps()
        self._save_owner(
            owner
            | {"main_pid": os.getpid(), "main_start": ticks, "status": "preparing"}
        )
        self._start_dummy()
        try:
            self._controller_body(deadline_epoch)
        finally:
            self._stop_dummy()

    def _controller_body(self, deadline_epoch: int) -> None:
        admission = Admission(self.root)
        prep = admission.reserve(
            self.run_id,
            "worker",
            [],
            {
                "cpu": 1,
                "memory_mib": 256,
                "disk_mib": 512,
                "seconds": self._remaining(deadline_epoch),
                "instances": 0,
            },
            {"vm_source": str(self.paths.source), "parent_token": self.token},
        )
        try:
            self._download_source(deadline_epoch)
            self.prepare(self.paths.source)
        finally:
            self.paths.source.unlink(missing_ok=True)
            self._record_files()
            admission.release(
                prep,
                lambda _: (
                    not self.paths.source.exists()
                    and not any(self.paths.directory.glob("disk.*.tmp"))
                ),
            )
        public_key = self._key()
        self._record_files()
        ssh_port = self._free_port()
        metadata_port = self._metadata(public_key)
        self._require_parent_lease()
        self._boot_qemu(ssh_port, provisioning=True, metadata_port=metadata_port)
        self._wait_ssh(ssh_port, deadline_epoch)
        self._probe_phase(ssh_port, restricted=False, deadline_epoch=deadline_epoch)
        self._record_files()
        self._ssh(ssh_port, ["cloud-init", "status", "--wait"], deadline_epoch)
        input_digest = self._copy_public_tree(ssh_port, deadline_epoch)
        for binary in ("k3d", "kubectl"):
            self._copy_binary(ssh_port, binary, deadline_epoch)
        self._ssh(
            ssh_port,
            ["sudo", "docker", "pull", "rancher/k3s:v1.35.0-k3s1"],
            deadline_epoch,
        )
        self._ssh(ssh_port, ["sudo", "docker", "pull", "busybox:1.37"], deadline_epoch)
        self._ssh(
            ssh_port,
            ["sudo", "-n", "docker", "pull", "rancher/mirrored-pause:3.6"],
            deadline_epoch,
        )
        self._ssh(
            ssh_port,
            [
                "sudo",
                "-n",
                "docker",
                "save",
                "-o",
                "/home/hyk8s/pause.tar",
                "rancher/mirrored-pause:3.6",
            ],
            deadline_epoch,
        )
        self._ssh(
            ssh_port,
            ["sudo", "-n", "docker", "pull", "ghcr.io/k3d-io/k3d-tools:5.9.0"],
            deadline_epoch,
        )
        self._ssh(
            ssh_port,
            ["sudo", "touch", "/etc/cloud/cloud-init.disabled"],
            deadline_epoch,
        )
        self._ssh(ssh_port, ["sync"], deadline_epoch)
        try:
            self._ssh(ssh_port, ["sudo", "shutdown", "-h", "now"], deadline_epoch)
        except VmError:
            pass  # SSH normally disconnects as the owned guest powers off.
        if self._qemu_process is None:
            raise VmError("VM_OWNERSHIP: provision QEMU process was lost")
        try:
            self._qemu_process.wait(timeout=self._remaining(deadline_epoch))
        except subprocess.TimeoutExpired as exc:
            raise VmError(
                "VM_STEP: prepared guest did not power off before restricted reboot"
            ) from exc
        self.reboot_restricted(ssh_port, deadline_epoch)
        self._wait_ssh(ssh_port, deadline_epoch)
        self._probe_phase(ssh_port, restricted=True, deadline_epoch=deadline_epoch)
        proof = self._capsule(input_digest, deadline_epoch)
        self._record_files()
        self._send_capsule(ssh_port, deadline_epoch)
        self._guest_enospc(ssh_port, deadline_epoch)
        selected = self._owner().get("apps")
        if not isinstance(selected, list) or not selected:
            raise VmError("VM_INPUT: selected Application closure is unavailable")
        guest = [
            "sudo",
            "-n",
            "env",
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "python3",
            "/home/hyk8s/work/scripts/test_cluster.py",
            "--root",
            "/home/hyk8s/work",
            "up",
            "--authority",
            "P07-bounded-VM",
            "--vm-capsule",
            "/root/hyk8s-vm-capsule.json",
            *selected,
        ]
        result = json.loads(self._ssh(ssh_port, guest, deadline_epoch))
        if not isinstance(result, dict) or result.get("status") != "up":
            raise VmError("VM_READY: selected guest cluster did not become ready")
        selected_probe = result.get("network_probe")
        if (
            not isinstance(selected_probe, dict)
            or selected_probe.get("internal_allowed") is not True
            or selected_probe.get("owned_host_denied") is not True
        ):
            raise VmError(
                "VM_NETWORK: guest pre-workload namespace probe is unverified"
            )
        self._probe_phase(ssh_port, restricted=True, deadline_epoch=deadline_epoch)
        self._save_owner(
            self._owner()
            | {
                "status": "ready",
                "proof": proof,
                "network_probe": selected_probe,
                "result": result,
            }
        )
        while (
            time.time() < deadline_epoch
            and self._qemu_process is not None
            and self._qemu_process.poll() is None
        ):
            time.sleep(1)


is_active = CLUSTER_ENV.vm_is_active
status_host = CLUSTER_ENV.vm_status_host


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    controller = sub.add_parser("controller")
    controller.add_argument("--root", type=Path, required=True)
    controller.add_argument("--run-id", required=True)
    controller.add_argument("--token", required=True)
    controller.add_argument("--deadline", type=int, required=True)
    args = parser.parse_args(argv)
    owned = VmRun(args.root, args.run_id, args.token)
    try:
        owned.controller(args.deadline)
    except (VmError, OSError, ValueError) as exc:
        try:
            owned._save_owner(
                owned._owner() | {"status": "failed", "failure": str(exc)[:160]}
            )
        except VmError:
            pass
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
