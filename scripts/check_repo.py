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
