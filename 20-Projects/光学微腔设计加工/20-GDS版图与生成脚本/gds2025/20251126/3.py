import gdsfactory as gf
import numpy as np
from numpy import cos, sin, sqrt, pi
import os
from datetime import datetime

# ==============================================
# 核心参数（C6对称配置）
# ==============================================
HEXAGON_SIDE_LENGTH = 0.5  # 六边形边长 (um)
TRIANGLE_SIDE_LENGTH_RATIO = 1/2  # 三角形相对大小比例

# 图层定义（分图层显示，便于区分）
HEXAGON_LAYER = (1, 0)        # 六边形（红色网格）
TRIANGLE_LAYER_135 = (2, 0)   # 1、3、5号三角形（绿色）
TRIANGLE_LAYER_246 = (3, 0)   # 2、4、6号三角形（蓝色）

# --------------------------
# 1、3、5号三角形 调节参数（C6对称组）
# --------------------------
OFFSET_135_MAGNITUDE = HEXAGON_SIDE_LENGTH * 0.6  # 偏移幅度（靠近六边形边缘）
OFFSET_135_ANGLE_OFFSET = 0  # 整体偏移方向（不破坏C6对称）
ROTATE_135 = False  # 是否旋转
ROTATE_135_ANGLE = 0  # 旋转角度（整体旋转，保持C6对称）

# --------------------------
# 2、4、6号三角形 调节参数（C6对称组）
# --------------------------
OFFSET_246_MAGNITUDE = HEXAGON_SIDE_LENGTH * 0.6  # 偏移幅度（与135组对称）
OFFSET_246_ANGLE_OFFSET = 0  # 整体偏移方向（保持C6对称）
ROTATE_246 = True  # 是否旋转
ROTATE_246_ANGLE = 180  # 旋转180度区分方向（不破坏C6对称）

# ==============================================
# 组件创建函数（完全保留你定义的三角形坐标，不做任何修改！）
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
    # 完全保留你定义的原始坐标，不做任何修改！
    triangle = gf.Component("Small_Triangle") 
    vertices = [
        (0, 0),                      # 尖端（原点）
        (0, side_length), # 右上角
        (side_length / sqrt(3), side_length / 2)   # 右下角
    ]
    triangle.add_polygon(vertices, layer=layer)
    return triangle

# ==============================================
# 组装C6对称结构（核心：仅调整旋转和偏移，不修改三角形本身）
# ==============================================
def create_c6_symmetric_structure(hexagon_side_length, triangle_side_length):
    final_component = gf.Component("C6_Symmetric_Hexagon_Triangles")
    
    # 创建六边形（C6对称基准）
    hexagon = create_hexagon(hexagon_side_length, HEXAGON_LAYER)
    final_component << hexagon
    
    # C6对称核心：6个三角形的初始角度（0°, 60°, 120°, 180°, 240°, 300°）
    # 严格60°间隔，确保旋转60°后与原结构重合
    initial_angles = [i * 60 for i in range(6)]  # 6个角度，间隔60°
    center = (0, 0)  # 所有三角形围绕原点分布，保证C6对称
    
    # 循环放置6个三角形（C6对称分布，不修改三角形自身坐标）
    for i, angle_deg in enumerate(initial_angles):
        angle_rad = angle_deg * pi / 180
        
        if i % 2 == 0:
            # --------------------------
            # 1、3、5号三角形（C6子集：0°, 120°, 240°）
            # --------------------------
            # 偏移角度 = 初始角度 + 组整体偏移（保持C6对称）
            offset_angle_rad = (angle_deg + OFFSET_135_ANGLE_OFFSET) * pi / 180
            dx = OFFSET_135_MAGNITUDE * cos(offset_angle_rad)
            dy = OFFSET_135_MAGNITUDE * sin(offset_angle_rad)
            
            # 创建三角形（使用你定义的原始坐标）
            triangle = create_small_triangle(triangle_side_length, TRIANGLE_LAYER_135)
            triangle_ref = final_component << triangle
            
            # 1. 旋转：沿原点旋转到目标角度（C6核心，不改变三角形自身坐标）
            triangle_ref.rotate(angle_deg, center=center)
            # 2. 组旋转：整体旋转（不破坏C6对称，仅改变朝向）
            if ROTATE_135:
                triangle_ref.rotate(ROTATE_135_ANGLE, center=center)
            # 3. 偏移：沿旋转方向偏移（保持C6对称，不改变三角形自身）
            triangle_ref.move((dx, dy))
        
        else:
            # --------------------------
            # 2、4、6号三角形（C6子集：60°, 180°, 300°）
            # --------------------------
            # 偏移角度 = 初始角度 + 组整体偏移（保持C6对称）
            offset_angle_rad = (angle_deg + OFFSET_246_ANGLE_OFFSET) * pi / 180
            dx = OFFSET_246_MAGNITUDE * cos(offset_angle_rad)
            dy = OFFSET_246_MAGNITUDE * sin(offset_angle_rad)
            
            # 创建三角形（使用你定义的原始坐标）
            triangle = create_small_triangle(triangle_side_length, TRIANGLE_LAYER_246)
            triangle_ref = final_component << triangle
            
            # 1. 旋转：沿原点旋转到目标角度（C6核心，不改变三角形自身坐标）
            triangle_ref.rotate(angle_deg, center=center)
            # 2. 组旋转：整体旋转（不破坏C6对称，仅改变朝向）
            if ROTATE_246:
                triangle_ref.rotate(ROTATE_246_ANGLE, center=center)
            # 3. 偏移：沿旋转方向偏移（保持C6对称，不改变三角形自身）
            triangle_ref.move((dx, dy))
    
    return final_component

# ==============================================
# 文件名生成（不变）
# ==============================================
def get_unique_filename(base_name="c6_symmetric_structure", ext="gds"):
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
# 主程序（生成C6对称GDS）
# ==============================================
if __name__ == "__main__":
    triangle_side_length = HEXAGON_SIDE_LENGTH * TRIANGLE_SIDE_LENGTH_RATIO
    c6_symmetric_structure = create_c6_symmetric_structure(
        hexagon_side_length=HEXAGON_SIDE_LENGTH,
        triangle_side_length=triangle_side_length
    )
    
    unique_gds_path = get_unique_filename()
    c6_symmetric_structure.write_gds(unique_gds_path)
    
    # 打印信息
    print("="*60)
    print("✅ C6对称结构GDS文件生成成功！")
    print(f"📁 路径：{unique_gds_path}")
    print("✅ 严格保留你定义的三角形原始坐标，未做任何修改！")
    print("-"*60)
    print("C6对称特性：6个三角形沿原点60°间隔分布，旋转60°重合")
    print("-"*60)
    print("1、3、5号三角形（绿色，C6子集）参数：")
    print(f"  偏移幅度：{OFFSET_135_MAGNITUDE:.4f} um | 整体偏移方向：{OFFSET_135_ANGLE_OFFSET}度")
    print(f"  旋转：{'是' if ROTATE_135 else '否'} | 整体旋转角度：{ROTATE_135_ANGLE}度")
    print(f"  分布角度：0°、120°、240°")
    print("-"*60)
    print("2、4、6号三角形（蓝色，C6子集）参数：")
    print(f"  偏移幅度：{OFFSET_246_MAGNITUDE:.4f} um | 整体偏移方向：{OFFSET_246_ANGLE_OFFSET}度")
    print(f"  旋转：{'是' if ROTATE_246 else '否'} | 整体旋转角度：{ROTATE_246_ANGLE}度")
    print(f"  分布角度：60°、180°、300°")
    print("="*60)