import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Mac中文配置
matplotlib.rcParams['font.sans-serif'] = ['Heiti TC', 'Songti SC', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

# --------------------------
# 1. 基础参数
# --------------------------
a = 0.5                  # 参考长度
b = a / 2                # 三角形边长（≈0.167）
translate_theta = 60     # 平移倾角（60°=右上）
rotate_angle = 60        # 旋转角度（60°逆时针）
rotate_center = (0, 0)   # 旋转中心（原点）
translate_radius = 1* (a / np.sqrt(3))    # 平移距离

# --------------------------
# 2. 原始三角形重心严格在原点
# --------------------------
r_triangle = b / np.sqrt(3)  # 等边三角形外接圆半径
triangle_points = np.array([
    [-r_triangle, 0],                                  
    [r_triangle * np.cos(1*np.pi/3), r_triangle * np.sin(1*np.pi/3)],  
    [r_triangle * np.cos(-1*np.pi/3), r_triangle * np.sin(-1*np.pi/3)]   
])

# --------------------------
# 3. 核心函数
# --------------------------
def rotate_points(points, angle, center=(0, 0)):
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    return (rotation_matrix @ points.T).T

def translate_points(points, theta_deg, translate_radius):
    theta_rad = np.radians(theta_deg)
    dx = translate_radius * np.cos(theta_rad)
    dy = translate_radius * np.sin(theta_rad)
    
    homogeneous_points = np.hstack([points, np.ones((len(points), 1))])
    translation_matrix = np.array([[1,0,dx], [0,1,dy], [0,0,1]])
    translated_points =  translation_matrix @ homogeneous_points.T
    return translated_points.T[:, :2]

# --------------------------
# 4. 执行变换
# --------------------------
# 只旋转不平移
rotated_only_triangle = rotate_points(triangle_points, rotate_angle, rotate_center)

# 旋转后再平移
rotated_triangle = rotate_points(triangle_points, rotate_angle, rotate_center)
rotated_translated_triangle = translate_points(rotated_triangle, translate_theta, translate_radius)

# 验证结果
print(f"原始三角形重心：({np.mean(triangle_points[:, 0]):.3f}, {np.mean(triangle_points[:, 1]):.3f})")
print(f"仅旋转后重心：({np.mean(rotated_only_triangle[:, 0]):.3f}, {np.mean(rotated_only_triangle[:, 1]):.3f})")
print(f"旋转+平移后重心：({np.mean(rotated_translated_triangle[:, 0]):.3f}, {np.mean(rotated_translated_triangle[:, 1]):.3f})")

expected_x = translate_radius * np.cos(np.radians(translate_theta))
expected_y = translate_radius * np.sin(np.radians(translate_theta))
print(f"预期平移中心：({expected_x:.3f}, {expected_y:.3f})")

# --------------------------
# 5. 画图显示 - 清晰展示三个状态
# --------------------------
plt.figure(figsize=(12, 8))

# 原始三角形（蓝色）
plt.fill(triangle_points[:, 0], triangle_points[:, 1], 'blue', alpha=0.6, 
         label=f'原始三角形（重心在原点）', edgecolor='darkblue', linewidth=2)

# 只旋转不平移的三角形（绿色）
#plt.fill(rotated_only_triangle[:, 0], rotated_only_triangle[:, 1], 'green', alpha=0.6, 
#         label=f'旋转{rotate_angle}°后（仍在原点）', edgecolor='darkgreen', linewidth=2)

# 旋转+平移后的三角形（红色）
plt.fill(rotated_translated_triangle[:, 0], rotated_translated_triangle[:, 1], 'red', alpha=0.6, 
         label=f'旋转{rotate_angle}°+平移{translate_radius}单位', edgecolor='darkred', linewidth=2)


# 标记关键点和连线
plt.scatter(0, 0, color='black', s=120, label='旋转中心/原点', zorder=5)
plt.scatter(expected_x, expected_y, color='red', s=120, marker='X', 
           label='预期平移中心', zorder=5)

# 添加箭头显示从旋转后到平移后的移动
#centroid_rotated = [np.mean(rotated_only_triangle[:, 0]), np.mean(rotated_only_triangle[:, 1])]
#centroid_final = [np.mean(rotated_translated_triangle[:, 0]), np.mean(rotated_translated_triangle[:, 1])]

#plt.arrow(centroid_rotated[0], centroid_rotated[1], 
#          centroid_final[0]-centroid_rotated[0], centroid_final[1]-centroid_rotated[1],
 #         head_width=0.08, head_length=0.1, fc='purple', ec='purple', 
 #         linestyle='--', linewidth=2, label='平移路径', zorder=4)

# 添加顶点连线，更清楚显示变换
for i in range(3):
    # 原始到旋转的连线（浅蓝色虚线）
    plt.plot([triangle_points[i, 0], rotated_only_triangle[i, 0]], 
             [triangle_points[i, 1], rotated_only_triangle[i, 1]], 
             'blue', linestyle=':', alpha=0.4)
    
    # 旋转到平移后的连线（浅红色虚线）
    plt.plot([rotated_only_triangle[i, 0], rotated_translated_triangle[i, 0]], 
             [rotated_only_triangle[i, 1], rotated_translated_triangle[i, 1]], 
             'red', linestyle=':', alpha=0.4)

# 图形美化
plt.axis('equal')
plt.xlabel('X轴', fontsize=12)
plt.ylabel('Y轴', fontsize=12)
plt.title(f'三角形变换过程可视化\n（旋转{rotate_angle}° + 沿{translate_theta}°方向平移{translate_radius}单位）', 
          fontsize=14, pad=20)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)


# 添加坐标轴
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

plt.tight_layout()
plt.show()

# 打印变换矩阵信息
print("\n=== 变换详情 ===")
print(f"旋转角度：{rotate_angle}°（逆时针）")
print(f"平移方向：{translate_theta}°")
print(f"平移距离：{translate_radius}")
print(f"平移向量：({expected_x:.3f}, {expected_y:.3f})")