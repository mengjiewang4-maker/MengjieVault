# 微纳加工实验记录系统总结（Dirac-vortex / Disclination）

## 1. 核心结论

### 1.1 当前真正需要建立的不是“笔记”，而是“样品数据库”

实验记录必须围绕：

```text
Sample（样品）
```

而不是：

- SEM
    
- ICP
    
- GDS
    
- EBL
    

因为真实科研流程是：

```text
一个样品
↓
经历：
GDS → EBL → ICP → RIE → SEM → Optical
```

最终目标：

实现：

```text
任何 SEM 图
↓
都能反查：
样品
GDS
Python脚本
Dose
PEC
工艺参数
结果
下一步
```

---

### 1.2 微纳加工中“我记得”≈“没记录”

真正决定实验成败的：

往往不是固定标准参数，

而是：

```text
今天和昨天哪里不一样
```

因此：

重点记录：

- Dose变化
    
- PEC变化
    
- 涂胶变化
    
- 显影变化
    
- ICP变化
    
- 去胶变化
    
- SEM观察结果
    

---

### 1.3 超净间推荐工作流

推荐：

```text
纸质实时记录
+
手机拍照归档
+
Obsidian长期数据库
```

其中：

- 纸质本：实时记录变化参数
    
- 手机：拍纸质记录、SEM、设备界面
    
- Obsidian：建立长期实验数据库
    

---

## 2. 方法流程

## 2.1 推荐实验流程

```text
Python生成GDS
↓
Dose Matrix设计
↓
EBL曝光
↓
显影
↓
ICP刻蚀
↓
RIE去胶
↓
SEM观察
↓
记录结果
↓
调整Dose/PEC/GDS
↓
下一轮EBL
```

---

## 2.2 推荐样品管理逻辑

正确结构：

```text
Sample
├── GDS
├── EBL
├── ICP
├── SEM
└── Optical
```

而不是：

```text
SEM/
GDS/
ICP/
```

---

## 2.3 推荐样品命名

推荐格式：

```text
B15_20260522_Si_DiscFig2_EBLICP_S1_OK
```

字段含义：

|字段|含义|
|---|---|
|B15|Batch15|
|20260522|日期|
|Si|基底|
|DiscFig2|结构来源|
|EBLICP|工艺阶段|
|S1|样品编号|
|OK|当前结果|

---

## 2.4 推荐 SEM 文件命名

推荐：

```text
B15_20260522_Si_DiscFig2_a559r0p2n3p4_D90_R01_center_30k_OK_001.tif
```

字段：

|字段|含义|
|---|---|
|Si|基底|
|DiscFig2|结构|
|a559r0p2n3p4|关键参数|
|D90|Dose|
|R01|区域|
|center|SEM位置|
|30k|倍率|
|OK|结果|

---

## 2.5 区域编号逻辑

一个样品上通常有多个版图。

因此建立：

```text
R01
R02
R03
```

对应：

|区域|对应GDS|
|---|---|
|R01|GDS01|
|R02|GDS02|
|R03|GDS03|

目标：

```text
SEM
↓
反查：
区域
↓
GDS
↓
Python
```

---

## 2.6 Dose Matrix 推荐逻辑

推荐：

```text
列 = GDS结构
行 = Dose
```

例如：

|区域|结构|Dose|
|---|---|---|
|A1|GDS01|25|
|A2|GDS01|30|
|A3|GDS01|35|

目标：

```text
SEM
↓
反查：
GDS + Dose
```

---

## 2.7 PEC 推荐逻辑

设备：

JEOL JBX-6300FS

推荐：

```text
PEC ON
+
低剂量Dose Matrix
```

原因：

Disclination 中心区域容易：

- 孔连
    
- 局部过曝
    

---

## 3. 参数

## 3.1 当前样品信息

|项目|内容|
|---|---|
|结构|Disclination cavity|
|文献|Nature Photonics 2024 Fig.2|
|基底|Si|
|样品名|BATCH15_20260522_EBL_ICP_RIE_S1|
|推荐新名|B15_20260522_Si_DiscFig2_EBLICP_S1_OK|

---

## 3.2 GDS 信息

|项目|内容|
|---|---|
|GDS|disclination_a559_r0p2_n3p4_extended_100um.gds|
|Python脚本|dxf_to_gds.py|

---

## 3.3 EBL 参数

|项目|参数|
|---|---|
|Dose|90%|
|PEC|OFF|
|Beam current|2 nA|
|设备|JEOL JBX-6300FS|

---

## 3.4 涂胶参数

|项目|参数|
|---|---|
|胶|AR-P 6200.09|
|旋涂1|500 rpm 5s|
|旋涂2|2000 rpm 60s|
|前烘|150℃ 60s|

---

## 3.5 显影参数

|项目|参数|
|---|---|
|显影液|乙酸乙酯|
|显影时间|60s|
|定影|IPA|

---

## 3.6 后处理

|项目|参数|
|---|---|
|后烘|130℃ 3min|
|RIE去胶|已进行|

---

## 4. 遇到的问题

## 4.1 实验记录混乱

当前问题：

- 不能从样品反查GDS
    
- 不能从SEM反查Python
    
- 文件命名不清晰
    
- 多个版图在一个样品上无法区分
    

---

## 4.2 SEM 文件命名不可追溯

当前：

```text
BATCH15_20260522_EBL_ICP_RIE_S1_P1_1.tif
```

问题：

- 不知道结构
    
- 不知道Dose
    
- 不知道区域
    
- 不知道倍率
    

---

## 4.3 第一轮 EBL 出现过曝

现象：

- 中心区域最严重
    
- 孔连在一起
    

原因：

- PEC OFF
    
- Dose偏高
    
- Disclination 中心密度高
    

---

## 4.4 容易遗忘的信息

最容易忘：

- 涂胶参数
    
- 去胶参数
    
- SEM对应区域
    
- GDS与Python对应关系
    

---

## 5. 下一步

## 5.1 建立正式样品数据库

目标：

```text
任何SEM
↓
反查：
样品
GDS
Python
Dose
PEC
结果
```

---

## 5.2 第二轮 EBL

推荐：

```text
PEC ON
+
低Dose Matrix
```

建议：

|Dose|PEC|
|---|---|
|25%|ON|
|30%|ON|
|35%|ON|
|40%|ON|

---

## 5.3 建立区域映射表

例如：

|区域|GDS|Dose|
|---|---|---|
|R01|GDS01|25|
|R02|GDS01|30|

---

## 5.4 建立正式 SEM 命名系统

目标：

任何文件名都能直接看出：

- 基底
    
- GDS
    
- Dose
    
- 区域
    
- SEM位置
    
- 倍率
    
- 结果
    

---

## 5.5 在 SOI 上制备光学测试样品

下一步：

```text
SOI
↓
EBL
↓
ICP
↓
SEM
↓
Optical test
```

建议样品名：

```text
B16_YYYYMMDD_SOI_DiscFig2_Optical_S1
```

---

## 6. 实验记录核心原则

## 6.1 纸质本

负责：

- 实时参数
    
- 临时变化
    
- 草图
    
- 时间点
    
- 现场观察
    

---

## 6.2 手机

负责：

- 拍纸质本
    
- 拍设备参数
    
- 拍SEM界面
    
- 临时数字归档
    

---

## 6.3 Obsidian

负责：

- 长期数据库
    
- 样品追溯
    
- GDS映射
    
- SEM总结
    
- 工艺总结
    

---

## 6.4 超净间原则

进入超净间：

先写样品名。

离开超净间：

先拍纸质本。

当天晚上：

先整理实验记录。

不要：

```text
“以后再整理”
```

因为：

```text
48小时后基本会忘。
```