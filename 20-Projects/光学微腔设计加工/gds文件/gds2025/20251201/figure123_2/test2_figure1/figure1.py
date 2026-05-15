import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import os
import signal
import sys
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

# 中断信号处理
def signal_handler(sig, frame):
    print('\n程序被用户中断')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# 中文配置
matplotlib.rcParams['font.sans-serif'] = ['Heiti TC', 'Songti SC', 'STHeiti', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# --------------------------
# 配置类（统一管理参数）
# --------------------------
@dataclass
class Config:
    """配置参数类"""
    a: float = 0.5  # 小六边形单元边长
    circle_radius: float = 5  # 整个图案半径
    offset_ratio: float = 0.1  # 额外偏移距离比例（相对于边长）
    
    @property
    def triangle_side(self) -> float:
        """正三角形边长（与小六边形边长相等）"""
        return self.a
    
    @property
    def offset_distance(self) -> float:
        """额外偏移距离"""
        return self.offset_ratio * self.a
    
    @property
    def sqrt3(self) -> float:
        """√3 常量（缓存）"""
        return np.sqrt(3)
    
    @property
    def triangle_base_configs(self) -> List[Tuple[float, np.ndarray]]:
        """六个正三角形的基础变换参数（旋转角度、初始平移向量）"""
        a = self.a
        sqrt3 = self.sqrt3
        return [
            (0,    np.array([0, a/sqrt3])),              # 1号：0°旋转，上顶点方向
            (60,   np.array([a/2, -a/(2*sqrt3)])),      # 2号：60°旋转，右下顶点方向
            (120,  np.array([-a/2, -a/(2*sqrt3)])),     # 3号：120°旋转，左下顶点方向
            (180,  np.array([0, -a/sqrt3])),            # 4号：180°旋转，下顶点方向
            (240,  np.array([-a/2, a/(2*sqrt3)])),      # 5号：240°旋转，左上顶点方向
            (300,  np.array([a/2, a/(2*sqrt3)]))        # 6号：300°旋转，右上顶点方向
        ]
    
    @property
    def extra_offset_configs(self) -> Dict[int, float]:
        """2、4、6号三角形的额外偏移配置（方向：60°、180°、300°）"""
        return {1: 60, 3: 180, 5: 300}  # 索引对应2、4、6号三角形
    
    @property
    def spacing_x(self) -> float:
        """水平间距（正六边形最优间距）"""
        return 1.5 * self.a
    
    @property
    def spacing_y(self) -> float:
        """垂直间距（紧密排列）"""
        return (self.sqrt3 / 2) * self.a

# 全局配置实例
config = Config()
center_1st_centroid: Optional[np.ndarray] = None  # 全局偏移原点：中心单元1号三角形的重心

# --------------------------
# 核心工具函数（优化性能，减少重复计算）
# --------------------------
# 旋转矩阵缓存（避免重复计算）
_rotation_matrix_cache: Dict[float, np.ndarray] = {}

def create_rotation_matrix(angle_deg: float) -> np.ndarray:
    """创建纯旋转矩阵（无缩放，确保正三角形旋转后不变形）"""
    if angle_deg not in _rotation_matrix_cache:
        angle_rad = np.radians(angle_deg)
        cosθ, sinθ = np.cos(angle_rad), np.sin(angle_rad)
        _rotation_matrix_cache[angle_deg] = np.array([[cosθ, -sinθ], [sinθ, cosθ]])
    return _rotation_matrix_cache[angle_deg]

def create_base_equilateral_triangle(side_length: float) -> np.ndarray:
    """创建标准正三角形（重心在原点，三边严格相等）"""
    sqrt3 = np.sqrt(3)
    height = (sqrt3 / 2) * side_length
    return np.array([
        [0, height / 3],                    # 上顶点
        [-side_length / 2, -height / 6],    # 左下顶点
        [side_length / 2, -height / 6]      # 右下顶点
    ])

def apply_transform(points: np.ndarray, 
                   rotate_matrix: Optional[np.ndarray] = None,
                   translate_vec: Optional[np.ndarray] = None) -> np.ndarray:
    """应用变换（先旋转后平移，仅线性变换，无变形）"""
    transformed = points.copy()
    if rotate_matrix is not None:
        transformed = transformed @ rotate_matrix.T
    if translate_vec is not None:
        transformed = transformed + translate_vec
    return transformed

def calculate_centroid(points: np.ndarray) -> np.ndarray:
    """计算三角形重心（用于偏移原点和标注）"""
    return np.mean(points, axis=0)

def verify_equilateral_triangle(points: np.ndarray, tolerance: float = 1e-6) -> bool:
    """验证是否为正三角形（变形检测）"""
    edges = np.array([
        np.linalg.norm(points[0] - points[1]),
        np.linalg.norm(points[1] - points[2]),
        np.linalg.norm(points[2] - points[0])
    ])
    is_equilateral = np.allclose(edges, edges[0], atol=tolerance)
    if not is_equilateral:
        print(f"三角形变形警告：三边长度{edges[0]:.6f}, {edges[1]:.6f}, {edges[2]:.6f}")
    return is_equilateral

# --------------------------
# 严格遵循「先阵列→再额外平移」流程
# --------------------------
def create_base_unit_cell() -> List[np.ndarray]:
    """创建基础单元（6个正三角形，无额外偏移）"""
    base_tri = create_base_equilateral_triangle(config.triangle_side)
    
    # 验证基础三角形
    assert verify_equilateral_triangle(base_tri), "基础三角形不是正三角形！"
    centroid = calculate_centroid(base_tri)
    edges = np.array([
        np.linalg.norm(base_tri[0] - base_tri[1]),
        np.linalg.norm(base_tri[1] - base_tri[2]),
        np.linalg.norm(base_tri[2] - base_tri[0])
    ])
    print(f"基础三角形验证：三边长度{edges[0]:.6f}, {edges[1]:.6f}, {edges[2]:.6f}，重心{centroid}")
    
    # 预计算旋转矩阵（避免重复计算）
    unit_triangles = []
    for idx, (rot_angle, trans_vec) in enumerate(config.triangle_base_configs):
        rot_matrix = create_rotation_matrix(rot_angle)
        tri = apply_transform(base_tri, rotate_matrix=rot_matrix, translate_vec=trans_vec)
        assert verify_equilateral_triangle(tri), f"基础单元三角形{idx+1}变形！"
        unit_triangles.append(tri)
    
    return unit_triangles

def generate_base_array() -> List[np.ndarray]:
    """第一步：生成基础阵列（无额外偏移，仅阵列操作）"""
    global center_1st_centroid
    base_unit = create_base_unit_cell()
    
    # 确定全局偏移原点：中心单元1号三角形的重心
    center_1st_centroid = calculate_centroid(base_unit[0])
    print(f"全局偏移原点（中心单元1号三角形重心）: ({center_1st_centroid[0]:.6f}, {center_1st_centroid[1]:.6f})")
    
    # 计算基础单元重心（使用所有三角形的第一个顶点）
    unit_centroid = calculate_centroid(np.vstack([tri[0] for tri in base_unit]))
    
    # 计算阵列范围（确保阵列后+额外偏移仍在半径内）
    max_point_dist = max(np.linalg.norm(point) for tri in base_unit for point in tri)
    max_unit_offset = config.circle_radius - config.offset_distance - max_point_dist
    min_spacing = min(config.spacing_x, config.spacing_y)
    grid_size = int(np.ceil(max_unit_offset / min_spacing)) + 2
    
    # 生成所有单元位置（向量化优化）
    all_unit_centers = []
    for i in range(-grid_size, grid_size + 1):
        for j in range(-grid_size, grid_size + 1):
            unit_x = i * config.spacing_x + (j % 2) * (config.spacing_x / 2)
            unit_y = j * config.spacing_y
            unit_center = np.array([unit_x, unit_y])
            
            # 过滤：单元重心到原点的距离≤最大允许偏移
            if np.linalg.norm(unit_center - unit_centroid) <= max_unit_offset:
                all_unit_centers.append(unit_center)
    
    # 生成基础阵列（批量处理，减少循环开销）
    base_array_triangles = []
    for unit_center in all_unit_centers:
        unit_trans_vec = unit_center - unit_centroid
        for tri in base_unit:
            array_tri = apply_transform(tri, translate_vec=unit_trans_vec)
            base_array_triangles.append(array_tri)
    
    print(f"基础阵列生成完成：{len(all_unit_centers)}个单元，{len(base_array_triangles)}个正三角形")
    return base_array_triangles

def apply_extra_offset_to_array(base_array_triangles: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """第二步：对基础阵列中的2、4、6号三角形添加额外平移"""
    # 预计算偏移向量（避免重复计算）
    offset_vectors = {}
    for tri_idx, angle_deg in config.extra_offset_configs.items():
        offset_rad = np.radians(angle_deg)
        offset_vectors[tri_idx] = config.offset_distance * np.array([
            np.cos(offset_rad), np.sin(offset_rad)
        ])
    
    final_triangles = []
    all_displacements = []
    
    for global_idx, tri in enumerate(base_array_triangles):
        tri_type_idx = global_idx % 6  # 0-5对应1-6号三角形
        
        # 应用额外偏移（如果适用）
        if tri_type_idx in offset_vectors:
            offset_tri = apply_transform(tri, translate_vec=offset_vectors[tri_type_idx])
            final_triangles.append(offset_tri)
        else:
            final_triangles.append(tri)
        
        # 计算总位移（最终重心相对于坐标原点）
        all_displacements.append(calculate_centroid(final_triangles[-1]))
    
    # 过滤：确保所有三角形完全在半径内（向量化优化）
    filtered_triangles = []
    filtered_displacements = []
    for tri, disp in zip(final_triangles, all_displacements):
        max_dist = max(np.linalg.norm(point) for point in tri)
        if max_dist <= config.circle_radius:
            filtered_triangles.append(tri)
            filtered_displacements.append(disp)
    
    print(f"额外偏移应用完成：过滤后剩余{len(filtered_triangles)}个正三角形")
    return filtered_triangles, filtered_displacements

# --------------------------
# 可视化与标注（要求3：标注所有三角形位移）
# --------------------------
# 三角形类型配置（预定义，避免重复创建）
TRIANGLE_INFO = {
    0: ('blue', '1号（无额外偏移）'),
    1: ('red', '2号（额外偏移60°）'),
    2: ('blue', '3号（无额外偏移）'),
    3: ('red', '4号（额外偏移180°）'),
    4: ('blue', '5号（无额外偏移）'),
    5: ('red', '6号（额外偏移300°）')
}

def _get_annotation_style(centroid_dist: float) -> Tuple[str, float, dict]:
    """根据距离返回标注样式"""
    if centroid_dist < 1.2:  # 核心区
        return 'detailed', 0.08, {'fontsize': 8, 'color': 'darkred', 'weight': 'bold',
                                  'bbox': dict(facecolor='white', alpha=0.9, pad=2)}
    elif centroid_dist < 3.0:  # 中间区
        return 'simple', 0.06, {'fontsize': 7, 'color': 'darkblue', 'weight': 'normal',
                                'bbox': dict(facecolor='white', alpha=0.8, pad=1)}
    else:  # 外围区
        return 'minimal', 0.05, {'fontsize': 6, 'color': 'black', 'weight': 'light'}

def visualize_with_full_annotations(final_triangles: List[np.ndarray], 
                                   all_displacements: List[np.ndarray]) -> str:
    """生成PNG图，标注所有三角形的位移（大小+方向）"""
    fig, ax = plt.subplots(figsize=(18, 18))
    
    # 绘制所有正三角形并标注位移
    for global_idx, (tri, disp) in enumerate(zip(final_triangles, all_displacements)):
        tri_type_idx = global_idx % 6
        color, label = TRIANGLE_INFO[tri_type_idx]
        
        # 绘制正三角形
        ax.fill(tri[:, 0], tri[:, 1], color=color, alpha=0.7,
                edgecolor='black', linewidth=1.0, label=label if global_idx < 6 else None)
        
        # 计算三角形重心和位移信息
        centroid = calculate_centroid(tri)
        centroid_dist = np.linalg.norm(centroid)
        disp_mag = np.linalg.norm(disp)
        disp_angle = np.degrees(np.arctan2(disp[1], disp[0])) % 360
        
        # 分区域标注
        style, offset, text_kwargs = _get_annotation_style(centroid_dist)
        x_offset, y_offset = offset, offset
        
        if style == 'detailed':
            annot_text = f"类型：{tri_type_idx+1}号\n位移大小：{disp_mag:.4f}\n方向：{disp_angle:.1f}°"
            ax.text(centroid[0] + x_offset, centroid[1] + y_offset, annot_text, **text_kwargs)
            # 绘制位移向量
            ax.arrow(0, 0, centroid[0], centroid[1], head_width=0.06, head_length=0.08,
                     fc='darkgreen', ec='darkgreen', alpha=0.7, linewidth=0.8)
        elif style == 'simple':
            annot_text = f"{disp_mag:.3f}\n{disp_angle:.0f}°"
            ax.text(centroid[0] + x_offset, centroid[1] + y_offset, annot_text, **text_kwargs)
        else:  # minimal
            ax.text(centroid[0] + x_offset, centroid[1] + y_offset, f"{disp_mag:.2f}", **text_kwargs)
    
    # 绘制关键参考元素
    boundary_circle = plt.Circle((0, 0), config.circle_radius, fill=False,
                                color='red', linestyle='--', linewidth=2.5,
                                label=f'图案边界（半径={config.circle_radius}）')
    ax.add_patch(boundary_circle)
    
    if center_1st_centroid is not None:
        ax.scatter(center_1st_centroid[0], center_1st_centroid[1],
                   color='orange', s=300, marker='*', zorder=10,
                   label=f'额外偏移原点\n({center_1st_centroid[0]:.6f}, {center_1st_centroid[1]:.6f})')
    
    ax.scatter(0, 0, color='black', s=150, marker='+', zorder=10, label='坐标原点(0,0)')
    
    # 图形样式配置
    ax.set_aspect('equal')
    limit = config.circle_radius * 1.1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_title('正三角形阵列（先阵列→再额外平移）- 全位移标注', fontsize=22, pad=25)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.6)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95, ncol=2)
    
    # 保存高分辨率PNG
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    png_path = os.path.join(os.getcwd(), f"equilateral_triangle_array_final_{timestamp}.png")
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"PNG文件已保存：{png_path}")
    return png_path

# --------------------------
# 主程序执行（严格流程：先阵列→再额外平移）
# --------------------------
def main():
    """主程序入口"""
    print("=== 正三角形阵列生成程序（严格遵循：先阵列→再额外平移）===")
    print("参数配置：")
    print(f"- 小六边形边长：{config.a}")
    print(f"- 正三角形边长：{config.triangle_side}")
    print(f"- 图案半径：{config.circle_radius}")
    print(f"- 额外偏移距离：{config.offset_distance}（小六边形边长的{config.offset_ratio}倍）")
    print(f"- 额外偏移规则：2号(60°)、4号(180°)、6号(300°)，原点=中心单元1号三角形重心")
    
    # 第一步：生成基础阵列（无额外偏移）
    base_array = generate_base_array()
    
    # 第二步：对基础阵列中的2、4、6号三角形添加额外平移
    final_triangles, all_displacements = apply_extra_offset_to_array(base_array)
    
    # 第三步：生成带全位移标注的PNG图
    visualize_with_full_annotations(final_triangles, all_displacements)
    
    print("\n=== 程序执行完成 ===")
    print("关键验证结果：所有三角形均为正三角形，无变形！")
    print("输出文件：高分辨率PNG（含所有三角形位移标注）")

if __name__ == "__main__":
    main()