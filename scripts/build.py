"""Build a six-page, dependency-free GitHub Pages website."""
from pathlib import Path
from html import escape
import json
import shutil
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
HOST = 'https://whu-geosciencecafe.github.io/'
activities = json.loads((ROOT / 'data/activities.json').read_text(encoding='utf-8'))
gallery = json.loads((ROOT / 'data/gallery.json').read_text(encoding='utf-8'))

for dataset in (activities, gallery):
    ids = [item['id'] for item in dataset]
    assert len(ids) == len(set(ids)), 'IDs must be unique within each dataset'
    for item in dataset:
        path = (ROOT / item['image']).resolve()
        assert path.is_relative_to((ROOT / 'assets').resolve()), 'Image must be an asset'
        assert path.is_file(), f'Missing image: {item["image"]}'
        assert item['sourceSlides'], f'Missing source: {item["id"]}'
assert {a['category'] for a in activities} <= {'academic', 'innovation', 'exchange', 'science'}
assert {a['category'] for a in gallery} <= {'academic', 'innovation', 'exchange', 'community'}

def activity_cards(items=None):
    cards = []
    for item in activities if items is None else items:
        a = {key: escape(str(value), quote=True) for key, value in item.items()}
        cards.append(f'''<article class="activity-card" data-category="{a['category']}">
  <div class="activity-image"><img src="{a['image']}" alt="{a['imageAlt']}" width="720" height="480" loading="lazy"></div>
  <div class="activity-meta"><span>{a['categoryLabel']}</span><span>{a['period']}</span></div>
  <h3><button class="activity-open" type="button" data-activity="{a['id']}" aria-haspopup="dialog" aria-controls="detail-dialog" aria-label="查看活动：{a['title']}">{a['title']}</button></h3>
  <p>{a['summary']}</p>
</article>''')
    return '\n'.join(cards)

def gallery_cards():
    cards = []
    for item in gallery:
        a = {key: escape(str(value), quote=True) for key, value in item.items()}
        cards.append(f'''<article class="gallery-card" data-category="{a['category']}"><button type="button" data-photo="{a['id']}" aria-haspopup="dialog" aria-controls="detail-dialog" aria-label="查看照片：{a['title']}"><span class="gallery-image"><img src="{a['image']}" alt="{a['description']}" width="720" height="576" loading="lazy"></span><span class="gallery-caption">{a['title']}</span><span class="gallery-category">{a['categoryLabel']}</span></button></article>''')
    return '\n'.join(cards)

pages = [
    ('home', 'index.html', 'GeoScience Café · 谈笑间，成就梦想', '武汉大学 GeoScience Café：交流前沿学术，探索时空智能，分享有意思的科普。从一杯咖啡开始，与一群好奇的人共同成长。'),
    ('events', 'events.html', '活动档案 · GeoScience Café', '回看 GeoScience Café 的学术讲座、AI Agent 现场开发、Vibe Coding 黑客马拉松、国际交流与气象科普活动。'),
    ('about', 'about.html', '关于我们 · GeoScience Café', '从1983年的咖啡券故事到2009年社团成立，了解武汉大学 GeoScience Café 的交流传统与六大学术方向。'),
    ('gallery', 'gallery.html', '社团相册 · GeoScience Café', '在实拍照片中回看 GeoScience Café 的学术交流、创新实践、国际合作与社团生活。'),
    ('growth', 'growth.html', '成长资源 · GeoScience Café', '探索科研写作、AI工具实践、学术与职业成长交流主题，以及 Café 成员的成长经历。'),
    ('partners', 'partners.html', '合作伙伴 · GeoScience Café', '了解 GeoScience Café 与 Datawhale、扣子空间、TRAE、GSIS期刊编辑部、武大出版社及校园组织的合作交流。'),
]
template = (ROOT / 'index.html').read_text(encoding='utf-8')
header = (ROOT / 'partials/header.html').read_text(encoding='utf-8')
footer = (ROOT / 'partials/footer.html').read_text(encoding='utf-8')
data = json.dumps({'activities': activities, 'gallery': gallery}, ensure_ascii=False).replace('<', '\\u003c')
assert OUTPUT.resolve().parent == ROOT.resolve() and OUTPUT.name == '_site'
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir()
for slug, filename, title, description in pages:
    body = (ROOT / f'pages/{slug}.html').read_text(encoding='utf-8')
    body = body.replace('__ACTIVITY_CARDS__', activity_cards()).replace('__HOME_ACTIVITY_CARDS__', activity_cards(activities[:3])).replace('__GALLERY_CARDS__', gallery_cards())
    nav = header
    for name in ('events', 'about', 'gallery', 'growth', 'partners'):
        nav = nav.replace(f'__ACTIVE_{name.upper()}__', 'aria-current="page"' if name == slug else '')
    html = template
    for marker, value in {'TITLE': escape(title), 'DESCRIPTION': escape(description, quote=True), 'PAGE_URL': '' if slug == 'home' else filename, 'HEADER': nav, 'BODY': body, 'FOOTER': footer, 'SITE_DATA': data}.items():
        html = html.replace(f'__{marker}__', value)
    for asset in ('styles.css', 'script.js'):
        revision = hashlib.sha256((ROOT / asset).read_bytes()).hexdigest()[:10]
        html = html.replace(f'"{asset}"', f'"{asset}?v={revision}"')
    (OUTPUT / filename).write_text(html, encoding='utf-8')
for name in ('styles.css', 'script.js'):
    shutil.copy2(ROOT / name, OUTPUT / name)
for name in ('assets', 'data'):
    shutil.copytree(ROOT / name, OUTPUT / name)
(OUTPUT / '.nojekyll').touch()
(OUTPUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {HOST}sitemap.xml\n', encoding='utf-8')
urls = ''.join(f'<url><loc>{HOST}{"" if slug == "home" else filename}</loc></url>' for slug, filename, _, _ in pages)
(OUTPUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding='utf-8')
print(f'Built {len(pages)} pages, {len(activities)} activities and {len(gallery)} photos: {OUTPUT}')
