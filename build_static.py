"""Build a static export for GitHub Pages.

This renders the Flask templates into plain HTML files in `docs/`
and copies static assets so the site can be hosted by GitHub Pages.
"""

from pathlib import Path
import re
import shutil

from flask import render_template

from app import app, get_latest_youtube_video_id


OUTPUT_DIR = Path("docs")


def rewrite_links_for_github_pages(html: str) -> str:
    """Convert Flask absolute links to local static-page links."""
    replacements = {
        'href="/static/': 'href="static/',
        'src="/static/': 'src="static/',
        "href='/static/": "href='static/",
        "src='/static/": "src='static/",
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


def main() -> None:
    """Create a static site snapshot in docs/ for GitHub Pages."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copytree("static", OUTPUT_DIR / "static")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    latest_video_id = get_latest_youtube_video_id()
    pages = {
        "index.html": ("index.html", {"page_title": "Home", "active_page": "home", "latest_video_id": latest_video_id}),
        "visit.html": ("visit.html", {"page_title": "Visit", "active_page": "visit"}),
        "about.html": ("about.html", {"page_title": "About", "active_page": "about"}),
        "contact.html": ("contact.html", {"page_title": "Contact", "active_page": "contact"}),
    }

    with app.app_context():
        with app.test_request_context("/"):
            for output_name, (template_name, context) in pages.items():
                rendered = render_template(template_name, **context)
                rendered = rewrite_links_for_github_pages(rendered)
                (OUTPUT_DIR / output_name).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
