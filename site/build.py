#!/usr/bin/env python3
"""Build the 5G Regulatory Compliance static site.

Usage:  python3 build.py

Reads Markdown posts from content/posts/, resource files from
content/resources/, templates from templates/, and site branding from
config.json. Copies media and writes a static site to docs/ (for GitHub Pages).

The card index, per-post pages, front-matter parser, multi-author cards,
permission credit, version footer, and BLOG_ENABLED switch follow the
data-driven blog engine this site was adapted from. Set BLOG_ENABLED = False
to skip generating post pages and hide post cards (source files stay in
content/posts/). Drafts (front matter draft: true) are always excluded.
The Resource Library still builds.

No heavy dependencies — Python 3 only.
"""
import datetime, json, os, re, shutil, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
VERSION = "1.2.0"
# Set to False to hide post cards and skip generating post pages
# (files stay in content/posts/). About and Archive still build.
BLOG_ENABLED = True

CONTENT = os.path.join(HERE, "content")
POSTS_DIR = os.path.join(CONTENT, "posts")
MEDIA_SRC = os.path.join(CONTENT, "media")
TPL_DIR = os.path.join(HERE, "templates")
DOCS = os.path.join(HERE, "docs")
CONFIG_PATH = os.path.join(HERE, "config.json")
RESOURCES_DIR = os.path.join(CONTENT, "resources")
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



DEFAULT_SHARE_BUTTONS = ("x", "linkedin", "gmail", "email", "copy", "native")

SHARE_ICONS = {
    "x": '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.727-8.835L1.254 2.25H8.08l4.253 5.622L18.244 2.25zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zM7.119 20.452H3.554V9h3.565v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    "gmail": '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5L4 8V6l8 5 8-5v2z"/></svg>',
    "email": '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6zm-2 0-8 5-8-5h16zm0 12H4V8l8 5 8-5v10z"/></svg>',
    "copy": '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7C4.24 7 2 9.24 2 12s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>',
    "native": '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11A2.99 2.99 0 0 0 21 5a3 3 0 1 0-2.96 2.39L11 11.5v.99l7.04 4.11A2.99 2.99 0 0 0 21 19a3 3 0 1 0-3-2.92z"/></svg>',
}

SHARE_SCRIPT = """<script>
(function(){
  function fallbackCopy(url, done){
    var ta = document.createElement("textarea");
    ta.value = url;
    ta.setAttribute("readonly", "");
    ta.style.position = "absolute";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); done(); } catch (e) {}
    document.body.removeChild(ta);
  }
  var bars = document.querySelectorAll(".share-bar");
  bars.forEach(function(bar){
    var nativeBtn = bar.querySelector(".share-native");
    if (nativeBtn && navigator.share) {
      nativeBtn.hidden = false;
      nativeBtn.addEventListener("click", function(){
        navigator.share({
          title: bar.getAttribute("data-share-title") || document.title,
          text: bar.getAttribute("data-share-text") || "",
          url: bar.getAttribute("data-share-url") || window.location.href
        }).catch(function(){});
      });
    }
    var copyBtn = bar.querySelector(".share-copy");
    if (copyBtn) {
      copyBtn.addEventListener("click", function(){
        var url = bar.getAttribute("data-share-url") || window.location.href;
        var label = copyBtn.querySelector(".share-label-text");
        var prev = label ? label.textContent : "Copy link";
        var done = function(){
          copyBtn.classList.add("copied");
          if (label) label.textContent = "Copied!";
          copyBtn.setAttribute("aria-label", "Copied!");
          setTimeout(function(){
            copyBtn.classList.remove("copied");
            if (label) label.textContent = prev;
            copyBtn.setAttribute("aria-label", "Copy link");
          }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done).catch(function(){ fallbackCopy(url, done); });
        } else {
          fallbackCopy(url, done);
        }
      });
    }
  });
})();
</script>"""


def absolute_url(config, path):
    base = (config.get("site_url") or "").rstrip("/")
    path = (path or "").lstrip("/")
    if not base:
        return path
    return base + ("/" + path if path else "")


def share_settings(config):
    share = config.get("share") or {}
    handle = (share.get("x_handle") or "").strip().lstrip("@")
    buttons = share.get("buttons") or list(DEFAULT_SHARE_BUTTONS)
    og_image = (share.get("og_image") or "media/share-card.png").lstrip("/")
    return {"x_handle": handle, "buttons": buttons, "og_image": og_image}


def social_meta(config, *, title, description, url, og_type="article"):
    settings = share_settings(config)
    image = absolute_url(config, settings["og_image"])
    site_name = config.get("site_name") or ""
    handle = settings["x_handle"]
    parts = [
        f'<meta name="description" content="{html_esc(description)}">',
        f'<link rel="canonical" href="{html_esc(url)}">',
        f'<meta property="og:title" content="{html_esc(title)}">',
        f'<meta property="og:description" content="{html_esc(description)}">',
        f'<meta property="og:url" content="{html_esc(url)}">',
        f'<meta property="og:type" content="{html_esc(og_type)}">',
        f'<meta property="og:image" content="{html_esc(image)}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{html_esc(site_name)}">',
        f'<meta property="og:site_name" content="{html_esc(site_name)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html_esc(title)}">',
        f'<meta name="twitter:description" content="{html_esc(description)}">',
        f'<meta name="twitter:image" content="{html_esc(image)}">',
    ]
    if handle:
        parts.append(f'<meta name="twitter:site" content="@{html_esc(handle)}">')
        parts.append(f'<meta name="twitter:creator" content="@{html_esc(handle)}">')
    return "\n".join(parts)


def _share_item(kind, href, label, extra_class="", tag="a", attrs=""):
    icon = SHARE_ICONS[kind]
    cls = f"share-btn share-{kind}{(' ' + extra_class) if extra_class else ''}"
    inner = f'{icon}<span class="share-label-text">{html_esc(label)}</span>'
    if tag == "a":
        return (
            f'<li><a class="{cls}" href="{html_esc(href)}" target="_blank" '
            f'rel="noopener noreferrer" aria-label="{html_esc(label)}">{inner}</a></li>'
        )
    return (
        f'<li><button type="button" class="{cls}" aria-label="{html_esc(label)}"'
        f'{attrs}>{inner}</button></li>'
    )


def share_bar(config, *, title, excerpt, url, position="top"):
    settings = share_settings(config)
    q_title = quote(title or "", safe="")
    q_url = quote(url or "", safe="")
    body = (excerpt or "").strip()
    if body and url:
        body = body + "\n\n" + url
    elif url:
        body = url
    q_body = quote(body, safe="")
    tweet = f"https://twitter.com/intent/tweet?text={q_title}&url={q_url}"
    if settings["x_handle"]:
        tweet += "&via=" + quote(settings["x_handle"], safe="")
    items = []
    for kind in settings["buttons"]:
        if kind == "x":
            items.append(_share_item("x", tweet, "Share on X"))
        elif kind == "linkedin":
            items.append(_share_item(
                "linkedin",
                "https://www.linkedin.com/sharing/share-offsite/?url=" + q_url,
                "Share on LinkedIn",
            ))
        elif kind == "gmail":
            items.append(_share_item(
                "gmail",
                f"https://mail.google.com/mail/?view=cm&fs=1&su={q_title}&body={q_body}",
                "Share via Gmail",
            ))
        elif kind == "email":
            # mailto should stay in the same tab; render as a plain link without target=_blank
            icon = SHARE_ICONS["email"]
            href = f"mailto:?subject={q_title}&body={q_body}"
            items.append(
                f'<li><a class="share-btn share-email" href="{html_esc(href)}" '
                f'aria-label="Share by email">'
                f'{icon}<span class="share-label-text">Email</span></a></li>'
            )
        elif kind == "copy":
            items.append(_share_item("copy", "", "Copy link", tag="button"))
        elif kind == "native":
            items.append(
                _share_item("native", "", "Share", tag="button", attrs=" hidden")
            )
    if not items:
        return ""
    pos_cls = "share-bar-top" if position == "top" else "share-bar-bottom"
    return (
        f'<nav class="share-bar {pos_cls}" aria-label="Share this page" '
        f'data-share-url="{html_esc(url)}" data-share-title="{html_esc(title)}" '
        f'data-share-text="{html_esc((excerpt or "").strip())}">'
        f'<ul class="share-list">{"".join(items)}</ul></nav>'
    )


def share_bundle(config, *, title, excerpt, url, og_type="article"):
    """Social meta, top and bottom share bars, and the one-time share script."""
    return {
        "<!--__SOCIAL_META__-->": social_meta(
            config, title=title, description=excerpt or "", url=url, og_type=og_type
        ),
        "<!--__SHARE_TOP__-->": share_bar(
            config, title=title, excerpt=excerpt, url=url, position="top"
        ),
        "<!--__SHARE_BOTTOM__-->": share_bar(
            config, title=title, excerpt=excerpt, url=url, position="bottom"
        ),
        "<!--__SHARE_SCRIPT__-->": SHARE_SCRIPT,
    }


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


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def rel_path(target, depth):
    return ("../" * depth) + target


def render_nav(config, active, depth):
    links = []
    for item in config.get("nav") or []:
        cls = ' class="on"' if item.get("id") == active else ""
        href = rel_path(item.get("href") or "", depth)
        links.append(f'<a href="{html_esc(href)}"{cls}>{html_esc(item.get("label") or "")}</a>')
    return "\n  ".join(links)


def apply_chrome(tpl, config, *, active, depth, **extra):
    """Fill branding, nav, version, and any extra __placeholders__."""
    text = (
        tpl
        .replace("<!--__HOME_HREF__-->", html_esc(rel_path("index.html", depth)))
        .replace("<!--__NAV__-->", render_nav(config, active, depth))
        .replace("/*__SITE_NAME__*/", html_esc(config.get("site_name") or ""))
        .replace("/*__SHORT_NAME__*/", html_esc(config.get("short_name") or ""))
        .replace("/*__TAGLINE__*/", html_esc(config.get("tagline") or ""))
        .replace("/*__FOOTER_NOTE__*/", html_esc(config.get("footer_note") or ""))
        .replace("/*__VERSION__*/", VERSION)
        .replace("/*__BUILT__*/", TODAY)
    )
    for key, value in extra.items():
        text = text.replace(key, value)
    return text


def load_resources():
    if not os.path.isdir(RESOURCES_DIR):
        return []
    resources = []
    for fn in os.listdir(RESOURCES_DIR):
        if not fn.endswith(".md"):
            continue
        r = parse_post(open(os.path.join(RESOURCES_DIR, fn), encoding="utf-8").read())
        r["_file"] = fn
        if r["is_draft"]:
            continue
        if not r.get("slug"):
            r["slug"] = re.sub(r"[^a-z0-9]+", "-", (r.get("title") or "").lower()).strip("-")
        resources.append(r)
    resources.sort(key=lambda r: (r.get("date") or "", r.get("title") or ""), reverse=True)
    return resources


def canvas_note_html(resource):
    url = (resource.get("canvas_url") or "").strip()
    if not url:
        return ""
    label = (resource.get("canvas_note") or "Also available as an interactive page").strip()
    return f'<p class="canvas-note"><a href="{html_esc(url)}">{html_esc(label)}</a>.</p>'


def render_widget(resource):
    widget = (resource.get("widget") or "").strip()
    if widget != "state-spectrum":
        return "", ""
    data_name = (resource.get("data") or "").strip()
    if not data_name or "/" in data_name or "\\" in data_name:
        raise ValueError(f"resource {resource.get('_file')} is missing a safe data file name")
    data_path = os.path.join(RESOURCES_DIR, data_name)
    if not os.path.isfile(data_path):
        raise ValueError(f"resource data file not found: {data_name}")
    data = open(data_path, encoding="utf-8").read()
    markup = open(os.path.join(TPL_DIR, "_widget_state_spectrum.html"), encoding="utf-8").read()
    script = open(os.path.join(TPL_DIR, "_widget_state_spectrum.js"), encoding="utf-8").read()
    markup = markup.replace("/*__STATE_DATA__*/", data)
    return markup, "<script>\n" + script + "\n</script>"


def resource_card(resource):
    title = html_esc(resource.get("title") or "")
    date = html_esc(fmt_long(resource["date"]) if resource.get("date") else "")
    excerpt = html_esc(resource.get("excerpt") or "")
    slug = html_esc(resource.get("slug") or "")
    canvas = ""
    url = (resource.get("canvas_url") or "").strip()
    if url:
        label = (resource.get("canvas_note") or "Also available as an interactive page").strip()
        canvas = (
            f'<p class="meta"><a href="{html_esc(url)}">{html_esc(label)}</a></p>'
        )
    return (
        f'<div class="card resource-card">'
        f'<a class="card-link-inner" href="{slug}/">'
        f"<h3>{title}</h3>"
        f'<div class="meta"><span class="date">{date}</span></div>'
        f"<p>{excerpt}</p>"
        f"</a>"
        f"{canvas}"
        f"</div>"
    )



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
    config = load_config()
    css = open(os.path.join(TPL_DIR, "_shared.css"), encoding="utf-8").read()
    home_tpl = open(os.path.join(TPL_DIR, "_home.html"), encoding="utf-8").read()
    post_tpl = open(os.path.join(TPL_DIR, "_post.html"), encoding="utf-8").read()
    about_tpl = open(os.path.join(TPL_DIR, "_about.html"), encoding="utf-8").read()
    archive_tpl = open(os.path.join(TPL_DIR, "_archive.html"), encoding="utf-8").read()
    resources_tpl = open(os.path.join(TPL_DIR, "_resources.html"), encoding="utf-8").read()
    resource_tpl = open(os.path.join(TPL_DIR, "_resource.html"), encoding="utf-8").read()

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
        page = apply_chrome(
            post_tpl,
            config,
            active="",
            depth=0,
            **{
                "/*__CSS__*/": css,
                "/*__POST_TITLE__*/": html_esc(p.get("title", "")),
                "/*__AUTHOR__*/": html_esc(p.get("author") or "Author"),
                "/*__DATE__*/": html_esc(fmt_long(p["date"])),
                "/*__SOURCE__*/": html_esc(p.get("source", "")),
                "/*__NOTE__*/": note_html,
                "/*__TAGS__*/": tag_pills(tags),
                "<!--__BODY__-->": render_body(p["body"]),
                **share_bundle(
                    config,
                    title=p.get("title") or "",
                    excerpt=p.get("excerpt") or "",
                    url=absolute_url(config, slug + ".html"),
                    og_type="article",
                ),
            },
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
    home = apply_chrome(
        home_tpl,
        config,
        active="home",
        depth=0,
        **{
            "/*__CSS__*/": css,
            "<!--__FILTERS__-->": "".join(filter_btns) if cards else "",
            "<!--__POSTS__-->": posts_html,
        },
    )
    write(os.path.join(DOCS, "index.html"), home)

    about = apply_chrome(about_tpl, config, active="about", depth=0, **{"/*__CSS__*/": css})
    write(os.path.join(DOCS, "about.html"), about)

    research = load_research()
    republished_html = []
    for item in research.get("republished") or []:
        url = item.get("original_url") or ""
        slug = url.rstrip("/").rsplit("/", 1)[-1] if url else ""
        local = slug if slug in slugs else None
        republished_html.append(archive_card(item, local_slug=local))
    located_html = [archive_card(item) for item in research.get("also_located") or []]
    archive = apply_chrome(
        archive_tpl,
        config,
        active="archive",
        depth=0,
        **{
            "/*__CSS__*/": css,
            "<!--__REPUBLISHED__-->": "\n".join(republished_html) or "<p>None listed.</p>",
            "<!--__LOCATED__-->": "\n".join(located_html) or "<p>None listed.</p>",
        },
    )
    write(os.path.join(DOCS, "archive.html"), archive)

    resources = load_resources()
    resource_cards = []
    for r in resources:
        slug = r["slug"]
        widget_html, widget_script = render_widget(r)
        disclaimer = (r.get("disclaimer") or (
            "This is general research and commentary, not legal advice "
            "and not an official publication of RIMBA or of any employer."
        )).strip()
        page = apply_chrome(
            resource_tpl,
            config,
            active="resources",
            depth=2,
            **{
                "/*__CSS__*/": css,
                "/*__RESOURCE_TITLE__*/": html_esc(r.get("title") or ""),
                "/*__AUTHOR__*/": html_esc(r.get("author") or config.get("site_name") or ""),
                "/*__DATE__*/": html_esc(fmt_long(r["date"]) if r.get("date") else ""),
                "<!--__CANVAS_NOTE__-->": canvas_note_html(r),
                "/*__DISCLAIMER__*/": html_esc(disclaimer),
                "<!--__WIDGET__-->": widget_html,
                "<!--__BODY__-->": render_body(r["body"]),
                "<!--__WIDGET_SCRIPT__-->": widget_script,
                "<!--__RESOURCES_HREF__-->": html_esc(rel_path("resources/", 2)),
                **share_bundle(
                    config,
                    title=r.get("title") or "",
                    excerpt=r.get("excerpt") or "",
                    url=absolute_url(config, f"resources/{slug}/"),
                    og_type="article",
                ),
            },
        )
        write(os.path.join(DOCS, "resources", slug, "index.html"), page)
        resource_cards.append(resource_card(r))

    resources_page = apply_chrome(
        resources_tpl,
        config,
        active="resources",
        depth=1,
        **{
            "/*__CSS__*/": css,
            "<!--__RESOURCES__-->": "\n".join(resource_cards) or "<p>No resources published yet.</p>",
            **share_bundle(
                config,
                title="Resource Library",
                excerpt=(
                    "Reference pieces for mortgage compliance work — maps, surveys, "
                    "and explainers that are meant to be used more than once, not just read as a post."
                ),
                url=absolute_url(config, "resources/"),
                og_type="website",
            ),
        },
    )
    write(os.path.join(DOCS, "resources", "index.html"), resources_page)

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
    print(f"  resources: {len(resources)}")
    print(f"  drafts excluded: {len(drafts)}" + (f" ({', '.join(drafts)})" if drafts else ""))
    return posts


if __name__ == "__main__":
    try:
        build()
    except Exception as ex:
        print("build failed:", ex, file=sys.stderr)
        sys.exit(1)
