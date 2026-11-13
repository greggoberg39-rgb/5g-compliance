#!/usr/bin/env python3
"""Convert an exported 5GRC Google Doc into a blog post for this site.

The source can be Markdown or HTML, as returned by the Google Drive
connector (export_file format=md or format=html, or read_file which
returns Markdown).

The Doc must start with a header block:

    Title: ...
    Author: Ben Giumarra   (or Gregg Oberg, or both)
    Tags: HMDA, CFPB
    Summary (1-2 sentences): ...
    Date: YYYY-MM-DD          (optional; defaults to today)
    Slug: short-url-name      (optional; derived from the title)

Everything after that block is the post body.

Usage:
    python3 drive_to_post.py path/to/export.md
    python3 drive_to_post.py path/to/export.html --date 2026-11-13
    python3 drive_to_post.py path/to/export.md --dry-run
    python3 drive_to_post.py path/to/export.md --allow-placeholder

Writes site/content/posts/YYYY-MM-DD-slug.md with front matter in the
same shape build.py already parses. Does not build, commit, or push;
see PUBLISHING.md for the daily routine.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
POSTS_DIR = os.path.join(REPO, "site", "content", "posts")

KNOWN_TAGS = ["HMDA", "TRID", "RESPA", "CFPB", "Flood", "Servicing", "QM"]
TAG_LOOKUP = {t.lower(): t for t in KNOWN_TAGS}

CANONICAL_AUTHORS = {
    "ben giumarra": "Ben Giumarra",
    "gregg oberg": "Gregg Oberg",
    "3g": "3G",
}

PLACEHOLDER_TITLES = {
    "your post title here",
    "post title",
    "title",
    "untitled",
}
PLACEHOLDER_AUTHORS = {
    "ben giumarra / gregg oberg",
    "ben giumarra/gregg oberg",
    "ben giumarra / gregg oberg",
}

LABEL_RE = re.compile(
    r"^\s*(?:\*\*)?(Title|Author|Tags|Date|Slug|Summary(?:\s*\(1-2 sentences\))?|Excerpt)(?:\*\*)?\s*:\s*(.*)$",
    re.IGNORECASE,
)


def fm_quote(value: str) -> str:
    return '"' + (value or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return slug


def normalize_tags(raw: str) -> str:
    parts = [p.strip() for p in re.split(r"[,;]", raw or "") if p.strip()]
    out = []
    for p in parts:
        out.append(TAG_LOOKUP.get(p.lower(), p))
    return ", ".join(out)


def normalize_author(raw: str) -> str:
    text = re.sub(r"\s+", " ", (raw or "").strip())
    if not text:
        return text
    key = text.lower().replace(" and ", " / ").replace("&", "/")
    key = re.sub(r"\s*/\s*", " / ", key)
    if key in PLACEHOLDER_AUTHORS:
        return text
    if " / " in key or " & " in key.lower():
        bits = re.split(r"\s*/\s*|\s+and\s+|\s*&\s*", text, flags=re.I)
        names = [CANONICAL_AUTHORS.get(b.strip().lower(), b.strip()) for b in bits if b.strip()]
        return " and ".join(names)
    return CANONICAL_AUTHORS.get(text.lower(), text)


def is_placeholder_title(title: str) -> bool:
    return (title or "").strip().lower() in PLACEHOLDER_TITLES or not (title or "").strip()


def is_placeholder_author(author: str) -> bool:
    key = re.sub(r"\s+", " ", (author or "").strip().lower())
    key = key.replace(" and ", " / ")
    key = re.sub(r"\s*/\s*", " / ", key)
    return (not key) or key in PLACEHOLDER_AUTHORS


class _DocHTML(HTMLParser):
    """Turn a Google-Docs HTML export into a Markdown-ish string."""

    SKIP = {"style", "script", "head", "title"}
    VOID_SKIP = {"meta", "link"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks: list[str] = []
        self._skip = 0
        self._href: str | None = None
        self._li_prefix = "- "

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag in self.VOID_SKIP:
            return
        if tag in self.SKIP:
            self._skip += 1
            return
        if self._skip:
            return
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "tr", "table"):
            self.chunks.append("\n")
        if tag == "h1":
            self.chunks.append("\n# ")
        elif tag == "h2":
            self.chunks.append("\n## ")
        elif tag == "h3":
            self.chunks.append("\n### ")
        elif tag == "h4":
            self.chunks.append("\n#### ")
        elif tag == "br":
            self.chunks.append("\n")
        elif tag == "li":
            self.chunks.append("\n" + self._li_prefix)
        elif tag == "ul":
            self._li_prefix = "- "
            self.chunks.append("\n")
        elif tag == "ol":
            self._li_prefix = "1. "
            self.chunks.append("\n")
        elif tag in ("strong", "b"):
            self.chunks.append("**")
        elif tag in ("em", "i"):
            self.chunks.append("*")
        elif tag == "a":
            self._href = attrs_d.get("href")
            self.chunks.append("[")
        elif tag == "img":
            alt = attrs_d.get("alt") or ""
            src = attrs_d.get("src") or ""
            if src:
                self.chunks.append(f"![{alt}]({src})")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            if self._skip:
                self._skip -= 1
            return
        if self._skip:
            return
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "tr", "ul", "ol"):
            self.chunks.append("\n")
        elif tag in ("strong", "b"):
            self.chunks.append("**")
        elif tag in ("em", "i"):
            self.chunks.append("*")
        elif tag == "a":
            href = self._href or ""
            self.chunks.append(f"]({href})" if href else "]")
            self._href = None

    def handle_data(self, data):
        if self._skip:
            return
        self.chunks.append(data)


def html_to_markdown(raw: str) -> str:
    parser = _DocHTML()
    parser.feed(raw)
    text = unescape("".join(parser.chunks))
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def looks_like_html(text: str) -> bool:
    s = text.lstrip().lower()
    return s.startswith("<!doctype html") or s.startswith("<html") or (
        s.startswith("<") and "</" in s[:1000] and re.search(r"<body|<p[\s>]|<h1[\s>]", s)
    )


def parse_header_and_body(text: str) -> tuple[dict, str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i = 0
    n = len(lines)
    while i < n and not lines[i].strip():
        i += 1
    # Skip a leading document-title heading such as "# Post Template"
    if i < n and re.match(r"^#\s+", lines[i]):
        heading = re.sub(r"^#\s+", "", lines[i]).strip().strip("*").lower()
        if heading in {"post template", "how to post (read me)", "how to post"} or heading.startswith("how to post"):
            i += 1
            while i < n and not lines[i].strip():
                i += 1

    meta: dict[str, str] = {}
    current = None
    while i < n:
        line = lines[i]
        m = LABEL_RE.match(line.strip())
        if m:
            raw_label = m.group(1).lower()
            if raw_label.startswith("summary") or raw_label == "excerpt":
                key = "excerpt"
            else:
                key = raw_label
            meta[key] = m.group(2).strip()
            current = key
            i += 1
            continue
        # Continuation of a multi-line summary, or the end of the header.
        if current and not line.strip():
            # A blank line after a filled field ends the header once we have a title
            # and have left room for remaining fields. Peek ahead: if the next
            # non-empty line is another label, keep going; if it is a heading or
            # body text, stop.
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and LABEL_RE.match(lines[j].strip()):
                i += 1
                continue
            break
        if current and not re.match(r"^#{1,6}\s+", line.strip()) and not LABEL_RE.match(line.strip()):
            # Append wrapped header values (common for Summary).
            extra = line.strip()
            if extra:
                meta[current] = (meta.get(current, "") + " " + extra).strip()
            i += 1
            continue
        break

    while i < n and not lines[i].strip():
        i += 1
    body = "\n".join(lines[i:]).strip() + ("\n" if i < n else "")
    return meta, body


def existing_slugs(posts_dir: str) -> dict[str, str]:
    found = {}
    if not os.path.isdir(posts_dir):
        return found
    for fn in os.listdir(posts_dir):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(posts_dir, fn)
        try:
            text = open(path, encoding="utf-8").read()
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        try:
            _lead, fm, _body = text.split("---", 2)
        except ValueError:
            continue
        slug = ""
        for line in fm.splitlines():
            if line.startswith("slug:"):
                slug = line.split(":", 1)[1].strip().strip('"')
                break
        if not slug:
            slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", fn[:-3])
            if fn.startswith("draft-"):
                slug = fn[6:-3]
        found[slug] = fn
    return found


def render_post(meta: dict, body: str, date: str) -> str:
    title = (meta.get("title") or "").strip()
    author = normalize_author(meta.get("author") or "")
    tags = normalize_tags(meta.get("tags") or "")
    excerpt = re.sub(r"\s+", " ", (meta.get("excerpt") or "").strip())
    slug = slugify(meta.get("slug") or title)
    date_val = (meta.get("date") or date or "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_val):
        raise SystemExit(f"Invalid date {date_val!r}; use YYYY-MM-DD")
    if not title:
        raise SystemExit("Missing Title: in the header block")
    if not slug:
        raise SystemExit("Could not derive a slug from the title")
    if not author:
        raise SystemExit("Missing Author: in the header block")
    lines = [
        "---",
        f"title: {fm_quote(title)}",
        f"date: {date_val}",
        f"author: {author}",
        f"excerpt: {fm_quote(excerpt)}",
        f"slug: {fm_quote(slug)}",
        f"tags: {fm_quote(tags)}",
        "---",
        "",
        body.rstrip() + "\n",
    ]
    return "\n".join(lines), slug, date_val, title


def load_source(path: str) -> str:
    text = open(path, encoding="utf-8").read()
    if looks_like_html(text):
        return html_to_markdown(text)
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Exported Doc: .md, .html, or .txt")
    parser.add_argument("--date", help="Publish date YYYY-MM-DD (default: today, or Date: in the Doc)")
    parser.add_argument("--out-dir", default=POSTS_DIR, help="Destination folder for the post file")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing file with the same name or slug")
    parser.add_argument("--dry-run", action="store_true", help="Print the post to stdout; do not write a file")
    parser.add_argument(
        "--allow-placeholder",
        action="store_true",
        help="Allow the Post Template placeholder title/author (for local tests only)",
    )
    args = parser.parse_args(argv)

    if not os.path.isfile(args.source):
        print(f"Source not found: {args.source}", file=sys.stderr)
        return 1

    today = args.date or datetime.date.today().isoformat()
    text = load_source(args.source)
    meta, body = parse_header_and_body(text)

    if args.date:
        meta["date"] = args.date
    elif not (meta.get("date") or "").strip():
        meta["date"] = today

    title = (meta.get("title") or "").strip()
    author = (meta.get("author") or "").strip()
    if is_placeholder_title(title) or is_placeholder_author(author):
        msg = (
            "Header still has placeholder Title or Author. "
            "Fill those in before publishing, or pass --allow-placeholder for a local test."
        )
        if not args.allow_placeholder:
            print(msg, file=sys.stderr)
            return 2
        print("warning: " + msg, file=sys.stderr)

    rendered, slug, date_val, title = render_post(meta, body, today)
    filename = f"{date_val}-{slug}.md"
    dest = os.path.join(args.out_dir, filename)

    slugs = existing_slugs(args.out_dir)
    if slug in slugs and os.path.join(args.out_dir, slugs[slug]) != dest and not args.force:
        print(
            f"Slug {slug!r} already used by {slugs[slug]}. Pick a different title/slug or pass --force.",
            file=sys.stderr,
        )
        return 3
    if os.path.exists(dest) and not args.force and not args.dry_run:
        print(f"Refusing to overwrite {dest}. Pass --force to replace it.", file=sys.stderr)
        return 3

    if args.dry_run:
        sys.stdout.write(rendered)
        print(f"\n# would write {dest}", file=sys.stderr)
        return 0

    os.makedirs(args.out_dir, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(dest)
    print(f"slug={slug}")
    print(f"title={title}")
    print(f"date={date_val}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
