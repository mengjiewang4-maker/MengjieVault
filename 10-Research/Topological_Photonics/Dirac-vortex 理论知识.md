---
title: Dirac-vortex 理论知识
aliases:
  - Dirac-vortex cavity
  - Dirac 涡旋腔
  - Jackiw-Rossi zero mode
  - surface metallic Dirac-vortex cavity
tags:
  - photonics/topological
  - photonics/dirac-vortex
  - paper-note
created: 2026-05-13
updated: 2026-05-13
---

# Dirac-vortex 理论知识

> [!abstract] 核心结论
> Dirac-vortex cavity（Dirac 涡旋腔）的本质不是“在光子晶体中心随便做一个缺陷”，而是让打开 Dirac cone（Dirac 锥）的 mass term（质量项）在二维实空间中绕中心旋转。这个 mass vortex（质量涡旋）会束缚 Jackiw-Rossi zero mode（Jackiw-Rossi 零模），从而形成一个位于 photonic bandgap（光子带隙）中间的拓扑腔模。  
> 2020 年 Nature Nanotechnology 论文提出并验证这套理论；2024 年 Nature Communications 论文把它改造成 surface metallic Dirac-vortex cavity（表面金属 Dirac 涡旋腔, SMDC），用于高功率电泵浦太赫兹拓扑激光器。

## 两篇文献定位

| 文献 | 作用 | 需要抓住的理论点 |
|---|---|---|
| Gao et al., *Dirac-vortex topological cavities*, Nature Nanotechnology, 2020. DOI: `10.1038/s41565-020-0773-7` | 提出 Dirac-vortex cavity 的通用理论和硅光子晶体实现 | Jackiw-Rossi zero mode、复数 Dirac mass、Kekule 调制、$w,m_0,R,\alpha$ 四个设计参数、$FSR\propto V^{-1/2}$ |
| Liu et al., *High-power electrically pumped terahertz topological laser based on a surface metallic Dirac-vortex cavity*, Nature Communications, 2024. DOI: `10.1038/s41467-024-48788-y` | 把 Dirac-vortex 腔移植到 THz QCL（太赫兹量子级联激光器）表面金属层中 | 表面金属实现、双金属波导耦合、非破坏有源区、3% 带隙、单模电泵浦、远场相位调控 |

## 一句话物理图像

Dirac cone 提供一个可以被打开的线性交叉点；Kekule modulation（Kekule 调制）提供打开带隙的复数质量项；复数质量项绕空间中心转一圈形成 Dirac vortex；涡旋中心束缚一个 mid-gap mode（中隙模）；这个中隙模可作为单模激光腔模。

可以把它类比成二维版本的 phase-shifted DFB（相移分布反馈）腔：

- 1D 相移 DFB：一维带隙中插入相位缺陷，产生一个中隙模。
- 2D Dirac-vortex cavity：二维 Dirac 质量项形成相位涡旋，产生一个中隙模。

关键区别是：Dirac-vortex 腔调的是整个二维带隙纹理，而不是只改一个局部孔洞。

## 理论链条

### 1. 从 double Dirac cone 出发

蜂窝晶格天然有 $K/K'$ 两个 Dirac points（Dirac 点）。2020 年论文使用 hexagonal supercell（六角超胞）把 $K/K'$ 点折叠到 $\Gamma$ 点，形成 double Dirac cone（双 Dirac 锥）。

这样做有两个好处：

1. $\Gamma$ 点没有面内波矢，更适合 surface emission（表面出射）。
2. 双 Dirac 锥附近可以写成二维有效 Dirac Hamiltonian（哈密顿量，描述能带/模式的数学算符）。

一个常用的低能形式是：

$$
H
= v_D(k_x\sigma_x\tau_z+k_y\sigma_z\tau_z)
+m_1\tau_x
+m_2\tau_y
+m'\sigma_y\tau_z
$$

其中：

- $k_x,k_y$：momentum terms（动量项），决定 Dirac cone 的线性色散。
- $m_1,m_2,m'$：mass terms（质量项），它们的作用是打开 Dirac 点处的带隙。
- $\sigma_i,\tau_i$：Pauli matrices（泡利矩阵），这里用来表示模式的两个内部自由度；不需要把它理解成真实电子自旋。
- $v_D$：Dirac velocity（Dirac 速度），表示线性色散斜率。

这里的 mass term 不是光子真的有静止质量，而是“能把 Dirac 点打开成带隙的参数”。

### 2. 质量项打开带隙

如果质量项为零，能带在 Dirac 点闭合。

如果质量项非零，能谱相对 Dirac 频率可以近似写成：

$$
E(k)=\pm\sqrt{v_D^2(k_x^2+k_y^2)+m_1^2+m_2^2+m'^2}
$$

所以 $|m|$ 越大，带隙通常越大。但实际光子晶体里不能无限增大调制，因为其他能带会下移、结构会变形，反而破坏目标带隙。

### 3. 手征对称性让零模靠近带隙中心

2020 年论文强调 chiral symmetry（手征对称性）近似保护中隙模。它可以写作：

$$
S=\sigma_y\tau_z
$$

直观理解：手征对称性让 Dirac 频率上下的谱近似镜面对称，因此由拓扑缺陷产生的 zero mode 会被钉在 gap centre（带隙中心）附近。

第三个质量项 $m'\sigma_y\tau_z$ 会破坏这个对称性。真实光子系统工作在非零频率，手征对称性只能近似成立，所以中隙模不一定严格在正中心，但仍然可以稳定存在。

### 4. 两个质量项组成复数 Dirac mass

当 $m'$ 可以近似忽略时，剩下两个质量项组成一个复数：

$$
m=m_1+i m_2=|m|e^{i\theta}
$$

这个复数有两个信息：

- $|m|$：带隙打开的强度。
- $\theta$：带隙的相位方向。

Dirac-vortex 的关键就是让这个相位 $\theta$ 在二维空间中绕中心旋转：

$$
m(r)\propto e^{iw\arg(r)}
$$

其中：

- $r$：相对涡旋中心的位置。
- $\arg(r)$：绕中心的方位角。
- $w$：winding number（绕数），即质量相位绕一圈时转了几圈。

更严格地说，绕数可理解为：

$$
w=\frac{1}{2\pi}\oint \nabla \arg[m(r)]\cdot d\mathbf{l}
$$

它是 topological invariant（拓扑不变量）：只要带隙不关闭、涡旋不被破坏，连续小扰动不会轻易改变它。

## Jackiw-Rossi zero mode

Jackiw-Rossi zero mode 是二维 Dirac 方程在 mass vortex 中出现的零能解。

在光子学里，“zero mode”不是光频率为 0，而是相对 Dirac gap 中心的频率偏移接近 0。它对应一个局域在涡旋中心附近的 topological mid-gap mode（拓扑中隙模）。

物理过程可以按四步理解：

1. 均匀质量项只打开带隙，不产生局域腔模。
2. 质量项相位绕空间中心旋转，形成拓扑缺陷。
3. 涡旋中心处 $|m|$ 必须趋近 0，局部带隙闭合。
4. 这个缺陷核心束缚一个中隙零模。

绕数 $w$ 的含义：

- $|w|$ 决定中隙拓扑模数量。
- $w$ 的正负决定 chirality（手性）。
- 在蜂窝晶格中，手性会表现为场主要落在哪一个 sublattice（子晶格）上。

因此 $w=1$ 通常用于设计单个优先 lasing mode（激光振荡模式）。

## Kekule 调制如何把理论落到结构上

Kekule modulation 原本来自石墨烯/苯环结构中的键强交替图案。在光子晶体中，它不是改变真实化学键，而是移动空气孔或金属孔的位置，让几何扰动等效为 Dirac mass。

### 2020 年硅光子晶体方案

2020 年论文的设计路径是：

1. 从 honeycomb photonic crystal（蜂窝光子晶体）出发。
2. 用六角超胞把 $K/K'$ 点折叠到 $\Gamma$ 点。
3. 移动超胞中三个子晶格空气孔。
4. 位移幅度对应 $|m|$。
5. 位移方向对应 $\arg(m)$。
6. 把不同相位的超胞绕中心排列，得到 $2\pi$ vortex gap（$2\pi$ 涡旋带隙）。

几何位移可以写成：

$$
m=m_0e^{i\phi_0}
$$

它等效于有效模型中的：

$$
m=m_1+i m_2
$$

这就是全文最重要的映射：

> 空气孔位移的幅度和方向 = Dirac 复质量的大小和相位。

### 2024 年 SMDC 方案

2024 年论文保留同一套 Dirac-vortex 理论，但把结构放到 surface metal layer（表面金属层）中。

它的设计路径是：

1. 使用 THz QCL 的 double-metal waveguide（双金属波导）。
2. 在表面金属层中做蜂窝晶格 Dirac-vortex 图案。
3. 不深刻蚀 active region（有源区），避免损伤增益区。
4. 依靠双金属波导的强模式限制，让表面金属图案仍能与有源区充分耦合。
5. 通过连续相位变化从 $0$ 到 $2\pi$ 形成 vortex bandgap（涡旋带隙）。

2024 年论文中，位移向量可以概括为：

$$
\mathbf{m}(r)=m e^{i\theta(r)}
$$

其中 $m$ 是位移幅度，$\theta(r)$ 随绕腔中心的角度连续变化。论文在主文中把它写成含初始相位 $\theta_0$ 和空间角 $\theta_r$ 的简化公式；核心意思仍然是“位移相位围绕中心绕转一圈”。

这篇文章的重要工程结论是：即使 SMDC 的带隙宽度小于深刻蚀有源区的传统拓扑腔，只要有足够耦合和足够 Q 差异，Jackiw-Rossi zero mode 仍可成为优先激射模式。

## 2020 年通用腔参数

2020 年论文用下面的空间调制函数描述 Dirac-vortex cavity：

$$
m(r-r_0;w,m_0,R,\alpha)
=m_0\tanh\left(\left|\frac{r-r_0}{R}\right|^\alpha\right)
e^{i[\phi_0-w\arg(r-r_0)]}
$$

这个公式分成两部分：

- 幅度项：中心 $|m|\approx 0$，远离中心 $|m|\rightarrow m_0$。
- 相位项：绕中心旋转，形成绕数为 $w$ 的质量涡旋。

| 参数 | 中文解释 | 主要物理作用 |
|---|---|---|
| $w$ | winding number（绕数） | 控制中隙模数量和手性；$w=1$ 对应单个拓扑中隙模 |
| $m_0$ | maximum modulation amplitude（最大调制幅度） | 控制带隙大小、势阱深度和辐射耦合强度 |
| $R$ | vortex radius（涡旋半径） | 控制质量项从中心到外侧的变化尺度，决定模式面积 |
| $\alpha$ | shape factor（形状因子） | 控制势阱边缘陡峭程度，影响远场条纹和模式面积 |
| $\phi_0$ | initial phase（初始相位） | 控制整体相位偏置，通常不改变核心拓扑机制 |

注意：$R$ 不是整个器件半径。为了让模式被带隙充分包围，涡旋区外还需要继续铺光子晶体周期。

## 为什么 FSR 异常大

FSR, free spectral range（自由光谱范围）指相邻腔模的频率或波长间隔。单模激光希望 FSR 大，因为旁模更不容易竞争。

传统 Fabry-Perot 腔、回音壁腔或普通 band-edge cavity 中，模式体积 $V$ 增大时：

$$
FSR\propto \frac{1}{V}
$$

二维 Dirac-vortex cavity 中，中隙模位于 Dirac spectrum（Dirac 谱）中心，而 Dirac 点附近 optical density of states（光学态密度）趋近于零，导致中隙模附近的频谱间隔特别大。

论文给出的尺度律是：

$$
FSR\propto \frac{1}{L}\propto\frac{1}{\sqrt{V}}
$$

其中 $L$ 是模式直径，二维模式体积近似随面积 $L^2$ 增大。

这就是 Dirac-vortex cavity 适合大面积单模的核心原因：面积变大时，FSR 下降得比普通腔慢。

零模波函数也能解释模式尺寸：

$$
|\Psi_0(r)|\sim
\exp\left[-\int_0^r |m(r')|dr'\right]
$$

若中心附近：

$$
|m(r)|\sim \left(\frac{r}{R}\right)^\alpha
$$

则模式直径满足：

$$
L\propto R^{\alpha/(\alpha+1)}
$$

例如 $\alpha=4$ 时：

$$
L\propto R^{4/5}
$$

## 2024 年 SMDC 的关键理论继承

2024 年 SMDC 不是提出新的拓扑分类，而是继承 2020 年 Dirac-vortex 理论，并解决电泵浦太赫兹器件中的工程矛盾。

### 继承的理论

- 仍然从蜂窝晶格的 Dirac cone 出发。
- 仍然把 $K/K'$ 折叠到 $\Gamma$ 点，以利于表面出射。
- 仍然用 Kekule 型相位绕转打开 vortex bandgap。
- 仍然依赖 Jackiw-Rossi zero mode 作为优先激射模式。
- 仍然利用 $C_{3v}$ 对称性解释近场和远场的典型形状。

### 改造的工程实现

| 问题 | 传统做法 | SMDC 做法 |
|---|---|---|
| 如何形成足够强的拓扑腔调制 | 深刻蚀有源区，获得高折射率对比 | 只图案化表面金属层 |
| 有源区是否受损 | 有源区被刻蚀，增益减少、侧壁散射增加 | 有源区基本不破坏，保留增益 |
| 模式如何耦合到有源区 | 依靠刻蚀结构本身 | 依靠双金属波导强耦合 |
| 如何抑制普通模式 | 主要靠拓扑带隙和 Q 差异 | 额外加入 absorption boundary（吸收边界）提高普通回音壁模式损耗 |

### 关键数值

2024 年论文给出的几个关键数值：

- 设计频段：约 3.0-3.6 THz。
- 表面金属 Dirac-vortex 腔的模拟带隙宽度：约 3%。
- 典型位移幅度：$m=0.18a$。
- FSR：约 0.03 THz。
- 最大直接测得峰值功率：150 mW。
- 垂直辐射效率：约 47.4%。

其中 $m$ 的作用和 2020 年的 $m_0$ 类似：位移越大，带隙和出射耦合通常越强；但太大又会导致晶格变形和器件退化，所以需要优化。

## 远场图案与相位调控

Dirac-vortex cavity 的远场不是随意产生的，而是由质量相位分布和腔的对称性决定。

2020 年论文指出，在 $C_{3v}$ 对称设计中，singlet cavity mode（单态腔模）与自由空间垂直方向的偏振 doublet（双重态）对称性不匹配，因此会出现 doughnut beam（甜甜圈光束）或矢量光束特征。

2024 年论文进一步利用这一点做 beam shaping（光束整形）：

- 保持拓扑腔基本机制不变。
- 改变 vortex phase distribution（涡旋相位分布）的角向函数。
- 用调制参数 $q$ 把原来的 $C_{3v}$ 远场调成双瓣或甜甜圈图案。
- 远场图案改变时，激光谱和矢量偏振特征基本保持。

这说明 Dirac-vortex 的相位纹理不仅决定“有没有拓扑零模”，也能作为调控出射光束形状的设计自由度。

## 两篇文献的关系

可以按三层关系理解：

1. **理论层**：2020 年建立 Dirac mass vortex $\rightarrow$ Jackiw-Rossi zero mode $\rightarrow$ 2D topological mid-gap cavity 的完整逻辑。
2. **结构层**：2020 年用硅光子晶体空气孔位移实现；2024 年用太赫兹 QCL 表面金属孔阵列实现。
3. **器件层**：2020 年主要验证可扩展单模腔和大 FSR；2024 年证明这套腔可以服务于高功率电泵浦太赫兹拓扑激光。

所以 2024 年论文的理论核心仍来自 2020 年，但它的重要贡献是证明：

> Dirac-vortex 腔不一定必须深刻蚀整个有源区；只要表面波导层与有源区耦合足够强，拓扑零模也可以在非破坏性电泵浦器件中工作。

## 易混概念

| 概念 | 容易误解 | 正确理解 |
|---|---|---|
| mass term（质量项） | 光子有真实静止质量 | 打开 Dirac 点带隙的有效参数 |
| zero mode（零模） | 光频率为 0 | 相对带隙中心频偏接近 0 的模式 |
| vortex（涡旋） | 光场本身一定旋转 | 首先指 Dirac 质量项相位的空间绕转 |
| topological protection（拓扑保护） | 完全不受任何扰动影响 | 在带隙不关闭、关键对称性不严重破坏时，对小扰动更鲁棒 |
| $R$ | 器件外半径 | 质量涡旋过渡尺度，不等于外部光子晶体尺寸 |
| $m_0$ 或 $m$ | 越大越好 | 增大可开大带隙和增强辐射，但过大可能引入其他能带干扰或结构退化 |
| $\Gamma$ 点出射 | 只要折叠到 $\Gamma$ 就高效出光 | 还要考虑 light cone、Q、辐射耦合和器件波导结构 |

## 如果要复现或设计，建议按这个流程

1. 先找一个蜂窝晶格结构，确认存在目标频段的 Dirac cone。
2. 用超胞折叠把 $K/K'$ Dirac 点搬到 $\Gamma$ 点。
3. 通过 Kekule 位移扫描调制幅度，确认 Dirac 点能打开干净带隙。
4. 建立 $m=m_0e^{i\phi}$ 的结构库，确认相位从 $0$ 到 $2\pi$ 都能保持带隙。
5. 选 $w=1$ 构造单模 Dirac vortex。
6. 调 $R$ 控制模式面积，调 $\alpha$ 控制势阱形状和远场质量。
7. 调 $m_0$ 或 $m$ 平衡带隙、Q、出射效率和加工可行性。
8. 检查中隙模是否在 gap 中孤立，FSR 是否足够大。
9. 对激光器件，再检查增益区是否被破坏、模式与增益区重叠、垂直辐射效率和热/电注入条件。

## 我的理解

Dirac-vortex cavity 的核心价值是把“单模选择”从普通几何缺陷问题，变成“二维带隙相位纹理设计”问题。

2020 年论文回答的是：为什么二维光子晶体中可以有一个可放大的拓扑中隙腔模？

2024 年论文回答的是：这种腔模能不能离开理想硅光子晶体平台，进入真实电泵浦半导体激光器？

两者合起来说明：Dirac-vortex 不只是一个漂亮的拓扑模型，它是一种可以在不同波段和不同波导平台中迁移的腔设计方法。

## 相关笔记

- [[10-Research/Topological_Photonics/00-索引]]
- [[10-Research/Topological_Photonics/01]]
- [[02]]
- [[Dirac-vortex topological cavities 精读笔记]]
