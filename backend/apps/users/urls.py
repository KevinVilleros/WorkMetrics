from django.urls import path
from .views import home, detect_person

urlpatterns = [
    path('', home, name='api-root'),
    path('detect/', detect_person, name='detect-person'),
]
