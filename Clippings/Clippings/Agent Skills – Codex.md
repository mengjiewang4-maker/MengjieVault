---
title: "Agent Skills – Codex"
title_zh: "代理技能 - Codex"
source: "https://developers.openai.com/codex/skills#create-a-skill"
author:
published:
created: 2026-05-06
description: "Give Codex new capabilities and expertise"
description_zh: "为 Codex 添加新的能力和专业知识"
tags:
  - "clippings"
---
Use agent skills to extend Codex with task-specific capabilities. A skill packages instructions, resources, and optional scripts so Codex can follow a workflow reliably. Skills build on the [open agent skills standard](https://agentskills.io/).  
使用代理技能可以为 Codex 扩展特定任务的功能。技能包含指令、资源和可选脚本，使 Codex 能够可靠地执行工作流程。技能基于 [开放的代理技能标准](https://agentskills.io/) 构建。

Skills are the authoring format for reusable workflows. Plugins are the installable distribution unit for reusable skills and apps in Codex. Use skills to design the workflow itself, then package it as a [plugin](https://developers.openai.com/codex/plugins/build) when you want other developers to install it.  
技能是可重用工作流的创作格式。插件是 Codex 中可重用技能和应用程序的可安装分发单元。使用技能设计工作流本身，然后在需要其他开发者安装时将其打包成 [插件](https://developers.openai.com/codex/plugins/build) 。

Skills are available in the Codex CLI, IDE extension, and Codex app.  
技能可在 Codex CLI、IDE 扩展和 Codex 应用程序中使用。

Skills use **progressive disclosure** to manage context efficiently: Codex starts with each skill’s name, description, and file path. Codex loads the full `SKILL.md` instructions only when it decides to use a skill.  
技能采用 **渐进式披露机制** 来高效管理上下文：Codex 首先加载每个技能的名称、描述和文件路径。只有在决定使用某个技能时，Codex 才会加载完整的 `SKILL.md` 指令。

Codex includes an initial list of available skills in context so it can choose the right skill for a task. To avoid crowding out the rest of the prompt, this list is capped at roughly 2% of the model’s context window, or 8,000 characters when the context window is unknown. If many skills are installed, Codex shortens skill descriptions first. For very large skill sets, some skills may be omitted from the initial list, and Codex will show a warning.  
Codex 会提供一个初始的可用技能列表，以便根据任务选择合适的技能。为了避免占用过多提示信息，该列表的长度限制在模型上下文窗口的 2% 左右，或者在上下文窗口未知的情况下限制为 8000 个字符。如果安装了多个技能，Codex 会优先缩短技能描述。对于非常庞大的技能集，某些技能可能会从初始列表中省略，此时 Codex 会显示警告。

This budget applies only to the initial skills list. When Codex selects a skill, it still reads the full SKILL.md instructions for that skill.  
此预算仅适用于初始技能列表。当 Codex 选择一项技能时，它仍然会读取该技能的完整 SKILL.md 指令。

A skill is a directory with a `SKILL.md` file plus optional scripts and references. The `SKILL.md` file must include `name` and `description`.  
技能是一个目录 `SKILL.md` 其中包含一个 `SKILL.md` 文件以及可选的脚本和引用。SKILL.md 文件必须包含 `name` 和 `description` 。

## Codex 如何使用技能 / How Codex uses skills

Codex can activate skills in two ways:  
Codex 可以通过两种方式激活技能：

1. **Explicit invocation:** Include the skill directly in your prompt. In CLI/IDE, run `/skills` or type `$` to mention a skill.  
	**显式调用：** 直接在提示符中输入技能名称。在命令行界面/集成开发环境 (CLI/IDE) 中，运行 `/skills` 或输入 `$` 来指定技能。
2. **Implicit invocation:** Codex can choose a skill when your task matches the skill `description`.  
	**隐式调用：** 当你的任务与技能 `description` 匹配时，Codex 可以选择一项技能。

Because implicit matching depends on `description`, write concise descriptions with clear scope and boundaries. Front-load the key use case and trigger words so Codex can still match the skill if descriptions are shortened.  
由于隐式匹配依赖于 `description` ，因此请编写简洁明了、范围和界限清晰的描述。提前列出关键用例和触发词，以便即使描述缩短，Codex 仍能匹配到相应的技能。

## 创建技能 / Create a skill

Use the built-in creator first:  
请先使用内置的创建工具：

```text
$skill-creator
```

The creator asks what the skill does, when it should trigger, and whether it should stay instruction-only or include scripts. Instruction-only is the default.  
创建者需要询问技能的功能、触发时机，以及是否仅提供指令或包含脚本。默认设置为仅提供指令。

You can also create a skill manually by creating a folder with a `SKILL.md` file:  
您也可以通过创建一个包含 `SKILL.md` 文件的文件夹来手动创建技能：

```md
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

Codex detects skill changes automatically. If an update doesn’t appear, restart Codex.  
Codex 会自动检测技能变更。如果未显示更新，请重启 Codex。

## 技能保存在哪里 / Where to save skills

Codex reads skills from repository, user, admin, and system locations. For repositories, Codex scans `.agents/skills` in every directory from your current working directory up to the repository root. If two skills share the same `name`, Codex doesn’t merge them; both can appear in skill selectors.  
Codex 会从仓库、用户、管理员和系统位置读取技能。对于仓库，Codex 会扫描从当前工作目录到仓库根目录的每个目录中的 `.agents/skills` 。如果两个技能 `name` 相同，Codex 不会合并它们；两者都可以出现在技能选择器中。

| Skill Scope 技能范围 | Location 地点 | Suggested use 建议用途 |
| --- | --- | --- |
| `REPO` | `$CWD/.agents/skills`   Current working directory: where you launch Codex.   当前工作目录：Codex 的启动目录。 | If you’re in a repository or code environment, teams can check in skills relevant to a working folder. For example, skills only relevant to a microservice or a module.   如果您身处代码仓库或代码环境中，团队可以提交与工作文件夹相关的技能。例如，仅与某个微服务或模块相关的技能。 |
| `REPO` | `$CWD/../.agents/skills`   A folder above CWD when you launch Codex inside a Git repository.   在 Git 仓库中启动 Codex 时，当前工作目录 (CWD) 的上一级文件夹。 | If you’re in a repository with nested folders, organizations can check in skills relevant to a shared area in a parent folder.   如果您在一个具有嵌套文件夹的存储库中，组织可以将与父文件夹中的共享区域相关的技能签入。 |
| `REPO` | `$REPO_ROOT/.agents/skills`   The topmost root folder when you launch Codex inside a Git repository.   在 Git 仓库中启动 Codex 时，最顶层的根文件夹。 | If you’re in a repository with nested folders, organizations can check in skills relevant to everyone using the repository. These serve as root skills available to any subfolder in the repository.   如果您使用的存储库包含嵌套文件夹，组织可以提交与存储库中所有用户相关的技能。这些技能将作为根技能，供存储库中的任何子文件夹使用。 |
| `USER` | `$HOME/.agents/skills`   Any skills checked into the user’s personal folder.   已将任何技能检入用户的个人文件夹。 | Use to curate skills relevant to a user that apply to any repository the user may work in.   用于整理与用户相关的技能，这些技能适用于用户可能参与的任何代码库。 |
| `ADMIN` | `/etc/codex/skills`   Any skills checked into the machine or container in a shared, system location.   任何技能都已检入到共享系统位置的机器或容器中。 | Use for SDK scripts, automation, and for checking in default admin skills available to each user on the machine.   可用于 SDK 脚本、自动化以及检查机器上每个用户可用的默认管理员技能。 |
| `SYSTEM` | Bundled with Codex by OpenAI.   与 OpenAI 的 Codex 捆绑在一起。 | Useful skills relevant to a broad audience such as the skill-creator and plan skills. Available to everyone when they start Codex.   面向广大用户的实用技能，例如技能创建和计划技能。所有 Codex 用户在注册时均可使用。 |

Codex supports symlinked skill folders and follows the symlink target when scanning these locations.  
Codex 支持符号链接的技能文件夹，并在扫描这些位置时跟随符号链接目标。

These locations are for authoring and local discovery. When you want to distribute reusable skills beyond a single repo, or optionally bundle them with app integrations, use [plugins](https://developers.openai.com/codex/plugins/build).  
这些位置用于创作和本地发现。如果您想将可重用的技能分发到单个代码库之外，或者选择将其与应用程序集成捆绑在一起，请使用 [插件](https://developers.openai.com/codex/plugins/build) 。

## 使用插件分发技能 / Distribute skills with plugins

Direct skill folders are best for local authoring and repo-scoped workflows. If you want to distribute a reusable skill, bundle two or more skills together, or ship a skill alongside an app integration, package them as a [plugin](https://developers.openai.com/codex/plugins/build).  
直接创建技能文件夹最适合本地创作和代码仓库范围的工作流。如果 你想分发一项可重用的技能，或者将两项或多项技能捆绑在一起，或者 将技能与应用程序集成一起发布，并将它们打包在一起。 [插件](https://developers.openai.com/codex/plugins/build) 。

Plugins can include one or more skills. They can also optionally bundle app mappings, MCP server configuration, and presentation assets in a single package.  
插件可以包含一项或多项技能。它们还可以选择将应用程序映射、MCP 服务器配置和演示资源打包到一个软件包中。

## 安装本地使用的精选技能 / Install curated skills for local use

To add curated skills beyond the built-ins for your own local Codex setup, use `$skill-installer`. For example, to install the `$linear` skill:  
要为本地 Codex 设置添加内置技能之外的精选技能，请使用 `$skill-installer` 。例如，要安装 `$linear` 技能：

```bash
$skill-installer linear
```

You can also prompt the installer to download skills from other repositories. Codex detects newly installed skills automatically; if one doesn’t appear, restart Codex.  
您还可以指示安装程序从其他存储库下载技能。Codex 会自动检测新安装的技能；如果某个技能未显示，请重启 Codex。

Use this for local setup and experimentation. For reusable distribution of your own skills, prefer plugins.  
可用于本地部署和实验。如需重复使用并分发您的技能，建议使用插件。

## 启用或禁用技能 / Enable or disable skills

Use `[[skills.config]]` entries in `~/.codex/config.toml` to disable a skill without deleting it:  
在 `~/.codex/config.toml` 文件中使用 `[[skills.config]]` 条目可以禁用技能而不将其删除：

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Restart Codex after changing `~/.codex/config.toml`.  
修改 `~/.codex/config.toml` 后重启 Codex。

## 可选元数据 / Optional metadata

Add `agents/openai.yaml` to configure UI metadata in the [Codex app](https://developers.openai.com/codex/app), to set invocation policy, and to declare tool dependencies for a more seamless experience with using the skill.  
在 [Codex 应用](https://developers.openai.com/codex/app) 中添加 `agents/openai.yaml` 以配置 UI 元数据，设置调用策略，并声明工具依赖项，从而获得更流畅的技能使用体验。

```yaml
interface:
  display_name: "Optional user-facing name"
  short_description: "Optional user-facing description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt to use the skill with"

policy:
  allow_implicit_invocation: false

dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

`allow_implicit_invocation` (default: `true`): When `false`, Codex won’t implicitly invoke the skill based on user prompt; explicit `$skill` invocation still works.  
`allow_implicit_invocation` （默认值： `true` ）：当设置为 `false` 时，Codex 不会根据用户提示隐式调用技能；显式 `$skill` 调用仍然有效。

## 最佳实践 / Best practices

- Keep each skill focused on one job.  
	每项技能都应专注于一项工作。
- Prefer instructions over scripts unless you need deterministic behavior or external tooling.  
	除非你需要确定性的行为或外部工具，否则请优先使用指令而不是脚本。
- Write imperative steps with explicit inputs and outputs.  
	写出包含明确输入和输出的命令式步骤。
- Test prompts against the skill description to confirm the right trigger behavior.  
	根据技能描述测试提示，以确认正确的触发行为。

For more examples, see [github.com/openai/skills](https://github.com/openai/skills) and [the agent skills specification](https://agentskills.io/specification).  
更多示例请参见 [github.com/openai/skills](https://github.com/openai/skills) 和 [代理技能规范](https://agentskills.io/specification) 。
