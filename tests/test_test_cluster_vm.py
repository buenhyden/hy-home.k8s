"""Synthetic regressions for the bounded P07 selected-cluster VM adapter."""

from __future__ import annotations

import hashlib
import importlib
import io
import json
import os
import struct
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def vm_module():
    return importlib.import_module("test_cluster_vm")


def qcow_header(*, backing: bool = False, virtual_mib: int = 3584) -> bytes:
    header = bytearray(104)
    header[:4] = b"QFI\xfb"
    struct.pack_into(">I", header, 4, 3)
    struct.pack_into(">Q", header, 8, 104 if backing else 0)
    struct.pack_into(">I", header, 16, 9 if backing else 0)
    struct.pack_into(">I", header, 20, 16)
    struct.pack_into(">Q", header, 24, virtual_mib * 1024 * 1024)
    return bytes(header) + (b"other.img" if backing else b"")


class VmContractTest(unittest.TestCase):
    def test_readiness_deadline_fails_without_discarding_owner_intent(self):
        vm = vm_module()

        def runner(command, **kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-ready-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline)
                with mock.patch.object(vm.time, "time", return_value=deadline + 1):
                    with self.assertRaisesRegex(vm.VmError, "VM_READY"):
                        owned.wait_ready(deadline)
            self.assertEqual(
                json.loads((owned.paths.directory / "owner.json").read_text())["token"],
                "a" * 32,
            )

    def test_readiness_requires_matching_owner_proof_and_guest_result(self):
        vm = vm_module()

        def runner(command, **_kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-ready-proof-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline, apps=["selected"])
            proof, guest = (
                {"vm_uuid": "synthetic-bound"},
                {"status": "up", "run_id": "p07vm001"},
            )
            network = {"internal_allowed": True, "owned_host_denied": True}
            owned._save_owner(
                owned._owner()
                | {
                    "status": "ready",
                    "proof": proof,
                    "result": guest,
                    "network_probe": network,
                }
            )
            self.assertEqual(
                owned.wait_ready(deadline),
                {"proof": proof, "result": guest, "network_probe": network},
            )
            without_network = owned._owner()
            without_network.pop("network_probe")
            owned._save_owner(without_network)
            with self.assertRaisesRegex(vm.VmError, "VM_READY"):
                owned.wait_ready(deadline)
            owned._save_owner(owned._owner() | {"network_probe": network})
            owned._save_owner(owned._owner() | {"deadline": deadline + 1})
            with self.assertRaisesRegex(vm.VmError, "VM_READY"):
                owned.wait_ready(deadline)

    def test_guest_proof_requires_exact_uuid_and_sole_fixed_vda(self):
        vm = vm_module()
        identity = "00000000-0000-4000-8000-000000000001"
        with tempfile.TemporaryDirectory(prefix="p07-vm-guest-") as temporary:
            root = Path(temporary)
            uuid_file = root / "sys/class/dmi/id/product_uuid"
            uuid_file.parent.mkdir(parents=True)
            uuid_file.write_text(identity)
            disk = root / "sys/block/vda/size"
            disk.parent.mkdir(parents=True)
            disk.write_text(str(4080 * 1024 * 1024 // 512))
            capsule = root / "capsule.json"
            capsule.write_text(
                json.dumps(
                    {
                        "run_id": "p07vm001",
                        "token": "a" * 32,
                        "vm_uuid": identity,
                        "disk_bytes": 4080 * 1024 * 1024,
                        "deadline": int(time.time()) + 300,
                        "host_cgroup_proof": {
                            "unit": "hyk8s-test-p07vm001-vm",
                            "cpu_max": "300000 100000",
                            "memory_max": str(4 * 1024**3),
                            "memory_swap_max": "0",
                        },
                    }
                )
            )
            capsule.chmod(0o600)
            self.assertEqual(
                vm.guest_disk_proof(capsule, sysroot=root)["vm_uuid"], identity
            )
            capsule.chmod(0o666)
            with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                vm.guest_disk_proof(capsule, sysroot=root)
            capsule.chmod(0o600)
            alias = root / "capsule-alias.json"
            alias.symlink_to(capsule)
            with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                vm.guest_disk_proof(alias, sysroot=root)
            (root / "sys/block/vdb").mkdir()
            with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                vm.guest_disk_proof(capsule, sysroot=root)

    def test_parent_cgroup_proof_binds_live_qemu_unit_limits_and_raw_disk(self):
        vm = vm_module()
        unit = "hyk8s-test-p07vm001-vm.service"
        group = f"/user.slice/{unit}"
        data = {
            "/proc/self/cgroup": f"0::{group}\n",
            "/proc/123456/cgroup": f"0::{group}\n",
            f"/sys/fs/cgroup{group}/cpu.max": "300000 100000\n",
            f"/sys/fs/cgroup{group}/memory.max": str(4 * 1024**3) + "\n",
            f"/sys/fs/cgroup{group}/memory.swap.max": "0\n",
        }

        def read_text(path, **_kwargs):
            return data[str(path)]

        with tempfile.TemporaryDirectory(prefix="p07-vm-cgroup-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32)
            owned.paths.directory.mkdir(parents=True)
            with owned.paths.raw.open("wb") as stream:
                stream.truncate(4080 * 1024 * 1024)
            owner = {"qemu_pid": 123456, "qemu_start": 777}
            with (
                mock.patch.object(owned, "_owner", return_value=owner),
                mock.patch.object(vm, "_process_start", return_value=777),
                mock.patch.object(vm.Path, "read_text", new=read_text),
                mock.patch.object(
                    vm.shutil, "which", return_value="/synthetic/qemu-system-x86_64"
                ),
                mock.patch.object(vm.os.path, "samefile", return_value=True),
            ):
                proof = owned._host_cgroup_proof()
                self.assertEqual(
                    (proof["unit"], proof["qemu_start"]),
                    ("hyk8s-test-p07vm001-vm", 777),
                )
                data[f"/sys/fs/cgroup{group}/cpu.max"] = "max 100000\n"
                with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                    owned._host_cgroup_proof()

    def test_parent_capsule_is_private_and_bound_to_host_input_and_deadline(self):
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-capsule-proof-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32)
            owned.paths.directory.mkdir(parents=True)
            deadline = int(time.time()) + 60
            owner = {
                "vm_uuid": "00000000-0000-4000-8000-000000000001",
                "dummy_port": 49152,
                "dummy_nonce": "a" * 32,
            }
            with (
                mock.patch.object(owned, "_owner", return_value=owner),
                mock.patch.object(
                    owned,
                    "_host_cgroup_proof",
                    return_value={"unit": vm.unit_name("p07vm001")},
                ),
                mock.patch.object(
                    vm, "Admission", return_value=mock.Mock(binding_id="test-binding")
                ),
            ):
                capsule = owned._capsule("public-digest", deadline)
                self.assertEqual(capsule["host_binding"], "test-binding")
                self.assertEqual(capsule["input_digest"], "public-digest")
                self.assertEqual(capsule["deadline"], deadline)
                self.assertEqual(
                    (capsule["dummy_port"], capsule["dummy_nonce"]), (49152, "a" * 32)
                )
                self.assertEqual(owned.paths.capsule.stat().st_mode & 0o077, 0)
                with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                    owned._capsule("different-input", deadline)
            self.assertEqual(json.loads(owned.paths.capsule.read_text()), capsule)

    def test_guest_profile_uses_proven_remaining_time_and_small_budget(self):
        vm = vm_module()
        environment = importlib.import_module("test_cluster_environment")
        capsule = Path("/synthetic/proof.json")
        with (
            mock.patch.object(
                vm,
                "guest_disk_proof",
                return_value={
                    "deadline": int(time.time()) + 300,
                    "dummy_port": 49152,
                    "dummy_nonce": "a" * 32,
                },
            ),
            mock.patch.object(
                environment, "verified_pause_tar", return_value="/home/hyk8s/pause.tar"
            ),
        ):
            profile = environment.verified_guest_profile(capsule)
        self.assertEqual(
            (profile["cpu"], profile["memory_mib"], profile["disk_mib"]),
            (3, 1536, 1024),
        )
        self.assertEqual(profile["server_memory"], "1536m")
        self.assertTrue(1 <= profile["seconds"] <= 300)
        with mock.patch.object(vm, "guest_disk_proof", return_value={"deadline": 0}):
            with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                environment.verified_guest_profile(capsule)

    def test_guest_profile_refuses_missing_or_unowned_pause_archive_before_cluster_start(
        self,
    ):
        vm = vm_module()
        environment = importlib.import_module("test_cluster_environment")
        capsule = Path("/synthetic/proof.json")
        with tempfile.TemporaryDirectory(prefix="p07-vm-pause-") as temporary:
            archive = Path(temporary) / "pause.tar"
            with (
                mock.patch.object(
                    vm,
                    "guest_disk_proof",
                    return_value={
                        "deadline": int(time.time()) + 300,
                        "dummy_port": 49152,
                        "dummy_nonce": "a" * 32,
                    },
                ),
                mock.patch.object(environment, "PAUSE_TAR", archive),
            ):
                with self.assertRaisesRegex(ValueError, "VM_INPUT"):
                    environment.verified_guest_profile(capsule)
                archive.write_bytes(b"synthetic archive")
                with self.assertRaisesRegex(ValueError, "VM_INPUT"):
                    environment.verified_guest_profile(capsule)

    def test_guest_cluster_mounts_only_the_verified_pause_archive_before_k3s_start(
        self,
    ):
        cluster = importlib.import_module("test_cluster")
        environment = importlib.import_module("test_cluster_environment")
        archive = str(environment.PAUSE_TAR)
        command = cluster.create_command(
            "hyk8s-test-p07vm001",
            "p07vm001",
            40222,
            "hyk8s-net-p07vm001",
            "1536m",
            pause_tar=archive,
        )
        volume = command[command.index("--volume") + 1]
        self.assertEqual(
            volume, archive + ":/var/lib/rancher/k3s/agent/images/pause.tar:ro@server:0"
        )
        own = "/repo/.workspace-test/p07vm001/pause.tar"
        self.assertIn(
            own + ":/var/lib/rancher/k3s/agent/images/pause.tar:ro@server:0",
            cluster.create_command(
                "hyk8s-test-p07vm001",
                "p07vm001",
                40222,
                "hyk8s-net-p07vm001",
                "1536m",
                pause_tar=own,
            ),
        )
        for untrusted in (
            "/tmp/untrusted.tar",
            "/tmp/pause.tar",
            "/repo/.workspace-test/othrrun1/pause.tar",
        ):
            with (
                self.subTest(untrusted=untrusted),
                self.assertRaisesRegex(ValueError, "CLUSTER_INPUT"),
            ):
                cluster.create_command(
                    "hyk8s-test-p07vm001",
                    "p07vm001",
                    40222,
                    "hyk8s-net-p07vm001",
                    "1536m",
                    pause_tar=untrusted,
                )

    def test_selected_guest_applies_product_only_after_controlled_namespace_probe(self):
        environment = importlib.import_module("test_cluster_environment")
        apps = {
            "platform-namespaces": {"path": "gitops/platform/namespaces", "uses": []},
            "platform-network-policies": {
                "path": "gitops/platform/network-policies",
                "uses": ["apps"],
            },
            "selected": {"path": "gitops/apps/selected", "uses": ["apps"]},
        }
        ordered = list(apps)
        rendered = {
            "platform-namespaces": [
                {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "apps"}}
            ],
            "platform-network-policies": [
                {
                    "apiVersion": "networking.k8s.io/v1",
                    "kind": "NetworkPolicy",
                    "metadata": {"name": "selected-policy", "namespace": "apps"},
                }
            ],
            "selected": [
                {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "metadata": {"name": "selected-product", "namespace": "apps"},
                }
            ],
        }
        profile = {
            "dummy_port": 49152,
            "dummy_nonce": "a" * 32,
            "pause_tar": "/home/hyk8s/pause.tar",
        }
        events = []

        def run(command, **kwargs):
            if (
                command[:3] == ["kubectl", "apply", "-f"]
                and "--dry-run=server" not in command
            ):
                kind = json.loads(kwargs["input_text"])["kind"]
                events.append("product" if kind == "Deployment" else "infrastructure")
            return ""

        def probe(*_args):
            events.append("probe")
            return {
                "namespace": "apps",
                "internal_allowed": True,
                "owned_host_denied": True,
            }

        with tempfile.TemporaryDirectory(prefix="p07-vm-selected-order-") as temporary:
            arguments = (
                run,
                Path(temporary),
                apps,
                ordered,
                rendered,
                {"KUBECONFIG": "/synthetic/kubeconfig"},
                "p07vm001",
                profile,
            )
            with mock.patch.object(
                environment, "selected_namespace_probe", side_effect=probe
            ):
                result = environment.apply_selected_guest(*arguments)
            self.assertLess(events.index("infrastructure"), events.index("probe"))
            self.assertLess(events.index("probe"), events.index("product"))
            self.assertTrue(result["network_probe"]["owned_host_denied"])
            events.clear()
            with mock.patch.object(
                environment,
                "selected_namespace_probe",
                side_effect=ValueError("CLUSTER_NETWORK: synthetic denial"),
            ):
                with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
                    environment.apply_selected_guest(*arguments)
            self.assertNotIn("product", events)

    def test_restricted_reboot_cannot_reset_the_original_deadline(self):
        vm = vm_module()
        commands = []

        def runner(command, **kwargs):
            commands.append(command)
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-deadline-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline)
                before = (owned.paths.directory / "owner.json").read_bytes()
                started_units = sum(command[0] == "systemd-run" for command in commands)
                with self.assertRaisesRegex(vm.VmError, "VM_LIMIT"):
                    owned.reboot_restricted(40222, deadline + 1)
                metadata = mock.Mock()
                owned._metadata_server = metadata
                with (
                    mock.patch.object(owned, "_stop_qemu") as stop,
                    mock.patch.object(owned, "_boot_qemu") as boot,
                ):
                    owned.reboot_restricted(40222, deadline)
                stop.assert_called_once_with(deadline)
                boot.assert_called_once_with(40222, provisioning=False)
                metadata.shutdown.assert_called_once_with()
                metadata.server_close.assert_called_once_with()
            self.assertEqual(
                (owned.paths.directory / "owner.json").read_bytes(), before
            )
            self.assertEqual(
                sum(command[0] == "systemd-run" for command in commands), started_units
            )

    def test_inactive_user_unit_preserves_owned_intent_without_direct_vm_start(self):
        vm = vm_module()
        commands = []

        def runner(command, **kwargs):
            commands.append(command)
            output = (
                "inactive\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-unit-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "_user_bus", return_value={}, create=True):
                with self.assertRaisesRegex(vm.VmError, "VM_UNIT"):
                    owned.start(int(time.time()) + 60)
            intent = json.loads((owned.paths.directory / "owner.json").read_text())
            self.assertEqual(intent["run_id"], "p07vm001")
            self.assertEqual(intent["token"], "a" * 32)
            self.assertTrue(any(command[0] == "systemd-run" for command in commands))
            self.assertFalse(
                any(command[0].startswith("qemu-system") for command in commands)
            )
            self.assertTrue(owned.paths.directory.exists())

    def test_prepare_rejects_unverified_image_before_raw_conversion(self):
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-prepare-") as temporary:
            root = Path(temporary)
            image = root / "untrusted.qcow2"
            image.write_bytes(b"not a qcow image")
            commands = []

            def runner(command, **kwargs):
                commands.append(command)
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            owned = vm.VmRun(root, "p07vm001", "a" * 32, runner=runner)
            with self.assertRaisesRegex(vm.VmError, "VM_IMAGE"):
                owned.prepare(image, "0" * 64)
            self.assertFalse(any("convert" in command for command in commands))
            self.assertFalse(owned.paths.raw.exists())

    def test_verified_qcow_conversion_keeps_virtual_size_and_fixed_raw_bound(self):
        vm = vm_module()
        virtual_bytes = 3584 * 1024 * 1024
        commands = []

        def runner(command, **kwargs):
            commands.append(command)
            if command[:2] == ["qemu-img", "info"]:
                output = json.dumps({"format": "qcow2", "virtual-size": virtual_bytes})
            elif command[:2] == ["qemu-img", "convert"]:
                with Path(command[-1]).open("wb") as stream:
                    stream.truncate(virtual_bytes)
                output = ""
            else:
                raise AssertionError("unexpected image operation")
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-raw-") as temporary:
            root = Path(temporary)
            image = root / "verified-source.qcow2"
            payload = qcow_header()
            image.write_bytes(payload)
            firmware = root / "OVMF_VARS.fd"
            firmware.write_bytes(b"synthetic firmware vars")
            owned = vm.VmRun(root, "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "OVMF_VARS", firmware):
                result = owned.prepare(image, hashlib.sha256(payload).hexdigest())
            self.assertEqual(result["virtual_size"], virtual_bytes)
            self.assertEqual(result["raw_bytes"], 4080 * 1024 * 1024)
            self.assertEqual(owned.paths.raw.stat().st_size, 4080 * 1024 * 1024)
            self.assertEqual(image.read_bytes(), payload)
            self.assertEqual(owned.paths.vars.read_bytes(), firmware.read_bytes())
            self.assertEqual(
                [command[:2] for command in commands],
                [["qemu-img", "info"], ["qemu-img", "convert"]],
            )

    def test_qemu_boot_keeps_command_digest_and_port_with_process_identity(self):
        vm = vm_module()

        def runner(command, **_kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-boot-identity-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(int(time.time()) + 60, apps=["selected"])
            owned.paths.raw.write_bytes(b"synthetic raw")
            owned.paths.vars.write_bytes(b"synthetic firmware")
            process = mock.Mock(pid=123456)
            with (
                mock.patch.object(
                    vm.subprocess, "Popen", return_value=process
                ) as spawned,
                mock.patch.object(vm, "_process_start", return_value=777),
            ):
                owned._boot_qemu(40222, provisioning=True, metadata_port=40223)
            owner = json.loads((owned.paths.directory / "owner.json").read_text())
            self.assertEqual((owner["qemu_pid"], owner["qemu_start"]), (123456, 777))
            self.assertEqual(owner["ssh_port"], 40222)
            self.assertEqual(owner["metadata_port"], 40223)
            self.assertEqual(len(owner["qemu_command_sha256"]), 64)
            self.assertEqual(spawned.call_args.args[0].count("-netdev"), 1)

    def test_qemu_stop_refuses_to_signal_a_reused_process_identity(self):
        vm = vm_module()

        def runner(command, **_kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-stop-pid-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline, apps=["selected"])
            process = mock.Mock(pid=123456)
            process.poll.return_value = None
            owned._qemu_process = process
            owned._save_owner(owned._owner() | {"qemu_pid": 123456, "qemu_start": 777})
            with mock.patch.object(vm, "_process_start", return_value=778):
                with self.assertRaisesRegex(vm.VmError, "VM_OWNERSHIP"):
                    owned._stop_qemu(deadline)
            process.terminate.assert_not_called()
            process.kill.assert_not_called()

    def test_owned_unit_identity_and_bounded_user_scope(self):
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-command-") as temporary:
            paths = vm.paths_for(Path(temporary), "p07vm001")
            command = vm.unit_command(paths, "p07vm001", "a" * 32, 1_800_000_600)
        text = " ".join(command)
        self.assertEqual(vm.unit_name("p07vm001"), "hyk8s-test-p07vm001-vm")
        for required in (
            "--user",
            "CPUQuota=300%",
            "MemoryMax=4G",
            "MemorySwapMax=0",
            "RuntimeMaxSec=",
            "TimeoutStopSec=",
            "LimitCORE=0",
            "KillMode=control-group",
        ):
            self.assertIn(required, text)
        runtime = int(
            next(item.split("=")[-1] for item in command if "RuntimeMaxSec=" in item)
        )
        grace = int(
            next(item.split("=")[-1] for item in command if "TimeoutStopSec=" in item)
        )
        self.assertLessEqual(runtime + grace, vm.VM_SECONDS)
        self.assertNotIn("0.0.0.0", text)

    def test_unit_runtime_is_only_the_remaining_original_deadline(self):
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-unit-time-") as temporary:
            paths = vm.paths_for(Path(temporary), "p07vm001")
            with mock.patch.object(vm.time, "time", return_value=1_800_000_000.2):
                command = vm.unit_command(paths, "p07vm001", "a" * 32, 1_800_000_010)
                with self.assertRaisesRegex(vm.VmError, "VM_LIMIT"):
                    vm.unit_command(paths, "p07vm001", "a" * 32, 1_800_000_005)
        runtime = int(
            next(item.split("=")[-1] for item in command if "RuntimeMaxSec=" in item)
        )
        grace = int(
            next(item.split("=")[-1] for item in command if "TimeoutStopSec=" in item)
        )
        self.assertGreater(grace, 0)
        self.assertLessEqual(runtime + grace, 10)
        self.assertNotIn("--property=RuntimeMaxSec=600", command)

    def test_bounded_vm_budget_is_1200_seconds_and_only_for_clusters(self):
        vm = vm_module()
        self.assertEqual(vm.VM_SECONDS, 1200)
        with tempfile.TemporaryDirectory(prefix="p07-vm-budget-") as temporary:
            paths = vm.paths_for(Path(temporary), "p07vm001")
            now = 1_800_000_000
            with mock.patch.object(vm.time, "time", return_value=now + 0.2):
                command = vm.unit_command(paths, "p07vm001", "a" * 32, now + 1200)
        self.assertIn("--property=RuntimeMaxSec=1194", command)
        admission = importlib.import_module("environment_admission")
        with tempfile.TemporaryDirectory(prefix="p07-vm-admission-") as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            gate = admission.Admission(root, state_dir=root / "state")
            budget = {
                "cpu": 2,
                "memory_mib": 256,
                "disk_mib": 64,
                "seconds": 1200,
                "instances": 1,
            }
            with mock.patch.object(
                admission, "_available_memory_mib", return_value=65536
            ):
                gate.reserve("p07vm001", "cluster", ["selected"], budget, {})
                with self.assertRaisesRegex(admission.AdmissionError, "per-run"):
                    gate.reserve(
                        "p07vm002", "native", [], budget | {"instances": 0}, {}
                    )
                with self.assertRaisesRegex(admission.AdmissionError, "per-run"):
                    gate.reserve(
                        "p07vm003",
                        "cluster",
                        ["selected"],
                        budget | {"seconds": 1201},
                        {},
                    )

    def test_runtime_command_has_one_restricted_nic_and_only_loopback_ssh(self):
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-command-") as temporary:
            paths = vm.paths_for(Path(temporary), "p07vm001")
            command = vm.qemu_command(
                paths, "00000000-0000-4000-8000-000000000001", 40222, provisioning=False
            )
            bootstrap = vm.qemu_command(
                paths,
                "00000000-0000-4000-8000-000000000001",
                40222,
                provisioning=True,
                metadata_port=40223,
            )
        text, setup = " ".join(command), " ".join(bootstrap)
        self.assertIn("restrict=on", text)
        self.assertIn("ipv6=off", text)
        self.assertIn("hostfwd=tcp:127.0.0.1:40222-:22", text)
        self.assertEqual(text.count("hostfwd="), 1)
        self.assertEqual(command.count("-netdev"), 1)
        self.assertEqual(command.count("-nodefaults"), 1)
        self.assertIn("guestfwd=", setup)
        for forbidden in (
            "guestfwd=",
            "0.0.0.0",
            "hostfwd=tcp::",
            "virtiofs",
            "-virtfs",
            "-fsdev",
            "-net tap",
        ):
            self.assertNotIn(forbidden, text)
        self.assertIn("-m 3072", text)
        self.assertIn("-smp 3", text)

    def test_provision_metadata_forward_spawns_one_relay_per_connection(self):
        # A guestfwd chardev carries one stream; cloud-init opens several.
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-guestfwd-") as temporary:
            paths = vm.paths_for(Path(temporary), "p07vm001")
            setup = " ".join(
                vm.qemu_command(
                    paths,
                    "00000000-0000-4000-8000-000000000001",
                    40222,
                    provisioning=True,
                    metadata_port=40223,
                )
            )
        self.assertIn("guestfwd=tcp:10.0.2.100:80-cmd:", setup)
        self.assertIn("test_cluster_vm_transport.py relay 40223", setup)
        self.assertNotIn("-tcp:127.0.0.1:40223", setup)
        self.assertIn("-serial stdio", setup)
        # The deprecated `nocloud-net` name makes `cloud-init status` exit 2.
        self.assertIn("serial=ds=nocloud;s=http://10.0.2.100/", setup)
        self.assertNotIn("nocloud-net", setup)

    def test_accelerator_uses_kvm_only_when_device_is_accessible(self):
        vm = vm_module()
        with tempfile.TemporaryDirectory(prefix="p07-vm-accel-") as temporary:
            paths = vm.paths_for(Path(temporary), "p07vm001")
            built = {}
            for allowed in (True, False):
                with mock.patch.object(vm.os, "access", return_value=allowed):
                    built[allowed] = " ".join(
                        vm.qemu_command(
                            paths,
                            "00000000-0000-4000-8000-000000000001",
                            40222,
                            provisioning=False,
                        )
                    )
        self.assertIn("q35,accel=kvm -cpu host", built[True])
        self.assertIn("q35,accel=tcg -cpu qemu64", built[False])

    def test_metadata_relay_serves_each_guest_connection_separately(self):
        import socket
        import threading

        transport = importlib.import_module("test_cluster_vm_transport")
        payloads = []

        class Handler(transport.http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                body = self.path.encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                return

        server = transport.BoundedHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            for path in ("/meta-data", "/user-data", "/vendor-data"):
                guest, relay_end = socket.socketpair()
                worker = threading.Thread(
                    target=transport.relay,
                    args=(server.server_port,),
                    kwargs={"fd": relay_end.fileno()},
                )
                worker.start()
                guest.sendall(f"GET {path} HTTP/1.0\r\n\r\n".encode())
                guest.settimeout(5)
                data = b""
                while chunk := guest.recv(4096):
                    data += chunk
                guest.close()
                worker.join(5)
                self.assertFalse(worker.is_alive())
                relay_end.close()
                payloads.append(data.rsplit(b"\r\n\r\n", 1)[-1])
        finally:
            server.shutdown()
            server.server_close()
        self.assertEqual(payloads, [b"/meta-data", b"/user-data", b"/vendor-data"])

    def test_image_digest_backing_and_oversized_virtual_disk_fail_before_conversion(
        self,
    ):
        vm = vm_module()
        calls = []

        def inspect(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=json.dumps(
                    {"format": "qcow2", "virtual-size": 3584 * 1024 * 1024}
                ),
                stderr="",
            )

        with tempfile.TemporaryDirectory(prefix="p07-vm-image-") as temporary:
            image = Path(temporary) / "source.qcow2"
            image.write_bytes(qcow_header())
            with self.assertRaisesRegex(vm.VmError, "VM_IMAGE"):
                vm.verify_source(image, "0" * 64, run=inspect)
            self.assertEqual(calls, [])
            image.write_bytes(qcow_header(backing=True))
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            with self.assertRaisesRegex(vm.VmError, "VM_IMAGE"):
                vm.verify_source(image, digest, run=inspect)
            image.write_bytes(qcow_header(virtual_mib=4096))
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            with self.assertRaisesRegex(vm.VmError, "VM_IMAGE"):
                vm.verify_source(image, digest, run=inspect)

    def test_public_guest_copy_excludes_untracked_file_and_rejects_symlinked_source_parent(
        self,
    ):
        vm = vm_module()
        transport = importlib.import_module("test_cluster_vm_transport")
        cluster = importlib.import_module("test_cluster")
        archives = []

        class Capture(io.BytesIO):
            def close(self):
                archives.append(self.getvalue())
                super().close()

        real_popen = subprocess.Popen

        def process(_command, **_kwargs):
            if Path(_command[0]).name == "git":
                return real_popen(_command, **_kwargs)
            child = mock.Mock(stdin=Capture())
            child.wait.return_value = 0
            return child

        with tempfile.TemporaryDirectory(prefix="p07-vm-index-") as temporary:
            root = Path(temporary)
            relative = [
                "gitops/apps/root/kustomization.yaml",
                "gitops/apps/selected/kustomization.yaml",
            ]
            relative += [
                f"scripts/{name}"
                for name in (
                    "test_cluster.py",
                    "test_cluster_environment.py",
                    "test_cluster_vm.py",
                    "test_cluster_vm_transport.py",
                    "environment_admission.py",
                )
            ]
            for name in relative:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"tracked public input")
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            subprocess.run(
                ["/usr/bin/git", "-C", str(root), "add", *relative],
                check=True,
                capture_output=True,
                timeout=10,
            )
            (root / "gitops/apps/selected/untracked-secret.yaml").write_bytes(
                b"not selected"
            )
            owned = vm.VmRun(root, "p07vm001", "a" * 32)
            with (
                mock.patch.object(owned, "_owner", return_value={"apps": ["selected"]}),
                mock.patch.object(
                    cluster,
                    "catalog",
                    return_value={"selected": {"path": "gitops/apps/selected"}},
                ),
                mock.patch.object(transport.subprocess, "Popen", side_effect=process),
                mock.patch.object(transport, "ssh", return_value=""),
            ):
                transport.copy_public_tree(owned, 40222, int(time.time()) + 60)
                with tarfile.open(fileobj=io.BytesIO(archives[-1])) as archive:
                    self.assertNotIn(
                        "gitops/apps/selected/untracked-secret.yaml", archive.getnames()
                    )
                (root / "gitops/apps").rename(root / "gitops/apps-real")
                (root / "gitops/apps").symlink_to("apps-real", target_is_directory=True)
                with self.assertRaisesRegex(vm.VmError, "VM_INPUT"):
                    transport.copy_public_tree(owned, 40222, int(time.time()) + 60)
                (root / "gitops/apps").unlink()
                (root / "gitops/apps-real").rename(root / "gitops/apps")
                with tempfile.TemporaryDirectory(
                    prefix="p07-vm-outside-"
                ) as outside_dir:
                    outside = Path(outside_dir) / "outside.bin"
                    outside.write_bytes(b"x" * (9 * 1024 * 1024))
                    target = root / "scripts/test_cluster.py"
                    original_lstat, seen = Path.lstat, [0]

                    def swap_after_checked_lstat(path, *args, **kwargs):
                        meta = original_lstat(path, *args, **kwargs)
                        if path == target:
                            seen[0] += 1
                            if seen[0] == 2:
                                target.rename(target.with_suffix(".original"))
                                target.symlink_to(outside)
                        return meta

                    with mock.patch.object(Path, "lstat", new=swap_after_checked_lstat):
                        with self.assertRaisesRegex(vm.VmError, "VM_INPUT"):
                            transport.copy_public_tree(
                                owned, 40222, int(time.time()) + 60
                            )
                    self.assertEqual(seen[0], 2)

    def test_vm_down_preserves_extra_sibling_and_retains_lease(self):
        vm = vm_module()
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-vm-parent-sibling-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            token = admission.reserve(
                "p07vm001",
                "cluster",
                ["selected"],
                {
                    "cpu": 3,
                    "memory_mib": 4096,
                    "disk_mib": 4096,
                    "seconds": vm_module().VM_SECONDS,
                    "instances": 1,
                },
                {"unit": vm.unit_name("p07vm001")},
            )
            parent = vm.paths_for(root, "p07vm001").directory.parent
            parent.mkdir(parents=True, mode=0o700)
            sibling = parent / "user-file"
            sibling.write_bytes(b"preserve this unrelated file")
            with mock.patch.object(vm.VmRun, "stop_owned", return_value=True):
                with self.assertRaisesRegex(vm.VmError, "VM_CLEANUP|VM_OWNERSHIP"):
                    importlib.import_module("test_cluster_vm_lifecycle").down_host(
                        None,
                        root,
                        {"run_id": "p07vm001", "admission_token": token},
                        admission=admission,
                    )
            self.assertEqual(sibling.read_bytes(), b"preserve this unrelated file")
            self.assertEqual(admission.active_for_run("p07vm001")[0]["token"], token)

    def test_vm_down_retains_lease_when_owner_record_is_missing_but_files_exist(self):
        vm = vm_module()
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-vm-no-owner-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            token = admission.reserve(
                "p07vm001",
                "cluster",
                ["selected"],
                {
                    "cpu": 3,
                    "memory_mib": 4096,
                    "disk_mib": 4096,
                    "seconds": vm_module().VM_SECONDS,
                    "instances": 1,
                },
                {"unit": vm.unit_name("p07vm001")},
            )
            directory = vm.paths_for(root, "p07vm001").directory
            directory.parent.mkdir(parents=True, mode=0o700)
            directory.mkdir(mode=0o700)
            marker = directory / "disk.raw"
            marker.write_bytes(b"unverified VM file")
            with self.assertRaisesRegex(vm.VmError, "VM_OWNERSHIP|VM_CLEANUP"):
                importlib.import_module("test_cluster_vm_lifecycle").down_host(
                    None,
                    root,
                    {"run_id": "p07vm001", "admission_token": token},
                    admission=admission,
                )
            self.assertTrue(marker.exists())
            self.assertEqual(admission.active_for_run("p07vm001")[0]["token"], token)

    def test_pre_owner_vm_intent_recovers_only_empty_private_dir_and_absent_unit(self):
        vm = vm_module()
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-vm-pre-owner-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            run_id = "p07vm001"
            directory = vm.paths_for(root, run_id).directory
            token = admission.reserve(
                run_id,
                "cluster",
                ["selected"],
                {
                    "cpu": 3,
                    "memory_mib": 4096,
                    "disk_mib": 4096,
                    "seconds": vm_module().VM_SECONDS,
                    "instances": 1,
                },
                {
                    "unit": vm.unit_name(run_id),
                    "vm_dir": str(directory),
                    "deadline": int(time.time()) + vm_module().VM_SECONDS,
                    "pid": 99999999,
                    "start_ticks": 1,
                },
            )
            directory.parent.mkdir(parents=True, mode=0o700)
            directory.mkdir(mode=0o700)
            record = {
                "run_id": run_id,
                "environment_kind": "vm",
                "admission_token": token,
                "unit": vm.unit_name(run_id),
                "status": "creating",
                "workspace_id": admission.workspace_id,
                "binding_id": admission.binding_id,
            }
            state = directory.parent / "state.json"
            state.write_text(json.dumps(record))
            state.chmod(0o600)

            def runner(command, **_kwargs):
                if command[:3] == ["systemctl", "--user", "stop"]:
                    self.assertEqual(command[-1], f"hyk8s-owned-{run_id}-{token}.timer")
                    return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
                self.assertIn(f"{vm.unit_name(run_id)}.service", command)
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                    stderr="",
                )

            environment = importlib.import_module("test_cluster_environment")
            with mock.patch.object(environment, "_user_bus", return_value={}):
                importlib.import_module("test_cluster_vm_lifecycle").recover_vm_intents(
                    root, admission, lambda _root, _run: record, runner=runner
                )
            self.assertEqual(admission.active_for_run(run_id), [])
            self.assertFalse(directory.parent.exists())

    def test_host_start_preserves_pre_state_failure_and_reserved_intent(self):
        vm = vm_module()
        cluster = importlib.import_module("test_cluster")
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-vm-pre-state-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            run_id = "p07vm001"
            parent = vm.paths_for(root, run_id).directory.parent
            original_mkdir = Path.mkdir

            def fail_run_parent(path, *args, **kwargs):
                if path == parent:
                    raise vm.VmError("VM_STEP: synthetic run parent creation failed")
                return original_mkdir(path, *args, **kwargs)

            selected = mock.Mock()
            selected.catalog.return_value = {}
            selected.plan.return_value = ["selected"]
            selected._write_state = cluster._write_state
            with mock.patch.object(Path, "mkdir", new=fail_run_parent):
                with self.assertRaisesRegex(
                    vm.VmError, "VM_STEP: synthetic run parent creation failed"
                ):
                    importlib.import_module("test_cluster_vm_lifecycle").up_host(
                        selected,
                        root,
                        ["selected"],
                        "synthetic",
                        run_id=run_id,
                        admission=admission,
                    )
            self.assertFalse(parent.exists())
            leases = admission.active_for_run(run_id)
            self.assertEqual(len(leases), 1)
            self.assertEqual(leases[0]["kind"], "cluster")

    def test_down_cannot_release_a_different_runs_cluster_lease(self):
        cluster = importlib.import_module("test_cluster")
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-cross-run-token-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            other = "other001"
            token = admission.reserve(
                other,
                "cluster",
                ["selected"],
                {
                    "cpu": 1,
                    "memory_mib": 512,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 1,
                },
                {"cluster": f"hyk8s-test-{other}"},
            )
            run_id = "first001"
            cluster._state_dir(root, run_id).mkdir(parents=True, mode=0o700)
            cluster._write_state(
                root,
                run_id,
                {
                    "run_id": run_id,
                    "cluster": f"hyk8s-test-{run_id}",
                    "admission_token": token,
                },
            )
            with (
                mock.patch.object(cluster, "list_clusters", return_value=[]),
                mock.patch.object(cluster, "_cleanup_owned", return_value=True),
                mock.patch.object(cluster, "_resources_absent", return_value=True),
            ):
                with self.assertRaisesRegex(
                    cluster.ClusterError, "CLUSTER_NOT_OWNED|ENV_BINDING"
                ):
                    cluster.down(root, run_id, admission=admission)
            self.assertEqual(
                [row["token"] for row in admission.active_for_run(other)], [token]
            )

    def test_expiry_keeps_a_live_creator_until_start_cannot_resume(self):
        cluster = importlib.import_module("test_cluster")
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-inflight-expiry-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            run_id = "expire01"
            token = admission.reserve(
                run_id,
                "cluster",
                ["selected"],
                {
                    "cpu": 1,
                    "memory_mib": 512,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 1,
                },
                {
                    "cluster": f"hyk8s-test-{run_id}",
                    "pid": os.getpid(),
                    "start_ticks": cluster._process_start(os.getpid()),
                },
            )
            cluster._state_dir(root, run_id).mkdir(parents=True, mode=0o700)
            cluster._write_state(
                root,
                run_id,
                {
                    "run_id": run_id,
                    "cluster": f"hyk8s-test-{run_id}",
                    "admission_token": token,
                    "expires_at": 0,
                },
            )
            with (
                mock.patch.object(cluster, "_cleanup_owned", return_value=True),
                mock.patch.object(cluster, "_resources_absent", return_value=True),
                mock.patch.object(cluster.CLUSTER_ENV, "disarm_expiry_timer"),
            ):
                self.assertEqual(
                    cluster.expire(root, run_id, token, admission=admission),
                    {"kept": run_id},
                )
                self.assertEqual(
                    [row["token"] for row in admission.active_for_run(run_id)], [token]
                )
                with mock.patch.object(
                    cluster.CLUSTER_ENV, "creator_gone", return_value=True, create=True
                ):
                    with mock.patch.object(
                        cluster.CLUSTER_ENV,
                        "create_inflight",
                        return_value=True,
                        create=True,
                    ):
                        self.assertEqual(
                            cluster.expire(root, run_id, token, admission=admission),
                            {"kept": run_id},
                        )
                        self.assertEqual(
                            [row["token"] for row in admission.active_for_run(run_id)],
                            [token],
                        )
                    with mock.patch.object(
                        cluster.CLUSTER_ENV,
                        "create_inflight",
                        return_value=False,
                        create=True,
                    ):
                        self.assertEqual(
                            cluster.expire(root, run_id, token, admission=admission),
                            {"deleted": f"hyk8s-test-{run_id}"},
                        )
            self.assertEqual(admission.active_for_run(run_id), [])

    def test_vm_controller_requires_guest_selected_probe_after_restricted_phase(self):
        vm = vm_module()
        steps, guest_commands = [], []

        class Admission:
            def __init__(self, _root):
                pass

            @staticmethod
            def reserve(*_args):
                return "prep-token"

            @staticmethod
            def release(_token, absent):
                if absent({}) is not True:
                    raise AssertionError("prep files remained")

        def runner(command, **kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        def boot(*_args, **_kwargs):
            owned._qemu_process = mock.Mock()
            owned._qemu_process.wait.return_value = 0
            owned._qemu_process.poll.return_value = 0

        def guest_ssh(_port, argv, _deadline):
            guest_commands.append(argv)
            if "rancher/mirrored-pause:3.6" in argv:
                steps.append("pause-pull" if "pull" in argv else "pause-save")
            if "ghcr.io/k3d-io/k3d-tools:5.9.0" in argv:
                steps.append("tools-pull")
            if any(part.endswith("/test_cluster.py") for part in argv):
                steps.append("guest-up")
            return '{"status":"up","run_id":"p07vm001","network_probe":{"internal_allowed":true,"owned_host_denied":true}}'

        with tempfile.TemporaryDirectory(prefix="p07-vm-routing-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline, apps=["selected"])
            with ExitStack() as patches:
                patches.enter_context(mock.patch.object(vm, "Admission", Admission))
                patches.enter_context(
                    mock.patch.object(
                        owned, "_require_parent_lease", return_value={}, create=True
                    )
                )
                patches.enter_context(
                    mock.patch.object(owned, "_own_cgroup_caps", return_value={})
                )
                for name, result in {
                    "_download_source": None,
                    "prepare": {},
                    "_key": "public-key",
                    "_free_port": 40222,
                    "_metadata": 40223,
                    "_wait_ssh": None,
                    "_copy_public_tree": "public-digest",
                    "_copy_binary": None,
                    "_capsule": {},
                    "_send_capsule": None,
                    "_guest_enospc": 900,
                }.items():
                    patches.enter_context(
                        mock.patch.object(owned, name, return_value=result)
                    )
                patches.enter_context(
                    mock.patch.object(owned, "_ssh", side_effect=guest_ssh)
                )
                patches.enter_context(
                    mock.patch.object(owned, "_boot_qemu", side_effect=boot)
                )
                patches.enter_context(
                    mock.patch.object(
                        owned,
                        "_start_dummy",
                        side_effect=lambda: steps.append("dummy"),
                        create=True,
                    )
                )
                patches.enter_context(
                    mock.patch.object(
                        owned,
                        "_stop_dummy",
                        side_effect=lambda: steps.append("stop"),
                        create=True,
                    )
                )
                patches.enter_context(
                    mock.patch.object(
                        owned,
                        "reboot_restricted",
                        side_effect=lambda *_: steps.append("reboot"),
                    )
                )
                patches.enter_context(
                    mock.patch.object(
                        owned,
                        "_probe_phase",
                        side_effect=lambda *_, **kw: (
                            steps.append(
                                "restricted" if kw.get("restricted") else "provision"
                            )
                            or {"restricted": kw.get("restricted")}
                        ),
                        create=True,
                    )
                )
                owned.controller(deadline)
            self.assertEqual(
                [
                    step
                    for step in steps
                    if step not in {"pause-pull", "pause-save", "tools-pull"}
                ],
                [
                    "dummy",
                    "provision",
                    "reboot",
                    "restricted",
                    "guest-up",
                    "restricted",
                    "stop",
                ],
            )
            for dependency in ("pause-pull", "pause-save", "tools-pull"):
                self.assertLess(steps.index("provision"), steps.index(dependency))
                self.assertLess(steps.index(dependency), steps.index("reboot"))
            self.assertLess(steps.index("pause-pull"), steps.index("pause-save"))
            owner = json.loads((owned.paths.directory / "owner.json").read_text())
            self.assertEqual(owner["status"], "ready")
            self.assertTrue(owner["network_probe"]["owned_host_denied"])
            # Each boundary result is kept, not only the final readiness.
            self.assertEqual(owner["restricted_probe"], {"restricted": True})
            self.assertEqual(owner["provision_probe"], {"restricted": False})
            self.assertEqual(owner["guest_enospc"], {"enospc": True, "free_mib": 900})
            order = ["image", "provision_ssh", "restricted_ssh", "enospc", "guest_up"]
            self.assertEqual(sorted(owner["phases"]), sorted(order))
            elapsed = [owner["phases"][name] for name in order]
            self.assertEqual(elapsed, sorted(elapsed))
            clean = next(
                i
                for i, argv in enumerate(guest_commands)
                if "apt-get clean" in " ".join(argv)
            )
            shutdown = next(
                i for i, argv in enumerate(guest_commands) if "shutdown" in argv
            )
            self.assertLess(clean, shutdown)
            selected_up = next(
                argv
                for argv in guest_commands
                if any(part.endswith("/test_cluster.py") for part in argv)
            )
            self.assertEqual(selected_up[:2], ["sudo", "-n"])
            capsule = selected_up[selected_up.index("--vm-capsule") + 1]
            self.assertTrue(capsule.startswith("/root/"))


if __name__ == "__main__":
    unittest.main()
