"""Bounded protected QA records; main verdicts never become PR reuse sources."""

from dataclasses import dataclass
from datetime import datetime
import json
import re

PROOF_LIMIT = 16 * 1024
CI_PATH = ".github/workflows/ci.yml"


@dataclass(frozen=True)
class Proof:
    record: dict


@dataclass(frozen=True)
class MainVerdict:
    record: dict


@dataclass(frozen=True)
class Reject:
    reason: str


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(value):
    require(
        isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value),
        "invalid Git identity",
    )
    return value


def positive(value):
    require(type(value) is int and 0 < value < 2**63, "invalid provider ID")
    return value


def fresh(value, now):
    require(
        isinstance(value, str) and re.fullmatch(r"[0-9-]{10}T[0-9:]{8}Z", value),
        "invalid timestamp",
    )
    age = (now - datetime.fromisoformat(value.replace("Z", "+00:00"))).total_seconds()
    require(0 <= age <= 30 * 86400, "proof is expired or from the future")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def decode(payload, limit):
    require(
        isinstance(payload, bytes) and len(payload) <= limit, "JSON byte limit exceeded"
    )
    return json.loads(payload, object_pairs_hook=unique_object)


def encode_proof(proof):
    payload = json.dumps(proof.record, sort_keys=True, separators=(",", ":"))
    require(len(payload.encode()) <= PROOF_LIMIT, "proof byte limit exceeded")
    return payload


def parse_record(payload, *, main, now):
    record = decode(payload, PROOF_LIMIT)
    require(
        set(record)
        == {
            "version",
            "repository",
            "checkout",
            "workflow",
            "source",
            "registry",
            "tools",
            "gates",
            "completed_at",
        }
        | ({"event", "ref", "control"} if main else {"pr", "base", "head"}),
        "invalid proof fields",
    )
    require(
        type(record["version"]) is int and record["version"] == (2 if main else 1),
        "unsupported proof version",
    )
    repository = record["repository"]
    require(
        set(repository) == {"id", "name"}
        and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository["name"]),
        "invalid repository",
    )
    positive(repository["id"])
    sha(record["registry"])
    if main:
        require(
            record["event"] == "push" and record["ref"] == "refs/heads/main",
            "not a main push",
        )
        sha(record["control"])
    else:
        positive(record["pr"])
        sha(record["base"])
        sha(record["head"])
    require(set(record["checkout"]) == {"commit", "tree"}, "invalid checkout")
    for value in record["checkout"].values():
        sha(value)
    require(
        set(record["workflow"]) == {"id", "path", "revision", "blob"},
        "invalid workflow",
    )
    positive(record["workflow"]["id"])
    require(record["workflow"]["path"] == CI_PATH, "wrong workflow")
    sha(record["workflow"]["revision"])
    sha(record["workflow"]["blob"])
    require(set(record["source"]) == {"run", "attempt", "job"}, "invalid source")
    for value in record["source"].values():
        positive(value)
    require(
        set(record["tools"]) == {"lock", "runtime"}
        and record["tools"]["runtime"] == "unattested",
        "invalid tools",
    )
    sha(record["tools"]["lock"])
    gates = record["gates"]
    require(isinstance(gates, dict) and 0 < len(gates) <= 128, "invalid gates")
    for name, disposition in gates.items():
        require(
            re.fullmatch(r"[a-z][a-z0-9-]{0,127}", name) and disposition == "PASS",
            "incomplete gate",
        )
    fresh(record["completed_at"], now)
    return MainVerdict(record) if main else Proof(record)
