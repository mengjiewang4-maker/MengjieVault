import numpy as np        # 导入 numpy，用于数学运算
import matplotlib.pyplot as plt  # 导入 matplotlib.pyplot，用于绘图
a=0.5
b=a/6
# 定义三角形的顶点（正等边三角形，边长=2，重心在(1, √3/3)）
triangle_points = np.array([
    [0, 0],                     # 顶点 A (0, 0)
    [b*np.sqrt(3)/2, b/2],      # 顶点 B (b√3/2,b/2)
    [b*np.sqrt(3)/2, -b/2]      # 顶点 C (b√3/2,-b/2)
])

def rotate_points(points, angle, center=(0, 0)):
    """
    旋转给定的点到指定角度（支持自定义旋转中心）
    :param points: 原始顶点坐标 (n×2 数组)
    :param angle: 旋转角度（度），逆时针为正
    :param center: 旋转中心（默认原点 (0,0)）
    :return: 旋转后的顶点坐标
    """
    angle_rad = np.radians(angle)  # 将角度转化为弧度
    # 2D 旋转矩阵
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    
    # 步骤：先平移到旋转中心→旋转→平移回原坐标系
    points_translated = points - center  # 平移到旋转中心
    points_rotated = points_translated @ rotation_matrix  # 矩阵乘法旋转
    points_final = points_rotated + center  # 平移回原坐标系
    return points_final

# --------------------------
# 核心参数配置
# --------------------------
angle = 60  # 旋转角度（度），逆时针为正
rotate_center = (a/np.sqrt(3), 0)  # 旋转中心（设为三角形自身重心，避免旋转偏移）
# rotate_center = (0, 0)  # 可选：围绕原点旋转
# rotate_center = (1, 0)  # 可选：围绕任意点旋转

# 执行旋转（关键：调用旋转函数）
rotated_triangle = rotate_points(triangle_points, angle, rotate_center)
rotated_triangle = rotate_points(triangle_points, angle, rotate_center)
# --------------------------
# 绘图显示
# --------------------------
plt.figure(figsize=(8, 6))  # 设置图形大小

# 绘制原始三角形（蓝色，透明度0.5）
plt.fill(triangle_points[:, 0], triangle_points[:, 1], 'b', alpha=0.5, label=f'Original (side=2)')
# 绘制旋转后的三角形（红色，透明度0.5）
plt.fill(rotated_triangle[:, 0], rotated_triangle[:, 1], 'r', alpha=0.5, label=f'Rotated {angle}°')

# 绘制旋转中心（黑色圆点标记）
plt.scatter(rotate_center[0], rotate_center[1], color='black', s=50, label=f'Rotation Center')

# 图形美化
plt.axis('equal')  # 保证坐标轴比例一致，避免图形拉伸
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Original vs Rotated Equilateral Triangle')
plt.legend()  # 显示图例
plt.grid(True, alpha=0.3)  # 显示网格
plt.show()  # 显示图形

