from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/search/', consumers.SearchConsumer.as_asgi()),
]