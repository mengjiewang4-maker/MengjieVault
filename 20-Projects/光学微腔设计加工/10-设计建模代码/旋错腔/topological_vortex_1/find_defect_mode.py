import numpy as np

def build_finite_model(model,Nx,Ny):

    m = model.cut_piece(Nx,0)
    m = m.cut_piece(Ny,1)

    return m
def add_disclination(model):

    n = model._norb

    for i in range(n):

        x,y = model.get_orb(i)

        if x>0.5 and y>0.5:

            model.set_onsite(5,i)
def find_defect_mode(model):

    evals,evecs = model.solve_all(eig_vectors=True)

    mid = len(evals)//2

    psi = evecs[:,mid]

    density = abs(psi)**2

    return psi,density
import numpy as np

def vortex_charge(psi):

    phase = np.angle(psi)

    dphi = np.max(phase)-np.min(phase)

    l = dphi/(2*np.pi)

    return l