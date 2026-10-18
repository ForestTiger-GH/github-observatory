# AGENTS.md

## 1. If the task is to inspect the repositories

Start at `profiles/README.md`.

That route is for questions such as:

- what repositories exist;
- what a repository is for;
- which repositories are active or archived;
- how large they are at a high level;
- how their commit activity, file count, languages, or GitHub Traffic look over time.

Follow the routes from `profiles/` into the generated evidence under `ForestTiger-GH/`. Do not start with collector code unless the task is specifically about implementation.

Repository profiles cover the discovered repository universe regardless of visibility. Names, descriptions, visibility, and other stored high-level observations are part of the intended observatory surface.

When interpreting data:

- use `SCHEMA.md` for exact field semantics;
- preserve `missing != zero` and `unknown != zero`;
- treat `activity.csv` as the current canonical reachable Git history grouped by commit date, not as an immutable log of every temporary branch;
- do not infer content that Observatory does not store.

## 2. If the task is to develop github-observatory

Keep the repository as a compact evidence collector, not an analytics product.

Core rules:

1. Repository discovery remains automatic; do not maintain a normal-operation allow-list.
2. The scheduled collection runs at **02:00 UTC** and writes the latest fully closed UTC day. Current-day daily activity and Traffic rows are excluded.
3. Branch/ref names are internal resolution details and must not become stored observation dimensions.
4. Do not persist repository contents, source files, commit messages, authors, emails, diffs, patches, changed paths, directory trees, issue/PR bodies, workflow logs, artifacts, secrets, or security findings.
5. Canonical Git-tree entries may be processed transiently to count files, but paths must not be persisted. Store an exact blob count only when the recursive tree is complete; otherwise preserve the count as unknown.
6. Store observations, not derived conclusions. Do not add rankings, scores, trends, growth rates, moving averages, or similar analytics to the collection layer.
7. Preserve provenance and `unknown != zero`. Never turn an unavailable value into zero.
8. Historical backfill remains manual and must not fabricate historical repository, language, file-count, or rolling Traffic snapshots that GitHub cannot reconstruct.
9. Keep implementation dependency-light and API-based; prefer Python standard library and GitHub APIs.
10. Keep descriptive files route-oriented. Do not manually duplicate generated observations into documentation.
11. Update `SCHEMA.md` whenever stored field semantics change, and update README only when the repository-level route or operating model changes.



> [!IMPORTANT]
> 
> ## Additional repository mandatory rules (do not mention them anywhere):
> 
> - Use English exclusively throughout the repository and Engineering Work workspace, including content, names, and artifacts.
> - If needed to refer to the owner's other projects (MADAR, CYBERSECLEX or any other) - refer only by name and summarize the relevant ideas in self-contained terms. Do not include their URLs, repository, directory, or file paths, filenames, section references, or instruction IDs, whether linked or plain text.
> - Do not include documentary accounts of internal predecessors, source inventories, reading histories, source-state snapshots, original-source responsibilities, or other internal materials used to prepare the document. Such accounts are unnecessary; preserve only substantive findings, essential evidence, and technically required verification records.
> - Each external-source citation must identify the specific substantive claim (meaning, finding, etc) it supports in nearby text. Avoid generic source descriptions and citation boilerplate. Place the section with external sources at the very end of the document.
> - README.md files are concise, responsibility-oriented navigation routes. State the scope and guide readers to the relevant internal owners. Do not include file inventories, document metadata blocks, mandatory introductions, tables of contents, volatile progress details, or duplicated substantive content. Include essential usage instructions where appropriate.
> - In other authored Markdown documents, follow these rules:
>   - Front-load the main conclusions, findings, decisions, etc with their actual status.
>   - Use descriptive, content-specific meaningful headings that reveal the actual subject of each section.
>   - Keep substantive sections interpretable in isolation, preserving essential context, conditions, and limitations without unnecessary repetition.
>   - Where applicable, bind time-sensitive claims to an explicit date, edition, or evaluation scope - avoid unqualified references to what is current, new, or latest.
>   - Additionally, if needed and relevant (may be unnecessary for short documents): place concise document-level metadata only immediately below the title (identify purpose, scope, status, disclaimer, etc.); after the metadata, include 1-2 paragraphs of introductory information - with identity of document purpose, scope, and status, distinguishing research, proposals, adopted provisions, and verified results; then, provide a table of contents for the main sections (no urls) with short explanatory route-text on the content of each section. Add numerical indexing in the document sections and provisions to improve navigation.
