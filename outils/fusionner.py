#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDEX — fusion des moissons d'agents en un jeu unique, injecté dans index.html.

Entrées : data/agents/*.json   (fichiers {"rows":[...]} par région + faitieres.json)
Sorties : data/atlas.json      (jeu complet, avec méta)
          index.html           (données injectées entre marqueurs)
          SOURCES.md           (dérivé du jeu — jamais rédigé à la main)

Règle de la maison : le document qui décrit est DÉRIVÉ de la source ;
SOURCES.md porte un compte qui doit concorder avec atlas.json.
"""
import json, glob, os, re, sys, datetime

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_AGENTS = os.path.join(RACINE, "data", "agents")
CHEMIN_HTML = os.path.join(RACINE, "index.html")

CONSTITUE_LE = "5 août 2026"

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
                p["effectif_nature"] = "etude_sectorielle"; p["effectif_source_url"] = ace_url
                p["notes"] = ((p.get("notes") or "") +
                    " Effectif repris de l'étude sectorielle ACE 2024, l'organisme n'en publiant pas.").strip()
                if p.get("qualite") in (None, "", "D"): p["qualite"] = "C"
        if not p.get("qualite"): p["qualite"] = "D"
    return lignes

def catalogue_depuis(lignes, catalogue_local):
    vus = {(c.get("pays"), c.get("url")) for c in catalogue_local}
    cat = list(catalogue_local)
    for p in sorted(lignes.values(), key=lambda x: x["pays"]):
        if p.get("donnees_ouvertes_url") and (p["pays"], p["donnees_ouvertes_url"]) not in vus:
            cat.append({"pays": p["pays"], "jeu": "Registre / données de " + (p.get("sigle") or p.get("organisme") or "l'organisme"),
                        "format": p.get("donnees_ouvertes_format") or "—",
                        "editeur": p.get("organisme"), "url": p["donnees_ouvertes_url"], "etat": "en ligne"})
    return cat

CATALOGUE_LOCAL = [
 {"pays":"États-Unis — Texas","jeu":"Roster complet des architectes actifs (TBAE, temps réel)","format":"XLSX→CSV",
  "editeur":"Texas Board of Architectural Examiners",
  "url":"https://indreg.tbae.texas.gov/Reports/RegistrantRosters","livre":"data/us-texas-tbae-architectes.csv (14 575 inscrits)"},
 {"pays":"Singapour","jeu":"Registre officiel des architectes (BOA) — donnée ouverte d'État","format":"CSV",
  "editeur":"Board of Architects via data.gov.sg",
  "url":"https://data.gov.sg/datasets/d_d77de0f78ca589a5c61da7a60fdee6ba/view","livre":"data/sg-boa-registre-architectes.csv (1 999 inscrits)"},
 {"pays":"Europe (32 pays)","jeu":"ACE Sector Study 2024 — effectifs par pays (table 1-1)","format":"PDF",
  "editeur":"Architects' Council of Europe","url":"https://ace-cae.eu/wp-content/uploads/2025/04/2024-ACE-Sector-Study-EN-04042025.pdf",
  "etat":"extrait dans l'atlas"},
 {"pays":"Monde","jeu":"UIA — présentation officielle : 117 sections, ~745 665 architectes","format":"PDF",
  "editeur":"Union internationale des architectes",
  "url":"https://www.uia-architectes.org/wp-content/uploads/2025/02/2-2025-UIA-presentation.pdf","etat":"extrait dans l'atlas"},
]

def faitieres_site(f):
    u, a = f.get("uia", {}), f.get("ace", {})
    return [
      {"sigle":"UIA","nom":"Union internationale des architectes — 5 régions, l'égide mondiale",
       "url":u.get("membres_url"),"chiffre":f"<b>{u.get('sections_revendiquees','—')}</b> sections · <b class='num'>{format(u.get('architectes_revendiques',0),',').replace(',',' ')}</b> architectes revendiqués ({u.get('pays_revendiques','—')} pays)",
       "note":"Présentation officielle, fév. 2025 — le « 3,2 M » parfois cité est introuvable dans les sources UIA."},
      {"sigle":"ACE","nom":"Architects' Council of Europe — étude sectorielle biennale",
       "url":a.get("etude_page"),"chiffre":f"<b class='num'>{format(a.get('total_architectes_europe',0),',').replace(',',' ')}</b> architectes en Europe-32 (2024)",
       "note":"Table 1-1 reprise pays par pays dans l'atlas."},
      {"sigle":"CAA","nom":"Commonwealth Association of Architects",
       "url":f.get("caa",{}).get("url"),"chiffre":f"<b>{f.get('caa',{}).get('nb_membres_listes','—')}</b> instituts membres listés","note":None},
      {"sigle":"AUA","nom":"Union africaine des architectes",
       "url":f.get("aua",{}).get("url"),"chiffre":"<b>43</b> sections revendiquées · > 70 000 architectes","note":"Aucune liste nominative publiée en ligne."},
      {"sigle":"FPAA","nom":"Federación Panamericana de Asociaciones de Arquitectos",
       "url":f.get("fpaa",{}).get("url"),"chiffre":"<b>32</b> pays · « casi 1 millón de arquitectos »","note":"Revendication non ventilée ; aucune liste publiée."},
      {"sigle":"ARCASIA","nom":"Architects Regional Council Asia",
       "url":f.get("arcasia",{}).get("url"),"chiffre":"<b>24</b> instituts membres (zones A, B, C)","note":None},
      {"sigle":"UMAR","nom":"Union méditerranéenne des architectes",
       "url":f.get("umar",{}).get("url"),"chiffre":"<b>14</b> pays membres","note":"Déclaration de Rabat, 1994."},
    ]

METHODE = [
 ["Ce que compte cet atlas",
  "Des architectes INSCRITS auprès de l'organisme officiel de leur pays — pas des diplômés, pas des praticiens de fait. Quand l'inscription passe par un syndicat d'ingénieurs (glyphe ▤), l'effectif isolé de la division architecture est donné quand il existe."],
 ["Grades A · B · C · D",
  "A — liste nominative téléchargeable en masse (open data, roster, tableau publié). B — registre public consultable en ligne, sans téléchargement. C — effectif officiel publié, registre non consultable. D — estimation ou liste d'association seulement."],
 ["Recoupements",
  "Chaque effectif est daté et sourcé (lien en fiche). Europe : recoupé avec l'étude sectorielle ACE 2024. Monde : adossé à la liste des 117 sections membres de l'UIA. Les listes alternatives (associations type RIBA/AIA, annuaires) sont données par pays."],
 ["Pièges connus",
  "Japon : les ~370 000 kenchikushi de 1re classe incluent une majorité d'ingénieurs du bâtiment — le chiffre n'est pas comparable à un ordre d'architectes. Fédérations (États-Unis, Canada, Australie, Argentine, Allemagne…) : l'inscription est infranationale, l'agrégat vient de l'organe de coordination. Afrique du Sud : SACAP compte plusieurs catégories, seuls les « professional architects » sont retenus. Grèce et monde arabe : inscription mêlée aux ingénieurs."],
 ["Densité",
  "Architectes pour 100 000 habitants, population ONU 2024 arrondie — un indicateur d'ordre de grandeur, pas une statistique fine."],
 ["Ce que cet atlas n'est pas",
  "Un annuaire nominatif mondial. Les listes de personnes restent chez leurs éditeurs, liées ici ; les fichiers bruts moissonnés sont conservés hors du dépôt public (RGPD) — le catalogue garde le lien vers chaque source."],
]

# Effectifs réels et sourcés, mais qui ne se comparent pas aux autres : ils sortent
# du calcul d'échelle des jauges et des parts continentales, et le disent.
HORS_ECHELLE = {
  "JP": "stock cumulé de licences kenchikushi de 1re classe, jamais apuré et majoritairement "
        "composé d'ingénieurs du bâtiment — ni un effectif d'ordre ni un effectif d'architectes",
}

def enrichir(pays):
    """Ajoute ce que le site seul ne peut pas déduire : nom anglais (recherche) et hors-échelle."""
    chemin = os.path.join(RACINE, "data", "carte.json")
    noms_en = {}
    if os.path.exists(chemin):
        noms_en = json.load(open(chemin, encoding="utf-8")).get("en", {})
    manquants = []
    for p in pays:
        en = noms_en.get(p["iso2"])
        if en and en != p["pays"]:
            p["nom_en"] = en
        elif not en:
            manquants.append(p["iso2"])
        if p["iso2"] in HORS_ECHELLE:
            p["hors_echelle"] = HORS_ECHELLE[p["iso2"]]
    if manquants:
        print("  ! sans nom anglais (recherche dégradée) :", " ".join(manquants))
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
      "signature": "recherche parallèle multi-agents + vérification des sources primaires",
      "uia": {"sections": (faitieres or {}).get("uia",{}).get("sections_revendiquees"),
              "architectes_revendiques": (faitieres or {}).get("uia",{}).get("architectes_revendiques")},
      "methode": METHODE,
    }
    # atlas.json — data/ (travail) + racine (copie canonique, servie sur https://index.archi/atlas.json ;
    # même script, même dump : les deux ne peuvent pas diverger)
    atlas = {"meta":meta,"pays":pays,"faitieres":faitieres,"catalogue":cat}
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
      "# SOURCES — dérivé de data/atlas.json par outils/fusionner.py — NE PAS ÉDITER À LA MAIN",
      f"\nConstitué le {CONSTITUE_LE}. **Compte de contrôle : {len(pays)} pays** (doit concorder avec atlas.json), "
      f"{n_eff} effectifs sourcés, {n_a} grade A, {n_b} grade B.\n",
      "| Pays | Organisme | Effectif | Année | Nature | Source |",
      "|---|---|---:|---|---|---|",
    ]
    for p in pays:
        src = p.get("effectif_source_url") or ""
        lignes_md.append(f"| {p['pays']} | {p.get('organisme') or '—'} | {p.get('effectif') if p.get('effectif') is not None else '—'} "
                         f"| {p.get('effectif_annee') or '—'} | {p.get('effectif_nature') or '—'} | {src} |")
    with open(os.path.join(RACINE,"SOURCES.md"),"w",encoding="utf-8") as f:
        f.write("\n".join(lignes_md)+"\n")
    print(f"OK — {len(pays)} pays, {len(cat)} entrées catalogue, {n_eff} effectifs, A:{n_a} B:{n_b}")

if __name__ == "__main__":
    principal()
