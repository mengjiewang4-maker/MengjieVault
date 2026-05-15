import gdsfactory as gf
import numpy as np
from numpy import cos, sin, sqrt, pi
import os
from datetime import datetime

# ==============================================
# 核心参数：修复偏移幅度和三角形分布
# ==============================================
HEXAGON_SIDE_LENGTH = 0.5  # 六边形边长 (um)
TRIANGLE_SIDE_LENGTH_RATIO = 1/2  # 三角形相对大小比例

# 图层定义（分图层显示，便于区分）
HEXAGON_LAYER = (1, 0)        # 六边形（红色网格）
TRIANGLE_LAYER_135 = (2, 0)   # 1、3、5号三角形（绿色）
TRIANGLE_LAYER_246 = (3, 0)   # 2、4、6号三角形（蓝色）

# --------------------------
# 1、3、5号三角形 调节参数（C3对称组）
# --------------------------
OFFSET_135_MAGNITUDE = HEXAGON_SIDE_LENGTH * 0.8  # 偏移幅度（远离中心）
OFFSET_135_ANGLE_OFFSET = 0  # 整体偏移方向（不破坏C3对称）
ROTATE_135 = False  # 是否旋转
ROTATE_135_ANGLE = 0  # 旋转角度（整体旋转，保持C3对称）

# --------------------------
# 2、4、6号三角形 调节参数（C3对称组）
# --------------------------
OFFSET_246_MAGNITUDE = HEXAGON_SIDE_LENGTH * 0.8  # 偏移幅度（与135组对称）
OFFSET_246_ANGLE_OFFSET = 0  # 整体偏移方向（不破坏C3对称）
ROTATE_246 = True  # 是否旋转
ROTATE_246_ANGLE = 180  # 旋转角度（整体旋转，保持C3对称）

# ==============================================
# 组件创建函数（不变，保持三角形原始顶点坐标）
# ==============================================
def create_hexagon(side_length, layer):
    hexagon = gf.Component("Hexagon")
    vertices = [
        (side_length * cos(pi/2 + i * pi/3), side_length * sin(pi/2 + i * pi/3))
        for i in range(6)
    ]
    hexagon.add_polygon(vertices, layer=layer)
    return hexagon

def create_small_triangle(side_length, layer):
    triangle = gf.Component("Small_Triangle")
    height = (sqrt(3) / 2) * side_length
    vertices = [
        (0, 0),                      # 尖端（原点）
        (0, side_length), # 右上角
        (side_length / sqrt(3), side_length / 2)   # 右下角
    ]
    triangle.add_polygon(vertices, layer=layer)
    return triangle

# ==============================================
# 组装C3对称结构（核心修改：保证6个三角形初始原点对齐+分别旋转60度）
# ==============================================
def create_c3_symmetric_structure(hexagon_side_length, triangle_side_length):
    final_component = gf.Component("C3_Symmetric_Hexagon_Triangles")
    
    # 创建六边形
    hexagon = create_hexagon(hexagon_side_length, HEXAGON_LAYER)
    final_component << hexagon
    
    # 6个三角形的初始旋转角度（0°, 60°, 120°, 180°, 240°, 300°）- 保证C3对称
    initial_rotation_angles = [i * 60 for i in range(6)]  # 初始旋转60度间隔
    # 分组：1、3、5号（索引0,2,4）属于135组；2、4、6号（索引1,3,5）属于246组
    
    # 循环放置6个三角形
    for i, initial_rot in enumerate(initial_rotation_angles):
        triangle_side = triangle_side_length
        center = (0, 0)  # 所有三角形初始以(0,0)为原点
        
        if i % 2 == 0:
            # --------------------------
            # 1、3、5号三角形（C3对称组）
            # --------------------------
            # 组内角度偏移：0°, 120°, 240°（保持C3对称）
            group_angle = i * 60  # 0°, 120°, 240°
            group_angle_rad = (group_angle + OFFSET_135_ANGLE_OFFSET) * pi / 180
            
            # 计算偏移量（基于组内角度，保持C3对称）
            dx = OFFSET_135_MAGNITUDE * cos(group_angle_rad)
            dy = OFFSET_135_MAGNITUDE * sin(group_angle_rad)
            
            # 创建三角形并应用初始旋转+组旋转
            triangle = create_small_triangle(triangle_side, TRIANGLE_LAYER_135)
            triangle_ref = final_component << triangle
            
            # 1. 初始旋转（60度间隔，保证初始分布）
            triangle_ref.rotate(initial_rot, center=center)
            # 2. 组旋转（可选，保持C3对称）
            if ROTATE_135:
                triangle_ref.rotate(ROTATE_135_ANGLE, center=center)
            # 3. 偏移（保持C3对称的位置偏移）
            triangle_ref.move((dx, dy))
        
        else:
            # --------------------------
            # 2、4、6号三角形（C3对称组）
            # --------------------------
            # 组内角度偏移：60°, 180°, 300°（保持C3对称，与135组错开60°）
            group_angle = i * 60  # 60°, 180°, 300°
            group_angle_rad = (group_angle + OFFSET_246_ANGLE_OFFSET) * pi / 180
            
            # 计算偏移量（基于组内角度，保持C3对称）
            dx = OFFSET_246_MAGNITUDE * cos(group_angle_rad)
            dy = OFFSET_246_MAGNITUDE * sin(group_angle_rad)
            
            # 创建三角形并应用初始旋转+组旋转
            triangle = create_small_triangle(triangle_side, TRIANGLE_LAYER_246)
            triangle_ref = final_component << triangle
            
            # 1. 初始旋转（60度间隔，保证初始分布）
            triangle_ref.rotate(initial_rot, center=center)
            # 2. 组旋转（可选，保持C3对称）
            if ROTATE_246:
                triangle_ref.rotate(ROTATE_246_ANGLE, center=center)
            # 3. 偏移（保持C3对称的位置偏移）
            triangle_ref.move((dx, dy))
    
    return final_component

# ==============================================
# 文件名生成（不变）
# ==============================================
def get_unique_filename(base_name="c3_symmetric_structure", ext="gds"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    seq = 1
    while True:
        filename = f"{base_name}_{timestamp}_{seq}.{ext}"
        full_path = os.path.join(current_dir, filename)
        if not os.path.exists(full_path):
            return full_path
        seq += 1

# ==============================================
# 主程序（仅生成GDS）
# ==============================================
if __name__ == "__main__":
    triangle_side_length = HEXAGON_SIDE_LENGTH * TRIANGLE_SIDE_LENGTH_RATIO
    c3_symmetric_structure = create_c3_symmetric_structure(
        hexagon_side_length=HEXAGON_SIDE_LENGTH,
        triangle_side_length=triangle_side_length
    )
    
    unique_gds_path = get_unique_filename()
    c3_symmetric_structure.write_gds(unique_gds_path)
    
    print("="*60)
    print("✅ GDS文件生成成功！")
    print(f"📁 路径：{unique_gds_path}")
    print("-"*60)
    print("1、3、5号三角形（C3对称组）参数：")
    print(f"  偏移幅度：{OFFSET_135_MAGNITUDE:.4f} um | 整体偏移方向：{OFFSET_135_ANGLE_OFFSET}度")
    print(f"  旋转：{'是' if ROTATE_135 else '否'} | 整体旋转角度：{ROTATE_135_ANGLE}度")
    print(f"  初始旋转：0°、120°、240°（60°间隔，C3对称）")
    print("-"*60)
    print("2、4、6号三角形（C3对称组）参数：")
    print(f"  偏移幅度：{OFFSET_246_MAGNITUDE:.4f} um | 整体偏移方向：{OFFSET_246_ANGLE_OFFSET}度")
    print(f"  旋转：{'是' if ROTATE_246 else '否'} | 整体旋转角度：{ROTATE_246_ANGLE}度")
    print(f"  初始旋转：60°、180°、300°（60°间隔，C3对称）")
    print("="*60)