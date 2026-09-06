# Produit et frontière du MVP

kuro vise l'écoute d'une grande bibliothèque personnelle depuis un desktop Linux. Le premier usage associe les fichiers locaux et un dossier NAS. L'accès Internet ne doit pas conditionner la consultation ou la lecture des fichiers disponibles.

Les données confirmées proviennent du [contexte utilisateur](contexte-utilisateur.md). Les critères ci-dessous stabilisent le périmètre du MVP, appelé M1 dans le [programme](programme.md). Les seuils encore inconnus restent ouverts.

## Utilisateur cible et besoins

L'utilisateur initial possède environ 20 000 albums, soit environ 3 To. Il veut retrouver un album, parcourir un artiste et écouter une suite de pistes depuis Linux sur Omarchy. Cette cible impose de considérer le volume dès l'import et la navigation du MVP.

| Priorité | Besoin | Conséquence pour M1 |
| --- | --- | --- |
| Obligatoire | Écouter les fichiers qu'il possède | Import local et NAS, sortie locale, aucune dépendance à un service de streaming |
| Obligatoire | Retrouver sa musique | Vues albums et artistes, recherche dans la bibliothèque indexée |
| Obligatoire | Choisir ce qui joue ensuite | Playlists et file de lecture modifiables |
| Obligatoire | Écouter un album continu | Gapless sur le corpus de formats retenus |
| Obligatoire | Conserver son travail | Persistance, sauvegarde et restauration vérifiables |
| Obligatoire | Protéger les originaux | Sources intactes pendant toutes les opérations du MVP |
| Obligatoire | Utiliser sa bibliothèque sans Internet | Métadonnées locales et lecture des sources joignables sans service externe |
| Ultérieur | Approfondir la bibliothèque et le son | M2 pour les métadonnées avancées, M3 pour les fonctions audiophiles |
| Ultérieur | Distribuer l'écoute et découvrir d'autres contenus | M4 pour le réseau audio, M5 pour les intégrations conditionnelles |

## Parcours qui définissent M1

| ID | Situation et action | Résultat attendu | Cas à documenter en P2 à P4 |
| --- | --- | --- | --- |
| U-01 | Ajouter un dossier local et un dossier NAS à la bibliothèque | Les fichiers pris en charge deviennent consultables sans modifier les sources | Chemins indisponibles, permissions, fichiers invalides et reprise d'import |
| U-02 | Ouvrir les albums puis un artiste | Retrouver les albums et les pistes correspondantes | Compilation, artiste absent, plusieurs disques, homonymes |
| U-03 | Rechercher un album, un artiste ou une piste | Obtenir des résultats exploitables dans la bibliothèque cible | Accents, titres absents et résultats nombreux |
| U-04 | Lancer un album puis modifier la file | Le lecteur respecte l'ordre choisi et les commandes locales | Passage de piste, pause, reprise, fin de file et erreur de lecture |
| U-05 | Enregistrer une sélection dans une playlist | Retrouver la sélection après redémarrage | Réordonnancement, référence à une piste devenue indisponible |
| U-06 | Écouter deux pistes qui s'enchaînent | Aucun silence ajouté entre les pistes du corpus gapless retenu | Frontières de formats, paramètres audio et limites du décodeur |
| U-07 | Fermer puis rouvrir kuro | Retrouver les données persistantes prévues par le contrat M1 | Données sauvegardées, état de lecture restauré ou non, arrêt imprévu |
| U-08 | Restaurer une sauvegarde de kuro | Retrouver une bibliothèque et ses playlists utilisables avec les sources disponibles | Version de sauvegarde, chemins déplacés, absence de sources |
| U-09 | Couper Internet tout en gardant le réseau local | Continuer à naviguer et lire les fichiers locaux ou NAS accessibles | Enrichissement externe indisponible, état du NAS distinct d'Internet |
| U-10 | Ouvrir une bibliothèque à l'échelle cible | Importer, rechercher, naviguer et lire avec 20 000 albums | Temps, mémoire, nombre réel de pistes et charge réseau à mesurer plus tard |

Les cas de la dernière colonne précisent le travail documentaire restant. Ils n'ajoutent pas silencieusement une promesse de comportement. P3 propose les contrats exacts. P4 définit les preuves et distingue critères approuvés et seuils proposés.

## Critères stables du MVP

| ID | Critère obligatoire | Preuve future attendue | Paramètres encore ouverts |
| --- | --- | --- | --- |
| MVP-01 | Fonctionner sur Linux dans l'environnement Omarchy | Parcours M1 sur un environnement identifié et reproductible | Versions, distribution et contraintes de packaging |
| MVP-02 | Importer des sources locales et un dossier NAS | Corpus des deux origines retrouvé après import et reprise | Protocole NAS, stratégie de montage et formats |
| MVP-03 | Supporter 20 000 albums, environ 3 To, dès M1 | Import, navigation, recherche et lecture sur un corpus à cette échelle | Pistes, matériel et budgets de temps ou mémoire |
| MVP-04 | Fournir les vues albums et artistes et la recherche | U-02 et U-03 réussis sur le corpus défini | Champs, règles de tri et rapprochements minimaux |
| MVP-05 | Fournir playlists, file et sortie locale | U-04 et U-05 réussis avec une sortie identifiée | Sortie, DAC et politiques de file |
| MVP-06 | Assurer le gapless sur les formats retenus | Mesure et écoute d'enchaînements dont le résultat attendu est connu | Formats, paramètres audio et méthode de mesure |
| MVP-07 | Conserver les données M1 après redémarrage | Comparaison de l'état persistant avant et après redémarrage | Contrat exact d'état persistant et reprise audio |
| MVP-08 | Fournir une sauvegarde restaurable | Restauration isolée avec comparaison des données et lecture d'une piste | Contenu, versionnement et gestion des chemins |
| MVP-09 | Laisser les fichiers sources intacts | Comparaison des sources avant et après import, lecture et restauration | Corpus et méthode de contrôle non destructive |
| MVP-10 | Permettre l'usage local sans Internet | U-09 sans accès aux services externes | Définition des données déjà disponibles et cache local |

Ces preuves sont à planifier. Aucune n'a été exécutée sur un produit kuro. Une démonstration avec quelques albums ne validerait pas MVP-03.

Une sauvegarde de kuro vise d'abord les données de l'application. Sa portée exacte reste à définir. Le dossier ne promet pas de dupliquer les 3 To de médias dans chaque sauvegarde.

Sans Internet signifie sans dépendance à Internet pour l'usage local. Lire sur le NAS suppose que le NAS reste joignable. Copier toute la bibliothèque pour écouter sans réseau local ne fait pas partie de la promesse M1.

## Frontière des fonctions ultérieures

M1 n'attend ni une implémentation RAAT, ni un compte de streaming, ni un fournisseur de métadonnées en ligne. P3 doit prévoir comment un fournisseur optionnel se raccorde sans rendre le fonctionnement local dépendant de ce fournisseur.

Les éditions, crédits détaillés, usages classiques, Focus, tags avancés et exports appartiennent à M2. M1 a toutefois besoin d'un modèle minimal cohérent pour album, artiste et piste. P2 et P3 doivent distinguer ce socle des capacités avancées.

Le mode exclusif, le signal path détaillé et le DSP appartiennent à M3. La sortie locale et le gapless restent obligatoires en M1. Le réseau de M4 désigne les contrôleurs et sorties distribuées. L'accès à un dossier NAS appartient déjà à M1.

Les intégrations de M5 dépendent de leurs interfaces, conditions d'accès et possibilités réelles. Les autres desktops relèvent de M6 et le mobile de M7. Aucun service externe ni logiciel de référence n'est considéré réutilisable sans examen.

## Environnement connu et inconnu

| Élément | Statut | Conséquence documentaire |
| --- | --- | --- |
| Desktop initial | Linux sur Omarchy confirmé | Priorité M1, versions à préciser |
| Volume | Environ 20 000 albums et 3 To confirmés | Dimensionner les preuves dès M1 |
| Nombre de pistes | Inconnu | Aucun ratio pistes par album supposé comme fait |
| Formats et paramètres audio | Inconnus | Corpus gapless et compatibilité à proposer, sans garantie générale |
| Matériel serveur | Inconnu | Aucun budget de performance présenté comme mesuré |
| Coexistence serveur, contrôle et sortie | Option initiale à étudier | Comparer un déploiement local avec séparation future |
| Protocole NAS et montage | Inconnus | Définir une frontière d'accès et les défaillances à prévoir |
| Débit et latence réseau | Inconnus | Validation NAS conditionnée à un environnement décrit |
| DAC et sortie audio | Inconnus | Aucun engagement sur une interface ou capacité matérielle précise |
| Qualité et organisation des tags | Inconnues | Décrire corpus incomplet et priorités de données en P2 |
| Besoin multi-utilisateur | Non précisé | Ne pas l'ajouter à M1 par défaut |
| Licence du projet | Ouverte | Comparer des options, sans fichier de licence imposé |
| Version et build Roon | Inconnus, application non exécutée | Documenter les limites de couverture en P2 |

## Décisions à garder ouvertes

| ID | Question | État | Traitement attendu |
| --- | --- | --- | --- |
| O-01 | Quelle licence open source choisir ? | Décision utilisateur requise | P3 examine les contraintes des dépendances, P5 présente les options |
| O-02 | Quels formats et paramètres audio garantir en M1 ? | Données utilisateur manquantes | Proposer un corpus et identifier les exclusions avant engagement |
| O-03 | Quels seuils de temps et mémoire rendent M1 acceptable ? | Matériel et nombre de pistes inconnus | P4 propose métriques et seuils à approuver, sans assouplir le volume cible |
| O-04 | Comment accéder au dossier NAS ? | Protocole inconnu | P3 compare les options sans configurer la machine |
| O-05 | Quelle stack et quel moteur audio retenir ? | Aucun choix approuvé | P3 compare faisabilité, maintenance, licence et preuves futures |
| O-06 | Quel état conserver et sauvegarder exactement ? | Contrats à préciser | P3 décrit les données, P4 relie la restauration aux parcours |
| O-07 | Quels fournisseurs externes restent accessibles ? | Faisabilité à documenter | P3 puis M5, aucune dépendance imposée au MVP |

Les propositions qui précisent ces questions devront porter leur statut. Le coordinateur ne remplace pas une approbation manquante par une hypothèse silencieuse.
