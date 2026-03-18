"""
Plumstead Baptist Church website — Flask application.

This file defines all the URLs (routes) and what each page displays.
No database: content is in the HTML templates and this file.
"""

from flask import Flask, render_template
import urllib.request
import xml.etree.ElementTree as ET

app = Flask(__name__)

# YouTube channel RSS feed: used to fetch the latest video ID for the home page embed.
# Channel ID is for @plumsteadbaptist3246 (Plumstead Baptist Church).
YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCLUc8HRKJjxlij8bintem4g"


def get_latest_youtube_video_id() -> str | None:
    try:
        with urllib.request.urlopen(YOUTUBE_RSS_URL, timeout=5) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
        }
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        video_id_elem = entry.find("yt:videoId", ns)
        if video_id_elem is None:
            return None
        return video_id_elem.text
    except Exception:
        return None


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


@app.route("/sermons")
def sermons():
    """Sermons page: recent series and video/audio embeds."""
    return render_template("sermons.html", page_title="Sermons", active_page="sermons")


@app.route("/contact")
def contact():
    """Contact page: phone, email, address, map."""
    return render_template("contact.html", page_title="Contact", active_page="contact")


if __name__ == "__main__":
    # Run the development server. Use a production server (e.g. gunicorn) for deployment.
    app.run(debug=True)
