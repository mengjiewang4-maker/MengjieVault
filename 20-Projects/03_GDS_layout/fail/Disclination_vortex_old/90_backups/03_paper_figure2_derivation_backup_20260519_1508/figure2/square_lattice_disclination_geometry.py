"""
提供方形晶格生成和旋错角度重映射两个基础几何函数。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np


def generate_lattice(Nx, Ny, a):
    """
    生成二维方形晶格坐标数组。
    """
    #生成一个二维正方形晶格坐标
    #Nx, Ny: 分别在 x 和 y 方向上的半长度（扩展范围）
    #a: 晶格常数（点与点之间的距离）
    pos = []# 初始化一个列表，用于存储坐标点 (x, y)
    
    # 嵌套循环：从 -Nx 到 Nx-1，从 -Ny 到 Ny-1 遍历所有格点
    for i in range(-Nx, Nx):
        for j in range(-Ny, Ny):

            x = i * a  # 计算当前格点的 x 物理坐标
            y = j * a  # 计算当前格点的 y 物理坐标

            pos.append((x,y))  # 将坐标以元组形式添加到列表中

    return np.array(pos)   # 将列表转换为 numpy 数组返回，方便后续数学运算


def apply_disclination(positions, n=5):
    """
    把原始坐标映射到旋错后的坐标；超出保留角区的点返回 None 或被重新映射。
    """
    #对输入的晶格坐标应用旋错（Disclination）变换
    #n: 旋转对称性（例如 n=5 表示 C5 对称性，通常对应扇形缺失/增加）

    """
    n = rotational symmetry
    例如 n=5 → C5 disclination
    """

    theta = 2*np.pi/n  # 计算旋转角度基数（例如 n=5 时，theta = 72度）

    new_pos = []       # 初始化存储变换后坐标的列表

    for x,y in positions:
        # 1. 将直角坐标 (x, y) 转换为极坐标 (r, angle)
        r = np.sqrt(x**2 + y**2) # 计算点到原点的径向距离（半径）

        angle = np.arctan2(y,x)  # 计算点相对于原点的方位角

        # 2. 角度重映射（核心变换）
        # 这里使用了系数 n/(n-1)，其物理意义是将原本 2π 的空间“拉伸”或“压缩”
        # 例如：将原本 2π(1 - 1/n) 的角度范围映射回全平面 2π
        new_angle = angle * (n/(n-1))
        
        # 3. 将新的极坐标 (r, new_angle) 转回直角坐标 (xn, yn)
        xn = r * np.cos(new_angle)
        yn = r * np.sin(new_angle)
 
        new_pos.append((xn,yn))   # 记录变换后的位置

    return np.array(new_pos)      # 返回变换后的坐标数组