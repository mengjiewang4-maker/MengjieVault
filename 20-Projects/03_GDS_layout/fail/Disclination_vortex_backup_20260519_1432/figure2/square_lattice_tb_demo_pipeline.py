"""
figure2 目录的教学入口脚本，串联晶格生成、旋错变换、求解和绘图。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np

from square_lattice_disclination_geometry import generate_lattice, apply_disclination
from tight_binding_hamiltonian_builder import build_tb
from tight_binding_eigensolver import solve_tb
from mode_angular_momentum_analysis import angular_momentum
from lattice_mode_plotting_helpers import plot_lattice, plot_spectrum, plot_mode


# 1 lattice
positions = generate_lattice(10,10,1)

# 2 disclination
positions = apply_disclination(positions,5)

# 3 plot structure
plot_lattice(positions)

# 4 TB Hamiltonian
H = build_tb(positions)

# 5 solve
E,psi = solve_tb(H)

# 6 spectrum
plot_spectrum(E)

# 7 defect mode
mode_index = len(E)//2

mode = psi[:,mode_index]

plot_mode(positions, np.angle(mode))

# 8 angular momentum
l = angular_momentum(positions, mode)

print("Angular momentum =",l)
