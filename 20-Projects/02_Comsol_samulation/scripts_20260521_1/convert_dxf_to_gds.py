#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 COMSOL 手动导出的 DXF/CSV/SVG 几何转换为 GDS。

优先使用 gdstk/gdspy；缺失时使用内置 GDSII writer。
支持的轻量格式：
- DXF: CIRCLE、LWPOLYLINE、POLYLINE/VERTEX
- CSV: x,y,r 三列，单位默认 um
- SVG: circle、polygon、polyline 的基本写法
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import List, Tuple

from gds_utils import Circle, Square, write_gds_with_fallback, write_json, write_preview_png


def read_csv_circles(path: Path) -> List[Circle]:
    circles: List[Circle] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            circles.append(
                Circle(
                    tag=row.get("tag") or f"circle_{i}",
                    x=float(row["x"]),
                    y=float(row["y"]),
                    r=float(row["r"]),
                    role="hole",
                    source_expr={"x": row["x"], "y": row["y"], "r": row["r"]},
                )
            )
    return circles


def read_dxf_circles(path: Path) -> Tuple[List[Circle], List[List[Tuple[float, float]]]]:
    """极简 DXF 解析器；复杂 DXF 建议安装 ezdxf 后扩展。"""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    pairs = [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines) - 1, 2)]
    circles: List[Circle] = []
    polylines: List[List[Tuple[float, float]]] = []
    i = 0
    while i < len(pairs):
        code, value = pairs[i]
        if code == "0" and value == "CIRCLE":
            x = y = r = 0.0
            i += 1
            while i < len(pairs) and pairs[i][0] != "0":
                c, v = pairs[i]
                if c == "10":
                    x = float(v)
                elif c == "20":
                    y = float(v)
                elif c == "40":
                    r = float(v)
                i += 1
            circles.append(Circle(f"circle_{len(circles)+1}", x, y, r, "hole", {"x": str(x), "y": str(y), "r": str(r)}))
            continue
        if code == "0" and value == "LWPOLYLINE":
            pts: List[Tuple[float, float]] = []
            cur_x = None
            i += 1
            while i < len(pairs) and pairs[i][0] != "0":
                c, v = pairs[i]
                if c == "10":
                    cur_x = float(v)
                elif c == "20" and cur_x is not None:
                    pts.append((cur_x, float(v)))
                    cur_x = None
                i += 1
            if pts:
                if pts[0] != pts[-1]:
                    pts.append(pts[0])
                polylines.append(pts)
            continue
        if code == "0" and value == "POLYLINE":
            pts = []
            i += 1
            while i < len(pairs):
                c, v = pairs[i]
                if c == "0" and v == "SEQEND":
                    i += 1
                    break
                if c == "0" and v == "VERTEX":
                    x = y = None
                    i += 1
                    while i < len(pairs) and pairs[i][0] != "0":
                        vc, vv = pairs[i]
                        if vc == "10":
                            x = float(vv)
                        elif vc == "20":
                            y = float(vv)
                        i += 1
                    if x is not None and y is not None:
                        pts.append((x, y))
                    continue
                i += 1
            if len(pts) >= 3:
                if pts[0] != pts[-1]:
                    pts.append(pts[0])
                polylines.append(pts)
            continue
        i += 1
    return circles, polylines


def read_svg_circles(path: Path) -> Tuple[List[Circle], List[List[Tuple[float, float]]]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    circles: List[Circle] = []
    polylines: List[List[Tuple[float, float]]] = []
    for i, m in enumerate(re.finditer(r"<circle\b[^>]*>", text), 1):
        tag = m.group(0)
        attrs = dict(re.findall(r"(\w+)=[\"']([^\"']+)[\"']", tag))
        if {"cx", "cy", "r"} <= attrs.keys():
            circles.append(Circle(f"circle_{i}", float(attrs["cx"]), float(attrs["cy"]), float(attrs["r"]), "hole", attrs))
    for m in re.finditer(r"<(?:polygon|polyline)\b[^>]*points=[\"']([^\"']+)[\"'][^>]*>", text):
        nums = [float(v) for v in re.split(r"[\s,]+", m.group(1).strip()) if v]
        pts = list(zip(nums[0::2], nums[1::2]))
        if len(pts) >= 3:
            if pts[0] != pts[-1]:
                pts.append(pts[0])
            polylines.append(pts)
    return circles, polylines


def main() -> int:
    parser = argparse.ArgumentParser(description="把 DXF/CSV/SVG 几何转换为 GDS。")
    parser.add_argument("input", help="输入 DXF/CSV/SVG")
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--circle-points", type=int, default=96)
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parents[1]
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = root_dir / input_path
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = root_dir / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    suffix = input_path.suffix.lower()
    polylines: List[List[Tuple[float, float]]] = []
    if suffix == ".csv":
        circles = read_csv_circles(input_path)
    elif suffix == ".dxf":
        circles, polylines = read_dxf_circles(input_path)
    elif suffix == ".svg":
        circles, polylines = read_svg_circles(input_path)
    else:
        raise RuntimeError("只支持 .dxf/.csv/.svg")

    gds_path = out_dir / "disclination_from_exported_geometry.gds"
    preview_path = out_dir / "disclination_from_exported_geometry_preview.png"
    params_path = out_dir / "disclination_from_exported_geometry_params.json"

    # 当前内置 writer 的公共入口支持圆孔；多段线可在安装 gdstk 后继续扩展为 polygon。
    writer = write_gds_with_fallback(
        gds_path,
        circles,
        [],
        [],
        polygon_points=args.circle_points,
        extra_polygons=polylines,
    )
    write_preview_png(preview_path, circles, [], [], extra_polygons=polylines)
    write_json(
        params_path,
        {
            "source": str(input_path),
            "units": "um",
            "writer_used": writer,
            "circle_count": len(circles),
            "polyline_count_detected": len(polylines),
            "note": "圆和闭合 polyline/polygon 会写入 layer 1；复杂曲线建议安装 gdstk/ezdxf 后做布尔清理。",
            "circles": [c.__dict__ for c in circles],
        },
    )
    print(f"写入: {gds_path}")
    print(f"写入: {preview_path}")
    print(f"写入: {params_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
