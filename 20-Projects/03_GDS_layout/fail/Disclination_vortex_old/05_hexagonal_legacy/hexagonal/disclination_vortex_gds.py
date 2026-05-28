"""
用 KLayout Python API 生成六边形 disclination vortex 空气孔版图，并按不同晶格常数/孔半径批量导出 GDS。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import klayout.db as db
import numpy as np
from pathlib import Path
from datetime import datetime

# ==================== 1. 参数设置 ====================
PARAM_SETS = [
    {"a": 0.554, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.15},
]
R = 60               # hexagon radius in lattice units
n_vertex = 256       # polygon vertex count for each air hole
eps = 1e-3           # angular tolerance for sector clipping
angle_ratio = 6 / 5  # disclination angular remap
radius_ratio = 6 / 5 # disclination radial remap
sample_name = "DISCLINATION_VORTEX"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

def is_point_in_hexagon(point, radius):
    """
    判断一个二维点是否位于六边形样品边界内。
    """
    x = np.abs(point[0])
    y = np.abs(point[1])
    return x < (radius - 0.5) * np.sqrt(3) and (x / 2 + y * np.sqrt(3) / 2) < (
        radius - 0.5
    ) * np.sqrt(3)


def apply_disclination(point):
    """
    把原始坐标映射到旋错后的坐标；超出保留角区的点返回 None 或被重新映射。
    """
    r = np.linalg.norm(point)
    theta = np.arctan2(point[1], point[0])

    if np.abs(theta) >= np.pi * 5 / 6 - eps:
        return None

    mapped_theta = theta * angle_ratio
    mapped_r = r * radius_ratio
    return np.array([mapped_r * np.cos(mapped_theta), mapped_r * np.sin(mapped_theta)])


def insert_air_hole(cell, layer, center, radius, npts):
    """
    在指定 GDS cell 和 layer 上插入一个圆形空气孔。
    """
    hole = db.DPolygon.ellipse(
        db.DBox(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        npts,
    )
    cell.shapes(layer).insert(hole)


def draw_vector_text(cell, layer, text, center_x, bottom_y, h):
    """
    用矩形拼出简单矢量文字，便于在 GDS 中标注参数。
    """
    width = h / 6.0
    char_w = h * 0.6
    gap = h * 0.3

    total_width = len(text) * char_w + (len(text) - 1) * gap
    curr_x = center_x - total_width / 2

    def rect(x, y, w_rect, h_rect):
        """
        在当前文字绘制位置插入一个矩形笔画。
        """
        cell.shapes(layer).insert(db.DBox(x, y, x + w_rect, y + h_rect))

    for char in text:
        l, b, r, t = curr_x, bottom_y, curr_x + char_w, bottom_y + h
        m = b + h / 2

        if char in {"w", "W"}:
            rect(l, b, width, h)
            rect(r - width, b, width, h)
            rect(l + char_w / 2 - width / 2, b, width, h * 0.6)
            rect(l, b, char_w, width)
        elif char == "-":
            rect(l, m - width / 2, char_w, width)
        elif char == "=":
            rect(l, m + width, char_w, width)
            rect(l, m - width * 2, char_w, width)
        elif char == "0":
            rect(l, b, width, h)
            rect(r - width, b, width, h)
            rect(l, b, char_w, width)
            rect(l, t - width, char_w, width)
        elif char == "1":
            rect(l + char_w / 2, b, width, h)
        elif char == "2":
            rect(l, t - width, char_w, width)
            rect(r - width, m, width, h / 2)
            rect(l, m - width / 2, char_w, width)
            rect(l, b, width, h / 2)
            rect(l, b, char_w, width)
        elif char == "3":
            rect(l, t - width, char_w, width)
            rect(r - width, b, width, h)
            rect(l, m - width / 2, char_w, width)
            rect(l, b, char_w, width)
        elif char == "4":
            rect(l, m, width, h / 2)
            rect(r - width, b, width, h)
            rect(l, m - width / 2, char_w, width)
        elif char == "5":
            rect(l, t - width, char_w, width)
            rect(l, m, width, h / 2)
            rect(l, m - width / 2, char_w, width)
            rect(r - width, b, width, h / 2)
            rect(l, b, char_w, width)
        elif char in {"d", "D"}:
            rect(l, b, width, h)
            rect(l, t - width, char_w * 0.8, width)
            rect(l, b, char_w * 0.8, width)
            rect(l + char_w * 0.8 - width, b, width, h)
        elif char in {"i", "I"}:
            rect(l + char_w / 2 - width / 2, b, width, h)
        elif char in {"s", "S"}:
            rect(l, t - width, char_w, width)
            rect(l, m - width / 2, char_w, width)
            rect(l, b, char_w, width)
            rect(l, m, width, h / 2)
            rect(r - width, b, width, h / 2)
        elif char in {"c", "C"}:
            rect(l, t - width, char_w, width)
            rect(l, b, char_w, width)
            rect(l, b, width, h)
        elif char in {"o", "O"}:
            rect(l, b, width, h)
            rect(r - width, b, width, h)
            rect(l, b, char_w, width)
            rect(l, t - width, char_w, width)
        elif char in {"v", "V"}:
            rect(l, b + h * 0.3, width, h * 0.7)
            rect(r - width, b + h * 0.3, width, h * 0.7)
            rect(l + char_w / 2 - width / 2, b, width, h * 0.45)

        curr_x += char_w + gap


def generate_sites(radius):
    """
    生成未施加旋错前的基础晶格点。
    """
    a1 = np.array([np.sqrt(3) / 2, 1 / 2])
    a2 = np.array([np.sqrt(3) / 2, -1 / 2])
    site = []

    for i in range(-2 * radius, 2 * radius + 1):
        for j in range(-2 * radius, 2 * radius + 1):
            if is_point_in_hexagon((i + 1 / 3) * a1 + (j + 1 / 3) * a2, radius):
                site.append((i + 1 / 3) * a1 + (j + 1 / 3) * a2)
            if is_point_in_hexagon((i + 2 / 3) * a1 + (j + 2 / 3) * a2, radius):
                site.append((i + 2 / 3) * a1 + (j + 2 / 3) * a2)

    return np.array(site)


def generate_disclination_sites(radius):
    """
    先生成基础晶格，再逐点施加旋错映射。
    """
    site = generate_sites(radius)
    site_disclination = []

    for point in site:
        mapped_point = apply_disclination(point)
        if mapped_point is not None:
            site_disclination.append(mapped_point)

    return np.array(site_disclination)


def format_param_token(value):
    """
    把浮点数转成适合文件名和版图标注的短字符串。
    """
    return f"{value:.3f}".replace(".", "p")


def write_gds(output_filename, radius, hole_sites, lattice_a, hole_radius, label_text):
    """
    根据点坐标、晶格常数和孔半径写出一个 GDS 文件。
    """
    ly = db.Layout()
    ly.dbu = 0.001
    top_cell = ly.create_cell(sample_name)
    layer1 = ly.layer(1, 0)

    for point in hole_sites:
        insert_air_hole(top_cell, layer1, point * lattice_a, hole_radius, n_vertex)

    mark_h = 8 * lattice_a
    mark_y = radius_ratio * 2 * radius * lattice_a + 4 * lattice_a
    draw_vector_text(top_cell, layer1, label_text, 0, mark_y, mark_h)

    ly.write(output_filename)

# ==================== 3. 生成点并保存 ====================
site_disclination = generate_disclination_sites(R)
R_half = R // 2
site_disclination_halfR = generate_disclination_sites(R_half)

date_str = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR.mkdir(exist_ok=True)

for index, params in enumerate(PARAM_SETS, start=1):
    a = params["a"]
    r_hole = params["r_ratio"] * a
    a_token = format_param_token(a)
    r_token = format_param_token(r_hole)
    label_text = f"a{a_token}_r{r_token}"
    full_seq = (index - 1) * 2 + 1
    half_seq = full_seq + 1

    filename = OUTPUT_DIR / f"mj{date_str}_{full_seq:02d}.gds"
    half_filename = OUTPUT_DIR / f"mj{date_str}_{half_seq:02d}.gds"

    write_gds(filename, R, site_disclination, a, r_hole, label_text)
    write_gds(half_filename, R_half, site_disclination_halfR, a, r_hole, label_text)

    print(f"完成！文件已保存为: {filename}，参数: R={R}, a={a}, r_ratio={params['r_ratio']}, r_hole={r_hole}")
    print(f"完成！半径减半文件已保存为: {half_filename}，参数: R={R_half}, a={a}, r_ratio={params['r_ratio']}, r_hole={r_hole}")
