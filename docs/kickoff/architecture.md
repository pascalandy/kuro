# Architecture retenue pour le démarrage audio

## Usage avant les types

L'utilisateur choisit Salon puis appuie sur Lecture dans un album. Ce geste autorise la préparation et le démarrage. Kuro affiche la progression sans exiger une seconde confirmation. Une nouvelle sélection se prépare pendant que la file active reste intacte. Elle la remplace quand elle est prête. Une erreur conserve la lecture active lorsque celle-ci peut continuer.

```text
session.play_album(album, renderer="salon", operation=unique_id)
session.edit_queue(insert_next=[track, track], revision=current_revision)
session.control(pause, revision=current_revision)
view = session.snapshot()
```

Ces appels sont une esquisse produit. Le client ne prépare ni URL, ni transaction, ni commande MPD. Les occurrences distinguent les deux ajouts de la même piste. La fenêtre garde les commandes de lecture visibles et retrouve la position de liste au retour d'un album. Fermer la fenêtre conserve le service. Quitter l'arrête après arrêt du renderer. Un redémarrage restaure la file et la meilleure position enregistrée, sans son.

## Problème

Le [nouveau besoin](scope-addendum.md) fixe deux machines distinctes. Le serveur lit le NAS et l'ordinateur du salon sort en USB vers le DDC, puis en I2S sur HDMI vers le Terminator. L'Aurender avec fichiers locaux est la référence à remplacer. Son protocole n'est pas une dépendance. Les modèles exacts et les domaines d'horloge du DDC et du DAC restent à identifier.

La priorité sonore exige des frontières observables. Elle ne justifie pas de construire un moteur audio avant d'avoir éprouvé un moteur existant. Les protections de bibliothèque et de sauvegarde restent requises malgré le changement de trajet.

## Forme

Le serveur possède toute la bibliothèque durable, les playlists, la file et la meilleure position rapportée. Un agent au salon adapte une fenêtre courante/suivante à un MPD privé. MPD possède décodage et exécution audio. La file MPD et les éventuels fichiers préparés sont reconstructibles. La sauvegarde ne dépend donc pas d'une seconde autorité durable au salon.

```text
Fenêtre ── commandes métier ──> service Kuro, état durable unique
                                  │
NAS, lecture seule ──> origine de fichiers ── HTTP ──> agent salon
                                                     │
                           comparaison laboratoire   ├─ URL progressive
                                                     └─ fichier complet vérifié
                                                            │
                                                         MPD privé
                                                   décodage et tampon PCM
                                                            │
                                                    ALSA et pilote USB
                                                            │
                                                     USB → DDC → I2S → DAC
Service Kuro ── contrôle autorisé ──> agent ── socket Unix ──> MPD
```

Le laboratoire compare récupération progressive et préparation locale complète. Cette seconde politique est un comparateur de première classe face à la référence Aurender. Ni sa supériorité sonore ni son adoption par défaut ne sont décidées. Le même transfert et ses traces permettent de comparer attente initiale et manque de données dans un modèle déclaré.

Le serveur de fichiers ne décode ni ne traite le signal. Le futur agent cache les commandes MPD, la projection d'occurrences et l'arrêt sur perte du contrôle. Les [contrats](contracts.md) concentrent ces règles dans leurs propriétaires, conformément à boundary-discipline et minimize-reader-load. Un client n'a pas à apprendre la représentation HTTP ou la file interne du moteur.

Go est retenu pour le laboratoire et comme direction provisoire du premier service. Le travail immédiat consiste en HTTP avec plages, fichiers, SHA-256, processus et tests. La bibliothèque standard couvre ces besoins, notamment [`http.ServeContent`](https://pkg.go.dev/net/http#ServeContent). Ce choix évite de décider un moteur et une interface FFI avec le langage du serveur. Rust reste une alternative crédible si les mesures de service, le typage ou le coût de maintenance l'emportent. Aucun avantage sonore n'est attribué au langage.

MPD est le premier moteur à éprouver, car son [protocole](https://mpd.readthedocs.io/en/stable/protocol.html) permet les fichiers locaux, les URL, la file et l'observation de lecture. Ses paramètres ne prouvent pas le format effectivement livré. Son [manuel](https://mpd.readthedocs.io/en/stable/user.html#bit-perfect-playback) décrit des conversions possibles lorsque le matériel refuse un format. Le profil futur exige de relever configuration, traitements, journaux et format ALSA réel. Une capture FIFO silencieuse ne remplace pas cette preuve USB.

La livraison réseau détermine la disponibilité des données. Le timer du laboratoire détermine seulement les échéances de son modèle. Les horloges du périphérique USB, du DDC et de la conversion ne sont pas déduites de ces traces. Les [sources et inconnues d'horloge](research/transport-and-clock-domains.md) précisent cette distinction.

## Décision de synthèse

La [synthèse de l'arena](synthesis.md) retient A pour la propriété durable centralisée et MPD éphémère. Elle ajoute la préparation vérifiée et ses erreurs depuis C, ainsi que le PCM canonique et les générations depuis B. Elle rejette la restauration distribuée et le transport PCM spécifique.

## Compromis acceptés

- La projection courte dans MPD exige de rapprocher ses observations de la file serveur. Elle évite une seconde bibliothèque durable.
- La préparation complète ajoute délai, stockage et vérification au salon. Ces coûts sont mesurés avant d'en faire un comportement produit.
- Le moteur existant limite le code audio à écrire, mais son format effectif, ses transitions et ses pannes restent à éprouver.
- Une perte du contrôle arrête après un délai de détection mesurable. Le retour ne reprend rien. Ce délai ne devient pas une promesse d'arrêt instantané.

## Alternatives considérées

La file durable au renderer concentre les transitions locales, mais oblige la sauvegarde à coordonner deux états durables. Le staging n'exige pas ce partage. Le PCM poussé centralise les décodeurs, mais ajoute crédits, formats, générations et purge à un protocole que les deux machines doivent connaître. Aucun besoin observé ne justifie encore ce coût. Un framework de renderers génériques reporte aussi trop de décisions pour l'unique ordinateur cible.

La recherche initiale [recommandait Rust et une préparation complète](research/engine-and-language.md). L'arena conserve cette option de transport comme expérience et choisit Go pour les tâches effectivement retenues. La recherche reste une contribution datée, pas une seconde décision active.

## Questions et risques ouverts

Quels formats et transitions passent sur le build MPD et le DDC réels sans conversion inexpliquée ? Quel délai de départ et quel budget courant/suivant conviennent au corpus cible ? Comment le service se comporte-t-il sous import et recherche simultanés ? L'arrêt sur crash de l'agent et la reprise arrêtée passent-ils sur deux machines ? Les essais locaux, préparés et progressifs donnent-ils une différence physique ou d'écoute reproductible avec moteur et connexions constants ?

La licence livrée, l'installation propre, le NAS réel, le corpus garanti, le gapless, la restauration et l'acceptation produit restent ouverts. Le laboratoire ne les remplace pas.

## Première étape d'implémentation

Construire le [laboratoire Go](implementation-plan.md), puis exécuter ses contrôles positifs et négatifs avant de présenter un résultat de transport.
