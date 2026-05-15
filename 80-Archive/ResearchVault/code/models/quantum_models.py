"""
Computational starting points for Zeng Jinyan's quantum mechanics textbook.

The script uses dimensionless units where hbar = m = omega = L = 1 unless
noted. It generates plots that are linked from the Obsidian book map.
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


def infinite_well_wavefunction(n: int, x: np.ndarray, length: float = 1.0) -> np.ndarray:
    return np.sqrt(2.0 / length) * np.sin(n * np.pi * x / length)


def infinite_well_energy(n: int, length: float = 1.0, hbar: float = 1.0, mass: float = 1.0) -> float:
    return n**2 * np.pi**2 * hbar**2 / (2.0 * mass * length**2)


def hermite_physicists(n: int, x: np.ndarray) -> np.ndarray:
    if n == 0:
        return np.ones_like(x)
    if n == 1:
        return 2.0 * x
    h_nm2 = np.ones_like(x)
    h_nm1 = 2.0 * x
    for k in range(1, n):
        h_n = 2.0 * x * h_nm1 - 2.0 * k * h_nm2
        h_nm2, h_nm1 = h_nm1, h_n
    return h_nm1


def factorial(n: int) -> int:
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def harmonic_oscillator_wavefunction(n: int, x: np.ndarray) -> np.ndarray:
    norm = 1.0 / np.sqrt((2.0**n) * factorial(n) * np.sqrt(np.pi))
    return norm * hermite_physicists(n, x) * np.exp(-(x**2) / 2.0)


def gaussian_packet(x: np.ndarray, x0: float = -3.0, k0: float = 5.0, sigma: float = 0.7) -> np.ndarray:
    envelope = np.exp(-((x - x0) ** 2) / (4.0 * sigma**2))
    phase = np.exp(1j * k0 * x)
    norm = (2.0 * np.pi * sigma**2) ** (-0.25)
    return norm * envelope * phase


def free_gaussian_density(x: np.ndarray, time: float, sigma: float = 0.5, k0: float = 4.0) -> np.ndarray:
    """Free-particle Gaussian density in units hbar = m = 1."""
    center = k0 * time
    width_sq = sigma**2 + time**2 / (4.0 * sigma**2)
    return np.exp(-((x - center) ** 2) / (2.0 * width_sq)) / np.sqrt(2.0 * np.pi * width_sq)


def barrier_transmission(energy: np.ndarray, height: float = 1.0, width: float = 1.0) -> np.ndarray:
    """Square barrier transmission in units where 2m/hbar^2 = 1."""
    energy = np.asarray(energy)
    transmission = np.empty_like(energy, dtype=float)
    below = energy < height
    above = ~below

    kappa = np.sqrt(np.maximum(height - energy[below], 1e-12))
    transmission[below] = 1.0 / (
        1.0 + (height**2 * np.sinh(kappa * width) ** 2) / (4.0 * energy[below] * (height - energy[below]))
    )

    q = np.sqrt(np.maximum(energy[above] - height, 1e-12))
    transmission[above] = 1.0 / (
        1.0 + (height**2 * np.sin(q * width) ** 2) / (4.0 * energy[above] * (energy[above] - height))
    )
    return np.clip(transmission, 0.0, 1.0)


def plot_infinite_well() -> None:
    x = np.linspace(0.0, 1.0, 600)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for n in range(1, 5):
        energy = infinite_well_energy(n)
        psi = infinite_well_wavefunction(n, x)
        ax.plot(x, 0.16 * psi + energy, label=f"n={n}, E={energy:.1f}")
        ax.hlines(energy, 0, 1, color="0.82", linewidth=0.8)
    ax.set_title("Infinite square well: eigenstates and energy levels")
    ax.set_xlabel("x / L")
    ax.set_ylabel("energy + scaled wavefunction")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "infinite_well_levels.png", dpi=180)
    plt.close(fig)


def plot_harmonic_oscillator() -> None:
    x = np.linspace(-4.0, 4.0, 800)
    potential = 0.5 * x**2
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(x, potential, color="0.35", linewidth=1.2, label="V(x)=x^2/2")
    for n in range(4):
        energy = n + 0.5
        psi = harmonic_oscillator_wavefunction(n, x)
        ax.plot(x, 0.55 * psi + energy, label=f"n={n}")
        ax.hlines(energy, -4, 4, color="0.86", linewidth=0.8)
    ax.set_ylim(-0.1, 5.0)
    ax.set_title("Harmonic oscillator: first four stationary states")
    ax.set_xlabel("dimensionless x")
    ax.set_ylabel("energy + scaled wavefunction")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "harmonic_oscillator_states.png", dpi=180)
    plt.close(fig)


def plot_free_gaussian_packet() -> None:
    x = np.linspace(-4.0, 14.0, 1000)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for time in (0.0, 0.6, 1.2, 2.0):
        ax.plot(x, free_gaussian_density(x, time), label=f"t={time:g}")
    ax.set_title("Free Gaussian wave packet spreading")
    ax.set_xlabel("dimensionless x")
    ax.set_ylabel(r"$|\psi(x,t)|^2$")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "free_gaussian_packet_spreading.png", dpi=180)
    plt.close(fig)


def plot_overview() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.0, 7.0))

    x_well = np.linspace(0.0, 1.0, 600)
    for n in range(1, 4):
        axes[0, 0].plot(x_well, infinite_well_wavefunction(n, x_well), label=f"n={n}")
    axes[0, 0].set_title("Infinite well wavefunctions")
    axes[0, 0].set_xlabel("x / L")
    axes[0, 0].legend(frameon=False, fontsize=8)

    n_values = np.arange(1, 7)
    axes[0, 1].bar(n_values, [infinite_well_energy(int(n)) for n in n_values], color="#3b6ea8")
    axes[0, 1].set_title("Infinite well energy scaling")
    axes[0, 1].set_xlabel("n")
    axes[0, 1].set_ylabel("E_n")

    x_ho = np.linspace(-4.0, 4.0, 800)
    for n in range(3):
        axes[1, 0].plot(x_ho, harmonic_oscillator_wavefunction(n, x_ho), label=f"n={n}")
    axes[1, 0].set_title("Harmonic oscillator states")
    axes[1, 0].set_xlabel("dimensionless x")
    axes[1, 0].legend(frameon=False, fontsize=8)

    energies = np.linspace(0.05, 4.0, 800)
    axes[1, 1].plot(energies, barrier_transmission(energies, height=1.0, width=2.0), color="#a84f3b")
    axes[1, 1].axvline(1.0, color="0.7", linestyle="--", linewidth=1.0)
    axes[1, 1].set_title("Square barrier transmission")
    axes[1, 1].set_xlabel("E / V0")
    axes[1, 1].set_ylabel("T")
    axes[1, 1].set_ylim(-0.03, 1.03)

    fig.tight_layout()
    fig.savefig(PLOT_DIR / "quantum_models_overview.png", dpi=180)
    plt.close(fig)


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    plot_infinite_well()
    plot_harmonic_oscillator()
    plot_free_gaussian_packet()
    plot_overview()


if __name__ == "__main__":
    main()
