import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import { saveAttentionEvent } from '../services/reportService';
import { API_BASE } from '../services/api';
import PersonTracker from '../services/trackingService';
import './PersonDetector.css';

const PersonDetector = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const overlayRef = useRef(null);
  const trackerRef = useRef(new PersonTracker(5, 5000));
  const [isDetecting, setIsDetecting] = useState(false);
  const [detectionResult, setDetectionResult] = useState(null);
  const [trackedPersons, setTrackedPersons] = useState([]);
  const [trackedStats, setTrackedStats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stream, setStream] = useState(null);
  const [fps, setFps] = useState(0);
  const fpsRef = useRef(0);
  const lastFrameRef = useRef(Date.now());

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' }
      });
      videoRef.current.srcObject = mediaStream;
      setStream(mediaStream);
      setIsDetecting(true);
      setError(null);
    } catch (err) {
      setError('No se pudo acceder a la cámara');
      console.error('Error al acceder a cámara:', err);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setIsDetecting(false);
    }
  };

  const captureFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const width = video.videoWidth;
    const height = video.videoHeight;
    if (!width || !height) return;

    const ctx = canvas.getContext('2d');
    canvas.width = width;
    canvas.height = height;
    ctx.drawImage(video, 0, 0, width, height);
    const imageData = canvas.toDataURL('image/jpeg', 0.8);

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/detect/`, {
        image: imageData
      });
      
      const result = response.data;
      
      // Procesar múltiples detecciones si existen
      const detections = Array.isArray(result) ? result : [result];
      
      // Actualizar tracking
      const trackingData = trackerRef.current.updateTracking(detections);
      setTrackedPersons(trackingData.trackedPersons);
      setTrackedStats(trackerRef.current.getAllStats());
      
      // Usar la primera detección para compatibilidad
      setDetectionResult(result);
      setError(null);

      // Guardar evento de atención para cada persona
      if (Array.isArray(result)) {
        result.forEach(async (res) => {
          await saveAttentionEvent({
            person_detected: res.person_detected,
            head_orientation: res.head_orientation,
            distracted: res.distracted,
            eyes_detected: res.eyes_detected,
            message: res.message,
            attention_score: res.attention_score,
          });
        });
      } else {
        await saveAttentionEvent({
          person_detected: result.person_detected,
          head_orientation: result.head_orientation,
          distracted: result.distracted,
          eyes_detected: result.eyes_detected,
          message: result.message,
          attention_score: result.attention_score,
        });
      }

      // Calcular FPS
      const now = Date.now();
      const deltaTime = now - lastFrameRef.current;
      if (deltaTime > 0) {
        fpsRef.current = Math.round(1000 / deltaTime);
        setFps(fpsRef.current);
      }
      lastFrameRef.current = now;
    } catch (err) {
      setError('Error en la detección del backend');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearOverlay = () => {
    if (!overlayRef.current) return;
    const ctx = overlayRef.current.getContext('2d');
    ctx.clearRect(0, 0, overlayRef.current.width, overlayRef.current.height);
  };

  const drawOverlay = (trackedPersonsData) => {
    if (!videoRef.current || !overlayRef.current || !trackedPersonsData || trackedPersonsData.length === 0) {
      clearOverlay();
      return;
    }
    
    const video = videoRef.current;
    const canvas = overlayRef.current;
    const width = video.videoWidth;
    const height = video.videoHeight;
    if (!width || !height) return;

    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, width, height);

    // Colores para diferentes IDs de personas
    const colors = ['#22c55e', '#ef4444', '#3b82f6', '#f59e0b', '#8b5cf6'];

    trackedPersonsData.forEach((person, index) => {
      const { box, detectionHistory, id, averageAttentionScore } = person;
      if (!box || !detectionHistory || detectionHistory.length === 0) return;

      const lastDetection = detectionHistory[detectionHistory.length - 1];
      const color = colors[id % colors.length];
      const highlightColor = lastDetection.distracted ? '#f97316' : color;

      // Dibujar caja de detección
      const { x, y, w, h } = box;
      ctx.fillStyle = `${highlightColor}33`;
      ctx.strokeStyle = highlightColor;
      ctx.lineWidth = 3;
      ctx.fillRect(x, y, w, h);
      ctx.strokeRect(x, y, w, h);

      // ID de persona
      ctx.font = 'bold 18px Inter, sans-serif';
      ctx.fillStyle = highlightColor;
      ctx.fillText(`Persona #${id}`, x + 10, y - 10);

      // Score de atención y estado
      ctx.font = '14px Inter, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.fillText(
        `Atención: ${(averageAttentionScore * 100).toFixed(0)}%`,
        x + 10,
        y + h + 20
      );
      ctx.fillText(
        `Frames: ${detectionHistory.length}`,
        x + 10,
        y + h + 38
      );

      // Indicador de estado
      const statusText = lastDetection.distracted ? '⚠ DISTRAÍDO' : '✓ ATENDIENDO';
      ctx.fillStyle = lastDetection.distracted ? '#f97316' : '#22c55e';
      ctx.fillText(statusText, x + 10, y + h + 56);

      // Dibujar histórico de movimiento (trail)
      if (detectionHistory.length > 1) {
        ctx.strokeStyle = `${highlightColor}66`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        detectionHistory.slice(-10).forEach((detection, idx) => {
          if (idx === 0) {
            ctx.moveTo(x + w / 2, y + h / 2);
          } else {
            ctx.lineTo(x + w / 2, y + h / 2);
          }
        });
        ctx.stroke();
      }
    });

    // Mostrar FPS
    ctx.font = 'bold 14px Inter, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`FPS: ${fps}`, 10, 25);
    ctx.fillText(`Personas: ${trackedPersonsData.length}`, 10, 45);
  };

  useEffect(() => {
    if (trackedPersons && trackedPersons.length > 0) {
      drawOverlay(trackedPersons);
    } else {
      clearOverlay();
    }
  }, [trackedPersons, fps]);

  useEffect(() => {
    if (!isDetecting) return;

    const interval = setInterval(() => {
      captureFrame();
    }, 1500);

    return () => clearInterval(interval);
  }, [isDetecting]);

  return (
    <div className="person-detector">
      <h2>Detector de Personas</h2>

      <div className="detector-container">
        <div className="video-section">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="video-feed"
          />
          <canvas ref={overlayRef} className="canvas-overlay" />
          <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>

        <div className="controls">
          {!isDetecting ? (
            <button onClick={startCamera} className="btn btn-primary">
              📹 Iniciar Cámara
            </button>
          ) : (
            <button onClick={stopCamera} className="btn btn-danger">
              ⏹️ Detener Cámara
            </button>
          )}
        </div>

        {loading && <div className="loading">Detectando persona...</div>}
        {error && <div className="error">❌ {error}</div>}

        {detectionResult && (
          <div className="detection-result">
            <h3>Resultado de Detección</h3>
            <p>
              <strong>Persona detectada:</strong>{' '}
              {detectionResult.person_detected ? '✅ Sí' : '❌ No'}
            </p>
            <p>
              <strong>Orientación de cabeza:</strong>{' '}
              {detectionResult.head_orientation}
            </p>
            <p>
              <strong>Estado de atención:</strong>{' '}
              {detectionResult.distracted ? '🟠 Distraída / mirando a otro lado' : '🟢 Atenta'}
            </p>
            <p>
              <strong>Ojos detectados:</strong>{' '}
              {detectionResult.eyes_detected}
            </p>
            <div className="graph-panel">
              <div className="score-label">Nivel de atención</div>
              <div className="score-bar">
                <div
                  className="score-fill"
                  style={{ width: `${(detectionResult.attention_score ?? 0) * 100}%` }}
                />
              </div>
              <div className="graph-metrics">
                <div className="metric-pill">
                  <span>Ojos</span>
                  <strong>{detectionResult.eyes_detected}</strong>
                </div>
                <div className="metric-pill">
                  <span>Tamaño</span>
                  <strong>{(detectionResult.face_size_ratio ?? 0).toFixed(2)}</strong>
                </div>
                <div className="metric-pill">
                  <span>Confiabilidad</span>
                  <strong>{(detectionResult.confidence ?? 0).toFixed(2)}</strong>
                </div>
              </div>
            </div>
            <p className="message">{detectionResult.message}</p>

            {detectionResult.person_detected && (
              <div className="landmarks">
                <h4>Puntos detectados:</h4>
                <ul>
                  {detectionResult.landmarks.slice(0, 5).map((lm, i) => (
                    <li key={i}>
                      Punto {i + 1}: ({lm.x.toFixed(3)}, {lm.y.toFixed(3)})
                    </li>
                  ))}
                  {detectionResult.landmarks.length > 5 && (
                    <li>... y {detectionResult.landmarks.length - 5} puntos más</li>
                  )}
                </ul>
              </div>
            )}
          </div>
        )}

        {trackedStats.length > 0 && (
          <div className="tracking-stats">
            <h3>📊 Estadísticas de Tracking</h3>
            <div className="stats-grid">
              {trackedStats.map((stat) => (
                <div key={stat.personId} className="stat-card">
                  <div className="stat-header">Persona #{stat.personId}</div>
                  <div className="stat-body">
                    <div className="stat-row">
                      <span>Frames rastreados:</span>
                      <strong>{stat.framesTracked}</strong>
                    </div>
                    <div className="stat-row">
                      <span>Atención promedio:</span>
                      <strong>{(stat.averageAttentionScore * 100).toFixed(1)}%</strong>
                    </div>
                    <div className="stat-row">
                      <span>Máx/Mín:</span>
                      <strong>
                        {(stat.maxAttentionScore * 100).toFixed(0)}% / {(stat.minAttentionScore * 100).toFixed(0)}%
                      </strong>
                    </div>
                    <div className="stat-row">
                      <span>Desatención:</span>
                      <strong>{stat.distractedPercentage.toFixed(1)}%</strong>
                    </div>
                    <div className="stat-row">
                      <span>Duración:</span>
                      <strong>{((stat.trackedDuration / 1000).toFixed(1))}s</strong>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PersonDetector;
