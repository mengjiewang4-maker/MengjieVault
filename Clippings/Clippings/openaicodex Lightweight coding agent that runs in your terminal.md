---
title: "openai/codex: Lightweight coding agent that runs in your terminal"
title_zh: "openai/codex：在终端中运行的轻量级编码代理"
source: "https://github.com/openai/codex#installing-and-running-codex-cli"
author:
published:
created: 2026-05-07
description: "Lightweight coding agent that runs in your terminal - openai/codex"
description_zh: "在终端中运行的轻量级编码代理 - openai/codex"
tags:
  - "clippings"
---
`npm i -g @openai/codex`  
or `brew install --cask codex`

**Codex CLI** is a coding agent from OpenAI that runs locally on your computer.

[![Codex CLI splash](https://github.com/openai/codex/raw/main/.github/codex-cli-splash.png)](https://github.com/openai/codex/blob/main/.github/codex-cli-splash.png)

  
If you want Codex in your code editor (VS Code, Cursor, Windsurf), [install in your IDE.](https://developers.openai.com/codex/ide)  
If you want the desktop app experience, run `codex app` or visit [the Codex App page](https://chatgpt.com/codex?app-landing-page=true).  
If you are looking for the *cloud-based agent* from OpenAI, **Codex Web**, go to [chatgpt.com/codex](https://chatgpt.com/codex).

---

## Quickstart

### Installing and running Codex CLI

Install globally with your preferred package manager:

```
# Install using npm
npm install -g @openai/codex
```
```
# Install using Homebrew
brew install --cask codex
```

Then simply run `codex` to get started.

You can also go to the [latest GitHub Release](https://github.com/openai/codex/releases/latest) and download the appropriate binary for your platform.

Each GitHub Release contains many executables, but in practice, you likely want one of these:

- macOS
	- Apple Silicon/arm64: `codex-aarch64-apple-darwin.tar.gz`
		- x86\_64 (older Mac hardware): `codex-x86_64-apple-darwin.tar.gz`
- Linux
	- x86\_64: `codex-x86_64-unknown-linux-musl.tar.gz`
		- arm64: `codex-aarch64-unknown-linux-musl.tar.gz`

Each archive contains a single entry with the platform baked into the name (e.g., `codex-x86_64-unknown-linux-musl`), so you likely want to rename it to `codex` after extracting it.

### Using Codex with your ChatGPT plan

Run `codex` and select **Sign in with ChatGPT**. We recommend signing into your ChatGPT account to use Codex as part of your Plus, Pro, Business, Edu, or Enterprise plan. [Learn more about what's included in your ChatGPT plan](https://help.openai.com/en/articles/11369540-codex-in-chatgpt).

You can also use Codex with an API key, but this requires [additional setup](https://developers.openai.com/codex/auth#sign-in-with-an-api-key).

## Docs

- [**Codex Documentation**](https://developers.openai.com/codex)
- [**Contributing**](https://github.com/openai/codex/blob/main/docs/contributing.md)
- [**Installing & building**](https://github.com/openai/codex/blob/main/docs/install.md)
- [**Open source fund**](https://github.com/openai/codex/blob/main/docs/open-source-fund.md)

This repository is licensed under the [Apache-2.0 License](https://github.com/openai/codex/blob/main/LICENSE).

---

## 中文翻译

`npm i -g @openai/codex`  
或 `brew install --cask codex`

**Codex CLI** 是 OpenAI 提供的本地编码代理，可以在你的电脑终端中运行。

如果想在代码编辑器中使用 Codex（VS Code、Cursor、Windsurf），可以安装 IDE 扩展。  
如果想使用桌面应用体验，可以运行 `codex app`，或访问 Codex App 页面。  
如果你寻找的是 OpenAI 的云端代理 **Codex Web**，请访问 `chatgpt.com/codex`。

## 快速开始

### 安装并运行 Codex CLI

使用你偏好的包管理器全局安装：

```bash
# 使用 npm 安装
npm install -g @openai/codex
```

```bash
# 使用 Homebrew 安装
brew install --cask codex
```

然后运行 `codex` 即可开始使用。

也可以前往最新的 GitHub Release，下载适合你平台的二进制文件。每个 Release 包含多个可执行文件；实际使用时，通常选择以下之一：

- macOS
  - Apple Silicon/arm64: `codex-aarch64-apple-darwin.tar.gz`
  - x86_64 旧款 Mac: `codex-x86_64-apple-darwin.tar.gz`
- Linux
  - x86_64: `codex-x86_64-unknown-linux-musl.tar.gz`
  - arm64: `codex-aarch64-unknown-linux-musl.tar.gz`

每个压缩包都只包含一个带平台名称的可执行文件，例如 `codex-x86_64-unknown-linux-musl`。解压后通常可以把它重命名为 `codex`。

### 使用 ChatGPT 方案登录 Codex

运行 `codex`，选择 **Sign in with ChatGPT**。官方建议使用 ChatGPT 账号登录，从而在 Plus、Pro、Business、Edu 或 Enterprise 方案中使用 Codex。

你也可以使用 API key 运行 Codex，但这需要额外配置。

## 文档

- **Codex 文档**
- **贡献指南**
- **安装与构建**
- **开源基金**

此仓库使用 Apache-2.0 许可证。
