from rest_framework import serializers
from ..models import Memories

class MemoriesSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.name', read_only=True)

    class Meta:
        model = Memories
        fields = ['id', 'guest', 'guest_name', 'memory_text', 'date_shared']
        read_only_fields = ['date_shared']

    def create(self, validated_data):
        memory = Memories.objects.create(**validated_data)
        return memory