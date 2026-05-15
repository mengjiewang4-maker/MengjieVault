"""
Relative-distance distributions for two identical free particles.

This reproduces the qualitative Chapter 4 result: symmetric exchange enhances
small relative distances, while antisymmetric exchange suppresses them.
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


def relative_distributions(z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return distinguishable, antisymmetric, and symmetric relative distributions.

    z = 2 k r is dimensionless. Curves are normalized to the distinguishable
    large-distance envelope used in the textbook's qualitative plot.
    """
    distinguishable = np.ones_like(z)
    sinc = np.ones_like(z)
    mask = z != 0
    sinc[mask] = np.sin(z[mask]) / z[mask]
    antisymmetric = 1.0 - sinc
    symmetric = 1.0 + sinc
    return distinguishable, antisymmetric, symmetric


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    z = np.linspace(0.0, 24.0, 1000)
    distinguishable, antisymmetric, symmetric = relative_distributions(z)

    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.plot(z, distinguishable, color="0.45", linestyle="--", label="distinguishable")
    ax.plot(z, symmetric, color="#3b6ea8", label="symmetric (Bose)")
    ax.plot(z, antisymmetric, color="#a84f3b", label="antisymmetric (Fermi)")
    ax.set_xlabel("dimensionless relative distance z = 2kr")
    ax.set_ylabel("relative probability density")
    ax.set_title("Exchange symmetry changes relative-distance probabilities")
    ax.set_ylim(-0.05, 2.15)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "identical_particle_exchange.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()

