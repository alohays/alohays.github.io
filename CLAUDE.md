# CLAUDE.md — Project Guidelines for Claude Code

## Project Overview

Personal homepage for Yunsung Lee, built with MkDocs (Material theme).
Deployed at https://alohays.github.io.

## Key Structure

```
docs/index.md          # Homepage (includes Recent Publications list)
docs/cv/index.md       # CV page (Markdown, year-based publication sections)
docs/cv/cv.pdf         # CV PDF served at https://alohays.github.io/cv/cv.pdf
docs/cv/yunsungs_cv/   # Git submodule (repo: alohays/yunsungs_cv)
  └── Resume_for_Frehers.tex   # LaTeX source for CV
  └── Resume_for_Frehers.pdf   # Compiled PDF output
mkdocs.yml             # MkDocs configuration
```

## CV Update Workflow

When updating CV content (publications, work experience, etc.), **all three sources must be kept in sync**:

1. **`docs/index.md`** — Update the "Recent Publications" list if the change affects it.
2. **`docs/cv/index.md`** — Update the Markdown CV page (publications are organized by year sections: `### 2026`, `### 2025`, etc.).
3. **`docs/cv/yunsungs_cv/Resume_for_Frehers.tex`** — Update the LaTeX source in the submodule.
4. **Rebuild PDF** — Run `pdflatex` in the submodule directory to regenerate `Resume_for_Frehers.pdf`.
5. **Copy PDF** — Copy the rebuilt PDF to the served location:
   ```
   cp docs/cv/yunsungs_cv/Resume_for_Frehers.pdf docs/cv/cv.pdf
   ```

### Commit & Push Order

Since `docs/cv/yunsungs_cv/` is a **git submodule**, commits and pushes must happen in this order:

1. **Submodule first**: Stage, commit, and push inside `docs/cv/yunsungs_cv/`.
2. **Parent repo second**: Stage the submodule ref update (`docs/cv/yunsungs_cv`), the copied `docs/cv/cv.pdf`, and any other changed files. Commit and push.

Use `git push --recurse-submodules=on-demand` from the parent repo to push both in one command, or push each repo individually.

## LaTeX Build

```bash
cd docs/cv/yunsungs_cv
pdflatex -interaction=nonstopmode Resume_for_Frehers.tex
```

## Publication Entry Formats

### Homepage (`docs/index.md`)
```
- **Paper Title** (VENUE'YY)
```

### CV Markdown (`docs/cv/index.md`)
```
- Authors, "Paper Title," Full Venue Name (**VENUE'YY**), YYYY. [[Project Code]](url)
```
- Escaped asterisks for equal contribution: `\*`
- Co-corresponding: `^†`

### CV LaTeX (`Resume_for_Frehers.tex`)
```latex
\item Authors, ``Paper Title," Full Venue Name ({\bf VENUE'YY}), YYYY. \href{url}{Project page}
```
- Equal contribution: `*`
- Co-corresponding: `$^{\dag}$`
