import matplotlib.pyplot as plt
import numpy as np


def plot_lattice(pos):
    """
    可视化晶格点阵
    pos: 坐标数组，形状为 [N, 2]
    """
    plt.scatter(pos[:,0], pos[:,1])  # 绘制散点图，pos[:,0] 是 X 坐标，pos[:,1] 是 Y 坐标
    plt.gca().set_aspect('equal')    # 设置坐标轴比例为 1:1，防止晶格看起来被拉伸（例如正方形变矩形）
    plt.title("Resonator lattice")   # 设置图表标题
    plt.show()                       # 显示图形


def plot_spectrum(E):
    """
    可视化能谱（特征值分布）
    E: 特征值数组（通常已排序）
    """
    plt.plot(E,'o')            # 绘制能级图，'o' 表示用点标记每一个能级
    plt.xlabel("mode index")   # 设置 X 轴标签（模态索引，从 0 到 N-1）
    plt.ylabel("energy")       # 设置 Y 轴标签（对应的能量值）
    plt.title("TB spectrum")
    plt.show()


def plot_mode(pos, phase):
    """
    可视化特定模式的相位空间分布
    pos: 坐标数组 [N, 2]
    phase: 对应每个点的相位值（弧度）
    """
    # 绘制散点图，颜色 c 由 phase（相位）决定
    # cmap="twilight" 是专门处理循环数据的色卡（-pi 和 pi 的颜色是连续的）
    plt.scatter(pos[:,0], pos[:,1], c=phase, cmap="twilight")

    # 添加颜色条，并设置标签为“相位”
    plt.colorbar(label="phase")

    # 保持物理空间的比例一致
    plt.gca().set_aspect('equal')
    plt.title("Mode phase distribution")
    plt.show()