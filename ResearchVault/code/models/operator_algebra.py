"""
Small operator-algebra checks for Chapter 3.

The matrices use units hbar = 1. They demonstrate Hermiticity, commutators,
eigenvalues, and the uncertainty relation with spin-1/2 operators.
"""

from __future__ import annotations

import numpy as np


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def expectation(state: np.ndarray, operator: np.ndarray) -> complex:
    return np.vdot(state, operator @ state)


def uncertainty(state: np.ndarray, operator: np.ndarray) -> float:
    mean = expectation(state, operator)
    mean_square = expectation(state, operator @ operator)
    return float(np.sqrt(np.real(mean_square - mean * np.conj(mean))))


def is_hermitian(operator: np.ndarray) -> bool:
    return np.allclose(operator.conj().T, operator)


def main() -> None:
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)

    sx = 0.5 * sigma_x
    sy = 0.5 * sigma_y
    sz = 0.5 * sigma_z

    print("Hermitian checks:")
    print("Sx", is_hermitian(sx))
    print("Sy", is_hermitian(sy))
    print("Sz", is_hermitian(sz))

    print("\nCommutator [Sx, Sy] and i Sz:")
    print(np.round(commutator(sx, sy), 6))
    print(np.round(1j * sz, 6))

    up_z = np.array([1, 0], dtype=complex)
    dx = uncertainty(up_z, sx)
    dy = uncertainty(up_z, sy)
    comm_mean = expectation(up_z, commutator(sx, sy))

    print("\nIn |up_z>:")
    print("<Sx>", expectation(up_z, sx))
    print("<Sy>", expectation(up_z, sy))
    print("<Sz>", expectation(up_z, sz))
    print("Delta Sx * Delta Sy =", dx * dy)
    print("1/2 |<[Sx,Sy]>| =", 0.5 * abs(comm_mean))


if __name__ == "__main__":
    main()

