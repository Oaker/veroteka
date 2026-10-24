# -*- coding: utf-8 -*-
"""
Веротека - сборщик сайта.
Markdown (content/) -> HTML (site/) + поисковый индекс (search-index.json).
Без сторонних движков: чистый Python 3.

Запуск:  python build/build.py
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = ROOT / "site"

import sys
sys.path.insert(0, str(ROOT / "build"))
from plain_texts import PLAIN

LABELS = {
    ".": "Прочее",
    "01_basics": "Основы религиоведения",
    "02_world": "Мировые религии",
    "03_ancient": "Древние и традиционные верования",
    "04_national": "Живые национальные традиции",
    "05_nrd": "Новые религиозные движения и секты",
    "06_esoteric": "Эзотерика и оккультизм",
    "07_mysticism": "Мистицизм в традициях",
    "08_skeptic": "Скептический отдел",
    "09_ref": "Справочный отдел",
    # --- авраамические ---
    "abrahamic": "Авраамические религии",
    "judaism": "Иудаизм",
    "orthodox": "Ортодоксальный иудаизм",
    "haredi": "Харедим (ультраортодоксы)",
    "modern_orthodox": "Модерн-ортодоксия",
    "hasidism": "Хасидизм",
    "conservative": "Консервативный иудаизм",
    "reform": "Реформистский иудаизм",
    "reconstructionism": "Реконструктивизм",
    "karaism": "Караизм",
    "samaritans": "Самаритяне",
    "christianity": "Христианство",
    "oriental_orthodox": "Древневосточные церкви",
    "coptic": "Коптская церковь",
    "armenian": "Армянская церковь",
    "ethiopian": "Эфиопская церковь",
    "syriac": "Сирийские традиции",
    "eastern_orthodox": "Православие",
    "old_believers": "Старообрядчество",
    "catholicism": "Католицизм",
    "eastern_catholic": "Восточнокатолические церкви",
    "protestantism": "Протестантизм",
    "lutheranism": "Лютеранство",
    "anglicanism": "Англиканство",
    "reformed": "Реформатство",
    "baptists": "Баптизм",
    "methodism": "Методизм",
    "pentecostalism": "Пятидесятничество",
    "adventism": "Адвентизм",
    "anabaptists": "Анабаптизм",
    "quakers": "Квакеры",
    "para_christianity": "Пара-христианские движения (статус спорный)",
    "mormonism": "Мормонизм",
    "jehovahs_witnesses": "Свидетели Иеговы",
    "islam": "Ислам",
    "sunni": "Суннизм",
    "madhabs": "Правовые школы (мазхабы)",
    "hanafi": "Ханафиты",
    "maliki": "Маликиты",
    "shafii": "Шафииты",
    "hanbali": "Ханбалиты",
    "salafism": "Салафизм",
    "shia": "Шиизм",
    "twelver": "Двунадесятники",
    "ismailism": "Исмаилизм",
    "zaydism": "Зайдизм",
    "ghulat": "Гулат (крайние шииты)",
    "sufism": "Суфизм (мистическая традиция)",
    "naqshbandi": "Накшбандия",
    "qadiri": "Кадирия",
    "mevlevi": "Мевлевия",
    "chishti": "Чиштия",
    "related_movements": "Связанные движения (статус спорный)",
    "ahmadiyya": "Ахмадие",
    "druze": "Друзы",
    "ibadism": "Ибадизм",
    "bahai": "Бахаи",
    # --- дхармические / иранские узлы ---
    "dharmic": "Дхармические религии (семейный узел)",
    "iranian": "Иранские религии (семейный узел)",
    "zoroastrianism": "Зороастризм",
    "parsi": "Парсы (Индия)",
    "iranian": "Иранские зороастрийцы",
    "zurvanism_historic": "Зурванизм (исторический, ушедшая ветвь)",
    "yazidism": "Езидизм",
    "yarsanism": "Ярсан",
    "mandaeism": "Мандеизм",
    # --- 01 Основы ---
    "concepts": "Ключевые понятия",
    "typology": "Типологии религий",
    "sociology_of_religion": "Социология религии",
    "psychology_of_religion": "Психология религии",
    "phenomenology": "Феноменология религии",
    "study_history": "История религиоведения",
    # --- 03 Древние ---
    "near_east": "Ближний Восток",
    "mesopotamian": "Месопотамия",
    "egyptian": "Египет",
    "canaanite": "Ханаан",
    "graeco_roman": "Греко-римский мир",
    "greek": "Греческая религия",
    "roman": "Римская религия",
    "hellenistic": "Эллинизм",
    "european": "Европа",
    "slavic_tradition": "Славянская древняя традиция",
    "norse": "Скандинавское",
    "celtic": "Кельтское",
    "baltic": "Балтийское",
    "american": "Америки",
    "mesoamerica": "Мезоамерика",
    "andes": "Анды",
    "north_america": "Северная Америка",
    "africa": "Африка",
    "steppe_siberia": "Степь и Сибирь",
    "oceania": "Океания",
    "yoruba_ifa": "Йоруба / Ифа",
    "vodun": "Водун",
    "diaspora": "Диаспорные традиции",
    "santeria": "Сантерия",
    "candomble": "Кандомбле",
    "asian_folk": "Азия (народные традиции)",
    "siberian_shamanism": "Сибирский шаманизм",
    "tengrism": "Тенгрианство",
    "australian": "Австралия (аборигенные)",
    "polynesian": "Полинезийские",
    "modern_traditions": "Возрождённые традиции (XIX-XXI вв.)",
    "wicca": "Викка",
    "heathenry": "Хитренство (германское)",
    "romuva": "Ромува",
    "dievturi": "Диевтури",
    "slavic_rodnovery": "Родноверие",
    # --- 04 Национальные ---
    "china": "Китай",
    "daoism": "Даосизм",
    "quanzhen": "Цюаньчжэнь",
    "zhengyi": "Чжэнъи",
    "confucianism": "Конфуцианство",
    "chinese_folk": "Китайская народная религия",
    "japan": "Япония",
    "shinto": "Синтоизм",
    "shrine_shinto": "Храмовый синто",
    "sect_shinto": "Сектантский синто",
    "state_shinto": "Государственный синто",
    "ryukyuan": "Рюкюсские верования",
    "korea": "Корея",
    "muism": "Муизм (корейский шаманизм)",
    "baltic_finnic": "Прибалтийско-финские традиции",
    "veps": "Вепсы",
    "cheondogyo": "Чхондогё",
    "vietnam": "Вьетнам",
    "dao_mau": "ДАО-мау (культ матерей)",
    # --- 05 НРД ---
    "spiritism_kardecism": "Спиритизм (кардецизм)",
    "parody": "Пародийные религии",
    "castanedianism": "Кастенедианство (последователи Кастанеды)",
    "neo_shamanism": "Неошаманизм",
    "subgenius": "Церковь Всевышнего Слова (SubGenius)",
    "dudeism": "Дудизм",
    "kopimism": "Копимизм",
    "jediism": "Джедаизм",
    "ufo": "НЛО-культизм",
    "raelism": "Раэлиты",
    "heavens_gate": "Врата Небес",
    "scientology": "Саентология",
    "russian": "Российские НРД",
    "vissarionites": "Виссарионовцы",
    "white_brotherhood": "Белое братство",
    "anastasians": "Анастасийцы",
    "east_asian_new": "Восточноазиатские новые движения",
    "falun_gong": "Фалуньгун",
    "lgat": "Крупногрупповые тренинги (LGAT)",
    "landmark": "Ландмарк",
    "thematic": "Тематические досье",
    "recruitment": "Как работает вербовка",
    "control_techniques": "Техники контроля",
    "exit_recovery": "Выход и восстановление",
    "cult_checklist": "Чек-лист распознавания",
    # --- 06 Эзотерика ---
    "hermeticism": "Герметизм",
    "gnosticism": "Гностицизм",
    "alchemy": "Алхимия",
    "astrology": "Астрология",
    "magic": "Магия",
    "grimoire": "Гримуарная традиция",
    "chaos_magic": "Хаос-магия",
    "folk_magic": "Народная магия",
    "kabbalah": "Каббала",
    "jewish_kabbalah": "Иудейская каббала",
    "hermetic_kabbalah": "Герметическая каббала",
    "rosicrucianism": "Розенкрейцерство",
    "golden_dawn": "Золотая Заря",
    "masonry": "Масонство",
    "masonry_russia": "Масонство в России",
    "discordianism": "Дискордианизм",
    "theosophy": "Теософия",
    "anthroposophy": "Антропософия",
    "spiritualism": "Спиритуализм",
    "new_thought": "Новая мысль",
    "new_age": "Нью-эйдж",
    # --- 07 Мистицизм ---
    "christian": "Христианский мистицизм",
    "islamic": "Исламский мистицизм",
    "jewish": "Еврейский мистицизм",
    "hindu": "Индуистский мистицизм",
    "buddhist": "Буддийский мистицизм",
    "taoist": "Даосский мистицизм",
    "comparative": "Сравнительное изучение",
    # --- 08 Скептический ---
    "atheism": "Атеизм",
    "agnosticism": "Агностицизм",
    "secular_humanism": "Светский гуманизм",
    "freethought": "Свободомыслие",
    "quasi_religions": "Квази-религии",
    "marxism": "Марксизм как политическая религия",
    "leninism": "Ленинизм как политическая религия",
    "stalinism": "Сталинизм как политическая религия",
    "civil_religion": "Гражданская религия",
    "scientism": "Сциентизм",
    "manipulation_detection": "Распознавание манипуляций",
    "pastafarianism": "Пастафарианство",
    "criticism_of_religion": "Критика религии",
    "science_of_religious_experience": "Наука о религиозном опыте",
    "pseudohistory": "Псевдоистория",
    "masonic_conspiracy": "Масонский заговор",
    "conspiracy": "Конспирология",
    "illuminati": "Иллюминаты",
    "satanic_panic": "Сатанинская паника",
    "flat_earth": "Плоская Земля",
    "hidden_symbols": "Скрытые символы",
    "tartaria": "Тартария",
    "debunking": "Как разоблачать",
    # --- 09 Справочный ---
    "glossary": "Глоссарий",
    "persons": "Персоналии",
    "timeline": "Хронология",
    "maps": "Карты",
    "bibliography": "Библиография",
    # --- индуизм ---
    "hinduism": "Индуизм",
    "shaivism": "Шиваизм",
    "shaiva_siddhanta": "Шайва-сиддханта",
    "pashupata": "Пашупата (историческая линия)",
    "kapalika_kalamukha": "Капалики и каламукхи (исторические)",
    "shaiva_siddhanta": "Шайва-сиддханта",
    "nondual_kashmir": "Недуальный тантрический шиваизм (кашмирский кластер)",
    "kula": "Кула",
    "krama": "Крама",
    "spanda": "Спанда",
    "pratyabhijna": "Пратьябхиджня",
    "trika": "Трика",
    "vira_shaiva_lingayat": "Вира-шайва (лингаяты) — спорный статус",
    "nath_tradition": "Натхи (горакханатхи)",
    "aghora": "Агхора",
    "siddhars_tamil": "Тамильские сиддхары",
    "kashirsky_shaivism": "Каширский шиваизм (Россия, НРД)",
    "advaita_juggling": "Адвайта-джаглинг (недуальное жонглирование)",
    "vaishnavism": "Вишнуизм",
    "sri_vaishnavism": "Шри-вайшнавизм",
    "gaudiya": "Гаудия-вайшнавизм",
    "madhva": "Мадхва",
    "vallabha": "Валлабха",
    "shaktism": "Шактизм",
    "sri_vidya": "Шри-видья",
    "kaula": "Каула",
    "smartism": "Смартизм",
    "darshanas": "Даршаны (философские школы)",
    "samkhya": "Санкхья",
    "yoga": "Йога",
    "nyaya": "Ньяя",
    "vaisheshika": "Вайшешика",
    "mimamsa": "Миманса",
    "vedanta": "Веданта",
    # --- буддизм ---
    "buddhism": "Буддизм",
    "historic_schools": "Исторические школы (ушедшие)",
    "theravada": "Тхеравада",
    "forest_tradition": "Лесная традиция",
    "vipassana": "Движение випассаны",
    "mahayana": "Махаяна",
    "chan_zen": "Семья чань/дзен",
    "chan": "Чань (Китай)",
    "zen_rinzai": "Дзен Риндзай (Япония)",
    "zen_soto": "Дзен Сото (Япония)",
    "korean_seon": "Сон (Корея)",
    "vietnamese_thien": "Тхиен (Вьетнам)",
    "pure_land": "Чистые земли",
    "jodo_shinshu": "Дзёдо-синсю",
    "tiantai": "Тяньтай",
    "huayan": "Хуаянь",
    "nichiren": "Ничирэн",
    "vajrayana": "Ваджраяна",
    "tibetan": "Тибетский буддизм",
    "nyingma": "Ньингма",
    "kagyu": "Кагью",
    "sakya": "Сакья",
    "gelug": "Гелуг",
    "shingon": "Сингон (Япония)",
    # --- прочие дхармические ---
    "sikhism": "Сикхизм",
    "jainism": "Джайнизм",
    "digambara": "Дигамбара",
    "sthanakvasi": "Стахакваси",
    "murtipujaka": "Муртипуджака",
    "nihang": "Ниханг (воинский орден)",
    "namdhari": "Намдхари (кука)",
    "nirankari": "Ниранкари",
    "udasi": "Удаси (аскетический орден)",
    "shvetambara": "Шветамбара",
}

# ------------------------------------------------------------- autolinking --
LINKMAP = []          # [(title, rel_url)]  заполняется в main()
PLACEHOLDER = "\x00"

def build_linkmap(articles):
    m = []
    for a in articles:
        if a["lang"] != "ru":
            continue
        m.append((a["title"], a["rel_url"]))
    ALIASES = {
        "Будда": "09_ref/persons/buddha",
        "Иисус": "02_world/abrahamic/christianity/christianity",
        "Мухаммад": "09_ref/persons/muhammad",
        "Конфуций": "09_ref/persons/confucius",
        "Лао-цзы": "09_ref/persons/laozi",
        "Шанкара": "09_ref/persons/shankara",
        "Абхинавагупта": "09_ref/persons/abhinavagupta",
        "Чжуан-цзы": "09_ref/persons/zhuangzi",
        "Насреддин": "09_ref/persons/nasreddin",
        "Коан": "09_ref/persons/koan",
        "Руми": "09_ref/persons/rumi",
        "Миларепа": "09_ref/persons/milarepa",
        "Нагарджуна": "09_ref/persons/nagarjuna",
        "Рамануджа": "09_ref/persons/ramanuja",
        "Нанак": "09_ref/persons/nanak",
        "Махавира": "09_ref/persons/mahavira",
        "Заратуштра": "09_ref/persons/zarathushtra",
        "Тереза Авильская": "09_ref/persons/teresa",
        "Далай-лама": "09_ref/persons/dalai_lama",
        "Ибн Араби": "02_world/abrahamic/islam/sufism/sufism",
        "Каширский вестник": "02_world/dharmic/hinduism/shaivism/advaita_juggling/kashira_vestnik",
        "Линия Каширы": "02_world/dharmic/hinduism/shaivism/kashirsky_shaivism/line_kashira",
        "Шиваизм": "02_world/dharmic/hinduism/shaivism/shaivism",
        "Адвайта-веданта": "02_world/dharmic/hinduism/darshanas/vedanta/vedanta",
        "Веданта": "02_world/dharmic/hinduism/darshanas/vedanta/vedanta",
        "Ария (ārya)": "09_ref/glossary/arya",
        "Трика": "02_world/dharmic/hinduism/shaivism/nondual_kashmir/trika/trika",
        "Спанда": "02_world/dharmic/hinduism/shaivism/nondual_kashmir/spanda/spanda",
        "Пратьябхиджня": "02_world/dharmic/hinduism/shaivism/nondual_kashmir/pratyabhijna/pratyabhijna",
        "Каббала": "06_esoteric/kabbalah/kabbalah",
        "Дзогчен": "07_mysticism/buddhist/dzogchen/dzogchen",
        "Махамудра": "07_mysticism/buddhist/mahamudra/mahamudra",
        "Исихазм": "07_mysticism/christian/hesychasm/hesychasm",
        "Тереза": "09_ref/persons/teresa",
        "Мадхьямака": "02_world/dharmic/buddhism/mahayana/mahayana",
    }
    for alias, url in ALIASES.items():
        m.append((alias, url))
    # длинные сначала, без дублей url+title
    seen = set()
    out = []
    for title, url in sorted(m, key=lambda x: -len(x[0])):
        key = (title.lower(), url)
        if key in seen:
            continue
        seen.add(key)
        out.append((title, url))
    return out

_autolink_n = [0]

def autolink(text, current_rel=None):
    """Первое вхождение каждого названия -> плейсхолдер-ссылка."""
    for title, url in LINKMAP:
        if current_rel and url == current_rel:
            continue
        if len(title) < 3:
            continue
        pat = re.compile(re.escape(title), re.IGNORECASE)
        m = pat.search(text)
        if not m:
            continue
        _autolink_n[0] += 1
        ph = "%s%d%s" % (PLACEHOLDER, _autolink_n[0], PLACEHOLDER)
        text = text[:m.start()] + ph + text[m.end():]
        LINK_PH[_autolink_n[0]] = (url, m.group(0))
    return text

LINK_PH = {}

def restore_links(html_text):
    def rep(m):
        url, label = LINK_PH.get(int(m.group(1)), ("#", "?"))
        return '<a href="ru/%s.html">%s</a>' % (url, html.escape(label))
    return re.sub('\x00(\\d+)\x00', rep, html_text)

# ---------------------------------------------------------------- markdown --
def md_inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = restore_links(text)
    return text

def md_plain(text):
    """Markdown -> чистый однострочный текст для анонсов и поиска."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = re.sub(r"^\s*---+\s*$", " ", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()

def md_to_html(md_text):
    out, i = [], 0
    lines = md_text.splitlines()
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("```"):
            block = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, md_inline(m.group(2)), level))
            i += 1; continue
        if re.match(r"^\s*---+\s*$", line):
            out.append("<hr>"); i += 1; continue
        if re.match(r"^\s*>\s?", line):
            block = []
            while i < n and re.match(r"^\s*>\s?", lines[i]):
                block.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append("<blockquote>" + md_to_html("\n".join(block)) + "</blockquote>")
            continue
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i])); i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % md_inline(x) for x in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i])); i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % md_inline(x) for x in items) + "</ol>")
            continue
        if line.strip() == "":
            i += 1; continue
        para = []
        while i < n and lines[i].strip() != "" and not re.match(r"^(#{1,4}\s|```|\s*>|\s*[-*]\s|\s*\d+\.\s|\s*---+\s*$)", lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>" + md_inline(" ".join(para)) + "</p>")
    return "\n".join(out)

# ---------------------------------------------------------------- frontmatter
def parse_frontmatter(md_text):
    meta, body = {}, md_text
    if md_text.lstrip().startswith("---"):
        parts = md_text.lstrip().split("---", 2)
        if len(parts) >= 3:
            for raw in parts[1].splitlines():
                if ":" in raw:
                    k, v = raw.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            body = parts[2]
    return meta, body

# ---------------------------------------------------------------- layout ----
PAGE_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Веротека</title>
<meta property="og:title" content="{title} — Веротека">
<meta property="og:description" content="Энциклопедия религий, конфессий, сект и эзотерических учений">
<meta property="og:type" content="article">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="{rel}index.html">Веротека</a>
  <nav class="topnav">
    <a href="{rel}tree.html">Дерево</a>
    <a href="{rel}az.html">А-Я</a>
    <a href="{rel}tags.html">Теги</a>
    <a href="{rel}axis.html">Ось</a>
  </nav>
  <input id="searchbox" type="search" placeholder="Поиск..." autocomplete="off">
  <button id="themeToggle" title="Тёмная/светлая тема">&#127769;</button>
</header>
<div id="searchresults"></div>
<main>
{content}
</main>
<footer>
<p>(c) 2026 Sergey Che - Веротека - Контент CC BY 4.0</p>
</footer>
<script src="{rel}assets/app.js"></script>
</body>
</html>"""

def render_page(title, content_html, lang="ru", rel=""):
    return PAGE_TMPL.format(title=html.escape(title), content=content_html, lang=lang, rel=rel)

# ---------------------------------------------------------------- сборка ----
def collect_articles():
    articles = []
    for lang in ("ru", "en"):
        base = CONTENT / lang
        if not base.exists():
            continue
        for md_file in sorted(base.rglob("*.md")):
            raw = md_file.read_text(encoding="utf-8-sig")
            meta, body = parse_frontmatter(raw)
            title = meta.get("title") or md_file.stem.replace("_", " ").capitalize()
            rel_url = str(md_file.relative_to(base)).replace("\\", "/")[:-3]
            articles.append({
                "lang": lang, "path": md_file, "rel_url": rel_url,
                "meta": meta, "body": body, "title": title,
            })
    return articles

AXIS_LABELS = {"dvaita": "двайта", "advaita": "адвайта", "sunyata": "пустотные"}

def article_html(a):
    meta = a["meta"]
    parts = []
    axis = meta.get("axis")
    if axis:
        al = AXIS_LABELS.get(axis.strip().lower(), axis)
        parts.append('<div class="axis">ось: %s</div>' % html.escape(al))
    plain = PLAIN.get("ru/" + a["rel_url"])
    if not plain:
        # автогенерация: первое предложение определения (до первой точки, из первых 400 знаков тела)
        body_flat = re.sub(r"\s+", " ", a["body"]).strip()
        m = re.match(r"^\*\*[^*]+\*\*\s*[—–-]\s*(.+?)(?:\.|$)", body_flat)
        if m and len(m.group(1)) > 20:
            plain = m.group(1).rstrip(". ") + "."
        else:
            m2 = re.match(r"^(.{80,240}?[.!?])(\s|$)", body_flat)
            plain = m2.group(1) if m2 else body_flat[:160] + "..."
    if plain:
        parts.append(
            '<details class="plain-box"><summary>Для профанов (просто о главном)</summary><div>%s</div></details>'
            % html.escape(plain)
        )
    level = meta.get("level")
    if level:
        parts.append('<div class="badge">уровень: %s</div>' % html.escape(level))
    tags = meta.get("tags")
    if tags:
        chips = "".join('<span class="chip">%s</span>' % html.escape(t.strip()) for t in tags.split(",") if t.strip())
        parts.append('<div class="chips">%s</div>' % chips)
    parts.append(md_to_html(autolink(a["body"], a["rel_url"])))
    editor = meta.get("editor")
    if editor:
        parts.append(
            '<div class="editor-box"><div class="who">Позиция редактора — Doctor Che</div>%s</div>'
            % md_to_html(autolink(editor, a["rel_url"]))
        )
    return "\n".join(parts)

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "assets").mkdir()

    articles = collect_articles()
    global LINKMAP
    LINKMAP = build_linkmap(articles)
    ru = [a for a in articles if a["lang"] == "ru"]

    # структура каталога: узлы-папки = иерархия разделов
    node_articles = {}
    all_dirs = set()
    for a in ru:
        d = a["rel_url"].rsplit("/", 1)[0] if "/" in a["rel_url"] else "."
        node_articles.setdefault(d, []).append(a)
        parts = d.split("/") if d != "." else []
        for i in range(1, len(parts) + 1):
            all_dirs.add("/".join(parts[:i]))
        if d == ".":
            all_dirs.add(".")
    content_root = CONTENT / "ru"
    for p in content_root.rglob("*"):
        if p.is_dir():
            rel = p.relative_to(content_root).as_posix()
            if not rel.startswith("."):
                all_dirs.add(rel)
    children = {}
    for d in all_dirs:
        if d == ".":
            continue
        parent = d.rsplit("/", 1)[0] if "/" in d else "."
        children.setdefault(parent, []).append(d)
    for k in list(children):
        children[k].sort()
    subtree_count = {}
    def accum(d):
        n = len(node_articles.get(d, []))
        for s in children.get(d, []):
            n += accum(s)
        subtree_count[d] = n
        return n
    for s in children.get(".", []):
        accum(s)
    existing = set((a["lang"], a["rel_url"]) for a in articles)

    def crumb_label(part):
        return LABELS.get(part, part.replace("_", " ").capitalize())

    def up_prefix(rel_url):
        return "../" * (rel_url.count("/") + 1)

    def crumbs_html(a):
        parts = a["rel_url"].split("/")
        rel = up_prefix(a["rel_url"])
        out = ['<nav class="crumbs"><a href="%sindex.html">Главная</a>' % rel]
        for i, p in enumerate(parts[:-1]):
            prefix = "/".join(parts[:i + 1])
            hub = prefix + "/" + p
            label = crumb_label(p)
            if (a["lang"], hub) in existing:
                out.append('<span class="sep">&rsaquo;</span><a href="%s%s/%s.html">%s</a>' % (rel, a["lang"], hub, html.escape(label)))
            else:
                out.append('<span class="sep">&rsaquo;</span><span>%s</span>' % html.escape(label))
        out.append('<span class="sep">&rsaquo;</span><b>%s</b>' % html.escape(a["title"]))
        out.append("</nav>")
        return "".join(out)

    def folder_link(s, prefix=""):
        label = crumb_label(s.split("/")[-1])
        n = subtree_count.get(s, 0)
        hub = s + "/" + s.split("/")[-1]
        if ("ru", hub) in existing:
            return '<li><a href="%sru/%s.html">%s</a> <span class="count">(%d)</span></li>' % (prefix, hub, html.escape(label), n)
        # иначе ищем первую статью в ПОДДЕРЕВЕ узла как вход
        def first_in(sub):
            arts = sorted(node_articles.get(sub, []), key=lambda t: t["title"])
            if arts:
                return arts[0]
            for ch in children.get(sub, []):
                r = first_in(ch)
                if r:
                    return r
            return None
        first = first_in(s)
        if first:
            return '<li><a href="%sru/%s.html">%s</a> <span class="count">(%d)</span></li>' % (prefix, first["rel_url"], html.escape(label), n)
        return '<li class="planned">%s <span class="count">(%d)</span></li>' % (html.escape(label), n)

    def section_nav_html(a):
        d = a["rel_url"].rsplit("/", 1)[0] if "/" in a["rel_url"] else "."
        if d == ".":
            return ""
        sibs = [x for x in node_articles.get(d, []) if x["rel_url"] != a["rel_url"]]
        subs = children.get(d, [])
        if not sibs and not subs:
            return ""
        rel = up_prefix(a["rel_url"])
        out = ['<div class="secnav"><div class="who">В этом разделе</div><ul>']
        for s in sorted(subs):
            out.append(folder_link(s, rel))
        for x in sorted(sibs, key=lambda t: t["title"]):
            out.append('<li><a href="%s%s/%s.html">%s</a></li>' % (rel, x["lang"], x["rel_url"], html.escape(x["title"])))
        out.append("</ul></div>")
        return "\n".join(out)

    (SITE / "assets" / "style.css").write_text(DEFAULT_CSS, encoding="utf-8")
    (SITE / "assets" / "app.js").write_text(DEFAULT_JS, encoding="utf-8")

    index_entries, az, tags = [], {}, {}
    for a in articles:
        out_file = SITE / a["lang"] / (a["rel_url"] + ".html")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        depth = a["rel_url"].count("/") + 1
        rel = "../" * depth
        out_file.write_text(render_page(a["title"], crumbs_html(a) + article_html(a) + section_nav_html(a), a["lang"], rel), encoding="utf-8")
        excerpt = md_plain(a["body"])[:300]
        index_entries.append({
            "title": a["title"], "url": "%s/%s.html" % (a["lang"], a["rel_url"]),
            "lang": a["lang"],
            "tags": [t.strip() for t in (a["meta"].get("tags") or "").split(",") if t.strip()],
            "excerpt": excerpt,
        })
        if a["lang"] == "ru":
            letter = a["title"][0].upper()
            az.setdefault(letter, []).append(a)
            for t in (a["meta"].get("tags") or "").split(","):
                t = t.strip()
                if t:
                    tags.setdefault(t, []).append(a)

    # index.html — иерархическая главная: разделы 1-го уровня с навигацией
    TOP_SECTIONS = ["01_basics", "02_world", "03_ancient", "04_national", "05_nrd", "06_esoteric", "07_mysticism", "08_skeptic", "09_ref"]
    home_parts = [
        "<h1>Веротека</h1>",
        "<p>Энциклопедия религий, конфессий, сект и эзотерических учений. Нейтральные статьи + позиция редактора (Doctor Che).</p>",
    ]
    for sec in TOP_SECTIONS:
        if sec not in all_dirs:
            continue
        home_parts.append('<h2 class="sech">%s <span class="count">(%d)</span></h2>' % (html.escape(crumb_label(sec)), subtree_count.get(sec, 0)))
        home_parts.append('<ul class="home-list">')
        for x in sorted(node_articles.get(sec, []), key=lambda t: t["title"]):
            home_parts.append('<li class="art"><a href="ru/%s.html">%s</a></li>' % (x["rel_url"], html.escape(x["title"])))
        for s in sorted(children.get(sec, [])):
            home_parts.append(folder_link(s))
        home_parts.append("</ul>")
    root_arts = node_articles.get(".", [])
    if root_arts:
        home_parts.append('<h2 class="sech">Прочее</h2><ul class="home-list">')
        for x in sorted(root_arts, key=lambda t: t["title"]):
            home_parts.append('<li class="art"><a href="ru/%s.html">%s</a></li>' % (x["rel_url"], html.escape(x["title"])))
        home_parts.append("</ul>")
    home = render_page("Главная", "\n".join(home_parts))
    (SITE / "index.html").write_text(home, encoding="utf-8")

    # tree.html — полное раскрытое дерево (структура папок = иерархия)
    tree_html = ["<h1>Дерево разделов</h1>",
                 "<p class=muted>Полная иерархия. Числа — количество статей. Пустые узлы показывают планируемые разделы.</p>"]

    def dir_label(name):
        return LABELS.get(name, name.replace("_", " "))

    def render_node(d, depth):
        out = []
        arts = node_articles.get(d, [])
        # статьи этого узла (лежащие прямо в нём)
        direct = [a for a in arts if (a["rel_url"].rsplit("/", 1)[0] if "/" in a["rel_url"] else ".") == d]
        subs = children.get(d, [])
        label = dir_label(d.split("/")[-1])
        if not subs and not direct:
            out.append('<li class="planned">%s</li>' % html.escape(label))
            return out
        count = subtree_count.get(d, 0)
        head = "%s <span class=count>(%d)</span>" % (html.escape(label), count)
        if depth == 0:
            out.append("<h2>%s</h2>" % head)
            for a in sorted(direct, key=lambda x: x["title"]):
                out.append('<li class=art><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
            for s in subs:
                out.extend(render_node(s, depth + 1))
        else:
            open_attr = " open" if depth <= 1 else ""
            out.append("<details%s><summary>%s</summary>" % (open_attr, head))
            if direct:
                out.append("<ul>")
                for a in sorted(direct, key=lambda x: x["title"]):
                    out.append('<li class=art><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
                out.append("</ul>")
            for s in subs:
                out.extend(render_node(s, depth + 1))
            out.append("</details>")
        return out

    top_sections = ["01_basics","02_world","03_ancient","04_national","05_nrd","06_esoteric","07_mysticism","08_skeptic","09_ref"]
    for sec in top_sections:
        if sec in all_dirs:
            tree_html.extend(render_node(sec, 0))
    # статьи в корне (вне разделов)
    root_arts = node_articles.get(".", [])
    if root_arts:
        tree_html.append("<h2>Прочее</h2><ul>")
        for a in sorted(root_arts, key=lambda x: x["title"]):
            tree_html.append('<li class=art><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        tree_html.append("</ul>")
    (SITE / "tree.html").write_text(render_page("Дерево", "\n".join(tree_html)), encoding="utf-8")

    # az.html
    az_html = ["<h1>Алфавитный указатель</h1>"]
    for letter in sorted(az):
        az_html.append("<h2>%s</h2><ul>" % html.escape(letter))
        for a in sorted(az[letter], key=lambda x: x["title"].lower()):
            az_html.append('<li><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        az_html.append("</ul>")
    if not az:
        az_html.append("<p>Статьи пока не написаны.</p>")
    (SITE / "az.html").write_text(render_page("А-Я", "\n".join(az_html)), encoding="utf-8")

    # tags.html
    tags_html = ["<h1>Теги</h1>"]
    for t in sorted(tags):
        tags_html.append("<h2>%s</h2><ul>" % html.escape(t))
        for a in tags[t]:
            tags_html.append('<li><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        tags_html.append("</ul>")
    if not tags:
        tags_html.append("<p>Теги пока не проставлены.</p>")
    (SITE / "tags.html").write_text(render_page("Теги", "\n".join(tags_html)), encoding="utf-8")

    # axis.html - navigacija po doktrinal'nym poljusam
    axis_groups = {"dvaita": [], "advaita": [], "sunyata": []}
    for a in ru:
        ax = (a["meta"].get("axis") or "").strip().lower()
        if ax in axis_groups:
            axis_groups[ax].append(a)
    ax_html = ["<h1>\u041e\u0441\u044c \u0432\u0437\u0433\u043b\u044f\u0434\u0430: \u0434\u0432\u0430\u0439\u0442\u0430 \u00b7 \u0430\u0434\u0432\u0430\u0439\u0442\u0430 \u00b7 \u043f\u0443\u0441\u0442\u043e\u0442\u0430</h1>",
               "<p>\u0421\u043a\u0432\u043e\u0437\u043d\u0430\u044f \u043a\u043b\u0430\u0441\u0441\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0412\u0435\u0440\u043e\u0442\u0435\u043a\u0438.</p>"]
    for key, title, desc in (
        ("dvaita", "\u0414\u0432\u0430\u0439\u0442\u0430 - \u0434\u0443\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c", "\u0422\u0432\u043e\u0440\u0435\u0446 \u0438 \u0442\u0432\u043e\u0440\u0435\u043d\u0438\u0435 \u0440\u0430\u0437\u043b\u0438\u0447\u043d\u044b."),
        ("advaita", "\u0410\u0434\u0432\u0430\u0439\u0442\u0430 - \u043d\u0435\u0434\u0432\u043e\u0439\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u044c", "\u0415\u0434\u0438\u043d\u043e\u0435 \u0435\u0441\u0442\u044c \u0432\u0441\u0451."),
        ("sunyata", "\u041f\u0443\u0441\u0442\u043e\u0442\u0430 - \u0448\u0443\u043d\u044c\u044f\u0442\u0430", "\u041d\u0438 \u0415\u0434\u0438\u043d\u043e\u0435, \u043d\u0438 \u043c\u043d\u043e\u0433\u043e\u0433\u043e."),
    ):
        ax_html.append("<h2>%s</h2><p class=muted>%s</p><ul>" % (html.escape(title), html.escape(desc)))
        if axis_groups[key]:
            for a in sorted(axis_groups[key], key=lambda x: x["title"]):
                ax_html.append('<li><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        else:
            ax_html.append('<li class=planned>\u0441\u0442\u0430\u0442\u044c\u0438 \u0441\u043a\u043e\u0440\u043e</li>')
        ax_html.append("</ul>")
    (SITE / "axis.html").write_text(render_page("Axis", "\n".join(ax_html)), encoding="utf-8")

    # поисковый индекс
    (SITE / "search-index.json").write_text(
        json.dumps(index_entries, ensure_ascii=False, indent=1), encoding="utf-8")

    print("OK: articles=%d (ru=%d), site files=%d" % (
        len(articles), len(ru), sum(1 for _ in SITE.rglob("*") if _.is_file())))

DEFAULT_CSS = """
:root { --bg:#fafafa; --fg:#222; --muted:#666; --accent:#0a66c2; --card:#fff; --border:#ddd; }
[data-theme="dark"] { --bg:#181a1b; --fg:#e8e6e3; --muted:#999; --accent:#4da3ff; --card:#222; --border:#444; }
* { box-sizing:border-box; }
body { margin:0; font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; background:var(--bg); color:var(--fg); line-height:1.65; }
.topbar { display:flex; align-items:center; gap:1rem; padding:.7rem 1.2rem; border-bottom:1px solid var(--border); position:sticky; top:0; background:var(--bg); flex-wrap:wrap; }
.brand { font-weight:700; font-size:1.2rem; color:var(--fg); text-decoration:none; }
.topnav a { margin-right:.8rem; color:var(--accent); text-decoration:none; }
#searchbox { flex:1; min-width:140px; padding:.4rem .7rem; border:1px solid var(--border); border-radius:8px; background:var(--card); color:var(--fg); }
main { max-width:760px; margin:0 auto; padding:1.5rem 1.2rem 4rem; }
h1,h2,h3 { line-height:1.25; }
a { color:var(--accent); }
blockquote { border-left:4px solid var(--accent); margin:1rem 0; padding:.4rem 1rem; background:var(--card); }
pre { overflow:auto; padding:1rem; background:var(--card); border:1px solid var(--border); border-radius:8px; }
code { background:var(--card); padding:.1rem .3rem; border-radius:4px; }
.card { background:var(--card); border:1px solid var(--border); border-radius:10px; padding:1rem 1.2rem; margin:1rem 0; }
.badge { display:inline-block; font-size:.8rem; color:var(--muted); border:1px solid var(--border); border-radius:999px; padding:.1rem .6rem; margin-bottom:.5rem; }
.chips { margin:.2rem 0 .8rem; }
.planned { color:var(--muted); list-style:none; }
.plain-box { border:1px dashed var(--border); border-radius:8px; padding:.5rem .8rem; margin:.8rem 0; background:var(--card); }
.plain-box summary { cursor:pointer; color:var(--muted); font-size:.92rem; }
.plain-box div { margin-top:.4rem; }\n.count { color:var(--muted); font-size:.85rem; font-weight:normal; }\nsummary { cursor:pointer; }\n.chip { display:inline-block; font-size:.78rem; background:var(--card); border:1px solid var(--border); border-radius:999px; padding:.05rem .55rem; margin-right:.3rem; color:var(--muted); }
.editor-box { border:1px solid var(--border); border-left:4px solid #b8860b; background:var(--card); border-radius:8px; padding:.8rem 1rem; margin:1.5rem 0; }
.crumbs { font-size:.85rem; color:var(--muted); margin:0 0 1rem; }
.crumbs a { color:var(--muted); }
.crumbs .sep { margin:0 .4rem; }
.secnav { border:1px solid var(--border); background:var(--card); border-radius:8px; padding:.8rem 1rem; margin-top:2rem; }
.secnav .who { font-weight:600; margin-bottom:.3rem; }
.secnav ul { margin:.2rem 0; padding-left:1.2rem; }
ul.home-list { list-style:none; padding-left:0; }
ul.home-list li { padding:.18rem 0; }
h2.sech { margin-top:2.2rem; border-bottom:1px solid var(--border); padding-bottom:.25rem; }
.editor-box .who { font-weight:600; margin-bottom:.3rem; }
#searchresults { max-width:760px; margin:0 auto; padding:.5rem 1.2rem; }
#searchresults .hit { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:.6rem 1rem; margin:.4rem 0; }
footer { border-top:1px solid var(--border); color:var(--muted); text-align:center; padding:1.5rem; margin-top:2rem; }
"""

DEFAULT_JS = """
// Тема: светлая по умолчанию, переключатель с запоминанием
const toggle = document.getElementById('themeToggle');
if (localStorage.getItem('vt-theme') === 'dark') document.documentElement.dataset.theme = 'dark';
toggle && toggle.addEventListener('click', () => {
  const d = document.documentElement.dataset.theme === 'dark';
  document.documentElement.dataset.theme = d ? '' : 'dark';
  localStorage.setItem('vt-theme', d ? 'light' : 'dark');
});

// Поиск по search-index.json
const box = document.getElementById('searchbox');
const res = document.getElementById('searchresults');
let INDEX = null;
box && box.addEventListener('input', async (e) => {
  const q = e.target.value.trim().toLowerCase();
  if (q.length < 2) { res.innerHTML = ''; return; }
  if (!INDEX) {
    try { INDEX = await (await fetch('search-index.json')).json(); } catch (err) { return; }
  }
  const hits = INDEX.filter(x =>
    x.title.toLowerCase().includes(q) || x.excerpt.toLowerCase().includes(q)
  ).slice(0, 8);
  res.innerHTML = hits.map(h =>
    '<div class="hit"><a href="' + h.url + '">' + h.title + '</a><div>' + h.excerpt.slice(0,120) + '...</div></div>'
  ).join('');
});
"""

if __name__ == "__main__":
    sys.exit(main())



