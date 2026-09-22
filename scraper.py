import os
import re
import json
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Configuration & Setup
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OUTPUT_FILE = os.path.join("data", "minutes.json")

# Community Board Targets
BOARDS = [
    {"board": "CB4", "url": "https://cbmanhattan.cityofnewyork.us/cb4/archive/full-board-minutes/"},
    {"board": "CB5", "url": "https://cbmanhattan.cityofnewyork.us/cb5/archive/minutes/"},
    {"board": "CB6", "url": "https://cbmanhattan.cityofnewyork.us/cb6/archive/minutes/"},
    {"board": "CB7", "url": "https://cbmanhattan.cityofnewyork.us/cb7/archive/minutes/"},
]


def fetch_pdf_links(board_info):
    """Scrapes PDF links from the board's web page."""
    pdf_items = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(board_info["url"], headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"[{board_info['board']}] Failed to fetch page. Status: {response.status_code}")
            return pdf_items

        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            text = a_tag.get_text(strip=True)
            
            # Match links pointing to PDF files
            if href.lower().endswith(".pdf") or "pdf" in href.lower():
                full_url = href if href.startswith("http") else f"https://cbmanhattan.cityofnewyork.us{href}"
                
                # Extract year/date from URL or link text if possible
                date_match = re.search(r"20\d{2}[-_/]\d{2}", href) or re.search(r"20\d{2}", href)
                date_str = date_match.group(0) if date_match else "2026-09"

                pdf_items.append({
                    "board": board_info["board"],
                    "title": f"{board_info['board']} Meeting Minutes - {text if text else 'Minutes'}",
                    "pdf_url": full_url,
                    "date": date_str,
                    "raw_text": text
                })
    except Exception as e:
        print(f"[{board_info['board']}] Scraping error: {e}")

    return pdf_items


def analyze_with_gemini(client, item):
    """Extracts structured intelligence using Gemini 2.5 Flash."""
    prompt = f"""
Analyze the following Community Board minute entry:
Title: {item['title']}
Context/Link Text: {item['raw_text']}
URL: {item['pdf_url']}

Extract structured details in JSON format matching this schema:
{{
  "summary": "Brief 1-2 sentence summary of key topics, resolutions, or applications discussed.",
  "committee": "Likely committee name (e.g. Land Use & Zoning, Transportation, Business & Licensing)",
  "high_priority": true or false (Set to true if it covers ULURP, BSA variances, rezoning, FAR changes, or SLA liquor licenses),
  "high_priority_reason": "Explanation if high_priority is true, otherwise empty string",
  "locations": [
    {{
      "address": "Full address in NYC (e.g. 501 W 34th St, New York, NY)",
      "description": "Short description of proposal at this address",
      "type": "Type of request (e.g., Zoning Variance, Liquor License, BSA Variance, Public Space)",
      "lat": latitude float or null,
      "lng": longitude float or null
    }}
  ]
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini processing error for {item['title']}: {e}")
        return {
            "summary": "Minutes cataloged from recent Community Board archive publication.",
            "committee": "General Board",
            "high_priority": False,
            "high_priority_reason": "",
            "locations": []
        }


def geocode_address(address):
    """Fallback geocoder using OpenStreetMap Nominatim API if coordinates are missing."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={requests.utils.quote(address)}"
        headers = {"User-Agent": "Midtown-CB-Intelligence/1.0"}
        res = requests.get(url, headers=headers, timeout=5).json()
        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])
    except Exception:
        pass
    return None, None


def main():
    print("Starting Community Board Scraper Pipeline...")
    
    # Initialize Gemini client
    client = None
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        print("Warning: GEMINI_API_KEY environment variable not found. AI extraction will be skipped.")

    all_records = []
    
    # 1. Scrape PDF links
    for b in BOARDS:
        print(f"Scraping {b['board']}...")
        items = fetch_pdf_links(b)
        # Limit processing to recent 3 items per board for efficiency
        all_records.extend(items[:3])

    structured_dataset = []

    # 2. Process items through Gemini & Geocoding
    for idx, item in enumerate(all_records):
        record_id = f"{item['board'].lower()}-{idx + 1}"
        print(f"Processing item [{idx + 1}/{len(all_records)}]: {item['title']}")
        
        if client:
            ai_data = analyze_with_gemini(client, item)
        else:
            ai_data = {
                "summary": "Document retrieved from Community Board archive.",
                "committee": "General",
                "high_priority": False,
                "high_priority_reason": "",
                "locations": []
            }

        # Geocode locations if lat/lng are missing
        for loc in ai_data.get("locations", []):
            if not loc.get("lat") or not loc.get("lng"):
                lat, lng = geocode_address(loc.get("address", ""))
                loc["lat"] = lat
                loc["lng"] = lng

        record = {
            "id": record_id,
            "board": item["board"],
            "date": item["date"],
            "title": item["title"],
            "summary": ai_data.get("summary", ""),
            "pdf_url": item["pdf_url"],
            "committee": ai_data.get("committee", "General"),
            "high_priority": ai_data.get("high_priority", False),
            "high_priority_reason": ai_data.get("high_priority_reason", ""),
            "locations": ai_data.get("locations", [])
        }
        structured_dataset.append(record)

    # 3. Create 'data' directory if it doesn't exist and save JSON
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_dataset, f, indent=2)

    print(f"Successfully saved {len(structured_dataset)} records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
