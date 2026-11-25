"""Reject internal editorial notes from the visitor-facing site."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parent / "dist"
INTERNAL_NOTES = (
    "版本与书目说明",
    "封面与团队公开海报",
    "画面取自团队公开海报",
    "本站不提供图书下载",
    "这里先收录能核对来源的节点",
    "依据高校报道、出版记录和公开课程资料整理",
    "不冒称学员原话",
    "删去过期课程信息",
    "本站为方便阅读而编辑",
    "获准发布的原片将逐步",
    "尚未公开出版的教学资料",
    "目前掌握的是首届筑基班学习版",
    "仍在评估购买、转赠、有效期和成本",
    "首版目录",
    "公开授权待核",
)


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth:
            self.parts.append(data)


def main():
    errors = []
    for path in sorted(ROOT.rglob("*.html")):
        parser = VisibleText()
        parser.feed(path.read_text(encoding="utf-8"))
        text = " ".join(parser.parts)
        errors.extend(f"{path.relative_to(ROOT)}: {phrase}" for phrase in INTERNAL_NOTES if phrase in text)
    for filename, phrase in (
        ("reading.html", "情绪智能时代"),
        ("teacher.html", "情绪智能时代"),
        ("archive.html", "首届本性治疗筑基班"),
        ("archive.html", "情商培训师认证班"),
    ):
        if phrase not in (ROOT / filename).read_text(encoding="utf-8"):
            errors.append(f"{filename}: 缺少 {phrase}")
    if (ROOT / "members").exists():
        errors.append("members/: 官网会员板块应整体撤下")
    for path in sorted(ROOT.rglob("*.html")):
        if 'href="members/' in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)}: 仍有会员入口")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Public copy audit passed")


if __name__ == "__main__":
    main()
