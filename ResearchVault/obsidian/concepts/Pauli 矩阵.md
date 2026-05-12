---
title: Pauli 矩阵
tags:
  - quantum/concept
  - spin
aliases:
  - Pauli matrices
  - 泡利矩阵
created: 2026-05-06
updated: 2026-05-06
---

# Pauli 矩阵

Pauli 矩阵是描述自旋 $1/2$ 系统的基本 $2\times2$ 矩阵：

$$
\sigma_x=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
\sigma_y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
\sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}
$$

自旋算符写作

$$
\hat{\mathbf S}=\frac{\hbar}{2}\boldsymbol\sigma
$$

## 关键点

- Pauli 矩阵是 Hermitian 矩阵，对应可观测的自旋分量。
- 满足 $\sigma_i\sigma_j=\delta_{ij}I+i\epsilon_{ijk}\sigma_k$。
- 不同方向自旋分量不对易，因此不能同时确定。
- 二能级系统常可用 Pauli 矩阵表示有效 Hamilton 量。

## 连接

- 是 [[自旋]] 的矩阵表示。
- 与 [[矩阵形式]]、[[厄米算符]] 和 [[对易关系与不确定性关系]] 直接相关。
- 章节入口：[[第8章 自旋]]
