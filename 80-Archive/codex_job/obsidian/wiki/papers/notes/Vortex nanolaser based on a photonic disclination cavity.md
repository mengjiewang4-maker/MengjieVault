---
title: Vortex nanolaser based on a photonic disclination cavity
type: source
status: draft
created: 2026-04-22
updated: 2026-04-22
tags:
  - literature
  - source
  - paper
  - topological-photonics
related:
  - "[[Vortex nanolaser based on a photonic disclination cavity - MOC]]"
  - "[[TB-to-photonic mapping]]"
  - "[[Angular momentum labeling in TB]]"
  - "[[Photonic disclination cavity]]"
  - "[[Modified disclination boundary]]"
  - "[[3D FEM eigenmode and Q analysis]]"
  - "[[Experimental verification of vortex nanolasing]]"
citekey: "vortex_2"
authors: []
year: 
journal: 
doi: 
zotero: 
related_concepts:
  - "[[TB-to-photonic mapping]]"
  - "[[Angular momentum labeling in TB]]"
  - "[[Photonic disclination cavity]]"
  - "[[Modified disclination boundary]]"
  - "[[vortex_2 - concept - Photonic disclination cavity 光子旋错腔|Photonic disclination cavity 光子旋错腔]]"
  - "[[vortex_2 - concept - Higher-order topology 高阶拓扑|Higher-order topology 高阶拓扑]]"
  - "[[vortex_2 - concept - Angular momentum l 角动量量子数|Angular momentum l 角动量量子数]]"
  - "[[vortex_2 - concept - TB probability density 紧束缚概率密度|TB probability density 紧束缚概率密度]]"
  - "[[vortex_2 - concept - FEM optical field profile 有限元光学场分布|FEM optical field profile 有限元光学场分布]]"
  - "[[vortex_2 - concept - Disclination bound states 旋错束缚态|Disclination bound states 旋错束缚态]]"
  - "[[vortex_2 - concept - Bandgap localized modes 带隙局域模|Bandgap localized modes 带隙局域模]]"
---

# Vortex nanolaser based on a photonic disclination cavity

## Source

- PDF: [[obsidian/raw/papers/Vortex nanolaser based on a photonic.pdf|Vortex nanolaser based on a photonic.pdf]]
- Existing source note: [[Vortex nanolaser based on a photonic-unknown-Vortex nanolaser based on a photonic]]

## Linked Structure

- MOC: [[Vortex nanolaser based on a photonic disclination cavity - MOC]]
- Concepts:
  - [[TB-to-photonic mapping]]
  - [[Angular momentum labeling in TB]]
  - [[Photonic disclination cavity]]
  - [[Modified disclination boundary]]
- Methods:
  - [[3D FEM eigenmode and Q analysis]]
- Experiments:
  - [[Experimental verification of vortex nanolasing]]

## Zotero Notes

## 可拆分知识点

### Insights

- Photonic disclination cavity 的核心判断是：晶格角缺陷会把高阶拓扑边界信息压缩成带隙内局域模，而不是只制造普通几何缺陷模
- 判断 disclination bound states 是否可用于纳米激光，应优先检查其是否位于 bulk bandgap 内、是否空间局域、是否能被光学模式继承
- Angular momentum l 可以作为连接 TB 本征态、FEM 光场模式与实验发射态的统一标签
- Fig.1 到 Fig.2 的可复用逻辑是：先用旋错构造破坏角点周期性，再用 higher-order topology 预测带隙局域态，最后用 TB probability density 与 FEM optical field profile 验证模式对应
- TB probability density 与 FEM optical field profile 若在对称性、局域中心和 angular momentum l 上一致，就可以把抽象拓扑束缚态解释为可实现的光学腔模
- Bandgap localized modes 的价值不只在局域增强，还在于它们把模式频率从体带中分离出来，降低与扩展态混合的风险

### Concepts

- Photonic disclination cavity 光子旋错腔
- Higher-order topology 高阶拓扑
- Angular momentum l 角动量量子数
- TB probability density 紧束缚概率密度
- FEM optical field profile 有限元光学场分布
- Disclination bound states 旋错束缚态
- Bandgap localized modes 带隙局域模

### Models

- Fig.1 的 disclination 构造模型：从规则光子晶格移除或插入角扇区，将 C6 对称结构映射为 C5/C7 型角缺陷
- Higher-order topology 到 disclination bound states 的判据模型：用 bulk bandgap 与角缺陷拓扑响应判断是否出现带隙内局域态
- Angular momentum l 分类模型：用旋错中心周围相位绕转与对称性表示标记 l=0,1,2 等局域模式
- TB probability density 到 FEM optical field profile 的映射模型：用 TB 本征态的概率密度预测光学模式的空间局域与角向节点
- Bandgap localized modes 的腔模筛选模型：优先选择位于带隙中、远离体带且具有明确 l 标签的局域态作为激光候选模式

### Figures

- Fig2(a/d/g): 能级图，展示旋错束缚态在带隙中的位置及角动量分类
- Fig2(b/e/h): TB 计算的概率密度分布，展示不同 l 模式的空间局域性
- Fig2(c/f/i): 光学 FEM 模拟场分布，展示 TB 模式到光学模式的对应关系
- Fig1: 光子晶格旋错构造示意，给出从拓扑晶格到 photonic disclination cavity 的几何起点
- Fig1 → Fig2: 从角缺陷构造到带隙局域模验证的逻辑链条，连接 topology、TB eigenstates 与 optical cavity modes

### Methods

- 先从 Fig.1 识别 disclination 的几何操作、剩余旋转对称性和缺陷中心，再预测可能的 angular momentum l 分类
- 在 TB 模型中计算含旋错晶格的能谱，筛选位于 bandgap 中的 disclination bound states
- 对每个带隙局域态提取 TB probability density，判断其是否围绕旋错中心稳定局域
- 对相同结构进行 FEM 光学仿真，比较 FEM optical field profile 与 TB probability density 的空间分布和 l 标签
- 用 Fig2(a/d/g) 的能级位置、Fig2(b/e/h) 的 TB 局域性和 Fig2(c/f/i) 的 FEM 场分布共同确认 TB → optical mode 的对应关系
