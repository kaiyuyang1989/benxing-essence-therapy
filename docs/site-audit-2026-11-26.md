# 官网四阶段诊断与改版记录（2026-11-26）

本文件是工作记录，不进入公开网站。

## 第一阶段：全面诊断

- 定位：网站已说明本性治疗、米杉与著作，但课程入口藏在首页海报卡片里。导航缺少“课程”，无法从首页直接进入一门课的完整介绍。
- 结构：首页至方法、导师、书目、文章及课程沿革已有路径；新增课程总览和三门课独立详情页，使课程咨询形成连续路径。
- 视觉：保留自然背景和当前品牌字色。原 1.8 MB 晨光背景和 1.7 MB 山景背景生成网页用 JPEG（约 188 KB、132 KB），保留原件。1280 像素宽时直接显示导航；390 像素宽手机导航收起。手机预览无横向溢出。
- 技术：基线 18 页、50 张页面图片、0 处断链、46 条缺图像尺寸或社交预览警告。改版后 22 页、60 张图片、静态审计 0 错误／0 警告。页面标题、描述、canonical 和社交预览已补齐；sitemap 按生成的页面更新。

## 第二阶段：内容与结构

- 首页课程卡片链接到详情页，详情页包括适合对象、学习主题、形式、目标、日期地点、费用与咨询入口；内容依据 2027 春季课程事实表及已公开课程文案，未编造每日课表或效果承诺。
- 著作页加入出版脉络；按作品与版本关系阅读，不把不同版次算成不同著作。每个节点链接到已上线的书籍详情页。参见 `book-poster-review-2026-11-26.md`。
- 课程二维码在窄屏上放大显示，并可打开原图；公众号和既有咨询入口保留。
- 学员反馈、课堂合影及试切视频仍须按具体授权核查，未添加未经确认素材。

## 第三阶段：SEO 与 AI 搜索可读性

- 各页面使用准确的 H1、标题、描述、canonical、OG 元信息和内部链接。六本书详情页添加以 ISBN、作者、出版社和出版年份为基础的 `Book` 结构化数据。
- `robots.txt` 允许公开页面抓取，屏蔽 `/finance/`；`sitemap.xml` 列出 22 个公开页面。
- 文章以已公开的原始论述和团队内容为基础，未批量生成无来源文章。Google 官方建议以内容准确、有用及常规 SEO 为基础；无需为了 AI 搜索另加所谓“排名秘籍”。

## 第四阶段：数据反馈与持续改进

目前仓库中未见 Clarity、Google Search Console 或百度搜索资源平台的站点验证／项目 ID，也未见真实访客指标。不得把本地预览和静态扫描当成流量数据。

上线后优先记录：课程总览到各详情页的点击、详情页咨询入口点击、课程二维码原图打开、书籍详情页扫码入口打开、文章到著作／课程的路径。按月观察页面访问、有效咨询、搜索词与手机端停留；课程更换后同步复核时间、价格和链接。

接入顺序：先核对现有百度／Google 站长平台归属并提交 sitemap；如使用 Microsoft Clarity，先建立官网独立项目并确认隐私告知、敏感内容遮蔽及适用地区的同意机制，确保 `/finance/` 不纳入录制。暂不加入未知账户的跟踪代码。

官方参考：

- Google Search Central: <https://developers.google.com/search/docs/fundamentals/ai-optimization-guide>
- Microsoft Clarity masking: <https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-masking>
- Microsoft Clarity consent management: <https://learn.microsoft.com/en-us/clarity/setup-and-installation/consent-management>
- 百度搜索资源平台：<https://ziyuan.baidu.com/linksubmit/index>

## 验收

- `python3 build_content.py`, `python3 build_editorial.py`, `python3 build_courses.py`, `python3 tools/finalize_site.py`
- `python3 tools/audit_site.py`：22 页、60 张图片、0 错误／0 警告
- `python3 check_public_copy.py`：通过
- 本地 HTTP 预览：1280×800 桌面与 390×844 手机，检查首页、课程总览、一阶详情咨询区和著作出版脉络，均无横向溢出。
