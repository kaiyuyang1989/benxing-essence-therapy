"""Build static English and French editions of every public page."""

import json
import re
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape as html_escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from bs4 import BeautifulSoup, NavigableString


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CACHE_PATH = ROOT / "content" / "i18n-cache.json"
HAN = re.compile(r"[\u3400-\u9fff]")
SITE = "https://essencetherapy.cn"
GLOSSARY = {
    "北京大学深圳研究生院": ("Peking University Shenzhen Graduate School", "École doctorale de Shenzhen de l'Université de Pékin"),
    "青岛精神分析协会": ("Qingdao Psychoanalytic Association", "Association de psychanalyse de Qingdao"),
    "石家庄龅牙兔": ("Shijiazhuang Baoyatu", "Baoyatu de Shijiazhuang"),
    "郑州心能量": ("Zhengzhou Xin Neng Liang", "Xin Neng Liang de Zhengzhou"),
    "向光里·心空间": ("Xiangguangli Heart Space", "Espace du cœur Xiangguangli"),
    "北京英酷百兴心理": ("Beijing Yingku Baixing Psychology", "Yingku Baixing Psychologie, Pékin"),
    "本性治疗一阶": ("Essence Therapy Level I", "Thérapie du Moi essentiel · Niveau I"),
    "本性治疗二阶": ("Essence Therapy Level II", "Thérapie du Moi essentiel · Niveau II"),
    "《内在父母与内在小孩的拥抱》": ("Embracing the Inner Parent and Child (《内在父母与内在小孩的拥抱》)", "L'étreinte du parent et de l'enfant intérieurs (《内在父母与内在小孩的拥抱》)"),
    "《情商教练手册》": ("The Emotional Intelligence Coach's Handbook (《情商教练手册》)", "Le manuel du coach en intelligence émotionnelle (《情商教练手册》)"),
    "《儿童情商教育》": ("Emotional Intelligence Education for Children (《儿童情商教育》)", "L'éducation émotionnelle des enfants (《儿童情商教育》)"),
    "《情绪智能时代》": ("The Age of Emotional Intelligence (《情绪智能时代》)", "L'ère de l'intelligence émotionnelle (《情绪智能时代》)"),
    "《育儿先育己》": ("Parent Yourself Before Raising Children (《育儿先育己》)", "Se construire avant d'élever ses enfants (《育儿先育己》)"),
    "《由心咨询》": ("Counseling from the Heart (《由心咨询》)", "La thérapie du Moi essentiel (《由心咨询》)"),
    "《梦的真相》": ("The Truth of Dreams (《梦的真相》)", "L'Appel du rêve (《梦的真相》)"),
    "世界图书出版公司": ("World Publishing Corporation", "World Publishing Corporation"),
    "奇毓教育科技（杭州）有限公司": ("Qiyu Education Technology (Hangzhou) Co., Ltd.", "Qiyu Education Technology (Hangzhou) Co., Ltd."),
    "扎根本性": ("Rooted in Essence", "Aux racines de l'Essence"),
    "本性治疗": ("Essence Therapy", "thérapie du Moi essentiel"),
    "情商教育": ("emotional intelligence education", "éducation à l'intelligence émotionnelle"),
    "年龄回溯": ("age regression", "régression en âge"),
    "梦工作": ("dreamwork", "travail sur les rêves"),
    "倪男奇": ("Ni Nanqi", "Ni Nanqi"),
    "米杉": ("Michel Claeys", "Michel Claeys"),
    "小扎": ("Xiao Zha", "Xiao Zha"),
    "心能量": ("Xin Neng Liang", "Xin Neng Liang"),
    "龅牙兔": ("Baoyatu", "Baoyatu"),
    "向光里": ("Xiangguangli", "Xiangguangli"),
    "英酷百兴": ("Yingku Baixing", "Yingku Baixing"),
    "本性": ("Essence", "Essence"),
    "情商": ("emotional intelligence", "intelligence émotionnelle"),
}
GLOSSARY_ITEMS = list(enumerate(sorted(GLOSSARY.items(), key=lambda item: len(item[0]), reverse=True)))
FR_HEADINGS = {
    "ABOUT MICHEL": "À PROPOS DE MICHEL", "THE JOURNEY": "LE PARCOURS", "WATCH & LISTEN": "VOIR ET ÉCOUTER",
    "BOOKS & WRITING": "LIVRES ET ÉCRITURE", "PEOPLE & PLACES": "PERSONNES ET LIEUX",
    "PUBLIC CONVERSATIONS": "ENTRETIENS PUBLICS", "OUR PHILOSOPHY": "NOTRE PHILOSOPHIE",
    "THE BOOKS": "LES LIVRES", "COURSES & PRACTICE": "FORMATIONS ET PRATIQUE",
    "THE APPROACH": "L'APPROCHE", "IN PRACTICE": "EN PRATIQUE", "FROM OUR ARCHIVE": "DE NOS ARCHIVES",
    "KEEP EXPLORING": "POURSUIVRE L'EXPLORATION", "SPRING 2027": "PRINTEMPS 2027",
    "SELECTED ARTICLES": "ARTICLES CHOISIS", "MORE IN CHINESE": "EN CHINOIS",
    "CONTACT": "CONTACT", "BOOK EXCERPTS": "EXTRAITS DE LIVRES",
    "SPRING 2027 / COURSE": "PRINTEMPS 2027 / FORMATION", "PEOPLE & PARTNERS": "PERSONNES ET PARTENAIRES",
    "MEET MICHEL CLAEYS": "RENCONTRER MICHEL CLAEYS", "TRANSLATION & PRACTICE": "TRADUCTION ET PRATIQUE",
    "PARTNERS IN PRACTICE": "PARTENAIRES DE TERRAIN", "ON THE JOURNEY": "SUR LE PARCOURS",
    "THE INNER WORK": "LE TRAVAIL INTÉRIEUR", "SEVEN PRINCIPLES": "SEPT PRINCIPES",
    "A CONTINUING PRACTICE": "UNE PRATIQUE CONTINUE", "IN HIS WORDS": "DANS SES MOTS",
    "MORE TO EXPLORE": "POUR ALLER PLUS LOIN", "THE JOURNEY IN CHINA": "LE PARCOURS EN CHINE",
}
OVERRIDES = {
    "en": {
        "首页": "Home", "课程": "Courses", "著作": "Books", "文章": "Articles", "专题": "Explore",
        "教学历程": "Teaching Journey", "影像": "Media", "理念": "Philosophy", "合作": "Partners", "联系": "Contact",
        "认识米杉": "Michel Claeys", "认识倪男奇": "Ni Nanqi", "米杉著作": "Books by Michel Claeys",
        "米杉中文著作": "Michel Claeys: Books in Chinese", "在中国的教学历程": "A Teaching Journey in China",
        "合作网络": "Partners in China", "课程与学习路径": "Courses and Learning Paths",
        "公众号文章选读": "Selected Articles", "经典文章": "Selected Articles",
        "影像与声音": "Film & Audio", "米杉的影像与声音": "Michel Claeys on Film & Audio",
        "学习与带领的理念": "Our Teaching Philosophy", "我们的理念": "Our Philosophy",
        "本性治疗的方法与原则": "Essence Therapy: Method and Principles",
        "让方法进入中文课堂": "Bringing the Work into Chinese Classrooms",
        "课程在不同城市相遇": "A Shared Journey Across Cities",
        "中文出版著作": "Books Published in Chinese",
        "从早期著作，到今天的六部书": "From Early Works to Six Books Today",
        "2027 春季课程": "Spring 2027 Courses", "本性治疗：": "Essence Therapy:",
        "从身体感受开始": "Begin with Embodied Experience",
        "本性治疗，": "Essence Therapy,", "以身体感受为入口。": "beginning with embodied experience.",
        "梦的真相": "The Truth of Dreams", "由心咨询": "Counseling from the Heart",
        "儿童情商教育": "Emotional Intelligence Education for Children",
        "情商教练手册": "The Emotional Intelligence Coach's Handbook",
        "育儿先育己": "Parent Yourself Before Raising Children",
        "内在父母与内在小孩的拥抱": "Embracing the Inner Parent and Child",
        "扎根本性｜本性治疗 · 米杉课程": "Rooted in Essence | Essence Therapy & Michel Claeys Courses",
        "法语 · 外部平台": "French · external platform",
    },
    "fr": {
        "首页": "Accueil", "课程": "Formations", "著作": "Livres", "文章": "Articles", "专题": "Explorer",
        "教学历程": "Parcours pédagogique", "影像": "Médias", "理念": "Philosophie", "合作": "Partenaires", "联系": "Contact",
        "认识米杉": "Michel Claeys", "认识倪男奇": "Ni Nanqi", "米杉著作": "Livres de Michel Claeys",
        "米杉中文著作": "Les livres de Michel Claeys en chinois", "在中国的教学历程": "Un parcours d'enseignement en Chine",
        "合作网络": "Partenaires en Chine", "课程与学习路径": "Formations et parcours d'apprentissage",
        "公众号文章选读": "Articles choisis", "经典文章": "Articles choisis",
        "影像与声音": "Vidéos et audio", "米杉的影像与声音": "Michel Claeys en images et en voix",
        "学习与带领的理念": "Notre philosophie de l'apprentissage", "我们的理念": "Notre philosophie",
        "本性治疗的方法与原则": "Thérapie du Moi essentiel : méthode et principes",
        "让方法进入中文课堂": "Faire vivre la méthode dans les cours en chinois",
        "课程在不同城市相遇": "Un parcours partagé entre les villes",
        "中文出版著作": "Livres publiés en chinois",
        "从早期著作，到今天的六部书": "Des premiers écrits aux six livres d'aujourd'hui",
        "2027 春季课程": "Formations du printemps 2027", "本性治疗：": "Thérapie du Moi essentiel :",
        "从身体感受开始": "Commencer par le ressenti corporel",
        "本性治疗，": "La thérapie du Moi essentiel,", "以身体感受为入口。": "à partir du ressenti corporel.",
        "梦的真相": "L'Appel du rêve", "由心咨询": "La thérapie du Moi essentiel",
        "儿童情商教育": "L'éducation émotionnelle des enfants",
        "情商教练手册": "Le manuel du coach en intelligence émotionnelle",
        "育儿先育己": "Se construire avant d'élever ses enfants",
        "内在父母与内在小孩的拥抱": "L'étreinte du parent et de l'enfant intérieurs",
        "扎根本性｜本性治疗 · 米杉课程": "Aux racines de l'Essence | Thérapie du Moi essentiel et formations de Michel Claeys",
        "法语 · 外部平台": "Français · plateforme externe",
    },
}


from i18n_reviewed import REVIEWED
for reviewed_language, reviewed_copy in REVIEWED.items():
    OVERRIDES[reviewed_language].update(reviewed_copy)
from i18n_eq2026 import TRANSLATIONS as EQ2026_TRANSLATIONS
for source, (english, french) in EQ2026_TRANSLATIONS.items():
    OVERRIDES["en"][source] = english
    OVERRIDES["fr"][source] = french


def protect(value):
    for index, (source, _) in GLOSSARY_ITEMS:
        value = value.replace(source, "⟪T%03d⟫" % index)
    return value


def unprotect(value, lang):
    for index, (_, translations) in GLOSSARY_ITEMS:
        value = re.sub(r"⟪\s*T%03d\s*⟫" % index, lambda _: translations[0 if lang == "en" else 1], value)
    return value


def curl_translate(texts, lang):
    if not texts:
        return []
    prepared = [protect(value) for value in texts]
    query = "\n".join(value + "\n⟪S%04d⟫" % i for i, value in enumerate(prepared[:-1])) + ("\n" if len(prepared) > 1 else "") + prepared[-1]
    command = ["curl", "--fail", "--max-time", "35", "-sS", "-A", "Mozilla/5.0", "-G", "--data-urlencode", "client=gtx", "--data-urlencode", "sl=zh-CN", "--data-urlencode", "tl=" + lang, "--data-urlencode", "dt=t", "--data-urlencode", "q=" + query, "https://translate.google.com/translate_a/single"]
    last_error = None
    for attempt in range(5):
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                translated = "".join(part[0] or "" for part in data[0])
                split = re.split(r"\s*⟪S\d{4}⟫\s*", translated)
                if len(split) == len(texts):
                    return [unprotect(value.strip(), lang) for value in split]
                last_error = "segment mismatch: expected %d, received %d" % (len(texts), len(split))
            except (ValueError, TypeError, IndexError) as exc:
                last_error = str(exc)
        else:
            last_error = result.stderr.strip()[:160]
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("Translation failed for %s (%s): %s" % (lang, len(texts), last_error))


def batches(values, limit=1600):
    batch = []
    size = 0
    for value in values:
        cost = len(protect(value)) + 18
        if batch and size + cost > limit:
            yield batch
            batch = []
            size = 0
        batch.append(value)
        size += cost
    if batch:
        yield batch


def page_strings(soup):
    for node in soup.find_all(string=True):
        if node.parent.name not in ("script", "style") and HAN.search(str(node)):
            yield str(node).strip()
    for tag in soup.find_all(True):
        for attr in ("alt", "aria-label", "title", "placeholder", "data-title"):
            value = tag.get(attr)
            if isinstance(value, str) and HAN.search(value):
                yield value.strip()
        if tag.name == "meta" and tag.get("name") == "description" or tag.name == "meta" and tag.get("property") in ("og:title", "og:description", "og:site_name"):
            value = tag.get("content", "")
            if HAN.search(value):
                yield value.strip()


def collect():
    pages = {file.name: BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser") for file in sorted(DIST.glob("*.html"))}
    # The previous build writes the language switcher and hreflang links back
    # into the Chinese source pages. Remove those generated nodes before
    # rebuilding, so repeated releases do not accumulate duplicate controls.
    for soup in pages.values():
        for switcher in soup.select(".language-switcher"):
            switcher.decompose()
        for alternate in soup.select('link[rel="alternate"][hreflang]'):
            alternate.decompose()
    values = set()
    for soup in pages.values():
        values.update(page_strings(soup))
    media = json.loads((DIST / "media.json").read_text(encoding="utf-8"))
    for item in media.get("items", []):
        for key in ("title", "description", "source", "originalTitle", "language"):
            value = item.get(key, "")
            if HAN.search(value):
                values.add(value.strip())
    return pages, media, sorted(values)


def fill_cache(values):
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {"en": {}, "fr": {}}
    lock = threading.Lock()
    for lang in ("en", "fr"):
        missing = [value for value in values if value not in cache[lang] and value not in OVERRIDES[lang]]
        work = list(batches(missing))
        print("%s: %d new strings in %d batches" % (lang, len(missing), len(work)), flush=True)
        if not work:
            continue
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {pool.submit(curl_translate, batch, lang): batch for batch in work}
            for done in as_completed(futures):
                original = futures[done]
                translated = done.result()
                with lock:
                    cache[lang].update(zip(original, translated))
                    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    return cache


def translated(value, lang, cache):
    lead = value[:len(value) - len(value.lstrip())]
    tail = value[len(value.rstrip()):]
    core = value.strip()
    override = OVERRIDES[lang].get(core)
    if not override and core.endswith("｜扎根本性"):
        prefix = core[:-len("｜扎根本性")]
        if prefix in OVERRIDES[lang]:
            override = OVERRIDES[lang][prefix] + " | " + GLOSSARY["扎根本性"][0 if lang == "en" else 1]
    if override:
        return lead + override + tail
    if not HAN.search(value):
        return FR_HEADINGS.get(core, value) if lang == "fr" else value
    result = cache[lang][core].replace("｜", " | ").replace("：", ": ")
    result = result.replace("second order", "Level II").replace("deuxième commande", "niveau II")
    for name in ("Michel Claeys", "Ni Nanqi", "Xin Neng Liang", "Baoyatu", "Xiangguangli", "Yingku Baixing"):
        result = re.sub(r"(?<=[A-Za-zÀ-ÿ])(?=" + re.escape(name) + r")", " ", result)
        result = re.sub(re.escape(name) + r"(?=[A-Za-zÀ-ÿ])", name + " ", result)
    result = re.sub(r"\s{2,}", " ", result)
    return lead + result + tail


def url_for(name, lang):
    return SITE + (("/" if name == "index.html" else "/" + name) if lang == "zh-CN" else ("/" + lang + "/" if name == "index.html" else "/" + lang + "/" + name))


def decorate(soup, name, lang):
    soup.html["lang"] = lang
    head = soup.head
    for link in head.select('link[rel="canonical"]'):
        link["href"] = url_for(name, lang)
    for code in ("zh-CN", "en", "fr"):
        link = soup.new_tag("link", rel="alternate", hreflang=code, href=url_for(name, code))
        head.append(link)
    head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=url_for(name, "zh-CN")))
    for meta in head.select('meta[property="og:url"]'):
        meta["content"] = url_for(name, lang)
    for meta in head.select('meta[property="og:locale"]'):
        meta["content"] = "en_US" if lang == "en" else "fr_FR" if lang == "fr" else "zh_CN"
    nav_label = {"zh-CN": "选择语言", "en": "Select language", "fr": "Choisir la langue"}[lang]
    switcher = soup.new_tag("nav", attrs={"class": "language-switcher", "aria-label": nav_label})
    for code, label in (("zh-CN", "中"), ("en", "EN"), ("fr", "FR")):
        anchor = soup.new_tag("a", href=("/" if name == "index.html" else "/" + name) if code == "zh-CN" else ("/" + code + "/" if name == "index.html" else "/" + code + "/" + name), lang=code)
        anchor.string = label
        if code == lang:
            anchor["aria-current"] = "page"
        switcher.append(anchor)
    header = soup.select_one(".header-inner")
    if header:
        header.append(switcher)


def localize_page(soup, name, lang, cache):
    for node in list(soup.find_all(string=True)):
        if node.parent.name in ("script", "style"):
            continue
        text = str(node)
        if HAN.search(text) or (lang == "fr" and text.strip() in FR_HEADINGS):
            node.replace_with(NavigableString(translated(text, lang, cache)))
    for tag in soup.find_all(True):
        for attr in ("alt", "aria-label", "title", "placeholder", "data-title"):
            value = tag.get(attr)
            if isinstance(value, str) and HAN.search(value):
                tag[attr] = translated(value, lang, cache)
        if tag.name == "meta" and (tag.get("name") == "description" or tag.get("property") in ("og:title", "og:description", "og:site_name")):
            value = tag.get("content", "")
            if HAN.search(value):
                tag["content"] = translated(value, lang, cache)
        for attr in ("href", "src", "data-poster"):
            value = tag.get(attr)
            if not isinstance(value, str) or not value or value.startswith(("#", "https:", "http:", "mailto:", "tel:", "/")):
                continue
            if value.startswith("assets/"):
                tag[attr] = "../" + value
            elif value in ("styles.css", "extra.css", "app.js"):
                tag[attr] = "../" + value
            elif value.split("#", 1)[0].endswith(".html"):
                path, sep, fragment = value.partition("#")
                tag[attr] = "/" + lang + ("/" if path == "index.html" else "/" + path) + (sep + fragment if sep else "")
    if name == "reading.html":
        author_heading = soup.select_one("h2")
        if author_heading:
            author_heading.clear()
            author_heading.string = "Michel Claeys Bouuaert"
    decorate(soup, name, lang)
    output = DIST / lang / name
    output.parent.mkdir(exist_ok=True)
    output.write_text(str(soup), encoding="utf-8")


def write_sitemap(page_names):
    urls = []
    for name in page_names:
        for lang in ("zh-CN", "en", "fr"):
            loc = url_for(name, lang)
            alternates = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (code, xml_escape(url_for(name, code))) for code in ("zh-CN", "en", "fr"))
            urls.append("  <url><loc>%s</loc>%s</url>" % (xml_escape(loc), alternates))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n"
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main():
    pages, media, values = collect()
    cache = fill_cache(values)
    for lang in ("en", "fr"):
        for name, source in pages.items():
            localize_page(BeautifulSoup(str(source), "html.parser"), name, lang, cache)
        localized_media = json.loads(json.dumps(media, ensure_ascii=False))
        for item in localized_media.get("items", []):
            for key in ("title", "description", "source", "originalTitle", "language"):
                if key in item and HAN.search(item[key]):
                    item[key] = translated(item[key], lang, cache)
        (DIST / lang / "media.json").write_text(json.dumps(localized_media, ensure_ascii=False, indent=2), encoding="utf-8")
    for name, soup in pages.items():
        decorate(soup, name, "zh-CN")
        rendered = re.sub(r"(?i)^<!doctype html>\n+", "<!DOCTYPE html>\n", str(soup))
        (DIST / name).write_text(rendered, encoding="utf-8")
    write_sitemap(sorted(pages))
    print("Built %d trilingual pages" % (len(pages) * 3))


if __name__ == "__main__":
    main()
