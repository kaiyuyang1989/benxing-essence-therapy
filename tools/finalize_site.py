"""Write the sitemap and intrinsic image dimensions after page generation."""

import re
import subprocess
from functools import lru_cache
from html import unescape
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1] / "dist"
IMG = re.compile(r"<img\b[^>]*>")
SRC = re.compile(r'\bsrc="([^"]+)"')


@lru_cache(maxsize=None)
def dimensions(name):
    path = ROOT / name
    if not path.is_file():
        return None
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True, text=True, check=False,
    )
    width = re.search(r"pixelWidth: (\d+)", result.stdout)
    height = re.search(r"pixelHeight: (\d+)", result.stdout)
    return (width.group(1), height.group(1)) if width and height else None


def add_image_size(match):
    tag = match.group()
    source = SRC.search(tag)
    if not source or re.search(r"\b(?:width|height)=", tag) or "://" in source.group(1):
        return tag
    size = dimensions(unescape(source.group(1)).split("?", 1)[0])
    if not size:
        return tag
    return tag[:-1] + f' width="{size[0]}" height="{size[1]}">'


def main():
    pages = sorted(ROOT.glob("*.html"))
    for path in pages:
        text = path.read_text(encoding="utf-8")
        revised = IMG.sub(add_image_size, text)
        if revised != text:
            path.write_text(revised, encoding="utf-8")
    urls = ["https://essencetherapy.cn/"] + [
        f"https://essencetherapy.cn/{path.name}"
        for path in pages if path.name != "index.html"
    ]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{escape(url)}</loc></url>\n" for url in urls)
    sitemap += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Finalized {len(pages)} pages and {len(urls)} sitemap URLs")


if __name__ == "__main__":
    main()
