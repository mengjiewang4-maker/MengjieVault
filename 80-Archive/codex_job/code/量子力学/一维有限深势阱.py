import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def square_well_potential(x: np.ndarray, well_width: float, depth: float) -> np.ndarray:
    potential = np.zeros_like(x)
    outside = np.abs(x) > (well_width / 2.0)
    potential[outside] = depth
    return potential


def build_hamiltonian(x: np.ndarray, potential: np.ndarray) -> np.ndarray:
    dx = x[1] - x[0]
    diagonal = 2.0 / dx**2 + potential
    off_diagonal = np.full(len(x) - 1, -1.0 / dx**2)
    return np.diag(diagonal) + np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)


def normalize_states(states: np.ndarray, dx: float) -> np.ndarray:
    norms = np.sqrt(np.sum(np.abs(states) ** 2, axis=0) * dx)
    states = states / norms
    for idx in range(states.shape[1]):
        peak_index = np.argmax(np.abs(states[:, idx]))
        if states[peak_index, idx] < 0:
            states[:, idx] *= -1
    return states


def solve_bound_states(
    domain_half_width: float,
    well_width: float,
    depth: float,
    num_points: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-domain_half_width, domain_half_width, num_points)
    potential = square_well_potential(x, well_width, depth)
    hamiltonian = build_hamiltonian(x, potential)
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)

    dx = x[1] - x[0]
    eigenvectors = normalize_states(eigenvectors, dx)
    bound_mask = eigenvalues < depth
    return x, potential, eigenvalues[bound_mask], eigenvectors[:, bound_mask]


def plot_results(
    x: np.ndarray,
    potential: np.ndarray,
    energies: np.ndarray,
    states: np.ndarray,
    max_states: int,
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(9, 9), sharex=True)
    shown_states = min(max_states, len(energies))

    axes[0].plot(x, potential, color="black", linewidth=1.5, label="V(x)")
    for idx in range(shown_states):
        psi = states[:, idx]
        energy = energies[idx]
        axes[0].plot(x, psi * 0.6 + energy, label=fr"$\psi_{idx + 1}(x)$ 平移后")
        axes[0].axhline(energy, color="gray", linestyle="--", alpha=0.4)

    axes[0].set_title("一维有限深势阱束缚态")
    axes[0].set_ylabel("能量 / 平移后的波函数")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=9)

    for idx in range(shown_states):
        axes[1].plot(x, np.abs(states[:, idx]) ** 2, label=fr"$|\psi_{idx + 1}(x)|^2$")

    axes[1].set_title("概率密度")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel(r"$|\psi(x)|^2$")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="用有限差分法求解一维有限深势阱。")
    parser.add_argument("--well-width", type=float, default=2.0, help="势阱宽度。")
    parser.add_argument("--depth", type=float, default=20.0, help="阱外势能高度。")
    parser.add_argument("--domain", type=float, default=6.0, help="数值计算区域的半宽。")
    parser.add_argument("--points", type=int, default=600, help="网格点数量。")
    parser.add_argument("--states", type=int, default=4, help="最多绘制的束缚态数量。")
    parser.add_argument(
        "--output",
        type=Path,
        default=RESULTS_DIR / "一维有限深势阱.png",
        help="输出图像路径。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.well_width <= 0 or args.depth <= 0 or args.domain <= 0:
        raise ValueError("--well-width、--depth 和 --domain 必须为正数。")
    if args.points < 50:
        raise ValueError("--points 至少为 50。")
    if args.domain <= args.well_width / 2.0:
        raise ValueError("--domain 必须大于势阱半宽。")

    x, potential, energies, states = solve_bound_states(
        domain_half_width=args.domain,
        well_width=args.well_width,
        depth=args.depth,
        num_points=args.points,
    )
    if len(energies) == 0:
        raise RuntimeError("没有找到束缚态，请增大 --depth 或扩大 --domain。")

    plot_results(
        x=x,
        potential=potential,
        energies=energies,
        states=states,
        max_states=args.states,
        output_path=args.output,
    )

    print("束缚态能量：")
    for idx, energy in enumerate(energies[: args.states], start=1):
        print(f"n={idx}, E={energy:.8f}")


if __name__ == "__main__":
    main()
