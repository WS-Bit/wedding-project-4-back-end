from rest_framework import serializers
from ..models import RSVP
from guests.models import Guest

class RSVPSerializer(serializers.ModelSerializer):
    guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), required=False)

    class Meta:
        model = RSVP
        fields = ['id', 'guest', 'wedding_selection', 'is_attending', 'additional_notes']

    def create(self, validated_data):
        guest = self.context['guest']
        validated_data['guest'] = guest
        return super().create(validated_data)

    def update(self, instance, validated_data):
        guest = self.context['guest']
        validated_data['guest'] = guest
        return super().update(instance, validated_data)