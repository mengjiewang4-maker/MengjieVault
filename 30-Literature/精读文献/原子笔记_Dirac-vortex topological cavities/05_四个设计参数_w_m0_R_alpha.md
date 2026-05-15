---
title: "Dirac-vortex cavity 的四个设计参数"
aliases:
  - w m0 R alpha
  - Dirac-vortex cavity parameters
tags:
  - atomic-note
  - cavity-design
  - topological-photonics
source: "[[Dirac-vortex topological cavities 精读笔记]]"
created: 2026-05-12
---

# Dirac-vortex cavity 的四个设计参数

Dirac-vortex cavity 的调制函数为：

$$
m(r-r_0;w,m_0,R,\alpha)
=m_0 \tanh \left(\left|\frac{r-r_0}{R}\right|^\alpha\right)
e^{j[\phi_0-w\arg(r-r_0)]}
$$

四个参数分别控制：

| 参数 | 含义 | 控制作用 |
|---|---|---|
| $w$ | winding number（绕数） | $|w|$ 决定中隙模数量，符号决定手性 |
| $m_0$ | maximum modulation amplitude（最大调制幅度） | 控制 gap 深度、辐射耦合和 Q |
| $R$ | vortex radius（涡旋半径） | 控制模式面积，不等于器件外尺寸 |
| $\alpha$ | shape factor（形状因子） | 控制势阱形状和远场质量 |

一句话记忆：

> $w$ 管模式数，$m_0$ 管耦合强度，$R$ 管大小，$\alpha$ 管形状。

相关笔记：

- [[04_Kekule调制如何实现复数Dirac质量]]
- [[06_FSR异常尺度律]]
