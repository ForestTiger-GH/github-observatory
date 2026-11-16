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
> ## Additional repository mandatory rules (do not mention them anywhere)
>
> Rule-types by file (Rule categories define their applicability. Apply each rule only to the corresponding artifact type and purpose. Do not extend type-specific requirements to unrelated artifacts.): [GR] – general rules; [RFR] – rules for research-files, [AFR] – rules for article-files, [SFR] – rules for service and operational files and catalogs; [TR] – rules for tests.
> 
>  - [GR]: Use English exclusively throughout the repository and Engineering Work workspace, including content, names, and artifacts.
>  - [GR]: Links from outside a madar-workspace to a madar-workspace is prohibited. Within documents located in the Madar workspace, only links within this same madar-workspace or to external destinations (non this repository) are permitted.
>  - [GR]: Do not include documentary accounts of internal predecessors, source inventories, reading histories, source-state snapshots, original-source responsibilities, or other internal materials used to prepare the document. Such accounts are unnecessary.
>  - [RFR] [AFR]: If needed to refer to the owner's other projects (MADAR, CMemory or any other) - refer only by name and summarize the relevant ideas in self-contained terms. Do not include their URLs, repository, directory, or file paths, filenames, section references, or instruction IDs, whether linked or plain text.
>  - [RFR]: Each external-source citation must identify the specific substantive claim (meaning, finding, etc) it supports in nearby text. Avoid generic source descriptions and citation boilerplate. Place the section with external sources at the very end of the document.
>  - [RFR] [AFR]: Front-load the main conclusions, findings, decisions, etc with their actual status.
>  - [RFR] [AFR]: Use descriptive, content-specific meaningful headings that reveal the actual subject of each section.
>  - [RFR]: When finally writing research-document: maintain a consistent, overarching idea throughout the research. Main ideas should run through the whole text, ensuring that there is meaning to be found between the lines.
>  - [AFR]: When finally writing article-document: maintain a consistent, overarching idea throughout each consistent section. Main ideas should run through the text of each section, ensuring that there is meaning to be found between the lines.
>  - [RFR] [AFR]: Keep substantive sections interpretable in isolation, preserving essential context, conditions, and limitations without unnecessary repetition.
>  - [RFR] [AFR]: Where applicable, bind time-sensitive claims to an explicit date, edition, or evaluation scope - avoid unqualified references to what is current, new, or latest.
>  - [RFR]: Place concise document-level metadata only immediately below the title (identify only functionally AI-useful details: data; terms, subject areas, domains, areas of responsibility, etc.); 
>  - [RFR] [AFR]: Below the title (or after the metadata if available), include 1-2 paragraphs of introductory information block - with identity of document purpose, scope, and status, distinguishing research, proposals, integrated provisions, and verified results.
>  - [RFR] [AFR]: After introductory block, provide classic table of contents for the main sections (no urls). For each item of content provide short explanatory route-text about the content of each section. 
>  - [RFR] [AFR]: Add numerical indexing in the document sections and provisions to improve navigation.
>  - [RFR] [AFR]: Where applicable, needed and relevant, list entities, rules, principes, laws, etc. through tables. Assign a code to each element — using a term, an abbreviation, an index, or a combination thereof—in the first column, which would facilitate future AI-based work.
>  - [AFR]: Articles must not contain references to external sources. Other projects by the same author may be mentioned in a neutral manner (without providing URLs, paths, directories, filenames, etc.).
>  - [AFR]: Sources in articles are permitted only if they belong to this specific corpus of articles. Articles may feature a navigational block of route-related sources at the top—predecessors and successors, including constituent parts. At the very bottom, there may be links to directly related articles.
>  - [SFR]: README.md files are concise, responsibility-oriented navigation routes. State the scope and guide readers to the relevant internal owners. 
>  - [SFR]: Do not include file inventories, document metadata blocks, mandatory introductions, tables of contents, volatile progress details, or duplicated substantive content. Include essential usage instructions where appropriate.
>  - [SFR]: When creating service files, system logs or directories for such logs, etc: you should anticipate a massive future volume—both in terms of the number of entries and file size. It is essential to plan for segmentation (or even granular, atomized partitioning, if convenient) based on functional/logical criteria or simple sequential ordering. If the directories are intended to store a collection of service files, you should assume that their number will grow significantly and design the directory structure accordingly.
>  - [SFR]: Do not create links to individual items in any catalog of files, as files may change dynamically.
>  - [SFR]: Service files and documents should contain precise, minimally necessary provisions and wording; examples may be included where needed, but only for the purpose of generalizing their functions and meaning.
>  - [TR]: When developing tests, you should anticipate that they will eventually expand considerably in both scale and execution time. Therefore, you should proactively segment and optimize them—including the structure of the associated files and directories—from the outset.
