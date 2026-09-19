# Literature retrieval policy for bib/

This directory is optimized for high-fidelity, low-context academic retrieval.

1. Start with `bib/INDEX.md`; identify only the relevant papers.
2. Read/search `bib/extracted/*.md` first. Markdown is the primary retrieval layer.
3. Formulae and tables in Markdown should be treated as structured extracted content, but
   critical exact values should still be verified against the original PDF when needed.
4. `bib/references/` is split out to reduce retrieval noise; search it for citation chaining.
5. `bib/assets/` exists only when extraction was run with `--assets`. Use a targeted crop
   when a visually encoded table/figure cannot be resolved reliably from Markdown.
6. `bib/pdf/*.pdf` is the source of truth.
7. Never infer a coefficient, p-value, confidence interval, sample size, or effect size from
   visibly corrupted extraction; verify it against the PDF.
