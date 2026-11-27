"""Check the public static site before publishing it."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1] / "dist"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.meta = []
        self.canonical = []
        self.headings = []
        self.title = ""
        self._capture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("a", "link") and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in ("img", "script") and attrs.get("src"):
            self.links.append(attrs["src"])
        if tag == "img":
            self.images.append(attrs)
        if tag == "meta":
            self.meta.append(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag in ("h1", "h2", "h3", "title"):
            self._capture = [tag, []]

    def handle_data(self, data):
        if self._capture:
            self._capture[1].append(data)

    def handle_endtag(self, tag):
        if self._capture and self._capture[0] == tag:
            value = " ".join("".join(self._capture[1]).split())
            if tag == "title":
                self.title = value
            else:
                self.headings.append((tag, value))
            self._capture = None


def main():
    pages = {}
    for file in sorted(ROOT.glob("*.html")):
        parser = Page()
        parser.feed(file.read_text(encoding="utf-8"))
        pages[file.name] = parser

    errors, warnings = [], []
    for name, page in pages.items():
        if not page.title:
            errors.append(f"{name}: missing title")
        if sum(tag == "h1" for tag, _ in page.headings) != 1:
            errors.append(f"{name}: expected one h1")
        if not any(meta.get("name") == "description" for meta in page.meta):
            errors.append(f"{name}: missing description")
        expected_url = f"https://essencetherapy.cn/{'' if name == 'index.html' else name}"
        if page.canonical != [expected_url]:
            errors.append(f"{name}: missing or incorrect canonical URL")
        og = {meta.get("property") for meta in page.meta}
        if not {"og:title", "og:description", "og:image"} <= og:
            warnings.append(f"{name}: incomplete social preview metadata")
        for image in page.images:
            if "alt" not in image:
                errors.append(f"{name}: image without alt: {image.get('src')}")
            if "width" not in image or "height" not in image:
                warnings.append(f"{name}: image without dimensions: {image.get('src')}")
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith(("mailto:", "tel:", "//")):
                continue
            target_name = unquote(url.path) or name
            target = ROOT / target_name.lstrip("/")
            if target_name.endswith("/"):
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{name}: broken local link: {link}")
            elif url.fragment and target.suffix == ".html":
                target_page = pages.get(target.name)
                if target_page and unquote(url.fragment) not in target_page.ids:
                    errors.append(f"{name}: missing anchor: {link}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for name in pages:
        if f"https://essencetherapy.cn/{name}" not in sitemap and name != "index.html":
            warnings.append(f"{name}: absent from sitemap")
    print(f"Pages: {len(pages)}; images: {sum(len(p.images) for p in pages.values())}")
    print(f"Errors: {len(errors)}; warnings: {len(warnings)}")
    for issue, count in Counter(warnings).most_common(30):
        print("WARN", issue, f"({count})" if count > 1 else "")
    for issue in errors:
        print("ERROR", issue)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
