---
title: Dirac 符号
tags:
  - quantum/notation
aliases:
  - bra-ket
  - 狄拉克符号
---

# Dirac 符号

Dirac 符号用 $|\psi\rangle$ 表示态矢，用 $\langle\phi|$ 表示对偶矢量，内积写作 $\langle\phi|\psi\rangle$。

若 $|k\rangle$ 是一组完备正交基，则

$$
|\psi\rangle=\sum_k |k\rangle\langle k|\psi\rangle,\qquad
\sum_k |k\rangle\langle k|=I
$$

连续谱情形中，求和换成积分，例如

$$
\int dx\,|x\rangle\langle x|=I,\qquad
\langle x|x'\rangle=\delta(x-x')
$$

## 关键点

- 把坐标表象、动量表象、矩阵表象统一为抽象态空间语言。
- 投影振幅 $\langle a_n|\psi\rangle$ 给出测量概率幅。
- 算符矩阵元写为 $\langle a_m|\hat A|a_n\rangle$。
- 投影算符 $|k\rangle\langle k|$ 抽取态在基矢 $|k\rangle$ 方向上的分量。
- Dirac 符号可以先做抽象推导，再选具体表象计算。

## 连接

- 第 7 章表象变换的主要语言。
- 与 [[力学量算符]] 和 [[态叠加与测量]] 直接相连。
- 与 [[矩阵形式]]、[[连续谱归一化]] 相连。
