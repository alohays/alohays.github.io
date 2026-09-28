# Repository editing policy

## Blog post change history

- A post with `draft: true` is still in private editorial work. Do not expose a `Changelog` or `변경 이력` section in the post or its translated reading edition. Keep pre-release revisions in internal audit or research records.
- After a post is released (`draft: false`), keep a reader-visible change-history section at the bottom of the English post and every complete translation. Append dated, material, reader-facing changes there instead of silently patching the published text.
- Do not backfill the public history with the draft's private editing history. Do not put internal QA, agent workflow, approval state, or implementation details into the reader-facing history.
- When editing a post, check that the English and translated public histories are synchronized, and that a draft has no public history block.

## Local review editions

- Keep complete Korean review editions, their translated figure assets, and private editorial records under `_workspace/`, which is Git-ignored. Preserve them locally when preparing publication.
- Publish the English post and its runtime assets. Do not stage local review pages, private revision records, or generated audit reports.
- Do not write translated review assets into `docs/`. Generate them in the ignored review workspace and keep the local reader usable.
