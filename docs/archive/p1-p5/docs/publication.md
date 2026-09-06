# Publication du dossier kuro

Le dossier préparatoire est publié dans le [dépôt public pascalandy/kuro](https://github.com/pascalandy/kuro). La [PR #1](https://github.com/pascalandy/kuro/pull/1) est ouverte et non draft. Elle propose `docs/plan-kuro` vers `main`. Aucune fusion n'a été effectuée.

## Références publiées

La branche par défaut est `main`. Elle contient le commit initial vide `fcdae687ae5e9bd0cfe49c1e3b4e1d90bc213a33`. La première version publiée du dossier est le commit P5 `cf6155fb62b4bcec968f6dc0b85dfad3c98850d9`. Git et GitHub ont renvoyé ce même SHA pour la branche documentaire et la PR après leur création.

Le reçu ajoute un commit à cette première version. Son propre SHA n'est pas inscrit dans son contenu. La commande ci-dessous compare le HEAD final avec les références distantes et la PR.

## Opérations effectuées

L'agent de publication a rejoué le contrôle P5 complet avant toute mutation distante. Le dépôt n'existait pas. Il l'a créé public avec une description de dossier préparatoire, puis a configuré `origin`.

Le premier push a échoué faute de helper HTTPS. L'agent a utilisé le helper `gh auth git-credential` pour chaque commande de push, sans modifier la configuration globale. GitHub a ensuite refusé le push avec GH007, car les commits portaient une adresse privée. Aucun commit n'avait encore été publié.

Le coordinateur a autorisé la reconstruction des six commits non publiés avec l'adresse noreply du compte GitHub confirmé. Les noms, dates, messages et contenus hors références SHA sont conservés. Le remappage des références dans les documents est la seule exception à leur préservation. Les références originales sont sauvegardées localement sous `refs/backup/pre-publication/`. Elles ne sont pas poussées. La configuration Git locale utilise désormais la même identité noreply. Aucune protection GitHub n'a été désactivée.

L'agent a vérifié le diff, limité aux références SHA, puis rejoué P5 sans erreur. Il a poussé `main` d'abord, vérifié qu'elle était la branche par défaut, puis poussé `docs/plan-kuro`. Il a ouvert une seule PR, sans mode draft. Origin CLI étant absent, les opérations GitHub utilisent `gh`. Aucun push forcé n'a été utilisé.

## Correspondance des commits

Les anciens SHAs désignent l'historique local avant publication. Ils ne sont pas des liens publics.

| Étape | SHA local antérieur | SHA publié |
| --- | --- | --- |
| Initial | `ebb7db9d5cfad86e621f637f6232aaec5a5081cd` | `fcdae687ae5e9bd0cfe49c1e3b4e1d90bc213a33` |
| P1 | `4164495f0feb8c9bbf8b930128ad878b3ef718ee` | `045a07e88339fd23c68bf5cc2e0d1c0e67feef2a` |
| P2 | `cb65c04127fd36d94cffbd07629bf314e8d8f3b9` | `734ed697a94f9172d831903c65571e6238602a14` |
| P3 | `647ecb9bd14f46359eda4e2d984bd5f0a09e90bd` | `a0429a44d113fd1bd5f7345d82e5a4b12869f5a8` |
| P4 | `493843acfc9d90b48d61d42cc7841c7a63f3fc8b` | `00bd920a90b04b760c76b92b9f08fc4617dc5f62` |
| P5 | `304a72c2d8f893ee7090aca9bada33427721c159` | `cf6155fb62b4bcec968f6dc0b85dfad3c98850d9` |

## Fichiers modifiés pour la publication

Le remappage mécanique touche `docs/passations/p3-architecture.md`, `docs/passations/p4-multiplan.md`, `docs/passations/p5-revue.md` et `docs/revue-finale.md`. Aucun critère, fonction, disposition, contrat, plan ou scénario n'a changé.

Le commit de reçu ajoute ce document, relie la PR depuis le [README](../README.md), met à jour la [checklist](checklist.md) et ajoute les opérations au [journal](decisions.tsv). Les lignes antérieures du journal sont conservées.

## Contrôles et limites

Avant publication, P5 confirme 195 fonctions, 84 sources Roon, 30 sources TECH, six plans, sept milestones, 28 phases sans cycle, 50 scénarios, 20 chaînes et neuf décisions ouvertes. Le résultat initial est de 32 Markdown, 755 liens locaux, 30 décisions de journal et 35 fichiers UTF-8, sans erreur. Après ajout du reçu et des cinq lignes de journal, le contrôle P5 confirme 33 Markdown, 765 liens locaux, 35 décisions et 36 fichiers documentaires, sans erreur. Ces comptes se régénèrent par le contrôle P5. `git diff --check` passe.

La recherche ciblée de secrets et détails privés n'a rien détecté dans les documents. Elle ne constitue pas une garantie universelle. Aucun logiciel, média, prototype, installation, import, scan NAS, test audio, benchmark ou résultat CI n'est livré. La licence reste ouverte, sans fichier LICENSE. Les composants proposés restent des candidats non adoptés.

## Vérifier le HEAD remis

Depuis la racine du dépôt, exécuter la première commande Bash de la [passation P5](passations/p5-revue.md), puis cette comparaison. Git et gh doivent disposer de leur accès existant à GitHub.

```bash
python - <<'PYVERIFY'
import json
import subprocess

def read(*args):
    return subprocess.check_output(args, text=True).strip()

head = read('git', 'rev-parse', 'HEAD')
refs = dict(line.split()[::-1] for line in read(
    'git', 'ls-remote', 'origin', 'refs/heads/main',
    'refs/heads/docs/plan-kuro').splitlines())
repo = json.loads(read('gh', 'repo', 'view', 'pascalandy/kuro',
    '--json', 'url,visibility,defaultBranchRef'))
pr = json.loads(read('gh', 'pr', 'view', '1', '--repo', 'pascalandy/kuro',
    '--json', 'url,state,isDraft,baseRefName,headRefName,headRefOid'))
assert refs['refs/heads/main'] == 'fcdae687ae5e9bd0cfe49c1e3b4e1d90bc213a33'
assert refs['refs/heads/docs/plan-kuro'] == head == pr['headRefOid']
assert repo['visibility'] == 'PUBLIC' and repo['defaultBranchRef']['name'] == 'main'
assert pr['state'] == 'OPEN' and pr['isDraft'] is False
assert pr['baseRefName'] == 'main' and pr['headRefName'] == 'docs/plan-kuro'
assert not read('git', 'status', '--porcelain')
subprocess.run(['git', 'diff', '--check'], check=True)
print(repo['url'], pr['url'], head, 'références concordantes; arbre propre')
PYVERIFY
```

## Passation et arrêt

L'agent de publication remet les références au coordinateur pour sa vérification indépendante. Ce reçu ne prétend pas que cette dernière revue distante est déjà effectuée. Le dossier est prêt pour le retour final au demandeur, sans prétendre que ce message a déjà été envoyé.

La suite consiste à examiner les [neuf décisions ouvertes](decisions-ouvertes.md). M1 conserve Linux Omarchy, les sources locales et NAS, environ 20 000 albums et 3 To. Toutes les milestones produit restent futures. Le travail s'arrête avant tout développement et aucune fusion n'est demandée.
