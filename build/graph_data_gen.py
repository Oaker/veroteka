# -*- coding: utf-8 -*-
"""graph-data.json: узлы (религии + пантеоны + боги) и рёбра (связи). ROOT-относительный."""
import os, io, re, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

nodes = []
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
        nodes.append({
            "id": rel, "title": title, "section": rel.split("/")[0],
            "axis": axis, "year": year, "url": rel + ".html"
        })

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
PANTHEON_LINKS = [
    ("03_ancient/graeco_roman/greek/greek", "10_pantheons/greek/greek"),
    ("03_ancient/graeco_roman/roman/roman", "10_pantheons/roman/roman"),
    ("03_ancient/near_east/egyptian/egyptian", "10_pantheons/egyptian/egyptian"),
    ("03_ancient/near_east/mesopotamian/mesopotamian", "10_pantheons/mesopotamian/mesopotamian"),
    ("03_ancient/european/norse/norse", "10_pantheons/norse/norse"),
    ("03_ancient/european/slavic_tradition/slavic_tradition", "10_pantheons/slavic/slavic"),
    ("02_world/dharmic/hinduism/hinduism", "10_pantheons/indian/indian"),
    ("02_world/iranian/zoroastrianism/zoroastrianism", "10_pantheons/iranian/iranian"),
    ("04_national/china/daoism/daoism", "10_pantheons/east_asian/east_asian"),
    ("04_national/japan/japan", "10_pantheons/east_asian/east_asian"),
    ("03_ancient/european/celtic/celtic", "10_pantheons/celtic/celtic"),
    ("03_ancient/american/mesoamerica/mesoamerica", "10_pantheons/maya/maya"),
    ("03_ancient/american/mesoamerica/mesoamerica", "10_pantheons/mesoamerican/mesoamerican"),
    ("04_national/africa/africa", "10_pantheons/west_african/west_african"),
]
GOD_LINKS = [
    ("10_pantheons/greek/zeus/zeus", "10_pantheons/greek"),
    ("10_pantheons/greek/athena/athena", "10_pantheons/greek"),
    ("10_pantheons/greek/apollo/apollo", "10_pantheons/greek"),
    ("10_pantheons/norse/odin/odin", "10_pantheons/norse"),
    ("10_pantheons/norse/thor/thor", "10_pantheons/norse"),
    ("10_pantheons/norse/loki/loki", "10_pantheons/norse"),
    ("10_pantheons/egyptian/ra/ra", "10_pantheons/egyptian"),
    ("10_pantheons/egyptian/osiris/osiris", "10_pantheons/egyptian"),
    ("10_pantheons/egyptian/isis/isis", "10_pantheons/egyptian"),
    ("10_pantheons/indian/shiva/shiva", "10_pantheons/indian"),
    ("10_pantheons/indian/vishnu/vishnu", "10_pantheons/indian"),
    ("10_pantheons/indian/indra/indra", "10_pantheons/indian"),
    ("10_pantheons/slavic/perun/perun", "10_pantheons/slavic"),
    ("10_pantheons/celtic/dagda/dagda", "10_pantheons/celtic"),
    ("10_pantheons/maya/itzamna/itzamna", "10_pantheons/maya"),
]

links = []
for src, dst, kind in GENEALOGY:
    links.append({"source": src, "target": dst, "kind": kind})
for src, dst in PANTHEON_LINKS:
    links.append({"source": src, "target": dst, "kind": "пантеон"})
for dst, src in GOD_LINKS:
    links.append({"source": src, "target": dst, "kind": "бог принадлежит"})

node_ids = set(n["id"] for n in nodes)
valid_links = [l for l in links if l["source"] in node_ids and l["target"] in node_ids]

data = {"nodes": nodes, "links": valid_links}
SITE.mkdir(exist_ok=True)
out = SITE / "graph-data.json"
io.open(str(out), "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
print("graph-data.json:", len(nodes), "nodes,", len(valid_links), "links")
