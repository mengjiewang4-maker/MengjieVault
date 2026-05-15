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
# 1、3、5号三角形 调节参数（修复偏移）
# --------------------------
OFFSET_135_MAGNITUDE = HEXAGON_SIDE_LENGTH * 0.8  # 偏移幅度（约0.4um，远离中心）
OFFSET_135_ANGLE_OFFSET = 0  # 偏移方向（默认对称方向）
ROTATE_135 = False  # 不旋转
ROTATE_135_ANGLE = 0
ROTATE_135_CENTER = (0, 0)

# --------------------------
# 2、4、6号三角形 调节参数（修复偏移和旋转）
# --------------------------
OFFSET_246_MAGNITUDE = HEXAGON_SIDE_LENGTH * 0.8  # 偏移幅度（与135号对称）
OFFSET_246_ANGLE_OFFSET = 0  # 偏移方向（默认对称方向）
ROTATE_246 = True  # 旋转180度以区分方向
ROTATE_246_ANGLE = 0  # 旋转180度，避免与135号重叠
ROTATE_246_CENTER = (0, 0)

# ==============================================
# 组件创建函数（不变）
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
# 组装C3对称结构（修复三角形分布逻辑）
# ==============================================
def create_c3_symmetric_structure(hexagon_side_length, triangle_side_length):
    final_component = gf.Component("C3_Symmetric_Hexagon_Triangles")
    
    # 创建六边形
    hexagon = create_hexagon(hexagon_side_length, HEXAGON_LAYER)
    final_component << hexagon
    
    # 6个三角形的基础方向角度（C3对称，60度间隔，覆盖360度）
    base_angles = [30 + i * 60 for i in range(6)]  # 修正角度：30,90,150,210,270,330度（对称分布）
    
    # 循环放置6个三角形（i=0→1号，i=1→2号，...，i=5→6号）
    for i, base_angle in enumerate(base_angles):
        if i % 2 == 0:
            # 1、3、5号三角形（135组）
            base_angle_rad = (base_angle + OFFSET_135_ANGLE_OFFSET) * pi / 180
            dx = OFFSET_135_MAGNITUDE * cos(base_angle_rad)
            dy = OFFSET_135_MAGNITUDE * sin(base_angle_rad)
            
            triangle = create_small_triangle(triangle_side_length, TRIANGLE_LAYER_135)
            triangle_ref = final_component << triangle
            triangle_ref.move((dx, dy))  # 移动到对称位置
            if ROTATE_135:
                triangle_ref.rotate(ROTATE_135_ANGLE, center=ROTATE_135_CENTER)
        
        else:
            # 2、4、6号三角形（246组）
            base_angle_rad = (base_angle + OFFSET_246_ANGLE_OFFSET) * pi / 180
            dx = OFFSET_246_MAGNITUDE * cos(base_angle_rad)
            dy = OFFSET_246_MAGNITUDE * sin(base_angle_rad)
            
            triangle = create_small_triangle(triangle_side_length, TRIANGLE_LAYER_246)
            triangle_ref = final_component << triangle
            triangle_ref.move((dx, dy))  # 移动到对称位置
            if ROTATE_246:
                triangle_ref.rotate(ROTATE_246_ANGLE, center=ROTATE_246_CENTER)
    
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
    print("1、3、5号三角形参数：")
    print(f"  偏移幅度：{OFFSET_135_MAGNITUDE:.4f} um | 方向：{OFFSET_135_ANGLE_OFFSET}度")
    print(f"  旋转：{'是' if ROTATE_135 else '否'} | 角度：{ROTATE_135_ANGLE}度")
    print("-"*60)
    print("2、4、6号三角形参数：")
    print(f"  偏移幅度：{OFFSET_246_MAGNITUDE:.4f} um | 方向：{OFFSET_246_ANGLE_OFFSET}度")
    print(f"  旋转：{'是' if ROTATE_246 else '否'} | 角度：{ROTATE_246_ANGLE}度")
    print("="*60)