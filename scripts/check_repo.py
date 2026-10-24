#!/usr/bin/env python3
"""Mechanical checks for the tutorial repo. Run from the repo root.

Covers what a script can see. Whether a sentence reads well still needs
the checklist in .claude/skills/close-chapter/checks.md.
"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


chapters = sorted((root / "chapters").glob("[0-9][0-9]-*.md"))
readme = (root / "README.md").read_text()
plan = (root / "docs" / "plan.md").read_text()

for ch in chapters:
    if f"chapters/{ch.name}" not in readme:
        err(f"README does not link {ch.name}")
    text = ch.read_text()
    for target in re.findall(r"\]\((?!https?:|#)([^)#]+)", text):
        if not (ch.parent / target).resolve().exists():
            err(f"{ch.name}: broken link {target}")
    if "## Decisions in this chapter" not in text:
        err(f"{ch.name}: missing the section 'Decisions in this chapter'")
    # every row of a table has as many cells as its header
    cells = None
    for i, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            cells = None
            continue
        count = len(re.findall(r"(?<!\\)\|", re.sub(r"`[^`]*`", "", line)))
        if cells is None:
            cells = count
        elif count != cells:
            err(f"{ch.name}:{i}: table row has {count - 1} cells, the header {cells - 1}")
    n = ch.name[:2]
    if f"`chapter-{n}`" not in plan:
        err(f"docs/plan.md section 12 has no row for chapter-{n}")

latest = {}
for f in (root / "model" / "sketch").glob("*.json"):
    h = json.loads(f.read_text()).get("snapshot", {})
    latest[h.get("board")] = max(latest.get(h.get("board"), ""), h.get("chapter", ""))

for f in (root / "model" / "sketch").glob("*.json"):
    d = json.loads(f.read_text())
    superseded = d.get("snapshot", {}).get("chapter", "") < latest.get(d.get("snapshot", {}).get("board"), "")
    def flat(areas, loose):
        for a in areas:
            yield from flat(a.get("areas", []), a.get("nodes", []))
        yield from loose

    nodes = {n["id"]: n for n in flat(d.get("areas", []), d["nodes"])}
    snap = d.get("snapshot", {})
    for key in ("chapter", "board", "savedVersion", "note"):
        if key not in snap:
            err(f"{f.name}: snapshot header lacks '{key}'")
    events = [n["text"] for n in nodes.values() if n["kind"] == "event"]
    order = snap.get("eventOrder")
    if order is None:
        err(f"{f.name}: snapshot lacks 'eventOrder'")
    elif sorted(order) != sorted(events):
        err(f"{f.name}: eventOrder does not match the event cards")
    linked = set()
    for e in d["edges"]:
        for end in ("sourceId", "targetId"):
            if e[end] not in nodes:
                err(f"{f.name}: edge points to unknown card {e[end]}")
            linked.add(e[end])
    for n in nodes.values():
        if n["id"] not in linked:
            if n["kind"] == "event":
                if not superseded:
                    warn(f"{f.name}: event without any connection (who or what causes it?): {n['text']}")
            else:
                err(f"{f.name}: card without any connection: {n['text']}")
        if n["kind"] == "event" and not any(
            t.startswith("src:") for t in n.get("tags", [])
        ):
            err(f"{f.name}: event without src: tag: {n['text']}")
        if n["kind"] == "hotspot" and not any(
            t.startswith("hotspot:") for t in n.get("tags", [])
        ):
            err(f"{f.name}: hotspot without type tag: {n['text']}")
        if n["kind"] == "policy" and not any(
            t.startswith("rule:") for t in n.get("tags", [])
        ):
            err(f"{f.name}: policy card without rule: tag: {n['text']}")

clar_file = root / "requirements" / "clarifications.md"
clar = clar_file.read_text() if clar_file.exists() else ""
known = set(re.findall(r"^(?:### |\| )(C-\d+)", clar, re.M))
for cid in sorted(set(re.findall(r"^### (C-\d+)", clar, re.M))):
    section = clar.split(f"### {cid}", 1)[1].split("\n### ", 1)[0]
    if "**Status:** proposed" in section:
        warn(f"clarifications: {cid} is still only proposed (no decision yet)")
cited = set()
for f in [*chapters, *(root / "model" / "sketch").glob("*.json"), *(root / "model" / "esdm").rglob("*.yaml")]:
    cited |= set(re.findall(r"\bC-\d+\b", f.read_text()))
for f in (root / "model" / "sketch").glob("*.json"):
    for tag in re.findall(r'"(?:clar|parked):(C-\d+)"', f.read_text()):
        cited.add(tag)
for cid in sorted(cited - known):
    err(f"{cid} is cited but has no entry in requirements/clarifications.md")

adr_dir = root / "docs" / "adr"
if adr_dir.exists():
    adr_index = (adr_dir / "README.md").read_text()
    # sections every record has (MADR full template, fixed in ADR 1)
    adr_sections = (
        "## Context and Problem Statement",
        "## Decision Drivers",
        "## Considered Options",
        "## Decision Outcome",
        "### Consequences",
        "## Pros and Cons of the Options",
    )
    adr_keys = ("status", "date", "decision-makers", "consulted", "informed")
    for adr in sorted(adr_dir.glob("0*.md")):
        if adr.name not in adr_index:
            err(f"docs/adr/README.md does not list {adr.name}")
        text = adr.read_text()
        number = int(adr.name[:4])
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        meta = {}
        if not fm:
            err(f"{adr.name}: missing metadata block (status, date, decision-makers, consulted, informed)")
        else:
            for line in fm.group(1).splitlines():
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"')
            for key in adr_keys:
                if not meta.get(key):
                    err(f"{adr.name}: metadata '{key}' is missing or empty")
        body = text[fm.end():] if fm else text
        if not re.match(rf"\n# {number}\. \S", "\n" + body.lstrip("\n")):
            err(f"{adr.name}: title must be '# {number}. <decision>'")
        for section in adr_sections:
            if f"\n{section}\n" not in text:
                err(f"{adr.name}: missing section '{section}'")
        status = meta.get("status", "")
        if status not in ("proposed", "accepted", "rejected", "deprecated") and not status.startswith("superseded by ADR-"):
            err(f"{adr.name}: status '{status}' is not proposed, accepted, rejected, deprecated or superseded by ADR-N")
        row = re.search(rf"\]\({re.escape(adr.name)}\) \| .*? \| (\S[^|]*?) \|", adr_index)
        if row and row.group(1) != status:
            err(f"{adr.name}: status '{status}' differs from the index ('{row.group(1)}')")
        if "## Decision Outcome" in body and "## Pros and Cons" in body:
            outcome = body.split("## Decision Outcome", 1)[1].split("## Pros and Cons", 1)[0]
            said = re.findall(r"^(Recommended|Chosen) option:", outcome, re.M)
            wanted = {"proposed": "Recommended", "accepted": "Chosen"}.get(status)
            if wanted and said != [wanted]:
                err(f"{adr.name}: status '{status}' needs exactly one line starting '{wanted} option:' in the Decision Outcome, found {said}")
        if "## Considered Options" in body and "## Pros and Cons" in body:
            options = body.split("## Considered Options", 1)[1].split("\n## ", 1)[0]
            pros = body.split("## Pros and Cons of the Options", 1)[-1].split("\n## ", 1)[0]
            for opt in re.findall(r"^(?:\*|\d+\.) (.+)$", options, re.M):
                if f"\n### {opt}\n" not in "\n" + pros:
                    err(f"{adr.name}: considered option '{opt}' has no heading under 'Pros and Cons of the Options'")

# the context map must not contain a circle (downstream depends on upstream)
deps = {}
roles_up = ("upstream", "host", "publisher", "supplier")
roles_down = ("downstream", "consumer", "customer")
for f in (root / "model" / "esdm" / "integration").glob("*.yaml"):
    text = f.read_text()
    def end(roles):
        for r in roles:
            m = re.search(rf"^{r}:\n  domain: \S+\n  boundedContext: (\S+)", text, re.M)
            if m:
                return m.group(1)
    up, down = end(roles_up), end(roles_down)
    if up and down:
        deps.setdefault(down, set()).add(up)

def find_circle(node, path):
    if node in path:
        return path[path.index(node):] + [node]
    for nxt in sorted(deps.get(node, ())):
        found = find_circle(nxt, path + [node])
        if found:
            return found

for start in sorted(deps):
    circle = find_circle(start, [])
    if circle:
        warn("context map has a circle (downstream depends on upstream): " + " -> ".join(circle))
        break

for f in (root / "model" / "domain-stories").glob("*.yaml"):
    text = f.read_text()
    for obj in set(re.findall(r"workObject: (\S+)", text)):
        if re.search(r"\d", obj):
            err(f"{f.name}: digits in work object name '{obj}' (rules belong in findings)")

if warnings:
    print("\n".join(f"WARN {w}" for w in warnings))
if errors:
    print("\n".join(f"FAIL {e}" for e in errors))
    sys.exit(1)
print(f"OK: {len(chapters)} chapters checked")
