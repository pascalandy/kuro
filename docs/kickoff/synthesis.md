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

La lecture comparée et la revue de conception sont terminées. Le [laboratoire Go](implementation-plan.md) est maintenant implémenté. Ses sept cas passent : `clean`, `corrupt`, `truncate`, `resume`, `changed-etag`, `stall` et `budget`. `Verify` relit les artefacts bruts, recalcule les empreintes et le modèle, et refuse une preuve absente ou modifiée. `go test ./...`, `go test -race ./...` et `go vet ./...` passent avec Go 1.27.0. Le module fixe Go 1.25 comme minimum.

La preuve audio séparée utilise une origine HTTP Python sur loopback. Le laboratoire Go transporte les WAV, pas les FLAC. L'origine Python a transporté deux FLAC, puis le script a comparé leurs octets reçus et leur PCM décodé aux maîtres. MPD 0.24.15 a produit trois captures FIFO à partir des WAV admis par Go, des FLAC reçus, puis des mêmes FLAC lus directement par HTTP. Chaque capture contient 192 000 octets et 48 000 frames stéréo, avec le SHA-256 `24d01720643e20bd7f7e09cc52f5370a5aeb12c6536adba0198b1e7951144ff5` attendu.

Le script de build fixe la source MPD 0.24.15, son empreinte, Meson 1.12.0 et Ninja 1.13.2. Les bibliothèques de développement de l'hôte restent des entrées non verrouillées. Le build du laboratoire désactive toutes les sorties physiques. Les configurations, versions, journaux, réponses HTTP et comparaisons restent dans le dossier de chaque exécution. Le [relevé relançable](verification.md) donne les commandes et les résultats minimaux. Les grands artefacts bruts et les fichiers audio ne sont pas versionnés.

Aucun U-M1, KV produit, format matériel garanti, jitter physique ou classement sonore n'est accepté par cette note. Le NAS, l'installation propre, l'agent de session, ALSA, USB, le DDC, I2S, le DAC, l'analogique et l'écoute restent à éprouver.
