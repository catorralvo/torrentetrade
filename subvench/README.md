# SubvenCH

SubvenCH est une marque de Torrente Trade & Advice.

Objectif: aider les PME suisses à identifier, sauvegarder et surveiller les aides, subventions, garanties et dispositifs de financement public pertinents à partir de leur profil et de leurs projets.

## Positionnement

SubvenCH n'est pas un annuaire. Le flux cible est:

profil entreprise → projet → filtrage par règles → opportunités pertinentes → explication → disponibilité → sources officielles → historique → GrantWatch → préparation du dossier.

## M2.1 actuel

- Web uniquement, sans installation.
- Périmètre: Vaud, Genève et principaux programmes fédéraux/internationaux accessibles aux PME suisses.
- **25 dispositifs structurés et sourcés**, versionnés dans le catalogue.
- Moteur de règles déterministe (`engine.mjs`).
- Matching explicable avec `confirmed`, `probable`, `to_verify`, `not_eligible`.
- Disponibilité séparée de l'éligibilité: `open`, `upcoming`, `call_based`, `closed`, `check`.
- Profil entreprise persistant dans le navigateur.
- Plusieurs projets sauvegardés et historique de scans immuable.
- GrantWatch local: comparaison automatique d'un ancien scan avec un nouveau catalogue.
- Alertes en cas de nouvelle piste, changement d'éligibilité, de pertinence ou de disponibilité.
- Export JSON des données utilisateur.
- Tests de régression + audit structurel du catalogue.
- Monitoring hebdomadaire de la santé des sources officielles via GitHub Actions.
- 12 cas pilotes suisses reproductibles (`data/pilot_cases.json`).
- Protocole de validation terrain pour GENIE.ch, platinn, COMETE et autres partenaires (`PARTNER_PILOT.md`).

## Sécurité / Supabase

La migration `supabase/migrations/0001_subvench_m2.sql` prépare:

- profils,
- projets,
- scans,
- watches,
- alertes,
- versions des programmes.

Chaque table exposée active RLS. Les tables utilisateur sont limitées à `auth.uid() = user_id`. Les grants Data API sont explicites. Les écritures système (versions de programmes et création d'alertes) restent côté serveur; aucune clé secrète/service ne doit être exposée dans le navigateur.

La conception tient compte du changement Supabase 2026: les nouvelles tables ne sont plus automatiquement exposées à la Data API sur les nouveaux projets; les grants nécessaires sont donc déclarés explicitement.

## Arborescence

- `index.html` / `styles.css` / `app.js`: prototype web M2.1
- `engine.mjs`: moteur d'éligibilité, pertinence et disponibilité
- `workspace.mjs`: persistance, historique et GrantWatch local
- `data/programs.json`: catalogue de base
- `data/programs_2026q4.json`: extension catalogue Q4 2026
- `data/catalog.meta.json`: version du catalogue
- `data/pilot_cases.json`: cas de validation
- `tests/`: tests de régression
- `scripts/catalog-audit.mjs`: contrôle qualité des données
- `scripts/pilot-benchmark.mjs`: benchmark des cas pilotes
- `scripts/source-health.mjs`: contrôle des sources officielles
- `supabase/migrations/`: schéma cible Supabase
- `PARTNER_PILOT.md`: protocole de validation avec l'écosystème PME
- `CODEX_M3_BRIEF.md`: spécification de conversion en application Next.js/Supabase

## Prochain jalon: M3

1. Next.js App Router.
2. Auth Supabase avec clé publishable et SSR.
3. Migration SQL appliquée à un projet Supabase isolé.
4. Remplacement du stockage local par le backend, avec migration des données locales.
5. GrantWatch serveur planifié.
6. Validation terrain avec partenaires.
7. Dossier Builder seulement après validation du matching.
