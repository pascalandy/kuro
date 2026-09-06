# Vérifier la qualité sonore du trajet Kuro

Statut : recherche primaire et plan de vérification datés du 2026-09-06. Ce rapport est une entrée de synthèse, pas une décision d'architecture ni une validation du trajet Kuro.

## Conclusion de travail

La chaîne à comparer est maintenant concrète.

`NAS -> serveur Kuro -> ordinateur de salon Linux -> USB -> DDC -> I2S sur HDMI -> DAC Terminator -> chaîne analogique`

La référence est un Aurender avec musique locale, piloté par Conductor 5, puis le même DDC, le même DAC et la même chaîne analogique.
L'utilisateur a nommé le fabricant du DDC "Dynafripp", mais ce nom et le fabricant restent à confirmer.
Les révisions exactes de l'Aurender, du DDC et du Terminator restent inconnues.
L'interface Aurender vers DDC reste aussi à confirmer.

Le témoignage d'une différence entre streamers est une observation à tester, pas une erreur à corriger par raisonnement.
Il ne détermine pas seul la cause, et aucune norme consultée ne permet de classer les protocoles par qualité sonore sans mesurer les appareils.
Conductor 5 appartient au plan de commande de la référence.
Le test doit consigner ses réglages, mais ne doit pas le traiter comme un transport audio sans preuve du modèle exact.

## Ce que les contrats Kuro prouvent aujourd'hui

- `KD-014` et `KD-039` bornent U-M1 à du PCM stéréo, à une sortie partagée et à l'absence de DSP, DSD, multicanal et mode exclusif.
- `KD-020` impose le volume système courant et interdit une hausse automatique.
- `KV-009` demande une mesure gapless et un contrôle du volume système.
- Aucun de ces éléments ne prouve l'intégrité du flux, l'absence de conversion, l'absence d'underrun, le comportement de l'horloge USB, la sortie analogique du DAC ou l'équivalence perceptive.
- `KB-003`, `KB-011`, `KB-012` et `KB-014` restent les études pertinentes. Le nouveau trajet réseau ne doit pas être déclaré validé par `KV-009`.

## Hiérarchie de preuve

Chaque étage doit produire son propre fait observable. Un étage qui passe ne fait pas passer les étages suivants.

| Étage | Fait à capturer | Passe | Échec | Ce que le résultat ne dit pas |
| --- | --- | --- | --- | --- |
| 1. Fichier source | Taille et SHA-256 du fichier lu sur le NAS | Les octets lus égalent le fichier de référence | Taille ou empreinte diffère, ou lecture incomplète | Rien sur le décodage, la lecture en temps réel ou le son |
| 2. Sortie du serveur | Empreinte du fichier ou des blocs PCM réellement envoyés, avec format et ordre | La sortie égale l'objet attendu pour le mode choisi | Octets, ordre, longueur ou format diffèrent | Rien sur ce que le renderer reçoit |
| 3. PCM décodé | PCM entier signé, nombre de canaux, fréquence, profondeur et nombre d'échantillons | L'empreinte du PCM canonique égale celle d'un décodeur de référence | Une valeur ou un paramètre diffère | Rien sur le DSP ultérieur, l'horloge ou l'analogique |
| 4. Chemin de signal | Format négocié à chaque frontière, gain, volume, mixage, conversion de fréquence et DSP | Aucun traitement non prévu, ou chaque traitement accepté correspond à la capture | Conversion ou gain inexpliqué, clipping, canal inversé ou DSP actif | Rien sur les échéances de livraison ou la qualité du DAC |
| 5. Temps réseau et tampon | Horodatage des blocs, pertes, reprises, niveau de tampon et underruns | Aucun underrun pendant le corpus et le profil réseau acceptés | Tampon vide, bloc tardif, dropout ou arrêt | Une arrivée irrégulière ne prouve pas du jitter à l'horloge du DAC |
| 6. Renderer et USB | Périphérique exact, descripteurs, format matériel, compteurs XRUN et rôle d'horloge | Le DDC reçoit le format attendu sans XRUN dans le cas testé | Mauvais format, resampling, perte du périphérique ou XRUN | Les descripteurs USB ne mesurent ni le bruit électrique ni le jitter réel du DDC |
| 7. DDC, I2S et DAC | Pinout et mode I2S, clocks, état du DAC et capture analogique calibrée | Le canal, la polarité, le niveau et les mesures acceptées passent | Mauvais canal, polarité, niveau, artefact, dérive ou sortie analogique différente | Une mesure isolée ne fixe pas un seuil d'audibilité universel |
| 8. Écoute | Essais randomisés, conditions, réponses brutes et analyse annoncée avant le test | Le critère d'écoute convenu passe | Le critère convenu échoue | Un résultat ne s'étend pas à d'autres auditeurs, morceaux, firmwares ou appareils |

[TCP selon la RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html) retransmet les segments perdus et livre un flux ordonné, mais son checksum n'est pas une preuve cryptographique de bout en bout.
L'empreinte applicative reste donc une mesure utile du cas testé.
[RTP selon la RFC 3550](https://www.rfc-editor.org/rfc/rfc3550.html) fournit des numéros de séquence et des horodatages, mais ne garantit ni livraison dans les délais ni qualité de service.
L'intégrité et le temps de livraison restent deux mesures différentes.

[La spécification FLAC](https://www.rfc-editor.org/rfc/rfc9639.html) définit la compression sans perte comme une décompression qui rend exactement les données d'origine.
Cette propriété du format ne prouve pas que le lecteur, le mixeur ou la sortie matérielle conserve ensuite ce PCM.
[PipeWire](https://docs.pipewire.org/1.4/page_man_pipewire_1.html) documente que des flux actifs peuvent être rééchantillonnés pour suivre le taux du graphe.
[`pw-top`](https://docs.pipewire.org/1.4/page_man_pw-top_1.html) expose le format négocié et compte les XRUN, ce qui donne des faits à conserver sur un renderer Linux.

[USB Audio 2.0](https://usb.org/sites/default/files/Audio2_with_Errata_and_ECN_through_Apr_2_2025.pdf) distingue les domaines d'horloge.
Un endpoint isochrone asynchrone suit une horloge externe au domaine USB ou une horloge interne libre.
Le standard prévoit un endpoint de feedback pour certaines sources adaptatives et certains puits asynchrones.
Il faut donc lire les descripteurs du DDC exact avant d'attribuer l'horloge au serveur, au renderer ou au DDC.

[DENAFRIPS indique](https://www.denafrips.com/support/1000) que son I2S sur HDMI n'a pas de pinout industriel unique.
Le fabricant demande de faire correspondre le mode de la source et celui du DAC.
Il revendique aussi un tampon FIFO adaptatif et un reclocking dans ses DDC et DAC, avec une latence variable.
Ces trois points sont des données de configuration du fabricant, pas des mesures de l'exemplaire de l'utilisateur.

## Expérience synthétique exécutée

Le script [`preliminary/transport_probe.py`](preliminary/transport_probe.py) génère deux secondes de PCM stéréo 48 kHz sur 16 bits.
Il encode le signal en FLAC 1.5.0, transfère les octets sur TCP via `127.0.0.1`, décode le FLAC reçu, puis compare les empreintes.
Il transfère aussi le PCM sous deux profils d'arrivée.
Le second profil impose une pause de 200 ms et alimente un modèle de consommateur avec périodes de 10 ms et préchargement de 40 ms.

Commande relançable :

```sh
python3 docs/kickoff/research/preliminary/transport_probe.py \
  | tee /tmp/kuro-preliminary-result.json
```

Le [résultat brut conservé](preliminary/transport-probe-result.json) a été observé avec Python 3.14.7 :

- SHA-256 du FLAC source et reçu : `2bf4a8e1027599d4693b1a690c1ee41d853880f81ea04b75b5911342839014f9`, passe.
- SHA-256 du PCM source et décodé : `5dd711a61f59c5e3d4eda0bdcaa30b77746d47397f37a6e694830df550211873`, passe.
- Profil fluide : octets identiques et zéro période d'underrun modélisée.
- Profil avec pause : octets identiques et 23 périodes d'underrun modélisées.
- L'artefact brut conservé a le SHA-256 `45f1ca208006f7aa94ee39108a841785f35c39ffc169ac88f786f6e6335c016b`.

Cette expérience préliminaire montre seulement que des octets identiques peuvent arriver avec un comportement temporel différent.
Elle n'a ouvert aucune sortie audio.
Elle ne prouve rien sur le NAS, le serveur Kuro futur, l'ordinateur de salon, le DDC, I2S, le DAC, l'analogique ou l'audibilité.
Le prototype retenu sera créé séparément après la synthèse. Il devra ajouter un transfert corrompu, un transfert tronqué et la trace brute des arrivées. Ces contrôles vérifieront les échecs et permettront de recalculer le modèle d'underrun.

## Matrice matérielle après identification des appareils

Utiliser le même fichier maître pour chaque cellule et consigner son empreinte.
Garder fixes le DDC, le mode I2S, le câble I2S, le DAC, son filtre, sa phase, son entrée, son volume, la chaîne analogique et la position d'écoute.
Si l'Aurender et le renderer Kuro n'utilisent pas la même entrée du DDC, la comparaison inclut ce changement et ne peut pas l'attribuer au streamer seul.

| Cas | Source et lecture | Question isolée |
| --- | --- | --- |
| A | Fichier local Aurender, Conductor 5, sortie numérique à confirmer | Référence observée |
| B | Même fichier local sur l'ordinateur de salon, renderer Kuro, USB vers DDC | Renderer, pile Linux et USB face à la référence |
| C | Même fichier local au serveur Kuro, réseau vers le renderer, USB vers DDC | Ajout du serveur et du transport réseau |
| D | Même fichier sur le NAS, serveur Kuro, réseau vers le renderer, USB vers DDC | Ajout de la lecture NAS |
| E | Cas D avec délai, débit limité et interruption bornés | Marge du tampon et comportement d'échec |

Pour A à D, effectuer au moins les contrôles suivants :

1. Capturer les réglages, firmwares, branchements, températures stabilisées et identifiants matériels.
2. Capturer les octets et le PCM aux frontières disponibles de B à D.
3. Capturer le graphe PipeWire ou ALSA, le format matériel, les horloges déclarées et les compteurs XRUN.
4. Capturer la sortie analogique du DAC avec le même analyseur, la même entrée, le même gain et la même bande de mesure.
5. Mesurer le niveau, la réponse en fréquence, le bruit, la distorsion, les raies parasites, la diaphonie et la réponse à un signal de test de jitter adapté.
6. Conserver les signaux bruts, les métadonnées de l'analyseur, son étalonnage et son plancher propre.
7. Répéter les captures dans un ordre alterné. Une différence doit suivre le cas et survivre à une reconnexion ou permutation prévue.
8. Après la mesure, mener une comparaison aveugle randomisée avec commutation temporellement alignée et niveau analogique vérifié.
9. Conserver l'ordre secret, les réponses essai par essai, les répétitions et la méthode statistique décidée avant de lire les résultats.

Si le PCM diffère, chercher d'abord le décodage, le gain, le DSP et la conversion de fréquence.
Si le PCM est identique mais que l'analogique diffère de façon répétable, examiner le renderer, l'USB, le DDC, les clocks, l'état du DAC et le montage de mesure.
Si l'analogique mesuré ne diffère pas au-dessus de l'incertitude du banc mais que l'écoute reste discriminante, le banc ou une variable contrôlée peut manquer le phénomène.
Ce cas ne justifie ni de rejeter l'écoute ni de nommer une cause sans nouvelle expérience.
Une absence de discrimination ne prouve pas l'identité universelle des chaînes.

## Dossier de preuve brute proposé

Chaque exécution reçoit un identifiant et conserve les données avant toute synthèse.

- `manifest.json` contient appareils, révisions, firmwares, branchements, réglages, fichier maître, ordre des cas et horodatages.
- `source.sha256`, `server-output.sha256` et `renderer-input.sha256` couvrent les frontières numériques disponibles.
- `decoded-pcm.json` contient l'empreinte, le format et le nombre d'échantillons. `transport.ndjson` contient les arrivées, le tampon et les erreurs.
- `usb-descriptors.txt`, `audio-graph.json`, `hw-params.txt` et `xrun.ndjson` conservent l'état du renderer sans le résumer.
- `analog-captures/` contient les captures, la calibration, le plancher du banc et les paramètres d'analyse.
- `listening-responses.csv` contient une ligne par essai. La randomisation et l'analyse annoncée sont scellées avant l'écoute, puis publiées avec le résultat.

## Entrées nécessaires avant le test matériel

- Modèle, révision, firmware et type de stockage de l'Aurender.
- Version exacte de Conductor 5 et réglages de lecture ou de sortie.
- Liaison Aurender vers DDC, modèle et firmware du DDC, puis descripteurs USB si applicables.
- Modèle et révision exacts du Terminator, firmware, filtre, phase, pinout I2S et usage éventuel de clocks externes.
- Modèle de l'ordinateur de salon, noyau, versions ALSA et PipeWire, interface réseau et sortie USB.
- NAS, montage, protocole, réseau physique, fichier maître et cas musicaux où la différence est déjà reconnue.
- Chaîne analogique, moyen de commutation, analyseur ou ADC de mesure et possibilité de masquer l'identité des sources.

Un renderer ouvert sur l'ordinateur de salon est compatible avec cette méthode s'il expose les empreintes, le PCM, le format négocié, le tampon et les XRUN.
La réutilisation de Conductor pour le piloter ne doit pas être supposée.
[La documentation Aurender](https://ask.aurender.com/hc/en-us/articles/33194272805399-Use-Aurender-as-a-Network-Renderer-Player) décrit Conductor comme l'application qui sélectionne la musique et configure les sorties Aurender.

## Sources primaires consultées

- IETF, TCP, RFC 9293 : https://www.rfc-editor.org/rfc/rfc9293.html
- IETF, RTP, RFC 3550 : https://www.rfc-editor.org/rfc/rfc3550.html
- IETF, FLAC, RFC 9639 : https://www.rfc-editor.org/rfc/rfc9639.html
- PipeWire, `pipewire` et `pw-top` : https://docs.pipewire.org/1.4/page_man_pipewire_1.html et https://docs.pipewire.org/1.4/page_man_pw-top_1.html
- Linux kernel, ALSA PCM et XRUN : https://docs.kernel.org/sound/designs/tracepoints.html
- USB-IF, USB Audio Device Class 2.0, avril 2025 : https://usb.org/sites/default/files/Audio2_with_Errata_and_ECN_through_Apr_2_2025.pdf
- AES, Benjamin et Gannon, effet théorique et audible du jitter, papier 4826 : https://aes.org/publications/elibrary-page/?id=8354
- ITU-R BS.1116-3, évaluations subjectives de faibles dégradations : https://www.itu.int/rec/R-REC-BS.1116-3-201502-I/en
- Audio Precision, six mesures audio de base : https://www.ap.com/fileadmin-ap/technical-library/TN-104.pdf
- DENAFRIPS, I2S, FIFO et reclocking : https://www.denafrips.com/support/1000 et https://www.denafrips.com/ddc
- Aurender, Conductor et renderer réseau : https://ask.aurender.com/hc/en-us/articles/33194272805399-Use-Aurender-as-a-Network-Renderer-Player
