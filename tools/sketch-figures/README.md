# Four-axis essay figures

The published post includes twelve `fig-*.html` snippets from
`docs/assets/images/blog/physical-units/`. Text wraps in HTML; SVG contains
tree geometry and numerical plot marks. The two raster images are cited in
the post.

## Rebuild the figures

From the repository root:

```sh
uv run --no-project --with matplotlib==3.11.2 --with numpy python tools/sketch-figures/responsive_plots.py
python3 tools/sketch-figures/responsive_figures.py
```

The shared styles are in `docs/stylesheets/physical-figures.css`; the
keyboard-accessible enlarged view is in `docs/javascripts/physical-figures.js`.
The numeric plot inputs and their source locators are in `energy-data.json`.

## Check the calculations and site

```sh
python3 tools/sketch-figures/audit.py
make check
make docs-test
```

The standard-library audit checks the illustrative calculations, source data,
footnote wiring, active images, and publication/history state. It does not
validate the proposed intelligence measures or the frontier-model priors.
Its report is written to the ignored `_workspace/physical-units-checks/`.

Inspect the rendered figures at phone and desktop widths in both color
schemes, with enlarged text and the figure viewer. Check text within the
padded cards, readable axis labels, contrast, and keyboard focus. The METR
source image retains its original labels and is available in the full-size
viewer.

## Local Korean review

`responsive_figures.py --korean-review` also writes translated snippets to
`_workspace/2026-09-20-self-contained/figures/`. The complete Korean reading
edition and its builder are kept in that local workspace and are not part of
the published site. Do not place review HTML or translated assets in `docs/`.

Private editorial records, generated reports, and retired figure experiments
are intentionally ignored by Git.
