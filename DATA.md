# DATA — the schema of atlas.json

DERIVED from `data/atlas.json` by `outils/documenter.py` — DO NOT EDIT BY HAND.

Dataset served at the stable address **https://index.archi/atlas.json** (UTF-8, CC BY 4.0).
Compiled on 6 August 2026. **Control count: 180 countries** (agrees with SOURCES.md), 88 sourced headcounts, A:26 B:54 C:9 D:91.

## Structure

| Block | Type | Contents |
|---|---|---|
| `meta` | object | compilation date, targeted scope (197 jurisdictions), method in 6 points, UIA claim |
| `countries` | list (180) | one entry per country — schema below |
| `umbrella_bodies` | object (8) | umbrella organisations (UIA, ACE, CAA, AUA…) with their sourced claims |
| `catalogue` | list (36) | public datasets recorded (publisher, format, URL) |

## Fields of a `countries` entry

| Field | Types | Filled | Description |
|---|---|---:|---|
| `acronym` | string | 135/180 | Usual acronym of the body. |
| `alternative_lists` | list | 180/180 | NON-official lists (associations such as RIBA or AIA, directories) that allow cross-checking — never conflated with the register. |
| `body` | string | 180/180 | Official registration body (order, chamber, board, council…). `null` = no body identified. Names of bodies are given in their own language, never translated. |
| `body_type` | string | 180/180 | Nature of the body (vocabulary counted below). |
| `compulsory_registration` | bool | 140/180 | Does registration condition the right to practise? `null` = not established. |
| `continent` | string | 180/180 | Continent (vocabulary counted below). |
| `country` | string | 180/180 | Country name in English, as published by this atlas (UN/ISO short forms). |
| `country_fr` | string | 180/180 | Country name in French — kept so the site can be searched in either language. |
| `grade` | string | 180/180 | Data quality grade: A = nominal list downloadable in bulk · B = public register searchable online · C = official headcount published, register not searchable · D = estimate or association list only. |
| `headcount` | integer | 88/180 | Architects registered with the official body — see `headcount_source_type`. `null` = not published. What the atlas counts: REGISTRANTS, not graduates and not de facto practitioners. |
| `headcount_source_type` | string | 88/180 | Nature of the source of the figure (vocabulary counted below). |
| `headcount_source_url` | string | 90/180 | Source of the figure — every headcount carries one (no figure without a source). |
| `headcount_year` | integer | 84/180 | Year of the figure. |
| `iso2` | string | 180/180 | ISO 3166-1 alpha-2 code — the key of the dataset. |
| `notes` | string | 180/180 | Country-specific reading notes (scope, traps, cross-checks). |
| `open_data_format` | string | 24/180 | Format of the downloadable dataset (CSV, XLSX, PDF…). |
| `open_data_url` | string | 33/180 | Dataset downloadable in bulk (open data, roster), where one exists. |
| `population_m` | number | 180/180 | UN 2024 population (millions, rounded) — used only for the indicative density. |
| `protected_title` | bool | 105/180 | Is the title « architect » protected by law? `null` = not established. |
| `register_searchable` | bool | 100/180 | Does the register offer a public search by name? |
| `register_url` | string | 94/180 | Public searchable register, where one exists. |
| `uia_member` | bool | 179/180 | Does the country have a UIA member section? |
| `uia_section` | string | 117/180 | Name of the UIA section when it differs from the registration body. |
| `ace_headcount_2024` | integer | 32/180 | Cross-check: headcount for the same country in the ACE 2024 sector study (Europe) — a SECOND measurement, not ours; the gap with `headcount` is readable in the country record. |
| `out_of_scale` | string | 1/180 | Present when the headcount, real and sourced, does NOT compare with the others (e.g. Japan: cumulative kenchikushi stock) — it leaves the totals and the gauges, and the reason is given. |

## Vocabularies counted

**`grade`**: A (26) · B (54) · C (9) · D (91)

**`continent`**: Africa (53) · Europe (49) · Asia (45) · Americas (29) · Oceania (4)

**`headcount_source_type`**: `register` (39) · `official_report` (22) · `press` (14) · `sector_study` (9) · `estimate` (3) · `electoral_roll` (1)

**`body_type`**: `order` (41) · `state_register` (28) · `association` (26) · `board` (23) · `none` (16) · `chamber` (16) · `council` (15) · `engineers_union` (15)

## Reading this honestly

- Comparing countries = comparing **registrants on the official register**, never graduates and never de facto practitioners.
- Entries carrying `out_of_scale` stay displayed and sourced but leave the totals and the scales.
- **91 countries are at grade D** (estimate or association only): that half of the table is a work plan, not a result.
- No personal data in this dataset or in this repository — lists of named individuals stay with their publishers, linked from the catalogue.
