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
    [60, 60, 1],         # 三角形2: 旋转60°, 沿60°方向平移
    [120, 120, 1],       # 三角形3: 旋转120°, 沿120°方向平移  
    [180, 180, 1],       # 三角形4: 旋转180°, 沿180°方向平移
    [240, 240, 1],       # 三角形5: 旋转240°, 沿240°方向平移
    [300, 300, 1]        # 三角形6: 旋转300°, 沿300°方向平移
]

# 第2、4、6号三角形的额外偏移配置
offset_configs = {
    1: {'offset_distance': 0.1, 'offset_angle': 60},    # 三角形2：沿60°方向平移
    3: {'offset_distance': 0.1, 'offset_angle': 180},   # 三角形4：沿180°方向平移  
    5: {'offset_distance': 0.1, 'offset_angle': 300}    # 三角形6：沿300°方向平移
}

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

def translate_points(points, dx, dy):
    """平移点集"""
    return points + np.array([dx, dy])

def get_triangle_centroid(triangle):
    """计算三角形的重心"""
    return np.mean(triangle, axis=0)

def create_unit_cell_without_offset(unit_center=(0, 0)):
    """创建没有额外偏移的基础单元，用于对比"""
    base_radius = a / np.sqrt(3)
    unit_triangles = []
    
    # 第一步：构建基础六边形单元（六个三角形各自完成旋转和平移）
    for config in triangle_configs:
        rotate_angle, translate_theta, translate_scale = config
        translate_distance = translate_scale * base_radius
        
        # 先旋转后平移
        rotated_points = rotate_points(triangle_points, rotate_angle, rotate_center)
        theta_rad = np.radians(translate_theta)
        dx_base = translate_distance * np.cos(theta_rad)
        dy_base = translate_distance * np.sin(theta_rad)
        transformed_points = rotated_points + np.array([dx_base, dy_base])
        
        unit_triangles.append(transformed_points)
    
    # 第二步：整体平移使1号三角形重心到原点
    triangle1_centroid = get_triangle_centroid(unit_triangles[0])
    dx_center = -triangle1_centroid[0]
    dy_center = -triangle1_centroid[1]
    
    centered_triangles = []
    for triangle in unit_triangles:
        centered_triangle = translate_points(triangle, dx_center, dy_center)
        centered_triangles.append(centered_triangle)
    
    # 将整个单元平移到指定的单元中心位置
    if unit_center != (0, 0):
        for i in range(len(centered_triangles)):
            centered_triangles[i] = translate_points(centered_triangles[i], unit_center[0], unit_center[1])
    
    return centered_triangles

def create_unit_cell(unit_center=(0, 0)):
    """创建完整的六边形单元：
    1. 构建六个三角形（各自完成旋转和平移）
    2. 整体平移所有三角形，使1号三角形的重心到原点(0,0)
    3. 以原点(0,0)为基准，对第2、4、6号三角形添加额外偏移
    """
    base_radius = a / np.sqrt(3)
    unit_triangles = []
    
    # 第一步：构建六个三角形（各自完成旋转和平移）
    for config in triangle_configs:
        rotate_angle, translate_theta, translate_scale = config
        translate_distance = translate_scale * base_radius
        
        # 先旋转后平移
        rotated_points = rotate_points(triangle_points, rotate_angle, rotate_center)
        theta_rad = np.radians(translate_theta)
        dx_base = translate_distance * np.cos(theta_rad)
        dy_base = translate_distance * np.sin(theta_rad)
        transformed_points = rotated_points + np.array([dx_base, dy_base])
        
        unit_triangles.append(transformed_points)
    
    # 第二步：整体平移使1号三角形重心到原点
    triangle1_centroid = get_triangle_centroid(unit_triangles[0])
    dx_center = -triangle1_centroid[0]
    dy_center = -triangle1_centroid[1]
    
    centered_triangles = []
    for triangle in unit_triangles:
        centered_triangle = translate_points(triangle, dx_center, dy_center)
        centered_triangles.append(centered_triangle)
    
    # 第三步：以原点(0,0)为基准，对第2、4、6号三角形添加额外偏移
    final_triangles = []
    triangle_types = []  # 记录三角形类型：0-无偏移，1-有偏移
    
    for i, triangle in enumerate(centered_triangles):
        # 检查是否为第2、4、6号三角形（索引1,3,5）
        if i in offset_configs:
            offset_config = offset_configs[i]
            offset_distance = offset_config['offset_distance']
            offset_angle = offset_config['offset_angle']
            
            # 应用额外偏移（以(0,0)为基准）
            offset_rad = np.radians(offset_angle)
            dx_offset = offset_distance * np.cos(offset_rad)
            dy_offset = offset_distance * np.sin(offset_rad)
            final_triangle = translate_points(triangle, dx_offset, dy_offset)
            
            final_triangles.append(final_triangle)
            triangle_types.append(1)  # 标记为有偏移的三角形
        else:
            final_triangles.append(triangle)
            triangle_types.append(0)  # 标记为无偏移的三角形
    
    # 最后：将整个单元平移到指定的单元中心位置
    if unit_center != (0, 0):
        for i in range(len(final_triangles)):
            final_triangles[i] = translate_points(final_triangles[i], unit_center[0], unit_center[1])
    
    return final_triangles, triangle_types

def is_triangle_completely_inside_circle(triangle, radius):
    """检查三角形是否完全在圆形内部"""
    for point in triangle:
        distance = np.sqrt(point[0]**2 + point[1]**2)
        if distance > radius:
            return False
    return True

def is_triangle_partially_inside_circle(triangle, radius):
    """检查三角形是否部分在圆内"""
    for point in triangle:
        distance = np.sqrt(point[0]**2 + point[1]**2)
        if distance <= radius:
            return True
    return False

def generate_optimized_circular_array():
    """优化的圆形阵列生成"""
    all_triangles = []
    all_triangle_types = []
    unit_positions = []
    removed_triangles_count = 0
    partial_triangles_count = 0
    
    # 六边形阵列间距
    spacing_x = 2 * a
    spacing_y = 1.732 * a
    
    # 计算单元的最大可能半径
    unit_max_radius = np.sqrt((a + r_triangle)**2 + (a + r_triangle)**2)
    
    # 计算需要的网格范围
    grid_size = int(np.ceil((circle_radius + unit_max_radius) / min(spacing_x, spacing_y))) + 2
    
    # 生成扩展网格的所有单元位置
    for i in range(-grid_size, grid_size + 1):
        for j in range(-grid_size, grid_size + 1):
            x = i * spacing_x + j * (spacing_x / 2)
            y = j * spacing_y
            
            center_distance = np.sqrt(x**2 + y**2)
            if center_distance <= circle_radius + unit_max_radius:
                unit_center = (x, y)
                unit_positions.append(unit_center)
                
                # 创建该位置的单元
                unit_triangles, unit_triangle_types = create_unit_cell(unit_center)
                
                for idx, triangle in enumerate(unit_triangles):
                    if is_triangle_completely_inside_circle(triangle, circle_radius):
                        all_triangles.append(triangle)
                        all_triangle_types.append(unit_triangle_types[idx])
                    else:
                        removed_triangles_count += 1
                        if is_triangle_partially_inside_circle(triangle, circle_radius):
                            partial_triangles_count += 1
    
    print(f"移除的三角形数量: {removed_triangles_count}")
    print(f"其中被圆分割的三角形数量: {partial_triangles_count}")
    
    if all_triangle_types:
        offset_count = sum(all_triangle_types)
        no_offset_count = len(all_triangle_types) - offset_count
        print(f"无偏移三角形数量: {no_offset_count}")
        print(f"有偏移三角形数量: {offset_count}")
    
    return all_triangles, all_triangle_types, unit_positions

def save_gds_file_optimized(all_triangles, all_triangle_types):
    """优化的GDS文件保存"""
    try:
        component = Component("C3_circular_array_with_offset")
        
        # 定义层映射
        layers_no_offset = (1, 0)   # 无偏移三角形
        layers_with_offset = (2, 0) # 有偏移三角形
        
        print("正在生成GDS多边形...")
        
        triangle_count = 0
        offset_count = 0
        no_offset_count = 0
        
        for i, (triangle, triangle_type) in enumerate(zip(all_triangles, all_triangle_types)):
            if triangle_type == 0:
                layer = layers_no_offset
                no_offset_count += 1
            else:
                layer = layers_with_offset
                offset_count += 1
            
            poly_points = [(point[0], point[1]) for point in triangle]
            component.add_polygon(poly_points, layer=layer[0])
            triangle_count += 1
            
            if triangle_count % 100 == 0:
                print(f"已处理 {triangle_count}/{len(all_triangles)} 个三角形")
        
        filename = f"C3_array_offset_centered_r{circle_radius}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.gds"
        filepath = os.path.join(os.getcwd(), filename)
        
        component.write_gds(filepath)
        print(f"✓ GDS文件已保存: {filepath}")
        print(f"✓ 组件包含 {triangle_count} 个多边形")
        print(f"  - 无偏移三角形: {no_offset_count} 个 (层1)")
        print(f"  - 有偏移三角形: {offset_count} 个 (层2)")
        
        return filepath
        
    except Exception as e:
        print(f"✗ GDS保存失败: {e}")
        return None

def quick_visualization(all_triangles, all_triangle_types):
    """快速可视化，通过颜色和样式展示额外偏移效果"""
    try:
        print("正在生成带偏移展示的预览图...")
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 10))
        
        # 颜色定义
        COLOR_NO_OFFSET = 'blue'      # 无偏移三角形
        COLOR_WITH_OFFSET = 'red'     # 有额外偏移三角形  
        COLOR_BASE = 'lightgray'      # 原始位置
        COLOR_CENTER = 'green'        # 中心标记
        
        # 左图：完整阵列视图
        for i, (triangle, triangle_type) in enumerate(zip(all_triangles, all_triangle_types)):
            if triangle_type == 0:
                color = COLOR_NO_OFFSET
                alpha = 0.6
                linewidth = 0.1
            else:
                color = COLOR_WITH_OFFSET
                alpha = 0.8
                linewidth = 0.5
            
            ax1.fill(triangle[:, 0], triangle[:, 1], color, alpha=alpha,
                    edgecolor='black', linewidth=linewidth)
        
        # 绘制圆形轮廓
        circle_angles = np.linspace(0, 2*np.pi, 100)
        circle_x = circle_radius * np.cos(circle_angles)
        circle_y = circle_radius * np.sin(circle_angles)
        ax1.plot(circle_x, circle_y, 'k-', linewidth=2, alpha=0.8)
        
        ax1.axis('equal')
        ax1.set_title(f'完整C3圆形阵列\n(半径={circle_radius}, 三角形总数={len(all_triangles)})', fontsize=16)
        ax1.grid(True, alpha=0.3)
        
        # 中图：中心单元偏移对比
        # 获取无偏移的基础单元
        base_triangles = create_unit_cell_without_offset((0, 0))
        # 获取有偏移的最终单元
        final_triangles, final_types = create_unit_cell((0, 0))
        
        print(f"中心单元三角形类型分布: {final_types}")
        
        # 绘制无偏移的基础三角形（半透明虚线边框）
        for i, triangle in enumerate(base_triangles):
            if i in offset_configs:  # 只绘制246号三角形的基础位置
                ax2.fill(triangle[:, 0], triangle[:, 1], COLOR_BASE, alpha=0.3,
                        edgecolor='gray', linewidth=1.5, linestyle='--')
        
        # 绘制有偏移的最终三角形
        for i, (triangle, triangle_type) in enumerate(zip(final_triangles, final_types)):
            if i in offset_configs:  # 只绘制246号三角形
                color = COLOR_WITH_OFFSET
                edgecolor = 'darkred'
                linewidth = 1.5
                
                ax2.fill(triangle[:, 0], triangle[:, 1], color, alpha=0.8,
                        edgecolor=edgecolor, linewidth=linewidth)
                
                # 在三角形中心添加标记
                centroid = get_triangle_centroid(triangle)
                ax2.plot(centroid[0], centroid[1], 'ro', markersize=4, alpha=0.8)
        
        # 特别标记1号三角形的重心（现在应该在原点）
        if len(final_triangles) > 0:
            triangle1_centroid = get_triangle_centroid(final_triangles[0])
            ax2.scatter(triangle1_centroid[0], triangle1_centroid[1], color='green', s=100, 
                       marker='*', zorder=10, label='1号三角形重心')
        
        # 标记原点
        ax2.scatter(0, 0, color='black', s=200, marker='+', zorder=10, linewidth=3)
        ax2.text(0.15, 0.15, '原点', fontsize=14, color='black', weight='bold')
        
        ax2.axis('equal')
        ax2.set_title('中心单元 - 偏移效果对比\n(虚线: 原始位置, 实线: 最终位置)', fontsize=16)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(-1.5, 1.5)
        ax2.set_ylim(-1.5, 1.5)
        
        # 右图：周边单元偏移对比
        example_pos = (2 * a, 1.732 * a)  # 周边单元位置
        base_neighbor = create_unit_cell_without_offset(example_pos)
        final_neighbor, neighbor_types = create_unit_cell(example_pos)
        
        print(f"周边单元三角形类型分布: {neighbor_types}")
        
        # 绘制无偏移的基础三角形
        for i, triangle in enumerate(base_neighbor):
            if i in offset_configs:  # 只绘制246号三角形的基础位置
                ax3.fill(triangle[:, 0], triangle[:, 1], COLOR_BASE, alpha=0.3,
                        edgecolor='gray', linewidth=1.5, linestyle='--')
        
        # 绘制有偏移的最终三角形
        for i, (triangle, triangle_type) in enumerate(zip(final_neighbor, neighbor_types)):
            if i in offset_configs:  # 只绘制246号三角形
                color = COLOR_WITH_OFFSET
                edgecolor = 'darkred'
                linewidth = 1.5
                
                ax3.fill(triangle[:, 0], triangle[:, 1], color, alpha=0.8,
                        edgecolor=edgecolor, linewidth=linewidth)
                
                # 在三角形中心添加红色标记
                centroid = get_triangle_centroid(triangle)
                ax3.plot(centroid[0], centroid[1], 'ro', markersize=4, alpha=0.8)
        
        ax3.axis('equal')
        ax3.set_title('周边单元 - 所有246号三角形都有偏移', fontsize=16)
        ax3.grid(True, alpha=0.3)
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLOR_NO_OFFSET, alpha=0.6, label='无偏移三角形 (1,3,5号)'),
            Patch(facecolor=COLOR_WITH_OFFSET, alpha=0.8, label='有额外偏移三角形 (2,4,6号)'),
            Patch(facecolor=COLOR_BASE, alpha=0.3, edgecolor='gray', linestyle='--', label='原始位置'),
            plt.Line2D([0], [0], marker='o', color='red', markerfacecolor='red', 
                      markersize=6, label='有偏移三角形中心', linestyle=''),
            plt.Line2D([0], [0], marker='*', color='green', markerfacecolor='green',
                      markersize=10, label='1号三角形重心', linestyle=''),
            plt.Line2D([0], [0], marker='+', color='black', markerfacecolor='black',
                      markersize=8, label='坐标原点', linestyle='')
        ]
        
        ax2.legend(handles=legend_elements, loc='upper right', fontsize=11)
        
        # 添加整体说明
        fig.suptitle('C3对称圆形阵列 - 246号三角形额外偏移可视化展示\n'
                    '处理流程: 1.构建六个三角形(各自旋转平移) → 2.整体平移使1号三角形重心到原点 → 3.以原点为基准对246号三角形添加偏移\n'
                    '偏移方向: 三角形2(60°方向) 三角形4(180°方向) 三角形6(300°方向) 各+0.1倍偏移', 
                    fontsize=16, y=0.96)
        
        plt.tight_layout(rect=[0, 0, 1, 0.93])  # 为顶部标题留出空间
        
        preview_file = os.path.join(os.getcwd(), f"preview_offset_centered_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(preview_file, dpi=200, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 带偏移展示的预览图已保存: {preview_file}")
        return preview_file
        
    except Exception as e:
        print(f"✗ 预览图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None

# --------------------------
# 5. 主程序执行
# --------------------------
def main():
    print("=== C3对称圆形阵列GDS生成器 ===")
    print(f"小单元六边形边长: {a}")
    print(f"圆形阵列半径: {circle_radius}")
    print(f"旋转中心: {rotate_center}")
    
    # 解释处理流程
    print("\n=== 处理流程 ===")
    print("1. 构建六个三角形（各自完成旋转和平移）")
    print("2. 整体平移所有三角形，使1号三角形重心到原点(0,0)")
    print("3. 以原点(0,0)为基准，对第2、4、6号三角形添加额外偏移")
    print("4. 将整个单元平移到网格位置")
    
    # 打印偏移配置
    print("\n=== 偏移配置 ===")
    for triangle_idx, config in offset_configs.items():
        triangle_num = triangle_idx + 1
        print(f"三角形{triangle_num}:")
        print(f"  - 额外偏移距离: {config['offset_distance']}")
        print(f"  - 额外偏移角度: {config['offset_angle']}°")
        print(f"  - 偏移方向: 沿{config['offset_angle']}°方向平移")
    
    # 生成阵列
    all_triangles, all_triangle_types, unit_positions = generate_optimized_circular_array()
    total_units = len(unit_positions)
    total_triangles = len(all_triangles)
    
    print(f"\n✓ 处理的单元数量: {total_units}")
    print(f"✓ 保留的三角形总数: {total_triangles}")
    
    # 显示统计信息
    if all_triangles:
        all_points = np.vstack(all_triangles)
        max_distance = np.max(np.sqrt(np.sum(all_points**2, axis=1)))
        print(f"✓ 实际最大半径: {max_distance:.2f}")
        print(f"✓ 安全边界距离: {circle_radius - max_distance:.2f}")
    
    # 生成预览图（重点展示偏移效果）
    print("\n=== 生成带偏移展示的预览图 ===")
    preview_file = quick_visualization(all_triangles, all_triangle_types)
    
    # 保存GDS文件
    print("\n=== 生成GDS文件 ===")
    gds_file = save_gds_file_optimized(all_triangles, all_triangle_types)
    
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