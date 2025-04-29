
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
        response = requests.get(AMIS_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all('table')
        for table in tables:
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            if 'Commodity' in headers and 'Market' in headers:
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        amis_data.append({
                            'commodity': cells[0].get_text(strip=True),
                            'unit': cells[1].get_text(strip=True),
                            'market': cells[2].get_text(strip=True),
                            'price_kes': cells[3].get_text(strip=True),
                            'scraped_at': datetime.datetime.utcnow().isoformat()
                        })

        if amis_data:
            with open('data/amis_market_updates.json', 'w') as f:
                json.dump(amis_data, f, indent=2)
            df = pd.DataFrame(amis_data)
            df.to_csv('data/amis_market_updates.csv', index=False)
            print(f"[AMIS SCRAPER] Scraped {len(amis_data)} entries from AMIS ✅")
        else:
            print("[AMIS SCRAPER] No valid market data found ❗")
    except Exception as e:
        print(f"[AMIS SCRAPER] Error scraping AMIS: {e}")
    if __name__ == "__main__":
    scrape_amis_market_prices()



