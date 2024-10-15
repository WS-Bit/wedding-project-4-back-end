from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from guests.models import Guest
from .models import RSVP
from .serializers.common import RSVPSerializer

class RSVPView(APIView):
    def post(self, request):
        guest_id = request.data.get('guest')
        if not guest_id:
            return Response({"error": "Guest ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            return Response({"error": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if RSVP already exists for this guest
        existing_rsvp = RSVP.objects.filter(guest=guest).first()
        if existing_rsvp:
            serializer = RSVPSerializer(existing_rsvp, data=request.data, partial=True, context={'guest': guest})
        else:
            serializer = RSVPSerializer(data=request.data, context={'guest': guest})

        if serializer.is_valid():
            serializer.save()  # We don't need to pass guest here anymore
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        guest_id = request.query_params.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            return Response({"error": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)

        rsvp = RSVP.objects.filter(guest=guest).first()
        if rsvp:
            serializer = RSVPSerializer(rsvp)
            return Response(serializer.data)
        else:
            return Response({"message": "RSVP not found for this guest"}, status=status.HTTP_404_NOT_FOUND)