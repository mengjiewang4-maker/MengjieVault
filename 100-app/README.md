# iPhone 实验记录卡 Web App

这个目录包含一个可部署到 GitHub Pages 的单文件 Web App：

- `index.html`

它用于快速记录微纳加工、SEM、光学测试、GDS/仿真和问题复盘信息，并生成可复制到 Obsidian 的 Markdown。

## 访问地址

GitHub 仓库：

```text
https://github.com/mengjiewang4-maker/MengjieVault
```

GitHub Pages 地址：

```text
https://mengjiewang4-maker.github.io/MengjieVault/100-app/
```

用 iPhone Safari 打开上面的 GitHub Pages 地址，就可以使用实验记录卡。

## GitHub Pages 部署

目标：让 iPhone Safari 访问这个网址：

```text
https://mengjiewang4-maker.github.io/MengjieVault/100-app/
```

步骤：

1. 把当前项目推送到 GitHub 仓库。
2. 打开 GitHub 仓库页面。
3. 进入 `Settings`。
4. 左侧找到 `Pages`。
5. 在 `Build and deployment` 里选择：
   - `Source`: `Deploy from a branch`
   - `Branch`: `main`
   - 文件夹：`/root`
6. 点击 `Save`。
7. 等待 GitHub Pages 构建完成。
8. 用 iPhone Safari 打开：

```text
https://mengjiewang4-maker.github.io/MengjieVault/100-app/
```

说明：GitHub Pages 是 GitHub 提供的静态网页托管服务。静态网页指不需要服务器程序运行的网页，本 App 只有 HTML、CSS 和 JavaScript，所以适合直接部署。

## 部署后检查

1. 在电脑浏览器打开 `https://mengjiewang4-maker.github.io/MengjieVault/100-app/`。
2. 确认页面标题是“iPhone 实验记录卡 Pro”。
3. 点击“SEM”模板，确认表单能自动填入提示。
4. 输入项目名、批次、GDS 版本、样品号，确认样品编号会自动生成。
5. 点击“生成”，确认 Markdown 输出区有内容。

如果页面显示 404，通常是 GitHub Pages 还没构建完成，等 1 到 3 分钟后刷新。404 是网页找不到的提示。

## 如何在 iPhone Safari 打开

1. 确认 GitHub Pages 已经部署成功。
2. 在 iPhone 上打开 Safari。
3. 输入 `https://mengjiewang4-maker.github.io/MengjieVault/100-app/`。
4. 页面打开后，先试着填写一条记录并点击底部的“生成”。

说明：Safari 是苹果手机自带浏览器。这个页面不依赖外部库，打开后主要数据保存在手机浏览器本机。

## 如何添加到主屏幕

1. 用 iPhone Safari 打开 GitHub Pages 地址。
2. 点击底部分享按钮。
3. 选择“添加到主屏幕”。
4. 名称可以改成“实验记录卡”。
5. 之后从主屏幕打开时，会更像一个轻量 App。

建议：第一次添加到主屏幕后，尽量固定使用这个入口记录实验。因为本机记录保存在浏览器本地数据里，换浏览器或清理 Safari 网站数据可能会影响历史记录。

## 手机现场使用建议

1. 实验开始前先打开主屏幕里的“实验记录卡”。
2. 选择一个快捷模板，例如“加工”或“SEM”。
3. 先填样品编号相关信息，再记录关键参数。
4. 每做完一个关键步骤就点击“保存”。
5. 实验结束后点击“导出当前 .md”或“复制”到 Obsidian。

## 如何复制到 Obsidian

1. 在 App 里填好记录。
2. 点击底部“生成”。
3. 点击底部“复制”。
4. 打开 Obsidian。
5. 新建一篇笔记，把内容粘贴进去。

Obsidian 是本地笔记软件；Markdown 是一种纯文本笔记格式，适合长期保存、搜索和版本管理。

## 如何导出 Markdown

当前记录：

1. 填写记录并点击“生成”。
2. 点击“导出当前 .md”。
3. 得到一个单独的 Markdown 文件。

全部记录：

1. 先用“保存”把多条记录保存在本机。
2. 点击“导出全部 .md”。
3. 得到一个合并后的 Markdown 文件。

## 如何备份 JSON

1. 点击“导出 JSON 备份”。
2. 保存生成的 `.json` 文件。
3. JSON 是结构化备份格式，适合以后恢复、整理或用脚本批量处理。

注意：本机保存使用浏览器的 `localStorage`。`localStorage` 是浏览器提供的本地小数据库，清理 Safari 网站数据时可能会被删除，所以重要记录建议定期导出 Markdown 和 JSON。

## 现场实验最低记录标准

每次实验至少记录：
1. 用的是哪个样品
2. 今天做了什么
3. 用了什么设备
4. 关键参数是多少
5. 看到了什么现象
6. 哪些地方不确定
7. 下一步做什么
