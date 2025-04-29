
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import json

SUPPLIER_SOURCES = [
    {'name': 'Naivas Kenya', 'url': 'https://www.naivas.co.ke/', 'product_selector': '.product-item-info', 'name_selector': '.product-item-name', 'price_selector': '.price'},
    {'name': 'Carrefour Kenya', 'url': 'https://www.carrefourkenya.com/', 'product_selector': '.plp-product', 'name_selector': '.plp-name', 'price_selector': '.plp-price'},
    {'name': 'Chandarana Foodplus', 'url': 'https://www.foodplus.co.ke/', 'product_selector': '.product-grid-item', 'name_selector': '.product-title', 'price_selector': '.price'},
    {'name': 'Quickmart Kenya', 'url': 'https://quickmart.co.ke/', 'product_selector': '.product-thumb', 'name_selector': '.caption h4', 'price_selector': '.price'}
]

def scrape_supplier_updates():
    all_products = []
    os.makedirs('data', exist_ok=True)

    for source in SUPPLIER_SOURCES:
        try:
            response = requests.get(source['url'], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.select(source['product_selector']):
                name_elem = item.select_one(source['name_selector'])
                price_elem = item.select_one(source['price_selector'])
                if name_elem and price_elem:
                    all_products.append({
                        'supplier': source['name'],
                        'name': name_elem.get_text(strip=True),
                        'price': price_elem.get_text(strip=True),
                        'scraped_at': datetime.datetime.utcnow().isoformat()
                    })
        except Exception:
            continue

    if all_products:
        with open('data/supplier_updates.json', 'w') as f:
            json.dump(all_products, f, indent=2)
        df = pd.DataFrame(all_products)
        df.to_csv('data/supplier_updates.csv', index=False)
        with open('data/supplier_updates_backup.json', 'w') as f:
            json.dump(all_products, f, indent=2)
        print("[DUKASMART SCRAPER] Live scrape successful ✅")
    else:
        if os.path.exists('data/supplier_updates_backup.json'):
            with open('data/supplier_updates_backup.json', 'r') as f:
                backup_data = json.load(f)
            with open('data/supplier_updates.json', 'w') as f:
                json.dump(backup_data, f, indent=2)

            df = pd.DataFrame(backup_data)
            df.to_csv('data/supplier_updates.csv', index=False)

            print("[DUKASMART SCRAPER] Live scrape failed. Using backup supplier data ✅")

def get_supplier_data():
    try:
        # Try to load live scraped data
        with open('data/supplier_updates.json', 'r') as f:
            data = json.load(f)
        if data:
            return data
    except Exception:
        pass

    # If live data fails or is empty, load from backup
    try:
        with open('data/supplier_updates_backup.json', 'r') as f:
            return json.load(f)
    except Exception:
        print("[DUKASMART SCRAPER] No data available.")
        return []

