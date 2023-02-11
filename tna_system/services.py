import dataclasses
import datetime
from user.services import UserDataClass
from . import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Event,Location, EventCategory

@dataclasses.dataclass
class EventDataClass:
    name : str
    description: str
    event_category : str 
    location : str
    start : datetime.datetime = None
    end : datetime.datetime = None
    created_by : UserDataClass = None
    created_at : datetime.datetime = None
    updated_at : datetime.datetime = None
    id : int = None
    is_deleted : bool = False
    


    @classmethod
    def from_instance(cls, event_model: "Event")-> "EventDataClass":
        return cls(
            name=event_model.name,
            description= event_model.description,
            start = event_model.start,
            end = event_model.end,
            created_by = event_model.created_by,
            created_at = event_model.created_at,
            updated_at = event_model.updated_at,
            id = event_model.id,
            event_category = event_model.event_category.name,
            location = event_model.location.name, 
            is_deleted = event_model.is_deleted


            
        )


def create_event(user, event:"EventDataClass")->"EventDataClass":
    instance= models.Event.objects.create(
        name=event.name,
        created_by=user,
        description=event.description,
        start = event.start,
        end = event.end,
        created_at = event.created_at,
        updated_at = event.updated_at, 
        location = models.Location.objects.filter(name=event.location).first(),
        event_category = models.EventCategory.objects.filter(name=event.event_category).first(),
        is_deleted = event.is_deleted
    )

    return EventDataClass.from_instance(event_model=instance)

@dataclasses.dataclass
class LocationDataClass:
    name : str
    is_deleted : bool = False
    id : int = None
    #metoda pretvara instancu klase Location u Dataclass
    @classmethod
    def from_instance(cls, location : "Location") -> "LocationDataClass":
        return cls(
            name = location.name,
            is_deleted = location.is_deleted,
            id = location.id
        )

def create_location(location_dc:"LocationDataClass")->"LocationDataClass":
    instance = models.Location.objects.create(
        name= location_dc.name,)

    return LocationDataClass.from_instance(location=instance)


    
@dataclasses.dataclass
class EventCategoryDataClass:
    name: str
    description : str
    created_by : UserDataClass = None
    created_at : datetime.datetime = None
    updated_at : datetime.datetime = None
    is_deleted : datetime.datetime = None
    id : int = None
    @classmethod
    def from_instance(cls, event_category : "EventCategory")->"EventCategoryDataClass":
        return cls(
            name = event_category.name,
            description = event_category.description,
            created_by = event_category.created_by,
            created_at = event_category.created_at,
            updated_at = event_category.updated_at,
            is_deleted = event_category.is_deleted,
            id = event_category.id 
        )

def create_category(user, category:"EventCategoryDataClass")->"EventCategoryDataClass":
    instance = models.EventCategory.objects.create(
        name=category.name,
        description = category.description,
        created_by = user, 
        is_deleted = False

    )
    return EventCategoryDataClass.from_instance(instance)