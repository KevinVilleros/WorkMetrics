import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import './PersonDetector.css';

const PersonDetector = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [detectionResult, setDetectionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stream, setStream] = useState(null);

  // Inicializar cámara
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

  // Detener cámara
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setIsDetecting(false);
    }
  };

  // Capturar frame y enviar al backend
  const captureFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const ctx = canvas.getContext('2d');

    // Ajustar dimensiones del canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Dibujar video en canvas
    ctx.drawImage(video, 0, 0);

    // Convertir a base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/detect/', {
        image: imageData
      });
      setDetectionResult(response.data);
      setError(null);
    } catch (err) {
      setError('Error en la detección');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Capturar automáticamente cada 1.5 segundos
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
              <strong>Puntos clave:</strong> {detectionResult.landmarks.length}
            </p>
            <p className="message">{detectionResult.message}</p>
            
            {detectionResult.person_detected && (
              <div className="landmarks">
                <h4>Puntos detectados:</h4>
                <ul>
                  {detectionResult.landmarks.slice(0, 5).map((lm, i) => (
                    <li key={i}>
                      Punto {i + 1}: ({lm.x.toFixed(2)}, {lm.y.toFixed(2)}) - Visibilidad: {(lm.visibility * 100).toFixed(0)}%
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
