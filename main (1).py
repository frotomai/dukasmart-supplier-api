
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io
import os
import json
from scraper import scrape_supplier_updates
from amis_scraper import scrape_amis_market_prices

app = FastAPI()

API_KEY = "dukasmart1234"

def get_supplier_data():
    try:
        if os.path.exists('data/supplier_updates.json'):
            with open('data/supplier_updates.json', 'r') as f:
                return json.load(f)
        else:
            with open('data/supplier_updates_backup.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading supplier data: {e}")
        return []

def get_amis_data():
    try:
        if os.path.exists('data/amis_market_updates.json'):
            with open('data/amis_market_updates.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading AMIS data: {e}")
    return []

@app.get("/")
async def root():
    return {"message": "DukaSmart Supplier API is running!"}

@app.get("/supplier_updates.json")
async def supplier_updates_json(api_key: str):
    if api_key != API_KEY:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    data = get_supplier_data()
    return JSONResponse(content=data)

@app.get("/supplier_updates.csv")
async def supplier_updates_csv(api_key: str):
    if api_key != API_KEY:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    data = get_supplier_data()
    if not data:
        return JSONResponse(content={"error": "No supplier data available"}, status_code=404)
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=supplier_updates.csv"
    return response

@app.get("/amis_market_updates.json")
async def amis_market_updates_json(api_key: str):
    if api_key != API_KEY:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    data = get_amis_data()
    if not data:
        return JSONResponse(content={"error": "No AMIS market data available"}, status_code=404)
    return JSONResponse(content=data)

@app.get("/amis_market_updates.csv")
async def amis_market_updates_csv(api_key: str):
    if api_key != API_KEY:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    data = get_amis_data()
    if not data:
        return JSONResponse(content={"error": "No AMIS market data available"}, status_code=404)
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=amis_market_updates.csv"
    return response

@app.on_event("startup")
async def startup_event():
    print("Starting automatic scrapers...")
    scrape_supplier_updates()
    scrape_amis_market_prices()
