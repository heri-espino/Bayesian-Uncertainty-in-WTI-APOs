"""Unit tests use synthetic files: never vendor market data."""
import hashlib
import json
from pathlib import Path

from scripts.audit_aao_manifests import audit


def fixture(tmp_path: Path):
    raw = tmp_path / "raw"
    raw.mkdir()
    ledgers = []
    for start, end in (("2020-01-01", "2020-02-01"),
                       ("2020-02-01", "2020-03-01")):
        completed = {}
        for schema in ("definition", "statistics"):
            name = f"aao_{schema}__{start}__{end}.dbn.zst"
            data = name.encode()
            (raw / name).write_bytes(data)
            completed[f"{schema}__{start}__{end}"] = {
                "file": name, "schema": schema, "start": start, "end": end,
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(), "quote_usd": .05,
            }
        ledger = tmp_path / f"{start}.json"
        ledger.write_text(json.dumps({
            "dataset": "GLBX.MDP3", "parent": "AAO.OPT",
            "completed_all_eligible": True, "completed": completed,
        }))
        ledgers.append(ledger)
    return raw, ledgers


def check(raw, ledgers):
    return audit(raw, ledgers, start="2020-01-01", end="2020-03-01")


def test_combined_success(tmp_path):
    raw, ledgers = fixture(tmp_path)
    result = check(raw, ledgers)
    assert result["success"]
    assert result["files_verified"] == 4
    assert result["month_count"] == 2
    assert result["combined_quoted_usd"] == .2


def test_corrupted_file(tmp_path):
    raw, ledgers = fixture(tmp_path)
    path = next(raw.glob("*.dbn.zst"))
    path.write_bytes(b"X" * path.stat().st_size)
    assert any("checksum_mismatch" in x for x in check(raw, ledgers)["issues"])


def test_missing_file(tmp_path):
    raw, ledgers = fixture(tmp_path)
    next(raw.glob("*.dbn.zst")).unlink()
    assert any("missing_file" in x for x in check(raw, ledgers)["issues"])


def test_duplicate_entry(tmp_path):
    raw, ledgers = fixture(tmp_path)
    assert any("duplicate_chunk" in x
               for x in check(raw, ledgers + ledgers)["issues"])


def test_missing_month(tmp_path):
    raw, ledgers = fixture(tmp_path)
    assert any("missing_schema" in x
               for x in check(raw, ledgers[:1])["issues"])


def test_untracked_file(tmp_path):
    raw, ledgers = fixture(tmp_path)
    (raw / "aao_statistics__2021-01-01__2021-02-01.dbn.zst").write_bytes(b"x")
    assert any("untracked_files" in x for x in check(raw, ledgers)["issues"])
