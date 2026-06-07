import { useEffect, useState } from 'react';
import './App.css';
import PersonDetector from './components/PersonDetector';
import ReportView from './components/Reports/ReportView';
import { API_BASE } from './services/api';

function App() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setStatus(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <div>
          <h1>MetricLab</h1>
          <p>Monitoreo en tiempo real para verificar si el trabajador está atendiendo y cumpliendo sus tareas.</p>
        </div>
        <div className="app-badges">
          <span className="badge">Visión por cámara</span>
          <span className="badge">Reporte de cumplimiento</span>
          <span className="badge">Análisis de atención</span>
        </div>
      </header>

      <section className="status-card section-card">
        {loading && <p>Cargando estado del servidor...</p>}
        {error && <p className="error">No se pudo conectar: {error}</p>}
        {status && (
          <div className="status-grid">
            <div>
              <h2>API conectada</h2>
              <p>{status.message}</p>
            </div>
            <div className="status-pill">Estado: {status.status}</div>
          </div>
        )}
      </section>

      <div className="dashboard-grid">
        <section className="section-card">
          <PersonDetector />
        </section>

        <section className="section-card">
          <ReportView />
        </section>
      </div>
    </div>
  );
}

export default App;
