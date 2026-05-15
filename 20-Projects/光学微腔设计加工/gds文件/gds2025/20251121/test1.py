import gdsfactory as gf
import numpy as np
from gdsfactory.typings import LayerSpec

@gf.cell
def topological_vortex_laser(
    a: float = 0.5,          # 晶格常数 (um)
    m0: float = 0.05,        # 拓扑位移量 (um)
    ltr: float = 0.166,      # 三角形尺寸参数 (um)
    n_rings: int = 15,       # 腔体半径（晶格层数）
    w0: float = 3.0,         # 涡旋核心半径参数
    charge: int = 1,         # 拓扑荷数
    layer: LayerSpec = (1, 0)
) -> gf.Component:
    
    c = gf.Component("Dirac_Vortex_Cavity")

    # --- 1. 定义基础三角形组件 (Master Component) ---
    # 将 numpy array 转换为 list of tuples，避免 Pydantic 哈希错误
    angles = np.array([np.pi/2, 7*np.pi/6, -np.pi/6])
    # 注意这里转成了 .tolist() 或者 list comprehension 生成 tuple
    triangle_pts = [(ltr * np.cos(ang), ltr * np.sin(ang)) for ang in angles]
    
    # 创建一个独立的三角形组件，之后我们在循环中只引用它
    # 这样可以避免在循环中重复创建新的 Component，极大提高速度并避免报错
    triangle_master = gf.Component("Triangle_Unit")
    triangle_master.add_polygon(points=triangle_pts, layer=layer)

    # --- 2. 准备晶格参数 ---
    vec_a1 = np.array([a, 0])
    vec_a2 = np.array([a/2, a * np.sqrt(3)/2])

    # --- 3. 生成阵列 ---
    grid_range = range(-n_rings, n_rings + 1)
    
    for i in grid_range:
        for j in grid_range:
            # 计算晶格中心坐标
            center_pos = i * vec_a1 + j * vec_a2
            
            # 限制在圆形区域内
            dist_from_origin = np.linalg.norm(center_pos)
            if dist_from_origin > n_rings * a:
                continue

            # --- 4. 计算拓扑位移 ---
            # 获取极角 theta (-pi, pi]
            theta = np.arctan2(center_pos[1], center_pos[0])
            
            # 广义涡旋相位调制
            phi = charge * theta + np.pi/2
            
            # 振幅调制 (tanh window)
            amplitude_modulation = np.tanh(dist_from_origin / (w0 * a))
            current_shift = m0 * amplitude_modulation
            
            # 位移矢量
            dx = current_shift * np.cos(phi)
            dy = current_shift * np.sin(phi)
            shift_vec = np.array([dx, dy])

            # --- 5. 放置三角形 (使用引用 Reference) ---
            
            # 子晶格 1 位置 (中心上方)
            pos1 = center_pos + np.array([0, a/np.sqrt(3)/2]) 
            # 子晶格 2 位置 (中心下方)
            pos2 = center_pos - np.array([0, a/np.sqrt(3)/2])
            
            # 添加三角形 1 的引用
            ref1 = c << triangle_master
            # move 方法接受 numpy array，但在某些版本为了安全转为 tuple
            ref1.move(pos1 + shift_vec)
            
            # 添加三角形 2 的引用 (需要翻转)
            ref2 = c << triangle_master
            # 镜像翻转 (沿x轴镜像，即y->-y)
            ref2.mirror(p1=(0,0), p2=(1,0)) 
            # 移动到位置 (注意：先镜像后移动，或者移动后局部镜像，GDSFactory默认是原点镜像)
            # 这里为了简单，我们直接再做一个倒三角的 master component 可能更直观，
            # 但用镜像也可以。ref2 目前在 (0,0) 镜像了。
            # 移动到目标位置
            ref2.move(pos2 - shift_vec)

    return c

if __name__ == "__main__":
    # 生成 GDS
    component = topological_vortex_laser(
        a=0.5, 
        m0=0.05, 
        ltr=0.166, 
        n_rings=20, 
        charge=1
    )
    
    # 显示并保存
    component.show() 
    component.write_gds("20251121_Dirac_Vortex_Fixed.gds")
    print("GDS file generated: 20251121_Dirac_Vortex_Fixed.gds")