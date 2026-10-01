# SubvenCH

SubvenCH est une marque de Torrente Trade & Advice.

Objectif: aider les PME suisses à identifier, sauvegarder et surveiller les aides, subventions, garanties et dispositifs de financement public pertinents à partir de leur profil et de leurs projets.

## Positionnement

SubvenCH n'est pas un annuaire. Le flux cible est:

profil entreprise → projet → filtrage par règles → opportunités pertinentes → explication → sources officielles → historique → GrantWatch → préparation du dossier.

## M2 actuel

- Web uniquement, sans installation.
- Périmètre: Vaud, Genève et principaux programmes fédéraux/internationaux accessibles aux PME suisses.
- Catalogue versionné et sourcé.
- Moteur de règles déterministe (`engine.mjs`).
- Matching explicable avec `confirmed`, `probable`, `to_verify`, `not_eligible`.
- Profil entreprise persistant dans le navigateur.
- Plusieurs projets sauvegardés.
- Historique de scans.
- GrantWatch local: comparaison automatique d'un ancien scan avec un nouveau catalogue.
- Alertes en cas de nouvelle piste ou changement d'éligibilité/pertinence.
- Export JSON des données utilisateur.
- Tests de régression + audit structurel du catalogue.
- Monitoring hebdomadaire de la santé des sources officielles via GitHub Actions.

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

- `index.html` / `styles.css` / `app.js`: prototype web M2
- `engine.mjs`: moteur d'éligibilité/matching
- `workspace.mjs`: persistance, historique et GrantWatch local
- `data/programs.json`: catalogue structuré
- `data/catalog.meta.json`: version du catalogue
- `tests/`: tests de régression
- `scripts/catalog-audit.mjs`: contrôle qualité des données
- `scripts/source-health.mjs`: contrôle des sources officielles
- `supabase/migrations/`: schéma cible Supabase
- `CODEX_M3_BRIEF.md`: spécification pour la conversion en vraie application Next.js/Supabase

## Prochain jalon: M3

1. Next.js App Router.
2. Auth Supabase avec clé publishable et SSR.
3. Migration SQL appliquée à un projet Supabase.
4. Remplacement du stockage local par le backend, avec migration automatique des données locales.
5. GrantWatch serveur planifié.
6. Extension contrôlée du catalogue.
7. Dossier Builder après validation terrain du matching.
