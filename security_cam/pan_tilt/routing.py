from django.urls import path
from .consumers import WSConsumer

ws_urlpatterns = [
    path('ws/pan_tilt/', WSConsumer.as_asgi())
]