---
title: MengjieVault 总入口
date: 2026-05-15
updated: 2026-05-28
tags:
  - 库结构
  - index
---

# MengjieVault

这个仓库是当前 Obsidian 主库，用来保存研究笔记、项目代码、文献精读、分享材料和归档资料。

## 快速入口

| 目录 | 用途 |
| --- | --- |
| [[00-Inbox/README|00-Inbox]] | 临时收集区，例如网页剪藏、随手记。 |
| [[10-Research/README|10-Research]] | 正式研究和长期学习笔记。当前主线是拓扑光子学、量子力学和 UAV。 |
| [[20-Projects/README|20-Projects]] | 有代码、脚本、环境文件或可执行产物的项目。 |
| [[30-Literature/README|30-Literature]] | 文献精读、原子笔记、论文汇报稿。 |
| [[80-Archive/README|80-Archive]] | 旧库、迁移残留、历史项目。优先只读，不作为新内容入口。 |
| [[90-Local_Not_Upload/README|90-Local_Not_Upload]] | 本地大文件和备份，不上传 GitHub。 |
| [[100-app/README|100-app]] | iPhone 实验记录卡 Web App，可通过 GitHub Pages 在手机 Safari 打开。 |

## 使用规则

- 新资料先放 `00-Inbox/`，整理后再进入研究、文献或项目目录。
- 正式研究内容优先写入 `10-Research/`。
- 代码和可复现实验流程放 `20-Projects/`。
- 文献精读和论文汇报放 `30-Literature/`。
- 手机实验记录 App 放 `100-app/`。
- 旧库资料可以引用，但不要继续在 `80-Archive/` 里扩展新主线。
- PDF、Git 备份、大型输出文件放 `90-Local_Not_Upload/`，该目录已被 Git 忽略。
- `.obsidian/workspace.json` 是 Obsidian 窗口状态，已停止跟踪，不需要提交。

## 术语说明

- Git：版本管理工具，用来保存文件修改历史。
- Obsidian：Markdown 笔记软件，本仓库就是当前 Obsidian 主库。
- GitHub Pages：GitHub 提供的网页托管功能，用来访问 `100-app`。
