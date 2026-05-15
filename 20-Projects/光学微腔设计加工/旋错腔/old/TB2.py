import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# -----------------------------
# parameters
# -----------------------------

t1 = -0.2
t2 = -1.0
tnn = t2/np.sqrt(2)

Nx = 10
Ny = 10

sites_per_cell = 4
N = Nx*Ny*sites_per_cell

# -----------------------------
# index mapping
# -----------------------------

def idx(x,y,s):
    return (y*Nx + x)*sites_per_cell + s


# site label
# 0 A
# 1 B
# 2 C
# 3 D

# -----------------------------
# build Hamiltonian
# -----------------------------

H = np.zeros((N,N))

for x in range(Nx):
    for y in range(Ny):

        A = idx(x,y,0)
        B = idx(x,y,1)
        C = idx(x,y,2)
        D = idx(x,y,3)

        # intracell hopping

        H[A,B] = t1
        H[B,A] = t1

        H[B,C] = t1
        H[C,B] = t1

        H[C,D] = t1
        H[D,C] = t1

        H[D,A] = t1
        H[A,D] = t1

        # intercell x direction

        if x+1 < Nx:

            B2 = idx(x+1,y,0)
            C2 = idx(x+1,y,3)

            H[B,B2] = t2
            H[B2,B] = t2

            H[C,C2] = t2
            H[C2,C] = t2

        # intercell y direction

        if y+1 < Ny:

            D2 = idx(x,y+1,0)
            C2 = idx(x,y+1,1)

            H[D,D2] = t2
            H[D2,D] = t2

            H[C,C2] = t2
            H[C2,C] = t2


# -----------------------------
# introduce disclination
# -----------------------------

cx = Nx//2
cy = Ny//2

radius = 2

for x in range(Nx):
    for y in range(Ny):

        if abs(x-cx) < radius and abs(y-cy) < radius:

            for s1 in range(4):
                for s2 in range(4):

                    i = idx(x,y,s1)
                    j = idx(x,y,s2)

                    H[i,j] *= 0.5


# -----------------------------
# diagonalize Hamiltonian
# -----------------------------

E, V = eigh(H)

# plot spectrum

plt.figure()

plt.plot(E,'o')

plt.xlabel("state")
plt.ylabel("energy")

plt.title("TB spectrum")

plt.show()


# -----------------------------
# choose defect mode
# -----------------------------

k = N//2

mode = V[:,k]

density = np.abs(mode)**2

# reshape for visualization

density_map = density.reshape(Ny,Nx,sites_per_cell).sum(axis=2)

plt.figure()

plt.imshow(density_map)

plt.colorbar()

plt.title("mode density")

plt.show()


# -----------------------------
# phase distribution
# -----------------------------

phase = np.angle(mode)

phase_map = phase.reshape(Ny,Nx,sites_per_cell).mean(axis=2)

plt.figure()

plt.imshow(phase_map,cmap="twilight")

plt.colorbar()

plt.title("vortex phase")

plt.show()