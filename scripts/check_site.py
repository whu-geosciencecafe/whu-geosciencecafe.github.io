"""Check every page, local link, asset, ID and generated content record."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
EXPECTED = {'index.html', 'events.html', 'about.html', 'gallery.html', 'growth.html', 'partners.html'}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs = [], []
        self.cards = self.photos = 0
        self.active_nav = 0
        self.h1s = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.refs.append(a[key])
        if tag == 'img':
            assert 'alt' in a, f'Missing image alternative: {a}'
        if tag == 'h1':
            self.h1s += 1
        self.active_nav += a.get('aria-current') == 'page'
        self.cards += 'activity-card' in a.get('class', '').split()
        self.photos += 'gallery-card' in a.get('class', '').split()

files = {p.name: p for p in SITE.glob('*.html')}
assert set(files) == EXPECTED, 'Missing pages or leftover QA harness'
pages = {}
for name, path in files.items():
    html = path.read_text(encoding='utf-8')
    page = Page()
    page.feed(html)
    assert page.h1s == 1, f'{name}: should have one page heading'
    assert len(page.ids) == len(set(page.ids)), f'{name}: duplicate IDs'
    assert not re.search(r'__[A-Z_]+__', html), f'{name}: unexpanded marker'
    assert page.active_nav == (0 if name == 'index.html' else 1), f'{name}: active navigation incorrect'
    pages[name] = page

for name, page in pages.items():
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (SITE / unquote(url.path)).resolve() if url.path else files[name].resolve()
        assert target.is_relative_to(SITE.resolve()), f'Path escapes site: {ref}'
        assert target.is_file(), f'{name}: broken local link: {ref}'
        if url.fragment:
            assert target.name in pages and url.fragment in pages[target.name].ids, f'{name}: broken anchor: {ref}'

activities = json.loads((SITE / 'data/activities.json').read_text(encoding='utf-8'))
photos = json.loads((SITE / 'data/gallery.json').read_text(encoding='utf-8'))
assert pages['events.html'].cards == len(activities) > 0
assert pages['gallery.html'].photos == len(photos) > 0
for filename, dataset in [('events.html', activities), ('gallery.html', photos)]:
    html = files[filename].read_text(encoding='utf-8')
    for item in dataset:
        assert item['title'] in html, f'Missing static content: {item["id"]}'
        assert (SITE / item['image']).is_file()
assert (SITE / 'robots.txt').is_file() and (SITE / 'sitemap.xml').is_file()
assert not list(SITE.rglob('*.pptx')) and not (SITE / 'docs').exists()
size = sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
print(f'PASS: {len(pages)} pages, {len(activities)} activities, {len(photos)} photos; all local links, anchors, IDs and assets valid; {size / 1024 / 1024:.2f} MiB')
