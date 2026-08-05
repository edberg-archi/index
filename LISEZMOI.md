# INDEX — atlas mondial des ordres et registres d'architectes

Un site de référence en un seul fichier : pour chaque pays, l'organisme officiel
d'inscription des architectes (ordre, chambre, board, conseil), le régime
(obligation, protection du titre), l'effectif sourcé et daté, le registre
consultable, le jeu de données téléchargeable quand il existe, et les listes
alternatives (associations, annuaires) qui permettent de recouper.

## Ouvrir

`index.html` — autonome, hors ligne, sans dépendance (fonds de carte compris).

- **Planisphère** teinté par grade de donnée : cliquer un pays ouvre sa fiche.
- **Trois graphes qui sont des commandes** : parts continentales de l'effectif,
  couverture par grade, extrêmes de densité. Cliquer un segment filtre le tableau.
- **Filtres à compteurs** — chaque jeton annonce ce qu'il ramènerait, ceux qui
  ne ramènent rien sont désactivés ; `× tout effacer` et la touche `Échap` remettent à plat.
- **Toute vue est une adresse** : les filtres vivent dans le `#hash`, `#p=SN` ouvre
  directement la fiche du Sénégal. Un lien copiable est au bas de chaque fiche.
- Recherche en français, en anglais ou par code ISO (`NG`, `Germany`, `kenchikushi`).
- Export JSON et CSV, **au périmètre choisi** (la sélection à l'écran ou l'atlas entier),
  provenance et adresse de la vue embarquées.
- Clair/nuit, imprimable, `/` met le curseur dans la recherche.

## Arborescence

    index.html          le site, données et géométrie intégrées
    atlas.json          copie canonique du jeu, servie sur https://index.archi/atlas.json
    SOURCES.md          DÉRIVÉ du jeu par outils/fusionner.py — ne pas éditer
    DONNEES.md          DÉRIVÉ du jeu par outils/documenter.py — schéma champ par champ
    data/atlas.json     le jeu complet (méta + pays + faîtières + catalogue)
    data/carte.json     DÉRIVÉ de Natural Earth par outils/carte.py — ne pas éditer
    data/agents/*.json  moissons brutes des agents de recherche, par région
    data/*.csv|xlsx     jeux nominatifs bruts téléchargés — HORS dépôt public (RGPD),
                        provenance conservée au catalogue
    outils/carte.py     planisphère : Natural Earth 110 m → Equal Earth simplifié (54 Ko)
    outils/fusionner.py fusion + recoupements (ACE, UIA) + injection dans index.html
    outils/documenter.py banc d'avant-publication : dérive DONNEES.md, refuse un champ
                        non documenté ou des comptes qui divergent
    sauvegardes/        états antérieurs du site, datés (hors dépôt)

## Reconstruire

    python3 outils/carte.py       # seulement si data/carte.json manque
    python3 outils/fusionner.py
    python3 outils/documenter.py  # banc + DONNEES.md

`carte.py` projette les contours en Equal Earth (projection équivalente : les
surfaces restent comparables), simplifie, et sort les micro-États en points ;
il vérifie qu'aucun pays de l'atlas ne se retrouve sans géométrie.
`fusionner.py` recharge `data/agents/*.json`, recoupe avec l'étude ACE 2024 et la
liste des sections UIA, recalcule les grades manquants, attache les noms anglais,
réinjecte tout dans `index.html` et re-dérive `SOURCES.md` (compte de contrôle inclus).

## Chiffres hors échelle

Un effectif peut être réel, sourcé et malgré tout incomparable. `HORS_ECHELLE`
dans `fusionner.py` porte ces cas — aujourd'hui le seul Japon, dont les 383 923
licences *kenchikushi* de 1re classe sont un stock cumulé jamais apuré,
majoritairement composé d'ingénieurs. Ces chiffres restent affichés et sourcés,
mais sortent des sommes, des parts continentales et de l'échelle des jauges,
et le disent en fiche.

## Grades de qualité

- **A** — liste nominative téléchargeable en masse (open data, roster, tableau publié)
- **B** — registre public consultable en ligne (recherche nominative)
- **C** — effectif officiel publié, registre non consultable
- **D** — estimation ou liste d'association seulement

## Licence

Compilation CC BY 4.0. Chaque donnée reste la propriété de sa source, citée
ligne à ligne (colonne `effectif_source_url`, fiches du site).
