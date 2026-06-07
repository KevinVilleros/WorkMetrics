from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AttentionEvent
from .serializers import AttentionEventSerializer


def _build_report(events):
    total = events.count()
    attentive = events.filter(person_detected=True, distracted=False).count()
    distracted = events.filter(person_detected=True, distracted=True).count()
    no_face = events.filter(person_detected=False).count()
    score = int((attentive / total) * 100) if total else 0
    if score >= 80:
        level = 'Alto'
        summary = 'El trabajador muestra un nivel de atención alto y está cumpliendo con su actividad.'
    elif score >= 50:
        level = 'Medio'
        summary = 'El trabajador presenta atención moderada, es recomendable revisar posibles distracciones.'
    else:
        level = 'Bajo'
        summary = 'El trabajador tiene bajo nivel de atención y puede no estar cumpliendo correctamente con la tarea.'

    orientation_breakdown = {}
    recent_events = []
    for event in events.order_by('-timestamp')[:10]:
        orientation_breakdown[event.head_orientation] = orientation_breakdown.get(event.head_orientation, 0) + 1
        recent_events.append({
            'timestamp': event.timestamp.isoformat(),
            'person_detected': event.person_detected,
            'head_orientation': event.head_orientation,
            'distracted': event.distracted,
            'eyes_detected': event.eyes_detected,
            'message': event.message,
        })

    return {
        'status': 'success',
        'total_checks': total,
        'attentive_checks': attentive,
        'distracted_checks': distracted,
        'no_face_checks': no_face,
        'compliance_score': score,
        'compliance_level': level,
        'summary': summary,
        'orientation_breakdown': orientation_breakdown,
        'recent_events': recent_events,
    }


@api_view(['GET'])
def compliance_report(request):
    cutoff = timezone.now() - timedelta(hours=2)
    events = AttentionEvent.objects.filter(timestamp__gte=cutoff)
    if events.count() == 0:
        return Response({
            'status': 'success',
            'total_checks': 0,
            'attentive_checks': 0,
            'distracted_checks': 0,
            'no_face_checks': 0,
            'compliance_score': 0,
            'compliance_level': 'Sin datos',
            'summary': 'Aún no hay suficientes registros para generar un informe.',
            'orientation_breakdown': {},
            'recent_events': [],
        })

    return Response(_build_report(events))


@api_view(['POST'])
def record_attention_event(request):
    serializer = AttentionEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'event': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
