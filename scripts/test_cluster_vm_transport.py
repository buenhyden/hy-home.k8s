"""Bounded public bootstrap and controlled network probes for one owned VM."""

from __future__ import annotations

import hashlib
import http.server
import io
import json
import os
import re
import select
import shlex
import shutil
import socket
import stat
import sys
import subprocess
import tarfile
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import test_cluster_environment as ENV

MIB = 1024 * 1024
SOURCE_LIMIT = 512 * MIB
SOURCE_URL = "https://cloud-images.ubuntu.com/minimal/releases/noble/release-20261105/ubuntu-24.04-minimal-cloudimg-amd64.img"


def relay(port: int, *, fd: int = 0, limit: int = MIB, seconds: int = 30) -> int:
    """Join one QEMU guestfwd connection (fd 0) to the owned metadata port."""
    guest = socket.socket(fileno=os.dup(fd))
    with guest, socket.create_connection(("127.0.0.1", port), timeout=5) as host:
        peer = {guest: host, host: guest}
        open_ends, moved = set(peer), 0
        deadline = time.monotonic() + seconds
        while open_ends and moved <= limit and time.monotonic() < deadline:
            for source in select.select(list(open_ends), [], [], 1)[0]:
                data = source.recv(65536)
                moved += len(data)
                if data:
                    peer[source].sendall(data)
                    continue
                open_ends.discard(source)
                try:
                    peer[source].shutdown(socket.SHUT_WR)
                except OSError:
                    pass
    return 0


class BoundedHTTPServer(http.server.HTTPServer):
    """Serve one fixed-payload request at a time with bounded socket reads."""

    request_queue_size = 1

    def get_request(self) -> tuple[Any, Any]:
        connection, address = super().get_request()
        connection.settimeout(3)
        return connection, address


def download_source(vm: Any, deadline: int) -> None:
    if vm.paths.source.exists():
        raise vm.error("VM_IMAGE: source image already exists")
    request = urllib.request.Request(
        SOURCE_URL, headers={"User-Agent": "hy-home-k8s-p07-vm/1"}
    )

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *_args: Any, **_kwargs: Any) -> None:
            raise vm.error("VM_IMAGE: official source redirected")

    try:
        with urllib.request.build_opener(NoRedirect()).open(
            request, timeout=min(30, vm._remaining(deadline))
        ) as response:
            final = urllib.parse.urlsplit(response.geturl())
            if final.scheme != "https" or final.hostname != "cloud-images.ubuntu.com":
                raise vm.error("VM_IMAGE: source redirected outside official host")
            descriptor = os.open(
                vm.paths.source,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
            )
            vm._record_files()
            with os.fdopen(descriptor, "wb") as stream:
                total = 0
                while chunk := response.read(MIB):
                    vm._remaining(deadline)
                    total += len(chunk)
                    if total > SOURCE_LIMIT:
                        raise vm.error("VM_IMAGE: official image exceeds 512 MiB")
                    stream.write(chunk)
                stream.flush()
                os.fsync(stream.fileno())
    except (OSError, ValueError) as exc:
        raise vm.error(
            "VM_IMAGE: official image download failed or exceeded budget"
        ) from exc


def metadata(vm: Any, public_key: str) -> int:
    user_data = (
        "#cloud-config\n"
        + json.dumps(
            {
                "users": [
                    {
                        "name": "hyk8s",
                        "groups": ["sudo"],
                        "sudo": "ALL=(ALL) NOPASSWD:ALL",
                        "shell": "/bin/bash",
                        "ssh_authorized_keys": [public_key],
                    }
                ],
                "package_update": True,
                "packages": [
                    "docker.io",
                    "python3-yaml",
                    "git",
                    "openssh-server",
                    "ca-certificates",
                ],
                "runcmd": [["usermod", "-aG", "docker", "hyk8s"]],
            }
        )
        + "\n"
    )
    payloads = {
        "/meta-data": f"instance-id: hyk8s-{vm.run_id}-{vm.token[:8]}\nlocal-hostname: hyk8s-vm\n".encode(),
        "/user-data": user_data.encode(),
        "/vendor-data": b"#cloud-config\n{}\n",
    }

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            body = payloads.get(self.path)
            if body is None:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: Any) -> None:
            return

    server = BoundedHTTPServer(("127.0.0.1", 0), Handler)
    vm._metadata_server = server
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return int(server.server_port)


def ssh_command(vm: Any, port: int, argv: list[str]) -> list[str]:
    command = [
        "ssh",
        "-F",
        "/dev/null",
        "-o",
        "BatchMode=yes",
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "ForwardAgent=no",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        f"UserKnownHostsFile={vm.paths.directory / 'known_hosts'}",
        "-o",
        "GlobalKnownHostsFile=/dev/null",
        "-i",
        str(vm.paths.private_key),
        "-p",
        str(port),
        "--",
        "hyk8s@127.0.0.1",
    ]
    return command + [" ".join(shlex.quote(part) for part in argv)]


def ssh(vm: Any, port: int, argv: list[str], deadline: int) -> str:
    return vm._exec(ssh_command(vm, port, argv), timeout=vm._remaining(deadline))


def wait_ssh(vm: Any, port: int, deadline: int) -> None:
    while vm._remaining(deadline) > 0:
        if vm._qemu_process is None or vm._qemu_process.poll() is not None:
            raise vm.error("VM_STEP: guest exited before SSH readiness")
        try:
            vm._exec(ssh_command(vm, port, ["true"]), timeout=5)
            return
        except ValueError:
            time.sleep(1)


def _public_relative(vm: Any, path: Path) -> str:
    try:
        relative = path.relative_to(vm.root)
        if (
            not relative.parts
            or any(
                part in {".", ".."} or part.startswith(".") for part in relative.parts
            )
            or not path.resolve(strict=True).is_relative_to(vm.root)
        ):
            raise ValueError("unsafe public path")
        cursor = vm.root
        for part in relative.parts:
            cursor = cursor / part
            if stat.S_ISLNK(cursor.lstat().st_mode):
                raise ValueError("symlinked public path")
        return relative.as_posix()
    except (OSError, ValueError) as exc:
        raise vm.error(
            "VM_INPUT: public source path is outside its owner or symlinked"
        ) from exc


def copy_public_tree(vm: Any, port: int, deadline: int) -> str:
    """Stream selected public manifests and all root Application declarations."""
    import test_cluster as cluster
    from validation.repository.bounded_io import (
        BoundedInputError,
        read_bytes as read_bounded_bytes,
    )

    owner = vm._owner()
    apps = cluster.catalog(vm.root)
    selected = owner.get("apps")
    if not isinstance(selected, list) or any(name not in apps for name in selected):
        raise vm.error("VM_OWNERSHIP: selected Application closure is unavailable")
    sources = [vm.root / "gitops/apps/root"] + [
        vm.root / apps[name]["path"] for name in selected
    ]
    scoped = [_public_relative(vm, source) for source in sources]
    try:
        tracked = subprocess.run(
            [
                "/usr/bin/git",
                "-C",
                str(vm.root),
                "ls-files",
                "-z",
                "--cached",
                "--",
                *scoped,
            ],
            capture_output=True,
            check=True,
            timeout=min(10, vm._remaining(deadline)),
            env={
                "PATH": "/usr/bin:/bin",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_OPTIONAL_LOCKS": "0",
            },
        ).stdout
        if len(tracked) > MIB:
            raise ValueError("tracked manifest list is too large")
        files = {
            vm.root / name.decode("utf-8") for name in tracked.split(b"\0") if name
        }
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
        raise vm.error(
            "VM_INPUT: selected public manifest index is unavailable"
        ) from exc
    files.update(
        vm.root / "scripts" / name
        for name in (
            "test_cluster.py",
            "test_cluster_environment.py",
            "test_cluster_vm.py",
            "test_cluster_vm_transport.py",
            "environment_admission.py",
        )
    )
    digest = hashlib.sha256()
    size = 0
    checked: list[tuple[str, bytes]] = []
    for path in sorted(files):
        relative = _public_relative(vm, path)
        meta = path.lstat()
        if (
            not stat.S_ISREG(meta.st_mode)
            or meta.st_size > 8 * MIB
            or (relative.startswith("gitops/") and path.suffix not in {".yaml", ".yml"})
        ):
            raise vm.error("VM_INPUT: public source contains an unsafe file")
        try:
            payload = read_bounded_bytes(path, max_bytes=8 * MIB)
        except BoundedInputError as exc:
            raise vm.error(
                "VM_INPUT: public source changed or exceeded its byte limit"
            ) from exc
        size += len(payload)
        if size > 32 * MIB:
            raise vm.error("VM_INPUT: public source exceeds 32 MiB")
        digest.update(relative.encode() + b"\0" + hashlib.sha256(payload).digest())
        checked.append((relative, payload))
    remote = ssh_command(
        vm,
        port,
        ["sh", "-lc", "mkdir -p /home/hyk8s/work && tar -xf - -C /home/hyk8s/work"],
    )
    try:
        process = subprocess.Popen(
            remote,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        assert process.stdin is not None
        with tarfile.open(fileobj=process.stdin, mode="w|") as archive:
            for relative, payload in checked:
                vm._remaining(deadline)
                info = tarfile.TarInfo(relative)
                info.size, info.mode, info.mtime = len(payload), 0o644, 0
                archive.addfile(info, io.BytesIO(payload))
        process.stdin.close()
        if process.wait(timeout=vm._remaining(deadline)) != 0:
            raise vm.error("VM_INPUT: guest source transfer failed")
    except (OSError, subprocess.SubprocessError) as exc:
        raise vm.error("VM_INPUT: guest source transfer failed") from exc
    ssh(
        vm,
        port,
        ["sudo", "-n", "chown", "-R", "root:root", "/home/hyk8s/work"],
        deadline,
    )
    ssh(
        vm,
        port,
        ["sudo", "-n", "git", "-C", "/home/hyk8s/work", "init", "-q"],
        deadline,
    )
    return digest.hexdigest()


def copy_binary(vm: Any, port: int, name: str, deadline: int) -> None:
    located = shutil.which(name)
    if located is None:
        raise vm.error(f"VM_INPUT: installed {name} binary is unavailable")
    source = Path(located).resolve()
    meta = source.lstat()
    if not stat.S_ISREG(meta.st_mode) or meta.st_size > 128 * MIB:
        raise vm.error(f"VM_INPUT: installed {name} binary is unverified")
    remote = ssh_command(
        vm,
        port,
        [
            "sh",
            "-lc",
            f"mkdir -p /home/hyk8s/bin && cat > /home/hyk8s/bin/{name} && chmod 755 /home/hyk8s/bin/{name}",
        ],
    )
    try:
        process = subprocess.Popen(
            remote,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        assert process.stdin is not None
        with source.open("rb") as stream:
            while chunk := stream.read(MIB):
                vm._remaining(deadline)
                process.stdin.write(chunk)
        process.stdin.close()
        if process.wait(timeout=vm._remaining(deadline)) != 0:
            raise vm.error(f"VM_INPUT: guest {name} transfer failed")
    except (OSError, subprocess.SubprocessError) as exc:
        raise vm.error(f"VM_INPUT: guest {name} transfer failed") from exc
    ssh(
        vm,
        port,
        [
            "sudo",
            "-n",
            "install",
            "-m",
            "755",
            f"/home/hyk8s/bin/{name}",
            f"/usr/local/bin/{name}",
        ],
        deadline,
    )
    ssh(vm, port, ["rm", "-f", f"/home/hyk8s/bin/{name}"], deadline)


def start_dummy(vm: Any) -> None:
    owner = vm._owner()
    port, nonce = owner["dummy_port"], owner["dummy_nonce"]
    if (
        type(port) is not int
        or not 49152 <= port <= 65535
        or not re.fullmatch(r"[0-9a-f]{32}", nonce)
    ):
        raise vm.error("VM_NETWORK: owned dummy identity is invalid")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path != "/":
                self.send_error(404)
                return
            body = nonce.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: Any) -> None:
            return

    try:
        vm._dummy_server = BoundedHTTPServer(("127.0.0.1", port), Handler)
    except OSError as exc:
        raise vm.error("VM_NETWORK: owned dummy port is unavailable") from exc
    threading.Thread(target=vm._dummy_server.serve_forever, daemon=True).start()


def stop_dummy(vm: Any) -> None:
    if vm._dummy_server is not None:
        vm._dummy_server.shutdown()
        vm._dummy_server.server_close()
        vm._dummy_server = None


def probe_phase(
    vm: Any, ssh_port: int, *, restricted: bool, deadline: int
) -> dict[str, bool]:
    owner = vm._owner()
    port, nonce = owner["dummy_port"], owner["dummy_nonce"]

    def local_get() -> str:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as response:
            return response.read(128).decode().strip()

    def guest_get() -> str:
        script = (
            "import urllib.request; "
            "\ntry:\n print(urllib.request.urlopen('http://10.0.2.2:%d/',timeout=3).read(128).decode().strip())"
            "\nexcept OSError: print('blocked')" % port
        )
        return ssh(vm, ssh_port, ["python3", "-c", script], deadline).strip()

    return ENV.probe_boundary(local_get, guest_get, nonce, restricted=restricted)


if __name__ == "__main__":
    # QEMU guestfwd `cmd:` entry: `relay <loopback metadata port>`.
    if len(sys.argv) != 3 or sys.argv[1] != "relay" or not sys.argv[2].isdigit():
        raise SystemExit(2)
    raise SystemExit(relay(int(sys.argv[2])))
