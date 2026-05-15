# LLM Wiki Schema

This vault is organized as a small LLM-readable knowledge base.

## Layers

1. `raw/`
   - Original source files.
   - Append-only by default.
   - Examples: PDFs, DOCX, PPTX, meeting notes, exported web pages, screenshots, datasets.

2. `wiki/`
   - Compiled knowledge written from the raw layer.
   - This is the main working memory for AI-assisted research.
   - Notes should be short, linked, source-backed, and easy to update.

3. `outputs/`
   - Deliverables created from the wiki layer.
   - Examples: reports, briefs, slide outlines, export files.

## Required Maintenance

- Update `wiki/index.md` when adding an important note.
- Update `wiki/log.md` after a significant ingest or synthesis pass.
- Add unresolved items to `wiki/questions/open-questions.md`.
- Prefer creating one focused note per concept, system, product, standard, project, or decision.

## Source Citation Format

Use this format inside wiki notes:

```markdown
## Sources

- `raw/path/to/source.pdf`
- `raw/path/to/source.docx`
```

