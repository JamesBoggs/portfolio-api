from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Quant Portfolio API", version="1.0.0")

# === Router Config ===
SERVICE_URLS = {
    "montecarlo": "https://montecarlo-fastapi.onrender.com",
    "forecast": "https://forecast-fastapi.onrender.com",
    "sentiment": "https://sentiment-fastapi.onrender.com"
}

# === Proxy: Health Check ===
@app.get("/health")
def health():
    return {"ok": True, "services": list(SERVICE_URLS.keys())}

# === Proxy: Monte Carlo ===
class MonteCarloRequest(BaseModel):
    S0: float = 100.0
    T: float = 1.0
    steps: int = 100
    sims: int = 1000

@app.post("/simulate")
def proxy_montecarlo(req: MonteCarloRequest):
    try:
        url = f"{SERVICE_URLS['montecarlo']}/simulate"
        resp = httpx.post(url, json=req.dict(), timeout=30.0)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

# === Proxy: Forecast ===
class ForecastRequest(BaseModel):
    values: list[float]  # expects 12 values

@app.post("/predict")
def proxy_forecast(req: ForecastRequest):
    try:
        url = f"{SERVICE_URLS['forecast']}/predict"
        resp = httpx.post(url, json=req.dict(), timeout=15.0)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

# === Proxy: Sentiment ===
class SentimentRequest(BaseModel):
    text: str

@app.post("/score")
def proxy_sentiment(req: SentimentRequest):
    try:
        url = f"{SERVICE_URLS['sentiment']}/score"
        resp = httpx.post(url, json=req.dict(), timeout=15.0)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
