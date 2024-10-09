from rest_framework import serializers
from ..models import RSVP

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = ['wedding_selection', 'is_attending', 'additional_notes']

    def create(self, validated_data):
        guest = self.context['guest']
        rsvp, created = RSVP.objects.update_or_create(
            guest=guest,
            defaults=validated_data
        )
        return rsvp