# UGS Platform Workflow Documentation

## n8n Automation Workflow

### Trigger
- New entry in `land_parcels` Supabase table

### Actions
1. **Webhook Trigger**: Fires on INSERT to `land_parcels`
2. **HTTP Request**: Call `GET /analyze-land?parcel_id={id}`
3. **HTTP Request**: Call `GET /generate-report?parcel_id={id}`
4. **Supabase Update**: Store report URL in `reports` table

## System Architecture

```
User Browser
    |
    v
Next.js Frontend (Vercel)
    |
    v
FastAPI Backend (Render)
    |
    +-- AI Agent (LangChain)
    |
    +-- Supabase Database
    |       +-- users
    |       +-- land_parcels
    |       +-- reports
    |
    +-- n8n Automation
    |
    +-- Metabase Dashboard
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload-land | Submit land coordinates |
| GET | /analyze-land | Get AI analysis |
| GET | /generate-report | Generate PDF report |

## Deployment URLs
- Frontend: TBD (Vercel)
- Backend: TBD (Render)
- Database: Supabase
