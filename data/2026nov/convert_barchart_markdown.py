"""Convierte historiales de Barchart copiados como .md/texto a CSV.

Ejemplos:
    python convert_barchart_markdown.py table1.md
    python convert_barchart_markdown.py 2.md 3.md table1.md
    python convert_barchart_markdown.py --all

El archivo de salida conserva el esquema de las descargas de Barchart:
Time, Open, High, Low, Latest, Change, %Change, Volume, Open Int.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path


HEADERS = ["Time", "Open", "High", "Low", "Latest", "Change", "%Change", "Volume", "Open Int"]
DATE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
CONTRACT = re.compile(r"\((?P<root>[A-Za-z0-9]+)\|(?P<strike>\d+)(?P<kind>[CP])\)")


def nonempty_lines(path: Path) -> list[str]:
    """Read the source while ignoring empty lines and surrounding whitespace."""
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def find_header(lines: list[str]) -> int:
    """Find the consecutive Barchart column labels, not incidental page text."""
    normalized = [line.casefold() for line in lines]
    target = [header.casefold() for header in HEADERS]
    for start in range(len(lines) - len(HEADERS) + 1):
        if normalized[start : start + len(HEADERS)] == target:
            return start
    raise ValueError("No se encontró la fila de encabezados de Price History.")


def parse_barchart_markdown(path: Path) -> list[list[str]]:
    lines = nonempty_lines(path)
    start = find_header(lines) + len(HEADERS)
    rows: list[list[str]] = []
    index = start

    while index < len(lines):
        # A new date marks the beginning of a complete daily-price row.
        if not DATE.fullmatch(lines[index]):
            index += 1
            continue
        row = lines[index : index + len(HEADERS)]
        if len(row) != len(HEADERS):
            raise ValueError(f"Fila incompleta después de la fecha {lines[index]}.")
        if not all(not DATE.fullmatch(value) for value in row[1:]):
            raise ValueError(f"Fila inválida después de la fecha {lines[index]}.")
        row[0] = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        # Barchart uses "unch" (unchanged) in both change columns.  CSV
        # downloads use numeric values, so normalize it for downstream use.
        if row[5].casefold() == "unch":
            row[5] = "0"
        if row[6].casefold() == "unch":
            row[6] = "0.00%"
        rows.append(row)
        index += len(HEADERS)

    if not rows:
        raise ValueError("Se encontraron encabezados, pero no precios diarios.")
    return rows


def write_csv(rows: list[list[str]], output: Path, overwrite: bool) -> None:
    if output.exists() and not overwrite:
        raise FileExistsError(f"Ya existe {output.name}. Usa --overwrite para reemplazarlo.")
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADERS)
        writer.writerows(rows)


def barchart_output_path(source: Path, download_date: str) -> Path:
    """Build Barchart's filename from the contract code in the page title."""
    title = nonempty_lines(source)[0]
    match = CONTRACT.search(title)
    if not match:
        raise ValueError(f"No se encontró un código de contrato como JAOX6|8250P en: {title}")
    contract = f"{match.group('root').lower()}_{match.group('strike')}{match.group('kind').lower()}"
    return source.with_name(f"{contract}_price-history-{download_date}.csv")


def selected_files(arguments: list[Path], all_files: bool) -> list[Path]:
    if all_files:
        return sorted(Path.cwd().glob("*.md"))
    if not arguments:
        raise ValueError("Indica al menos un archivo .md o usa --all.")
    return arguments


def main() -> int:
    parser = argparse.ArgumentParser(description="Convierte texto de Price History de Barchart a CSV.")
    parser.add_argument("inputs", nargs="*", type=Path, help="Uno o más archivos .md.")
    parser.add_argument("--all", action="store_true", help="Intenta convertir todos los .md de la carpeta actual.")
    parser.add_argument("--overwrite", action="store_true", help="Permite reemplazar un CSV ya existente.")
    parser.add_argument("--download-date", default="09-12-2026", help="Fecha incluida en el nombre, en formato MM-DD-YYYY.")
    args = parser.parse_args()

    try:
        inputs = selected_files(args.inputs, args.all)
    except ValueError as error:
        parser.error(str(error))

    failures = 0
    for source in inputs:
        try:
            if not source.is_file():
                raise FileNotFoundError(f"No existe: {source}")
            rows = parse_barchart_markdown(source)
            destination = barchart_output_path(source, args.download_date)
            write_csv(rows, destination, args.overwrite)
            print(f"Creado: {destination.name} ({len(rows)} filas)")
        except (OSError, UnicodeDecodeError, ValueError) as error:
            failures += 1
            print(f"No se convirtió {source.name}: {error}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
