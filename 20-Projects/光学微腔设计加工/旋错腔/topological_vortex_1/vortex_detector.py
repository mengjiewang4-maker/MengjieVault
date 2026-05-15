import numpy as np

def vortex_charge(psi):

    phase=np.angle(psi)

    dphi=np.max(phase)-np.min(phase)

    l=dphi/(2*np.pi)

    return l