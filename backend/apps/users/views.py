from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image, UnidentifiedImageError

# Import MediaPipe with proper error handling
MEDIAPIPE_AVAILABLE = False
mp = None
MP_TASKS_VISION = None
MP_BASE_OPTIONS = None
try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core import base_options
    MP_TASKS_VISION = vision
    MP_BASE_OPTIONS = base_options
    if hasattr(mp, 'solutions'):
        MEDIAPIPE_AVAILABLE = True
    else:
        print('Warning: MediaPipe installed, but mp.solutions is unavailable. Using OpenCV fallback.')
except ImportError as e:
    print(f"Warning: MediaPipe not available: {e}")
except Exception as e:
    print(f"Warning: MediaPipe import error: {e}")


def _load_cascades():
    face_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    profile_path = cv2.data.haarcascades + 'haarcascade_profileface.xml'
    eye_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
    eye_tree_path = cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml'
    face_cascade = cv2.CascadeClassifier(face_path)
    profile_cascade = cv2.CascadeClassifier(profile_path)
    eye_cascade = cv2.CascadeClassifier(eye_path)
    eye_tree_cascade = cv2.CascadeClassifier(eye_tree_path)
    return face_cascade, profile_cascade, eye_cascade, eye_tree_cascade


def _select_largest_face(faces):
    if len(faces) == 0:
        return None
    return max(faces, key=lambda rect: rect[2] * rect[3])


def _filter_eye_candidates(eyes, face):
    x, y, w, h = face
    filtered = []
    for ex, ey, ew, eh in eyes:
        center_y = ey + eh / 2
        if center_y > h * 0.65:
            continue
        if ew < 0.08 * w or ew > 0.35 * w:
            continue
        if ew * eh < 0.0025 * w * h:
            continue
        filtered.append((ex, ey, ew, eh))
    return sorted(filtered, key=lambda rect: rect[0])


def _analyze_face_attention(face, eyes, image_size):
    x, y, w, h = face
    image_w, image_h = image_size
    orientation = 'frente'
    distracted = False
    message = 'Persona frente a cámara y atendiendo'

    face_center = (x + w / 2, y + h / 2)
    face_center_norm = (face_center[0] / image_w, face_center[1] / image_h)
    face_size_ratio = w / image_w

    eye_candidates = _filter_eye_candidates(eyes, face)
    eye_centers = [
        (ex + ew / 2, ey + eh / 2)
        for (ex, ey, ew, eh) in eye_candidates[:2]
    ]

    if len(eye_centers) >= 2:
        left_eye, right_eye = eye_centers[:2]
        avg_x = (left_eye[0] + right_eye[0]) / 2
        avg_y = (left_eye[1] + right_eye[1]) / 2
        norm_x = avg_x / w
        norm_y = avg_y / h
        eye_tilt = abs((right_eye[1] - left_eye[1]) / w)

        if eye_tilt > 0.10:
            orientation = 'inclinada'
            message = 'Cabeza inclinada; atención parcial'
        elif abs(norm_x - 0.5) > 0.18:
            orientation = 'derecha' if norm_x < 0.5 else 'izquierda'
            message = f'Persona mirando hacia la {orientation}'
        elif abs(norm_y - 0.5) > 0.14:
            orientation = 'arriba' if norm_y < 0.5 else 'abajo'
            message = f'Persona mirando hacia {orientation}'
        else:
            orientation = 'frente'
            message = 'Persona frente a cámara y atendiendo'

        distracted = orientation != 'frente'

        if face_size_ratio < 0.16:
            distracted = True
            message = 'Rostro pequeño; ajusta la cámara más cerca'
        if face_center_norm[0] < 0.12 or face_center_norm[0] > 0.88:
            distracted = True
            message = 'Rostro muy lateral; centra tu cara'

    elif len(eye_centers) == 1:
        cx, cy = eye_centers[0]
        norm_x = cx / w
        norm_y = cy / h
        if norm_x < 0.35:
            orientation = 'derecha'
            message = 'Rostro detectado, mirada hacia la derecha'
        elif norm_x > 0.65:
            orientation = 'izquierda'
            message = 'Rostro detectado, mirada hacia la izquierda'
        elif norm_y < 0.22:
            orientation = 'arriba'
            message = 'Rostro detectado, mirada hacia arriba'
        elif norm_y > 0.40:
            orientation = 'abajo'
            message = 'Rostro detectado, mirada hacia abajo'
        else:
            orientation = 'frente'
            message = 'Rostro detectado, pero sólo se detecta un ojo claramente'
        distracted = True

    else:
        orientation = 'desconocida'
        distracted = True
        message = 'Rostro detectado, pero no se detectaron ojos para evaluar atención'

    attention_score = 0.0
    if len(eye_centers) >= 2 and orientation == 'frente':
        attention_score = 1.0
    elif len(eye_centers) >= 2:
        attention_score = max(0.25, 1.0 - (abs(norm_x - 0.5) * 1.5 + abs(norm_y - 0.5)))
    elif len(eye_centers) == 1:
        attention_score = 0.25
    else:
        attention_score = 0.1

    confidence = 0.2
    if len(eye_centers) >= 2:
        confidence += 0.45
    elif len(eye_centers) == 1:
        confidence += 0.2
    if 0.16 <= face_size_ratio <= 0.45:
        confidence += 0.2
    if 0.12 < face_center_norm[0] < 0.88:
        confidence += 0.1
    if orientation == 'frente' and len(eye_centers) >= 2:
        confidence += 0.1

    confidence = float(min(max(confidence, 0.0), 1.0))
    attention_score = float(min(max(attention_score, 0.0), 1.0))

    return {
        'orientation': orientation,
        'distracted': distracted,
        'message': message,
        'eye_centers': eye_centers,
        'face_center_norm': face_center_norm,
        'face_size_ratio': face_size_ratio,
        'attention_score': attention_score,
        'confidence': confidence,
    }


def _validate_face_detection(face, eyes, face_size_ratio, face_center_norm):
    x, y, w, h = face
    aspect_ratio = w / h if h else 1.0

    if aspect_ratio < 0.55 or aspect_ratio > 1.8:
        return False, 'Rostro con proporciones atípicas; posible falso positivo.'

    if face_size_ratio < 0.12:
        return False, 'Rostro muy pequeño o lejano. Ajusta la cámara más cerca.'

    if len(eyes) == 0:
        return False, 'No se detectaron ojos; posible falso positivo.'

    if len(eyes) == 1 and face_size_ratio < 0.25:
        return False, 'Solo se detectó un ojo y el rostro es pequeño; posible falso positivo.'

    if face_center_norm[0] < 0.08 or face_center_norm[0] > 0.92:
        return False, 'Rostro muy lateral; coloca la cámara frente a ti.'

    return True, None


def _get_mediapipe_models():
    global mp
    if not MEDIAPIPE_AVAILABLE or not hasattr(mp, 'solutions'):
        return None, None
    if not hasattr(_get_mediapipe_models, 'face_detection'):
        _get_mediapipe_models.face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.45,
        )
        _get_mediapipe_models.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            refine_landmarks=True,
            min_detection_confidence=0.45,
        )
    return _get_mediapipe_models.face_detection, _get_mediapipe_models.face_mesh


def _compute_mesh_orientation(landmarks, box, image_size):
    x, y, w, h = box
    image_w, image_h = image_size
    face_center = (x + w / 2, y + h / 2)
    face_center_norm = (face_center[0] / image_w, face_center[1] / image_h)
    face_size_ratio = w / image_w

    def norm_point(index):
        lm = landmarks[index]
        return (lm.x * image_w, lm.y * image_h)

    left_eye = norm_point(33)
    right_eye = norm_point(263)
    nose_tip = norm_point(1)
    mouth = norm_point(0)

    avg_eye_x = (left_eye[0] + right_eye[0]) / 2
    avg_eye_y = (left_eye[1] + right_eye[1]) / 2
    norm_x = (nose_tip[0] - x) / w
    norm_y = (nose_tip[1] - y) / h
    eye_tilt = abs((right_eye[1] - left_eye[1]) / w)

    orientation = 'frente'
    message = 'Persona frente a cámara y atendiendo'
    distracted = False

    if eye_tilt > 0.09:
        orientation = 'inclinada'
        message = 'Cabeza inclinada; posible desviación'
        distracted = True
    elif abs(norm_x - 0.5) > 0.18:
        orientation = 'derecha' if norm_x < 0.5 else 'izquierda'
        message = f'Persona mirando hacia la {orientation}'
        distracted = True
    elif abs(norm_y - 0.5) > 0.14:
        orientation = 'arriba' if norm_y < 0.5 else 'abajo'
        message = f'Persona mirando hacia {orientation}'
        distracted = True

    if face_size_ratio < 0.16:
        message = 'Rostro pequeño; acercarse a la cámara'
        distracted = True

    if face_center_norm[0] < 0.12 or face_center_norm[0] > 0.88:
        message = 'Rostro muy lateral; deslízate al centro'
        distracted = True

    attention_score = 1.0 - min(max(abs(norm_x - 0.5) * 1.5 + abs(norm_y - 0.5), 0.0), 0.8)
    if orientation != 'frente':
        attention_score *= 0.6
    if face_size_ratio < 0.16:
        attention_score *= 0.4

    confidence = 0.25
    if eye_tilt <= 0.09:
        confidence += 0.2
    if abs(norm_x - 0.5) < 0.12 and abs(norm_y - 0.5) < 0.12:
        confidence += 0.25
    if 0.16 <= face_size_ratio <= 0.45:
        confidence += 0.2
    if 0.12 < face_center_norm[0] < 0.88:
        confidence += 0.1

    return {
        'orientation': orientation,
        'distracted': distracted,
        'message': message,
        'face_center_norm': face_center_norm,
        'face_size_ratio': face_size_ratio,
        'attention_score': float(min(max(attention_score, 0.0), 1.0)),
        'confidence': float(min(max(confidence, 0.0), 1.0)),
        'eye_centers': [left_eye, right_eye],
    }


def _detect_faces_mediapipe(image_array):
    face_detection, face_mesh = _get_mediapipe_models()
    if face_detection is None or face_mesh is None:
        return []

    image_rgb = image_array.copy()
    results = face_detection.process(image_rgb)
    if not results.detections:
        return []

    mesh_results = face_mesh.process(image_rgb)
    faces = []
    for idx, detection in enumerate(results.detections):
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = image_rgb.shape
        x = int(max(bbox.xmin, 0) * w)
        y = int(max(bbox.ymin, 0) * h)
        fw = int(bbox.width * w)
        fh = int(bbox.height * h)
        if fw <= 0 or fh <= 0:
            continue
        face_box = (x, y, fw, fh)
        landmarks = None
        if mesh_results and mesh_results.multi_face_landmarks:
            landmarks = mesh_results.multi_face_landmarks[0].landmark
        faces.append({
            'face_box': face_box,
            'landmarks': landmarks,
        })
    return faces


def home(request):
    return JsonResponse({
        'message': 'Bienvenido a MetricLab API',
        'status': 'ok',
    })


@api_view(['POST'])
def detect_person(request):
    """
    Detecta personas en una imagen enviada como base64
    Ahora soporta múltiples detecciones y retorna un array
    """
    try:
        # Obtener imagen base64
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'No image provided'}, status=400)
        
        # Decodificar base64
        image_data = image_data.split(',')[-1]  # Remover prefijo data:image/jpeg;base64,
        try:
            image_bytes = base64.b64decode(image_data, validate=True)
            image_pil = Image.open(BytesIO(image_bytes))
        except (ValueError, UnidentifiedImageError):
            return Response({'error': 'Invalid image data'}, status=400)
        
        # Convertir a numpy array y asegurar formato RGB
        image_array = np.array(image_pil)
        if len(image_array.shape) == 2:  # Escala de grises
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
        elif image_array.shape[2] == 4:  # RGBA
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        h, w = image_array.shape[:2]
        detected_people = []
        
        # Intentar detección con MediaPipe primero
        if MEDIAPIPE_AVAILABLE:
            mp_faces = _detect_faces_mediapipe(image_array)
            for face_data in mp_faces:
                x, y, fw, fh = face_data['face_box']
                
                # Procesar con malla si está disponible
                if face_data.get('landmarks'):
                    landmarks = []
                    eye_centers = []
                    for idx in (33, 263):
                        lm = face_data['landmarks'][idx]
                        eye_centers.append((lm.x * w, lm.y * h))
                    for cx, cy in eye_centers:
                        landmarks.append({
                            'x': float((cx - x) / fw) if fw > 0 else 0.5,
                            'y': float((cy - y) / fh) if fh > 0 else 0.5,
                            'visibility': 1.0,
                        })
                    
                    analysis = _compute_mesh_orientation(face_data['landmarks'], face_data['face_box'], (w, h))
                else:
                    landmarks = [{
                        'x': 0.5,
                        'y': 0.5,
                        'visibility': 1.0,
                    }]
                    analysis = {
                        'message': 'Rostro detectado sin análisis completo',
                        'orientation': 'desconocida',
                        'distracted': False,
                        'face_center_norm': (0.5, 0.5),
                        'face_size_ratio': fw / w,
                        'attention_score': 0.5,
                        'confidence': 0.6,
                    }
                
                detected_people.append({
                    'status': 'success',
                    'person_detected': True,
                    'landmarks': landmarks,
                    'message': analysis['message'],
                    'head_orientation': analysis['orientation'],
                    'distracted': analysis['distracted'],
                    'eyes_detected': len(landmarks) - 1,
                    'face_box': {'x': int(x), 'y': int(y), 'w': int(fw), 'h': int(fh)},
                    'face_center': {
                        'x': float(analysis['face_center_norm'][0]),
                        'y': float(analysis['face_center_norm'][1]),
                    },
                    'face_size_ratio': float(analysis['face_size_ratio']),
                    'attention_score': float(analysis['attention_score']),
                    'confidence': float(analysis['confidence']),
                })
        
        # Si no se detectó con MediaPipe, usar OpenCV Cascades
        if not detected_people:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            face_cascade, profile_cascade, eye_cascade, eye_tree_cascade = _load_cascades()
            
            # Detectar caras de frente
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(140, 140))
            if len(faces) == 0:
                # Intentar detectar perfiles
                faces = profile_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(140, 140))
            
            if len(faces) == 0:
                return Response({
                    'status': 'success',
                    'person_detected': False,
                    'landmarks': [],
                    'message': 'No se detectó una cara claramente',
                    'head_orientation': 'desconocida',
                    'distracted': True,
                    'eyes_detected': 0,
                    'face_box': None,
                    'face_center': {'x': 0.0, 'y': 0.0},
                    'face_size_ratio': 0.0,
                    'attention_score': 0.0,
                    'confidence': 0.0,
                })
            
            # Procesar todas las caras detectadas (hasta 5)
            for face in faces[:5]:
                x, y, fw, fh = face
                face_gray = gray[y:y+fh, x:x+fw]
                
                # Detectar ojos
                eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
                if len(eyes) < 2:
                    alt_eyes = eye_tree_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
                    if len(alt_eyes) > len(eyes):
                        eyes = alt_eyes
                
                analysis = _analyze_face_attention(face, eyes, (w, h))
                valid_face, invalid_reason = _validate_face_detection(
                    face, eyes, analysis['face_size_ratio'], analysis['face_center_norm']
                )
                
                if not valid_face:
                    continue
                
                landmarks = []
                for cx, cy in analysis['eye_centers']:
                    landmarks.append({
                        'x': float(cx / fw) if fw > 0 else 0.5,
                        'y': float(cy / fh) if fh > 0 else 0.5,
                        'visibility': 1.0,
                    })
                
                detected_people.append({
                    'status': 'success',
                    'person_detected': True,
                    'landmarks': landmarks,
                    'message': analysis['message'],
                    'head_orientation': analysis['orientation'],
                    'distracted': analysis['distracted'],
                    'eyes_detected': len(eyes),
                    'face_box': {'x': int(x), 'y': int(y), 'w': int(fw), 'h': int(fh)},
                    'face_center': {
                        'x': float(analysis['face_center_norm'][0]),
                        'y': float(analysis['face_center_norm'][1]),
                    },
                    'face_size_ratio': float(analysis['face_size_ratio']),
                    'attention_score': float(analysis['attention_score']),
                    'confidence': float(analysis['confidence']),
                })
        
        # Retornar resultados
        if not detected_people:
            return Response({
                'status': 'success',
                'person_detected': False,
                'message': 'No se detectaron rostros válidos',
            })
        
        # Retornar como array si hay múltiples personas, sino como objeto único
        if len(detected_people) == 1:
            return Response(detected_people[0])
        else:
            return Response(detected_people)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


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
