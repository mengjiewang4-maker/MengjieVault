---
title: 薛定谔方程
tags:
  - quantum-mechanics
  - math
aliases:
  - Schrodinger Equation
status: draft
---

# 薛定谔方程 / Schrodinger Equation

## 作用

薛定谔方程描述量子态如何随时间演化，是从 [[wavefunction|波函数]] 计算概率分布变化的核心模型。

## 时间依赖形式

$$
i\hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t)=\hat{H}\Psi(\mathbf{r},t)
$$

其中 $\hat{H}$ 是哈密顿算符，代表系统总能量。

## 一维定态形式

$$
-\frac{\hbar^2}{2m}\frac{d^2\psi(x)}{dx^2}+V(x)\psi(x)=E\psi(x)
$$

## 学习提示

先把它理解为“状态演化规则”，再进入具体势阱、谐振子等模型。

## 相关笔记

- [[wavefunction]]
- [[superposition]]
