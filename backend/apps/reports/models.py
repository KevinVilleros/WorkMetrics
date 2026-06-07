from django.db import models


class AttentionEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    person_detected = models.BooleanField(default=False)
    head_orientation = models.CharField(max_length=32, default='desconocida')
    distracted = models.BooleanField(default=True)
    eyes_detected = models.IntegerField(default=0)
    message = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp.isoformat()} - {'Atenta' if not self.distracted else 'Distraída'}"
