import gdsfactory as gf
import numpy as np
import os
from datetime import datetime

# --------------------------
# 基础参数配置（可按需调整）
# --------------------------
SIDE_LENGTH = 0.2  # 六边形边长（单位：μm，200nm = 0.2μm）
LAYER_HEXAGON = 1  # 六边形所在图层
LAYER_TRIANGLES = 2  # 三角形所在图层
SCALE_FACTOR = 1/3  # 三角形缩小比例（0 < scale_factor < 1）
ROTATE_ANGLE = 30  # 三角形旋转角度（单位：度），可设为0、15、45等任意角度
FILE_SERIAL = 1  # 文件序号（可手动调整或自动递增）

# --------------------------
# 工具函数：旋转矩阵
# --------------------------
def rotate_point(point, angle_deg):
    """
    对单个点应用旋转矩阵（围绕原点旋转）
    :param point: 原始坐标 (x, y)
    :param angle_deg: 旋转角度（单位：度），正角为逆时针旋转
    :return: 旋转后的坐标 (x', y')
    """
    angle_rad = np.radians(angle_deg)  # 角度转弧度
    # 2D旋转矩阵
    cosθ = np.cos(angle_rad)
    sinθ = np.sin(angle_rad)
    x = point[0] * cosθ - point[1] * sinθ
    y = point[0] * sinθ + point[1] * cosθ
    return (x, y)

# --------------------------
# 文件名生成函数
# --------------------------
def get_gds_filename(serial_num):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 文件名包含旋转角度，便于区分
    filename = f"hexagon_triangles_rot{ROTATE_ANGLE}deg_{current_time}_serial{serial_num}.gds"
    code_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(code_dir, filename)
    return full_path

# --------------------------
# 图形生成函数（结合旋转矩阵）
# --------------------------
def create_hexagon_points(side_length):
    """生成正六边形顶点坐标（重心在原点）"""
    points = []
    angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
    for angle in angles:
        x = side_length * np.cos(angle)
        y = side_length * np.sin(angle)
        points.append((x, y))
    return points

def create_triangle_points(side_length, scale_factor, triangle_index, rotate_angle_deg):
    """
    生成等边三角形顶点坐标（支持旋转，重心对齐原大三角形）
    :param side_length: 原六边形边长
    :param scale_factor: 缩小比例
    :param triangle_index: 三角形索引（0-5）
    :param rotate_angle_deg: 旋转角度（单位：度）
    :return: 旋转后的等边三角形顶点坐标
    """
    base_angle = triangle_index * np.pi / 3  # 原大三角形起始角度（0°, 60°, ..., 300°）
    angle1 = base_angle
    angle2 = base_angle + np.pi/3
    
    # 等边三角形外接圆半径（确保边长=scale_factor×side_length）
    r = (side_length * scale_factor) / np.sqrt(3)
    
    # 生成原始等边三角形的三个顶点（未旋转）
    original_angles = [
        angle1,
        angle2,
        base_angle + np.pi/6  # 角平分线方向（保证等边）
    ]
    original_points = [
        (r * np.cos(ang), r * np.sin(ang)) for ang in original_angles
    ]
    
    # 对每个顶点应用旋转矩阵（核心步骤）
    rotated_points = [rotate_point(point, rotate_angle_deg) for point in original_points]
    
    return rotated_points

# --------------------------
# 主程序
# --------------------------
if __name__ == "__main__":
    # 创建GDS组件
    c = gf.Component("hexagon_with_rotated_equilateral_triangles")
    
    # 1. 绘制图层1的正六边形
    hexagon_points = create_hexagon_points(SIDE_LENGTH)
    c.add_polygon(hexagon_points, layer=LAYER_HEXAGON)
    
    # 2. 绘制图层2的6个旋转等边三角形
    for i in range(6):
        triangle_points = create_triangle_points(
            side_length=SIDE_LENGTH,
            scale_factor=SCALE_FACTOR,
            triangle_index=i,
            rotate_angle_deg=ROTATE_ANGLE  # 传入旋转角度
        )
        c.add_polygon(triangle_points, layer=LAYER_TRIANGLES)
    
    # 3. 保存GDS文件
    gds_path = get_gds_filename(FILE_SERIAL)
    c.write_gds(gds_path)
    
    # 输出信息
    print("="*60)
    print("GDS文件生成完成！")
    print(f"文件路径：{gds_path}")
    print(f"核心参数：")
    print(f"  - 六边形（图层{LAYER_HEXAGON}）：边长{int(SIDE_LENGTH*1000)}nm，重心(0,0)")
    print(f"  - 三角形（图层{LAYER_TRIANGLES}）：6个严格等边三角形")
    print(f"    - 三角形边长：{int(SIDE_LENGTH*1000*SCALE_FACTOR)}nm（原边长×{SCALE_FACTOR}）")
    print(f"    - 旋转角度：{ROTATE_ANGLE}°（逆时针为正）")
    print(f"    - 重心：与原大三角形重心重合，整体重心(0,0)")
    print(f"  - 文件序号：{FILE_SERIAL}")
    print("="*60)