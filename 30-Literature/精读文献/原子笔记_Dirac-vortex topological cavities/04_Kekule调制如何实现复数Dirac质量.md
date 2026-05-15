---
title: "Kekule 调制如何实现复数 Dirac 质量"
aliases:
  - generalized Kekule modulation
  - Kekule modulation Dirac mass
tags:
  - atomic-note
  - photonic-crystal
  - kekule-modulation
source: "[[Dirac-vortex topological cavities 精读笔记]]"
created: 2026-05-12
---

# Kekule 调制如何实现复数 Dirac 质量

本文用蜂窝光子晶体中的 generalized Kekule modulation（广义 Kekule 调制）实现复数 Dirac mass。

实现步骤：

1. 采用蜂窝光子晶体超胞，把 $K$ 和 $K'$ 两个 Dirac 点折叠到 $\Gamma$ 点，形成 double Dirac cone（双 Dirac 锥）。
2. 移动灰色子晶格中的三个三角形空气孔。
3. 位移幅度记为 $m_0$，位移方向由相位 $\phi_0$ 控制。
4. 几何调制可写成：

$$
m=m_0e^{j\phi_0}
$$

它与有效 Dirac 方程中的复数质量

$$
m=m_1+jm_2
$$

具有相同物理效果。

直观理解：

- $m_0$ 决定 gap 打开多大。
- $\phi_0$ 决定 gap 的内部相位方向。
- 让 $\phi_0$ 在实空间绕转，就得到 Dirac-vortex cavity。

相关笔记：

- [[03_Dirac质量涡旋与Jackiw-Rossi零模]]
- [[05_四个设计参数_w_m0_R_alpha]]
