#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import multiprocessing
import os
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Diagnostic:
    file: Optional[str]
    line: Optional[int]
    column: Optional[int]
    severity: str
    message: str
    check: str = "cmake-build"


def run_cmd(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    """Helper to run shell commands with full environment."""
    return subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, env=os.environ
    )


def parse_cmake_errors(stderr: str) -> List[Diagnostic]:
    """Parses CMake configuration errors."""
    errors = []
    pattern = re.compile(r"CMake (Error|Warning) at (.*?):(\d+)")
    for line in stderr.splitlines():
        if m := pattern.search(line):
            errors.append(
                Diagnostic(
                    file=m.group(2),
                    line=int(m.group(3)),
                    column=0,
                    severity=m.group(1).lower(),
                    message=line.strip(),
                )
            )
    if not errors and stderr.strip():
        errors.append(Diagnostic(None, None, None, "error", stderr.strip()))
    return errors


def parse_compiler_json(output: str) -> List[Diagnostic]:
    """Parses GCC/Clang JSON diagnostics."""
    diags = []
    try:
        data = json.loads(output)
        items = data if isinstance(data, list) else data.get("diagnostics", [])
        for item in items:
            for loc in item.get("locations", []):
                caret = loc.get("caret", {})
                diags.append(
                    Diagnostic(
                        file=caret.get("file"),
                        line=caret.get("line"),
                        column=caret.get("column"),
                        severity=item.get("kind", "error"),
                        message=item.get("message", ""),
                        check=item.get("option", "compiler"),
                    )
                )
    except Exception:
        pass
    return diags


def configure_project(root: Path, build_dir: Path, preset: str) -> Dict[str, Any]:
    cmd = [
        "cmake",
        "-S",
        str(root),
        "-B",
        str(build_dir),
        f"--preset={preset}",
        "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
    ]
    res = run_cmd(cmd, root)
    return {
        "success": res.returncode == 0,
        "errors": [asdict(d) for d in parse_cmake_errors(res.stderr)],
    }
def build_project(root: Path, build_dir: Path, jobs: int, targets: List[str]) -> Dict[str, Any]:
    cmd = ["cmake", "--build", str(build_dir), "--parallel", str(jobs)]
    for t in targets:
        cmd.extend(["--target", t])
    res = run_cmd(cmd, root)
    success = res.returncode == 0

    # Combined output for parsing
    output = res.stdout + res.stderr
    errors = [asdict(d) for d in parse_compiler_json(output)] if not success else []

    if not success and not errors:
        errors = [asdict(Diagnostic(None, None, None, "error", output))]
    return {"success": success, "errors": errors}


def test_project(root: Path, build_dir: Path, preset: str, jobs: int) -> Dict[str, Any]:
    cmd = [
        "ctest",
        "--test-dir",
        str(build_dir),
        "--preset",
        preset,
        "-j",
        str(jobs),
        "--output-on-failure",
    ]
    res = run_cmd(cmd, root)
    success = res.returncode == 0
    errors = (
        [asdict(Diagnostic("CTest", None, None, "error", res.stdout + res.stderr))]
        if not success
        else []
    )
    return {"success": success, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser(description="Agent-Native CMake Specialist")
    ap.add_argument(
        "action", choices=["configure", "build", "test", "list", "pipeline"]
    )
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--preset", help="CMake preset name")
    ap.add_argument("--target", action="append", default=[])
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--jobs", "-j", type=int, default=multiprocessing.cpu_count())
    ap.add_argument("--output-dir", default=".lint")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    os.chdir(str(root))

    if args.action == "list":
        p_file = root / "CMakePresets.json"
        print(
            json.dumps(
                json.loads(p_file.read_text()).get("configurePresets", [])
                if p_file.exists()
                else [],
                indent=2,
            )
        )
        return 0

    preset = args.preset
    p_file = root / "CMakePresets.json"
    if not preset and p_file.exists():
        preset = (
            json.loads(p_file.read_text()).get("configurePresets", [{}])[0].get("name")
        )

    if not preset:
        print(json.dumps({"error": "No preset found"}, indent=2))
        return 1

    build_dir = root / "build" / preset
    if args.clean and build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    report_dir = build_dir / args.output_dir
    report_dir.mkdir(exist_ok=True)

    steps = (
        ["configure", "build", "test"] if args.action == "pipeline" else [args.action]
    )
    all_results = {}
    overall_success = True

    for step in steps:
        if step == "configure":
            res = configure_project(root, build_dir, preset)
        elif step == "build":
            res = build_project(root, build_dir, args.jobs, args.target)
        else:
            res = test_project(root, build_dir, preset, args.jobs)

        all_results[step] = res
        if not res["success"]:
            overall_success = False
            break

    # Save structured report
    rep_json = report_dir / "cmake_report.json"
    rep_json.write_text(json.dumps(all_results, indent=2, ensure_ascii=False))

    # Token-efficient summary
    summary = {
        "quick_ref": {
            "success": overall_success,
            "steps": {k: ("SUCCESS" if v["success"] else "FAILED") for k, v in all_results.items()},
        },
        "artifacts": {
            "human_report": str(root / "cmake_report.md"),
            "machine_report": str(rep_json.resolve()),
        },
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if overall_success else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
