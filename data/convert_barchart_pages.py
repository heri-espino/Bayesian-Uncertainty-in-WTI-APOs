"""Convert Barchart Price History pages copied as Markdown into clean CSV files.

Run from the directory that contains ``md_original`` and ``csv``:
    python convert_barchart_pages.py

Only Markdown files that contain both a Barchart contract code and the
``Daily Prices`` table are converted.  Navigation/help text from the copied
page is never written to the CSV files.
"""

from __future__ import annotations

import csv
import argparse
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


HEADERS = ["Time", "Open", "High", "Low", "Latest", "Change", "%Change", "Volume", "Open Int"]
DATE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
CONTRACT = re.compile(r"\((?P<root>[A-Za-z0-9]+)\|(?P<strike>\d+)(?P<right>[CP])\)")


def lines_of(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def selected_history(lines: list[str]) -> str:
    for index, line in enumerate(lines[:-1]):
        if line == "Select History:":
            return lines[index + 1]
    return "not recorded"


def parse_page(path: Path) -> tuple[str, list[list[str]], str]:
    lines = lines_of(path)
    match = next((CONTRACT.search(line) for line in lines if CONTRACT.search(line)), None)
    if match is None:
        raise ValueError("contract code not found")
    try:
        first_row = next(
            index for index in range(len(lines) - len(HEADERS) + 1)
            if lines[index : index + len(HEADERS)] == HEADERS
        ) + len(HEADERS)
    except StopIteration as error:
        raise ValueError("Daily Prices header not found") from error

    rows: list[list[str]] = []
    index = first_row
    while index + len(HEADERS) <= len(lines) and DATE.fullmatch(lines[index]):
        row = lines[index : index + len(HEADERS)]
        row[0] = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        if row[5].casefold() == "unch":
            row[5] = "0"
        if row[6].casefold() == "unch":
            row[6] = "0.00%"
        rows.append(row)
        index += len(HEADERS)
    if not rows:
        raise ValueError("no price rows found")

    symbol = f"{match.group('root').lower()}_{match.group('strike')}{match.group('right').lower()}"
    return symbol, rows, selected_history(lines)


def write_csv(destination: Path, rows: list[list[str]]) -> None:
    with destination.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(HEADERS)
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert copied Barchart Price History pages to CSV.")
    parser.add_argument("folders", nargs="*", help="Expiration folders to process, for example mar2027.")
    parser.add_argument("--md-root", type=Path, default=Path("md_original"), help="Root folder containing copied Markdown pages.")
    parser.add_argument("--csv-root", type=Path, default=Path("csv"), help="Root folder for clean CSV output.")
    args = parser.parse_args()
    folders = [args.md_root / name for name in args.folders] if args.folders else sorted(path for path in args.md_root.iterdir() if path.is_dir())
    groups: dict[tuple[Path, str], list[tuple[Path, list[list[str]], str]]] = defaultdict(list)
    ignored = 0
    for folder in folders:
        if not folder.is_dir():
            parser.error(f"Folder not found: {folder}")
        for source in folder.glob("*.md"):
            try:
                symbol, rows, history = parse_page(source)
            except ValueError:
                ignored += 1
                continue
            groups[(folder, symbol)].append((source, rows, history))

    report = [["folder", "contract_csv", "source_pages", "selected_history", "rows", "oldest_date", "latest_date", "status"]]
    for (folder, symbol), pages in sorted(groups.items()):
        by_date: dict[str, list[str]] = {}
        conflict_dates: list[str] = []
        histories: set[str] = set()
        for _, rows, history in pages:
            histories.add(history)
            for row in rows:
                previous = by_date.setdefault(row[0], row)
                if previous != row:
                    conflict_dates.append(row[0])
        rows = [by_date[key] for key in sorted(by_date, reverse=True)]
        last_date = datetime.strptime(rows[0][0], "%Y-%m-%d").strftime("%m-%d-%Y")
        output_folder = args.csv_root / folder.name
        output_folder.mkdir(parents=True, exist_ok=True)
        output = output_folder / f"{symbol}_price-history-{last_date}.csv"
        write_csv(output, rows)
        status = "ok" if not conflict_dates else f"review conflicting duplicate dates: {', '.join(sorted(set(conflict_dates)))}"
        report.append([
            folder.name,
            output.name,
            "; ".join(page.name for page, _, _ in pages),
            "; ".join(sorted(histories)),
            str(len(rows)),
            rows[-1][0],
            rows[0][0],
            status,
        ])
        print(f"Created: {output} ({len(rows)} rows)")

    args.csv_root.mkdir(parents=True, exist_ok=True)
    with (args.csv_root / "conversion_report.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        csv.writer(stream).writerows(report)
    print(f"Created: {args.csv_root / 'conversion_report.csv'} ({len(report) - 1} contracts; {ignored} non-history Markdown files ignored)")


if __name__ == "__main__":
    main()
