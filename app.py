"""
Plumstead Baptist Church website — Flask application.

This file defines all the URLs (routes) and what each page displays.
No database: content is in the HTML templates and this file.
"""

import os
import time
import urllib.request
import xml.etree.ElementTree as ET

from flask import Flask, render_template

app = Flask(__name__)

# YouTube channel RSS feed: used to fetch the latest video ID for the home page embed.
# Channel ID is for @plumsteadbaptist3246 (Plumstead Baptist Church).
YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCLUc8HRKJjxlij8bintem4g"

# In-memory cache for the latest YouTube video ID.
#
# Why: without this, every single home-page load during local preview
# (python app.py) would re-fetch the YouTube RSS feed, which can take
# several seconds. With the cache, we only fetch once per 10 minutes
# within the same running process, which makes refreshing the home page
# locally feel instant.
#
# This is purely a local-preview convenience. The published GitHub Pages
# site is static HTML, so visitors never trigger this code; the function
# only runs at build time (once per `build_static.py` invocation) and
# during local preview. Each fresh process starts with an empty cache.
_YOUTUBE_CACHE: dict[str, tuple[float, "str | None"]] = {}
_YOUTUBE_CACHE_SECONDS = 600  # 10 minutes


def get_latest_youtube_video_id() -> str | None:
    """Return the most recent video ID from the church's YouTube channel.

    Returns ``None`` if the RSS feed is unreachable, malformed, or empty;
    callers (templates and the static-site builder) treat ``None`` as
    "show the placeholder card instead of an iframe". A failure is also
    cached briefly so we don't hammer YouTube during an outage.
    """
    now = time.monotonic()
    cached = _YOUTUBE_CACHE.get("latest")
    if cached is not None and (now - cached[0]) < _YOUTUBE_CACHE_SECONDS:
        return cached[1]

    video_id: str | None = None
    try:
        with urllib.request.urlopen(YOUTUBE_RSS_URL, timeout=5) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        entry = root.find("atom:entry", ns)
        if entry is not None:
            video_id_elem = entry.find("yt:videoId", ns)
            if video_id_elem is not None:
                video_id = video_id_elem.text
    except Exception:
        video_id = None

    _YOUTUBE_CACHE["latest"] = (now, video_id)
    return video_id


# -----------------------------------------------------------------------------
# ROUTES (URLs) — each function below maps a URL to a template and optional data.
# -----------------------------------------------------------------------------

@app.route("/")
def home():
    """Home page: hero, who we are, services, YouTube/Facebook embeds, visit section."""
    latest_video_id = get_latest_youtube_video_id()
    return render_template(
        "index.html",
        page_title="Home",
        active_page="home",
        latest_video_id=latest_video_id,
    )


@app.route("/visit")
def visit():
    """Visit page: plan your visit, service times, location, map."""
    return render_template("visit.html", page_title="Visit", active_page="visit")


@app.route("/about")
def about():
    """About page: church story, beliefs, what to expect."""
    return render_template("about.html", page_title="About", active_page="about")


@app.route("/contact")
def contact():
    """Contact page: phone, email, address, map."""
    return render_template("contact.html", page_title="Contact", active_page="contact")


if __name__ == "__main__":
    # Development server (only used when previewing the site locally).
    #
    # Why debug is OFF by default:
    #   Flask's "debug" mode shows a helpful error page in the browser and
    #   auto-reloads templates while you edit them. That error page also
    #   includes an INTERACTIVE PYTHON CONSOLE. If this app were ever exposed
    #   on the public internet with debug enabled, a visitor could run any
    #   Python code on the machine — a serious security hole. Defaulting to
    #   off means a stray "python app.py" on a server can never expose that
    #   console.
    #
    # This site is published as static HTML to GitHub Pages via
    # build_static.py, so app.py is only ever used locally for preview and
    # by the build script (which imports the app without running this block).
    #
    # If you want auto-reload while editing templates locally, set the
    # FLASK_DEBUG environment variable to 1 before running the app:
    #   PowerShell:  $env:FLASK_DEBUG = "1"; python app.py
    #   CMD:         set FLASK_DEBUG=1 && python app.py
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
