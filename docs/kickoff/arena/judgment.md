# Jugement indépendant de l'arena SQ

Lecture intégrale des neuf fichiers candidats, de la rubrique, du cadrage additionnel, du grounding et des trois études communes. Aucun candidat abandonné, aucune préférence du parent reçue, aucun fichier candidat modifié. Les notes évaluent les contrats et preuves proposées, pas un logiciel livré ni une qualité sonore mesurée.

| Critère, sur 2 | A, HTTP progressif et file serveur | B, PCM poussé et file serveur | C, fichiers préparés et file renderer |
| --- | ---: | ---: | ---: |
| Responsabilités audio et horloges | 2 | 2 | 2 |
| Fidélité au nouveau besoin | 2 | 2 | 2 |
| Faisabilité protocolaire et matériel | 2 | 2 | 2 |
| Preuve synthétique falsifiable | 2 | 2 | 2 |
| Architecture et langage proportionnés | 2 | 1 | 1 |
| Décision SQ honnête et test suivant | 2 | 2 | 2 |
| Total sur 12 | **12** | **11** | **11** |

Aucune élimination. Les trois propositions traitent deux ordinateurs distincts, USB vers le DDC inconnu puis I2S vers le Terminator, et prennent l'Aurender comme référence à remplacer. Elles distinguent les octets, le PCM, les échéances modélisées et la chaîne physique. Aucun langage ni protocole ne reçoit de supériorité sonore déduite. B traite la révision de l'ancien contrat surtout dans son plan de preuve; la synthèse devra rendre la contradiction avec U-M1 local aussi explicite que A et C.

## Base recommandée

Retenir **A pour les propriétaires, les opérations et le premier service**. Le serveur garde catalogue, playlists, occurrences et meilleure position durable. Le renderer possède l'exécution temporaire, les tampons et l'adaptation MPD. La projection courant/suivant demande une réconciliation, mais elle ne transforme pas la sauvegarde en transaction entre deux magasins durables. Voir [A, contrats](a/contracts.md), lignes 18 à 25 et 68 à 80.

Go est justifié ici par le travail réellement proposé, HTTP avec plages, fichiers, contrôle de processus, traces et vérification sans FFI. Rust reste crédible, mais les types opaques et l'absence de GC ne suffisent pas à imposer son coût au service. Le prototype ne choisit pas définitivement le langage produit.

C est deuxième. Sa préparation locale est le meilleur complément expérimental, mais sa file durable au salon oblige une barrière de snapshot, un journal d'activation, des epochs et un protocole de récupération entre machines. C reconnaît ce coût dans [ses contrats](c/contracts.md), ligne 81. La sauvegarde complète est déjà un contrat conservé; elle ne doit pas devenir une priorité à confirmer pour justifier une file serveur. Le staging ne nécessite pas cette ownership distante.

B est troisième. Son protocole avec crédits, offsets, générations, purge et deux canaux est cohérent. Cependant, la centralisation des décodeurs ne répond encore ni à une contrainte matérielle observée ni à un traitement demandé. Une meilleure instrumentation du PCM est un bénéfice de laboratoire, insuffisant pour adopter ce transport comme cœur du produit. GStreamer reste un moteur de repli utile sans exiger le protocole de B.

## Greffes exactes

1. **De C, préparation locale vérifiée, derrière le renderer de A.** Ajouter une politique de laboratoire qui écrit `.part`, vérifie longueur et SHA-256, publie atomiquement et réserve courant/suivant. Garder son budget comptant partiels et fichiers réservés, son refus explicite de capacité insuffisante et son arrêt si la prochaine piste manque. Le cache reste reconstructible et la file demeure au serveur. Source : C, contrats, lignes 71 à 75.
2. **De C, comparer les deux politiques depuis la même preuve brute.** Dans un seul outil, conserver un transfert HTTP réel et sa trace; recalculer attente initiale, admission locale et manque de données progressif séparément. Ajouter corruption, troncature, reprise avec changement d'objet et piste suivante tardive. Ces scénarios testent le transport et les politiques, sans adopter deux implémentations de production. Source : C, proof-plan, cas obligatoires et modèle; conserver aussi les oracles de A.
3. **De C, séparer perte média et perte du contrôle.** Un fichier préparé peut rester disponible si seul le service fichier tombe. La perte du contrôle arrête après le bail; le retour ne reprend rien. Un essai sans aucun trafic réseau doit être explicitement un mode de laboratoire, car le heartbeat produit reste actif. Source : C, contrats, ligne 77, et fin du proof-plan.
4. **De B, rendre testable l'incertitude de position et le rejet des générations périmées.** Le serveur ne fait pas avancer son occurrence sur un simple reçu réseau. Conserver les scénarios seek, messages anciens et restart silencieux dans la preuve future de l'agent MPD. Ne pas importer le framing PCM ni les crédits. Source : B, contrats, « États et effets audio ».
5. **De C, protéger l'expérience de remplacement d'album.** Une préparation en cours peut coexister avec la file jouée; le geste Lecture autorise son démarrage après préparation. Garder ces états distincts dans l'interface plutôt que demander au client un arrêt préalable. Source : C, début des contrats; corrige la restriction de A, contrats, ligne 66.

Le staging doit être un comparateur de première classe dès l'étude, particulièrement pertinent face à l'Aurender à stockage local. Ces notes ne permettent pas encore de le déclarer meilleur choix sonore, ni d'imposer le téléchargement complet comme politique produit.

## Rejets et contrôle des red flags

Rejeter la file durable renderer de C et son protocole de restauration distribué. Rejeter le transport PCM spécifique de B pour cette première architecture. Ne pas imposer dès maintenant les deux caches de C : son spool immuable résout la cohérence des reprises, mais son besoin et son coût doivent être établis pour le NAS réel. Un digest de transfert ne remplace jamais l'identité catalogue.

Les trois interfaces cachent des opérations substantielles; aucune ne présente une chaîne de simples wrappers comme une architecture profonde. A doit toutefois exposer une opération de lecture d'album qui compose préparation et départ, comme il le prévoit, et ne pas reporter cette coordination sur chaque client. La frontière `Renderer` est justifiée par la projection MPD et le bail, pas par une simple délégation homonyme. C concentre bien le savoir local, mais laisse fuir son partage durable jusque dans sauvegarde et restauration. B garde son framing privé, tout en obligeant deux exécutables à partager de nombreuses règles audio nouvelles. Ces deux derniers points motivent leur note d'architecture.

## Risques non résolus et prochain test

Le transfert loopback ne prouve ni le réseau des deux machines ni MPD. MPD peut convertir malgré une configuration native; ses logs et `hw_params` détectent un écart sans garantir un refus avant le premier échantillon. Les arrêts sur crash de l'agent, le bail, les restrictions SSH, les événements de transition et la reprise arrêtée restent à exécuter. A doit aussi compléter Pause et son état avant de prétendre couvrir tout le contrat produit conservé.

Le test discriminant suivant utilise le même ordinateur du salon et le même MPD : fichier local de référence, fichier préparé par Kuro, puis lecture HTTP progressive. Fixer fichier, format, gain, USB, DDC, câble I2S et réglages DAC; relever traitements, transitions et XRUN, puis captures analogiques et écoute contrôlée selon l'équipement disponible. Comparer ensuite l'Aurender, en consignant toute différence d'entrée DDC. Cela distingue un problème de livraison d'un problème de moteur ou de chaîne physique. Modèles exacts, modes USB/I2S, formats acceptés, délai de départ et budget cache restent inconnus. Aucun classement de jitter physique ou de son n'est acquis.
