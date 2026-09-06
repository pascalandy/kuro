# Synthèse de l'arena audio

La base retenue est A. Le serveur conserve bibliothèque, file et sauvegarde durables. Le renderer conserve une exécution MPD reconstructible. Go est choisi pour le laboratoire et comme direction provisoire du premier service. Cette décision n'est ni une garantie sonore ni une adoption de stack complète.

## Candidats et jugement

Les trois candidats et le juge ont utilisé GPT-6 Astra avec raisonnement high. Le parent a lu les neuf fichiers intégralement avant son classement. Le juge a reçu les candidats terminés et la [rubrique](arena/rubric.md), sans la préférence du parent. Aucun candidat SQ n'a abandonné. Deux candidats de la première exploration locale ont été interrompus après le changement de besoin; ils ne sont pas des échecs de cette arena.

| Critère, sur 2 | Parent A | Parent B | Parent C | Juge A | Juge B | Juge C |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Responsabilités audio et horloges | 2 | 2 | 2 | 2 | 2 | 2 |
| Fidélité au besoin réseau | 2 | 2 | 2 | 2 | 2 | 2 |
| Faisabilité protocolaire et matériel | 2 | 1 | 2 | 2 | 2 | 2 |
| Preuve synthétique falsifiable | 2 | 2 | 2 | 2 | 2 | 2 |
| Architecture et langage proportionnés | 2 | 1 | 1 | 2 | 1 | 1 |
| Conclusion SQ et prochain essai | 2 | 2 | 2 | 2 | 2 | 2 |
| Total | 12 | 10 | 11 | 12 | 11 | 11 |

Le point d'écart sur B vient d'une prudence du parent devant un nouveau protocole PCM à réaliser. Il ne change ni la base ni les greffes. Le [jugement](arena/judgment.md) et le [classement du parent](arena/parent-score.md) restent disponibles avec les paquets [A](arena/a/rationale.md), [B](arena/b/rationale.md) et [C](arena/c/rationale.md).

## Base et greffes

| Source | Décision retenue | Raison |
| --- | --- | --- |
| A | Propriété durable au serveur, agent MPD privé et projection courante/suivante | Une sauvegarde cohérente n'exige pas deux magasins de file durables. |
| C | Préparation complète vérifiée comme comparateur de première classe | Compare concrètement la lecture préparée à la récupération progressive, avec la référence Aurender locale comme motivation. Aucun vainqueur sonore présumé. |
| C | Temporaire isolé, admission atomique et budget courant/suivant | Un fichier incomplet ou corrompu ne devient jamais jouable; le stockage et l'attente restent visibles. |
| C | Préparer le remplacement sans détruire la file jouée | Le geste Lecture reste unique et une préparation lente ne force pas un arrêt préalable. |
| C | Perte média distincte de perte du contrôle | Le fichier local disponible ne constitue pas une autorisation de lecture autonome. |
| B | PCM canonique, générations et incertitude de position | Les preuves portent sur des mots définis; la future session ne confond pas reçu réseau et position réellement rapportée. |

Les greffes de cycle de vie sont des contrats futurs. La première implémentation ne fabrique pas de faux agent de session pour les déclarer testées. Le laboratoire [borné](implementation-plan.md) porte sur le transfert et les décisions de préparation seulement.

## Rejets et contrôle de la forme

La file durable au renderer de C est rejetée. Elle oblige sauvegarde et restauration à coordonner les deux machines, alors que le contrat de snapshot complet existe déjà. Le staging garde sa valeur sans cette seconde autorité.

Le protocole PCM de B, ses crédits et son framing sont rejetés pour ce lot. Aucun besoin établi de DSP ou de ressources renderer insuffisantes ne justifie de le maintenir. Les outils de preuve de PCM n'imposent pas le même transport en production.

Le framework de renderers génériques, les deux caches obligatoires et la copie préalable systématique de tout album ne sont pas adoptés. Ils ajoutent abstractions, attente ou stockage avant mesure. La version immuable sur NAS reste un problème réel à résoudre, pas une garantie héritée des fixtures du laboratoire.

Le contrôle des red flags a écarté le partage durable qui laisse fuir ses règles dans la sauvegarde. L'API publique conserve une opération Lecture qui cache préparation et activation. La frontière renderer n'est justifiée que par les règles MPD, les observations et le contrôle de session qu'elle possède. Aucun bus universel ni chaîne de wrappers n'est ajouté.

## Vérification et état

La lecture comparée et la revue de conception sont terminées. L'implémentation du laboratoire est autorisée par le [plan stable](implementation-plan.md). Au moment de cette synthèse, ses contrôles sont en attente. Aucun succès de la preuve préliminaire ou du build MPD ne remplace cette exécution.

Le parent complétera ici les résultats réellement obtenus, les artefacts et toute déviation de contrat après les tests Go, les contrôles négatifs et les essais FLAC ou MPD distincts. Aucun U-M1, KV produit, format garanti, jitter physique ou classement sonore n'est accepté par cette note.
