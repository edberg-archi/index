#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDEX — dérive DONNEES.md (documentation du jeu) depuis data/atlas.json.

Règle de la maison : le document qui décrit est DÉRIVÉ de la source, jamais
rédigé à la main. Ce script est aussi le banc d'avant-publication :

  - il REFUSE un champ observé dans le jeu qui n'a pas de description ici ;
  - il REFUSE des copies atlas.json (racine / data/) qui divergent ;
  - il REFUSE un compte de pays qui ne concorde pas avec SOURCES.md.

Sortie : DONNEES.md (schéma champ par champ + recensements de vocabulaire
+ comptes de contrôle).
"""
import json, os, re, sys, collections

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# La seule partie rédigée : le SENS des champs. Tout le reste est mesuré.
DESCRIPTIONS = {
    "iso2":                     "Code ISO 3166-1 alpha-2 — la clé du jeu.",
    "pays":                     "Nom du pays en français.",
    "nom_en":                   "Nom anglais (sert la recherche) — présent quand il diffère du français.",
    "continent":                "Continent (vocabulaire recensé ci-dessous).",
    "organisme":                "Organisme officiel d'inscription (ordre, chambre, board, conseil…). `null` = aucun organisme identifié.",
    "sigle":                    "Sigle usuel de l'organisme.",
    "type_organisme":           "Nature de l'organisme (vocabulaire recensé ci-dessous).",
    "inscription_obligatoire":  "L'inscription conditionne-t-elle l'exercice ? `null` = non établi.",
    "titre_protege":            "Le titre « architecte » est-il protégé par la loi ? `null` = non établi.",
    "uia_membre":               "Le pays a-t-il une section membre de l'UIA ?",
    "uia_section":              "Nom de la section UIA quand elle diffère de l'organisme d'inscription.",
    "effectif":                 "Inscrits auprès de l'organisme officiel — voir `effectif_nature`. `null` = non publié. Ce que compte l'atlas : des INSCRITS, pas des diplômés ni des praticiens de fait.",
    "effectif_annee":           "Année du chiffre.",
    "effectif_source_url":      "Source du chiffre — chaque effectif la porte (aucun chiffre sans source).",
    "effectif_nature":          "Nature de la source du chiffre (vocabulaire recensé ci-dessous).",
    "ace_effectif_2024":        "Recoupement : effectif du même pays dans l'étude sectorielle ACE 2024 (Europe) — une DEUXIÈME mesure, pas la nôtre ; l'écart avec `effectif` se lit en fiche.",
    "registre_url":             "Registre public consultable, quand il existe.",
    "registre_recherche_publique": "Le registre offre-t-il une recherche nominative publique ?",
    "donnees_ouvertes_url":     "Jeu de données téléchargeable en masse (open data, roster), quand il existe.",
    "donnees_ouvertes_format":  "Format du jeu téléchargeable (CSV, XLSX, PDF…).",
    "alternatives":             "Listes NON officielles (associations type RIBA/AIA, annuaires) qui permettent de recouper — jamais confondues avec le registre.",
    "qualite":                  "Grade de qualité de la donnée : A = liste nominative téléchargeable en masse · B = registre public consultable · C = effectif officiel publié, registre non consultable · D = estimation ou liste d'association seulement.",
    "population_m":             "Population ONU 2024 (millions, arrondie) — sert uniquement la densité indicative.",
    "notes":                    "Précisions de lecture propres au pays (périmètre, pièges, recoupements).",
    "hors_echelle":             "Présent quand l'effectif, réel et sourcé, ne se COMPARE pas aux autres (ex. Japon : stock cumulé kenchikushi) — il sort des sommes et des jauges, et le motif est donné.",
}

def types_de(valeurs):
    """Recense les types JSON observés (hors null) + présence de null."""
    t = set()
    nuls = 0
    for v in valeurs:
        if v is None: nuls += 1
        elif isinstance(v, bool): t.add("bool")
        elif isinstance(v, int): t.add("entier")
        elif isinstance(v, float): t.add("nombre")
        elif isinstance(v, str): t.add("texte")
        elif isinstance(v, list): t.add("liste")
        elif isinstance(v, dict): t.add("objet")
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
    pays = d["pays"]

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
        m = re.search(r"Compte de contrôle : (\d+) pays", f.read())
    if not m or int(m.group(1)) != len(pays):
        sys.exit(f"ÉCHEC : SOURCES.md annonce {m.group(1) if m else '?'} pays, atlas.json en porte {len(pays)}")

    # Recensements (mesurés, jamais rédigés).
    n_eff = sum(1 for p in pays if p.get("effectif") is not None)
    grades = collections.Counter(p.get("qualite") for p in pays)
    continents = collections.Counter(p.get("continent") for p in pays)
    natures = collections.Counter(p.get("effectif_nature") for p in pays if p.get("effectif_nature"))
    types_org = collections.Counter(p.get("type_organisme") for p in pays if p.get("type_organisme"))

    L = []
    L.append("# DONNÉES — schéma d'atlas.json")
    L.append("")
    L.append("DÉRIVÉ de `data/atlas.json` par `outils/documenter.py` — NE PAS ÉDITER À LA MAIN.")
    L.append("")
    L.append(f"Jeu servi à l'adresse stable **https://index.archi/atlas.json** (UTF-8, licence CC BY 4.0).")
    L.append(f"Constitué le {d['meta']['constitue_le']}. **Compte de contrôle : {len(pays)} pays** "
             f"(concorde avec SOURCES.md), {n_eff} effectifs sourcés, "
             f"A:{grades.get('A',0)} B:{grades.get('B',0)} C:{grades.get('C',0)} D:{grades.get('D',0)}.")
    L.append("")
    L.append("## Structure")
    L.append("")
    L.append("| Bloc | Type | Contenu |")
    L.append("|---|---|---|")
    L.append(f"| `meta` | objet | date de constitution, périmètre visé ({d['meta']['pays_vises']} juridictions), méthode en {len(d['meta']['methode'])} points, revendication UIA |")
    L.append(f"| `pays` | liste ({len(pays)}) | une entrée par pays — schéma ci-dessous |")
    L.append(f"| `faitieres` | objet ({len(d['faitieres'])}) | organisations faîtières (UIA, ACE, CAA, AUA…) avec leurs revendications sourcées |")
    L.append(f"| `catalogue` | liste ({len(d['catalogue'])}) | jeux de données publics recensés (éditeur, format, URL) |")
    L.append("")
    L.append("## Champs d'une entrée `pays`")
    L.append("")
    L.append("| Champ | Types | Renseigné | Description |")
    L.append("|---|---|---:|---|")
    for k in sorted(champs, key=lambda k: (-champs[k], k)):
        t, nuls = types_de([p.get(k) for p in pays if k in p])
        L.append(f"| `{k}` | {', '.join(t) or '—'} | {champs[k] - nuls}/{len(pays)} | {DESCRIPTIONS[k]} |")
    L.append("")
    L.append("## Vocabulaires recensés")
    L.append("")
    L.append("**`qualite`** : " + " · ".join(f"{g} ({n})" for g, n in sorted(grades.items(), key=lambda x: x[0] or 'Z')))
    L.append("")
    L.append("**`continent`** : " + " · ".join(f"{c} ({n})" for c, n in continents.most_common()))
    L.append("")
    L.append("**`effectif_nature`** : " + " · ".join(f"`{c}` ({n})" for c, n in natures.most_common()))
    L.append("")
    L.append("**`type_organisme`** : " + " · ".join(f"`{c}` ({n})" for c, n in types_org.most_common()))
    L.append("")
    L.append("## Lecture honnête")
    L.append("")
    L.append("- Comparer des pays = comparer des **inscrits au registre officiel**, jamais des diplômés ni des praticiens de fait.")
    L.append("- Les entrées portant `hors_echelle` restent affichées et sourcées mais sortent des sommes et des échelles.")
    L.append(f"- **{grades.get('D',0)} pays sont en grade D** (estimation ou association seulement) : cette moitié du tableau est un plan de travail, pas un résultat.")
    L.append("- Aucune donnée nominative dans ce jeu ni dans ce dépôt — les listes de personnes restent chez leurs éditeurs, liées par le catalogue.")
    L.append("")

    with open(os.path.join(RACINE, "DONNEES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"OK — DONNEES.md dérivé : {len(champs)} champs documentés, {len(pays)} pays, "
          f"copies atlas.json identiques, concordance SOURCES.md.")

if __name__ == "__main__":
    principal()
