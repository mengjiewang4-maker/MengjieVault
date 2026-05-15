import matplotlib.pyplot as plt
import numpy as np

def plot_structure(pos):
    pos = np.array(pos)
    plt.scatter(pos[:,0], pos[:,1])
    plt.gca().set_aspect('equal')
    plt.show()