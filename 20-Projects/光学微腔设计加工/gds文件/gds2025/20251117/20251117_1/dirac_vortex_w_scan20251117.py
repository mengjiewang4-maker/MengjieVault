"""
make_honeycomb_dirac.py

生成三份 GDS：honeycomb_case_A.gds, honeycomb_case_B.gds, honeycomb_case_C.gds
每份对应一个代表性的 winding number:
  A -> w = 1
  B -> w = 2
  C -> w = 3

要求: 已安装 gdsfactory (7.x) 和 numpy
在你的 gdsfactory 环境中运行： python make_honeycomb_dirac.py
"""

import math
import numpy as np
import gdsfactory as gf

# ---------------------
# 参数（可修改）
# ---------------------
SIDE = 10.0            # 单个正六边形边长（从中心到顶点的距离）
SPACING = 2 * SIDE     # 六边形格子间距（中心到中心）
RINGS = 2              # 环数（0 = 只有中心；1 = 中心 + 第一圈 6 个；2 = 中心 + 2 圈）
TRI_SCALE = 0.45       # 三角形相对于六边形尺寸的缩放
LAYER_HEX = (1, 0)
LAYER_TRI_RED = (2, 0)
LAYER_TRI_GREEN = (3, 0)
LAYER_TRI_BLUE = (4, 0)
LAYER_TEXT = (5, 0)
LAYER_LINES = (6, 0)

# 代表性 w 值（你可以改成图注里的 -2,+1,+4 等）
CASES = {
    "A": 1,
    "B": 2,
    "C": 3,
}


# ---------------------
# 几何工具
# ---------------------
def regular_hex_vertices(side: float):
    """返回正六边形的 6 个顶点（以中心为原点）"""
    verts = []
    for i in range(6):
        ang = math.radians(60 * i + 30)  # +30 让一条边水平（更美观）
        x = side * math.cos(ang)
        y = side * math.sin(ang)
        verts.append((x, y))
    return verts


def rotate_point(pt, theta):
    x, y = pt
    ct = math.cos(theta)
    st = math.sin(theta)
    return (ct * x - st * y, st * x + ct * y)


def translate_point(pt, dx, dy):
    return (pt[0] + dx, pt[1] + dy)


def polygon_rotate_translate(points, theta, dx, dy):
    return [translate_point(rotate_point(p, theta), dx, dy) for p in points]


# ---------------------
# 生成单个六边形单元（包含 3 个彩色三角）
# 内部三角原始方向（相对于六边形中心）设为：
#   triangle 0: 指向 0deg (red)
#   triangle 1: 指向 120deg (green)
#   triangle 2: 指向 240deg (blue)
# ---------------------
def create_hexagon_component(side_length=SIDE, tri_scale=TRI_SCALE):
    c = gf.Component("hex_base")

    # 六边形外框（中心在 0,0）
    verts = regular_hex_vertices(side_length)
    hex_poly = gf.Polygon(points=verts, layer=LAYER_HEX)
    c.add(hex_poly)

    # 定义三个小三角（相对于中心）
    # 我们构造等边小三角，中心距离为 side_length*0.5，朝三个主方向
    tri_distance = side_length * 0.45  # 三角心距
    tri_size = side_length * tri_scale

    tri_dirs = [0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0]
    tri_points = []
    for d in tri_dirs:
        # 三角为等边，用中心点 + 三个角点构造
        cx = tri_distance * math.cos(d)
        cy = tri_distance * math.sin(d)
        # 基础等边三角朝 +x（0度）方向，顶点在正方向
        a = tri_size
        base = [(0.0, a * 2.0 / 3.0), (-a / 2.0, -a / 3.0), (a / 2.0, -a / 3.0)]
        # 将 base 旋转到方向 d 并平移到 (cx,cy)
        pts = [translate_point(rotate_point(p, d), cx, cy) for p in base]
        tri_points.append(pts)

    # 添加三角占位（不旋转）
    c.add(gf.Polygon(points=tri_points[0], layer=LAYER_TRI_RED))
    c.add(gf.Polygon(points=tri_points[1], layer=LAYER_TRI_GREEN))
    c.add(gf.Polygon(points=tri_points[2], layer=LAYER_TRI_BLUE))

    return c, tri_points, verts


# ---------------------
# 生成蜂窝中心坐标（六边形格子）
# 使用 axial coordinates -> 转换到笛卡尔
# ---------------------
def hex_grid_centers(rings: int, spacing: float):
    centers = []
    # 六边形格子用 axial coords (q,r)
    for q in range(-rings, rings + 1):
        for r in range(-rings, rings + 1):
            s = -q - r
            if abs(s) <= rings:
                # 转换到 x,y（pointy-top hex）
                x = spacing * (3.0/2.0 * q)
                y = spacing * (math.sqrt(3)/2.0 * q + math.sqrt(3) * r)
                centers.append((x, y))
    return centers


# ---------------------
# 主生成函数：为一个 case 生成 GDS
# ---------------------
def make_case(case_name: str, w_value: float, outname: str = None):
    if outname is None:
        outname = f"honeycomb_case_{case_name}.gds"

    base_comp, tri_points, hex_verts = create_hexagon_component()
    c = gf.Component(f"honeycomb_{case_name}")

    centers = hex_grid_centers(RINGS, SPACING)

    # 把每个六边形放入，并按 phi 旋转三角
    for (cx, cy) in centers:
        # 计算该单元相对于中心的极角 phi （取 -pi..pi）
        phi = math.atan2(cy, cx)  # radians
        # 旋转角度 theta = w * phi
        theta = w_value * phi

        # 添加六边形外框副本（直接用 base polygon）
        # 使用 add_polygon + transform: 先旋转六边形外框（这里外框不随 theta 旋转，保留原向）
        hex_pts_world = [translate_point(p, cx, cy) for p in hex_verts]
        c.add(gf.Polygon(points=hex_pts_world, layer=LAYER_HEX))

        # 将三个三角按 theta 旋转并放置（不同 layer 区分）
        tri_r = polygon_rotate_translate(tri_points[0], theta, cx, cy)
        tri_g = polygon_rotate_translate(tri_points[1], theta, cx, cy)
        tri_b = polygon_rotate_translate(tri_points[2], theta, cx, cy)

        c.add(gf.Polygon(points=tri_r, layer=LAYER_TRI_RED))
        c.add(gf.Polygon(points=tri_g, layer=LAYER_TRI_GREEN))
        c.add(gf.Polygon(points=tri_b, layer=LAYER_TRI_BLUE))

    # 添加分界线（画三条方向线：水平、斜+60、斜-60）
    # 我们以中心长度 L_line 为参考
    L_line = SPACING * (RINGS + 1.5)
    # 水平（虚线样式用多个小段实现）
    dash = 6.0
    x0 = -L_line
    while x0 < L_line:
        c.add(gf.Polygon(points=[(x0, 0), (x0 + dash, 0)], layer=LAYER_LINES))
        x0 += dash * 2

    # 斜线 +60 deg
    angs = [math.radians(60), math.radians(-60)]
    for ang in angs:
        # param t 控制线沿方向切片以虚线形式绘制
        ux = math.cos(ang)
        uy = math.sin(ang)
        t = -L_line
        while t < L_line:
            p1 = (t * ux, t * uy)
            p2 = ((t + dash) * ux, (t + dash) * uy)
            c.add(gf.Polygon(points=[p1, p2], layer=LAYER_LINES))
            t += dash * 2

    # 添加大标题 A/B/C
    c.add_label(text=f"({case_name}) w = {w_value}", position=(-SPACING * (RINGS + 1), SPACING * (RINGS + 1)), layer=LAYER_TEXT)

    # 写出 GDS
    c.write_gds(outname)
    print(f"✅ 写出 {outname} （case {case_name}, w={w_value}）")

    return c


# ---------------------
# 执行：为每个 case 生成 GDS
# ---------------------
if __name__ == "__main__":
    for name, w in CASES.items():
        make_case(name, w_value=w)
    print("全部完成。请用 KLayout 打开生成的 GDS 查看。")
