"""Curated web editions of articles already published by 扎根本性."""

from build_content import page, hero, section_head
from html import escape


PRINCIPLES_2024 = [
    ("自我负责", "把关注带回自己的体验与选择。", "来访创造了其自身现实。变化来自内在。咨询过程完全以来访为中心。"),
    ("全然临在", "回到此时此地，辨认身体里的感受。", "把问题识别为身体里的感受，此时此地，对感受全然敞开。"),
    ("年龄回溯", "倾听当下感受可能连着的早期经验。", "探索我们受伤感受源点的一种方式，深度聆听受伤的内在空间。"),
    ("去除认同", "辨认受伤状态，同时认识自己不只等于它。", "去除对内在受伤空间的认同；转换内在空间，认同有力量的自我。"),
    ("转化能量", "从有资源的内在位置回应受伤部分。", "通过拥抱受伤的内在空间如同是我们自身内在的小孩一般，转化未解决的情绪能量。"),
    ("锚定内核", "熟悉能够接纳与支持自己的内在状态。", "进一步锚定本性和认同内在父母。"),
    ("整合变化", "把内在工作带回日常行动。", "澄清需要和目标，制定具体实操步骤，以便在日常生活中落实内在转化成果。"),
]


def principle_sections():
    jumps = ''.join(f'<a href="#principle-{i}">{escape(title)}</a>' for i, (title, _, _) in enumerate(PRINCIPLES_2024, 1))
    cards = ''.join(f'<article id="principle-{i}"><span>{i:02d}</span><h3>{escape(title)}</h3><p>{escape(summary)}</p><details><summary>阅读米杉原文</summary><blockquote>{escape(original)}</blockquote></details></article>' for i, (title, summary, original) in enumerate(PRINCIPLES_2024, 1))
    return f'<nav class="principle-jumps" aria-label="本性治疗七原则">{jumps}</nav><div class="principle-cards">{cards}</div>'


ARTICLES = [
    {
        "path": "article-essence.html", "category": "方法 / APPROACH",
        "title": "本性治疗：从身体感受到内在空间",
        "summary": "米杉 2024 年更新的论述，回答这套方法从哪里进入、怎样认识内在资源。",
        "credit": "米杉《什么是本性治疗》 · 倪男奇译",
        "body": '''
        <h2>本性治疗的方法定位</h2>
        <p>米杉把本性治疗定义为一种以身体为中心、采用超个人心理学视角的心理咨询方法。咨询师除了倾听和支持，还会引导来访者进入内在过程，辨认不同的内在空间，并对当下呈现的体验进行工作。</p>
        <p>这里的“内在空间”，主要指两种状态：一种承载受伤的感受、记忆与习惯性的反应；另一种能够提供支持、接纳和选择，被米杉称为资源性的内在空间，也常用“内在父母”来说明。</p>
        <h2>身体感受作为工作入口</h2>
        <p>一个人可以知道自己为什么焦虑，却仍在某些场景里反复紧张。本性治疗不把“明白道理”当作工作的终点。它邀请人注意：当此刻说起这件事，胸口、呼吸、肩背或腹部有什么感受？这种感受怎样变化？</p>
        <p>对身体经验保持觉察，是识别受伤空间的入口。之后，咨询师可能引导来访者倾听相关经历，也可能帮助其联结较有力量的内在状态。年龄回溯是其中一种工具，并非每次咨询都必须进行。</p>
        <h2>资源性内在空间</h2>
        <p>资源不是一句安慰自己的口号，而是人实际能够体验到的稳定、关怀、信心和选择能力。米杉认为，工作的一项关键，是帮助来访者逐步辨认受伤的状态，同时不把它等同于“全部的我”。从更有资源的状态出发，人才能以新的方式回应内在的伤痛。</p>
        <h2>将变化整合到日常</h2>
        <p>一次内在体验可能带来新的理解，但整合仍需要具体行动：澄清自己的需要、决定下一次怎样表达，或在熟悉的关系里尝试不同的回应。米杉把这一环节列为七原则的最后一步。</p>
        <div class="article-callout"><strong>继续读</strong><p>想看完整论述与方法脉络，可从《由心咨询》和《内在父母与内在小孩的拥抱》开始。想继续深入，可从米杉的原著与专业训练入手。</p><a href="reading.html">查看米杉著作 ↗</a></div>'''
    },
    {
        "path": "article-principles.html", "category": "方法 / PRINCIPLES",
        "title": "七个原则，怎样从概念走向练习",
        "summary": "把米杉公开文章中的七原则放回工作过程，说明早期表述与 2024 年版本的差异。",
        "credit": "米杉《本性治疗的七个原则》《什么是本性治疗》",
        "body": '''
        <h2>七原则的实践脉络</h2>
        <p>米杉在公开文章里强调：本性治疗的重点，是帮助来访者体验并整合一套内在工作的能力。它涉及责任、当下的身体感受、受伤与资源性空间，以及把变化带回生活。把七条背熟，并不等于已经掌握工作方法。</p>
        <div class="article-steps"><div><b>01</b><h3>自我负责</h3><p>先把关注带回自己的体验与选择。它指向可以做的内在工作，不应被用来责备受伤的人。</p></div><div><b>02</b><h3>全然临在</h3><p>回到此时此地，辨认情绪在身体里的具体感受。</p></div><div><b>03</b><h3>年龄回溯</h3><p>当有需要且具备安全条件时，倾听当下感受可能连着的早期经验。</p></div><div><b>04</b><h3>去除认同</h3><p>辨认“我正处于受伤状态”，同时意识到自己并不只等于这个状态。</p></div><div><b>05</b><h3>转化能量</h3><p>从有资源的内在位置接近和回应受伤部分，而非压下感受。</p></div><div><b>06</b><h3>锚定内核</h3><p>进一步熟悉能够接纳、支持和作出选择的内在状态。</p></div><div><b>07</b><h3>整合变化</h3><p>澄清需要与目标，找出生活里下一步可实践的行动。</p></div></div>
        <h2>早期与 2024 年表述的区别</h2>
        <p>较早发表的《本性治疗的七个原则》，依次写作“承担责任、锚定、回到当下、放大、去除认同、转化、整合变化”。2024 年更新论述则使用上文的“自我负责、全然临在、年龄回溯、去除认同、转化能量、锚定内核、整合变化”。两个版本有共同的核心，但侧重点和顺序不同。两组表述呈现了米杉对工作步骤的不同侧重；学习操作时，仍需理解各环节之间的联系。</p>
        <div class="article-callout"><strong>进一步学习</strong><p>先认识身体感受，再辨认两个内在空间，最后思考生活中的具体行动。涉及回溯与强烈情绪时，应在具备相应训练的带领下开展。</p><a href="approach.html">认识本性治疗 ↗</a></div>'''
    },
    {
        "path": "article-regression.html", "category": "实践 / REGRESSION",
        "title": "心理咨询一定要回到过去吗？",
        "summary": "本性团队的经典释疑：什么时候回看过往可能有帮助，什么时候应先处理眼前的需要。",
        "credit": "本性团队《心理咨询一定要“挖”过去吗？》",
        "body": '''
        <h2>回溯不是每次咨询的必经步骤</h2>
        <p>有些困扰与眼前的现实条件有关，比如工作安排、沟通或近期压力，直接处理当下的问题就可能更有帮助。对刚经历重大事件、尚未稳定下来的人，先建立安全感与日常支持通常更重要。</p>
        <p>本性团队在公众号文章里提出的判断是：回看过去，是否有助于理解当下反复出现的感受，并为改变打开空间？这个问题比“必须挖到多早”更实际。</p>
        <h2>可能需要回溯的情形</h2>
        <p>当类似的关系模式不断重现，或一次普通的批评引发远超眼前事件的强烈反应，咨询师可能会和来访者一起留意：这种熟悉的感受是否与更早的经验相关。理解背景有其价值，但本性治疗不会只停在原因分析上。</p>
        <h2>本性治疗中的年龄回溯</h2>
        <p>在本性治疗里，年龄回溯是从当下感受进入内在工作的一个方法。它试着在相对安全、稳定的条件下，倾听过去未得到充分回应的感受，并练习从更有资源的内在状态与之相处。是否使用、何时停下，都要根据来访者的状态和边界判断。</p>
        <h2>回到当下的生活选择</h2>
        <p>回看过去的意义，是帮助人更清楚地理解自己在现在的反应，并在现实生活里获得更多选择。具体能否受益，因人和情境而异。若正在经历明显的心理危机，宜先寻求合适的专业支持。</p>
        <div class="article-callout"><strong>继续读</strong><p>关于回溯与“内在小孩”的更完整论述，可参看米杉原著与本性团队已公开文章。</p><a href="book-inner-child.html">了解相关著作 ↗</a></div>'''
    },
    {
        "path": "article-dreams.html", "category": "实践 / DREAM WORK",
        "title": "梦工作：先倾听，再理解",
        "summary": "从倪男奇的公开文章出发，介绍记梦、听梦、转译和内在工作四个环节。",
        "credit": "倪男奇《来访者主动提起梦时才进行梦工作？》",
        "body": '''
        <h2>梦境作为内在工作的素材</h2>
        <p>一个梦可能带着强烈的感受，也可能呈现梦主尚未注意到的关系和资源。倪男奇在公众号文章中提出，咨询师可以开放地邀请来访者留意、记录梦，但邀请不等于要求，更不意味着所有梦都需要解释。</p>
        <h2>梦工作的四个环节</h2>
        <div class="article-steps"><div><b>01</b><h3>邀请记梦</h3><p>梦醒后记下人物、场景、事件与身体感受，先保留细节。</p></div><div><b>02</b><h3>倾心听梦</h3><p>让梦主把梦讲完整；必要时询问遗漏之处，先不急于下解释。</p></div><div><b>03</b><h3>转译梦境</h3><p>探索梦中的形象对梦主本人意味着什么。梦主的经验与理解不可被一个通用的“解梦字典”替代。</p></div><div><b>04</b><h3>进入内在工作</h3><p>若梦触及重要感受，才进一步探索它与现实议题、内在资源的关系。</p></div></div>
        <h2>梦主的经验是理解梦境的基础</h2>
        <p>同一人物或物件，在不同人的梦里可能意义完全不同。倪男奇强调，梦主对梦境意义有最终的发言权。咨询师的工作是帮助对方更准确地辨认线索，而不是替他宣布结论。</p>
        <p>公开文章还提醒：明白隐喻只是工作的一部分。梦中浮现的情绪如何被感受，可能的资源怎样支持现实中的行动，也需要在互动中继续探索。</p>
        <div class="article-callout"><strong>继续读</strong><p>想从米杉的原著系统了解梦工作，可读《梦的真相》。梦的讨论应尊重梦主的隐私和节奏。</p><a href="book-dream.html">了解《梦的真相》 ↗</a></div>'''
    },
]


def build():
    cards = ''.join(
        f'<a class="article-card reveal" href="{a["path"]}"><small>{a["category"]}</small><h3>{a["title"]}</h3><p>{a["summary"]}</p><span>阅读全文 ↗</span></a>'
        for a in ARTICLES
    )
    body = hero("SELECTED ARTICLES", "公众号文章选读", "从方法原理到梦工作与年龄回溯，循着具体问题继续阅读。", "经典文章")
    body += f'''<section class="section-space editorial-list"><div class="container">{section_head('FROM OUR ARCHIVE', '经典文章', '围绕本性治疗、七原则、年龄回溯和梦工作展开。')}<div class="article-grid">{cards}</div><p class="source-note">更多文章可在微信公众号「扎根本性」阅读。<a href="https://weixin.qq.com/r/QBPG3qvE6vaVre_990ZS" target="_blank" rel="noopener">打开公众号 ↗</a></p></div></section>'''
    page("经典文章", "米杉与本性团队在公众号已发表的本性治疗、七原则、年龄回溯和梦工作文章。", "insights.html", body)

    for a in ARTICLES:
        body = hero(a["category"], "本性治疗：<br>感受与内在空间" if a["path"] == "article-essence.html" else a["title"], a["summary"], "经典文章")
        article_body = a["body"]
        if a["path"] == "article-principles.html":
            start = article_body.index('<div class="article-steps">')
            end = article_body.index('<h2>早期与 2024 年表述的区别</h2>')
            article_body = article_body[:start] + principle_sections() + article_body[end:]
        body += f'''<section class="section-space article-layout"><div class="container article-shell"><aside class="article-side"><span>扎根本性 · 文章选读</span><a href="insights.html">← 返回文章目录</a></aside><article class="article-prose"><p class="article-credit">{a["credit"]}</p>{article_body}<footer class="article-source"><p>更多原著论述与文章，可在公众号「扎根本性」继续阅读。</p><a href="https://weixin.qq.com/r/QBPG3qvE6vaVre_990ZS" target="_blank" rel="noopener">打开公众号 ↗</a></footer></article></div></section>'''
        page(a["title"], a["summary"], a["path"], body, "insights.html")


if __name__ == "__main__":
    build()
