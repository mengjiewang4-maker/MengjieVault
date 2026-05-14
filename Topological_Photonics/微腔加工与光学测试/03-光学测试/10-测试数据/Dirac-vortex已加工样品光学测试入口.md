---
title: Dirac-vortex已加工样品光学测试入口
date: 2026-05-14
tags:
  - Dirac-vortex
  - 光学测试
  - Q
  - FSR
  - 待测
---

# Dirac-vortex 已加工样品光学测试入口

## 当前状态

Dirac-vortex 样品已经加工完成，当前优先任务是光学测试。测试目标是复现或对齐 Gao et al. `Dirac-vortex topological cavities` 中 Fig. 5 的证据链。

## 测试主线

```text
样品定位 → SEM核对 → 粗扫找共振 → 细扫拟合Q → 计算FSR → 拍近场/远场 → 偏振和背景对照 → 汇报图
```

## 测试目标

1. 找到设计波段附近可重复的共振峰或共振谷。
2. 提取共振中心 $\lambda_0$、线宽 $\Delta\lambda$ 和 Q。
3. 测同一腔内相邻模式，计算 FSR。
4. 在共振波长处拍近场，判断是否局域在 vortex core。
5. 拍远场或后焦面图样，检查是否符合 Dirac-vortex 模式特征。
6. 做偏振分辨测试，记录不同偏振角下的图样变化。
7. 做无腔区、离共振波长和背景对照。

## 待测样品表

| 器件编号 | 样品批次 | $w$ | $m_0$ | $R$ | $\alpha$ | $a$ | SEM状态 | 测试状态 |
|---|---|---:|---:|---:|---:|---:|---|---|
| 待补 | 待补 |  |  |  |  |  | 待补 | 待测 |

## 每次测试记录模板

- 测试日期：
- 测试人：
- 器件编号：
- 样品批次：
- GDS 文件：
- SEM 记录：
- 显微镜坐标：
- 激光器型号：
- 扫描范围：
- 粗扫步进：
- 细扫步进：
- 输入功率：
- 偏振角：
- 探测通道：
- 原始光谱文件：
- 背景光谱文件：
- 近场图片：
- 远场图片：
- 初步判断：

## 推荐数据命名

```text
DV-DISC-YYYY-NNN_spectrum_raw_YYYYMMDD_run01.csv
DV-DISC-YYYY-NNN_spectrum_bg_YYYYMMDD.csv
DV-DISC-YYYY-NNN_fit_Q_FSR_YYYYMMDD.md
DV-DISC-YYYY-NNN_nearfield_onres_YYYYMMDD.png
DV-DISC-YYYY-NNN_nearfield_offres_YYYYMMDD.png
DV-DISC-YYYY-NNN_farfield_pol000_YYYYMMDD.png
```

## 分析入口

- [[微腔加工与光学测试/03-光学测试/01-测试平台搭建/Dirac-vortex光学测试判据总结|Dirac-vortex 光学测试判据总结]]
- [[微腔加工与光学测试/05-数据分析/光谱分析/Q与FSR数据处理入口|Q与FSR数据处理入口]]
- [[02]]
- [[微腔加工与光学测试/templates/光学测试记录模板|光学测试记录模板]]
- [[微腔加工与光学测试/templates/数据分析记录模板|数据分析记录模板]]

## 判断边界

一个共振峰或共振谷只能说明“有候选模式”。要说它是 Dirac-vortex 腔模，需要同时有：

- 器件位置和 GDS 对得上；
- SEM 显示结构可测；
- 重复扫描可复现；
- 背景区没有同样峰；
- 共振处近场比离共振更局域；
- 远场或偏振图样与预期一致；
- Q 和 FSR 的数量级合理。
