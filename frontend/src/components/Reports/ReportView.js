import React, { useEffect, useState } from 'react';
import { getComplianceReport } from '../../services/reportService';
import './ReportView.css';

const ReportView = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadReport = async () => {
    setLoading(true);
    try {
      const response = await getComplianceReport();
      setReport(response.data);
      setError(null);
    } catch (err) {
      console.error('Error cargando informe:', err);
      setError('No se pudo cargar el informe de cumplimiento.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, []);

  return (
    <div className="report-view">
      <div className="report-header">
        <h2>Informe de Cumplimiento</h2>
        <button className="btn btn-secondary" onClick={loadReport} disabled={loading}>
          {loading ? 'Actualizando...' : 'Actualizar informe'}
        </button>
      </div>

      {error && <div className="report-error">❌ {error}</div>}

      {report ? (
        <div className="report-content">
          <div className="report-summary">
            <div className="report-score">
              <span className="score-value">{report.compliance_score}%</span>
              <span className="score-label">Nivel de cumplimiento</span>
            </div>
            <div className="report-text">
              <p>{report.summary}</p>
              <p>
                <strong>Estado:</strong> {report.compliance_level}
              </p>
            </div>
          </div>

          <div className="report-metrics">
            <div className="metric-card">
              <h4>Total de observaciones</h4>
              <p>{report.total_checks}</p>
            </div>
            <div className="metric-card">
              <h4>Observaciones atentas</h4>
              <p>{report.attentive_checks}</p>
            </div>
            <div className="metric-card">
              <h4>Observaciones distraídas</h4>
              <p>{report.distracted_checks}</p>
            </div>
            <div className="metric-card">
              <h4>No se detectó rostro</h4>
              <p>{report.no_face_checks}</p>
            </div>
          </div>

          {report.orientation_breakdown && Object.keys(report.orientation_breakdown).length > 0 && (
            <div className="report-breakdown">
              <h4>Orientación de cabeza</h4>
              <ul>
                {Object.entries(report.orientation_breakdown).map(([orientation, count]) => (
                  <li key={orientation}>
                    <strong>{orientation}:</strong> {count}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {report.recent_events && report.recent_events.length > 0 && (
            <div className="report-events">
              <h4>Últimos eventos</h4>
              <ul>
                {report.recent_events.map((event, index) => (
                  <li key={index}>
                    {new Date(event.timestamp).toLocaleTimeString()} - {event.person_detected ? 'Rostro detectado' : 'Sin rostro'} - {event.head_orientation} - {event.distracted ? 'Distraído' : 'Atento'}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ) : (
        !loading && <p>No hay datos suficientes para generar el informe.</p>
      )}
    </div>
  );
};

export default ReportView;
