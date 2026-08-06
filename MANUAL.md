# INDEX — the manual

A single-file reference site: for every country, the official body that registers
architects (order, chamber, board, council), the regime (compulsory registration,
title protection), the sourced and dated headcount, the searchable register, the
downloadable dataset where one exists, and the alternative lists (associations,
directories) that allow cross-checking.

**Language.** English is the language of publication — the site, the dataset and
the derived documents. Names of bodies are kept in their own language and are
never translated: *Ordre des Architectes du Sénégal*, *Камара на архитектите в
България*, *Lembaga Arkitek Malaysia*. Each country also carries its French name
(`country_fr`), so the site can be searched in either language.

## Opening it

`index.html` — self-contained, offline, no dependency (base map included).

- **World map** shaded by data grade: click a country to open its record.
- **Three charts that are controls**: continental shares of the headcount,
  coverage by grade, extremes of density. Click a segment to filter the table.
- **Filters with counters** — every chip announces what it would return, and
  chips that would return nothing are disabled; `× clear all` and `Esc` reset.
- **Every view is an address**: filters live in the `#hash`, `#p=SN` opens
  Senegal's record directly. A copyable link sits at the foot of every record.
- Search in English, in French or by ISO code (`NG`, `Allemagne`, `kenchikushi`).
- JSON and CSV export, **at the chosen scope** (the on-screen selection or the
  whole atlas), with provenance and the address of the view embedded.
- Light/dark, printable, `/` puts the cursor in the search box.

## Layout

    index.html          the site, data and geometry embedded
    atlas.json          canonical copy of the dataset, served at https://index.archi/atlas.json
    README.md           the repository front page
    MANUAL.md           this file
    SOURCES.md          DERIVED from the dataset by outils/fusionner.py — do not edit
    DATA.md             DERIVED from the dataset by outils/documenter.py — field-by-field schema
    CITATION.cff        machine-readable citation
    llms.txt            entry point for machine readers — hand-written, check it after a rebuild
    data/atlas.json     the full dataset (meta + countries + umbrella bodies + catalogue)
    data/carte.json     DERIVED from Natural Earth by outils/carte.py — do not edit
    data/agents/*.json  raw research harvests, by region (internal schema, French keys)
    data/*.csv|xlsx     raw nominal datasets downloaded — OUTSIDE the public repository
                        (GDPR), provenance kept in the catalogue
    outils/carte.py     world map: Natural Earth 110 m → simplified Equal Earth (54 KB)
    outils/fusionner.py merge + cross-checks (ACE, UIA) + injection into index.html
    outils/documenter.py pre-publication bench: derives DATA.md, refuses an undocumented
                        field or counts that disagree
    sauvegardes/        previous states of the site, dated (outside the repository)

## Rebuilding

    python3 outils/carte.py       # only if data/carte.json is missing
    python3 outils/fusionner.py
    python3 outils/documenter.py  # bench + DATA.md

`carte.py` projects the outlines in Equal Earth (an equal-area projection: areas
stay comparable), simplifies them, and puts micro-states out as points; it checks
that no country of the atlas ends up without geometry.
`fusionner.py` reloads `data/agents/*.json`, cross-checks against the ACE 2024
sector study and the list of UIA sections, recomputes missing grades, attaches the
English names, injects everything into `index.html` and re-derives `SOURCES.md`
(control count included).

`llms.txt` is the one document that is **not** derived: after a rebuild that
changes the grade counts, its figures must be corrected by hand or they drift.

## Two languages, one boundary

The working language of the workshop is French: the internal schema of
`data/agents/*.json` and the code keep their French field names. The **published**
artefacts — `atlas.json`, the exports, `SOURCES.md`, `DATA.md` and the site itself
— are English. The translation happens at a single boundary, the `CLES_EN` table,
which exists once in `outils/fusionner.py` and once in `index.html`. Nothing else
translates anything.

Country names follow the UN/ISO short forms, not the cartographic forms of the
base map: the `NOMS_EN` override table in `fusionner.py` carries the nine that
differ (Côte d'Ivoire, Czechia, Timor-Leste, Cabo Verde, Türkiye, China, United
States, Bahamas, Gambia) and survives any regeneration of `carte.json`.

## Out-of-scale figures

A headcount can be real, sourced and still not comparable. `HORS_ECHELLE` in
`fusionner.py` carries those cases — today only Japan, whose 383,923 first-class
*kenchikushi* licences are a cumulative stock that has never been cleared and is
mostly made up of engineers. Those figures stay displayed and sourced, but they
leave the totals, the continental shares and the gauge scale, and say so in the
country record.

## Quality grades

- **A** — nominal list downloadable in bulk (open data, roster, published register)
- **B** — public register searchable online (search by name)
- **C** — official headcount published, register not searchable
- **D** — estimate or association list only

## Licence

Compilation CC BY 4.0. Every datum remains the property of its source, cited line
by line (`headcount_source_url` column, and the records on the site).
