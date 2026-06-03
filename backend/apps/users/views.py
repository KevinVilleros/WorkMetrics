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


def _load_cascades():
    face_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    eye_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
    face_cascade = cv2.CascadeClassifier(face_path)
    eye_cascade = cv2.CascadeClassifier(eye_path)
    return face_cascade, eye_cascade


def _select_largest_face(faces):
    if len(faces) == 0:
        return None
    return max(faces, key=lambda rect: rect[2] * rect[3])


def _analyze_face_attention(face, eyes):
    x, y, w, h = face
    orientation = 'frente'
    distracted = False
    message = 'Persona frente a cámara y atendiendo'

    eye_centers = [
        (ex + ew / 2, ey + eh / 2)
        for (ex, ey, ew, eh) in eyes[:2]
    ]

    if len(eye_centers) >= 2:
        avg_x = sum(cx for cx, _ in eye_centers) / len(eye_centers)
        avg_y = sum(cy for _, cy in eye_centers) / len(eye_centers)
        norm_x = avg_x / w
        norm_y = avg_y / h

        if norm_y < 0.22:
            orientation = 'arriba'
            message = 'Persona mirando hacia arriba'
        elif norm_y > 0.40:
            orientation = 'abajo'
            message = 'Persona mirando hacia abajo'
        elif norm_x < 0.45:
            orientation = 'derecha'
            message = 'Persona mirando hacia la derecha'
        elif norm_x > 0.55:
            orientation = 'izquierda'
            message = 'Persona mirando hacia la izquierda'
        else:
            orientation = 'frente'
            message = 'Persona frente a cámara y atendiendo'

        distracted = orientation != 'frente'
    elif len(eye_centers) == 1:
        cx, cy = eye_centers[0]
        norm_x = cx / w
        norm_y = cy / h
        if norm_x < 0.35:
            orientation = 'derecha'
            message = 'Persona mirando hacia la derecha'
        elif norm_x > 0.65:
            orientation = 'izquierda'
            message = 'Persona mirando hacia la izquierda'
        elif norm_y < 0.22:
            orientation = 'arriba'
            message = 'Persona mirando hacia arriba'
        elif norm_y > 0.40:
            orientation = 'abajo'
            message = 'Persona mirando hacia abajo'
        else:
            orientation = 'frente'
            message = 'Rostro detectado, pero sólo se detecta un ojo claramente'
        distracted = True
    else:
        orientation = 'desconocida'
        distracted = True
        message = 'Rostro detectado, pero no se detectaron ojos para evaluar atención'

    return orientation, distracted, message, eye_centers


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
        
        # Detectar rostro y ojos con OpenCV para evaluar orientación y atención
        detections = []
        h, w = image_array.shape[:2]
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        face_cascade, eye_cascade = _load_cascades()
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(120, 120))

        if len(faces) == 0:
            return Response({
                'status': 'success',
                'person_detected': False,
                'landmarks': [],
                'message': 'No se detectó una cara claramente',
                'head_orientation': 'desconocida',
                'distracted': False,
                'eyes_detected': 0,
                'face_box': None,
            })

        face = _select_largest_face(faces)
        x, y, fw, fh = face
        face_gray = gray[y:y+fh, x:x+fw]
        eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        orientation, distracted, attention_message, eye_centers = _analyze_face_attention(face, eyes)

        landmarks = []
        for cx, cy in eye_centers:
            landmarks.append({
                'x': float(cx / fw),
                'y': float(cy / fh),
                'visibility': 1.0,
            })
        landmarks.append({
            'x': float((x + fw / 2) / w),
            'y': float((y + fh / 2) / h),
            'visibility': 1.0,
        })

        return Response({
            'status': 'success',
            'person_detected': True,
            'landmarks': landmarks,
            'message': attention_message,
            'head_orientation': orientation,
            'distracted': distracted,
            'eyes_detected': len(eyes),
            'face_box': {'x': int(x), 'y': int(y), 'w': int(fw), 'h': int(fh)},
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

