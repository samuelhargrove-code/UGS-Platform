from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="UGS Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LandData(BaseModel):
    latitude: float
    longitude: float
    location: Optional[str] = ""
    size: Optional[float] = 0.0

@app.get("/")
def root():
    return {"message": "UGS Platform API is running", "status": "ok"}

@app.post("/upload-land")
async def upload_land(data: LandData):
    return {
        "status": "success",
        "message": "Land data received",
        "parcel_id": "parcel-001",
        "data": {
            "latitude": data.latitude,
            "longitude": data.longitude,
            "location": data.location,
            "size": data.size
        }
    }

@app.get("/analyze-land")
async def analyze_land(parcel_id: str = "parcel-001"):
    from ai_agents.agent import analyze_land_parcel
    result = analyze_land_parcel({
        "parcel_id": parcel_id,
        "location": "Raleigh, NC",
        "size": 5.0,
        "soil_score": 7.5
    })
    return result

@app.get("/generate-report")
async def generate_report(parcel_id: str = "parcel-001"):
    return {
        "status": "success",
        "parcel_id": parcel_id,
        "report_url": f"/reports/{parcel_id}.pdf",
        "message": "Report generated successfully"
    }
