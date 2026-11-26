"""Build the public subject guide from reviewed site content."""

from html import escape as esc

from build_content import hero, page


TOPICS = [
    {
        "id": "method", "label": "THE METHOD", "title": "本性治疗的方法",
        "intro": "从当下的身体感受进入，辨认受伤与资源性的内在空间，再思考怎样把内在工作落实到生活。以下资料分别说明方法定义、工作原则、原著论述与现场学习。",
        "image": "assets/books/heart-front-web.jpg", "alt": "米杉《由心咨询》中文出版封面",
        "resources": [
            ("方法论述", "本性治疗：从身体感受到内在空间", "阅读米杉 2024 年更新论述的中文导读。", "article-essence.html"),
            ("方法结构", "七个原则，怎样进入实践", "区分当下体验、资源联结与生活整合。", "article-principles.html"),
            ("中文著作", "《由心咨询》", "从原著认识咨询关系、工作原则与超个人视角。", "book-heart.html"),
            ("现场学习", "本性治疗一阶", "查看学习对象、课程主题、练习形式与当期安排。", "course-level-one.html"),
        ],
    },
    {
        "id": "dream", "label": "DREAM WORK", "title": "梦工作",
        "intro": "梦境的形象需要放回梦主自己的经验中理解。记梦、倾听、转译与内在工作构成一条探索路径；梦主的感受和现实处境比套用固定解释更重要。",
        "image": "assets/books/dream-new.jpg", "alt": "米杉《梦的真相》中文出版封面",
        "resources": [
            ("文章", "梦工作：先倾听，再理解", "从公开文章了解记梦、听梦和转译的基本顺序。", "article-dreams.html"),
            ("中文著作", "《梦的真相》", "系统阅读梦的语言、释梦过程与内在工作。", "book-dream.html"),
            ("教学记录", "2005 年北京首个梦工作坊", "了解梦工作在中国的早期实践。", "archive.html#dream-2005"),
            ("现场学习", "米杉梦工作坊", "查看梦境转译、示范与小组练习的当期安排。", "course-dream.html"),
        ],
    },
    {
        "id": "education", "label": "EMOTIONAL EDUCATION", "title": "情商教育与养育",
        "intro": "米杉的情绪与社会性教育工作面向不同年龄与场景。中文著作从教育者的活动设计，延伸到儿童成长和家庭关系；阅读时可按实践场景选择入口。",
        "image": "assets/books/eq-coach.jpg", "alt": "米杉《情商教练手册》中文出版封面",
        "resources": [
            ("教育者", "《情商教练手册》", "阅读团体活动、情绪表达与社会性学习的设计。", "book-eq-coach.html"),
            ("儿童教育", "《儿童情商教育》", "了解面向儿童的情绪与社会性学习主题。", "book-child-eq.html"),
            ("家庭养育", "《育儿先育己》", "从照顾者自身的觉察进入亲子关系。", "book-parenting.html"),
            ("教学记录", "北京印刷学院情商课程", "查看 2006—2007 年两期高校课程的资料。", "archive.html#eq-class-2006"),
        ],
    },
    {
        "id": "history", "label": "THE PUBLIC RECORD", "title": "米杉与在华教学",
        "intro": "人物介绍、著作和课程历程相互补充。高校公开资料记录了米杉在中国的讲座计划与专业培训；近年的课程信息帮助读者理解不同阶段的现场学习。",
        "image": "assets/michel-claeys-mobile.jpg", "alt": "本性治疗创始人米杉",
        "resources": [
            ("人物", "认识米杉", "阅读米杉的专业经历、中文著作和教学方向。", "teacher.html"),
            ("历程", "在中国的教学记录", "按年份、城市和主题查看已核实的公开节点。", "archive.html"),
            ("高校报道", "2010 年华侨大学专业培训", "校方报道记录了五天指导中的七原则与梦工作。", "https://www.hqu.edu.cn/info/1073/14191.htm"),
            ("高校预告", "2013 年北京师范大学梦主题讲座", "查看校方发布的讲座预告。", "https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html"),
        ],
    },
]


def resource_card(kind, title, description, url):
    external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
    return (f'<a class="guide-resource" href="{esc(url)}"{external}>'
            f'<span class="guide-resource-kind">{esc(kind)}</span><h3>{esc(title)}</h3>'
            f'<p>{esc(description)}</p><span class="guide-resource-action">阅读资料</span></a>')


def build():
    body = hero("A GUIDE TO THE WORK", "专题阅读", "沿着方法、梦工作、情商教育与教学记录，阅读米杉的著作和已公开资料。", "专题阅读")
    jumps = "".join(f'<a href="#guide-{t["id"]}">{esc(t["title"])}<span aria-hidden="true">↗</span></a>' for t in TOPICS)
    body += f'''<section class="guide-opening section-space"><div class="container guide-opening-grid"><div><p class="eyebrow"><span class="eyebrow-line"></span>READING PATHS</p><h2>从一个主题开始，<br>把资料连接起来。</h2></div><div><p>同一个主题可以从文章、原著、教学记录和课程四个层次阅读。选择你关心的方向，再进入具体资料。</p><nav class="guide-jumps" aria-label="选择专题">{jumps}</nav></div></div></section>'''
    for index, topic in enumerate(TOPICS):
        resources = "".join(resource_card(*row) for row in topic["resources"])
        tone = " guide-topic-alt" if index % 2 else ""
        body += f'''<section class="guide-topic section-space{tone}" id="guide-{topic['id']}"><div class="container guide-topic-grid"><div class="guide-topic-intro"><p class="eyebrow"><span class="eyebrow-line"></span>{esc(topic['label'])}</p><h2>{esc(topic['title'])}</h2><p>{esc(topic['intro'])}</p><figure class="guide-topic-image"><img src="{esc(topic['image'])}" alt="{esc(topic['alt'])}" loading="lazy"></figure></div><div class="guide-resource-grid">{resources}</div></div></section>'''
    body += '''<section class="guide-outro section-space"><div class="container guide-outro-grid"><div><p class="eyebrow eyebrow-light"><span class="eyebrow-line"></span>CONTINUE READING</p><h2>回到原著与现场。</h2><p>专题导读帮助找到入口。更完整的方法论述请阅读原著；课程的具体安排与咨询方式见当期课程页。</p></div><div class="guide-outro-actions"><a class="button button-cream" href="reading.html">浏览中文著作</a><a class="text-link text-link-light" href="courses.html">查看课程</a></div></div></section>'''
    page("专题阅读", "按本性治疗、梦工作、情商教育与在华教学四个主题，进入米杉著作、公开文章、课程与高校资料。", "guide.html", body)


if __name__ == "__main__":
    build()
