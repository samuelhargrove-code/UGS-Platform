# UGS Platform

UGS (United Growth Systems) is an AI-powered land intelligence and financial enablement platform that converts land data into bankable financial 

## Live Deployment

- **Frontend**: https://ugs-platform.vercel.app
- **Backend API**: https://ugs-backend.onrender.com
- **API Docs**: https://ugs-backend.onrender.com/docsinsights.

## Architecture

- **Frontend**: Next.js + Leaflet (deployed on Vercel)
- **Backend**: FastAPI + Python (deployed on Render)
- **Database**: Supabase (PostgreSQL)
- **AI Engine**: LangChain-powered land analysis agent
- **Automation**: n8n workflow automation
- **Analytics**: Metabase dashboard

## Project Structure

```
/frontend     - Next.js app with Leaflet map interface
/backend      - FastAPI Python backend with AI endpoints
/ai-agents    - LangChain AI land analysis engine
/geospatial   - Geospatial data processing module
/docs         - Architecture and workflow documentation
```

## API Endpoints

- `POST /upload-land` - Submit land coordinates
- `GET /analyze-land` - Get AI-powered land analysis
- `GET /generate-report` - Generate PDF report

## Features

- Interactive map for land parcel selection
- AI-powered soil quality analysis
- Land value estimation
- Funding program recommendations
- Automated PDF report generation
- Real-time analytics dashboard

## Live URLs

- Frontend: https://ugs-platform.vercel.app (LIVE)
- Backend API: https://ugs-backend.onrender.com (pending)
- Database: Supabase
