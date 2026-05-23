"""Geometry helpers for disclination layouts."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Hole:
    """One circular air hole in micrometer units."""

    x_um: float
    y_um: float
    radius_um: float


@dataclass(frozen=True)
class HoleSite:
    """一个空气孔中心和半径，附带角色标记（bulk / core_dc_adjusted 等）。"""

    x_um: float
    y_um: float
    radius_um: float
    role: str


@dataclass(frozen=True)
class Fig2Parameters:
    """保存 Fig. 2 C5 结构参数。单位默认使用 um。"""

    lattice_constant_um: float
    hole_radius_um: float
    center_to_hole_distance_um: float
    lattice_range: int
    source_sector_angle_rad: float
    added_sector_angle_rad: float
    target_sector_count: int
    inner_radius_um: float
    outer_radius_um: float
    core_shift_um: float
    boundary_shift_um: float
    interior_corner_shift_um: float
    layer: int
    datatype: int
    circle_points: int
    png_dpi: int
    dbu_um: float
    refractive_index: float
    slab_thickness_um: float | None
    output_dir: str


# ---------------------------------------------------------------------------
# Placeholder helpers (used by generate_disclination_gds.py)
# ---------------------------------------------------------------------------

def build_lattice(
    period_um: float = 0.56,
    radius_um: float = 0.10,
    nx: int = 3,
    ny: int = 3,
) -> list[Hole]:
    """Build a small placeholder square lattice.

    This is intentionally minimal. Replace it later with the validated
    disclination geometry generator.
    """

    if period_um <= 0:
        raise ValueError("period_um must be positive")
    if radius_um <= 0:
        raise ValueError("radius_um must be positive")
    if nx <= 0 or ny <= 0:
        raise ValueError("nx and ny must be positive")

    x0 = -(nx - 1) * period_um / 2
    y0 = -(ny - 1) * period_um / 2
    holes: list[Hole] = []
    for ix in range(nx):
        for iy in range(ny):
            holes.append(
                Hole(
                    x_um=x0 + ix * period_um,
                    y_um=y0 + iy * period_um,
                    radius_um=radius_um,
                )
            )
    return holes


# ---------------------------------------------------------------------------
# Fig.2 C5 photonic disclination cavity geometry (论文复现核心)
# ---------------------------------------------------------------------------

def generate_square_ssh_lattice(params: Fig2Parameters) -> list[HoleSite]:
    """生成原始 C4 square SSH-like lattice 的 1/4 扇区空气孔坐标。

    每个方形单胞有四个空气孔，孔中心位于单胞中心到四个角方向的 d0 距离。
    """

    a = params.lattice_constant_um
    d_axis = params.center_to_hole_distance_um / math.sqrt(2.0)
    sites: list[HoleSite] = []
    seen: set[tuple[int, int]] = set()

    for ix in range(params.lattice_range):
        for iy in range(params.lattice_range):
            cell_center = np.array([(ix + 0.5) * a, (iy + 0.5) * a])
            offsets = [
                np.array([d_axis, d_axis]),
                np.array([-d_axis, d_axis]),
                np.array([-d_axis, -d_axis]),
                np.array([d_axis, -d_axis]),
            ]
            for offset in offsets:
                xy = cell_center + offset
                radius = float(np.linalg.norm(xy))
                theta = math.atan2(float(xy[1]), float(xy[0]))
                if radius < params.inner_radius_um or radius > params.outer_radius_um:
                    continue
                if theta < -1e-9 or theta > params.source_sector_angle_rad + 1e-9:
                    continue
                key = (
                    round(float(xy[0]) / params.dbu_um),
                    round(float(xy[1]) / params.dbu_um),
                )
                if key in seen:
                    continue
                seen.add(key)
                sites.append(
                    HoleSite(
                        float(xy[0]),
                        float(xy[1]),
                        params.hole_radius_um,
                        "bulk_source_sector",
                    )
                )

    return sites


def apply_volterra_added_quarter_sector(
    source_sites: list[HoleSite], params: Fig2Parameters
) -> list[HoleSite]:
    """把 90 度 C4 原始扇区压缩为 72 度，并复制 5 份形成 added 1/4 sector C5 结构。"""

    angle_ratio = (
        (2 * math.pi / params.target_sector_count) / params.source_sector_angle_rad
    )
    radius_ratio = 4.0 / params.target_sector_count
    target_sector_angle = 2 * math.pi / params.target_sector_count
    all_sites: list[HoleSite] = []

    for source in source_sites:
        x, y = source.x_um, source.y_um
        r = math.hypot(x, y)
        theta = math.atan2(y, x)
        mapped_r = r * radius_ratio
        mapped_theta = theta * angle_ratio

        # 按论文 C5 参数应用核心孔 dc 修正：靠近中心的一圈孔径向移动到 dc。
        role = "bulk"
        if mapped_r < 0.45 * params.lattice_constant_um:
            mapped_r = params.core_shift_um
            role = "core_dc_adjusted"

        base = np.array(
            [mapped_r * math.cos(mapped_theta), mapped_r * math.sin(mapped_theta)]
        )

        for sector_index in range(params.target_sector_count):
            rotation = sector_index * target_sector_angle
            cos_t = math.cos(rotation)
            sin_t = math.sin(rotation)
            rot_x = base[0] * cos_t - base[1] * sin_t
            rot_y = base[0] * sin_t + base[1] * cos_t
            all_sites.append(
                HoleSite(float(rot_x), float(rot_y), params.hole_radius_um, role)
            )

    return remove_duplicate_or_overlapping_holes(all_sites, params)


def generate_0325_style_c5_lattice(params: Fig2Parameters) -> list[HoleSite]:
    """生成 0325 TB 脚本风格的 C5 几何，避免明显的扇区拼接分界线。

    旧版 0325 脚本不是先裁一个完整 90 度扇区再复制，而是从第一象限的
    square SSH 点阵直接做角度映射。这样得到的点阵纹理更接近用户截图左图。
    """

    a = params.lattice_constant_um
    d_axis = params.center_to_hole_distance_um / math.sqrt(2.0)
    angle_ratio = (
        (2 * math.pi / params.target_sector_count) / params.source_sector_angle_rad
    )
    target_sector_angle = 2 * math.pi / params.target_sector_count
    sites: list[HoleSite] = []

    for ix in range(params.lattice_range):
        for iy in range(params.lattice_range):
            cell_center = np.array([ix * a, iy * a])
            offsets = [
                np.array([-d_axis, -d_axis]),
                np.array([d_axis, -d_axis]),
                np.array([-d_axis, d_axis]),
                np.array([d_axis, d_axis]),
            ]
            for offset in offsets:
                xy = cell_center + offset
                if xy[0] < -1e-9 or xy[1] < -1e-9:
                    continue

                source_r = float(np.linalg.norm(xy))
                if source_r < params.inner_radius_um:
                    continue

                mapped_theta = math.atan2(float(xy[1]), float(xy[0])) * angle_ratio
                mapped_r = source_r
                if mapped_r > params.outer_radius_um:
                    continue

                role = "bulk_0325_style"
                if mapped_r < 0.45 * params.lattice_constant_um:
                    mapped_r = params.core_shift_um
                    role = "core_dc_adjusted"

                base = np.array(
                    [mapped_r * math.cos(mapped_theta), mapped_r * math.sin(mapped_theta)]
                )
                for sector_index in range(params.target_sector_count):
                    rotation = sector_index * target_sector_angle
                    cos_t = math.cos(rotation)
                    sin_t = math.sin(rotation)
                    rot_x = base[0] * cos_t - base[1] * sin_t
                    rot_y = base[0] * sin_t + base[1] * cos_t
                    sites.append(
                        HoleSite(float(rot_x), float(rot_y), params.hole_radius_um, role)
                    )

    return remove_duplicate_or_overlapping_holes(sites, params)


def remove_duplicate_or_overlapping_holes(
    sites: list[HoleSite], params: Fig2Parameters
) -> list[HoleSite]:
    """去掉重复或明显重叠的孔，避免 GDS 中出现不可加工的重复圆孔。"""

    min_center_distance = max(params.hole_radius_um * 1.20, params.dbu_um)
    result: list[HoleSite] = []

    for site in sorted(
        sites, key=lambda h: (math.hypot(h.x_um, h.y_um), math.atan2(h.y_um, h.x_um))
    ):
        too_close = False
        for kept in result:
            if math.hypot(site.x_um - kept.x_um, site.y_um - kept.y_um) < min_center_distance:
                too_close = True
                break
        if not too_close:
            result.append(site)

    return result
