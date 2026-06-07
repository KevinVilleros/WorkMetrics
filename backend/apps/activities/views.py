"""
Activities - Vistas/API para detección de personas y análisis de eficiencia
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Avg, Q
from datetime import timedelta

from .models import AttentionEvent, EfficiencyMetrics, SessionTracking, PersonDetection
from .serializers import (
    AttentionEventSerializer, EfficiencyMetricsSerializer, 
    SessionTrackingSerializer, PersonDetectionSerializer
)


class AttentionEventViewSet(viewsets.ModelViewSet):
    """
    API para eventos de atención/distracción detectados
    """
    serializer_class = AttentionEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AttentionEvent.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Eventos de hoy"""
        today = timezone.now().date()
        events = self.get_queryset().filter(timestamp__date=today)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def this_week(self, request):
        """Eventos de esta semana"""
        today = timezone.now()
        week_ago = today - timedelta(days=7)
        events = self.get_queryset().filter(timestamp__gte=week_ago)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas de atención"""
        today = timezone.now().date()
        events = self.get_queryset().filter(timestamp__date=today)
        
        stats = {
            'total_events': events.count(),
            'average_attention': events.aggregate(Avg('attention_score'))['attention_score__avg'] or 0,
            'distracted_events': events.filter(distracted='distracted').count(),
            'away_events': events.filter(distracted='away').count(),
            'focused_events': events.filter(distracted='focused').count(),
        }
        return Response(stats)


class EfficiencyMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para métricas de eficiencia (calculadas)
    """
    serializer_class = EfficiencyMetricsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EfficiencyMetrics.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Eficiencia de hoy"""
        today = timezone.now().date()
        metric = self.get_queryset().filter(
            date=today,
            aggregation='daily'
        ).first()
        
        if metric:
            serializer = self.get_serializer(metric)
            return Response(serializer.data)
        
        return Response({
            'error': 'No hay datos de hoy',
            'efficiency_percentage': 0,
            'average_attention_score': 0
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def this_week(self, request):
        """Eficiencia semanal"""
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        metrics = self.get_queryset().filter(
            date__gte=week_ago,
            date__lte=today,
            aggregation='daily'
        ).order_by('date')
        
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)


class SessionTrackingViewSet(viewsets.ModelViewSet):
    """
    API para sesiones de tracking
    """
    serializer_class = SessionTrackingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SessionTracking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail='pk', methods=['post'])
    def end_session(self, request, pk=None):
        """Terminar sesión"""
        session = self.get_object()
        session.end_time = timezone.now()
        session.status = 'completed'
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail='pk', methods=['post'])
    def pause(self, request, pk=None):
        """Pausar sesión"""
        session = self.get_object()
        session.status = 'paused'
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail='pk', methods=['post'])
    def resume(self, request, pk=None):
        """Reanudar sesión"""
        session = self.get_object()
        session.status = 'active'
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Sesión activa del usuario"""
        session = self.get_queryset().filter(
            status__in=['active', 'paused']
        ).first()
        
        if session:
            serializer = self.get_serializer(session)
            return Response(serializer.data)
        
        return Response({
            'error': 'No hay sesión activa'
        }, status=status.HTTP_404_NOT_FOUND)


class PersonDetectionViewSet(viewsets.ModelViewSet):
    """
    API para detecciones de personas en sesiones
    """
    serializer_class = PersonDetectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PersonDetection.objects.filter(
            session__user=self.request.user
        )
