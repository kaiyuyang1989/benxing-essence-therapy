"""Public biography and course journey for the Benxing website."""

from html import escape as E


MILESTONES = [
    {
        "id": "beijing-2000", "year": "2000", "date": "2000—2015", "city": "北京",
        "kind": "在华教学起点", "title": "从北京出发",
        "intro": "米杉在北京开展心理咨询、讲座与培训，与中国高校及专业机构建立持续的教学联系。",
        "details": ["自 2000 年底起，米杉以北京为工作重心，持续开展咨询与教学。", "著作、公开讲座与工作坊，逐步成为中国学习者认识本性治疗和梦工作的路径。"],
        "link": "https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html", "link_text": "北京师范大学讲座预告",
    },
    {
        "id": "dream-2005", "year": "2005", "date": "5 月起", "city": "北京",
        "kind": "首个梦工作坊", "title": "从一间办公室开始的梦工作",
        "intro": "米杉在北京带领首个梦工作坊，参加者带着自己记录的梦，在小组中探索梦与个人经验的联系。",
        "details": ["《梦的真相》2010 年版译者序记载，工作坊于 2005 年 5 月在北京服装学院的一间办公室开始。", "小组成员分享各自的梦，从探问理论背景，逐渐进入对内在经验的探索。"],
        "link": "book-dream.html", "link_text": "了解《梦的真相》",
    },
    {
        "id": "eq-class-2006", "year": "2006", "date": "2006—2007", "city": "北京",
        "kind": "高校情商课程", "title": "北京印刷学院的连续情商课",
        "intro": "受北京印刷学院心理中心邀请，米杉为本科生和研究生开设两期连续情商课。",
        "details": ["《情商教练手册》2018 年版译者序记载了两期课程的缘起和课堂经历。", "倪男奇担任翻译，并与刘霞共同参与助教工作；课堂中的体验和讨论，也与书中的情商教育方法形成呼应。"],
        "link": "book-eq-coach.html", "link_text": "了解《情商教练手册》",
    },
    {
        "id": "quanzhou-2010", "year": "2010", "date": "11 月 4—8 日", "city": "泉州",
        "kind": "高校专业培训", "title": "华侨大学：七原则与梦工作",
        "intro": "华侨大学心理辅导中心的五天专题指导，将本性治疗原则与梦工作带入高校专业培训。",
        "details": ["五天的课程包含方法指导、启发式练习与案例讨论。", "从本性治疗七原则到梦工作，理论与实际的咨询、辅导场景相互连接。"],
        "link": "https://www.hqu.edu.cn/info/1073/14191.htm", "link_text": "阅读华侨大学报道",
    },
    {
        "id": "beijing-2013", "year": "2013", "date": "4 月 17 日发布", "city": "北京",
        "kind": "高校讲座预告", "title": "北京师范大学的梦主题讲座预告",
        "intro": "北京师范大学发布米杉梦主题讲座预告，内容涉及梦境信息、内在资源与个人经验。",
        "details": ["校方预告发布于 2013 年 4 月 17 日，列出的讲座时间为 4 月 27 日。", "预告介绍了梦的意义、理解梦境信息及辨认内在资源等讨论方向。"],
        "link": "https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html", "link_text": "阅读北师大讲座预告",
    },
    {
        "id": "zhengzhou-2017", "year": "2017", "date": "4 月", "city": "郑州",
        "kind": "本性治疗课程", "title": "与心能量在郑州的课程合作",
        "intro": "米杉与郑州心能量的课程合作留下了课堂照片，也连接起当地持续学习本性治疗的伙伴。",
        "details": ["2017 年 4 月的郑州课程照片，在团队的历史资料整理中被重新辨认。", "郑州心能量此后继续与米杉合作开展本性治疗课程。"],
        "link": "partners.html#xin-neng-liang", "link_text": "认识郑州合作伙伴",
    },
    {
        "id": "zhengzhou-2019", "year": "2019", "date": "本性治疗课程", "city": "郑州",
        "kind": "本性治疗课程", "title": "郑州心能量的教学现场",
        "intro": "米杉与倪男奇在郑州心能量的本性治疗课程中继续教学与交流。",
        "details": ["课程期间，心能量团队组织了学员咨询师形象照拍摄。", "米杉与倪男奇的合影也拍摄于这次郑州课程。"],
        "link": "partners.html#xin-neng-liang", "link_text": "查看合作资料",
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
        "id": "beijing-regression-2025", "year": "2025", "date": "年龄回溯工作坊", "city": "北京",
        "kind": "合作课程", "title": "英酷百兴心理主办年龄回溯工作坊",
        "intro": "北京英酷百兴心理主办米杉年龄回溯工作坊，围绕当下感受与早期经验开展现场学习。",
        "details": ["课程于 2025 年在北京举办。", "年龄回溯是本性治疗从当下身体感受进入内在工作的方式之一。"],
        "link": "partners.html#ying-ku-bai-xing", "link_text": "认识北京合作伙伴",
    },
    {
        "id": "dongguan-2026", "year": "2026", "date": "5 月—8 月", "city": "东莞 · 大湾区",
        "kind": "本性治疗一阶与二阶", "title": "从入门到深化",
        "intro": "东莞的本性治疗课程从一阶延续至二阶；2026 年 8 月二阶之前的课程由向光里主办。",
        "details": ["2026 年 8 月二阶之前的东莞米杉课程均由向光里主办。", "5 月的一阶以身体感受和内在空间为起点；8 月二阶继续深化年龄回溯与资源锚定。"],
        "link": "partners.html#xiang-guang-li", "link_text": "认识东莞课程伙伴",
    },
    {
        "id": "pku-shenzhen-2026", "year": "2026", "date": "5 月 7 日", "city": "深圳",
        "kind": "高校交流", "title": "走进北京大学深圳研究生院",
        "intro": "米杉与倪男奇走进北京大学深圳研究生院，与学工教师团队开展本性情商体验交流。",
        "details": ["交流以体验激发觉察，讨论教育者如何认识自己的情绪与内在经验。", "团队于 2026 年 6 月发布过这次 5 月 7 日活动的公开回顾。"],
        "link": "nanni.html", "link_text": "认识倪男奇",
    },
    {
        "id": "dongguan-space-2026", "year": "2026", "date": "8 月 3 日", "city": "东莞",
        "kind": "本性学习交流", "title": "向光里·心空间的现场交流",
        "intro": "米杉东莞二阶课程期间，伙伴们在向光里·心空间交流本性学习经验。",
        "details": ["郑小鹰老师引介米杉课程来到东莞，并筹备向光里·心空间。", "8 月 3 日的交流围绕空间体验、本性学习心得与米杉答疑展开。"],
        "link": "partners.html#xiang-guang-li", "link_text": "认识东莞合作伙伴",
    },
    {
        "id": "beijing-2026", "year": "2026", "date": "8 月 7—9 日", "city": "北京",
        "kind": "本性治疗一阶", "title": "北京的一阶学习",
        "intro": "米杉再次在北京带领本性治疗入门工作坊，让理论与现场练习相互印证。",
        "details": ["一阶从辨认身体感受开始，认识受伤与资源性的内在空间。", "方法示范和小组练习，为后续系统学习建立共同语言。"],
        "link": "book-heart.html", "link_text": "读《由心咨询》",
    },
    {
        "id": "qingdao-association-2026", "year": "2026", "date": "10 月 24—25 日", "city": "青岛",
        "kind": "学术年会与工作坊", "title": "青岛精神分析协会：年龄回溯",
        "intro": "米杉在青岛精神分析协会学术年会开展年龄回溯主题分享，并带领体验工作坊。",
        "details": ["10 月 24 日为年龄回溯大会报告，10 月 25 日为年龄回溯体验工作坊。", "现场合影的课程横幅标注“青岛精神分析年会 · 2026.10.25”。"],
        "image": "qingdao-age-regression-2026.jpg", "image_alt": "2026 年 10 月 25 日青岛年龄回溯体验工作坊合影",
        "link": "article-regression.html", "link_text": "了解年龄回溯",
    },
    {
        "id": "qingdao-2026", "year": "2026", "date": "10 月 30 日—11 月 1 日", "city": "青岛",
        "kind": "本性梦工作坊", "title": "从梦境到内在工作",
        "intro": "三天的课程围绕梦境元素、转译、内在空间和小组练习展开。",
        "details": ["第一天认识梦的隐喻语言与转译方法。", "第二天把梦境中的情绪与内在空间联系起来。", "第三天通过角色扮演和案例练习，探索如何把梦中的认识带回生活。"],
        "image": "qingdao-dream-2026.jpg", "image_alt": "2026 年 10 月 30 日至 11 月 1 日青岛米杉梦工坊合影",
        "link": "book-dream.html", "link_text": "读《梦的真相》",
    },
    {
        "id": "eq-2026", "year": "2026", "date": "11 月 3—8 日", "city": "北京",
        "kind": "情商培训师认证", "title": "米杉情商培训师认证班",
        "intro": "北京的认证班将情绪教育与团体带领放进连续训练和实践。",
        "details": ["课程面向希望在教育与团体场景中应用情商教育方法的学习者。", "从理解情绪到设计活动、带领团体，训练关注方法如何进入真实关系。"],
        "image": "beijing-eq-2026.jpg", "image_alt": "2026 年 11 月 3 日至 8 日北京米杉情商培训师认证班二阶合影",
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


TRACKS = {
    "beijing-2000": "therapy", "dream-2005": "dream",
    "eq-class-2006": "education university", "quanzhou-2010": "therapy dream university",
    "beijing-2013": "dream university", "zhengzhou-2017": "therapy", "zhengzhou-2019": "therapy", "cohort-2025": "therapy",
    "south-2025": "therapy", "dream-2025": "dream", "beijing-regression-2025": "therapy", "dongguan-2026": "therapy",
    "pku-shenzhen-2026": "education university", "dongguan-space-2026": "therapy", "beijing-2026": "therapy", "qingdao-association-2026": "therapy university", "qingdao-2026": "dream",
    "eq-2026": "education", "zhengzhou-2026": "therapy",
}


def milestone_card(item):
    paragraphs = "".join(f"<p>{E(detail)}</p>" for detail in item["details"])
    target = ' target="_blank" rel="noopener noreferrer"' if item["link"].startswith("http") else ""
    photo = f'<a class="journey-photo" href="assets/{item["image"]}" target="_blank" rel="noopener" aria-label="查看{E(item["image_alt"])}原图"><img src="assets/{item["image"]}" alt="{E(item["image_alt"])}" loading="lazy"></a>' if item.get("image") else ""
    return f'''<article class="journey-card" id="{item['id']}" data-track="{TRACKS[item['id']]}"><div class="journey-stamp"><span>{item['year']}</span><small>{E(item['date'])}</small></div><div class="journey-card-body"><p class="journey-kind">{E(item['city'])} <span aria-hidden="true">·</span> {E(item['kind'])}</p><h3>{E(item['title'])}</h3><p>{E(item['intro'])}</p>{photo}<details><summary>查看教学内容 <span aria-hidden="true">＋</span></summary><div class="journey-detail">{paragraphs}<a href="{E(item['link'])}"{target}>{E(item['link_text'])} ↗</a></div></details></div></article>'''


def build_archive_page(page, hero, section_head):
    body = hero("THE JOURNEY", "在中国的教学历程", "按年份、城市和主题，阅读米杉在中国的高校资料、工作坊与系统培训记录。", "教学历程")
    years = ("2000", "2005", "2006", "2010", "2013", "2017", "2019", "2025", "2026")
    links = ''.join(f'<a href="#year-{year}">{year}</a>' for year in years)
    body += f'''<section class="journey-opening section-space"><div class="container journey-opening-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>MICHEL IN CHINA</p><h2>著作、讲座与<br>现场课程</h2></div><div><p>2000 年以来，北京、泉州与各地课程留下了不同形式的教学资料。从梦工作坊和情商课程，到近年的筑基班与培训师认证，可以沿着年份阅读，也可以按主题筛选。</p><nav class="year-jump" aria-label="按年份查看教学历程">{links}</nav></div></div></section>'''
    body += '''<section class="journey-main section-space"><div class="container"><div class="journey-filter" aria-label="按主题筛选教学记录"><span>按主题阅读</span><div class="journey-filter-buttons" role="group" aria-label="教学主题"><button type="button" data-journey-filter="all" aria-pressed="true">全部</button><button type="button" data-journey-filter="therapy" aria-pressed="false">本性治疗</button><button type="button" data-journey-filter="dream" aria-pressed="false">梦工作</button><button type="button" data-journey-filter="education" aria-pressed="false">情商教育</button><button type="button" data-journey-filter="university" aria-pressed="false">高校资料</button></div><p id="journey-filter-status" class="sr-only" aria-live="polite"></p></div><div class="journey-rail">'''
    for year in years:
        cards = ''.join(milestone_card(item) for item in MILESTONES if item["year"] == year)
        body += f'<div class="journey-year" id="year-{year}"><div class="journey-year-label"><span>{year}</span></div><div class="journey-year-cards">{cards}</div></div>'
    body += '</div></div></section>'
    city_stops = (
        ("北京", "dream-2005"), ("泉州", "quanzhou-2010"), ("石家庄", None), ("郑州", "zhengzhou-2017"),
        ("青岛", "qingdao-association-2026"), ("西安", None), ("兰州", None),
        ("乌鲁木齐", None), ("江门", None), ("深圳", "south-2025"), ("东莞", "dongguan-2026"),
    )
    cities = ''.join(f'<a href="#{anchor}" aria-label="查看{city}的教学记录">{city}</a>' if anchor else f'<span>{city}</span>' for city, anchor in city_stops)
    body += f'''<section class="section-space city-journey"><div class="container"><p class="eyebrow"><span class="eyebrow-line"></span>PLACES ALONG THE WAY</p><h2>开展过教学交流的城市</h2><p>从北京、泉州到沿海与大湾区，课程与交流逐渐延伸到更多城市。选择有详细记录的城市，可直接查看对应节点。</p><div class="city-route" aria-label="米杉在中国开展过教学交流的城市">{cities}</div></div></section>
<section class="section-space archive-visuals"><div class="container">''' + section_head("NEXT CHAPTER", "2027 春季课程", "查看课程主题与当期安排") + '''<div class="archive-visual-grid"><a href="course-level-one.html"><img src="assets/course-level-1.jpg" alt="2027 春季本性治疗一阶课程海报" loading="lazy"><span>本性治疗一阶 · 杭州 ↗</span></a><a href="course-dream.html"><img src="assets/course-dream.jpg" alt="2027 春季米杉梦工作坊海报" loading="lazy"><span>米杉梦工作坊 · 郑州 ↗</span></a><a href="course-level-two.html"><img src="assets/course-level-2.jpg" alt="2027 春季本性治疗二阶课程海报" loading="lazy"><span>本性治疗二阶 · 郑州 ↗</span></a></div></div></section>'''
    page("在中国的教学历程", "按年份、城市和主题阅读米杉在中国的高校资料、本性治疗课程、梦工作坊与情商培训。", "archive.html", body)


def build_teacher_page(page, hero, section_head):
    body = hero("MICHEL CLAEYS BOUUAERT", "认识米杉", "比利时心理治疗师 · 本性治疗创始人 · 梦工作与情商教育实践者", "认识米杉")
    body += '''<section class="section-space teacher-biography"><div class="container teacher-bio-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>ABOUT MICHEL</p><h2>咨询、教学与写作</h2><p>米杉（Michel Claeys Bouuaert）出生于比利时，早年学习法律与犯罪学，随后转向教育、咨询和个人成长。他长期从事心理咨询与专业培训，将人本主义、超个人心理学及以身体为中心的工作方法融入实践，逐渐形成了本性治疗。</p><p>自 2000 年底起，他以北京为工作重心，在中国高校与心理专业机构开展讲座和培训。梦工作、本性治疗与情商教育的课程随后进入更多城市；中文著作则为这些方法提供了可持续阅读的文本。</p><a class="text-link" href="archive.html">查看在华教学历程 ↗</a></div><figure class="teacher-bio-photo"><img src="assets/michel-claeys.jpg" alt="米杉 Michel Claeys Bouuaert" loading="lazy"><figcaption>Michel Claeys Bouuaert</figcaption></figure></div></section>
<section class="section-space credentials"><div class="container">''' + section_head("WORK & WRITING", "持续工作的几个方向") + '''<div class="credentials-grid"><article><span>01</span><h3>本性治疗</h3><p>从当下的身体感受出发，辨认受伤与资源性的内在空间，展开咨询与教学。</p></article><article><span>02</span><h3>梦工作</h3><p>把梦主自己的经验作为理解梦境的起点，再探索梦与现实生活的联系。</p></article><article><span>03</span><h3>情商教育</h3><p>面向教育者、父母与团体带领者，发展可以进入课堂和关系的学习方法。</p></article><article><span>04</span><h3>中文著作</h3><p>从《由心咨询》到《梦的真相》，在文字中延续方法的论述与交流。</p></article></div></div></section>
<section class="section-space teacher-sources"><div class="container">''' + section_head("PUBLIC RECORDS", "高校公开资料", "阅读校方原始页面，了解米杉在中国的专业培训与讲座主题。") + '''<div class="teacher-sources-grid"><a href="https://www.hqu.edu.cn/info/1073/14191.htm" target="_blank" rel="noopener noreferrer"><small>2010 · 华侨大学报道</small><h3>五天专业培训：七原则与梦工作</h3><p>华侨大学心理辅导中心报道了米杉的专题指导与方法交流。</p><span>阅读校方报道 ↗</span></a><a href="https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html" target="_blank" rel="noopener noreferrer"><small>2013 · 北京师范大学预告</small><h3>“我们的梦说的都是我们自己”</h3><p>校方发布的讲座预告，介绍梦的意义、梦境信息与内在资源。</p><span>阅读讲座预告 ↗</span></a></div></div></section>
<section class="section-space teacher-photo-story"><div class="container teacher-photo-story-grid"><div class="teacher-photo-story-image"><img src="assets/michel-life-web.jpg" alt="米杉在室内留影" loading="lazy"></div><div><p class="eyebrow"><span class="eyebrow-line"></span>BEYOND THE CLASSROOM</p><h2>在实践中深化方法</h2><p>咨询、写作、现场示范与长期带领共同构成米杉的工作。对于学习者，理解概念之后，还需要通过现场练习和反思来认识方法的边界与应用。</p><a class="text-link" href="reading.html">浏览米杉中文著作 ↗</a></div></div></section>
<section class="section-space teacher-path"><div class="container">''' + section_head("THE JOURNEY IN CHINA", "从北京到更多城市") + '''<div class="teacher-path-grid"><a href="archive.html#beijing-2000"><small>2000—2015 · BEIJING</small><h3>在北京扎根</h3><p>咨询、著作与高校讲座，为中国读者和学习者打开认识本性治疗的入口。</p><span>查看教学记录 ↗</span></a><a href="archive.html#cohort-2025"><small>2025 · FIRST COHORT</small><h3>首届筑基班</h3><p>连续的课程把理论、方法示范、小组练习与阶段复盘连接起来。</p><span>查看教学记录 ↗</span></a><a href="archive.html#eq-2026"><small>2026 · MORE CITIES</small><h3>多地课程与认证班</h3><p>本性治疗、梦工作和情商培训师认证，延续到北京、青岛、郑州与大湾区。</p><span>查看教学记录 ↗</span></a></div></div></section>
<section class="section-space teacher-new-book"><div class="container"><p class="eyebrow"><span class="eyebrow-line"></span>FORTHCOMING</p><h2>《情绪智能时代》</h2><p>米杉新著，出版中。</p><a class="text-link" href="reading.html">阅读米杉著作目录 ↗</a></div></section>'''
    page("认识米杉", "米杉 Michel Claeys Bouuaert 的经历、方法、中文著作及在中国的教学历程。", "teacher.html", body)
