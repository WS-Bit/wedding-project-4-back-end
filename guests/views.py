from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Guest
from .serializers.common import GuestSerializer

class GuestView(APIView):
    def get(self, request):
        guest_id = request.session.get('guest_id')
        if guest_id:
            try:
                guest = Guest.objects.get(id=guest_id)
                serializer = GuestSerializer(guest)
                return Response(serializer.data)
            except Guest.DoesNotExist:
                return Response({"message": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "No guest registered for this session"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        guest_to_add = GuestSerializer(data=request.data)
        try:
            if guest_to_add.is_valid():
                guest = guest_to_add.save()
                request.session['guest_id'] = guest.id
                return Response(guest_to_add.data, status=status.HTTP_201_CREATED)
            return Response(guest_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)