# Passation P4 au coordinateur

P4 est validée par le coordinateur après revue intégrale des livrables et exécution indépendante du contrôle documentaire. Il a autorisé le commit local de finalisation, sans push. L’auteur P4 conserve les écritures jusqu’à ce commit, puis les cesse. Le coordinateur attribue ensuite les écritures au prochain auteur de phase, sans devenir lui-même rédacteur des livrables.

## Travail terminé

Six plans répartissent les responsabilités, collaborateurs, dépendances et preuves. Sept milestones indépendantes détaillent 28 phases produit futures, avec parcours, entrée, sortie, zones de fichiers indicatives et vérifications par niveau. Les fichiers du modèle P3 restent des propositions. Aucune structure applicative n’a été créée.

La couverture conserve les 195 identifiants, milestones et dispositions de P2. Chaque fonction a un plan responsable, une phase et un scénario. Les 50 scénarios reprennent chacun leurs cas `validation_future` spécifiques, sans remplacer ces cas par une formule générique. Les conditions fournisseurs et propositions ne deviennent pas obligatoires.

M1 commence par une petite tranche réellement écoutable, puis exige la taille cible et le NAS avant livraison. Le nombre de pistes reste inconnu. La stratégie distingue capture logicielle et physique, gapless à format constant et transitions, padding, crash entre commande et accusé, source absente et suppression, restauration après déplacement et intégrité des originaux. Les budgets P3 restent proposés et aucune baseline n’existe.

Technical writing et Unslop ont guidé la rédaction. Les adaptations Poteto du [suivi](../checklist.md) s’appliquent. Un générateur temporaire de documents hors dépôt a servi à répartir les cas canoniques, puis les fichiers réels ont été relus et contrôlés avec la commande ci-dessous. Le générateur n’est ni un fichier produit ni un livrable requis. Le contrôle rejouable inclus ici constitue la preuve documentaire conservée.

## Fichiers remis

| Ensemble | Contenu |
| --- | --- |
| [Roadmap](../roadmap.md) | Navigation des six plans et sept milestones, graphe et table des dépendances |
| [Bibliothèque](../plans/bibliotheque-et-metadonnees.md), [Audio](../plans/moteur-audio.md), [Client](../plans/client-ordinateur.md) | Responsabilités et étapes des usages locaux puis avancés |
| [Réseau](../plans/reseau-et-zones.md), [Intégrations](../plans/integrations-et-decouverte.md), [Exploitation](../plans/installation-et-exploitation.md) | Distribution, fournisseurs, persistance et acceptation |
| [M1](../milestones/m01-mvp-local.md), [M2](../milestones/m02-bibliotheque-avancee.md), [M3](../milestones/m03-audio-audiophile.md), [M4](../milestones/m04-reseau-domestique.md), [M5](../milestones/m05-decouverte-et-integrations.md), [M6](../milestones/m06-desktop-et-distribution.md), [M7](../milestones/m07-mobile.md) | 28 phases ordonnées avec dépendances explicites et résultats non cochés |
| [Validation](../validation.md) | Corpus, mesures et 50 scénarios produit futurs |
| [Couverture](../couverture.tsv) | 195 correspondances uniques et dispositions conservées |
| [README](../../README.md), [Checklist](../checklist.md), [Journal](../decisions.tsv) | Accès et suivi P4, cinq lignes de journal ajoutées sans réécriture |
| [Cette passation](p4-multiplan.md) | Commande de contrôle, limites et transfert d’écriture |

## Vérification documentaire reproductible

Exécuter depuis la racine du dépôt. Python et sa bibliothèque standard suffisent. La commande reprend la vérification P3, qui reprend P2, sur les fichiers actuels. Elle contrôle aussi les cas spécifiques et le graphe des phases. Le résultat compte des documents et références, aucun test de logiciel.

```bash
python - <<'PY'
import csv
import re
from pathlib import Path
from collections import Counter

root = Path.cwd()
source = (root / 'docs/passations/p3-architecture.md').read_text()
command = re.search(r"```bash\npython - <<'PY'\n(.*?)\nPY\n", source, re.S).group(1)
exec(compile(command, 'verification-p3', 'exec'))

def table(name):
    with (root / 'docs' / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

inventory = {r['id']: r for r in table('inventaire-fonctions.tsv')}
coverage = table('couverture.tsv')
assert list(coverage[0]) == ['id_fonction', 'plan', 'milestone',
                             'phase', 'scenario', 'disposition']
assert len(coverage) == 195
assert len({r['id_fonction'] for r in coverage}) == 195
assert {r['id_fonction'] for r in coverage} == set(inventory)
with (root / 'docs/couverture.tsv').open() as f:
    for row in csv.reader(f, delimiter='\t'):
        assert len(row) == 6 and all(row)
        assert not any(v.lstrip().startswith(('=', '+', '-', '@')) for v in row)
        assert not any('\n' in v or '\r' in v or '\t' in v for v in row)

plans = list((root / 'docs/plans').glob('*.md'))
milestones = list((root / 'docs/milestones').glob('*.md'))
assert len(plans) == 6 and len(milestones) == 7
validation = (root / 'docs/validation.md').read_text()
scenario_parts = re.split(r'^## (V-\d{3})\n', validation, flags=re.M)
scenarios = dict(zip(scenario_parts[1::2], scenario_parts[2::2]))
assert list(scenarios) == [f'V-{i:03}' for i in range(1, 51)]
phases = {}
edges = {}
for path in milestones:
    text = path.read_text()
    assert '- [x]' not in text.lower()
    parts = re.split(r'^## (M\d-P\d{2})\n', text, flags=re.M)
    assert 2 <= len(parts[1::2]) <= 6
    for id, block in zip(parts[1::2], parts[2::2]):
        assert id not in phases
        phases[id] = path.relative_to(root / 'docs').as_posix() + '#' + id.lower()
        dependency = re.search(r'^Dépendances : (.+)$', block, re.M).group(1)
        edges[id] = re.findall(r'\[(M\d-P\d{2})\]', dependency)
        assert all(k in block for k in ['| Unité |', '| Intégration |',
                                       '| Parcours réel |', '| Performance pertinente |'])
        assert re.search(r'\[V-\d{3}\]', block), id
assert len(phases) == 28

visited, active = set(), set()
def visit(id):
    assert id in phases, id
    assert id not in active, ('cycle', id)
    if id in visited:
        return
    active.add(id)
    for dep in edges[id]:
        visit(dep)
    active.remove(id)
    visited.add(id)
for id in phases:
    visit(id)
roadmap = (root / 'docs/roadmap.md').read_text()
for id, deps in edges.items():
    line = next(line for line in roadmap.splitlines() if line.startswith('| [' + id + ']'))
    assert re.findall(r'\[(M\d-P\d{2})\]', line)[1:] == deps, id

cases = []
for row in coverage:
    original = inventory[row['id_fonction']]
    assert row['milestone'] == original['milestone']
    assert row['disposition'] == original['disposition']
    assert (root / 'docs' / row['plan']) in plans
    phase_id = row['phase'].split('#')[1].upper()
    assert row['phase'] == phases[phase_id]
    assert phase_id.startswith(row['milestone'] + '-')
    scenario_id = row['scenario'].split('#')[1].upper()
    assert row['scenario'] == 'validation.md#' + scenario_id.lower()
    block = scenarios[scenario_id]
    expected_link = "[" + phase_id + "]" + "(" + row["phase"] + ")"
    assert expected_link in block
    expected = f'| {row["id_fonction"]} | {original["validation_future"]} | {original["disposition"]} |'
    assert expected in block, row['id_fonction']
for block in scenarios.values():
    cases += re.findall(r'^\| (F\d{2}-\d{3}) \|', block, re.M)
assert Counter(cases) == Counter(inventory.keys())
for path in root.rglob('*.md'):
    if path.name == 'p4-multiplan.md':
        continue
    for id in re.findall(r'\bV-\d{3}\b', path.read_text()):
        assert id in scenarios, (path, id)
    for id in re.findall(r'\bM\d-P\d{2}\b', path.read_text()):
        assert id in phases, (path, id)
print(f'{len(plans)} plans; {len(milestones)} milestones; {len(phases)} phases sans cycle; '
      f'{len(scenarios)} scénarios; {len(coverage)}/{len(inventory)} fonctions couvertes')
print('Milestones et dispositions inchangées; 195 cas spécifiques conservés; 0 erreur')
PY
git diff --check
git diff --exit-code a0429a4 -- docs/programme.md docs/produit-et-mvp.md docs/inventaire-fonctions.tsv docs/inventaire-roon.md docs/architecture.md docs/faisabilite.md docs/sources.md docs/sources-techniques.md
```

## Résultat et limites

Le contrôle intégral exécuté sur les fichiers réels a produit :

```text
195 fonctions; 84 sources externes; 15 familles; 29 Markdown; 628 liens locaux; 24 décisions; 0 erreurs
30 sources TECH; 9 contrats; 8 études futures; références valides
6 plans; 7 milestones; 28 phases sans cycle; 50 scénarios; 195/195 fonctions couvertes
Milestones et dispositions inchangées; 195 cas spécifiques conservés; 0 erreur
```

`git diff --check` est propre. Le diff des huit documents et registres P1–P3 cités dans la commande contre `a0429a4` est vide. Le statut Git montre trois fichiers suivis modifiés et les nouveaux livrables P4. Une nouvelle ligne du journal ou un nouveau lien peut modifier les comptes documentaires. La commande régénère ces comptes.

La revue progressive du coordinateur a demandé un lien précis vers la campagne de performance et des listes complètes de plans collaborateurs. Ces deux corrections sont intégrées. Elles ne changent aucun critère ni aucune disposition. Le coordinateur a ensuite confirmé le passage P4.

Aucun test produit, import, benchmark, capture audio, restauration ou installation n’a été exécuté. Les 20 000 albums et environ 3 To restent une cible confirmée, sans consultation des médias privés. Aucun contenu fournisseur ni secret n’est ajouté au dépôt. Licence, stack, formats, matériel, état C-06 et budgets attendent leurs décisions d’adoption futures.

## Suite attendue

Le coordinateur a autorisé le commit `docs(kuro): define domain plans and milestone validation`, sans push. Après le commit et la vérification du statut propre, l’auteur P4 cesse ses écritures. Le coordinateur transmet la responsabilité d’écriture au prochain auteur. P5 doit relire les liens usages, exigences, contrats, phases et validations, examiner les contradictions et produire les décisions ouvertes consolidées. P4 ne remplace pas cette revue indépendante. L’autorisation documentaire s’arrête avant tout développement.

## Revue manager et finalisation locale

Le coordinateur a lu les six plans, les sept milestones, la roadmap, la couverture et les 50 scénarios. Il a exécuté indépendamment la commande intégrale de cette passation. Son résultat confirme 29 Markdown, 628 liens locaux, 24 décisions, 195 fonctions, 84 sources externes Roon, 30 sources TECH, neuf contrats et huit études futures, sans erreur. Le contrôle P4 confirme six plans, sept milestones, 28 phases sans cycle, 50 scénarios et 195 cas spécifiques conservés. Les documents et registres P1–P3 contrôlés sont inchangés contre `a0429a4`.

Les deux retouches éditoriales demandées, lien vers la campagne de performance et collaborateurs des milestones, étaient intégrées avant cette revue finale. Le passage P4 vers P5 est accepté. Une ligne ajoutée au journal consigne la validation et porte le total à 25 décisions. Le contrôle final de l’auteur a confirmé les mêmes résultats après cette mise à jour, avec 25 décisions et toujours 628 liens locaux, sans erreur. `git diff --check` est propre et le diff des huit fichiers P1–P3 contrôlés contre `a0429a4` est vide. Aucun push ni développement n’est autorisé par cette finalisation locale.
