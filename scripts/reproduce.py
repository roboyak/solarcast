"""Small command runner for reproducing the SolarCast notebook.

Examples:
    python scripts/reproduce.py smoke
    python scripts/reproduce.py notebook
    python scripts/reproduce.py fetch-openmeteo
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> int:
    print("+", " ".join(args), flush=True)
    return subprocess.call(args, cwd=REPO_ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="SolarCast reproducibility helper")
    parser.add_argument(
        "command",
        choices=["smoke", "notebook", "fetch-openmeteo", "fetch-nsrdb"],
        help="Task to run",
    )
    ns = parser.parse_args()

    if ns.command == "smoke":
        return run([sys.executable, "scripts/smoke_check.py"])
    if ns.command == "notebook":
        return run([
            sys.executable,
            "-m",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "Solar_PV_Forecasting.ipynb",
            "--output",
            "Solar_PV_Forecasting.executed.ipynb",
            "--ExecutePreprocessor.timeout=900",
        ])
    if ns.command == "fetch-openmeteo":
        return run([sys.executable, "scripts/fetch_openmeteo.py"])
    if ns.command == "fetch-nsrdb":
        return run([sys.executable, "scripts/fetch_nsrdb.py"])
    raise AssertionError(f"Unhandled command: {ns.command}")


if __name__ == "__main__":
    raise SystemExit(main())
