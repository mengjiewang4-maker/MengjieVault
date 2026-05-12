"""
Chapter 5 computational notes: central potentials.

The plots use dimensionless units. They are meant as qualitative companions
for the Obsidian notes, not as a replacement for formula derivations.
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


def coulomb_effective_potential(r: np.ndarray, ell: int) -> np.ndarray:
    """Dimensionless V_eff = -1/r + l(l+1)/(2r^2), with hbar = mu = 1."""
    return -1.0 / r + ell * (ell + 1) / (2.0 * r**2)


def hydrogen_radial_probability(r: np.ndarray, state: str) -> np.ndarray:
    """Return r^2 |R_nl(r)|^2 for selected hydrogen states in units a0 = 1."""
    if state == "1s":
        radial = 2.0 * np.exp(-r)
    elif state == "2s":
        radial = (2.0 - r) * np.exp(-r / 2.0) / (2.0 * np.sqrt(2.0))
    elif state == "2p":
        radial = r * np.exp(-r / 2.0) / (2.0 * np.sqrt(6.0))
    elif state == "3d":
        radial = 4.0 * r**2 * np.exp(-r / 3.0) / (81.0 * np.sqrt(30.0))
    else:
        raise ValueError(f"unknown state: {state}")
    return r**2 * radial**2


def plot_coulomb_effective_potential() -> None:
    r = np.linspace(0.12, 12.0, 1200)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for ell in range(4):
        potential = np.clip(coulomb_effective_potential(r, ell), -1.2, 4.0)
        ax.plot(r, potential, label=f"l={ell}")
    ax.axhline(0.0, color="0.75", linewidth=0.9)
    ax.set_ylim(-1.2, 4.0)
    ax.set_title("Coulomb effective radial potential")
    ax.set_xlabel(r"$r/a_0$")
    ax.set_ylabel(r"$V_{\rm eff}$")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "central_potential_effective.png", dpi=180)
    plt.close(fig)


def plot_spherical_box_levels() -> None:
    roots = {
        0: [np.pi, 2.0 * np.pi, 3.0 * np.pi, 4.0 * np.pi],
        1: [4.493, 7.725, 10.904, 14.066],
        2: [5.764, 9.095, 12.323, 15.515],
        3: [6.988, 10.417, 13.698, 16.924],
    }
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for ell, ell_roots in roots.items():
        energies = [root**2 / 2.0 for root in ell_roots]
        for idx, energy in enumerate(energies):
            ax.hlines(energy, ell - 0.32, ell + 0.32, color="#3b6ea8", linewidth=2.0)
            ax.text(ell + 0.36, energy, f"{idx}{'spdf'[ell]}", va="center", fontsize=8)
    ax.set_title("Infinite spherical well: low radial levels")
    ax.set_xlabel("orbital angular momentum l")
    ax.set_ylabel(r"$E = \alpha_{n_rl}^2/2$  (hbar = mu = a = 1)")
    ax.set_xticks([0, 1, 2, 3], ["s", "p", "d", "f"])
    ax.set_ylim(0, 150)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "spherical_box_levels.png", dpi=180)
    plt.close(fig)


def plot_hydrogen_radial_probabilities() -> None:
    r = np.linspace(0.0, 32.0, 1600)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for state in ("1s", "2s", "2p", "3d"):
        ax.plot(r, hydrogen_radial_probability(r, state), label=state)
    ax.set_title("Hydrogen radial probability distributions")
    ax.set_xlabel(r"$r/a_0$")
    ax.set_ylabel(r"$r^2 |R_{nl}(r)|^2$")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "hydrogen_radial_probabilities.png", dpi=180)
    plt.close(fig)


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    plot_coulomb_effective_potential()
    plot_spherical_box_levels()
    plot_hydrogen_radial_probabilities()


if __name__ == "__main__":
    main()
