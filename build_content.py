"""Generate the static editorial pages and book details from reviewed content."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BOOKS = json.loads((ROOT / "content/books.json").read_text(encoding="utf-8"))
E = html.escape


def header(active=""):
    items = [
        ("approach.html", "本性治疗"),
        ("courses.html", "课程"),
        ("teacher.html", "米杉"),
        ("nanni.html", "倪男奇"),
        ("reading.html", "著作"),
        ("insights.html", "文章"),
        ("guide.html", "专题"),
        ("archive.html", "教学历程"),
        ("partners.html", "合作"),
        ("watch.html", "影像"),
        ("voices.html", "理念"),
    ]
    links = "".join(
        f'<a href="{url}"{(" aria-current=" + chr(34) + "page" + chr(34)) if active == url else ""}>{name}</a>'
        for url, name in items
    )
    return f'''<a class="skip-link" href="#main">跳到正文</a>
<header class="site-header"><div class="header-inner container">
<a class="brand" href="index.html"><img src="assets/essence-logo-web.png" alt="" width="86" height="48"><span class="brand-name">扎根本性<span class="brand-en">ESSENCE THERAPY</span></span></a>
<button class="menu-toggle" type="button" aria-label="打开导航" aria-controls="site-nav" aria-expanded="false"><span></span><span></span><span></span></button>
<nav class="site-nav" id="site-nav" aria-label="主导航">{links}<a class="nav-contact" href="index.html#contact">联系 / Contact</a></nav>
</div></header>'''


def footer():
    return '''<footer class="site-footer"><div class="container footer-inner"><div><strong>扎根本性</strong><p>本性治疗、梦工作与社会情感学习。 / Essence Therapy, Dream Work & SEL.</p><div class="footer-links"><a href="index.html">首页</a><a href="approach.html">本性治疗</a><a href="teacher.html">米杉</a><a href="nanni.html">倪男奇</a><a href="reading.html">著作</a><a href="guide.html">专题阅读</a><a href="archive.html">教学历程</a><a href="partners.html">合作网络</a><a href="watch.html">影像</a><a href="index.html#contact">联系</a></div></div><div class="footer-meta"><span>奇毓教育科技（杭州）有限公司</span><a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">浙ICP备2026078107号-1</a><span>© <span id="year">2026</span> 扎根本性</span></div></div></footer>'''


def page(title, description, path, body, active=None, og_image="assets/mountain-dawn-web.jpg", structured_data=None):
    canonical = f"https://essencetherapy.cn/{path}"
    schema_json = json.dumps(structured_data, ensure_ascii=False).replace("</", "<\\/") if structured_data else ""
    schema = f'<script type="application/ld+json">{schema_json}</script>' if schema_json else ""
    document = f'''<!doctype html><html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#173d34">
<meta name="description" content="{E(description)}"><link rel="canonical" href="{canonical}"><title>{E(title)}｜扎根本性</title>
<meta property="og:type" content="website"><meta property="og:site_name" content="扎根本性"><meta property="og:locale" content="zh_CN"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{E(title)}｜扎根本性"><meta property="og:description" content="{E(description)}"><meta property="og:image" content="https://essencetherapy.cn/{E(og_image)}">
{schema}<link rel="icon" type="image/png" href="assets/essence-logo-web.png"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="extra.css"><script defer src="app.js"></script></head>
<body id="top">{header(active or path)}<main id="main">{body}</main>{footer()}</body></html>'''
    (DIST / path).write_text(document, encoding="utf-8")


def hero(label, title, lead, crumb):
    return f'''<section class="page-hero nature-page"><div class="container page-hero-inner"><p class="breadcrumb"><a href="index.html">首页</a><span aria-hidden="true">/</span> {E(crumb)}</p><p class="eyebrow"><span class="eyebrow-line"></span>{E(label)}</p><h1>{title}</h1><p class="page-lead">{lead}</p></div></section>'''


def section_head(label, title, intro=""):
    return f'''<div class="section-heading"><div><p class="eyebrow"><span class="eyebrow-line"></span>{E(label)}</p><h2>{title}</h2></div>{f'<p class="section-intro">{intro}</p>' if intro else ''}</div>'''


def book_card(book, index):
    cover = '<div class="poster-book-cover" role="img" aria-label="《内在父母与内在小孩的拥抱》封面"></div>' if book["image"] == "poster-crop" else f'<img src="assets/books/{E(book["image"])}" alt="《{E(book["title"])}》封面" loading="lazy" class="{E(book["image_class"])}">'
    return f'''<article class="catalog-card reveal" id="{E(book['slug'])}"><a class="catalog-cover" href="book-{E(book['slug'])}.html" aria-label="查看《{E(book['title'])}》详情">{cover}</a><div class="catalog-copy"><p class="micro-en">{index:02d} / {E(book['topic'])}</p><h3><a href="book-{E(book['slug'])}.html">{E(book['title'])}</a></h3><p class="catalog-subtitle">{E(book['subtitle'])}</p><p>{E(book['summary'])}</p><div class="catalog-meta"><span>{E(book['year'])} · {E(book['publisher'])}</span><a class="text-link" href="book-{E(book['slug'])}.html">阅读详情 ↗</a></div></div></article>'''


def bookshop_code():
    return '''<div class="bookshop-panel"><div class="bookshop-copy"><p class="eyebrow"><span class="eyebrow-line"></span>WECHAT BOOKSHOP</p><h3>选购米杉著作</h3><p>微信扫一扫，进入世界图书出版公司小店选购米杉著作。</p><p class="bookshop-mobile-hint">手机浏览可长按图片识别。</p></div><a class="bookshop-code" href="assets/wechat-books-shop.jpg" target="_blank" rel="noopener" aria-label="打开微信小店购书码原图"><img src="assets/wechat-books-shop.jpg" alt="世界图书出版公司微信小店购书码" loading="lazy"></a></div>'''


def publication_journey():
    stages = [
        ("2000年代", "情商课堂与早期著作", "米杉在中国写作的情商课堂著作，早期曾以《应该补上的一课》出版。它后来持续修订，发展为今天读到的《情商教练手册》。", "book-eq-coach.html", "读《情商教练手册》"),
        ("2010", "梦的真相", "《梦的真相》早期中文版出版。书中以梦者的亲身经验为起点，讨论记录梦、理解梦境和开展内在工作。", "book-dream.html", "走进梦工作"),
        ("2013", "内在空间与儿童情商教育", "《内在父母与内在小孩的拥抱》和《儿童情商教育》分别从个人成长与儿童教育出发，拓宽了这些方法的阅读入口。", "book-inner-child.html", "读《内在父母与内在小孩的拥抱》"),
        ("2018—2019", "情商教学与本性治疗", "《情商教练手册》在 2018 年出版；2019 年版《由心咨询》系统讨论本性治疗的咨询关系、原则与工作过程。", "book-heart.html", "读《由心咨询》"),
        ("2021—2022", "面向家庭与新一代读者", "《育儿先育己》、新版《梦的真相》与新版《儿童情商教育》陆续出版，分别回应养育、梦工作与儿童社会情感学习。", "book-parenting.html", "读《育儿先育己》"),
    ]
    cards = "".join(f'<article class="publication-step"><span class="publication-year">{E(year)}</span><div><h3>{E(title)}</h3><p>{E(summary)}</p><a class="text-link" href="{link}">{E(label)} ↗</a></div></article>' for year, title, summary, link, label in stages)
    return f'''<section class="section-space publication-journey" id="publication-journey"><div class="container">{section_head("A READING JOURNEY", "从早期著作，到今天的六部书", "同一部作品曾以不同书名或新版面世。沿着出版时间阅读，也能看见米杉持续发展的工作。")}
<div class="publication-steps">{cards}</div><div class="publication-links"><a href="book-eq-coach.html">情商教育 ↗</a><a href="book-dream.html">梦工作 ↗</a><a href="book-heart.html">本性治疗 ↗</a><a href="book-child-eq.html">儿童情商教育 ↗</a></div></div></section>'''


def build_books():
    cards = "".join(book_card(book, i) for i, book in enumerate(BOOKS, 1))
    body = hero("BOOKS & WRITING", "米杉中文著作", "六部公开出版著作，涵盖本性治疗、梦工作、情商教育与养育。", "米杉著作")
    body += f'''<section class="section-space reading-profile"><div class="container profile-grid"><div class="profile-photo"><img src="assets/michel-life-web.jpg" alt="米杉老师坐在室内的生活照" loading="lazy"></div><div><p class="eyebrow"><span class="eyebrow-line"></span>MEET THE AUTHOR</p><h2>米杉 <span lang="fr">Michel Claeys Bouuaert</span></h2><p>比利时心理治疗师、本性治疗创始人，长期从事情商与社会情感教育。他的著作涵盖本性治疗方法、梦工作和面向家庭与教育者的实践。</p><a class="text-link" href="teacher.html">认识米杉与他的经历 ↗</a></div></div></section>
<section class="section-space book-section" id="published"><div class="container">{section_head('PUBLISHED IN CHINESE', '中文出版著作', '从本性治疗、梦工作到情商教育与养育，沿着不同主题阅读米杉。')}<div class="catalog-grid">{cards}</div></div></section>
{publication_journey()}
<section class="section-space bookshop-section"><div class="container">{bookshop_code()}</div></section>
<section class="section-space forthcoming-book"><div class="container forthcoming-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>FORTHCOMING / 新著</p><h2>《情绪智能时代》</h2><p>米杉正在出版中的新著。关于情绪智能的下一部作品，敬请关注后续出版消息。</p></div><span class="forthcoming-mark">出版中</span></div></section>
<section class="section-space quote-gallery-section" id="quotes"><div class="container">{section_head('BOOK EXCERPTS', '从著作继续阅读')}<p class="section-lead">从《内在父母与内在小孩的拥抱》的短句进入，再回到原书阅读完整论述。</p><div class="quote-gallery"><a href="assets/quote-inner-022.jpg" target="_blank" rel="noopener"><img src="assets/quote-inner-022.jpg" alt="《内在父母与内在小孩的拥抱》摘录卡片" loading="lazy"><span>著作摘录 01 ↗</span></a><a href="assets/quote-inner-030.jpg" target="_blank" rel="noopener"><img src="assets/quote-inner-030.jpg" alt="《内在父母与内在小孩的拥抱》摘录卡片" loading="lazy"><span>著作摘录 02 ↗</span></a><a href="assets/quote-inner-015.jpg" target="_blank" rel="noopener"><img src="assets/quote-inner-015.jpg" alt="《内在父母与内在小孩的拥抱》摘录卡片" loading="lazy"><span>著作摘录 03 ↗</span></a></div><p class="source-note"><a href="https://kaiyuyang1989.github.io/mishan-quote-cards/" target="_blank" rel="noopener">浏览更多著作卡片 ↗</a></p></div></section>'''
    page("米杉著作", "米杉六部中文出版著作的介绍、微信扫码购书入口及出版中的《情绪智能时代》。", "reading.html", body)

    for book in BOOKS:
        cover = '<div class="poster-book-cover" role="img" aria-label="《内在父母与内在小孩的拥抱》封面"></div>' if book["image"] == "poster-crop" else f'<img src="assets/books/{E(book["image"])}" alt="《{E(book["title"])}》封面" class="{E(book["image_class"])}">'
        body = hero("THE BOOKS", E(book["title"]), E(book["topic"]), "米杉著作")
        focus = "".join(f'<li>{E(item)}</li>' for item in book["focus"])
        body += f'''<section class="section-space book-detail"><div class="container book-detail-grid"><div class="book-detail-cover">{cover}</div><div class="book-detail-copy"><p class="eyebrow"><span class="eyebrow-line"></span>{E(book['year'])} · {E(book['publisher'])}</p><h2>{E(book['title'])}</h2><p class="book-detail-subtitle">{E(book['subtitle'])}</p><p class="lead">{E(book['summary'])}</p><h3>内容介绍</h3><p>{E(book['about'])}</p><h3>本书关注</h3><ul class="book-focus">{focus}</ul><h3>适合谁阅读</h3><p>{E(book['reading'])}</p><h3>书目信息</h3><dl><div><dt>作者</dt><dd>米杉 Michel Claeys Bouuaert</dd></div><div><dt>出版年份</dt><dd>{E(book['year'])}</dd></div><div><dt>出版社</dt><dd>{E(book['publisher'])}</dd></div><div><dt>ISBN</dt><dd>{E(book['isbn'])}</dd></div></dl>{bookshop_code()}</div></div></section><section class="section-space related"><div class="container">{section_head('KEEP EXPLORING', '继续阅读')}<div class="related-grid"><a href="reading.html"><small>ALL BOOKS</small><strong>全部著作</strong><span>回到书目 ↗</span></a><a href="teacher.html"><small>THE AUTHOR</small><strong>认识米杉</strong><span>经历与教学 ↗</span></a><a href="approach.html"><small>THE APPROACH</small><strong>认识本性治疗</strong><span>从方法开始 ↗</span></a></div></div></section>'''
        image = f'assets/books/{book["image"]}' if book["image"] != "poster-crop" else "assets/mountain-dawn-web.jpg"
        book_schema = {
            "@context": "https://schema.org", "@type": "Book", "name": book["title"],
            "author": {"@type": "Person", "name": "米杉", "alternateName": "Michel Claeys Bouuaert"},
            "inLanguage": "zh-CN", "isbn": book["isbn"], "datePublished": book["year"],
            "publisher": {"@type": "Organization", "name": book["publisher"]},
            "url": f'https://essencetherapy.cn/book-{book["slug"]}.html',
        }
        page(book["title"], f'米杉《{book["title"]}》内容介绍与微信扫码购书入口。', f'book-{book["slug"]}.html', body, "reading.html", image, book_schema)


def build_teacher():
    from build_journey import build_teacher_page
    build_teacher_page(page, hero, section_head)
    return


def build_approach():
    body = hero("THE APPROACH", "本性治疗的方法与原则", "从身体感受进入，辨认受伤与资源性的内在空间，并在生活中整合变化。", "认识本性")
    body += '''<section class="section-space detail-intro"><div class="container intro-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>WHAT IT IS</p><h2>以身体感受为工作入口</h2></div><div class="intro-copy"><p class="lead">反复出现的情绪与反应，常常需要在当下的体验中得到更深入的理解。</p><p>本性治疗是米杉发展的一套心理咨询方法。它从当下的身体感受进入内在工作，帮助人辨认受伤的部分与可以支持自己的资源空间，并在生活中尝试新的选择。</p><p>这里介绍的是学习入口。若要深入理解方法、适用范围和实际操作，请阅读米杉原著，并在具备相应资质的带领下学习。</p></div></div></section>
<section class="section-space principles"><div class="container">''' + section_head("THE CORE", "方法的三个核心环节") + '''<div class="principle-stack"><article class="principle-row" id="presence"><span class="principle-no">01</span><div><p class="micro-en">PRESENCE · 此时此地</p><h3>从身体感受进入</h3><p>当情绪升起，先留意呼吸、身体和此刻的感受。让经验有机会被看见，而不是急着解释它。</p></div><a href="book-heart.html">读《由心咨询》 ↗</a></article><article class="principle-row" id="resources"><span class="principle-no">02</span><div><p class="micro-en">INNER SPACES · 内在空间</p><h3>看见受伤，也找到资源</h3><p>米杉用“内在小孩”和“内在父母”说明不同的内在状态：一边需要被倾听，一边能够给予支持。</p></div><a href="book-inner-child.html">读《内在父母…》 ↗</a></article><article class="principle-row" id="integration"><span class="principle-no">03</span><div><p class="micro-en">INTEGRATION · 回到生活</p><h3>把体验化成可以做的事</h3><p>课堂里的理解，需要回到关系和日常中继续练习。变化往往来自一次次具体的回应。</p></div><a href="archive.html">看课程资料 ↗</a></article></div></div></section>
<section class="section-space approach-terms"><div class="container approach-terms-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>KEY IDEAS</p><h2>读懂方法中的几个概念</h2><p>这些词指向工作时的具体经验。先认识它们，再阅读完整的方法论述。</p><a class="text-link" href="guide.html#guide-method">按主题继续阅读 ↗</a></div><div class="approach-term-list"><details><summary>身体感受<span aria-hidden="true">＋</span></summary><p>留意此刻呼吸、紧张或松弛等身体反应，为理解情绪提供一个可觉察的入口。</p></details><details><summary>内在空间<span aria-hidden="true">＋</span></summary><p>米杉用这一说法描述人在不同状态下的内在体验。辨认这些状态，有助于理解当下的反应。</p></details><details><summary>资源性空间<span aria-hidden="true">＋</span></summary><p>除了受伤经验，内在也可能有稳定、支持与力量的感受；工作会关注如何重新与之联结。</p></details><details><summary>整合变化<span aria-hidden="true">＋</span></summary><p>把咨询或课堂中得到的认识带回关系与日常，以具体的选择继续练习。</p></details></div></div></section>
<section class="section-space seven-principles"><div class="container">''' + section_head("SEVEN PRINCIPLES", "米杉提出的七个原则。", "七个原则贯穿从当下体验到生活整合的工作过程。") + '''<ol class="seven-grid"><li><b>01</b><strong>自我负责</strong><span>从自己能选择的地方开始。</span></li><li><b>02</b><strong>全然临在</strong><span>回到此时此地的感受。</span></li><li><b>03</b><strong>年龄回溯</strong><span>倾听受伤经验的来处。</span></li><li><b>04</b><strong>去除认同</strong><span>不把一个受伤状态当作全部的自己。</span></li><li><b>05</b><strong>转化能量</strong><span>以新的关系回应旧的感受。</span></li><li><b>06</b><strong>锚定内核</strong><span>联结有力量的内在空间。</span></li><li><b>07</b><strong>整合变化</strong><span>明确下一步，把体验带回生活。</span></li></ol><p class="source-note">延伸阅读：米杉《由心咨询》与《什么是本性治疗》。<a href="reading.html">继续读原著 ↗</a></p></div></section>
<section class="section-space related"><div class="container">''' + section_head("KEEP EXPLORING", "延伸阅读") + '''<div class="related-grid"><a href="teacher.html"><small>MICHEL</small><strong>认识米杉</strong><span>人、书与教学 ↗</span></a><a href="reading.html"><small>BOOKS</small><strong>走进著作</strong><span>从原书继续 ↗</span></a><a href="archive.html"><small>ARCHIVE</small><strong>课程沿革</strong><span>过去与现在 ↗</span></a></div></div></section>'''
    page("认识本性治疗", "本性治疗从身体感受出发，认识内在空间与资源。了解米杉方法及七个原则。", "approach.html", body)


def build_archive():
    from build_journey import build_archive_page
    build_archive_page(page, hero, section_head)
    return


def build_watch():
    body = hero("WATCH & LISTEN", "米杉的影像与声音", "通过访谈与公开节目，听米杉谈本性治疗、梦与情绪教育。", "影像与声音")
    body += '''<section class="section-space media-section"><div class="container">''' + section_head("PUBLIC CONVERSATIONS", "访谈与公开节目") + '''<div class="media-grid" id="media-list"><p class="media-loading">正在载入节目…</p></div><noscript><p>查看节目列表需要启用 JavaScript。</p></noscript></div></section>
<section class="section-space media-follow"><div class="container media-follow-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>MORE IN CHINESE</p><h2>公众号 · 扎根本性</h2><p>方法文章、著作讨论与课程资讯，持续在公众号更新。</p><a class="button button-dark" href="https://weixin.qq.com/r/QBPG3qvE6vaVre_990ZS" target="_blank" rel="noopener">打开公众号 ↗</a></div><div class="qr-card"><img src="assets/wechat-official-qr.png" alt="扎根本性公众号二维码" loading="lazy"><p>微信扫码关注</p></div></div></section>'''
    page("影像与声音", "米杉的公开影像和声音节目。包括访谈与公开节目，继续了解米杉的方法与教学。", "watch.html", body)


def build_voices():
    body = hero("OUR PHILOSOPHY", "学习与带领的理念", "关于倾听、练习、边界与持续学习的团队原则。", "我们的理念")
    body += '''<section class="section-space attitude-intro"><div class="container note-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>WHAT WE BELIEVE</p><h2>尊重体验，也尊重专业边界</h2></div><div><p>课程以理论讲授、方法示范和小组练习帮助学习者建立体验。每个人的经历和承受能力不同，带领者需要尊重其节奏与边界。</p><p>在课程中，理论讲授、方法示范与小组练习相互支持；课后仍需要持续实践与复盘。</p></div></div></section>
<section class="section-space statement-section"><div class="container">''' + section_head("IN PRACTICE", "四项实践原则") + '''<div class="statement-grid"><article class="statement-card reveal"><span>01 / LISTEN</span><h3>以倾听进入工作</h3><p>关注来访者当下的身体感受与表达，避免仓促解释。</p></article><article class="statement-card reveal"><span>02 / PRACTICE</span><h3>重视练习与整合</h3><p>通过示范、练习与课后复盘，支持学习者将方法应用于现实生活。</p></article><article class="statement-card reveal"><span>03 / RESPECT</span><h3>尊重个人节奏与边界</h3><p>在团体和个人工作中，依据参与者的意愿与状态调整探索深度。</p></article><article class="statement-card reveal"><span>04 / TOGETHER</span><h3>持续学习与督导</h3><p>专业能力依赖阅读、实操、反馈和督导的长期积累。</p></article></div><p class="statement-credit">扎根本性团队</p></div></section>
<section class="section-space voice-journey"><div class="container voice-journey-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>FROM HERE</p><h2>继续了解本性治疗</h2><p>可从著作、公开节目和课程沿革继续了解方法。</p></div><div class="related-grid"><a href="reading.html"><small>READ</small><strong>读著作</strong><span>从文字开始 ↗</span></a><a href="watch.html"><small>WATCH</small><strong>看与听</strong><span>公开节目 ↗</span></a><a href="archive.html"><small>ARCHIVE</small><strong>课程沿革</strong><span>看这段路 ↗</span></a></div></div></section>'''
    page("我们的理念", "扎根本性团队关于倾听、练习、专业边界与同行学习的理念。", "voices.html", body)


def update_home():
    p = DIST / "index.html"
    text = (ROOT / "content/home-base.html").read_text(encoding="utf-8")
    if 'href="extra.css"' not in text:
        text = text.replace('href="styles.css">', 'href="styles.css"><link rel="stylesheet" href="extra.css">', 1)
    text = text.replace('七种著作，<br>从你关心的那本读起。', '六部著作，<br>从原书认识本性。')
    text = text.replace('七种中文出版物，逐本介绍。', '六部中文出版物，逐本介绍。')
    text = text.replace('七种已核实的中文出版著作', '六部中文出版著作')
    new_nav = '      ' + re.search(r'<nav class="site-nav".*?</nav>', header(), flags=re.S).group().replace('href="index.html#contact"', 'href="#contact"')
    text = re.sub(r'      <nav class="site-nav"[^>]*>.*?</nav>', new_nav, text, count=1, flags=re.S)
    text = text.replace('向内走，<br><em>把力量带回生活。</em>', '本性治疗，<br><em>从真实感受开始。</em>')
    text = text.replace('从此刻的身体感受开始，认识自己的内在空间；在一次次练习中，学习与自己相处，也把新的选择带回日常。', '米杉创立的本性治疗，以身体感受为入口，辨认受伤与资源性的内在空间，并通过持续练习，把新的理解带回生活。')
    text = text.replace('这条路，<br>可以慢慢走。', '怎样学习<br>本性治疗？')
    text = text.replace('你可以从一次阅读或体验开始，再按自己的节奏进入工作坊。课后的练习与交流，也是在生活里继续应用方法的一部分。', '从书和文章认识方法，再在课程中体验、练习。理解一个概念之后，仍需要在生活里检验它。')
    text = text.replace('有时候，我们已经想明白了很多道理，心里却还是会难受。', '情绪不只是一种想法，也会表现为身体里的感受。')
    text = text.replace('本性治疗是一套以身体感受为入口的内在工作方法。它邀请我们暂时放下分析，去觉察当下发生了什么，认识受伤的内在空间，也重新联结有力量、有资源的自己。', '本性治疗由米杉创立，是一种以身体为中心的心理咨询方法。它帮助来访者辨认受伤的内在空间和资源性的内在空间，并在咨询师的引导下，对当下的体验进行工作。')
    text = text.replace('理解只是开始。通过体验、练习和持续的整合，新的觉察才有机会走进关系与生活。', '内在工作的成果还需要通过具体选择，在日常生活和关系中继续整合。')
    text = text.replace('感受 · 觉察 · 练习 · 整合', '从感受出发，在生活里练习')
    text = text.replace('给自己一条<br>可以继续走的路。', '这条路，<br>可以慢慢走。')
    text = text.replace('一页文字，<br>也可以是一个开始。', '米杉中文著作')
    text = text.replace('先从米杉的著作和已经公开的金句卡片认识这些方法。', '六部中文出版著作，涵盖本性治疗、梦工作、儿童情商教育与养育。')
    text = text.replace('走进米杉与著作 ↗', '查看全部著作 ↗')
    text = text.replace('一页文字，<br>也可以是一个开始。', '米杉中文著作')
    text = text.replace('读我们的态度', '读我们的理念')
    text = text.replace('<a href="voices.html">态度</a>', '<a href="voices.html">理念</a>')
    a = text.index('    <section class="teacher section-space"')
    b = text.index('    <section class="reading section-space"', a)
    teacher = '''    <section class="teacher section-space" id="teacher" aria-labelledby="teacher-heading"><div class="container teacher-grid"><div class="teacher-photo-stack"><img src="assets/michel-life-web.jpg" alt="米杉老师坐在室内的生活照" loading="lazy"><span>Michel Claeys Bouuaert</span></div><div class="teacher-copy"><p class="eyebrow"><span class="eyebrow-line"></span>MEET MICHEL CLAEYS</p><h2 id="teacher-heading">认识米杉</h2><p class="teacher-name">Michel Claeys Bouuaert</p><ul class="teacher-titles"><li>比利时心理治疗师</li><li>本性治疗创始人</li><li>世界人本主义心理学大会组织者</li><li>法国情商协会创始人</li></ul><p>米杉有四十余年专业咨询实践经验，2000 至 2015 年间以北京为工作重心，开展讲座与培训。他的中文著作涉及本性治疗、梦工作、情商教育与养育。</p><div class="teacher-links"><a class="text-link" href="teacher.html">阅读米杉完整介绍 ↗</a><a class="text-link" href="reading.html">浏览他的著作 ↗</a></div></div></div></section>\n\n'''
    text = text[:a] + teacher + text[b:]
    text = re.sub(r'    <section class="member-home-bridge[^\n]*?</section>\n\n', '', text, count=1, flags=re.S)
    a = text.index('    <section class="dispatch section-space"')
    b = text.index('    <section class="public-voice section-space"', a)
    dispatch = '''    <section class="dispatch section-space" aria-labelledby="dispatch-heading"><div class="container"><div class="section-heading"><div><p class="eyebrow"><span class="eyebrow-line"></span>EXPLORE FURTHER</p><h2 id="dispatch-heading">专题导读</h2></div><p class="section-intro">从你关心的主题出发，连接文章、著作、课程与公开记录。</p></div><div class="dispatch-grid"><a href="guide.html#guide-method"><small>01 / METHOD</small><h3>本性治疗</h3><p>从身体感受到内在空间，再到生活中的整合。</p><span aria-hidden="true">↗</span></a><a href="guide.html#guide-dream"><small>02 / DREAM WORK</small><h3>梦工作</h3><p>沿着梦主的经验，理解梦境与内在探索。</p><span aria-hidden="true">↗</span></a><a href="guide.html#guide-education"><small>03 / EDUCATION</small><h3>情商教育与养育</h3><p>为教育者、儿童与家庭选择合适的阅读入口。</p><span aria-hidden="true">↗</span></a><a href="guide.html#guide-history"><small>04 / THE JOURNEY</small><h3>米杉与在华教学</h3><p>从人物经历，进入高校资料与各地课程历程。</p><span aria-hidden="true">↗</span></a></div><a class="text-link dispatch-more" href="guide.html">浏览完整专题阅读 ↗</a></div></section>\n\n'''
    text = text[:a] + dispatch + text[b:]
    a = text.index('    <section class="public-voice section-space"')
    b = text.index('    <section class="contact section-space"', a)
    article_feature = '''    <section class="public-voice section-space" aria-labelledby="voice-heading"><div class="container public-voice-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>FROM OUR ARCHIVE</p><h2 id="voice-heading">本性治疗文献与<br>公众号文章选读</h2><p>阅读米杉与本性团队关于本性治疗、七原则、年龄回溯与梦工作的文章。</p><a class="text-link" href="insights.html">阅读经典文章 ↗</a></div><div class="voice-image" role="img" aria-label="晨光中的远山与树林"></div></div></section>\n\n'''
    text = text[:a] + article_feature + text[b:]
    people_feature = '''    <section class="section-space people-feature"><div class="container people-feature-grid"><a class="people-feature-photo" href="nanni.html"><img src="assets/ni-nanqi.jpg" alt="倪男奇肖像" loading="lazy"></a><div><p class="eyebrow"><span class="eyebrow-line"></span>PEOPLE & PARTNERS</p><h2>倪男奇与在地合作伙伴</h2><p>倪男奇长期参与米杉著作翻译、课程教学与本性治疗实践；郑州、石家庄、东莞和北京的合作伙伴，支持课程进入不同城市。</p><div class="people-feature-links"><a class="text-link" href="nanni.html">认识倪男奇 ↗</a><a class="text-link" href="partners.html">走进合作网络 ↗</a></div></div></div></section>\n\n'''
    text = text.replace('    <section class="contact section-space"', people_feature + '    <section class="contact section-space"', 1)
    text = text.replace('本性治疗、梦工作与社会情感学习。 / Essence Therapy, Dream Work & SEL.', '本性治疗、梦工作与社会情感学习。 / Essence Therapy, Dream Work & SEL.')
    text = text.replace('米杉是比利时心理治疗师、本性治疗创始人。', '米杉是比利时心理治疗师、本性治疗创始人。')
    text = text.replace('在中国，他通过著作、分享、工作坊与练习，和学习者一起探索如何把内在工作带回生活。', '他在中国的著作和课程积累多年，留下了许多可以继续读、继续练的资料。')
    text = text.replace('从他的著作开始阅读 <span aria-hidden="true">↗</span>', '阅读米杉完整介绍 <span aria-hidden="true">↗</span>')
    text = text.replace('<a class="text-link" href="reading.html">阅读米杉完整介绍', '<a class="text-link" href="teacher.html">阅读米杉完整介绍')
    text = text.replace('米杉老师的著作与课程', '米杉老师的著作与课程')
    text = re.sub(r'<a href="members/">[^<]*</a>', '', text)
    text = text.replace('一页文字，<br>也可以是一个开始。', '米杉中文著作')
    text = text.replace('米杉著作选读', '米杉著作选读')
    text = text.replace('<a href="reading.html#inner-child">《内在父母与内在小孩的拥抱》 ↗</a>', '<a href="book-inner-child.html">《内在父母与内在小孩的拥抱》 ↗</a>')
    text = text.replace('<a href="reading.html#heart">《由心咨询》 ↗</a>', '<a href="book-heart.html">《由心咨询》 ↗</a>')
    text = text.replace('<a href="reading.html#dream">《梦的真相》 ↗</a>', '<a href="book-dream.html">《梦的真相》 ↗</a>')
    text = text.replace('公开访谈与声音，课堂视频持续收录。', '从访谈与公开节目认识米杉。')
    text = text.replace('© <span id="year">2026</span> 扎根本性', '© <span id="year">2026</span> 扎根本性')
    text = text.replace('本性治疗，<br><em>从真实感受开始。</em>', '本性治疗：<br><em>从身体感受开始</em>')
    text = text.replace('本性治疗：<br><em>以身体感受进入内在工作。</em>', '本性治疗：<br><em>从身体感受开始</em>')
    text = text.replace('米杉创立的本性治疗，以身体感受为入口，辨认受伤与资源性的内在空间，并通过持续练习，把新的理解带回生活。', '米杉创立的本性治疗，是超个人心理学视角下、以身体为中心的心理咨询方法。通过识别受伤与资源性的内在空间，开展内在工作，并将变化整合到生活。')
    text = text.replace('本性治疗，<br>从真实的感受开始。', '本性治疗，<br>以身体感受为入口。')
    text = text.replace('情绪不只是一种想法，也会表现为身体里的感受。', '当情绪和反应反复出现，身体感受为进一步理解内在经验提供了入口。')
    text = text.replace('怎样学习<br>本性治疗？', '学习路径：<br>理论、示范与练习')
    text = text.replace('从书和文章认识方法，再在课程中体验、练习。理解一个概念之后，仍需要在生活里检验它。', '从著作与公开文章建立理论认识；在课程中通过方法示范、小组练习与督导反馈发展实际能力，并在课后持续整合。')
    text = text.replace('三场线下工作坊，分别从本性治疗的基础、梦工作与深入练习展开。选择你现在想走的那一步。', '三场线下工作坊分别聚焦本性治疗基础、梦工作与二阶深化。课程采用理论讲授、方法示范和小组实操相结合的形式。')
    text = text.replace('从自己开始，<br>走进本性治疗。', '本性治疗一阶：<br>核心方法入门')
    text = text.replace('认识内在空间，体验本性治疗的核心流程，在现场练习中建立初步的感受与理解。', '学习识别身体感受、区分受伤与资源性的内在空间，并通过示范和小组练习认识本性治疗的核心流程。')
    text = text.replace('学习识别身体感受、区分受伤与资源性的内在空间，并通过示范和小组练习认识本性治疗的核心流程。', '从身体感受进入，认识内在小孩与内在父母资源，并在示范、练习中学习本性治疗的基础方法。')
    text = text.replace('从梦出发，<br>听见内在的语言。', '米杉梦工作坊：<br>转译与内在工作')
    text = text.replace('以梦为入口，探索梦与内在空间之间的联系，体验梦工作的学习路径。', '学习梦境元素的理解与转译，并以梦为素材探索受伤与资源性的内在空间。')
    text = text.replace('让内在工作，<br>走得更深一些。', '本性治疗二阶：<br>深化方法实践')
    text = text.replace('在一阶基础上继续学习与练习本性治疗的方法，深化对内在过程的理解。', '在一阶基础上继续学习本性治疗核心流程，并深化年龄回溯、情绪转化与内在资源锚定的练习。')
    text = text.replace('在一阶基础上继续学习本性治疗核心流程，并深化年龄回溯、情绪转化与内在资源锚定的练习。', '在一阶基础上，学习年龄回溯、情绪转化与认知重构，并通过个案演示和督导反馈深化练习。')
    text = text.replace('从这里，<br>继续你的探索。', '课程咨询与<br>内容订阅')
    text = text.replace('想了解课程、报名方式，或找到适合自己的学习入口？扫码联系小扎，告诉我们你现在最想了解什么。', '了解课程内容、报名方式与学习路径，可扫描二维码联系小扎；公众号「扎根本性」持续更新方法文章与课程资料。')
    text = text.replace('把力量带回生活', '本性治疗方法与课程')
    text = text.replace('从身体的感受出发，练习与内在资源重新联结。了解本性治疗与 2027 春季课程。', '了解米杉创立的本性治疗、中文著作、公开文章及 2027 春季课程。')
    p.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    build_books()
    build_teacher()
    build_approach()
    build_archive()
    build_watch()
    build_voices()
    update_home()
