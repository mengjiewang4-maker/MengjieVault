---
title: TE-like基模能带与场分布计算
type: concept
status: draft
created: 2026-04-21
updated: 2026-04-21
tags:
  - wiki
  - concept
  - optics
  - topological-photonics
  - photonic-crystal
source: "@Vortex nanolaser based on a photonic disclination cavity"
zotero: "zotero://select/items/@Vortex nanolaser based on a photonic disclination cavity"
concepts:
  - "[[TE-like基模能带与场分布计算]]"
related:
  - "[[TE-like模]]"
  - "[[光子晶体能带]]"
  - "[[场分布]]"
---

# [[TE-like基模能带与场分布计算]]

## Source

@Vortex nanolaser based on a photonic disclination cavity
[zotero://select/items/@Vortex nanolaser based on a photonic disclination cavity](zotero://select/items/@Vortex nanolaser based on a photonic disclination cavity)

## 白话解释

这句话的核心意思是：作者先算了这个结构里最基本的一支 `TE-like` 模式的 [[光子晶体能带]]，同时也看了对应本征模的 [[场分布]]。

这里的 `TE-like` 不是严格理想二维里的纯 TE 模，而是实际光子晶体薄膜中“主要表现得像 TE”的模式，也就是电场主要分布在平面内，法向分量相对较弱。算 `bandstructure` 是为了知道不同 Bloch 波矢下允许出现哪些模；算 `field profile` 是为了看这些模的电场到底集中在哪、偏振长什么样、是不是符合后面缺陷腔或涡旋模设计的需要。

## 核心公式

对周期结构中的电磁模，通常求解 Maxwell 本征值问题：

$$
\nabla \times \left( \frac{1}{\varepsilon(\mathbf{r})} \nabla \times \mathbf{H}(\mathbf{r}) \right)
= \left( \frac{\omega}{c} \right)^2 \mathbf{H}(\mathbf{r})
$$

结合 Bloch 条件：

$$
\mathbf{H}_{n,\mathbf{k}}(\mathbf{r}) = e^{i\mathbf{k}\cdot\mathbf{r}} u_{n,\mathbf{k}}(\mathbf{r})
$$

其中：

- $\mathbf{k}$：布里渊区中的波矢；
- $n$：能带编号；
- $\omega_n(\mathbf{k})$：对应的本征频率；
- `field profile` 就是本征模对应的 $\mathbf{E}(\mathbf{r})$ 或 $\mathbf{H}(\mathbf{r})$ 空间分布。

如果只关心 `TE-like` 基模，通常就是在最低几支带里挑出偏振特征最接近 TE 的那一支来分析。

## 代码映射

```python
import numpy as np

def plane_wave_band_mock(kx, ky, c0=3e8, eps_eff=12.0):
    """
    一个简化示意：把 TE-like 模近似成有效介质中的色散关系。
    这不是完整光子晶体求解，只是说明 bandstructure 的数值对象是什么。
    """
    k2 = kx**2 + ky**2
    omega = c0 * np.sqrt(k2 / eps_eff)
    return omega

def sample_band_path(k_path):
    omegas = []
    for kx, ky in k_path:
        omegas.append(plane_wave_band_mock(kx, ky))
    return np.array(omegas)

def field_intensity(E):
    """
    E.shape = (..., 3)
    返回 |E|^2，作为 field profile 的强度图
    """
    return np.sum(np.abs(E)**2, axis=-1)

k_path = [
    (0.0, 0.0),
    (0.1, 0.0),
    (0.2, 0.0),
    (0.2, 0.1),
    (0.2, 0.2),
]

band = sample_band_path(k_path)

Nx, Ny = 50, 50
x = np.linspace(-1, 1, Nx)
y = np.linspace(-1, 1, Ny)
X, Y = np.meshgrid(x, y, indexing="ij")

E = np.zeros((Nx, Ny, 3), dtype=complex)
E[..., 0] = np.cos(np.pi * X) * np.sin(np.pi * Y)
E[..., 1] = -np.sin(np.pi * X) * np.cos(np.pi * Y)
E[..., 2] = 0.05 * np.sin(np.pi * X) * np.sin(np.pi * Y)

I = field_intensity(E)

print("Band frequencies:", band)
print("Max field intensity:", I.max())
```

## 代码理解

这里的数值映射关系是：

- `k_path`：布里渊区高对称路径，对应论文里画能带时横轴走过的波矢路径。
- `band`：每个波矢点对应的本征频率，连起来就是能带。
- `E[..., 0:3]`：模场的三个分量，对应 field profile。
- `I = |E|^2`：常用来画模式强度分布，判断能量主要局域在哪些位置。

如果要做真实计算，通常不是手写这个简化模型，而是用：

- 平面波展开法求 `bandstructure`
- FDTD / FEM 求缺陷模和场分布

## 原子关联

- [[TE-like模]]
- [[光子晶体能带]]
- [[场分布]]
- [[Bloch模]]
- [[Maxwell本征值问题]]
