#!/usr/bin/env python3
"""Compare the old 0325 C5 TB geometry with the new Fig.2 GDS geometry."""

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
OUTPUT_DIR = PROJECT_ROOT / "Fig2_0325_comparison_outputs"
OLD_SCRIPT_PATH = (
    "/Users/mac/Documents/mengjie/MengjieVault/20-Projects/03_GDS_layout/"
    "Disclination_vortex_old/03_paper_figure2_derivation_by_mengjie/"
    "03_c5_mode_analysis/c5_cell_center_cut_mode_workflow_0325.py"
)
NEW_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "disclination_fig2_def_gds.py"

from disclination.geometry import (
    generate_0325_style_c5_lattice,
    generate_square_ssh_lattice,
)


def generate_old_0325_geometry() -> tuple[np.ndarray, dict[str, Any]]:
    """按旧 0325 脚本的写法生成 TB site 坐标。"""

    target_n = 5
    nx, ny = 8, 8
    a = 1.0
    delta = 0.2

    q1_atoms = []
    for i in range(nx):
        for j in range(ny):
            cx, cy = i * a, j * a
            basis = np.array(
                [
                    [cx - delta, cy - delta],
                    [cx + delta, cy - delta],
                    [cx - delta, cy + delta],
                    [cx + delta, cy + delta],
                ]
            )
            for atom in basis:
                if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                    q1_atoms.append(atom)

    q1_pos = np.array(q1_atoms)
    coeff = (360.0 / target_n) / 90.0
    stretched = []
    for x, y in q1_pos:
        radius = math.hypot(float(x), float(y))
        phi = math.atan2(float(y), float(x)) * coeff
        stretched.append([radius * math.cos(phi), radius * math.sin(phi)])

    stretched_unit = np.array(stretched)
    final_pos = []
    for sector_index in range(target_n):
        theta = sector_index * (2 * math.pi / target_n)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        final_pos.extend(stretched_unit @ rot.T)

    pos = np.array(final_pos)
    pos = pos[np.linalg.norm(pos, axis=1) < nx * a * 0.85]
    meta = {
        "target_n": target_n,
        "Nx": nx,
        "Ny": ny,
        "a_dimensionless": a,
        "delta": delta,
        "effective_d0_over_a": math.sqrt(2.0) * delta,
        "q1_atom_count": int(len(q1_pos)),
        "final_site_count": int(len(pos)),
    }
    return pos, meta


def load_new_fig2_module():
    """加载新 GDS 生成脚本中的函数，不重新运行主程序。"""

    spec = importlib.util.spec_from_file_location("disclination_fig2_def_gds", NEW_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {NEW_SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def generate_new_fig2_geometry() -> tuple[np.ndarray, dict[str, Any]]:
    """调用新脚本函数生成 Fig.2 C5 GDS 孔位中心。"""

    module = load_new_fig2_module()
    args = module.parse_args()
    args.output_dir = str(OUTPUT_DIR / "unused_generation_dir")
    params, pending, sources = module.load_or_define_parameters(args)
    source_sites = generate_square_ssh_lattice(params)
    final_sites = generate_0325_style_c5_lattice(params)
    pos = np.array([[site.x_um, site.y_um] for site in final_sites])
    meta = {
        "lattice_constant_um": params.lattice_constant_um,
        "hole_radius_um": params.hole_radius_um,
        "d0_over_a": params.center_to_hole_distance_um / params.lattice_constant_um,
        "core_shift_over_a": params.core_shift_um / params.lattice_constant_um,
        "boundary_shift_over_a": params.boundary_shift_um / params.lattice_constant_um,
        "lattice_range": params.lattice_range,
        "source_sector_count": int(len(source_sites)),
        "final_hole_count": int(len(final_sites)),
        "pending_confirmation": pending,
        "sources": sources,
    }
    return pos, meta


def geometry_metrics(pos: np.ndarray) -> dict[str, Any]:
    """计算坐标点集的基础几何指标。"""

    radius = np.linalg.norm(pos, axis=1)
    return {
        "count": int(len(pos)),
        "bbox": {
            "xmin": float(pos[:, 0].min()),
            "ymin": float(pos[:, 1].min()),
            "xmax": float(pos[:, 0].max()),
            "ymax": float(pos[:, 1].max()),
        },
        "radius_min": float(radius.min()),
        "radius_max": float(radius.max()),
        "radius_mean": float(radius.mean()),
    }


def export_comparison_png(old_pos: np.ndarray, new_pos: np.ndarray, output_path: Path) -> Path:
    """导出旧 TB 几何与新 GDS 几何的并排对比图。"""

    if output_path.exists():
        raise FileExistsError(output_path)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].scatter(old_pos[:, 0], old_pos[:, 1], s=8, c="#4c72b0", alpha=0.75)
    axes[0].set_title("Old 0325 TB geometry\nunitless sites")
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].grid(True, linewidth=0.25, alpha=0.35)
    axes[0].set_xlabel("x / a")
    axes[0].set_ylabel("y / a")

    axes[1].scatter(new_pos[:, 0], new_pos[:, 1], s=5, c="#dd8452", alpha=0.75)
    axes[1].set_title("New Fig.2 GDS geometry\nhole centers in um")
    axes[1].set_aspect("equal", adjustable="box")
    axes[1].grid(True, linewidth=0.25, alpha=0.35)
    axes[1].set_xlabel("x (um)")
    axes[1].set_ylabel("y (um)")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def write_outputs(old_pos: np.ndarray, old_meta: dict[str, Any], new_pos: np.ndarray, new_meta: dict[str, Any]) -> None:
    """写出比较 JSON、PNG 和 README。"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUTPUT_DIR / "0325_tb_vs_fig2_gds_geometry_comparison.png"
    json_path = OUTPUT_DIR / "comparison_metrics.json"
    readme_path = OUTPUT_DIR / "README.md"

    if png_path.exists() or json_path.exists() or readme_path.exists():
        raise FileExistsError(f"Comparison output already exists in {OUTPUT_DIR}")

    export_comparison_png(old_pos, new_pos, png_path)

    payload = {
        "old_script": OLD_SCRIPT_PATH,
        "new_script": str(NEW_SCRIPT_PATH),
        "old_meta": old_meta,
        "new_meta": new_meta,
        "old_metrics": geometry_metrics(old_pos),
        "new_metrics": geometry_metrics(new_pos),
        "main_difference": [
            "Old script is a TB/mode-analysis script and does not output GDS.",
            "New script is a fabrication-oriented GDS generator and does not solve TB modes.",
            "Old uses dimensionless delta=0.2, equivalent d0/a=sqrt(2)*delta=0.2828.",
            "New uses paper Extended Data Fig.3 C5 parameter d0/a=0.45 and r0/a=0.20.",
        ],
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 0325 TB Script vs Fig.2 GDS Script Comparison",
        "",
        "## 文件",
        "",
        f"- 旧脚本：`{OLD_SCRIPT_PATH}`",
        f"- 新脚本：`{NEW_SCRIPT_PATH}`",
        "",
        "## 关键结论",
        "",
        "- 旧脚本是 TB/SSH 模式求解探索脚本，不生成 GDS。",
        "- 新脚本是 Fig.2 C5 photonic cavity 的 GDS 生成脚本，不求解 TB 模式。",
        "- 两者都使用 C5 的 90° -> 72° Volterra 角度压缩逻辑。",
        "- 两者的单胞内部点位不同：旧脚本用 `delta=0.2`，等效 `d0/a=0.2828`；新脚本用论文参数 `d0/a=0.45`。",
        "",
        "## 定量对比",
        "",
        "| 项目 | 旧 0325 TB 脚本 | 新 Fig.2 GDS 脚本 |",
        "|---|---:|---:|",
        f"| 原始 1/4 扇区点数 | {old_meta['q1_atom_count']} | {new_meta['source_sector_count']} |",
        f"| 最终点/孔数 | {old_meta['final_site_count']} | {new_meta['final_hole_count']} |",
        f"| d0/a | {old_meta['effective_d0_over_a']:.4f} | {new_meta['d0_over_a']:.4f} |",
        f"| 结构范围参数 | Nx=Ny={old_meta['Nx']} | lattice_range={new_meta['lattice_range']} |",
        "",
        "## 输出",
        "",
        f"- 对比图：`{png_path.name}`",
        f"- 指标 JSON：`{json_path.name}`",
        "",
        "## 下一步建议",
        "",
        "如果要让 GDS 和 TB 严格一致，应把新脚本生成的孔位中心作为 TB site，重新构建 Hamiltonian，避免几何和模式计算使用两套不同坐标。",
    ]
    readme_path.write_text("\n".join(lines), encoding="utf-8")

    print("Generated comparison outputs:")
    print(f"  - {png_path}")
    print(f"  - {json_path}")
    print(f"  - {readme_path}")


def main() -> None:
    """主入口。"""

    old_pos, old_meta = generate_old_0325_geometry()
    new_pos, new_meta = generate_new_fig2_geometry()
    write_outputs(old_pos, old_meta, new_pos, new_meta)


if __name__ == "__main__":
    main()
