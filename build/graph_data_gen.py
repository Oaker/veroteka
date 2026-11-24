# -*- coding: utf-8 -*-
import os, io, re, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

nodes = []
title_map = {}
for dirpath, dirs, files in os.walk(str(ROOT / "content" / "ru")):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, str(ROOT / "content" / "ru")).replace(os.sep, "/")[:-3]
        c = io.open(p, encoding="utf-8").read()
        m = re.match(r"---\s*\n([\s\S]*?)\n---\s*\n", c)
        if not m:
            continue
        fm = m.group(1)
        t = re.search(r"title: (.+)", fm)
        a = re.search(r"axis:\s*(\S+)", fm)
        y = re.search(r"year: (.+)", fm)
        title = t.group(1).strip() if t else fn[:-3]
        axis = a.group(1) if a else ""
        year = y.group(1).strip() if y else ""
        nodes.append({"id": rel, "title": title, "section": rel.split("/")[0],
                      "axis": axis, "year": year, "url": rel + ".html"})
        title_map[title.lower()] = rel

links = set()
for dirpath, dirs, files in os.walk(str(ROOT / "content" / "ru")):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, str(ROOT / "content" / "ru")).replace(os.sep, "/")[:-3]
        c = io.open(p, encoding="utf-8").read()
        m = re.search(r"## [^\n]*также[\s\S]*?\n([\s\S]*?)(?:\n## |\Z)", c)
        if not m:
            continue
        for line in m.group(1).splitlines():
            for part in line.split("\u00b7"):
                t = part.strip(" \u00b7-\u2014")
                if not t or len(t) < 2:
                    continue
                target = title_map.get(t.lower())
                if target and target != rel:
                    k = tuple(sorted([rel, target]))
                    links.add((k[0], k[1]))

GENEALOGY = [
    ("02_world/abrahamic/judaism/judaism", "02_world/abrahamic/christianity/christianity", "выделилась"),
    ("02_world/abrahamic/judaism/judaism", "02_world/abrahamic/islam/islam", "влияние"),
    ("02_world/abrahamic/christianity/christianity", "02_world/abrahamic/islam/islam", "влияние"),
    ("02_world/abrahamic/christianity/christianity", "02_world/abrahamic/christianity/protestantism/protestantism", "выделилась"),
    ("02_world/abrahamic/christianity/christianity", "02_world/abrahamic/christianity/orthodox/orthodox", "раскол"),
    ("02_world/abrahamic/christianity/christianity", "02_world/abrahamic/christianity/catholicism/catholicism", "раскол"),
    ("02_world/abrahamic/christianity/orthodox/orthodox", "02_world/abrahamic/christianity/orthodox/old_believers/old_believers", "выделилась"),
    ("02_world/dharmic/hinduism/hinduism", "02_world/dharmic/buddhism/buddhism", "выделилась"),
    ("02_world/dharmic/hinduism/hinduism", "02_world/dharmic/jainism/jainism", "выделилась"),
    ("02_world/dharmic/hinduism/hinduism", "02_world/dharmic/sikhism/sikhism", "выделилась"),
    ("02_world/dharmic/buddhism/buddhism", "02_world/dharmic/buddhism/mahayana/mahayana", "выделилась"),
    ("02_world/dharmic/buddhism/mahayana/mahayana", "02_world/dharmic/buddhism/mahayana/chan_zen/chan_zen", "выделилась"),
    ("02_world/dharmic/buddhism/mahayana/mahayana", "02_world/dharmic/buddhism/mahayana/pure_land/pure_land", "выделилась"),
    ("02_world/dharmic/buddhism/mahayana/mahayana", "02_world/dharmic/buddhism/vajrayana/vajrayana", "выделилась"),
    ("02_world/dharmic/hinduism/hinduism", "02_world/dharmic/hinduism/shaivism/shaivism", "ветка"),
    ("02_world/dharmic/hinduism/hinduism", "02_world/dharmic/hinduism/vaishnavism/vaishnavism", "ветка"),
    ("02_world/dharmic/hinduism/shaivism/shaivism", "02_world/dharmic/hinduism/shaivism/kashirsky_shaivism/kashirsky_shaivism", "ветка"),
    ("03_ancient/graeco_roman/greek/greek", "03_ancient/graeco_roman/roman/roman", "влияние"),
    ("03_ancient/graeco_roman/greek/greek", "03_ancient/graeco_roman/orpheus/orpheus", "ветка"),
    ("03_ancient/graeco_roman/greek/greek", "03_ancient/graeco_roman/pythagoreanism/pythagoreanism", "влияние"),
]
all_links = []
for src, dst in links:
    all_links.append({"source": src, "target": dst, "kind": "связь"})
node_ids = set(n['id'] for n in nodes)
for src, dst, kind in GENEALOGY:
    if src in node_ids and dst in node_ids:
        all_links.append({"source": src, "target": dst, "kind": kind})

data = {"nodes": nodes, "links": all_links}
SITE.mkdir(exist_ok=True)
out = SITE / "graph-data.json"
io.open(str(out), "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
print("graph-data.json:", len(nodes), "nodes,", len(all_links), "links")
