from fastapi import FastAPI, HTTPException
from scraper import search_scholar, get_working_proxy, init_proxies

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_proxies()

@app.get("/search/")
async def search(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    working_proxy = get_working_proxy()  # Attempt to get a working proxy
    if not working_proxy:
        raise HTTPException(status_code=500, detail="No working proxies available.")
    
    try:
        results = search_scholar(keyword, working_proxy)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
