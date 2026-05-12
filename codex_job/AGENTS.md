# Repository Operating Guide

## Directory Roles

- `obsidian/raw/` stores original source material. Keep imported papers, clips, transcripts, figures, and raw data here.
- `obsidian/wiki/` stores cleaned and structured knowledge. Concepts, topic notes, project notes, templates, and MOCs belong here.
- `obsidian/outputs/` stores final expression. Reports, slides, and polished summaries belong here.
- `code/` stores runnable code, scripts, notebooks, and engineering workspaces.
- `results/` stores important figures, generated artifacts, and durable outputs worth keeping outside the vault.

## Working Rules

- Prefer moving material rather than deleting note bodies.
- New reference material should land in `obsidian/raw/` first, then be distilled into `obsidian/wiki/`.
- Final-facing deliverables should be written in `obsidian/outputs/`.
- Avoid creating parallel vault roots or duplicate top-level knowledge trees.
- Cache files, temporary editor state, and OS metadata should stay ignored by git.
