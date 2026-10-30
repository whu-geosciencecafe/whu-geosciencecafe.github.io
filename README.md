# GeoScience Café · 武汉大学

基于社团 2026 年展示资料重写的六页静态官网。首页采用社团深蓝与暖白配色、左右分栏实拍、衬线标题与社团故事叙事。活动与相册作为独立页面，支持类别筛选、详情弹窗和可分享的内容链接。

- 正式网站：<https://whu-geosciencecafe.github.io/>
- GitHub 组织：<https://github.com/whu-geosciencecafe>

## 本地构建与预览

无需安装前端依赖。使用 Python 3：

```sh
python scripts/build.py
python scripts/check_site.py
python -m http.server 8000 --directory _site
```

打开 <http://localhost:8000/>。修改源文件后重新构建并刷新。CSS 和 JavaScript 的内容哈希会自动更新 URL，避免浏览器使用旧版缓存。也可以直接打开 `_site/index.html` 浏览构建后的静态网站。

## 文件结构

| 文件 | 用途 |
| --- | --- |
| `index.html` | 共享 HTML 外壳、页面元数据、详情弹窗和数据嵌入位置 |
| `pages/home.html` | 首页：社团主题、历史、精选活动、六个方向、国际交流、社团生活 |
| `pages/events.html` | 活动档案页 |
| `pages/about.html` | 社团历史与学术方向 |
| `pages/gallery.html` | 社团相册页 |
| `pages/growth.html` | 成长资源与成员毕业去向 |
| `pages/partners.html` | 合作伙伴及对应项目 |
| `partials/header.html`、`partials/footer.html` | 各页面共享导航和页脚 |
| `data/activities.json` | 可由 agent 编辑的活动、摘要、详情、图片与来源页码 |
| `data/gallery.json` | 可由 agent 编辑的照片、分类、说明与来源页码 |
| `styles.css` | 全站主题、排版和响应式样式 |
| `script.js` | 手机菜单、活动/相册筛选、详情弹窗、分享 URL 与焦点恢复 |
| `assets/` | PPT 提取的社团标识与优化后的实拍 WebP 图片 |
| `docs/asset-provenance.json` | 网页图片与 PPT 资产 ID、页码和裁剪区域的对应关系 |
| `docs/content-sources.md` | 文案与数据来源口径 |
| `scripts/build.py` | 生成六个完整静态页面、站点地图与 robots 文件 |
| `scripts/check_site.py` | 验证所有页面、内部链接、锚点、图片和生成内容 |

## 给维护 agent

1. 文案在对应 `pages/*.html` 中编辑，公共导航与页脚在 `partials/` 中编辑。
2. 增补活动时编辑 `data/activities.json`，保留稳定 `id`。分类为 `academic`、`innovation`、`exchange`、`science`。日期不详时使用系列名称，不补写日期。
3. 增补照片时编辑 `data/gallery.json`。相册分类为 `academic`、`innovation`、`exchange`、`community`。
4. 活动链接示例：`events.html?activity=agent-hackathon`。类别链接示例：`events.html?category=innovation`。相册支持 `gallery.html?category=exchange` 和 `gallery.html?photo=summer`。
5. 上传优化后的图片到 `assets/photos/`，并在数据和溯源文件中记录真实说明、资产 ID 和来源页码。不要将 500MB 原始资产包或 PPT 提交到网站。
6. 执行构建、校验和 `node --check script.js` 后检查浏览器。`_site/` 是构建输出，不应直接修改或提交。

统计为社团 2026 年展示资料口径，并非实时累计。本网站展示活动回顾，没有虚构报名、招新或岗位。联系方式沿用原网站 GitHub 入口，不新增未核实的微信、邮箱、地址或成员私人联系方式。

所有页面页脚包含 OpenStreetMap 交互地图，显示武汉大学周边，支持拖动、缩放与打开大图。地图为校园概览，不标注未经确认的社团办公室。可在 `partials/footer.html` 修改地图的 `bbox` 范围及大图链接；地图延迟加载，保留提供方署名。地图功能需要访问 OpenStreetMap。

手机竖屏首页将照片放在标题之后、介绍文字之前，使用 3:2 的图片比例，让首屏可见完整合影；桌面保留左右分栏。

## 部署

保留原 GitHub Pages 方式。PR 自动构建并检查页面、链接和 JavaScript；推送或合并到 `main` 后，构建通过再部署 `_site/`。PR 不触发线上部署。工作流为 `.github/workflows/pages.yml`，仓库 Pages 来源应为 **GitHub Actions**。

组织主页 README 位于独立的 `.github` 仓库，本项目不会修改该仓库。
