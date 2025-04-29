
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from scraper import get_supplier_data
from amis_scraper import scrape_amis_market_prices
import pandas as pd
import io
import json
import os

app = FastAPI()
API_KEY = "dukasmart1234"
templates = Jinja2Templates(directory="templates")

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

@app.get("/dashboard", response_class=HTMLResponse)
async def view_dashboard(request: Request, api_key: str):
    if api_key != API_KEY:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    data = get_supplier_data()
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": data})

@app.get("/amis_market_updates.json")
async def amis_market_updates(api_key: str):
    if api_key != API_KEY:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)

    scrape_amis_market_prices()

    try:
        with open("data/amis_market_updates.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    return JSONResponse(content=data)
