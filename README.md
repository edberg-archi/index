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
| [`DONNEES.md`](DONNEES.md) | field-by-field schema (FR), **derived** from the dataset |
| [`SOURCES.md`](SOURCES.md) | one line per country with the source URL of each headcount |
| [`LISEZMOI.md`](LISEZMOI.md) | the site's manual (FR) and how to rebuild everything |
| [`llms.txt`](https://index.archi/llms.txt) | machine-readable entry point for AI agents |

Rebuild: `python3 outils/carte.py && python3 outils/fusionner.py && python3 outils/documenter.py`
— the last one is a pre-publication bench that fails on any undocumented field or
diverging count.

## Corrections

Open an issue — corrections **from registration bodies themselves** are especially
welcome and are credited. Every figure can be disputed against its source URL.

## Cite

> Edberg Porporty (2026). *INDEX — Atlas mondial des ordres et registres
> d'architectes*. Zenodo. https://doi.org/10.5281/zenodo.21819381

The DOI above is the **concept DOI**: it always resolves to the latest version.
To cite this exact release, use `10.5281/zenodo.21819382` (v1.0.0).
Machine-readable citation: [`CITATION.cff`](CITATION.cff).

---

## En français

Atlas de référence des organismes d'inscription des architectes : pour chaque pays,
l'organisme officiel, le régime (obligation d'inscription, protection du titre),
l'effectif **sourcé et daté**, le registre consultable, les jeux ouverts et les listes
alternatives. Chaque chiffre porte sa source, son année, sa nature et un grade A–D.
Ce que l'atlas n'est pas : un annuaire nominatif — les listes de personnes restent
chez leurs éditeurs, liées, jamais copiées. **91 pays sont en grade D** : la moitié
sud du tableau est un plan de travail, et le dit.

Site en français, autonome, hors ligne : [`index.html`](index.html) — manuel dans
[`LISEZMOI.md`](LISEZMOI.md). Compilation CC BY 4.0, Edberg Porporty (EDBERG.archi),
architecte DE-HMONP.
