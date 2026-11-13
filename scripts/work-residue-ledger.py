"""Print the work residue ledger on demand; no view is stored or committed."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections.abc import Sequence
from pathlib import Path


def _gate():
    path = Path(__file__).with_name("validate-work-residue-ledger.py")
    spec = importlib.util.spec_from_file_location("_work_residue_gate", path)
    if spec is None or spec.loader is None:
        raise ImportError("the work residue gate could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--kind")
    parser.add_argument("--state")
    parser.add_argument("--owner")
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    gate = _gate()
    try:
        entries = gate.load_ledger(Path(arguments.root).resolve())["entries"]
    except gate.LedgerError as error:
        print(f"FAIL WORK-RESIDUE {error}", file=sys.stderr)
        return 2
    wanted = {
        "kind": arguments.kind,
        "state": arguments.state,
        "owner": arguments.owner,
    }
    for entry in entries:
        if all(
            value is None or entry.get(key) == value for key, value in wanted.items()
        ):
            print(
                "\t".join(
                    (
                        entry["id"],
                        entry["kind"],
                        entry["state"],
                        entry["owner"],
                        entry["resume_condition"],
                        entry["source"]["path"],
                    )
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
