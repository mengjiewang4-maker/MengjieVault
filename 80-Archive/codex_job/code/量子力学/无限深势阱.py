import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def analytic_energy(n: int, length: float) -> float:
    return (n**2 * np.pi**2) / (length**2)


def analytic_wavefunction(n: int, x: np.ndarray, length: float) -> np.ndarray:
    return np.sqrt(2.0 / length) * np.sin(n * np.pi * x / length)


def build_hamiltonian(num_points: int, length: float) -> tuple[np.ndarray, np.ndarray]:
    dx = length / (num_points + 1)
    diagonal = np.full(num_points, 2.0 / dx**2)
    off_diagonal = np.full(num_points - 1, -1.0 / dx**2)
    hamiltonian = np.diag(diagonal) + np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
    x_interior = np.linspace(dx, length - dx, num_points)
    return x_interior, hamiltonian


def numerical_solutions(num_points: int, length: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_interior, hamiltonian = build_hamiltonian(num_points, length)
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)

    dx = x_interior[1] - x_interior[0]
    eigenvectors /= np.sqrt(np.sum(np.abs(eigenvectors) ** 2, axis=0) * dx)

    # 修正本征矢量的任意符号，使数值解与解析解方向一致。
    for idx in range(eigenvectors.shape[1]):
        if eigenvectors[0, idx] < 0:
            eigenvectors[:, idx] *= -1

    return x_interior, eigenvalues, eigenvectors


def plot_results(length: float, num_states: int, num_points: int, output_path: Path) -> None:
    x = np.linspace(0.0, length, 1000)
    x_num, numerical_energies, numerical_vectors = numerical_solutions(num_points, length)

    fig, axes = plt.subplots(2, 1, figsize=(9, 9), sharex=False)

    for n in range(1, num_states + 1):
        psi = analytic_wavefunction(n, x, length)
        axes[0].plot(x, np.abs(psi) ** 2, label=fr"$|\psi_{n}(x)|^2$")

    axes[0].set_title("无限深势阱概率密度")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel(r"$|\psi_n(x)|^2$")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    for n in range(1, num_states + 1):
        analytic = analytic_wavefunction(n, x_num, length)
        numeric = numerical_vectors[:, n - 1]
    axes[1].plot(x_num, analytic, linewidth=2, label=fr"解析 $\psi_{n}$")
    axes[1].plot(x_num, numeric, "--", linewidth=1.5, label=fr"数值 $\psi_{n}$")

    axes[1].set_title("有限差分与解析本征函数对比")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel(r"$\psi_n(x)$")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(ncol=2, fontsize=9)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    print("n  analytic_E        numeric_E         abs_error")
    for n in range(1, num_states + 1):
        analytic_e = analytic_energy(n, length)
        numeric_e = numerical_energies[n - 1]
        print(f"{n:<2d} {analytic_e:<16.8f} {numeric_e:<16.8f} {abs(analytic_e - numeric_e):.3e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="无限深势阱的解析解与有限差分数值解对比。")
    parser.add_argument("--length", type=float, default=1.0, help="势阱宽度 L。")
    parser.add_argument("--states", type=int, default=3, help="要绘制和比较的本征态数量。")
    parser.add_argument("--points", type=int, default=200, help="有限差分内部网格点数。")
    parser.add_argument(
        "--output",
        type=Path,
        default=RESULTS_DIR / "无限深势阱.png",
        help="输出图像路径。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.length <= 0:
        raise ValueError("--length 必须为正数。")
    if args.states <= 0:
        raise ValueError("--states 必须为正整数。")
    if args.points < 3:
        raise ValueError("--points 至少为 3。")

    plot_results(
        length=args.length,
        num_states=args.states,
        num_points=args.points,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
