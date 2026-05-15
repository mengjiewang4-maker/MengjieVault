import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 核心参数
# ==========================================
target_n = 5
Nx, Ny = 8, 8
a = 1.0
delta = 0.2  # 调小一点，使胞内点更聚集，方便观察
t1, t2 = -0.2, -1.0
tn = -0.8    # 跨象限的核心耦合

# ==========================================
# 2. 带标签的原子生成 (Step 1 改进)
# ==========================================
q1_atoms = []
q1_tags = [] # 记录 (cell_i, cell_j, sub_index)

for i in range(Nx):
    for j in range(Ny):
        cx, cy = i * a, j * a
        # 胞内 4 个点：0:(左下), 1:(右下), 2:(左上), 3:(右上)
        basis = np.array([
            [cx-delta, cy-delta], [cx+delta, cy-delta],
            [cx-delta, cy+delta], [cx+delta, cy+delta]
        ])
        for idx, atom in enumerate(basis):
            # 这里的切割逻辑：保留属于第一象限的物理点
            if atom[0] >= -1e-9 and atom[1] >= -1e-9:
                q1_atoms.append(atom)
                q1_tags.append((i, j, idx))

q1_pos = np.array(q1_atoms)
coeff = (360.0 / target_n) / 90.0

# = ::::::::::::::::::::::::::::::::::::::::
# 3. 旋转与拼接 (保留标签)
# = ::::::::::::::::::::::::::::::::::::::::
final_pos = []
final_tags = [] # 记录 (sector_k, cell_i, cell_j, sub_index)

for k in range(target_n):
    theta = k * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    
    for m in range(len(q1_pos)):
        x, y = q1_pos[m]
        r = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x) * coeff
        new_xy = np.array([r * np.cos(phi), r * np.sin(phi)]) @ rot.T
        
        final_pos.append(new_xy)
        # tag: [象限序号, 晶胞x, 晶胞y, 胞内序号]
        final_tags.append((k, q1_tags[m][0], q1_tags[m][1], q1_tags[m][2]))

pos = np.array(final_pos)
tags = np.array(final_tags)
num = len(pos)

# = ::::::::::::::::::::::::::::::::::::::::
# 4. 构建哈密顿量 (精准逻辑判定)
# = ::::::::::::::::::::::::::::::::::::::::
H = np.zeros((num, num), dtype=complex)

for i in range(num):
    k1, xi1, yi1, sub1 = tags[i]
    for j in range(i + 1, num):
        k2, xi2, yi2, sub2 = tags[j]
        
        # --- 情况 A: 同一扇区 (k1 == k2) ---
        if k1 == k2:
            # 胞内耦合 (同一 xi, yi)
            if xi1 == xi2 and yi1 == yi2:
                H[i, j] = H[j, i] = t1
            # 胞间耦合 (相邻 xi 或 yi)
            elif abs(xi1 - xi2) + abs(yi1 - yi2) == 1:
                # 只有面对面的原子才耦合 (BBH模型标准逻辑)
                dist_phys = np.linalg.norm(pos[i] - pos[j])
                if dist_phys < a * 1.1: # 辅助距离判定
                    H[i, j] = H[j, i] = t2

        # --- 情况 B: 跨扇区核心耦合 (重点！) ---
        else:
            # 判断是否是相邻扇区 (例如 0和1, 1和2, ..., n-1和0)
            if abs(k1 - k2) == 1 or abs(k1 - k2) == target_n - 1:
                # 1. 中心晶胞 (0,0) 的跨象限原子耦合
                if xi1 == 0 and yi1 == 0 and xi2 == 0 and yi2 == 0:
                    H[i, j] = H[j, i] = tn
                
                # 2. 邻边晶胞 (i=1, j=0) 或 (i=0, j=1) 
                # 判定“内侧原子”：通常是 index 0 或 2 (取决于坐标系旋转方向)
                # 这里简化处理：只要物理距离极近且在中心附近的跨扇区点
                dist_phys = np.linalg.norm(pos[i] - pos[j])
                if dist_phys < (a - 2*delta) * 1.2 and (xi1+yi1 <= 1 and xi2+yi2 <= 1):
                    H[i, j] = H[j, i] = tn

# ==========================================
# 5. 求解与绘图
# ==========================================
E, V = np.linalg.eigh(H)
mid_idx = len(E) // 2 # 寻找零能模

plt.figure(figsize=(10, 8))
plt.scatter(pos[:,0], pos[:,1], c=np.abs(V[:, mid_idx])**2, s=100, cmap='hot_r', edgecolors='k')
plt.colorbar(label="Localization Intensity")
plt.title(f"C{target_n} Disclination Mode (Refined Coupling)")
plt.gca().set_aspect('equal')
plt.show()

# 打印能级图确认 gap
plt.figure(figsize=(6, 4))
plt.plot(E, 'o', ms=2)
plt.axhline(0, color='r', ls='--')
plt.title("Energy Spectrum")
plt.show()