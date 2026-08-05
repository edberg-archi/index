#!/usr/bin/env python3
"""Construit data/carte.json — la géométrie du planisphère de l'atlas.

Source : Natural Earth 110 m (domaine public), polygones + micro-États en points.
Projection : Equal Earth (Šavrič, Patterson & Jenny 2018) — équivalente, donc les
surfaces restent comparables ; c'est la seule honnêteté cartographique qui compte
quand on teinte des pays.

Sortie : {"vb":[x,y,w,h], "poly":{"FR":"M…"}, "pts":{"MC":[x,y]}, "en":{"FR":"France"}}
Les tracés sont simplifiés (Douglas-Peucker) et arrondis au dixième d'unité.

    python3 outils/carte.py            # utilise le cache s'il existe
    python3 outils/carte.py --refaire  # retélécharge les sources

Le fichier produit est injecté dans index.html par outils/fusionner.py.
"""
import json, math, os, sys, urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RACINE, "data", "sources-carte")
SORTIE = os.path.join(RACINE, "data", "carte.json")
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FICHIERS = {"poly": "ne_110m_admin_0_countries.geojson",
            "tiny": "ne_110m_admin_0_tiny_countries.geojson"}

# Les huit pays de l'atlas absents des deux jeux 110 m — placés à la main (lon, lat, nom anglais).
A_LA_MAIN = {"AD": (1.52, 42.51, "Andorra"), "CV": (-23.6, 15.12, "Cape Verde"),
             "HK": (114.17, 22.32, "Hong Kong"), "LI": (9.55, 47.16, "Liechtenstein"),
             "MC": (7.42, 43.74, "Monaco"), "MO": (113.55, 22.2, "Macao"),
             "SC": (55.49, -4.62, "Seychelles"), "SM": (12.46, 43.94, "San Marino")}

# ---------------------------------------------------------------- projection
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
RAC3_2 = math.sqrt(3) / 2

def equal_earth(lon, lat):
    lam, phi = math.radians(lon), math.radians(max(-89.9, min(89.9, lat)))
    th = math.asin(RAC3_2 * math.sin(phi))
    t2 = th * th
    den = 9 * A4 * t2 * t2 * t2 * t2 + 7 * A3 * t2 * t2 * t2 + 3 * A2 * t2 + A1
    x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * den)
    y = A4 * th ** 9 + A3 * th ** 7 + A2 * th ** 3 + A1 * th
    return x, -y                      # y inversé : l'écran descend

# ---------------------------------------------------------------- géométrie
def rdp(pts, eps):
    """Douglas-Peucker itératif — un anneau de 3000 points ferait exploser la pile."""
    if len(pts) < 3:
        return pts
    garde = [False] * len(pts)
    garde[0] = garde[-1] = True
    pile = [(0, len(pts) - 1)]
    while pile:
        i, j = pile.pop()
        if j <= i + 1:
            continue
        ax, ay = pts[i]; bx, by = pts[j]
        dx, dy = bx - ax, by - ay
        norme = math.hypot(dx, dy)
        dmax, imax = -1.0, i
        for k in range(i + 1, j):
            px, py = pts[k]
            d = abs(dx * (ay - py) - (ax - px) * dy) / norme if norme else math.hypot(px - ax, py - ay)
            if d > dmax:
                dmax, imax = d, k
        if dmax > eps:
            garde[imax] = True
            pile.append((i, imax)); pile.append((imax, j))
    return [p for p, g in zip(pts, garde) if g]

def anneaux(geom):
    t = geom["type"]
    if t == "Polygon":
        return [geom["coordinates"][0]]
    if t == "MultiPolygon":
        return [poly[0] for poly in geom["coordinates"]]
    return []

def code_iso(prop):
    for cle in ("ISO_A2_EH", "ISO_A2"):
        v = prop.get(cle)
        if v and v != "-99" and len(v) == 2:
            return v
    return None

def nom_en(prop):
    return prop.get("NAME_EN") or prop.get("NAME_LONG") or prop.get("NAME") or ""

# ---------------------------------------------------------------- fabrication
def charger(cle, refaire):
    os.makedirs(CACHE, exist_ok=True)
    chemin = os.path.join(CACHE, FICHIERS[cle])
    if refaire or not os.path.exists(chemin):
        print(f"… téléchargement {FICHIERS[cle]}")
        urllib.request.urlretrieve(BASE + FICHIERS[cle], chemin)
    return json.load(open(chemin, encoding="utf-8"))

def construire(refaire=False):
    poly_src = charger("poly", refaire)
    tiny_src = charger("tiny", refaire)

    ECH = 200.0          # unités par radian projeté ≈ planisphère de 1020 de large
    EPS = 1.15           # tolérance de simplification, dans ces unités
    SEUIL_ANNEAU = 0.9   # aire minimale d'un anneau conservé

    poly, en = {}, {}
    for f in poly_src["features"]:
        iso = code_iso(f["properties"])
        if not iso or iso == "AQ":                     # l'Antarctique n'a pas d'ordre
            continue
        en[iso] = nom_en(f["properties"])
        candidats = []                                 # (aire, points) par anneau
        for anneau in anneaux(f["geometry"]):
            pts = [equal_earth(x, y) for x, y in anneau if y > -60]
            if len(pts) < 4:
                continue
            pts = [(x * ECH, y * ECH) for x, y in pts]
            aire = abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1]
                           for i in range(len(pts)))) / 2
            candidats.append((aire, pts))
        gardes = [c for c in candidats if c[0] >= SEUIL_ANNEAU]
        if not gardes and candidats:                   # un micro-État garde sa plus grande île
            gardes = [max(candidats, key=lambda c: c[0])]
        morceaux = []
        for aire, pts in gardes:
            simple = rdp(pts, EPS if aire >= SEUIL_ANNEAU else EPS / 4)
            if len(simple) < 4:
                simple = pts
            morceaux.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in simple) + "Z")
        if morceaux:
            poly[iso] = "".join(morceaux)

    pts = {}
    for f in tiny_src["features"]:
        iso = code_iso(f["properties"])
        if not iso or iso in poly:
            continue
        en[iso] = nom_en(f["properties"])
        lon, lat = f["geometry"]["coordinates"][:2]
        x, y = equal_earth(lon, lat)
        pts[iso] = [round(x * ECH, 1), round(y * ECH, 1)]
    for iso, (lon, lat, nom) in A_LA_MAIN.items():
        if iso in poly or iso in pts:
            continue
        en.setdefault(iso, nom)
        x, y = equal_earth(lon, lat)
        pts[iso] = [round(x * ECH, 1), round(y * ECH, 1)]

    # cadre
    xs, ys = [], []
    for iso, d in poly.items():
        nombres = d.replace("M", " ").replace("L", " ").replace("Z", " ").split()
        for i in range(0, len(nombres) - 1, 2):
            xs.append(float(nombres[i])); ys.append(float(nombres[i + 1]))
    for x, y in pts.values():
        xs.append(x); ys.append(y)
    marge = 4
    x0, y0 = min(xs) - marge, min(ys) - marge
    vb = [round(x0, 1), round(y0, 1),
          round(max(xs) - min(xs) + 2 * marge, 1), round(max(ys) - min(ys) + 2 * marge, 1)]

    carte = {"vb": vb, "poly": poly, "pts": pts, "en": en,
             "source": "Natural Earth 110 m — domaine public · projection Equal Earth"}
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as fh:
        json.dump(carte, fh, ensure_ascii=False, separators=(",", ":"))

    # contrôle : tout pays de l'atlas doit avoir une forme ou un point
    atlas = os.path.join(RACINE, "data", "atlas.json")
    orphelins = []
    if os.path.exists(atlas):
        a = json.load(open(atlas, encoding="utf-8"))
        liste = a["pays"] if isinstance(a, dict) and "pays" in a else a
        orphelins = sorted(p["iso2"] for p in liste
                           if p["iso2"] not in poly and p["iso2"] not in pts)
    ko = os.path.getsize(SORTIE) / 1024
    print(f"OK — {len(poly)} contours, {len(pts)} points, {ko:.0f} Ko, cadre {vb}")
    print("orphelins (aucune géométrie) :", orphelins or "aucun")
    return carte

if __name__ == "__main__":
    construire("--refaire" in sys.argv)
