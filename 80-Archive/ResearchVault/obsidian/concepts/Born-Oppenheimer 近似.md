---
title: Born-Oppenheimer 近似
tags:
  - quantum/method
aliases:
  - 玻恩-奥本海默近似
---

# Born-Oppenheimer 近似

Born-Oppenheimer 近似利用原子核远重于电子这一事实，把电子运动与核运动近似分离。

常写作

$$
\Psi(\mathbf r,\mathbf R)\approx \psi_e(\mathbf r;\mathbf R)\chi(\mathbf R)
$$

其中先把核坐标 $\mathbf R$ 当参数求电子态，再让原子核在电子能量面上运动。

## 物理图像

- 电子对核位置的变化响应很快。
- 先固定核位置求电子能量，再把它作为核运动的有效势能面。
- 是分子结构和化学键量子理论的基础。
- 适用基础是 $m_e/M_{\mathrm{nucleus}}\ll1$，电子运动通常比核运动快得多。

## 连接

- 第 12 章分子结构部分。
- 与 [[变分法]]、氢分子离子、双原子分子转动振动相连。
- 是理解 [[分子结构]] 的基础近似。
- 章节入口：[[第12章 其他近似方法]]
