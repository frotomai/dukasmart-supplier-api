
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from scraper import scrape_supplier_updates, get_supplier_data
import os
import io
import pandas as pd
import uvicorn
import threading
import schedule
import time

app = FastAPI()
API_KEY = os.getenv('API_KEY', 'dukasmart1234')

def scheduled_scraping():
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.on_event("startup")
def startup_event():
    scrape_supplier_updates()
    schedule.every(4).hours.do(scrape_supplier_updates)
    threading.Thread(target=scheduled_scraping, daemon=True).start()

@app.get("/supplier_updates.json")
async def get_supplier_json(request: Request):
    if request.query_params.get('api_key') != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = get_supplier_data()
    return JSONResponse(content=data)

@app.get("/supplier_updates.csv")
async def get_supplier_csv(request: Request):
    if request.query_params.get('api_key') != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = get_supplier_data()
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=supplier_updates.csv"
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
