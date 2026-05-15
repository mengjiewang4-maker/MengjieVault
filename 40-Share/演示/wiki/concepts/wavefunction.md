---
title: 波函数
tags:
  - quantum-mechanics
  - concept
aliases:
  - Wavefunction
status: draft
---

# 波函数 / Wavefunction

## 直觉理解

波函数不是普通空间中的物质波本身，而是量子态的一种数学表示。它的模平方给出测量结果的概率密度。

## 形式化表述

在一维位置表象中，波函数可写作 $\psi(x)$。粒子出现在区间 $[a,b]$ 的概率为：

$$
P(a \le x \le b)=\int_a^b |\psi(x)|^2 dx
$$

归一化条件为：

$$
\int_{-\infty}^{\infty} |\psi(x)|^2 dx = 1
$$

## 常见误解

- 误解：波函数的值本身就是直接可见的物理量。
- 更准确：通常可测的是由波函数计算出的概率、期望值或相关测量统计。

## 相关笔记

- [[40-Share/演示/wiki/math/schrodinger-equation]]
- [[40-Share/演示/wiki/concepts/measurement]]
- [[40-Share/演示/量子力学/01]]
