from rest_framework import serializers
from django.utils import timezone
from ..models import Memories

class MemoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memories
        fields = ['memory_text', 'date_shared', ...] # include other fields
        extra_kwargs = {'date_shared': {'required': False}}

    def create(self, validated_data):
        if 'date_shared' not in validated_data:
            validated_data['date_shared'] = timezone.now().date()
        return super().create(validated_data)