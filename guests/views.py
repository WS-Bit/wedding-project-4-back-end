from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import redirect

from .models import Guest
from .serializers.common import GuestSerializer

class GuestView(APIView):
    def post(self, request):
        guest_to_add = GuestSerializer(data=request.data)
        try:
            if guest_to_add.is_valid():
                guest_to_add.save()
                return redirect('home')  # Redirect to home page after successful registration
            return Response(guest_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)