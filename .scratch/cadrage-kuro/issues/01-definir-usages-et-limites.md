# Définir les usages et les limites avec le premier entretien

Type: grilling
Status: resolved
Assignee: orchestrateur
Blocked by: none

## Question

Quels usages, comportements, limites et critères de passage doivent former le cadrage courant de kuro avant un second entretien indépendant ?

## Answer

Cette réponse reconstitue après coup les 25 réponses recueillies par l'orchestrateur pendant un entretien délégué. Le ticket n'a donc pas été réclamé avant l'échange. Cette exception est déclarée ici au lieu d'inventer un historique de suivi.

### KD-001. Conserver les dix critères de M1

M1 conserve Linux sur Omarchy, les sources locales et NAS, 20 000 albums et environ 3 To, les vues et la recherche, les playlists et la file, la sortie locale, le gapless retenu, la persistance, une sauvegarde restaurable, les sources intactes et l'usage sans Internet.

### KD-002. Inclure les pochettes locales dans M1

M1 conserve les pochettes locales qui ne peuvent pas être reconstruites. Les caches de pochettes reconstructibles restent hors des données durables.

### KD-003. Distinguer la fenêtre, Quitter et la session

Fermer la fenêtre laisse le service actif. La commande explicite **Quitter** arrête kuro. Le service n'a pas à survivre à la fermeture de session pour M1.

### KD-004. Restaurer sans reprendre le son

Après un redémarrage, kuro restaure la file et la meilleure position enregistrée, mais reste arrêté. La commande **Lecture** reprend la piste restaurée. Le choix d'une autre piste commence cette piste.

### KD-005. Recevoir un montage NAS déjà disponible

Pour M1, kuro reçoit le chemin d'un montage NAS fourni par la session. kuro ne gère ni les identifiants, ni le protocole, ni le montage du NAS.

### KD-006. Sauvegarder les données durables sur demande

La sauvegarde manuelle exporte les sources configurées, les identités, le catalogue, les playlists, la file, la position, les préférences et les pochettes non reconstructibles. Elle exclut les médias, les index et caches reconstructibles, ainsi que les secrets. Un historique de sauvegardes n'est pas requis.

### KD-007. Ordonner la suite par usages

Après M1 viennent la redécouverte par favoris et filtres simples, puis l'organisation des éditions et coffrets. Le classique avancé, le DSP, le multiroom, les intégrations et les autres systèmes d'exploitation retournent au backlog avec une condition de réadmission.

### KD-008. Garder le mobile comme dernier horizon conditionnel

Le mobile peut commencer après l'acceptation de M1, la validation des parcours desktop retenus et de la restauration, puis 14 jours d'usage régulier journalisé. Ce passage exige zéro blocage, aucune perte de données et aucun incident critique non résolu. Sa portée reste à examiner au second entretien.

### KD-009. Définir l'usage hors Internet de M1

Après une installation déjà effectuée, le démarrage à froid, la relance et toutes les fonctions de M1 fonctionnent sans Internet pendant une durée indéfinie. Aucun compte ni validation cloud n'est requis. La lecture du NAS dépend seulement de sa joignabilité sur le réseau local.

### KD-010. Borner le passage d'une piste indisponible

Pendant une traversée de la file, kuro passe une piste indisponible une fois et affiche l'erreur. La fin de cette traversée arrête la lecture. Le retour du NAS ne déclenche aucune reprise automatique.

### KD-011. Arrêter après la perte de la sortie

La perte de la sortie audio arrête la lecture. kuro ne bascule pas automatiquement vers une autre sortie.

### KD-012. Reprendre depuis le meilleur point enregistré

La position durable est le meilleur point de reprise enregistré, sans promesse d'exactitude à l'échantillon. Une reprise explicite continue cette piste depuis ce point.

### KD-013. Préserver les sources distinctes et relocaliser explicitement

Deux sources ou copies distinctes restent distinctes. kuro ne les fusionne pas selon leur nom ou leurs tags seuls. Une relocalisation explicite de racine réconcilie une référence existante lorsque le chemin relatif correspond. kuro rend une ambiguïté visible au lieu de choisir seul.

### KD-014. Étudier le corpus de formats et le gapless

Le corpus candidat comprend FLAC, MP3, AAC, ALAC, WAV, AIFF, Vorbis et Opus en PCM stéréo. Une étude fixe la garantie exacte. Le gapless est exigé sur les enchaînements homogènes du corpus retenu. Les enchaînements hétérogènes sont qualifiés, sans garantie universelle.

### KD-015. Garder les budgets de recherche comme objectifs

La recherche visible sous 300 ms au 95e percentile et la première page sous une seconde restent des budgets de conception. Le projet doit chiffrer la mémoire et la durée d'import avant d'accepter la cible connue. Aucun de ces nombres n'est une mesure actuelle.

### KD-016. Rendre le scan pilotable

Le scan incrémental peut reprendre et être annulé. La lecture et la navigation restent disponibles pendant le scan. kuro affiche la progression et les erreurs, et propose un nouveau scan manuel. La surveillance automatique avancée reste au backlog. Une source NAS absente ne provoque jamais de suppression automatique.

### KD-017. Définir l'affichage minimal à partir des tags

Pour attribuer et afficher l'artiste d'un album, kuro préfère `albumartist`, puis `artist`, puis une valeur inconnue explicite. Ces tags ne définissent pas seuls l'identité d'un fichier. Les numéros de disque et de piste, avec le contexte du dossier et de la source, empêchent la fusion automatique des éditions et homonymes. kuro regroupe un album multidisque lorsque les tags et le contexte concordent, et montre les ambiguïtés.

### KD-018. Séparer file et playlists

La file est un instantané indépendant d'une playlist et accepte les doublons. **Lecture** remplace clairement la file sans imposer une fenêtre modale. **Jouer ensuite** et **Ajouter** conservent leurs sens propres. La fin de la file arrête la lecture et ne lance pas de radio.

### KD-019. Livrer le socle d'accessibilité dans M1

M1 couvre le clavier, un focus visible, les libellés accessibles, le zoom et le déplacement dans la piste. MPRIS est un confort indépendant prévu avec la redécouverte et les filtres simples.

### KD-020. Utiliser la sortie partagée sans hausse automatique

M1 utilise une sortie partagée avec le système. kuro mémorise le volume choisi, mais ne l'augmente jamais automatiquement. Le mode exclusif, le bit-perfect et le DSP restent au backlog.

### KD-021. Ne jamais modifier ou supprimer les médias

kuro lit les médias sans les modifier. Retirer une source du catalogue ne supprime aucun fichier. Les playlists gardent les références devenues indisponibles.

### KD-022. Limiter l'accès et expurger les diagnostics

M1 n'écoute pas sur le réseau local. Le contrôle local utilise une communication limitée à l'utilisateur de la session. Les journaux expurgent les données sensibles et l'utilisateur peut consulter un aperçu avant export.

### KD-023. Rendre le paquet Linux reproductible

L'installation et la désinstallation utilisent des versions figées et sont reproductibles dans un environnement propre. Une désinstallation normale conserve les données. Le service appartient à la session utilisateur. La mise à jour automatique et les autres systèmes d'exploitation restent au backlog.

### KD-024. Cibler un usage personnel local

M1 sert une personne sur son compte local. Il n'exige aucun compte kuro, aucune télémétrie obligatoire et aucun engagement de niveau de service.

### KD-025. Séparer le cadrage de l'adoption technique

Le cadrage documentaire ne réalise aucun code, média, test, installation ou fusion. Les études de licence, de stack, de formats, de matériel et de NAS bloquent l'adoption technique concernée, mais pas la clôture du cadrage.

## Evidence

Les sources suivantes ont été consultées le 6 septembre 2026. Elles donnent des points de comparaison. Elles ne prouvent aucun comportement de kuro et la recherche n'a exécuté ni Roon ni kuro.

- [Roon 2.0.28 build 1365](https://community.roonlabs.com/t/roon-2-0-28-is-live/263614) décrit en 2024 un retour de l'usage sans connexion constante. Cette note de version ne constitue pas un contrat exhaustif ni une garantie de durée.
- [Architecture de Roon](https://help.roonlabs.com/portal/en/kb/articles/architecture) distingue les responsabilités du serveur, du contrôle et de la sortie.
- [Sauvegardes Roon](https://help.roonlabs.com/portal/en/kb/articles/what-is-a-backup-in-roon) distingue la base et les réglages des fichiers musicaux.
- [Dossiers surveillés Roon](https://help.roonlabs.com/portal/en/kb/articles/faq-what-s-a-watched-folder) décrit des sources musicales laissées intactes.
- [Écoute hors ligne dans Roon ARC](https://help.roonlabs.com/portal/en/kb/articles/offline-listening-in-roon-arc) concerne des copies mobiles téléchargées. Ce parcours appartient à un projet distinct de M1.
- [Roon Optimized Core Kit](https://help.roonlabs.com/portal/en/kb/articles/roon-optimized-core-kit) cite des bibliothèques de plus de 12 000 albums pour son propre matériel. Cette indication ne définit aucune exigence matérielle de kuro.
