name: clippings_to_notes

input:
  type: folder
  path: obsidian/clippings/

process:
  - clean_markdown:
      remove:
        - ads
        - navigation
        - redundant_links

  - summarize:
      structured:
        sections:
          - 背景
          - 核心内容
          - 关键结论
          - 我的启发

  - add_metadata:
      type: source_note
      tags: auto

output:
  path: obsidian/来源/
  format: markdown