from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "src" / "content" / "insights"
OUTPUT = ROOT / "preview_dist"
IMAGE_SOURCE = ROOT / "public" / "assets" / "images" / "insights"


def parse_frontmatter(text: str):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        raise ValueError("Missing frontmatter")
    data, current = {}, None
    for raw in match.group(1).splitlines():
        item = re.match(r"^\s+-\s+[\"']?(.*?)[\"']?\s*$", raw)
        if item and current:
            data.setdefault(current, []).append(item.group(1))
            continue
        field = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", raw)
        if not field:
            continue
        current, value = field.groups()
        value = value.strip()
        if not value:
            data[current] = []
        elif value in ("[]", "{}"): data[current] = []
        elif value.lower() in ("true", "false"): data[current] = value.lower() == "true"
        else: data[current] = value.strip('"\'')
    return data, match.group(2)


def inline(text: str):
    value = escape(text, quote=False)
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    return value


def markdown(body: str):
    lines, out, paragraph, list_kind = body.splitlines(), [], [], None
    def flush_paragraph():
        if paragraph:
            out.append(f"<p>{inline(' '.join(x.strip() for x in paragraph))}</p>")
            paragraph.clear()
    def close_list():
        nonlocal list_kind
        if list_kind:
            out.append(f"</{list_kind}>")
            list_kind = None
    for raw in lines + [""]:
        line = raw.strip()
        if not line:
            flush_paragraph(); close_list(); continue
        heading = re.match(r"^(#{2,4})\s+(.+)$", line)
        if heading:
            flush_paragraph(); close_list(); level = len(heading.group(1)); out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>"); continue
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        numbered = re.match(r"^\d+\.\s+(.+)$", line)
        if bullet or numbered:
            flush_paragraph(); wanted = "ul" if bullet else "ol"
            if list_kind != wanted:
                close_list(); out.append(f"<{wanted}>"); list_kind = wanted
            out.append(f"<li>{inline((bullet or numbered).group(1))}</li>"); continue
        if line.startswith("> "):
            flush_paragraph(); close_list(); out.append(f"<blockquote>{inline(line[2:])}</blockquote>"); continue
        paragraph.append(line)
    return "\n".join(out)


def set_head(shell: str, *, title: str, description: str, canonical: str, image: str | None, schema=None):
    replacements = {
        r"<title>.*?</title>": f"<title>{escape(title)}</title>",
        r'<meta name="description" content="[^"]*">': f'<meta name="description" content="{escape(description, quote=True)}">',
        r'<link rel="canonical" href="[^"]*">': f'<link rel="canonical" href="{escape(canonical, quote=True)}">',
        r'<meta property="og:title" content="[^"]*">': f'<meta property="og:title" content="{escape(title, quote=True)}">',
        r'<meta property="og:description" content="[^"]*">': f'<meta property="og:description" content="{escape(description, quote=True)}">',
    }
    for pattern, replacement in replacements.items(): shell = re.sub(pattern, replacement, shell, count=1, flags=re.S)
    if image:
        absolute = f"https://alankyeong.com{image}"
        shell = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{absolute}">', shell, count=1)
        shell = shell.replace("</head>", f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{absolute}"></head>', 1)
    if schema:
        shell = shell.replace("</head>", f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>', 1)
    return shell


subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_preview.py")], check=True)
(OUTPUT / "assets" / "images" / "insights").mkdir(parents=True, exist_ok=True)
for image in IMAGE_SOURCE.glob("*.webp"):
    shutil.copy2(image, OUTPUT / "assets" / "images" / "insights" / image.name)

articles = []
for source in sorted(CONTENT.glob("ay-sea-2026-*.md")):
    data, body = parse_frontmatter(source.read_text(encoding="utf-8-sig"))
    slug = data["slug"]
    description = data.get("excerpt") or data.get("description") or ""
    publish = datetime.fromisoformat(data.get("publish_at") or data["publishDate"])
    image = data.get("featured_image") or data.get("image")
    alt = data.get("featured_image_alt") or data.get("imageAlt") or ""
    articles.append({**data, "slug": slug, "description": description, "publish": publish, "image": image, "alt": alt, "body": body})

shell = (OUTPUT / "insights" / "index.html").read_text(encoding="utf-8")
cards = []
for article in sorted(articles, key=lambda x: x["publish"], reverse=True):
    cards.append(f'''<article class="insight-card image-insight-card"><a href="/insights/{article['slug']}/"><img src="{escape(article['image'])}" alt="{escape(article['alt'], quote=True)}" width="600" height="400" loading="lazy"></a><div class="insight-card-copy"><div class="article-labels"><p class="eyebrow">{escape(article['category'])}</p><span class="draft-badge">Preview draft</span></div><a href="/insights/{article['slug']}/"><h2>{escape(article['title'])}</h2></a><p>{escape(article['description'])}</p><p class="meta">{article['publish'].strftime('%-d %B %Y') if sys.platform != 'win32' else article['publish'].strftime('%d %B %Y').lstrip('0')}</p><a href="/insights/{article['slug']}/">Read insight →</a></div></article>''')
index_main = f'''<main><header class="page-hero"><div class="wrap narrow"><p class="eyebrow">Insights</p><h1>Ideas for better-informed decisions</h1><p class="lead">Perspectives on Asian markets, consumer behaviour, research practice, commercial judgement and the responsible use of AI.</p></div></header><section><div class="wrap insight-grid">{''.join(cards)}</div></section></main>'''
shell = re.sub(r"<main>.*?</main>", index_main, shell, count=1, flags=re.S)
shell = set_head(shell, title="Insights on Asian Markets, Consumers and AI | Alan Yeong", description="Articles and perspectives on Asian markets, consumer intelligence, research, commercial strategy and practical AI in business.", canonical="https://alankyeong.com/insights/", image="/images/thought-leadership.jpg")
(OUTPUT / "insights" / "index.html").write_text(shell, encoding="utf-8")

for article in articles:
    canonical = article.get("canonical_url") or f"https://alankyeong.com/insights/{article['slug']}/"
    title = article.get("meta_title") or f"{article['title']} | Alan Yeong"
    description = article.get("meta_description") or article["description"]
    published = article["publish"].isoformat()
    schema = {"@context":"https://schema.org","@type":"Article","headline":article["title"],"description":description,"image":f"https://alankyeong.com{article['image']}","datePublished":published,"dateModified":published,"author":{"@type":"Person","name":"Alan Yeong","url":"https://alankyeong.com"},"publisher":{"@type":"Person","name":"Alan Yeong"},"mainEntityOfPage":canonical}
    main = f'''<main><article class="article wrap narrow"><div class="article-labels"><p class="eyebrow">{escape(article['category'])}</p><span class="draft-badge">Preview draft</span></div><h1>{escape(article['title'])}</h1><p class="lead">{escape(article['description'])}</p><p class="meta"><time datetime="{published}">{article['publish'].strftime('%d %B %Y').lstrip('0')}</time> · By Alan Yeong</p><img class="article-hero" src="{escape(article['image'])}" alt="{escape(article['alt'], quote=True)}" width="1536" height="1024" loading="eager"><div class="prose">{markdown(article['body'])}</div><aside class="article-cta"><h2>Facing a decision across Asia?</h2><p>Bring the market question, evidence or assumption that needs a more experienced perspective.</p><a class="button" href="/contact/">Discuss a professional enquiry</a></aside></article></main>'''
    page = re.sub(r"<main>.*?</main>", main, shell, count=1, flags=re.S)
    page = set_head(page, title=title, description=description, canonical=canonical, image=article["image"], schema=schema)
    destination = OUTPUT / "insights" / article["slug"]
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(page, encoding="utf-8")

print(f"Imported {len(articles)} scheduled draft articles into {OUTPUT}")
