# 官网内容、视觉和交互升级记录（2026-11-27）

## 本轮目标

让初访者按主题进入本性治疗、梦工作、情商教育与在华教学资料。重要信息直接呈现，次要解释按需展开；每条路径都能继续读文章、原著、课程或原始报道。

## 设计与语言依据

- [Ant Design 文案规范](https://ant.design/docs/spec/copywriting/)与[字体规范](https://ant.design/docs/spec/font-cn/)：标题准确，段落简洁，正文层级和对比清晰。首页及人物页删去过于抒情的句子，改写为读者可以核对的内容。
- [GOV.UK 内容设计](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/)与[折叠组件规范](https://design-system.service.gov.uk/components/accordion/)：让访客按任务找资料；主要内容直接可见，术语解释与历程详情使用原生 `details`。
- [Nielsen Norman Group 对动效目的的研究](https://www.nngroup.com/articles/animation-purpose-ux/)与[W3C 的交互动效指导](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)：仅在悬停、筛选、展开时给短促反馈；尊重系统的减少动态效果设置。无自动轮播、视频背景或新的脚本依赖。
- 用户此前指定的 [Dentosophie 网站](https://www.dentosophie.com/fr/)只参考其主题层级和深度阅读方式，不复制文字、图片或诊疗主张。

## 来源核验

| 内容 | 依据 | 使用方式 |
| --- | --- | --- |
| 本性治疗概念及七原则 | 已公开的米杉《什么是本性治疗》2024 年更新论述；《由心咨询》 | 概述和术语释义，不写效果保证 |
| 梦工作及北京早期工作坊 | 《梦的真相》2010 年版译者序；已公开梦工作文章 | 专题阅读和时间轴，链接书页与文章页 |
| 高校情商课程 | 《情商教练手册》2018 年版译者序 | 北京印刷学院节点，链接书页 |
| 2010 年泉州专业培训 | [华侨大学报道](https://www.hqu.edu.cn/info/1073/14191.htm) | 教师资料卡、时间轴和专题页，标为报道 |
| 2013 年北京梦主题讲座 | [北京师范大学讲座预告](https://xueronghua.bnu.edu.cn/kcypx/jz/jzyg/52692.html) | 只标为预告，不据此声称活动已举办 |
| 2025—2026 年课程 | 已确认的本性课程资料与活动事实表 | 时间轴，按年份和主题筛选 |
| 《由心咨询》封面 | 已留存的书店封面图，对照小扎提供的新版著作海报 | 仅复制到新的 `heart-front-web.jpg`，用于专题和书页；原整张书衣继续留档 |

课堂合影、学员逐字反馈和试切视频仍按现有公开范围管理；本轮没有把未确认素材加入官网。没有向访客展示资料核验过程、内部指令或书籍下载入口。购书码、会员隐藏、备案号和既有课程事实保持原有口径。

## 技术选择与验收

比较了 GitHub 上的 [Motion](https://github.com/motiondivision/motion)、[GSAP](https://github.com/greensock/GSAP) 与 [AOS](https://github.com/michalsnik/aos)。对这个静态站，原生 CSS、`details` 和少量筛选脚本已足够完成交互，避免增加运行包和首次载入负担。

生成顺序：`build_content.py` → `build_guide.py` → `build_editorial.py` → `build_courses.py` → `tools/finalize_site.py`。随后运行站内链接审计和公开文案检查。正式发布后核对 `guide.html`、`archive.html`、`teacher.html` 和首页的实际响应；浏览器视觉检查情况单独记录。

补充检查：新增专题导航后，980 像素及以下宽度使用折叠菜单，避免平板宽度一行导航拥挤；菜单与原有屏幕阅读标签保持一致。
