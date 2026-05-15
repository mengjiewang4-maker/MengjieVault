---
title: "Dirac-vortex cavity 的 FSR 异常尺度律"
aliases:
  - FSR V^-1/2
  - Dirac-vortex FSR scaling
tags:
  - atomic-note
  - free-spectral-range
  - scaling-law
source: "[[Dirac-vortex topological cavities 精读笔记]]"
created: 2026-05-12
---

# Dirac-vortex cavity 的 FSR 异常尺度律

FSR（free spectral range，自由光谱范围）是相邻腔模之间的频率或波长间隔。FSR 越大，越有利于单模工作。

普通腔通常满足：

$$
FSR\propto \frac{1}{V}
$$

Dirac-vortex cavity 满足：

$$
FSR\propto \frac{1}{L}\propto \frac{1}{\sqrt{V}}
$$

其中 $L$ 是模式直径，$V$ 是模式体积。二维情况下可以粗略理解为 $V\sim L^2$。

物理原因：

- 目标中隙模位于 Dirac frequency（Dirac 频率）附近。
- Dirac 点附近 optical density of states（光学态密度）低。
- 因此中隙模附近的模式谱更稀疏，FSR 更大。

关键表述：

> 它不是靠把腔做小来增大 FSR，而是在大腔中利用 Dirac 点低态密度保持较大的模式间隔。

实验量化：

- 50 μm Dirac-vortex cavity 的实验 FSR 为 8.22 nm。
- 相同模式体积的 Fabry-Perot cavity 约为 1.28 nm。

相关笔记：

- [[05_四个设计参数_w_m0_R_alpha]]
- [[08_SOI实验验证]]
