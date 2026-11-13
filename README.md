# 5G Regulatory Compliance

A professional blog on mortgage regulatory compliance by Ben Giumarra and Gregg Oberg, with help from Grok. **3G** = Giumarra, Gregg, and Grok.

Published on GitHub Pages at [https://greggoberg39-rgb.github.io/5g-compliance/](https://greggoberg39-rgb.github.io/5g-compliance/). This folder is the local copy of the site.

## What’s in this folder

- `site/` — the static site. Run the build from here.
- `site/config.json` — site name, tagline, navigation, site URL, and share settings (the reskin point for branding).
- `site/content/posts/` — one Markdown file per post (front matter + body).
- `site/content/resources/` — Resource Library entries (front matter + body, plus optional data files).
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

## How to add a resource

1. Add a Markdown file in `site/content/resources/` with front matter (`title`, `date`, `excerpt`, `slug`, `author`). The body can be Markdown or HTML (HTML is used as-is if the body starts with `<`).
2. Optional front matter: `canvas_url` and `canvas_note` (a link to an interactive companion page, listed on the index and near the top of the resource), `widget: state-spectrum` plus `data: some-file.json` for a 50-state map/table widget, or `draft: true` to keep it out of the build.
3. Rebuild with `python3 build.py` from the `site` folder.

## Turn the posts off (BLOG_ENABLED)

At the top of `site/build.py` is a switch:

```
BLOG_ENABLED = True
```

Set it to `False` and run `python3 build.py` again. Post pages and home-page cards disappear; the files in `content/posts/` are left in place. The About, Archive, and Resources pages still build. Set it back to `True` and rebuild to restore them.

## Requirements

Python 3 only. No extra packages.

## Changelog

### 1.2.0 — 2026-11-13

- Added a share bar to every post and every Resource Library page (after the title/byline and again at the end): Share on X, LinkedIn, Gmail, Email, Copy link, and a native Share button on devices that support it.
- Share buttons are plain links plus a small bit of vanilla JavaScript. No third-party scripts or trackers.
- Posts and resource pages now include Open Graph and Twitter Card tags so links preview with a title, excerpt, and a branded 1200×630 image (`site/content/media/share-card.png`).
- Site URL, X handle, default share image, and which share buttons appear all live in `site/config.json`.
- Footer version bumped to 1.2.0.

### 1.1.0 — 2026-11-13

- Added a public Resource Library (`/resources/`), driven by Markdown files in `site/content/resources/` and site branding/nav in `site/config.json`.
- Every page header now includes a Resources nav link.
- First resource: a 50-state (plus D.C.) map and table on consumer protection vs. sanctity of contract, at `/resources/consumer-protection-vs-contract/`.
- Footer version bumped to 1.1.0.

### 1.0.0 — 2026-11-12

- First local scaffold of the 5G Regulatory Compliance site.
- Home page is a post card index (title, author, date, excerpt, topic tags) with a simple tag filter.
- About page credits Ben Giumarra and Gregg Oberg.
- Archive page lists 2017–2018 RIMBA posts (republished pieces plus other located posts as links only).
- Twelve RIMBA posts republished in full with permission, each with an “Originally published at” link. `HMDA on Hold?` is credited to Gregg Oberg, as the original page states and as Gregg confirmed.
- One unpublished draft (`draft-qm-after-the-gse-patch.md`) is kept in `content/posts/` and excluded from the build.
- Version number in the footer. Output goes to `docs/` for a later GitHub Pages publish, which has not been done.
