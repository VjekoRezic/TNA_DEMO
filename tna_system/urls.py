from django.urls import path
from . import apis

urlpatterns = [
    path("event/", apis.EventController.as_view(), name="event"),
    path("location/", apis.LocationController.as_view(), name="location"),
    path("categories/", apis.EventCategoryController.as_view(), name="event categories"),
    
    
]