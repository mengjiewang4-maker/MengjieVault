#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 COMSOL .mph 内部 XML 几何参数生成 GDS。

说明：
- 不修改 .mph 原文件；
- 优先尝试 gdstk/gdspy；
- 没有 gdstk/gdspy 时，使用 scripts/gds_utils.py 的内置 GDSII writer。
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import time
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple
from xml.etree import ElementTree as ET

from gds_utils import (
    Circle,
    Square,
    bbox_of_circles,
    run_basic_checks,
    write_gds_with_fallback,
    write_json,
    write_preview_png,
)


UNIT_TO_UM = {
    "nm": 1e-3,
    "um": 1.0,
    "µm": 1.0,
    "m": 1e6,
}


def clean_expr(expr: str) -> str:
    return (expr or "").strip().strip("'").replace("^", "**")


def eval_expr_um(expr: str, env: Dict[str, float]) -> float:
    """计算 COMSOL 表达式并统一为 um。

    这里支持本模型中出现的 a、R、r、数字、四则运算和 [nm]/[um]/[m] 单位。
    """
    expr = clean_expr(expr)
    if not expr:
        return 0.0
    if " " in expr and "*" not in expr and "[" not in expr:
        # 例如 p:pos 的 value="0 0"，外层会拆开；这里只兜底取第一个值。
        expr = expr.split()[0]

    def repl_unit(match: re.Match[str]) -> str:
        value = match.group(1)
        unit = match.group(2)
        return f"({value}*{UNIT_TO_UM[unit]})"

    expr = re.sub(
        r"([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s*\[\s*(nm|um|µm|m)\s*\]",
        repl_unit,
        expr,
    )
    allowed = {
        "pi": math.pi,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "abs": abs,
    }
    allowed.update(env)
    return float(eval(expr, {"__builtins__": {}}, allowed))


def parse_value_matrix(value_matrix: str) -> List[str]:
    """解析 COMSOL valueMatrix，例如 1|2,'0.1*a','-0.2*a'。"""
    if not value_matrix:
        return []
    found = re.findall(r"'([^']*)'", value_matrix)
    if found:
        return found
    return [v for v in re.split(r"[,| ]+", value_matrix) if v and not v.isdigit()]


def read_dmodel_from_mph(mph_path: Path) -> Tuple[bytes, str]:
    with zipfile.ZipFile(mph_path) as zf:
        names = set(zf.namelist())
        if "dmodel.xml" not in names:
            raise RuntimeError("mph 中没有 dmodel.xml，无法从内部 XML 提取几何。")
        dmodel = zf.read("dmodel.xml")
        try:
            fileversion = zf.read("fileversion").decode("utf-8", errors="replace").strip()
        except Exception:
            fileversion = "unknown"
    return dmodel, fileversion


def evaluate_parameter_expressions(raw: Dict[str, str]) -> Dict[str, Dict[str, object]]:
    """计算参数表达式。

    raw 的例子：{"a": "554[nm]", "R": "18*a", "r": "0.2*a"}。
    """
    values: Dict[str, float] = {}
    # 多轮解析，处理 R=18*a 这种依赖。
    pending = dict(raw)
    for _ in range(10):
        changed = False
        for name, expr in list(pending.items()):
            try:
                values[name] = eval_expr_um(expr, values)
                del pending[name]
                changed = True
            except Exception:
                continue
        if not changed:
            break

    result: Dict[str, Dict[str, object]] = {}
    for name, expr in raw.items():
        result[name] = {"expr": expr}
        if name in values:
            result[name]["value_um_or_scalar"] = values[name]
    return result


def parse_parameters(root: ET.Element) -> Dict[str, Dict[str, object]]:
    raw: Dict[str, str] = {}
    for expr in root.iter("expressions"):
        name = expr.attrib.get("name")
        value = expr.attrib.get("expr")
        if name and value and name not in raw:
            raw[name] = value
    return evaluate_parameter_expressions(raw)


def apply_parameter_overrides(
    params: Dict[str, Dict[str, object]],
    overrides: List[str],
) -> Dict[str, Dict[str, object]]:
    """应用命令行参数覆盖，例如 --set-param a=554[nm]。"""
    if not overrides:
        return params
    raw = {name: str(info.get("expr", "")) for name, info in params.items()}
    overridden_names = []
    for item in overrides:
        if "=" not in item:
            raise RuntimeError(f"--set-param 格式错误：{item}，应为 name=expr")
        name, expr = item.split("=", 1)
        name = name.strip()
        expr = expr.strip()
        if not name or not expr:
            raise RuntimeError(f"--set-param 格式错误：{item}，应为 name=expr")
        raw[name] = expr
        overridden_names.append(name)
    new_params = evaluate_parameter_expressions(raw)
    for name in overridden_names:
        new_params.setdefault(name, {})["overridden"] = True
    return new_params


def feature_props(feature: ET.Element) -> Dict[str, object]:
    props: Dict[str, object] = {}
    for child in feature:
        if child.tag != "propertyValue":
            continue
        name = child.attrib.get("name")
        if not name:
            continue
        if "valueMatrix" in child.attrib:
            props[name] = parse_value_matrix(child.attrib["valueMatrix"])
        elif "value" in child.attrib:
            props[name] = child.attrib["value"]
    return props


def parse_position(props: Dict[str, object], env: Dict[str, float]) -> Tuple[float, float, Dict[str, str]]:
    source = {"x": "", "y": ""}
    if "p:x" in props and "p:y" in props:
        source["x"] = str(props["p:x"])
        source["y"] = str(props["p:y"])
        return eval_expr_um(source["x"], env), eval_expr_um(source["y"], env), source
    pos = props.get("p:pos")
    if isinstance(pos, list) and len(pos) >= 2:
        source["x"] = str(pos[0])
        source["y"] = str(pos[1])
        return eval_expr_um(source["x"], env), eval_expr_um(source["y"], env), source
    if isinstance(pos, str):
        parts = pos.split()
        if len(parts) >= 2:
            source["x"], source["y"] = parts[0], parts[1]
            return eval_expr_um(parts[0], env), eval_expr_um(parts[1], env), source
    return 0.0, 0.0, source


def parse_geometry(root: ET.Element, param_values: Dict[str, float]) -> Tuple[List[Circle], List[Circle], List[Square]]:
    holes: List[Circle] = []
    reference_circles: List[Circle] = []
    reference_squares: List[Square] = []

    for feature in root.iter("GeomFeature"):
        op = feature.attrib.get("op")
        tag = feature.attrib.get("tag", "")
        props = feature_props(feature)
        if op == "Circle":
            r_expr = str(props.get("p:r", "0"))
            x, y, pos_source = parse_position(props, param_values)
            r = eval_expr_um(r_expr, param_values)
            role = "hole" if tag.startswith("circle_") else "reference_boundary"
            circle = Circle(
                tag=tag,
                x=x,
                y=y,
                r=r,
                role=role,
                source_expr={"r": r_expr, **pos_source},
            )
            if role == "hole":
                holes.append(circle)
            else:
                reference_circles.append(circle)
        elif op == "Square":
            size_expr = str(props.get("p:size", props.get("p:l", "0")))
            x, y, pos_source = parse_position(props, param_values)
            size = eval_expr_um(size_expr, param_values)
            reference_squares.append(
                Square(
                    tag=tag,
                    x=x,
                    y=y,
                    size=size,
                    role="reference_partition",
                    source_expr={"size": size_expr, **pos_source},
                )
            )

    holes.sort(key=lambda c: int(c.tag.split("_")[1]) if "_" in c.tag and c.tag.split("_")[1].isdigit() else 0)
    return holes, reference_circles, reference_squares


def scale_geometry(
    holes: List[Circle],
    reference_circles: List[Circle],
    reference_squares: List[Square],
    scale: float,
) -> None:
    """整体缩放几何。

    scale 是缩放倍数；例如 2 表示所有坐标和半径都变成原来的 2 倍。
    """
    for circle in holes + reference_circles:
        circle.x *= scale
        circle.y *= scale
        circle.r *= scale
    for square in reference_squares:
        square.x *= scale
        square.y *= scale
        square.size *= scale


def pattern_diameter_um(holes: List[Circle]) -> float:
    """孔阵列外包络直径，按最大宽/高估算。"""
    xmin, xmax, ymin, ymax = bbox_of_circles(holes)
    return max(xmax - xmin, ymax - ymin)


def first_sector_disclination_points(grid_size: int) -> List[Tuple[float, float]]:
    """生成一个 disclination 扇区的归一化孔中心坐标。

    归一化的意思是坐标单位为 a。原始 COMSOL 文件中每个扇区是 15 x 15；
    这里把同一规律扩展到更大的奇数 grid_size，例如 59 x 59。
    """
    if grid_size < 3 or grid_size % 2 == 0:
        raise RuntimeError("--extend-grid-size 必须是大于等于 3 的奇数。")
    cos18 = math.cos(math.radians(18.0))
    sin18 = math.sin(math.radians(18.0))
    dx = 0.1 * cos18
    dy = 0.1 * sin18
    first_core_y = -0.39270509831248424

    def row_offset(i: int) -> float:
        if i % 2 == 0:
            return -float(i // 2)
        return -(float(i // 2) + 0.8)

    points: List[Tuple[float, float]] = []
    for i in range(grid_size):
        ro = row_offset(i)
        for j in range(grid_size):
            if j == 0:
                if i == 0:
                    x = 3.0 * dx
                    y = first_core_y
                else:
                    x = dx
                    y = ro - 0.1 - dy
            else:
                k = (j + 1) // 2
                if j % 2 == 1:
                    x = k * cos18 - dx
                    y = ro - k * sin18 - 0.1 + dy
                else:
                    x = k * cos18 + dx
                    y = ro - k * sin18 - 0.1 - dy
            points.append((x, y))
    return points


def rotate_point(x: float, y: float, degrees: float) -> Tuple[float, float]:
    angle = math.radians(degrees)
    ca = math.cos(angle)
    sa = math.sin(angle)
    return x * ca - y * sa, x * sa + y * ca


def generated_pattern_diameter_um(grid_size: int, a_um: float, r_um: float) -> float:
    points = []
    first_sector = first_sector_disclination_points(grid_size)
    for sector in range(5):
        rotation = -72.0 * sector
        for x, y in first_sector:
            xr, yr = rotate_point(x, y, rotation)
            points.append((xr * a_um, yr * a_um))
    xmin = min(x - r_um for x, y in points)
    xmax = max(x + r_um for x, y in points)
    ymin = min(y - r_um for x, y in points)
    ymax = max(y + r_um for x, y in points)
    return max(xmax - xmin, ymax - ymin)


def choose_grid_size_for_target(target_um: float, a_um: float, r_um: float) -> int:
    """选择最接近目标外包络直径的奇数 grid_size。"""
    candidates = range(3, 301, 2)
    return min(
        candidates,
        key=lambda n: abs(generated_pattern_diameter_um(n, a_um, r_um) - target_um),
    )


def generate_extended_disclination_holes(
    grid_size: int,
    a_um: float,
    r_um: float,
) -> List[Circle]:
    holes: List[Circle] = []
    first_sector = first_sector_disclination_points(grid_size)
    index = 1
    for sector in range(5):
        rotation = -72.0 * sector
        for x_norm, y_norm in first_sector:
            x_rot, y_rot = rotate_point(x_norm, y_norm, rotation)
            holes.append(
                Circle(
                    tag=f"extended_circle_{index}",
                    x=x_rot * a_um,
                    y=y_rot * a_um,
                    r=r_um,
                    role="hole",
                    source_expr={
                        "x": f"{x_rot}*a",
                        "y": f"{y_rot}*a",
                        "r": "r",
                        "sector": str(sector),
                        "grid_size": str(grid_size),
                    },
                )
            )
            index += 1
    return holes


def write_readme(
    path: Path,
    mph_path: Path,
    gds_path: Path,
    preview_path: Path,
    params_path: Path,
    writer_used: str,
    hole_count: int,
    checks: Dict[str, object],
    scale_info: Dict[str, object],
) -> None:
    if scale_info.get("extended_grid_size"):
        geometry_source = (
            f"- 来自 COMSOL：参数 `a/R/r`、原始 5 扇区坐标规律、`substrate1`/`PML1` 参考圆、四个 `square_*` 分区边界。\n"
            f"- 手动设定：按原始规律向外扩展为 `5 x {scale_info.get('extended_grid_size')} x {scale_info.get('extended_grid_size')}` 个圆孔、圆孔多边形近似点数、layer 编号、GDS 文本标注、最小线宽/间距检查阈值。"
        )
    else:
        geometry_source = (
            "- 来自 COMSOL：参数 `a/R/r`、1125 个 `circle_*` 圆孔的位置和半径、`substrate1`/`PML1` 参考圆、四个 `square_*` 分区边界。\n"
            "- 手动设定：圆孔多边形近似点数、layer 编号、GDS 文本标注、最小线宽/间距检查阈值。"
        )
    text = f"""# COMSOL 几何到 GDS 版图

## 输入文件

- COMSOL 仿真文件：`{mph_path.name}`
- 读取来源：`.mph` 内部的 `dmodel.xml` 几何特征，而不是仿真截图。

## 输出文件

- GDS：`{gds_path.name}`
- PNG 预览：`{preview_path.name}`
- 参数 JSON：`{params_path.name}`
- 本说明：`{path.name}`

## 单位

- 脚本内部和 JSON 均使用 `um`。
- GDS library unit 为 `1 um`，数据库精度为 `1 nm`。

## Layer 定义

- layer 1：光子晶体圆孔/刻蚀图形，共 `{hole_count}` 个圆孔，多边形近似。
- layer 10：参考边界，包括 COMSOL 中的 `substrate1`、`PML1` 和四个 partition square；不建议直接作为刻蚀层。
- layer 20：文本标注。

## 缩放

- 原始孔阵列外包络直径：`{scale_info.get("original_pattern_diameter_um")}` um
- 当前缩放倍数：`{scale_info.get("scale")}`
- 当前孔阵列外包络直径：`{scale_info.get("final_pattern_diameter_um")}` um
- 扩展阵列 grid size：`{scale_info.get("extended_grid_size")}`
- 扩展阵列说明：`{scale_info.get("extension_note")}`

## 重新运行

在当前目录执行：

```bash
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph
```

如果需要改变圆孔近似精度：

```bash
python3 scripts_20260521_1/comsol_mph_to_gds.py origin/disclination_1.mph --circle-points 64
```

## 几何来源

{geometry_source}
- 未使用：微信截图/仿真场图。截图只适合人工核对外观，不适合直接加工。

## 基本检查结果

- GDS 写入方式：`{writer_used}`
- 最小孔径：`{checks.get("min_hole_diameter_um")}` um
- 最小孔边到孔边距离：`{checks.get("min_hole_edge_spacing_um")}` um
- 超出 substrate 的孔数量：`{checks.get("outside_substrate_count")}`
- 超出 PML 的孔数量：`{checks.get("outside_pml_count")}`

注意：如果最小孔间距为负数，表示同层圆孔有重叠。GDS 文件本身有效，但正式送厂前建议在 KLayout/gdstk 中做 Boolean union（布尔并集，把重叠图形合成一个图形）和工艺 DRC。
"""
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="从 COMSOL .mph 内部几何参数生成 GDS。")
    parser.add_argument("mph", nargs="?", default="origin/disclination_1.mph", help="输入 .mph 文件")
    parser.add_argument("--output-dir", default="output_20260521_1", help="输出目录")
    parser.add_argument("--output-prefix", default="disclination_from_comsol", help="输出文件名前缀")
    parser.add_argument("--circle-points", type=int, default=96, help="每个圆孔的多边形点数，建议 64 或 96")
    parser.add_argument("--set-param", action="append", default=[], help="覆盖 COMSOL 参数，例如 --set-param 'a=554[nm]' --set-param 'r=0.2*a'")
    parser.add_argument("--extend-pattern-diameter-um", type=float, default=None, help="保持 a/r 不变，向外补阵列，使孔阵列外包络直径接近该值")
    parser.add_argument("--extend-grid-size", type=int, default=None, help="手动指定扩展阵列阶数；必须为奇数，每个扇区为 N x N")
    parser.add_argument("--scale", type=float, default=1.0, help="整体缩放倍数；坐标和半径都会按此倍数缩放")
    parser.add_argument("--target-pattern-diameter-um", type=float, default=None, help="目标孔阵列外包络直径，单位 um")
    parser.add_argument("--min-feature-um", type=float, default=0.05, help="最小特征尺寸检查阈值，单位 um")
    parser.add_argument("--min-spacing-um", type=float, default=0.05, help="最小间距检查阈值，单位 um")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parents[1]
    mph_path = Path(args.mph)
    if not mph_path.is_absolute():
        mph_path = root_dir / mph_path
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = root_dir / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    dmodel_bytes, fileversion = read_dmodel_from_mph(mph_path)
    root = ET.fromstring(dmodel_bytes)
    params = parse_parameters(root)
    params = apply_parameter_overrides(params, args.set_param)
    param_values = {
        name: float(info["value_um_or_scalar"])
        for name, info in params.items()
        if "value_um_or_scalar" in info
    }
    holes, reference_circles, reference_squares = parse_geometry(root, param_values)
    if not holes:
        raise RuntimeError("没有在 dmodel.xml 中找到 circle_* 圆孔。")
    extension_note = "未扩展，使用 .mph 中原始孔坐标。"
    extended_grid_size = None
    if args.extend_pattern_diameter_um or args.extend_grid_size:
        a_um = param_values["a"]
        r_um = param_values["r"]
        extended_grid_size = args.extend_grid_size
        if extended_grid_size is None:
            extended_grid_size = choose_grid_size_for_target(
                args.extend_pattern_diameter_um,
                a_um,
                r_um,
            )
        holes = generate_extended_disclination_holes(extended_grid_size, a_um, r_um)
        extension_note = (
            f"保持 a={a_um} um、r={r_um} um 不变，"
            f"按原始 5 扇区 disclination 规律扩展为 5 x {extended_grid_size} x {extended_grid_size} 个圆孔。"
        )
    original_pattern_diameter = pattern_diameter_um(holes)
    scale = args.scale
    if args.target_pattern_diameter_um:
        scale *= args.target_pattern_diameter_um / original_pattern_diameter
    if scale <= 0:
        raise RuntimeError("--scale 必须大于 0。")
    scale_geometry(holes, reference_circles, reference_squares, scale)
    final_pattern_diameter = pattern_diameter_um(holes)
    scale_info = {
        "original_pattern_diameter_um": original_pattern_diameter,
        "scale": scale,
        "target_pattern_diameter_um": args.target_pattern_diameter_um,
        "final_pattern_diameter_um": final_pattern_diameter,
        "definition": "按 layer 1 孔阵列外包络最大宽/高作为整体直径。",
        "extend_pattern_diameter_um": args.extend_pattern_diameter_um,
        "extended_grid_size": extended_grid_size,
        "extension_note": extension_note,
    }

    prefix = args.output_prefix
    gds_path = out_dir / f"{prefix}.gds"
    preview_path = out_dir / f"{prefix}_preview.png"
    params_path = out_dir / f"{prefix}_params.json"
    if prefix == "disclination_from_comsol":
        readme_path = out_dir / "README_comsol_to_gds.md"
    else:
        readme_path = out_dir / f"README_{prefix}.md"

    checks = run_basic_checks(
        holes,
        reference_circles,
        reference_squares,
        polygon_points=args.circle_points,
        min_feature_um=args.min_feature_um,
        min_spacing_um=args.min_spacing_um,
    )
    writer_used = write_gds_with_fallback(
        gds_path,
        holes,
        reference_circles,
        reference_squares,
        polygon_points=args.circle_points,
    )
    write_preview_png(preview_path, holes, reference_circles, reference_squares)

    data = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "route": "B: 从 .mph 内部 dmodel.xml 的 COMSOL 几何参数重建 GDS",
        "source_mph": str(mph_path),
        "comsol_fileversion": fileversion,
        "units": "um",
        "gds_unit": "1 user unit = 1 um; database precision = 1 nm",
        "writer_used": writer_used,
        "layers": {
            "1": "主体刻蚀区域/光子晶体孔",
            "10": "参考边界/芯区/PML/partition square",
            "20": "文本标注",
        },
        "parameters": params,
        "feature_counts": {
            "holes": len(holes),
            "reference_circles": len(reference_circles),
            "reference_squares": len(reference_squares),
        },
        "scaling": scale_info,
        "holes": [c.__dict__ for c in holes],
        "reference_circles": [c.__dict__ for c in reference_circles],
        "reference_squares": [s.__dict__ for s in reference_squares],
        "checks": checks,
    }
    write_json(params_path, data)
    write_readme(
        readme_path,
        mph_path,
        gds_path,
        preview_path,
        params_path,
        writer_used,
        len(holes),
        checks,
        scale_info,
    )

    print(f"写入: {gds_path}")
    print(f"写入: {preview_path}")
    print(f"写入: {params_path}")
    print(f"写入: {readme_path}")
    print(f"GDS writer: {writer_used}")
    print(f"圆孔数量: {len(holes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
