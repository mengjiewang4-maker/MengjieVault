import gdsfactory as gf
import numpy as np
import os
from datetime import datetime

# --------------------------
# 基础参数配置（可按需调整）
# --------------------------
# 六边形参数
HEXAGON_SIDE = 0.2  # 六边形边长（μm，200nm=0.2μm）
HEXAGON_LAYER = 1   # 六边形图层

# 三角形基础参数
TRIANGLE_LAYER = 2        # 三角形图层
TRIANGLE_SCALE = 1/3      # 缩小比例（保持等边）
TRIANGLE_ROT_ANGLE = 30   # 旋转角度（度，逆时针为正）
TRIANGLE_SERIAL = 1       # 文件序号

# 自定义旋转中心（相对原点的绝对坐标，单位：μm）
# 例：(0, 0)→原点旋转；(0.05, 0)→x轴正方向50nm处；(0, 0.03)→y轴正方向30nm处
ROTATION_CENTER = (0.05, 0.03)  # 旋转中心 (x, y)

# 自定义位移中心（三角形最终整体平移到的目标中心，单位：μm）
# 例：(0, 0)→保持原重心位置；(0.1, 0)→整体右移100nm；(-0.08, 0.06)→左移80nm+上移60nm
TRANSLATION_CENTER = (0, 0)  # 最终位移中心（默认与原大三角形重心重合）

# --------------------------
# 核心工具函数：旋转+平移矩阵
# --------------------------
def rotate_around_point(point, rotate_center, angle_deg):
    """
    围绕任意旋转中心旋转单个点（先平移到旋转中心，再旋转，最后平移回原坐标系）
    :param point: 原始坐标 (x, y)
    :param rotate_center: 旋转中心 (cx, cy)（绝对坐标）
    :param angle_deg: 旋转角度（度，逆时针为正）
    :return: 旋转后的坐标 (x', y')
    """
    # 步骤1：平移到旋转中心坐标系（减去旋转中心坐标）
    x_rel = point[0] - rotate_center[0]
    y_rel = point[1] - rotate_center[1]
    
    # 步骤2：应用旋转矩阵（围绕原点旋转）
    angle_rad = np.radians(angle_deg)
    cosθ = np.cos(angle_rad)
    sinθ = np.sin(angle_rad)
    x_rot = x_rel * cosθ - y_rel * sinθ
    y_rot = x_rel * sinθ + y_rel * cosθ
    
    # 步骤3：平移回原坐标系（加上旋转中心坐标）
    x_final = x_rot + rotate_center[0]
    y_final = y_rot + rotate_center[1]
    return (x_final, y_final)

def translate_point(point, translation):
    """
    平移单个点到目标位置
    :param point: 原始坐标 (x, y)
    :param translation: 位移向量 (dx, dy)（从原位置平移到目标位置的增量）
    :return: 平移后的坐标 (x+dx, y+dy)
    """
    return (point[0] + translation[0], point[1] + translation[1])

# --------------------------
# 文件名生成函数（包含关键参数）
# --------------------------
def get_gds_filename(serial_num):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 文件名包含旋转中心、位移中心、旋转角度，便于区分
    rot_center_str = f"rotC({ROTATION_CENTER[0]:.3f},{ROTATION_CENTER[1]:.3f})"
    trans_center_str = f"transC({TRANSLATION_CENTER[0]:.3f},{TRANSLATION_CENTER[1]:.3f})"
    filename = f"hexagon_triangles_{rot_center_str}_rot{TRIANGLE_ROT_ANGLE}deg_{trans_center_str}_{current_time}_serial{serial_num}.gds"
    code_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(code_dir, filename)

# --------------------------
# 图形生成函数（支持旋转中心+位移中心）
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

def create_triangle_points(
    hex_side, scale_factor, triangle_index, 
    rotate_center, rotate_angle_deg, translation_center
):
    """
    生成等边三角形顶点坐标（支持自定义旋转中心、位移中心）
    :param hex_side: 原六边形边长
    :param scale_factor: 缩小比例
    :param triangle_index: 三角形索引（0-5）
    :param rotate_center: 旋转中心 (cx, cy)
    :param rotate_angle_deg: 旋转角度（度）
    :param translation_center: 最终位移中心 (tx, ty)
    :return: 旋转+平移后的等边三角形顶点坐标
    """
    # 1. 生成原大三角形对应的小等边三角形（未旋转、未平移，重心在原大三角形重心）
    base_angle = triangle_index * np.pi / 3  # 原大三角形起始角度
    r = (hex_side * scale_factor) / np.sqrt(3)  # 小等边三角形外接圆半径
    original_angles = [base_angle, base_angle + np.pi/3, base_angle + np.pi/6]
    original_points = [(r * np.cos(ang), r * np.sin(ang)) for ang in original_angles]
    
    # 2. 围绕自定义旋转中心旋转所有顶点
    rotated_points = [
        rotate_around_point(point, rotate_center, rotate_angle_deg) 
        for point in original_points
    ]
    
    # 3. 计算位移向量（从原重心平移到目标位移中心）
    # 原重心：旋转后的三角形自身重心（等边三角形重心=外接圆圆心，即原大三角形重心）
    original_triangle_center = (
        np.mean([p[0] for p in rotated_points]),
        np.mean([p[1] for p in rotated_points])
    )
    translation = (
        translation_center[0] - original_triangle_center[0],
        translation_center[1] - original_triangle_center[1]
    )
    
    # 4. 应用平移，得到最终坐标
    final_points = [translate_point(point, translation) for point in rotated_points]
    
    return final_points

# --------------------------
# 主程序
# --------------------------
if __name__ == "__main__":
    # 创建GDS组件
    c = gf.Component("hexagon_with_custom_rot_trans_triangles")
    
    # 1. 绘制图层1的正六边形
    hexagon_points = create_hexagon_points(HEXAGON_SIDE)
    c.add_polygon(hexagon_points, layer=HEXAGON_LAYER)
    
    # 2. 绘制图层2的6个等边三角形（自定义旋转中心+位移中心）
    for i in range(6):
        triangle_points = create_triangle_points(
            hex_side=HEXAGON_SIDE,
            scale_factor=TRIANGLE_SCALE,
            triangle_index=i,
            rotate_center=ROTATION_CENTER,
            rotate_angle_deg=TRIANGLE_ROT_ANGLE,
            translation_center=TRANSLATION_CENTER
        )
        c.add_polygon(triangle_points, layer=TRIANGLE_LAYER)
    
    # 3. 保存GDS文件
    gds_path = get_gds_filename(TRIANGLE_SERIAL)
    c.write_gds(gds_path)
    
    # 输出关键信息
    print("="*80)
    print("GDS文件生成完成！")
    print(f"文件路径：{gds_path}")
    print(f"核心参数：")
    print(f"  - 六边形（图层{HEXAGON_LAYER}）：边长{int(HEXAGON_SIDE*1000)}nm，重心(0,0)")
    print(f"  - 三角形（图层{TRIANGLE_LAYER}）：6个严格等边三角形")
    print(f"    - 三角形边长：{int(HEXAGON_SIDE*1000*TRIANGLE_SCALE)}nm（原边长×{TRIANGLE_SCALE}）")
    print(f"    - 旋转中心：{ROTATION_CENTER} μm（绝对坐标）")
    print(f"    - 旋转角度：{TRIANGLE_ROT_ANGLE}°（逆时针为正）")
    print(f"    - 最终位移中心：{TRANSLATION_CENTER} μm（绝对坐标）")
    print(f"  - 文件序号：{TRIANGLE_SERIAL}")
    print("="*80)