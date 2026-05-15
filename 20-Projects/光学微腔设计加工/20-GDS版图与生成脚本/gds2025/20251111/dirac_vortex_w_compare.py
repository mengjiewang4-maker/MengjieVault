import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================
# 参数设置
# ============================================
R = 2.5     # 调制半径 (µm)
alpha = 4   # 调制陡峭度
m0 = 0.05   # 调制幅度 (µm)
w_list = [1, 2, 3]   # 拓扑绕数
dpi = 300   # 输出分辨率
save_path = "dirac_vortex_w_compare_fixed.png"  # 输出文件名

# ============================================
# 构建坐标网格
# ============================================
x = np.linspace(-3 * R, 3 * R, 600)
y = np.linspace(-3 * R, 3 * R, 600)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)
phi = np.arctan2(Y, X)

# ============================================
# 幅度函数 |m(r)| = m0 * tanh((r/R)^α)
# ============================================
amp = m0 * np.tanh((r / R) ** alpha)

# ============================================
# 绘图
# ============================================
# 关键修改 1: 添加 layout="constrained"
fig, axes = plt.subplots(1, len(w_list), figsize=(15, 5), layout="constrained")

for i, w in enumerate(w_list):
    phase = (w * phi) % (2 * np.pi)
    img = axes[i].imshow(
        phase,
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        cmap="twilight_shifted"
    )
    axes[i].set_title(f"w = {w}", fontsize=12)
    axes[i].set_xlabel("x (µm)")
    if i == 0:
        axes[i].set_ylabel("y (µm)")
    axes[i].set_aspect("equal")

fig.suptitle("Dirac-Vortex Phase Field Comparison", fontsize=14)

# 关键修改 2: 使用 fig.colorbar 并关联到所有轴
# constrained 布局会自动在右侧为它腾出空间
fig.colorbar(img, ax=axes.ravel().tolist(), shrink=0.8, label="Phase (radians)")

# 关键修改 3: 移除 plt.tight_layout()，因为它已不再需要

# ============================================
# 保存图像
# ============================================
plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
plt.close()
print(f"✅ 相位对比图已保存为：{os.path.abspath(save_path)}")