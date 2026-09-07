#!/usr/bin/env python3
"""Read-only checks for kuro's reconciled documentation set."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


COMMIT = "c478909"
ALLOWED_STEPS = {"U-M1", "U-M2", "U-M3", "U-M4", "backlog", "étude"}
DISPOSITION_VALUES = {"engage", "differe", "etude", "hors_portee", "partiel"}
REQUIRED_DISPOSITION = [
    "id_fonction", "disposition_courante", "etape", "source_decision",
    "reference_backlog", "portee_courante", "validation_courante",
]


class Checker:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.counts: dict[str, int] = {}

    def error(self, message: str) -> None:
        self.errors.append(message)

    def count(self, name: str, amount: int = 1) -> None:
        self.counts[name] = self.counts.get(name, 0) + amount

    def git(self, *args: str) -> bytes | None:
        result = subprocess.run(["git", *args], cwd=self.root, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode:
            self.error(f"git {' '.join(args)}: {result.stderr.decode(errors='replace').strip()}")
            return None
        return result.stdout

    def snapshot(self) -> None:
        raw = self.git("ls-tree", "-r", "--name-only", COMMIT)
        if raw is None:
            return
        expected = [p for p in raw.decode().splitlines() if p == "README.md" or p.startswith("docs/")]
        self.count("snapshot_files", len(expected))
        if len(expected) != 36:
            self.error(f"snapshot: {len(expected)} fichiers Git, 36 attendus")
        archive = self.root / "docs/archive/p1-p5"
        present: dict[str, bytes] = {}
        if archive.exists():
            for path in archive.rglob("*"):
                if path.is_file():
                    present[str(path.relative_to(archive))] = path.read_bytes()
        expected_set = set(expected)
        got_set = set(present)
        for missing in sorted(expected_set - got_set):
            self.error(f"archive: fichier manquant {missing}")
        for extra in sorted(got_set - expected_set):
            self.error(f"archive: fichier inattendu {extra}")
        for rel in sorted(expected_set & got_set):
            git_bytes = self.git("show", f"{COMMIT}:{rel}")
            if git_bytes is None:
                continue
            if present[rel] != git_bytes:
                self.error(f"archive: contenu différent de {rel}")
            else:
                self.count("archive_octets")
        manifest = self.root / "docs/archive/p1-p5.sha256"
        entries: dict[str, str] = {}
        if not manifest.is_file():
            self.error("archive: manifeste docs/archive/p1-p5.sha256 absent")
        else:
            for lineno, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = re.match(r"^([0-9a-fA-F]{64})\s+(?:\*?)(.+)$", line)
                if not match:
                    self.error(f"manifest: ligne {lineno} invalide")
                    continue
                rel = match.group(2).strip()
                if rel in entries:
                    self.error(f"manifest: chemin dupliqué {rel}")
                entries[rel] = match.group(1).lower()
            if set(entries) != expected_set:
                self.error("manifest: ensemble de chemins différent du snapshot")
            for rel, digest in entries.items():
                if rel in present and hashlib.sha256(present[rel]).hexdigest() != digest:
                    self.error(f"manifest: empreinte incorrecte {rel}")
        provenance = self.root / "docs/archive/p1-p5-source.md"
        if not provenance.is_file():
            self.error("archive: provenance docs/archive/p1-p5-source.md absente")
        else:
            text = provenance.read_text(encoding="utf-8")
            if COMMIT not in text:
                self.error(f"provenance: commit {COMMIT} absent")

    @staticmethod
    def mask_markdown(text: str) -> str:
        """Blank fenced blocks and remove inline delimiters, retaining their text."""
        text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1\s*$", lambda m: "\n" * m.group(0).count("\n"), text)
        return re.sub(r"(`+)(.+?)\1", lambda m: m.group(2), text)

    @staticmethod
    def mask_inline(text: str) -> str:
        return re.sub(r"(`+)(.+?)\1", lambda m: " " * len(m.group(0)), text)

    @staticmethod
    def slugify(heading: str) -> str:
        heading = re.sub(r"\s+#+\s*$", "", heading.strip()).lower()
        heading = "".join(ch for ch in heading if not unicodedata.category(ch).startswith("P") or unicodedata.category(ch) == "Pd")
        return re.sub(r"\s+", "-", heading).strip("-")

    def headings(self, path: Path) -> set[str]:
        text = self.mask_markdown(path.read_text(encoding="utf-8", errors="replace"))
        seen: dict[str, int] = {}
        slugs: set[str] = set()
        for line in text.splitlines():
            match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
            if not match:
                continue
            base = self.slugify(match.group(1))
            n = seen.get(base, 0)
            seen[base] = n + 1
            slugs.add(base if n == 0 else f"{base}-{n}")
        return slugs

    def links(self) -> None:
        files = [self.root / "README.md", self.root / "CONTEXT.md"]
        files += [p for p in sorted((self.root / "docs").rglob("*.md")) if not (self.root / "docs/archive") in p.parents]
        files += sorted((self.root / ".scratch").rglob("*.md")) if (self.root / ".scratch").exists() else []
        archive = self.root / "docs/archive/p1-p5"
        files += sorted(archive.rglob("*.md")) if archive.exists() else []
        for source in files:
            if not source.is_file():
                continue
            raw = source.read_text(encoding="utf-8", errors="replace")
            without_fences = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1\s*$", lambda m: "\n" * m.group(0).count("\n"), raw)
            masked = self.mask_inline(without_fences)
            for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", masked):
                target = match.group(1).strip().split()[0].strip("<>")
                if re.match(r"(?:[A-Za-z][A-Za-z0-9+.-]*:|//)", target):
                    continue
                target_path, _, fragment = target.partition("#")
                if archive.exists() and archive in source.parents:
                    # Resolve archived links against the original tree, then map the result
                    # back into the archive's mirrored tree.
                    virtual_source = self.root / source.relative_to(archive)
                    virtual_target = (virtual_source.parent / target_path).resolve() if target_path else virtual_source.resolve()
                    try:
                        resolved = archive / virtual_target.relative_to(self.root)
                    except ValueError:
                        resolved = virtual_target
                else:
                    resolved = (source.parent / target_path).resolve() if target_path else source.resolve()
                if not resolved.is_file():
                    self.error(f"lien: {source.relative_to(self.root)} -> {target}")
                    continue
                self.count("local_links")
                if fragment and fragment not in self.headings(resolved):
                    self.error(f"ancre: {source.relative_to(self.root)} -> {target}")

    def tsv_paths(self) -> None:
        files = [p for p in sorted(self.root.glob("docs/**/*.tsv")) if not (self.root / "docs/archive") in p.parents]
        archive = self.root / "docs/archive/p1-p5"
        files += sorted(archive.rglob("*.tsv")) if archive.exists() else []
        for path in files:
            try:
                rows = list(csv.reader(path.read_text(encoding="utf-8", errors="replace").splitlines(), delimiter="\t"))
            except OSError as exc:
                self.error(f"tsv: {path}: {exc}")
                continue
            width = len(rows[0]) if rows else 0
            decision_log = bool(rows) and rows[0] == ["ts", "phase", "decision", "why", "evidence", "result"]
            for lineno, row in enumerate(rows[1:], 2):
                if len(row) != width:
                    self.error(f"tsv: {path.relative_to(self.root)} ligne {lineno}: colonnes incohérentes")
                    continue
                cells = row[4].split("; ") if decision_log else row
                for cell in cells:
                    value = cell.strip().strip("`<>")
                    if not value or value.startswith(("http://", "https://", "mailto:")):
                        continue
                    if decision_log:
                        value = re.sub(r":\d+(?::\d+)?$", "", value)
                    if not re.search(r"\.(?:md|tsv|csv|json|yaml|yml)(?:#[^\s]+)?$", value, re.I):
                        continue
                    value_path = value.split("#", 1)[0]
                    if archive.exists() and archive in path.parents:
                        virtual_path = self.root / path.relative_to(archive)
                        virtual_target = (virtual_path.parent / value_path).resolve()
                        try:
                            candidate = archive / virtual_target.relative_to(self.root)
                        except ValueError:
                            candidate = virtual_target
                    else:
                        candidate = (path.parent / value_path).resolve()
                    if not candidate.is_file() and value_path.startswith(("docs/", ".scratch/", "README", "CONTEXT.md")):
                        base = archive if archive in path.parents else self.root
                        candidate = (base / value_path).resolve()
                    if not candidate.is_file():
                        self.error(f"tsv: {path.relative_to(self.root)} -> {value}")
                    else:
                        self.count("tsv_file_refs")

    def definitions(self) -> dict[str, set[str]]:
        issues = self.root / ".scratch/cadrage-kuro/issues"
        sources = {
            "KD": sorted(issues.glob("*.md")),
            "KB": [self.root / "docs/backlog.md"],
            "KV": [self.root / "docs/validation.md"],
        }
        definitions = {}
        for prefix, paths in sources.items():
            text = "\n".join(self.mask_markdown(path.read_text(encoding="utf-8"))
                             for path in paths if path.is_file())
            pattern = rf"^#+\s+({prefix}-\d{{3}})\b"
            if prefix == "KB":
                pattern = r"^\|\s*(KB-\d{3})\s*\|"
            definitions[prefix] = set(re.findall(pattern, text, re.M))
        return definitions

    def functions(self) -> None:
        current = self.root / "docs/disposition-fonctions.tsv"
        archive = self.root / "docs/archive/p1-p5/docs/inventaire-fonctions.tsv"
        if not current.is_file():
            self.error("fonctions: docs/disposition-fonctions.tsv absent")
            return
        if not archive.is_file():
            self.error("fonctions: inventaire archivé absent")
            return
        def read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
            with path.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream, delimiter="\t")
                rows = []
                for lineno, row in enumerate(reader, 2):
                    if None in row or any(value is None for value in row.values()):
                        self.error(f"tsv: {path.relative_to(self.root)} ligne {lineno}: colonnes incohérentes")
                        continue
                    rows.append(row)
                return reader.fieldnames or [], rows
        fields, rows = read(current)
        _, arows = read(archive)
        if fields != REQUIRED_DISPOSITION:
            self.error(f"fonctions: colonnes attendues {REQUIRED_DISPOSITION}, obtenues {fields}")
        ids = [r.get("id_fonction", "") for r in rows]
        aids = [r.get("id", "") for r in arows]
        if len(ids) != 195 or len(set(ids)) != len(ids):
            self.error(f"fonctions: {len(ids)} lignes courantes, IDs non uniques ou 195 attendus")
        if len(aids) != 195 or len(set(aids)) != len(aids):
            self.error(f"inventaire: {len(aids)} lignes, IDs non uniques ou 195 attendus")
        if set(ids) != set(aids):
            self.error("fonctions: ensemble d'IDs différent de l'inventaire archivé")
        definitions = self.definitions()
        kd_defs, kb_defs, kv_defs = (definitions[prefix] for prefix in ("KD", "KB", "KV"))
        for row in rows:
            function_id = row.get("id_fonction", "")
            if row.get("disposition_courante") not in DISPOSITION_VALUES:
                self.error(f"fonctions: disposition invalide pour {function_id}")
            if row.get("etape") not in ALLOWED_STEPS:
                self.error(f"fonctions: étape invalide pour {function_id}")
            source = row.get("source_decision", "")
            backlog_ref = row.get("reference_backlog", "")
            validation_ref = row.get("validation_courante", "")
            for ident in re.findall(r"\bKD-\d{3}\b", source):
                self.count("KD_refs")
                if ident not in kd_defs:
                    self.error(f"fonctions: {function_id}: décision absente {ident}")
            for ident in re.findall(r"\bKB-\d{3}\b", backlog_ref):
                self.count("KB_refs")
                if ident not in kb_defs:
                    self.error(f"fonctions: {function_id}: backlog absent {ident}")
            for ident in re.findall(r"\bKV-\d{3}\b", validation_ref):
                self.count("KV_refs")
                if ident not in kv_defs:
                    self.error(f"fonctions: {function_id}: validation absente {ident}")
            disposition = row.get("disposition_courante", "")
            if disposition in {"engage", "partiel"} and row.get("etape") == "U-M1" and not re.search(r"\bKV-\d{3}\b", validation_ref):
                self.error(f"fonctions: {function_id}: disposition engagée sans KV")
            if disposition in {"differe", "etude", "partiel"} and not re.search(r"\bKB-\d{3}\b", backlog_ref):
                self.error(f"fonctions: {function_id}: disposition différée/étude sans KB")
            if not row.get("portee_courante", "").strip():
                self.error(f"fonctions: {function_id}: portee_courante vide")
            if not source.strip() or not re.search(r"\bKD-\d{3}\b", source):
                self.error(f"fonctions: {function_id}: source_decision sans KD")

    def decisions_and_wayfinder(self) -> None:
        docs = [p for p in (self.root / "docs").rglob("*.md")
                if not (self.root / "docs/archive") in p.parents]
        docs += [self.root / "README.md", self.root / "CONTEXT.md"]
        issue_dir = self.root / ".scratch/cadrage-kuro/issues"
        issues = sorted(issue_dir.glob("*.md")) if issue_dir.exists() else []
        current_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in docs if p.is_file())
        for prefix, definitions in self.definitions().items():
            for ident in sorted(set(re.findall(rf"\b{prefix}-\d{{3}}\b", current_text))):
                if ident not in definitions:
                    self.error(f"référence: définition absente {ident}")
        map_path = self.root / ".scratch/cadrage-kuro/map.md"
        if not map_path.is_file():
            self.error("wayfinder: carte absente")
            return
        map_text = map_path.read_text(encoding="utf-8", errors="replace")
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", map_text):
            if not (map_path.parent / target).is_file():
                self.error(f"wayfinder: lien absent {target}")
        statuses: dict[str, str] = {}
        deps: dict[str, list[str]] = {}
        for path in issues:
            text = path.read_text(encoding="utf-8", errors="replace")
            ident = path.stem.split("-", 1)[0]
            status = re.search(r"^Status:\s*(\S+)", text, re.M)
            blocked = re.search(r"^Blocked by:\s*(.+)", text, re.M)
            statuses[ident] = status.group(1).lower() if status else ""
            dep = (blocked.group(1).strip() if blocked else "none")
            deps[ident] = [] if dep.lower() in {"none", ""} else re.findall(r"\d+", dep)
            if statuses[ident] != "resolved":
                self.error(f"wayfinder: ticket {path.name} status {statuses[ident] or 'absent'}")
        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(node: str) -> None:
            if node in visiting:
                self.error(f"wayfinder: cycle détecté autour de {node}")
                return
            if node in visited:
                return
            visiting.add(node)
            for dep in deps.get(node, []):
                if dep not in deps:
                    self.error(f"wayfinder: dépendance inconnue {dep} pour {node}")
                else:
                    visit(dep)
            visiting.remove(node)
            visited.add(node)
        for node in deps:
            visit(node)
        if re.search(r"second entretien.*(?:pas commencé|n'a pas commencé|not started)", map_text, re.I):
            self.error("wayfinder: note indiquant que le second entretien n'a pas commencé")

    def run(self) -> int:
        self.snapshot()
        self.links()
        self.tsv_paths()
        self.functions()
        self.decisions_and_wayfinder()
        print("verify_docs: " + ", ".join(f"{k}={v}" for k, v in sorted(self.counts.items())))
        if self.errors:
            print(f"verify_docs: {len(self.errors)} erreur(s)", file=sys.stderr)
            for error in self.errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        print("verify_docs: OK")
        return 0


if __name__ == "__main__":
    raise SystemExit(Checker(Path(__file__).resolve().parents[1]).run())
