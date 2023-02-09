from django.contrib import admin
from .models import Event, Record, EventCategory, Location
# Register your models here.
admin.site.register(Event)
admin.site.register(Record)
admin.site.register(EventCategory)
admin.site.register(Location)