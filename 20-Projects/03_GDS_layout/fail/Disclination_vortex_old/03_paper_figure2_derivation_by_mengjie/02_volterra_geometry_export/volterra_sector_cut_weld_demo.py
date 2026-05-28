"""
用二维网格可视化 Volterra 过程：切除一个扇区，再把剩余角区重新粘合。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_volterra_disclination():
    """
    绘制 Volterra 切割和粘合前后的点阵对比。
    """
    # 1. 初始化晶格参数
    N = 25  # 网格点数
    limit = 10
    x = np.linspace(-limit, limit, N)
    y = np.linspace(-limit, limit, N)
    X, Y = np.meshgrid(x, y)
    
    # 将网格展平为点集
    points_x = X.flatten()
    points_y = Y.flatten()
    
    # 转换为极坐标 (r, theta)
    r = np.sqrt(points_x**2 + points_y**2)
    theta = np.arctan2(points_y, points_x)
    
    # 将角度调整到 [0, 2*pi] 范围内
    theta = np.mod(theta, 2 * np.pi)
    
    # 2. 第一步：切割 (移除第一象限 0 到 pi/2)
    # 仅保留角度在 [pi/2, 2*pi] 之间的点
    mask = (theta >= np.pi/2)
    r_cut = r[mask]
    theta_cut = theta[mask]
    
    # 计算切割状态下的直角坐标
    x_cut = r_cut * np.cos(theta_cut)
    y_cut = r_cut * np.sin(theta_cut)
    
    # 3. 第二步：粘合 (将 270度 映射回 360度)
    # 将剩余的角度区间从 [pi/2, 2*pi] 线性映射到 [0, 2*pi]
    # 映射公式: theta_new = (theta_old - pi/2) * (2*pi / (3*pi/2)) = (theta_old - pi/2) * (4/3)
    theta_welded = (theta_cut - np.pi/2) * (4.0 / 3.0)
    
    # 计算粘合后的直角坐标
    x_welded = r_cut * np.cos(theta_welded)
    y_welded = r_cut * np.sin(theta_welded)
    
    # 4. 绘图对比
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左图：切割后的状态 (去掉了 1/4)
    ax1.scatter(x_cut, y_cut, c=r_cut, cmap='coolwarm', s=15, edgecolors='none')
    ax1.set_title("1. Cutting: Removed 1/4 Sector", fontsize=14)
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_xlim(-limit-1, limit+1)
    ax1.set_ylim(-limit-1, limit+1)
    
    # 右图：粘合后的状态 (形成 +90度 旋错)
    ax2.scatter(x_welded, y_welded, c=r_cut, cmap='coolwarm', s=15, edgecolors='none')
    ax2.set_title("2. Welding: +90° Disclination (Volterra)", fontsize=14)
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.set_xlim(-limit-1, limit+1)
    ax2.set_ylim(-limit-1, limit+1)
    
    plt.tight_layout()
    plt.show()

# 执行绘图
plot_volterra_disclination()