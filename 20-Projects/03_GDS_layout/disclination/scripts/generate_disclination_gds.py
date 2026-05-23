#!/usr/bin/env python3
"""Entry script for generating a placeholder disclination GDS."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from disclination.dose_matrix import default_dose_matrix
from disclination.gds_export import write_gds
from disclination.geometry import build_lattice


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a placeholder disclination GDS.")
    parser.add_argument("--write", action="store_true", help="Actually write the GDS file. Default is dry-run.")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting the output GDS file.")
    parser.add_argument("--output", default="outputs/gds/disclination_placeholder.gds", help="Output GDS path.")
    parser.add_argument("--period-um", type=float, default=0.56, help="Lattice period in micrometers.")
    parser.add_argument("--radius-um", type=float, default=0.10, help="Hole radius in micrometers.")
    parser.add_argument("--nx", type=int, default=3, help="Placeholder lattice size in x.")
    parser.add_argument("--ny", type=int, default=3, help="Placeholder lattice size in y.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = PROJECT_ROOT / args.output

    print("Start generate_disclination_gds")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output path: {output_path}")
    print(f"Mode: {'write' if args.write else 'dry-run'}")

    holes = build_lattice(period_um=args.period_um, radius_um=args.radius_um, nx=args.nx, ny=args.ny)
    dose_matrix = default_dose_matrix()

    print(f"Hole count: {len(holes)}")
    print(f"Dose matrix count: {len(dose_matrix)}")

    if not args.write:
        print("Dry-run complete. Use --write to create the GDS file.")
        return

    written_path = write_gds(holes, output_path, overwrite=args.overwrite)
    print(f"Wrote GDS: {written_path}")
    print("Done")


if __name__ == "__main__":
    main()

