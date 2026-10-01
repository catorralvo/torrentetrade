# SubvenCH — protocole pilote partenaires

## Objectif

Valider le moteur avec des professionnels qui accompagnent réellement des PME suisses (par exemple GENIE.ch, platinn, COMETE et réseaux analogues) avant d'investir dans le Dossier Builder ou une couverture nationale.

Le pilote ne cherche pas à demander un financement au partenaire. Il cherche à mesurer la qualité du diagnostic.

## Démonstration

Pour chaque cas test, le partenaire reçoit uniquement:

1. le profil synthétique de l'entreprise;
2. la description du projet;
3. les 3–5 pistes proposées par SubvenCH;
4. les exclusions importantes;
5. les raisons, critères à confirmer et sources officielles.

Le partenaire répond sans modifier le moteur pendant la session.

## Grille de validation

Pour chaque cas:

- Une aide importante manque-t-elle? `oui/non` + nom.
- Une aide proposée est-elle clairement hors sujet? `oui/non` + raison.
- Une exclusion est-elle erronée? `oui/non` + raison.
- Un critère décisif manque-t-il dans la règle? `oui/non` + critère.
- La source officielle est-elle la bonne? `oui/non`.
- La distinction `éligibilité / pertinence / disponibilité` est-elle compréhensible? note 1–5.
- Le résultat permet-il de décider rapidement quelle démarche approfondir? note 1–5.
- Utiliseriez-vous cet outil avec une PME réelle? `oui/non/peut-être` + pourquoi.

## Seuil de passage vers M4

Le pilote est considéré suffisamment bon pour poursuivre si:

- zéro faux `confirmed` sur un cas objectivement inéligible;
- au moins 80% des aides jugées importantes par les experts sont retrouvées dans les résultats utiles;
- moins de 15% de faux positifs clairement hors sujet dans le top 5;
- moyenne ≥4/5 sur la compréhension du résultat;
- au moins deux professionnels déclarent qu'ils utiliseraient le produit sur un dossier réel ou qu'il leur ferait gagner du temps.

Un échec à ces seuils entraîne d'abord une correction du catalogue/rules engine, pas l'ajout d'IA générative.

## Cas de départ

Le fichier `data/pilot_cases.json` contient 12 cas fictifs couvrant:

- industrie Vaud;
- installation pilote Genève;
- start-up digitale Genève;
- start-up digitale Vaud;
- impact;
- cleantech;
- efficience électrique;
- Eurostars/R&D internationale;
- projet déjà commencé;
- entreprise >249 ETP;
- micro-crédit Ville de Genève;
- formation technique Vaud.

Le script `npm run benchmark` produit une base reproductible avant toute session partenaire.

## Règle de confidentialité

Pour le premier pilote, utiliser des cas fictifs ou des cas réels anonymisés. Ne pas collecter de données client identifiantes tant que le backend authentifié et la politique de confidentialité ne sont pas en place.
