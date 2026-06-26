"""Shared site URL and SEO settings for templates and the static build.

Edit SITE_URL when the church's public web address changes. The same value is
used for canonical links, Open Graph tags, JSON-LD structured data, robots.txt,
and sitemap.xml.
"""

# Public site address (must end with a trailing slash).
SITE_URL = "https://plumsteadbaptist.co.za/"

# Photo used when the site is shared on WhatsApp, Facebook, Slack, etc., and in
# Google's knowledge panel. Path is relative to static/. property.jpg shows the
# church building from outside. For best previews, replace with a 1200×630 image.
OG_IMAGE_PATH = "images/site/property.jpg"

CHURCH_NAME = "Plumstead Baptist Church"

# Church contact and location (used in JSON-LD for Google search results).
CHURCH_PHONE = "+27-76-589-0261"
CHURCH_EMAIL = "office@plumsteadbaptist.co.za"
CHURCH_STREET = "20 Toulon Avenue"
CHURCH_LOCALITY = "Plumstead"
CHURCH_REGION = "Western Cape"
CHURCH_POSTAL_CODE = "7945"
CHURCH_COUNTRY = "ZA"

FACEBOOK_URL = "https://www.facebook.com/people/Plumstead-Baptist-Church/100064453489540/"
YOUTUBE_URL = "https://www.youtube.com/@plumsteadbaptist3246"

# Per-page canonical path (after SITE_URL) and plain-text description for
# <meta name="description">, Open Graph, and Twitter cards. Keep in sync with
# each page's {% block meta_description %} in templates/.
PAGE_SEO: dict[str, tuple[str, str]] = {
    "home": (
        "",
        "Plumstead Baptist Church is a Bible-believing Evangelical church in Plumstead, Cape Town. "
        "Join us Sundays at 10:00 for worship, teaching and community.",
    ),
    "visit": (
        "visit.html",
        "Planning your first visit to Plumstead Baptist Church? Find our service times, address, "
        "parking, and what to expect at 20 Toulon Avenue, Plumstead.",
    ),
    "about": (
        "about.html",
        "Learn about Plumstead Baptist Church in Cape Town — our ministries, history since the "
        "early 1900s, statement of faith, and Squirrels Leap Farm.",
    ),
    "contact": (
        "contact.html",
        "Contact Plumstead Baptist Church in Plumstead, Cape Town. Office hours, phone, email, "
        "address and map for general enquiries and hall hire.",
    ),
}


def absolute_static_url(relative_path: str) -> str:
    """Return a full URL for a file under static/ (e.g. for og:image)."""
    return f"{SITE_URL}static/{relative_path.lstrip('/')}"


def seo_page_context(active_page: str) -> dict[str, str]:
    """Canonical URL and description for one public page."""
    if active_page not in PAGE_SEO:
        raise KeyError(f"Unknown page key for SEO: {active_page!r}")
    path, description = PAGE_SEO[active_page]
    return {
        "canonical_url": f"{SITE_URL}{path}",
        "seo_description": description,
        "og_image_url": absolute_static_url(OG_IMAGE_PATH),
    }


def church_json_ld() -> dict:
    """Schema.org Church data for Google (service times, address, phone, social links)."""
    return {
        "@context": "https://schema.org",
        "@type": "Church",
        "name": CHURCH_NAME,
        "url": SITE_URL,
        "image": absolute_static_url(OG_IMAGE_PATH),
        "telephone": CHURCH_PHONE,
        "email": CHURCH_EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CHURCH_STREET,
            "addressLocality": CHURCH_LOCALITY,
            "addressRegion": CHURCH_REGION,
            "postalCode": CHURCH_POSTAL_CODE,
            "addressCountry": CHURCH_COUNTRY,
        },
        # Sunday morning worship only (main service at 10:00).
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "https://schema.org/Sunday",
                "opens": "10:00",
                "closes": "12:00",
            }
        ],
        "sameAs": [FACEBOOK_URL, YOUTUBE_URL],
    }
