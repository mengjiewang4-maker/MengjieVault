# iPhone 实验记录卡 Web App

这是一个面向微纳加工现场的轻量实验数据库雏形。它部署在 GitHub Pages 上，用 iPhone Safari 打开后可以添加到主屏幕，像一个小 App 一样使用。

当前重点服务：

- 超净间加工记录
- SEM 记录
- 每个加工步骤的拍照/选图入口
- 样品编号和 SEM 文件名追踪
- Obsidian Markdown 导出
- JSON 备份

光学测试、GDS/仿真、问题复盘目前作为扩展入口保留。

## 访问地址

GitHub Pages 地址：

```text
https://mengjiewang4-maker.github.io/MengjieVault/100-app/
```

GitHub 仓库：

```text
https://github.com/mengjiewang4-maker/MengjieVault
```

## iPhone Safari 如何打开

1. 在 iPhone 上打开 Safari。
2. 输入：

```text
https://mengjiewang4-maker.github.io/MengjieVault/100-app/
```

3. 页面打开后，先进入“加工记录”或“SEM记录”测试一条记录。

说明：Safari 是苹果手机自带浏览器。这个 App 不依赖外部库，数据默认保存在手机浏览器本机。

## 如何添加到主屏幕

1. 用 iPhone Safari 打开 GitHub Pages 地址。
2. 点击底部分享按钮。
3. 选择“添加到主屏幕”。
4. 名称可以改成“实验记录卡”。
5. 之后从主屏幕打开，界面会更像轻量 App。

建议固定使用同一个入口记录实验。因为本机数据保存在浏览器 `localStorage` 中，换浏览器或清理 Safari 网站数据可能会清掉历史记录。

## 样品和 SEM 文件名规则

当前规则示例：

```text
B16_20260522_SOI_DicFig2_EBL3_ICP90S_RIE4min_S1_P2S70__003
```

字段含义：

| 字段 | 含义 |
|---|---|
| `B16` | 第 16 批次 |
| `20260522` | 日期 |
| `SOI` / `Si` | 基底类型 |
| `DicFig2` / `Dirac` / `Disclination` | 图案类型 |
| `EBL3` / `EBL6` | EBL 模式 |
| `ICP90S` | ICP 刻蚀时间 |
| `RIE4min` | RIE 去胶或刻蚀时间 |
| `S1` / `S2` | 样品编号 |
| `P2` | 图案阵列编号 |
| `S70` | 剂量，例如 70% |
| `003` | SEM 图片编号 |

App 支持：

- 自动生成样品编号
- 自动拆解已有编号
- SEM 图片编号自动递增
- 自动生成完整 SEM 图片文件名

## 如何记录加工

1. 首页点击“加工记录”。
2. 填写批次、日期、基底、图案、EBL 模式、ICP 时间、RIE 时间、样品、阵列和剂量。
3. 如果同一批次做了多个样品，样品编号可以写成 `S1-S2-S3`。
4. 查看“样品编号预览”，确认每个样品编号是否正确。
4. 用短句填写：
   - 今天做了什么
   - 观察结果
   - 现场异常
   - 下一步
5. 用短句填写：
   - 今天做了什么
   - 观察结果
   - 现场异常
   - 下一步
6. 可选填写照片编号范围，例如 `2381` 到 `2388`，自动生成 `IMG_2381-IMG_2388`。
7. 点击底部“保存”。

如果样品编号写的是 `S1-S2-S3`，保存后会自动生成 3 条加工记录，每条记录都有独立样品编号和 Markdown。

## 如何在每个加工步骤拍照

“加工记录”页面里，每个关键步骤都有独立拍照入口：

1. 基底处理
2. 旋涂/前烘
3. EBL曝光
4. 显影/定影
5. ICP刻蚀
6. RIE去胶
7. 绿光显微镜检查
8. SEM前样品状态

在 iPhone Safari 中点击某个步骤下的“选择文件/拍照”控件，可以调起相机或相册。建议现场这样用：

1. 每完成一个步骤，马上在对应步骤下拍照。
2. 在照片说明里写一句短说明，例如 `ICP 参数页，HBr 50sccm，90S`。
3. 不要把照片原图长期依赖浏览器保存，原图仍以 iPhone 相册为准。
4. App 会保存照片文件名、步骤名和说明，并写进 JSON 和 Markdown。

这样后续回看时，可以知道每张现场照片对应哪一步工艺。

## 如何记录 SEM

1. 首页点击“SEM记录”。
2. 从“选择已有样品”中选择加工记录保存过的样品，或手动输入样品编号。
3. 填写 SEM 图片编号，例如 `001`。
4. App 自动生成完整 SEM 文件名，例如：

```text
B16_20260522_SOI_DicFig2_EBL3_ICP90S_RIE4min_S1_P2S70__001
```

5. 填写放大倍率、加速电压、工作距离、拍摄区域、图片说明。
6. 标记是否异常、是否需要重加工。
7. 点击底部“保存”。

每张 SEM 图都会保存为独立 JSON 记录，并关联到样品编号。

## 如何连续记录 SEM 图片

连续拍摄时推荐流程：

1. 先选择或输入样品编号。
2. 填写第一张 SEM 编号，例如 `001`。
3. 填写本张图片说明。
4. 点击“保存”。
5. 点击“下一张”，编号会自动变为 `002`。
6. 修改拍摄区域和图片说明。
7. 再次点击“保存”。

这样可以快速得到：

```text
...__001
...__002
...__003
```

每一张图都有独立记录，后续搜索和导出更方便。

## 如何导出 Markdown 到 Obsidian

1. 进入“历史记录”。
2. 点击某条记录。
3. 点击“复制 Markdown”。
4. 打开 Obsidian，新建笔记并粘贴。

也可以点击“导出当前 .md”，得到单条 Markdown 文件。

导出文件名格式：

```text
YYYYMMDD_样品编号_记录类型.md
```

Markdown 会包含 frontmatter，方便后续用 Obsidian Dataview 查询。frontmatter 是 Markdown 顶部的结构化信息区。

## 如何备份 JSON

1. 进入“历史记录”。
2. 点击“导出 JSON 备份”。
3. 保存生成的 `.json` 文件。

JSON 是结构化数据格式，适合未来迁移到 SQLite、Supabase、Firebase、Notion API 或 Obsidian Dataview。

建议：每次重要实验结束后，同时导出 Markdown 和 JSON。

## 历史记录搜索和筛选

历史记录支持按以下字段筛选：

- 批次
- 日期
- 样品
- 图案类型
- EBL 模式
- ICP 时间
- RIE 时间
- 剂量
- SEM 编号
- 是否异常
- 记录类型

点击历史记录可查看详情、复制 Markdown、导出当前 `.md`、导出全部 `.md`、导出 JSON 备份。

清空本机记录需要二次确认。

## 数据结构说明

每条记录以 JSON 对象保存，核心字段如下：

```json
{
  "id": "rec_xxx",
  "type": "加工记录",
  "batch": "B16",
  "date": "20260522",
  "substrate": "SOI",
  "pattern": "DicFig2",
  "ebl_mode": "EBL3",
  "icp_time": "ICP90S",
  "rie_time": "RIE4min",
  "sample": "S1",
  "array": "P2",
  "dose": "S70",
  "sem_index": "003",
  "sample_id": "B16_20260522_SOI_DicFig2_EBL3_ICP90S_RIE4min_S1_P2S70",
  "sem_filename": "B16_20260522_SOI_DicFig2_EBL3_ICP90S_RIE4min_S1_P2S70__003",
  "operation": "完成 EBL 曝光、ICP 90S、RIE 去胶",
  "observation": "孔阵列完整，疑似残胶薄膜",
  "abnormal": "否",
  "need_rework": "否",
  "next_step": "继续拍 SEM 或进入光学测试",
  "photo_range": "IMG_2381-IMG_2388",
  "photo_note": "iPhone 拍屏范围",
  "step_photos": [
    {
      "step": "ICP刻蚀",
      "files": "IMG_2381.jpeg, IMG_2382.jpeg",
      "note": "ICP 参数页，90S"
    }
  ],
  "markdown": "...",
  "timestamp": "2026-05-27T..."
}
```

这些字段保留了未来数据库化需要的主键、类型、样品编号、SEM 文件名、工艺参数、观察、异常判断和导出文本。

## 未来数据库升级建议

当前版本使用 `localStorage`。`localStorage` 是浏览器本地小数据库，适合快速原型，但不适合长期唯一备份。

未来可升级为：

1. **SQLite**：适合本地结构化数据库，便于离线分析。
2. **Supabase**：适合网页同步、多设备访问和 SQL 查询。
3. **Firebase**：适合快速云同步和移动端使用。
4. **Notion API**：适合把实验记录同步到 Notion 数据库。
5. **Obsidian Dataview**：适合继续用 Markdown，但用 frontmatter 做表格查询。

推荐路线：

1. 继续用本 App 记录 1 到 2 周。
2. 定期导出 JSON。
3. 根据真实字段稳定程度，决定是否迁移到 SQLite 或 Supabase。

## 现场实验最低记录标准

每次实验至少记录：

1. 用的是哪个样品
2. 今天做了什么
3. 用了什么设备
4. 关键参数是多少
5. 看到了什么现象
6. 哪些地方不确定
7. 下一步做什么
