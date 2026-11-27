"""Public 2026 Level II classroom roster and reviewed short introductions.

The source roster is the 22 person facilitation schedule. Background labels
come from 2026 application forms or corroborated public reports; classroom
descriptions come from recorded activity headings. No assessment, score,
personal disclosure or certification decision is included here.
"""

BACKGROUNDS = {
    "legal": ("法律工作与婚姻家庭课程", "Legal practice and family education", "Pratique juridique et éducation familiale"),
    "education": ("教育与青少年发展", "Education and youth development", "Éducation et développement des jeunes"),
    "helping": ("心理与助人工作", "Psychological support and helping practice", "Accompagnement psychologique et relation d'aide"),
    "family": ("家庭教育与个人成长", "Family education and personal development", "Éducation familiale et développement personnel"),
    "group": ("成长团体带领", "Personal development group facilitation", "Animation de groupes de développement personnel"),
    "children": ("儿童团体与家长课程", "Children's groups and parent education", "Groupes d'enfants et formation des parents"),
    "university": ("高校教学与学生发展", "University teaching and student development", "Enseignement supérieur et développement des étudiants"),
    "courses": ("本性课程与内容协作", "Essence course and editorial collaboration", "Collaboration pédagogique et éditoriale Essence"),
    "teachers": ("教师成长与团体培训", "Teacher development and group training", "Formation d'enseignants et animation de groupes"),
    "eq": ("情商教育与家长课程", "Emotional education and parent programs", "Éducation émotionnelle et programmes pour parents"),
    "public_youth": ("未成年人心理辅导与公益实践", "Youth counseling and community practice", "Accompagnement psychologique des jeunes et action de proximité"),
    "public_teacher": ("青少年情商教育与教师培训", "Emotional education for youth and teacher training", "Éducation émotionnelle des jeunes et formation des enseignants"),
    "public_university": ("高校心理咨询与教学", "University counseling and teaching", "Accompagnement psychologique et enseignement à l'université"),
    "classroom": ("2026 北京二阶课堂实践", "2026 Beijing Level II classroom practice", "Pratique en classe au niveau II à Pékin en 2026"),
}

# Public, independently readable pages that match both the participant's name
# and the professional context recorded in the local application materials.
PUBLIC_LINKS = {
    "符春燕": ("https://hn.rednet.cn/content/2020/12/09/8691545.html", "阅读公益辅导报道 ↗", "Read the community report ↗", "Lire le reportage sur l'action de proximité ↗"),
    "田秭萁": ("https://m.sohu.com/a/1022185693_121124527", "阅读教师培训报道 ↗", "Read the teacher training report ↗", "Lire le reportage sur la formation des enseignants ↗"),
    "李东艳": ("https://bm.cugb.edu.cn/xgb/c/2015-11-17/725582.shtml", "阅读高校讲座资料 ↗", "Read the university lecture notice ↗", "Lire l'annonce de la conférence universitaire ↗"),
}

# day, name, romanization, background code, topic (zh/en/fr), activity (zh/en/fr)
PEOPLE = [
    (1, "王建华", "Wang Jianhua", "legal", ("团队合作", "Teamwork", "Coopération d'équipe"),
     ("以职场猜词和合作练习，引导团体观察表达、分工与相互支持。", "Word games and cooperative exercises invited the group to notice communication, shared tasks and mutual support.", "Des jeux de mots et des exercices coopératifs ont invité le groupe à observer la communication, le partage des tâches et l'entraide.")),
    (1, "李江红", "Li Jianghong", "education", ("自由行走、信任圈与拍打", "Movement, trust and rhythm", "Mouvement, confiance et rythme"),
     ("从自由行走和信任圈开始，让参与者在团体活动中体验身体与信任。", "Free movement and a trust circle helped participants explore bodily experience and trust in a group.", "La marche libre et un cercle de confiance ont permis d'explorer l'expérience corporelle et la confiance dans le groupe.")),
    (1, "符春燕", "Fu Chunyan", "public_youth", ("信任与共创", "Trust and co-creation", "Confiance et cocréation"),
     ("通过蒙眼唤名等练习，探索信任如何在同伴之间逐步形成。", "Blindfolded name calling and other exercises explored how trust gradually forms among peers.", "Des exercices d'appel par le prénom les yeux bandés ont exploré la construction progressive de la confiance entre pairs.")),
    (2, "王凝初", "Wang Ningchu", "classroom", ("接纳亲密关系中的差异", "Accepting difference in close relationships", "Accueillir les différences dans les relations proches"),
     ("用联想与互动活动，带领团体观察亲密关系中的期待和差异。", "Association and interactive activities invited reflection on expectations and differences in close relationships.", "Des activités d'association et d'interaction ont invité à réfléchir aux attentes et aux différences dans les relations proches.")),
    (2, "赖炜", "Lai Wei", "helping", ("情绪识别与自我放松", "Recognizing emotions and relaxing", "Reconnaître les émotions et se détendre"),
     ("从身体体验进入情绪识别，练习在压力中重新找到放松的方式。", "The session began with bodily experience to identify emotions and practise relaxation under stress.", "L'atelier est parti de l'expérience corporelle pour reconnaître les émotions et retrouver la détente face au stress.")),
    (2, "江劭瀚", "Jiang Shaohan", "family", ("感受信任", "Experiencing trust", "Éprouver la confiance"),
     ("以慢动作和团体互动，探索信任在关系中的感受与变化。", "Slow movement and group interaction explored how trust is felt and changes in relationships.", "Le mouvement lent et l'interaction de groupe ont permis d'explorer la confiance vécue dans la relation.")),
    (2, "田秭萁", "Tian Ziqi", "public_teacher", ("觉察与注意力", "Awareness and attention", "Conscience de soi et attention"),
     ("借助手指舞与画面观察，分辨直接看见的事实和随后出现的判断。", "Finger movements and image observation helped distinguish what is seen from the judgments that follow.", "Les mouvements des doigts et l'observation d'images ont aidé à distinguer ce qui est vu des jugements qui suivent.")),
    (3, "台燕", "Tai Yan", "group", ("应该与期待", "The weight of shoulds and expectations", "Le poids des « il faut » et des attentes"),
     ("从团体游戏出发，观察内心的“应该”和期待如何影响选择。", "Group activities invited participants to notice how inner shoulds and expectations shape their choices.", "Des activités de groupe ont permis d'observer comment les « il faut » et les attentes orientent les choix.")),
    (3, "何明月", "He Mingyue", "children", ("欢迎情绪，听见需要", "Welcoming emotions and hearing needs", "Accueillir les émotions et entendre les besoins"),
     ("以“情绪天气预报”开启分享，让感受与心理需要获得更清楚的语言。", "An emotional weather report opened a conversation about feelings and underlying psychological needs.", "Une « météo des émotions » a ouvert un échange sur les ressentis et les besoins psychologiques sous-jacents.")),
    (3, "王尹琪", "Wang Yinqi", "classroom", ("听见需要", "Hearing needs", "Entendre les besoins"),
     ("用分组游戏与讨论，探索一个人怎样表达并听见自己的需要。", "Group games and discussion explored how people express and hear their own needs.", "Des jeux de groupe et des échanges ont exploré la manière d'exprimer et d'entendre ses propres besoins.")),
    (3, "杨锴毓", "Yang Kaiyu", "courses", ("超越评判", "Beyond judgment", "Au-delà du jugement"),
     ("通过互动体验，辨认观察、解释与评判之间的差别。", "Interactive exercises helped distinguish observation, interpretation and judgment.", "Des exercices interactifs ont aidé à distinguer observation, interprétation et jugement.")),
    (4, "边永卫", "Bian Yongwei", "classroom", ("看见、允许与转化情绪", "Seeing, allowing and transforming emotion", "Voir, accueillir et transformer les émotions"),
     ("借助情绪卡与生活场景，练习辨认感受并与自己建立联系。", "Emotion cards and everyday scenarios supported the practice of recognizing feelings and reconnecting with oneself.", "Des cartes d'émotions et des situations quotidiennes ont aidé à reconnaître ses ressentis et à renouer avec soi-même.")),
    (4, "李东艳", "Li Dongyan", "public_university", ("与连接感同行", "Exploring the sense of connection", "Explorer le sentiment de lien"),
     ("从呼吸、绘画和身体雕塑进入，探索人与自我及他人的连接。", "Breathing, drawing and body sculpture became ways to explore connection with self and others.", "La respiration, le dessin et la sculpture corporelle ont servi à explorer le lien avec soi et les autres.")),
    (4, "何菲", "He Fei", "education", ("家庭关系中的紧张体验", "Tension in family relationships", "Les tensions dans les relations familiales"),
     ("以家庭关系中的紧张感为主题，组织一场体验式课堂活动。", "The session explored felt tension in family relationships through experiential activities.", "L'atelier a exploré les tensions ressenties dans les relations familiales à travers des activités expérientielles.")),
    (4, "刘倩", "Liu Qian", "helping", ("与自己及他人连结", "Connecting with self and others", "Se relier à soi et aux autres"),
     ("从正念品尝与慢行开始，逐步进入自我关怀和人际连接。", "Mindful tasting and slow walking opened a path toward self-care and connection with others.", "La dégustation attentive et la marche lente ont ouvert un chemin vers le soin de soi et le lien aux autres.")),
    (5, "李宇", "Li Yu", "family", ("从卡点到自信", "From obstacles to confidence", "Des blocages à la confiance en soi"),
     ("通过“夸夸圈”和书写练习，寻找已有的支持与个人资源。", "A circle of appreciation and writing exercises helped participants identify support and personal resources.", "Un cercle de reconnaissance et des exercices d'écriture ont aidé à repérer soutien et ressources personnelles.")),
    (5, "崔秋", "Cui Qiu", "helping", ("合作的能力", "The ability to cooperate", "La capacité à coopérer"),
     ("以动物家族等团体游戏，观察合作、角色与共同完成任务的过程。", "Group games such as finding an animal family explored cooperation, roles and shared tasks.", "Des jeux de groupe, dont la recherche de sa famille animale, ont exploré la coopération, les rôles et les tâches communes.")),
    (5, "魏然", "Wei Ran", "education", ("向内寻找答案", "Looking inward for answers", "Chercher des réponses en soi"),
     ("从安静、呼吸和无声协作开始，给内在觉察留出空间。", "Silence, breathing and wordless cooperation made room for inner awareness.", "Le silence, la respiration et la coopération sans paroles ont ouvert un espace à la conscience intérieure.")),
    (5, "赵巧辨", "Zhao Qiaobian", "teachers", ("三段旅程与高光时刻", "Three journeys and moments of strength", "Trois parcours et des moments forts"),
     ("以人生旅程和高光时刻为线索，回看成长中的经验与资源。", "Life journeys and significant moments offered a way to revisit experiences and resources for growth.", "Les parcours de vie et les moments marquants ont permis de revisiter les expériences et les ressources de croissance.")),
    (6, "王一伊", "Wang Yiyi", "classroom", ("身体与连结：从声音到相遇", "Body and connection: from sound to encounter", "Corps et lien : du son à la rencontre"),
     ("从声音、动作与静默行走进入，探索身体经验中的关系与连接。", "Sound, movement and silent walking helped explore relationships through bodily experience.", "Le son, le mouvement et la marche silencieuse ont permis d'explorer la relation par l'expérience corporelle.")),
    (6, "谢进", "Xie Jin", "education", ("从婴儿到成人", "From infancy to adulthood", "Du nourrisson à l'adulte"),
     ("以生命历程为线索，观察不同成长阶段的需要与资源。", "The life course provided a lens for exploring needs and resources across stages of development.", "Le parcours de vie a servi à explorer les besoins et les ressources aux différents âges.")),
    (6, "尹继恩", "Yin Jien", "eq", ("从受害到承担责任", "From victimhood to responsibility", "De la posture de victime à la responsabilité"),
     ("在活动与讨论中，辨认受害者心态和责任人心态带来的不同选择。", "Activities and discussion examined the different choices associated with a victim mindset and a responsible one.", "Les activités et les échanges ont examiné les choix liés à une posture de victime ou de responsabilité.")),
]

assert len(PEOPLE) == 22
assert len({person[1] for person in PEOPLE}) == 22
