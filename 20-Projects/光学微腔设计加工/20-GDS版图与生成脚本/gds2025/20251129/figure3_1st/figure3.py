import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import os
import gdsfactory as gf
from gdsfactory.component import Component
import signal
import sys

# 设置中断信号处理
def signal_handler(sig, frame):
    print('\n程序被用户中断')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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

def save_gds_file_optimized():
    """优化的GDS文件保存，避免显示问题"""
    try:
        # 创建新的组件
        component = Component("C3_circular_array")
        
        # 定义层映射
        layers = {
            0: (1, 0),  # 三角形1
            1: (2, 0),  # 三角形2
            2: (3, 0),  # 三角形3
            3: (4, 0),  # 三角形4
            4: (5, 0),  # 三角形5
            5: (6, 0)   # 三角形6
        }
        
        print("正在生成GDS多边形...")
        
        # 批量添加三角形，提高效率
        triangle_count = 0
        for i, triangle in enumerate(all_triangles):
            layer_idx = i % 6
            layer = layers[layer_idx]
            
            # 直接创建多边形，不创建临时组件
            poly_points = [(point[0], point[1]) for point in triangle]
            component.add_polygon(poly_points, layer=layer[0])
            triangle_count += 1
            
            # 进度显示
            if triangle_count % 100 == 0:
                print(f"已处理 {triangle_count}/{len(all_triangles)} 个三角形")
        
        # 生成文件名
        filename = f"C3_circular_array_r{circle_radius}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.gds"
        filepath = os.path.join(os.getcwd(), filename)
        
        # 保存GDS文件
        print("正在保存GDS文件...")
        component.write_gds(filepath)
        print(f"✓ GDS文件已保存: {filepath}")
        print(f"✓ 组件包含 {triangle_count} 个多边形")
        
        return filepath
        
    except Exception as e:
        print(f"✗ GDS保存失败: {e}")
        return None

def quick_visualization():
    """快速可视化，避免matplotlib显示问题"""
    try:
        print("正在生成快速预览...")
        fig = plt.figure(figsize=(12, 12))
        
        # 只绘制部分三角形以提高速度
        sample_triangles = all_triangles[::2]  # 每隔一个取一个
        
        for i, triangle in enumerate(sample_triangles):
            color_idx = i % len(colors)
            plt.fill(triangle[:, 0], triangle[:, 1], colors[color_idx], alpha=0.6,
                    edgecolor='black', linewidth=0.2)
        
        # 绘制圆形轮廓
        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = circle_radius * np.cos(circle_angles)
        circle_y = circle_radius * np.sin(circle_angles)
        plt.plot(circle_x, circle_y, 'r-', linewidth=2, alpha=0.8)
        
        plt.axis('equal')
        plt.title(f'C3圆形阵列预览 (半径={circle_radius}, 三角形数={len(all_triangles)})')
        plt.grid(True, alpha=0.3)
        
        # 保存预览图但不显示
        preview_file = os.path.join(os.getcwd(), f"preview_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(preview_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 预览图已保存: {preview_file}")
        return preview_file
        
    except Exception as e:
        print(f"✗ 预览图生成失败: {e}")
        return None

# --------------------------
# 5. 主程序执行
# --------------------------
def main():
    print("=== C3对称圆形阵列GDS生成器 ===")
    print(f"小单元六边形边长: {a}")
    print(f"圆形阵列半径: {circle_radius}")
    print(f"预计覆盖范围: 直径 {2 * circle_radius}")
    
    # 生成阵列
    global all_triangles, unit_positions
    all_triangles, unit_positions = generate_optimized_circular_array()
    total_units = len(unit_positions)
    total_triangles = len(all_triangles)
    
    print(f"✓ 处理的单元数量: {total_units}")
    print(f"✓ 保留的三角形总数: {total_triangles}")
    
    # 显示统计信息
    if all_triangles:
        all_points = np.vstack(all_triangles)
        max_distance = np.max(np.sqrt(np.sum(all_points**2, axis=1)))
        print(f"✓ 实际最大半径: {max_distance:.2f}")
        print(f"✓ 安全边界距离: {circle_radius - max_distance:.2f}")
    
    # 保存GDS文件
    print("\n=== 生成GDS文件 ===")
    gds_file = save_gds_file_optimized()
    
    # 生成预览图
    print("\n=== 生成预览图 ===")
    preview_file = quick_visualization()
    
    # 边界验证
    print("\n=== 边界验证 ===")
    if all_triangles:
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
    else:
        print("⚠ 没有三角形可验证")
    
    print(f"\n=== 完成 ===")
    if gds_file:
        print(f"GDS文件: {os.path.basename(gds_file)}")
    if preview_file:
        print(f"预览图: {os.path.basename(preview_file)}")
    print(f"工作目录: {os.getcwd()}")

if __name__ == "__main__":
    main()