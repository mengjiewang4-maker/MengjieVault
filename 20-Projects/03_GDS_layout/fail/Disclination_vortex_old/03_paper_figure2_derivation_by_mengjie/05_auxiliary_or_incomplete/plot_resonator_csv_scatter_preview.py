"""
读取 resonators.csv 并画出谐振器/空气孔坐标散点图，用来快速检查导出的点阵形状。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("resonators.csv",delimiter=",")

plt.scatter(data[:,0],data[:,1])

plt.gca().set_aspect("equal")

plt.show()