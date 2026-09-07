# Relancer les preuves du prototype

Ce relevé décrit les contrôles exécutés le 2026-09-06 et les commandes pour les reproduire. Exécutez-les depuis la racine du dépôt. Les scripts écrivent tous les artefacts dans un nouveau dossier temporaire et ne modifient aucune installation système.

## Vérifier le laboratoire Go

Le module exige Go 1.25 ou une version plus récente. L'exécution consignée a utilisé Go 1.27.0.

```sh
go -C experiments/transport test ./...
go -C experiments/transport test -race ./...
go -C experiments/transport vet ./...

lab_root="$(mktemp -d /tmp/kuro-lab.XXXXXXXX)"
go -C experiments/transport run ./cmd/kuro-transport-lab run \
  --out "$lab_root/transport"
go -C experiments/transport run ./cmd/kuro-transport-lab verify \
  --out "$lab_root/transport"
```

`mktemp` crée le parent. Le chemin `transport` doit rester absent avant `run`, car la CLI refuse un dossier de sortie existant. `Verify` ouvre ensuite ce dossier en lecture, recalcule les empreintes et le modèle depuis les artefacts, puis sort avec un code non nul si une preuve manque ou diffère.

L'exécution finale a produit sept contrôles réussis.

| Cas | Fait vérifié |
| --- | --- |
| `clean` | Deux WAV admis, octets et PCM égaux aux fixtures. |
| `corrupt` | Payload modifié refusé sans publication dans `ready`. |
| `truncate` | Corps incomplet refusé et conservé dans `rejected`. |
| `resume` | Reprise `Range` avec offset, statut et ETag cohérents. |
| `changed-etag` | Changement d'ETag à la reprise refusé. |
| `stall` | Admission exacte, période progressive manquante et départ préparé après vérification. |
| `budget` | Fenêtre refusée avant admission sans éviction d'une réservation active. |

Le [rapport observé](evidence/go-report.json) avait le SHA-256 `4a19a5744270cca10a8fdbd0081b992074c4dbe69336a012e36b7fec402b40fa`. Le [manifeste](evidence/go-manifest.json) et la [trace du retard injecté](evidence/stall.json) sont aussi conservés. Les tests, la détection de courses de données et `go vet` ont réussi. Ces extraits ne remplacent pas le dossier brut complet. La commande ci-dessus en crée un nouveau avec les fixtures, les reçus HTTP, les traces de tous les cas et les corps reçus.

## Vérifier FLAC et MPD

Le contrôle audio exige Python 3, `flac`, les outils de compilation listés dans la [recette MPD](renderer-build.md) et un accès réseau pour télécharger les sources et les outils épinglés. Il construit MPD dans le même parent temporaire, puis utilise les artefacts Go déjà créés.

```sh
scripts/build_lab_mpd.sh "$lab_root/mpd"

python3 scripts/verify_audio_lab.py \
  --proof-dir "$lab_root/transport" \
  --mpd "$lab_root/mpd/mpd-0.24.15/build-lab/mpd" \
  --out "$lab_root/audio"
```

Les chemins `mpd` et `audio` sont absents avant ces commandes. La recette fixe MPD 0.24.15, le SHA-256 de sa source, Meson 1.12.0 et Ninja 1.13.2. Elle vérifie les sources avant réutilisation. Les bibliothèques de développement viennent toutefois de l'hôte et leurs versions ne sont pas verrouillées.

Le script audio exécute deux preuves distinctes. Le laboratoire Go fournit les WAV admis. Une origine HTTP Python séparée sert les FLAC encodés, capture les réponses, écrit les fichiers reçus, vérifie leur empreinte, puis les décode. MPD lit ensuite trois entrées vers une FIFO silencieuse : les WAV admis par Go, les FLAC reçus par Python et les FLAC servis directement par cette origine HTTP.

| Contrôle observé | Résultat |
| --- | --- |
| Deux transports FLAC par l'origine Python | Tailles et SHA-256 reçus égaux aux fichiers encodés. |
| Deux décodages FLAC | 24 000 frames et 96 000 octets de PCM par piste, égaux aux maîtres. |
| WAV admis par Go vers MPD FIFO | 48 000 frames, 192 000 octets, empreinte exacte. |
| FLAC reçus par Python vers MPD FIFO | 48 000 frames, 192 000 octets, empreinte exacte. |
| FLAC lus directement par HTTP vers MPD FIFO | 48 000 frames, 192 000 octets, empreinte exacte. |

Les trois captures MPD avaient le SHA-256 `24d01720643e20bd7f7e09cc52f5370a5aeb12c6536adba0198b1e7951144ff5`. Le [rapport audio observé](evidence/audio-report.json) avait le SHA-256 `65cf04550d0276f12c4b3ce1dc62c550a6af87f88c08c35210b29a008648ecc7`. Le [journal HTTP](evidence/flac-http.json) distingue les requêtes Python et MPD. Le dossier temporaire `audio` conserve en plus les configurations MPD, les versions et les captures. Les fichiers audio ne sont pas committés.

## Limites de la preuve

Tous les transferts utilisent `127.0.0.1` et des fixtures synthétiques. Le build MPD désactive les sorties physiques. Les captures FIFO prouvent l'ordre et l'égalité du PCM produit dans ces trois cas. Elles ne mesurent pas la tolérance de MPD aux retards réseau. Les essais sur deux machines, le NAS réel, une installation propre et la chaîne USB, DDC, I2S et DAC restent à réaliser. Le jitter physique et les différences audibles demandent des observations séparées sur cette chaîne.
