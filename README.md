# INDEX — the global atlas of architects' registration bodies

**https://index.archi** · dataset: [`atlas.json`](https://index.archi/atlas.json) · licence **CC BY 4.0**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21819381.svg)](https://doi.org/10.5281/zenodo.21819381)

For each of **180 countries**: the official registration body (order, chamber, board,
council), whether registration is mandatory, whether the title *architect* is legally
protected, the **sourced and dated headcount**, the public register, downloadable open
datasets, and the alternative lists (member associations, directories) that allow
cross-checking. Every figure carries its source URL, its year, its nature, and an
**A–D quality grade**.

What this is *not*: a directory of persons. Name lists stay with their publishers —
linked, never copied.

**Why it exists.** No worldwide source breaks architects down by registration body.
The UIA claims 745,665 architects across 117 sections (Feb 2025) with no per-country
ventilation published anywhere. This atlas is that ventilation — reconstructible from
raw harvest files by two scripts, disputable line by line.

**Honest limits.** 91 of the 197 targeted jurisdictions are still grade D (estimate or
association list only): the southern half of the table is a work plan, honestly
labelled. Japan's kenchikushi figure is flagged non-comparable and excluded from sums.

## Data & docs

| File | What |
|---|---|
| [`atlas.json`](https://index.archi/atlas.json) | complete dataset — meta, 180 countries, federations, open-data catalogue |
| [`DATA.md`](DATA.md) | field-by-field schema, **derived** from the dataset |
| [`SOURCES.md`](SOURCES.md) | one line per country with the source URL of each headcount |
| [`MANUAL.md`](MANUAL.md) | the site's manual and how to rebuild everything |
| [`llms.txt`](https://index.archi/llms.txt) | machine-readable entry point for AI agents |

Rebuild: `python3 outils/carte.py && python3 outils/fusionner.py && python3 outils/documenter.py`
— the last one is a pre-publication bench that fails on any undocumented field or
diverging count.

## Corrections

Open an issue — corrections **from registration bodies themselves** are especially
welcome and are credited. Every figure can be disputed against its source URL.

## Cite

> Edberg Porporty (2026). *INDEX — World atlas of architects' registration bodies*.
> Zenodo. https://doi.org/10.5281/zenodo.21819381

The DOI above is the **concept DOI**: it always resolves to the latest version.
Each release also gets its own version DOI — `10.5281/zenodo.21819382` is v1.0.0.
Machine-readable citation: [`CITATION.cff`](CITATION.cff).

**Breaking change in v1.1.0** — `atlas.json` moved from French to English keys
(`effectif` → `headcount`, `qualite` → `grade`, `pays` → `country`, and so on;
the block `pays` became `countries`, `faitieres` became `umbrella_bodies`).
Anything built against v1.0.0 must be updated; v1.0.0 remains archived and
citable under its own DOI. The full field list is in [`DATA.md`](DATA.md).

---

## En français

Atlas de référence des organismes d'inscription des architectes : pour chaque pays,
l'organisme officiel, le régime (obligation d'inscription, protection du titre),
l'effectif **sourcé et daté**, le registre consultable, les jeux ouverts et les listes
alternatives. Chaque chiffre porte sa source, son année, sa nature et un grade A–D.
Ce que l'atlas n'est pas : un annuaire nominatif — les listes de personnes restent
chez leurs éditeurs, liées, jamais copiées. **91 pays sont en grade D** : la moitié
sud du tableau est un plan de travail, et le dit.

Le site est publié **en anglais** — langue de publication de l'atlas, qui s'adresse à
un lectorat international. Les noms d'organismes restent dans leur langue et chaque
pays garde son nom français (`country_fr`) : la recherche fonctionne en français comme
en anglais. Site autonome, hors ligne : [`index.html`](index.html) — manuel dans
[`MANUAL.md`](MANUAL.md). Compilation CC BY 4.0, Edberg Porporty (EDBERG.archi),
architecte DE-HMONP.
