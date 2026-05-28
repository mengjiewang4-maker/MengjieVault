"""
分步演示 cell-centered cut 旋错构造，并求解 SSH/BBH 模型中的旋错态。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设置
# ==========================================
target_n = 5       # 旋错对称性: 3, 5, 6
Nx, Ny = 8, 8      # 原始象限的晶胞阵列大小
a = 1.0            # 晶胞间距
delta = 0.2       # 胞内偏移 (delta越小，同一个晶胞内的4个点靠得越近)

# 耦合强度 (SSH/BBH模型参数)
t1 = -0.2           # 胞内 (Intra-cell hopping) - 较弱
t2 = -1.0           # 胞间 (Inter-cell hopping) - 较强 (拓扑相)
tn = t2/np.sqrt(2)  # 旋错中心近邻 (Near-neighbor) - 跨象限耦合

# ==========================================
# 2. 实验全流程 (分步绘图)
# ==========================================
plt.figure(figsize=(20, 5))

# --- Step 1: 晶胞内切割 (Cell-centered Cut) ---
# 此时坐标原点 (0,0) 正好落在第一个晶胞的中心
q1_atoms = []
for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        # 生成胞内 4 个格点
        basis = np.array([
            [cx-delta, cy-delta], [cx+delta, cy-delta],
            [cx-delta, cy+delta], [cx+delta, cy+delta]
        ])
        # 严格保留第一象限原子 (x>=0, y>=0，含坐标为 0 的边界点)
        # 对于 i=0, j=0 的晶胞，只有 [cx+delta, cy+delta] 这一个点会被留下
        for atom in basis:
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
q1_pos = np.array(q1_atoms)

plt.subplot(141)
plt.scatter(q1_pos[:,0], q1_pos[:,1], s=18, c='royalblue', edgecolors='k', lw=0.5)
# 绘制切割线示意：穿过了原本 (0,0) 的晶胞
plt.axvline(0, color='r', ls='--', alpha=0.6); plt.axhline(0, color='r', ls='--', alpha=0.6)
plt.gca().set_aspect('equal')
plt.title(f"Step 1: Cell-centered Cut\n(90° Quadrant, delta={delta})")

# --- Step 2: 角度映射 (90° -> 360/n°) ---
# C_3 为 120°，C_5 为 72°
coeff = (360.0 / target_n) / 90.0
stretched_list = []
for x, y in q1_pos:
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * coeff
    stretched_list.append([r * np.cos(phi), r * np.sin(phi)])
stretched_unit = np.array(stretched_list)

plt.subplot(142)
plt.scatter(stretched_unit[:,0], stretched_unit[:,1], s=18, c='forestgreen', edgecolors='k', lw=0.5)
plt.gca().set_aspect('equal')
plt.title(f"Step 2: Angular Stretch\nto {360/target_n:.0f}°")

# --- Step 3: 旋转拼接 (C{n} 对称核心聚集) ---
final_pos = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    final_pos.extend(stretched_unit @ rot.T)

pos = np.array(final_pos)
# 严格去重 (防止由于旋转产生的坐标极近的点)
#_, indices = np.unique(np.round(pos, 6), axis=0, return_index=True)
#pos = pos[indices]
# 边缘圆形截断 (使微腔形状规整)
pos = pos[np.linalg.norm(pos, axis=1) < Nx * a * 0.85]

plt.subplot(143)
plt.scatter(pos[:,0], pos[:,1], s=12, c='gray', alpha=0.4)
plt.xlim(-8, 8); plt.ylim(-8, 8)
plt.scatter(0, 0, marker='+', c='k', s=50) # 标记原点
plt.gca().set_aspect('equal')
plt.title(f"Step 3: C{target_n} Stitched Core\n(Center Aggregated)")

# --- Step 4: SSH/BBH 哈密顿量求解 (Disclination Mode) ---
num = len(pos)
H = np.zeros((num, num), dtype=complex)
# 定义特征距离用于判定跳跃类型
d_intra = 2 * delta                    # 理论胞内距离 (Clustering)
d_inter = a - 2 * delta                # 理论胞间距离 (Topological)

# 修改 Step 4 中的耦合判定逻辑
for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j])
        
        # 1. 胞内耦合 t1 (最近的原子对)
        if 0.1 < r < d_intra * 1.1:
            H[i, j] = H[j, i] = t1
        
        # 2. 胞间耦合 t2 (标准拓扑连接)
        elif d_intra * 1.1 <= r < d_inter * 1.1:
            H[i, j] = H[j, i] = t2
            
        # 3. 核心区域 tn (针对中心聚集的 5 个原子)
        # 这里的距离通常比 d_inter 更小，因为角度被压缩了
        elif r < d_intra: # 极靠近中心的跨象限耦合
            H[i, j] = H[j, i] = tn
# 求解能谱和特征向量
E, V = np.linalg.eigh(H)
mid_idx = len(E) // 2
mode = V[:, mid_idx]
intensity = np.abs(mode)**2

plt.subplot(144)
# 用点的大小(s)表示强度(Intensity)，用颜色控制相位
plt.scatter(pos[:,0], pos[:,1], c=np.angle(mode), s=intensity*12000+10, 
            cmap="twilight", edgecolors='k', lw=0.1)
plt.colorbar(label="Phase")
plt.gca().set_aspect('equal')
plt.title(f"Step 4: Topological Mode\nEnergy: {E[mid_idx]:.4f}")

plt.tight_layout()
plt.show()