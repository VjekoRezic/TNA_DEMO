from django.db import models
from user.models import User
from django.conf import settings


class Event(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    description = models.TextField(verbose_name="Description")
    start = models.DateTimeField(verbose_name="Start")
    end = models.DateTimeField(verbose_name="End")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,  verbose_name="Creator")
    created_at = models.DateTimeField(verbose_name="Created at",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", null=True)


    def __str__(self):
        return self.name + "  {}".format(self.created_at)




class Record(models.Model):
    in_time = models.DateTimeField(verbose_name="IN", auto_now_add=True)
    out_time = models.DateTimeField(verbose_name="OUT", null=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Event")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name="User")
    record_type = models.PositiveSmallIntegerField(verbose_name="0=RFID 1=BT")

    def __str__(self) -> str:
        return super().__str__()


    