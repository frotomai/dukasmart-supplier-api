
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import json

AMIS_URL = 'https://amis.co.ke/index.php/site/market'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def scrape_amis_market_prices():
    os.makedirs('data', exist_ok=True)
    amis_data = []

    try:
        print("[AMIS SCRAPER] Sending request to AMIS...")
        response = requests.get(AMIS_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        print("[AMIS SCRAPER] Response received.")

        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all('table')
        print(f"[AMIS SCRAPER] Found {len(tables)} tables.")

        for table in tables:
    headers = [header.get_text(strip=True) for header in table.find_all('th')]
    print("[AMIS DEBUG] HEADERS FOUND:", headers)  # 👈 see what headers are there

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        print("[AMIS DEBUG] ROW CELLS:", [cell.get_text(strip=True) for cell in cells])  # 👈 log each row

        if len(cells) >= 4:
            amis_data.append({
                'commodity': cells[0].get_text(strip=True),
                'unit': cells[1].get_text(strip=True),
                'market': cells[2].get_text(strip=True),
                'price_kes': cells[3].get_text(strip=True),
                'scraped_at': datetime.datetime.utcnow().isoformat()
            })


        if amis_data:
            print(f"[AMIS SCRAPER] Scraped {len(amis_data)} records ✅")
            with open('data/amis_market_updates.json', 'w') as f:
                json.dump(amis_data, f, indent=2)
        else:
            print("[AMIS SCRAPER] No data found ❗")

    except Exception as e:
        print(f"[AMIS SCRAPER] ERROR: {e}")




