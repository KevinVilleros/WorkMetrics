from django.test import SimpleTestCase


class HealthCheckTests(SimpleTestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})


class DetectPersonTests(SimpleTestCase):
    def test_detect_person_rejects_invalid_image_payload(self):
        response = self.client.post(
            '/api/detect/',
            {'image': 'data:image/jpeg;base64,not-valid-base64'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid image data'})
