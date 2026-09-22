"""
Midtown CB Minutes Scraper

For each board: find minutes PDFs, keep the most recent ones, download each PDF,
extract its text, and ask Gemini to pull out only what appears in that text.
Every extracted item carries a verbatim excerpt, and the script checks that the
excerpt actually appears in the PDF. Priority flags are set by fixed keyword
rules in this file, not by the model.

Results accumulate in data/minutes.json. Documents already analyzed are not
re-sent to Gemini on later runs.
"""

import hashlib
import io
import json
import os
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from pypdf import PdfReader

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OUTPUT_FILE = os.path.join("data", "minutes.json")
MODEL = "gemini-2.5-flash"
PER_BOARD = 3            # most recent documents to process per board, per run
MAX_CHARS = 150_000      # text sent to Gemini per document
MIN_TEXT_CHARS = 500     # less text than this = scanned PDF, can't be read
HEADERS = {"User-Agent": "Mozilla/5.0 (Midtown-CB-Intelligence research tool)"}

# Minutes archive pages. CB4 is confirmed working.
# CB5, CB6 and CB7 are no longer at the old city URLs. Paste each board's
# minutes page URL here; a board set to None is skipped with a log message.
BOARDS = [
    {"board": "CB4", "url": "https://cbmanhattan.cityofnewyork.us/cb4/archive/full-board-minutes/"},
    {"board": "CB5", "url": None},  # CB5 site: cb5.org
    {"board": "CB6", "url": None},  # CB6 site: cbsix.org
    {"board": "CB7", "url": None},
]

# Priority rules. These drive the Alerts & Rules tab.
PRIORITY_RULES = {
    "ULURP / Land Use": ["ulurp", "uniform land use", "rezoning", "zoning map", "zoning text", "floor area ratio"],
    "BSA Variance": ["board of standards and appeals", "bsa", "variance", "special permit"],
    "SLA Liquor License": ["state liquor authority", "sla", "liquor license", "on-premises", "on premises", "500-foot", "500 foot", "4 am", "4am"],
}
PRIORITY_CATEGORIES = {"ULURP / Land Use", "BSA Variance", "SLA Liquor License"}

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}
MONTHS.update({m[:3]: i for m, i in list(MONTHS.items())})
MONTHS["sept"] = 9


# ---------------------------------------------------------------------------
# Finding documents
# ---------------------------------------------------------------------------
def parse_meeting_date(*texts):
    """Find a meeting date in link text or filename. Returns 'YYYY-MM' / 'YYYY-MM-DD' or None."""
    blob = " ".join(t for t in texts if t)
    blob = re.sub(r"[_\-]+", " ", blob.lower())

    # "january 15 2026", "jan 2026", "01 january 2026"
    m = re.search(r"\b(" + "|".join(sorted(MONTHS, key=len, reverse=True)) +
                  r")\.?\s*(\d{1,2})?(?:st|nd|rd|th)?,?\s*(20\d{2})\b", blob)
    if m:
        month, day, year = MONTHS[m.group(1)], m.group(2), m.group(3)
        if day and 1 <= int(day) <= 31:
            return f"{year}-{month:02d}-{int(day):02d}"
        return f"{year}-{month:02d}"

    # "2026 01 15"
    m = re.search(r"\b(20\d{2})\s(\d{1,2})\s(\d{1,2})\b", blob)
    if m and 1 <= int(m.group(2)) <= 12:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # "minutes 04 11" (month, two-digit year)
    m = re.search(r"minutes\s(\d{1,2})\s(\d{2})\b", blob)
    if m and 1 <= int(m.group(1)) <= 12:
        return f"20{m.group(2)}-{int(m.group(1)):02d}"
    return None


def fetch_pdf_links(board):
    """Collect PDF links from a board's archive page, newest first."""
    try:
        res = requests.get(board["url"], headers=HEADERS, timeout=20)
    except requests.RequestException as e:
        print(f"[{board['board']}] Could not reach {board['url']}: {e}")
        return []
    if res.status_code != 200:
        print(f"[{board['board']}] {board['url']} returned HTTP {res.status_code}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    seen, links = set(), []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.lower().split("?")[0].endswith(".pdf"):
            continue
        url = urljoin(board["url"], href)
        if url in seen:
            continue
        seen.add(url)
        text = a.get_text(" ", strip=True)
        filename = url.rsplit("/", 1)[-1]
        links.append({
            "board": board["board"],
            "pdf_url": url,
            "link_text": text,
            "date": parse_meeting_date(text, filename),
        })

    print(f"[{board['board']}] Found {len(links)} PDF links")
    # Dated documents newest first; undated ones last.
    links.sort(key=lambda x: x["date"] or "0000", reverse=True)
    return links


# ---------------------------------------------------------------------------
# Reading documents
# ---------------------------------------------------------------------------
def extract_pdf_text(url):
    res = requests.get(url, headers=HEADERS, timeout=60)
    res.raise_for_status()
    reader = PdfReader(io.BytesIO(res.content))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def normalize(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", (s or "").lower())).strip()


EXTRACTION_PROMPT = """You are extracting information from official Manhattan Community Board minutes for a newsroom.

Rules:
- Use ONLY the text between the DOCUMENT markers. Do not use outside knowledge.
- If something is not stated in the text, use null or leave it out. Never guess.
- Copy addresses exactly as written in the text.
- "evidence" must be copied word for word from the text (under 30 words).

Return JSON only, in this shape:
{
  "meeting_date": "YYYY-MM-DD if the text states the meeting date, else null",
  "meeting_type": "Full Board, or the committee name as stated",
  "summary": "2-3 sentences on the most significant actions the board took",
  "items": [
    {
      "topic": "short description of the matter",
      "category": "one of: ULURP / Land Use, BSA Variance, SLA Liquor License, Cannabis License, Landmarks, Transportation, Budget, Other",
      "address": "street address exactly as written, or null",
      "action": "what the board did, as stated (approved, denied, approved with stipulations, laid over...)",
      "vote": "vote tally as stated, or null",
      "evidence": "verbatim excerpt supporting this item"
    }
  ]
}

-----BEGIN DOCUMENT-----
{text}
-----END DOCUMENT-----
"""


def analyze_with_gemini(client, text):
    prompt = EXTRACTION_PROMPT.replace("{text}", text[:MAX_CHARS])
    last_error = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0,
                ),
            )
            raw = re.sub(r"^```(?:json)?|```$", "", (response.text or "").strip()).strip()
            return json.loads(raw)
        except Exception as e:
            last_error = e
            wait = 20 * (attempt + 1)
            print(f"   Gemini error (attempt {attempt + 1}/3): {e}")
            if attempt < 2:
                time.sleep(wait)
    raise RuntimeError(f"Gemini failed after 3 attempts: {last_error}")


def flag_priority(items, full_text):
    """Apply fixed keyword rules. Returns (high_priority, reason)."""
    reasons = []
    for item in items:
        if item.get("category") in PRIORITY_CATEGORIES:
            reasons.append(f"{item['category']}: {item.get('topic', '')}".strip(": "))
    if not reasons:
        lowered = full_text.lower()
        for rule, terms in PRIORITY_RULES.items():
            hit = next((t.strip() for t in terms
                        if re.search(r"\b" + re.escape(t.strip()) + r"\b", lowered)), None)
            if hit:
                reasons.append(f"{rule} (keyword: '{hit}')")
    return bool(reasons), "; ".join(dict.fromkeys(reasons))[:600]


# ---------------------------------------------------------------------------
# Geocoding
# ---------------------------------------------------------------------------
_geo_cache = {}
MANHATTAN_BOUNDS = (40.68, 40.89, -74.03, -73.90)  # lat min, lat max, lng min, lng max


def geocode(address):
    if not address:
        return None, None
    if address in _geo_cache:
        return _geo_cache[address]
    query = address if "new york" in address.lower() else f"{address}, Manhattan, New York, NY"
    lat = lng = None
    try:
        time.sleep(1.1)  # Nominatim usage policy: max 1 request per second
        res = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"format": "json", "limit": 1, "q": query},
            headers={"User-Agent": "Midtown-CB-Intelligence/2.0"},
            timeout=15,
        ).json()
        if res:
            la, ln = float(res[0]["lat"]), float(res[0]["lon"])
            b = MANHATTAN_BOUNDS
            if b[0] <= la <= b[1] and b[2] <= ln <= b[3]:
                lat, lng = la, ln
            else:
                print(f"   Geocode for '{address}' landed outside Manhattan; discarded")
    except Exception as e:
        print(f"   Geocode failed for '{address}': {e}")
    _geo_cache[address] = (lat, lng)
    return lat, lng


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def load_existing():
    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            data = json.load(f)
        # Records without a status came from the old scraper and were never read; drop them.
        return {r["pdf_url"]: r for r in data
                if isinstance(r, dict) and r.get("pdf_url") and r.get("status")}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def build_record(link, client):
    record = {
        "id": f"{link['board'].lower()}-{hashlib.md5(link['pdf_url'].encode()).hexdigest()[:8]}",
        "board": link["board"],
        "date": link["date"] or "Undated",
        "title": f"{link['board']} — {link['link_text'] or link['pdf_url'].rsplit('/', 1)[-1]}",
        "pdf_url": link["pdf_url"],
        "status": "not_analyzed",
        "summary": "",
        "committee": "",
        "high_priority": False,
        "high_priority_reason": "",
        "items": [],
        "locations": [],
    }

    try:
        text = extract_pdf_text(link["pdf_url"])
    except Exception as e:
        print(f"   Could not download or open PDF: {e}")
        record["status"] = "download_error"
        return record

    if len(text.strip()) < MIN_TEXT_CHARS:
        record["status"] = "no_text"
        return record

    if not client:
        return record

    try:
        ai = analyze_with_gemini(client, text)
    except Exception as e:
        record["status"] = "ai_error"
        print(f"   {e}")
        return record

    norm_text = normalize(text)
    items = []
    for item in ai.get("items") or []:
        if not isinstance(item, dict):
            continue
        item["verified"] = bool(item.get("evidence")) and normalize(item["evidence"]) in norm_text
        items.append(item)

    if ai.get("meeting_date"):
        record["date"] = ai["meeting_date"]
    record["status"] = "analyzed"
    record["summary"] = ai.get("summary") or ""
    record["committee"] = ai.get("meeting_type") or "Full Board"
    record["items"] = items
    record["high_priority"], record["high_priority_reason"] = flag_priority(items, text)

    for item in items:
        if item.get("address"):
            lat, lng = geocode(item["address"])
            record["locations"].append({
                "address": item["address"],
                "description": item.get("topic", ""),
                "type": item.get("category", ""),
                "action": item.get("action"),
                "verified": item["verified"],
                "lat": lat,
                "lng": lng,
            })

    unverified = sum(1 for i in items if not i["verified"])
    print(f"   Analyzed: {len(items)} items, {len(record['locations'])} addresses, "
          f"{unverified} excerpts not found verbatim in the PDF")
    return record


def main():
    print("Starting Community Board minutes pipeline")
    client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
    if not client:
        print("WARNING: GEMINI_API_KEY is not set. Documents will be listed but not analyzed.")

    existing = load_existing()
    for rec in existing.values():  # reuse earlier geocodes
        for loc in rec.get("locations", []):
            if loc.get("lat") and loc.get("lng"):
                _geo_cache[loc["address"]] = (loc["lat"], loc["lng"])

    for board in BOARDS:
        if not board["url"]:
            print(f"[{board['board']}] Skipped: no minutes page URL set in BOARDS")
            continue
        for link in fetch_pdf_links(board)[:PER_BOARD]:
            prior = existing.get(link["pdf_url"])
            if prior and prior.get("status") in ("analyzed", "no_text"):
                print(f"[{board['board']}] Already processed: {link['pdf_url']}")
                continue
            print(f"[{board['board']}] Processing {link['date'] or 'undated'}: {link['pdf_url']}")
            existing[link["pdf_url"]] = build_record(link, client)

    records = sorted(existing.values(), key=lambda r: r.get("date") or "", reverse=True)
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    counts = {}
    for r in records:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"Saved {len(records)} records to {OUTPUT_FILE}: {counts}")


if __name__ == "__main__":
    main()
