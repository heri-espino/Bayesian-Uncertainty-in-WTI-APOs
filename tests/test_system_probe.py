import json

from scripts.system_probe import _format_bytes, write_reports


def test_format_bytes():
    assert _format_bytes(1024) == "1.00 KiB"
    assert _format_bytes(1024**3) == "1.00 GiB"
    assert _format_bytes(None) is None


def test_write_reports_creates_timestamped_and_latest_files(tmp_path):
    report = {
        "schema_version": 1,
        "generated_at_utc": "2026-09-09T12:00:00+00:00",
        "system": {"hostname": "test-host", "platform": "test", "architecture": "x86_64"},
        "hardware": {
            "psutil": {"cpu": {}, "memory": {}, "disks": []},
            "fallback_repository_disk": {},
            "nvidia": {"available": False, "gpus": []},
        },
        "software": {
            "python_version": "3.11",
            "conda": {},
            "cupy": {},
            "packages": {},
        },
        "git": {"commit": "abc", "branch": "main", "dirty": False},
    }

    paths = write_reports(report, tmp_path)

    assert all(path.exists() for path in paths.values())
    loaded = json.loads(paths["latest_json"].read_text(encoding="utf-8"))
    assert loaded["system"]["hostname"] == "test-host"
    assert "Workstation reproducibility report" in paths["latest_text"].read_text(
        encoding="utf-8"
    )
