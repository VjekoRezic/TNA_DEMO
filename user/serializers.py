from rest_framework import serializers
from . import services

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.CharField()
    password=serializers.CharField(write_only=True)
    card_id=serializers.CharField(required=False)
    is_staff=serializers.BooleanField(default=False, required=False)
    is_superuser=serializers.BooleanField(default=False, required=False)
    is_deleted=serializers.BooleanField(default=False, required=False)




    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.UserDataClass(**data)



class UserBasicSerializer(serializers.Serializer):
    
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    
    