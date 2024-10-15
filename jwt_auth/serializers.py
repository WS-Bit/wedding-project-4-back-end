# # jwt_auth/serializers.py
# from django.contrib.auth import authenticate
# from rest_framework import serializers

# class SignInSerializer(serializers.Serializer):
#     password = serializers.CharField()

#     def validate(self, attrs):
#         user = authenticate(**attrs)
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         attrs['user'] = user
#         return attrs
