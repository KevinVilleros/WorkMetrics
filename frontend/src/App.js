import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/')
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
        <h1>Sec-0,1-bet</h1>
        <p>Sistema de Monitoreo de Eficiencia Laboral</p>
      </header>

      <section className="status-card">
        {loading && <p>Cargando estado del servidor...</p>}
        {error && <p className="error">No se pudo conectar: {error}</p>}
        {status && (
          <div>
            <h2>API conectada</h2>
            <p>{status.message}</p>
            <p>Estado: {status.status}</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
