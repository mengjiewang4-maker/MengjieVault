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
rotate_center = (0, 0)   # 旋转中心（原点）

# --------------------------
# 2. 六个三角形的配置参数
# 每个三角形配置: [旋转角度(度), 平移角度(度), 平移距离倍数]
# --------------------------
triangle_configs = [
    # [旋转角度, 平移角度, 平移距离倍数]
    [0, 0, 1],           # 三角形1: 沿60°方向平移1倍距离
    [60, 60, 1.2],         # 三角形2: 旋转60°, 沿60°方向平移1.2倍距离
    [120, 120, 1],       # 三角形3: 旋转120°, 沿120°方向平移1倍距离  
    [180, 180, 1.2],       # 三角形4: 旋转180°, 沿180°方向平移1.2倍距离
    [240, 240, 1],       # 三角形5: 旋转240°, 沿240°方向平移1倍距离
    [300, 300, 1.2]        # 三角形6: 旋转300°, 沿300°方向平移1.2倍距离
]

# 颜色配置
colors = ['blue', 'red', 'blue', 'red', 'blue', 'red']
color_names = ['蓝色', '红色', '蓝色', '红色', '蓝色', '红色']

# --------------------------
# 3. 原始三角形重心严格在原点
# --------------------------
r_triangle = b / np.sqrt(3)  # 等边三角形外接圆半径
triangle_points = np.array([
    [-r_triangle, 0],                                  
    [r_triangle * np.cos(1*np.pi/3), r_triangle * np.sin(1*np.pi/3)],  
    [r_triangle * np.cos(-1*np.pi/3), r_triangle * np.sin(-1*np.pi/3)]   
])

# --------------------------
# 4. 核心函数
# --------------------------
def rotate_points(points, angle, center=(0, 0)):
    """旋转点集"""
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    return (rotation_matrix @ (points - center).T).T + center

def translate_points(points, theta_deg, translate_distance):
    """平移点集"""
    theta_rad = np.radians(theta_deg)
    dx = translate_distance * np.cos(theta_rad)
    dy = translate_distance * np.sin(theta_rad)
    
    homogeneous_points = np.hstack([points, np.ones((len(points), 1))])
    translation_matrix = np.array([[1,0,dx], [0,1,dy], [0,0,1]])
    translated_points = translation_matrix @ homogeneous_points.T
    return translated_points.T[:, :2]

def transform_triangle(points, rotate_angle, translate_theta, translate_scale):
    """对三角形进行旋转和平移变换"""
    base_radius = a / np.sqrt(3)  # 基础平移距离
    translate_distance = translate_scale * base_radius
    
    # 先旋转后平移
    rotated_points = rotate_points(points, rotate_angle, rotate_center)
    transformed_points = translate_points(rotated_points, translate_theta, translate_distance)
    
    return rotated_points, transformed_points

# --------------------------
# 5. 执行所有三角形的变换
# --------------------------
transformed_triangles = []
rotated_triangles = []

print("=== 三角形变换详情 ===")
for i, config in enumerate(triangle_configs):
    rotate_angle, translate_theta, translate_scale = config
    base_radius = a / np.sqrt(3)
    translate_distance = translate_scale * base_radius
    
    rotated_only, transformed = transform_triangle(
        triangle_points, rotate_angle, translate_theta, translate_scale
    )
    
    rotated_triangles.append(rotated_only)
    transformed_triangles.append(transformed)
    
    # 计算和显示重心位置
    original_centroid = np.mean(triangle_points, axis=0)
    rotated_centroid = np.mean(rotated_only, axis=0)
    transformed_centroid = np.mean(transformed, axis=0)
    
    print(f"\n三角形{i+1} ({color_names[i]}):")
    print(f"  旋转角度: {rotate_angle}°, 平移: {translate_theta}°方向 {translate_distance:.3f}单位")
    print(f"  原始重心: ({original_centroid[0]:.3f}, {original_centroid[1]:.3f})")
    print(f"  旋转后重心: ({rotated_centroid[0]:.3f}, {rotated_centroid[1]:.3f})")
    print(f"  最终重心: ({transformed_centroid[0]:.3f}, {transformed_centroid[1]:.3f})")

# --------------------------
# 6. 画图显示 - 六个三角形
# --------------------------
plt.figure(figsize=(14, 10))

# 绘制原始三角形（参考）
plt.fill(triangle_points[:, 0], triangle_points[:, 1], 'gray', alpha=0.3, 
         label='原始三角形', edgecolor='black', linewidth=1, linestyle='--')

# 绘制每个变换后的三角形
for i, (config, triangle, color, color_name) in enumerate(zip(
    triangle_configs, transformed_triangles, colors, color_names)):
    
    rotate_angle, translate_theta, translate_scale = config
    base_radius = a / np.sqrt(3)
    translate_distance = translate_scale * base_radius
    
    # 绘制变换后的三角形
    plt.fill(triangle[:, 0], triangle[:, 1], color, alpha=0.6, 
             label=f'三角形{i+1}: 旋转{rotate_angle}°+平移{translate_theta}°', 
             edgecolor=color, linewidth=2)
    
    # 标记最终重心位置
    centroid = np.mean(triangle, axis=0)
    plt.scatter(centroid[0], centroid[1], color=color, s=100, marker='o', zorder=5)
    
    # 添加从原点到重心的连线（虚线）
    plt.plot([0, centroid[0]], [0, centroid[1]], color=color, 
             linestyle=':', alpha=0.6, linewidth=1)

# 标记旋转中心
plt.scatter(0, 0, color='black', s=150, marker='*', label='旋转中心/原点', zorder=6)

# 图形美化
plt.axis('equal')
plt.xlabel('X轴', fontsize=12)
plt.ylabel('Y轴', fontsize=12)
plt.title('六个三角形变换可视化\n(每个三角形可独立配置旋转和平移参数)', fontsize=14, pad=20)
plt.legend(loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)

# 添加坐标轴
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# 设置坐标轴范围以便更好地观察
max_extent = max([np.max(np.abs(triangle)) for triangle in transformed_triangles])
axis_limit = max_extent * 1.2
plt.xlim(-axis_limit, axis_limit)
plt.ylim(-axis_limit, axis_limit)

plt.tight_layout()
plt.show()

# --------------------------
# 7. 可选：单独显示每个三角形的变换过程
# --------------------------
def plot_individual_transformation(triangle_idx):
    """绘制单个三角形的详细变换过程"""
    if triangle_idx < 0 or triangle_idx >= len(triangle_configs):
        print("三角形索引无效")
        return
    
    config = triangle_configs[triangle_idx]
    rotate_angle, translate_theta, translate_scale = config
    base_radius = a / np.sqrt(3)
    translate_distance = translate_scale * base_radius
    
    rotated_only = rotated_triangles[triangle_idx]
    transformed = transformed_triangles[triangle_idx]
    
    plt.figure(figsize=(10, 8))
    
    # 原始三角形
    plt.fill(triangle_points[:, 0], triangle_points[:, 1], 'blue', alpha=0.4, 
             label='原始三角形', edgecolor='darkblue', linewidth=2)
    
    # 旋转后的三角形
    plt.fill(rotated_only[:, 0], rotated_only[:, 1], 'green', alpha=0.4, 
             label=f'旋转{rotate_angle}°后', edgecolor='darkgreen', linewidth=2)
    
    # 最终变换后的三角形
    plt.fill(transformed[:, 0], transformed[:, 1], 'red', alpha=0.6, 
             label=f'旋转{rotate_angle}°+平移{translate_distance:.2f}单位', 
             edgecolor='darkred', linewidth=2)
    
    # 标记关键点
    plt.scatter(0, 0, color='black', s=120, label='旋转中心', zorder=5)
    
    # 添加变换路径连线
    for i in range(3):
        plt.plot([triangle_points[i, 0], rotated_only[i, 0]], 
                 [triangle_points[i, 1], rotated_only[i, 1]], 
                 'green', linestyle=':', alpha=0.5, linewidth=1)
        plt.plot([rotated_only[i, 0], transformed[i, 0]], 
                 [rotated_only[i, 1], transformed[i, 1]], 
                 'red', linestyle=':', alpha=0.5, linewidth=1)
    
    plt.axis('equal')
    plt.xlabel('X轴', fontsize=12)
    plt.ylabel('Y轴', fontsize=12)
    plt.title(f'三角形{triangle_idx+1}变换过程详情\n(旋转{rotate_angle}° + 沿{translate_theta}°方向平移{translate_distance:.2f}单位)', 
              fontsize=12, pad=20)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 可以选择显示某个三角形的详细变换过程（取消注释下面的行）
# plot_individual_transformation(1)  # 显示第二个三角形的详细变换

print(f"\n=== 配置说明 ===")
print(f"基础三角形边长: {b:.3f}")
print(f"基础平移距离: {a/np.sqrt(3):.3f}")
print(f"可通过修改 triangle_configs 列表来调整每个三角形的参数")