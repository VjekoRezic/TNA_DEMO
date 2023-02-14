from django.urls import path
from . import apis

urlpatterns = [
    path("event/", apis.EventController.as_view(), name="event"),
    path("event/<int:event_id>/", apis.EventDetails.as_view(), name="event details"),
    path("location/", apis.LocationController.as_view(), name="location"),
    path("categories/", apis.EventCategoryController.as_view(), name="event categories"),
    path("record/", apis.RecordController.as_view(), name="record"),
    path("users/<int:user_id>/", apis.UserRecords.as_view(), name="user records"),
    

    
    
]