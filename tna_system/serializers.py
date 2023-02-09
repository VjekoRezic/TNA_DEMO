from rest_framework import serializers
from user.serializers import UserSerializer, UserBasicSerializer
from .services import EventDataClass


class EventCategoryBasicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    


class EventCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    is_deleted = serializers.BooleanField(required=False)

class LocationSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    is_deleted = serializers.BooleanField(required=False)

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
    event_category = serializers.CharField()
    location = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return EventDataClass(**data)