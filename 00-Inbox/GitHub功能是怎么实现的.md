---
tags:
  - GitHub
  - Git
  - 工作流
created: 2026-05-23
---

# GitHub 功能是怎么实现的

这篇笔记是给自己和别人看的，用来说明：我们平时说的“GitHub 备份、提交、推送、同步”，背后到底发生了什么。

## 一句话理解

Git 是本地的版本管理工具，GitHub 是放在网上的 Git 仓库服务。

可以把它理解成：

- Git：电脑里的“版本记录本”
- GitHub：云端的“共享版本记录本”
- commit：把当前选中的文件变化拍一张快照
- push：把本地快照上传到 GitHub
- pull：把 GitHub 上的新快照下载到本地

## Git 解决什么问题

不用 Git 时，一个项目常常会变成这样：

```text
论文.docx
论文_修改版.docx
论文_最终版.docx
论文_最终最终版.docx
论文_老师意见后修改.docx
```

Git 的做法不是复制很多文件，而是记录每一次变化：

```text
第 1 次提交：建立项目结构
第 2 次提交：加入 COMSOL 到 GDS 笔记
第 3 次提交：修改 GitHub 使用说明
```

每一次提交都可以回看，也可以知道是谁、什么时候、改了什么。

## GitHub 解决什么问题

GitHub 本身不是“编辑器”，它更像一个项目云盘加版本记录系统。

它主要做这些事：

- 远程备份：电脑坏了，GitHub 上还有一份
- 多人协作：别人可以看到你提交了什么
- 历史追踪：每次改动都有记录
- 对比变化：能看到一行一行改了哪里
- 回到旧版本：如果改坏了，可以回退
- 分享项目：别人可以 clone，也就是复制一份仓库

## 我们刚才做的事情

刚才的要求是：

只提交笔记，不提交大文件。

实际做法是：

1. 先查看仓库状态：

```bash
git status
```

这个命令会告诉我们哪些文件改了、哪些文件还没被 Git 管理。

2. 只选择笔记文件：

```bash
git add 10-Research/COMSOL到GDS画图研究/
```

`git add` 的意思不是“上传”，而是“加入本次准备提交的清单”。

3. 确认暂存区只剩笔记：

```bash
git diff --cached --name-only
```

`cached` 指的是暂存区，也就是即将进入 commit 的内容。

4. 生成提交：

```bash
git commit -m "Add COMSOL to GDS workflow notes"
```

`commit` 是本地保存一个版本快照。到这一步，还没有上传 GitHub。

5. 上传到 GitHub：

```bash
git push
```

`push` 才是把本地 commit 上传到 GitHub。

## 为什么不能直接 git add .

`git add .` 的意思是：把当前目录下所有变化都加入暂存区。

这在文件很干净的小项目里可以用，但在 Obsidian vault 或科研项目里很危险，因为可能会把这些东西一起提交：

- 大型 COMSOL `.mph` 文件
- GDS/OAS 版图文件
- 仿真结果图片
- Python 依赖目录 `.python_deps`
- 临时文件 `.DS_Store`
- 不相关的笔记移动和删除

所以这类仓库更适合精确提交：

```bash
git add 某个具体文件
git add 某个具体笔记文件夹
```

## 什么文件适合提交

适合提交：

- `.md` 笔记
- 小型脚本，例如 `.py`
- 参数说明，例如 `.json`
- README 文档
- 重要但体积不大的配置文件

不适合直接提交：

- 几 GB 的 `.mph` 仿真文件
- 大量图片和视频
- 自动生成的中间文件
- Python 安装依赖目录
- 临时缓存文件

这些大文件如果真的要管理，应该考虑 Git LFS。

Git LFS 是 Git Large File Storage 的缩写，意思是“大文件存储”。它会让 Git 只记录大文件的指针，真正的大文件放在专门的大文件存储里。

## 本地和 GitHub 的关系

可以这样理解：

```text
本地文件夹
  ↓ git add
暂存区
  ↓ git commit
本地 Git 历史
  ↓ git push
GitHub 远程仓库
```

反过来，如果 GitHub 上有新变化：

```text
GitHub 远程仓库
  ↓ git pull
本地 Git 历史和本地文件夹
```

## 常用命令

查看状态：

```bash
git status
```

查看有哪些文件准备提交：

```bash
git diff --cached --name-only
```

只添加某个文件：

```bash
git add 文件路径
```

取消暂存，但不删除文件：

```bash
git restore --staged 文件路径
```

提交：

```bash
git commit -m "说明这次改了什么"
```

上传到 GitHub：

```bash
git push
```

下载 GitHub 上的新变化：

```bash
git pull
```

## 最重要的习惯

提交前先看：

```bash
git status
git diff --cached --name-only
```

确认暂存区里只有自己想提交的文件，再 commit。

对科研项目尤其重要：笔记可以频繁提交，大型仿真文件和加工版图要谨慎提交。
