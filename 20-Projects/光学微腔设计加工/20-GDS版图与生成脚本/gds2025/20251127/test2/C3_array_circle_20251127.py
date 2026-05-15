import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import os

# Mac中文配置
matplotlib.rcParams['font.sans-serif'] = ['Heiti TC', 'Songti SC', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

# --------------------------
# 1. 基础参数 - 六边形单元定义
# --------------------------
a = 0.5                  # 小六边形单元边长
b = a / 2                # 三角形边长
rotate_center = (0, 0)   # 旋转中心（原点）
circle_radius = 5        # 圆形阵列半径

# --------------------------
# 2. 单元内六个三角形的配置参数
# --------------------------
triangle_configs = [
    [0, 0, 1],           # 三角形1: 旋转0°, 沿0°方向平移
    [60, 60, 1.2],       # 三角形2: 旋转60°, 沿60°方向平移
    [120, 120, 1],       # 三角形3: 旋转120°, 沿120°方向平移  
    [180, 180, 1.2],     # 三角形4: 旋转180°, 沿180°方向平移
    [240, 240, 1],       # 三角形5: 旋转240°, 沿240°方向平移
    [300, 300, 1.2]      # 三角形6: 旋转300°, 沿300°方向平移
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

def is_triangle_completely_inside_circle(triangle, radius):
    """检查三角形是否完全在圆形内部（所有顶点都在圆内）"""
    for point in triangle:
        distance = np.sqrt(point[0]**2 + point[1]**2)
        if distance > radius:
            return False
    return True

def is_triangle_partially_inside_circle(triangle, radius):
    """检查三角形是否部分在圆内（至少有一个顶点在圆内）"""
    for point in triangle:
        distance = np.sqrt(point[0]**2 + point[1]**2)
        if distance <= radius:
            return True
    return False

def generate_optimized_circular_array():
    """优化的圆形阵列生成，只保留完全在圆内的三角形"""
    all_triangles = []
    unit_positions = []
    removed_triangles_count = 0
    partial_triangles_count = 0
    
    # 六边形阵列间距
    spacing_x = 2 * a  # 六边形宽度
    spacing_y = 1.732 * a  # 六边形高度（√3*a）
    
    # 计算单元的最大可能半径（用于初步筛选）
    unit_max_radius = np.sqrt((a + r_triangle)**2 + (a + r_triangle)**2)
    
    # 计算需要的网格范围
    grid_size = int(np.ceil((circle_radius + unit_max_radius) / min(spacing_x, spacing_y))) + 2
    
    # 生成扩展网格的所有单元位置
    for i in range(-grid_size, grid_size + 1):
        for j in range(-grid_size, grid_size + 1):
            # 计算单元中心坐标
            x = i * spacing_x + j * (spacing_x / 2)
            y = j * spacing_y
            
            # 初步筛选：单元中心在扩展圆内
            center_distance = np.sqrt(x**2 + y**2)
            if center_distance <= circle_radius + unit_max_radius:
                unit_center = (x, y)
                unit_positions.append(unit_center)
                
                # 创建该位置的单元
                unit_triangles = create_unit_cell(unit_center)
                
                # 精确筛选：只保留完全在圆形内部的三角形
                for triangle in unit_triangles:
                    if is_triangle_completely_inside_circle(triangle, circle_radius):
                        all_triangles.append(triangle)
                    else:
                        removed_triangles_count += 1
                        # 统计被分割的三角形数量
                        if is_triangle_partially_inside_circle(triangle, circle_radius):
                            partial_triangles_count += 1
    
    print(f"移除的三角形数量: {removed_triangles_count}")
    print(f"其中被圆分割的三角形数量: {partial_triangles_count}")
    return all_triangles, unit_positions

def get_timestamp_filename(prefix="circular_pattern", extension="png"):
    """生成带时间戳的文件名"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.{extension}"
    return filename

def save_high_resolution_image():
    """保存高分辨率图像到当前文件夹"""
    # 创建图形
    fig = plt.figure(figsize=(30, 30))
    
    # 绘制所有三角形
    for i, triangle in enumerate(all_triangles):
        color_idx = i % len(colors)
        plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=0.7,
                 edgecolor=colors[color_idx], linewidth=0.3)
    
    # 绘制圆形轮廓
    circle_angles = np.linspace(0, 2*np.pi, 200)
    circle_x = circle_radius * np.cos(circle_angles)
    circle_y = circle_radius * np.sin(circle_angles)
    plt.plot(circle_x, circle_y, 'k-', linewidth=4, alpha=0.9)
    
    # 标记中心点
    plt.scatter(0, 0, color='red', s=300, marker='*', zorder=10)
    
    # 设置图形属性
    plt.axis('equal')
    plt.axis('off')  # 隐藏坐标轴
    
    # 生成文件名并保存
    filename = get_timestamp_filename()
    filepath = os.path.join(os.getcwd(), filename)
    
    plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    print(f"高分辨率图像已保存为: {filepath}")
    return filepath

def save_preview_image():
    """保存预览图像（带坐标轴信息）"""
    fig = plt.figure(figsize=(20, 20))
    
    # 绘制所有三角形
    for i, triangle in enumerate(all_triangles):
        color_idx = i % len(colors)
        alpha = 0.7
        plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=alpha,
                 edgecolor=colors[color_idx], linewidth=0.5)

    # 标记中心点和圆形轮廓
    plt.scatter(0, 0, color='red', s=200, marker='*', zorder=10, label='阵列中心')
    
    circle_angles = np.linspace(0, 2*np.pi, 200)
    circle_x = circle_radius * np.cos(circle_angles)
    circle_y = circle_radius * np.sin(circle_angles)
    plt.plot(circle_x, circle_y, 'k-', linewidth=4, alpha=0.9, label=f'圆形轮廓 (半径={circle_radius})')
    
    # 设置图形属性
    plt.axis('equal')
    plt.xlabel('X轴', fontsize=14)
    plt.ylabel('Y轴', fontsize=14)
    plt.title(f'精确圆形阵列图案\n(由{total_triangles}个完全在圆内的三角形组成，半径={circle_radius})', 
              fontsize=16, pad=20)
    plt.legend(loc='upper right', fontsize=12)
    plt.grid(True, alpha=0.2)
    
    # 调整坐标轴范围
    if all_triangles:
        all_points = np.vstack(all_triangles)
        x_min, x_max = np.min(all_points[:, 0]), np.max(all_points[:, 0])
        y_min, y_max = np.min(all_points[:, 1]), np.max(all_points[:, 1])
        margin = max(x_max - x_min, y_max - y_min) * 0.05
        plt.xlim(x_min - margin, x_max + margin)
        plt.ylim(y_min - margin, y_max + margin)
    
    # 生成文件名并保存
    filename = get_timestamp_filename("preview", "png")
    filepath = os.path.join(os.getcwd(), filename)
    
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"预览图像已保存为: {filepath}")
    return filepath

# --------------------------
# 5. 生成精确圆形阵列图案
# --------------------------
print("=== 精确圆形阵列图案生成 ===")
print(f"小单元六边形边长: {a}")
print(f"圆形阵列半径: {circle_radius}")
print(f"预计覆盖范围: 直径 {2 * circle_radius}")

# 使用优化的生成函数
all_triangles, unit_positions = generate_optimized_circular_array()
total_units = len(unit_positions)
total_triangles = len(all_triangles)

print(f"处理的单元数量: {total_units}")
print(f"保留的三角形总数: {total_triangles}")

# --------------------------
# 6. 画图显示 - 精确圆形阵列图案
# --------------------------
plt.figure(figsize=(20, 20))

# 绘制所有保留的三角形（完全在圆内的）
for i, triangle in enumerate(all_triangles):
    color_idx = i % len(colors)
    alpha = 0.7
    
    plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=alpha,
             edgecolor=colors[color_idx], linewidth=0.5)

# 标记圆形阵列的中心
plt.scatter(0, 0, color='red', s=200, marker='*', zorder=10, label='阵列中心')

# 绘制圆形轮廓
def draw_circle_outline():
    """绘制圆形的外轮廓"""
    circle_angles = np.linspace(0, 2*np.pi, 200)
    circle_x = circle_radius * np.cos(circle_angles)
    circle_y = circle_radius * np.sin(circle_angles)
    
    plt.plot(circle_x, circle_y, 'k-', linewidth=4, 
             alpha=0.9, label=f'圆形轮廓 (半径={circle_radius})')

draw_circle_outline()

# 图形美化
plt.axis('equal')
plt.xlabel('X轴', fontsize=14)
plt.ylabel('Y轴', fontsize=14)
plt.title(f'精确圆形阵列图案\n(由{total_triangles}个完全在圆内的三角形组成，半径={circle_radius})', 
          fontsize=16, pad=20)

# 添加图例
plt.legend(loc='upper right', fontsize=12)

# 网格和坐标轴
plt.grid(True, alpha=0.2)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# 自动调整坐标轴范围
if all_triangles:
    all_points = np.vstack(all_triangles)
    x_min, x_max = np.min(all_points[:, 0]), np.max(all_points[:, 0])
    y_min, y_max = np.min(all_points[:, 1]), np.max(all_points[:, 1])
    margin = max(x_max - x_min, y_max - y_min) * 0.05
    plt.xlim(x_min - margin, x_max + margin)
    plt.ylim(y_min - margin, y_max + margin)
else:
    plt.xlim(-circle_radius, circle_radius)
    plt.ylim(-circle_radius, circle_radius)

plt.tight_layout()
plt.show()

# --------------------------
# 7. 显示图案统计信息
# --------------------------
def print_pattern_stats():
    """打印图案统计信息"""
    print(f"\n=== 图案统计信息 ===")
    print(f"圆形阵列半径: {circle_radius}")
    print(f"小单元六边形边长: {a}")
    
    if all_triangles:
        all_points = np.vstack(all_triangles)
        max_distance = np.max(np.sqrt(np.sum(all_points**2, axis=1)))
        print(f"实际最大半径: {max_distance:.2f}")
        print(f"安全边界距离: {circle_radius - max_distance:.2f}")
    
    print(f"处理的单元数量: {total_units}")
    print(f"保留的三角形总数: {total_triangles}")

print_pattern_stats()

# --------------------------
# 8. 保存图像文件
# --------------------------
print("\n=== 保存图像文件 ===")
print(f"当前工作目录: {os.getcwd()}")

# 保存高分辨率图像（无坐标轴）
high_res_file = save_high_resolution_image()

# 保存预览图像（带坐标轴信息）
preview_file = save_preview_image()

print(f"\n已保存的文件:")
print(f"- 高分辨率图像: {os.path.basename(high_res_file)}")
print(f"- 预览图像: {os.path.basename(preview_file)}")

# --------------------------
# 9. 边界验证
# --------------------------
def validate_circular_boundary():
    """验证所有三角形确实完全在圆内"""
    if not all_triangles:
        print("没有三角形可验证")
        return
    
    all_valid = True
    for triangle in all_triangles:
        for point in triangle:
            distance = np.sqrt(point[0]**2 + point[1]**2)
            if distance > circle_radius:
                all_valid = False
                break
    
    if all_valid:
        print("✓ 边界验证通过: 所有三角形完全在圆内")
    else:
        print("✗ 边界验证失败: 存在超出圆形的三角形")

print("\n=== 边界验证 ===")
validate_circular_boundary()