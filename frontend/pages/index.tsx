import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import the map to avoid SSR issues
const MapComponent = dynamic(() => import('../components/MapComponent'), {
  ssr: false,
  loading: () => <div className="map-loading">Loading map...</div>
});

interface AnalysisResult {
  status: string;
  parcel_id: string;
  analysis?: {
    soil_summary: string;
    soil_quality: string;
    soil_score: number;
    land_value_estimate: {
      estimated_value: number;
      value_per_acre: number;
      total_acres: number;
    };
    funding_recommendation: {
      type: string;
      programs: string[];
      notes: string;
    };
  };
}

export default function Home() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCoords, setSelectedCoords] = useState<[number, number] | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ugs-backend.onrender.com';

  const handleMapClick = async (lat: number, lng: number) => {
    setSelectedCoords([lat, lng]);
    setLoading(true);
    setError(null);
    try {
      const uploadRes = await fetch(`${API_URL}/upload-land`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: lat, longitude: lng, location: `${lat.toFixed(4)}, ${lng.toFixed(4)}`, size: 5.0 })
      });
      const uploadData = await uploadRes.json();
      const analyzeRes = await fetch(`${API_URL}/analyze-land?parcel_id=${uploadData.parcel_id}`);
      const analyzeData = await analyzeRes.json();
      setResult(analyzeData);
    } catch (err) {
      setError('Failed to connect to API. Please check backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', minHeight: '100vh', background: '#0f172a', color: '#e2e8f0' }}>
      <header style={{ background: '#1e293b', padding: '16px 24px', borderBottom: '2px solid #10b981' }}>
        <h1 style={{ margin: 0, color: '#10b981', fontSize: '24px' }}>UGS Platform</h1>
        <p style={{ margin: '4px 0 0', color: '#94a3b8', fontSize: '14px' }}>United Growth Systems - AI Land Intelligence</p>
      </header>
      <main style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ background: '#1e293b', borderRadius: '8px', padding: '16px', marginBottom: '24px' }}>
          <h2 style={{ color: '#10b981', marginTop: 0 }}>Click on the map to analyze land</h2>
          <div style={{ height: '400px', borderRadius: '8px', overflow: 'hidden' }}>
            <MapComponent onMapClick={handleMapClick} selectedCoords={selectedCoords} />
          </div>
        </div>
        {loading && <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', textAlign: 'center' }}>Analyzing land parcel...</div>}
        {error && <div style={{ background: '#7f1d1d', padding: '16px', borderRadius: '8px', color: '#fca5a5' }}>{error}</div>}
        {result && result.analysis && (
          <div style={{ background: '#1e293b', borderRadius: '8px', padding: '24px' }}>
            <h2 style={{ color: '#10b981', marginTop: 0 }}>Land Analysis Report</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', borderLeft: '4px solid #10b981' }}>
                <h3 style={{ color: '#10b981', marginTop: 0 }}>Soil Analysis</h3>
                <p><strong>Quality:</strong> {result.analysis.soil_quality}</p>
                <p><strong>Score:</strong> {result.analysis.soil_score}/10</p>
                <p style={{ fontSize: '14px', color: '#94a3b8' }}>{result.analysis.soil_summary}</p>
              </div>
              <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', borderLeft: '4px solid #3b82f6' }}>
                <h3 style={{ color: '#3b82f6', marginTop: 0 }}>Land Value Estimate</h3>
                <p><strong>Total Value:</strong> ${result.analysis.land_value_estimate.estimated_value.toLocaleString()}</p>
                <p><strong>Per Acre:</strong> ${result.analysis.land_value_estimate.value_per_acre.toLocaleString()}</p>
                <p><strong>Total Acres:</strong> {result.analysis.land_value_estimate.total_acres}</p>
              </div>
              <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', borderLeft: '4px solid #f59e0b' }}>
                <h3 style={{ color: '#f59e0b', marginTop: 0 }}>Funding Recommendation</h3>
                <p><strong>Type:</strong> {result.analysis.funding_recommendation.type}</p>
                <ul style={{ fontSize: '14px', color: '#94a3b8', paddingLeft: '16px' }}>
                  {result.analysis.funding_recommendation.programs.map((p, i) => <li key={i}>{p}</li>)}
                </ul>
                <p style={{ fontSize: '13px', color: '#94a3b8' }}>{result.analysis.funding_recommendation.notes}</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
