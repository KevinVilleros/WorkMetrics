import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import { saveAttentionEvent } from '../services/reportService';
import { API_BASE } from '../services/api';
import './PersonDetector.css';

const PersonDetector = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const overlayRef = useRef(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [detectionResult, setDetectionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stream, setStream] = useState(null);

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
      setDetectionResult(result);
      setError(null);

      await saveAttentionEvent({
        person_detected: result.person_detected,
        head_orientation: result.head_orientation,
        distracted: result.distracted,
        eyes_detected: result.eyes_detected,
        message: result.message,
      });
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

  const drawOverlay = (result) => {
    if (!videoRef.current || !overlayRef.current || !result) return;
    const video = videoRef.current;
    const canvas = overlayRef.current;
    const width = video.videoWidth;
    const height = video.videoHeight;
    if (!width || !height) return;

    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, width, height);

    if (!result.person_detected || !result.face_box) return;

    const { x, y, w, h } = result.face_box;
    const highlightColor = result.distracted ? '#f97316' : '#22c55e';

    ctx.fillStyle = `${highlightColor}33`;
    ctx.strokeStyle = highlightColor;
    ctx.lineWidth = 4;
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);

    ctx.font = '16px Inter, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`Score: ${(result.attention_score || 0).toFixed(2)}`, x + 10, Math.max(20, y - 10));

    const eyePoints = (result.landmarks || []).slice(0, 2).map((lm) => ({
      x: x + lm.x * w,
      y: y + lm.y * h,
    }));

    eyePoints.forEach((point) => {
      ctx.beginPath();
      ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
      ctx.fillStyle = '#38bdf8';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    if (result.face_center) {
      const centerX = result.face_center.x * width;
      const centerY = result.face_center.y * height;
      ctx.strokeStyle = '#facc15';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(centerX - 10, centerY);
      ctx.lineTo(centerX + 10, centerY);
      ctx.moveTo(centerX, centerY - 10);
      ctx.lineTo(centerX, centerY + 10);
      ctx.stroke();
    }
  };

  useEffect(() => {
    if (detectionResult) {
      drawOverlay(detectionResult);
    } else {
      clearOverlay();
    }
  }, [detectionResult]);

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
      </div>
    </div>
  );
};

export default PersonDetector;
