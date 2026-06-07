"""
Activities - Modelos para registro de actividades y detección de personas
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AttentionEvent(models.Model):
    """
    Registro de eventos de atención/distracción detectados por cámara
    """
    PERSON_DETECTED_CHOICES = [
        ('yes', 'Persona detectada'),
        ('no', 'Sin persona'),
        ('partial', 'Persona parcial'),
    ]
    
    DISTRACTION_CHOICES = [
        ('focused', 'Enfocado'),
        ('distracted', 'Distraído'),
        ('away', 'Ausente'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attention_events')
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Detección de persona
    person_detected = models.CharField(max_length=10, choices=PERSON_DETECTED_CHOICES)
    head_orientation = models.CharField(max_length=50, null=True, blank=True)  # JSON: {yaw, pitch, roll}
    distracted = models.CharField(max_length=20, choices=DISTRACTION_CHOICES)
    
    # Ojos
    eyes_detected = models.BooleanField(default=False)
    left_eye_open = models.BooleanField(null=True)
    right_eye_open = models.BooleanField(null=True)
    
    # Puntuación
    attention_score = models.IntegerField(default=100)  # 0-100
    
    # Metadata
    message = models.CharField(max_length=255, null=True, blank=True)
    frame_number = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp} - {self.attention_score}%"


class EfficiencyMetrics(models.Model):
    """
    Métricas calculadas de eficiencia laboral
    """
    AGGREGATION_CHOICES = [
        ('hourly', 'Cada hora'),
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='efficiency_metrics')
    date = models.DateField()
    aggregation = models.CharField(max_length=10, choices=AGGREGATION_CHOICES)
    
    # Métricas de eficiencia
    total_time = models.IntegerField()  # Segundos
    productive_time = models.IntegerField()  # Segundos
    distracted_time = models.IntegerField()  # Segundos
    away_time = models.IntegerField()  # Segundos
    
    # Puntuaciones
    efficiency_percentage = models.FloatField()  # 0-100
    average_attention_score = models.IntegerField()  # 0-100
    
    # Estadísticas
    events_count = models.IntegerField()
    distraction_count = models.IntegerField()
    away_count = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date', 'aggregation')
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.efficiency_percentage}%"


class SessionTracking(models.Model):
    """
    Sesión de tracking de un usuario (cuando empezó a trabajar/paró)
    """
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('paused', 'En pausa'),
        ('completed', 'Completado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Resumen de sesión
    total_events = models.IntegerField(default=0)
    total_efficiency = models.FloatField(default=0)  # Porcentaje promedio
    
    notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', '-start_time']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.start_time} ({self.status})"
    
    @property
    def duration(self):
        """Duración de la sesión en minutos"""
        end = self.end_time or timezone.now()
        return (end - self.start_time).total_seconds() / 60


class PersonDetection(models.Model):
    """
    Registro de detecciones de personas (pueden ser múltiples en 1 sesión)
    """
    session = models.ForeignKey(SessionTracking, on_delete=models.CASCADE, related_name='detections')
    person_id = models.IntegerField()  # ID de persona en video
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Estadísticas de detección
    frames_total = models.IntegerField(default=0)
    frames_detected = models.IntegerField(default=0)  # Cuántos frames la persona fue detectada
    average_attention = models.IntegerField(default=0)  # 0-100
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['session', 'person_id']),
        ]
    
    def __str__(self):
        return f"Persona {self.person_id} - {self.start_time}"
    
    @property
    def detection_percentage(self):
        """Porcentaje de frames donde fue detectada"""
        if self.frames_total == 0:
            return 0
        return (self.frames_detected / self.frames_total) * 100
