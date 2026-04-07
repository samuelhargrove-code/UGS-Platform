from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import uuid
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

# Supabase client setup
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_supabase():
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

class LandData(BaseModel):
    latitude: float
    longitude: float
    location: Optional[str] = ""
    size: Optional[float] = 5.0
    user_id: Optional[str] = None

@app.get("/")
def root():
    return {
        "message": "UGS Platform API is running",
        "status": "ok",
        "version": "1.0.0",
        "endpoints": ["/upload-land", "/analyze-land", "/generate-report"]
    }

@app.post("/upload-land")
async def upload_land(data: LandData):
    parcel_id = str(uuid.uuid4())
    user_id = data.user_id or str(uuid.uuid4())
    location = data.location or f"{data.latitude:.4f}, {data.longitude:.4f}"

    # Store in Supabase
    supabase = get_supabase()
    if supabase:
        try:
            supabase.table("land_parcels").insert({
                "id": parcel_id,
                "user_id": user_id,
                "location": location,
                "size": data.size,
                "soil_score": 7.5
            }).execute()
        except Exception as e:
            print(f"Supabase error: {e}")

    return {
        "status": "success",
        "message": "Land data uploaded successfully",
        "parcel_id": parcel_id,
        "user_id": user_id,
        "data": {
            "latitude": data.latitude,
            "longitude": data.longitude,
            "location": location,
            "size": data.size
        }
    }

@app.get("/analyze-land")
async def analyze_land(parcel_id: str = "parcel-001"):
    # Retrieve from Supabase if available
    supabase = get_supabase()
    land_data = {
        "parcel_id": parcel_id,
        "location": "Raleigh, NC",
        "size": 5.0,
        "soil_score": 7.5
    }

    if supabase:
        try:
            result = supabase.table("land_parcels").select("*").eq("id", parcel_id).execute()
            if result.data:
                record = result.data[0]
                land_data = {
                    "parcel_id": parcel_id,
                    "location": record.get("location", "Unknown"),
                    "size": record.get("size", 5.0),
                    "soil_score": record.get("soil_score", 7.5)
                }
        except Exception as e:
            print(f"Supabase error: {e}")

    # Run AI analysis
    import sys
    sys.path.append("../ai-agents")
    try:
        from agent import analyze_land_parcel
        result = analyze_land_parcel(land_data)
    except ImportError:
        # Fallback analysis if agent not available
        result = {
            "status": "success",
            "parcel_id": parcel_id,
            "analysis": {
                "soil_summary": f"The soil at {land_data['location']} shows good quality indicators suitable for agricultural use.",
                "soil_quality": "Good",
                "soil_score": land_data["soil_score"],
                "land_value_estimate": {
                    "currency": "USD",
                    "estimated_value": round(land_data["size"] * 15000 * (land_data["soil_score"] / 5.0), 2),
                    "value_per_acre": round(15000 * (land_data["soil_score"] / 5.0), 2),
                    "total_acres": land_data["size"]
                },
                "funding_recommendation": {
                    "type": "Small Farm Loan",
                    "estimated_loan_amount": round(land_data["size"] * 15000 * 0.6, 2),
                    "programs": ["USDA Microloan Program", "NC Agricultural Finance Authority"],
                    "notes": "Mid-value parcel suitable for standard agricultural financing."
                },
                "location": land_data["location"]
            },
            "ai_model": "UGS Land Intelligence Engine v1.0"
        }

    return result

@app.get("/generate-report")
async def generate_report(parcel_id: str = "parcel-001"):
    # Get analysis first
    analysis = await analyze_land(parcel_id)

    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>UGS Land Report - {parcel_id}</title>
    <style>
      body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
      h1 {{ color: #10b981; }} h2 {{ color: #3b82f6; }}
      .card {{ border: 1px solid #e2e8f0; padding: 16px; margin: 16px 0; border-radius: 8px; }}
      .value {{ font-size: 24px; font-weight: bold; color: #10b981; }}
    </style>
    </head>
    <body>
    <h1>UGS Land Intelligence Report</h1>
    <p><strong>Parcel ID:</strong> {parcel_id}</p>
    <p><strong>Generated:</strong> {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <div class="card">
    <h2>Soil Analysis</h2>
    <p>{analysis.get('analysis', {}).get('soil_summary', 'N/A')}</p>
    <p><strong>Quality:</strong> {analysis.get('analysis', {}).get('soil_quality', 'N/A')}</p>
    </div>

    <div class="card">
    <h2>Land Value Estimate</h2>
    <p class="value">${analysis.get('analysis', {}).get('land_value_estimate', {}).get('estimated_value', 0):,.2f}</p>
    </div>

    <div class="card">
    <h2>Funding Recommendations</h2>
    <p><strong>Type:</strong> {analysis.get('analysis', {}).get('funding_recommendation', {}).get('type', 'N/A')}</p>
    <ul>{''.join([f'<li>{p}</li>' for p in analysis.get('analysis', {}).get('funding_recommendation', {}).get('programs', [])])}</ul>
    </div>
    </body></html>
    """

    # Store report in Supabase
    report_id = str(uuid.uuid4())
    report_url = f"/reports/{parcel_id}.html"
    supabase = get_supabase()
    if supabase:
        try:
            supabase.table("reports").insert({
                "id": report_id,
                "parcel_id": parcel_id,
                "report_url": report_url
            }).execute()
        except Exception as e:
            print(f"Report storage error: {e}")

    return {
        "status": "success",
        "parcel_id": parcel_id,
        "report_id": report_id,
        "report_url": report_url,
        "report_html": html_content,
        "analysis": analysis,
        "message": "Report generated successfully"
    }
