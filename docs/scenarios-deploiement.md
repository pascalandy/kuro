# Scénarios de déploiement

Ces scénarios appliquent les [termes du domaine](../CONTEXT.md) à trois destinations de lecture. Ils fixent les destinations admises, pas une architecture d'implémentation. KD-046.

Les chemins de contrôle et de média restent distincts sur le plan logique. Ils peuvent partager un hôte, une application ou un processus. Le chemin média peut transporter un fichier, un flux encodé ou du PCM selon la destination et le protocole.

## Scénario 1 : lecture sur l'ordinateur du Kuro Client

KuroKor et le Kuro Client vivent sur deux ordinateurs. L'ordinateur du Kuro Client fournit aussi la lecture locale. L'utilisateur écoute sur cet ordinateur.

```text
Chemin de contrôle
[ordinateur du Kuro Client] -- intentions --> [ordinateur de KuroKor]
[ordinateur du Kuro Client] <-- état ------- [ordinateur de KuroKor]

Chemin média
[NAS, médias maîtres] --> [KuroKor] --> [lecture sur l'ordinateur du Kuro Client]
                                              |
                                              v
                                      [sortie audio locale]
```

Ce scénario fixe l'hôte de lecture. Il n'impose ni une application ou un processus audio séparé du Kuro Client, ni du PCM sur le réseau. La technique retenue déterminera la représentation transportée ainsi que la répartition du décodage, des tampons et de la sortie.

## Scénario 2 : lecture locale sur l'hôte de KuroKor

KuroKor fournit la lecture sur l'ordinateur du salon relié à la chaîne existante. Un Kuro Client peut partager cet ordinateur ou fonctionner à distance.

```text
Chemin de contrôle
[Kuro Client local ou distant] -- intentions --> [KuroKor dans le salon]
[Kuro Client local ou distant] <-- état ------- [KuroKor dans le salon]

Chemin média
[NAS, médias maîtres] --> [KuroKor et lecture locale]
                                      |
                                      v
                              [USB -> DDC -> I2S -> DAC]
```

## Scénario 3 : point de lecture réseau distinct

KuroKor peut envoyer le média à un appareil supplémentaire dans le salon. Ce point de lecture peut être un streamer commercial ou un ordinateur peu puissant, par exemple de la famille Raspberry Pi.

```text
[NAS, médias maîtres] --> [KuroKor] --> [point de lecture réseau distinct]
                                               |
                                               v
                                         [chaîne audio]
```

UPnP est un candidat parmi d'autres. Aucun protocole, appareil, modèle ou achat n'est retenu. La compatibilité des streamers et la capacité d'un ordinateur peu puissant restent à mesurer. Kuro ne possède pas nécessairement les tampons internes d'un appareil tiers.

| Élément | Scénario 1 | Scénario 2 | Scénario 3 |
| --- | --- | --- | --- |
| KuroKor | Ordinateur distinct | Ordinateur du salon | Ordinateur qui alimente le réseau |
| Kuro Client | Contrôle et lecture sur son hôte | Local ou distant | Local ou distant |
| Point de lecture | Hôte du Kuro Client | Hôte de KuroKor | Appareil supplémentaire |
| Représentation transportée | À étudier | Chemin local | À étudier |

Ces scénarios décrivent une destination à la fois. Ils n'ajoutent ni lecture multiroom synchronisée, ni DSP, ni changement de la cible d'environ 20 000 albums et 3 To. Le NAS conserve les fichiers musicaux maîtres en lecture seule pour Kuro. L'état durable de Kuro reste une responsabilité distincte.
