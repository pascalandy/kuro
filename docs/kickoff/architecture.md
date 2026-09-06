# Architecture retenue pour le démarrage audio

Ce document présente l'architecture courante à étudier après les laboratoires du kickoff. Les rapports de l'arena conservent leur décision historique sur un service, un agent salon et MPD. Cette décision ne fixe plus le nombre de machines, le moteur de production ou la limite entre KuroKor et un éventuel point de lecture distant. KD-044, KD-045.

## Usage avant les types

L'utilisateur choisit Salon puis appuie sur Lecture dans un album. Ce geste autorise la préparation et le démarrage. Kuro affiche la progression sans exiger une seconde confirmation. Une nouvelle sélection se prépare pendant que la file active reste intacte. Elle la remplace quand elle est prête. Une erreur conserve la lecture active lorsque celle-ci peut continuer.

```text
session.play_album(album, output="salon", operation=unique_id)
session.edit_queue(insert_next=[track, track], revision=current_revision)
session.control(pause, revision=current_revision)
view = session.snapshot()
```

Ces appels sont une esquisse produit. Le Kuro Client ne prépare ni URL, ni transaction, ni commande de moteur. Il ne décode pas, ne produit pas le son et ne transporte pas de PCM. Les occurrences distinguent les deux ajouts de la même piste. La fenêtre garde les commandes de lecture visibles et retrouve la position de liste au retour d'un album. Fermer la fenêtre conserve KuroKor. Quitter l'arrête après arrêt de la sortie. Un redémarrage restaure la file et la meilleure position enregistrée, sans son.

## Problème

Le [besoin amendé](scope-addendum.md) distingue KuroKor, les Kuro Clients et la bibliothèque musicale sur le NAS. KuroKor possède l'état durable et coordonne la lecture. Les Kuro Clients contrôlent KuroKor et affichent son état. Le NAS conserve les fichiers musicaux maîtres. Le nombre de machines dépend du [scénario de déploiement](../scenarios-deploiement.md). L'Aurender avec fichiers locaux est la référence à remplacer. Son protocole n'est pas une dépendance. Les modèles exacts et les domaines d'horloge du DDC et du DAC restent à identifier.

La priorité sonore exige des frontières observables. Kuro doit posséder ses tampons PCM et sa sortie audio. La place de cette responsabilité reste à définir lorsque le point de lecture est distant. Les protections de bibliothèque et de sauvegarde restent requises malgré le changement de trajet.

## Rôles et première cible

KuroKor possède le catalogue durable, les playlists, la file et la meilleure position rapportée. Ces données ne vivent pas sur le NAS par implication. Kuro lit les fichiers musicaux du NAS sans les modifier. La sauvegarde de Kuro ne dépend pas d'une seconde autorité durable au point de lecture.

```text
Kuro Client ── intentions ──> KuroKor
Kuro Client <── état ───────── KuroKor
                                 │
NAS, fichiers maîtres ───────────┤
consultés en lecture seule        │
                     moteur audio possédé par Kuro
                     tampons PCM et sortie locale
                                 │
                         USB → DDC → I2S → DAC
```

Ce diagramme décrit la [première cible dans le salon](../scenarios-deploiement.md#scénario-2-première-cible-dans-le-salon). KuroKor et le moteur audio partagent alors la machine reliée au DDC. Le Kuro Client peut partager cette machine ou fonctionner à distance. Dans le scénario où KuroKor et le Kuro Client occupent deux ordinateurs, l'emplacement du point de lecture reste ouvert. Le Kuro Client ne devient jamais le point de lecture par défaut.

## Candidat proposé pendant le kickoff

L'arena a proposé un agent salon avec un MPD privé. Cet agent adapterait une fenêtre courante et suivante à MPD. Il n'est pas implémenté. Les essais ont piloté MPD par des scripts silencieux et capturé sa sortie FIFO. La file MPD et les éventuels fichiers préparés resteraient reconstructibles dans cette proposition. Cette forme demeure une référence de comparaison, pas l'architecture de production exclusive.

Le laboratoire compare récupération progressive et préparation locale complète. Cette seconde politique est un comparateur de première classe face à la référence Aurender. Ni sa supériorité sonore ni son adoption par défaut ne sont décidées. Le même transfert et ses traces permettent de comparer attente initiale et manque de données dans un modèle déclaré.

Le Kuro Client n'apprend ni la représentation des médias, ni la file interne du moteur. Les [contrats](contracts.md) décrivent encore le candidat MPD pour conserver la preuve du kickoff. Ils marquent les limites que l'étude de KuroKor doit réévaluer.

Go reste le langage du laboratoire de transport. Son travail sur HTTP avec plages, fichiers, SHA-256, processus et tests reste valide, notamment l'usage de [`http.ServeContent`](https://pkg.go.dev/net/http#ServeContent). Cette preuve ne choisit pas le langage du produit.

L'étude de KuroKor évalue Rust en priorité, car Kuro doit posséder les tampons PCM et la sortie audio. Elle compare les mêmes responsabilités, budgets mémoire, coûts réseau et contraintes de maintenance avant toute adoption. Aucun portage du laboratoire Go n'est demandé et aucun avantage sonore n'est attribué au langage. KD-045.

MPD est le moteur déjà éprouvé pour comparaison. Son [protocole](https://mpd.readthedocs.io/en/stable/protocol.html) permet les fichiers locaux, les URL, la file et l'observation de lecture. Ses paramètres ne prouvent pas le format effectivement livré. Son [manuel](https://mpd.readthedocs.io/en/stable/user.html#bit-perfect-playback) décrit des conversions possibles lorsque le matériel refuse un format. Toute comparaison future doit relever la configuration, les traitements, les journaux et le format ALSA réel. Une capture FIFO silencieuse ne remplace pas cette preuve USB.

La livraison réseau détermine la disponibilité des données. Le timer du laboratoire détermine seulement les échéances de son modèle. Les horloges du périphérique USB, du DDC et de la conversion ne sont pas déduites de ces traces. Les [sources et inconnues d'horloge](research/transport-and-clock-domains.md) précisent cette distinction.

## Décision de synthèse

La [synthèse de l'arena](synthesis.md) a retenu A pour la propriété durable centralisée et MPD éphémère. Elle a ajouté la préparation vérifiée et ses erreurs depuis C, ainsi que le PCM canonique et les générations depuis B. Elle a rejeté la restauration distribuée et le transport PCM spécifique. Ce résultat historique reste intact. KD-044 et KD-045 rouvrent le moteur, le langage de production, la limite locale ou distante du moteur audio et le nombre de machines.

## Compromis proposés dans le candidat MPD

- La projection courte dans MPD exige de rapprocher ses observations de la file serveur. Elle évite une seconde bibliothèque durable.
- La préparation complète ajoute délai, stockage et vérification au salon. Ces coûts sont mesurés avant d'en faire un comportement produit.
- Le moteur existant limite le code audio à écrire, mais son format effectif, ses transitions et ses pannes restent à éprouver.
- Une perte du contrôle arrête après un délai de détection mesurable. Le retour ne reprend rien. Ce délai ne devient pas une promesse d'arrêt instantané.

## Alternatives considérées par l'arena

Dans le modèle étudié par l'arena, la file durable au renderer concentrait les transitions locales, mais obligeait la sauvegarde à coordonner deux états durables. Le staging n'exigeait pas ce partage. Le PCM poussé centralisait les décodeurs, mais ajoutait crédits, formats, générations et purge au protocole entre les deux machines supposées. L'arena a aussi rejeté un framework de renderers génériques pour son unique ordinateur cible. Ces conclusions décrivent le modèle historique. Elles ne fixent pas le point de lecture du scénario séparé.

La recherche initiale [recommandait Rust et une préparation complète](research/engine-and-language.md). L'arena a conservé cette option de transport comme expérience et a choisi Go pour les tâches du laboratoire. La recherche et l'arena restent des contributions datées. La priorité actuelle d'évaluer Rust vient de la responsabilité audio de Kuro, pas d'une adoption automatique de la recommandation initiale.

## Questions et risques ouverts

Quels formats et transitions passent sur le moteur et le DDC réels sans conversion inexpliquée ? Quel délai de départ et quel budget courant ou suivant conviennent au corpus cible ? Comment KuroKor se comporte-t-il sous import et recherche simultanés ? Où vit le point de lecture du scénario séparé ? Les essais locaux, préparés et progressifs donnent-ils une différence physique ou d'écoute reproductible avec moteur et connexions constants ?

La licence livrée, l'installation propre, le NAS réel, le corpus garanti, le gapless, la restauration et l'acceptation produit restent ouverts. Le laboratoire ne les remplace pas.

## Prochaine étude

Conserver le [laboratoire Go](implementation-plan.md) comme référence reproductible. Comparer ensuite les limites du moteur audio, dont Rust en priorité, sur les deux scénarios de déploiement avant de choisir le langage ou le moteur de production.
