"""Public biography and course journey for the Benxing website."""

from html import escape as E


MILESTONES = [
    {
        "id": "beijing-2000", "year": "2000", "date": "2000—2015", "city": "北京",
        "kind": "在华教学起点", "title": "从北京出发",
        "intro": "米杉在北京开展心理咨询、讲座与培训，与中国高校及专业机构建立持续的教学联系。",
        "details": ["自 2000 年底起，米杉以北京为工作重心，持续开展咨询与教学。", "著作、公开讲座与工作坊，逐步成为中国学习者认识本性治疗和梦工作的路径。"],
        "link": "https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html", "link_text": "北京师范大学讲座资料",
    },
    {
        "id": "quanzhou-2010", "year": "2010", "date": "11 月 4—8 日", "city": "泉州",
        "kind": "高校专业培训", "title": "华侨大学：七原则与梦工作",
        "intro": "华侨大学心理辅导中心的五天专题指导，将本性治疗原则与梦工作带入高校专业培训。",
        "details": ["五天的课程包含方法指导、启发式练习与案例讨论。", "从本性治疗七原则到梦工作，理论与实际的咨询、辅导场景相互连接。"],
        "link": "https://www.hqu.edu.cn/info/1073/14191.htm", "link_text": "阅读华侨大学报道",
    },
    {
        "id": "beijing-2013", "year": "2013", "date": "4 月 27 日", "city": "北京",
        "kind": "公开讲座", "title": "“我们的梦说的都是我们自己”",
        "intro": "在北京师范大学，米杉面向公众讨论梦的功能、梦境语言与内在资源。",
        "details": ["讲座从“如何理解梦里的这出戏”出发，讨论梦与个人经验之间的关系。", "现场为英语讲座，提供汉语翻译。"],
        "link": "https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html", "link_text": "阅读讲座介绍",
    },
    {
        "id": "cohort-2025", "year": "2025", "date": "首届", "city": "中国",
        "kind": "系统培训", "title": "首届本性治疗筑基班",
        "intro": "从单次工作坊走向连续学习，首届筑基班把理论、示范、练习和阶段复盘连成一条路径。",
        "details": ["学员在不同阶段学习身体感受、内在空间与本性治疗核心流程。", "随着课程推进，练习逐渐延伸到日常关系与专业应用。"],
        "link": "approach.html", "link_text": "了解本性治疗方法",
    },
    {
        "id": "south-2025", "year": "2025", "date": "11 月", "city": "深圳 · 东莞",
        "kind": "本性治疗工作坊", "title": "大湾区的学习现场",
        "intro": "深圳一阶与东莞二阶课程，让不同学习阶段的人在现场完成示范、练习与交流。",
        "details": ["深圳的一阶课程面向初次接触本性治疗的学习者。", "东莞的二阶课程继续深化内在工作；当地也举办了体验团体。"],
        "link": "reading.html", "link_text": "从米杉著作继续了解",
    },
    {
        "id": "dream-2025", "year": "2025", "date": "11 月 28—30 日", "city": "北京",
        "kind": "梦工作坊", "title": "在北京，把梦带进工作",
        "intro": "三天的梦工作坊，把记梦、梦境转译与内在探索放进学习现场。",
        "details": ["梦不被当作固定符号的谜语；梦主自己的经验，是理解梦境的起点。", "从梦中的情绪和人物进入内在空间，再将认识带回现实生活。"],
        "link": "book-dream.html", "link_text": "读《梦的真相》",
    },
    {
        "id": "dongguan-2026", "year": "2026", "date": "5 月—8 月", "city": "东莞 · 大湾区",
        "kind": "本性治疗一阶与二阶", "title": "从入门到深化",
        "intro": "春夏两季的大湾区课程，延续本性治疗的阶段式学习。",
        "details": ["5 月的一阶课程以身体感受、内在空间与基础流程为起点。", "8 月东莞的二阶课程进一步练习评估、年龄回溯与资源锚定。"],
        "link": "approach.html", "link_text": "查看方法与原则",
    },
    {
        "id": "beijing-2026", "year": "2026", "date": "8 月 7—9 日", "city": "北京",
        "kind": "本性治疗一阶", "title": "北京的一阶学习",
        "intro": "米杉再次在北京带领本性治疗入门工作坊，让理论与现场练习相互印证。",
        "details": ["一阶从辨认身体感受开始，认识受伤与资源性的内在空间。", "方法示范和小组练习，为后续系统学习建立共同语言。"],
        "link": "book-heart.html", "link_text": "读《由心咨询》",
    },
    {
        "id": "qingdao-2026", "year": "2026", "date": "10 月 30 日—11 月 1 日", "city": "青岛",
        "kind": "本性梦工作坊", "title": "从梦境到内在工作",
        "intro": "三天的课程围绕梦境元素、转译、内在空间和小组练习展开。",
        "details": ["第一天认识梦的隐喻语言与转译方法。", "第二天把梦境中的情绪与内在空间联系起来。", "第三天通过角色扮演和案例练习，探索如何把梦中的认识带回生活。"],
        "link": "book-dream.html", "link_text": "读《梦的真相》",
    },
    {
        "id": "eq-2026", "year": "2026", "date": "11 月 3—8 日", "city": "北京",
        "kind": "情商培训师认证", "title": "米杉情商培训师认证班",
        "intro": "北京的认证班将情绪教育与团体带领放进连续训练和实践。",
        "details": ["课程面向希望在教育与团体场景中应用情商教育方法的学习者。", "从理解情绪到设计活动、带领团体，训练关注方法如何进入真实关系。"],
        "link": "book-eq-coach.html", "link_text": "读《情商教练手册》",
    },
    {
        "id": "zhengzhou-2026", "year": "2026", "date": "11 月 13—15 日", "city": "郑州",
        "kind": "本性治疗一阶", "title": "从身份、情绪到内在资源",
        "intro": "郑州一阶按三天展开：认识身份与内在空间，识别情绪，练习联结资源。",
        "details": ["第一天：探索“我是谁”，辨认受伤与资源性的内在空间。", "第二天：从身体感受进入，观察情绪能量与核心工作流程。", "第三天：练习联结内在父母和资源空间，并讨论如何在生活中整合。"],
        "link": "approach.html", "link_text": "认识本性治疗",
    },
]


def milestone_card(item):
    paragraphs = "".join(f"<p>{E(detail)}</p>" for detail in item["details"])
    target = ' target="_blank" rel="noopener noreferrer"' if item["link"].startswith("http") else ""
    return f'''<article class="journey-card" id="{item['id']}"><div class="journey-stamp"><span>{item['year']}</span><small>{E(item['date'])}</small></div><div class="journey-card-body"><p class="journey-kind">{E(item['city'])} <span aria-hidden="true">·</span> {E(item['kind'])}</p><h3>{E(item['title'])}</h3><p>{E(item['intro'])}</p><details><summary>走进这一站 <span aria-hidden="true">↗</span></summary><div class="journey-detail">{paragraphs}<a href="{E(item['link'])}"{target}>{E(item['link_text'])} ↗</a></div></details></div></article>'''


def build_archive_page(page, hero, section_head):
    body = hero("THE JOURNEY", "一条持续展开的学习之路", "从北京的高校讲座，到不同城市的工作坊与系统培训。沿着年份，走进米杉在中国的教学现场。", "课程沿革")
    links = ''.join(f'<a href="#year-{year}">{year}</a>' for year in ("2000", "2010", "2013", "2025", "2026"))
    body += f'''<section class="journey-opening section-space"><div class="container journey-opening-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>MICHEL IN CHINA</p><h2>从北京出发，<br>走进更多城市的课堂。</h2></div><div><p>米杉自 2000 年底起在北京从事咨询与教学。后来，梦工作、本性治疗和情商教育的课程在更多城市展开。首届筑基班与情商培训师认证班，让这段教学历程有了更连续的结构。</p><nav class="year-jump" aria-label="按年份查看课程历程">{links}</nav></div></div></section>'''
    body += '<section class="journey-main section-space"><div class="container"><div class="journey-rail">'
    for year in ("2000", "2010", "2013", "2025", "2026"):
        cards = ''.join(milestone_card(item) for item in MILESTONES if item["year"] == year)
        body += f'<div class="journey-year" id="year-{year}"><div class="journey-year-label"><span>{year}</span><small>{"起点" if year == "2000" else "继续前行"}</small></div><div class="journey-year-cards">{cards}</div></div>'
    body += '</div></div></section>'
    body += '''<section class="section-space city-journey"><div class="container"><p class="eyebrow"><span class="eyebrow-line"></span>PLACES ALONG THE WAY</p><h2>教学的足迹，不止于时间轴。</h2><p>从北方到西部，再到沿海与大湾区，这些城市都留下过本性治疗、梦工作或情商教育的交流与学习。</p><div class="city-route" aria-label="米杉在中国开展过教学交流的城市"><span>北京</span><span>石家庄</span><span>郑州</span><span>青岛</span><span>西安</span><span>兰州</span><span>乌鲁木齐</span><span>江门</span><span>深圳</span><span>东莞</span></div></div></section>
<section class="section-space archive-visuals"><div class="container">''' + section_head("NEXT CHAPTER", "下一程，继续在现场相遇。", "2027 年春季课程") + '''<div class="archive-visual-grid"><a href="index.html#courses"><img src="assets/course-level-1.jpg" alt="2027 春季本性治疗一阶课程海报" loading="lazy"><span>本性治疗一阶 · 杭州 ↗</span></a><a href="index.html#courses"><img src="assets/course-dream.jpg" alt="2027 春季米杉梦工作坊海报" loading="lazy"><span>米杉梦工作坊 · 郑州 ↗</span></a><a href="index.html#courses"><img src="assets/course-level-2.jpg" alt="2027 春季本性治疗二阶课程海报" loading="lazy"><span>本性治疗二阶 · 郑州 ↗</span></a></div></div></section>'''
    page("课程沿革", "米杉在中国的高校讲座、本性治疗筑基班、梦工作坊与情商培训师认证班。", "archive.html", body)


def build_teacher_page(page, hero, section_head):
    body = hero("MICHEL CLAEYS BOUUAERT", "认识米杉", "比利时心理治疗师 · 本性治疗创始人 · 梦工作与情商教育实践者", "认识米杉")
    body += '''<section class="section-space teacher-biography"><div class="container teacher-bio-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>ABOUT MICHEL</p><h2>从咨询室走向课堂</h2><p>米杉（Michel Claeys Bouuaert）出生于比利时，早年学习法律与犯罪学，随后转向教育、咨询和个人成长。他长期从事心理咨询与专业培训，将人本主义、超个人心理学及以身体为中心的工作方法融入实践，逐渐形成了本性治疗。</p><p>自 2000 年底起，他以北京为工作重心，在中国高校与心理专业机构开展讲座和培训。后来，梦工作、本性治疗和情商教育的课程来到更多城市。他的著作把这些工作经验延伸到中文读者的阅读与实践中。</p><a class="text-link" href="archive.html">沿着时间走进课程历程 ↗</a></div><figure class="teacher-bio-photo"><img src="assets/michel-claeys.jpg" alt="米杉 Michel Claeys Bouuaert" loading="lazy"><figcaption>Michel Claeys Bouuaert</figcaption></figure></div></section>
<section class="section-space credentials"><div class="container">''' + section_head("WORK & WRITING", "持续工作的几个方向") + '''<div class="credentials-grid"><article><span>01</span><h3>本性治疗</h3><p>从当下的身体感受出发，辨认受伤与资源性的内在空间，展开咨询与教学。</p></article><article><span>02</span><h3>梦工作</h3><p>把梦主自己的经验作为理解梦境的起点，再探索梦与现实生活的联系。</p></article><article><span>03</span><h3>情商教育</h3><p>面向教育者、父母与团体带领者，发展可以进入课堂和关系的学习方法。</p></article><article><span>04</span><h3>中文著作</h3><p>从《由心咨询》到《梦的真相》，在文字中延续方法的论述与交流。</p></article></div></div></section>
<section class="section-space teacher-photo-story"><div class="container teacher-photo-story-grid"><div class="teacher-photo-story-image"><img src="assets/michel-life-web.jpg" alt="米杉在室内留影" loading="lazy"></div><div><p class="eyebrow"><span class="eyebrow-line"></span>BEYOND THE CLASSROOM</p><h2>专业的训练，<br>来自持续的实践。</h2><p>咨询、写作、现场示范与长期带领共同构成米杉的工作。对于学习者，理解一个概念之后，还要在真实的相遇和练习中，逐步看见它如何发挥作用。</p><a class="text-link" href="reading.html">浏览米杉中文著作 ↗</a></div></div></section>
<section class="section-space teacher-path"><div class="container">''' + section_head("THE JOURNEY IN CHINA", "从北京到更多城市") + '''<div class="teacher-path-grid"><a href="archive.html#beijing-2000"><small>2000—2015 · BEIJING</small><h3>在北京扎根</h3><p>咨询、著作与高校讲座，为中国读者和学习者打开认识本性治疗的入口。</p><span>走进这一段 ↗</span></a><a href="archive.html#cohort-2025"><small>2025 · FIRST COHORT</small><h3>首届筑基班</h3><p>连续的课程把理论、方法示范、小组练习与阶段复盘连接起来。</p><span>走进这一段 ↗</span></a><a href="archive.html#eq-2026"><small>2026 · MORE CITIES</small><h3>走向系统培训</h3><p>本性治疗、梦工作和情商培训师认证，延续到北京、青岛、郑州与大湾区。</p><span>走进这一段 ↗</span></a></div></div></section>
<section class="section-space teacher-new-book"><div class="container"><p class="eyebrow"><span class="eyebrow-line"></span>FORTHCOMING</p><h2>《情绪智能时代》</h2><p>米杉新著，出版中。</p><a class="text-link" href="reading.html">阅读米杉著作目录 ↗</a></div></section>'''
    page("认识米杉", "米杉 Michel Claeys Bouuaert 的经历、方法、中文著作及在中国的教学历程。", "teacher.html", body)
