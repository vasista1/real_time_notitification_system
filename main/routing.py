from django.urls import path
from main.consumers import NotificationSystem

websocket_urlpatterns = [
    path('ws/notify/<str:group>/',NotificationSystem.as_asgi())
]