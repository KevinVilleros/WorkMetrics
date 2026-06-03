from django.urls import path
from .views import compliance_report, record_attention_event

urlpatterns = [
    path('compliance/', compliance_report, name='compliance-report'),
    path('attention/', record_attention_event, name='attention-event'),
]
