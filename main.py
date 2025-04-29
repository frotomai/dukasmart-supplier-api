
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import os
from scraper import get_supplier_data, scrape_supplier_updates
import pandas as pd
import io

app = FastAPI()

API_KEY = os.getenv("API_KEY", "dukasmart1234")

# 🚀 First Load: Always scrape or fallback immediately at server startup
scrape_supplier_updates()

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path.startswith("/supplier_updates"):
        api_key = request.query_params.get("api_key")
        if api_key != API_KEY:
            raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    response = await call_next(request)
    return response

@app.get("/supplier_updates.json")
async def supplier_updates_json():
    data = get_supplier_data()
    return JSONResponse(content=data)

@app.get("/supplier_updates.csv")
async def supplier_updates_csv():
    data = get_supplier_data()
    if not data:
        return JSONResponse(content={"error": "No supplier data available"}, status_code=404)

    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=supplier_updates.csv"
    return response
