"""Build a static export for GitHub Pages.

This renders the Flask templates into plain HTML files in `docs/`
and copies static assets so the site can be hosted by GitHub Pages.
It also writes a robots.txt and a sitemap.xml so Google and other
search engines know which pages exist and which they may crawl.
"""

from datetime import date
from pathlib import Path
import re
import shutil

from flask import render_template

from app import app, get_latest_youtube_video_id


OUTPUT_DIR = Path("docs")

# =============================================================================
# LIVE SITE URL
# This is the full address visitors type into their browser to reach the
# published church website. It is used to write absolute URLs into
# robots.txt and sitemap.xml so Google can crawl the right pages.
#
# *** UPDATE THIS WHEN THE SITE GOES LIVE. ***
#
# Examples:
#   - Custom domain:        "https://plumsteadbaptist.co.za/"
#   - Default GitHub Pages: "https://your-github-username.github.io/Plumstead-Baptist/"
#
# Must end with a trailing slash.
# =============================================================================
SITE_URL = "https://plumsteadbaptist.co.za/"

# Pages we publish. Used both for rendering the HTML and for listing
# their URLs in sitemap.xml. Keep this list in sync if you add a new page.
# Tuple: (output filename, sitemap path relative to SITE_URL, priority 0.0-1.0)
PAGES = [
    ("index.html", "", 1.0),
    ("visit.html", "visit.html", 0.8),
    ("about.html", "about.html", 0.8),
    ("contact.html", "contact.html", 0.7),
]


def rewrite_links_for_github_pages(html: str) -> str:
    """Convert Flask absolute links to local static-page links."""
    replacements = {
        'href="/static/': 'href="static/',
        'src="/static/': 'src="static/',
        'data-bg="/static/': 'data-bg="static/',
        "href='/static/": "href='static/",
        "src='/static/": "src='static/",
        "data-bg='/static/": "data-bg='static/",
        "url('/static/": "url('static/",
        'url("/static/': 'url("static/',
        "url(/static/": "url(static/",
        'href="/visit"': 'href="visit.html"',
        'href="/about"': 'href="about.html"',
        'href="/contact"': 'href="contact.html"',
        'href="/"': 'href="index.html"',
        "href='/visit'": "href='visit.html'",
        "href='/about'": "href='about.html'",
        "href='/contact'": "href='contact.html'",
        "href='/'": "href='index.html'",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    # Leave full external URLs untouched; tidy accidental double slashes in local refs.
    html = re.sub(r'(?<!https:)(?<!http:)//+', '/', html)
    return html


def write_robots_txt() -> None:
    """Write docs/robots.txt.

    Tells search engines (Google, Bing, DuckDuckGo, ...) what they may crawl.
    The church site is fully public, so we allow everything. We also point
    crawlers at sitemap.xml so they don't have to guess at the page list.
    """
    content = (
        "# robots.txt for Plumstead Baptist Church\n"
        "# Public church site: allow all search engines to index every page.\n"
        "# If you ever want to hide a page from search results, add a\n"
        '#   Disallow: /that-page.html\n'
        "# line below the User-agent rule.\n"
        "\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {SITE_URL}sitemap.xml\n"
    )
    (OUTPUT_DIR / "robots.txt").write_text(content, encoding="utf-8")


def write_sitemap_xml() -> None:
    """Write docs/sitemap.xml.

    A sitemap is a simple machine-readable list of every public URL on the
    site. Google reads it (via the Sitemap line in robots.txt) so it knows
    which pages to index and how recently each one changed.

    Lastmod is set to today's date on every build, so the sitemap stays
    current automatically.
    """
    today = date.today().isoformat()
    url_entries = []
    for _output_name, sitemap_path, priority in PAGES:
        loc = SITE_URL + sitemap_path
        url_entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <priority>{priority:.1f}</priority>\n"
            "  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )
    (OUTPUT_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")


def main() -> None:
    """Create a static site snapshot in docs/ for GitHub Pages."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copytree("static", OUTPUT_DIR / "static")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    latest_video_id = get_latest_youtube_video_id()
    page_contexts = {
        "index.html": {"page_title": "Home", "active_page": "home", "latest_video_id": latest_video_id},
        "visit.html": {"page_title": "Visit", "active_page": "visit"},
        "about.html": {"page_title": "About", "active_page": "about"},
        "contact.html": {"page_title": "Contact", "active_page": "contact"},
    }

    with app.app_context():
        with app.test_request_context("/"):
            for output_name, _sitemap_path, _priority in PAGES:
                context = page_contexts[output_name]
                rendered = render_template(output_name, **context)
                rendered = rewrite_links_for_github_pages(rendered)
                (OUTPUT_DIR / output_name).write_text(rendered, encoding="utf-8")

    write_robots_txt()
    write_sitemap_xml()


if __name__ == "__main__":
    main()
