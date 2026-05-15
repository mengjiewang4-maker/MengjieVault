import numpy as np
import matplotlib.pyplot as plt

# 计算六边形的顶点坐标
def hexagon(x_center, y_center, size):
    # 六个角的角度
    angles = np.linspace(0, 2 * np.pi, 7)  # 包含七个角度
    x_hexagon = x_center + size * np.cos(angles)  # 计算x坐标
    y_hexagon = y_center + size * np.sin(angles)  # 计算y坐标
    
    # 去掉最后一个重复的角度，确保六边形闭合
    return x_hexagon[:-1], y_hexagon[:-1]  # 返回前6个点，去掉最后一个重复的点

# 使用极坐标计算三角形的顶点
def polar_triangle(x_center, y_center, radius, angle_offset, triangle_size):
    # 计算三角形的顶点角度，6个角度，每个角度偏移60度
    angles = np.linspace(angle_offset, angle_offset + 2 * np.pi, 4)[:-1]  # 3个角，360度
    x_triangle = x_center + triangle_size * np.cos(angles)
    y_triangle = y_center + triangle_size * np.sin(angles)
    return x_triangle, y_triangle

# 创建六边形晶面，并在每个六边形中绘制六个小三角形
def create_honeycomb_lattice(rows, cols, size=1.0):
    fig, ax = plt.subplots(figsize=(8, 8))

    # 计算每个三角形的中心偏移位置，距离六边形中心 size / 3
    triangle_radius = size / 3  # 距离六边形中心的半径（1/3 六边形边长）
    # 三角形的大小是六边形的1/3
    triangle_size = size / 3

    for i in range(rows):
        for j in range(cols):
            # 计算每个六边形的中心位置
            x_center = i * 1.5 * size  # 水平方向的间距
            y_center = j * np.sqrt(3) * size  # 垂直方向的间距

            # 偶数行和奇数行需要偏移
            if i % 2 == 1:
                y_center += np.sqrt(3) * size / 2  # 偶数行和奇数行之间的偏移

            # 获取六边形的顶点坐标
            x_hexagon, y_hexagon = hexagon(x_center, y_center, size)

            # 绘制六边形
            ax.fill(x_hexagon, y_hexagon, edgecolor='black', facecolor='none')

            # 在每个六边形中绘制六个小三角形
            for k in range(6):
                # 每个三角形的中心距六边形中心的距离为 size / 3
                angle_offset = np.pi / 6 + k * np.pi / 3  # 偏角，每次偏移π/3
                # 使用极坐标计算小三角形的顶点
                x_triangle, y_triangle = polar_triangle(x_center, y_center, triangle_radius, angle_offset, triangle_size)
                
                # 绘制小三角形
                ax.fill(x_triangle, y_triangle, edgecolor='black', facecolor='none')

    ax.set_aspect('equal')  # 保持比例
    ax.set_axis_off()  # 关闭坐标轴
    plt.show()

# 设置六边形晶面大小和排列
size = 1.0  # 六边形的边长
rows = 10  # 行数
cols = 10  # 列数

# 创建六边形晶面，并在每个六边形中绘制六个小三角形
create_honeycomb_lattice(rows, cols, size)

