from django.test import TestCase

from .models import AttentionEvent


class ComplianceReportTests(TestCase):
    def test_empty_report_returns_no_data_summary(self):
        response = self.client.get('/api/reports/compliance/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_checks'], 0)
        self.assertEqual(data['compliance_level'], 'Sin datos')
        self.assertEqual(data['recent_events'], [])

    def test_report_counts_recent_attention_events(self):
        AttentionEvent.objects.create(
            person_detected=True,
            distracted=False,
            head_orientation='frente',
            eyes_detected=2,
            message='Atenta',
        )
        AttentionEvent.objects.create(
            person_detected=True,
            distracted=True,
            head_orientation='izquierda',
            eyes_detected=1,
            message='Distraida',
        )
        AttentionEvent.objects.create(
            person_detected=False,
            distracted=True,
            head_orientation='desconocida',
            eyes_detected=0,
            message='Sin rostro',
        )

        response = self.client.get('/api/reports/compliance/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_checks'], 3)
        self.assertEqual(data['attentive_checks'], 1)
        self.assertEqual(data['distracted_checks'], 1)
        self.assertEqual(data['no_face_checks'], 1)
        self.assertEqual(data['compliance_score'], 33)
