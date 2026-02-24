import requests
import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET

GOODREADS_USER_ID = "148356708"
STATS_FILE = "stats.json"


def get_strava_km():
    """Fetch total km run (all time) from Strava API."""
    client_id = os.environ.get("STRAVA_CLIENT_ID")
    client_secret = os.environ.get("STRAVA_CLIENT_SECRET")
    refresh_token = os.environ.get("STRAVA_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("  ⚠ Strava credentials not set — skipping")
        return None

    # Exchange refresh token for a short-lived access token
    token_resp = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=15,
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]

    # Fetch athlete stats
    stats_resp = requests.get(
        "https://www.strava.com/api/v3/athlete/stats",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    stats_resp.raise_for_status()

    distance_m = stats_resp.json()["all_run_totals"]["distance"]
    km = round(distance_m / 1000, 1)
    print(f"  ✓ Strava: {km:,.1f} km run (all time)")
    return km


def get_goodreads_books_this_year():
    """Count books marked as read this calendar year from Goodreads RSS."""
    current_year = datetime.now().year
    url = (
        f"https://www.goodreads.com/review/list_rss/{GOODREADS_USER_ID}"
        "?shelf=read&per_page=200&sort=date_read"
    )

    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    count = 0

    for item in root.findall(".//item"):
        read_at_el = item.find("user_read_at")
        if read_at_el is None or not read_at_el.text:
            continue
        text = read_at_el.text.strip()
        # Format: "Thu Feb 12 00:00:00 -0800 2026"
        try:
            read_date = datetime.strptime(text, "%a %b %d %H:%M:%S %z %Y")
            if read_date.year == current_year:
                count += 1
        except ValueError:
            # Fall back to checking if the year string is present
            if str(current_year) in text:
                count += 1

    print(f"  ✓ Goodreads: {count} books read in {current_year}")
    return count


def load_existing_stats():
    """Return existing stats.json values as fallbacks."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            return json.load(f)
    return {"km_run": 15096.7, "books_read_this_year": 25}


if __name__ == "__main__":
    print("=" * 50)
    print("Stats updater")
    print("=" * 50)

    existing = load_existing_stats()

    print("\nFetching Strava data...")
    try:
        km = get_strava_km()
    except Exception as e:
        print(f"  ⚠ Strava error: {e}")
        km = None

    print("\nFetching Goodreads data...")
    try:
        books = get_goodreads_books_this_year()
    except Exception as e:
        print(f"  ⚠ Goodreads error: {e}")
        books = None

    stats = {
        "km_run": km if km is not None else existing.get("km_run", 15096.7),
        "books_read_this_year": (
            books if books is not None else existing.get("books_read_this_year", 25)
        ),
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
    }

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\n✓ Saved to {STATS_FILE}:")
    print(json.dumps(stats, indent=2))
