from rest_framework import serializers
from .models import Script

class ScriptSerializer(serializers.ModelSerializer):
    """
    Serializer for the Script model.

    This serializer converts Script model instances into JSON format for the API
    and validates data for incoming create/update requests.

    The `is_free` property is included as a read-only field to be exposed in the API.
    """
    is_free = serializers.BooleanField(read_only=True)
    video_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Script
        fields = [
            'id',
            'title',
            'description',
            'price',
            'is_free',
            'video_url',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'is_free', 'created_at', 'updated_at')
