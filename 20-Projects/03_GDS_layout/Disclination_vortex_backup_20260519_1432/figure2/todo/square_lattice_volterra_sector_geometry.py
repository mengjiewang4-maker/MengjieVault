"""
生成简单二维方形点阵，并通过删除角扇区构造 Volterra 旋错几何。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np

def generate_structure(Nx,Ny,a):#创建一个 二维正方形点阵 的坐标列表

    pos=[]                      # 初始化一个空列表，用来存储所有原子的坐标 (x, y)

    for i in range(Nx):         # 外层循环：遍历 x 方向的第 i 个晶胞
        for j in range(Ny):     # 内层循环：遍历 y 方向的第 j 个晶胞

            x=i*a               # 计算当前原子的 x 坐标：索引乘以晶格常数 a
            y=j*a               # 计算当前原子的 y 坐标：索引乘以晶格常数 a

            pos.append((x,y))   # 将计算出的坐标以元组 (x, y) 的形式存入列表

    return pos                  # 返回包含所有原子位置的列表


def remove_sector(pos,angle):   # 执行 Volterra 过程中的“剪”
    # 1. 计算所有原子的几何中心 (Centroid)
    # 取所有 x 的平均值作为中心 cx，所有 y 的平均值作为中心 cy
    cx=np.mean([p[0] for p in pos])
    cy=np.mean([p[1] for p in pos])

    new=[]  # 初始化新列表，存放“剪剩”下来的原子坐标

    for x,y in pos: # 遍历原始晶格中的每一个原子
        # 2. 计算当前原子相对于中心点 (cx, cy) 的极角 theta
        # arctan2 函数会根据 (y, x) 自动处理正负号，返回范围是 (-pi, pi]
        theta=np.arctan2(y-cy,x-cx)
        # 3. 逻辑判断：如果原子的角度小于设定的 angle，则保留
        # 角度大于或等于 angle 的那个“扇区”会被剔除
        if theta < angle:

            new.append((x,y))

    return new  # 返回剪裁后的残缺晶格坐标