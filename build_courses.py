"""Build course pages from the confirmed 2027 spring fact table."""

from html import escape as E

from build_content import page, hero, section_head


COURSES = [
    {
        "path": "course-level-one.html", "title": "本性治疗一阶", "theme": "从身体感受开始，认识本性治疗的核心方法。",
        "kind": "本性治疗 · 入门", "city": "杭州", "date": "2027 年 4 月 16—18 日", "weekday": "周五至周日",
        "price": "¥3,980", "regular": "¥5,800", "deadline": "2027 年 3 月 15 日", "poster": "course-level-1.jpg",
        "summary": "从超个人心理学的整合视角出发，以身体感受为入口，学习辨认内在空间、理解内在小孩工作与内在父母资源。",
        "audience": "希望系统认识本性治疗的学习者；从事心理咨询、教育或其他助人工作的伙伴，也可从一阶建立共同的方法语言。",
        "topics": ["认识本性治疗的超个人心理学视角与整合性方法。", "从身体感受出发，辨认当下的情绪反应和不同的内在空间。", "理解内在小孩的工作方法，学习联结与锚定内在父母资源。", "通过现场示范与小组练习，认识本性治疗的核心流程。"],
        "format": "米杉现场带领，结合方法讲授、示范与小组实操；围绕身体感受、内在小孩与内在父母资源展开学习。",
        "goal": "建立对身体感受和内在空间的初步辨认能力，理解本性治疗如何从体验进入工作。",
        "next": "一阶之后，可结合学习目标继续阅读米杉原著，并了解二阶、梦工作或练习督导的安排。",
        "related": "book-heart.html", "related_name": "《由心咨询》",
    },
    {
        "path": "course-dream.html", "title": "米杉梦工作坊", "theme": "从梦境元素出发，学习理解与转译。",
        "kind": "梦工作 · 专题", "city": "郑州", "date": "2027 年 4 月 23—25 日", "weekday": "周五至周日",
        "price": "¥3,980", "regular": "¥5,800", "deadline": "2027 年 3 月 22 日", "poster": "course-dream.jpg",
        "summary": "从梦者自己的经验出发，学习理解梦境中的人物、场景与情绪，并以梦为素材探索内在空间。",
        "audience": "对梦的理解与梦工作有兴趣的学习者，以及希望把梦带入个人成长或专业学习的伙伴。",
        "topics": ["记录梦境，并辨认其中的人物、场景与情绪。", "在梦者自身的生活语境中理解与转译梦境元素。", "探索梦与受伤、资源性内在空间的联系。"],
        "format": "从梦者带来的梦出发，结合讲解、现场示范与小组交流，练习倾听梦、理解梦境元素，并把认识带回个人经验。",
        "goal": "认识以梦者经验为中心的梦工作路径，练习从梦境线索进入内在探索。",
        "next": "梦工作可与本性治疗方法互相参照。继续学习时，可阅读《梦的真相》或了解其他工作坊。",
        "related": "book-dream.html", "related_name": "《梦的真相》",
    },
    {
        "path": "course-level-two.html", "title": "本性治疗二阶", "theme": "在一阶基础上，深化内在工作的理解与练习。",
        "kind": "本性治疗 · 深化", "city": "郑州", "date": "2027 年 5 月 2—5 日", "weekday": "周日至周三",
        "price": "¥5,980", "regular": "¥7,800", "repeat": "¥3,900", "deadline": "2027 年 3 月 31 日", "poster": "course-level-2.jpg",
        "summary": "在一阶基础上，进一步学习年龄回溯、情绪转化与认知重构，并通过小组练习、个案演示和现场督导反馈深化方法。",
        "audience": "已有本性治疗一阶学习基础、希望继续深化方法练习的伙伴。具体学习基础可在报名前咨询。",
        "topics": ["在已有基础上，深化从身体感受进入内在工作的流程。", "学习年龄回溯、情绪转化与认知重构等方法。", "通过个案演示，观察这些方法如何用于具体工作情境。", "结合小组练习与现场督导反馈，辨认操作中的关键环节。"],
        "format": "小组练习、个案演示与现场督导反馈相结合。课程强调在具体情境中理解方法、练习操作并获得反馈。",
        "goal": "在已有的一阶经验上，提高对内在过程的观察与理解，继续练习方法的应用。",
        "next": "方法学习需要持续实践与反馈；可结合阅读、练习和督导继续巩固。",
        "related": "book-inner-child.html", "related_name": "《内在父母与内在小孩的拥抱》",
    },
]


def course_tile(item):
    return f'''<article class="course-hub-card"><p class="micro-en">{E(item['kind'])}</p><h3><a href="{item['path']}">{E(item['title'])}</a></h3><p>{E(item['summary'])}</p><div class="course-hub-facts"><span>{E(item['date'])}</span><span>{E(item['city'])}</span></div><a class="text-link" href="{item['path']}">查看课程详情 ↗</a></article>'''


def build_hub():
    body = hero("COURSES & PRACTICE", "课程与学习路径", "认识本性治疗、梦工作与情商教育的不同学习路径，并查看当前课程安排。", "课程")
    body += f'''<section class="section-space course-hub-intro"><div class="container course-intro-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>HOW WE LEARN</p><h2>阅读、示范、练习与持续复盘</h2></div><div><p>本性治疗的学习从概念进入体验：阅读著作和公开文章，理解身体感受与内在空间；在工作坊中观看示范、参加练习，并在课后继续实践与复盘。</p><p>不同课程有各自的重点。一阶建立基础，梦工作以梦境为入口，二阶在已有学习经验上深化方法。</p></div></div></section>
<section class="section-space course-hub-section" id="spring-2027"><div class="container">{section_head('SPRING 2027', '2027 春季课程', '点击课程查看适合对象、学习内容、时间地点与报名咨询方式。')}<div class="course-hub-grid">{''.join(course_tile(item) for item in COURSES)}</div><a class="text-link course-hub-schedule" href="assets/spring-2027-schedule.png" target="_blank" rel="noopener">查看春季总课表 ↗</a></div></section>
<section class="section-space eq-course-bridge"><div class="container">{section_head('EMOTIONAL INTELLIGENCE', '情商教育与带领实践', '从北京一阶的六天体验式学习，走向二阶主题设计和学员现场带领。')}<div class="eq-course-bridge-grid"><a href="course-eq-level-one.html"><img src="assets/eq1-beijing-group-practice-2026.jpg" alt="2026 年北京情商一阶团体活动" loading="lazy"><div><small>2026 · BEIJING</small><h3>情商教育培训师一阶</h3><p>阅读六天的学习主题与课堂记录。</p><span>了解一阶 ↗</span></div></a><a href="eq-alliance.html"><img src="assets/beijing-eq-2026.jpg" alt="2026 年北京情商二阶班级合影" loading="lazy"><div><small>TRAINERS & PRACTICE</small><h3>米杉本性情商培训师联盟</h3><p>走进教学现场、实践带领者与正在共创的项目。</p><span>认识联盟 ↗</span></div></a></div></div></section>
<section class="section-space course-path"><div class="container">{section_head('A CONTINUING PRACTICE', '课程之外，学习仍在继续')}<div class="course-path-grid"><a href="reading.html"><span>01</span><h3>从著作建立认识</h3><p>米杉中文著作分别讨论本性治疗、梦工作、情商教育与养育。</p><b>浏览著作 ↗</b></a><a href="archive.html"><span>02</span><h3>从历程认识现场</h3><p>了解筑基班、工作坊和情商培训师认证班的公开教学记录。</p><b>查看教学历程 ↗</b></a><a href="index.html#contact"><span>03</span><h3>咨询适合的学习入口</h3><p>课程阶段和个人学习基础不同，可先联系小扎了解具体安排。</p><b>联系课程咨询 ↗</b></a></div></div></section>'''
    page("课程与学习路径", "查看米杉本性治疗、梦工作与情商教育的学习路径，以及 2027 春季课程安排。", "courses.html", body)


def build_detail(item):
    topics = "".join(f"<li>{E(topic)}</li>" for topic in item["topics"])
    repeat_price = f'<div><dt>复训价</dt><dd>{E(item["repeat"])}<small>适用资格请咨询</small></dd></div>' if item.get("repeat") else ""
    body = hero("SPRING 2027 / COURSE", E(item["title"]), E(item["theme"]), "课程")
    body += f'''<section class="section-space course-detail-intro"><div class="container course-detail-grid"><div class="course-detail-main"><p class="eyebrow"><span class="eyebrow-line"></span>{E(item['kind'])}</p><h2>课程概览</h2><p class="lead">{E(item['summary'])}</p><h3>适合谁学习</h3><p>{E(item['audience'])}</p><h3>课程中学什么</h3><ul>{topics}</ul><h3>学习方式</h3><p>{E(item['format'])}</p><h3>学习目标</h3><p>{E(item['goal'])}</p><h3>接下来可以怎样学</h3><p>{E(item['next'])}</p><a class="text-link" href="{item['related']}">相关著作：{E(item['related_name'])} ↗</a></div>
<aside class="course-facts" aria-label="课程安排"><p class="micro-en">AT A GLANCE</p><h2>{E(item['title'])}</h2><dl><div><dt>时间</dt><dd>{E(item['date'])}<small>{E(item['weekday'])}</small></dd></div><div><dt>城市</dt><dd>{E(item['city'])}</dd></div><div><dt>带领</dt><dd>米杉</dd></div><div><dt>早鸟价</dt><dd>{E(item['price'])}<small>截止 {E(item['deadline'])}</small></dd></div><div><dt>原价</dt><dd>{E(item['regular'])}</dd></div>{repeat_price}</dl><a class="button button-dark" href="#course-inquiry">咨询报名 <span aria-hidden="true">↗</span></a></aside></div></section>
<section class="section-space course-poster-section"><div class="container course-poster-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>COURSE POSTER</p><h2>查看课程海报</h2><p>课程日期、地点与费用可在海报中查看。报名时请联系小扎确认具体地点与课程安排。</p><a class="text-link" href="assets/{item['poster']}" target="_blank" rel="noopener">打开海报原图 ↗</a></div><a href="assets/{item['poster']}" target="_blank" rel="noopener"><img src="assets/{item['poster']}" alt="{E(item['title'])}课程海报" loading="lazy"></a></div></section>
<section class="section-space course-inquiry" id="course-inquiry"><div class="container course-inquiry-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>ENQUIRY & REGISTRATION</p><h2>咨询课程与报名</h2><p>微信扫码联系小扎，说明想了解的课程。可进一步确认学习基础、课程地点、名额与报名方式。</p><a class="text-link" href="courses.html">返回全部课程 ↗</a></div><a class="consult-qr-image" href="assets/contact-wechat.jpg" target="_blank" rel="noopener" aria-label="打开小扎课程咨询二维码原图"><img src="assets/contact-wechat.jpg" alt="小扎微信课程咨询二维码" loading="lazy"></a></div></section>'''
    page(item["title"], f"米杉{item['title']}：{item['date']}在{item['city']}举办。了解学习内容、适合对象、费用和报名咨询方式。", item["path"], body, "courses.html", f"assets/{item['poster']}")


if __name__ == "__main__":
    build_hub()
    for course in COURSES:
        build_detail(course)
