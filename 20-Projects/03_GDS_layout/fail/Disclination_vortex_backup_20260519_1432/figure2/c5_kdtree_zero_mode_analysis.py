"""
使用 KDTree 加速近邻搜索，构建 C5 旋错的紧束缚哈密顿量并绘制零模。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# ==========================================
# 1. 参数设置
# ==========================================
target_n = 5       # 旋错对称性: 3, 5, 6
Nx, Ny = 10, 10    # 稍微增大阵列
a = 1.0            
delta = 0.35       

t1 = -0.2          # 胞内 (Intra)
t2 = -1.0          # 胞间 (Inter) - 拓扑相
tn = t2 / np.sqrt(2) # 旋错中心耦合

# ==========================================
# 2. 几何构建 (优化逻辑)
# ==========================================
def build_geometry(n_sym, nx, ny, a, d):
    """
    生成一个角度映射并旋转拼接后的 Cn 旋错点阵。
    """
    q1_atoms = []
    for i in range(nx):
        for j in range(ny):
            cx, cy = i * a, j * a
            basis = np.array([
                [cx-d, cy-d], [cx+d, cy-d],
                [cx-d, cy+d], [cx+d, cy+d]
            ])
            # 仅保留第一象限
            mask = (basis[:, 0] >= -1e-9) & (basis[:, 1] >= -1e-9)
            q1_atoms.extend(basis[mask])
    
    q1_pos = np.array(q1_atoms)
    
    # 角度映射
    coeff = (360.0 / n_sym) / 90.0
    r = np.linalg.norm(q1_pos, axis=1)
    phi = np.arctan2(q1_pos[:, 1], q1_pos[:, 0]) * coeff
    unit_pos = np.column_stack([r * np.cos(phi), r * np.sin(phi)])
    
    # 旋转拼接
    final_pos = []
    for i in range(n_sym):
        theta = i * (2 * np.pi / n_sym)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        final_pos.extend(unit_pos @ rot.T)
    
    pos = np.array(final_pos)
    # 截断与去重
    pos = pos[np.linalg.norm(pos, axis=1) < nx * a * 0.8]
    _, indices = np.unique(np.round(pos, 6), axis=0, return_index=True)
    return pos[indices]

pos = build_geometry(target_n, Nx, Ny, a, delta)

# ==========================================
# 3. 优化哈密顿量构建 (KDTree)
# ==========================================
num = len(pos)
H = np.zeros((num, num), dtype=complex)
tree = KDTree(pos)

# 动态计算特征距离（应对形变后的平均值）
d_intra_ref = 2 * delta
d_inter_ref = a - 2 * delta

# 使用 KDTree 搜索最大可能的耦合半径
max_r = max(d_intra_ref, d_inter_ref) * 1.5
pairs = tree.query_pairs(max_r)

edges_t1 = []
edges_t2 = []
edges_tn = []

for i, j in pairs:
    r = np.linalg.norm(pos[i] - pos[j])
    
    # 逻辑判定：
    # 1. 核心耦合 tn (距离原点极近的跨象限耦合)
    dist_to_origin = (np.linalg.norm(pos[i]) + np.linalg.norm(pos[j])) / 2
    if dist_to_origin < d_intra_ref and r < d_intra_ref * 1.2:
        # 这里判断是否跨越了扇区边界，简化为中心聚集点
        H[i, j] = H[j, i] = tn
        edges_tn.append([i, j])
    
    # 2. 胞内耦合 t1
    elif r < d_intra_ref * 1.1:
        H[i, j] = H[j, i] = t1
        edges_t1.append([i, j])
        
    # 3. 胞间耦合 t2
    elif r < d_inter_ref * 1.3:
        H[i, j] = H[j, i] = t2
        edges_t2.append([i, j])

# ==========================================
# 4. 求解与可视化
# ==========================================
E, V = np.linalg.eigh(H)
mid_idx = num // 2
# 寻找最接近 0 能级的态（可能是多个简并态）
zero_modes = np.where(np.abs(E) < 1e-2)[0]
mode_idx = zero_modes[0] if len(zero_modes) > 0 else mid_idx

plt.figure(figsize=(18, 5))

# Plot A: 能谱图 (Spectrum)
plt.subplot(131)
plt.scatter(range(num), E, s=5, c='k')
plt.axhline(0, color='r', lw=0.5, ls='--')
plt.title("Energy Spectrum\nZero modes indicate topological states")
plt.xlabel("State Index")
plt.ylabel("Energy")

# Plot B: 晶格与跳跃 (Lattice & Hopping)
plt.subplot(132)
for i, j in edges_t1:
    plt.plot([pos[i,0], pos[j,0]], [pos[i,1], pos[j,1]], 'gray', lw=0.5, alpha=0.3)
for i, j in edges_t2:
    plt.plot([pos[i,0], pos[j,0]], [pos[i,1], pos[j,1]], 'blue', lw=1, alpha=0.5)
for i, j in edges_tn:
    plt.plot([pos[i,0], pos[j,0]], [pos[i,1], pos[j,1]], 'red', lw=1.5)
plt.scatter(pos[:,0], pos[:,1], s=10, c='k', zorder=3)
plt.gca().set_aspect('equal')
plt.title("Hopping Links\n(Red: $t_n$, Blue: $t_2$, Gray: $t_1$)")

# Plot C: 拓扑旋错态 (Topological Mode)
plt.subplot(133)
mode = V[:, mode_idx]
intensity = np.abs(mode)**2
plt.scatter(pos[:,0], pos[:,1], c=np.angle(mode), s=intensity * (20000/np.max(intensity)), 
            cmap="hsv", edgecolors='k', lw=0.2, zorder=3)
plt.colorbar(label="Phase")
plt.gca().set_aspect('equal')
plt.title(f"Zero Mode (E={E[mode_idx]:.4f})\nLocalized at Disclination Core")

plt.tight_layout()
plt.show()