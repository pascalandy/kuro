# Programme documentaire P1 à P5

Le programme prépare une décision de développement de kuro. Son résultat est un dossier traçable sur le produit, les fonctions de référence, la faisabilité et l'ordre d'exécution. Il ne réalise aucune milestone produit.

L'autorisation et les paramètres confirmés figurent dans le [contexte utilisateur](contexte-utilisateur.md). Le MVP conserve la cible de 20 000 albums et 3 To dès M1.

## Livrables et critères de passage

| Phase | Travail attendu | Critère de passage contrôlé par le coordinateur |
| --- | --- | --- |
| P1 | Usages, cible, frontière MVP, corpus de référence et structure documentaire | Les paramètres confirmés sont distingués des inconnues. Les critères M1 sont identifiés. Le programme, la checklist et le journal existent. Les liens locaux fonctionnent. |
| P2 | Inventaire fonctionnel du serveur et du desktop, corpus sourcé, identifiants stables | Chaque domaine est couvert par des fonctions identifiées, une portée et un statut de preuve. Chaque affirmation sur Roon renvoie à une source ou à une observation à faire. Les lacunes sont visibles. |
| P3 | Faisabilité, options d'architecture, contrats entre composants et fournisseurs | Les options répondent aux fonctions P2 et aux contraintes M1. Les risques techniques et dépendances externes ont une conclusion ou un test futur. Aucune recommandation n'est présentée comme une décision approuvée. |
| P4 | Six plans de domaine, sept milestones et stratégie de validation | Chaque fonction retenue a un domaine et une milestone. Les dépendances, sorties attendues et validations sont définies. M1 inclut la taille cible et le NAS. |
| P5 | Revue de couverture et cohérence, consolidation et décisions ouvertes | Aucun élément obligatoire n'est perdu entre usages, fonctions, architecture, plans et validation. Chaque écart a un statut et un responsable de décision. Le dossier est lisible depuis le README. |

P1 précède P2, qui précède P3, puis P4, puis P5. Une passation produite n'est pas une approbation. Le coordinateur examine les fichiers et les preuves avant de consigner le passage dans le journal.

## Portée des phases

P2 vise un inventaire exhaustif dans le périmètre documenté du serveur et du desktop. Cette ambition ne prouve pas la parité avec toutes les versions de Roon. Le relevé indique la date de consultation, la version connue ou inconnue, et les surfaces non observées.

P3 étudie les rôles serveur, contrôle et sortie sur une même machine, puis leur séparation future. Le monorepo modulaire est une recommandation de départ. Les choix de langage, interface, base de données, moteur audio et protocole restent à comparer. Les contrats sont documentaires. Aucun code ni prototype ne valide leur faisabilité pendant ce programme.

P4 contient exactement six plans de domaine. Le découpage proposé ci-dessous sera vérifié contre P2 et P3. Un changement de découpage qui modifie le périmètre reste une proposition pour l'utilisateur.

| Domaine proposé | Contenu à planifier |
| --- | --- |
| Bibliothèque et métadonnées | Sources, import, index, identités, éditions et enrichissement |
| Lecture et audio | File de lecture, moteur, sortie, gapless et traitements audio |
| Desktop et usages | Navigation, recherche, playlists et interactions Linux |
| Réseau et distribution | Contrôleurs, endpoints, zones et synchronisation |
| Découverte et intégrations | Recommandations, fournisseurs et services facultatifs |
| Plateforme et exploitation | Persistance, sauvegarde, sécurité, packaging, performance et portabilité |

Chaque plan devra relier les fonctions P2, les options P3, les milestones et les preuves futures. Les plans ne sont pas encore créés en P1.

## Milestones produit à affiner en P4

| Milestone | Frontière approuvée |
| --- | --- |
| M1 | Linux local, import local et NAS, albums, artistes, recherche, playlists, file, sortie locale, gapless sur formats retenus, persistance, sauvegarde restaurable, sources intactes, fonctionnement sans Internet, bibliothèque cible de 20 000 albums |
| M2 | Bibliothèque avancée, éditions, crédits, classique, Focus, tags et exports |
| M3 | Mode exclusif, signal path et DSP audiophile |
| M4 | Contrôleurs, endpoints et zones indépendantes, puis synchronisation entre zones |
| M5 | Découverte et intégrations sous réserve de faisabilité et de droits d'accès |
| M6 | Autres desktops et approfondissement des performances, au-delà du niveau déjà requis en M1 |
| M7 | Mobile futur |

Les milestones décrivent un ordre produit. Elles ne constituent ni un calendrier, ni une autorisation de développement. P4 doit rendre explicites les étapes intermédiaires de M4 et les conditions d'entrée de M5.

## Corpus documentaire et limites de preuve

Les chercheurs préparatoires ont signalé quatre sources Roon consultées le 5 septembre 2026. P2 doit les consulter de nouveau et enregistrer les affirmations utiles avec des identifiants. P1 conserve uniquement leurs adresses, sans reprendre de faits techniques non vérifiés.

| Source signalée | Usage prévu en P2 |
| --- | --- |
| `https://help.roonlabs.com/portal/en/kb/articles/architecture` | Rôles et frontières du système de référence |
| `https://help.roonlabs.com/portal/en/kb/articles/metadata-model` | Organisation des métadonnées |
| `https://help.roonlabs.com/portal/en/kb/articles/raat` | Réseau audio de référence et limites d'accès à étudier |
| `https://roon.app/en/valence` | Découverte et enrichissement à examiner |

Roon n'a pas été exécuté. Sa version et son build sont inconnus. P2 distingue faits sourcés, inférences de conception et comportements à observer. Une source inaccessible reste une lacune, sans contenu inventé. Aucun examen des médias de l'utilisateur n'est nécessaire pour ce corpus.

## Protocole des agents

Le coordinateur affecte un agent neuf à chaque phase. Tous utilisent GPT-6 Astra avec effort medium, conformément à l'instruction utilisateur. L'agent lit la passation précédente, les contraintes et les livrables dont il dépend.

L'agent de phase possède les écritures du répertoire kuro pendant sa phase. Le coordinateur reste en lecture pendant la rédaction. Après passation, l'agent cesse les écritures et le coordinateur reprend la main pour la revue. Le coordinateur peut lancer des chercheurs indépendants en lecture seule pendant une phase. Ces chercheurs ne deviennent pas écrivains. Aucun agent de phase ou chercheur ne délègue à son tour.

La passation contient le travail terminé, les fichiers modifiés, les vérifications réellement exécutées, les limites et la suite attendue. Les décisions vont dans `docs/decisions.tsv`, sans réécriture de l'historique. Une correction de décision ajoute une ligne qui remplace explicitement la conclusion précédente.

Le coordinateur crée les commits après revue, puis publie le dossier selon l'autorisation existante. Il peut déléguer ces opérations Git à l'agent de phase après validation explicite. L'autorisation de push et de PR ne permet pas de prétendre qu'une publication a eu lieu sans URL et SHA vérifiables. Aucun agent ne modifie le wiki `johnny` ni les skills installés.

## Checkpoint de débit

| Dimension | Organisation retenue | Réexamen |
| --- | --- | --- |
| Premiers travaux bloquants | Validation des critères P1 avant l'inventaire P2 | À chaque passage de phase |
| Travaux indépendants | La recherche du coordinateur peut préparer des sources sans écrire dans les fichiers de l'agent | Si une recherche change les données d'entrée |
| État partagé | Un seul écrivain pour kuro et le journal, transfert explicite à la passation | Avant toute correction ou publication |
| Plus petite décomposition sûre | Un agent par phase, car les mêmes critères et identifiants traversent ses documents | Au début de P2, P3, P4 et P5 |

Le coordinateur relève l'avancement, les lacunes et les décisions à chaque phase. Aucun délai de développement n'est inventé à partir du nombre de documents rédigés.

## Définition de fin vérifiable

Le programme documentaire est terminé lorsque P1 à P5 ont passé leur revue, que les liens et identifiants se résolvent, et que chaque exigence a une disposition explicite. Les recommandations ouvertes restent nommées, avec l'information manquante et leur effet sur la suite.

La checklist distingue la fin documentaire de la publication Git. Une publication complète exige les références réelles du dépôt distant, du commit et de la PR. Si l'accès distant manque, le coordinateur termine et vérifie le dossier local, puis décrit exactement ce blocage.

La fin ne signifie ni que le MVP fonctionne, ni que la faisabilité est démontrée par exécution. L'utilisateur devra autoriser séparément tout développement. La licence exacte reste une décision ouverte.
