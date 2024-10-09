from rest_framework import serializers
from ..models import Guest
from phonenumber_field.serializerfields import PhoneNumberField

class GuestSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = Guest
        fields = '__all__'

    def validate_phone(self, value):
        """
        Check that the phone number is valid.
        """
        if not value.is_valid():
            raise serializers.ValidationError("Invalid phone number")
        return value.as_e164