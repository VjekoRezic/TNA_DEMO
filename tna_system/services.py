import dataclasses
import datetime
from user.services import UserDataClass
from . import models
from typing import TYPE_CHECKING
from django.utils import timezone

if TYPE_CHECKING:
    from models import Event,Location, EventCategory, Record

@dataclasses.dataclass
class EventDataClass:
    name : str
    description: str
    event_category : id 
    location : id
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
            event_category = event_model.event_category.id,
            location = event_model.location.id, 
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
        location = models.Location.objects.filter(id=event.location).first(),
        event_category = models.EventCategory.objects.filter(id=event.event_category).first(),
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


def check_if_availible(event):

    scheduled_events = models.Event.objects.filter(start__date = event.start.date() , location__id=event.location).all()
    for obj in scheduled_events:
        if obj.start <= event.start < obj.end <= event.end :
            return False
        
        if obj.start<=event.start<=event.end<=obj.end:
            return False
        if event.start <= obj.start < obj.end <= event.end:
            return False
        if event.start <= obj.start< event.end <= obj.end:
            return False

    
    return True

@dataclasses.dataclass
class RecordDataClass:
    event : int
    in_time : datetime.datetime = None
    user : UserDataClass = None
    out_time : datetime.datetime = None
    id : int = None
    @classmethod
    def from_instance(cls, record: "Record")-> "RecordDataClass":
        return cls(
            event = record.event.name,
            in_time = record.in_time,
            user = record.user,
            out_time = record.out_time,
            id = record.id
        )


def create_record_in(user, event)-> "RecordDataClass":
        instance= models.Record.objects.create(
            event = models.Event.objects.filter(id=event.id).first(),
            user=user
        )

        return RecordDataClass(instance)

def create_record_out(user, event):
    instance = models.Record.objects.filter(user=user, event=event).first()
    instance.out_time = timezone.now()
    instance.save()
    return RecordDataClass(instance)

def get_categories_and_percentage(backoffice_user, student_id ):
    filter_categories = models.Record.objects.values_list('event__event_category').filter(event__created_by=backoffice_user, user__id=student_id).distinct()
    categories=models.EventCategory.objects.filter(id__in=filter_categories).all()
    records = models.Record.objects.filter(event__event_category__id__in=filter_categories, user__id=student_id).all()
    events = models.Event.objects.filter(event_category__id__in=filter_categories)
    resp = []
    for cat in categories:
        numEvents= events.filter(event_category=cat).count()
        numRecords = records.filter(event__event_category=cat).count()
        percentage = int((numRecords/numEvents)*100)
        temp={
            "category_id":cat.id,
            "category":cat.name,
            "percentage":percentage
        }
        resp.append(temp)

    return resp

        




