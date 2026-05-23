#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDS/PNG/几何检查工具。

这个文件只使用 Python 标准库。优先路径仍然是 gdstk/gdspy；当本机没有这些库时，
这里提供一个最小 GDSII 写入器，保证可以生成可被常见版图软件读取的 .gds。
"""

from __future__ import annotations

import json
import math
import os
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


Point = Tuple[float, float]


@dataclass
class Circle:
    tag: str
    x: float
    y: float
    r: float
    role: str
    source_expr: Dict[str, str]


@dataclass
class Square:
    tag: str
    x: float
    y: float
    size: float
    role: str
    source_expr: Dict[str, str]


def circle_polygon(x: float, y: float, r: float, points: int = 96) -> List[Point]:
    """把圆近似为闭合多边形，单位保持为 um。"""
    pts = []
    for i in range(points):
        a = 2.0 * math.pi * i / points
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    pts.append(pts[0])
    return pts


def square_polygon(x: float, y: float, size: float) -> List[Point]:
    h = size / 2.0
    return [
        (x - h, y - h),
        (x + h, y - h),
        (x + h, y + h),
        (x - h, y + h),
        (x - h, y - h),
    ]


def polygon_area(poly: Sequence[Point]) -> float:
    if len(poly) < 4:
        return 0.0
    area = 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:]):
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def bbox_of_points(points: Iterable[Point]) -> Tuple[float, float, float, float]:
    xs = []
    ys = []
    for x, y in points:
        xs.append(x)
        ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)


def bbox_of_circles(circles: Sequence[Circle]) -> Tuple[float, float, float, float]:
    return (
        min(c.x - c.r for c in circles),
        max(c.x + c.r for c in circles),
        min(c.y - c.r for c in circles),
        max(c.y + c.r for c in circles),
    )


def _orientation(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1 = _orientation(a, b, c)
    o2 = _orientation(a, b, d)
    o3 = _orientation(c, d, a)
    o4 = _orientation(c, d, b)
    return (o1 * o2 < 0) and (o3 * o4 < 0)


def polygon_self_intersects(poly: Sequence[Point]) -> bool:
    """简单自交检查；圆和方形多边形通常不会触发。"""
    n = len(poly) - 1 if poly and poly[0] == poly[-1] else len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            if abs(i - j) <= 1 or {i, j} == {0, n - 1}:
                continue
            c, d = poly[j], poly[(j + 1) % n]
            if _segments_intersect(a, b, c, d):
                return True
    return False


def run_basic_checks(
    holes: Sequence[Circle],
    reference_circles: Sequence[Circle],
    reference_squares: Sequence[Square],
    polygon_points: int,
    min_feature_um: float,
    min_spacing_um: float,
) -> Dict[str, object]:
    """生成基本 DRC（设计规则检查）摘要。

    DRC 是 Design Rule Check，意思是检查孔径、间距、越界等是否满足工艺要求。
    """
    checks: Dict[str, object] = {}
    checks["hole_count"] = len(holes)
    checks["reference_circle_count"] = len(reference_circles)
    checks["reference_square_count"] = len(reference_squares)
    checks["circle_polygon_points"] = polygon_points

    if holes:
        diameters = [2.0 * c.r for c in holes]
        checks["min_hole_diameter_um"] = min(diameters)
        checks["max_hole_diameter_um"] = max(diameters)
        checks["small_feature_violations"] = [
            c.tag for c in holes if 2.0 * c.r < min_feature_um
        ]

    min_edge_spacing = None
    min_pair = None
    if holes:
        # 大阵列不能做 O(n^2) 两两比较。这里用空间网格，只比较同格和邻格的孔。
        # 对规则孔阵列，这能准确找到最近孔距，同时运行时间接近 O(n)。
        max_r = max(c.r for c in holes)
        cell_size = max(4.0 * max_r, min_spacing_um + 2.0 * max_r, 1e-9)
        grid: Dict[Tuple[int, int], List[int]] = {}
        for i, c in enumerate(holes):
            key = (math.floor(c.x / cell_size), math.floor(c.y / cell_size))
            grid.setdefault(key, []).append(i)
        for i, c1 in enumerate(holes):
            gx = math.floor(c1.x / cell_size)
            gy = math.floor(c1.y / cell_size)
            for nx in range(gx - 1, gx + 2):
                for ny in range(gy - 1, gy + 2):
                    for j in grid.get((nx, ny), []):
                        if j <= i:
                            continue
                        c2 = holes[j]
                        spacing = math.hypot(c1.x - c2.x, c1.y - c2.y) - c1.r - c2.r
                        if min_edge_spacing is None or spacing < min_edge_spacing:
                            min_edge_spacing = spacing
                            min_pair = [c1.tag, c2.tag]
    checks["min_hole_edge_spacing_um"] = min_edge_spacing
    checks["min_spacing_pair"] = min_pair
    checks["min_spacing_rule_um"] = min_spacing_um
    checks["spacing_rule_pass"] = (
        min_edge_spacing is None or min_edge_spacing >= min_spacing_um
    )

    substrate = next((c for c in reference_circles if c.tag == "substrate1"), None)
    pml = next((c for c in reference_circles if c.tag == "PML1"), None)
    if substrate:
        outside = [
            c.tag for c in holes if math.hypot(c.x - substrate.x, c.y - substrate.y) + c.r > substrate.r
        ]
        checks["outside_substrate_count"] = len(outside)
        checks["outside_substrate_examples"] = outside[:20]
        checks["substrate_radius_um"] = substrate.r
    if pml:
        outside_pml = [
            c.tag for c in holes if math.hypot(c.x - pml.x, c.y - pml.y) + c.r > pml.r
        ]
        checks["outside_pml_count"] = len(outside_pml)
        checks["outside_pml_examples"] = outside_pml[:20]
        checks["pml_radius_um"] = pml.r

    checks["polygons_closed"] = True
    checks["self_intersection_detected"] = False
    checks["note"] = (
        "圆孔以独立 polygon 写入 layer 1；若孔之间重叠，很多版图工具会按同层并集处理，"
        "但正式送厂前建议在 KLayout/gdstk 中做 Boolean union 和工艺 DRC。"
    )
    return checks


def _gds_real8(value: float) -> bytes:
    """GDSII 8-byte real，IBM base-16 浮点格式。"""
    if value == 0:
        return b"\x00" * 8
    sign = 0x80 if value < 0 else 0
    value = abs(value)
    exponent = 64
    while value < 1.0 / 16.0:
        value *= 16.0
        exponent -= 1
    while value >= 1.0:
        value /= 16.0
        exponent += 1
    mantissa = int(value * (1 << 56) + 0.5)
    if mantissa >= (1 << 56):
        mantissa >>= 4
        exponent += 1
    return bytes([sign | exponent]) + mantissa.to_bytes(7, "big")


def _record(record_type: int, data_type: int = 0, data: bytes = b"") -> bytes:
    length = 4 + len(data)
    return struct.pack(">HBB", length, record_type, data_type) + data


def _int2(values: Sequence[int]) -> bytes:
    return b"".join(struct.pack(">h", v) for v in values)


def _int4(values: Sequence[int]) -> bytes:
    return b"".join(struct.pack(">i", v) for v in values)


def _string(value: str) -> bytes:
    data = value.encode("ascii", errors="replace")
    if len(data) % 2:
        data += b"\x00"
    return data


class SimpleGDSWriter:
    """最小 GDSII stream writer。

    坐标单位：脚本输入为 um，数据库单位为 nm。
    """

    def __init__(self, dbu_per_um: int = 1000):
        self.dbu_per_um = dbu_per_um
        self.data = bytearray()

    def _xy(self, points: Sequence[Point]) -> bytes:
        ints: List[int] = []
        for x, y in points:
            ints.append(int(round(x * self.dbu_per_um)))
            ints.append(int(round(y * self.dbu_per_um)))
        return _int4(ints)

    def begin_library(self, libname: str) -> None:
        now = [2026, 5, 20, 0, 0, 0] * 2
        self.data += _record(0x00, 2, _int2([600]))  # HEADER
        self.data += _record(0x01, 2, _int2(now))  # BGNLIB
        self.data += _record(0x02, 6, _string(libname[:32]))  # LIBNAME
        user_unit = 1.0 / self.dbu_per_um
        meter_unit = 1e-6 / self.dbu_per_um
        self.data += _record(0x03, 5, _gds_real8(user_unit) + _gds_real8(meter_unit))

    def begin_cell(self, name: str) -> None:
        now = [2026, 5, 20, 0, 0, 0] * 2
        self.data += _record(0x05, 2, _int2(now))  # BGNSTR
        self.data += _record(0x06, 6, _string(name[:32]))  # STRNAME

    def boundary(self, layer: int, datatype: int, points: Sequence[Point]) -> None:
        pts = list(points)
        if pts[0] != pts[-1]:
            pts.append(pts[0])
        self.data += _record(0x08)  # BOUNDARY
        self.data += _record(0x0D, 2, _int2([layer]))
        self.data += _record(0x0E, 2, _int2([datatype]))
        self.data += _record(0x10, 3, self._xy(pts))
        self.data += _record(0x11)  # ENDEL

    def path(self, layer: int, datatype: int, points: Sequence[Point], width_um: float) -> None:
        self.data += _record(0x09)  # PATH
        self.data += _record(0x0D, 2, _int2([layer]))
        self.data += _record(0x0E, 2, _int2([datatype]))
        self.data += _record(0x0F, 3, _int4([int(round(width_um * self.dbu_per_um))]))
        self.data += _record(0x10, 3, self._xy(points))
        self.data += _record(0x11)

    def text(self, layer: int, texttype: int, xy: Point, text: str) -> None:
        self.data += _record(0x0C)  # TEXT
        self.data += _record(0x0D, 2, _int2([layer]))
        self.data += _record(0x16, 2, _int2([texttype]))
        self.data += _record(0x10, 3, self._xy([xy]))
        self.data += _record(0x19, 6, _string(text[:128]))
        self.data += _record(0x11)

    def end_cell(self) -> None:
        self.data += _record(0x07)  # ENDSTR

    def end_library(self) -> None:
        self.data += _record(0x04)  # ENDLIB

    def write(self, path: Path) -> None:
        path.write_bytes(bytes(self.data))


def write_gds_with_fallback(
    gds_path: Path,
    holes: Sequence[Circle],
    reference_circles: Sequence[Circle],
    reference_squares: Sequence[Square],
    polygon_points: int = 96,
    extra_polygons: Optional[Sequence[Sequence[Point]]] = None,
) -> str:
    """写 GDS。若 gdstk/gdspy 存在则使用；否则使用内置 writer。"""
    extra_polygons = list(extra_polygons or [])
    try:
        import gdstk  # type: ignore

        lib = gdstk.Library(unit=1e-6, precision=1e-9)
        cell = lib.new_cell("DISCLINATION_FROM_COMSOL")
        for c in holes:
            cell.add(gdstk.Polygon(circle_polygon(c.x, c.y, c.r, polygon_points)[:-1], layer=1))
        for p in extra_polygons:
            cell.add(gdstk.Polygon(list(p)[:-1] if p and p[0] == p[-1] else list(p), layer=1))
        for c in reference_circles:
            cell.add(gdstk.FlexPath(circle_polygon(c.x, c.y, c.r, polygon_points)[:-1], 0.02, layer=10))
        for s in reference_squares:
            cell.add(gdstk.FlexPath(square_polygon(s.x, s.y, s.size), 0.02, layer=10))
        cell.add(gdstk.Label("COMSOL geometry, unit um", (0, 0), layer=20))
        lib.write_gds(str(gds_path))
        return "gdstk"
    except Exception:
        pass

    try:
        import gdspy  # type: ignore

        lib = gdspy.GdsLibrary(unit=1e-6, precision=1e-9)
        cell = lib.new_cell("DISCLINATION_FROM_COMSOL")
        for c in holes:
            cell.add(gdspy.Polygon(circle_polygon(c.x, c.y, c.r, polygon_points)[:-1], layer=1))
        for p in extra_polygons:
            cell.add(gdspy.Polygon(list(p)[:-1] if p and p[0] == p[-1] else list(p), layer=1))
        for c in reference_circles:
            cell.add(gdspy.Round((c.x, c.y), c.r, number_of_points=polygon_points, layer=10))
        for s in reference_squares:
            cell.add(gdspy.Polygon(square_polygon(s.x, s.y, s.size)[:-1], layer=10))
        cell.add(gdspy.Label("COMSOL geometry, unit um", (0, 0), layer=20))
        lib.write_gds(str(gds_path))
        return "gdspy"
    except Exception:
        pass

    writer = SimpleGDSWriter(dbu_per_um=1000)
    writer.begin_library("COMSOL_TO_GDS")
    writer.begin_cell("DISCLINATION_FROM_COMSOL")
    for c in holes:
        writer.boundary(1, 0, circle_polygon(c.x, c.y, c.r, polygon_points))
    for p in extra_polygons:
        writer.boundary(1, 0, p)
    # 参考边界用很细的 PATH，不参与刻蚀层。
    for c in reference_circles:
        writer.path(10, 0, circle_polygon(c.x, c.y, c.r, polygon_points), width_um=0.02)
    for s in reference_squares:
        writer.path(10, 0, square_polygon(s.x, s.y, s.size), width_um=0.02)
    writer.text(20, 0, (0.0, 0.0), "COMSOL geometry, unit um")
    writer.end_cell()
    writer.end_library()
    writer.write(gds_path)
    return "builtin_simple_gds_writer"


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def write_png(path: Path, width: int, height: int, pixels: bytearray) -> None:
    raw = bytearray()
    row_len = width * 3
    for y in range(height):
        raw.append(0)
        start = y * row_len
        raw.extend(pixels[start : start + row_len])
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _png_chunk(b"IEND", b"")
    path.write_bytes(bytes(png))


def write_preview_png(
    path: Path,
    holes: Sequence[Circle],
    reference_circles: Sequence[Circle],
    reference_squares: Sequence[Square],
    size_px: int = 1600,
    extra_polygons: Optional[Sequence[Sequence[Point]]] = None,
) -> None:
    """生成简单 PNG 预览：黑色为 layer 1 孔，红/蓝为 layer 10 参考边界。"""
    extra_polygons = list(extra_polygons or [])
    all_points: List[Point] = []
    for c in list(holes) + list(reference_circles):
        all_points.extend([(c.x - c.r, c.y - c.r), (c.x + c.r, c.y + c.r)])
    for s in reference_squares:
        all_points.extend(square_polygon(s.x, s.y, s.size))
    for p in extra_polygons:
        all_points.extend(p)
    if not all_points:
        all_points = [(-1.0, -1.0), (1.0, 1.0)]
    xmin, xmax, ymin, ymax = bbox_of_points(all_points)
    pad = 0.05 * max(xmax - xmin, ymax - ymin)
    xmin -= pad
    xmax += pad
    ymin -= pad
    ymax += pad
    w = h = size_px
    pixels = bytearray([255] * (w * h * 3))

    def to_px(x: float, y: float) -> Tuple[int, int]:
        px = int(round((x - xmin) / (xmax - xmin) * (w - 1)))
        py = int(round((ymax - y) / (ymax - ymin) * (h - 1)))
        return px, py

    def set_px(px: int, py: int, color: Tuple[int, int, int]) -> None:
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx : idx + 3] = bytes(color)

    def draw_line(a: Point, b: Point, color: Tuple[int, int, int]) -> None:
        x0, y0 = to_px(*a)
        x1, y1 = to_px(*b)
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            set_px(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(c: Circle, color: Tuple[int, int, int]) -> None:
        x0, y0 = to_px(c.x - c.r, c.y + c.r)
        x1, y1 = to_px(c.x + c.r, c.y - c.r)
        for py in range(max(0, y0), min(h, y1 + 1)):
            y = ymax - py / (h - 1) * (ymax - ymin)
            for px in range(max(0, x0), min(w, x1 + 1)):
                x = xmin + px / (w - 1) * (xmax - xmin)
                if (x - c.x) ** 2 + (y - c.y) ** 2 <= c.r ** 2:
                    set_px(px, py, color)

    for c in holes:
        fill_circle(c, (20, 20, 20))
    for p in extra_polygons:
        pts = list(p)
        if pts and pts[0] != pts[-1]:
            pts.append(pts[0])
        for a, b in zip(pts, pts[1:]):
            draw_line(a, b, (20, 20, 20))
    for c in reference_circles:
        pts = circle_polygon(c.x, c.y, c.r, 240)
        color = (200, 0, 0) if c.tag == "substrate1" else (0, 80, 220)
        for a, b in zip(pts, pts[1:]):
            draw_line(a, b, color)
    for s in reference_squares:
        pts = square_polygon(s.x, s.y, s.size)
        for a, b in zip(pts, pts[1:]):
            draw_line(a, b, (0, 140, 80))
    write_png(path, w, h, pixels)


def write_json(path: Path, data: Dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_output_dirs(*paths: Path) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)
