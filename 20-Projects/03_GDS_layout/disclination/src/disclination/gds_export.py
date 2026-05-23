"""GDS export helpers (gdspy + klayout backends)."""

from __future__ import annotations

from pathlib import Path

from .geometry import Hole, HoleSite, Fig2Parameters


# ---------------------------------------------------------------------------
# gdspy backend (placeholder / simple lattice)
# ---------------------------------------------------------------------------

def write_gds(
    holes: list[Hole], output_path: str | Path, *, overwrite: bool = False
) -> Path:
    """Write circular holes to a GDS file using gdspy.

    The file is not overwritten unless overwrite=True.
    """

    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Output already exists: {path}")

    try:
        import gdspy
    except ImportError as exc:
        raise ImportError(
            "gdspy is required to write GDS. Install it from environment.yml first."
        ) from exc

    path.parent.mkdir(parents=True, exist_ok=True)
    gdspy.current_library = gdspy.GdsLibrary()
    lib = gdspy.GdsLibrary(unit=1e-6, precision=1e-9)
    cell = lib.new_cell("DISCLINATION_PLACEHOLDER")

    for hole in holes:
        cell.add(
            gdspy.Round(
                (hole.x_um, hole.y_um),
                hole.radius_um,
                number_of_points=64,
                layer=1,
            )
        )

    lib.write_gds(str(path))
    return path


# ---------------------------------------------------------------------------
# klayout backend (Fig.2 C5 photonic disclination cavity)
# ---------------------------------------------------------------------------

def _ensure_klayout() -> None:
    """Raise a clear error if klayout.db is not importable."""
    try:
        import klayout.db  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "缺少 klayout.db。请先安装 klayout，"
            "或使用 /Applications/klayout.app/Contents/MacOS/klayout 运行。"
        ) from exc


def create_circular_holes(
    cell,  # klayout.db.Cell
    layer_index: int,
    sites: list[HoleSite],
    params: Fig2Parameters,
) -> None:
    """在 klayout Cell 中创建圆形空气孔。"""
    import klayout.db as db

    for site in sites:
        box = db.DBox(
            site.x_um - site.radius_um,
            site.y_um - site.radius_um,
            site.x_um + site.radius_um,
            site.y_um + site.radius_um,
        )
        circle = db.DPolygon.ellipse(box, params.circle_points)
        cell.shapes(layer_index).insert(circle)


def write_gds_klayout(
    sites: list[HoleSite], params: Fig2Parameters, output_path: Path
) -> Path:
    """使用 klayout.db 导出真实 GDS 文件（Fig.2 C5 cavity）。"""

    _ensure_klayout()
    import klayout.db as db

    if output_path.exists():
        raise FileExistsError(f"输出 GDS 已存在，避免覆盖：{output_path}")

    layout = db.Layout()
    layout.dbu = params.dbu_um
    top = layout.create_cell("FIG2_DEF_C5_PHOTONIC_DISCLINATION_CAVITY")
    layer_index = layout.layer(params.layer, params.datatype)
    create_circular_holes(top, layer_index, sites, params)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    layout.write(str(output_path))
    return output_path
