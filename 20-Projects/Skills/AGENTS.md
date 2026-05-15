# Repository Instructions

This vault follows a Karpathy-style LLM wiki layout: keep source material in `raw/`, maintain distilled knowledge in `wiki/`, and use this file as the operating schema for agents.

## Purpose

Build a quantum mechanics demonstration library that connects concepts, equations, simulations, visual explanations, and source references.

## Directory Contract

- `raw/`: original materials. Prefer preserving files exactly as collected.
- `wiki/`: distilled, linked Markdown notes. This is the working knowledge layer.
- `templates/`: reusable note templates for new concepts, demos, experiments, and sources.
- `.obsidian/`: Obsidian vault configuration. Do not edit unless the change is explicitly vault-related.

## Raw Material Rules

- Put papers in `raw/papers/`, books in `raw/books/`, videos in `raw/videos/`, web captures in `raw/articles/`, quick notes in `raw/notes/`, datasets in `raw/datasets/`, and media assets in `raw/assets/`.
- Do not rewrite source materials in `raw/`. Add summaries or commentary in `wiki/`.
- When creating a wiki note from raw material, cite the raw path under a `Sources` section.

## Wiki Rules

- Keep `wiki/index.md` as the entry point.
- Update `wiki/log.md` whenever a meaningful source, concept, or demo is added.
- Prefer small, linkable notes over long monolithic notes.
- Use Obsidian wikilinks for internal references, for example `[[concepts/wavefunction]]`.
- Use LaTeX for equations and keep notation definitions near the first use.

## Naming

- Use lowercase kebab-case for file and folder names.
- Concept notes go in `wiki/concepts/`.
- Mathematical derivations go in `wiki/math/`.
- Demonstration plans go in `wiki/demos/`.
- Runnable or reproducible experiment descriptions go in `wiki/experiments/`.
- Open questions go in `wiki/questions/`.

## Quality Bar

- Separate physical intuition, mathematical statement, and visualization idea.
- Mark uncertainty explicitly.
- Do not invent citations. If a claim needs a source and none is available, add it to `wiki/questions/`.
