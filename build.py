#!/usr/bin/env python3
"""
Build script for Massimiliano Berardi's portfolio site.
Usage: python build.py
Reads projects/*.md → generates index.html + project-*.html
Generates thumbnails in assets/thumbs/ (requires Pillow: pip install pillow)
"""

import os
import re
import shutil
import hashlib
import html

VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov'}

# ── Thumbnail generation ────────────────────────────────────────────────────

THUMB_WIDTH = 600

def make_thumbnail(src, dst):
    try:
        from PIL import Image
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        img = Image.open(src)
        w, h = img.size
        if w > THUMB_WIDTH:
            ratio = THUMB_WIDTH / w
            img = img.resize((THUMB_WIDTH, int(h * ratio)), Image.LANCZOS)
        img.save(dst, quality=85, optimize=True)
        print(f"  thumb: {os.path.basename(dst)}")
    except ImportError:
        print("  [!] Pillow not installed — copying original as thumb. Run: pip install pillow")
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"  [!] Thumbnail failed for {src}: {e}")
        shutil.copy2(src, dst)

# ── Markdown / frontmatter parsing ─────────────────────────────────────────

def parse_md(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()

    meta = {}
    body = text

    if text.startswith('---'):
        end = text.index('---', 3)
        frontmatter = text[3:end].strip()
        body = text[end + 3:].strip()
        for line in frontmatter.splitlines():
            if ':' in line:
                k, _, v = line.partition(':')
                meta[k.strip()] = v.strip()

    return meta, body

def render_inline_markdown(text):
    inline_pattern = re.compile(r'(`[^`]+`|\[([^\]]+)\]\(([^)]+)\))')
    parts = []
    last = 0

    for match in inline_pattern.finditer(text):
        parts.append(html.escape(text[last:match.start()]))
        token = match.group(0)
        if token.startswith('`'):
            parts.append(f'<code>{html.escape(token[1:-1])}</code>')
        else:
            label, href = match.group(2), match.group(3)
            parts.append(
                f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener">'
                f'{html.escape(label)}</a>'
            )
        last = match.end()

    parts.append(html.escape(text[last:]))
    return ''.join(parts)

def is_video(src):
    return os.path.splitext(src)[1].lower() in VIDEO_EXTENSIONS

def render_media_figure(alt, src, row_item=False):
    classes = ['ref-image']
    if row_item:
        classes.append('row-item')
    if is_video(src):
        classes.append('video-figure')
    class_attr = ' '.join(classes)
    caption_html = f'\n  <figcaption>{alt}</figcaption>' if alt else ''

    if is_video(src):
        media_html = (
            f'  <video preload="metadata" playsinline muted>\n'
            f'    <source src="assets/pictures/{src}">\n'
            f'  </video>'
        )
    else:
        media_html = f'  <img src="assets/pictures/{src}" alt="{alt}">'

    if row_item:
        media_html = media_html.replace('\n  ', '\n    ')
        caption_html = f'\n    <figcaption>{alt}</figcaption>' if alt else ''

    return f'<figure class="{class_attr}">\n{media_html}{caption_html}\n</figure>'

def split_markdown_blocks(text):
    blocks = []
    current = []
    in_code = False

    for line in text.splitlines():
        if line.startswith('```'):
            current.append(line)
            if in_code:
                blocks.append('\n'.join(current).strip('\n'))
                current = []
            in_code = not in_code
            continue

        if in_code:
            current.append(line)
            continue

        if line.strip():
            current.append(line)
        elif current:
            blocks.append('\n'.join(current).strip('\n'))
            current = []

    if current:
        blocks.append('\n'.join(current).strip('\n'))

    return blocks

def md_to_html(text):
    """Paragraphs, fenced code, inline media, and media rows."""
    image_pattern = re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)$')
    code_pattern = re.compile(r'^```([A-Za-z0-9_-]*)\n(.*?)\n```$', re.DOTALL)
    blocks = split_markdown_blocks(text)
    parts = []
    for block in blocks:
        code_match = code_pattern.match(block)
        if code_match:
            lang, code = code_match.group(1), code_match.group(2)
            language_class = f' class="language-{html.escape(lang, quote=True)}"' if lang else ''
            parts.append(f'<pre class="code-block"><code{language_class}>{html.escape(code)}</code></pre>')
            continue

        block = block.strip()
        m = image_pattern.match(block)
        if m:
            alt, src = m.group(1), m.group(2)
            parts.append(render_media_figure(alt, src))
            continue

        row_items = [item.strip() for item in block.split('|')]
        row_matches = [image_pattern.match(item) for item in row_items]
        if len(row_items) > 1 and all(row_matches):
            figures = []
            for match in row_matches:
                alt, src = match.group(1), match.group(2)
                figures.append('  ' + render_media_figure(alt, src, row_item=True).replace('\n', '\n  '))
            parts.append('<div class="image-row">\n' + '\n'.join(figures) + '\n</div>')
        else:
            parts.append(f'<p>{render_inline_markdown(block)}</p>')
    return '\n'.join(parts)

def slugify(name):
    return os.path.splitext(os.path.basename(name))[0]

def asset_url(base, rel_path):
    path = os.path.join(base, rel_path)
    with open(path, 'rb') as f:
        digest = hashlib.sha256(f.read()).hexdigest()[:10]
    return f'{rel_path}?v={digest}'

# ── HTML templates ──────────────────────────────────────────────────────────

# Inline theme init prevents flash of wrong theme
THEME_SCRIPT = '''  <script>
    (function(){
      var t=localStorage.getItem('theme');
      var d=window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.documentElement.classList.add(t==='dark'||(!t&&d)?'dark':'light');
    })();
  </script>'''

LOGO_SVG = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="24" cy="24" r="21.5" stroke="currentColor" stroke-width="1.2"/>
      <text x="24" y="29.5" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="currentColor" letter-spacing="2">MB</text>
    </svg>'''

THEME_BTN = '''<button id="theme-toggle" class="theme-btn" aria-label="Toggle dark mode">
      <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
      <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>
    </button>'''

def make_head(title, css_url):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="icon" type="image/svg+xml" href="assets/logo.svg">
  <link rel="stylesheet" href="{css_url}">
{THEME_SCRIPT}
</head>
<body>
  <canvas id="ripple-canvas"></canvas>'''

def make_nav(work_href):
    return f'''  <nav>
    <a href="index.html" class="logo" aria-label="Home">
    {LOGO_SVG}
    </a>
    <ul class="nav-links">
      <li><a href="{work_href}">Work</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
    <div class="nav-right">
      <a href="assets/CV.pdf" download class="cv-btn">CV</a>
      {THEME_BTN}
    </div>
  </nav>'''

FOOT = '''  <footer>Massimiliano Berardi &middot; 2026</footer>
  <script src="{js_url}"></script>
</body>
</html>'''

# ── Index page ──────────────────────────────────────────────────────────────

def card_html(meta, slug):
    title = meta.get('title', 'Untitled')
    year = meta.get('year', '')
    subtitle = meta.get('subtitle', '')
    thumb = f'assets/thumbs/{meta.get("image", "")}'
    return f'''    <a href="project-{slug}.html" class="project-card">
      <div class="thumb-wrap">
        <img src="{thumb}" alt="{title}" loading="lazy">
      </div>
      <div class="card-body">
        <div class="year-chip">{year}</div>
        <div class="card-title">{title}</div>
        <div class="card-subtitle">{subtitle}</div>
      </div>
    </a>'''

def build_index(projects):
    cards = '\n'.join(card_html(meta, slug) for slug, meta, _ in projects)
    base = os.path.dirname(os.path.abspath(__file__))
    html = make_head('Massimiliano Berardi', asset_url(base, 'assets/style.css'))
    html += '\n' + make_nav('#projects') + '\n'
    html += '''
  <section class="hero">
    <h1>Massimiliano Berardi</h1>
    <p class="role">Software Engineer</p>
    <p class="location">Syntho B.V. &middot; Amsterdam, NL</p>
    <a href="#projects" class="scroll-hint">
      <span>Projects</span>
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 12 15 18 9"/>
      </svg>
    </a>
  </section>

  <section id="projects" class="projects-section">
    <p class="section-label">Selected work</p>
    <div class="projects-grid">
'''
    html += cards
    html += '''
    </div>
  </section>

'''
    html += FOOT.format(js_url=asset_url(base, 'assets/animation.js'))
    return html

# ── Project page ────────────────────────────────────────────────────────────

def build_project_page(meta, body):
    title = meta.get('title', 'Untitled')
    year = meta.get('year', '')
    subtitle = meta.get('subtitle', '')
    image = meta.get('image', '')
    description_html = md_to_html(body)
    base = os.path.dirname(os.path.abspath(__file__))

    html = make_head(f'{title} — Massimiliano Berardi', asset_url(base, 'assets/style.css'))
    html += '\n' + make_nav('index.html#projects') + '\n'
    html += f'''
  <div class="project-intro">
    <a href="index.html" class="back-link">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"/>
      </svg>
      Back
    </a>
    <div class="project-header">
      <div class="year-chip">{year}</div>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
    </div>
  </div>

  <div class="project-hero">
    <img src="assets/pictures/{image}" alt="{title}">
  </div>

  <div class="project-body">
    <hr class="project-divider">
    <div class="description">
      {description_html}
    </div>
  </div>

'''
    html += FOOT.format(js_url=asset_url(base, 'assets/animation.js'))
    return html

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base, 'projects')
    pictures_dir = os.path.join(base, 'assets', 'pictures')
    thumbs_dir = os.path.join(base, 'assets', 'thumbs')
    os.makedirs(thumbs_dir, exist_ok=True)

    md_files = sorted(f for f in os.listdir(projects_dir) if f.endswith('.md'))
    if not md_files:
        print("No .md files found in projects/")
        return

    projects = []
    for fname in md_files:
        slug = slugify(fname)
        meta, body = parse_md(os.path.join(projects_dir, fname))
        projects.append((slug, meta, body))

        image = meta.get('image', '')
        if image:
            src = os.path.join(pictures_dir, image)
            dst = os.path.join(thumbs_dir, image)
            if os.path.exists(src):
                make_thumbnail(src, dst)
            else:
                print(f"  [!] Image not found: assets/pictures/{image}")

    projects.sort(key=lambda x: int(x[1].get('year', 0) or 0), reverse=True)

    index_path = os.path.join(base, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(build_index(projects))
    print(f"Built index.html ({len(projects)} projects)")

    for slug, meta, body in projects:
        page_path = os.path.join(base, f'project-{slug}.html')
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(build_project_page(meta, body))
        print(f"Built project-{slug}.html")

    print("Done.")

if __name__ == '__main__':
    main()
