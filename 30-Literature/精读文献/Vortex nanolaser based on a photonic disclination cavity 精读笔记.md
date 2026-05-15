---
title: "Vortex nanolaser based on a photonic disclination cavity 精读笔记"
aliases:
  - Vortex nanolaser based on a photonic disclination cavity
  - 光子旋错腔涡旋纳米激光器
tags:
  - paper/on-chip-lasers
  - paper/topological-photonics
  - paper/nanolaser
  - paper/deep-reading
status: first-pass
journal: Nature Photonics
year: 2024
doi: 10.1038/s41566-023-01338-2
official_main_url: "https://www.nature.com/articles/s41566-023-01338-2"
source_pdfs:
  - "90-Local_Not_Upload/PDF/papers/02_on_chip_lasers/Vortex nanolaser based on a photonic.pdf"
  - "90-Local_Not_Upload/PDF/papers/02_on_chip_lasers/SI_Vortex nanolaser based on a photonic disclination cavity.pdf"
created: 2026-05-12
---

# Vortex nanolaser based on a photonic disclination cavity 精读笔记

> [!warning] 文件说明
> 你给出的两个本地 PDF 哈希完全相同，内容都是 Supplementary Information（补充材料），不是主文。主文内容本笔记使用 Nature 官方页面/PDF：<https://www.nature.com/articles/s41566-023-01338-2>。本地 SI 仍用于补充材料精读。

> [!abstract] 一句话总结
> 这篇论文利用 photonic disclination cavity（光子旋错腔）中的拓扑缺陷态实现了 wavelength-scale mode volume（波长量级模式体积）的 vortex nanolaser（涡旋纳米激光器），并通过 Stokes 参数、自干涉和拓扑电荷测量证明其发射具有 orbital angular momentum（轨道角动量）和偏振涡旋特征。

## 论文基本信息

- Title: Vortex nanolaser based on a photonic disclination cavity
- Authors: Sun-Joo Choi, Jong-Woong Yoon, Ki-Young Jeong, Hwan-Gyu Park, Motoki Shiga, Hiroyuki Takahashi, Koichi Takata, Motohiko Ezawa, Zheng Liu, and Shinichi Saito
- Journal: Nature Photonics
- Year: 2024
- DOI: 10.1038/s41566-023-01338-2
- Research field: nanolaser（纳米激光器）, topological photonics（拓扑光子学）, vortex beam（涡旋光束）, higher-order topology（高阶拓扑）
- Keywords: photonic disclination cavity, vortex nanolaser, orbital angular momentum, topological defect state, photonic crystal slab, InGaAsP multiple quantum wells

## 先抓住研究问题

vortex beams（涡旋光束）携带 orbital angular momentum, OAM（轨道角动量），可用于通信、量子信息、光镊、手性光学等方向。已有很多产生 OAM 光束的方法，但如果要在芯片上实现小体积、低阈值、可集成的 vortex laser（涡旋激光器），仍然很困难。

传统涡旋激光器常见问题：

- 器件尺寸偏大，模式体积不够小。
- 需要额外光学元件或复杂腔设计来产生 OAM。
- 多模竞争或偏振态控制困难。
- 很难把涡旋发射、强局域腔模和片上激光集成到同一结构中。

这篇文章要解决的问题是：

> 能否利用拓扑晶体缺陷本身构造一个纳米尺度激光腔，使其自然发射具有涡旋相位和偏振结构的激光？

## 作者解决的核心矛盾

这篇文章的核心矛盾是：

> vortex beam 通常需要空间相位绕转，而 nanolaser 需要强空间局域；如何在小模式体积中同时实现涡旋光场？

作者的答案是 photonic disclination cavity。

disclination（旋错）是晶体中的一种拓扑缺陷，可以理解为把晶格切掉或插入一个扇区后再拼接，导致局部旋转对称性改变。本文利用这种几何拓扑缺陷在 photonic crystal slab（光子晶体薄膜）中产生局域的 defect modes（缺陷模）。这些模式既被限制在纳米腔中，又具有与旋转对称性相关的 angular momentum（角动量）结构，因此能发射涡旋光。

## 与上一篇 Dirac-vortex cavity 的关系

两篇文章都属于“拓扑缺陷腔”，但机制不同：

| 论文 | 缺陷类型 | 主要物理 | 应用目标 |
|---|---|---|---|
| Dirac-vortex topological cavities | Dirac mass vortex（Dirac 质量涡旋） | Jackiw-Rossi zero mode，中隙单模，大 FSR | 大面积单模 PCSEL |
| Vortex nanolaser based on a photonic disclination cavity | disclination（旋错） | 高阶拓扑/旋转对称缺陷态，OAM 发射 | 波长尺度涡旋纳米激光 |

可以把前者理解为“用质量项绕转束缚一个大面积单模腔”，后者理解为“用晶格旋错缺陷束缚一个自带涡旋角动量的小模式体积腔”。

## 核心机制

### 1. Photonic disclination cavity

photonic disclination cavity（光子旋错腔）是在光子晶体中引入 disclination defect（旋错缺陷）形成的腔。

直观理解：

- 普通光子晶体是规则周期阵列。
- 旋错相当于改变中心附近的晶格连接方式或旋转对称性。
- 这种缺陷会在 photonic bandgap（光子带隙）中产生局域态。
- 局域态的角向结构由晶格的旋转对称性约束。

本文重点是 C5 disclination cavity（五重旋转旋错腔）。C5 旋转对称性会限制模式的 angular momentum $l$，并影响远场涡旋结构。

### 2. Disclination state 与 higher-order topology

作者把 disclination cavity 的缺陷模与 higher-order topological insulator, HOTI（高阶拓扑绝缘体）中的 corner/disclination states 联系起来。

高阶拓扑的常见特点是：

- 2D 体相不一定有 1D 边界态，但可以有 0D corner states（角态）。
- 在具有旋转对称性的拓扑晶体中，disclination defect 可以绑定 fractional disclination charge（分数旋错电荷）。
- 即使 chiral symmetry（手征对称性）不存在，中隙态仍可通过 filling anomaly（填充异常）体现拓扑来源。

这也是 SI Note 2 的重点：没有手征对称性时，中隙态不一定钉在 gap 中心，但仍可调到带隙中并保持拓扑特征。

### 3. 为什么会发射 vortex beam

vortex beam（涡旋光束）通常具有绕中心变化的相位：

$$
E \sim e^{i l\phi}
$$

其中 $l$ 是 topological charge（拓扑荷）或 OAM 模式阶数。

在本文中，光子晶体薄膜中的 $H_z$ 模式可按角向多极展开：

$$
H_z(r,\phi)=\sum_m f_m(r)e^{im\phi}
$$

如果结构有 $C_n$ 旋转对称性，允许的角向分量满足：

$$
m=l+qn
$$

其中 $q$ 是整数。这意味着腔模的角动量不是任意的，而是由离散旋转对称性选择。

SI Note 1 进一步说明：薄膜中的 $H_z$ 模式通过 Maxwell curl equations（麦克斯韦旋度方程）转化为面内电场 $E_x,E_y$，在 circular polarization basis（圆偏振基）中会出现 $e^{\pm i\phi}$ 相位因子，从而形成 polarization vortex（偏振涡旋）和 OAM 发射。

## 主文图表精读

### Fig. 1：概念和结构

Fig. 1 的主要作用是介绍 photonic disclination cavity 的设计思想。

读图路线：

1. 看光子晶体如何形成旋错缺陷。
2. 看缺陷如何产生局域模式。
3. 看该局域模式如何与远场 vortex emission（涡旋发射）联系。
4. 关注器件材料：InGaAsP multiple quantum wells（多量子阱）提供增益，薄膜光子晶体提供腔和拓扑缺陷。

这一图要回答的问题是：

> 这个涡旋激光不是通过外部相位板产生，而是由纳米腔本征模式直接发射。

### Fig. 2：拓扑模型和 disclination defect states

Fig. 2 主要解释 C5 disclination cavity 中为什么会有局域 in-gap states（带隙内态）。

关键点：

- 结构具有旋转对称性。
- 通过 tight-binding model（紧束缚模型）或光子晶体模拟，可以看到 disclination defect 处出现局域态。
- 这些态与 HOTI 的 filling anomaly 和 fractional disclination charge 有关。
- 缺陷态的能量可通过边界设计或耦合参数调节到 bandgap 内。

这部分是全文的理论基础。

### Fig. 3：腔模和激光特性

Fig. 3 通常对应样品和激光行为：

- SEM 或结构图展示实际加工的 disclination cavity。
- 光谱随泵浦功率变化，显示 lasing peak（激光峰）。
- L-L curve（输入输出曲线）显示 threshold（阈值）。
- linewidth narrowing（线宽变窄）证明从自发辐射进入激光振荡。

本图的核心是证明：

> disclination cavity 不是只有被动共振，而是可以在增益材料中实现纳米激光。

### Fig. 4：OAM 与自干涉验证

涡旋光束不能只看 doughnut-shaped intensity（甜甜圈强度分布），因为普通矢量光束也可能出现中心暗斑。作者需要证明相位真的绕转。

常用证据是 self-interference（自干涉）：

- 把同一束涡旋光分成两路。
- 让两束光偏心重叠。
- 如果具有 OAM，会出现 fork-shaped fringes（叉形干涉条纹）。

SI Supplementary Fig. 2 给出 off-center self-interference setup（偏心自干涉测量装置），说明作者如何验证涡旋性质。

### Fig. 5：Stokes 参数与偏振涡旋

Fig. 5 重点是测量 Stokes parameters（斯托克斯参数）来重建偏振态。

Stokes 参数用于描述偏振：

- $S_0$：总强度。
- $S_1$：水平/垂直线偏振差。
- $S_2$：$45^\circ/-45^\circ$ 线偏振差。
- $S_3$：右旋/左旋圆偏振差。

SI Supplementary Fig. 1 中的 intra-modal phase（模内相位）用：

$$
\arctan(S_3/S_2)
$$

计算，用来分析模式内部偏振相位结构。

Fig. 5 的作用是证明：

> 激光发射不仅有强度涡旋，还具有可测量的偏振/相位绕转结构。

## SI 精读

### Supplementary Fig. 1：Intra-modal phase

图注说明，intra-modal phases 由主文 Figs. 5a、5b、5c 中测得的 Stokes 参数计算：

$$
\arctan(S_3/S_2)
$$

这用于进一步确认模式内部的相位结构。

### Supplementary Fig. 2：Off-center self-interference setup

这个图解释如何测 OAM。

实验逻辑：

1. 用 beam splitter（分束器）把同一束 doughnut-shaped lasing emission 分成两路。
2. 通过 mirrors（反射镜）调整光路和中心位置。
3. 让两束偏心重叠。
4. 观察 fork-shaped fringes（叉形条纹）。

叉形条纹是涡旋相位的典型证据。

### Supplementary Table 1：与其他涡旋纳米/微激光器比较

该表比较本文 photonic disclination nanolaser 与其他 vortex nano-/microlasers。

比较维度通常包括：

- device footprint（器件尺寸）
- mode volume（模式体积）
- threshold（阈值）
- OAM/topological charge（拓扑荷）
- 是否片上集成
- 是否需要额外光学元件

本文的优势是把 vortex emission 和 wavelength-scale cavity 结合在一个拓扑缺陷纳米腔里。

### Supplementary Note 1：光子晶体薄膜模式分析

这一节从 Maxwell equations（麦克斯韦方程）出发，说明 quasi-2D photonic crystal slab（准二维光子晶体薄膜）中的模式可分为：

- TM modes：非零分量为 $(H_x,H_y,E_z)$。
- TE modes：非零分量为 $(E_x,E_y,H_z)$。

本文主要分析 TE modes，用 $H_z(x,y)$ 描述。

接着作者把 $H_z$ 按圆柱坐标多极展开：

$$
H_z(r,\phi)=\sum_m f_m(r)e^{im\phi}
$$

在 $C_n$ 旋转对称下，角向分量满足：

$$
m=l+qn
$$

这说明模式角动量 $l$ 与结构对称性绑定。

然后用 Maxwell 旋度方程把 $H_z$ 转成电场，在圆偏振基下得到左右旋圆偏振分量。对 $l=0$ 的模式，电场可形成 polarization vortex；对非零 $l$ 的模式，尤其 $|l|=2$，可以复现 hybrid modes（混合模式）结构。

最后作者解释 slab 内模式和 emitted field（出射场）不同：薄膜内 $H_z$ 可能主要呈三重对称，即 $|l|=3$，但由于 C5 对称性会耦合 $l$ 与 $l\pm5$，所以可在出射场中看到等效的 $|l|=2$ quadrupole mode（四极模式）特征。

### Supplementary Note 2：Disclination states 的能量可调性

这一节回答一个重要问题：

> 没有 chiral symmetry 时，拓扑 in-gap modes 不在 gap 中心，它们还算拓扑态吗？

作者的回答是：算。原因是高阶拓扑相的特征可以通过 filling anomaly 和 fractional disclination charge 体现，而不完全依赖中隙态是否钉在 gap 正中心。

具体论证：

- 在 Cn 对称的 HOTI 中，旋转拓扑不变量可导致 fractional corner/disclination charges。
- 即使 NNN coupling（次近邻耦合）破坏 chiral symmetry，使能谱不对称，edge/corner/disclination topological states 仍可存在。
- Tight-binding simulation 显示，改变 $t_2/t_1$ 可以把 $|l|=0,1,2$ 的 disclination modes 在 bulk gap 中移动。
- 改变 boundary hopping parameter $t_w'$ 也可以调节 in-gap states 的能量和简并情况。

工程含义：

> 通过改变旋错边界附近空气孔大小或等效耦合，可以把拓扑缺陷态调到适合激光的频率位置。

## 术语表

| Term | 中文解释 | 在本文中的作用 |
|---|---|---|
| vortex beam | 涡旋光束 | 携带 OAM 的输出光 |
| orbital angular momentum, OAM | 轨道角动量 | 光场相位绕转对应的角动量 |
| topological charge | 拓扑荷 | 相位绕转阶数 |
| disclination | 旋错 | 通过移除/插入晶格扇区形成的拓扑缺陷 |
| photonic disclination cavity | 光子旋错腔 | 本文纳米激光腔 |
| higher-order topological insulator, HOTI | 高阶拓扑绝缘体 | 提供角态/缺陷态理论背景 |
| filling anomaly | 填充异常 | 表征高阶拓扑相的一种方式 |
| fractional disclination charge | 分数旋错电荷 | 旋错缺陷处的拓扑特征 |
| Stokes parameters | 斯托克斯参数 | 测量偏振态 |
| self-interference | 自干涉 | 验证涡旋相位 |
| fork-shaped fringes | 叉形干涉条纹 | OAM 的实验特征 |

## 最容易误解的点

1. doughnut intensity（甜甜圈强度）本身不能证明 OAM；必须看相位或干涉。
2. 没有 chiral symmetry 不代表没有拓扑态；只是中隙态不一定钉在 gap 中心。
3. disclination cavity 不是普通缺陷孔腔，而是利用晶格旋转拓扑缺陷形成局域态。
4. 出射场的 OAM/偏振结构不一定和薄膜内 $H_z$ 的最高对称分量一一对应，因为远场辐射会优先耦合较低阶多极。
5. 本文实现的是纳米涡旋激光器，不是大面积 PCSEL；它与 Dirac-vortex cavity 的目标不同。

## 对片上激光研究的启发

- 拓扑缺陷可以同时承担“模式局域”和“波前结构设计”两个角色。
- 纳米激光器不一定只能追求小模式体积，也可以把输出光的 OAM/偏振态作为核心功能。
- 旋错缺陷提供了一条不同于边界态、角态、质量涡旋的拓扑腔路线。
- 如果后续关注片上 OAM 光源，这篇文章比传统微环 OAM 激光器更接近纳米尺度集成。

## 建议精读顺序

1. 先读主文引言，理解为什么需要片上 vortex nanolaser。
2. 读 Fig. 1，弄清 photonic disclination cavity 的几何结构。
3. 读 Fig. 2 和 SI Note 2，理解 disclination states 的拓扑来源和能量可调。
4. 读 Fig. 3，确认纳米激光证据：阈值、光谱、线宽。
5. 读 Fig. 4 和 SI Fig. 2，理解 OAM 如何通过自干涉验证。
6. 读 Fig. 5 和 SI Fig. 1，理解 Stokes 参数如何证明偏振涡旋。
7. 最后读 SI Note 1，建立 $H_z$ 多极展开、角动量和远场发射之间的数学联系。

## 读完后的总判断

这篇论文的核心贡献是：

> 它把高阶拓扑/旋错缺陷态引入纳米激光腔设计，使腔的局域模式天然携带涡旋光场结构，从而在波长量级模式体积中实现片上 vortex nanolaser。

它和 Dirac-vortex cavity 共同说明：拓扑光子学的价值不只在“抗散射传输”，还可以转化为主动器件中的模式选择、模式局域和波前工程。
