# Migration Report

- Source file: `../onenote.docx`
- Pandoc command: not executed because `pandoc` was not available in PATH and `./onenote.docx` was absent.
- Conversion fallback: standard-library DOCX XML parser with media extraction.
- Generated temp markdown: `temp.md`
- Split notes: 287
- Extracted attachments: 25
- Attachment embeds used in notes: 25

## 分类统计

- 来源: 143
- 概念: 40
- 方法: 25
- 模型: 45
- 洞察: 34

## 异常内容

- `pandoc` was not available, so the requested pandoc command could not be run.
- `onenote.docx` was not present in the current directory; used `../onenote.docx`.
