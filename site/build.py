#!/usr/bin/env python3
"""Build the 5G Regulatory Compliance static site.

Usage:  python3 build.py

Reads Markdown posts from content/posts/ and templates from templates/,
copies media, and writes a static site to docs/ (for GitHub Pages).

The card index, per-post pages, front-matter parser, multi-author cards,
permission credit, version footer, and BLOG_ENABLED switch follow the
data-driven blog engine this site was adapted from. Set BLOG_ENABLED = False
to skip generating post pages and hide post cards (source files stay in
content/posts/). Drafts (front matter draft: true) are always excluded.

No heavy dependencies — Python 3 only.
"""
import datetime, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
VERSION = "1.0.0"
# Set to False to hide post cards and skip generating post pages
# (files stay in content/posts/). About and Archive still build.
BLOG_ENABLED = True

CONTENT = os.path.join(HERE, "content")
POSTS_DIR = os.path.join(CONTENT, "posts")
MEDIA_SRC = os.path.join(CONTENT, "media")
TPL_DIR = os.path.join(HERE, "templates")
DOCS = os.path.join(HERE, "docs")
RESEARCH = os.path.join(os.path.dirname(HERE), "research", "rimba-posts.json")


def parse_post(text):
    if not text.startswith("---"):
        raise ValueError("post is missing front matter")
    _lead, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        meta[k.strip()] = v
    meta["body"] = body.strip()
    raw_tags = meta.get("tags") or ""
    meta["tag_list"] = [t.strip() for t in raw_tags.split(",") if t.strip()]
    draft = (meta.get("draft") or "").strip().lower()
    meta["is_draft"] = draft in ("true", "yes", "1")
    return meta


def fmt_long(d):
    y, m, dd = map(int, d.split("-"))
    return datetime.date(y, m, dd).strftime("%B ") + str(dd) + datetime.date(y, m, dd).strftime(", %Y")


def html_esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def tag_pills(tags, as_buttons=False):
    out = []
    for t in tags:
        if as_buttons:
            out.append(f'<button type="button" class="tag" data-tag="{html_esc(t)}">{html_esc(t)}</button>')
        else:
            out.append(f'<span class="tag">{html_esc(t)}</span>')
    return "".join(out)


def is_html_body(body):
    s = body.lstrip()
    return s.startswith("<")


def render_markdown(body):
    """Small Markdown subset for new posts. No extra packages required."""
    lines = body.splitlines()
    out, para, in_ul, in_ol = [], [], False, False

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + " ".join(para) + "</p>")
            para = []

    def flush_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def inline(s):
        s = html_esc(s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s

    for line in lines:
        if not line.strip():
            flush_para()
            flush_lists()
            continue
        if line.startswith("### "):
            flush_para(); flush_lists()
            out.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("## "):
            flush_para(); flush_lists()
            out.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("# "):
            flush_para(); flush_lists()
            out.append("<h2>" + inline(line[2:]) + "</h2>")
        elif re.match(r"^\d+\.\s+", line):
            flush_para()
            if in_ul:
                out.append("</ul>"); in_ul = False
            if not in_ol:
                out.append("<ol>"); in_ol = True
            out.append("<li>" + inline(re.sub(r"^\d+\.\s+", "", line)) + "</li>")
        elif line.startswith("- "):
            flush_para()
            if in_ol:
                out.append("</ol>"); in_ol = False
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append("<li>" + inline(line[2:]) + "</li>")
        else:
            flush_lists()
            para.append(inline(line))
    flush_para()
    flush_lists()
    return "\n".join(out)


def render_body(body):
    return body if is_html_body(body) else render_markdown(body)


def load_posts():
    if not os.path.isdir(POSTS_DIR):
        return []
    posts = []
    for fn in os.listdir(POSTS_DIR):
        if not fn.endswith(".md"):
            continue
        p = parse_post(open(os.path.join(POSTS_DIR, fn), encoding="utf-8").read())
        p["_file"] = fn
        if p["is_draft"]:
            continue
        posts.append(p)
    posts.sort(key=lambda p: (p.get("date") or "", p.get("title") or ""), reverse=True)
    return posts


def load_research():
    if not os.path.isfile(RESEARCH):
        return {"republished": [], "also_located": []}
    with open(RESEARCH, encoding="utf-8") as f:
        return json.load(f)


def clean_docs():
    if os.path.isdir(DOCS):
        for name in os.listdir(DOCS):
            path = os.path.join(DOCS, name)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    else:
        os.makedirs(DOCS, exist_ok=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def archive_card(item, local_slug=None):
    title = html_esc(item.get("title") or "")
    authors = html_esc(item.get("authors_as_credited") or ", ".join(item.get("authors") or []))
    date = html_esc(fmt_long(item["date"]) if item.get("date") else "")
    summary = html_esc(item.get("summary") or "")
    url = item.get("original_url") or ""
    tags = tag_pills(item.get("topic_tags") or [])
    flag = ""
    if item.get("byline_unconfirmed"):
        flag = ' <span class="tag">Byline uncertain</span>'
    local = f'<a href="{html_esc(local_slug)}.html">Read on this site</a> · ' if local_slug else ""
    return (
        f'<div class="card archive-item">'
        f"<h3>{title}</h3>"
        f'<div class="meta"><span class="date">{date}</span> · {authors}{flag}</div>'
        f"<p>{summary}</p>"
        f'<p class="meta">{local}<a href="{html_esc(url)}">{html_esc(url)}</a></p>'
        f'<p class="tags">{tags}</p>'
        f"</div>"
    )


def build():
    css = open(os.path.join(TPL_DIR, "_shared.css"), encoding="utf-8").read()
    home_tpl = open(os.path.join(TPL_DIR, "_home.html"), encoding="utf-8").read()
    post_tpl = open(os.path.join(TPL_DIR, "_post.html"), encoding="utf-8").read()
    about_tpl = open(os.path.join(TPL_DIR, "_about.html"), encoding="utf-8").read()
    archive_tpl = open(os.path.join(TPL_DIR, "_archive.html"), encoding="utf-8").read()

    clean_docs()
    os.makedirs(DOCS, exist_ok=True)
    # GitHub Pages: don't run Jekyll on the docs/ folder
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    if os.path.isdir(MEDIA_SRC):
        shutil.copytree(MEDIA_SRC, os.path.join(DOCS, "media"))

    posts = load_posts() if BLOG_ENABLED else []
    slugs = {}
    cards = []
    all_tags = []
    for p in posts:
        slug = p.get("slug") or re.sub(r"[^a-z0-9]+", "-", (p.get("title") or "").lower()).strip("-")
        p["slug"] = slug
        slugs[slug] = p
        tags = p.get("tag_list") or []
        for t in tags:
            if t not in all_tags:
                all_tags.append(t)
        cards.append(
            f'<a class="card card-link" href="{html_esc(slug)}.html" data-tags="{html_esc(",".join(tags))}">'
            f'<h3>{html_esc(p.get("title", ""))}</h3>'
            f'<div class="meta"><span class="date">{html_esc(fmt_long(p["date"]))}</span> · {html_esc(p.get("author") or "Author")}</div>'
            f'<p>{html_esc(p.get("excerpt", ""))}</p>'
            f'<p class="tags">{tag_pills(tags)}</p></a>'
        )
        note = (p.get("note") or "").strip()
        note_html = (" " + html_esc(note)) if note else ""
        page = (
            post_tpl
            .replace("/*__CSS__*/", css)
            .replace("/*__POST_TITLE__*/", html_esc(p.get("title", "")))
            .replace("/*__AUTHOR__*/", html_esc(p.get("author") or "Author"))
            .replace("/*__DATE__*/", html_esc(fmt_long(p["date"])))
            .replace("/*__SOURCE__*/", html_esc(p.get("source", "")))
            .replace("/*__NOTE__*/", note_html)
            .replace("/*__TAGS__*/", tag_pills(tags))
            .replace("/*__VERSION__*/", VERSION)
            .replace("/*__BUILT__*/", TODAY)
            .replace("<!--__BODY__-->", render_body(p["body"]))
        )
        write(os.path.join(DOCS, slug + ".html"), page)

    filter_btns = ['<button type="button" class="tag on" data-tag="all">All</button>']
    for t in all_tags:
        filter_btns.append(f'<button type="button" class="tag" data-tag="{html_esc(t)}">{html_esc(t)}</button>')
    posts_html = "\n".join(cards) if cards else (
        "<p>Post pages are turned off (<code>BLOG_ENABLED = False</code> in build.py). "
        "Source files remain in <code>content/posts/</code>.</p>"
        if not BLOG_ENABLED else "<p>No published posts yet.</p>"
    )
    home = (
        home_tpl
        .replace("/*__CSS__*/", css)
        .replace("<!--__FILTERS__-->", "".join(filter_btns) if cards else "")
        .replace("<!--__POSTS__-->", posts_html)
        .replace("/*__VERSION__*/", VERSION)
        .replace("/*__BUILT__*/", TODAY)
    )
    write(os.path.join(DOCS, "index.html"), home)

    about = (
        about_tpl
        .replace("/*__CSS__*/", css)
        .replace("/*__VERSION__*/", VERSION)
        .replace("/*__BUILT__*/", TODAY)
    )
    write(os.path.join(DOCS, "about.html"), about)

    research = load_research()
    republished_html = []
    for item in research.get("republished") or []:
        url = item.get("original_url") or ""
        slug = url.rstrip("/").rsplit("/", 1)[-1] if url else ""
        local = slug if slug in slugs else None
        republished_html.append(archive_card(item, local_slug=local))
    located_html = [archive_card(item) for item in research.get("also_located") or []]
    archive = (
        archive_tpl
        .replace("/*__CSS__*/", css)
        .replace("<!--__REPUBLISHED__-->", "\n".join(republished_html) or "<p>None listed.</p>")
        .replace("<!--__LOCATED__-->", "\n".join(located_html) or "<p>None listed.</p>")
        .replace("/*__VERSION__*/", VERSION)
        .replace("/*__BUILT__*/", TODAY)
    )
    write(os.path.join(DOCS, "archive.html"), archive)

    drafts = []
    if os.path.isdir(POSTS_DIR):
        for fn in os.listdir(POSTS_DIR):
            if fn.endswith(".md"):
                p = parse_post(open(os.path.join(POSTS_DIR, fn), encoding="utf-8").read())
                if p["is_draft"]:
                    drafts.append(fn)
    print(f"Built v{VERSION} on {TODAY} -> {DOCS}")
    print(f"  BLOG_ENABLED={BLOG_ENABLED}")
    print(f"  published posts: {len(posts)}")
    print(f"  drafts excluded: {len(drafts)}" + (f" ({', '.join(drafts)})" if drafts else ""))
    return posts


if __name__ == "__main__":
    try:
        build()
    except Exception as ex:
        print("build failed:", ex, file=sys.stderr)
        sys.exit(1)
