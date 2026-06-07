"""
Activities - Serializers para DRF
"""
from rest_framework import serializers
from .models import AttentionEvent, EfficiencyMetrics, SessionTracking, PersonDetection


class AttentionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttentionEvent
        fields = [
            'id', 'timestamp', 'person_detected', 'head_orientation',
            'distracted', 'eyes_detected', 'left_eye_open', 'right_eye_open',
            'attention_score', 'message', 'frame_number'
        ]
        read_only_fields = ['id', 'timestamp']


class EfficiencyMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EfficiencyMetrics
        fields = [
            'id', 'date', 'aggregation', 'total_time', 'productive_time',
            'distracted_time', 'away_time', 'efficiency_percentage',
            'average_attention_score', 'events_count', 'distraction_count',
            'away_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PersonDetectionSerializer(serializers.ModelSerializer):
    detection_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = PersonDetection
        fields = [
            'id', 'person_id', 'start_time', 'end_time', 'frames_total',
            'frames_detected', 'average_attention', 'detection_percentage'
        ]
        read_only_fields = ['id']
    
    def get_detection_percentage(self, obj):
        return obj.detection_percentage


class SessionTrackingSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    detections = PersonDetectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SessionTracking
        fields = [
            'id', 'start_time', 'end_time', 'status', 'total_events',
            'total_efficiency', 'notes', 'duration', 'detections'
        ]
        read_only_fields = ['id', 'start_time', 'created_at', 'updated_at']
    
    def get_duration(self, obj):
        return obj.duration
