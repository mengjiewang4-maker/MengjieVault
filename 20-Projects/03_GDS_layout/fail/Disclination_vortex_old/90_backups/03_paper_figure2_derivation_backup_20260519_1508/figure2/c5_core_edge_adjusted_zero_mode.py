"""
在 C5 旋错结构中手动调节第二层点位和核心耦合，用于探索零能局域模。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设置
# ==========================================
target_n = 5       # 旋错对称性
Nx, Ny = 10, 10    # 阵列大小
a = 1.0            
delta = 0.25       # 初始胞内偏移

# 耦合强度
t1 = -0.2          # 胞内 (弱)
t2 = -1.0          # 胞间 (强 -> 拓扑相)
tn = -0.8          # 中心核心耦合

# ==========================================
# 2. 基础几何构建 (Step 1-3 整合)
# ==========================================
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        basis = np.array([[cx-delta, cy-delta], [cx+delta, cy-delta],
                          [cx-delta, cy+delta], [cx+delta, cy+delta]])
        for atom in basis:
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
q1_pos = np.array(q1_atoms)

# 角度映射与旋转拼接
coeff = (360.0 / target_n) / 90.0
final_pos = []
for i in range(target_n):
    theta_rot = i * (2 * np.pi / target_n)
    rot_mat = np.array([[np.cos(theta_rot), -np.sin(theta_rot)], 
                        [np.sin(theta_rot), np.cos(theta_rot)]])
    for x, y in q1_pos:
        r = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x) * coeff
        p_stretched = np.array([r * np.cos(phi), r * np.sin(phi)])
        final_pos.append(p_stretched @ rot_mat.T)

pos = np.array(final_pos)
# 去除极近的重复点
_, indices = np.unique(np.round(pos, 5), axis=0, return_index=True)
pos = pos[indices]
# 截断边缘，保持圆形外观
pos = pos[np.linalg.norm(pos, axis=1) < (Nx-2)*a]

# ==========================================
# 3. 精确结构调整 (关键步骤)
# ==========================================
r_vals = np.linalg.norm(pos, axis=1)
angles = np.degrees(np.arctan2(pos[:, 1], pos[:, 0])) % 360

# --- A. 识别中心 5 个原子 ---
core_indices = np.argsort(r_vals)[:target_n]

# --- B. 识别并调整第二层 ---
# 定义第二层的径向范围 (根据 delta 和 a 估算)
layer1_mask = (r_vals > 0.8) & (r_vals < 2.2)
layer1_indices = np.where(layer1_mask)[0]

# C5 对称下：角(Corner)位于 0, 72, 144... 度；边(Edge)位于 36, 108, 180... 度
edge_centers = np.array([36, 108, 180, 252, 324])

adjusted_pos = pos.copy()
for idx in layer1_indices:
    phi = angles[idx]
    # 判断是否属于“边”晶胞区域
    is_edge = any(abs(phi - ec) < 20 for ec in edge_centers)
    
    if is_edge:
        # 对边晶胞内靠近中心的原子进行微调 (向中心移动 15%)
        # 这会自动改变其与 core 原子的距离，从而改变后续耦合判定
        adjusted_pos[idx] *= 0.85 

# ==========================================
# 4. 哈密顿量与能谱求解
# ==========================================
num = len(adjusted_pos)
H = np.zeros((num, num), dtype=complex)
d_intra_limit = 2 * delta * 1.2
d_inter_limit = (a - 2 * delta) * 1.2

for i in range(num):
    for j in range(i + 1, num):
        dist = np.linalg.norm(adjusted_pos[i] - adjusted_pos[j])
        
        # 1. 中心核心耦合 (tn)
        if i in core_indices and j in core_indices:
            if dist < 1.5: # 核心 5 原子互联
                H[i, j] = H[j, i] = tn
            continue
            
        # 2. 标准 SSH/BBH 耦合判定
        if 0.1 < dist < d_intra_limit:
            H[i, j] = H[j, i] = t1
        elif d_intra_limit <= dist < d_inter_limit:
            H[i, j] = H[j, i] = t2

# 求解
E, V = np.linalg.eigh(H)

# ==========================================
# 5. 可视化
# ==========================================
plt.figure(figsize=(16, 6))

# 子图 1: 结构微调示意
plt.subplot(131)
plt.scatter(adjusted_pos[:, 0], adjusted_pos[:, 1], c='lightgray', s=20)
plt.scatter(adjusted_pos[core_indices, 0], adjusted_pos[core_indices, 1], c='red', s=40, label='Core')
# 突出显示被移动的边晶胞原子
edge_show = [i for i in layer1_indices if any(abs(angles[i]-ec)<20 for ec in edge_centers)]
plt.scatter(adjusted_pos[edge_show, 0], adjusted_pos[edge_show, 1], c='green', s=30, label='Adj. Edge')
plt.title("Modified Lattice Structure")
plt.legend()
plt.gca().set_aspect('equal')

# 子图 2: 能谱图 (寻找零能模)
plt.subplot(132)
plt.plot(E, 'o', ms=3, color='royalblue', alpha=0.6)
plt.axhline(0, color='k', ls='--', lw=1)
plt.title("Energy Spectrum")
plt.ylabel("Energy")
plt.xlabel("Mode Index")

# 子图 3: 拓扑波导/旋错模空间分布
plt.subplot(133)
mid_idx = num // 2
# 选取能量最接近 0 的模
zero_mode_idx = np.argmin(np.abs(E))
mode_dist = np.abs(V[:, zero_mode_idx])**2
plt.scatter(adjusted_pos[:,0], adjusted_pos[:,1], c=mode_dist, cmap='magma', s=mode_dist*5000+10)
plt.colorbar(label="Intensity")
plt.title(f"Disclination Mode (E={E[zero_mode_idx]:.4f})")
plt.gca().set_aspect('equal')

plt.tight_layout()
plt.show()