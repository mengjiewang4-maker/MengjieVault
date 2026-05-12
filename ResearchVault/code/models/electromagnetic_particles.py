"""
Chapter 6 computational notes: charged particles in electromagnetic fields.

The plots use dimensionless units where hbar = e = mu = c = 1, so
omega_L = B / 2 and omega_c = B.
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


def zeeman_energies(ell: int, magnetic_field: float, base_energy: float = 0.0) -> list[tuple[int, float]]:
    omega_l = magnetic_field / 2.0
    return [(m, base_energy + m * omega_l) for m in range(-ell, ell + 1)]


def landau_energy(n: int, magnetic_field: float) -> float:
    return (n + 0.5) * magnetic_field


def plot_zeeman_splitting() -> None:
    fields = np.array([0.0, 0.7, 1.4])
    ell = 2
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for x, field in enumerate(fields):
        for m, energy in zeeman_energies(ell, field):
            ax.hlines(energy, x - 0.28, x + 0.28, color="#3b6ea8", linewidth=2.0)
            if field > 0:
                ax.text(x + 0.32, energy, f"m={m}", va="center", fontsize=8)
    ax.set_title("Normal Zeeman splitting for l=2")
    ax.set_xlabel("magnetic field B")
    ax.set_ylabel(r"$\Delta E / \hbar$")
    ax.set_xticks(range(len(fields)), [f"{field:g}" for field in fields])
    ax.axhline(0.0, color="0.82", linewidth=0.9)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "zeeman_splitting.png", dpi=180)
    plt.close(fig)


def plot_landau_levels() -> None:
    magnetic_fields = np.linspace(0.0, 3.0, 400)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for n in range(5):
        ax.plot(magnetic_fields, landau_energy(n, magnetic_fields), label=f"n={n}")
    ax.set_title("Landau levels scale linearly with B")
    ax.set_xlabel("magnetic field B")
    ax.set_ylabel(r"$E_n / \hbar$")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "landau_levels.png", dpi=180)
    plt.close(fig)


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    plot_zeeman_splitting()
    plot_landau_levels()


if __name__ == "__main__":
    main()
