"""
Compact computational figures for chapters 8-12.

The plots are qualitative, using dimensionless units chosen to keep each
chapter's main structure visible.
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


def plot_spin_precession() -> None:
    t = np.linspace(0.0, 4.0 * np.pi, 600)
    sx = np.cos(t)
    sy = np.sin(t)
    sz = np.full_like(t, 0.35)
    fig = plt.figure(figsize=(6.2, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(sx, sy, sz, color="#3b6ea8")
    ax.scatter([sx[0]], [sy[0]], [sz[0]], color="#a84f3b", s=36)
    ax.set_title("Spin expectation precession")
    ax.set_xlabel(r"$\langle S_x\rangle$")
    ax.set_ylabel(r"$\langle S_y\rangle$")
    ax.set_zlabel(r"$\langle S_z\rangle$")
    ax.set_box_aspect((1, 1, 0.6))
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "spin_precession.png", dpi=180)
    plt.close(fig)


def plot_avoided_crossing() -> None:
    delta = np.linspace(-3.0, 3.0, 800)
    coupling = 0.45
    e_plus = np.sqrt((delta / 2.0) ** 2 + coupling**2)
    e_minus = -e_plus
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(delta, delta / 2.0, color="0.75", linestyle="--", label="uncoupled")
    ax.plot(delta, -delta / 2.0, color="0.75", linestyle="--")
    ax.plot(delta, e_plus, color="#3b6ea8", label="with coupling")
    ax.plot(delta, e_minus, color="#a84f3b")
    ax.set_title("Near-degenerate perturbation: avoided crossing")
    ax.set_xlabel("detuning")
    ax.set_ylabel("energy")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "avoided_crossing.png", dpi=180)
    plt.close(fig)


def plot_fermi_golden_sinc() -> None:
    omega = np.linspace(-10.0, 10.0, 1600)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for duration in (1.0, 2.0, 5.0):
        x = omega * duration / 2.0
        profile = duration**2 * np.sinc(x / np.pi) ** 2
        profile = profile / profile.max()
        ax.plot(omega, profile, label=f"T={duration:g}")
    ax.set_title("Finite-time transition peak approaches energy selection")
    ax.set_xlabel(r"$\omega-\omega_{fi}$")
    ax.set_ylabel("normalized transition probability")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "fermi_golden_sinc.png", dpi=180)
    plt.close(fig)


def plot_fermi_occupation() -> None:
    energy = np.linspace(0.0, 2.0, 800)
    ef = 1.0
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.step(energy, (energy <= ef).astype(float), where="post", label="T=0")
    for temperature in (0.06, 0.14):
        occupation = 1.0 / (np.exp((energy - ef) / temperature) + 1.0)
        ax.plot(energy, occupation, label=f"T={temperature:g}")
    ax.set_title("Fermi gas occupation")
    ax.set_xlabel(r"$E/E_F$")
    ax.set_ylabel("occupation probability")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "fermi_occupation.png", dpi=180)
    plt.close(fig)


def plot_molecular_effective_potential() -> None:
    r = np.linspace(0.45, 4.5, 1000)
    de = 1.0
    a = 1.35
    re = 1.45
    morse = de * (1.0 - np.exp(-a * (r - re))) ** 2 - de
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(r, morse, color="#3b6ea8")
    for v in range(4):
        level = -de + (v + 0.5) * 0.22
        ax.hlines(level, re - 0.45, re + 0.45, color="#a84f3b", linewidth=1.5)
        ax.text(re + 0.5, level, f"v={v}", va="center", fontsize=8)
    ax.axhline(0.0, color="0.82", linewidth=0.9)
    ax.set_title("Diatomic molecule effective potential")
    ax.set_xlabel("internuclear distance")
    ax.set_ylabel("effective energy")
    ax.set_ylim(-1.1, 0.8)
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "molecular_effective_potential.png", dpi=180)
    plt.close(fig)


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    plot_spin_precession()
    plot_avoided_crossing()
    plot_fermi_golden_sinc()
    plot_fermi_occupation()
    plot_molecular_effective_potential()


if __name__ == "__main__":
    main()
