# Daily publishing routine for 5G Regulatory Compliance

Ben and Gregg are equal partners. A finished Google Doc in **Drafts** is ready to go live; neither person has to approve the other's post. Do **not** share Drive folders or files from this routine (sharing sends email). Gregg shares the 5GRC folder with Ben himself.

The live site is [https://greggoberg39-rgb.github.io/5g-compliance/](https://greggoberg39-rgb.github.io/5g-compliance/). The repo is [greggoberg39-rgb/5g-compliance](https://github.com/greggoberg39-rgb/5g-compliance), branch `main`. GitHub Pages deploys the already-built files in `site/docs/` on every push to `main` (the workflow does not run `build.py`).

## Drive IDs (Gregg's My Drive)

| Item | ID | URL |
| --- | --- | --- |
| 5GRC | `1UeCLTXvGwOsuHyyS8C5UF92ly87ojBGn` | https://drive.google.com/drive/folders/1UeCLTXvGwOsuHyyS8C5UF92ly87ojBGn |
| Drafts | `12oEDsnlkoKtNRT3aoYXyrShH1c16W_SL` | https://drive.google.com/drive/folders/12oEDsnlkoKtNRT3aoYXyrShH1c16W_SL |
| Published | `10BRPudAP9BnO2csobEwLH-vVSaW_FzXi` | https://drive.google.com/drive/folders/10BRPudAP9BnO2csobEwLH-vVSaW_FzXi |
| Knowledge Base | `1V8NdJbtA6D985XWzZjiPl1UYPPI2_lvd` | https://drive.google.com/drive/folders/1V8NdJbtA6D985XWzZjiPl1UYPPI2_lvd |
| HOW TO POST (read me) | `1kt71-vfDUfDtH1ZMpWRAkmGpcqQKG7cdWBtGxK-dDgU` | https://docs.google.com/document/d/1kt71-vfDUfDtH1ZMpWRAkmGpcqQKG7cdWBtGxK-dDgU/edit |
| Post Template | `1yNuePTX8g1LfQGWyFe452WRB6Wei9qwRiSryePax5c4` | https://docs.google.com/document/d/1yNuePTX8g1LfQGWyFe452WRB6Wei9qwRiSryePax5c4/edit |

Use the `user-Google-drive` connector. Never invent these IDs; if a folder is missing, search Drive by exact name before creating a replacement.

## What a finished draft looks like

The Doc starts with this header block (labels must stay as written):

```
Title: ...
Author: Ben Giumarra
Tags: HMDA, CFPB
Summary (1-2 sentences): ...
```

`Author` is Ben Giumarra, Gregg Oberg, or both. Tags come from: HMDA, TRID, RESPA, CFPB, Flood, Servicing, QM. `Date:` and `Slug:` are optional. If `Date` is omitted, use the day the routine runs (America/New_York).

Skip a Doc and leave it in Drafts if:

- It is still the Post Template placeholder (`Title: Your post title here` or `Author: Ben Giumarra / Gregg Oberg`).
- It is named `Post Template` or `HOW TO POST (read me)` (those belong in the 5GRC root, not Drafts).
- It is a folder, shortcut, or not a Google Doc.
- `drive_to_post.py` exits non-zero.

## Steps the routine should follow each day

Work on a clean checkout of `greggoberg39-rgb/5g-compliance` at `main` (`/workspace/5g-compliance` on this computer). Do not push a test or placeholder post.

1. **List Drafts.** Call `list_folder` on Drafts (`12oEDsnlkoKtNRT3aoYXyrShH1c16W_SL`). Page with `nextPageToken` until the list is complete. Ignore everything that is not a Google Doc (`application/vnd.google-apps.document`).

2. **Export each new Doc.** For every remaining Doc, export Markdown with `export_file` (`fileId`, `format: "md"`) and save the decoded bytes to a temp file such as `/tmp/5grc-<fileId>.md`. `read_file` also returns Markdown and can be used the same way. HTML (`format: "html"`) is supported by the converter if Markdown export fails.

3. **Convert.** From the repo root:

   ```
   python3 tools/drive_to_post.py /tmp/5grc-<fileId>.md
   ```

   This writes `site/content/posts/YYYY-MM-DD-slug.md` with front matter matching `site/build.py` (`title`, `date`, `author`, `excerpt`, `slug`, `tags`). Do **not** pass `--allow-placeholder` in the daily routine. If the script exits 2 (placeholders) or 3 (slug/file clash), leave the Doc in Drafts and report it; do not publish.

4. **Build.** From `site/`:

   ```
   python3 build.py
   ```

   Confirm the new slug is counted in `published posts` and that `site/docs/<slug>.html` exists. If the build fails, stop, do not commit, and leave the Doc in Drafts.

5. **Commit.** Stage the new Markdown file under `site/content/posts/` **and** the updated built files under `site/docs/` (`index.html`, `archive.html` if touched, and `<slug>.html`). The Pages workflow publishes `site/docs/` as-is, so a Markdown-only commit will not go live. Commit message, for example: `Publish <title>`.

6. **Push to `greggoberg39-rgb/5g-compliance` `main`.** Wait about a minute for GitHub Pages to deploy.

7. **Verify the live URL returns 200.** Request:

   `https://greggoberg39-rgb.github.io/5g-compliance/<slug>.html`

   Also check the home page still returns 200. If Pages is still updating, wait and retry a few times (up to a few minutes). Do not move the Doc out of Drafts until this check succeeds.

8. **Move the Doc to Published.** Call `move_or_rename` with the Doc's `fileId` and `parentId` `10BRPudAP9BnO2csobEwLH-vVSaW_FzXi`. Do not rename it. Confirm with `get_file_metadata` or `list_folder` on Published that the parent changed. Then tell Ben and Gregg the live URL.

Repeat steps 2–8 for each ready Doc in Drafts, one post per commit if that keeps failures easier to isolate. If two Docs are both ready, publishing them in one build/commit/push is also fine, but still verify each live URL and move each Doc only after its URL returns 200.

## Converter reference

```
python3 tools/drive_to_post.py path/to/export.md
python3 tools/drive_to_post.py path/to/export.html --date 2026-11-13
python3 tools/drive_to_post.py path/to/export.md --dry-run
python3 tools/drive_to_post.py path/to/export.md --allow-placeholder   # local tests only
```

`--force` overwrites an existing post with the same filename or slug. Do not use it in the daily routine unless you are intentionally replacing a post.

Images in a Doc are not copied into `site/content/media/` automatically. If a post has images, save them under `site/content/media/`, point the Markdown at `media/<filename>`, rebuild, and include those files in the same commit.

The `Knowledge Base` folder is for source material, not for posts. Do not publish files from it.
