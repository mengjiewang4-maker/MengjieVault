import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Mac中文配置
matplotlib.rcParams['font.sans-serif'] = ['Heiti TC', 'Songti SC', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

# --------------------------
# 1. 基础参数 - 六边形单元定义
# --------------------------
a = 0.5                  # 小六边形单元边长
b = a / 2                # 三角形边长
rotate_center = (0, 0)   # 旋转中心（原点）
large_hex_size = 50      # 大六边形边长（由50个小六边形组成）

# --------------------------
# 2. 单元内六个三角形的配置参数
# --------------------------
triangle_configs = [
    [0, 0, 1],           # 三角形1: 旋转0°, 沿0°方向平移
    [60, 60, 1.2],         # 三角形2: 旋转60°, 沿60°方向平移
    [120, 120, 1],       # 三角形3: 旋转120°, 沿120°方向平移  
    [180, 180, 1.2],       # 三角形4: 旋转180°, 沿180°方向平移
    [240, 240, 1],       # 三角形5: 旋转240°, 沿240°方向平移
    [300, 300, 1.2]        # 三角形6: 旋转300°, 沿300°方向平移
]

# 颜色配置
colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']

# --------------------------
# 3. 原始三角形定义
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
    return points + np.array([dx, dy])

def create_unit_cell(unit_center=(0, 0)):
    """创建一个完整的六边形单元"""
    base_radius = a / np.sqrt(3)
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

def generate_large_hexagon():
    """生成大六边形图案"""
    all_triangles = []
    unit_positions = []
    
    # 六边形阵列间距
    spacing_x = 2 * a  # 六边形宽度
    spacing_y = 1.732 * a  # 六边形高度（√3*a）
    
    # 生成大六边形的所有单元位置
    for i in range(-large_hex_size + 1, large_hex_size):
        for j in range(-large_hex_size + 1, large_hex_size):
            # 六边形边界条件：|i| + |j| + |k| <= 2*(size-1)，其中 k = -i-j
            k = -i - j
            if abs(i) + abs(j) + abs(k) <= 2 * (large_hex_size - 1):
                # 计算单元中心坐标（六边形网格坐标转笛卡尔坐标）
                x = i * spacing_x + j * (spacing_x / 2)
                y = j * spacing_y
                
                unit_center = (x, y)
                unit_positions.append(unit_center)
                
                # 创建该位置的单元
                unit_triangles = create_unit_cell(unit_center)
                all_triangles.extend(unit_triangles)
    
    return all_triangles, unit_positions

# --------------------------
# 5. 生成大六边形图案
# --------------------------
print("=== 大六边形图案生成 ===")
print(f"小单元六边形边长: {a}")
print(f"大六边形边长: {large_hex_size} 个小单元")
print(f"预计单元数量: {3 * large_hex_size * (large_hex_size - 1) + 1}")

all_triangles, unit_positions = generate_large_hexagon()  # 修正了函数名
total_units = len(unit_positions)
total_triangles = len(all_triangles)

print(f"实际生成的单元数量: {total_units}")
print(f"三角形总数: {total_triangles}")

# --------------------------
# 6. 画图显示 - 大规模六边形图案
# --------------------------
plt.figure(figsize=(20, 20))

# 绘制所有三角形（使用统一的颜色和透明度以获得更好的视觉效果）
for i, triangle in enumerate(all_triangles):
    # 根据在单元内的位置确定颜色
    color_idx = i % len(colors)
    
    # 使用统一的透明度
    alpha = 0.7
    
    plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=alpha,
             edgecolor=colors[color_idx], linewidth=0.5)

# 标记大六边形的中心
plt.scatter(0, 0, color='red', s=200, marker='*', zorder=10, label='大六边形中心')

# 绘制大六边形轮廓
def draw_large_hexagon_outline():
    """绘制大六边形的外轮廓"""
    # 计算大六边形的顶点
    large_hex_radius = large_hex_size * a  # 大六边形外接圆半径
    hex_angles = np.linspace(0, 2*np.pi, 7)
    hex_vertices = np.column_stack([
        large_hex_radius * np.cos(hex_angles),
        large_hex_radius * np.sin(hex_angles)
    ])
    
    plt.plot(hex_vertices[:, 0], hex_vertices[:, 1], 'k-', linewidth=3, 
             alpha=0.8, label='大六边形轮廓')

draw_large_hexagon_outline()

# 图形美化
plt.axis('equal')
plt.xlabel('X轴', fontsize=14)
plt.ylabel('Y轴', fontsize=14)
plt.title(f'大六边形图案\n(由{total_units}个小六边形单元组成，边长={large_hex_size}个单元)', 
          fontsize=16, pad=20)

# 添加图例
plt.legend(loc='upper right', fontsize=12)

# 网格和坐标轴
plt.grid(True, alpha=0.2)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# 自动调整坐标轴范围
all_points = np.vstack(all_triangles)
x_min, x_max = np.min(all_points[:, 0]), np.max(all_points[:, 0])
y_min, y_max = np.min(all_points[:, 1]), np.max(all_points[:, 1])
margin = max(x_max - x_min, y_max - y_min) * 0.05
plt.xlim(x_min - margin, x_max + margin)
plt.ylim(y_min - margin, y_max + margin)

plt.tight_layout()
plt.show()

# --------------------------
# 7. 可选：显示图案统计信息
# --------------------------
def print_pattern_stats():
    """打印图案统计信息"""
    print(f"\n=== 图案统计信息 ===")
    print(f"大六边形边长: {large_hex_size} 个单元")
    print(f"小单元六边形边长: {a}")
    print(f"大六边形实际半径: {large_hex_size * a:.2f}")
    print(f"单元总数: {total_units}")
    print(f"三角形总数: {total_triangles}")
    print(f"图案覆盖范围: X[{x_min:.2f}, {x_max:.2f}], Y[{y_min:.2f}, {y_max:.2f}]")
    
    # 理论单元数量计算（六边形数公式）
    theoretical_units = 3 * large_hex_size * (large_hex_size - 1) + 1
    print(f"理论单元数量: {theoretical_units}")
    print(f"实际/理论匹配: {total_units == theoretical_units}")

print_pattern_stats()

# --------------------------
# 8. 可选：保存高分辨率图像
# --------------------------
def save_high_resolution():
    """保存高分辨率图像"""
    fig = plt.figure(figsize=(30, 30))
    
    # 重新绘制所有三角形
    for i, triangle in enumerate(all_triangles):
        color_idx = i % len(colors)
        plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=0.7,
                 edgecolor=colors[color_idx], linewidth=0.3)
    
    # 绘制轮廓和标记
    draw_large_hexagon_outline()
    plt.scatter(0, 0, color='red', s=300, marker='*', zorder=10)
    
    plt.axis('equal')
    plt.axis('off')  # 隐藏坐标轴
    
    # 保存图像
    filename = f'large_hexagon_pattern_{large_hex_size}units.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print(f"\n高分辨率图像已保存为: {filename}")

# 取消注释下面的行来保存高分辨率图像
save_high_resolution()