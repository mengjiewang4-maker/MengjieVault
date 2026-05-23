"""
用 KLayout Python API 生成四角晶格切开并添加 1/4 扇区后的 disclination vortex 版图。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import klayout.db as db
import numpy as np
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent

# ==================== 1. 参数设置 ====================
PARAM_SETS = [
    {"a": 0.554, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.15},
]
R = 60               # quadrilateral half-side length in lattice units
n_vertex = 256       # polygon vertex count for each air hole
eps = 1e-3           # angular tolerance for sector clipping
source_sector_count = 4
added_sector_count = 1
target_sector_count = source_sector_count + added_sector_count
source_sector_angle = 2 * np.pi / source_sector_count
target_sector_angle = 2 * np.pi / target_sector_count
angle_ratio = target_sector_angle / source_sector_angle  # 5/4 圈晶格压缩到 360 度，90 度压缩成 72 度
radius_ratio = source_sector_count / target_sector_count # 与角度压缩同步的半径比例
square_lattice_offset = 0.5  # 让切割线落在格点之间，避免拼接边界重叠
sample_name = "DISCLINATION_VORTEX"
OUTPUT_BASE_DIR = ROOT

def is_point_in_quadrilateral(point, radius):
    """
    判断一个二维点是否位于第一象限的四角晶格裁剪区域内。
    """
    x = point[0]
    y = point[1]
    return 0 <= x < (radius - 0.5) and 0 <= y < (radius - 0.5)


def apply_disclination(point):
    """
    把第一象限的 1/4 四角晶格扇区映射到目标扇区。
    """
    r = np.linalg.norm(point)
    theta = np.arctan2(point[1], point[0])

    if theta < -eps or theta > source_sector_angle + eps:
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
    生成切开后的四角/方形晶格 1/4 扇区。

    这里先只生成第一象限的方形晶格。后面的 generate_disclination_sites()
    会把这个 1/4 扇区复制成 5 份，相当于在原来的四角晶格中额外加 1/4 晶格。
    """
    site = []

    for i in range(radius):
        for j in range(radius):
            point = np.array([i + square_lattice_offset, j + square_lattice_offset])
            if is_point_in_quadrilateral(point, radius):
                site.append(point)

    return np.array(site)


def generate_disclination_sites(radius):
    """
    先生成 1/4 方形晶格，再映射、旋转复制成 5/4 晶格压缩到 360 度后的结构。
    """
    site = generate_sites(radius)
    stretched_sector = []

    for point in site:
        mapped_point = apply_disclination(point)
        if mapped_point is not None:
            stretched_sector.append(mapped_point)

    stretched_sector = np.array(stretched_sector)
    site_disclination = []

    for sector_index in range(target_sector_count):
        theta = sector_index * target_sector_angle
        rotation = np.array(
            [
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)],
            ]
        )
        site_disclination.extend(stretched_sector @ rotation.T)

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

    output_filename.parent.mkdir(parents=True, exist_ok=True)

    ly.write(str(output_filename))

    print("GDS saved:", output_filename.resolve())


def write_parameter_note(output_dir, date_str, records):
    """
    写出一份 Markdown 参数记录，方便之后在 Obsidian 里查看每个 GDS 的来源。
    """
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note_filename = output_dir / f"mj{date_str}_GDS参数记录.md"

    lines = [
        "---",
        f"title: mj{date_str} GDS 参数记录",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "tags:",
        "  - GDS",
        "  - disclination-vortex",
        "  - vippy",
        "---",
        "",
        f"# mj{date_str} GDS 参数记录",
        "",
        f"- 生成时间：{generated_at}",
        f"- 生成脚本：`{Path(__file__).name}`",
        f"- 输出文件夹：`{output_dir}`",
        f"- 版图名称：`{sample_name}`",
        "- 晶格类型：四角晶格，先形成 5/4 晶格，再压缩到 360 度",
        f"- 原始扇区数：{source_sector_count}",
        f"- 添加扇区数：{added_sector_count}",
        f"- 最终扇区数：{target_sector_count}",
        f"- GDS 数据库单位 dbu：0.001",
        f"- 空气孔多边形顶点数：{n_vertex}",
        f"- 角度映射比例 angle_ratio：{angle_ratio}",
        f"- 半径映射比例 radius_ratio：{radius_ratio}",
        f"- 裁剪容差 eps：{eps}",
        "",
        "## 文件参数表",
        "",
        "| 序号 | 文件名 | R | a | r/a | r_hole | 空气孔数量 | GDS 标注 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for record in records:
        lines.append(
            "| {seq:02d} | `{filename}` | {radius} | {a:.3f} | {r_ratio:.2f} | {r_hole:.6f} | {hole_count} | `{label_text}` |".format(
                **record
            )
        )

    lines.extend(
        [
            "",
            "## 参数说明",
            "",
            "- `R`：裁剪区域半径，数字越大，生成的结构范围越大。",
            "- `a`：晶格常数，也就是相邻晶格点的基础距离。",
            "- `r/a`：空气孔半径相对晶格常数的比例。",
            "- `r_hole`：实际写入 GDS 的空气孔半径，计算方式是 `r_hole = a * r/a`。",
            "- `空气孔数量`：该 GDS 文件中写入的孔数量。",
            "",
        ]
    )

    note_filename.write_text("\n".join(lines), encoding="utf-8")
    print("参数记录已保存:", note_filename.resolve())


# ==================== 3. 生成点并保存 ====================
site_disclination = generate_disclination_sites(R)
R_half = R // 2
site_disclination_halfR = generate_disclination_sites(R_half)

date_str = datetime.now().strftime("%Y%m%d")
OUTPUT_DIR = OUTPUT_BASE_DIR / date_str
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
generation_records = []

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

    generation_records.append(
        {
            "seq": full_seq,
            "filename": filename.name,
            "radius": R,
            "a": a,
            "r_ratio": params["r_ratio"],
            "r_hole": r_hole,
            "hole_count": len(site_disclination),
            "label_text": label_text,
        }
    )
    generation_records.append(
        {
            "seq": half_seq,
            "filename": half_filename.name,
            "radius": R_half,
            "a": a,
            "r_ratio": params["r_ratio"],
            "r_hole": r_hole,
            "hole_count": len(site_disclination_halfR),
            "label_text": label_text,
        }
    )

    print(f"完成！文件已保存为: {filename}，参数: R={R}, a={a}, r_ratio={params['r_ratio']}, r_hole={r_hole}")
    print(f"完成！半径减半文件已保存为: {half_filename}，参数: R={R_half}, a={a}, r_ratio={params['r_ratio']}, r_hole={r_hole}")

write_parameter_note(OUTPUT_DIR, date_str, generation_records)
