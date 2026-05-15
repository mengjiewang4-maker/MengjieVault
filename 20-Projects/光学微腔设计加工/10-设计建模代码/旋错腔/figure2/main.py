import numpy as np

from lattice import generate_lattice, apply_disclination
from tb_model import build_tb
from solver import solve_tb
from analysis import angular_momentum
from plotter import plot_lattice, plot_spectrum, plot_mode


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