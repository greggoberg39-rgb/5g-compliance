# 5G Regulatory Compliance

A professional blog on mortgage regulatory compliance by Ben Giumarra and Gregg Oberg, with help from Grok. **3G** = Giumarra, Gregg, and Grok.

This folder is a local draft only. Nothing has been published, and no GitHub repository has been created.

## What’s in this folder

- `site/` — the static site. Run the build from here.
- `site/content/posts/` — one Markdown file per post (front matter + body).
- `site/content/media/` — images used in republished posts.
- `site/templates/` — HTML templates and CSS.
- `site/docs/` — the built site (this is what GitHub Pages would serve later).
- `research/` — inventory of 2017–2018 RIMBA posts (summaries and links).
- `preview-*.png` — local screenshots of the built home and a post page.

## How to add a post and rebuild

1. Copy an existing file in `site/content/posts/`, or start a new one named like `2026-11-12-short-title.md`.
2. Fill in the front matter at the top:

```
---
title: "Your title"
date: 2026-11-12
author: Gregg Oberg
excerpt: "One or two sentences for the home-page card."
slug: "short-url-name"
tags: "HMDA, TRID"
---
```

   Available topic tags: HMDA, TRID, RESPA, CFPB, Flood, Servicing, QM.

3. Write the body in Markdown (or HTML, which is used as-is). For a piece that is not ready to publish, add `draft: true` to the front matter. Drafts are not built into the site.
4. Open a terminal in the `site` folder and run:

```
python3 build.py
```

5. Open `site/docs/index.html` in a browser to check your work.

For a republished piece, include a `source:` URL in the front matter. The built page will add “Originally published at &lt;url&gt;” and a permission note automatically.

## Turn the posts off (BLOG_ENABLED)

At the top of `site/build.py` is a switch:

```
BLOG_ENABLED = True
```

Set it to `False` and run `python3 build.py` again. Post pages and home-page cards disappear; the files in `content/posts/` are left in place. The About and Archive pages still build. Set it back to `True` and rebuild to restore them.

## Requirements

Python 3 only. No extra packages.

## Changelog

### 1.0.0 — 2026-11-12

- First local scaffold of the 5G Regulatory Compliance site.
- Home page is a post card index (title, author, date, excerpt, topic tags) with a simple tag filter.
- About page credits Ben Giumarra and Gregg Oberg.
- Archive page lists 2017–2018 RIMBA posts (republished pieces plus other located posts as links only).
- Twelve RIMBA posts republished in full with permission, each with an “Originally published at” link. `HMDA on Hold?` is credited to Gregg Oberg, as the original page states and as Gregg confirmed.
- One unpublished draft (`draft-qm-after-the-gse-patch.md`) is kept in `content/posts/` and excluded from the build.
- Version number in the footer. Output goes to `docs/` for a later GitHub Pages publish, which has not been done.
