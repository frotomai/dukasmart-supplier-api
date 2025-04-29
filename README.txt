
# DukaSmart Live Supplier Scraper Deployment Guide

1. Upload all files to a new GitHub repository.
2. Create a free Render.com account.
3. Create a new Web Service:
   - Connect to your GitHub repo.
   - Environment Variables:
     - KEY: API_KEY
     - VALUE: dukasmart1234
   - Start command: uvicorn main:app --host 0.0.0.0 --port 8000
4. Render will give you a public URL like:
   https://yourapp.onrender.com/supplier_updates.json?api_key=dukasmart1234
   https://yourapp.onrender.com/supplier_updates.csv?api_key=dukasmart1234
5. Use these URLs inside DukaSmart for real-time updates.
