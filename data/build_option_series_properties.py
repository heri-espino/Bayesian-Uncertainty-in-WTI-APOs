"""Profile every Average Price option CSV and rank the richest series.

Run from the directory that contains the ``csv`` and ``md_original`` folders:
    python build_option_series_properties.py

Outputs:
  - option_series_properties.csv: one row per contract series, sorted by score
  - richest_option_series.csv: the 30 series with the most complete data
"""

from __future__ import annotations

import csv
import math
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import fmean, pstdev


HEADERS = ["Time", "Open", "High", "Low", "Latest", "Change", "%Change", "Volume", "Open Int"]
FILENAME = re.compile(
    r"^(?P<root>jao[a-z]\d)_(?P<strike>\d+)(?P<right>[cp])_price-history-\d{2}-\d{2}-\d{4}\.csv$",
    re.IGNORECASE,
)
MONTHS = {"F": 1, "G": 2, "H": 3, "J": 4, "K": 5, "M": 6, "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12}


def number(value: str) -> float | None:
    value = value.strip().replace(",", "")
    if not value or value.casefold() in {"n/a", "na", "unch", "-"}:
        return None
    if value.endswith("%"):
        value = value[:-1]
    try:
        return float(value)
    except ValueError:
        return None


def mean_or_blank(values: list[float]) -> str:
    return f"{fmean(values):.6g}" if values else ""


def std_or_blank(values: list[float]) -> str:
    return f"{pstdev(values):.6g}" if len(values) > 1 else ""


def percent(part: int | float, whole: int | float) -> float:
    return 100 * part / whole if whole else 0.0


def expiration(root: str) -> str:
    code = root.upper()
    month = MONTHS[code[-2]]
    year = 2020 + int(code[-1])
    return date(year, month, 1).strftime("%Y-%m")


def source_contracts(folder: Path) -> set[str]:
    pattern = re.compile(r"\(([A-Za-z0-9]+)\|(\d+)([CP])\)")
    values: set[str] = set()
    for page in folder.glob("*.md"):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for root, strike, right in pattern.findall(text):
            values.add(f"{root.lower()}_{strike}{right.lower()}")
    return values


def profile(path: Path, sources: set[str]) -> dict[str, object] | None:
    match = FILENAME.fullmatch(path.name)
    if match is None:
        return None
    with path.open(encoding="utf-8-sig", newline="") as stream:
        table = list(csv.DictReader(stream))
    if not table or list(table[0].keys()) != HEADERS:
        return None

    rows = []
    for row in table:
        if set(row) != set(HEADERS):
            continue
        try:
            row["_date"] = date.fromisoformat(row["Time"])
        except ValueError:
            continue
        rows.append(row)
    if not rows:
        return None
    rows.sort(key=lambda row: row["_date"])
    open_values = [number(row["Open"]) for row in rows]
    high_values = [number(row["High"]) for row in rows]
    low_values = [number(row["Low"]) for row in rows]
    latest = [number(row["Latest"]) for row in rows]
    latest_values = [value for value in latest if value is not None]
    changes = [number(row["Change"]) for row in rows]
    change_values = [value for value in changes if value is not None]
    pct_changes = [number(row["%Change"]) for row in rows]
    pct_change_values = [value for value in pct_changes if value is not None]
    volumes = [number(row["Volume"]) for row in rows]
    volume_values = [value for value in volumes if value is not None]
    interests = [number(row["Open Int"]) for row in rows]
    interest_values = [value for value in interests if value is not None]
    measured_columns = [open_values, high_values, low_values, latest, changes, pct_changes, volumes, interests]
    observed_cells = sum(sum(value is not None for value in column) for column in measured_columns)
    available_fields = sum(any(value is not None for value in column) for column in measured_columns)
    root = match.group("root").lower()
    strike_code = match.group("strike")
    right = match.group("right").lower()
    contract = f"{root}_{strike_code}{right}"
    first, last = rows[0]["_date"], rows[-1]["_date"]
    return {
        "folder": path.parent.name,
        "csv_file": path.name,
        "contract": contract,
        "root_symbol": root.upper(),
        "expiration": expiration(root),
        "right": "call" if right == "c" else "put",
        "strike": f"{int(strike_code) / 100:.2f}",
        "strike_code": strike_code,
        "has_source_page": "yes" if contract in sources else "no",
        "first_date": first.isoformat(),
        "last_date": last.isoformat(),
        "calendar_days": (last - first).days + 1,
        "sessions": len(rows),
        "open_observations": sum(value is not None for value in open_values),
        "high_observations": sum(value is not None for value in high_values),
        "low_observations": sum(value is not None for value in low_values),
        "price_observations": len(latest_values),
        "price_completeness_pct": percent(len(latest_values), len(rows)),
        "available_measurement_fields": available_fields,
        "measurement_field_count": len(measured_columns),
        "measurement_completeness_pct": percent(observed_cells, len(rows) * len(measured_columns)),
        "nonzero_price_sessions": sum(value != 0 for value in latest_values),
        "first_latest": f"{latest_values[0]:.6g}" if latest_values else "",
        "last_latest": f"{latest_values[-1]:.6g}" if latest_values else "",
        "min_latest": f"{min(latest_values):.6g}" if latest_values else "",
        "max_latest": f"{max(latest_values):.6g}" if latest_values else "",
        "mean_latest": mean_or_blank(latest_values),
        "std_latest": std_or_blank(latest_values),
        "change_observations": len(change_values),
        "mean_absolute_change": mean_or_blank([abs(value) for value in change_values]),
        "pct_change_observations": len(pct_change_values),
        "mean_absolute_pct_change": mean_or_blank([abs(value) for value in pct_change_values]),
        "volume_observations": len(volume_values),
        "nonzero_volume_sessions": sum(value > 0 for value in volume_values),
        "nonzero_volume_pct": percent(sum(value > 0 for value in volume_values), len(rows)),
        "total_volume": f"{sum(volume_values):.6g}" if volume_values else "",
        "mean_volume": mean_or_blank(volume_values),
        "max_volume": f"{max(volume_values):.6g}" if volume_values else "",
        "open_interest_observations": len(interest_values),
        "nonzero_open_interest_sessions": sum(value > 0 for value in interest_values),
        "nonzero_open_interest_pct": percent(sum(value > 0 for value in interest_values), len(rows)),
        "last_open_interest": f"{interest_values[-1]:.6g}" if interest_values else "",
        "max_open_interest": f"{max(interest_values):.6g}" if interest_values else "",
        "mean_open_interest": mean_or_blank(interest_values),
    }


def main() -> None:
    csv_root = Path("csv")
    md_root = Path("md_original")
    if not csv_root.is_dir():
        raise SystemExit("CSV root folder not found: csv")
    profiles: list[dict[str, object]] = []
    for folder in sorted(path for path in csv_root.iterdir() if path.is_dir()):
        source_folder = md_root / folder.name
        sources = source_contracts(source_folder) if source_folder.is_dir() else set()
        for csv_path in folder.glob("*.csv"):
            item = profile(csv_path, sources)
            if item is not None:
                profiles.append(item)
    if not profiles:
        raise SystemExit("No valid option history CSV files found.")

    # The same contract can appear more than once when it was downloaded on
    # different days. Keep the richest version, but preserve that provenance.
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in profiles:
        grouped[str(item["contract"])].append(item)
    profiles = []
    for contract, candidates in grouped.items():
        candidates.sort(key=lambda item: (int(item["sessions"]), str(item["last_date"]), str(item["csv_file"])), reverse=True)
        chosen = candidates[0]
        chosen["source_csv_files"] = "; ".join(str(item["csv_file"]) for item in candidates)
        chosen["source_csv_count"] = len(candidates)
        profiles.append(chosen)

    max_sessions = max(int(item["sessions"]) for item in profiles)
    max_span = max(int(item["calendar_days"]) for item in profiles)
    for item in profiles:
        # This is a data-richness score, not a liquidity or investment score.
        # It rewards more sessions, a longer observed time span, and the
        # proportion of all eight numerical fields that are actually present.
        score = (
            45 * int(item["sessions"]) / max_sessions
            + 30 * int(item["calendar_days"]) / max_span
            + 25 * float(item["measurement_completeness_pct"]) / 100
        )
        item["information_score"] = round(score, 2)
        item["information_tier"] = "rich" if score >= 70 else "moderate" if score >= 40 else "limited"
        item["information_score_definition"] = "45% session count + 30% calendar span + 25% numeric-field completeness"
    profiles.sort(key=lambda item: (-float(item["information_score"]), -int(item["sessions"]), item["contract"]))
    for rank, item in enumerate(profiles, start=1):
        item["information_rank"] = rank

    fields = list(profiles[0].keys())
    for target, rows in ((csv_root / "option_series_properties.csv", profiles), (csv_root / "richest_option_series.csv", profiles[:30])):
        with target.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Created: {target} ({len(rows)} series)")


if __name__ == "__main__":
    main()
