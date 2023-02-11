from django.db import models
from django.conf import settings



class EventCategory(models.Model):
    name = models.CharField(verbose_name="name", max_length=255)
    description = models.TextField(verbose_name="description")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,  verbose_name="Creator")
    created_at = models.DateTimeField(verbose_name="Created at",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", null=True)
    is_deleted = models.BooleanField(verbose_name="is_deleted", default=False)


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name="name")
    created_at=models.DateTimeField(verbose_name="Created at",auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="is_deleted", default=False)

class Event(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    description = models.TextField(verbose_name="Description")
    start = models.DateTimeField(verbose_name="Start")
    end = models.DateTimeField(verbose_name="End")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,  verbose_name="Creator")
    created_at = models.DateTimeField(verbose_name="Created at",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", null=True, default=None)
    is_deleted = models.BooleanField(verbose_name="is_deleted", default=False)
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, verbose_name="Event category")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Location")

    def __str__(self):
        return self.name + "  {}".format(self.created_at)

class Record(models.Model):
    in_time = models.DateTimeField(verbose_name="IN", auto_now_add=True)
    out_time = models.DateTimeField(verbose_name="OUT", null=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Event")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name="User")
    record_type = models.PositiveSmallIntegerField(verbose_name="0=RFID 1=BT", default=0)
    


    def __str__(self) -> str:
        return super().__str__()