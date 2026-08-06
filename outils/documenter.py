#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDEX — dérive DATA.md (documentation du jeu) depuis data/atlas.json.

Règle de la maison : le document qui décrit est DÉRIVÉ de la source, jamais
rédigé à la main. Ce script est aussi le banc d'avant-publication :

  - il REFUSE un champ observé dans le jeu qui n'a pas de description ici ;
  - il REFUSE des copies atlas.json (racine / data/) qui divergent ;
  - il REFUSE un compte de pays qui ne concorde pas avec SOURCES.md.

Langue : atlas.json est l'artefact PUBLIÉ, donc à clés et à prose anglaises
(voir la frontière `en_anglais()` de fusionner.py). Ce script lit et écrit
donc en anglais ; seuls ses propres commentaires restent français.

Sortie : DATA.md (schéma champ par champ + recensements de vocabulaire
+ comptes de contrôle).
"""
import json, os, re, sys, collections

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# La seule partie rédigée : le SENS des champs. Tout le reste est mesuré.
DESCRIPTIONS = {
    "iso2":                    "ISO 3166-1 alpha-2 code — the key of the dataset.",
    "country":                 "Country name in English, as published by this atlas (UN/ISO short forms).",
    "country_fr":              "Country name in French — kept so the site can be searched in either language.",
    "continent":               "Continent (vocabulary counted below).",
    "body":                    "Official registration body (order, chamber, board, council…). `null` = no body identified. Names of bodies are given in their own language, never translated.",
    "acronym":                 "Usual acronym of the body.",
    "body_type":               "Nature of the body (vocabulary counted below).",
    "compulsory_registration": "Does registration condition the right to practise? `null` = not established.",
    "protected_title":         "Is the title « architect » protected by law? `null` = not established.",
    "uia_member":              "Does the country have a UIA member section?",
    "uia_section":             "Name of the UIA section when it differs from the registration body.",
    "headcount":               "Architects registered with the official body — see `headcount_source_type`. `null` = not published. What the atlas counts: REGISTRANTS, not graduates and not de facto practitioners.",
    "headcount_year":          "Year of the figure.",
    "headcount_source_url":    "Source of the figure — every headcount carries one (no figure without a source).",
    "headcount_source_type":   "Nature of the source of the figure (vocabulary counted below).",
    "ace_headcount_2024":      "Cross-check: headcount for the same country in the ACE 2024 sector study (Europe) — a SECOND measurement, not ours; the gap with `headcount` is readable in the country record.",
    "register_url":            "Public searchable register, where one exists.",
    "register_searchable":     "Does the register offer a public search by name?",
    "open_data_url":           "Dataset downloadable in bulk (open data, roster), where one exists.",
    "open_data_format":        "Format of the downloadable dataset (CSV, XLSX, PDF…).",
    "alternative_lists":       "NON-official lists (associations such as RIBA or AIA, directories) that allow cross-checking — never conflated with the register.",
    "grade":                   "Data quality grade: A = nominal list downloadable in bulk · B = public register searchable online · C = official headcount published, register not searchable · D = estimate or association list only.",
    "population_m":            "UN 2024 population (millions, rounded) — used only for the indicative density.",
    "notes":                   "Country-specific reading notes (scope, traps, cross-checks).",
    "out_of_scale":            "Present when the headcount, real and sourced, does NOT compare with the others (e.g. Japan: cumulative kenchikushi stock) — it leaves the totals and the gauges, and the reason is given.",
}

def types_de(valeurs):
    """Recense les types JSON observés (hors null) + présence de null."""
    t = set()
    nuls = 0
    for v in valeurs:
        if v is None: nuls += 1
        elif isinstance(v, bool): t.add("bool")
        elif isinstance(v, int): t.add("integer")
        elif isinstance(v, float): t.add("number")
        elif isinstance(v, str): t.add("string")
        elif isinstance(v, list): t.add("list")
        elif isinstance(v, dict): t.add("object")
    return sorted(t), nuls

def principal():
    atlas_data = os.path.join(RACINE, "data", "atlas.json")
    atlas_racine = os.path.join(RACINE, "atlas.json")

    # Banc 1 — les deux copies d'atlas.json sont identiques à l'octet.
    with open(atlas_data, "rb") as f: octets_data = f.read()
    if not os.path.exists(atlas_racine):
        sys.exit("ÉCHEC : atlas.json manquant à la racine — lancer outils/fusionner.py")
    with open(atlas_racine, "rb") as f:
        if f.read() != octets_data:
            sys.exit("ÉCHEC : atlas.json (racine) diverge de data/atlas.json — relancer outils/fusionner.py")

    d = json.loads(octets_data)
    pays = d["countries"]

    # Banc 2 — tout champ observé est documenté.
    champs = collections.Counter()
    for p in pays:
        for k in p: champs[k] += 1
    inconnus = sorted(set(champs) - set(DESCRIPTIONS))
    if inconnus:
        sys.exit(f"ÉCHEC : champ(s) non documenté(s) dans documenter.py : {', '.join(inconnus)}")
    fantomes = sorted(set(DESCRIPTIONS) - set(champs))
    if fantomes:
        sys.exit(f"ÉCHEC : description(s) sans champ observé : {', '.join(fantomes)}")

    # Banc 3 — concordance avec SOURCES.md.
    with open(os.path.join(RACINE, "SOURCES.md"), encoding="utf-8") as f:
        m = re.search(r"Control count: (\d+) countries", f.read())
    if not m or int(m.group(1)) != len(pays):
        sys.exit(f"ÉCHEC : SOURCES.md annonce {m.group(1) if m else '?'} pays, atlas.json en porte {len(pays)}")

    # Recensements (mesurés, jamais rédigés).
    n_eff = sum(1 for p in pays if p.get("headcount") is not None)
    grades = collections.Counter(p.get("grade") for p in pays)
    continents = collections.Counter(p.get("continent") for p in pays)
    natures = collections.Counter(p.get("headcount_source_type") for p in pays if p.get("headcount_source_type"))
    types_org = collections.Counter(p.get("body_type") for p in pays if p.get("body_type"))

    L = []
    L.append("# DATA — the schema of atlas.json")
    L.append("")
    L.append("DERIVED from `data/atlas.json` by `outils/documenter.py` — DO NOT EDIT BY HAND.")
    L.append("")
    L.append("Dataset served at the stable address **https://index.archi/atlas.json** (UTF-8, CC BY 4.0).")
    L.append(f"Compiled on {d['meta']['compiled_on']}. **Control count: {len(pays)} countries** "
             f"(agrees with SOURCES.md), {n_eff} sourced headcounts, "
             f"A:{grades.get('A',0)} B:{grades.get('B',0)} C:{grades.get('C',0)} D:{grades.get('D',0)}.")
    L.append("")
    L.append("## Structure")
    L.append("")
    L.append("| Block | Type | Contents |")
    L.append("|---|---|---|")
    L.append(f"| `meta` | object | compilation date, targeted scope ({d['meta']['countries_targeted']} jurisdictions), method in {len(d['meta']['method'])} points, UIA claim |")
    L.append(f"| `countries` | list ({len(pays)}) | one entry per country — schema below |")
    L.append(f"| `umbrella_bodies` | object ({len(d['umbrella_bodies'])}) | umbrella organisations (UIA, ACE, CAA, AUA…) with their sourced claims |")
    L.append(f"| `catalogue` | list ({len(d['catalogue'])}) | public datasets recorded (publisher, format, URL) |")
    L.append("")
    L.append("## Fields of a `countries` entry")
    L.append("")
    L.append("| Field | Types | Filled | Description |")
    L.append("|---|---|---:|---|")
    for k in sorted(champs, key=lambda k: (-champs[k], k)):
        t, nuls = types_de([p.get(k) for p in pays if k in p])
        L.append(f"| `{k}` | {', '.join(t) or '—'} | {champs[k] - nuls}/{len(pays)} | {DESCRIPTIONS[k]} |")
    L.append("")
    L.append("## Vocabularies counted")
    L.append("")
    L.append("**`grade`**: " + " · ".join(f"{g} ({n})" for g, n in sorted(grades.items(), key=lambda x: x[0] or 'Z')))
    L.append("")
    L.append("**`continent`**: " + " · ".join(f"{c} ({n})" for c, n in continents.most_common()))
    L.append("")
    L.append("**`headcount_source_type`**: " + " · ".join(f"`{c}` ({n})" for c, n in natures.most_common()))
    L.append("")
    L.append("**`body_type`**: " + " · ".join(f"`{c}` ({n})" for c, n in types_org.most_common()))
    L.append("")
    L.append("## Reading this honestly")
    L.append("")
    L.append("- Comparing countries = comparing **registrants on the official register**, never graduates and never de facto practitioners.")
    L.append("- Entries carrying `out_of_scale` stay displayed and sourced but leave the totals and the scales.")
    L.append(f"- **{grades.get('D',0)} countries are at grade D** (estimate or association only): that half of the table is a work plan, not a result.")
    L.append("- No personal data in this dataset or in this repository — lists of named individuals stay with their publishers, linked from the catalogue.")
    L.append("")

    with open(os.path.join(RACINE, "DATA.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"OK — DATA.md dérivé : {len(champs)} champs documentés, {len(pays)} pays, "
          f"copies atlas.json identiques, concordance SOURCES.md.")

if __name__ == "__main__":
    principal()
