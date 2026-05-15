name: source_to_atomic

input:
  type: file

process:
  - extract_atomic:
      types:
        - concept
        - model
        - insight
        - method

output:
  path: obsidian/原子/
  