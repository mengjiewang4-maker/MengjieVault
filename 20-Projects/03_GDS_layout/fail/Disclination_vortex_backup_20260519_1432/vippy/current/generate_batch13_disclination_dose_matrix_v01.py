"""
Batch13 disclination vortex GDS generator with Dose/PEC mapping.

This script keeps the batch12 geometry unchanged, then creates marked
GDS copies for the batch13 dose matrix. Dose and PEC are exposure plan
metadata; they do not change the hole geometry.

术语提示：
- GDS：芯片版图文件。
- disclination：旋错缺陷。
- PEC：邻近效应修正，用于补偿电子束散射造成的额外曝光。
"""

from datetime import datetime
from pathlib import Path
import argparse
import math
import os


db = None


SCRIPT_DIR = Path(__file__).resolve().parent
VIPPY_DIR = SCRIPT_DIR.parent

BATCH_NAME = "batch13_Si_EBL"
SCRIPT_VERSION = "v01"
SAMPLE_NAME = "BATCH13_DISCLINATION"

# Fixed output roots. Do not depend on where this script is moved later.
OUTPUT_BASE_DIR = VIPPY_DIR / "outputs" / "gds" / BATCH_NAME
MAPPING_DIR = VIPPY_DIR / "outputs" / "mapping"

# ==================== 1. Geometry parameters ====================
# Keep these exactly aligned with batch12 current geometry.
PARAM_SETS = [
    {"a": 0.554, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.20},
    {"a": 0.559, "r_ratio": 0.15},
]
R = 60
N_VERTEX = 256
EPS = 1e-3
SOURCE_SECTOR_COUNT = 4
ADDED_SECTOR_COUNT = 1
TARGET_SECTOR_COUNT = SOURCE_SECTOR_COUNT + ADDED_SECTOR_COUNT
SOURCE_SECTOR_ANGLE = 2 * math.pi / SOURCE_SECTOR_COUNT
TARGET_SECTOR_ANGLE = 2 * math.pi / TARGET_SECTOR_COUNT
ANGLE_RATIO = TARGET_SECTOR_ANGLE / SOURCE_SECTOR_ANGLE
RADIUS_RATIO = SOURCE_SECTOR_COUNT / TARGET_SECTOR_COUNT
SQUARE_LATTICE_OFFSET = 0.5

# ==================== 2. Batch13 exposure plan ====================
DOSE_MATRIX = [
    {"group": "D1", "dose_percent": 20, "pec": "on", "purpose": "低剂量边界"},
    {"group": "D2", "dose_percent": 25, "pec": "on", "purpose": "候选低剂量"},
    {"group": "D3", "dose_percent": 30, "pec": "on", "purpose": "候选剂量"},
    {"group": "D4", "dose_percent": 35, "pec": "on", "purpose": "候选剂量"},
    {"group": "D5", "dose_percent": 40, "pec": "on", "purpose": "接近原最低剂量"},
    {"group": "D6", "dose_percent": 45, "pec": "on", "purpose": "第一轮 45% 对照"},
]


def unique_output_path(path):
    """
    Return a non-existing path by adding _oldNN if needed.
    """
    if not path.exists():
        return path

    for index in range(1, 100):
        candidate = path.with_name(f"{path.stem}_old{index:02d}{path.suffix}")
        if not candidate.exists():
            return candidate

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return path.with_name(f"{path.stem}_{timestamp}{path.suffix}")


def is_point_in_quadrilateral(point, radius):
    """
    Check whether a point is inside the first-quadrant square-lattice crop.
    """
    x = point[0]
    y = point[1]
    return 0 <= x < (radius - 0.5) and 0 <= y < (radius - 0.5)


def apply_disclination(point):
    """
    Map the first-quadrant 1/4 sector into the target disclination sector.
    """
    r = math.hypot(point[0], point[1])
    theta = math.atan2(point[1], point[0])

    if theta < -EPS or theta > SOURCE_SECTOR_ANGLE + EPS:
        return None

    mapped_theta = theta * ANGLE_RATIO
    mapped_r = r * RADIUS_RATIO
    return (mapped_r * math.cos(mapped_theta), mapped_r * math.sin(mapped_theta))


def insert_air_hole(cell, layer, center, radius, npts):
    """
    Insert a circular air hole into a GDS cell.
    """
    hole = db.DPolygon.ellipse(
        db.DBox(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        npts,
    )
    cell.shapes(layer).insert(hole)


def draw_vector_text(cell, layer, text, center_x, bottom_y, h):
    """
    Draw compact text using rectangles.

    Batch13 marks intentionally use only supported characters, such as
    d20-01, where d20 is dose 20% and 01 is the GDS sequence number.
    """
    width = h / 6.0
    char_w = h * 0.6
    gap = h * 0.3

    total_width = len(text) * char_w + (len(text) - 1) * gap
    curr_x = center_x - total_width / 2

    def rect(x, y, w_rect, h_rect):
        cell.shapes(layer).insert(db.DBox(x, y, x + w_rect, y + h_rect))

    for char in text:
        l, b, r, t = curr_x, bottom_y, curr_x + char_w, bottom_y + h
        m = b + h / 2

        if char == "-":
            rect(l, m - width / 2, char_w, width)
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
        elif char == "6":
            rect(l, b, width, h)
            rect(l, t - width, char_w, width)
            rect(l, m - width / 2, char_w, width)
            rect(l, b, char_w, width)
            rect(r - width, b, width, h / 2)
        elif char == "7":
            rect(l, t - width, char_w, width)
            rect(r - width, b, width, h)
        elif char == "8":
            rect(l, b, width, h)
            rect(r - width, b, width, h)
            rect(l, b, char_w, width)
            rect(l, m - width / 2, char_w, width)
            rect(l, t - width, char_w, width)
        elif char == "9":
            rect(l, m, width, h / 2)
            rect(r - width, b, width, h)
            rect(l, m - width / 2, char_w, width)
            rect(l, t - width, char_w, width)
        elif char in {"d", "D"}:
            rect(l, b, width, h)
            rect(l, t - width, char_w * 0.8, width)
            rect(l, b, char_w * 0.8, width)
            rect(l + char_w * 0.8 - width, b, width, h)

        curr_x += char_w + gap


def generate_sites(radius):
    """
    Generate the first-quadrant square lattice before disclination mapping.
    """
    site = []

    for i in range(radius):
        for j in range(radius):
            point = (i + SQUARE_LATTICE_OFFSET, j + SQUARE_LATTICE_OFFSET)
            if is_point_in_quadrilateral(point, radius):
                site.append(point)

    return site


def generate_disclination_sites(radius):
    """
    Generate 5/4 disclination lattice compressed into 360 degrees.
    """
    site = generate_sites(radius)
    stretched_sector = []

    for point in site:
        mapped_point = apply_disclination(point)
        if mapped_point is not None:
            stretched_sector.append(mapped_point)

    site_disclination = []

    for sector_index in range(TARGET_SECTOR_COUNT):
        theta = sector_index * TARGET_SECTOR_ANGLE
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        for x, y in stretched_sector:
            site_disclination.append(
                (
                    x * cos_theta - y * sin_theta,
                    x * sin_theta + y * cos_theta,
                )
            )

    return site_disclination


def format_param_token(value):
    """
    Convert a float to a filename-safe token.
    """
    return f"{value:.3f}".replace(".", "p")


def write_gds(output_filename, radius, hole_sites, lattice_a, hole_radius, mark_text):
    """
    Write one GDS file for a structure/dose combination.
    """
    if db is None:
        raise RuntimeError("klayout.db is not available. Use --dry-run to create mapping tables without writing GDS.")

    ly = db.Layout()
    ly.dbu = 0.001
    top_cell = ly.create_cell(SAMPLE_NAME)
    layer1 = ly.layer(1, 0)

    for point in hole_sites:
        insert_air_hole(top_cell, layer1, (point[0] * lattice_a, point[1] * lattice_a), hole_radius, N_VERTEX)

    mark_h = 8 * lattice_a
    mark_y = RADIUS_RATIO * 2 * radius * lattice_a + 4 * lattice_a
    draw_vector_text(top_cell, layer1, mark_text, 0, mark_y, mark_h)

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    final_filename = unique_output_path(output_filename)
    ly.write(str(final_filename))

    print("GDS saved:", final_filename.resolve())
    return final_filename


def build_output_suffix(dry_run, priority_only):
    """
    Build filename suffix for metadata files.
    """
    suffix_parts = []
    if dry_run:
        suffix_parts.append("dryrun")
    if priority_only:
        suffix_parts.append("priority")
    return "_" + "_".join(suffix_parts) if suffix_parts else ""


def write_parameter_note(output_dir, date_str, records, dry_run, priority_only):
    """
    Write batch13 parameter and dose metadata.
    """
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    suffix = build_output_suffix(dry_run, priority_only)
    note_filename = unique_output_path(output_dir / f"batch13_{date_str}_GDS参数记录{suffix}.md")

    lines = [
        "---",
        f"title: batch13 {date_str} GDS 参数记录",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "tags:",
        "  - GDS",
        "  - disclination-vortex",
        "  - batch13_Si_EBL",
        "---",
        "",
        f"# batch13 {date_str} GDS 参数记录",
        "",
        f"- 生成时间：{generated_at}",
        f"- 生成脚本：`{Path(__file__).name}`",
        f"- 脚本版本：`{SCRIPT_VERSION}`",
        f"- 输出文件夹：`{output_dir}`",
        f"- 版图名称：`{SAMPLE_NAME}`",
        f"- dry-run：`{dry_run}`",
        f"- priority-only：`{priority_only}`",
        "- 结构策略：保持 batch12 的 6 个 GDS 结构参数不变",
        "- 本轮新增：Dose/PEC 对应关系和版图 mark",
        "- 晶格类型：四角晶格，先形成 5/4 晶格，再压缩到 360 度",
        f"- 原始扇区数：{SOURCE_SECTOR_COUNT}",
        f"- 添加扇区数：{ADDED_SECTOR_COUNT}",
        f"- 最终扇区数：{TARGET_SECTOR_COUNT}",
        f"- GDS 数据库单位 dbu：0.001",
        f"- 空气孔多边形顶点数：{N_VERTEX}",
        f"- 角度映射比例 ANGLE_RATIO：{ANGLE_RATIO}",
        f"- 半径映射比例 RADIUS_RATIO：{RADIUS_RATIO}",
        f"- 裁剪容差 EPS：{EPS}",
        "",
        "## 文件参数表",
        "",
        "| 区域编号 | GDS编号 | 文件名 | 是否已生成GDS | Dose/% | PEC | R | a/um | r/a | r_hole/um | 空气孔数量 | mark |",
        "| --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for record in records:
        lines.append(
            "| {region_id} | {gds_id} | `{filename}` | {gds_written} | {dose_percent} | {pec} | {radius} | {a:.3f} | {r_ratio:.2f} | {r_hole:.6f} | {hole_count} | `{mark_text}` |".format(
                **record
            )
        )

    note_filename.write_text("\n".join(lines), encoding="utf-8")
    print("参数记录已保存:", note_filename.resolve())
    return note_filename


def write_region_mapping(output_dir, date_str, records, dry_run, priority_only):
    """
    Write the GDS-Dose-PEC-region mapping table for EBL and SEM.
    """
    suffix = build_output_suffix(dry_run, priority_only)
    mapping_filename = unique_output_path(MAPPING_DIR / f"batch13_{date_str}_GDS_Dose_PEC_区域对应表{suffix}.md")

    lines = [
        "---",
        f"title: batch13 {date_str} GDS-Dose-PEC-区域对应表",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "tags:",
        "  - batch13_Si_EBL",
        "  - EBL",
        "  - SEM",
        "  - mapping",
        "---",
        "",
        f"# batch13 {date_str} GDS-Dose-PEC-区域对应表",
        "",
        f"- GDS 输出文件夹：`{output_dir}`",
        f"- PEC 状态：`on` 表示建议在 JBX-6300FS 上开启 PEC。",
        f"- dry-run：`{dry_run}`",
        f"- priority-only：`{priority_only}`",
        "",
        "| 区域编号 | GDS编号 | GDS文件名 | 是否已生成GDS | Dose百分比 | PEC状态 | 预期观察 | SEM文件名 | 结论 |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]

    for record in records:
        lines.append(
            "| {region_id} | {gds_id} | `{filename}` | {gds_written} | {dose_percent} | {pec} | 中心是否孔连；边缘是否正常 |  |  |".format(
                **record
            )
        )

    mapping_filename.write_text("\n".join(lines), encoding="utf-8")
    print("区域对应表已保存:", mapping_filename.resolve())
    return mapping_filename


def build_structure_variants():
    """
    Build full-size and half-size site arrays once, then reuse them.
    """
    site_disclination = generate_disclination_sites(R)
    r_half = R // 2
    site_disclination_half = generate_disclination_sites(r_half)

    variants = []
    for index, params in enumerate(PARAM_SETS, start=1):
        full_seq = (index - 1) * 2 + 1
        half_seq = full_seq + 1
        variants.append(
            {
                "seq": full_seq,
                "gds_id": f"GDS_{full_seq:02d}",
                "radius": R,
                "a": params["a"],
                "r_ratio": params["r_ratio"],
                "sites": site_disclination,
                "hole_count": len(site_disclination),
            }
        )
        variants.append(
            {
                "seq": half_seq,
                "gds_id": f"GDS_{half_seq:02d}",
                "radius": r_half,
                "a": params["a"],
                "r_ratio": params["r_ratio"],
                "sites": site_disclination_half,
                "hole_count": len(site_disclination_half),
            }
        )

    return variants


def parse_args():
    """
    Parse command-line options.
    """
    parser = argparse.ArgumentParser(
        description="Generate batch13 disclination GDS files and Dose/PEC mapping tables."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only write expected filename and region mapping tables. Do not import KLayout or write GDS.",
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check klayout.db import, then exit without writing files.",
    )
    parser.add_argument(
        "--priority-only",
        action="store_true",
        help="Use only the recommended compact dose set: 25, 30, 35 and 40 percent.",
    )
    args, _unknown = parser.parse_known_args()
    env_dry_run = os.environ.get("BATCH13_DRY_RUN", "").strip().lower()
    env_check_deps = os.environ.get("BATCH13_CHECK_DEPS", "").strip().lower()
    env_priority_only = os.environ.get("BATCH13_PRIORITY_ONLY", "").strip().lower()
    if env_dry_run in {"1", "true", "yes", "on"}:
        args.dry_run = True
    if env_check_deps in {"1", "true", "yes", "on"}:
        args.check_deps = True
    if env_priority_only in {"1", "true", "yes", "on"}:
        args.priority_only = True
    return args


def load_klayout():
    """
    Import KLayout only when real GDS writing is requested.
    """
    global db
    import klayout.db as klayout_db

    db = klayout_db


def check_dependencies():
    """
    Check runtime dependencies without generating files.
    """
    load_klayout()
    print("Dependency check OK: klayout.db is available.")


def build_structure_variants_dry_run():
    """
    Build metadata-only variants without NumPy.

    Hole counts come from the verified batch12 20260517 parameter record.
    """
    variants = []
    for index, params in enumerate(PARAM_SETS, start=1):
        full_seq = (index - 1) * 2 + 1
        half_seq = full_seq + 1
        variants.append(
            {
                "seq": full_seq,
                "gds_id": f"GDS_{full_seq:02d}",
                "radius": R,
                "a": params["a"],
                "r_ratio": params["r_ratio"],
                "sites": None,
                "hole_count": 17405,
            }
        )
        variants.append(
            {
                "seq": half_seq,
                "gds_id": f"GDS_{half_seq:02d}",
                "radius": R // 2,
                "a": params["a"],
                "r_ratio": params["r_ratio"],
                "sites": None,
                "hole_count": 4205,
            }
        )

    return variants


def main():
    args = parse_args()
    if args.check_deps:
        check_dependencies()
        return

    if not args.dry_run:
        load_klayout()

    date_str = datetime.now().strftime("%Y%m%d")
    output_dir = OUTPUT_BASE_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    MAPPING_DIR.mkdir(parents=True, exist_ok=True)

    variants = build_structure_variants_dry_run() if args.dry_run else build_structure_variants()
    dose_matrix = (
        [dose for dose in DOSE_MATRIX if dose["dose_percent"] in {25, 30, 35, 40}]
        if args.priority_only
        else DOSE_MATRIX
    )
    generation_records = []
    region_index = 1

    for dose in dose_matrix:
        for variant in variants:
            a = variant["a"]
            r_hole = variant["r_ratio"] * a
            a_token = format_param_token(a)
            r_token = format_param_token(r_hole)
            mark_text = f"d{dose['dose_percent']}-{variant['seq']:02d}"
            filename = (
                output_dir
                / f"batch13_{date_str}_{dose['group']}_dose{dose['dose_percent']:02d}_pec_{dose['pec']}_GDS{variant['seq']:02d}_a{a_token}_r{r_token}.gds"
            )

            if args.dry_run:
                final_filename = unique_output_path(filename)
                gds_written = "否"
                print("Dry-run expected GDS:", final_filename.resolve())
            else:
                final_filename = write_gds(
                    filename,
                    variant["radius"],
                    variant["sites"],
                    a,
                    r_hole,
                    mark_text,
                )
                gds_written = "是"

            generation_records.append(
                {
                    "region_id": f"A{region_index:02d}",
                    "gds_id": variant["gds_id"],
                    "filename": final_filename.name,
                    "gds_written": gds_written,
                    "dose_group": dose["group"],
                    "dose_percent": dose["dose_percent"],
                    "pec": dose["pec"],
                    "radius": variant["radius"],
                    "a": a,
                    "r_ratio": variant["r_ratio"],
                    "r_hole": r_hole,
                    "hole_count": variant["hole_count"],
                    "mark_text": mark_text,
                    "purpose": dose["purpose"],
                }
            )
            region_index += 1

    write_parameter_note(output_dir, date_str, generation_records, args.dry_run, args.priority_only)
    write_region_mapping(output_dir, date_str, generation_records, args.dry_run, args.priority_only)


if __name__ == "__main__":
    main()
