import gdsfactory as gf
import numpy as np
from numpy import cos, sin, sqrt, pi
# 1. 定义基本参数和图层
hexagon_side_length = 0.5  # 六边形的边长 (um)
a=hexagon_side_length
triangle_side_length =hexagon_side_length/5
b=triangle_side_length 
HEXAGON_LAYER = (1, 0)    # 六边形所在的图层 (图层1, 数据类型0)
TRIANGLE_LAYER = (2, 0)   # 三角形所在的图层 (图层2, 数据类型0)

# 2. 创建一个六边形组件 (Component)
def create_hexagon(a, layer):
    """
    创建一个正六边形组件。
    六边形的中心在原点 (0, 0)。
    """
    hexagon = gf.Component("Hexagon")
    
    vertices = []
    for i in range(6):
        angle = pi/2 + i * pi/3  # 从 90 度开始，第一个顶点在正上方
        x = a * cos(angle)
        y = b * sin(angle)
        vertices.append((x, y))
    
    # 在绘制时指定图层
    hexagon.add_polygon(vertices, layer=layer)
    
    return hexagon

# 3. 创建一个三角形组件 (Component)
def create_triangle(b, layer):
    """
    创建一个正三角形组件。
    三角形的中心的坐标是(a/sqrt(3)*cos(pi/3), a/sqrt(3)*sin(pi/3))
    """
    triangle = gf.Component("Triangle")
    vertex=(a/sqrt(3)*cos(pi/3), a/sqrt(3)*sin(pi/3))
    vertex_a = (a/sqrt(3)*cos(pi/3)+b/sqrt(3)*cos(0), a/sqrt(3)*sin(pi/3)+b/sqrt(3)*sin(0))
    vertex_b = (a/sqrt(3)*cos(pi/3)+b/sqrt(3)*cos(2*pi/3), a/sqrt(3)*sin(pi/3)+b/sqrt(3)*sin(2*pi/3))
    vertex_c = (a/sqrt(3)*cos(pi/3)+b/sqrt(3)*cos(4*pi/3), a/sqrt(3)*sin(pi/3)+b/sqrt(3)*sin(4*pi/3))
    
    
    # 在绘制时指定图层                                      
    triangle.add_polygon(vertices, layer=layer)
    
    triangle.add_port(name="tip", center=vertex_a, orientation=0, width=0.5)
    
    return triangle

# 4. 组装最终的组件
def create_hexagon_with_triangles(hexagon_side_length, hexagon_layer, triangle_layer):
    """
    创建一个最终的组件，包含一个六边形和内部的六个三角形，分别在不同图层。
    """
    final_component = gf.Component("Hexagon_with_Triangles")
    
    # 创建六边形和三角形的“模板”，并传入各自的图层参数
    hexagon = create_hexagon(hexagon_side_length, hexagon_layer)
    triangle = create_triangle(hexagon_side_length, triangle_layer)
    
    # 将六边形添加到最终组件中
    final_component << hexagon
    
    # 将六个三角形添加到最终组件中
    for i in range(6):
        rotation_angle = i * 60
        
        triangle_ref = final_component << triangle
        triangle_ref.move(origin=(0, 0))
        triangle_ref.rotate(rotation_angle)

    return final_component

# 5. 生成 GDS 文件并显示
if __name__ == "__main__":
    # 创建最终的组件，传入两个不同的图层
    hex_with_tris = create_hexagon_with_triangles(
        hexagon_side_length,
        HEXAGON_LAYER,
        TRIANGLE_LAYER
    )
    
    # 显示组件
    hex_with_tris.show()
    
    # 将组件保存为 GDS 文件
    hex_with_tris.write_gds("hexagon_with_triangles_two_layers.gds")
    
    print("GDS 文件已保存为 'hexagon_with_triangles_two_layers.gds'")