"""Extrae el historial de precios de páginas completas de Barchart guardadas como Markdown.

Cada página puede incluir navegación, ayuda y otros textos. Solo se exporta la
tabla Daily Prices. Los CSV se nombran con el contrato, por ejemplo:
jaov6_9200c_price-history-09-12-2026.csv.

Uso desde esta carpeta:
    python convert_oct2026_barchart.py
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import datetime
from pathlib import Path


HEADERS = ["Time", "Open", "High", "Low", "Latest", "Change", "%Change", "Volume", "Open Int"]
DATE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
CONTRACT = re.compile(r"\((?P<root>[A-Za-z0-9]+)\|(?P<strike>\d+)(?P<kind>[CP])\)")
DOWNLOAD_DATE = "09-12-2026"


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def two_years_selected(lines: list[str]) -> bool:
    """Check the selected control, not an incidental mention in page help."""
    for index, value in enumerate(lines[:-1]):
        if value == "Select History:":
            return lines[index + 1] == "2 Years"
    return False


def extract_rows(lines: list[str], source: Path) -> list[list[str]]:
    try:
        start = next(index for index in range(len(lines) - len(HEADERS) + 1) if lines[index : index + len(HEADERS)] == HEADERS)
    except StopIteration as error:
        raise ValueError("No se encontró la tabla Daily Prices.") from error

    rows: list[list[str]] = []
    index = start + len(HEADERS)
    while index + len(HEADERS) <= len(lines) and DATE.fullmatch(lines[index]):
        row = lines[index : index + len(HEADERS)]
        row[0] = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        # Barchart writes "unch" when there is no change. Keep columns numeric.
        if row[5].casefold() == "unch":
            row[5] = "0"
        if row[6].casefold() == "unch":
            row[6] = "0.00%"
        rows.append(row)
        index += len(HEADERS)
    if not rows:
        raise ValueError("La tabla no contiene filas de precios.")
    if any(len(row) != len(HEADERS) for row in rows):
        raise ValueError("Se detectó una fila con columnas incompletas.")
    return rows


def output_path(source: Path, lines: list[str]) -> Path:
    match = next((CONTRACT.search(line) for line in lines if CONTRACT.search(line)), None)
    if not match:
        raise ValueError("No se encontró el identificador de contrato en el título.")
    symbol = f"{match.group('root').lower()}_{match.group('strike')}{match.group('kind').lower()}"
    return source.with_name(f"{symbol}_price-history-{DOWNLOAD_DATE}.csv")


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(HEADERS)
        writer.writerows(rows)


def main() -> int:
    report: list[list[str]] = [["source", "contract_csv", "selected_2_years", "rows", "oldest_date", "latest_date", "status"]]
    sources = sorted(Path(".").glob("[0-9][0-9].md"))
    failures = 0
    for source in sources:
        try:
            lines = read_lines(source)
            rows = extract_rows(lines, source)
            destination = output_path(source, lines)
            write_csv(destination, rows)
            selected = two_years_selected(lines)
            status = "ok" if selected else "review: page does not show 2 Years selected"
            report.append([source.name, destination.name, str(selected).lower(), str(len(rows)), rows[-1][0], rows[0][0], status])
            print(f"Created: {destination.name} ({len(rows)} rows; 2 Years selected: {selected})")
        except (OSError, UnicodeDecodeError, ValueError) as error:
            failures += 1
            report.append([source.name, "", "", "", "", "", f"error: {error}"])
            print(f"Could not convert {source.name}: {error}", file=sys.stderr)

    with Path("coverage_report.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        csv.writer(stream).writerows(report)
    print("Created: coverage_report.csv")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
