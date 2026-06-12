# Plumstead Baptist Church — Website

A simple church website built with **Python (Flask)** for local previewing and **HTML templates + CSS** for the actual pages. There is no database — all content lives in the templates and one shared partial. The site is designed to be easy to edit for someone with little coding experience; key sections are clearly commented in the code.

**The published site is fully static HTML** rendered ahead of time and hosted on **GitHub Pages**. Flask is only used as a convenient way to build the pages from templates; no Python runs on the live website.

---

## What this project does

- **Home page**: Rotating banner images, welcome message, “Who we are”, service times, latest YouTube sermon (refreshed when the site is rebuilt — see _Automatic content_ below), Facebook feed embed, and a visit section with address and map.
- **Visit page**: Plan your visit, service times (same list as home), location, parking, and embedded Google Map.
- **About page**: Five sub-tabs covering Ministries, History, Statement of Faith, Leadership (elders and deacons), and Squirrels Leap Farm. **Ministries** is the tab shown by default when the page opens.
- **Contact page**: Phone, email, office hours, address, and map.

Shared across the site:

- **Header**: Same blue bar with nav links (Home, Visit, About, Contact) and logo on every page. The logo links to Home. The bar stays visible when you scroll and shrinks slightly.
- **Footer**: Address, contact details, service times, and bank details on every page (edited in one place in `base.html`).
- **Service times**: One list in `templates/partials/service_times.html` is included on both the Home and Visit pages — edit that file once to update both.
- **Mobile and tablet**: The same site works on phones and tablets. Layout and spacing adjust at 920px (tablet) and 620px (phone) so nav, cards, map, and footer stack and stay readable. Desktop appearance is unchanged.

---

## Project structure (where to edit what)

| Path | Purpose |
|------|---------|
| **`app.py`** | Flask app used for local preview. Defines the URLs (`/`, `/visit`, `/about`, `/contact`) and fetches the latest YouTube video ID. Not used on the live site (which is static HTML) — only when you run the app locally to preview your changes. |
| **`build_static.py`** | Builds the published site. Renders every template into a plain HTML file inside `docs/`, copies `static/` across, and writes a `robots.txt` plus a `sitemap.xml` so search engines can index the site. The first few lines of the file contain a `SITE_URL` constant (and a list of pages) that you may need to edit — see _Before going live_ below. Normally run automatically by the GitHub Action; you only need to run it by hand if you want to preview the exact static HTML locally. |
| **`templates/base.html`** | Shared layout: `<head>`, footer (address, contact links, service times), security meta tags, and scripts that run on every page. Edit the footer here to change contact info site-wide. |
| **`templates/index.html`** | Home page: hero banner, “Who we are”, services + YouTube/Facebook embeds, visit block. Comments in the file describe each section. |
| **`templates/visit.html`** | Visit page: intro text, service times (from partial), location, parking, map. |
| **`templates/about.html`** | About page: tabbed content (Ministries, History, Statement of Faith, Leadership, Squirrels Leap Farm). **Ministries is the default tab** (the radio input with `checked`); to change which tab opens first, move `checked` to a different input. The Leadership tab lists elders (with photos) and deacons (bios only); add elder photos to `static/images/leadership/` and update the `src` in each elder card. |
| **`templates/contact.html`** | Contact page: contact details and address + map. |
| **`templates/partials/service_times.html`** | **Single source for service times and ministry list.** Used on Home and Visit; edit here to change both. |
| **`templates/partials/map_embed.html`** | **Single source for the Google Maps iframe.** Used anywhere the site embeds the church map (Home, Visit, Contact); edit here if the address or map embed ever changes. |
| **`templates/partials/social_links.html`** | **Single source for the church's social media links** (Facebook, YouTube). Used in the footer on every page and in the “Follow us” block on the Contact page. To add a new network or change a URL, edit only this file. |
| **`static/css/styles.css`** | All styling: colours, layout, buttons, cards, footer, responsive behaviour. Section comments explain what each block styles. |
| **`static/images/`** | Logo and other images. Logo file: `PBC logo transparent.png`. Banner images live in `static/images/banners/` (`banner1.jpg` … `banner7.jpg`). General site photos live in `static/images/site/`, and historical photos in `static/images/history/`. |
| **`docs/`** | Build output of `build_static.py` (a local snapshot you can preview). **Do not edit by hand** — it is regenerated by the build. On the live site, GitHub Actions rebuilds this folder and publishes it directly to GitHub Pages, so the committed copy here is only for local inspection. Includes a generated `robots.txt` (tells search engines what they may crawl) and `sitemap.xml` (lists the four public pages with a fresh "last modified" date on every build). |
| **`.github/workflows/rebuild.yml`** | GitHub Actions workflow that builds the site and **publishes it straight to GitHub Pages** — every 6 hours, whenever you push changes to `main`, and on demand from the Actions tab. It no longer commits anything back to the repo. Edit this file if you ever want to change how often the site refreshes. |

---

## Running the site locally

You can preview the site on your own laptop before publishing it.

> **Does GitHub Pages change how I test locally? No.** The live site is static HTML served by GitHub Pages, but you still preview your changes the same way as always: with `python app.py`. Flask only ever runs **on your own machine** as a convenient way to render the templates — it never runs on the live site. So `python app.py` remains the correct command for local testing.

1. **Optional but recommended**: Create and activate a virtual environment.
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Start the local preview**:
   ```powershell
   python app.py
   ```
4. Open **http://127.0.0.1:5000** in your browser.

### Auto-reload while editing

By default the local server runs in "production" mode — pages load, but you have to stop (`Ctrl+C`) and rerun the app to see template changes. If you want Flask to automatically reload pages as you edit templates, set the `FLASK_DEBUG` environment variable before starting:

```powershell
$env:FLASK_DEBUG = "1"; python app.py
```

(Use only on your own laptop, never on a public-facing server. See the comment block near the bottom of `app.py` for the security reason.)

---

## Editing content (no code experience needed)

- **Service times and ministry list**: Edit **`templates/partials/service_times.html`**. Changes appear on the Home and Visit pages.
- **Footer (address, phone, email, service times, bank details)**: Edit the **footer** section in **`templates/base.html`**.
- **Home page welcome text and “Who we are”**: Edit **`templates/index.html`** in the hero and intro sections (comments in the file point to them).
- **Visit, About, Contact**: Edit the corresponding file in **`templates/`** (e.g. `visit.html`, `about.html`). Each template has a short comment at the top describing the page.
- **Page description for Google search results**: Each page has a short "meta description" near the top of its template (look for the `{% block meta_description %}` block in `index.html`, `visit.html`, `about.html`, and `contact.html`). This is the grey snippet shown under the blue page title in Google search results, and the preview some chat apps show when someone shares the link. Keep each one to about 150 characters and mention "Plumstead" and "Cape Town" so the church is easy to find. The fallback used by any future page that forgets to set its own lives near the top of `base.html`.

All main sections in the templates and in `styles.css` are marked with comments so you can search for a section name (e.g. “Hero”, “Footer”, “Service times”) to find where to change things.

> **Important**: To publish your changes, commit and push them to GitHub — the rebuild happens automatically on the server (see _Publishing changes_ below). You don’t normally need to run `python build_static.py` yourself.

---

## Automatic content

- **Latest YouTube video**: When `build_static.py` runs, it reads the church YouTube channel’s RSS feed and embeds the most recent upload on the home page. A GitHub Action runs this script automatically **every 6 hours**, so the home page picks up new sermons on its own without anyone touching the code. (See _Publishing changes_ below for details.)
- **Facebook feed**: The home page embeds the church’s Facebook page timeline via Facebook’s Page Plugin (an iframe served by Facebook). This stays up to date with your latest posts automatically, because Facebook serves the embed live every time someone opens the page.

---

## Before going live (one-time URL update)

The published site includes a `robots.txt` and a `sitemap.xml` so Google and other search engines can index it. Both files need to know the **real** address where the site is published. Until that is known, the build uses a placeholder.

When the church website's real public URL is decided (e.g. `https://plumsteadbaptist.co.za/` if you set up the custom domain, or `https://<username>.github.io/Plumstead-Baptist/` for the default GitHub Pages URL), open **`build_static.py`** and change the `SITE_URL` line near the top:

```python
SITE_URL = "https://plumsteadbaptist.co.za/"  # <-- change this to the real URL
```

Keep the trailing slash. Then commit and push — the next rebuild will regenerate `robots.txt` and `sitemap.xml` with the correct URLs, and you can submit `sitemap.xml` to **Google Search Console** to ask Google to index the site sooner.

---

## Publishing changes (deploying to GitHub Pages)

The live site is hosted on **GitHub Pages** and published by a GitHub Action (see `.github/workflows/rebuild.yml`). The workflow builds the site from the templates and deploys it straight to Pages — you do **not** need to run `build_static.py` yourself, and nothing is committed back to the repository.

The full cycle from "I edited a template" to "the world can see it" is:

1. **Make your edits** in the relevant `templates/` file (or in `static/css/styles.css`).
2. **Preview locally** with `python app.py` and check the page in your browser at http://127.0.0.1:5000.
3. **Commit and push** to GitHub:
   ```powershell
   git add .
   git commit -m "Describe what you changed"
   git push
   ```
4. **GitHub does the rest**: the workflow runs `build_static.py` on its servers and publishes the result to GitHub Pages within a minute or two. Watch progress on the **Actions** tab.

### How the automatic publish works

The workflow runs in three situations:

- **Every 6 hours**, on a schedule. This is what keeps the latest YouTube sermon up to date on the home page — even if nobody has edited any templates.
- **Whenever you push** changes to `main`. Push-triggered runs publish straight away rather than waiting for the next 6-hour tick.
- **On demand**, from the **Actions** tab on github.com: open _Build and deploy site to GitHub Pages_ and click _Run workflow_.

### Manual rebuild / faithful local preview (optional)

If you ever want to build `docs/` yourself — for example to inspect the exact HTML that will go live — run:

```powershell
python build_static.py
```

To preview the **exact** static files GitHub Pages will serve (rather than the Flask preview), serve the `docs/` folder with Python's built-in web server:

```powershell
python -m http.server 8000 --directory docs
```

Then visit **http://127.0.0.1:8000**. This is the most faithful local test of the published site, because it uses the same relative links and pre-built HTML that go live. For day-to-day editing, though, `python app.py` is quicker.

### One-time GitHub Pages setup

On GitHub: **Settings → Pages → "Build and deployment" → Source = "GitHub Actions"**. (This is different from the older "Deploy from a branch" option — the workflow now does the publishing, so Pages must be told to use GitHub Actions as its source.)

The empty `.nojekyll` file created by `build_static.py` tells GitHub Pages to serve the files as-is without running Jekyll on them.

---

## Keeping the project maintainable

- **Comments**: All new or changed sections in templates, `app.py`, and `styles.css` should include clear comments describing what the section is for and what it does, so that someone with little coding experience can find and edit the right place.
- **README**: When you add new pages, features, or important files, update this README (structure table, _What this project does_, and any new editing or publishing steps) so the overview and instructions stay accurate.

---

## Dependencies

- **Flask** (see `requirements.txt`). Standard library only otherwise (`os`, `urllib`, `xml.etree` for the YouTube RSS, `pathlib`, `re`, `shutil` for the static build).
- **No production web server is needed.** Because the live site is static HTML on GitHub Pages, there is nothing to run with a WSGI server such as `gunicorn` or `waitress` — those belong to the old "host the Flask app" approach and are intentionally **not** in `requirements.txt`. The only things that ever execute Python are your laptop (local preview) and the GitHub Actions runner (the rebuild).
