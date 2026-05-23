#!/usr/bin/env python3
"""Run a sparse tight-binding check on all generated Fig.2 GDS hole centers."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.spatial import cKDTree


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
FIG2_SCRIPT = PROJECT_ROOT / "scripts" / "disclination_fig2_def_gds.py"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "Fig2_GDS_site_sparse_TB_outputs"

from disclination.geometry import (
    generate_0325_style_c5_lattice,
)


def load_fig2_module():
    """加载 Fig.2 GDS 脚本中的几何函数，但不执行它的 main。"""

    spec = importlib.util.spec_from_file_location("disclination_fig2_def_gds", FIG2_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {FIG2_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def default_fig2_args(output_dir: Path) -> SimpleNamespace:
    """构造和 GDS 生成脚本一致的默认参数。"""

    return SimpleNamespace(
        output_dir=str(output_dir),
        lattice_constant_nm=500.0,
        hole_radius_ratio=0.20,
        center_to_hole_ratio=0.45,
        lattice_range=13,
        inner_radius_ratio=0.0,
        outer_radius_ratio=1.05,
        core_shift_ratio=0.25,
        boundary_shift_ratio=0.23,
        interior_corner_shift_ratio=0.0,
        layer=1,
        datatype=0,
        circle_points=96,
        png_dpi=300,
        dbu_um=0.001,
    )


def load_gds_site_geometry(output_dir: Path) -> tuple[np.ndarray, list[str], Any, list[str], dict[str, Any]]:
    """复用 GDS 脚本，得到最终孔中心坐标和参数。"""

    module = load_fig2_module()
    params, pending, sources = module.load_or_define_parameters(default_fig2_args(output_dir))
    final_sites = generate_0325_style_c5_lattice(params)
    pos = np.array([[site.x_um, site.y_um] for site in final_sites], dtype=float)
    roles = [site.role for site in final_sites]
    return pos, roles, params, pending, sources


def select_core_sites(pos: np.ndarray, roles: list[str], radius_um: float) -> tuple[np.ndarray, list[str], np.ndarray]:
    """选择中心附近孔位，用于快速调试。"""

    radial = np.linalg.norm(pos, axis=1)
    mask = radial <= radius_um
    indices = np.flatnonzero(mask)
    return pos[mask], [roles[i] for i in indices], indices


def choose_sites(
    pos: np.ndarray,
    roles: list[str],
    analysis_radius_um: float | None,
) -> tuple[np.ndarray, list[str], np.ndarray]:
    """默认使用全部 GDS 孔位；给半径时只取中心区域做快速调试。"""

    if analysis_radius_um is None:
        indices = np.arange(len(pos), dtype=int)
        return pos, roles, indices
    return select_core_sites(pos, roles, analysis_radius_um)


def estimate_bond_distances(
    lattice_constant_um: float,
    center_to_hole_distance_um: float,
    tolerance: float,
) -> dict[str, float]:
    """给距离近邻模型估计 strong/weak bond 的判据。"""

    delta_axis = center_to_hole_distance_um / math.sqrt(2.0)
    radius_ratio = 4.0 / 5.0
    strong_distance = max((lattice_constant_um - 2.0 * delta_axis) * radius_ratio, lattice_constant_um * 0.05)
    weak_distance = (2.0 * delta_axis) * radius_ratio
    return {
        "strong_distance_um": strong_distance,
        "weak_distance_um": weak_distance,
        "split_distance_um": 0.5 * (strong_distance + weak_distance),
        "max_bond_distance_um": weak_distance * (1.0 + tolerance),
    }


def build_sparse_tb_hamiltonian(
    pos: np.ndarray,
    roles: list[str],
    lattice_constant_um: float,
    center_to_hole_distance_um: float,
    t_strong: float,
    t_weak: float,
    t_core: float,
    tolerance: float,
) -> tuple[sp.csr_matrix, dict[str, Any]]:
    """根据 GDS 孔位中心构建稀疏 tight-binding 哈密顿量。

    稀疏矩阵：只存非零耦合项。对 2250 个孔位来说，大多数孔位之间没有直接耦合，
    所以用 scipy.sparse 比普通二维大数组更合适。
    """

    n = len(pos)
    distances = estimate_bond_distances(lattice_constant_um, center_to_hole_distance_um, tolerance)
    max_bond_distance = distances["max_bond_distance_um"]
    split_distance = distances["split_distance_um"]

    tree = cKDTree(pos)
    pairs = tree.query_pairs(max_bond_distance, output_type="ndarray")
    if pairs.size == 0:
        hamiltonian = sp.csr_matrix((n, n), dtype=float)
        return hamiltonian, {
            "site_count": n,
            **distances,
            "strong_bond_count": 0,
            "weak_bond_count": 0,
            "core_bond_count": 0,
            "total_bond_count": 0,
            "matrix_shape": [n, n],
            "matrix_nnz": 0,
            "matrix_format": "csr",
        }

    deltas = pos[pairs[:, 0]] - pos[pairs[:, 1]]
    pair_distances = np.linalg.norm(deltas, axis=1)

    strong_count = 0
    weak_count = 0
    core_count = 0
    values = np.empty(len(pairs), dtype=float)

    for k, ((i, j), d) in enumerate(zip(pairs, pair_distances)):
        if d <= 1e-9:
            values[k] = 0.0
            continue
        if roles[i] == "core_dc_adjusted" and roles[j] == "core_dc_adjusted":
            values[k] = t_core
            core_count += 1
        elif d <= split_distance:
            values[k] = t_strong
            strong_count += 1
        else:
            values[k] = t_weak
            weak_count += 1

    valid = values != 0.0
    rows = np.concatenate([pairs[valid, 0], pairs[valid, 1]])
    cols = np.concatenate([pairs[valid, 1], pairs[valid, 0]])
    data = np.concatenate([values[valid], values[valid]])
    hamiltonian = sp.coo_matrix((data, (rows, cols)), shape=(n, n), dtype=float).tocsr()

    meta = {
        "site_count": n,
        **distances,
        "strong_bond_count": strong_count,
        "weak_bond_count": weak_count,
        "core_bond_count": core_count,
        "total_bond_count": strong_count + weak_count + core_count,
        "matrix_shape": [n, n],
        "matrix_nnz": int(hamiltonian.nnz),
        "matrix_format": "csr",
    }
    return hamiltonian, meta


def solve_sparse_near_zero_modes(
    hamiltonian: sp.csr_matrix,
    mode_count: int,
    spectrum_count: int,
    sigma: float,
    tol: float,
    maxiter: int | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    """用 scipy.sparse.linalg.eigsh 求近零本征模式。

    eigsh：稀疏矩阵的本征值求解器。`sigma=0` 表示优先找最靠近零能的本征值。
    """

    n = hamiltonian.shape[0]
    if n < 2:
        raise ValueError("Need at least 2 sites to solve eigenmodes.")

    k = min(max(mode_count, spectrum_count), n - 2)
    try:
        eigenvalues, eigenvectors = spla.eigsh(
            hamiltonian,
            k=k,
            sigma=sigma,
            which="LM",
            tol=tol,
            maxiter=maxiter,
        )
        method = "scipy.sparse.linalg.eigsh(sigma)"
    except RuntimeError:
        eigenvalues, eigenvectors = spla.eigsh(
            hamiltonian,
            k=k,
            which="SM",
            tol=tol,
            maxiter=maxiter,
        )
        method = "scipy.sparse.linalg.eigsh(SM fallback)"

    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    selected = np.argsort(np.abs(eigenvalues))[:mode_count]
    selected = selected[np.argsort(eigenvalues[selected])]
    return eigenvalues, eigenvectors, selected, method


def export_spectrum(eigenvalues: np.ndarray, selected: np.ndarray, output_path: Path) -> Path:
    """导出近零能谱图。"""

    if output_path.exists():
        raise FileExistsError(output_path)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(eigenvalues))
    ax.plot(x, eigenvalues, ".", ms=4, color="#4c72b0", label="computed sparse eigenvalues")
    ax.plot(selected, eigenvalues[selected], "o", ms=6, color="#d62728", label="selected near-zero modes")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("computed mode rank")
    ax.set_ylabel("TB eigenvalue")
    ax.set_title("Sparse near-zero TB spectrum from Fig.2 GDS hole centers")
    ax.legend()
    ax.grid(True, linewidth=0.25, alpha=0.35)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def export_mode_maps(pos: np.ndarray, eigenvectors: np.ndarray, eigenvalues: np.ndarray, selected: np.ndarray, output_path: Path) -> Path:
    """导出近零模式空间分布图。"""

    if output_path.exists():
        raise FileExistsError(output_path)
    cols = 3
    rows = math.ceil(len(selected) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.0 * rows), squeeze=False)
    for ax, idx in zip(axes.ravel(), selected):
        mode = eigenvectors[:, idx]
        amp = np.abs(mode) ** 2
        size = 8 + 1800 * amp / max(float(amp.max()), 1e-12)
        sc = ax.scatter(pos[:, 0], pos[:, 1], c=np.sign(mode), s=size, cmap="coolwarm", vmin=-1, vmax=1, alpha=0.85)
        ax.set_title(f"rank={idx}, E={eigenvalues[idx]:.4f}")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linewidth=0.25, alpha=0.25)
        ax.set_xlabel("x (um)")
        ax.set_ylabel("y (um)")
    for ax in axes.ravel()[len(selected):]:
        ax.axis("off")
    fig.colorbar(sc, ax=axes.ravel().tolist(), shrink=0.75, label="mode sign")
    fig.suptitle("Sparse near-zero TB modes on Fig.2 GDS hole centers", y=0.995)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def write_json(output_path: Path, payload: dict[str, Any]) -> Path:
    """写出 JSON 结果。"""

    if output_path.exists():
        raise FileExistsError(output_path)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def write_readme(output_path: Path, payload: dict[str, Any]) -> Path:
    """写出 README。"""

    if output_path.exists():
        raise FileExistsError(output_path)
    lines = [
        "# TB From Fig.2 GDS Sites",
        "",
        "本目录使用新 Fig.2 GDS 生成脚本的全部孔位中心作为 TB site，构建 scipy.sparse 稀疏 Hamiltonian 并求近零模式。",
        "",
        "## 重要说明",
        "",
        "- 这是几何一致性检查，不是论文完整 TB 复现。",
        "- `scipy.sparse` 是稀疏矩阵工具，只保存非零耦合项，适合 2250 个孔位的 Hamiltonian。",
        "- 默认使用全部 GDS 孔位；如需快速调试，可用 `--analysis-radius-um` 只取中心区域。",
        "- 这里的 strong/weak bond 用距离近邻近似分类，仍需要后续和论文完整 coupling rule 对齐。",
        "",
        "## 参数",
        "",
        f"- analysis radius: `{payload['analysis_radius_um']} um`" if payload["analysis_radius_um"] is not None else "- analysis radius: `None`，使用全部孔位",
        f"- selected site count: `{payload['selected_site_count']}`",
        f"- total GDS site count: `{payload['total_gds_site_count']}`",
        f"- Hamiltonian shape: `{payload['bond_meta']['matrix_shape']}`",
        f"- Hamiltonian non-zero entries: `{payload['bond_meta']['matrix_nnz']}`",
        f"- eigensolver: `{payload['eigensolver']}`",
        f"- t_strong: `{payload['couplings']['t_strong']}`",
        f"- t_weak: `{payload['couplings']['t_weak']}`",
        f"- t_core: `{payload['couplings']['t_core']}`",
        "",
        "## 输出",
        "",
        "- `tb_spectrum_from_gds_sites.png`：能谱图",
        "- `tb_near_zero_modes_from_gds_sites.png`：近零模式图",
        "- `tb_from_gds_sites_results.json`：数值结果",
        "",
        "## 近零本征值",
        "",
    ]
    for item in payload["selected_modes"]:
        lines.append(f"- computed rank `{item['computed_rank']}`: E = `{item['eigenvalue']:.6f}`")
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "如果需要更接近论文 Fig.2d/e，应显式实现论文 Extended Data Fig.2/3 中的 boundary coupling rule，而不只按距离把键分成 strong/weak。",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="TB check using Fig.2 GDS hole centers.")
    parser.add_argument("--output-dir", default=None, help="输出目录；默认写入 Fig2_GDS_site_sparse_TB_outputs。")
    parser.add_argument("--analysis-radius-um", type=float, default=None, help="中心分析半径，单位 um；默认不裁剪，使用全部孔位。")
    parser.add_argument("--mode-count", type=int, default=9, help="输出最接近零能的模式数量。")
    parser.add_argument("--spectrum-count", type=int, default=80, help="用于画近零能谱的稀疏本征值数量。")
    parser.add_argument("--t-strong", type=float, default=-1.0, help="strong bond hopping。")
    parser.add_argument("--t-weak", type=float, default=-0.2, help="weak bond hopping。")
    parser.add_argument("--t-core", type=float, default=-1.0 / math.sqrt(2.0), help="core hopping。")
    parser.add_argument("--distance-tolerance", type=float, default=0.35, help="近邻距离容差。")
    parser.add_argument("--sigma", type=float, default=0.0, help="eigsh shift-invert 目标能量；0 表示找近零模式。")
    parser.add_argument("--eigsh-tol", type=float, default=1e-10, help="eigsh 收敛容差。")
    parser.add_argument("--eigsh-maxiter", type=int, default=None, help="eigsh 最大迭代次数；默认交给 scipy。")
    return parser.parse_args()


def resolve_output_dir(output_dir_arg: str | None) -> Path:
    """解析输出目录；默认目录已有内容时自动使用带时间戳的新目录。"""

    explicit = output_dir_arg is not None
    output_dir = Path(output_dir_arg).expanduser().resolve() if explicit else DEFAULT_OUTPUT_DIR.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        if explicit:
            raise FileExistsError(f"Output directory is not empty: {output_dir}")
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = output_dir.with_name(f"{output_dir.name}_run_{stamp}")
    return output_dir


def main() -> None:
    """主程序入口。"""

    args = parse_args()
    output_dir = resolve_output_dir(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pos_all, roles_all, params, pending, sources = load_gds_site_geometry(output_dir)
    pos, roles, selected_indices = choose_sites(pos_all, roles_all, args.analysis_radius_um)
    hamiltonian, bond_meta = build_sparse_tb_hamiltonian(
        pos,
        roles,
        params.lattice_constant_um,
        params.center_to_hole_distance_um,
        args.t_strong,
        args.t_weak,
        args.t_core,
        args.distance_tolerance,
    )
    eigenvalues, eigenvectors, selected_modes, eigensolver = solve_sparse_near_zero_modes(
        hamiltonian,
        args.mode_count,
        args.spectrum_count,
        args.sigma,
        args.eigsh_tol,
        args.eigsh_maxiter,
    )

    spectrum_path = export_spectrum(eigenvalues, selected_modes, output_dir / "tb_spectrum_from_gds_sites.png")
    modes_path = export_mode_maps(pos, eigenvectors, eigenvalues, selected_modes, output_dir / "tb_near_zero_modes_from_gds_sites.png")

    payload = {
        "total_gds_site_count": int(len(pos_all)),
        "selected_site_count": int(len(pos)),
        "analysis_radius_um": args.analysis_radius_um,
        "selected_original_indices": selected_indices.tolist(),
        "uses_all_gds_sites": bool(len(pos) == len(pos_all)),
        "couplings": {
            "t_strong": args.t_strong,
            "t_weak": args.t_weak,
            "t_core": args.t_core,
            "distance_tolerance": args.distance_tolerance,
        },
        "bond_meta": bond_meta,
        "eigensolver": eigensolver,
        "computed_eigenvalues": [float(v) for v in eigenvalues],
        "selected_modes": [
            {"computed_rank": int(idx), "eigenvalue": float(eigenvalues[idx])}
            for idx in selected_modes
        ],
        "parameters": {
            "lattice_constant_um": params.lattice_constant_um,
            "hole_radius_um": params.hole_radius_um,
            "center_to_hole_distance_um": params.center_to_hole_distance_um,
            "core_shift_um": params.core_shift_um,
        },
        "pending_confirmation_from_gds_script": pending,
        "sources": sources,
        "generated_files": {
            "spectrum_png": str(spectrum_path),
            "modes_png": str(modes_path),
            "json": str(output_dir / "tb_from_gds_sites_results.json"),
            "readme": str(output_dir / "README.md"),
        },
    }
    json_path = write_json(output_dir / "tb_from_gds_sites_results.json", payload)
    readme_path = write_readme(output_dir / "README.md", payload)

    print("TB from Fig.2 GDS sites complete")
    print("Hamiltonian type: scipy.sparse csr_matrix")
    print(f"Total GDS sites: {len(pos_all)}")
    print(f"Selected sites: {len(pos)}")
    print(f"Matrix shape: {bond_meta['matrix_shape']}")
    print(f"Matrix nnz: {bond_meta['matrix_nnz']}")
    print(f"Total bonds: {bond_meta['total_bond_count']}")
    print(f"Eigensolver: {eigensolver}")
    print("Near-zero modes:")
    for item in payload["selected_modes"]:
        print(f"  - computed rank {item['computed_rank']}: E={item['eigenvalue']:.6f}")
    print("Generated files:")
    print(f"  - {spectrum_path}")
    print(f"  - {modes_path}")
    print(f"  - {json_path}")
    print(f"  - {readme_path}")


if __name__ == "__main__":
    main()
