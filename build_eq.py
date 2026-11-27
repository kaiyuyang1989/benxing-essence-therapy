"""Build the public emotional intelligence course and alliance pages."""

from html import escape as E

from build_content import hero, page, section_head
from tools.eq_people import BACKGROUNDS, PEOPLE, PUBLIC_LINKS


LEVEL_ONE_DAYS = [
    ("01", "相识与信任", "通过欢迎活动、共同约定与合作练习，建立可以表达和探索的课堂氛围。"),
    ("02", "沟通与责任", "练习倾听、提问与回应，观察交流如何影响彼此的选择和关系。"),
    ("03", "自我觉察与情绪识别", "从身体反应与日常经验出发，辨认情绪，并学习用清楚的语言表达感受。"),
    ("04", "优势、反馈与集体智慧", "在同伴反馈中发现个人资源，尝试让团体中的不同经验彼此支持。"),
    ("05", "合作、共识与整合", "通过小组活动体验协作与分歧，把个人觉察放进真实的团体关系。"),
    ("06", "课程设计与回看", "从学习者转向带领者，梳理活动目标、流程和复盘方式，形成自己的课程设计。"),
]


def photo(name, alt, caption, featured=False):
    class_name = ' class="eq-photo eq-photo-featured"' if featured else ' class="eq-photo"'
    return f'''<figure{class_name}><a href="assets/{E(name)}" target="_blank" rel="noopener" aria-label="查看{E(alt)}原图"><img src="assets/{E(name)}" alt="{E(alt)}" loading="lazy"></a><figcaption>{E(caption)}</figcaption></figure>'''


def build_level_one():
    body = hero(
        "EMOTIONAL INTELLIGENCE / LEVEL I",
        "情商教育培训师一阶",
        "2026 年 8 月 11—16 日 · 北京。六天体验式学习，从情绪觉察、关系沟通走向活动设计与带领。",
        "情商一阶",
    )
    body += '''<section class="section-space eq-opening"><div class="container eq-opening-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>LEARNING BY EXPERIENCE</p><h2>先成为学习者，再学习带领</h2><p>情商教育不止于认识情绪概念。米杉的课程让参与者在活动中经历倾听、表达、合作与反馈，同时观察活动为什么这样设计、带领者如何回应团体。个人体验与课程设计由此相互连接。</p><p>这是一段已完成的教学记录。下方按 2026 年北京一阶课程的实际主题，呈现它的学习路径与课堂现场。</p><div class="eq-links"><a class="text-link" href="eq-alliance.html">走进培训师联盟 ↗</a><a class="text-link" href="book-eq-coach.html">阅读《情商教练手册》 ↗</a></div></div><div class="eq-opening-image"><img src="assets/eq1-beijing-group-practice-2026.jpg" alt="2026 年 8 月北京情商培训师一阶课堂，学员围成圆圈练习" loading="lazy"><span>BEIJING · AUGUST 2026</span></div></div></section>'''
    days = "".join(
        f'<article class="eq-day"><span>DAY {E(num)}</span><div><h3>{E(title)}</h3><p>{E(summary)}</p></div></article>'
        for num, title, summary in LEVEL_ONE_DAYS
    )
    body += f'''<section class="section-space eq-days"><div class="container">{section_head("SIX DAYS IN BEIJING", "六天的学习路径", "每一天既有个人体验，也有对教学方法的观察与复盘。")}
<div class="eq-day-grid">{days}</div></div></section>'''
    body += '''<section class="section-space eq-pillars"><div class="container eq-pillars-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>THE LEARNING ARC</p><h2>从临在，到关系与行动</h2><p>课程把个人情绪能力与团体带领放在同一条学习线上：先能觉察自己，再练习理解他人、与人合作，最后设计让别人也能参与和学习的活动。</p></div><div class="eq-pillar-list"><span>临在与自我觉察</span><span>情绪识别与调节</span><span>倾听、沟通与关系</span><span>合作与共识</span><span>活动设计与带领</span></div></div></section>'''
    body += '<section class="section-space eq-gallery-section"><div class="container">'
    body += section_head("INSIDE THE CLASSROOM", "北京一阶课堂", "从米杉的讲授到学员的团体练习，看看方法怎样在现场展开。")
    body += '<div class="eq-gallery-grid">'
    body += photo("eq1-beijing-michel-teaching-2026.jpg", "米杉在北京情商一阶课堂讲解情绪识别", "米杉在课堂上讲解情绪与活动设计。")
    body += photo("eq1-beijing-group-practice-2026.jpg", "北京情商一阶学员围成圆圈进行活动", "学员通过团体活动体验关系与合作。", True)
    body += photo("eq1-beijing-classroom-2026.jpg", "2026 年北京情商一阶课堂的团体活动", "2026 / 08 · 从活动体验进入课堂讨论。")
    body += '</div></div></section>'
    body += '''<section class="section-space eq-continue"><div class="container eq-continue-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>FROM CLASS TO PRACTICE</p><h2>学习之后，继续带领</h2><p>2026 年 11 月的北京二阶课程，让学员把一阶经验带入自己的主题活动：设计、带领、观察团体，再接收反馈。课程由此延伸为同伴之间的持续学习。</p><a class="text-link" href="eq-alliance.html">认识本性情商培训师联盟 ↗</a></div><a href="eq-alliance.html" class="eq-continue-photo"><img src="assets/beijing-eq-2026.jpg" alt="2026 年 11 月北京情商培训师二阶课程合影" loading="lazy"></a></div></section>'''
    page(
        "情商教育培训师一阶",
        "米杉 2026 年北京情商教育培训师一阶课程：六天学习主题、课堂照片、活动设计与后续带领实践。",
        "course-eq-level-one.html", body, "courses.html", "assets/eq1-beijing-group-practice-2026.jpg",
    )


def build_alliance():
    body = hero(
        "EQ TRAINERS · A SHARED PRACTICE",
        "米杉本性情商培训师联盟",
        "从北京一、二阶的连续学习出发，把情绪觉察、关系沟通与体验式教育带进更多课堂和团体。",
        "培训师联盟",
    )
    body += '''<section class="section-space eq-alliance-intro"><div class="container eq-alliance-intro-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>THE COMMUNITY</p><h2>一群学习者，<br>继续成为带领者</h2></div><div><p>2026 年北京情商培训师课程以两个阶段展开：八月一阶重在个人体验与教学观察，十一月二阶走向学员自主设计和现场带领。课程之后，团队正与伙伴们讨论如何在教育、家庭和团体场景中继续实践。</p><p>联盟承接这份共同学习：以真实课堂为基础，在实践中复盘，在合作中形成更成熟的带领方式。</p><div class="eq-links"><a class="text-link" href="course-eq-level-one.html">了解情商一阶 ↗</a><a class="text-link" href="archive.html#eq-2026">查看北京二阶记录 ↗</a></div></div></div></section>'''
    body += '<section class="section-space eq-gallery-section eq-alliance-gallery" id="classroom"><div class="container">'
    body += section_head("FROM THE CLASSROOM", "两个阶段的课堂", "体验、观察、设计和带领，构成连续的学习过程。")
    body += '<div class="eq-gallery-grid eq-gallery-three">'
    body += photo("eq1-beijing-group-practice-2026.jpg", "2026 年 8 月北京情商一阶课堂团体练习", "2026 / 08 · 北京一阶：在活动中建立信任。")
    body += photo("eq2-beijing-classroom-2026.jpg", "2026 年 11 月北京情商二阶课堂学员带领活动", "2026 / 11 · 北京二阶：学员走到课堂中央。")
    body += photo("eq2-beijing-facilitation-2026.jpg", "北京情商二阶课堂中的学员主题带领", "2026 / 11 · 主题活动与同伴观察。")
    body += photo("eq2-beijing-circle-2026.jpg", "2026 年北京情商二阶课堂围圈活动", "2026 / 11 · 团体在圆圈中继续练习。")
    body += photo("eq2-beijing-group-2026.jpg", "2026 年北京情商二阶课堂集体练习", "2026 / 11 · 从学员带领回到共同体验。")
    body += '</div></div></section>'
    body += '''<section class="section-space eq-people"><div class="container">'''
    body += section_head("PEOPLE IN PRACTICE", "导师与实践带领者", "方法教学与课堂实践相接，带领能力在一次次设计和反馈中形成。")
    body += '''<div class="eq-people-grid"><article class="eq-person-card"><img src="assets/michel-life-web.jpg" alt="米杉肖像" loading="lazy"><div><small>COURSE FOUNDER</small><h3>米杉 <span>Michel Claeys Bouuaert</span></h3><p>比利时心理治疗师、本性治疗创始人。长期从事情商教育、心理咨询与体验式培训，为课程提供方法和现场教学。</p><a class="text-link" href="teacher.html">认识米杉 ↗</a></div></article><article class="eq-person-card"><img src="assets/ni-nanqi.jpg" alt="倪男奇肖像" loading="lazy"><div><small>TEACHING COLLABORATOR</small><h3>倪男奇 <span>Ni Nanqi</span></h3><p>长期参与米杉著作的中文译介和课程协作，连接方法文本与中文学习现场，并持续开展本性治疗教学。</p><a class="text-link" href="nanni.html">认识倪男奇 ↗</a></div></article></div>'''
    body += '''<div class="eq-practice-intro"><div><small>THE 2026 COHORT</small><h3>来自不同实践领域的带领者</h3></div><p>二阶课程中，22 位学员分别设计并带领约 90 分钟的主题活动。有人从情绪识别进入，有人聚焦亲密关系、家庭、信任、合作或自我联结。不同的专业经验，在同一个课堂中相互校准。<a class="text-link" href="#facilitators">认识 22 位课堂带领者 ↗</a></p></div>'''
    themes = [
        ("情绪与自我觉察", "认识感受、需要与身体信号。"),
        ("倾听与关系", "在亲密关系和团体中练习沟通。"),
        ("信任与合作", "让参与者在活动中体验支持与共创。"),
        ("家庭与成长", "回应养育、人生阶段与责任主题。"),
    ]
    body += '<div class="eq-theme-grid">' + ''.join(
        f'<article><span>0{i}</span><h4>{E(title)}</h4><p>{E(summary)}</p></article>'
        for i, (title, summary) in enumerate(themes, 1)
    ) + '</div></div></section>'
    body += '<section class="section-space eq-members" id="facilitators"><div class="container">'
    body += section_head("THE PEOPLE · BEIJING 2026", "22 位课堂带领者", "六天课程，每人围绕自己的主题设计和带领一场课堂活动。")
    body += '''<figure class="eq-members-photo"><a href="assets/beijing-eq-2026.jpg" target="_blank" rel="noopener" aria-label="查看2026年北京情商二阶班级合影原图"><img src="assets/beijing-eq-2026.jpg" alt="2026年北京情商培训师二阶班级合影" loading="lazy"></a><figcaption>北京 · 2026 年 11 月 3—8 日</figcaption></figure>'''
    body += '<nav class="eq-day-jump" aria-label="按课程日期查看带领者">' + ''.join(
        f'<a href="#facilitators-day-{day}">11 月 {day + 2} 日</a>' for day in range(1, 7)
    ) + '</nav>'
    for day in range(1, 7):
        cards = []
        for number, person in enumerate(PEOPLE, 1):
            person_day, name, _, background_code, topic, activity = person
            if person_day != day:
                continue
            source = PUBLIC_LINKS.get(name)
            source_link = f'<a class="text-link" href="{E(source[0])}" target="_blank" rel="noopener noreferrer">{E(source[1])}</a>' if source else ''
            cards.append(f'''<article class="eq-member-card"><div class="eq-member-top"><span>{number:02d}</span><small>{E(BACKGROUNDS[background_code][0])}</small></div><h4>{E(name)}</h4><h5>{E(topic[0])}</h5><p>{E(activity[0])}</p>{source_link}</article>''')
        body += f'''<div class="eq-member-day" id="facilitators-day-{day}"><div class="eq-member-day-head"><span>DAY {day:02d}</span><h3>11 月 {day + 2} 日</h3></div><div class="eq-member-grid">{"".join(cards)}</div></div>'''
    body += '</div></section>'
    body += '<section class="section-space eq-projects" id="projects"><div class="container">'
    body += section_head("WORK IN PROGRESS", "从课堂延伸的项目", "持续学习有不同形式；每一个项目都从真实的参与和需求出发。")
    body += '''<div class="eq-project-grid"><article><small>ONGOING PRACTICE</small><h3>主题活动与同伴复盘</h3><p>从二阶的现场带领继续整理活动设计、团体观察和反馈，让课堂经验成为可以反复打磨的实践。</p></article><article><small>IN DEVELOPMENT</small><h3>带领者访谈</h3><p>邀请愿意分享的伙伴谈自己的学习路径、专业背景与带领经验，让不同实践者的声音逐步被看见。</p></article><article><small>IN DEVELOPMENT</small><h3>家庭与青少年情商学习</h3><p>围绕家长和青少年的不同需要，调研并共创体验式学习内容；具体形式与时间仍在形成中。</p></article></div><div class="eq-project-links"><a class="text-link" href="book-eq-coach.html">从《情商教练手册》继续阅读 ↗</a><a class="text-link" href="index.html#contact">联系课程与合作 ↗</a></div></div></section>'''
    page(
        "米杉本性情商培训师联盟",
        "认识米杉本性情商培训师联盟：北京一、二阶课堂、导师与实践带领者、情商教育主题和正在共创的项目。",
        "eq-alliance.html", body, "courses.html", "assets/beijing-eq-2026.jpg",
    )


if __name__ == "__main__":
    build_level_one()
    build_alliance()
