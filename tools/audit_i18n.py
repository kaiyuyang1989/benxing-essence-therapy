"""Check all locale routes, alternate tags, assets and page anchors."""

from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1] / "dist"
BASE = "https://essencetherapy.cn"
LANGUAGES = ("zh-CN", "en", "fr")


def url(name, lang):
    if lang == "zh-CN":
        return BASE + ("/" if name == "index.html" else "/" + name)
    return BASE + ("/" + lang + "/" if name == "index.html" else "/" + lang + "/" + name)


def main():
    names = {page.name for page in ROOT.glob("*.html")}
    errors = []
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for lang in LANGUAGES:
        directory = ROOT if lang == "zh-CN" else ROOT / lang
        found = {page.name for page in directory.glob("*.html")}
        if found != names:
            errors.append("%s pages differ: %s" % (lang, sorted(names ^ found)))
        for name in sorted(names & found):
            file = directory / name
            soup = BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")
            label = "%s/%s" % (lang, name)
            if soup.html.get("lang") != lang:
                errors.append(label + ": wrong html lang")
            if not soup.title or not soup.title.get_text(strip=True):
                errors.append(label + ": missing title")
            if len(soup.find_all("h1")) != 1:
                errors.append(label + ": expected one h1")
            canonical = soup.select_one('link[rel="canonical"]')
            if not canonical or canonical.get("href") != url(name, lang):
                errors.append(label + ": wrong canonical")
            alternates = {tag.get("hreflang"): tag.get("href") for tag in soup.select('link[rel="alternate"][hreflang]')}
            if any(alternates.get(code) != url(name, code) for code in LANGUAGES):
                errors.append(label + ": missing language alternate")
            switcher = soup.select_one(".language-switcher")
            if not switcher or len(switcher.select("a")) != 3:
                errors.append(label + ": missing language selector")
            ids = [tag["id"] for tag in soup.select("[id]")]
            if len(ids) != len(set(ids)):
                errors.append(label + ": duplicate anchor")
            for tag in soup.select("[href],[src],[data-poster]"):
                for attr in ("href", "src", "data-poster"):
                    raw = tag.get(attr)
                    if not raw:
                        continue
                    parsed = urlsplit(raw)
                    if parsed.scheme or parsed.netloc or raw.startswith(("mailto:", "tel:", "//")):
                        continue
                    path = unquote(parsed.path)
                    target = ROOT / path.lstrip("/") if path.startswith("/") else file.parent / path if path else file
                    if path.endswith("/") or target.is_dir():
                        target /= "index.html"
                    if not target.is_file():
                        errors.append(label + ": broken " + raw)
                    elif parsed.fragment and target.suffix == ".html":
                        target_soup = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
                        if not target_soup.find(id=unquote(parsed.fragment)):
                            errors.append(label + ": missing anchor " + raw)
            if url(name, lang) not in sitemap:
                errors.append(label + ": absent from sitemap")
    print("Locales: %s; pages per locale: %d; errors: %d" % (", ".join(LANGUAGES), len(names), len(errors)))
    for error in errors[:80]:
        print("ERROR", error)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
