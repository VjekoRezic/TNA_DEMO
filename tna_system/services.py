import dataclasses
import datetime
from user.services import UserDataClass
from . import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Event

@dataclasses.dataclass
class EventDataClass:
    name : str
    description: str
    start : datetime.datetime = None
    end : datetime.datetime = None
    created_by : UserDataClass = None
    created_at : datetime.datetime = None
    updated_at : datetime.datetime = None
    id : int = None

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
            
        )


def create_event(user, event:"EventDataClass")->"EventDataClass":
    instance= models.Event.objects.create(
        name=event.name,
        created_by=user,
        description=event.description,
        start = event.start,
        end = event.end,
        created_at = event.created_at,
        updated_at = event.updated_at
    )

    return EventDataClass.from_instance(event_model=instance)
