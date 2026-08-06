# DONNÉES — schéma d'atlas.json

DÉRIVÉ de `data/atlas.json` par `outils/documenter.py` — NE PAS ÉDITER À LA MAIN.

Jeu servi à l'adresse stable **https://index.archi/atlas.json** (UTF-8, licence CC BY 4.0).
Constitué le 5 août 2026. **Compte de contrôle : 180 pays** (concorde avec SOURCES.md), 88 effectifs sourcés, A:26 B:54 C:9 D:91.

## Structure

| Bloc | Type | Contenu |
|---|---|---|
| `meta` | objet | date de constitution, périmètre visé (197 juridictions), méthode en 6 points, revendication UIA |
| `pays` | liste (180) | une entrée par pays — schéma ci-dessous |
| `faitieres` | objet (8) | organisations faîtières (UIA, ACE, CAA, AUA…) avec leurs revendications sourcées |
| `catalogue` | liste (36) | jeux de données publics recensés (éditeur, format, URL) |

## Champs d'une entrée `pays`

| Champ | Types | Renseigné | Description |
|---|---|---:|---|
| `alternatives` | liste | 180/180 | Listes NON officielles (associations type RIBA/AIA, annuaires) qui permettent de recouper — jamais confondues avec le registre. |
| `continent` | texte | 180/180 | Continent (vocabulaire recensé ci-dessous). |
| `donnees_ouvertes_format` | texte | 24/180 | Format du jeu téléchargeable (CSV, XLSX, PDF…). |
| `donnees_ouvertes_url` | texte | 33/180 | Jeu de données téléchargeable en masse (open data, roster), quand il existe. |
| `effectif` | entier | 88/180 | Inscrits auprès de l'organisme officiel — voir `effectif_nature`. `null` = non publié. Ce que compte l'atlas : des INSCRITS, pas des diplômés ni des praticiens de fait. |
| `effectif_annee` | entier | 84/180 | Année du chiffre. |
| `effectif_nature` | texte | 88/180 | Nature de la source du chiffre (vocabulaire recensé ci-dessous). |
| `effectif_source_url` | texte | 90/180 | Source du chiffre — chaque effectif la porte (aucun chiffre sans source). |
| `inscription_obligatoire` | bool | 140/180 | L'inscription conditionne-t-elle l'exercice ? `null` = non établi. |
| `iso2` | texte | 180/180 | Code ISO 3166-1 alpha-2 — la clé du jeu. |
| `notes` | texte | 180/180 | Précisions de lecture propres au pays (périmètre, pièges, recoupements). |
| `organisme` | texte | 180/180 | Organisme officiel d'inscription (ordre, chambre, board, conseil…). `null` = aucun organisme identifié. |
| `pays` | texte | 180/180 | Nom du pays en français. |
| `population_m` | nombre | 180/180 | Population ONU 2024 (millions, arrondie) — sert uniquement la densité indicative. |
| `qualite` | texte | 180/180 | Grade de qualité de la donnée : A = liste nominative téléchargeable en masse · B = registre public consultable · C = effectif officiel publié, registre non consultable · D = estimation ou liste d'association seulement. |
| `registre_recherche_publique` | bool | 100/180 | Le registre offre-t-il une recherche nominative publique ? |
| `registre_url` | texte | 94/180 | Registre public consultable, quand il existe. |
| `sigle` | texte | 135/180 | Sigle usuel de l'organisme. |
| `titre_protege` | bool | 105/180 | Le titre « architecte » est-il protégé par la loi ? `null` = non établi. |
| `type_organisme` | texte | 180/180 | Nature de l'organisme (vocabulaire recensé ci-dessous). |
| `uia_membre` | bool | 179/180 | Le pays a-t-il une section membre de l'UIA ? |
| `nom_en` | texte | 122/180 | Nom anglais (sert la recherche) — présent quand il diffère du français. |
| `uia_section` | texte | 117/180 | Nom de la section UIA quand elle diffère de l'organisme d'inscription. |
| `ace_effectif_2024` | entier | 32/180 | Recoupement : effectif du même pays dans l'étude sectorielle ACE 2024 (Europe) — une DEUXIÈME mesure, pas la nôtre ; l'écart avec `effectif` se lit en fiche. |
| `hors_echelle` | texte | 1/180 | Présent quand l'effectif, réel et sourcé, ne se COMPARE pas aux autres (ex. Japon : stock cumulé kenchikushi) — il sort des sommes et des jauges, et le motif est donné. |

## Vocabulaires recensés

**`qualite`** : A (26) · B (54) · C (9) · D (91)

**`continent`** : Afrique (53) · Europe (49) · Asie (45) · Amériques (29) · Océanie (4)

**`effectif_nature`** : `registre` (39) · `rapport_officiel` (22) · `presse` (14) · `etude_sectorielle` (9) · `estimation` (3) · `liste_electorale` (1)

**`type_organisme`** : `ordre` (41) · `registre_etatique` (28) · `association` (26) · `board` (23) · `aucun` (16) · `chambre` (16) · `conseil` (15) · `syndicat_ingenieurs` (15)

## Lecture honnête

- Comparer des pays = comparer des **inscrits au registre officiel**, jamais des diplômés ni des praticiens de fait.
- Les entrées portant `hors_echelle` restent affichées et sourcées mais sortent des sommes et des échelles.
- **91 pays sont en grade D** (estimation ou association seulement) : cette moitié du tableau est un plan de travail, pas un résultat.
- Aucune donnée nominative dans ce jeu ni dans ce dépôt — les listes de personnes restent chez leurs éditeurs, liées par le catalogue.
