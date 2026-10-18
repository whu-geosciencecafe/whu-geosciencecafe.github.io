# WHU Geoscience Café · 地学咖啡馆

组织网站的源代码。围绕地球科学、空间信息与开放研究，分享知识、交流问题、共同探索。

- 网站：<https://whu-geosciencecafe.github.io/>
- GitHub 组织：<https://github.com/whu-geosciencecafe>
- 话题与反馈：[Issues](https://github.com/whu-geosciencecafe/whu-geosciencecafe.github.io/issues)

## 本地预览

无需安装前端依赖，使用 Python 3：

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

浏览器打开 <http://localhost:8000>。修改源文件后，重新运行构建命令并刷新。

## 内容维护

- `index.html`：中文首页、交流主题、动态与参与入口。
- `styles.css`：响应式布局、配色与排版。
- `script.js`：移动端导航与键盘操作。
- `assets/favicon.svg`：网站图标。
- `scripts/build.py`：仅将网站运行所需文件复制到 `_site/`。

目前未公布具体活动安排、成员名单或联系方式。新增这些内容前请核实，不要把示例信息作为真实信息发布。请勿提交私人联系方式、访问凭据或未授权的个人资料。

## 部署

推送到 `main` 自动运行 `.github/workflows/pages.yml`，构建后部署 GitHub Pages。也可在 Actions 中手动运行工作流。

仓库的 **Settings → Pages → Build and deployment → Source** 应为 **GitHub Actions**。默认网址为 <https://whu-geosciencecafe.github.io/>，尚未配置自定义域名。

组织主页 README 位于独立的 [`.github` 仓库](https://github.com/whu-geosciencecafe/.github/blob/main/profile/README.md)，修改它不会触发网站部署。
