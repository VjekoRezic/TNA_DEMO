from rest_framework import serializers
from user.serializers import UserSerializer, UserBasicSerializer
from .services import EventDataClass, LocationDataClass, EventCategoryDataClass, RecordDataClass


class EventCategoryBasicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    def to_internal_value(self, data):
        data=super().to_internal_value(data)
        return EventCategoryDataClass(**data)
    


class EventCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    def to_internal_value(self, data):
        data=super().to_internal_value(data)
        return EventCategoryDataClass(**data)

class LocationSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    is_deleted = serializers.BooleanField(required=False)
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return LocationDataClass(**data)

class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    event_category = EventCategorySerializer()
    location = LocationSerializer()
    


    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return EventDataClass(**data)

class EventListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    created_by = UserBasicSerializer(read_only=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    event_category = EventCategoryBasicSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

class EventPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    created_by = UserBasicSerializer(read_only=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    event_category = serializers.IntegerField()
    location = serializers.IntegerField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return EventDataClass(**data)

class RecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    in_time = serializers.DateTimeField(required=False)
    out_time = serializers.DateTimeField(required=False)
    event = EventSerializer(read_only=True)
    user = UserBasicSerializer(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return RecordDataClass(**data)

class RecordPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    in_time = serializers.DateTimeField(required=False)
    out_time = serializers.DateTimeField(required=False)
    event = serializers.CharField()
    user = UserBasicSerializer(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return RecordDataClass(**data)

class RecordBasicSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True),
    in_time = serializers.DateTimeField(required=False)
    out_time = serializers.DateTimeField(required=False)
    user = UserBasicSerializer(read_only=True)
