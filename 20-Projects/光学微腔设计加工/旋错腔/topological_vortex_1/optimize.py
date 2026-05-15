import numpy as np
from tb_model import *
from find_modes import *
from vortex_detector import *

def scan_parameters():

    results=[]

    for t1 in np.linspace(-0.1,-0.5,10):

        for t2 in np.linspace(-0.8,-1.5,10):

            model=build_model(t1,t2)

            psi=find_mode(model)

            l=vortex_charge(psi)

            results.append((t1,t2,l))

    return results