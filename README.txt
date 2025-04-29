
# DukaSmart Supplier Scraper with Backup Fallback

Features:
- Scrapes Naivas, Carrefour, Quickmart, Chandarana
- Backs up last good scrape
- Falls back to backup if live scraping fails
- Secured with API Key 'dukasmart1234'

# Deployment:
- Upload to GitHub
- Deploy to Render.com
- Start Command: uvicorn main:app --host 0.0.0.0 --port 8000
