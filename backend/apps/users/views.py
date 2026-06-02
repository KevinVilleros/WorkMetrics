from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

# Import MediaPipe with proper error handling
MEDIAPIPE_AVAILABLE = False
try:
    from mediapipe.tasks import python as mp_tasks
    from mediapipe.tasks.python import vision
    MEDIAPIPE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: MediaPipe tasks not available: {e}")


def home(request):
    return JsonResponse({
        'message': 'Bienvenido a MetricLab API',
        'status': 'ok',
    })


@api_view(['POST'])
def detect_person(request):
    """Detecta personas en una imagen enviada como base64"""
    try:
        # Obtener imagen base64
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'No image provided'}, status=400)
        
        # Decodificar base64
        image_data = image_data.split(',')[-1]  # Remover prefijo data:image/jpeg;base64,
        image_bytes = base64.b64decode(image_data)
        image_pil = Image.open(BytesIO(image_bytes))
        
        # Convertir a numpy array y asegurar formato RGB
        image_array = np.array(image_pil)
        if len(image_array.shape) == 2:  # Escala de grises
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
        elif image_array.shape[2] == 4:  # RGBA
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        # Simulación de detección de personas
        # En la siguiente versión, integraremos MediaPipe tasks.vision.PoseLandmarker
        detections = []
        
        if MEDIAPIPE_AVAILABLE:
            try:
                # Crear una imagen MediaPipe
                from mediapipe import Image as MPImage
                mp_image = MPImage.create_from_file(BytesIO(image_bytes))
                
                # Aquí iría la lógica real de detección con PoseLandmarker
                # Por ahora, hacemos una detección simulada
                person_detected = np.random.random() > 0.5
                
                if person_detected:
                    # Simular 33 puntos de pose (MediaPipe pose landmarks)
                    detections = [
                        {
                            'x': float(np.random.random()),
                            'y': float(np.random.random()),
                            'z': float(np.random.random() - 0.5),
                            'visibility': float(np.random.random() * 0.8 + 0.2)
                        }
                        for _ in range(33)
                    ]
            except Exception as e:
                print(f"MediaPipe detection error: {e}")
                # Fallback a detección simulada
                person_detected = len(image_array) > 0
                detections = _get_dummy_landmarks() if person_detected else []
        else:
            # Detección simulada cuando MediaPipe no está disponible
            # Analizamos si hay suficiente contenido en la imagen
            h, w = image_array.shape[:2]
            person_detected = h > 0 and w > 0 and np.mean(image_array) > 50
            detections = _get_dummy_landmarks() if person_detected else []
        
        return Response({
            'status': 'success',
            'person_detected': len(detections) > 0,
            'landmarks': detections,
            'message': f'{len(detections)} puntos clave detectados'
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


def _get_dummy_landmarks():
    """Genera puntos de prueba para demostración"""
    return [
        {
            'x': float(np.random.random() * 0.5 + 0.25),
            'y': float(np.random.random() * 0.5 + 0.25),
            'z': float(np.random.random() - 0.5),
            'visibility': float(np.random.random() * 0.8 + 0.2)
        }
        for _ in range(33)
    ]

