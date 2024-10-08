from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Guest
from .serializers.common import GuestSerializer

# Create your views here.

class GuestView(APIView):
    def post(self, request):
            print(request.data)
            print(request.user.id)
            guest_to_add = GuestSerializer(data=request.data)
            try:
                guest_to_add.is_valid()
                guest_to_add.save()
                return Response(guest_to_add.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error")
                return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
