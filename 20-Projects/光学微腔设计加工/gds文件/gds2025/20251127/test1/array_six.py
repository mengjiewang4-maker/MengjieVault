import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Mac中文配置
matplotlib.rcParams['font.sans-serif'] = ['Heiti TC', 'Songti SC', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

# --------------------------
# 1. 基础参数 - 六边形单元定义
# --------------------------
a = 0.5                  # 六边形边长（单元尺寸）
b = a / 2                # 三角形边长
rotate_center = (0, 0)   # 旋转中心（原点）

# --------------------------
# 2. 单元内六个三角形的配置参数
# 每个三角形配置: [旋转角度(度), 平移角度(度), 平移距离倍数]
# --------------------------
triangle_configs = [
    # [旋转角度, 平移角度, 平移距离倍数]
    [0, 0, 1],           # 三角形1: 中心三角形，不旋转不平移
    [60, 60, 1],         # 三角形2: 旋转60°, 沿60°方向平移1倍距离
    [120, 120, 1],       # 三角形3: 旋转120°, 沿120°方向平移1倍距离  
    [180, 180, 1],       # 三角形4: 旋转180°, 沿180°方向平移1倍距离
    [240, 240, 1],       # 三角形5: 旋转240°, 沿240°方向平移1倍距离
    [300, 300, 1]        # 三角形6: 旋转300°, 沿300°方向平移1倍距离
]

# 颜色配置
colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
color_names = ['蓝色', '红色', '绿色', '橙色', '紫色', '棕色']

# --------------------------
# 3. 阵列参数配置
# --------------------------
# 阵列排列方式
array_rows = 50           # 行数
array_cols = 50           # 列数
array_spacing_x = 2 * a  # X方向间距（六边形宽度）
array_spacing_y = 1.732 * a  # Y方向间距（六边形高度，√3*a）

# 阵列起始位置
array_start_x = -array_spacing_x  # 起始X坐标
array_start_y = -array_spacing_y  # 起始Y坐标

# --------------------------
# 4. 原始三角形重心严格在原点
# --------------------------
r_triangle = b / np.sqrt(3)  # 等边三角形外接圆半径
triangle_points = np.array([
    [-r_triangle, 0],                                  
    [r_triangle * np.cos(1*np.pi/3), r_triangle * np.sin(1*np.pi/3)],  
    [r_triangle * np.cos(-1*np.pi/3), r_triangle * np.sin(-1*np.pi/3)]   
])

# --------------------------
# 5. 核心函数
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

def create_unit_cell(unit_center=(0, 0)):
    """创建一个完整的六边形单元"""
    base_radius = a / np.sqrt(3)  # 基础平移距离
    unit_triangles = []
    
    for config in triangle_configs:
        rotate_angle, translate_theta, translate_scale = config
        translate_distance = translate_scale * base_radius
        
        # 先旋转后平移
        rotated_points = rotate_points(triangle_points, rotate_angle, rotate_center)
        transformed_points = translate_points(rotated_points, translate_theta, translate_distance)
        
        # 将三角形平移到单元中心位置
        if unit_center != (0, 0):
            transformed_points = transformed_points + np.array(unit_center)
        
        unit_triangles.append(transformed_points)
    
    return unit_triangles

def create_array():
    """创建单元阵列"""
    all_triangles = []
    unit_positions = []
    
    for row in range(array_rows):
        for col in range(array_cols):
            # 计算单元中心位置
            # 交错排列：偶数行正常，奇数行偏移半个间距
            offset_x = 0 if row % 2 == 0 else array_spacing_x / 2
            center_x = array_start_x + col * array_spacing_x + offset_x
            center_y = array_start_y + row * array_spacing_y
            
            unit_center = (center_x, center_y)
            unit_positions.append(unit_center)
            
            # 创建该位置的单元
            unit_triangles = create_unit_cell(unit_center)
            all_triangles.extend(unit_triangles)
    
    return all_triangles, unit_positions

# --------------------------
# 6. 创建阵列并绘制
# --------------------------
print("=== 六边形单元阵列生成 ===")
print(f"单元边长 a = {a}")
print(f"阵列规模: {array_rows} × {array_cols}")
print(f"单元间距: X方向 {array_spacing_x:.3f}, Y方向 {array_spacing_y:.3f}")

all_triangles, unit_positions = create_array()
total_triangles = len(all_triangles)
print(f"生成的三角形总数: {total_triangles}")

# --------------------------
# 7. 画图显示 - 单元阵列
# --------------------------
plt.figure(figsize=(15, 12))

# 绘制所有三角形
for i, triangle in enumerate(all_triangles):
    # 确定颜色：根据在单元内的位置循环使用颜色
    color_idx = i % len(colors)
    unit_idx = i // len(triangle_configs)  # 单元索引
    triangle_in_unit = i % len(triangle_configs)  # 在单元内的三角形索引
    
    # 透明度设置：第一个单元用实色，其他单元用半透明
    alpha = 0.8 if unit_idx == (array_rows * array_cols) // 2 else 0.5
    
    plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=alpha,
             edgecolor=colors[color_idx], linewidth=1)

# 标记单元中心位置
for i, center in enumerate(unit_positions):
    plt.scatter(center[0], center[1], color='black', s=30, marker='+', zorder=5)
    # 可选：显示单元编号
    # plt.text(center[0], center[1], f'U{i}', fontsize=8, ha='center', va='center')

# 标记中心单元（原始单元）
center_unit_idx = (array_rows * array_cols) // 2
if center_unit_idx < len(unit_positions):
    center_pos = unit_positions[center_unit_idx]
    plt.scatter(center_pos[0], center_pos[1], color='red', s=100, marker='*', 
               zorder=6, label='中心单元')

# 图形美化
plt.axis('equal')
plt.xlabel('X轴', fontsize=12)
plt.ylabel('Y轴', fontsize=12)
plt.title(f'六边形三角形单元阵列\n单元边长 a={a}, 阵列规模: {array_rows}×{array_cols}, 三角形总数: {total_triangles}', 
          fontsize=14, pad=20)

# 添加图例说明颜色对应关系
legend_elements = []
for i, (color, color_name) in enumerate(zip(colors, color_names)):
    legend_elements.append(plt.Line2D([0], [0], color=color, lw=4, 
                                     label=f'三角形{i+1} ({color_name})'))
legend_elements.append(plt.Line2D([0], [0], marker='*', color='red', linestyle='None',
                                 markersize=10, label='单元中心'))

plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# 自动调整坐标轴范围
all_points = np.vstack(all_triangles)
x_min, x_max = np.min(all_points[:, 0]), np.max(all_points[:, 0])
y_min, y_max = np.min(all_points[:, 1]), np.max(all_points[:, 1])
margin_x = (x_max - x_min) * 0.1
margin_y = (y_max - y_min) * 0.1
plt.xlim(x_min - margin_x, x_max + margin_x)
plt.ylim(y_min - margin_y, y_max + margin_y)

plt.tight_layout()
plt.show()

# --------------------------
# 8. 可选：单独显示单个单元
# --------------------------
def plot_single_unit(unit_center=(0, 0)):
    """绘制单个六边形单元的详细视图"""
    unit_triangles = create_unit_cell(unit_center)
    
    plt.figure(figsize=(10, 10))
    
    # 绘制单元内的所有三角形
    for i, (triangle, config, color, color_name) in enumerate(zip(
        unit_triangles, triangle_configs, colors, color_names)):
        
        rotate_angle, translate_theta, translate_scale = config
        base_radius = a / np.sqrt(3)
        translate_distance = translate_scale * base_radius
        
        plt.fill(triangle[:, 0], triangle[:, 1], color, alpha=0.7,
                 label=f'三角形{i+1}: 旋转{rotate_angle}°+平移{translate_theta}°', 
                 edgecolor=color, linewidth=2)
        
        # 标记三角形重心
        centroid = np.mean(triangle, axis=0)
        plt.scatter(centroid[0], centroid[1], color=color, s=80, marker='o', zorder=5)
    
    # 标记单元中心
    plt.scatter(unit_center[0], unit_center[1], color='black', s=150, marker='*', 
               label='单元中心', zorder=6)
    
    # 绘制六边形轮廓（可选）
    hex_radius = a  # 六边形外接圆半径
    hex_angles = np.linspace(0, 2*np.pi, 7)
    hex_points = np.column_stack([
        unit_center[0] + hex_radius * np.cos(hex_angles),
        unit_center[1] + hex_radius * np.sin(hex_angles)
    ])
    plt.plot(hex_points[:, 0], hex_points[:, 1], 'k--', alpha=0.5, 
             linewidth=1, label='六边形轮廓')
    
    plt.axis('equal')
    plt.xlabel('X轴', fontsize=12)
    plt.ylabel('Y轴', fontsize=12)
    plt.title(f'单个六边形单元详细视图 (边长 a={a})', fontsize=14, pad=20)
    plt.legend(loc='upper left', fontsize=9)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 可以选择显示单个单元的详细视图（取消注释下面的行）
# plot_single_unit()

print(f"\n=== 阵列配置说明 ===")
print(f"六边形边长 a = {a}")
print(f"三角形边长 b = a/2 = {b:.3f}")
print(f"阵列间距: X方向 {array_spacing_x:.3f}, Y方向 {array_spacing_y:.3f}")
print(f"可通过修改 array_rows 和 array_cols 调整阵列规模")