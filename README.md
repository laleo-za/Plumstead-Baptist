# Plumstead Baptist Church — Website

A simple, static-style church website built with **Python (Flask)**, **HTML templates**, and **CSS**. No database: all content is in the templates and one shared partial. The site is designed to be easy to edit for someone with little coding experience; key sections are clearly commented in the code.

---

## What this project does

- **Home page**: Rotating banner images, welcome message, “Who we are”, service times, latest YouTube sermon (auto-updated), Facebook feed embed, and a visit section with address and map.
- **Visit page**: Plan your visit, service times (same list as home), location, parking, and embedded Google Map.
- **About page**: Four sub-tabs covering church history, statement of faith, Squirrels Leap Farm, and ministries.
- **Contact page**: Phone, email, office hours, address, and map.

Shared across the site:

- **Header**: Same blue bar with nav links (Home, Visit, About, Contact) and logo on every page. The logo links to Home. The bar stays visible when you scroll and shrinks slightly.
- **Footer**: Address, contact details, service times, and bank details on every page (edited in one place in `base.html`).
- **Service times**: One list in `templates/partials/service_times.html` is included on both the Home and Visit pages—edit that file once to update both.
- **Mobile and tablet**: The same site works on phones and tablets. Layout and spacing adjust at 920px (tablet) and 620px (phone) so nav, cards, map, and footer stack and stay readable. Desktop appearance is unchanged.

---

## Project structure (where to edit what)

| Path | Purpose |
|------|--------|
| **`app.py`** | Flask app: defines URLs (/, /visit, /about, /contact) and fetches the latest YouTube video ID for the home page. Add or change routes here. |
| **`templates/base.html`** | Shared layout: `<head>`, footer (address, service times, bank details), and a script that makes the header shrink on scroll. Edit the footer here to change contact info site-wide. |
| **`templates/index.html`** | Home page: hero banner, “Who we are”, services + YouTube/Facebook embeds, visit block. Comments in the file describe each section. |
| **`templates/visit.html`** | Visit page: intro text, service times (from partial), location, parking, map. |
| **`templates/about.html`** | About page: church story and image placeholder. |
| **`templates/contact.html`** | Contact page: contact details and address + map. |
| **`templates/partials/service_times.html`** | **Single source for service times and ministry list.** Used on Home and Visit; edit here to change both. |
| **`static/css/styles.css`** | All styling: colours, layout, buttons, cards, footer, responsive behaviour. Section comments explain what each block styles. |
| **`static/images/`** | Logo and other images. Logo file: `PBC logo transparent.png`. Banner images: `banners/banner1.jpg` … `banners/banner4.jpg`. |

---

## Running the site locally

1. **Optional but recommended**: Create and activate a virtual environment.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the app**:
   ```bash
   python app.py
   ```
4. Open **http://127.0.0.1:5000** in your browser.

---

## Editing content (no code experience needed)

- **Service times and ministry list**: Edit **`templates/partials/service_times.html`**. Changes appear on the Home and Visit pages.
- **Footer (address, phone, email, service times, bank details)**: Edit the **footer** section in **`templates/base.html`**.
- **Home page welcome text and “Who we are”**: Edit **`templates/index.html`** in the hero and intro sections (comments in the file point to them).
- **Visit, About, Contact**: Edit the corresponding file in **`templates/`** (e.g. `visit.html`, `about.html`). Each template has a short comment at the top describing the page.

All main sections in the templates and in `styles.css` are marked with comments so you can search for a section name (e.g. “Hero”, “Footer”, “Service times”) to find where to change things.

---

## Automatic / dynamic content

- **Latest YouTube video**: The app reads the church YouTube channel’s RSS feed and embeds the most recent upload on the home page. No manual URL updates needed when you upload a new sermon.
- **Facebook feed**: The home page embeds the church’s Facebook page timeline via Facebook’s Page Plugin; it stays up to date with your latest posts.

---

## Deployment (e.g. PythonAnywhere)

- Use a production WSGI server (e.g. **gunicorn**) to run `app` when deploying.
- Point the WSGI config to the Flask `app` in `app.py`.
- Ensure **static files** are served from the `static/` directory (Flask does this by default at `/static/`).
- For a **custom domain**, configure it in your host’s dashboard and point it at your web app.

---

## Keeping the project maintainable

- **Comments**: All new or changed sections in templates, `app.py`, and `styles.css` should include clear comments describing what the section is for and what it does, so that someone with little coding experience can find and edit the right place.
- **README**: When you add new pages, features, or important files, update this README (structure table, “What this project does”, and any new editing or deployment steps) so the overview and instructions stay accurate.

---

## Dependencies

- **Flask** (see `requirements.txt`). Standard library only otherwise (e.g. `urllib`, `xml.etree` for the YouTube RSS).
