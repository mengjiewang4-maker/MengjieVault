"""
Chapter 7 computational notes: matrix representations and basis changes.

The examples use finite-dimensional truncations, so they illustrate matrix
structure rather than exact infinite-dimensional identities.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "results" / ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / "results" / ".cache"))

import matplotlib.pyplot as plt
import numpy as np


PLOT_DIR = ROOT / "results" / "plots"


def rotation_unitary(theta: float) -> np.ndarray:
    return np.array(
        [
            [np.cos(theta / 2.0), -np.sin(theta / 2.0)],
            [np.sin(theta / 2.0), np.cos(theta / 2.0)],
        ]
    )


def harmonic_oscillator_matrices(size: int = 8) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    a = np.zeros((size, size), dtype=complex)
    for n in range(1, size):
        a[n - 1, n] = np.sqrt(n)
    adag = a.conj().T
    x = (a + adag) / np.sqrt(2.0)
    p = 1j * (adag - a) / np.sqrt(2.0)
    h = adag @ a + 0.5 * np.eye(size)
    return x, p, h


def plot_unitary_basis_transform() -> None:
    theta = np.deg2rad(55.0)
    s = rotation_unitary(theta)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]])
    transformed = s @ sigma_z @ s.conj().T

    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.2))
    data = [s, sigma_z, transformed]
    titles = [r"$S$", r"$\sigma_z$", r"$S\sigma_zS^\dagger$"]
    for ax, matrix, title in zip(axes, data, titles):
        image = ax.imshow(np.real(matrix), vmin=-1.0, vmax=1.0, cmap="coolwarm")
        ax.set_title(title)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        for (row, col), value in np.ndenumerate(np.real(matrix)):
            ax.text(col, row, f"{value:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(image, ax=axes, shrink=0.75)
    fig.suptitle("Unitary basis transform preserves eigenvalues")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "unitary_basis_transform.png", dpi=180)
    plt.close(fig)


def plot_harmonic_oscillator_matrices() -> None:
    x, p, h = harmonic_oscillator_matrices()
    fig, axes = plt.subplots(1, 3, figsize=(10.0, 3.4))
    for ax, matrix, title in zip(axes, [x, p.imag, h], ["x matrix", "imaginary part of p", "H matrix"]):
        image = ax.imshow(np.real(matrix), cmap="coolwarm")
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel("m")
    fig.colorbar(image, ax=axes, shrink=0.78)
    fig.suptitle("Harmonic oscillator in the energy basis")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "harmonic_oscillator_matrices.png", dpi=180)
    plt.close(fig)


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    plot_unitary_basis_transform()
    plot_harmonic_oscillator_matrices()


if __name__ == "__main__":
    main()
