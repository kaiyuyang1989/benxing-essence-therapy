"""Render the verified media list into each public language edition."""

import json
from html import escape
from pathlib import Path
from urllib.parse import urlparse


DIST = Path(__file__).resolve().parents[1] / "dist"
START_TAG = '<div class="media-grid" id="media-list">'
START_MARKER = '<!-- media-cards:start -->'
END_MARKER = '<!-- media-cards:end -->'
ACTION = {
    "zh": {"video": "观看原节目", "audio": "收听原节目", "empty": "公开节目正在整理。"},
    "en": {"video": "Watch the original", "audio": "Listen to the original", "empty": "Public programmes are being curated."},
    "fr": {"video": "Voir la vidéo originale", "audio": "Écouter l’émission originale", "empty": "Les programmes publics sont en cours de sélection."},
}


def card(item, lang):
    url = str(item.get("url", ""))
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"Media URL must be absolute HTTPS: {url!r}")
    kind = item.get("kind")
    if kind not in ("video", "audio"):
        raise ValueError(f"Unsupported media kind: {kind!r}")
    field = lambda key: escape(str(item.get(key, "")), quote=True)
    label = ACTION[lang][kind]
    icon = "▷" if kind == "video" else "♫"
    return (
        f'<a class="media-card {kind}" href="{field("url")}" target="_blank" rel="noopener noreferrer">'
        f'<div class="media-kind"><span>{kind.upper()} / {field("language")}</span>'
        f'<strong aria-hidden="true">{icon}</strong></div>'
        f'<h3>{field("title")}</h3><p class="original-title">{field("originalTitle")}</p>'
        f'<p>{field("description")}</p><div class="media-card-footer">'
        f'<span>{field("source")}</span><b>{escape(label)}</b></div></a>'
    )


def render(lang):
    directory = DIST if lang == "zh" else DIST / lang
    page_path = directory / "watch.html"
    media_path = directory / "media.json"
    page = page_path.read_text(encoding="utf-8")
    items = json.loads(media_path.read_text(encoding="utf-8")).get("items", [])
    cards = "".join(card(item, lang) for item in items)
    content = cards or f'<p class="media-loading">{ACTION[lang]["empty"]}</p>'
    block = f'{START_MARKER}{content}{END_MARKER}'
    if START_MARKER in page:
        start = page.index(START_MARKER)
        end = page.index(END_MARKER, start) + len(END_MARKER)
        revised = page[:start] + block + page[end:]
    else:
        start = page.index(START_TAG) + len(START_TAG)
        end = page.index('</div>', start)
        following = end + len('</div>')
        if page.startswith('<noscript>', following):
            following = page.index('</noscript>', following) + len('</noscript>')
        revised = page[:start] + block + '</div>' + page[following:]
    page_path.write_text(revised, encoding="utf-8")
    print(f"{lang}: rendered {len(items)} public media cards")


if __name__ == "__main__":
    for language in ("zh", "en", "fr"):
        render(language)
