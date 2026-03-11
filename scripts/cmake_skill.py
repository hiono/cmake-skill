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
from datetime import datetime
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
    return subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, env=os.environ
    )


def parse_cmake_configure_errors(stderr: str) -> List[Diagnostic]:
    """Parses CMake configuration errors from stderr."""
    errors = []
    pattern = re.compile(r"CMake (Error|Warning) at (.*?):(\d+)")
    for line in stderr.splitlines():
        m = pattern.search(line)
        if m:
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
        errors.append(
            Diagnostic(
                file=None,
                line=None,
                column=None,
                severity="error",
                message=stderr.strip(),
            )
        )
    return errors


def parse_gcc_json_diagnostics(output: str) -> List[Diagnostic]:
    """Parses GCC/Clang JSON diagnostic format."""
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


def generate_report_md(results: Dict[str, Any]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"# CMake Automation Report ({now})", ""]

    for phase in ["configure", "build", "test"]:
        if phase not in results:
            continue
        data = results[phase]
        status = "✅ SUCCESS" if data["success"] else "❌ FAILED"
        lines.append(f"## Phase: {phase.capitalize()} ({status})")

        if data["errors"]:
            lines.append("| Severity | File | Line | Message |")
            lines.append("|---|---|---:|---|")
            for e in data["errors"]:
                file_link = f"`{e['file']}`" if e["file"] else "N/A"
                lines.append(
                    f"| {e['severity']} | {file_link} | {e['line'] or ''} | {e['message']} |"
                )
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Agent-Native CMake Specialist")
    ap.add_argument("action", choices=["configure", "build", "test", "pipeline"])
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--preset", help="CMake preset name")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--jobs", "-j", type=int, default=multiprocessing.cpu_count())
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    os.chdir(str(project_root))

    presets_file = project_root / "CMakePresets.json"
    preset = args.preset
    if not preset and presets_file.exists():
        with open(presets_file, "r") as f:
            data = json.load(f)
            preset = data.get("configurePresets", [{}])[0].get("name")

    if not preset:
        print("Error: No preset found.")
        return 1

    build_dir = project_root / "build" / preset
    if args.clean and build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    report_dir = build_dir / ".lint"
    report_dir.mkdir(exist_ok=True)

    steps = (
        ["configure", "build", "test"] if args.action == "pipeline" else [args.action]
    )
    all_results = {}
    overall_success = True

    for step in steps:
        res_data = {"success": False, "errors": []}
        if step == "configure":
            cmd = [
                "cmake",
                "-S",
                str(project_root),
                "-B",
                str(build_dir),
                f"--preset={preset}",
                "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
            ]
            process = run_cmd(cmd, project_root)
            res_data["success"] = process.returncode == 0
            if not res_data["success"]:
                res_data["errors"] = [
                    asdict(d) for d in parse_cmake_configure_errors(process.stderr)
                ]

        elif step == "build":
            cmd = ["cmake", "--build", str(build_dir), "--parallel", str(args.jobs)]
            process = run_cmd(cmd, project_root)
            res_data["success"] = process.returncode == 0
            if not res_data["success"]:
                compiler_errors = parse_gcc_json_diagnostics(process.stderr)
                if not compiler_errors:
                    compiler_errors = [
                        Diagnostic(
                            file=None,
                            line=None,
                            column=None,
                            severity="error",
                            message=process.stderr,
                        )
                    ]
                res_data["errors"] = [asdict(d) for d in compiler_errors]

        elif step == "test":
            cmd = [
                "ctest",
                "--test-dir",
                str(build_dir),
                "--preset",
                preset,
                "-j",
                str(args.jobs),
                "--output-on-failure",
            ]
            process = run_cmd(cmd, project_root)
            res_data["success"] = process.returncode == 0
            if not res_data["success"]:
                res_data["errors"].append(
                    asdict(
                        Diagnostic(
                            file="CTest",
                            line=None,
                            column=None,
                            severity="error",
                            message=process.stdout + process.stderr,
                        )
                    )
                )

        all_results[step] = res_data
        if not res_data["success"]:
            overall_success = False
            break

    report_md = generate_report_md(all_results)
    (project_root / "cmake_report.md").write_text(report_md)

    report_json = report_dir / "report.json"
    report_json.write_text(json.dumps(all_results, indent=2, ensure_ascii=False))

    # Final concise output for Token efficiency
    total_errors = sum(len(v["errors"]) for v in all_results.values())
    summary = {
        "quick_ref": {
            "success": overall_success,
            "total_errors": total_errors,
            "steps": {k: ("SUCCESS" if v["success"] else "FAILED") for k, v in all_results.items()},
        },
        "artifacts": {
            "human_report": str(project_root / "cmake_report.md"),
            "machine_report": str(report_json.resolve()),
        },
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if overall_success else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
