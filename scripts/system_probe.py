"""Collect reproducibility-relevant workstation specifications.

The probe is designed for restricted university/workstation environments. It does not
require administrator privileges and degrades gracefully when optional tools such as
``nvidia-smi``, CuPy, or psutil are unavailable.

By default it writes both timestamped and ``latest`` JSON/text reports under
``results/system`` relative to the repository root.

Examples
--------
From an activated Conda environment::

    python -m scripts.system_probe

Without activating the environment::

    conda run -n asian-options python -m scripts.system_probe
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "results" / "system"


def _run(command: list[str], *, cwd: Path | None = None) -> dict[str, Any]:
    """Run a read-only command and return structured success/error information."""
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": repr(exc), "stdout": None}

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    return {
        "available": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": stdout or None,
        "stderr": stderr or None,
    }


def _format_bytes(value: int | float | None) -> str | None:
    if value is None:
        return None
    size = float(value)
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    for unit in units:
        if abs(size) < 1024.0 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TiB"


def _package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _cpu_model() -> str | None:
    model = platform.processor().strip()
    if model:
        return model

    if platform.system() == "Windows":
        result = _run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name)",
            ]
        )
        if result.get("available") and result.get("stdout"):
            return str(result["stdout"]).strip()

    if platform.system() == "Linux":
        try:
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return None


def _psutil_snapshot() -> dict[str, Any]:
    try:
        import psutil  # type: ignore
    except Exception as exc:
        return {"available": False, "error": repr(exc)}

    result: dict[str, Any] = {"available": True, "version": getattr(psutil, "__version__", None)}

    try:
        freq = psutil.cpu_freq()
        result["cpu"] = {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "frequency_mhz_current": None if freq is None else freq.current,
            "frequency_mhz_min": None if freq is None else freq.min,
            "frequency_mhz_max": None if freq is None else freq.max,
        }
    except Exception as exc:
        result["cpu"] = {"error": repr(exc)}

    try:
        vm = psutil.virtual_memory()
        result["memory"] = {
            "total_bytes": int(vm.total),
            "total_human": _format_bytes(vm.total),
            "available_bytes": int(vm.available),
            "available_human": _format_bytes(vm.available),
        }
    except Exception as exc:
        result["memory"] = {"error": repr(exc)}

    disks: list[dict[str, Any]] = []
    seen: set[str] = set()
    try:
        for partition in psutil.disk_partitions(all=False):
            mountpoint = partition.mountpoint
            if mountpoint in seen:
                continue
            seen.add(mountpoint)
            try:
                usage = psutil.disk_usage(mountpoint)
            except (OSError, PermissionError):
                continue
            disks.append(
                {
                    "device": partition.device,
                    "mountpoint": mountpoint,
                    "filesystem": partition.fstype,
                    "total_bytes": int(usage.total),
                    "total_human": _format_bytes(usage.total),
                    "free_bytes": int(usage.free),
                    "free_human": _format_bytes(usage.free),
                }
            )
    except Exception as exc:
        result["disk_error"] = repr(exc)
    result["disks"] = disks
    return result


def _fallback_disk() -> dict[str, Any]:
    try:
        usage = shutil.disk_usage(REPO_ROOT)
        return {
            "path": str(REPO_ROOT),
            "total_bytes": int(usage.total),
            "total_human": _format_bytes(usage.total),
            "free_bytes": int(usage.free),
            "free_human": _format_bytes(usage.free),
        }
    except OSError as exc:
        return {"error": repr(exc)}


def _nvidia_snapshot() -> dict[str, Any]:
    query = _run(
        [
            "nvidia-smi",
            "--query-gpu=index,name,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    if not query.get("available"):
        return {
            "available": False,
            "error": query.get("error") or query.get("stderr") or "nvidia-smi unavailable",
        }

    gpus: list[dict[str, Any]] = []
    for line in str(query.get("stdout") or "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 4:
            continue
        try:
            memory_mib: float | None = float(parts[2])
        except ValueError:
            memory_mib = None
        gpus.append(
            {
                "index": parts[0],
                "name": parts[1],
                "memory_total_mib": memory_mib,
                "memory_total_human": None if memory_mib is None else _format_bytes(memory_mib * 1024**2),
                "driver_version": parts[3],
            }
        )

    full = _run(["nvidia-smi"])
    cuda_version = None
    if full.get("stdout"):
        match = re.search(r"CUDA Version:\s*([0-9.]+)", str(full["stdout"]))
        if match:
            cuda_version = match.group(1)

    return {
        "available": True,
        "cuda_version_reported_by_driver": cuda_version,
        "gpus": gpus,
    }


def _cupy_snapshot() -> dict[str, Any]:
    try:
        import cupy as cp  # type: ignore
    except Exception as exc:
        return {
            "installed": _package_version("cupy") is not None,
            "usable": False,
            "version": _package_version("cupy"),
            "error": repr(exc),
        }

    result: dict[str, Any] = {
        "installed": True,
        "usable": False,
        "version": getattr(cp, "__version__", _package_version("cupy")),
    }
    try:
        count = int(cp.cuda.runtime.getDeviceCount())
        result["device_count"] = count
        result["cuda_runtime_version"] = int(cp.cuda.runtime.runtimeGetVersion())
        result["cuda_driver_version"] = int(cp.cuda.runtime.driverGetVersion())
        devices: list[dict[str, Any]] = []
        for index in range(count):
            props = cp.cuda.runtime.getDeviceProperties(index)
            raw_name = props.get("name") if isinstance(props, dict) else None
            if isinstance(raw_name, bytes):
                name = raw_name.decode(errors="replace")
            else:
                name = str(raw_name) if raw_name is not None else None
            devices.append(
                {
                    "index": index,
                    "name": name,
                    "compute_capability": (
                        f"{props.get('major')}.{props.get('minor')}"
                        if isinstance(props, dict)
                        and props.get("major") is not None
                        and props.get("minor") is not None
                        else None
                    ),
                    "total_global_memory_bytes": (
                        int(props.get("totalGlobalMem"))
                        if isinstance(props, dict) and props.get("totalGlobalMem") is not None
                        else None
                    ),
                    "total_global_memory_human": (
                        _format_bytes(int(props.get("totalGlobalMem")))
                        if isinstance(props, dict) and props.get("totalGlobalMem") is not None
                        else None
                    ),
                }
            )
        result["devices"] = devices
        result["usable"] = count > 0
    except Exception as exc:
        result["error"] = repr(exc)
    return result


def _git_snapshot() -> dict[str, Any]:
    commit = _run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
    branch = _run(["git", "branch", "--show-current"], cwd=REPO_ROOT)
    status = _run(["git", "status", "--porcelain"], cwd=REPO_ROOT)
    return {
        "commit": commit.get("stdout") if commit.get("available") else None,
        "branch": branch.get("stdout") if branch.get("available") else None,
        "dirty": bool(status.get("stdout")) if status.get("available") else None,
    }


def _conda_snapshot() -> dict[str, Any]:
    version = _run(["conda", "--version"])
    return {
        "active_environment": os.environ.get("CONDA_DEFAULT_ENV"),
        "prefix": os.environ.get("CONDA_PREFIX"),
        "conda_version": version.get("stdout") if version.get("available") else None,
        "available": bool(version.get("available")),
        "error": None if version.get("available") else version.get("error") or version.get("stderr"),
    }


def collect_report() -> dict[str, Any]:
    """Collect a JSON-serializable workstation/reproducibility report."""
    psutil_info = _psutil_snapshot()
    return {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(REPO_ROOT),
        "system": {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "operating_system": platform.system(),
            "operating_system_release": platform.release(),
            "architecture": platform.machine(),
            "cpu_model": _cpu_model(),
            "logical_cpu_count_stdlib": os.cpu_count(),
        },
        "hardware": {
            "psutil": psutil_info,
            "fallback_repository_disk": _fallback_disk(),
            "nvidia": _nvidia_snapshot(),
        },
        "software": {
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "packages": {
                name: _package_version(name)
                for name in ("numpy", "pandas", "scipy", "matplotlib", "pytest", "psutil", "cupy")
            },
            "conda": _conda_snapshot(),
            "cupy": _cupy_snapshot(),
        },
        "git": _git_snapshot(),
    }


def _human_report(report: dict[str, Any]) -> str:
    system = report.get("system", {})
    hardware = report.get("hardware", {})
    software = report.get("software", {})
    psutil_info = hardware.get("psutil", {})
    cpu = psutil_info.get("cpu", {}) if isinstance(psutil_info, dict) else {}
    memory = psutil_info.get("memory", {}) if isinstance(psutil_info, dict) else {}
    nvidia = hardware.get("nvidia", {})
    conda = software.get("conda", {})
    cupy = software.get("cupy", {})

    lines = [
        "Workstation reproducibility report",
        "==================================",
        f"Generated UTC: {report.get('generated_at_utc')}",
        f"Hostname: {system.get('hostname')}",
        f"OS: {system.get('platform')}",
        f"Architecture: {system.get('architecture')}",
        f"CPU: {system.get('cpu_model')}",
        f"Physical cores: {cpu.get('physical_cores')}",
        f"Logical cores: {cpu.get('logical_cores') or system.get('logical_cpu_count_stdlib')}",
        f"RAM total: {memory.get('total_human')}",
        f"Python: {software.get('python_version')}",
        f"Conda environment: {conda.get('active_environment')}",
        f"Git commit: {report.get('git', {}).get('commit')}",
        f"Git branch: {report.get('git', {}).get('branch')}",
        f"Git dirty: {report.get('git', {}).get('dirty')}",
        "",
        "NVIDIA",
        "------",
        f"nvidia-smi available: {nvidia.get('available')}",
        f"CUDA reported by driver: {nvidia.get('cuda_version_reported_by_driver')}",
    ]
    for gpu in nvidia.get("gpus", []) if isinstance(nvidia, dict) else []:
        lines.append(
            f"GPU {gpu.get('index')}: {gpu.get('name')} | VRAM {gpu.get('memory_total_human')} | driver {gpu.get('driver_version')}"
        )
    if not nvidia.get("available"):
        lines.append(f"NVIDIA error: {nvidia.get('error')}")

    lines.extend(
        [
            "",
            "CuPy",
            "----",
            f"Installed: {cupy.get('installed')}",
            f"Usable: {cupy.get('usable')}",
            f"Version: {cupy.get('version')}",
            f"CUDA runtime version: {cupy.get('cuda_runtime_version')}",
            f"CUDA driver version: {cupy.get('cuda_driver_version')}",
        ]
    )
    if cupy.get("error"):
        lines.append(f"CuPy error: {cupy.get('error')}")

    disks = psutil_info.get("disks", []) if isinstance(psutil_info, dict) else []
    lines.extend(["", "Disks", "-----"])
    if disks:
        for disk in disks:
            lines.append(
                f"{disk.get('device')} at {disk.get('mountpoint')}: total {disk.get('total_human')}, free {disk.get('free_human')}"
            )
    else:
        fallback = hardware.get("fallback_repository_disk", {})
        lines.append(
            f"Repository disk: total {fallback.get('total_human')}, free {fallback.get('free_human')}"
        )

    lines.extend(["", "Package versions", "----------------"])
    for name, version in software.get("packages", {}).items():
        lines.append(f"{name}: {version}")

    lines.append("")
    return "\n".join(lines)


def write_reports(report: dict[str, Any], output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Path]:
    """Write timestamped and latest JSON/text reports and return their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = str(report.get("generated_at_utc") or datetime.now(timezone.utc).isoformat())
    stamp = re.sub(r"[^0-9A-Za-z]", "", timestamp.replace("+00:00", "Z"))
    json_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    human_text = _human_report(report)

    paths = {
        "timestamped_json": output_dir / f"hardware_report_{stamp}.json",
        "timestamped_text": output_dir / f"hardware_report_{stamp}.txt",
        "latest_json": output_dir / "hardware_report_latest.json",
        "latest_text": output_dir / "hardware_report_latest.txt",
    }
    for key in ("timestamped_json", "latest_json"):
        paths[key].write_text(json_text, encoding="utf-8")
    for key in ("timestamped_text", "latest_text"):
        paths[key].write_text(human_text, encoding="utf-8")
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for timestamped and latest reports.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also print the complete JSON report to stdout.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = collect_report()
    paths = write_reports(report, args.output_dir)
    print(_human_report(report))
    print("Reports written:")
    for path in paths.values():
        print(f"  {path}")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
