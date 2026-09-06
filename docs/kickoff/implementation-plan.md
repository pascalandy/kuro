# Construire la preuve de transport

Ce plan implémente le laboratoire défini dans [les contrats](contracts.md). Il ne construit ni bibliothèque, ni service de lecture, ni agent MPD. La [synthèse](synthesis.md) retient leurs responsabilités futures séparément.

## Contrat remis au développeur

Créer le module Go `kuro/transportlab` dans `experiments/transport`. Utiliser seulement la bibliothèque standard. Un développeur possède le runtime et la CLI. Un autre peut écrire des tests d'intégration dans `integration_test.go`, package `lab_test`, après lecture du contrat ci-dessous. Aucun de ces tests ne modifie le runtime.

```text
experiments/transport/
  go.mod
  lab.go                         # fixtures, HTTP réel, réception disque, Run, Verify
  model.go                       # Analyze pur et structures de trace
  cmd/kuro-transport-lab/main.go  # analyse des arguments, sortie JSON, codes de sortie
  lab_test.go                    # tests ciblés du développeur
  integration_test.go            # tests indépendants, si second développeur
```

Viser moins de 700 lignes de runtime hors tests. Une déviation nécessaire est consignée avant d'ajouter un framework ou une seconde couche. Les fonctions publiques suivantes sont le contrat stable pour les tests. Les détails privés des fichiers JSON peuvent évoluer pendant l'implémentation, puis leur schéma livré est versionné.

```go
package lab

type Config struct { OutDir string }
type Check struct {
    Name string `json:"name"`
    Passed bool `json:"passed"`
    Detail string `json:"detail"`
}
type Report struct {
    Version int `json:"version"`
    Checks []Check `json:"checks"`
}
type Arrival struct {
    AtNS int64 `json:"at_ns"`
    Bytes int64 `json:"bytes"` // Total cumulé du corps reçu, en-tête WAV inclus.
}
type Trace struct {
    Arrivals []Arrival `json:"arrivals"`
    ExpectedBytes int64 `json:"expected_bytes"`
    HeaderBytes int64 `json:"header_bytes"`
    VerifiedAtNS int64 `json:"verified_at_ns"` // -1 si aucun fichier admis.
}
type Model struct {
    SampleRate int64 `json:"sample_rate"`
    FrameBytes int64 `json:"frame_bytes"`
    PeriodFrames int64 `json:"period_frames"`
    PrebufferFrames int64 `json:"prebuffer_frames"`
}
type Comparison struct {
    ProgressiveStartNS int64 `json:"progressive_start_ns"`
    ProgressiveMissingPeriods int64 `json:"progressive_missing_periods"`
    StagedStartNS int64 `json:"staged_start_ns"`
}
func Run(ctx context.Context, config Config) (Report, error)
func Verify(outDir string) (Report, error)
func Analyze(trace Trace, model Model) (Comparison, error)
```

`Run` crée un dossier de sortie absent et refuse tout chemin déjà existant. Il exécute toute la suite, écrit les résultats bruts puis appelle `Verify`. `Verify` relit les fichiers, recalcule empreintes et modèle, et vérifie les oracles attendus. Il ne fait confiance ni à `report.json` ni aux anciens booléens de réussite. Il ne modifie aucun artefact. Une preuve manquante ou un contrôle faux produit une erreur non nulle. `Analyze` valide les paramètres et les temps monotones à sa frontière puis calcule sans réseau ni attente.

## Cas et sorties exigés

Générer deux WAV PCM stéréo 48 kHz, entiers signés 16 bits little-endian, canaux entrelacés gauche puis droite. Utiliser une formule entière documentée indexée par frame et canal. Les deux pistes se suivent dans le même signal. Conserver PCM maître et fichier WAV séparément. La durée peut rester courte, mais doit permettre le trou de livraison du cas `stall`.

L'origine expose uniquement les IDs de ces fixtures sur un listener `127.0.0.1` à port attribué par le système. Aucun chemin fourni par le client, aucune écoute LAN et aucun accès au NAS. Le serveur ouvre les fixtures en lecture seule. Les fautes modifient une réponse, jamais le fichier maître. Utiliser un ETag fort dérivé des octets, des plages vérifiées et une réponse HTTP visible dans les traces.

Le récepteur écrit chaque transfert dans un fichier temporaire propre à ce transfert. Il vérifie taille, ETag et SHA-256 attendus avant de publier le fichier prêt par renommage atomique sur le même filesystem. Un partiel ou un fichier rejeté reste identifié comme tel et n'apparaît jamais dans le dossier prêt. Conserver les corps rejetés pour l'audit dans un dossier distinct.

| Cas | Oracle obligatoire |
| --- | --- |
| `clean` | Deux objets admis, octets et PCM identiques, sources inchangées. |
| `corrupt` | Inverser un bit du payload transmis; aucune admission, faute d'intégrité observée. |
| `truncate` | Fermer le corps avant la longueur annoncée; aucune admission, longueur reçue insuffisante. |
| `resume` | Première réponse interrompue, reprise Range au bon offset avec même ETag; objet final identique et statut/plage contrôlés. |
| `changed-etag` | Changer le validateur de la réponse de reprise; refuser toute concaténation/admission comme objet initial. |
| `stall` | Transfert finalement exact, pause injectée après prébuffer; la trace montre au moins une période progressive manquante et un départ staged retardé jusqu'à vérification. |
| `budget` | Budget inférieur à courant plus suivant; refus explicite avant admission de la fenêtre, aucun objet réservé évincé. |

Le budget du laboratoire peut se limiter à deux réservations et compter l'espace cumulé des fichiers prêts et partiels. Ne pas implémenter un cache produit avec éviction générale. Une reprise ne réserve pas deux fois le même transfert. Garder les numéros de réponse, offsets, Content-Range et ETag observés dans les artefacts.

`manifest.json` fixe version, formule, formats, longueurs et empreintes attendues. Chaque cas conserve corps reçu, trace d'arrivées, reçus HTTP et constat d'admission. `report.json` récapitule les contrôles. `Verify` exige les cas, fixtures et fichiers bruts annoncés. Il compare sources avant et après et recalcule l'empreinte du PCM reçu pour les cas admis.

## Règles du modèle

Le temps enregistré est relatif au début du transfert. Les octets sont cumulatifs. Les frames disponibles valent la partie entière des octets reçus après l'en-tête divisée par `FrameBytes`. Une période ne consomme jamais un demi-échantillon. La première échéance de consommation suit le début d'une période.

Le mode progressif démarre quand le prébuffer est disponible. Une fois ce départ fixé, une arrivée tardive ne déplace pas les échéances suivantes. Compter chaque période dont les frames requises ne sont pas encore arrivées. Le mode staged démarre au premier tick de période qui suit ou égale la vérification complète. Sans admission, son départ vaut `-1`. Un prébuffer jamais atteint donne aussi un départ progressif `-1`.

Les temps système du transfert peuvent varier entre exécutions. Le recalcul sur une même trace doit être identique. Les tests unitaires utilisent des traces déterministes pour clean, pause, en-tête fragmenté et paramètres invalides. Le résultat parle de périodes manquantes dans ce modèle, jamais de jitter DAC ou de comportement MPD.

## Commandes exactes

Exécuter depuis `experiments/transport` après implémentation :

```sh
go test ./...
go test -race ./...
go run ./cmd/kuro-transport-lab run --out /tmp/kuro-transport-proof-001
go run ./cmd/kuro-transport-lab verify --out /tmp/kuro-transport-proof-001
```

La CLI imprime le rapport JSON sur stdout, les erreurs sur stderr et sort avec un code non nul si un oracle échoue. Un rejet injecté attendu fait réussir son cas. Les arguments inconnus, un `--out` absent et un répertoire déjà existant pour `run` échouent. `verify` exige un dossier existant et ne l'écrase pas. Ne pas ajouter d'option d'écrasement.

Les tests indépendants appellent `Run`, vérifient les sept noms de cas et tous les booléens, puis appellent `Verify`. Ils retirent ou corrompent une copie d'un artefact brut et exigent que `Verify` échoue. Ils contrôlent aussi le refus d'écrasement et les résultats exacts de `Analyze` sur leurs propres traces.

## Vérifications séparées

Le décodage réel FLAC utilise un outil installé et identifié. Encoder le PCM maître, transporter le fichier encodé, décoder puis comparer au PCM canonique. Conserver commandes, versions et résultat séparés du rapport Go.

Une capture MPD silencieuse vers FIFO reste une preuve distincte. Le build disponible pendant la conception est MPD 0.24.15 avec FLAC, WAV et FIFO, sans ALSA. Le script relançable doit recevoir son chemin en argument et conserver configuration et version. Il ne prouve ni USB, ni DDC, ni DAC. Le script MPD et sa recette de build appartiennent au lot de recherche, pas au runtime Go.

Après les contrôles, le parent met à jour [la synthèse](synthesis.md) avec les commandes réellement exécutées et leurs résultats. Aucun test du laboratoire ne clôt un KV produit.
