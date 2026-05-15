import gdsfactory as gf
import numpy as np
from numpy import cos, sin, sqrt, pi

# 1. 核心参数定义
HEXAGON_SIDE_LENGTH = 0.5  # 六边形边长 (um)
TRIANGLE_SIDE_LENGTH_RATIO = 1/2  # 小三角形边长相对六边形的比例
HEXAGON_LAYER = (1, 0)  # 六边形图层
TRIANGLE_LAYER_135 = (2, 0)  # 1、3、5号三角形的图层
TRIANGLE_LAYER_246 = (3, 0)  # 2、4、6号三角形的图层
OFFSET_MAGNITUDE = HEXAGON_SIDE_LENGTH / sqrt(3)  # 偏移量（六边形边长/√3）

# 2. 创建六边形组件（中心在原点）
def create_hexagon(side_length, layer):
    hexagon = gf.Component("Hexagon")
    vertices = [
        (side_length * cos(pi/2 + i * pi/3), side_length * sin(pi/2 + i * pi/3))
        for i in range(6)
    ]
    hexagon.add_polygon(vertices, layer=layer)
    return hexagon

# 3. 创建小三角形组件（尖端朝上，中心在原点）
def create_small_triangle(side_length, layer):
    triangle = gf.Component("Small_Triangle")
    height = (sqrt(3) / 2) * side_length
    vertices = [
        (0, 0),                      # 尖端（原点）
        (-side_length / 2, -height), # 左下角
        (side_length / 2, -height)   # 右下角
    ]
    triangle.add_polygon(vertices, layer=layer)
    return triangle

# 4. 组装C3对称结构（核心逻辑：区分1/3/5和2/4/6号三角形）
def create_c3_symmetric_structure(hexagon_side_length, triangle_side_length):
    final_component = gf.Component("C3_Symmetric_Hexagon_Triangles")
    
    # 创建基础组件模板
    hexagon = create_hexagon(hexagon_side_length, HEXAGON_LAYER)
    
    # 将六边形添加到最终组件
    final_component << hexagon
    
    # 6个三角形的基础方向角度
    base_angles = [150 + i * 60 for i in range(6)]
    
    # 循环放置6个三角形
    for i, base_angle in enumerate(base_angles):
        base_angle_rad = base_angle * pi / 180
        
        # 计算偏移
        dx = OFFSET_MAGNITUDE * cos(base_angle_rad)
        dy = OFFSET_MAGNITUDE * sin(base_angle_rad)
        
        # --------------------------
        # 根据三角形编号选择不同的图层
        # --------------------------
        if i % 2 == 0:
            # 1、3、5号三角形（i为偶数）
            triangle = create_small_triangle(triangle_side_length, TRIANGLE_LAYER_135)
            triangle_ref = final_component << triangle
            triangle_ref.move((dx, dy))
        else:
            # 2、4、6号三角形（i为奇数）
            triangle = create_small_triangle(triangle_side_length, TRIANGLE_LAYER_246)
            triangle_ref = final_component << triangle
            triangle_ref.move((dx, dy))
            triangle_ref.rotate(180, center=(0, 0))  # 绕原点旋转180°
    
    return final_component

# 5. 生成GDS并显示
if __name__ == "__main__":
    triangle_side_length = HEXAGON_SIDE_LENGTH * TRIANGLE_SIDE_LENGTH_RATIO
    
    c3_symmetric_structure = create_c3_symmetric_structure(
        hexagon_side_length=HEXAGON_SIDE_LENGTH,
        triangle_side_length=triangle_side_length
    )
    
    c3_symmetric_structure.show()
    c3_symmetric_structure.write_gds("c3_symmetric_hexagon_triangles_two_layers.gds")
    
    print("="*50)
    print("C3对称结构生成完成！")
    print(f"六边形边长：{HEXAGON_SIDE_LENGTH} um")
    print(f"小三角形边长：{triangle_side_length} um")
    print(f"三角形偏移量：{OFFSET_MAGNITUDE:.4f} um")
    print(f"1、3、5号三角形图层：{TRIANGLE_LAYER_135}")
    print(f"2、4、6号三角形图层：{TRIANGLE_LAYER_246}")
    print(f"GDS文件路径：c3_symmetric_hexagon_triangles_two_layers.gds")
    print("="*50)