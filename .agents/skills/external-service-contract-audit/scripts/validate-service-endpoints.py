#!/usr/bin/env python3
"""Validate selectorless external Service/EndpointSlice joins without network access."""

from __future__ import annotations

import argparse
import ipaddress
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Sequence

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
from validation.repository.bounded_io import (  # noqa: E402
    BoundedInputError,
    BoundedOutputError,
    read_text,
    run,
)

PREFIX = Path("gitops/platform/external-services")
MAX_FILES = 128
MAX_DOCUMENTS = 512


def _mapping(value):
    if not isinstance(value, dict):
        raise ValueError("expected mapping")
    return value


def _name(value):
    if not isinstance(value, str) or not value or len(value) > 253:
        raise ValueError("invalid name")
    return value


def _ports(value, *, service=False):
    if not isinstance(value, list) or not value or len(value) > 128:
        raise ValueError("invalid ports")
    result = set()
    names = set()
    for raw in value:
        port = _mapping(raw)
        name = port.get("name", "")
        protocol = port.get("protocol", "TCP")
        number = port.get("port")
        target = port.get("targetPort", number) if service else number
        if (
            not isinstance(name, str)
            or len(name) > 63
            or protocol not in ("TCP", "UDP", "SCTP")
            or type(number) is not int
            or not 1 <= number <= 65535
            or type(target) is not int
            or not 1 <= target <= 65535
            or (name, protocol) in names
        ):
            raise ValueError("invalid port contract")
        names.add((name, protocol))
        result.add((name, protocol, target))
    return result


def _endpoints(document):
    family = document.get("addressType")
    if family not in ("IPv4", "IPv6", "FQDN"):
        raise ValueError("invalid address type")
    endpoints = document.get("endpoints")
    if not isinstance(endpoints, list) or not endpoints or len(endpoints) > 1000:
        raise ValueError("invalid endpoints")
    addresses = set()
    for endpoint in endpoints:
        values = _mapping(endpoint).get("addresses")
        if not isinstance(values, list) or not values or len(values) > 100:
            raise ValueError("invalid addresses")
        for value in values:
            if not isinstance(value, str):
                raise ValueError("invalid address")
            if family == "FQDN":
                if len(value) > 253 or any(
                    not re.fullmatch(
                        r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label
                    )
                    for label in value.split(".")
                ):
                    raise ValueError("invalid DNS address")
            else:
                address = ipaddress.ip_address(value)
                if (
                    address.version != (4 if family == "IPv4" else 6)
                    or address.is_loopback
                    or address.is_link_local
                    or address.is_multicast
                    or address.is_unspecified
                ):
                    raise ValueError("address family or routing differs")
            addresses.add(value)
    return addresses


def validate_documents(root: Path, paths: Sequence[Path]) -> list[str]:
    """Return bounded field diagnostics; input content and parser details stay private."""
    if len(paths) > MAX_FILES:
        return ["external-services: file count exceeds limit"]
    root = Path(os.path.abspath(root))
    services = {}
    managed = set()
    slices = []
    errors = []
    count = 0
    identities = set()
    for index, raw_path in enumerate(paths):
        label = f"external-services input[{index}]"
        try:
            path = Path(raw_path)
            if not path.is_absolute():
                path = root / path
            relative = path.relative_to(root)
            if (
                ".." in relative.parts
                or relative.parent != PREFIX
                or relative.suffix not in (".yaml", ".yml")
            ):
                raise ValueError("path outside contract scope")
            text = read_text(path, max_bytes=1024 * 1024)
            # Aliases are unnecessary in this manifest surface and can hide recursive inputs.
            if any(isinstance(event, yaml.AliasEvent) for event in yaml.parse(text)):
                raise ValueError("aliases outside contract")
            for raw in yaml.safe_load_all(text):
                if raw is None:
                    continue
                count += 1
                if count > MAX_DOCUMENTS:
                    return errors + ["external-services: document count exceeds limit"]
                document = _mapping(raw)
                kind = document.get("kind")
                if kind == "Kustomization":
                    continue
                if kind not in ("Service", "EndpointSlice"):
                    raise ValueError("unexpected kind")
                metadata = _mapping(document.get("metadata"))
                name = _name(metadata.get("name"))
                namespace = _name(metadata.get("namespace", "default"))
                identity = (kind, namespace, name)
                if identity in identities:
                    raise ValueError("duplicate object identity")
                identities.add(identity)
                if kind == "Service":
                    spec = _mapping(document.get("spec"))
                    key = (namespace, name)
                    selector = spec.get("selector")
                    if "selector" in spec:
                        _mapping(selector)
                    if selector:
                        managed.add(key)
                        continue
                    services[key] = _ports(spec.get("ports"), service=True)
                else:
                    labels = _mapping(metadata.get("labels"))
                    key = (namespace, _name(labels.get("kubernetes.io/service-name")))
                    addresses = _endpoints(document)
                    slices.append((key, _ports(document.get("ports")), addresses))
        except (
            ValueError,
            TypeError,
            RecursionError,
            yaml.YAMLError,
            BoundedInputError,
            OSError,
        ):
            errors.append(
                f"{label}: invalid path, YAML, metadata, port or endpoint contract"
            )
    covered = {key: set() for key in services}
    for key, ports, addresses in slices:
        if key in managed:
            continue
        if key not in services:
            errors.append(
                "external-services: slice has no same-namespace selectorless Service"
            )
        elif not ports <= services[key]:
            errors.append(
                "external-services: slice port name, protocol or backend differs"
            )
        elif addresses:
            covered[key].update(ports)
    for key, ports in services.items():
        if covered[key] != ports:
            errors.append("external-services: Service backend coverage is incomplete")
    return list(dict.fromkeys(errors))[:MAX_FILES]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    try:
        result = run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                str(PREFIX),
            ],
            cwd=args.root,
            timeout=30,
            stdout_limit=1024 * 1024,
            stderr_limit=65536,
        )
        if result.returncode or (result.stdout and not result.stdout.endswith(b"\0")):
            raise ValueError("inventory unavailable")
        names = sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})
        paths = [Path(name) for name in names if Path(name).suffix in (".yaml", ".yml")]
        if not paths:
            raise ValueError("no contract inputs")
        errors = validate_documents(args.root, paths)
    except (OSError, ValueError, BoundedOutputError, subprocess.TimeoutExpired):
        print("[FAIL] external-service-contracts: required input or tool unavailable")
        return 1
    for error in errors:
        print(f"[FAIL] {error}")
    if not errors:
        print(
            "[PASS] external-service-contracts: static joins valid; selector-managed Services excluded"
        )
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
