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
BUILD = ROOT / "build"
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
    "popovtsy": "Поповцы",
    "belokrinitskaya": "Белокриницкая иерархия",
    "bespopovtsy": "Беспоповцы",
    "pomortsy": "Поморцы",
    "fedoseevtsy": "Федосеевцы",
    "beguny": "Бегуны (странники)",
    "spasovtsy": "Спасовцы (нетовщики)",
    "filippovtsy": "Филипповцы",
    "edinoverie": "Единоверие",
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
    "mennonites": "Меннониты",
    "amish": "Амиши",
    "quakers": "Квакеры",
    "presbyterians_us": "Пресвитериане (США)",
    "episcopalians_us": "Епископальная церковь США",
    "holiness": "Движение святости",
    "christian_science": "Христианская наука",
    "unitarianism": "Унитарианство",
    "campbellites": "Церкви Христа",
    "moravians": "Моравские братья",
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
    "indus_valley": "Индская цивилизация",
    "mesopotamian": "Месопотамия",
    "egyptian": "Египет",
    "canaanite": "Ханаан",
    "graeco_roman": "Греко-римский мир",
    "mithraism": "Митраизм",
    "orpheus": "Орфизм",
    "pythagoreanism": "Пифагорейство",
    "greek": "Греческая религия",
    "roman": "Римская религия",
    "hellenistic": "Эллинизм",
    "european": "Европа",
    "slavic_tradition": "Славянская древняя традиция",
    "norse": "Скандинавское",
    "celtic": "Кельтское",
    "baltic": "Балтийское",
    "etskaya": "Этрусская религия",
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
    "martinism": "Мартинизм",
    "tarot": "Таро",
    "thelema": "Телема",
    "la_vey_satanism": "Сатанизм ЛаВея",
    "anthroposophy": "Антропософия",
    "spiritualism": "Спиритуализм",
    "new_thought": "Новая мысль",
    "new_age": "Нью-эйдж",
    # --- 07 Мистицизм ---
    "christian": "Христианский мистицизм",
    "islamic": "Исламский мистицизм",
    "rabia": "Рабия аль-Адавия",
    "jewish": "Еврейский мистицизм",
    "hindu": "Индуистский мистицизм",
    "mirabai": "Мирабай",
    "buddhist": "Буддийский мистицизм",
    "mahamudra_path": "Махамудра: ступени практики",
    "taoist": "Даосский мистицизм",
    "neidan_practice": "Нэйдань: практика",
    "comparative": "Сравнительное изучение",
    "modern": "Современный мистицизм",
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
    # --- дозаполнение 2026-11: русские названия узлов ---
    "about": "О проекте",
    "attar": "Фарид ад-Дин Аттар",
    "bonhoeffer_nonreligious": "Безрелигиозное христианство",
    "church_of_east": "Ассирийская Церковь Востока",
    "cloud_unknowing": "Облако неведения",
    "conversion_psych": "Психология обращения",
    "dogen": "Догэн",
    "dzogchen": "Дзогчен",
    "faq_kashira": "Вопросы о линии Каширы",
    "hakuin": "Хакуин",
    "hesychasm": "Исихазм",
    "ibn_arabi": "Ибн Араби",
    "jhanas": "Джханы",
    "john_cross": "Иоанн Креста",
    "line_kashira": "Линия Каширы",
    "mahamudra": "Махамудра",
    "palama": "Григорий Палама",
    "practice_kashira": "Практика линии",
    "ramakrishna": "Рамакришна",
    "ruusbroec": "Ян ван Рёйсбрук",
    "terapanthi": "Терапантхи",
    "tilopa": "Тилопа",
    "vivekananda": "Вивекананда",
    "advaita_vedanta": "Адвайта-веданта",
    "religion_and_society": "Религия и общество",
    "revived_traditions": "Возрождённые традиции",
    "10_pantheons": "Боги, герои и пророки",
    "morena": "Морена",
    "yarilo": "Ярило",
    "svarog": "Сварог",
    "stribog": "Стрибог",
    "hors": "Хорс",
    "dazhbog": "Дажьбог",
    "yggdrasil": "Иггдрасиль",
    "vidar": "Видар",
    "ullr": "Улль",
    "forseti": "Форсети",
    "bragi": "Браги",
    "ragnarok": "Рагнарёк",
    "valkyries": "Валькирии",
    "norns": "Норны",
    "sif": "Сиф",
    "idunn": "Идунн",
    "heimdallr": "Хеймдалль",
    "freyr": "Фрейр",
    "kama": "Кама",
    "tara": "Тара",
    "ganga": "Ганга",
    "kubera": "Кубера",
    "vayu": "Ваю",
    "soma": "Сома",
    "yama": "Яма",
    "surya": "Сурья",
    "radha": "Радха",
    "sita": "Сита",
    "hanuman": "Хануман",
    "ganesha": "Ганеша",
    "parvati": "Парвати",
    "brahma": "Брахма",
    "prometheus": "Прометей",
    "dioscuri": "Диоскуры",
    "pan": "Пан",
    "hecate": "Геката",
    "helios": "Гелиос",
    "hestia": "Гестия",
    "xunzi": "Сюнь-цзы",

    "william_james": "Уильям Джеймс",

    "tsongkhapa": "Цонкапа",

    "theodore_of_mopsuestia": "Феодор Мопсуестийский",

    "steiner": "Рудольф Штайнер",

    "sergiy_radonezhsky": "Сергий Радонежский",

    "serafim_sarovsky": "Серафим Саровский",

    "padmasambhava": "Падмасамбхава",

    "ouspensky": "Пётр Успенский",

    "origen": "Ориген",

    "nestorius": "Несторий",

    "naropa": "Наропа",

    "mencius": "Мэн-цзы",

    "meister_eckhart": "Мейстер Экхарт",

    "marpa": "Марпа",

    "mani": "Мани",

    "maimonides": "Маймонид",

    "luther": "Мартин Лютер",

    "jung": "Карл Густав Юнг",

    "hafiz": "Хафиз",

    "gurdjieff": "Георгий Гурджиев",

    "george_fox": "Джордж Фокс",

    "gampopa": "Гампопа",

    "ephrem_syrian": "Ефрем Сирин",

    "eliade": "Мирча Элиаде",

    "crowley": "Алистер Кроули",

    "chaitanya": "Чайтанья",

    "castaneda": "Карлос Кастанеда",

    "calvin": "Жан Кальвин",

    "blavatsky": "Елена Блаватская",

    "baal_shem_tov": "Бааль Шем Тов",

    "augustine": "Августин Аврелий",

    "atisha": "Атиша",

    "aquinas": "Фома Аквинский",

    "al_ghazali": "Аль-Газали",

    "akiva": "Рабби Акива",

    "abraham_isaac_kook": "Авраам Исаак Кук",

    "zhuangzi": "Чжуан-цзы",

    "zarathushtra": "Заратуштра",

    "teresa": "Тереза Авильская",

    "shankara": "Шанкара",

    "sergey_chernov": "Сергей Чернов (Doctor Che)",

    "rumi": "Руми",

    "ramanuja": "Рамануджа",

    "nasreddin": "Насреддин (Ходжа Насреддин)",

    "nanak": "Нанак",

    "nagarjuna": "Нагарджуна",

    "milarepa": "Миларепа",

    "mahavira": "Махавира",

    "laozi": "Лао-цзы",

    "koan": "Коан",

    "jesus": "Иисус Христос (исторический)",

    "dalai_lama": "Далай-лама",

    "confucius": "Конфуций",

    "buddha": "Будда (Сиддхартха Гаутама)",

    "bonhoeffer": "Дитрих Бонхёффер",

    "abhinavagupta": "Абхинавагупта",

    "muhammad": "Мухаммад",
    "freyja": "Фрейя",
    "west_african": "Западная Африка",
    "slavic": "Славяне",
    "mesoamerican": "Мезоамерика",
    "indian": "Индия",
    "east_asian": "Восточная Азия",
    "crossrefs": "Боги, которые совпадают",
    "heroes": "Герои",
    "heracles": "Геракл",
    "gilgamesh": "Гильгамеш",
    "odysseus": "Одиссей",
    "cuchulainn": "Кухулин",
    "ilya_muromets": "Илья Муромец",
    "rama": "Рама",
    "arjuna": "Арджуна",
    "prophets": "Пророки",
    "abraham": "Авраам",
    "moses": "Моисей",
    "elijah": "Илия",
    "isaiah": "Исайя",
    "john_baptist": "Иоанн Креститель",
    "pantheons": "Пантеоны и боги",
    "greek": "Греческий пантеон",
    "zeus": "Зевс",
    "hera": "Гера",
    "athena": "Афина",
    "apollo": "Аполлон",
    "artemis": "Артемида",
    "aphrodite": "Афродита",
    "ares": "Арес",
    "hephaestus": "Гефест",
    "hermes": "Гермес",
    "demeter": "Деметра",
    "dionysus": "Дионис",
    "poseidon": "Посейдон",
    "hades": "Аид",
    "persephone": "Персефона",
    "jupiter": "Юпитер",
    "mars": "Марс",
    "venus": "Венера",
    "minerva": "Минерва",
    "juno": "Юнона",
    "odin": "Один",
    "thor": "Тор",
    "freya": "Фрейя",
    "loki": "Локи",
    "tyr": "Тюр",
    "baldr": "Бальдр",
    "hel": "Хель",
    "ra": "Ра",
    "osiris": "Осирис",
    "isis": "Исида",
    "horus": "Гор",
    "anubis": "Анубис",
    "set": "Сет",
    "ishtar": "Иштар",
    "marduk": "Мардук",
    "shamash": "Шамаш",
    "ea": "Эа",
    "tammuz": "Таммуз",
    "enlil": "Энлиль",
    "perun": "Перун",
    "veles": "Велес",
    "mokosh": "Мокошь",
    "indra": "Индра",
    "agni": "Агни",
    "varuna": "Варуна",
    "vishnu": "Вишну",
    "shiva": "Шива",
    "krishna": "Кришна",
    "durga": "Дурга",
    "kali": "Кали",
    "saraswati": "Сарасвати",
    "lakshmi": "Лакшми",
    "ahura_mazda": "Ахура Мазда",
    "mithra": "Митра",
    "anahita": "Анахита",
    "angra_mainyu": "Ангра-Майнью",
    "jade_emperor": "Нефритовый император",
    "guanyin": "Гуаньинь",
    "amaterasu": "Аматэрасу",
    "susanoo": "Сусаноо",
    "izanami_izanagi": "Идзанами и Идзанаги",
    "quetzalcoatl": "Кецалькоатль",
    "tezcatlipoca": "Тескатлипока",
    "huitzilopochtli": "Уицилопочтли",
    "eshu": "Эшу",
    "oshun": "Ошун",
    "shango": "Шанго",
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
        "Линия Каширы": "02_world/dharmic/hinduism/shaivism/kashirsky_shaivism/line_kashira/line_kashira",
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
        "Палама": "07_mysticism/christian/hesychasm/hesychasm",
        "Рёйсбрук": "07_mysticism/christian/ruusbroec/ruusbroec",
        "Иоанн Креста": "09_ref/persons/john_cross/john_cross",
        "Догэн": "09_ref/persons/dogen/dogen",
        "Хакуин": "09_ref/persons/hakuin/hakuin",
        "Аттар": "09_ref/persons/attar/attar",
        "Тилопа": "09_ref/persons/tilopa/tilopa",
        "Наропа": "09_ref/persons/tilopa/tilopa",
        "Рамакришна": "09_ref/persons/ramakrishna/ramakrishna",
        "Вивекананда": "09_ref/persons/vivekananda/vivekananda",
        "Гампопа": "09_ref/persons/tilopa/tilopa",
        "Марпа": "09_ref/persons/tilopa/tilopa",
        "Кумбха": "09_ref/persons/ramakrishna/ramakrishna",
        "Тереза": "09_ref/persons/teresa",
        "Мадхьямака": "02_world/dharmic/buddhism/mahayana/mahayana",
        "Зевс": "10_pantheons/greek/zeus/zeus",
        "Гера": "10_pantheons/greek/hera/hera",
        "Афина": "10_pantheons/greek/athena/athena",
        "Аполлон": "10_pantheons/greek/apollo/apollo",
        "Артемида": "10_pantheons/greek/artemis/artemis",
        "Афродита": "10_pantheons/greek/aphrodite/aphrodite",
        "Арес": "10_pantheons/greek/ares/ares",
        "Гефест": "10_pantheons/greek/hephaestus/hephaestus",
        "Гермес": "10_pantheons/greek/hermes/hermes",
        "Деметра": "10_pantheons/greek/demeter/demeter",
        "Дионис": "10_pantheons/greek/dionysus/dionysus",
        "Посейдон": "10_pantheons/greek/poseidon/poseidon",
        "Аид": "10_pantheons/greek/hades/hades",
        "Персефона": "10_pantheons/greek/persephone/persephone",
        "Юпитер": "10_pantheons/roman/jupiter/jupiter",
        "Марс": "10_pantheons/roman/mars/mars",
        "Венера": "10_pantheons/roman/venus/venus",
        "Минерва": "10_pantheons/roman/minerva/minerva",
        "Юнона": "10_pantheons/roman/juno/juno",
        "Один": "10_pantheons/norse/odin/odin",
        "Тор": "10_pantheons/norse/thor/thor",
        "Фрейя": "10_pantheons/norse/freyja/freyja",
        "Локи": "10_pantheons/norse/loki/loki",
        "Тюр": "10_pantheons/norse/tyr/tyr",
        "Бальдр": "10_pantheons/norse/baldr/baldr",
        "Ра": "10_pantheons/egyptian/ra/ra",
        "Осирис": "10_pantheons/egyptian/osiris/osiris",
        "Исида": "10_pantheons/egyptian/isis/isis",
        "Гор": "10_pantheons/egyptian/horus/horus",
        "Анубис": "10_pantheons/egyptian/anubis/anubis",
        "Иштар": "10_pantheons/mesopotamian/ishtar/ishtar",
        "Мардук": "10_pantheons/mesopotamian/marduk/marduk",
        "Шамаш": "10_pantheons/mesopotamian/shamash/shamash",
        "Таммуз": "10_pantheons/mesopotamian/tammuz/tammuz",
        "Перун": "10_pantheons/slavic/perun/perun",
        "Велес": "10_pantheons/slavic/veles/veles",
        "Мокошь": "10_pantheons/slavic/mokosh/mokosh",
        "Индра": "10_pantheons/indian/indra/indra",
        "Варуна": "10_pantheons/indian/varuna/varuna",
        "Вишну": "10_pantheons/indian/vishnu/vishnu",
        "Шива": "10_pantheons/indian/shiva/shiva",
        "Кришна": "10_pantheons/indian/krishna/krishna",
        "Дурга": "10_pantheons/indian/durga/durga",
        "Кали": "10_pantheons/indian/kali/kali",
        "Лакшми": "10_pantheons/indian/lakshmi/lakshmi",
        "Ахура Мазда": "10_pantheons/iranian/ahura_mazda/ahura_mazda",
        "Митра": "10_pantheons/iranian/mithra/mithra",
        "Ангра-Майнью": "10_pantheons/iranian/angra_mainyu/angra_mainyu",
        "Нефритовый император": "10_pantheons/east_asian/jade_emperor/jade_emperor",
        "Гуаньинь": "10_pantheons/east_asian/guanyin/guanyin",
        "Аматэрасу": "10_pantheons/east_asian/amaterasu/amaterasu",
        "Сусаноо": "10_pantheons/east_asian/susanoo/susanoo",
        "Кецалькоатль": "10_pantheons/mesoamerican/quetzalcoatl/quetzalcoatl",
        "Тескатлипока": "10_pantheons/mesoamerican/tezcatlipoca/tezcatlipoca",
        "Уицилопочтли": "10_pantheons/mesoamerican/huitzilopochtli/huitzilopochtli",
        "Эшу": "10_pantheons/west_african/eshu/eshu",
        "Ошун": "10_pantheons/west_african/oshun/oshun",
        "Шанго": "10_pantheons/west_african/shango/shango",
        "Прометей": "10_pantheons/greek/prometheus/prometheus",
        "Диоскуры": "10_pantheons/greek/dioscuri/dioscuri",
        "Пан": "10_pantheons/greek/pan/pan",
        "Геката": "10_pantheons/greek/hecate/hecate",
        "Гелиос": "10_pantheons/greek/helios/helios",
        "Гестия": "10_pantheons/greek/hestia/hestia",
        "Геракл": "10_pantheons/heroes/heracles/heracles",
        "Геркулес": "10_pantheons/heroes/heracles/heracles",
        "Гильгамеш": "10_pantheons/heroes/gilgamesh/gilgamesh",
        "Одиссей": "10_pantheons/heroes/odysseus/odysseus",
        "Кухулин": "10_pantheons/heroes/cuchulainn/cuchulainn",
        "Илья Муромец": "10_pantheons/heroes/ilya_muromets/ilya_muromets",
        "Рама": "10_pantheons/heroes/rama/rama",
        "Арджуна": "10_pantheons/heroes/arjuna/arjuna",
        "Авраам": "10_pantheons/prophets/abraham/abraham",
        "Моисей": "10_pantheons/prophets/moses/moses",
        "Илия": "10_pantheons/prophets/elijah/elijah",
        "Исайя": "10_pantheons/prophets/isaiah/isaiah",
        "Иоанн Креститель": "10_pantheons/prophets/john_baptist/john_baptist",
        "Мухаммад": "10_pantheons/prophets/muhammad/muhammad",
        "Яма": "10_pantheons/indian/yama/yama",
        "Кама": "10_pantheons/indian/kama/kama",
        "Тара": "10_pantheons/indian/tara/tara",
        "Ганга": "10_pantheons/indian/ganga/ganga",
        "Кубера": "10_pantheons/indian/kubera/kubera",
        "Ваю": "10_pantheons/indian/vayu/vayu",
        "Сома": "10_pantheons/indian/soma/soma",
        "Иггдрасиль": "10_pantheons/norse/yggdrasil/yggdrasil",
        "Видар": "10_pantheons/norse/vidar/vidar",
        "Улль": "10_pantheons/norse/ullr/ullr",
        "Форсети": "10_pantheons/norse/forseti/forseti",
        "Браги": "10_pantheons/norse/bragi/bragi",
        "Сурья": "10_pantheons/indian/surya/surya",
        "Радха": "10_pantheons/indian/radha/radha",
        "Сита": "10_pantheons/indian/sita/sita",
        "Хануман": "10_pantheons/indian/hanuman/hanuman",
        "Ганеша": "10_pantheons/indian/ganesha/ganesha",
        "Парвати": "10_pantheons/indian/parvati/parvati",
        "Брахма": "10_pantheons/indian/brahma/brahma",
        "Морена": "10_pantheons/slavic/morena/morena",
        "Ярило": "10_pantheons/slavic/yarilo/yarilo",
        "Сварог": "10_pantheons/slavic/svarog/svarog",
        "Стрибог": "10_pantheons/slavic/stribog/stribog",
        "Хорс": "10_pantheons/slavic/hors/hors",
        "Дажьбог": "10_pantheons/slavic/dazhbog/dazhbog",
        "Рагнарёк": "10_pantheons/norse/ragnarok/ragnarok",
        "Валькирии": "10_pantheons/norse/valkyries/valkyries",
        "Норны": "10_pantheons/norse/norns/norns",
        "Сиф": "10_pantheons/norse/sif/sif",
        "Идунн": "10_pantheons/norse/idunn/idunn",
        "Хеймдалль": "10_pantheons/norse/heimdallr/heimdallr",
        "Фрейр": "10_pantheons/norse/freyr/freyr",


            "Мейстер Экхарт": "09_ref/persons/meister_eckhart/meister_eckhart",
        "Экхарт": "09_ref/persons/meister_eckhart/meister_eckhart",
        "Несторий": "09_ref/persons/nestorius/nestorius",
        "Феодор Мопсуестийский": "09_ref/persons/theodore_of_mopsuestia/theodore_of_mopsuestia",
        "Ефрем Сирин": "09_ref/persons/ephrem_syrian/ephrem_syrian",
        "Мартин Лютер": "09_ref/persons/luther/luther",
        "Лютер": "09_ref/persons/luther/luther",
        "Жан Кальвин": "09_ref/persons/calvin/calvin",
        "Кальвин": "09_ref/persons/calvin/calvin",
        "Джордж Фокс": "09_ref/persons/george_fox/george_fox",
        "Августин": "09_ref/persons/augustine/augustine",
        "Ориген": "09_ref/persons/origen/origen",
        "Фома Аквинский": "09_ref/persons/aquinas/aquinas",
        "Рабия": "09_ref/persons/rabia/rabia",
        "аль-Газали": "09_ref/persons/al_ghazali/al_ghazali",
        "Газали": "09_ref/persons/al_ghazali/al_ghazali",
        "Хафиз": "09_ref/persons/hafiz/hafiz",
        "Мадхва": "09_ref/persons/madhva/madhva",
        "Чайтанья": "09_ref/persons/chaitanya/chaitanya",
        "Падмасамбхава": "09_ref/persons/padmasambhava/padmasambhava",
        "Гуру Ринпоче": "09_ref/persons/padmasambhava/padmasambhava",
        "Цонкапа": "09_ref/persons/tsongkhapa/tsongkhapa",
        "Атиша": "09_ref/persons/atisha/atisha",
        "Бааль Шем Тов": "09_ref/persons/baal_shem_tov/baal_shem_tov",
        "Маймонид": "09_ref/persons/maimonides/maimonides",
        "Рамбам": "09_ref/persons/maimonides/maimonides",
        "Акива": "09_ref/persons/akiva/akiva",
        "Авраам Исаак Кук": "09_ref/persons/abraham_isaac_kook/abraham_isaac_kook",
        "Мэн-цзы": "09_ref/persons/mencius/mencius",
        "Сюнь-цзы": "09_ref/persons/xunzi/xunzi",
        "Мани": "09_ref/persons/mani/mani",
        "Елена Блаватская": "09_ref/persons/blavatsky/blavatsky",
        "Блаватская": "09_ref/persons/blavatsky/blavatsky",
        "Рудольф Штайнер": "09_ref/persons/steiner/steiner",
        "Штайнер": "09_ref/persons/steiner/steiner",
        "Кроули": "09_ref/persons/crowley/crowley",
        "Гурджиев": "09_ref/persons/gurdjieff/gurdjieff",
        "Успенский": "09_ref/persons/ouspensky/ouspensky",
        "Кастанеда": "09_ref/persons/castaneda/castaneda",
        "Уильям Джеймс": "09_ref/persons/william_james/william_james",
        "Джеймс": "09_ref/persons/william_james/william_james",
        "Юнг": "09_ref/persons/jung/jung",
        "Элиаде": "09_ref/persons/eliade/eliade",
        "Сергий Радонежский": "09_ref/persons/sergiy_radonezhsky/sergiy_radonezhsky",
        "Серафим Саровский": "09_ref/persons/serafim_sarovsky/serafim_sarovsky",
        "Гампопа": "09_ref/persons/tilopa/tilopa",
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
_autolink_rel = [""]

def autolink(text, current_rel=None):
    """Первое вхождение каждого названия -> плейсхолдер-ссылка."""
    _autolink_rel[0] = ("../" * (current_rel.count("/") + 1)) if current_rel else ""
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

def restore_links(html_text, rel=""):
    def rep(m):
        url, label = LINK_PH.get(int(m.group(1)), ("#", "?"))
        return '<a href="%sru/%s.html">%s</a>' % (rel, url, html.escape(label))
    return re.sub('\x00(\\d+)\x00', rep, html_text)

# ---------------------------------------------------------------- markdown --
def md_inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = restore_links(text, _autolink_rel[0])
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
<meta property="og:image" content="https://oaker.github.io/veroteka/assets/img/og-cover.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{rel}assets/favicon.svg">
<link rel="alternate" type="application/rss+xml" title="Веротека — новые статьи" href="https://oaker.github.io/veroteka/feed.xml">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="{rel}index.html">Веротека</a>
  <nav class="topnav">
    <a href="{rel}az.html">А-Я</a>
    <a href="{rel}tags.html">Теги</a>
    <a href="{rel}axis.html">Ось</a>
    <a href="{rel}quiz.html">Познание себя</a>
    <a href="{rel}ru/09_ref/about/about.html">О проекте</a>
  </nav>
  <input id="searchbox" type="search" placeholder="Поиск..." autocomplete="off">
  <button id="themeToggle" title="Тёмная/светлая тема">&#127769;</button>
</header>
<div id="searchresults"></div>
<main class="{maincls}">
{content}
</main>
<footer>
<p>(c) 2026 Sergey Che - Веротека - Контент CC BY 4.0</p>
</footer>
<script src="{rel}assets/app.js"></script>
</body>
</html>"""

def render_page(title, content_html, lang="ru", rel="", maincls=""):
    return PAGE_TMPL.format(title=html.escape(title), content=content_html, lang=lang, rel=rel, maincls=maincls)

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
    yr = meta.get("year")
    if yr:
        parts.append('<span class="badge year-badge">год: %s</span>' % html.escape(yr))
    img = meta.get("image")
    if img:
        rel_prefix = ("../" * (a["rel_url"].count("/") + 1)) if a["rel_url"] else ""
        parts.append('<figure class="article-img"><img src="%sassets/img/%s" alt="" loading="lazy"></figure>' % (rel_prefix, html.escape(img.rsplit("/", 1)[-1])))
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
    body_md = a["body"]
    marker = "## См. также"
    if marker in body_md:
        main_md, see_md = body_md.split(marker, 1)
        see_md = marker + see_md
    else:
        main_md, see_md = body_md, ""
    parts.append(md_to_html(main_md))
    if see_md:
        parts.append(md_to_html(autolink(see_md, a["rel_url"])))
    editor = meta.get("editor")
    if editor:
        parts.append(
            '<div class="editor-box"><div class="who">От редакции</div>%s</div>'
            % md_to_html(editor)
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
    img_src = ROOT / "assets" / "img"
    if img_src.exists():
        shutil.copytree(img_src, SITE / "assets" / "img", dirs_exist_ok=True)
    fav_src = ROOT / "assets" / "favicon.svg"
    if fav_src.exists():
        shutil.copyfile(fav_src, SITE / "assets" / "favicon.svg")
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

    # index.html — аккордеонная главная (v2)
    TOP_SECTIONS = ["01_basics","10_pantheons","02_world","03_ancient","04_national","05_nrd","06_esoteric","07_mysticism","08_skeptic","09_ref"]
    p = []
    p.append('<section class="hero-min">')
    p.append('<h1>Веротека</h1>')
    p.append('<p>Энциклопедия религий, конфессий, сект и эзотерических учений: %d статей, нейтральный текст и отдельный слой «позиция редактора».</p>' % len(ru))
    p.append('<div class="quick">'
             '<a href="search-index.json" onclick="document.getElementById(\'searchbox\').focus();return false;">🔎 Поиск</a>'
             ''
             '<a href="axis.html">🧭 Ось взгляда</a>'
             '<a href="ru/09_ref/timeline/timeline.html">📜 Хронология</a>'
             '<a href="ru/09_ref/about/about.html">О проекте</a>'
             '<a href="ru/09_ref/about/author.html">Об авторе</a>'
             '</div>')
    p.append('</section>')
    # карточка «Познание себя» (тест)
    p.append('<a class="quiz-cta" href="quiz.html">'
             '<span class="quiz-cta-l">'
             '<span class="quiz-cta-t">Познание себя</span>'
             '<span class="quiz-cta-d">Адаптивный тест из 10–14 вопросов: ответь — и Веротека подберёт традицию, которая тебе ближе, со ссылкой на статью о ней.</span>'
             '</span>'
             '<span class="quiz-cta-btn">Пройти →</span>'
             '</a>')

    def node_link(s):
        """Ссылка на узел: свой хаб, иначе первая статья в поддереве."""
        hub = s + "/" + s.split("/")[-1]
        if ("ru", hub) in existing:
            return "ru/" + hub + ".html"
        def first_in(sub):
            arts = sorted(node_articles.get(sub, []), key=lambda t: t["title"])
            if arts:
                return arts[0]
            for ch in children.get(sub, []):
                r = first_in(ch)
                if r:
                    return r
            return None
        f = first_in(s)
        return ("ru/" + f["rel_url"] + ".html") if f else None

    # порядок разделов + открытый по умолчанию
    OPEN_SEC = "02_world"
    for sec in TOP_SECTIONS:
        if sec not in all_dirs:
            continue
        n = subtree_count.get(sec, 0)
        label = crumb_label(sec)
        is_open = " open" if sec == OPEN_SEC else ""
        p.append('<details class="acc"%s><summary><span class="chev">›</span>'
                 '<span class="ttl">%s</span><span class="n">%d</span></summary>'
                 '<div class="acc-body"><ul>' % (is_open, html.escape(label), n))
        # прямые статьи раздела
        for a in sorted(node_articles.get(sec, []), key=lambda t: t["title"]):
            p.append('<li><a href="ru/%s.html">%s<span class="cnt">статья</span></a></li>' % (a["rel_url"], html.escape(a["title"])))
        # подразделы второго уровня — рекурсивно до 3-го уровня
        def render_sub(s, depth=2):
            sn = subtree_count.get(s, 0)
            sub_label = crumb_label(s.split("/")[-1])
            link = node_link(s)
            kids = sorted(children.get(s, []))
            direct = sorted(node_articles.get(s, []), key=lambda t: t["title"])
            if depth > 5 or (not kids and not direct):
                if link:
                    p.append('<li class="lv%d"><a href="%s">%s<span class="cnt">%d</span></a></li>' % (depth, link, html.escape(sub_label), sn))
                return
            # Одиночная статья без подпапок: рисуем статью напрямую — без «задвоения» узел→статья
            if not kids and len(direct) == 1:
                a = direct[0]
                p.append('<li class="lv%d"><a href="ru/%s.html">%s<span class="cnt">статья</span></a></li>' % (depth, a["rel_url"], html.escape(a["title"])))
                return
            open_attr = " open" if depth == 2 else ""
            p.append('<li class="lv%d sub-node"><details class="sub-acc"%s><summary><span class="chev2">›</span><span class="ttl2">%s</span><span class="cnt">%d</span></summary><ul>' % (depth, open_attr, html.escape(sub_label), sn))
            for a in direct:
                p.append('<li class="lv3"><a href="ru/%s.html">%s<span class="cnt">статья</span></a></li>' % (a["rel_url"], html.escape(a["title"])))
            for k in kids:
                render_sub(k, depth + 1)
            # «Весь раздел →» не нужен, если hub-статья уже показана выше (не задваивать вход)
            if link and link.split('/')[-1].replace('.html', '') not in [a["rel_url"].split('/')[-1] for a in direct]:
                p.append('<li class="lv3"><a href="%s"><b>Весь раздел →</b></a></li>' % link)
            p.append('</ul></details></li>')

        for s in sorted(children.get(sec, [])):
            render_sub(s, 2)
        hub = sec + "/" + sec
        # «Весь раздел →» на верхнем уровне: рисуем только если hub-статья ещё не показана
        hub_shown = bool(node_articles.get(sec))
        if ("ru", hub) in existing and not hub_shown:
            p.append('<li><a href="ru/%s.html"><b>Весь раздел →</b><span class="cnt"></span></a></li>' % hub)
        p.append('</ul></div></details>')

    p.append('<nav class="landing-foot">')
    for lbl, href in [("Алфавитный указатель","az.html"),("Теги","tags.html"),("Ось взгляда","axis.html"),("О проекте","ru/09_ref/about/about.html"),("Об авторе","ru/09_ref/about/author.html")]:
        p.append('<a href="%s">%s</a>' % (href, lbl))
        p.append('</nav>')

    home = render_page("Главная", "\n".join(p))
    (SITE / "index.html").write_text(home, encoding="utf-8")

    # az.html
    az_html = []
    az_head = ('<div class="page-head"><h1>Алфавитный указатель</h1>'
               '<p>Все статьи «Веротеки» по алфавиту.</p></div>'
               '<div class="page-quick">'
               '<a href="tags.html">Теги</a>'
               '<a href="axis.html">Ось взгляда</a>'
               '<a href="ru/09_ref/about/about.html">О проекте</a>'
               '<a href="index.html">На главную</a>'
               '</div>')
    for letter in sorted(az):
        az_html.append("<h2>%s <span class=\"n\">(%d)</span></h2><ul>" % (html.escape(letter), len(az[letter])))
        for a in sorted(az[letter], key=lambda x: x["title"].lower()):
            az_html.append('<li><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        az_html.append("</ul>")
    if not az:
        az_html.append("<p>Статьи пока не написаны.</p>")
    (SITE / "az.html").write_text(render_page("Алфавитный указатель", az_head + '<div class="az-cols">' + "\n".join(az_html) + '</div>', maincls="wide"), encoding="utf-8")

    # tags.html
    tags_html = []
    tags_head = ('<div class="page-head"><h1>Теги</h1>'
                 '<p>Сквозная навигация по темам: тип практики, семья традиций, статус.</p></div>'
                 '<div class="page-quick">'
                 '<a href="az.html">Алфавитный указатель</a>'
                 '<a href="axis.html">Ось взгляда</a>'
                 '<a href="ru/09_ref/about/about.html">О проекте</a>'
                 '<a href="index.html">На главную</a>'
                 '</div>')
    for t in sorted(tags):
        tags_html.append("<h2>%s</h2><ul>" % html.escape(t))
        for a in tags[t]:
            tags_html.append('<li><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        tags_html.append("</ul>")
    if not tags:
        tags_html.append("<p>Теги пока не проставлены.</p>")
    (SITE / "tags.html").write_text(render_page("Теги", tags_head + '<div class="tag-sec">' + "\n".join(tags_html) + '</div>', maincls="wide"), encoding="utf-8")

    # axis.html
    axis_groups = {"dvaita": [], "advaita": [], "sunyata": []}
    for a in ru:
        ax = (a["meta"].get("axis") or "").strip().lower()
        if ax in axis_groups:
            axis_groups[ax].append(a)
    ax_html = []
    for key, title, desc in (
        ("dvaita", "Двайта — дуальность", "Творец и творение различны: теизм авраамических традиций, шайва-сиддханта, зороастризм."),
        ("advaita", "Адвайта — недвойственность", "Единое есть всё: адвайта-веданта, кашмирский шиваизм, недуальные линии, Каширский шиваизм."),
        ("sunyata", "Пустотные", "Ни двайта, ни адвайта: шуньята, апофатика, традиции без метафизики Единого."),
    ):
        ax_html.append('<div class="pole"><h2>%s</h2><p>%s</p><ul>' % (html.escape(title), html.escape(desc)))
        if axis_groups[key]:
            for a in sorted(axis_groups[key], key=lambda x: x["title"]):
                ax_html.append('<li><a href="ru/%s.html">%s</a></li>' % (a["rel_url"], html.escape(a["title"])))
        else:
            ax_html.append('<li class="planned">статьи скоро</li>')
        ax_html.append("</ul></div>")
    axis_head = ('<div class="page-head"><h1>Ось взгляда</h1>'
                 '<p>Сквозная классификация «Веротеки»: не «кто старее», а как традиция отвечает на вопрос о Едином и мире.</p></div>'
                 '<div class="page-quick">'
                 '<a href="az.html">Алфавитный указатель</a>'
                 '<a href="ru/01_basics/typology/axis_typology.html">Методология оси</a>'
                 '<a href="ru/09_ref/about/about.html">О проекте</a>'
                 '<a href="index.html">На главную</a>'
                 '</div>')
    (SITE / "axis.html").write_text(render_page("Ось взгляда", axis_head + '<div class="axis-grid">' + "\n".join(ax_html) + '</div>', maincls="wide"), encoding="utf-8")

    # ---------- видимость: sitemap / robots / 404 / feed ----------
    SITE_URL = "https://oaker.github.io/veroteka/"
    # sitemap.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm.append('<url><loc>%s</loc><priority>1.0</priority></url>' % SITE_URL)
    for p in ("quiz.html", "az.html", "tags.html", "axis.html"):
        sm.append('<url><loc>%s%s</loc><priority>0.8</priority></url>' % (SITE_URL, p))
    for a in articles:
        if a["lang"] == "ru":
            sm.append('<url><loc>%sru/%s.html</loc></url>' % (SITE_URL, a["rel_url"]))
    sm.append('</urlset>')
    (SITE / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

    # robots.txt
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % SITE_URL, encoding="utf-8")

    # 404.html — навигация домой
    notfound_links = "".join(
        '<a class="nf-link" href="%s">%s</a>' % (h, t) for h, t in [
            ("index.html", "Главная"), ("quiz.html", "Познание себя"),
            ("az.html", "Алфавитный указатель"), ("tags.html", "Теги"), ("axis.html", "Ось взгляда"),
        ])
    nf = render_page("Страница не найдена",
        '<div class="nf-wrap"><h1>404 — страница не найдена</h1>'
        '<p>Такой статьи нет или она переехала. Начните с навигации:</p>'
        '<div class="nf-links">%s</div></div>'
        '<style>.nf-wrap{max-width:560px;margin:8vh auto 0;text-align:center;padding:0 16px}'
        '.nf-wrap h1{font-size:1.6rem;margin:0 0 12px}.nf-wrap p{color:var(--muted)}'
        '.nf-links{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:22px}'
        '.nf-link{border:1px solid var(--border);border-radius:12px;padding:10px 16px;text-decoration:none;color:var(--fg);background:var(--card)}'
        '.nf-link:hover{border-color:var(--accent);color:var(--accent)}</style>' % notfound_links)
    (SITE / "404.html").write_text(nf, encoding="utf-8")

    # feed.xml — RSS по 30 последним (по полю year строкой — сортируем обратным алфавитом года)
    def _yr(a):
        y = a.get("meta", {}).get("year", "")
        m = re.search(r"(\d{3,4})", str(y))
        return int(m.group(1)) if m else 0
    latest = sorted([a for a in articles if a["lang"] == "ru"], key=_yr, reverse=True)[:30]
    feed = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<rss version="2.0"><channel>',
            '<title>Веротека — новые статьи</title>',
            '<link>%s</link>' % SITE_URL,
            '<description>Энциклопедия религий, конфессий, сект и эзотерических учений</description>',
            '<language>ru</language>']
    for a in latest:
        excerpt = re.sub(r"<[^>]+>", "", a.get("excerpt", ""))[:300]
        feed.append('<item><title>%s</title><link>%sru/%s.html</link><description>%s</description></item>' % (
            html.escape(a["title"]), SITE_URL, a["rel_url"], html.escape(excerpt)))
    feed.append('</channel></rss>')
    (SITE / "feed.xml").write_text("\n".join(feed), encoding="utf-8")
    print("visibility: sitemap/robots/404/feed OK")

    # поисковый индекс
    (SITE / "search-index.json").write_text(
        json.dumps(index_entries, ensure_ascii=False, indent=1), encoding="utf-8")


    # quiz «Познание себя» — чистая версия агента (quiz_agent.html), публикую как есть
    _qa = BUILD / "quiz_agent.html"
    if _qa.exists():
        shutil.copyfile(_qa, SITE / "quiz.html")
        print("quiz.html: agent version copied")
    else:
        print("quiz skip: build/quiz_agent.html missing")
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
.article-img { margin:.6rem 0 1rem; border:1px solid var(--border); border-radius:10px; overflow:hidden; background:var(--card); }
.article-img img { width:100%; display:block; }
.books { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:.7rem 1rem; margin:1.2rem 0; font-size:.93rem; }
.books ul { margin:.3rem 0 0; padding-left:1.2rem; }
.books li { margin-bottom:.15rem; }
.books h2 { font-size:1rem; margin:0 0 .4rem; }
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

/* ---------- landing / hero ---------- */
.hero-min { padding:2.2rem 0 1.3rem; }
.hero-min h1 { font-size:clamp(1.95rem,4.2vw,2.7rem); margin:0 0 .5rem; letter-spacing:-.03em; }
.hero-min p { color:var(--muted); max-width:600px; margin:0 0 1.1rem; }
.quick { display:flex; gap:.5rem; flex-wrap:wrap; margin-bottom:1.7rem; }
.quick a { font-size:.88rem; padding:.45rem .9rem; border:1px solid var(--border); border-radius:10px; text-decoration:none; color:var(--fg); background:var(--card); transition:.15s; }
.quick a:hover { border-color:var(--accent); color:var(--accent); }

/* ---------- accordion (home) ---------- */
.acc { border:1px solid var(--border); border-radius:16px; background:var(--card); overflow:hidden; margin:0 0 .7rem; }
.acc > summary { display:flex; align-items:center; gap:.6rem; padding:.95rem 1.15rem; cursor:pointer; font-weight:700; font-size:1.03rem; list-style:none; }
.acc > summary::-webkit-details-marker { display:none; }
.acc > summary::marker { content:""; }
.acc > summary .chev { color:var(--muted); font-size:.9rem; transition:transform .18s; flex:0 0 auto; }
.acc > summary .ttl { flex:1; min-width:0; }
.acc > summary .n { font-size:.8rem; font-weight:500; color:var(--muted); background:var(--bg); border:1px solid var(--border); border-radius:999px; padding:.1rem .62rem; flex:0 0 auto; }
.acc[open] > summary .chev { transform:rotate(90deg); }
.acc[open] > summary { border-bottom:1px solid var(--border); }
.acc-body { padding:.4rem .6rem .85rem; }
.acc-body ul { list-style:none; margin:0; padding:0; }
.acc-body li a { display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:.5rem .65rem; border-radius:9px; text-decoration:none; color:var(--fg); font-size:.95rem; }
.acc-body li a:hover { background:var(--accent-soft); color:var(--accent); }
.acc-body li a .cnt { color:var(--muted); font-size:.78rem; flex:0 0 auto; }
.acc-body li a b { font-weight:650; }
.acc-body li + li { margin-top:.05rem; }


/* nested accordion (3rd level on home) */
.acc-body .sub-acc { border:0; margin:0; background:transparent; }
.acc-body .sub-acc > summary { display:flex; align-items:center; gap:.45rem; padding:.42rem .6rem; border-radius:9px; list-style:none; font-weight:600; font-size:.94rem; cursor:pointer; }
.acc-body .sub-acc > summary::-webkit-details-marker { display:none; }
.acc-body .sub-acc > summary::marker { content:""; }
.acc-body .sub-acc:hover > summary { background:var(--accent-soft); }
.acc-body .sub-acc[open] > summary { color:var(--accent); }
.chev2 { color:var(--muted); font-size:.85rem; transition:transform .18s; flex:0 0 auto; }
.sub-acc[open] > summary .chev2 { transform:rotate(90deg); }
.ttl2 { flex:1; min-width:0; }
.acc-body .sub-acc ul { padding-left:.9rem; }
.acc-body li.lv3 a { padding:.34rem .6rem; font-size:.9rem; color:var(--muted); }
.acc-body li.lv3 a:hover { color:var(--accent); background:var(--accent-soft); }
.sub-node { list-style:none; }

/* ---------- quiz CTA card ---------- */
.quiz-cta { display:flex; align-items:center; justify-content:space-between; gap:14px; margin:1.1rem 0 .4rem; padding:16px 20px; background:linear-gradient(135deg,rgba(79,70,229,.06),rgba(139,92,246,.08)); border:1px solid rgba(79,70,229,.22); border-radius:16px; text-decoration:none; transition:box-shadow .15s, transform .1s; }
.quiz-cta:hover { box-shadow:0 3px 14px rgba(79,70,229,.14); transform:translateY(-1px); }
.quiz-cta-t { display:block; font-weight:700; font-size:1.06rem; color:var(--fg); }
.quiz-cta-d { display:block; color:var(--muted); font-size:.9rem; margin-top:3px; max-width:520px; }
.quiz-cta-btn { flex-shrink:0; background:linear-gradient(135deg,#4f46e5,#8b5cf6); color:#fff; border-radius:12px; padding:10px 18px; font-size:.95rem; font-weight:600; }
@media (max-width:640px){ .quiz-cta{ flex-direction:column; align-items:flex-start; padding:14px 16px; } .quiz-cta-btn{ width:100%; text-align:center; } }

/* ---------- landing footer ---------- */
.landing-foot { display:flex; flex-wrap:wrap; gap:.5rem 1.4rem; justify-content:center; margin:2.4rem 0 0; padding-top:1.3rem; border-top:1px solid var(--border); }
.landing-foot a { color:var(--muted); font-size:.87rem; text-decoration:none; }
.landing-foot a:hover { color:var(--accent); }

/* ---------- topbar spacing (не сливаются) ---------- */
.topnav { display:flex; gap:.25rem; flex-wrap:wrap; }
.topnav a { padding:.4rem .75rem; border-radius:9px; color:var(--muted); text-decoration:none; font-size:.92rem; }
.topnav a:hover { color:var(--fg); background:var(--accent-soft); }
#themeToggle { border:1px solid var(--border); background:var(--card); border-radius:10px; width:38px; height:38px; cursor:pointer; flex:0 0 auto; }
#searchbox:focus { border-color:var(--accent); outline:none; }

/* ---------- year badge ---------- */
.badge.year-badge { color:#b8860b; border-color:#b8860b; }

/* ---------- tree ---------- */
#treewrap details > summary { list-style:none; }
#treewrap details > summary::-webkit-details-marker { display:none; }
#treewrap ul { list-style:none; padding-left:1.15rem; margin:.1rem 0; }
#treewrap ul ul { border-left:1px solid var(--border); padding-left:.9rem; }
#treewrap li.art a { text-decoration:none; color:var(--fg); display:inline-block; padding:.12rem 0; }
#treewrap li.art a:hover { color:var(--accent); text-decoration:underline; text-decoration-color:var(--accent); }
#treewrap .planned { color:var(--muted); }
#treewrap .count { color:var(--muted); font-size:.8rem; }
#treewrap summary { padding:.28rem 0; }
#treewrap summary:hover { color:var(--accent); }

/* ---------- mobile ---------- */
@media (max-width:640px) {
  body { font-size:16px; }
  .topbar { padding:.5rem .8rem; gap:.5rem; }
  .brand { font-size:1.05rem; }
  #searchbox { order:3; flex:1 1 100%; max-width:none; padding:.6rem .9rem; }
  .topnav { order:2; flex:1 1 auto; overflow-x:auto; white-space:nowrap; gap:.15rem; scrollbar-width:none; }
  .topnav::-webkit-scrollbar { display:none; }
  .topnav a { flex:0 0 auto; padding:.45rem .65rem; font-size:.9rem; }
  #themeToggle { order:1; width:36px; height:36px; }
  main { padding:1rem .9rem 3rem; }
  .hero-min { padding:1.3rem 0 .9rem; }
  .quick { gap:.4rem; margin-bottom:1.2rem; }
  .quick a { flex:1 1 calc(50% - .4rem); text-align:center; min-height:44px; display:flex; align-items:center; justify-content:center; font-size:.86rem; }
  .acc > summary { padding:.9rem .95rem; font-size:1rem; min-height:52px; }
  .acc-body { padding:.3rem .4rem .7rem; }
  .acc-body li a { padding:.7rem .6rem; min-height:46px; }
  .landing-foot { gap:.45rem 1rem; margin-top:1.8rem; }
  .landing-foot a { font-size:.84rem; padding:.3rem 0; }
  h1 { font-size:1.7rem; }
  .article-img { border-radius:12px; }
  .plain-box, .editor-box { padding:.7rem .85rem; }
  #searchresults { padding:.4rem .9rem; }
}
@media (max-width:380px) {
  .quick a { flex:1 1 100%; }
}


/* ---------- service pages ---------- */
.page-head h1 { font-size:clamp(1.75rem,3.5vw,2.25rem); margin:0 0 .45rem; letter-spacing:-.02em; }
.page-head p { color:var(--muted); margin:0 0 1rem; }
.page-quick { display:flex; gap:.5rem; flex-wrap:wrap; margin:0 0 1.5rem; }
.page-quick a { font-size:.86rem; padding:.42rem .85rem; border:1px solid var(--border); border-radius:10px; text-decoration:none; color:var(--fg); background:var(--card); }
.page-quick a:hover { border-color:var(--accent); color:var(--accent); }
main.wide { max-width:1000px; }

/* А-Я: колонки */
.az-cols { columns:2; column-gap:2.4rem; }
@media (min-width:960px){ .az-cols { columns:3; } }
.az-cols h2 { font-size:1.02rem; margin:1rem 0 .3rem; break-after:avoid; color:var(--accent); }
.az-cols ul { list-style:none; margin:0; padding:0; }
.az-cols li a { text-decoration:none; color:var(--fg); }
.az-cols li a:hover { color:var(--accent); }

/* Теги: чипы + списки */
.tag-sec h2 { display:inline-block; font-size:.9rem; font-weight:650; color:var(--accent); background:var(--accent-soft); border:1px solid var(--border); border-radius:999px; padding:.22rem .75rem; margin:.7rem .2rem .3rem 0; }
.tag-sec ul { list-style:none; margin:.15rem 0 1.1rem; padding:0; display:flex; flex-wrap:wrap; gap:.1rem 1rem; }
.tag-sec ul li a { font-size:.92rem; color:var(--fg); text-decoration:none; }
.tag-sec ul li a:hover { color:var(--accent); }

/* Ось: карточки полюсов */
.axis-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(270px,1fr)); gap:14px; margin-top:1rem; }
.axis-grid .pole { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.15rem 1.25rem; box-shadow:var(--shadow); }
.axis-grid .pole h2 { font-size:1.06rem; margin:0 0 .35rem; }
.axis-grid .pole > p { color:var(--muted); font-size:.9rem; margin:.15rem 0 .8rem; }
.axis-grid ul { list-style:none; margin:0; padding:0; }
.axis-grid li a { color:var(--fg); text-decoration:none; display:block; padding:.26rem 0; font-size:.94rem; }
.axis-grid li a:hover { color:var(--accent); }
.axis-grid .planned { color:var(--muted); font-size:.9rem; }
.axis-grid .n { color:var(--muted); font-size:.78rem; }

@media (max-width:640px){
  .az-cols { columns:1; }
  .page-head h1 { font-size:1.6rem; }
}

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
// на мобиле: фокус в поиск мягко скроллит к верху
box && box.addEventListener('focus', () => { window.scrollTo({top:0, behavior:'smooth'}); });

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



