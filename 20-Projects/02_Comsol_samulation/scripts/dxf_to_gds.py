#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COMSOL DXF -> Shapely 修复 -> 可加工 GDS。

流程严格按本次要求：
1. ezdxf 读取 DXF；
2. 所有 entity 转成线段；
3. 删除 construction/辅助线；
4. merge 重复线段；
5. shapely polygonize 自动闭合边界；
6. unary_union 合并；
7. buffer(0) 修复几何；
8. 写 GDS、JSON、Markdown 报告、修复前后对比图。
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEPS = ROOT / ".python_deps"
if DEPS.exists():
    sys.path.insert(0, str(DEPS))

try:
    import ezdxf
    import gdstk
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.geometry import GeometryCollection, LineString, MultiLineString, MultiPolygon, Polygon
    from shapely.ops import linemerge, polygonize, unary_union
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "缺少必要依赖。请先运行：\n"
        "python3 -m pip install --target ./.python_deps -r requirements.txt\n"
        f"原始错误：{exc}"
    )


Point = Tuple[float, float]


@dataclass
class Candidate:
    name: str
    path: str
    size_bytes: int
    entity_counts: Dict[str, int]
    keywords: List[str]
    raw_extent: float
    score: int


@dataclass
class Report:
    selected_dxf: str
    unit_conversion: str
    entity_counts: Dict[str, int]
    construction_removed_count: int
    raw_line_count: int
    merged_line_type: str
    polygonized_count: int
    final_polygon_count: int
    hole_count: int
    boundary_count: int
    total_width_um: float
    total_height_um: float
    max_dimension_um: float
    min_polygon_size_um: float
    min_polygon_area_um2: float
    approx_min_hole_edge_spacing_um: Optional[float]
    tiny_fragment_count: int
    invalid_before_count: int
    invalid_after_count: int
    fabrication_assessment: str
    risks: List[str]


def find_dxf_files(root: Path) -> List[Path]:
    files = []
    for path in sorted(root.rglob("*.dxf")):
        if any(part.startswith("backup_") for part in path.parts):
            continue
        files.append(path)
    return files


def entity_counts(doc) -> Counter:
    return Counter(e.dxftype() for e in doc.modelspace())


def get_raw_extent(doc) -> float:
    xs: List[float] = []
    ys: List[float] = []
    for e in doc.modelspace():
        try:
            for line in entity_to_lines_raw(e, factor=1.0):
                for x, y in line.coords:
                    xs.append(float(x))
                    ys.append(float(y))
        except Exception:
            continue
    if not xs or not ys:
        return 0.0
    return max(max(xs) - min(xs), max(ys) - min(ys))


def unit_factor_to_um(doc, raw_extent: float) -> Tuple[float, str]:
    insunits = int(doc.header.get("$INSUNITS", 0) or 0)
    mapping = {
        1: (25400.0, "inch"),
        2: (304800.0, "foot"),
        4: (1000.0, "mm"),
        5: (10000.0, "cm"),
        6: (1_000_000.0, "m"),
        13: (1.0, "um"),
        14: (0.001, "nm"),
    }
    if insunits in mapping:
        factor, name = mapping[insunits]
        return factor, f"$INSUNITS={insunits} ({name})"
    if raw_extent < 1e-3:
        return 1_000_000.0, "auto: raw extent < 1e-3, treat as meter"
    return 1.0, "auto: treat as um"


def analyze_candidate(path: Path) -> Candidate:
    doc = ezdxf.readfile(path)
    counts = entity_counts(doc)
    raw_extent = get_raw_extent(doc)
    keywords = [
        k
        for k in ["lattice", "hole", "disclination", "square", "vortex", "photonic", "crystal"]
        if k in path.name.lower()
    ]
    return Candidate(
        name=path.name,
        path=str(path),
        size_bytes=path.stat().st_size,
        entity_counts=dict(counts),
        keywords=keywords,
        raw_extent=raw_extent,
        score=sum(counts.values()) + 1000 * len(keywords),
    )


def is_construction_entity(e) -> bool:
    layer = str(getattr(e.dxf, "layer", "")).lower()
    linetype = str(getattr(e.dxf, "linetype", "")).lower()
    color = int(getattr(e.dxf, "color", 256) or 256)
    name = f"{layer} {linetype}"
    construction_words = ["construction", "construct", "aux", "helper", "axis", "center", "datum"]
    if any(w in name for w in construction_words):
        return True
    if e.dxftype() in {"XLINE", "RAY"}:
        return True
    # COMSOL 常把参考边界放在 0 层，不直接删除。颜色 8/9 等也不可靠。
    _ = color
    return False


def pxy(point, factor: float) -> Point:
    return (float(point[0]) * factor, float(point[1]) * factor)


def line_from_points(points: Sequence[Point]) -> Optional[LineString]:
    if len(points) < 2:
        return None
    # 删除连续重复点。
    cleaned = [points[0]]
    for p in points[1:]:
        if math.hypot(p[0] - cleaned[-1][0], p[1] - cleaned[-1][1]) > 1e-9:
            cleaned.append(p)
    if len(cleaned) < 2:
        return None
    return LineString(cleaned)


def arc_points(center: Point, radius: float, start_deg: float, end_deg: float, factor: float, max_step_deg: float = 4.0) -> List[Point]:
    if end_deg < start_deg:
        end_deg += 360.0
    span = end_deg - start_deg
    steps = max(8, min(128, int(math.ceil(abs(span) / max_step_deg))))
    pts = []
    for i in range(steps + 1):
        a = math.radians(start_deg + span * i / steps)
        pts.append(((center[0] + radius * math.cos(a)) * factor, (center[1] + radius * math.sin(a)) * factor))
    return pts


def circle_points(center: Point, radius: float, factor: float, n: int = 128) -> List[Point]:
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append(((center[0] + radius * math.cos(a)) * factor, (center[1] + radius * math.sin(a)) * factor))
    pts.append(pts[0])
    return pts


def virtual_entity_to_line(e, factor: float) -> List[LineString]:
    kind = e.dxftype()
    lines: List[LineString] = []
    if kind == "LINE":
        line = line_from_points([pxy(e.dxf.start, factor), pxy(e.dxf.end, factor)])
        if line:
            lines.append(line)
    elif kind == "ARC":
        pts = arc_points(
            (float(e.dxf.center[0]), float(e.dxf.center[1])),
            float(e.dxf.radius),
            float(e.dxf.start_angle),
            float(e.dxf.end_angle),
            factor,
        )
        line = line_from_points(pts)
        if line:
            lines.append(line)
    elif kind == "CIRCLE":
        line = line_from_points(circle_points((float(e.dxf.center[0]), float(e.dxf.center[1])), float(e.dxf.radius), factor, 128))
        if line:
            lines.append(line)
    return lines


def entity_to_lines_raw(e, factor: float) -> List[LineString]:
    kind = e.dxftype()
    lines: List[LineString] = []
    if kind in {"LWPOLYLINE", "POLYLINE"}:
        try:
            virtual = list(e.virtual_entities())
            for ve in virtual:
                lines.extend(virtual_entity_to_line(ve, factor))
            if getattr(e, "closed", False) and lines:
                coords_first = list(lines[0].coords)[0]
                coords_last = list(lines[-1].coords)[-1]
                if math.hypot(coords_first[0] - coords_last[0], coords_first[1] - coords_last[1]) > 1e-9:
                    close = line_from_points([coords_last, coords_first])
                    if close:
                        lines.append(close)
        except Exception:
            pts = [(float(p[0]) * factor, float(p[1]) * factor) for p in e.get_points()]
            if getattr(e, "closed", False) and pts and pts[0] != pts[-1]:
                pts.append(pts[0])
            line = line_from_points(pts)
            if line:
                lines.append(line)
    elif kind in {"LINE", "ARC", "CIRCLE"}:
        lines.extend(virtual_entity_to_line(e, factor))
    elif kind == "SPLINE":
        pts = []
        try:
            # flattening 距离使用原始单位。factor 越大，原始公差越小。
            tol = max(1e-9, 0.005 / factor)
            pts = [pxy(p, factor) for p in e.flattening(tol)]
        except Exception:
            try:
                pts = [pxy(p, factor) for p in e.control_points]
            except Exception:
                pts = []
        line = line_from_points(pts)
        if line:
            lines.append(line)
    return lines


def collect_lines(doc, factor: float) -> Tuple[List[LineString], Counter, int]:
    counts = entity_counts(doc)
    lines: List[LineString] = []
    removed = 0
    for e in doc.modelspace():
        if is_construction_entity(e):
            removed += 1
            continue
        lines.extend(entity_to_lines_raw(e, factor))
    return lines, counts, removed


def polygon_parts(geom) -> List[Polygon]:
    if geom.is_empty:
        return []
    if isinstance(geom, Polygon):
        return [geom]
    if isinstance(geom, MultiPolygon):
        return list(geom.geoms)
    if isinstance(geom, GeometryCollection):
        out: List[Polygon] = []
        for g in geom.geoms:
            out.extend(polygon_parts(g))
        return out
    return []


def repair_geometry(lines: List[LineString]) -> Tuple[List[Polygon], List[Polygon], object, object]:
    # unary_union 会 noding，并去除重复线段；linemerge 再合并连续线。
    merged_lines = linemerge(unary_union(lines))
    raw_polygons = list(polygonize(merged_lines))
    unioned = unary_union(raw_polygons)
    repaired = unioned.buffer(0)
    final_polygons = polygon_parts(repaired)
    return raw_polygons, final_polygons, merged_lines, repaired


def classify_layout(raw_polygons: Sequence[Polygon], final_polygons: Sequence[Polygon]) -> Tuple[List[Polygon], List[Polygon]]:
    """从 Shapely 修复结果中分出孔和参考边界。

    COMSOL 导出的 DXF 常把一个空气孔拆成很多互相相交的小折线。
    `polygonize` 后会得到许多小面片，所以这里先选出小闭合面片，
    再用 `unary_union + buffer(0)` 把它们合并回真实孔轮廓。
    """
    if not raw_polygons and not final_polygons:
        return [], []

    base_polys = list(final_polygons) if final_polygons else list(raw_polygons)
    minx, miny, maxx, maxy = bounds_of_polygons(base_polys)
    layout_size = max(maxx - minx, maxy - miny)
    hole_piece_limit = max(layout_size * 0.05, 0.5)

    hole_pieces: List[Polygon] = []
    for p in raw_polygons:
        size = max(p.bounds[2] - p.bounds[0], p.bounds[3] - p.bounds[1])
        if size < hole_piece_limit and p.area > 1e-8:
            hole_pieces.append(p)

    holes = polygon_parts(unary_union(hole_pieces).buffer(0)) if hole_pieces else []
    holes = [p for p in holes if p.area > 1e-6 and p.is_valid]

    boundaries: List[Polygon] = []
    for p in final_polygons:
        if p.area <= 1e-6:
            continue
        shell = Polygon(p.exterior).buffer(0)
        boundaries.extend([part for part in polygon_parts(shell) if part.area > 1e-6])

    if not holes and final_polygons:
        # 兜底：如果输入本身已经是简单闭合孔轮廓，则按尺寸重新分类。
        sizes = [max(p.bounds[2] - p.bounds[0], p.bounds[3] - p.bounds[1]) for p in final_polygons]
        max_size = max(sizes)
        threshold = max_size * 0.2
        boundaries = []
        for p, size in zip(final_polygons, sizes):
            if size >= threshold:
                boundaries.append(p)
            else:
                holes.append(p)

    return holes, boundaries


def bounds_of_polygons(polygons: Sequence[Polygon]) -> Tuple[float, float, float, float]:
    minx = min(p.bounds[0] for p in polygons)
    miny = min(p.bounds[1] for p in polygons)
    maxx = max(p.bounds[2] for p in polygons)
    maxy = max(p.bounds[3] for p in polygons)
    return minx, miny, maxx, maxy


def approx_min_spacing(polygons: Sequence[Polygon]) -> Optional[float]:
    if len(polygons) < 2:
        return None
    centers = []
    for i, p in enumerate(polygons):
        minx, miny, maxx, maxy = p.bounds
        cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
        r = max(maxx - minx, maxy - miny) / 2
        centers.append((i, cx, cy, r))
    max_r = max(c[3] for c in centers)
    cell = max(4 * max_r, 0.01)
    grid: Dict[Tuple[int, int], List[int]] = {}
    for n, (_, cx, cy, _) in enumerate(centers):
        grid.setdefault((math.floor(cx / cell), math.floor(cy / cell)), []).append(n)
    best = None
    for n, (_, cx, cy, r) in enumerate(centers):
        gx, gy = math.floor(cx / cell), math.floor(cy / cell)
        for ix in range(gx - 1, gx + 2):
            for iy in range(gy - 1, gy + 2):
                for m in grid.get((ix, iy), []):
                    if m <= n:
                        continue
                    _, cx2, cy2, r2 = centers[m]
                    spacing = math.hypot(cx - cx2, cy - cy2) - r - r2
                    if best is None or spacing < best:
                        best = spacing
    return best


def write_gds(path: Path, holes: Sequence[Polygon], boundaries: Sequence[Polygon]) -> None:
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    cell = lib.new_cell("disclination_vortex")

    def add_poly(poly: Polygon, layer: int) -> None:
        exterior = list(poly.exterior.coords)
        if len(exterior) >= 4:
            cell.add(gdstk.Polygon(exterior, layer=layer))
        for interior in poly.interiors:
            pts = list(interior.coords)
            if len(pts) >= 4:
                cell.add(gdstk.Polygon(pts, layer=layer))

    for p in holes:
        add_poly(p, 1)
    for p in boundaries:
        add_poly(p, 10)

    all_polys = list(holes) + list(boundaries)
    if all_polys:
        minx, miny, _, _ = bounds_of_polygons(all_polys)
        cell.add(gdstk.Label("Generated_from_COMSOL", (minx, miny - 0.5), layer=20))
    else:
        cell.add(gdstk.Label("Generated_from_COMSOL", (0, 0), layer=20))
    lib.write_gds(str(path))


def plot_polygons(ax, polygons: Sequence[Polygon], color: str, linewidth: float = 0.4) -> None:
    for p in polygons:
        x, y = p.exterior.xy
        ax.plot(x, y, color=color, linewidth=linewidth)
        for ring in p.interiors:
            x, y = ring.xy
            ax.plot(x, y, color=color, linewidth=linewidth)


def write_comparison(before_path: Path, after_path: Path, raw_polygons: Sequence[Polygon], holes: Sequence[Polygon], boundaries: Sequence[Polygon]) -> None:
    for path, title, mode in [
        (before_path, "Before repair: polygonize result", "before"),
        (after_path, "After repair: unary_union + buffer(0)", "after"),
    ]:
        fig, ax = plt.subplots(figsize=(9, 9), dpi=220)
        if mode == "before":
            plot_polygons(ax, raw_polygons, "0.1", 0.35)
        else:
            plot_polygons(ax, holes, "0.05", 0.35)
            plot_polygons(ax, boundaries, "#0057d8", 0.45)
        ax.axhline(0, color="0.85", linewidth=0.4)
        ax.axvline(0, color="0.85", linewidth=0.4)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(title)
        ax.set_xlabel("x (um)")
        ax.set_ylabel("y (um)")
        # 尺寸标尺
        all_polys = raw_polygons if mode == "before" else list(holes) + list(boundaries)
        if all_polys:
            minx, miny, maxx, maxy = bounds_of_polygons(all_polys)
            bar = 10.0 if max(maxx - minx, maxy - miny) > 20 else 1.0
            ax.plot([minx, minx + bar], [miny, miny], color="red", linewidth=3)
            ax.text(minx, miny, f" {bar:g} um", color="red", va="bottom")
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)


def write_preview(path: Path, holes: Sequence[Polygon], boundaries: Sequence[Polygon]) -> None:
    write_comparison(path, path, holes, holes, boundaries)


def make_report(
    selected: Path,
    unit_note: str,
    counts: Counter,
    construction_removed: int,
    raw_lines: List[LineString],
    raw_polygons: List[Polygon],
    final_polygons: List[Polygon],
    holes: List[Polygon],
    boundaries: List[Polygon],
    merged_lines,
) -> Report:
    all_polys = list(holes) + list(boundaries)
    minx, miny, maxx, maxy = bounds_of_polygons(all_polys)
    sizes = [max(p.bounds[2] - p.bounds[0], p.bounds[3] - p.bounds[1]) for p in all_polys]
    areas = [p.area for p in all_polys]
    tiny = [p for p in all_polys if max(p.bounds[2] - p.bounds[0], p.bounds[3] - p.bounds[1]) < 0.02 or p.area < 1e-6]
    invalid_before = [p for p in raw_polygons if not p.is_valid]
    invalid_after = [p for p in final_polygons if not p.is_valid]
    min_spacing = approx_min_spacing(holes)
    risks: List[str] = []
    if tiny:
        risks.append(f"存在 {len(tiny)} 个小于 20 nm 或面积过小的结构，需确认工艺能力")
    else:
        risks.append("未发现小于 20 nm 的小特征")
    if min_spacing is not None and min_spacing < 0.02:
        risks.append(f"近似最小孔边距为 {min_spacing:.6f} um，可能小于工艺最小间距或存在重叠")
    else:
        risks.append("近似最小孔边距未低于 20 nm")
    if invalid_after:
        risks.append("修复后仍存在 invalid polygon，需要人工修复")
    else:
        risks.append("buffer(0) 后未检测到 invalid polygon")
    risks.append("已用 polygonize + unary_union + buffer(0) 修复，但送厂前仍建议用 KLayout 做工艺 DRC")
    if invalid_after:
        assessment = "需要修复异常 polygon 后再加工"
    elif tiny or (min_spacing is not None and min_spacing < 0.02):
        assessment = "GDS 有效，但存在小特征/小间距风险，需工艺确认后用于电子束曝光"
    else:
        assessment = "适合进入电子束曝光前检查流程"
    return Report(
        selected_dxf=str(selected),
        unit_conversion=unit_note,
        entity_counts=dict(counts),
        construction_removed_count=construction_removed,
        raw_line_count=len(raw_lines),
        merged_line_type=merged_lines.geom_type,
        polygonized_count=len(raw_polygons),
        final_polygon_count=len(final_polygons),
        hole_count=len(holes),
        boundary_count=len(boundaries),
        total_width_um=maxx - minx,
        total_height_um=maxy - miny,
        max_dimension_um=max(maxx - minx, maxy - miny),
        min_polygon_size_um=min(sizes) if sizes else 0.0,
        min_polygon_area_um2=min(areas) if areas else 0.0,
        approx_min_hole_edge_spacing_um=min_spacing,
        tiny_fragment_count=len(tiny),
        invalid_before_count=len(invalid_before),
        invalid_after_count=len(invalid_after),
        fabrication_assessment=assessment,
        risks=risks,
    )


def write_geometry_report(path: Path, report: Report) -> None:
    risks = "\n".join(f"- {r}" for r in report.risks)
    min_spacing = "None" if report.approx_min_hole_edge_spacing_um is None else f"{report.approx_min_hole_edge_spacing_um:.6f} um"
    text = f"""# Geometry Report

生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}

## 输入

- DXF：`{report.selected_dxf}`
- 单位转换：{report.unit_conversion}

## 修复流程

1. `ezdxf` 读取所有 entity。
2. 删除 construction/aux/helper/axis 等辅助线。
3. CIRCLE 用 128 点离散，ARC 自动离散，SPLINE flattening 采样。
4. `shapely.unary_union` 合并和去重线段。
5. `shapely.linemerge` 合并连续线段。
6. `shapely.polygonize` 自动闭合边界生成 polygon。
7. `unary_union` 合并 polygon。
8. `buffer(0)` 修复 invalid 几何。
9. 从 polygonize 小面片重建孔轮廓，从修复后的大面提取参考边界。

## 统计

- entity 统计：`{json.dumps(report.entity_counts, ensure_ascii=False)}`
- 删除辅助 entity：{report.construction_removed_count}
- 原始线段数量：{report.raw_line_count}
- polygonize 后 polygon 数：{report.polygonized_count}
- 修复后 polygon 数：{report.final_polygon_count}
- 空气孔/刻蚀孔：{report.hole_count}
- 外边界/参考边界：{report.boundary_count}
- 总宽度：{report.total_width_um:.6f} um
- 总高度：{report.total_height_um:.6f} um
- 最大尺寸：{report.max_dimension_um:.6f} um
- 最小 polygon 尺寸：{report.min_polygon_size_um:.6f} um
- 最小 polygon 面积：{report.min_polygon_area_um2:.6e} um^2
- 近似最小孔边距：{min_spacing}

## 几何有效性

- 修复前 invalid polygon：{report.invalid_before_count}
- 修复后 invalid polygon：{report.invalid_after_count}
- 过小结构数量：{report.tiny_fragment_count}

## 可加工性分析

结论：{report.fabrication_assessment}

风险：

{risks}

## 对比图

- 修复前：`output/disclination_before_repair.png`
- 修复后：`output/disclination_after_repair.png`
"""
    path.write_text(text, encoding="utf-8")


def write_readme(path: Path, report: Report) -> None:
    text = f"""# COMSOL DXF to GDS

## 输入文件

- `{report.selected_dxf}`

## 输出文件

- `output/disclination_from_comsol.gds`
- `output/disclination_preview.png`
- `output/disclination_before_repair.png`
- `output/disclination_after_repair.png`
- `output/disclination_params.json`
- `output/geometry_report.md`

## 单位

- DXF 原始单位：{report.unit_conversion}
- GDS 输出单位：um
- GDS 数据库精度：1 nm

## Layer 定义

- layer 1：空气孔/刻蚀孔
- layer 10：外边界
- layer 20：文字说明 `Generated_from_COMSOL`

## 生成时间

{time.strftime('%Y-%m-%d %H:%M:%S')}

## 运行方法

```bash
PYTHONPATH=.python_deps python3 scripts/dxf_to_gds.py
```

## 可加工性

{report.fabrication_assessment}
"""
    path.write_text(text, encoding="utf-8")


def main() -> int:
    root = Path.cwd()
    output = root / "output"
    output.mkdir(exist_ok=True)

    candidates = [analyze_candidate(p) for p in find_dxf_files(root)]
    if not candidates:
        raise SystemExit("未找到 .dxf 文件。")
    selected_info = max(candidates, key=lambda c: c.score)
    selected = Path(selected_info.path)

    doc = ezdxf.readfile(selected)
    raw_extent = get_raw_extent(doc)
    factor, unit_note = unit_factor_to_um(doc, raw_extent)
    raw_lines, counts, construction_removed = collect_lines(doc, factor)
    raw_polygons, final_polygons, merged_lines, repaired = repair_geometry(raw_lines)
    holes, boundaries = classify_layout(raw_polygons, final_polygons)

    report = make_report(selected, unit_note, counts, construction_removed, raw_lines, raw_polygons, final_polygons, holes, boundaries, merged_lines)
    data = asdict(report)
    data["dxf_candidates"] = [asdict(c) for c in candidates]
    data["recommended_dxf"] = asdict(selected_info)
    data["cell"] = "disclination_vortex"
    data["layers"] = {"1": "空气孔/刻蚀孔", "10": "外边界", "20": "文字说明"}

    write_gds(output / "disclination_from_comsol.gds", holes, boundaries)
    write_comparison(output / "disclination_before_repair.png", output / "disclination_after_repair.png", raw_polygons, holes, boundaries)
    # 兼容任务指定的 preview.png 命名。
    write_comparison(output / "disclination_preview.png", output / "disclination_preview.png", raw_polygons, holes, boundaries)
    (output / "disclination_params.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_geometry_report(output / "geometry_report.md", report)
    write_readme(output / "README.md", report)

    print("DXF candidates:")
    for c in candidates:
        print(f"- {c.name} | {c.path} | {c.size_bytes} bytes | {c.entity_counts} | keywords={c.keywords}")
    print(f"Recommended DXF: {selected}")
    print(f"Unit conversion: {unit_note}")
    print("Repair pipeline: ezdxf -> line merge -> polygonize -> unary_union -> buffer(0)")
    print(f"Output GDS: {output / 'disclination_from_comsol.gds'}")
    print(f"Before repair: {output / 'disclination_before_repair.png'}")
    print(f"After repair: {output / 'disclination_after_repair.png'}")
    print(f"Preview: {output / 'disclination_preview.png'}")
    print(f"Holes: {report.hole_count}")
    print(f"Total size: {report.total_width_um:.6f} x {report.total_height_um:.6f} um")
    print(f"Fabrication assessment: {report.fabrication_assessment}")
    print("Risks:")
    for risk in report.risks:
        print(f"- {risk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
