from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from guests.models import Guest
from .models import RSVP
from .serializers.common import RSVPSerializer

class RSVPView(APIView):
    def get(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        rsvp = RSVP.objects.filter(guest=guest).first()
        if rsvp:
            serializer = RSVPSerializer(rsvp)
            return Response(serializer.data)
        else:
            return Response({"message": "RSVP not found for this guest"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        serializer = RSVPSerializer(data=request.data, context={'guest': guest})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)