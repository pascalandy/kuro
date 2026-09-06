# Preuve bornée et relançable

## Décision testée

Le premier outil teste que la piste jouable est un objet complet et vérifié, et qu'un délai de transfert devient une attente de préparation. Il doit aussi montrer qu'une piste suivante peut manquer son échéance malgré des octets finalement identiques. Il n'ouvre ni ALSA ni USB. Le modèle de temps n'est jamais nommé jitter DAC.

Les commandes ci-dessous sont proposées, pas exécutées. Le script Python de recherche existant a déjà comparé FLAC et PCM sur loopback, mais ne couvre pas encore les négatifs requis; ne pas recycler son succès comme résultat de cet outil.

```sh
cargo run --locked -p kuro-transport-probe -- fixture --out /tmp/kuro-stage-fixture
cargo run --locked -p kuro-transport-probe -- serve --root /tmp/kuro-stage-fixture --listen 127.0.0.1:8787
cargo run --locked -p kuro-transport-probe -- exercise --source http://127.0.0.1:8787 --out /tmp/kuro-stage-proof
cargo run --locked -p kuro-transport-probe -- verify --run /tmp/kuro-stage-proof
```

`fixture` produit deux pistes WAV PCM stéréo 48 kHz, 16 bits signés, dix secondes chacune. Les valeurs viennent d'une formule entière publique indexée par frame et canal; aucune fonction aléatoire dépendante de la plateforme. L'en-tête et le payload ont des empreintes distinctes. Un manifeste fixe endian, interleaving, ordre des canaux, profondeur valide, fréquence et nombre de frames. Les fichiers deviennent lecture seule. `serve` fait un spool local immuable borné avant publication, expose uniquement les IDs fixture, et enregistre les octets réellement envoyés. Aucune entrée NAS utilisateur.

`exercise` crée des dossiers serveur/récepteur séparés. Son transport réel est HTTP sur TCP, d'abord loopback; les nombres d'octets, l'ordre, les temps monotones et les points d'injection sont écrits avant synthèse. Il conserve les reçus de transfert et le résultat de validation de chaque objet. Les délais sont injectés dans l'outil, sans changer le réseau système.

## Cas obligatoires

| Cas | Manipulation | Résultat attendu |
| --- | --- | --- |
| Propre | Transfert, vérification et admission des deux pistes | Source, spool, envoyé et reçu ont mêmes octets; les deux pistes deviennent jouables. |
| Corruption | Un bit inversé dans le corps transmis après lecture du spool | SHA-256 reçu différent; zéro admission du fichier; résultat global du cas négatif passe seulement si rejet observé. |
| Troncature | Fermer la connexion avant la longueur annoncée | Aucun `.part` jouable; erreur de longueur ou transfert visible. |
| Reprise | Couper une réponse puis reprendre à un offset enregistré | Objet final identique; offsets et contenu relus vérifiés. Objet/ETag changé interdit la concaténation, nouvelle préparation nécessaire. |
| Source modifiée | Remplacer la fixture après publication du spool | L'objet publié demeure immuable; une nouvelle version a une nouvelle identité. Sources avant/après diffèrent seulement dans ce scénario d'injection. |
| Budget | Capacité inférieure aux deux objets réservés | Refus explicite avant Play; aucun objet réservé évincé. |
| Délai initial | Pause de livraison 200 ms avant vérification complète | Départ décalé d'au moins la pause observée; zéro consommation de fichier partiel. |
| Piste suivante tardive | Insérer la seconde piste non préparée pendant la première; la retenir jusqu'après sa fin | Arrêt à la frontière, cause « préparation tardive », même si les octets deviennent corrects ensuite; aucun redémarrage automatique. |
| Média indisponible | Arrêter seulement le service fichier après préparation; contrôle labo reste vivant | Consommation modélisée possible depuis cache, sans requête audio. |
| Contrôle perdu | Cesser le heartbeat du modèle | Arrêt au délai configuré, reconnexion arrêtée; indépendant du succès des médias. |

Le modèle consomme 480 frames par période de 10 ms. Son horloge virtuelle avance depuis des événements enregistrés, indépendamment du scheduler réel. Un départ staged intervient au premier tick suivant la validation requise. Une comparaison progressive commence avec 40 ms de données et compte chaque période où il manque des frames. La même trace reçue alimente les deux politiques; l'attente initiale reste comptée séparément des underruns. Les fichiers arrivés trop tard pour une transition produisent un arrêt de politique C, pas une prétendue défaillance USB. `verify` recalcule tout depuis les traces, rejette un fichier brut absent et exige les négatifs attendus.

Le rapport conserve `manifest.json`, les fixtures et corps reçus, `transfer.ndjson`, `simulation.ndjson`, `assertions.json`, source/spool/reçu SHA-256, versions, lockfile, commande exacte, code de sortie et budget cache. Les profils propres doivent rendre les mêmes empreintes et décisions, pas nécessairement les mêmes durées système. Exécuter aussi une fois serveur et récepteur sur deux machines de laboratoire démontrera le réseau réel; le loopback seul ne le démontre pas.

## Preuves suivantes, distinctes

| Étape | Observation et critère | Limite |
| --- | --- | --- |
| Décodeur réel | Encoder la fixture en FLAC puis décoder avec un outil figé; comparer PCM canonique frame par frame, canal compris. | Prouve ce décodeur et ces fixtures. Aucun moteur MPD ou output testé. [RFC FLAC](https://www.rfc-editor.org/rfc/rfc9639.html). |
| Agent + MPD local | Cache admis ajouté via socket Unix; queue doublonnée, retrait courant, seek, fin, crash à chaque point de commit, redémarrage arrêté. | Prouve la projection et les erreurs observées, pas le PCM après moteur. |
| Sortie MPD laboratoire | Capture du PCM dans un sink identifié et comparaison des échantillons. Paires de pistes complémentaires détectent frames manquantes/répétées. | Le sink de capture ne prouve pas le chemin USB réel. |
| Renderer et DDC | Inventorier USB/ALSA, jouer corpus natif, conserver conversion logs, `hw_params`, XRUN, périodes et buffers. USB retiré: arrêt sans repli. | Descripteurs et absence d'XRUN ne mesurent ni le DDC ni la conversion analogique. |
| Chaîne physique | Même DDC, USB, câble I2S, DAC et réglages; comparer fichiers locaux au salon, fichiers stagés par Kuro et lecture progressive sur le même moteur. | Isolation d'une variable possible seulement si format, niveau et branchement restent identiques. |

Le protocole minimal s'éprouve avant la comparaison sonore. Figement du build MPD, décodeurs compilés, dépendances et licence font partie de la reproductibilité; aucune dernière version supposée. Si MPD transforme le PCM sans contrôle suffisant ou échoue au corpus gapless, tester GStreamer avec ses [bindings Rust maintenus](https://github.com/GStreamer/gstreamer-rs), sans écrire un moteur complet. Un rejet de format est une preuve utile.

Le prochain essai matériel commence par identifier DDC, Terminator, firmware, endpoint USB et pinout. « Dynafripp » n'identifie pas encore le fabricant. La documentation générale [Denafrips](https://www.denafrips.com/support/1000) décrit des FIFO et un reclocking, mais ne prouve pas leur fonctionnement dans ces appareils. Conserver aussi le branchement Aurender vers DDC réel et les réglages Conductor 5. Ne pas attribuer à HTTP un changement d'entrée DDC entre les cas.

Puis comparer Aurender local à MPD local sur le salon, et MPD local aux deux modes réseau. La lecture staged garde son heartbeat pour respecter l'arrêt sur perte du contrôle. Un test de silence réseau complet exige un mode laboratoire isolé, explicitement exclu du comportement produit. Mesurer au moins le format, le niveau analogique et les transitions. Avec un ADC/analyseur adapté, conserver captures brutes, calibration, bruit propre et spectres; sans cet équipement, consigner le manque de mesure physique et poursuivre la compatibilité et l'écoute contrôlée.

L'écoute utilise un ordre randomisé masqué, les mêmes extraits et un niveau analogique vérifié. Préannoncer durée, nombre d'essais et analyse; conserver les réponses individuelles. [ITU-R BS.1116-3](https://www.itu.int/rec/R-REC-BS.1116-3-201502-I/en) fournit une méthode de référence. Une différence répétable appelle une recherche de cause; des hashes égaux ou un essai non discriminant ne prouvent aucune identité sonore universelle. L'ancien résultat Roon n'a pas de cause attribuée.

C perd si ses préparations ou son stockage sont inacceptables sur le corpus réel, si sa sauvegarde distribuée ne peut respecter KV-011 simplement, ou si une autre forme passe les mêmes critères numériques et physiques avec une meilleure expérience. Le choix Rust est révisé si le prototype révèle une complexité de dépendances, de packaging ou de maintenance inutile face à Go. Aucun de ces verdicts ne demande une affirmation sur le son d'un langage.
