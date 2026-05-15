import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("resonators.csv",delimiter=",")

plt.scatter(data[:,0],data[:,1])

plt.gca().set_aspect("equal")

plt.show()