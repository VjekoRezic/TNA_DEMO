from django.urls import path
from . import apis

urlpatterns = [
    path("event/", apis.EventController.as_view(), name="event"),
    
]