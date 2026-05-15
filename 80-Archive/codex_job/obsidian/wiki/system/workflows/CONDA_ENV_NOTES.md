# Conda Environment Notes

## `ai_automation_tools`

用途说明：
- 这个环境主要偏向自动化内容处理 / 文档解析 / 多模态本地工具链
- 当前已看到的核心包包括 `openai-whisper`、`onnxruntime`、`opencv-python`、`pdfplumber`、`python-docx`
- 还包含 `sentence-transformers`、`transformers`、`keybert`、`scikit-learn`
- 适合做音频转写、PDF/Word 文档抽取、关键词提取、文本向量化、图像预处理、去背景等自动化任务

判断：
- 它不是通用 Python 基础环境
- 也不是 GDS / 量化环境
- 更像一个本地 AI 自动化工具环境

建议：
- 如果你还会做文档处理、转写、关键词提取、图片处理之类的任务，建议保留
- 如果你已经明确不再使用这些自动化工具链，再考虑删除
- 由于体积约 `1.4G`，如果磁盘空间紧张，可以作为后续重点清理候选，但不建议在用途未确认前直接删

## `photonic_gds_design`

用途说明：
- 这个环境主要用于 GDS / 版图相关工作
- 当前已看到的核心包包括 `gdsfactory`、`gdspy`、`gdstk`
- 适合运行版图生成、GDS 几何处理、光子版图相关脚本

建议：
- 保留
- 如果后续还有其他 GDS 项目，可以优先复用这个环境
- 如果未来你想把所有版图工作统一迁到更清晰的命名，可以考虑以后重命名或新建一个更明确的环境名

## `quant_research`

用途说明：
- 这个环境主要用于量化/行情/回测相关工作
- 当前已看到的核心包包括 `akshare`、`backtrader`、`matplotlib`
- 适合运行行情数据获取、策略回测、量化分析类脚本

建议：
- 保留
- 如果你后面继续做金融数据分析或策略研究，这个环境可以直接复用

## Current Recommendation

- `auto_tools`: 保留，作为自动化内容处理 / AI 工具环境
- `photonic_gds_design`: 保留，作为 GDS/版图环境
- `quant_research`: 保留，作为量化分析环境
- `project_vortex_layout`: 保留，作为 `工作区/Project_Replication_Vortex` 项目专用环境
