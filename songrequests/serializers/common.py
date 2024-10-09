from rest_framework import serializers
from ..models import SongRequest

class SongRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongRequest
        fields = ['song_title', 'artist']

    def create(self, validated_data):
        guest = self.context['guest']
        song_request, created = SongRequest.objects.update_or_create(
            guest=guest,
            defaults=validated_data
        )
        return song_request