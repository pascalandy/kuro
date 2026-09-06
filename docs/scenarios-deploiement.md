# Scénarios de déploiement

Ces scénarios appliquent les [termes du domaine](../CONTEXT.md) à deux répartitions physiques. Ils fixent une direction de cadrage, pas une architecture d'implémentation.

La clarification actuelle remplace l'ancienne contrainte de deux ordinateurs. Les documents de l'arena conservent cette contrainte comme contexte historique, mais elle ne fixe plus le déploiement de kuro.

## Scénario 1 : KuroKor et Kuro Client sur deux ordinateurs

KuroKor et le Kuro Client vivent sur deux ordinateurs distincts. Le NAS reste un troisième appareil séparé et la source musicale maîtresse.

```text
Chemin de contrôle
[ordinateur du Kuro Client] -- intentions --> [ordinateur de KuroKor]
[ordinateur du Kuro Client] <-- état ------- [ordinateur de KuroKor]

Chemin média
[NAS, médias maîtres] --> [moteur audio de kuro] --> [point de lecture] --> [chaîne audio]
                              emplacement physique à fixer
```

Ce compte d'appareils ne répond pas à la question audio. L'emplacement physique du moteur audio et du point de lecture reste à fixer. Le PCM ne passe pas par le Kuro Client, et ce scénario ne suppose aucun ordinateur supplémentaire.

## Scénario 2 : première cible dans le salon

La première cible place KuroKor sur l'ordinateur du salon avec le moteur audio et le point de lecture local. Le Kuro Client peut partager cet ordinateur ou s'exécuter sur un appareil distant.

```text
Chemin de contrôle
[Kuro Client local ou distant] -- intentions --> [KuroKor dans le salon]
[Kuro Client local ou distant] <-- état ------- [KuroKor dans le salon]

Chemin média
[NAS, médias maîtres] --> [KuroKor + moteur audio + point de lecture]
                                      |
                                      v
                              [USB -> DDC -> I2S -> DAC]
```

| Élément | Scénario 1 | Scénario 2 |
|---|---|---|
| KuroKor | Ordinateur distinct du Kuro Client | Ordinateur du salon |
| Kuro Client | Ordinateur de contrôle séparé | Local ou distant |
| NAS | Appareil séparé, source musicale maîtresse | Appareil séparé, source musicale maîtresse |
| Moteur audio | Affectation physique ouverte | Avec KuroKor dans le salon |
| Point de lecture | Emplacement physique ouvert | Sortie locale de l'ordinateur du salon |

Dans les deux scénarios, le Kuro Client reste limité au contrôle et peut occuper un hôte aux ressources modestes. KuroKor vise l'hôte le plus capable du déploiement. Cette répartition permet d'étudier plus tard un traitement DSP dans KuroKor sans l'adopter dans le cadrage courant.

Un point de lecture réseau UPnP pourra être étudié plus tard. Il restera distinct du Kuro Client et n'entraînera pas, à lui seul, une fonction multiroom.
