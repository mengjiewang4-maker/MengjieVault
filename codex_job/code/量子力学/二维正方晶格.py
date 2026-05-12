import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def generate_square_lattice(size: int, spacing: float) -> tuple[list[float], list[float]]:
    """生成二维正方晶格的坐标。"""
    xs: list[float] = []
    ys: list[float] = []

    for row in range(size):
        for col in range(size):
            xs.append(col * spacing)
            ys.append(row * spacing)

    return xs, ys


def plot_square_lattice(size: int, spacing: float) -> None:
    """用 matplotlib 绘制二维正方晶格并保存图像。"""
    xs, ys = generate_square_lattice(size, spacing)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(xs, ys, s=80, color="#1f77b4")
    ax.set_title(f"二维正方晶格 ({size}x{size})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.4)

    padding = spacing * 0.5
    max_coord = (size - 1) * spacing
    ax.set_xlim(-padding, max_coord + padding)
    ax.set_ylim(-padding, max_coord + padding)

    plt.tight_layout()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "二维正方晶格.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="绘制二维正方晶格。")
    parser.add_argument("--size", type=int, default=5, help="每条边上的晶格点数量。")
    parser.add_argument("--spacing", type=float, default=1.0, help="相邻晶格点之间的间距。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.size <= 0:
        raise ValueError("--size 必须为正整数。")
    if args.spacing <= 0:
        raise ValueError("--spacing 必须为正数。")
    plot_square_lattice(size=args.size, spacing=args.spacing)


if __name__ == "__main__":
    main()
