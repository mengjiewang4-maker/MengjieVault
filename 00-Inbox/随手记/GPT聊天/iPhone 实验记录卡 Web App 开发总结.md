

## 1. 核心结论

本次工作的核心目标，是将普通实验笔记升级为：

「微纳加工 + SEM + 光学测试 + GDS/仿真 + 样品追踪」  
一体化实验记录系统。

当前阶段重点：

- 超净间加工记录
    
- SEM 图像记录
    

最终方向：  
逐步发展成完整实验数据库。

核心设计思想：

1. 手机优先
    

- iPhone Safari
    
- 单手操作
    
- 现场快速记录
    

2. 少输入
    

- 短句填空
    
- 下拉菜单
    
- 快捷按钮
    
- 自动生成编号
    

3. 数据结构化
    

- 不再只是 Markdown
    
- 使用 JSON 保存
    
- 为未来数据库迁移做准备
    

4. 样品全生命周期追踪  
    实现：
    

加工 → SEM → 光测 → 仿真 → 复盘  
完整关联。

---

# 2. 方法流程

## 阶段1：原型阶段

首先构建：

lab_record_card.html

功能：

- 基础表单
    
- Markdown生成
    
- localStorage保存
    
- Obsidian复制
    

目标：  
验证手机实验记录流程是否可行。

---

## 阶段2：iPhone Web App 化

升级方向：

- Safari打开
    
- 添加到主屏幕
    
- 类 App 操作体验
    

解决：  
iPhone 本地 HTML 打开不稳定问题。

最终方案：

- GitHub Pages
    
- Safari 网页入口
    

---

## 阶段3：功能模块化

首页改为：

功能入口页。

包含：

- 加工记录
    
- SEM记录
    
- 光学测试
    
- GDS/仿真
    
- 问题复盘
    
- 今日待办
    
- 历史记录
    

而不是：  
一个超大表单。

---

## 阶段4：样品编号系统

建立统一命名规则：

B16_20260522_SOI_DicFig2_EBL3_ICP90S_RIE4min_S1_P2S70__003

实现：

- 自动生成编号
    
- 自动拆解字段
    
- 自动生成 SEM 文件名
    
- 自动递增 SEM 图片编号
    

---

## 阶段5：数据库化设计

数据不再只保存 Markdown。

改为：

JSON结构。

每条记录包含：

- batch
    
- substrate
    
- pattern
    
- ebl_mode
    
- icp_time
    
- rie_time
    
- sample
    
- array
    
- dose
    
- sem_index
    
- observation
    
- abnormal
    
- timestamp
    

为未来迁移：

- SQLite
    
- Firebase
    
- Supabase
    
- Notion API
    
- Obsidian Dataview
    

做准备。

---

# 3. 参数

## 当前样品编号规则

格式：

B16_20260522_SOI_DicFig2_EBL3_ICP90S_RIE4min_S1_P2S70__003

字段：

|字段|含义|
|---|---|
|B16|第16批次|
|20260522|日期|
|SOI|基底|
|DicFig2|图案|
|EBL3|EBL模式|
|ICP90S|ICP时间|
|RIE4min|RIE时间|
|S1|样品编号|
|P2|阵列编号|
|S70|剂量|
|003|SEM图片编号|

---

## 当前技术路线

前端：

- HTML
    
- CSS
    
- JavaScript
    

存储：

- localStorage
    
- JSON结构
    

平台：

- iPhone Safari
    
- GitHub Pages
    

风格：

- Apple
    
- Notion
    
- Linear
    

---

## 当前核心页面

1. 首页
    
2. 加工记录
    
3. SEM记录
    
4. 今日待办
    
5. 历史记录
    

---

# 4. 遇到的问题

## 1. iPhone 无法直接打开 HTML

问题：  
本地 `.html` 文件在 iPhone 中无法稳定调用 Safari。

解决：  
改用：  
GitHub Pages 部署。

---

## 2. 现场输入太多

问题：  
实验室里无法长时间打字。

解决：

- 短句填空
    
- 快捷按钮
    
- 下拉菜单
    
- 自动编号
    

---

## 3. SEM 图片难追踪

问题：  
SEM 图片容易混乱。

解决：  
统一：  
样品编号 + SEM序号。

实现：  
自动递增编号。

---

## 4. Markdown 不够结构化

问题：  
后期难数据库化。

解决：  
使用 JSON 保存。

Markdown仅作为导出格式。

---

## 5. 单一大表单太复杂

问题：  
操作负担大。

解决：  
改成：  
模块化入口页。

---

# 5. 下一步

## 第一阶段（当前）

完成：

- 首页
    
- 加工记录
    
- SEM记录
    
- Markdown导出
    
- JSON保存
    

---

## 第二阶段

增加：

- SEM连续记录模式
    
- 图片关联
    
- 自动统计
    
- 历史筛选
    

---

## 第三阶段

增加：

- 光学测试模块
    
- GDS关联
    
- COMSOL关联
    
- Python脚本关联
    

---

## 第四阶段

数据库升级：

- SQLite
    
- Supabase
    
- Firebase
    

实现：

实验数据库系统。

---

## 第五阶段

未来方向：

建立：

「拓扑光子实验数据平台」

实现：

- 样品生命周期管理
    
- 工艺版本管理
    
- 图像数据库
    
- 实验统计
    
- 参数回溯
    
- 自动生成实验报告
    

---

# 6. Obsidian 标签建议

tags:

- lab-record
    
- sem
    
- nanofabrication
    
- topology-photonics
    
- obsidian
    
- iphone-webapp
    
- experiment-database
    
- process-management
    

---

# 7. 推荐文件结构

Lab_Record_System/  
├── index.html  
├── README.md  
├── data/  
├── exports/  
├── attachments/  
├── sem/  
├── process/  
├── optical/  
└── backup/

---

# 8. 一句话总结

本次工作的本质：

不是做“实验笔记”。

而是在搭建：

「微纳实验全流程数字化管理系统」。