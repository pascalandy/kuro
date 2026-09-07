# Plan de preuve progressif

## Premier programme à implémenter

`kuro-pull-probe` sera un seul programme Go avec scénarios, origine HTTP et récepteur de laboratoire en goroutines séparées. Aucun accès ALSA, fichier utilisateur ou NAS réel. Exposer uniquement des IDs de fixtures sur `127.0.0.1`. Générer PCM entier stéréo 48 kHz/16 bits à motif déterministe, puis son conteneur WAV ; conserver séparément les empreintes du fichier et du PCM canonique little-endian interleavé.

Le récepteur vérifie les en-têtes WAV, reconstitue les frames et enregistre leurs arrivées monotones. Son consommateur modélisé retire 480 frames par période de 10 ms après 250 ms de PCM disponible. Il calcule, depuis la trace reçue, frames arrivées après échéance, minimum du tampon et périodes d'underrun. Il ne produit aucun son, ne simule aucune boucle USB et ne mesure aucun jitter de DAC.

La source envoie des blocs PCM correspondant à 10 ms à travers HTTP. Le scénario de délai suspend les octets après le début modélisé pendant 600 ms. Le modèle ne s'arrête pas pendant ce trou et ne redéfinit pas son origine temporelle après une panne. Le scénario troncature conserve la longueur attendue indépendante du nombre reçu. L'intégrité finale et les échéances constituent deux résultats distincts.

Commandes futures depuis le répertoire du prototype retenu :

```sh
go version
go test ./...
go run ./cmd/kuro-pull-probe --scenario clean --out artifacts/clean
go run ./cmd/kuro-pull-probe --scenario corrupt --out artifacts/corrupt
go run ./cmd/kuro-pull-probe --scenario truncate --out artifacts/truncate
go run ./cmd/kuro-pull-probe --scenario stall --out artifacts/stall
go run ./cmd/kuro-pull-probe --scenario range-resume --out artifacts/range
go run ./cmd/kuro-pull-probe --recompute artifacts/stall/arrivals.ndjson
```

| Scénario | Résultat observable attendu |
| --- | --- |
| Normal | Fichier et PCM reçus égaux ; 0 période d'underrun dans ce profil |
| Corruption | Un bit modifié dans le payload WAV fait échouer empreinte fichier et PCM, même si toutes les échéances passent |
| Troncature | EOF prématurée visible, longueur et empreinte fausses ; aucune réussite de transfert partiel |
| Pause de 600 ms | Octets et PCM finalement identiques ; au moins une période tardive/underrun avec le tampon de 250 ms |
| Plage/reprise | Une coupure puis requête Range reconstitue le fichier exact, ou un changement de validateur le fait rejeter ; ceci ne prouve pas une reprise MPD sans rupture |
| Recalcul | Les mêmes arrivées donnent exactement les mêmes résultats du modèle sans relancer le transfert |

Conserver `manifest.json`, versions, paramètres de profils, `source.wav`, PCM maître/reçu, tailles, SHA-256 source avant/après, statut HTTP/Content-Range, erreurs, trace d'arrivées et `result.json`. L'origine n'ouvre les fixtures qu'en lecture ; les fautes touchent le flux reçu, jamais le maître. Un scénario échoue avec code non nul si son oracle négatif ne détecte pas la faute. Ne pas compter une détection attendue comme échec de la suite.

Ajouter ensuite un décodage réel FLAC séparé avec l'outil disponible documenté FLAC 1.5.0 : encoder le WAV maître, transporter, décoder, comparer le PCM canonique et le nombre de frames. Cela prouve ce décodeur et cette fixture ; ni MPD, ni gain aval, ni sortie USB. La preuve commune existante montre déjà bytes identiques et échéances différentes ; notre ajout nécessaire est corruption/troncature et conservation des arrivées brutes.

## Essai suivant sur deux machines et matériel

Installer des versions figées de MPD et de l'agent dans un environnement de test. Ne pas changer le NAS ni les réglages existants du DDC/DAC. Identifier le matériel, le noyau, les sorties et le chemin de volume avant tout démarrage audible ; relever descripteurs USB, `hw_params`, firmware, pinout I2S et branchement Aurender. Aucun modèle de DDC n'est supposé.

1. Sur l'ordinateur du salon, comparer le même morceau original local puis récupéré progressivement par MPD depuis Kuro. Même MPD, réglages, périphérique USB, DDC, câble, DAC et niveau analogique. Une fois la version locale disponible, le mode local n'exige plus le réseau de fichiers. Cela départage buffering/activité réseau avec un moteur fixe.
2. Relever plugins MPD compilés, protocole, requêtes HTTP/ranges, paramètres source, décodage et sortie ALSA. Vérifier gain, ReplayGain, normalisation, crossfade et conversion dans configuration et logs. Capturer le PCM à une sortie instrumentée séparée si possible ; ne pas appeler cette sortie la preuve des octets réellement reçus par USB.
3. Vérifier seek et deux pistes complémentaires dont la concaténation forme un signal continu. Mesurer missing/duplicate samples et silence sur capture PCM disponible, puis capture analogique lorsque disponible. Séparer transitions homogènes et changement de fréquence/reverrouillage ; aucun résultat ne garantit tous les formats.
4. Introduire une coupure du service, du contrôle, de l'origine, puis une perte de sortie. Observer arrêt borné par bail, absence de repli et aucun redémarrage au retour. Tuer aussi l'agent et vérifier arrêt de MPD. Vérifier fenêtre fermée versus Quitter et redémarrage arrêté avec même occurrence/position.
5. Comparer le cas progressif au local sur le même renderer, puis à la référence Aurender avec le même maître. Si l'entrée DDC change, le noter comme facteur non isolé. Écoute randomisée, niveau et alignement vérifiés, réponses brutes et critère d'analyse annoncé avant lecture des résultats.
6. Selon équipement disponible, capturer analogique du Terminator avec calibration et plancher du banc. Une différence répétable motive une enquête sur traitements, USB, alimentation ou horloges ; aucun hash ou résultat d'écoute seul ne désigne sa cause. Une mesure physique de jitter exige son point de mesure, appareil et stimulus propres.

Documents directeurs : [preuve commune](../../research/verification.md), [transports](../../research/transport-and-clock-domains.md), [moteurs et langages](../../research/engine-and-language.md). Les commandes d'inventaire exactes viennent de ces études ; les commandes de lecture attendent l'identification réelle du périphérique pour éviter d'utiliser une sortie par défaut.

## Conditions de révision et preuves restantes

Le progressive pull perd si sa marge de tampon ne tient pas le réseau accepté, si MPD transforme les formats retenus sans contrôle suffisant, ou si le mode local donne un avantage sonore reproductible dans la comparaison contrôlée. Dans les deux premiers cas, essayer d'abord préparation locale ou autre moteur avec les mêmes fixtures ; ne pas attribuer l'échec au langage sans test de service sous charge.

Le choix Go reste réversible. Mesurer débit, CPU, mémoire, délais de service et marge du renderer pendant lecture NAS/import/recherche concurrents. Comparer Rust seulement si ces résultats ou le coût de maintenance rendent Go inadapté. Le choix de licence dépend de l'artefact distribué, y compris MPD et codecs, pas de ce schéma.

Restent intégralement ouverts avant adoption : import/reprise et identité KB-022, recherche/échelle cible, formats et gapless matériels, absence/retrait NAS, paquet propre reproductible, restauration après interruption, reprise arrêtée sur deux machines, sécurité du contrôle et tests desktop accessibles. Ce prototype n'accepte ni U-M1 ni une stack, et ne conclut aucune supériorité sonore.
