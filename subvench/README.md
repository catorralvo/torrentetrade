# SubvenCH

SubvenCH est une marque de Torrente Trade & Advice.

Objectif: aider les PME suisses à identifier les aides, subventions, garanties et dispositifs de financement public pertinents à partir de leur profil et de leur projet.

## Positionnement

SubvenCH n'est pas un simple annuaire. Le produit cible le flux suivant:

profil entreprise → description du projet → filtrage par règles → opportunités pertinentes → explication → sources officielles → préparation du dossier.

## MVP actuel

- Web uniquement, sans installation.
- Périmètre initial: Vaud, Genève et principaux programmes fédéraux.
- Matching explicable.
- Les critères objectifs priment sur le scoring.
- Les éléments non vérifiables restent `à vérifier`.
- L'organisme compétent reste seul décisionnaire.

## Architecture prévue

- Frontend: Next.js
- Backend/Auth/DB: Supabase
- Moteur de règles déterministe
- IA utilisée pour interpréter le projet et expliquer les résultats, pas pour inventer l'éligibilité

## Étapes suivantes

1. Étendre le catalogue officiel.
2. Formaliser les règles de chaque dispositif.
3. Ajouter profils/projets sauvegardés.
4. Ajouter GrantWatch.
5. Ajouter Dossier Builder.
6. Préparer une vue Advisor pour fiduciaires, incubateurs et coaches PME.
