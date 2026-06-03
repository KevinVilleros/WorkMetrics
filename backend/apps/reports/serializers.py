from rest_framework import serializers
from .models import AttentionEvent


class AttentionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttentionEvent
        fields = '__all__'
