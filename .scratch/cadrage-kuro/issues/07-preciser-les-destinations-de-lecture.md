# Préciser les destinations de lecture

Type: task
Status: resolved
Assignee: playback_destinations
Blocked by: 06

## Question

Quelles destinations KuroKor peut-il alimenter sans confondre le rôle de contrôle du Kuro Client avec l'hôte qui produit le son, ni imposer du PCM et des tampons possédés par Kuro à tous les appareils ?

## Comments

### 2026-09-07. Précisions directes

L'utilisateur confirme que l'ordinateur qui héberge un Kuro Client peut aussi produire le son envoyé depuis KuroKor. Dans le salon, KuroKor peut utiliser sa sortie locale existante ou envoyer le média par UPnP, ou par une autre technique à étudier, vers un streamer commercial ou un ordinateur peu puissant tel qu'un Raspberry Pi.

## Answer

### KD-046. Retenir trois destinations sans fixer leur réalisation

KuroKor coordonne la lecture vers trois destinations possibles. La sortie locale de l'hôte de KuroKor reste la cible existante. L'ordinateur qui héberge un Kuro Client peut aussi être le point de lecture, afin que l'utilisateur écoute sur cet ordinateur. Une option ultérieure peut utiliser un point de lecture réseau distinct, tel qu'un streamer commercial ou un ordinateur peu puissant.

Le Kuro Client reste le rôle logique de contrôle. Son hôte peut fournir une capacité de lecture, dans la même application ou le même processus si la conception retenue le permet. Les chemins de contrôle et de média restent distincts sur le plan logique. Cette distinction n'impose aucune séparation physique ou logicielle.

Le chemin média peut transporter un fichier, un flux encodé ou du PCM. Le protocole et la destination déterminent où se trouvent le décodage, les tampons et la sortie. Kuro possède les parties qu'il implémente et contrôle, mais ne possède pas nécessairement les tampons physiques d'un streamer tiers. Rust reste prioritaire à évaluer pour les parties audio possédées par Kuro, sans créer d'exigence pour le matériel ou le logiciel interne d'un appareil tiers.

UPnP reste un candidat, pas un choix ni une garantie de compatibilité universelle. La capacité d'un ordinateur peu puissant reste à mesurer. Aucun modèle ou achat n'est recommandé. Cette clarification ne change ni la portée multiroom, ni la synchronisation, ni le DSP, ni la cible d'environ 20 000 albums et 3 To. Le NAS conserve les fichiers musicaux maîtres en lecture seule pour Kuro. L'état durable de Kuro reste une responsabilité distincte.

KD-046 résout l'emplacement du point de lecture laissé ouvert par KD-044. Il précise aussi les formulations trop absolues sur le Kuro Client, le PCM et la possession des tampons dans KD-044 et KD-045. Le reste de leur historique demeure valide.

## Evidence

Ces choix viennent des réponses directes de l'utilisateur du 7 septembre 2026. Ils fixent les destinations admises et les séparations logiques. Ils ne choisissent aucun protocole, moteur, langage de production, modèle de streamer ou Raspberry Pi. Ils ne prouvent aucune compatibilité, capacité, qualité sonore ou synchronisation.
