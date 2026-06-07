"""
Modelo para almacenar eventos de detección y tracking de personas
"""
from django.db import models
from django.utils import timezone


class PersonDetectionEvent(models.Model):
    """Registro de eventos de detección de personas"""
    
    ORIENTATION_CHOICES = [
        ('frente', 'Frente'),
        ('izquierda', 'Izquierda'),
        ('derecha', 'Derecha'),
        ('arriba', 'Arriba'),
        ('abajo', 'Abajo'),
        ('inclinada', 'Inclinada'),
        ('desconocida', 'Desconocida'),
    ]
    
    # Identificación
    person_id = models.IntegerField(default=0, help_text="ID único de la persona rastreada")
    session_id = models.CharField(max_length=100, null=True, blank=True, help_text="Sesión de tracking")
    
    # Detección
    person_detected = models.BooleanField(default=False)
    head_orientation = models.CharField(max_length=20, choices=ORIENTATION_CHOICES, default='desconocida')
    distracted = models.BooleanField(default=False)
    
    # Puntuaciones
    attention_score = models.FloatField(default=0.0, help_text="Score de atención (0-1)")
    confidence = models.FloatField(default=0.0, help_text="Confianza de la detección (0-1)")
    
    # Datos de rostro
    face_box_x = models.IntegerField(default=0)
    face_box_y = models.IntegerField(default=0)
    face_box_w = models.IntegerField(default=0)
    face_box_h = models.IntegerField(default=0)
    face_size_ratio = models.FloatField(default=0.0)
    
    # Características
    eyes_detected = models.IntegerField(default=0)
    face_center_x = models.FloatField(default=0.0)
    face_center_y = models.FloatField(default=0.0)
    
    # Metadata
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['person_id', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Detección Persona #{self.person_id} - {self.timestamp}"


class PersonTrackingSession(models.Model):
    """Sesión de tracking de una persona"""
    
    person_id = models.IntegerField(unique=True)
    session_id = models.CharField(max_length=100, unique=True)
    
    # Estadísticas
    total_frames = models.IntegerField(default=0)
    total_distracted_frames = models.IntegerField(default=0)
    average_attention_score = models.FloatField(default=0.0)
    max_attention_score = models.FloatField(default=0.0)
    min_attention_score = models.FloatField(default=0.0)
    
    # Temporal
    started_at = models.DateTimeField(auto_now_add=True)
    last_detected_at = models.DateTimeField(auto_now=True)
    duration_seconds = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['person_id']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"Sesión Persona #{self.person_id} - {self.started_at}"
    
    def update_statistics(self):
        """Actualiza las estadísticas basadas en los eventos"""
        events = PersonDetectionEvent.objects.filter(session_id=self.session_id)
        
        self.total_frames = events.count()
        self.total_distracted_frames = events.filter(distracted=True).count()
        
        if self.total_frames > 0:
            scores = list(events.values_list('attention_score', flat=True))
            self.average_attention_score = sum(scores) / len(scores)
            self.max_attention_score = max(scores)
            self.min_attention_score = min(scores)
        
        if self.started_at and self.last_detected_at:
            self.duration_seconds = int((self.last_detected_at - self.started_at).total_seconds())
        
        self.save()
