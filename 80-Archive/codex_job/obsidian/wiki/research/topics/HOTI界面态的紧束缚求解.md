---
title: HOTI界面态的紧束缚求解
type: concept
status: draft
created: 2026-04-21
updated: 2026-04-21
aliases:
  - Tight-binding calculation of HOTI interface states
tags:
  - wiki
  - concept
  - optics
  - topological-photonics
  - hoti
  - 2d-ssh
  - tight-binding
source: "@Vortex nanolaser based on a photonic disclination cavity"
zotero: "zotero://select/items/@Vortex nanolaser based on a photonic disclination cavity"
concepts:
  - "[[HOTI界面态的紧束缚求解]]"
  - "[[二维SSH模型]]"
  - "[[离散晶格近似]]"
related:
  - "[[基于光子位错腔的涡旋纳米激光器]]"
---

# [[HOTI界面态的紧束缚求解]]

## Source

@Vortex nanolaser based on a photonic disclination cavity
[zotero://select/items/@Vortex nanolaser based on a photonic disclination cavity](zotero://select/items/@Vortex nanolaser based on a photonic disclination cavity)

## 白话解释

这句话的意思是：在研究二维 [[二维SSH模型]] 里的高阶拓扑绝缘体（HOTI）时，人们通常先用 [[紧束缚模型]] 来算界面态。

这里默认系统是一个一个格点拼起来的 [[离散晶格近似]]，并且每个格点上放着“原子”或“谐振单元”这样的局域自由度。这样做的好处是：

- 可以把整个结构写成矩阵哈密顿量。
- 界面、缺陷、边界都能通过修改格点之间的耦合来直接表示。
- 算出来的本征值和本征态可以直接判断界面态是否存在、是否局域。

## 核心公式

二维 SSH 紧束缚哈密顿量可抽象写成

$$
H = \sum_{m,n} \Big(
t_x^{(1)} a_{m,n}^\dagger b_{m,n}
+ t_x^{(2)} b_{m,n}^\dagger a_{m+1,n}
+ t_y^{(1)} a_{m,n}^\dagger c_{m,n}
+ t_y^{(2)} c_{m,n}^\dagger a_{m,n+1}
+ \mathrm{h.c.}
\Big)
+ \sum_i \epsilon_i c_i^\dagger c_i
$$

其中：

- $t_x^{(1)}, t_x^{(2)}$：$x$ 方向胞内/胞间耦合。
- $t_y^{(1)}, t_y^{(2)}$：$y$ 方向胞内/胞间耦合。
- $\epsilon_i$：格点上的 on-site 项。
- 界面态通常出现在两侧拓扑相不同、导致耦合排布发生跳变的位置。

如果只关心“是否有界面态”，核心就是求解

$$
H \psi = E \psi
$$

并检查：

- $E$ 是否落在带隙内；
- $\psi$ 是否局域在界面附近。

## 代码映射

```python
import numpy as np

def idx(cell_x, cell_y, orb, Ny, n_orb=4):
    return (cell_x * Ny + cell_y) * n_orb + orb

def build_2d_ssh_hamiltonian(Nx, Ny, tx_intra, tx_inter, ty_intra, ty_inter, onsite=0.0):
    """
    2D SSH tight-binding Hamiltonian on a discrete lattice.
    Each unit cell has 4 orbitals/sites.
    """
    n_orb = 4
    dim = Nx * Ny * n_orb
    H = np.zeros((dim, dim), dtype=complex)

    def add_hop(i, j, t):
        H[i, j] += t
        H[j, i] += np.conjugate(t)

    for x in range(Nx):
        for y in range(Ny):
            a = idx(x, y, 0, Ny)
            b = idx(x, y, 1, Ny)
            c = idx(x, y, 2, Ny)
            d = idx(x, y, 3, Ny)

            for s in [a, b, c, d]:
                H[s, s] += onsite

            add_hop(a, b, tx_intra)
            add_hop(a, c, ty_intra)
            add_hop(b, d, ty_intra)
            add_hop(c, d, tx_intra)

            if x + 1 < Nx:
                a_r = idx(x + 1, y, 0, Ny)
                c_r = idx(x + 1, y, 2, Ny)
                add_hop(b, a_r, tx_inter)
                add_hop(d, c_r, tx_inter)

            if y + 1 < Ny:
                a_u = idx(x, y + 1, 0, Ny)
                b_u = idx(x, y + 1, 1, Ny)
                add_hop(c, a_u, ty_inter)
                add_hop(d, b_u, ty_inter)

    return H

H = build_2d_ssh_hamiltonian(
    Nx=8, Ny=8,
    tx_intra=1.0, tx_inter=1.8,
    ty_intra=1.0, ty_inter=1.8,
    onsite=0.0
)

eigvals, eigvecs = np.linalg.eigh(H)

gap_threshold = 0.2
in_gap = np.where(np.abs(eigvals) < gap_threshold)[0]

print("In-gap state energies:", eigvals[in_gap])
```

## 代码理解

上面的矩阵操作对应物理图像是：

- `H`：整个离散晶格系统的紧束缚哈密顿量。
- `add_hop(i, j, t)`：给两个格点之间加耦合，就是论文里的 hopping term。
- `np.linalg.eigh(H)`：求本征模，相当于找系统允许的模式频率/能量。
- `abs(eigvals) < gap_threshold`：筛出带隙中的态，它们往往就是界面态或角态候选。

如果要专门算“界面态”，通常进一步做：

- 让左半区和右半区取不同的 $t_\text{intra}/t_\text{inter}$；
- 再看本征矢量强度 $|\psi|^2$ 是否集中在相界面。

## 原子关联

- [[二维SSH模型]]
- [[HOTI界面态]]
- [[紧束缚模型]]
- [[离散晶格近似]]
- [[带隙中的局域态判据]]
