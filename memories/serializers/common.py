from rest_framework import serializers
from django.utils import timezone
from ..models import Memories
from guests.models import Guest

class MemoriesSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.name', read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), source='guest')
    date_shared = serializers.DateField(default=timezone.now().date())

    class Meta:
        model = Memories
        fields = ['id', 'guest_id', 'guest_name', 'memory_text', 'date_shared']
        extra_kwargs = {'date_shared': {'required': False}}

    def create(self, validated_data):
        if 'date_shared' not in validated_data:
            validated_data['date_shared'] = timezone.now().date()
        return super().create(validated_data)

    def validate_memory_text(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Memory text must be 100 characters or less.")
        return value