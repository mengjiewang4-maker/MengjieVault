"""
演示 bond-center cut 的旋错拼接方法，并求解简化紧束缚模型的缺陷模。

术语提示：GDS 是芯片版图文件；disclination 表示旋错缺陷；TB/紧束缚模型用于用矩阵近似描述耦合模态。
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 手动设置区域 (修改这里即可)
# ==========================================
target_n = 6       # 手动改为 3, 5 或 6
Nx, Ny = 12, 12    # 原始象限的尺寸
t1, t2 = 1.0, 0.05 # 拓扑参数 (t1 > t2 为拓扑相)
a = 1.0            # 晶格常数

# ==========================================
# 2. 核心算法逻辑
# ==========================================

# Step 1: 键中心切割 (Bond-center Cut)
# 偏移 0.5a 确保切割线在格点中间，旋转拼接时不会重叠
ticks = (np.arange(0, Nx) + 0.5) * a
xv, yv = np.meshgrid(ticks, ticks)
q1_lat = np.vstack([xv.ravel(), yv.ravel()]).T

# Step 2: 角度映射 (90度 -> 360/n 度)
# n=3 时拉伸为 120度; n=5 时压缩为 72度; n=6 时压缩为 60度
target_unit_angle = 360.0 / target_n
coeff = target_unit_angle / 90.0

stretched_unit = []
for x, y in q1_lat:
    r = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    new_phi = phi * coeff
    stretched_unit.append([r * np.cos(new_phi), r * np.sin(new_phi)])
stretched_unit = np.array(stretched_unit)

# Step 3: 旋转复制 n 次并拼接
final_pos_list = []
for i in range(target_n):
    theta = i * (2 * np.pi / target_n)
    rot = np.array([[np.cos(theta), -np.sin(theta)], 
                    [np.sin(theta),  np.cos(theta)]])
    final_pos_list.extend(stretched_unit @ rot.T)

pos = np.array(final_pos_list)
# 圆形截断：去除参差不齐的边缘，使微腔更美观
pos = pos[np.linalg.norm(pos, axis=1) < Nx * 0.9]

# Step 4: 构建哈密顿量 (Tight-Binding)
num = len(pos)
H = np.zeros((num, num))
cutoff = 1.3 * a # 容差半径
for i in range(num):
    for j in range(i + 1, num):
        r = np.linalg.norm(pos[i] - pos[j])
        if r < cutoff:
            # 自动判定最近邻(t1)和次近邻(t2)
            H[i, j] = H[j, i] = t1 if r < cutoff * 0.85 else t2

# 求解能谱和本征模
E, V = np.linalg.eigh(H)
mid_idx = len(E) // 2  # 取能隙中间的态
mode = V[:, mid_idx]
intensity = np.abs(mode)**2

# ==========================================
# 3. 结果可视化
# ==========================================
plt.figure(figsize=(14, 5))

# 左图：晶格几何结构
plt.subplot(121)
plt.scatter(pos[:,0], pos[:,1], s=15, c='lightgray', edgecolors='gray', alpha=0.6)
# 绘制缝合线参考
for i in range(target_n):
    ang = i * (2 * np.pi / target_n)
    plt.plot([0, Nx*np.cos(ang)], [0, Nx*np.sin(ang)], 'r--', lw=1, alpha=0.4)
plt.gca().set_aspect('equal')
plt.title(f"Rigid Stitched C{target_n} Lattice (Bond-cut)")

# 右图：拓扑缺陷态分布 (Disclination Mode)
plt.subplot(122)
# s=intensity*8000 突出显示能量局域化的位置
plt.scatter(pos[:,0], pos[:,1], c=np.angle(mode), 
            s=intensity * 10000 + 10, cmap="twilight", edgecolors='none')
plt.colorbar(label="Phase")
plt.gca().set_aspect('equal')
plt.title(f"Topological Mode (E={E[mid_idx]:.3f})")

plt.tight_layout()
plt.show()