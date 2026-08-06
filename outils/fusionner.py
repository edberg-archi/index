#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDEX — fusion des moissons d'agents en un jeu unique, injecté dans index.html.

Entrées : data/agents/*.json   (fichiers {"rows":[...]} par région + faitieres.json)
Sorties : data/atlas.json      (jeu complet publié, CLÉS ANGLAISES)
          index.html           (données injectées entre marqueurs, clés internes)
          SOURCES.md           (dérivé du jeu — jamais rédigé à la main)

Règle de la maison : le document qui décrit est DÉRIVÉ de la source ;
SOURCES.md porte un compte qui doit concorder avec atlas.json.

LANGUE (décidé le 06.08.2026) : la langue de PUBLICATION est l'anglais — tout ce
qu'un lecteur voit, ici comme dans index.html. Le code et son schéma interne
restent français, langue de travail de l'atelier ; la traduction se fait à la
FRONTIÈRE, dans `en_anglais()`, au moment d'écrire atlas.json. Une seule table
de clés, côté Python comme côté JS (constante CLES_EN d'index.html).
"""
import json, glob, os, re, sys, datetime

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_AGENTS = os.path.join(RACINE, "data", "agents")
CHEMIN_HTML = os.path.join(RACINE, "index.html")

CONSTITUE_LE = "6 August 2026"

# Frontière de publication : schéma interne (français) → jeu publié (anglais).
CLES_EN = {
 "iso2":"iso2", "nom_en":"country", "pays":"country_fr", "continent":"continent",
 "organisme":"body", "sigle":"acronym", "type_organisme":"body_type",
 "inscription_obligatoire":"compulsory_registration", "titre_protege":"protected_title",
 "uia_membre":"uia_member", "uia_section":"uia_section",
 "effectif":"headcount", "effectif_annee":"headcount_year",
 "effectif_nature":"headcount_source_type", "effectif_source_url":"headcount_source_url",
 "ace_effectif_2024":"ace_headcount_2024",
 "registre_url":"register_url", "registre_recherche_publique":"register_searchable",
 "donnees_ouvertes_url":"open_data_url", "donnees_ouvertes_format":"open_data_format",
 "alternatives":"alternative_lists", "population_m":"population_m",
 "qualite":"grade", "hors_echelle":"out_of_scale", "notes":"notes",
}
CLES_META_EN = {"constitue_le":"compiled_on", "pays_vises":"countries_targeted",
                "signature":"method_signature", "uia":"uia", "methode":"method"}

def en_anglais(p, table):
    """Renomme les clés d'un enregistrement pour la publication. Une clé absente
    de la table sortirait en silence : on la garde telle quelle et on la signale."""
    inconnues = [k for k in p if k not in table]
    if inconnues:
        print("  ! clés hors table de publication (laissées telles quelles) :", " ".join(inconnues))
    return {table.get(k, k): v for k, v in p.items()}

# Population ONU 2024, millions, arrondie — sert UNIQUEMENT à la densité indicative.
POP_M = {
 "FR":66.5,"GB":69.1,"DE":84.5,"IT":58.9,"ES":48.4,"PT":10.4,"BE":11.8,"NL":18.0,"LU":0.67,
 "IE":5.3,"AT":9.1,"CH":8.9,"LI":0.04,"MC":0.04,"AD":0.08,"SE":10.6,"NO":5.5,"DK":6.0,
 "FI":5.6,"IS":0.39,"EE":1.37,"LV":1.87,"LT":2.87,"PL":38.0,"CZ":10.9,"SK":5.4,"HU":9.6,
 "RO":19.0,"BG":6.4,"HR":3.85,"SI":2.12,"RS":6.6,"BA":3.2,"ME":0.62,"MK":1.8,"AL":2.7,
 "XK":1.66,"MD":2.5,"UA":37.9,"BY":9.0,"RU":144.0,"TR":85.5,"GE":3.7,"AM":3.0,"AZ":10.2,
 "KZ":20.0,"UZ":36.0,"KG":7.1,"TJ":10.1,"TM":6.5,"GR":10.3,"MT":0.55,"CY":1.26,"SM":0.03,
 "MA":37.5,"DZ":46.0,"TN":12.3,"LY":6.9,"MR":4.9,"SN":18.0,"ML":23.5,"BF":23.0,"NE":27.0,
 "CI":29.0,"TG":9.2,"BJ":14.0,"GN":14.0,"GW":2.1,"CM":28.5,"GA":2.5,"CG":6.1,"CD":105.0,
 "TD":18.5,"CF":5.7,"MG":30.5,"DJ":1.1,"KM":0.85,"BI":13.5,"RW":14.0,"NG":227.0,"GH":34.0,
 "KE":55.0,"UG":48.5,"TZ":67.0,"ZA":63.0,"ZM":21.0,"ZW":16.5,"BW":2.5,"NA":2.6,"MW":21.0,
 "ET":128.0,"ER":3.5,"SO":18.0,"SD":49.0,"SS":11.0,"SL":8.8,"LR":5.5,"GM":2.7,"MZ":34.0,
 "AO":37.0,"CV":0.52,"ST":0.23,"MU":1.26,"SC":0.12,"LS":2.3,"SZ":1.2,"EG":114.0,
 "US":341.0,"CA":39.0,"MX":129.5,"GT":18.0,"BZ":0.41,"SV":6.3,"HN":10.6,"NI":7.0,"CR":5.2,
 "PA":4.5,"CU":11.0,"DO":11.3,"HT":11.7,"JM":2.8,"TT":1.5,"BB":0.28,"BS":0.41,"GY":0.81,
 "SR":0.62,"BR":211.0,"AR":46.0,"CL":19.7,"CO":52.0,"PE":34.0,"EC":18.0,"UY":3.4,"PY":6.9,
 "BO":12.4,"VE":28.3,
 "JP":123.5,"CN":1419.0,"KR":51.7,"KP":26.0,"TW":23.4,"HK":7.5,"MO":0.7,"MN":3.5,"SG":5.9,
 "MY":34.0,"TH":71.7,"VN":100.0,"PH":114.0,"ID":279.0,"MM":54.5,"KH":17.0,"LA":7.6,"BN":0.45,
 "TL":1.4,"AU":26.6,"NZ":5.2,"PG":10.5,"FJ":0.93,"IN":1442.0,"PK":245.0,"BD":173.0,"LK":22.0,
 "NP":30.5,"BT":0.79,"MV":0.52,"AF":42.0,"IR":89.0,"IQ":45.5,"SY":24.0,"LB":5.8,"JO":11.4,
 "PS":5.5,"IL":9.8,"SA":33.0,"AE":10.0,"QA":2.7,"KW":4.9,"BH":1.5,"OM":4.6,"YE":34.5,
}

def charger():
    lignes, faitieres = {}, None
    for chemin in sorted(glob.glob(os.path.join(DOSSIER_AGENTS, "*.json"))):
        with open(chemin, encoding="utf-8") as f:
            d = json.load(f)
        if os.path.basename(chemin) == "faitieres.json":
            faitieres = d; continue
        for r in d.get("rows", []):
            iso = (r.get("iso2") or "").upper()
            if not iso:
                continue
            if iso in lignes:  # doublon inter-régions : garde la ligne la plus renseignée
                a, b = lignes[iso], r
                na = sum(1 for v in a.values() if v not in (None, "", []))
                nb = sum(1 for v in b.values() if v not in (None, "", []))
                r = b if nb >= na else a
            lignes[iso] = r
    return lignes, faitieres

def croiser(lignes, faitieres):
    uia_par_iso = {s["iso2"]: s for s in (faitieres or {}).get("uia", {}).get("sections", [])}
    ace = {e["iso2"]: e["effectif"] for e in (faitieres or {}).get("ace", {}).get("effectifs_par_pays", [])}
    ace_url = (faitieres or {}).get("ace", {}).get("etude_url")
    for iso, p in lignes.items():
        p["population_m"] = POP_M.get(iso)
        # UIA : la liste des sections fait foi quand l'agent n'a pas conclu
        if iso in uia_par_iso:
            if p.get("uia_membre") is None: p["uia_membre"] = True
            p["uia_section"] = uia_par_iso[iso]["organisme"]
        # ACE : recoupement, et bouche-trou sourcé quand l'organisme ne publie rien
        if iso in ace:
            p["ace_effectif_2024"] = ace[iso]
            if p.get("effectif") is None:
                p["effectif"] = ace[iso]; p["effectif_annee"] = 2024
                p["effectif_nature"] = "sector_study"; p["effectif_source_url"] = ace_url
                p["notes"] = ((p.get("notes") or "") +
                    " Headcount taken from the ACE 2024 sector study, the body itself publishing none.").strip()
                if p.get("qualite") in (None, "", "D"): p["qualite"] = "C"
        if not p.get("qualite"): p["qualite"] = "D"
    return lignes

def catalogue_depuis(lignes, catalogue_local):
    vus = {(c.get("pays"), c.get("url")) for c in catalogue_local}
    cat = list(catalogue_local)
    for p in sorted(lignes.values(), key=lambda x: nom_publie(x)):
        if p.get("donnees_ouvertes_url") and (nom_publie(p), p["donnees_ouvertes_url"]) not in vus:
            cat.append({"pays": nom_publie(p), "jeu": "Register / data of " + (p.get("sigle") or p.get("organisme") or "the body"),
                        "format": p.get("donnees_ouvertes_format") or "—",
                        "editeur": p.get("organisme"), "url": p["donnees_ouvertes_url"], "etat": "online"})
    return cat

CATALOGUE_LOCAL = [
 {"pays":"United States — Texas","jeu":"Full roster of active architects (TBAE, live)","format":"XLSX→CSV",
  "editeur":"Texas Board of Architectural Examiners",
  "url":"https://indreg.tbae.texas.gov/Reports/RegistrantRosters","livre":"data/us-texas-tbae-architectes.csv (14,575 registrants)"},
 {"pays":"Singapore","jeu":"Official register of architects (BOA) — state open data","format":"CSV",
  "editeur":"Board of Architects via data.gov.sg",
  "url":"https://data.gov.sg/datasets/d_d77de0f78ca589a5c61da7a60fdee6ba/view","livre":"data/sg-boa-registre-architectes.csv (1,999 registrants)"},
 {"pays":"Europe (32 countries)","jeu":"ACE Sector Study 2024 — headcounts by country (table 1-1)","format":"PDF",
  "editeur":"Architects' Council of Europe","url":"https://ace-cae.eu/wp-content/uploads/2025/04/2024-ACE-Sector-Study-EN-04042025.pdf",
  "etat":"extracted into the atlas"},
 {"pays":"World","jeu":"UIA — official presentation: 117 sections, ~745,665 architects","format":"PDF",
  "editeur":"International Union of Architects",
  "url":"https://www.uia-architectes.org/wp-content/uploads/2025/02/2-2025-UIA-presentation.pdf","etat":"extracted into the atlas"},
]

def faitieres_site(f):
    u, a = f.get("uia", {}), f.get("ace", {})
    return [
      {"sigle":"UIA","nom":"International Union of Architects — 5 regions, the global umbrella",
       "url":u.get("membres_url"),"chiffre":f"<b>{u.get('sections_revendiquees','—')}</b> sections · <b class='num'>{format(u.get('architectes_revendiques',0),',')}</b> architects claimed ({u.get('pays_revendiques','—')} countries)",
       "note":"Official presentation, February 2025 — the « 3.2 M » sometimes quoted is not found in any UIA source."},
      {"sigle":"ACE","nom":"Architects' Council of Europe — biennial sector study",
       "url":a.get("etude_page"),"chiffre":f"<b class='num'>{format(a.get('total_architectes_europe',0),',')}</b> architects in Europe-32 (2024)",
       "note":"Table 1-1 taken country by country into the atlas."},
      {"sigle":"CAA","nom":"Commonwealth Association of Architects",
       "url":f.get("caa",{}).get("url"),"chiffre":f"<b>{f.get('caa',{}).get('nb_membres_listes','—')}</b> member institutes listed","note":None},
      {"sigle":"AUA","nom":"African Union of Architects",
       "url":f.get("aua",{}).get("url"),"chiffre":"<b>43</b> sections claimed · > 70,000 architects","note":"No nominal list published online."},
      {"sigle":"FPAA","nom":"Federación Panamericana de Asociaciones de Arquitectos",
       "url":f.get("fpaa",{}).get("url"),"chiffre":"<b>32</b> countries · « casi 1 millón de arquitectos »","note":"Claim not broken down; no list published."},
      {"sigle":"ARCASIA","nom":"Architects Regional Council Asia",
       "url":f.get("arcasia",{}).get("url"),"chiffre":"<b>24</b> member institutes (zones A, B, C)","note":None},
      {"sigle":"UMAR","nom":"Mediterranean Union of Architects",
       "url":f.get("umar",{}).get("url"),"chiffre":"<b>14</b> member countries","note":"Rabat Declaration, 1994."},
    ]

METHODE = [
 ["What this atlas counts",
  "Architects REGISTERED with the official body of their country — not graduates, not de facto practitioners. Where registration runs through an engineers' union (glyph ▤), the architecture division's own headcount is given when one exists."],
 ["Grades A · B · C · D",
  "A — nominal list downloadable in bulk (open data, roster, published register). B — public register searchable online, no download. C — official headcount published, register not searchable. D — estimate or association list only."],
 ["Cross-checks",
  "Every headcount is dated and sourced (link in the record). Europe: cross-checked against the ACE 2024 sector study. World: set against the list of the UIA's 117 member sections. Alternative lists (associations such as RIBA or AIA, directories) are given country by country."],
 ["Known traps",
  "Japan: the ~370,000 first-class kenchikushi are mostly building engineers — the figure is not comparable to an architects' order. Federal states (United States, Canada, Australia, Argentina, Germany…): registration is subnational and the aggregate comes from the coordinating body. South Africa: SACAP counts several categories, only « professional architects » are retained. Greece and the Arab world: registration is merged with engineers."],
 ["Density",
  "Architects per 100,000 inhabitants, UN 2024 population rounded — an order-of-magnitude indicator, not a fine statistic."],
 ["What this atlas is not",
  "A worldwide directory of named individuals. Lists of people stay with their publishers and are linked from here; the raw harvested files are kept outside the public repository (GDPR) — the catalogue keeps the link to every source."],
]

# Effectifs réels et sourcés, mais qui ne se comparent pas aux autres : ils sortent
# du calcul d'échelle des jauges et des parts continentales, et le disent.
HORS_ECHELLE = {
  "JP": "a cumulative stock of first-class kenchikushi licences, never cleared and made up "
        "mostly of building engineers — neither an order's headcount nor a headcount of architects.",
}

# Le fonds Natural Earth nomme en cartographe ; un ouvrage de référence nomme
# comme l'ONU et l'ISO 3166. Ces neuf-là se corrigent ICI, pour survivre à toute
# régénération de carte.json — l'atlas décide des noms qu'il publie.
NOMS_EN = {
 "CI":"Côte d'Ivoire",   # forme officielle anglaise, demandée par le pays
 "CZ":"Czechia",         # nom court ISO depuis 2016
 "TL":"Timor-Leste",     # forme ONU
 "CV":"Cabo Verde",      # forme ONU depuis 2013
 "TR":"Türkiye",         # forme ONU depuis 2022
 "CN":"China",           # nom court, pas la forme longue du fonds de carte
 "US":"United States",
 "BS":"Bahamas",
 "GM":"Gambia",
}

def nom_publie(p):
    """Le nom d'usage de la publication est l'anglais ; `pays` (français) ne sert
    plus qu'à la recherche. Les deux coïncident pour 58 pays (Angola, Canada…)."""
    return p.get("nom_en") or p.get("pays")

def enrichir(pays):
    """Ajoute ce que le site seul ne peut pas déduire : nom anglais et hors-échelle.
    `nom_en` est TOUJOURS posé — sinon la colonne « country » de l'export sortirait
    vide pour les 58 pays dont le nom français est déjà l'anglais."""
    chemin = os.path.join(RACINE, "data", "carte.json")
    noms_en = {}
    if os.path.exists(chemin):
        noms_en = json.load(open(chemin, encoding="utf-8")).get("en", {})
    repris = []
    for p in pays:
        en = NOMS_EN.get(p["iso2"]) or noms_en.get(p["iso2"])
        p["nom_en"] = en or p["pays"]
        if not en:
            repris.append(p["iso2"])
        if p["iso2"] in HORS_ECHELLE:
            p["hors_echelle"] = HORS_ECHELLE[p["iso2"]]
    if repris:
        print(f"  · {len(repris)} pays sans nom anglais au fonds de carte — nom français repris tel quel")
    return pays

def injecter(html, marqueur_debut, marqueur_fin, contenu_json):
    motif = re.compile(re.escape(marqueur_debut) + r".*?" + re.escape(marqueur_fin), re.S)
    remplacement = marqueur_debut + contenu_json + marqueur_fin
    nouveau, n = motif.subn(lambda m: remplacement, html)
    if n != 1:
        sys.exit(f"ÉCHEC injection : {marqueur_debut} trouvé {n} fois")
    return nouveau

def principal():
    lignes, faitieres = charger()
    if not lignes:
        sys.exit("Aucune ligne pays — les fichiers data/agents/*.json manquent.")
    lignes = croiser(lignes, faitieres or {})
    pays = enrichir(sorted(lignes.values(), key=lambda p: (p.get("continent",""), p.get("pays",""))))
    cat = catalogue_depuis(lignes, CATALOGUE_LOCAL)
    fs = faitieres_site(faitieres or {})
    meta = {
      "constitue_le": CONSTITUE_LE,
      "pays_vises": 197,
      "signature": "parallel multi-agent research + verification against primary sources",
      "uia": {"sections": (faitieres or {}).get("uia",{}).get("sections_revendiquees"),
              "architectes_revendiques": (faitieres or {}).get("uia",{}).get("architectes_revendiques")},
      "methode": METHODE,
    }
    # atlas.json — data/ (travail) + racine (copie canonique, servie sur https://index.archi/atlas.json ;
    # même script, même dump : les deux ne peuvent pas diverger).
    # C'est l'artefact PUBLIÉ : il sort avec les noms de champs anglais.
    atlas = {"meta": en_anglais(meta, CLES_META_EN),
             "countries": [en_anglais(p, CLES_EN) for p in pays],
             "umbrella_bodies": faitieres,
             "catalogue": cat}
    for chemin_atlas in (os.path.join(RACINE,"data","atlas.json"), os.path.join(RACINE,"atlas.json")):
        with open(chemin_atlas,"w",encoding="utf-8") as f:
            json.dump(atlas, f, ensure_ascii=False, indent=1)
    # injection html
    with open(CHEMIN_HTML, encoding="utf-8") as f: html = f.read()
    html = injecter(html, "/*__META__*/", "/*__FIN_META__*/", json.dumps(meta, ensure_ascii=False))
    html = injecter(html, "/*__DATA__*/", "/*__FIN_DATA__*/", json.dumps(pays, ensure_ascii=False))
    html = injecter(html, "/*__FAITIERES__*/", "/*__FIN_FAITIERES__*/", json.dumps(fs, ensure_ascii=False))
    html = injecter(html, "/*__CATALOGUE__*/", "/*__FIN_CATALOGUE__*/", json.dumps(cat, ensure_ascii=False))
    chemin_carte = os.path.join(RACINE, "data", "carte.json")
    if not os.path.exists(chemin_carte):
        sys.exit("data/carte.json manquant — lancer d'abord : python3 outils/carte.py")
    with open(chemin_carte, encoding="utf-8") as f: carte = f.read().strip()
    html = injecter(html, "/*__CARTE__*/", "/*__FIN_CARTE__*/", carte)
    with open(CHEMIN_HTML,"w",encoding="utf-8") as f: f.write(html)
    # SOURCES.md dérivé
    n_eff = sum(1 for p in pays if p.get("effectif") is not None)
    n_a = sum(1 for p in pays if p.get("qualite")=="A"); n_b = sum(1 for p in pays if p.get("qualite")=="B")
    lignes_md = [
      "# SOURCES — derived from data/atlas.json by outils/fusionner.py — DO NOT EDIT BY HAND",
      f"\nCompiled on {CONSTITUE_LE}. **Control count: {len(pays)} countries** (must agree with atlas.json), "
      f"{n_eff} sourced headcounts, {n_a} at grade A, {n_b} at grade B.\n",
      "| Country | Body | Headcount | Year | Source type | Source |",
      "|---|---|---:|---|---|---|",
    ]
    for p in pays:
        src = p.get("effectif_source_url") or ""
        lignes_md.append(f"| {nom_publie(p)} | {p.get('organisme') or '—'} | {p.get('effectif') if p.get('effectif') is not None else '—'} "
                         f"| {p.get('effectif_annee') or '—'} | {p.get('effectif_nature') or '—'} | {src} |")
    with open(os.path.join(RACINE,"SOURCES.md"),"w",encoding="utf-8") as f:
        f.write("\n".join(lignes_md)+"\n")
    print(f"OK — {len(pays)} pays, {len(cat)} entrées catalogue, {n_eff} effectifs, A:{n_a} B:{n_b}")

if __name__ == "__main__":
    principal()
