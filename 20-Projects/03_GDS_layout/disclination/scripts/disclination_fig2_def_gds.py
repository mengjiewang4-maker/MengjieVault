#!/usr/bin/env python3
"""Generate Fig. 2 d/e/f C5 photonic disclination cavity GDS.

本脚本用于复现论文 "Vortex nanolaser based on a photonic disclination
cavity" Fig. 2 中 C5 added-quarter-sector 结构。Fig. 2d/e 是 TB 能级和
概率密度，Fig. 2f 是对应的 photonic disclination cavity 几何，因此这里
输出一套 C5 几何，并在 README 中说明 d/e/f 的关系。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np

# -- 项目模块路径 -----------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from disclination.geometry import (
    Fig2Parameters,
    HoleSite,
    apply_volterra_added_quarter_sector,
    generate_0325_style_c5_lattice,
    generate_square_ssh_lattice,
)
from disclination.gds_export import write_gds_klayout

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "Fig2_def_GDS_outputs_no_boundary"
PAPER_PATH = (
    "/Users/mac/Documents/mengjie/MengjieVault/90-Local_Not_Upload/PDF/papers/"
    "02_on_chip_lasers/Vortex nanolaser based on a photonic disclination cavity.pdf"
)
ORIGINAL_SCRIPT = (
    "/Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/"
    "Disclination_vortex_backup_20260519_1432/vippy_backup_20260519_1230/"
    "disclination_vortex_gds.py"
)


# ---------------------------------------------------------------------------
# 参数加载
# ---------------------------------------------------------------------------

def load_or_define_parameters(
    args: argparse.Namespace,
) -> tuple[Fig2Parameters, list[str], dict[str, Any]]:
    """读取或定义参数；当前主要参数来自论文 Extended Data Fig. 3 和本地 COMSOL 截图。

    返回值包括参数、待确认事项、参数来源说明。
    """

    output_dir = Path(args.output_dir).expanduser().resolve()

    # 论文 Extended Data Fig. 3: C5 2D FEM 参数为 a=500 nm, r0=0.20a, d0=0.45a。
    lattice_constant_um = args.lattice_constant_nm / 1000.0
    hole_radius_um = args.hole_radius_ratio * lattice_constant_um
    center_to_hole_distance_um = args.center_to_hole_ratio * lattice_constant_um

    # C5 magnified region: (dc, db, di) = (0.25a, 0.23a, 0)。
    core_shift_um = args.core_shift_ratio * lattice_constant_um
    boundary_shift_um = args.boundary_shift_ratio * lattice_constant_um
    interior_corner_shift_um = args.interior_corner_shift_ratio * lattice_constant_um

    outer_radius_um = args.outer_radius_ratio * args.lattice_range * lattice_constant_um

    params = Fig2Parameters(
        lattice_constant_um=lattice_constant_um,
        hole_radius_um=hole_radius_um,
        center_to_hole_distance_um=center_to_hole_distance_um,
        lattice_range=args.lattice_range,
        source_sector_angle_rad=math.pi / 2,
        added_sector_angle_rad=math.pi / 2,
        target_sector_count=5,
        inner_radius_um=args.inner_radius_ratio * lattice_constant_um,
        outer_radius_um=outer_radius_um,
        core_shift_um=core_shift_um,
        boundary_shift_um=boundary_shift_um,
        interior_corner_shift_um=interior_corner_shift_um,
        layer=args.layer,
        datatype=args.datatype,
        circle_points=args.circle_points,
        png_dpi=args.png_dpi,
        dbu_um=args.dbu_um,
        refractive_index=3.33,
        slab_thickness_um=0.275,
        output_dir=str(output_dir),
    )

    pending = [
        "论文 Fig. 2d/e 是 TB 结果，不是独立 GDS 几何；本脚本只输出对应 C5 photonic cavity 几何。",
        "COMSOL 目录只有截图，没有可机器读取的 mph/txt/md 参数文件；截图参数仅作为本地历史参考。",
        "论文 Extended Data Fig. 3 给出 db/di，但没有完整说明每个边界孔的逐点位移规则；当前 GDS 使用 0325 TB 风格连续点阵并显式应用核心 dc 修正，db/di 写入参数等待进一步核对。",
        "GDS 只包含平面空气孔图形；slab 厚度和折射率写入 JSON/README，供 COMSOL/Lumerical 建模使用。",
    ]

    sources = {
        "paper_fig2": "Fig. 2d/e are TB in-gap states and probability density; Fig. 2f is C5 photonic cavity and Hz modes.",
        "paper_extended_data_fig3": {
            "a": "500 nm",
            "C5_r0_d0": "(r0, d0) = (0.20a, 0.45a)",
            "C5_dc_db_di": "(dc, db, di) = (0.25a, 0.23a, 0)",
            "refractive_index": 3.33,
            "note": "These cavities are identical to Fig. 2c/f/i; C5 is Fig. 2f.",
        },
        "local_comsol_screenshots": [
            {"a": "554 nm", "R": "18a", "r": "0.20a", "n_substrate": 3.33},
            {"a": "559 nm", "R": "18a", "r": "0.20a", "n_substrate": 3.4},
            {"a": "555 nm", "R": "18a", "r": "0.15a", "n_substrate": 3.4},
        ],
        "geometry_mode": "0325_style_continuous_c5_no_visible_sector_boundaries",
        "original_script": ORIGINAL_SCRIPT,
        "paper_path": PAPER_PATH,
    }

    return params, pending, sources


# ---------------------------------------------------------------------------
# 输出辅助（PNG / JSON / README）
# ---------------------------------------------------------------------------

def export_png_preview(
    sites: list[HoleSite], params: Fig2Parameters, output_path: Path
) -> Path:
    """导出版图 PNG 预览图。"""

    if output_path.exists():
        raise FileExistsError(f"输出 PNG 已存在，避免覆盖：{output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 8))

    coords = np.array([[s.x_um, s.y_um] for s in sites])
    colors = ["#d62728" if site.role == "core_dc_adjusted" else "#1f77b4" for site in sites]
    ax.scatter(coords[:, 0], coords[:, 1], s=5.0, color=colors, alpha=0.75)
    ax.scatter([0], [0], s=8, color="black")

    ax.set_aspect("equal", adjustable="box")
    margin = params.lattice_constant_um
    ax.set_xlim(coords[:, 0].min() - margin, coords[:, 0].max() + margin)
    ax.set_ylim(coords[:, 1].min() - margin, coords[:, 1].max() + margin)
    ax.set_xlabel("x (um)")
    ax.set_ylabel("y (um)")
    ax.set_title("Fig.2 d/e/f C5 photonic disclination cavity")
    ax.grid(True, linewidth=0.25, alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path, dpi=params.png_dpi)
    plt.close(fig)
    return output_path


def write_parameters_json(
    params: Fig2Parameters,
    sites: list[HoleSite],
    pending: list[str],
    sources: dict[str, Any],
    output_path: Path,
    generated_files: dict[str, str],
) -> Path:
    """写出参数 JSON，便于后续仿真和加工记录追踪。"""

    if output_path.exists():
        raise FileExistsError(f"输出 JSON 已存在，避免覆盖：{output_path}")

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "implementation_library": "klayout.db",
        "fig2_mapping": {
            "Fig2d": "C5 TB in-gap states; not a separate GDS geometry.",
            "Fig2e": "C5 TB probability density and angular momentum classification; not a separate GDS geometry.",
            "Fig2f": "Designed C5 photonic disclination cavity and optical Hz modes; this GDS geometry corresponds to Fig.2f.",
        },
        "parameters": asdict(params),
        "hole_count": len(sites),
        "role_counts": {
            role: sum(1 for site in sites if site.role == role)
            for role in sorted({site.role for site in sites})
        },
        "pending_confirmation": pending,
        "sources": sources,
        "generated_files": generated_files,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return output_path


def write_readme(
    params: Fig2Parameters,
    sites: list[HoleSite],
    pending: list[str],
    sources: dict[str, Any],
    output_path: Path,
    generated_files: dict[str, str],
) -> Path:
    """写出输出文件夹 README。"""

    if output_path.exists():
        raise FileExistsError(f"输出 README 已存在，避免覆盖：{output_path}")

    role_counts = {
        role: sum(1 for site in sites if site.role == role)
        for role in sorted({site.role for site in sites})
    }

    lines = [
        "# Fig.2 d/e/f C5 Photonic Disclination Cavity GDS",
        "",
        "## 复现目标",
        "",
        "复现论文《Vortex nanolaser based on a photonic disclination cavity》Fig.2 中 d/e/f 对应的 C5 photonic disclination cavity。",
        "本输出不是示意图，而是可导入 KLayout/COMSOL/Lumerical 的平面空气孔 GDS。",
        "",
        "## 参考论文",
        "",
        f"- 本地论文路径：`{sources['paper_path']}`",
        "- DOI/页面：`https://www.nature.com/articles/s41566-023-01338-2`",
        "- 关键参数来源：主文 Fig.2、Methods、Extended Data Fig.3。",
        "",
        "## Fig.2 d/e/f 与 GDS 的对应关系",
        "",
        "| 图 | 内容 | 是否独立 GDS 几何 | 本输出对应关系 |",
        "|---|---|---|---|",
        "| Fig.2d | C5 symmetric disclination 的 TB in-gap states | 否 | TB 能级结果，不单独生成 GDS |",
        "| Fig.2e | 五个 C5 能态的概率密度和角动量分类 | 否 | TB 模式结果，不单独生成 GDS |",
        "| Fig.2f | C5 photonic disclination cavity 和 Hz 模式 | 是 | `fig2def_c5_no_boundary_0325_style.gds` |",
        "",
        "## 参数表",
        "",
        "| 参数 | 数值 | 来源/说明 |",
        "|---|---:|---|",
        f"| lattice constant a | {params.lattice_constant_um * 1000:.1f} nm | Extended Data Fig.3 C5 2D FEM |",
        f"| hole radius r0 | {params.hole_radius_um / params.lattice_constant_um:.3f} a = {params.hole_radius_um * 1000:.1f} nm | Extended Data Fig.3 C5 |",
        f"| center-to-hole distance d0 | {params.center_to_hole_distance_um / params.lattice_constant_um:.3f} a = {params.center_to_hole_distance_um * 1000:.1f} nm | Extended Data Fig.3 C5 |",
        f"| added sector angle | {params.added_sector_angle_rad / math.pi:.2f} pi | +1/4 sector |",
        f"| target symmetry | C{params.target_sector_count} | C5, added one sector to C4 |",
        f"| core shift dc | {params.core_shift_um / params.lattice_constant_um:.3f} a = {params.core_shift_um * 1000:.1f} nm | Extended Data Fig.3 C5 |",
        f"| boundary shift db | {params.boundary_shift_um / params.lattice_constant_um:.3f} a = {params.boundary_shift_um * 1000:.1f} nm | 记录为参数，逐点规则待确认 |",
        f"| interior corner shift di | {params.interior_corner_shift_um / params.lattice_constant_um:.3f} a | Extended Data Fig.3 C5 |",
        f"| lattice range | {params.lattice_range} unit cells per side | 可调参数 |",
        f"| GDS layer/datatype | {params.layer}/{params.datatype} | 可调参数 |",
        f"| hole count | {len(sites)} | 生成结果 |",
        "",
        "## 输出文件",
        "",
        f"- GDS：`{Path(generated_files['gds']).name}`",
        f"- PNG：`{Path(generated_files['png']).name}`",
        f"- 参数 JSON：`{Path(generated_files['json']).name}`",
        f"- README：`{Path(generated_files['readme']).name}`",
        "",
        "## 孔类型统计",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for role, count in role_counts.items():
        lines.append(f"| {role} | {count} |")

    lines.extend([
        "",
        "## 代码运行方式",
        "",
        "```bash",
        "cd /Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/disclination",
        "python3 scripts/disclination_fig2_def_gds.py",
        "```",
        "",
        "常用可调参数示例：",
        "",
        "```bash",
        "python3 scripts/disclination_fig2_def_gds.py --lattice-constant-nm 500 --hole-radius-ratio 0.20 --center-to-hole-ratio 0.45 --lattice-range 13",
        "```",
        "",
        "## 当前假设",
        "",
        "- 使用 KLayout Python API (`klayout.db`) 写 GDS。",
        "- 使用 square SSH-like 单胞：每个 C4 单胞四个圆孔，孔中心距单胞中心为 d0。",
        "- 默认使用 0325 TB 脚本风格的第一象限点阵角度映射，避免 5 个硬扇区拼接产生明显分界线。",
        "- 旧版 `generate_square_ssh_lattice + apply_volterra_added_quarter_sector` 扇区复制函数仍保留在源码中，便于对照。",
        "- GDS 仅描述空气孔平面图形；材料、厚度、PML、端口等仿真设置不在 GDS 中。",
        "",
        "## 尚未确认的问题",
        "",
    ])
    for item in pending:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## 后续导入建议",
        "",
        "### KLayout",
        "",
        "直接打开 `.gds`，检查 layer/datatype、孔径、中心五重对称结构和总尺寸。",
        "",
        "### COMSOL",
        "",
        "将 GDS 导入为二维几何后，按论文设置折射率 n=3.33；如做 3D slab，需要额外设置 slab thickness。",
        "",
        "### Lumerical",
        "",
        "可将 GDS 作为 mask 导入，再将空气孔区域设为 air，背景 slab 设为目标材料。",
        "",
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------------
# CLI & main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(
        description="Generate Fig.2 d/e/f C5 disclination cavity GDS."
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="输出目录。")
    parser.add_argument("--lattice-constant-nm", type=float, default=500.0, help="晶格常数 a，单位 nm。")
    parser.add_argument("--hole-radius-ratio", type=float, default=0.20, help="空气孔半径 r0/a。")
    parser.add_argument("--center-to-hole-ratio", type=float, default=0.45, help="单胞中心到空气孔中心距离 d0/a。")
    parser.add_argument("--lattice-range", type=int, default=13, help="原始 1/4 扇区每边单胞数。")
    parser.add_argument("--inner-radius-ratio", type=float, default=0.0, help="中心排除半径，单位 a。")
    parser.add_argument("--outer-radius-ratio", type=float, default=1.05, help="外裁剪半径比例，相对 lattice_range*a。")
    parser.add_argument("--core-shift-ratio", type=float, default=0.25, help="C5 核心孔 dc/a。")
    parser.add_argument("--boundary-shift-ratio", type=float, default=0.23, help="C5 边界孔 db/a，仅记录。")
    parser.add_argument("--interior-corner-shift-ratio", type=float, default=0.0, help="C5 内角孔 di/a，仅记录。")
    parser.add_argument("--layer", type=int, default=1, help="GDS layer。")
    parser.add_argument("--datatype", type=int, default=0, help="GDS datatype。")
    parser.add_argument("--circle-points", type=int, default=96, help="圆孔多边形顶点数。")
    parser.add_argument("--png-dpi", type=int, default=300, help="PNG 预览分辨率。")
    parser.add_argument("--dbu-um", type=float, default=0.001, help="GDS database unit，单位 um。")
    return parser.parse_args()


def main() -> None:
    """主程序入口。"""

    args = parse_args()
    params, pending, sources = load_or_define_parameters(args)
    output_dir = Path(params.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Start Fig.2 d/e/f C5 photonic disclination cavity generation")
    print("GDS library: klayout.db")
    print(f"Output directory: {output_dir}")
    print(f"Paper parameter source: Extended Data Fig.3, C5, a={params.lattice_constant_um * 1000:.1f} nm")
    print("Fig.2 d/e are TB results; Fig.2 f is the generated photonic cavity geometry.")

    sector_source_sites = generate_square_ssh_lattice(params)
    sector_reference_sites = apply_volterra_added_quarter_sector(sector_source_sites, params)
    final_sites = generate_0325_style_c5_lattice(params)

    print(f"Reference sector-copy source hole count: {len(sector_source_sites)}")
    print(f"Reference sector-copy final hole count: {len(sector_reference_sites)}")
    print(f"No-boundary 0325-style final hole count: {len(final_sites)}")
    if pending:
        print("Pending confirmation:")
        for item in pending:
            print(f"  - {item}")

    gds_path = output_dir / "fig2def_c5_no_boundary_0325_style.gds"
    png_path = output_dir / "fig2def_c5_no_boundary_0325_style_preview.png"
    json_path = output_dir / "parameters.json"
    readme_path = output_dir / "README.md"

    generated_files: dict[str, str] = {}
    generated_files["gds"] = str(write_gds_klayout(final_sites, params, gds_path))
    generated_files["png"] = str(export_png_preview(final_sites, params, png_path))
    generated_files["readme"] = str(readme_path)
    generated_files["json"] = str(
        write_parameters_json(params, final_sites, pending, sources, json_path, generated_files)
    )
    generated_files["readme"] = str(
        write_readme(params, final_sites, pending, sources, readme_path, generated_files)
    )

    print("Generated files:")
    for key, value in generated_files.items():
        print(f"  - {key}: {value}")
    print("Done")


if __name__ == "__main__":
    main()
