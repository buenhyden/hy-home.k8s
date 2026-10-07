"""Derive the sample-app YAML copy set from its Kustomization."""

import re
from collections.abc import Mapping


YAML_NAME = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.yaml\Z")
OPTIONAL_RESOURCE = re.compile(r"^  # - (?P<name>\S+)\s*$")


def sample_app_yaml_filenames(kustomization: Mapping, source: str) -> set[str]:
    """Return files that a copy of this sample may carry as YAML."""
    resources = kustomization.get("resources")
    if not isinstance(resources, list) or not resources:
        raise ValueError("sample-app resources must be a non-empty YAML list")
    active: set[str] = set()
    for resource in resources:
        if not isinstance(resource, str) or not YAML_NAME.fullmatch(resource):
            raise ValueError("sample-app resource must be a direct YAML filename")
        if resource in active or resource == "kustomization.yaml":
            raise ValueError("sample-app resource is repeated")
        active.add(resource)

    optional: set[str] = set()
    inside_resources = False
    for line in source.splitlines():
        if line == "resources:":
            inside_resources = True
            continue
        if inside_resources and line and not line[0].isspace():
            inside_resources = False
        if not inside_resources:
            continue
        match = OPTIONAL_RESOURCE.fullmatch(line)
        if match is None:
            continue
        name = match.group("name")
        if not YAML_NAME.fullmatch(name) or name in active or name in optional:
            raise ValueError("sample-app optional resource is invalid or repeated")
        optional.add(name)
    return {"kustomization.yaml", *active, *optional}


def sample_app_copyset_errors(
    actual_yaml_names: set[str], kustomization: Mapping, source: str
) -> list[str]:
    try:
        declared = sample_app_yaml_filenames(kustomization, source)
    except ValueError as exc:
        return [str(exc)]
    if actual_yaml_names != declared:
        return ["sample-app YAML copy set differs from Kustomization declaration"]
    return []
