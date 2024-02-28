import os
from fastapi import FastAPI, HTTPException, Request
from scraper import search_papers, get_working_proxy, init_proxies
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from the environment variable and split into a set
API_KEYS = set(os.getenv("API_KEYS", "").split(","))
if not API_KEYS:
    raise Exception("API_KEYS environment variable is not set.")

@app.on_event("startup")
async def startup_event():
    init_proxies()

def validate_api_key(api_key: str):
    """Validate the provided API key."""
    return api_key in API_KEYS

@app.get("/search/")
async def search(request: Request, keyword: str):
    # Extract the API key from the request headers
    api_key = request.headers.get("x-api-key")
    if not api_key or not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    working_proxy = get_working_proxy()  # Attempt to get a working proxy
    if not working_proxy:
        raise HTTPException(status_code=500, detail="No working proxies available.")
    
    try:
        results = search_papers(keyword, working_proxy)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
